#!/usr/bin/env python3
"""
Debug simple pour identifier la cause des erreurs 422
"""

import requests
import json

BASE_URL = "http://localhost:5000"

def test_flask_health():
    """Tester que Flask répond"""
    print("🔍 TEST SANTÉ FLASK")
    print("=" * 50)
    
    try:
        response = requests.get(f"{BASE_URL}/", timeout=5)
        print(f"📥 Status page d'accueil: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ Flask fonctionne")
            return True
        else:
            print("⚠️ Flask répond mais avec erreur")
            return False
    except Exception as e:
        print(f"❌ Flask non accessible: {str(e)}")
        return False

def test_login_detailed():
    """Test de connexion détaillé"""
    print("\n🔍 TEST CONNEXION DÉTAILLÉ")
    print("=" * 50)
    
    login_data = {
        "email": "test@example.com",
        "password": "test123"
    }
    
    print(f"📤 Données de connexion: {login_data}")
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/auth/login",
            json=login_data,
            headers={'Content-Type': 'application/json'},
            timeout=10
        )
        
        print(f"📥 Status: {response.status_code}")
        print(f"📄 Headers: {dict(response.headers)}")
        
        if response.status_code == 200:
            try:
                result = response.json()
                token = result.get('access_token')
                print(f"✅ Connexion réussie")
                print(f"🔑 Token obtenu: {token[:20]}..." if token else "❌ Pas de token")
                return token
            except Exception as e:
                print(f"❌ Erreur parsing JSON: {str(e)}")
                print(f"📄 Réponse brute: {response.text}")
                return None
        elif response.status_code == 422:
            print("❌ Erreur 422 sur LOGIN")
            try:
                error = response.json()
                print(f"💬 Erreur: {error}")
            except:
                print(f"💬 Réponse: {response.text}")
            return None
        else:
            print(f"❌ Erreur connexion: {response.status_code}")
            try:
                error = response.json()
                print(f"💬 Erreur: {error}")
            except:
                print(f"💬 Réponse: {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ Erreur: {str(e)}")
        return None

def test_documents_get_detailed(token):
    """Test GET documents détaillé"""
    print("\n🔍 TEST GET DOCUMENTS DÉTAILLÉ")
    print("=" * 50)
    
    if not token:
        print("❌ Pas de token pour tester")
        return False
    
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    
    print(f"📤 Headers: {headers}")
    
    try:
        response = requests.get(
            f"{BASE_URL}/api/documents/",
            headers=headers,
            timeout=10
        )
        
        print(f"📥 Status: {response.status_code}")
        print(f"📄 Headers réponse: {dict(response.headers)}")
        
        if response.status_code == 200:
            try:
                data = response.json()
                documents = data.get('documents', [])
                print(f"✅ {len(documents)} documents récupérés")
                return True
            except Exception as e:
                print(f"❌ Erreur parsing JSON: {str(e)}")
                print(f"📄 Réponse brute: {response.text[:200]}...")
                return False
        elif response.status_code == 422:
            print("❌ ERREUR 422 SUR GET DOCUMENTS")
            try:
                error = response.json()
                print(f"💬 Erreur: {error}")
            except:
                print(f"💬 Réponse: {response.text}")
            return False
        else:
            print(f"❌ Autre erreur: {response.status_code}")
            try:
                error = response.json()
                print(f"💬 Erreur: {error}")
            except:
                print(f"💬 Réponse: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Erreur: {str(e)}")
        return False

def test_routes_availability():
    """Tester la disponibilité des routes"""
    print("\n🔍 TEST DISPONIBILITÉ ROUTES")
    print("=" * 50)
    
    routes_to_test = [
        "/api/auth/login",
        "/api/documents/",
        "/api/appointments/",
        "/documents",
        "/appointments"
    ]
    
    for route in routes_to_test:
        try:
            response = requests.get(f"{BASE_URL}{route}", timeout=5)
            print(f"📍 {route}: Status {response.status_code}")
        except Exception as e:
            print(f"❌ {route}: {str(e)}")

def check_flask_logs():
    """Vérifier les logs Flask"""
    print("\n🔍 INSTRUCTIONS POUR LOGS FLASK")
    print("=" * 50)
    print("💡 Pour voir les logs Flask détaillés:")
    print("1. Regardez la console où Flask tourne")
    print("2. Les erreurs 422 devraient y apparaître")
    print("3. Cherchez les messages commençant par ❌")

def main():
    """Diagnostic principal"""
    print("🚀 DIAGNOSTIC SIMPLE ERREURS 422")
    print("=" * 70)
    print("🔍 Flask | 🔑 Login | 📄 GET Docs | 🌐 Routes")
    print("=" * 70)
    
    # Tests séquentiels
    flask_ok = test_flask_health()
    
    if not flask_ok:
        print("\n❌ FLASK NE FONCTIONNE PAS")
        print("💡 Démarrez Flask avec: python app.py")
        return
    
    # Test routes
    test_routes_availability()
    
    # Test connexion
    token = test_login_detailed()
    
    # Test documents si on a un token
    if token:
        docs_ok = test_documents_get_detailed(token)
    else:
        docs_ok = False
        print("❌ Impossible de tester documents sans token")
    
    # Instructions pour logs
    check_flask_logs()
    
    # Résumé
    print(f"\n📊 RÉSUMÉ DIAGNOSTIC")
    print("=" * 70)
    print(f"🌐 Flask: {'✅ OK' if flask_ok else '❌ PROBLÈME'}")
    print(f"🔑 Login: {'✅ OK' if token else '❌ PROBLÈME'}")
    print(f"📄 Documents: {'✅ OK' if docs_ok else '❌ PROBLÈME'}")
    
    if not token:
        print("\n💡 PROBLÈME PRINCIPAL: AUTHENTIFICATION")
        print("🔧 Vérifiez que l'utilisateur test@example.com existe")
        print("🔧 Vérifiez la base de données")
    elif not docs_ok:
        print("\n💡 PROBLÈME PRINCIPAL: ROUTE DOCUMENTS")
        print("🔧 Vérifiez les logs Flask pour l'erreur exacte")
        print("🔧 Problème probablement dans document_routes.py")
    else:
        print("\n🎉 TOUT FONCTIONNE!")

if __name__ == "__main__":
    main()
