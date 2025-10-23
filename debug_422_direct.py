#!/usr/bin/env python3
"""
Debug direct de l'erreur 422 documents
"""

import requests
import tempfile
import os

BASE_URL = "http://localhost:5000"

def test_login():
    """Test de connexion"""
    print("🔍 TEST CONNEXION")
    print("=" * 30)
    
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
        
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            token = response.json().get('access_token')
            print("Connexion OK")
            return token
        else:
            print(f"Erreur connexion: {response.text}")
            return None
            
    except Exception as e:
        print(f"Erreur: {str(e)}")
        return None

def test_get_documents(token):
    """Test GET documents"""
    print("\n🔍 TEST GET DOCUMENTS")
    print("=" * 30)
    
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
        
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"GET OK - {len(data.get('documents', []))} documents")
            return True
        else:
            print(f"Erreur GET: {response.text}")
            return False
            
    except Exception as e:
        print(f"Erreur: {str(e)}")
        return False

def test_post_documents_minimal(token):
    """Test POST documents avec données minimales"""
    print("\n🔍 TEST POST DOCUMENTS MINIMAL")
    print("=" * 30)
    
    headers = {
        'Authorization': f'Bearer {token}'
    }
    
    # Créer un fichier de test très simple
    content = "Test minimal"
    temp_file = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt')
    temp_file.write(content)
    temp_file.close()
    
    try:
        with open(temp_file.name, 'rb') as f:
            files = {
                'file': ('test_minimal.txt', f, 'text/plain')
            }
            
            # Données minimales
            data = {
                'type_document': 'autre',
                'nom_document': 'Test Minimal'
            }
            
            print(f"Données: {data}")
            
            response = requests.post(
                f"{BASE_URL}/api/documents/",
                headers=headers,
                files=files,
                data=data,
                timeout=30
            )
            
            print(f"Status: {response.status_code}")
            
            if response.status_code == 201:
                result = response.json()
                print("POST OK!")
                print(f"Message: {result.get('message')}")
                return True
            else:
                print(f"Erreur POST: {response.text}")
                return False
                
    except Exception as e:
        print(f"Erreur: {str(e)}")
        return False
    finally:
        try:
            os.unlink(temp_file.name)
        except:
            pass

def test_flask_direct():
    """Test direct de Flask"""
    print("\n🔍 TEST FLASK DIRECT")
    print("=" * 30)
    
    try:
        response = requests.get(f"{BASE_URL}/", timeout=5)
        print(f"Page accueil: {response.status_code}")
        
        response = requests.get(f"{BASE_URL}/documents", timeout=5)
        print(f"Page documents: {response.status_code}")
        
        return True
    except Exception as e:
        print(f"Flask non accessible: {str(e)}")
        return False

def check_flask_logs():
    """Instructions pour vérifier les logs Flask"""
    print("\n💡 VÉRIFICATION LOGS FLASK")
    print("=" * 30)
    print("1. Regardez la console où Flask tourne")
    print("2. Cherchez les messages d'erreur")
    print("3. Les erreurs 422 devraient y apparaître")
    print("4. Notez l'erreur exacte")

def main():
    """Test principal"""
    print("🚨 DEBUG DIRECT ERREUR 422 DOCUMENTS")
    print("=" * 50)
    
    # Test Flask
    if not test_flask_direct():
        print("❌ Flask non accessible")
        print("💡 Démarrez Flask: python app.py")
        return
    
    # Test connexion
    token = test_login()
    if not token:
        print("❌ Connexion impossible")
        print("💡 Vérifiez que l'utilisateur test@example.com existe")
        return
    
    # Test GET
    get_ok = test_get_documents(token)
    
    # Test POST
    post_ok = test_post_documents_minimal(token)
    
    # Instructions logs
    check_flask_logs()
    
    # Résumé
    print(f"\n📊 RÉSUMÉ")
    print("=" * 50)
    print(f"🌐 Flask: OK")
    print(f"🔑 Login: OK")
    print(f"📥 GET: {'OK' if get_ok else 'ERREUR'}")
    print(f"📤 POST: {'OK' if post_ok else 'ERREUR 422'}")
    
    if not get_ok:
        print("\n❌ PROBLÈME GET DOCUMENTS")
        print("💡 Erreur dans la route GET ou modèle")
    
    if not post_ok:
        print("\n❌ PROBLÈME POST DOCUMENTS")
        print("💡 Erreur 422 - Vérifiez les logs Flask")
        print("💡 Causes possibles:")
        print("  - Problème de validation")
        print("  - Erreur dans le modèle DocumentMedical")
        print("  - Problème de base de données")
        print("  - Import manquant")
    
    if get_ok and post_ok:
        print("\n🎉 TOUT FONCTIONNE!")
        print("💡 Le problème était temporaire")

if __name__ == "__main__":
    main()
