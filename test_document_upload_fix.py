#!/usr/bin/env python3
"""
Test spécifique pour l'upload de documents (correction erreur 422)
"""

import requests
import tempfile
import os

BASE_URL = "http://localhost:5000"

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

def create_test_file():
    """Créer un fichier de test"""
    content = """Document de test pour vérifier la correction de l'erreur 422.

Ce fichier teste l'upload après les corrections apportées au schéma de validation.

Date: 2025-01-16
Type: Test automatique
"""
    
    temp_file = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt')
    temp_file.write(content)
    temp_file.close()
    
    return temp_file.name

def test_document_upload_detailed(token):
    """Test détaillé de l'upload de documents"""
    print("\n🔍 TEST UPLOAD DOCUMENTS DÉTAILLÉ")
    print("=" * 50)
    
    headers = {
        'Authorization': f'Bearer {token}'
    }
    
    # Créer un fichier de test
    test_file_path = create_test_file()
    print(f"📄 Fichier de test créé: {test_file_path}")
    
    try:
        with open(test_file_path, 'rb') as f:
            files = {
                'file': ('test_correction_422.txt', f, 'text/plain')
            }
            
            # Données exactement comme envoyées par l'interface
            data = {
                'type_document': 'autre',
                'nom_document': 'Test Correction 422',  # Sera mappé vers 'titre'
                'description': 'Test après correction erreur 422',  # Sera mappé vers 'contenu'
                'date_document': '2025-01-16',
                'medecin_prescripteur': 'Dr Test'
            }
            
            print(f"📤 Données envoyées:")
            for key, value in data.items():
                print(f"  {key}: {value}")
            
            print(f"📁 Fichier: {files['file'][0]}")
            
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
                print("✅ UPLOAD RÉUSSI!")
                print(f"📋 Message: {result.get('message')}")
                
                document = result.get('document', {})
                print(f"🆔 ID: {document.get('id')}")
                print(f"📄 Titre: {document.get('titre')}")
                print(f"📂 Type: {document.get('type_document')}")
                print(f"📝 Contenu: {document.get('contenu')}")
                
                return True
                
            elif response.status_code == 422:
                print("❌ ERREUR 422 PERSISTANTE")
                try:
                    error_data = response.json()
                    print(f"💬 Détails: {error_data}")
                except:
                    print(f"💬 Réponse brute: {response.text}")
                return False
                
            else:
                print(f"❌ AUTRE ERREUR: {response.status_code}")
                try:
                    error_data = response.json()
                    print(f"💬 Erreur: {error_data}")
                except:
                    print(f"💬 Réponse: {response.text}")
                return False
                
    except Exception as e:
        print(f"❌ Erreur: {str(e)}")
        return False
    finally:
        # Nettoyer le fichier de test
        try:
            os.unlink(test_file_path)
            print(f"🗑️  Fichier de test supprimé")
        except:
            pass

def test_get_documents(token):
    """Tester la récupération des documents"""
    print("\n🔍 TEST RÉCUPÉRATION DOCUMENTS")
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
            data = response.json()
            documents = data.get('documents', [])
            print(f"✅ {len(documents)} documents récupérés")
            
            for i, doc in enumerate(documents[:3]):
                print(f"  {i+1}. {doc.get('titre', 'Sans titre')} ({doc.get('type_document', 'Sans type')})")
            
            return True
        else:
            print(f"❌ Erreur récupération: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Erreur: {str(e)}")
        return False

def test_documents_page():
    """Tester l'accès à la page documents"""
    print("\n🔍 TEST PAGE DOCUMENTS")
    print("=" * 50)
    
    try:
        response = requests.get(f"{BASE_URL}/documents", timeout=5)
        if response.status_code == 200:
            print("✅ Page documents accessible")
            return True
        else:
            print(f"❌ Page documents: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Erreur: {str(e)}")
        return False

def main():
    """Test principal de la correction upload documents"""
    print("🚀 TEST CORRECTION UPLOAD DOCUMENTS")
    print("=" * 70)
    print("🔧 Correction erreur 422 | 📄 Schéma adapté | 🗂️ Champs mappés")
    print("=" * 70)
    
    # Test page documents
    page_ok = test_documents_page()
    
    # Obtenir le token
    token = get_auth_token()
    if not token:
        print("❌ Impossible d'obtenir le token")
        return
    
    # Tests avec authentification
    get_ok = test_get_documents(token)
    upload_ok = test_document_upload_detailed(token)
    
    # Résumé final
    print(f"\n📊 RÉSUMÉ CORRECTION DOCUMENTS")
    print("=" * 70)
    
    results = {
        "Page Documents": page_ok,
        "Récupération": get_ok,
        "Upload (422)": upload_ok
    }
    
    total_tests = len(results)
    passed_tests = sum(1 for result in results.values() if result)
    
    for test_name, result in results.items():
        status = "✅ CORRIGÉ" if result else "❌ PROBLÈME"
        print(f"{test_name}: {status}")
    
    print(f"\n🎯 RÉSULTAT: {passed_tests}/{total_tests} tests OK")
    
    if passed_tests == total_tests:
        print("🎉 ERREUR 422 DOCUMENTS CORRIGÉE!")
        print("\n💡 CORRECTIONS APPLIQUÉES:")
        print("📋 Schéma DocumentSchema adapté (titre, contenu)")
        print("🔄 Mapping automatique nom_document -> titre")
        print("🔄 Mapping automatique description -> contenu")
        print("💾 Création document avec bons champs")
        print("📥 Récupération avec date_creation")
    else:
        print("⚠️  PROBLÈMES PERSISTANTS")
        print("💡 Vérifiez les logs Flask pour plus de détails")
    
    return passed_tests == total_tests

if __name__ == "__main__":
    main()
