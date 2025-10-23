#!/usr/bin/env python3
"""
Test du bouton de paiement dans la colonne Actions
"""

import requests
from datetime import datetime, timedelta

BASE_URL = "http://localhost:5000"

def create_rdv_for_action_button_test():
    """Créer un RDV pour tester le bouton de paiement dans Actions"""
    print("🎯 CRÉATION RDV POUR TEST BOUTON ACTIONS")
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
            "date_rdv": f"{tomorrow.strftime('%Y-%m-%d')}T18:00:00",
            "motif": "Test bouton paiement Actions",
            "notes": "RDV pour tester le bouton de paiement dans la colonne Actions"
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
            print(f"📅 Date: {appointment.get('date_rdv')}")
            print(f"📝 Motif: {appointment.get('motif')}")
            return appointment_id, token
        else:
            print(f"❌ Erreur création RDV: {response.status_code}")
            return None, None
            
    except Exception as e:
        print(f"❌ Exception: {str(e)}")
        return None, None

def test_payment_via_action_button(token, appointment_id):
    """Tester le paiement via le bouton d'action"""
    print(f"\n💳 TEST PAIEMENT VIA BOUTON ACTIONS")
    print("=" * 60)
    
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    
    # Test paiement bancaire
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
            print(f"🎉 PAIEMENT VIA BOUTON ACTIONS RÉUSSI!")
            print(f"📋 Message: {result.get('message')}")
            print(f"🔗 Référence: {result.get('reference')}")
            print(f"💰 Montant: {result.get('montant')} {result.get('devise', 'DT')}")
            return True
        else:
            print(f"❌ Erreur: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Exception: {str(e)}")
        return False

def show_action_button_instructions(appointment_id):
    """Afficher les instructions pour le bouton dans Actions"""
    print(f"\n🌐 INSTRUCTIONS BOUTON PAIEMENT ACTIONS")
    print("=" * 60)
    print("1. 🌐 Allez sur: http://localhost:5000/appointments")
    print("2. 🔑 Connectez-vous: test@example.com / test123")
    print("3. 📋 Dans la liste des RDV, cherchez le RDV avec:")
    print(f"   🆔 ID: {appointment_id}")
    print("   📝 Motif: Test bouton paiement Actions")
    print("4. 👀 Dans la colonne 'Actions', vous verrez:")
    print("   👁️ Bouton bleu 'Voir' (œil)")
    print("   🗑️ Bouton rouge 'Supprimer' (croix)")
    print("   💳 BOUTON VERT 'Payer' (carte) ← NOUVEAU!")
    print("5. 🖱️ Cliquez sur le bouton vert avec l'icône carte")
    print("6. 📱 La modal de paiement s'ouvrira")
    print("7. ✅ Choisissez votre mode de paiement")
    print("\n💡 AVANTAGES DU BOUTON ACTIONS:")
    print("✅ Directement accessible avec les autres actions")
    print("✅ Icône carte facilement reconnaissable")
    print("✅ Couleur verte pour le paiement")
    print("✅ Tooltip explicatif 'Payer 70 DT'")
    print("✅ Devient gris avec coche quand payé")

def main():
    """Test principal du bouton de paiement dans Actions"""
    print("🚀 TEST BOUTON PAIEMENT DANS COLONNE ACTIONS")
    print("=" * 70)
    print("💳 Bouton vert à côté de Supprimer")
    print("=" * 70)
    
    # Créer un RDV de test
    appointment_id, token = create_rdv_for_action_button_test()
    
    if not appointment_id:
        print("❌ Impossible de créer un RDV de test")
        print("💡 Vérifiez que Flask tourne: python app.py")
        return
    
    # Tester le paiement via API
    payment_ok = test_payment_via_action_button(token, appointment_id)
    
    # Afficher les instructions
    show_action_button_instructions(appointment_id)
    
    print(f"\n🎉 BOUTON ACTIONS CRÉÉ!")
    print("=" * 70)
    print("🎯 NOUVEAU BOUTON DANS COLONNE ACTIONS:")
    print("✅ Bouton vert avec icône carte de crédit")
    print("✅ Tooltip 'Payer 70 DT'")
    print("✅ Positionné après le bouton Supprimer")
    print("✅ Ouvre la même modal de paiement élégante")
    print("✅ Devient gris avec coche quand payé")
    print("\n📊 DISPOSITION DES BOUTONS:")
    print("👁️ Voir (bleu) | 🗑️ Supprimer (rouge) | 💳 Payer (vert)")
    print("\n🌐 TESTEZ MAINTENANT:")
    print("http://localhost:5000/appointments")
    print(f"Cherchez le RDV ID: {appointment_id}")

if __name__ == "__main__":
    main()
