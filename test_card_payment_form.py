#!/usr/bin/env python3
"""
Test du formulaire de carte bancaire avec SMS
"""

import requests
from datetime import datetime, timedelta

BASE_URL = "http://localhost:5000"

def create_rdv_for_card_test():
    """Créer un RDV pour tester le formulaire de carte"""
    print("💳 CRÉATION RDV POUR TEST FORMULAIRE CARTE")
    print("=" * 60)
    
    # Connexion
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
        
        if response.status_code != 200:
            print("❌ Connexion impossible")
            return None
        
        token = response.json().get('access_token')
        print("✅ Connexion réussie")
        
        # Créer un RDV
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }
        
        tomorrow = datetime.now() + timedelta(days=1)
        while tomorrow.weekday() == 6:  # Éviter dimanche
            tomorrow += timedelta(days=1)
        
        appointment_data = {
            "medecin_id": 1,
            "date_rdv": f"{tomorrow.strftime('%Y-%m-%d')}T19:00:00",
            "motif": "Test formulaire carte bancaire",
            "notes": "RDV pour tester le formulaire de paiement par carte"
        }
        
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
            return appointment_id, token
        else:
            print(f"❌ Erreur création RDV: {response.status_code}")
            return None, None
            
    except Exception as e:
        print(f"❌ Exception: {str(e)}")
        return None, None

def test_card_payment_with_sms(token, appointment_id):
    """Tester le paiement par carte avec SMS"""
    print(f"\n💳 TEST PAIEMENT CARTE AVEC SMS")
    print("=" * 60)
    
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    
    # Données de carte de test
    card_payment_data = {
        "mode_paiement": "bancaire",
        "card_data": {
            "number": "4532123456789012",  # Numéro Visa de test
            "expiry": "12/26",
            "cvv": "123",
            "name": "AHMED BEN ALI",
            "phone": "+216 12 345 678"
        }
    }
    
    print("📤 Envoi paiement avec données carte:")
    print(f"💳 Carte: **** **** **** {card_payment_data['card_data']['number'][-4:]}")
    print(f"👤 Nom: {card_payment_data['card_data']['name']}")
    print(f"📱 Téléphone: {card_payment_data['card_data']['phone']}")
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/appointments/{appointment_id}/payment",
            json=card_payment_data,
            headers=headers,
            timeout=30
        )
        
        print(f"📥 Status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"🎉 PAIEMENT PAR CARTE RÉUSSI!")
            print(f"📋 Message: {result.get('message')}")
            print(f"🔗 Référence: {result.get('reference')}")
            print(f"💰 Montant: {result.get('montant')} {result.get('devise', 'DT')}")
            print(f"💳 Carte: **** **** **** {result.get('card_last4')}")
            print(f"📱 SMS envoyé: {result.get('sms_envoye')}")
            print(f"📞 Téléphone masqué: {result.get('phone_masked')}")
            print(f"⏰ Heure: {result.get('transaction_time')}")
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

def show_card_form_instructions(appointment_id):
    """Afficher les instructions pour le formulaire de carte"""
    print(f"\n🌐 INSTRUCTIONS FORMULAIRE CARTE BANCAIRE")
    print("=" * 60)
    print("1. 🌐 Allez sur: http://localhost:5000/appointments")
    print("2. 🔑 Connectez-vous: test@example.com / test123")
    print("3. 📋 Cherchez le RDV avec:")
    print(f"   🆔 ID: {appointment_id}")
    print("   📝 Motif: Test formulaire carte bancaire")
    print("4. 💳 Cliquez sur le bouton vert 'Payer' dans Actions")
    print("5. 📱 Dans la modal, cliquez sur 'Paiement Bancaire'")
    print("6. 💳 FORMULAIRE DE CARTE S'AFFICHE:")
    print("   📝 Numéro de carte: 4532 1234 5678 9012")
    print("   📅 Expiration: 12/26")
    print("   🔒 CVV: 123")
    print("   👤 Nom: AHMED BEN ALI")
    print("   📱 Téléphone: +216 12 345 678")
    print("7. ✅ Cliquez 'Payer 70 DT'")
    print("8. 📱 SMS de confirmation sera affiché dans les logs")
    
    print(f"\n💡 FONCTIONNALITÉS DU FORMULAIRE:")
    print("✅ Formatage automatique du numéro de carte")
    print("✅ Validation en temps réel")
    print("✅ Masquage sécurisé des données")
    print("✅ Simulation de traitement bancaire")
    print("✅ SMS de confirmation détaillé")
    print("✅ Référence de transaction unique")

def main():
    """Test principal du formulaire de carte"""
    print("🚀 TEST FORMULAIRE CARTE BANCAIRE + SMS")
    print("=" * 70)
    print("💳 Formulaire complet + SMS de confirmation")
    print("=" * 70)
    
    # Créer un RDV de test
    appointment_id, token = create_rdv_for_card_test()
    
    if not appointment_id:
        print("❌ Impossible de créer un RDV de test")
        print("💡 Vérifiez que Flask tourne: python app.py")
        return
    
    # Tester le paiement par carte avec SMS
    card_ok = test_card_payment_with_sms(token, appointment_id)
    
    # Afficher les instructions
    show_card_form_instructions(appointment_id)
    
    print(f"\n📊 RÉSUMÉ TEST FORMULAIRE CARTE")
    print("=" * 70)
    print(f"📅 RDV créé: ✅ ID {appointment_id}")
    print(f"💳 Paiement carte: {'✅ RÉUSSI' if card_ok else '❌ ERREUR'}")
    
    if card_ok:
        print("\n🎉 FORMULAIRE CARTE OPÉRATIONNEL!")
        print("\n✅ FONCTIONNALITÉS DISPONIBLES:")
        print("💳 Formulaire de carte sécurisé")
        print("📝 Validation automatique des champs")
        print("🔒 Formatage et masquage des données")
        print("📱 SMS de confirmation détaillé")
        print("🔗 Référence de transaction unique")
        print("⏰ Horodatage précis")
        print("🇹🇳 Montant en dinars tunisiens")
        
        print("\n🌐 TESTEZ MAINTENANT DANS L'INTERFACE:")
        print("1. Ouvrez: http://localhost:5000/appointments")
        print("2. Cliquez sur le bouton vert 'Payer'")
        print("3. Sélectionnez 'Paiement Bancaire'")
        print("4. Remplissez le formulaire de carte")
        print("5. Confirmez le paiement")
        print("6. Vérifiez le SMS dans les logs Flask")
    else:
        print("\n❌ PROBLÈME DÉTECTÉ")
        print("💡 Vérifiez les logs Flask pour plus de détails")

if __name__ == "__main__":
    main()
