#!/usr/bin/env python3
"""
Test simple pour déboguer le paiement
"""

import requests

def test_simple_payment():
    """Test simple de paiement"""
    print("🔧 TEST SIMPLE PAIEMENT")
    print("=" * 40)
    
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
            print("✅ Token obtenu")
            
            # Test paiement simple sur RDV 14
            headers = {
                'Authorization': f'Bearer {token}',
                'Content-Type': 'application/json'
            }
            
            payment_data = {
                "mode_paiement": "bancaire"
            }
            
            print("📤 Test paiement RDV 14...")
            
            response = requests.post(
                "http://localhost:5000/api/appointments/14/payment",
                json=payment_data,
                headers=headers,
                timeout=30
            )
            
            print(f"📥 Status: {response.status_code}")
            print(f"📋 Réponse: {response.text}")
            
            if response.status_code == 200:
                print("✅ PAIEMENT RÉUSSI!")
            else:
                print("❌ PAIEMENT ÉCHOUÉ")
                
        else:
            print(f"❌ Connexion échouée: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Erreur: {str(e)}")

def main():
    print("🚨 DÉBOGAGE PAIEMENT")
    print("=" * 50)
    
    test_simple_payment()
    
    print("\n💡 INSTRUCTIONS DÉBOGAGE:")
    print("1. Ouvrez la console du navigateur (F12)")
    print("2. Allez sur: http://localhost:5000/appointments")
    print("3. Cliquez sur un bouton vert 'Payer'")
    print("4. Regardez les logs dans la console:")
    print("   - 🔍 Ouverture modal paiement")
    print("   - 💳 Mode de paiement")
    print("   - 📤 Envoi requête paiement")
    print("   - 📥 Réponse status")
    print("5. Si erreur 400, vérifiez les logs Flask")

if __name__ == "__main__":
    main()
