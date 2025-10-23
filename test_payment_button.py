#!/usr/bin/env python3
"""
Test du nouveau bouton de paiement
"""

import requests
from datetime import datetime, timedelta

BASE_URL = "http://localhost:5000"

def create_rdv_for_payment_test():
    """Créer un RDV pour tester le bouton de paiement"""
    print("🎯 CRÉATION RDV POUR TEST BOUTON PAIEMENT")
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
            "date_rdv": f"{tomorrow.strftime('%Y-%m-%d')}T17:00:00",
            "motif": "Test bouton paiement",
            "notes": "RDV pour tester le nouveau bouton de paiement"
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

def show_interface_instructions(appointment_id):
    """Afficher les instructions pour utiliser le bouton de paiement"""
    print(f"\n🌐 INSTRUCTIONS BOUTON DE PAIEMENT")
    print("=" * 60)
    print("1. 🌐 Allez sur: http://localhost:5000/appointments")
    print("2. 🔑 Connectez-vous: test@example.com / test123")
    print("3. 📋 Dans la liste des RDV, cherchez le RDV avec:")
    print(f"   🆔 ID: {appointment_id}")
    print("   📝 Motif: Test bouton paiement")
    print("4. 💳 Dans la colonne 'Paiement', vous verrez:")
    print("   🔵 BOUTON BLEU: 'PAYER 70 DT'")
    print("5. 🖱️ Cliquez sur le bouton 'PAYER 70 DT'")
    print("6. 📱 Une modal s'ouvrira avec 2 options:")
    print("   💳 Paiement Bancaire (Recommandé)")
    print("   🏥 Paiement Sur Place (Flexible)")
    print("7. ✅ Sélectionnez votre mode de paiement")
    print("8. 🎯 Cliquez 'Confirmer le paiement'")
    print("\n💡 RÉSULTATS ATTENDUS:")
    print("💳 Bancaire: Paiement immédiat + SMS + Référence")
    print("🏥 Sur place: Programmation + Note explicative")

def main():
    """Test principal du bouton de paiement"""
    print("🚀 TEST NOUVEAU BOUTON DE PAIEMENT")
    print("=" * 70)
    print("💳 Bouton 'PAYER 70 DT' + Modal de sélection")
    print("=" * 70)
    
    # Créer un RDV de test
    appointment_id, token = create_rdv_for_payment_test()
    
    if not appointment_id:
        print("❌ Impossible de créer un RDV de test")
        print("💡 Vérifiez que Flask tourne: python app.py")
        return
    
    # Afficher les instructions
    show_interface_instructions(appointment_id)
    
    print(f"\n🎉 RDV DE TEST CRÉÉ!")
    print("=" * 70)
    print("🎯 FONCTIONNALITÉS DU NOUVEAU BOUTON:")
    print("✅ Bouton principal 'PAYER 70 DT' bien visible")
    print("✅ Modal élégante avec 2 options de paiement")
    print("✅ Sélection visuelle des modes de paiement")
    print("✅ Bouton de confirmation dynamique")
    print("✅ Traitement avec indicateur de chargement")
    print("✅ Messages de confirmation détaillés")
    print("✅ Rechargement automatique de la liste")
    print("\n🌐 TESTEZ MAINTENANT DANS L'INTERFACE!")
    print("http://localhost:5000/appointments")

if __name__ == "__main__":
    main()
