#!/usr/bin/env python3
"""
Test final avec le bon utilisateur
"""

import requests
import json

BASE_URL = "http://localhost:5000"

def test_login():
    """Test connexion avec test@example.com"""
    print("🔍 TEST CONNEXION")
    print("=" * 30)
    
    login_data = {
        "email": "test@example.com",
        "password": "test123"
    }
    
    print(f"📤 Connexion: {login_data['email']}")
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/auth/login",
            json=login_data,
            headers={'Content-Type': 'application/json'},
            timeout=10
        )
        
        print(f"📥 Status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            token = result.get('access_token')
            print(f"✅ Connexion OK!")
            return token
        else:
            print(f"❌ Erreur: {response.status_code}")
            try:
                error = response.json()
                print(f"💬 Détails: {error}")
            except:
                print(f"💬 Réponse: {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ Exception: {str(e)}")
        return None

def test_create_appointment(token):
    """Test création RDV"""
    print("\n🔍 TEST CRÉATION RDV")
    print("=" * 30)
    
    if not token:
        print("❌ Pas de token")
        return False
    
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    
    appointment_data = {
        "medecin_id": 1,
        "date_rdv": "2025-07-18T14:30:00",
        "motif": "Test final",
        "notes": "Test creation RDV"
    }
    
    print(f"📤 Données: {appointment_data}")
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/appointments/",
            json=appointment_data,
            headers=headers,
            timeout=30
        )
        
        print(f"📥 Status: {response.status_code}")
        
        if response.status_code == 201:
            result = response.json()
            print(f"✅ RDV CRÉÉ!")
            print(f"📋 Message: {result.get('message')}")
            return True
        else:
            print(f"❌ Erreur: {response.status_code}")
            try:
                error = response.json()
                print(f"💬 Détails: {json.dumps(error, indent=2)}")
            except:
                print(f"💬 Réponse: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Exception: {str(e)}")
        return False

def test_get_appointments(token):
    """Test récupération RDV"""
    print("\n🔍 TEST GET RDV")
    print("=" * 30)
    
    if not token:
        print("❌ Pas de token")
        return False
    
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    
    try:
        response = requests.get(
            f"{BASE_URL}/api/appointments/",
            headers=headers,
            timeout=10
        )
        
        print(f"📥 Status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            appointments = result.get('appointments', [])
            print(f"✅ {len(appointments)} RDV récupérés")
            return True
        else:
            print(f"❌ Erreur: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Exception: {str(e)}")
        return False

def test_get_documents(token):
    """Test récupération documents"""
    print("\n🔍 TEST GET DOCUMENTS")
    print("=" * 30)
    
    if not token:
        print("❌ Pas de token")
        return False
    
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
            result = response.json()
            documents = result.get('documents', [])
            print(f"✅ {len(documents)} documents récupérés")
            return True
        else:
            print(f"❌ Erreur: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Exception: {str(e)}")
        return False

def main():
    """Test final complet"""
    print("🎉 TEST FINAL COMPLET")
    print("=" * 50)
    print("🎯 Avec utilisateur test@example.com")
    print("=" * 50)
    
    # Test connexion
    token = test_login()
    
    if not token:
        print("\n❌ CONNEXION IMPOSSIBLE")
        print("💡 Vérifiez que Flask tourne")
        print("💡 Exécutez: python create_test_user.py")
        return
    
    # Tests API
    get_appointments_ok = test_get_appointments(token)
    get_documents_ok = test_get_documents(token)
    create_appointment_ok = test_create_appointment(token)
    
    # Résumé
    print(f"\n📊 RÉSUMÉ FINAL")
    print("=" * 50)
    print(f"🔑 Connexion: ✅ OK")
    print(f"📥 GET RDV: {'✅ OK' if get_appointments_ok else '❌ ERREUR'}")
    print(f"📥 GET Docs: {'✅ OK' if get_documents_ok else '❌ ERREUR'}")
    print(f"📤 CREATE RDV: {'✅ OK' if create_appointment_ok else '❌ ERREUR'}")
    
    if create_appointment_ok:
        print("\n🎉 PROBLÈME RÉSOLU!")
        print("💡 Le bouton 'Confirmer le rendez-vous' devrait marcher")
        print("🌐 Testez: http://localhost:5000/book-appointment")
        print("🔑 Connectez-vous: test@example.com / test123")
    else:
        print("\n❌ PROBLÈME PERSISTE")
        print("💡 Vérifiez les logs Flask pour l'erreur exacte")
    
    return create_appointment_ok

if __name__ == "__main__":
    main()
