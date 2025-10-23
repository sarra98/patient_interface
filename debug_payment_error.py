#!/usr/bin/env python3
"""
Déboguer l'erreur 400 du paiement
"""

import requests
import json

BASE_URL = "http://localhost:5000"

def get_token():
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
            return response.json().get('access_token')
        else:
            print(f"Erreur connexion: {response.status_code}")
            return None
            
    except Exception as e:
        print(f"Exception connexion: {str(e)}")
        return None

def test_payment_api(token, appointment_id):
    """Tester l'API de paiement directement"""
    print(f"TEST API PAIEMENT RDV {appointment_id}")
    print("=" * 50)
    
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    
    # Test 1: Paiement simple sans carte
    print("1. Test paiement simple:")
    simple_data = {
        "mode_paiement": "bancaire"
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/appointments/{appointment_id}/payment",
            json=simple_data,
            headers=headers,
            timeout=30
        )
        
        print(f"Status: {response.status_code}")
        print(f"Réponse: {response.text}")
        
        if response.status_code != 200:
            print("❌ Paiement simple échoué")
        else:
            print("✅ Paiement simple réussi")
            return True
            
    except Exception as e:
        print(f"Exception: {str(e)}")
    
    # Test 2: Paiement avec données carte
    print("\n2. Test paiement avec carte:")
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
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/appointments/{appointment_id}/payment",
            json=card_data,
            headers=headers,
            timeout=30
        )
        
        print(f"Status: {response.status_code}")
        print(f"Réponse: {response.text}")
        
        if response.status_code == 200:
            print("✅ Paiement avec carte réussi")
            return True
        else:
            print("❌ Paiement avec carte échoué")
            
    except Exception as e:
        print(f"Exception: {str(e)}")
    
    return False

def check_rdv_status(token, appointment_id):
    """Vérifier le statut du RDV"""
    print(f"\nVÉRIFICATION STATUT RDV {appointment_id}")
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
            
            for rdv in appointments:
                if rdv.get('id') == appointment_id:
                    print(f"RDV trouvé:")
                    print(f"  ID: {rdv.get('id')}")
                    print(f"  Statut: {rdv.get('statut')}")
                    print(f"  Statut paiement: {rdv.get('statut_paiement')}")
                    print(f"  Montant: {rdv.get('montant')}")
                    print(f"  Mode paiement: {rdv.get('mode_paiement')}")
                    return rdv
            
            print(f"❌ RDV {appointment_id} non trouvé")
        else:
            print(f"❌ Erreur récupération RDV: {response.status_code}")
            
    except Exception as e:
        print(f"Exception: {str(e)}")
    
    return None

def main():
    """Test principal"""
    print("🚨 DÉBOGAGE ERREUR PAIEMENT 400")
    print("=" * 60)
    
    # Obtenir le token
    token = get_token()
    if not token:
        print("❌ Impossible d'obtenir le token")
        return
    
    print("✅ Token obtenu")
    
    # Utiliser le RDV ID 14 mentionné dans l'erreur
    appointment_id = 14
    
    # Vérifier le statut du RDV avant paiement
    rdv_before = check_rdv_status(token, appointment_id)
    
    if not rdv_before:
        print(f"❌ RDV {appointment_id} non trouvé, créons-en un nouveau")
        # Ici on pourrait créer un nouveau RDV
        return
    
    # Tester l'API de paiement
    payment_ok = test_payment_api(token, appointment_id)
    
    # Vérifier le statut après paiement
    if payment_ok:
        rdv_after = check_rdv_status(token, appointment_id)
        
        print(f"\n📊 COMPARAISON AVANT/APRÈS:")
        print(f"Avant - Statut paiement: {rdv_before.get('statut_paiement')}")
        print(f"Après - Statut paiement: {rdv_after.get('statut_paiement') if rdv_after else 'N/A'}")
    
    print(f"\n💡 SOLUTION:")
    if payment_ok:
        print("✅ L'API fonctionne, le problème vient du JavaScript")
        print("🔧 Vérifiez la fonction processSelectedPayment()")
    else:
        print("❌ L'API ne fonctionne pas")
        print("🔧 Vérifiez la route /payment dans Flask")

if __name__ == "__main__":
    main()
