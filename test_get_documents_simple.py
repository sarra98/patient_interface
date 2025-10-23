#!/usr/bin/env python3
"""
Test simple de récupération des documents
"""

import requests

BASE_URL = "http://localhost:5000"

def test_get_documents_simple():
    """Test simple de récupération"""
    print("📋 TEST RÉCUPÉRATION DOCUMENTS SIMPLE")
    print("=" * 50)
    
    # Connexion
    login_data = {
        "email": "test@example.com",
        "password": "test123"
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/auth/login",
            json=login_data,
            timeout=10
        )
        
        if response.status_code == 200:
            token = response.json().get('access_token')
            print("✅ Connexion réussie")
            
            # Récupérer les documents
            headers = {
                'Authorization': f'Bearer {token}'
            }
            
            response = requests.get(
                f"{BASE_URL}/api/documents/",
                headers=headers,
                timeout=10
            )
            
            print(f"📊 Status Code: {response.status_code}")
            print(f"📋 Response: {response.text}")
            
            if response.status_code == 200:
                result = response.json()
                documents = result.get('documents', [])
                
                print(f"🎉 RÉCUPÉRATION RÉUSSIE!")
                print(f"📄 Nombre de documents: {len(documents)}")
                
                for i, doc in enumerate(documents, 1):
                    print(f"\n📄 DOCUMENT {i}:")
                    print(f"   🆔 ID: {doc.get('id')}")
                    print(f"   📝 Nom: {doc.get('nom_document')}")
                    print(f"   📂 Type: {doc.get('type_document')}")
                    print(f"   📁 Fichier: {doc.get('nom_fichier')}")
                    print(f"   📏 Taille: {doc.get('taille_fichier')} bytes")
                    print(f"   📅 Date: {doc.get('date_upload')}")
                
                return True
            else:
                print(f"❌ Erreur: {response.status_code}")
                return False
                
        else:
            print(f"❌ Connexion échouée: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Exception: {str(e)}")
        return False

def test_download_document(doc_id):
    """Test de téléchargement"""
    print(f"\n📥 TEST TÉLÉCHARGEMENT DOCUMENT {doc_id}")
    print("=" * 50)
    
    # Connexion
    login_data = {
        "email": "test@example.com",
        "password": "test123"
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/auth/login",
            json=login_data,
            timeout=10
        )
        
        if response.status_code == 200:
            token = response.json().get('access_token')
            
            # Télécharger
            headers = {
                'Authorization': f'Bearer {token}'
            }
            
            response = requests.get(
                f"{BASE_URL}/api/documents/{doc_id}",
                headers=headers,
                timeout=30
            )
            
            print(f"📊 Status Code: {response.status_code}")
            
            if response.status_code == 200:
                print(f"🎉 TÉLÉCHARGEMENT RÉUSSI!")
                print(f"📏 Taille: {len(response.content)} bytes")
                print(f"📄 Content-Type: {response.headers.get('Content-Type')}")
                return True
            else:
                print(f"❌ Erreur: {response.status_code}")
                print(f"📋 Response: {response.text}")
                return False
                
        else:
            print(f"❌ Connexion échouée: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Exception: {str(e)}")
        return False

def main():
    """Test principal"""
    print("🚀 TEST DOCUMENTS COMPLET")
    print("=" * 50)
    
    # Test récupération
    get_ok = test_get_documents_simple()
    
    # Test téléchargement du document 2 (celui qu'on vient de créer)
    download_ok = test_download_document(2)
    
    print(f"\n📊 RÉSUMÉ:")
    print(f"📋 Récupération: {'✅ OK' if get_ok else '❌ ERREUR'}")
    print(f"📥 Téléchargement: {'✅ OK' if download_ok else '❌ ERREUR'}")
    
    if get_ok and download_ok:
        print("\n🎉 SYSTÈME DOCUMENTS OPÉRATIONNEL!")
        print("\n🌐 TESTEZ SUR L'INTERFACE:")
        print("http://localhost:5000/documents")
    else:
        print("\n❌ PROBLÈMES DÉTECTÉS")

if __name__ == "__main__":
    main()
