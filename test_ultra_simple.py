#!/usr/bin/env python3
"""
Test ultra-simple pour identifier le problème exact
"""

import requests
import json

BASE_URL = "http://localhost:5000"

def test_login_step_by_step():
    """Test de connexion étape par étape"""
    print("🔍 TEST CONNEXION ÉTAPE PAR ÉTAPE")
    print("=" * 50)
    
    # Données de connexion
    login_data = {
        "email": "lin@gmail.com",  # Utiliser l'email qui existe
        "password": "123456"       # Mot de passe simple
    }
    
    print(f"📤 Tentative connexion avec: {login_data['email']}")
    
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
            result = response.json()
            token = result.get('access_token')
            print(f"✅ Connexion réussie!")
            print(f"🔑 Token: {token[:20]}..." if token else "❌ Pas de token")
            return token
        else:
            print(f"❌ Erreur connexion")
            try:
                error = response.json()
                print(f"💬 Erreur: {error}")
            except:
                print(f"💬 Réponse brute: {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ Exception: {str(e)}")
        return None

def test_simple_get_request(token, endpoint, description):
    """Test GET simple"""
    print(f"\n🔍 TEST {description}")
    print("=" * 50)
    
    if not token:
        print("❌ Pas de token")
        return False
    
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    
    try:
        print(f"📤 GET {endpoint}")
        response = requests.get(
            f"{BASE_URL}{endpoint}",
            headers=headers,
            timeout=10
        )
        
        print(f"📥 Status: {response.status_code}")
        
        if response.status_code == 200:
            try:
                data = response.json()
                print(f"✅ Succès! Données reçues")
                return True
            except Exception as e:
                print(f"❌ Erreur JSON: {str(e)}")
                print(f"📄 Réponse: {response.text[:200]}...")
                return False
        elif response.status_code == 422:
            print("❌ ERREUR 422!")
            try:
                error = response.json()
                print(f"💬 Détails: {json.dumps(error, indent=2)}")
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
        print(f"❌ Exception: {str(e)}")
        return False

def test_simple_post_appointment(token):
    """Test POST rendez-vous ultra-simple"""
    print(f"\n🔍 TEST POST RENDEZ-VOUS ULTRA-SIMPLE")
    print("=" * 50)
    
    if not token:
        print("❌ Pas de token")
        return False
    
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    
    # Données ultra-simples
    appointment_data = {
        "medecin_id": 1,
        "date_rdv": "2025-07-18T14:30:00",
        "motif": "Test simple",
        "notes": "Test"
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
            print(f"✅ RDV créé!")
            print(f"📋 Message: {result.get('message')}")
            return True
        elif response.status_code == 422:
            print("❌ ERREUR 422!")
            try:
                error = response.json()
                print(f"💬 Détails: {json.dumps(error, indent=2)}")
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
        print(f"❌ Exception: {str(e)}")
        return False

def check_flask_status():
    """Vérifier que Flask fonctionne"""
    print("🔍 VÉRIFICATION FLASK")
    print("=" * 50)
    
    try:
        response = requests.get(f"{BASE_URL}/", timeout=5)
        print(f"📥 Page d'accueil: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ Flask fonctionne")
            return True
        else:
            print("❌ Flask a un problème")
            return False
    except Exception as e:
        print(f"❌ Flask non accessible: {str(e)}")
        print("💡 Démarrez Flask avec: python app.py")
        return False

def main():
    """Test principal ultra-simple"""
    print("🚨 TEST ULTRA-SIMPLE POUR IDENTIFIER LE PROBLÈME")
    print("=" * 70)
    print("🎯 Objectif: Trouver pourquoi TOUT retourne 422")
    print("=" * 70)
    
    # Vérifier Flask
    if not check_flask_status():
        return
    
    # Test connexion
    token = test_login_step_by_step()
    
    if not token:
        print("\n❌ PROBLÈME PRINCIPAL: CONNEXION IMPOSSIBLE")
        print("💡 Vérifiez:")
        print("  - L'utilisateur lin@gmail.com existe")
        print("  - Le mot de passe est correct")
        print("  - La route /api/auth/login fonctionne")
        return
    
    # Tests GET
    appointments_get = test_simple_get_request(token, "/api/appointments/", "GET APPOINTMENTS")
    documents_get = test_simple_get_request(token, "/api/documents/", "GET DOCUMENTS")
    
    # Test POST
    appointment_post = test_simple_post_appointment(token)
    
    # Résumé
    print(f"\n📊 RÉSUMÉ ULTRA-SIMPLE")
    print("=" * 70)
    print(f"🌐 Flask: ✅ OK")
    print(f"🔑 Login: ✅ OK")
    print(f"📥 GET Appointments: {'✅ OK' if appointments_get else '❌ ERREUR 422'}")
    print(f"📥 GET Documents: {'✅ OK' if documents_get else '❌ ERREUR 422'}")
    print(f"📤 POST Appointment: {'✅ OK' if appointment_post else '❌ ERREUR 422'}")
    
    if not appointments_get and not documents_get and not appointment_post:
        print("\n🚨 PROBLÈME SYSTÉMIQUE!")
        print("💡 TOUTES les routes API retournent 422")
        print("💡 Causes possibles:")
        print("  1. Problème dans les modèles (to_dict())")
        print("  2. Problème dans les routes (validation)")
        print("  3. Problème de base de données")
        print("  4. Import ou dépendance manquante")
        print("\n🔧 SOLUTION:")
        print("  1. Vérifiez les logs Flask dans la console")
        print("  2. Cherchez les erreurs Python")
        print("  3. Exécutez: python emergency_repair.py")
    elif appointments_get or documents_get or appointment_post:
        print("\n🎉 CERTAINES ROUTES FONCTIONNENT!")
        print("💡 Le problème est spécifique à certaines routes")
    else:
        print("\n❌ PROBLÈME PERSISTANT")
        print("💡 Vérifiez les logs Flask pour l'erreur exacte")

if __name__ == "__main__":
    main()
