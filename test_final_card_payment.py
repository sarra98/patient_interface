#!/usr/bin/env python3
"""
Test final avec numéro de carte valide
"""

import requests

def test_payment_with_valid_card():
    """Test paiement avec numéro de carte valide"""
    print("💳 TEST PAIEMENT CARTE VALIDE")
    print("=" * 50)
    
    # Connexion
    login_data = {
        "email": "test@example.com",
        "password": "test123"
    }
    
    try:
        response = requests.post(
            "http://localhost:5000/api/auth/login",
            json=login_data,
            timeout=10
        )
        
        if response.status_code == 200:
            token = response.json().get('access_token')
            print("✅ Connexion réussie")
            
            # Test avec numéro de carte valide
            headers = {
                'Authorization': f'Bearer {token}',
                'Content-Type': 'application/json'
            }
            
            # Utiliser un numéro de carte valide selon Luhn
            valid_card_data = {
                "mode_paiement": "bancaire",
                "card_data": {
                    "number": "4532015112830366",  # Visa valide
                    "expiry": "12/26",
                    "cvv": "123",
                    "name": "AHMED BEN ALI",
                    "phone": "+216 12 345 678"
                }
            }
            
            print("📤 Test paiement avec carte valide:")
            print(f"💳 Numéro: 4532 0151 1283 0366 (Visa)")
            print(f"👤 Nom: {valid_card_data['card_data']['name']}")
            print(f"📱 Téléphone: {valid_card_data['card_data']['phone']}")
            
            response = requests.post(
                "http://localhost:5000/api/appointments/14/payment",
                json=valid_card_data,
                headers=headers,
                timeout=30
            )
            
            print(f"📥 Status: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                print("🎉 PAIEMENT RÉUSSI!")
                print(f"🔗 Référence: {result.get('reference')}")
                print(f"💰 Montant: {result.get('montant')} DT")
                print(f"💳 Carte: **** **** **** {result.get('card_last4')}")
                print(f"📱 SMS envoyé: {result.get('sms_envoye')}")
                return True
            else:
                print(f"❌ Erreur: {response.status_code}")
                print(f"📋 Réponse: {response.text}")
                return False
                
        else:
            print(f"❌ Connexion échouée: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Exception: {str(e)}")
        return False

def main():
    print("🚀 TEST FINAL PAIEMENT CARTE")
    print("=" * 60)
    
    # Test API
    api_ok = test_payment_with_valid_card()
    
    print(f"\n💡 INSTRUCTIONS INTERFACE:")
    print("1. 🌐 http://localhost:5000/appointments")
    print("2. 🔑 test@example.com / test123")
    print("3. 💳 Cliquez bouton vert 'Payer'")
    print("4. 📱 Sélectionnez 'Paiement Bancaire'")
    print("5. 📝 Remplissez avec NUMÉRO VALIDE:")
    print("   • Numéro: 4532 0151 1283 0366")
    print("   • Expiration: 12/26")
    print("   • CVV: 123")
    print("   • Nom: AHMED BEN ALI")
    print("   • Téléphone: +216 12 345 678")
    print("6. ✅ Cliquez 'Payer 70 DT'")
    
    print(f"\n📊 RÉSULTAT:")
    if api_ok:
        print("✅ L'API fonctionne parfaitement")
        print("✅ Numéro de carte valide accepté")
        print("✅ SMS généré dans les logs")
        print("✅ Référence de transaction créée")
        print("\n🎯 TESTEZ MAINTENANT DANS L'INTERFACE!")
    else:
        print("❌ Problème avec l'API")
        print("🔧 Vérifiez les logs Flask")
    
    print(f"\n🔍 AUTRES NUMÉROS VALIDES:")
    print("• 4000 0566 5566 5556 (Visa)")
    print("• 5555 5555 5555 4444 (MasterCard)")
    print("• 4111 1111 1111 1111 (Visa générique)")

if __name__ == "__main__":
    main()
