#!/usr/bin/env python3
"""
Test simple du formulaire de carte
"""

import requests

def test_card_payment():
    print("TEST FORMULAIRE CARTE BANCAIRE")
    print("=" * 50)
    
    # Données de test
    card_data = {
        "mode_paiement": "bancaire",
        "card_data": {
            "number": "4532123456789012",
            "expiry": "12/26", 
            "cvv": "123",
            "name": "AHMED BEN ALI",
            "phone": "+216 12 345 678"
        }
    }
    
    print("Données de carte de test:")
    print(f"Numéro: **** **** **** {card_data['card_data']['number'][-4:]}")
    print(f"Nom: {card_data['card_data']['name']}")
    print(f"Téléphone: {card_data['card_data']['phone']}")
    
    print("\nPOUR TESTER DANS L'INTERFACE:")
    print("1. http://localhost:5000/appointments")
    print("2. Connectez-vous: test@example.com / test123")
    print("3. Cliquez bouton vert 'Payer' sur un RDV")
    print("4. Sélectionnez 'Paiement Bancaire'")
    print("5. Remplissez le formulaire:")
    print("   - Numéro: 4532 1234 5678 9012")
    print("   - Expiration: 12/26")
    print("   - CVV: 123")
    print("   - Nom: AHMED BEN ALI")
    print("   - Téléphone: +216 12 345 678")
    print("6. Cliquez 'Payer 70 DT'")
    print("7. SMS apparaîtra dans les logs Flask")

if __name__ == "__main__":
    test_card_payment()
