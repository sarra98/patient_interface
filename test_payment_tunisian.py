#!/usr/bin/env python3
"""
Test du système de paiement en dinars tunisiens (70 DT)
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
            print("✅ Connexion réussie")
            return token
        else:
            print(f"❌ Connexion échouée: {response.status_code}")
            return None
            
    except Exception as e:
        print(f"❌ Erreur connexion: {str(e)}")
        return None

def create_rdv_for_payment(token):
    """Créer un RDV pour tester le paiement"""
    print("\n📅 CRÉATION RDV POUR PAIEMENT")
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
        "date_rdv": f"{tomorrow.strftime('%Y-%m-%d')}T16:00:00",
        "motif": "Consultation - Test paiement 70 DT",
        "notes": "RDV pour tester paiement en dinars tunisiens"
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
            print(f"📝 Motif: {appointment.get('motif')}")
            print(f"📅 Date: {appointment.get('date_rdv')}")
            return appointment_id
        else:
            print(f"❌ Erreur création RDV: {response.status_code}")
            return None
            
    except Exception as e:
        print(f"❌ Exception: {str(e)}")
        return None

def test_paiement_bancaire_70dt(token, appointment_id):
    """Tester le paiement bancaire 70 DT"""
    print(f"\n💳 TEST PAIEMENT BANCAIRE 70 DT")
    print("=" * 50)
    
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    
    payment_data = {
        "mode_paiement": "bancaire"
    }
    
    print(f"📤 Paiement bancaire pour RDV ID: {appointment_id}")
    
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
            print(f"🎉 PAIEMENT BANCAIRE RÉUSSI!")
            print(f"📋 Message: {result.get('message')}")
            print(f"🔗 Référence: {result.get('reference')}")
            print(f"💰 Montant: {result.get('montant')} {result.get('devise', 'DT')}")
            print(f"💳 Mode: {result.get('mode')}")
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

def test_paiement_sur_place_70dt(token, appointment_id):
    """Tester le paiement sur place 70 DT"""
    print(f"\n🏥 TEST PAIEMENT SUR PLACE 70 DT")
    print("=" * 50)
    
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    
    payment_data = {
        "mode_paiement": "sur_place"
    }
    
    print(f"📤 Paiement sur place pour RDV ID: {appointment_id}")
    
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
            print(f"🎉 PAIEMENT SUR PLACE PROGRAMMÉ!")
            print(f"📋 Message: {result.get('message')}")
            print(f"💰 Montant: {result.get('montant')} {result.get('devise', 'DT')}")
            print(f"🏥 Mode: {result.get('mode')}")
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

def show_payment_instructions():
    """Afficher les instructions pour utiliser le paiement dans l'interface"""
    print(f"\n🌐 INSTRUCTIONS INTERFACE WEB")
    print("=" * 50)
    print("1. 🌐 Allez sur: http://localhost:5000/appointments")
    print("2. 🔑 Connectez-vous: test@example.com / test123")
    print("3. 📅 Créez un RDV via: http://localhost:5000/book-appointment")
    print("4. 📋 Dans la liste des RDV, vous verrez:")
    print("   💳 Colonne 'Paiement' avec montant '70 DT'")
    print("   🔵 Bouton 'Bancaire' pour paiement en ligne")
    print("   🟢 Bouton 'Sur place' pour paiement différé")
    print("5. 💳 Cliquez sur 'Bancaire' pour:")
    print("   ✅ Paiement immédiat par carte")
    print("   📱 SMS de confirmation automatique")
    print("   🔗 Référence de transaction")
    print("6. 🏥 Cliquez sur 'Sur place' pour:")
    print("   📝 Programmer le paiement lors de la consultation")
    print("   ⏰ Paiement différé à 70 DT")

def main():
    """Test complet paiement tunisien"""
    print("🇹🇳 TEST PAIEMENT 70 DINARS TUNISIENS")
    print("=" * 70)
    print("💳 Bancaire + Sur place en DT")
    print("=" * 70)
    
    # Connexion
    token = get_auth_token()
    if not token:
        print("❌ Impossible de se connecter")
        return
    
    # Créer 2 RDV pour tester les 2 modes de paiement
    rdv_bancaire = create_rdv_for_payment(token)
    rdv_sur_place = create_rdv_for_payment(token)
    
    if not rdv_bancaire or not rdv_sur_place:
        print("❌ Impossible de créer les RDV de test")
        return
    
    # Tester paiement bancaire
    bancaire_ok = test_paiement_bancaire_70dt(token, rdv_bancaire)
    
    # Tester paiement sur place
    sur_place_ok = test_paiement_sur_place_70dt(token, rdv_sur_place)
    
    # Afficher les instructions
    show_payment_instructions()
    
    # Résumé
    print(f"\n📊 RÉSUMÉ PAIEMENT TUNISIEN")
    print("=" * 70)
    print(f"🔑 Connexion: ✅ OK")
    print(f"📅 Création RDV: ✅ OK")
    print(f"💳 Paiement bancaire 70 DT: {'✅ OK' if bancaire_ok else '❌ ERREUR'}")
    print(f"🏥 Paiement sur place 70 DT: {'✅ OK' if sur_place_ok else '❌ ERREUR'}")
    
    if bancaire_ok and sur_place_ok:
        print("\n🎉 SYSTÈME PAIEMENT 70 DT OPÉRATIONNEL!")
        print("\n💰 TARIFS:")
        print("🏥 Consultation: 70 Dinars Tunisiens")
        print("💳 Paiement bancaire: Immédiat avec SMS")
        print("🏥 Paiement sur place: Lors de la consultation")
        print("\n🌐 TESTEZ MAINTENANT DANS L'INTERFACE!")
    else:
        print("\n❌ PROBLÈMES DÉTECTÉS")
        print("💡 Vérifiez les logs Flask")
    
    return bancaire_ok and sur_place_ok

if __name__ == "__main__":
    main()
