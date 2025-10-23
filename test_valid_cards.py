#!/usr/bin/env python3
"""
Test avec des numéros de carte valides
"""

def luhn_check(card_number):
    """Vérifier un numéro de carte avec l'algorithme de Luhn"""
    digits = [int(d) for d in card_number.replace(' ', '')]
    checksum = 0
    is_even = False
    
    for digit in reversed(digits):
        if is_even:
            digit *= 2
            if digit > 9:
                digit -= 9
        checksum += digit
        is_even = not is_even
    
    return checksum % 10 == 0

def test_card_numbers():
    """Tester différents numéros de carte"""
    print("🔍 TEST NUMÉROS DE CARTE VALIDES")
    print("=" * 50)
    
    test_cards = [
        ("4532015112830366", "Visa Test 1"),
        ("4000056655665556", "Visa Test 2"), 
        ("5555555555554444", "MasterCard Test 1"),
        ("5105105105105100", "MasterCard Test 2"),
        ("4532123456789012", "Notre numéro test"),
        ("4111111111111111", "Visa générique"),
        ("4242424242424242", "Stripe test")
    ]
    
    print("Numéros de carte valides selon Luhn:")
    for card, name in test_cards:
        is_valid = luhn_check(card)
        status = "✅ VALIDE" if is_valid else "❌ INVALIDE"
        formatted = f"{card[:4]} {card[4:8]} {card[8:12]} {card[12:]}"
        print(f"{status} - {formatted} ({name})")
    
    print(f"\n💳 INSTRUCTIONS POUR TESTER:")
    print("1. Allez sur: http://localhost:5000/appointments")
    print("2. Cliquez sur bouton vert 'Payer'")
    print("3. Sélectionnez 'Paiement Bancaire'")
    print("4. Utilisez UN DE CES NUMÉROS VALIDES:")
    print("   • 4532 0151 1283 0366 (Visa)")
    print("   • 4000 0566 5566 5556 (Visa)")
    print("   • 5555 5555 5555 4444 (MasterCard)")
    print("   • 5105 5105 5105 5100 (MasterCard)")
    print("5. Autres champs:")
    print("   • Expiration: 12/26")
    print("   • CVV: 123")
    print("   • Nom: AHMED BEN ALI")
    print("   • Téléphone: +216 12 345 678")
    print("6. Cliquez 'Payer 70 DT'")
    
    print(f"\n🎯 RÉSULTAT ATTENDU:")
    print("✅ Validation réussie")
    print("✅ Paiement traité")
    print("✅ SMS dans les logs Flask")
    print("✅ Statut mis à jour: 'Payé (70 DT)'")

if __name__ == "__main__":
    test_card_numbers()
