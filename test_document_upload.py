#!/usr/bin/env python3
"""
Test de l'upload de documents PDF/images
"""

import requests
import os
from io import BytesIO

BASE_URL = "http://localhost:5000"

def create_test_pdf():
    """Créer un fichier PDF de test"""
    pdf_content = b"""%PDF-1.4
1 0 obj
<<
/Type /Catalog
/Pages 2 0 R
>>
endobj

2 0 obj
<<
/Type /Pages
/Kids [3 0 R]
/Count 1
>>
endobj

3 0 obj
<<
/Type /Page
/Parent 2 0 R
/MediaBox [0 0 612 792]
/Contents 4 0 R
>>
endobj

4 0 obj
<<
/Length 44
>>
stream
BT
/F1 12 Tf
72 720 Td
(Test Document) Tj
ET
endstream
endobj

xref
0 5
0000000000 65535 f 
0000000009 00000 n 
0000000058 00000 n 
0000000115 00000 n 
0000000206 00000 n 
trailer
<<
/Size 5
/Root 1 0 R
>>
startxref
299
%%EOF"""
    return pdf_content

def test_document_upload():
    """Tester l'upload d'un document"""
    print("📄 TEST UPLOAD DOCUMENT")
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
            
            # Préparer les headers
            headers = {
                'Authorization': f'Bearer {token}'
            }
            
            # Créer un fichier PDF de test
            pdf_content = create_test_pdf()
            
            # Préparer les données du formulaire
            files = {
                'file': ('test_document.pdf', BytesIO(pdf_content), 'application/pdf')
            }
            
            data = {
                'nom_document': 'Document de test',
                'type_document': 'analyse',
                'description': 'Test upload PDF'
            }
            
            print(f"📤 Upload en cours...")
            print(f"📄 Fichier: test_document.pdf")
            print(f"📏 Taille: {len(pdf_content)} bytes")
            
            # Upload du document
            response = requests.post(
                f"{BASE_URL}/api/documents/",
                headers=headers,
                files=files,
                data=data,
                timeout=30
            )
            
            print(f"📊 Status Code: {response.status_code}")
            print(f"📋 Response: {response.text}")
            
            if response.status_code == 201:
                result = response.json()
                print("🎉 UPLOAD RÉUSSI!")
                print(f"📋 Message: {result.get('message')}")
                document = result.get('document', {})
                print(f"🆔 ID: {document.get('id')}")
                print(f"📝 Titre: {document.get('titre')}")
                return True
            else:
                print("❌ UPLOAD ÉCHOUÉ!")
                try:
                    error_data = response.json()
                    print(f"❌ Erreur: {error_data.get('error')}")
                except:
                    print(f"❌ Erreur brute: {response.text}")
                return False
                
        else:
            print(f"❌ Connexion échouée: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Exception: {str(e)}")
        return False

def test_image_upload():
    """Tester l'upload d'une image"""
    print("\n🖼️ TEST UPLOAD IMAGE")
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
            
            # Préparer les headers
            headers = {
                'Authorization': f'Bearer {token}'
            }
            
            # Créer une image PNG simple (1x1 pixel transparent)
            png_content = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x06\x00\x00\x00\x1f\x15\xc4\x89\x00\x00\x00\rIDATx\x9cc\xf8\x0f\x00\x00\x01\x00\x01\x00\x00\x00\x00\x00\x00IEND\xaeB`\x82'
            
            # Préparer les données du formulaire
            files = {
                'file': ('test_image.png', BytesIO(png_content), 'image/png')
            }
            
            data = {
                'nom_document': 'Image de test',
                'type_document': 'radio',
                'description': 'Test upload PNG'
            }
            
            print(f"📤 Upload en cours...")
            print(f"🖼️ Fichier: test_image.png")
            print(f"📏 Taille: {len(png_content)} bytes")
            
            # Upload du document
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
                print("🎉 UPLOAD IMAGE RÉUSSI!")
                print(f"📋 Message: {result.get('message')}")
                return True
            else:
                print("❌ UPLOAD IMAGE ÉCHOUÉ!")
                print(f"📋 Response: {response.text}")
                return False
                
        else:
            print(f"❌ Connexion échouée: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Exception: {str(e)}")
        return False

def show_upload_instructions():
    """Afficher les instructions pour l'upload"""
    print(f"\n🌐 INSTRUCTIONS UPLOAD DOCUMENTS")
    print("=" * 60)
    print("1. 🌐 Allez sur: http://localhost:5000/documents")
    print("2. 🔑 Connectez-vous: test@example.com / test123")
    print("3. 📤 Cliquez sur 'Ajouter un document'")
    print("4. 📋 Remplissez le formulaire:")
    print("   📝 Type: Analyse, Ordonnance, Radio, Autre")
    print("   📄 Nom: Nom descriptif du document")
    print("   📁 Fichier: PDF, JPG, PNG, DOC, DOCX (max 10MB)")
    print("   📝 Description: Optionnelle")
    print("5. 📤 Cliquez 'Ajouter le document'")
    print("6. ✅ Le document apparaît dans la liste")
    
    print(f"\n📁 FORMATS SUPPORTÉS:")
    print("📄 PDF - Documents, analyses, ordonnances")
    print("🖼️ JPG/PNG - Images, radios, photos")
    print("📝 DOC/DOCX - Documents Word")
    
    print(f"\n🔧 EN CAS D'ERREUR 500:")
    print("✅ Vérifiez les logs Flask dans la console")
    print("✅ Vérifiez que le dossier uploads/ existe")
    print("✅ Vérifiez les permissions de fichiers")

def main():
    """Test principal de l'upload de documents"""
    print("🚀 TEST UPLOAD DOCUMENTS PDF/IMAGES")
    print("=" * 70)
    
    # Tester upload PDF
    pdf_ok = test_document_upload()
    
    # Tester upload image
    image_ok = test_image_upload()
    
    # Afficher les instructions
    show_upload_instructions()
    
    print(f"\n📊 RÉSUMÉ TESTS")
    print("=" * 70)
    print(f"📄 Upload PDF: {'✅ OK' if pdf_ok else '❌ ERREUR'}")
    print(f"🖼️ Upload Image: {'✅ OK' if image_ok else '❌ ERREUR'}")
    
    if pdf_ok and image_ok:
        print("\n🎉 UPLOAD DOCUMENTS OPÉRATIONNEL!")
        print("\n✅ FONCTIONNALITÉS:")
        print("📄 Upload PDF - Analyses, ordonnances")
        print("🖼️ Upload Images - Radios, photos")
        print("📝 Métadonnées - Nom, type, description")
        print("🔒 Sécurisé - Authentification requise")
        print("📁 Organisé - Dossiers par patient")
        
        print("\n🌐 TESTEZ MAINTENANT:")
        print("http://localhost:5000/documents")
        print("Uploadez vos documents médicaux!")
    else:
        print("\n❌ PROBLÈMES DÉTECTÉS")
        print("🔧 Vérifiez les logs Flask")
        print("🔧 Vérifiez la configuration des routes")

if __name__ == "__main__":
    main()
