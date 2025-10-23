#!/usr/bin/env python3
"""
Test de l'interface complète des documents
"""

import requests
import os
from io import BytesIO

BASE_URL = "http://localhost:5000"

def test_get_documents():
    """Tester la récupération des documents"""
    print("📋 TEST RÉCUPÉRATION DOCUMENTS")
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
            
            if response.status_code == 200:
                result = response.json()
                documents = result.get('documents', [])
                
                print(f"🎉 RÉCUPÉRATION RÉUSSIE!")
                print(f"📄 Nombre de documents: {len(documents)}")
                
                if documents:
                    print(f"\n📋 LISTE DES DOCUMENTS:")
                    print("-" * 80)
                    print("ID | Type | Nom | Fichier | Taille | Date")
                    print("-" * 80)
                    
                    for doc in documents:
                        doc_id = doc.get('id', 'N/A')
                        type_doc = doc.get('type_document', 'N/A')
                        nom = doc.get('nom_document', 'N/A')
                        fichier = doc.get('nom_fichier', 'N/A')
                        taille = doc.get('taille_fichier', 0)
                        date_upload = doc.get('date_upload', 'N/A')
                        
                        nom_short = (nom[:20] + '...') if len(str(nom)) > 20 else nom
                        fichier_short = (fichier[:15] + '...') if len(str(fichier)) > 15 else fichier
                        taille_str = f"{taille}B" if taille else "N/A"
                        date_str = date_upload[:10] if date_upload else "N/A"
                        
                        print(f"{doc_id:2} | {type_doc:8} | {nom_short:23} | {fichier_short:18} | {taille_str:8} | {date_str}")
                
                return documents
            else:
                print(f"❌ Erreur récupération: {response.status_code}")
                print(f"📋 Response: {response.text}")
                return []
                
        else:
            print(f"❌ Connexion échouée: {response.status_code}")
            return []
            
    except Exception as e:
        print(f"❌ Exception: {str(e)}")
        return []

def test_download_document(document_id):
    """Tester le téléchargement d'un document"""
    print(f"\n📥 TEST TÉLÉCHARGEMENT DOCUMENT {document_id}")
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
            
            # Télécharger le document
            headers = {
                'Authorization': f'Bearer {token}'
            }
            
            response = requests.get(
                f"{BASE_URL}/api/documents/{document_id}",
                headers=headers,
                timeout=30
            )
            
            print(f"📊 Status Code: {response.status_code}")
            
            if response.status_code == 200:
                # Vérifier les headers
                content_type = response.headers.get('Content-Type', 'N/A')
                content_length = response.headers.get('Content-Length', 'N/A')
                content_disposition = response.headers.get('Content-Disposition', 'N/A')
                
                print("🎉 TÉLÉCHARGEMENT RÉUSSI!")
                print(f"📄 Content-Type: {content_type}")
                print(f"📏 Content-Length: {content_length}")
                print(f"📎 Content-Disposition: {content_disposition}")
                print(f"📊 Taille reçue: {len(response.content)} bytes")
                
                # Sauvegarder temporairement pour vérifier
                temp_file = f"temp_download_{document_id}.pdf"
                with open(temp_file, 'wb') as f:
                    f.write(response.content)
                
                print(f"💾 Fichier temporaire créé: {temp_file}")
                
                # Nettoyer
                if os.path.exists(temp_file):
                    os.remove(temp_file)
                    print(f"🗑️ Fichier temporaire supprimé")
                
                return True
            else:
                print(f"❌ Erreur téléchargement: {response.status_code}")
                print(f"📋 Response: {response.text}")
                return False
                
        else:
            print(f"❌ Connexion échouée: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Exception: {str(e)}")
        return False

def test_upload_new_document():
    """Tester l'upload d'un nouveau document"""
    print(f"\n📤 TEST UPLOAD NOUVEAU DOCUMENT")
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
            
            # Créer un fichier image PNG simple
            png_content = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x06\x00\x00\x00\x1f\x15\xc4\x89\x00\x00\x00\rIDATx\x9cc\xf8\x0f\x00\x00\x01\x00\x01\x00\x00\x00\x00\x00\x00IEND\xaeB`\x82'
            
            # Préparer les données
            headers = {
                'Authorization': f'Bearer {token}'
            }
            
            files = {
                'file': ('radio_test.png', BytesIO(png_content), 'image/png')
            }
            
            data = {
                'nom_document': 'Radio de test',
                'type_document': 'radio',
                'description': 'Image de test pour vérifier l\'upload'
            }
            
            print(f"📤 Upload en cours...")
            print(f"🖼️ Fichier: radio_test.png")
            print(f"📏 Taille: {len(png_content)} bytes")
            
            # Upload
            response = requests.post(
                f"{BASE_URL}/api/documents/",
                headers=headers,
                files=files,
                data=data,
                timeout=30
            )
            
            print(f"📊 Status Code: {response.status_code}")
            
            if response.status_code == 201:
                result = response.json()
                print("🎉 UPLOAD RÉUSSI!")
                print(f"📋 Message: {result.get('message')}")
                document = result.get('document', {})
                print(f"🆔 ID: {document.get('id')}")
                print(f"📝 Nom: {document.get('nom_document')}")
                print(f"📄 Type: {document.get('type_document')}")
                return document.get('id')
            else:
                print(f"❌ Upload échoué: {response.status_code}")
                print(f"📋 Response: {response.text}")
                return None
                
        else:
            print(f"❌ Connexion échouée: {response.status_code}")
            return None
            
    except Exception as e:
        print(f"❌ Exception: {str(e)}")
        return None

def show_interface_instructions():
    """Afficher les instructions pour l'interface"""
    print(f"\n🌐 INSTRUCTIONS INTERFACE DOCUMENTS")
    print("=" * 60)
    print("1. 🌐 Allez sur: http://localhost:5000/documents")
    print("2. 🔑 Connectez-vous: test@example.com / test123")
    print("3. 📋 Vous verrez la liste de vos documents:")
    print("   📄 Nom du document")
    print("   📂 Type (Analyse, Ordonnance, Radio, Autre)")
    print("   📅 Date d'upload")
    print("   📏 Taille du fichier")
    print("   🔗 Actions (Télécharger, Supprimer)")
    
    print(f"\n📤 POUR AJOUTER UN DOCUMENT:")
    print("1. 🔘 Cliquez 'Ajouter un document'")
    print("2. 📋 Remplissez le formulaire:")
    print("   📂 Type de document")
    print("   📝 Nom descriptif")
    print("   📁 Sélectionnez le fichier")
    print("   📝 Description (optionnelle)")
    print("3. 📤 Cliquez 'Ajouter le document'")
    print("4. ✅ Le document apparaît dans la liste")
    
    print(f"\n📥 POUR TÉLÉCHARGER UN DOCUMENT:")
    print("1. 🔍 Trouvez le document dans la liste")
    print("2. 🔘 Cliquez sur l'icône de téléchargement")
    print("3. 💾 Le fichier se télécharge automatiquement")
    
    print(f"\n🗑️ POUR SUPPRIMER UN DOCUMENT:")
    print("1. 🔍 Trouvez le document dans la liste")
    print("2. 🔘 Cliquez sur l'icône de suppression")
    print("3. ✅ Confirmez la suppression")

def main():
    """Test principal de l'interface documents"""
    print("🚀 TEST INTERFACE COMPLÈTE DOCUMENTS")
    print("=" * 70)
    
    # Récupérer les documents existants
    documents = test_get_documents()
    
    # Tester le téléchargement si des documents existent
    download_ok = False
    if documents:
        first_doc_id = documents[0].get('id')
        if first_doc_id:
            download_ok = test_download_document(first_doc_id)
    
    # Tester l'upload d'un nouveau document
    new_doc_id = test_upload_new_document()
    
    # Afficher les instructions
    show_interface_instructions()
    
    print(f"\n📊 RÉSUMÉ TESTS")
    print("=" * 70)
    print(f"📋 Récupération documents: {'✅ OK' if documents else '❌ ERREUR'}")
    print(f"📥 Téléchargement: {'✅ OK' if download_ok else '❌ ERREUR'}")
    print(f"📤 Upload nouveau: {'✅ OK' if new_doc_id else '❌ ERREUR'}")
    
    if documents and download_ok and new_doc_id:
        print("\n🎉 INTERFACE DOCUMENTS COMPLÈTEMENT OPÉRATIONNELLE!")
        print("\n✅ FONCTIONNALITÉS TESTÉES:")
        print("📋 Affichage liste des documents")
        print("📥 Téléchargement de fichiers")
        print("📤 Upload de nouveaux documents")
        print("🗄️ Enregistrement en base de données")
        print("📁 Stockage physique sécurisé")
        
        print(f"\n📊 STATISTIQUES:")
        print(f"📄 Documents en base: {len(documents)}")
        print(f"🆔 Dernier document uploadé: {new_doc_id}")
        
        print("\n🌐 TESTEZ MAINTENANT:")
        print("http://localhost:5000/documents")
        print("Gérez vos documents médicaux!")
    else:
        print("\n❌ PROBLÈMES DÉTECTÉS")
        print("🔧 Vérifiez les logs Flask")

if __name__ == "__main__":
    main()
