#!/usr/bin/env python3
"""
Debug spécifique pour l'erreur 500 des documents
"""

import sqlite3
import requests

BASE_URL = "http://localhost:5000"

def check_documents_table():
    """Vérifier la structure de la table documents"""
    print("🔍 VÉRIFICATION TABLE DOCUMENTS")
    print("=" * 50)
    
    try:
        conn = sqlite3.connect('instance/secretaire_medicale.db')
        cursor = conn.cursor()
        
        # Vérifier si la table existe
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='documents_medicaux'")
        table_exists = cursor.fetchone()
        
        if not table_exists:
            print("❌ Table documents_medicaux n'existe pas")
            conn.close()
            return False
        
        print("✅ Table documents_medicaux existe")
        
        # Vérifier la structure
        cursor.execute("PRAGMA table_info(documents_medicaux)")
        columns = cursor.fetchall()
        
        print(f"📋 Structure ({len(columns)} colonnes):")
        column_names = []
        for col in columns:
            column_names.append(col[1])
            print(f"  - {col[1]} ({col[2]}) {'NOT NULL' if col[3] else 'NULL'}")
        
        # Vérifier les colonnes requises
        required_columns = ['id', 'patient_id', 'titre', 'contenu', 'fichier_path', 'is_active', 'date_creation']
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

def test_model_directly():
    """Tester le modèle DocumentMedical directement"""
    print("\n🔍 TEST MODÈLE DIRECT")
    print("=" * 50)
    
    try:
        from models import DocumentMedical
        from app import create_app
        
        app = create_app()
        
        with app.app_context():
            # Récupérer tous les documents
            documents = DocumentMedical.query.all()
            print(f"📊 {len(documents)} documents trouvés")
            
            if documents:
                doc = documents[0]
                print(f"📄 Test avec document ID: {doc.id}")
                
                # Tester les attributs un par un
                attrs_to_test = ['id', 'patient_id', 'titre', 'contenu', 'fichier_path', 'is_active', 'date_creation']
                
                for attr in attrs_to_test:
                    try:
                        value = getattr(doc, attr, 'MANQUANT')
                        print(f"  {attr}: {value}")
                    except Exception as e:
                        print(f"  {attr}: ERREUR - {str(e)}")
                
                # Tester la conversion en dict
                try:
                    doc_dict = {
                        'id': doc.id,
                        'nom_document': doc.titre or '',
                        'titre': doc.titre or '',
                        'type_document': getattr(doc, 'type_document', 'autre'),
                        'description': doc.contenu or '',
                        'contenu': doc.contenu or '',
                        'date_upload': str(doc.date_creation) if doc.date_creation else None
                    }
                    print("✅ Conversion dict réussie")
                    return True
                except Exception as e:
                    print(f"❌ Erreur conversion dict: {str(e)}")
                    return False
            else:
                print("⚠️  Aucun document pour tester")
                return True  # Pas d'erreur, juste pas de données
                
    except Exception as e:
        print(f"❌ Erreur modèle: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def test_documents_route_direct():
    """Tester la route documents directement"""
    print("\n🔍 TEST ROUTE DOCUMENTS DIRECT")
    print("=" * 50)
    
    # Obtenir un token
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
        
        if response.status_code != 200:
            print("❌ Connexion impossible")
            return False
        
        token = response.json().get('access_token')
        print("✅ Token obtenu")
        
        # Tester GET documents avec logs détaillés
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }
        
        print("📤 Requête GET /api/documents/")
        response = requests.get(
            f"{BASE_URL}/api/documents/",
            headers=headers,
            timeout=10
        )
        
        print(f"📥 Status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            documents = result.get('documents', [])
            print(f"✅ {len(documents)} documents récupérés")
            return True
        elif response.status_code == 500:
            print("❌ Erreur 500 - Exception serveur")
            try:
                error = response.json()
                print(f"💬 Erreur: {error}")
            except:
                print(f"💬 Réponse: {response.text}")
            return False
        else:
            print(f"❌ Autre erreur: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Exception: {str(e)}")
        return False

def main():
    """Diagnostic complet documents"""
    print("🚨 DIAGNOSTIC ERREUR 500 DOCUMENTS")
    print("=" * 60)
    print("🎯 Identifier la cause exacte")
    print("=" * 60)
    
    # Tests séquentiels
    table_ok = check_documents_table()
    model_ok = test_model_directly()
    route_ok = test_documents_route_direct()
    
    # Résumé
    print(f"\n📊 RÉSUMÉ DIAGNOSTIC")
    print("=" * 60)
    print(f"🗃️ Table: {'✅ OK' if table_ok else '❌ PROBLÈME'}")
    print(f"🏗️ Modèle: {'✅ OK' if model_ok else '❌ PROBLÈME'}")
    print(f"🌐 Route: {'✅ OK' if route_ok else '❌ PROBLÈME'}")
    
    if not table_ok:
        print("\n💡 PROBLÈME: Structure de table")
        print("🔧 La table documents_medicaux a un problème")
    elif not model_ok:
        print("\n💡 PROBLÈME: Modèle DocumentMedical")
        print("🔧 Le modèle a une erreur dans les attributs")
    elif not route_ok:
        print("\n💡 PROBLÈME: Route GET documents")
        print("🔧 Erreur dans la logique de la route")
    else:
        print("\n🎉 TOUS LES TESTS PASSENT!")
        print("💡 Le problème était temporaire")
    
    return table_ok and model_ok and route_ok

if __name__ == "__main__":
    main()
