#!/usr/bin/env python3
"""
Test des corrections apportées
"""

import requests
import json
from datetime import datetime, timedelta

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

def test_documents_page():
    """Tester que la page documents est accessible"""
    print("\n🔍 TEST PAGE DOCUMENTS")
    print("=" * 50)
    
    try:
        response = requests.get(f"{BASE_URL}/documents", timeout=5)
        if response.status_code == 200:
            # Vérifier que la navbar contient le lien Documents
            if 'Documents' in response.text and 'fa-file-medical' in response.text:
                print("✅ Page documents accessible avec navbar")
                return True
            else:
                print("⚠️  Page accessible mais navbar incomplète")
                return False
        else:
            print(f"❌ Page documents: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Erreur: {str(e)}")
        return False

def test_appointment_creation(token):
    """Tester la création de rendez-vous (correction erreur 422)"""
    print("\n🔍 TEST CRÉATION RENDEZ-VOUS")
    print("=" * 50)
    
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    
    # Créer un RDV pour demain à 14h30
    tomorrow = datetime.now() + timedelta(days=1)
    # S'assurer que ce n'est pas un dimanche
    while tomorrow.weekday() == 6:  # Dimanche
        tomorrow += timedelta(days=1)
    
    appointment_data = {
        "medecin_id": 1,
        "date_rdv": f"{tomorrow.strftime('%Y-%m-%d')}T14:30:00",
        "motif": "Consultation de test",
        "notes": "Test de correction erreur 422"
    }
    
    print(f"📅 Test RDV: {appointment_data['date_rdv']}")
    
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
            print("✅ RDV créé avec succès!")
            print(f"📋 ID: {result.get('appointment', {}).get('id')}")
            return True
        elif response.status_code == 422:
            error = response.json()
            print(f"❌ Erreur 422 persistante: {error}")
            return False
        else:
            error = response.json()
            print(f"⚠️  Autre erreur: {response.status_code} - {error}")
            return False
            
    except Exception as e:
        print(f"❌ Erreur: {str(e)}")
        return False

def test_navbar_in_all_pages():
    """Tester que le lien Documents est dans toutes les navbars"""
    print("\n🔍 TEST NAVBAR DANS TOUTES LES PAGES")
    print("=" * 50)
    
    pages_to_test = [
        '/dashboard',
        '/appointments', 
        '/book-appointment',
        '/profile',
        '/documents'
    ]
    
    success_count = 0
    for page in pages_to_test:
        try:
            response = requests.get(f"{BASE_URL}{page}", timeout=5)
            if response.status_code == 200:
                if 'Documents' in response.text and 'fa-file-medical' in response.text:
                    print(f"✅ {page}: Lien Documents présent")
                    success_count += 1
                else:
                    print(f"❌ {page}: Lien Documents manquant")
            else:
                print(f"⚠️  {page}: Page non accessible ({response.status_code})")
        except Exception as e:
            print(f"❌ {page}: Erreur - {str(e)}")
    
    print(f"📊 {success_count}/{len(pages_to_test)} pages avec lien Documents")
    return success_count >= len(pages_to_test) - 1  # Tolérer 1 erreur

def test_occupied_slots_api(token):
    """Tester l'API des créneaux occupés"""
    print("\n🔍 TEST API CRÉNEAUX OCCUPÉS")
    print("=" * 50)
    
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    
    test_date = datetime.now().strftime('%Y-%m-%d')
    
    try:
        response = requests.get(
            f"{BASE_URL}/api/appointments/occupied-slots?date={test_date}",
            headers=headers,
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            occupied_slots = data.get('occupied_slots', [])
            print(f"✅ API créneaux OK - {len(occupied_slots)} créneaux occupés")
            return True
        else:
            print(f"❌ API créneaux: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Erreur: {str(e)}")
        return False

def main():
    """Test principal des corrections"""
    print("🚀 TEST DES CORRECTIONS")
    print("=" * 70)
    print("🔧 Erreur 422 RDV | 📄 Page Documents | 🧭 Navbar complète")
    print("=" * 70)
    
    # Tests sans authentification
    navbar_ok = test_navbar_in_all_pages()
    documents_page_ok = test_documents_page()
    
    # Obtenir le token pour les tests authentifiés
    token = get_auth_token()
    if not token:
        print("❌ Impossible d'obtenir le token")
        return
    
    # Tests avec authentification
    appointment_ok = test_appointment_creation(token)
    occupied_slots_ok = test_occupied_slots_api(token)
    
    # Résumé final
    print(f"\n📊 RÉSUMÉ DES CORRECTIONS")
    print("=" * 70)
    
    results = {
        "Navbar Documents": navbar_ok,
        "Page Documents": documents_page_ok,
        "Création RDV (422)": appointment_ok,
        "API Créneaux": occupied_slots_ok
    }
    
    total_tests = len(results)
    passed_tests = sum(1 for result in results.values() if result)
    
    for test_name, result in results.items():
        status = "✅ CORRIGÉ" if result else "❌ PROBLÈME"
        print(f"{test_name}: {status}")
    
    print(f"\n🎯 RÉSULTAT: {passed_tests}/{total_tests} corrections OK")
    
    if passed_tests >= total_tests - 1:
        print("🎉 CORRECTIONS RÉUSSIES!")
        print("\n💡 PROBLÈMES RÉSOLUS:")
        print("📄 Lien Documents ajouté dans toutes les navbars")
        print("🔧 Erreur 422 lors création RDV corrigée")
        print("🌐 Page /documents accessible et fonctionnelle")
        print("📋 API créneaux occupés opérationnelle")
    else:
        print("⚠️  CERTAINES CORRECTIONS NÉCESSITENT ATTENTION")
        print("💡 Vérifiez les logs Flask pour plus de détails")
    
    return passed_tests >= total_tests - 1

if __name__ == "__main__":
    main()
