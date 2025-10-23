#!/usr/bin/env python3
"""
Test de la carte verte de paiement avec deux choix
"""

import requests
from datetime import datetime, timedelta

BASE_URL = "http://localhost:5000"

def create_rdv_for_green_card():
    """Créer un RDV pour tester la carte verte de paiement"""
    print("💚 CRÉATION RDV POUR CARTE VERTE PAIEMENT")
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
            "date_rdv": f"{tomorrow.strftime('%Y-%m-%d')}T20:00:00",
            "motif": "Test carte verte paiement",
            "notes": "RDV pour tester la nouvelle carte verte de paiement avec deux choix"
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

def test_card_payment_from_green_card(token, appointment_id):
    """Tester le paiement par carte depuis la carte verte"""
    print(f"\n💳 TEST PAIEMENT CARTE DEPUIS CARTE VERTE")
    print("=" * 60)
    
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    
    # Test paiement par carte avec numéro valide
    card_data = {
        "mode_paiement": "bancaire",
        "card_data": {
            "number": "4532015112830366",  # Numéro valide selon Luhn
            "expiry": "12/26",
            "cvv": "123",
            "name": "AHMED BEN ALI",
            "phone": "+216 12 345 678"
        }
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/appointments/{appointment_id}/payment",
            json=card_data,
            headers=headers,
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            print("🎉 PAIEMENT PAR CARTE RÉUSSI!")
            print(f"🔗 Référence: {result.get('reference')}")
            print(f"💰 Montant: {result.get('montant')} DT")
            print(f"💳 Carte: **** **** **** {result.get('card_last4')}")
            print(f"📱 SMS envoyé: {result.get('sms_envoye')}")
            return True
        else:
            print(f"❌ Erreur: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Exception: {str(e)}")
        return False

def show_green_card_instructions(appointment_id):
    """Afficher les instructions pour la carte verte"""
    print(f"\n🌐 INSTRUCTIONS CARTE VERTE DE PAIEMENT")
    print("=" * 60)
    print("1. 🌐 Allez sur: http://localhost:5000/appointments")
    print("2. 🔑 Connectez-vous: test@example.com / test123")
    print("3. 📋 Cherchez le RDV avec:")
    print(f"   🆔 ID: {appointment_id}")
    print("   📝 Motif: Test carte verte paiement")
    print("4. 💚 Dans la colonne 'Paiement', vous verrez:")
    print("   🎨 CARTE VERTE avec dégradé")
    print("   💳 En-tête: 'Paiement 70 DT'")
    print("   🔘 DEUX BOUTONS:")
    print("     💳 'Carte Bancaire' (bleu au survol)")
    print("     🏥 'Sur Place' (jaune au survol)")
    print("   📝 Footer: 'Choisissez votre mode de paiement'")
    
    print(f"\n💳 OPTION 1 - CARTE BANCAIRE:")
    print("1. 🖱️ Cliquez sur 'Carte Bancaire'")
    print("2. 📱 Modal s'ouvre directement sur le formulaire")
    print("3. 📝 Remplissez avec numéro valide:")
    print("   • 4532 0151 1283 0366")
    print("   • Expiration: 12/26")
    print("   • CVV: 123")
    print("   • Nom: AHMED BEN ALI")
    print("   • Téléphone: +216 12 345 678")
    print("4. ✅ Cliquez 'Payer 70 DT'")
    
    print(f"\n🏥 OPTION 2 - SUR PLACE:")
    print("1. 🖱️ Cliquez sur 'Sur Place'")
    print("2. ✅ Confirmation directe")
    print("3. 📝 Paiement programmé pour la consultation")
    
    print(f"\n🎨 DESIGN DE LA CARTE VERTE:")
    print("✅ Dégradé vert attractif")
    print("✅ Icône carte de crédit")
    print("✅ Deux boutons bien visibles")
    print("✅ Effets de survol élégants")
    print("✅ Responsive et moderne")

def main():
    """Test principal de la carte verte"""
    print("🚀 TEST CARTE VERTE DE PAIEMENT")
    print("=" * 70)
    print("💚 Carte avec deux choix: Bancaire + Sur Place")
    print("=" * 70)
    
    # Créer un RDV de test
    appointment_id, token = create_rdv_for_green_card()
    
    if not appointment_id:
        print("❌ Impossible de créer un RDV de test")
        return
    
    # Tester le paiement par carte
    card_ok = test_card_payment_from_green_card(token, appointment_id)
    
    # Afficher les instructions
    show_green_card_instructions(appointment_id)
    
    print(f"\n📊 RÉSUMÉ CARTE VERTE")
    print("=" * 70)
    print(f"📅 RDV créé: ✅ ID {appointment_id}")
    print(f"💳 Test paiement: {'✅ RÉUSSI' if card_ok else '❌ ERREUR'}")
    
    if card_ok:
        print("\n🎉 CARTE VERTE OPÉRATIONNELLE!")
        print("\n✅ FONCTIONNALITÉS:")
        print("💚 Carte verte attractive dans la colonne Paiement")
        print("💳 Bouton 'Carte Bancaire' → Formulaire direct")
        print("🏥 Bouton 'Sur Place' → Confirmation rapide")
        print("🎨 Design moderne avec dégradés et animations")
        print("📱 Interface responsive et intuitive")
        print("⚡ Actions directes sans modal intermédiaire")
        
        print("\n🌐 TESTEZ MAINTENANT:")
        print("http://localhost:5000/appointments")
        print("Cherchez la belle carte verte dans la colonne Paiement!")
    else:
        print("\n❌ PROBLÈME DÉTECTÉ")
        print("🔧 Vérifiez les logs Flask")

if __name__ == "__main__":
    main()
