#!/usr/bin/env python3
"""
Diagnostic complet des problèmes de documents
"""

import requests
import sqlite3
import tempfile
import os

BASE_URL = "http://localhost:5000"

def check_database_structure():
    """Vérifier la structure de la base de données"""
    print("🔍 VÉRIFICATION STRUCTURE BASE")
    print("=" * 50)
    
    try:
        conn = sqlite3.connect('instance/secretaire_medicale.db')
        cursor = conn.cursor()
        
        # Vérifier la table documents_medicaux
        cursor.execute("PRAGMA table_info(documents_medicaux)")
        columns = cursor.fetchall()
        
        print(f"📋 Structure table documents_medicaux ({len(columns)} colonnes):")
        column_names = []
        for col in columns:
            column_names.append(col[1])
            print(f"  - {col[1]} ({col[2]}) {'NOT NULL' if col[3] else 'NULL'}")
        
        # Vérifier les colonnes requises
        required_columns = ['id', 'patient_id', 'type_document', 'titre', 'contenu', 'fichier_path', 'date_creation', 'is_active']
        missing_columns = [col for col in required_columns if col not in column_names]
        
        if missing_columns:
            print(f"❌ Colonnes manquantes: {missing_columns}")
            return False
        else:
            print("✅ Toutes les colonnes requises sont présentes")
        
        # Compter les documents
        cursor.execute("SELECT COUNT(*) FROM documents_medicaux")
        count = cursor.fetchone()[0]
        print(f"📊 {count} documents en base")
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Erreur: {str(e)}")
        return False

def test_model_to_dict():
    """Tester la méthode to_dict du modèle"""
    print("\n🔍 TEST MODÈLE TO_DICT")
    print("=" * 50)
    
    try:
        from models import DocumentMedical
        from app import create_app
        
        app = create_app()
        
        with app.app_context():
            # Récupérer un document de la base
            doc = DocumentMedical.query.first()
            
            if doc:
                print(f"📋 Test avec document ID: {doc.id}")
                print(f"📄 Titre: {doc.titre}")
                
                try:
                    doc_dict = doc.to_dict()
                    print("✅ Conversion to_dict() réussie")
                    
                    # Afficher les clés principales
                    keys = ['id', 'titre', 'type_document', 'fichier_path', 'date_creation']
                    for key in keys:
                        value = doc_dict.get(key, 'MANQUANT')
                        print(f"  {key}: {value}")
                    
                    if 'error' in doc_dict:
                        print(f"⚠️  Erreur dans to_dict: {doc_dict['error']}")
                        return False
                    
                    return True
                    
                except Exception as e:
                    print(f"❌ Erreur to_dict(): {str(e)}")
                    import traceback
                    traceback.print_exc()
                    return False
            else:
                print("⚠️  Aucun document en base pour tester")
                return True  # Pas d'erreur, juste pas de données
                
    except Exception as e:
        print(f"❌ Erreur: {str(e)}")
        return False

def get_auth_token():
    """Obtenir un token d'authentification"""
    login_data = {
        "email": "test@example.com",
        "password": "test123"
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/auth/login",
            json=login_data,
            headers={'Content-Type': 'application/json'},
            timeout=10
        )
        
        if response.status_code == 200:
            token = response.json().get('access_token')
            print("✅ Token obtenu")
            return token
        else:
            print(f"❌ Échec connexion: {response.status_code}")
            return None
            
    except Exception as e:
        print(f"❌ Erreur connexion: {str(e)}")
        return None

def test_get_documents_api(token):
    """Tester l'API GET documents"""
    print("\n🔍 TEST API GET DOCUMENTS")
    print("=" * 50)
    
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    
    try:
        response = requests.get(
            f"{BASE_URL}/api/documents/",
            headers=headers,
            timeout=10
        )
        
        print(f"📥 Status: {response.status_code}")
        
        if response.status_code == 200:
            try:
                data = response.json()
                documents = data.get('documents', [])
                
                print(f"✅ {len(documents)} documents récupérés")
                
                for i, doc in enumerate(documents[:3]):
                    print(f"  {i+1}. {doc.get('nom_document', 'Sans nom')} ({doc.get('type_document', 'Sans type')})")
                    print(f"     ID: {doc.get('id')}")
                    print(f"     Fichier: {doc.get('nom_fichier', 'Aucun')}")
                    
                    # Vérifier s'il y a des erreurs dans la conversion
                    if 'error' in doc:
                        print(f"     ⚠️  Erreur: {doc['error']}")
                
                return True
                
            except Exception as json_error:
                print(f"❌ Erreur parsing JSON: {str(json_error)}")
                print(f"📄 Réponse brute: {response.text[:500]}...")
                return False
                
        elif response.status_code == 422:
            print("❌ Erreur 422 - Problème de validation")
            try:
                error_data = response.json()
                print(f"💬 Erreur: {error_data}")
            except:
                print(f"💬 Réponse: {response.text}")
            return False
        else:
            print(f"❌ Erreur HTTP: {response.status_code}")
            try:
                error_data = response.json()
                print(f"💬 Erreur: {error_data}")
            except:
                print(f"💬 Réponse: {response.text}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Flask non accessible - Démarrez avec: python app.py")
        return False
    except Exception as e:
        print(f"❌ Erreur: {str(e)}")
        return False

def test_upload_documents_api(token):
    """Tester l'API POST documents"""
    print("\n🔍 TEST API POST DOCUMENTS")
    print("=" * 50)
    
    headers = {
        'Authorization': f'Bearer {token}'
    }
    
    # Créer un fichier de test
    content = "Document de test pour diagnostic complet"
    temp_file = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt')
    temp_file.write(content)
    temp_file.close()
    
    try:
        with open(temp_file.name, 'rb') as f:
            files = {
                'file': ('test_diagnostic.txt', f, 'text/plain')
            }
            
            data = {
                'type_document': 'autre',
                'nom_document': 'Test Diagnostic Complet',
                'description': 'Test pour diagnostic des erreurs'
            }
            
            response = requests.post(
                f"{BASE_URL}/api/documents/",
                headers=headers,
                files=files,
                data=data,
                timeout=30
            )
            
            print(f"📥 Status: {response.status_code}")
            
            if response.status_code == 201:
                result = response.json()
                print("✅ Upload réussi!")
                return True
            elif response.status_code == 422:
                print("❌ Erreur 422 - Problème de validation")
                try:
                    error_data = response.json()
                    print(f"💬 Erreur: {error_data}")
                except:
                    print(f"💬 Réponse: {response.text}")
                return False
            else:
                print(f"❌ Autre erreur: {response.status_code}")
                return False
                
    except Exception as e:
        print(f"❌ Erreur: {str(e)}")
        return False
    finally:
        try:
            os.unlink(temp_file.name)
        except:
            pass

def main():
    """Diagnostic complet"""
    print("🚀 DIAGNOSTIC COMPLET DOCUMENTS")
    print("=" * 70)
    print("🔧 Base | 🏗️ Modèle | 📥 GET API | 📤 POST API")
    print("=" * 70)
    
    # Tests sans authentification
    db_ok = check_database_structure()
    model_ok = test_model_to_dict()
    
    # Obtenir le token pour les tests API
    token = get_auth_token()
    if not token:
        print("❌ Impossible d'obtenir le token")
        return
    
    # Tests avec authentification
    get_ok = test_get_documents_api(token)
    post_ok = test_upload_documents_api(token)
    
    # Résumé final
    print(f"\n📊 RÉSUMÉ DIAGNOSTIC COMPLET")
    print("=" * 70)
    
    results = {
        "Structure Base": db_ok,
        "Modèle to_dict": model_ok,
        "API GET": get_ok,
        "API POST": post_ok
    }
    
    total_tests = len(results)
    passed_tests = sum(1 for result in results.values() if result)
    
    for test_name, result in results.items():
        status = "✅ OK" if result else "❌ PROBLÈME"
        print(f"{test_name}: {status}")
    
    print(f"\n🎯 RÉSULTAT: {passed_tests}/{total_tests} tests OK")
    
    if passed_tests == total_tests:
        print("🎉 TOUS LES PROBLÈMES RÉSOLUS!")
        print("💡 Le système de documents fonctionne parfaitement")
    else:
        print("⚠️  PROBLÈMES PERSISTANTS")
        print("💡 Vérifiez les logs Flask pour plus de détails")
        
        if not db_ok:
            print("🔧 Problème base de données - Vérifiez la structure")
        if not model_ok:
            print("🏗️ Problème modèle - Vérifiez to_dict()")
        if not get_ok:
            print("📥 Problème GET API - Vérifiez la route")
        if not post_ok:
            print("📤 Problème POST API - Vérifiez la validation")
    
    return passed_tests == total_tests

if __name__ == "__main__":
    main()
