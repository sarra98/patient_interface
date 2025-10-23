#!/usr/bin/env python3
"""
Test de la confirmation automatique du RDV par le paiement
"""

import requests
from datetime import datetime, timedelta

BASE_URL = "http://localhost:5000"

def create_planned_rdv():
    """Créer un RDV planifié pour tester la confirmation par paiement"""
    print("📅 CRÉATION RDV PLANIFIÉ POUR TEST CONFIRMATION")
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
            timeout=10
        )
        
        if response.status_code == 200:
            token = response.json().get('access_token')
            print("✅ Connexion réussie")
            
            # Créer un RDV
            headers = {
                'Authorization': f'Bearer {token}',
                'Content-Type': 'application/json'
            }
            
            tomorrow = datetime.now() + timedelta(days=2)
            while tomorrow.weekday() == 6:  # Éviter dimanche
                tomorrow += timedelta(days=1)
            
            appointment_data = {
                "medecin_id": 1,
                "date_rdv": f"{tomorrow.strftime('%Y-%m-%d')}T15:00:00",
                "motif": "Test confirmation par paiement",
                "notes": "RDV planifié qui sera confirmé par le paiement"
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
                statut_initial = appointment.get('statut')
                print(f"✅ RDV créé avec ID: {appointment_id}")
                print(f"📊 Statut initial: {statut_initial}")
                return appointment_id, token, statut_initial
            else:
                print(f"❌ Erreur création RDV: {response.status_code}")
                return None, None, None
                
        else:
            print(f"❌ Connexion échouée: {response.status_code}")
            return None, None, None
            
    except Exception as e:
        print(f"❌ Exception: {str(e)}")
        return None, None, None

def test_payment_confirmation_bancaire(token, appointment_id):
    """Tester la confirmation par paiement bancaire"""
    print(f"\n💳 TEST CONFIRMATION PAR PAIEMENT BANCAIRE")
    print("=" * 60)
    
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    
    # Paiement bancaire avec carte valide
    payment_data = {
        "mode_paiement": "bancaire",
        "card_data": {
            "number": "4532015112830366",
            "expiry": "12/26",
            "cvv": "123",
            "name": "AHMED BEN ALI",
            "phone": "+216 12 345 678"
        }
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/appointments/{appointment_id}/payment",
            json=payment_data,
            headers=headers,
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            print("🎉 PAIEMENT BANCAIRE RÉUSSI!")
            print(f"📋 Message: {result.get('message')}")
            print(f"🔗 Référence: {result.get('reference')}")
            print(f"💰 Montant: {result.get('montant')} DT")
            print(f"📱 SMS envoyé: {result.get('sms_envoye')}")
            
            # Vérifier le statut du RDV après paiement
            return check_rdv_status_after_payment(token, appointment_id)
        else:
            print(f"❌ Erreur: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Exception: {str(e)}")
        return False

def test_payment_confirmation_sur_place(token, appointment_id):
    """Tester la confirmation par paiement sur place"""
    print(f"\n🏥 TEST CONFIRMATION PAR PAIEMENT SUR PLACE")
    print("=" * 60)
    
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    
    # Paiement sur place
    payment_data = {
        "mode_paiement": "sur_place"
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/appointments/{appointment_id}/payment",
            json=payment_data,
            headers=headers,
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            print("🎉 PAIEMENT SUR PLACE PROGRAMMÉ!")
            print(f"📋 Message: {result.get('message')}")
            print(f"💰 Montant: {result.get('montant')} DT")
            print(f"📝 Note: {result.get('note')}")
            print(f"📊 Changement statut: {result.get('statut_change')}")
            
            # Vérifier le statut du RDV après paiement
            return check_rdv_status_after_payment(token, appointment_id)
        else:
            print(f"❌ Erreur: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Exception: {str(e)}")
        return False

def check_rdv_status_after_payment(token, appointment_id):
    """Vérifier le statut du RDV après paiement"""
    print(f"\n🔍 VÉRIFICATION STATUT APRÈS PAIEMENT")
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
                    print(f"📊 RDV {appointment_id} après paiement:")
                    print(f"   Statut RDV: {rdv.get('statut')}")
                    print(f"   Statut paiement: {rdv.get('statut_paiement')}")
                    print(f"   Mode paiement: {rdv.get('mode_paiement')}")
                    print(f"   Référence: {rdv.get('reference_paiement', 'N/A')}")
                    
                    # Vérifier si le RDV est confirmé
                    if rdv.get('statut') == 'confirme':
                        print("✅ RDV CONFIRMÉ PAR LE PAIEMENT!")
                        return True
                    else:
                        print(f"❌ RDV pas confirmé: {rdv.get('statut')}")
                        return False
            
            print(f"❌ RDV {appointment_id} non trouvé")
            return False
        else:
            print(f"❌ Erreur récupération: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Exception: {str(e)}")
        return False

def show_confirmation_instructions():
    """Afficher les instructions pour tester la confirmation"""
    print(f"\n🌐 INSTRUCTIONS CONFIRMATION PAR PAIEMENT")
    print("=" * 60)
    print("1. 🌐 Allez sur: http://localhost:5000/appointments")
    print("2. 🔑 Connectez-vous: test@example.com / test123")
    print("3. 📋 Cherchez les RDV avec statut 'Planifié'")
    print("4. 💳 Cliquez sur le bouton vert 'Confirmer & Payer'")
    print("5. 📱 Dans la modal, vous verrez:")
    print("   📊 'Confirmer le RDV'")
    print("   💰 Montant: 70 DT")
    print("   ℹ️ 'Le paiement confirmera automatiquement votre RDV'")
    print("   📈 'Statut: Planifié → Confirmé après paiement'")
    print("6. 🔘 Choisissez votre mode:")
    print("   💳 Carte Bancaire → Paiement + Confirmation immédiate")
    print("   🏥 Sur Place → Confirmation immédiate + Paiement différé")
    print("7. ✅ Après paiement:")
    print("   📊 Statut RDV: Planifié → Confirmé")
    print("   💳 Statut paiement: En attente → Payé (bancaire) ou En attente (sur place)")

def main():
    """Test principal de la confirmation par paiement"""
    print("🚀 TEST CONFIRMATION RDV PAR PAIEMENT")
    print("=" * 70)
    print("📊 Planifié → Confirmé via paiement")
    print("=" * 70)
    
    # Créer un RDV planifié
    appointment_id, token, statut_initial = create_planned_rdv()
    
    if not appointment_id:
        print("❌ Impossible de créer un RDV de test")
        return
    
    print(f"\n📊 STATUT INITIAL: {statut_initial}")
    
    # Créer un deuxième RDV pour tester les deux modes
    appointment_id2, token2, statut_initial2 = create_planned_rdv()
    
    # Tester paiement bancaire (confirme le RDV)
    if appointment_id:
        bancaire_ok = test_payment_confirmation_bancaire(token, appointment_id)
    
    # Tester paiement sur place (confirme aussi le RDV)
    if appointment_id2:
        sur_place_ok = test_payment_confirmation_sur_place(token2, appointment_id2)
    
    # Afficher les instructions
    show_confirmation_instructions()
    
    print(f"\n📊 RÉSUMÉ CONFIRMATION")
    print("=" * 70)
    print(f"📅 RDV créés: ✅ IDs {appointment_id}, {appointment_id2}")
    print(f"💳 Confirmation bancaire: {'✅ OK' if bancaire_ok else '❌ ERREUR'}")
    print(f"🏥 Confirmation sur place: {'✅ OK' if sur_place_ok else '❌ ERREUR'}")
    
    if bancaire_ok and sur_place_ok:
        print("\n🎉 CONFIRMATION AUTOMATIQUE OPÉRATIONNELLE!")
        print("\n✅ FONCTIONNALITÉS:")
        print("📊 Paiement bancaire → RDV confirmé + Payé")
        print("📊 Paiement sur place → RDV confirmé + Paiement différé")
        print("🔄 Changement automatique: Planifié → Confirmé")
        print("💳 Bouton adaptatif: 'Confirmer & Payer' ou 'Payer'")
        print("📱 Messages explicites avec changement de statut")
        
        print("\n🌐 TESTEZ MAINTENANT:")
        print("http://localhost:5000/appointments")
        print("Cherchez les RDV 'Planifiés' et testez la confirmation!")
    else:
        print("\n❌ PROBLÈMES DÉTECTÉS")
        print("🔧 Vérifiez les logs Flask")

if __name__ == "__main__":
    main()
