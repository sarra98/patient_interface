#!/usr/bin/env python3
"""
Test simple pour vérifier l'upload après correction 422
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

def test_upload_exact_format(token):
    """Test avec le format exact envoyé par l'interface"""
    print("🔍 TEST UPLOAD FORMAT EXACT")
    print("=" * 50)
    
    headers = {
        'Authorization': f'Bearer {token}'
    }
    
    # Créer un fichier de test
    content = "Test upload après correction définitive erreur 422"
    temp_file = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt')
    temp_file.write(content)
    temp_file.close()
    
    try:
        with open(temp_file.name, 'rb') as f:
            files = {
                'file': ('test_final.txt', f, 'text/plain')
            }
            
            # Données EXACTEMENT comme envoyées par l'interface
            data = {
                'type_document': 'autre',
                'nom_document': 'Test Final 422',
                'description': 'Test après correction définitive',
                'date_document': '2025-01-16',
                'medecin_prescripteur': 'Dr Test Final'
            }
            
            print(f"📤 Données envoyées (format interface):")
            for key, value in data.items():
                print(f"  {key}: {value}")
            
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
                print("🎉 UPLOAD RÉUSSI!")
                print(f"📋 Message: {result.get('message')}")
                
                document = result.get('document', {})
                print(f"🆔 ID: {document.get('id')}")
                print(f"📄 Titre: {document.get('titre')}")
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
        try:
            os.unlink(temp_file.name)
        except:
            pass

def test_get_after_upload(token):
    """Test GET après upload"""
    print("\n🔍 TEST GET APRÈS UPLOAD")
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
            
            if documents:
                doc = documents[0]
                print(f"📄 Premier document: {doc.get('titre', 'Sans titre')}")
                print(f"📂 Type: {doc.get('type_document', 'Sans type')}")
            
            return True
        else:
            print(f"❌ Erreur GET: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Erreur: {str(e)}")
        return False

def main():
    """Test principal"""
    print("🚀 TEST SIMPLE UPLOAD DOCUMENTS")
    print("=" * 60)
    print("🔧 Correction définitive erreur 422")
    print("=" * 60)
    
    # Obtenir le token
    token = get_auth_token()
    if not token:
        print("❌ Impossible d'obtenir le token")
        return
    
    # Tests
    upload_ok = test_upload_exact_format(token)
    get_ok = test_get_after_upload(token)
    
    # Résumé
    print(f"\n📊 RÉSUMÉ TEST SIMPLE")
    print("=" * 60)
    print(f"📤 Upload: {'✅ RÉUSSI' if upload_ok else '❌ ÉCHOUÉ'}")
    print(f"📥 Get: {'✅ RÉUSSI' if get_ok else '❌ ÉCHOUÉ'}")
    
    if upload_ok and get_ok:
        print("\n🎉 ERREUR 422 DÉFINITIVEMENT CORRIGÉE!")
        print("💡 Le système de documents fonctionne parfaitement")
        print("🌐 Testez dans l'interface: http://localhost:5000/documents")
    else:
        print("\n❌ PROBLÈMES PERSISTANTS")
        print("💡 Vérifiez les logs Flask pour plus de détails")
    
    return upload_ok and get_ok

if __name__ == "__main__":
    main()
