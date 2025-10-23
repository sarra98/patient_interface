#!/usr/bin/env python3
"""
Test du système de paiement complet
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
            print(f"❌ Connexion échouée: {response.status_code}")
            return None
            
    except Exception as e:
        print(f"❌ Erreur connexion: {str(e)}")
        return None

def create_test_appointment(token):
    """Créer un RDV de test pour le paiement"""
    print("\n🔍 CRÉATION RDV DE TEST")
    print("=" * 50)
    
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    
    # Créer un RDV pour demain
    tomorrow = datetime.now() + timedelta(days=1)
    while tomorrow.weekday() == 6:  # Éviter dimanche
        tomorrow += timedelta(days=1)
    
    appointment_data = {
        "medecin_id": 1,
        "date_rdv": f"{tomorrow.strftime('%Y-%m-%d')}T15:00:00",
        "motif": "Consultation pour test paiement",
        "notes": "RDV créé pour tester le système de paiement"
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/appointments/",
            json=appointment_data,
            headers=headers,
            timeout=30
        )
        
        if response.status_code == 201:
            result = response.json()
            appointment = result.get('appointment', {})
            appointment_id = appointment.get('id')
            print(f"✅ RDV créé avec ID: {appointment_id}")
            return appointment_id
        else:
            print(f"❌ Erreur création RDV: {response.status_code}")
            return None
            
    except Exception as e:
        print(f"❌ Exception: {str(e)}")
        return None

def test_payment_bancaire(token, appointment_id):
    """Tester le paiement bancaire"""
    print(f"\n💳 TEST PAIEMENT BANCAIRE")
    print("=" * 50)
    
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    
    payment_data = {
        "mode_paiement": "bancaire"
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/appointments/{appointment_id}/payment",
            json=payment_data,
            headers=headers,
            timeout=30
        )
        
        print(f"📥 Status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Paiement bancaire réussi!")
            print(f"📋 Message: {result.get('message')}")
            print(f"🔗 Référence: {result.get('reference')}")
            print(f"💰 Montant: {result.get('montant')}€")
            print(f"📱 SMS envoyé: {result.get('sms_envoye')}")
            return True
        else:
            print(f"❌ Erreur: {response.status_code}")
            try:
                error = response.json()
                print(f"💬 Détails: {error}")
            except:
                print(f"💬 Réponse: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Exception: {str(e)}")
        return False

def test_payment_sur_place(token, appointment_id):
    """Tester le paiement sur place"""
    print(f"\n🏥 TEST PAIEMENT SUR PLACE")
    print("=" * 50)
    
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    
    payment_data = {
        "mode_paiement": "sur_place"
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/appointments/{appointment_id}/payment",
            json=payment_data,
            headers=headers,
            timeout=30
        )
        
        print(f"📥 Status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Paiement sur place programmé!")
            print(f"📋 Message: {result.get('message')}")
            print(f"💰 Montant: {result.get('montant')}€")
            print(f"📝 Note: {result.get('note')}")
            return True
        else:
            print(f"❌ Erreur: {response.status_code}")
            try:
                error = response.json()
                print(f"💬 Détails: {error}")
            except:
                print(f"💬 Réponse: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Exception: {str(e)}")
        return False

def test_get_appointments_with_payment(token):
    """Tester la récupération des RDV avec infos de paiement"""
    print(f"\n📋 TEST RÉCUPÉRATION RDV AVEC PAIEMENT")
    print("=" * 50)
    
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
        
        if response.status_code == 200:
            result = response.json()
            appointments = result.get('appointments', [])
            print(f"✅ {len(appointments)} RDV récupérés")
            
            for rdv in appointments[:3]:  # Afficher les 3 premiers
                print(f"\n📅 RDV ID: {rdv.get('id')}")
                print(f"  📝 Motif: {rdv.get('motif')}")
                print(f"  📊 Statut: {rdv.get('statut')}")
                print(f"  💳 Statut paiement: {rdv.get('statut_paiement', 'N/A')}")
                print(f"  💰 Mode paiement: {rdv.get('mode_paiement', 'N/A')}")
                print(f"  💵 Montant: {rdv.get('montant', 'N/A')}€")
                print(f"  ✅ Confirmé: {rdv.get('paiement_confirme', False)}")
            
            return True
        else:
            print(f"❌ Erreur: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Exception: {str(e)}")
        return False

def main():
    """Test complet du système de paiement"""
    print("🚀 TEST SYSTÈME DE PAIEMENT COMPLET")
    print("=" * 70)
    print("💳 Bancaire + Sur place + Récupération")
    print("=" * 70)
    
    # Obtenir le token
    token = get_auth_token()
    if not token:
        print("❌ Impossible d'obtenir le token")
        return
    
    # Créer un RDV de test
    appointment_id = create_test_appointment(token)
    if not appointment_id:
        print("❌ Impossible de créer un RDV de test")
        return
    
    # Tester paiement bancaire
    bancaire_ok = test_payment_bancaire(token, appointment_id)
    
    # Créer un autre RDV pour tester paiement sur place
    appointment_id_2 = create_test_appointment(token)
    sur_place_ok = False
    if appointment_id_2:
        sur_place_ok = test_payment_sur_place(token, appointment_id_2)
    
    # Tester récupération avec infos paiement
    get_ok = test_get_appointments_with_payment(token)
    
    # Résumé
    print(f"\n📊 RÉSUMÉ TEST PAIEMENT")
    print("=" * 70)
    print(f"🔑 Connexion: ✅ OK")
    print(f"📅 Création RDV: ✅ OK")
    print(f"💳 Paiement bancaire: {'✅ OK' if bancaire_ok else '❌ ERREUR'}")
    print(f"🏥 Paiement sur place: {'✅ OK' if sur_place_ok else '❌ ERREUR'}")
    print(f"📋 Récupération: {'✅ OK' if get_ok else '❌ ERREUR'}")
    
    if bancaire_ok and sur_place_ok and get_ok:
        print("\n🎉 SYSTÈME DE PAIEMENT OPÉRATIONNEL!")
        print("\nFONCTIONNALITÉS DISPONIBLES:")
        print("💳 Paiement en ligne par carte bancaire")
        print("🏥 Paiement sur place lors de la consultation")
        print("📱 SMS de confirmation automatique")
        print("📋 Suivi du statut de paiement")
        print("🔗 Références de transaction")
        print("\nTESTEZ DANS L'INTERFACE:")
        print("🌐 http://localhost:5000/appointments")
        print("🔑 test@example.com / test123")
    else:
        print("\n❌ PROBLÈMES DÉTECTÉS")
        print("💡 Vérifiez les logs Flask pour plus de détails")
    
    return bancaire_ok and sur_place_ok and get_ok

if __name__ == "__main__":
    main()
