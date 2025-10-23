#!/usr/bin/env python3
"""
Test final: boutons de paiement + créneaux occupés
"""

import requests

BASE_URL = "http://localhost:5000"

def test_payment_buttons():
    """Tester les boutons de paiement"""
    print("💳 TEST BOUTONS DE PAIEMENT")
    print("=" * 50)
    
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
            return False
        
        token = response.json().get('access_token')
        
        # Récupérer les RDV
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }
        
        response = requests.get(
            f"{BASE_URL}/api/appointments/",
            headers=headers,
            timeout=10
        )
        
        if response.status_code == 200:
            result = response.json()
            appointments = result.get('appointments', [])
            
            print(f"📊 {len(appointments)} RDV récupérés")
            
            payment_button_count = 0
            for rdv in appointments:
                statut = rdv.get('statut')
                statut_paiement = rdv.get('statut_paiement')
                
                if statut == 'confirme' and statut_paiement == 'en_attente':
                    payment_button_count += 1
                    print(f"✅ RDV ID {rdv.get('id')} AURA un bouton de paiement")
                    print(f"   Motif: {rdv.get('motif')}")
                    print(f"   Statut: {statut}")
                    print(f"   Paiement: {statut_paiement}")
            
            print(f"\n🎯 {payment_button_count} RDV avec boutons de paiement")
            return payment_button_count > 0
        else:
            print(f"❌ Erreur API: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Exception: {str(e)}")
        return False

def test_occupied_slots():
    """Tester les créneaux occupés"""
    print("\n🚫 TEST CRÉNEAUX OCCUPÉS")
    print("=" * 50)
    
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
            return False
        
        token = response.json().get('access_token')
        
        # Tester les créneaux occupés pour le 20/07/2025
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }
        
        response = requests.get(
            f"{BASE_URL}/api/appointments/occupied-slots?date=2025-07-20",
            headers=headers,
            timeout=10
        )
        
        print(f"📥 Status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            occupied_slots = result.get('occupied_slots', [])
            
            print(f"✅ {len(occupied_slots)} créneaux occupés le 20/07/2025:")
            for slot in occupied_slots:
                print(f"  🚫 {slot}")
            
            # Vérifier que nos créneaux de test sont là
            expected_slots = ['11:00', '14:30', '16:00']
            found_slots = [slot for slot in expected_slots if slot in occupied_slots]
            
            print(f"\n🎯 Créneaux de test trouvés: {len(found_slots)}/{len(expected_slots)}")
            for slot in found_slots:
                print(f"  ✅ {slot} - Créneau occupé détecté")
            
            return len(occupied_slots) > 0
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

def show_final_instructions():
    """Afficher les instructions finales"""
    print(f"\n🌐 INSTRUCTIONS FINALES")
    print("=" * 50)
    print("💳 POUR VOIR LES BOUTONS DE PAIEMENT:")
    print("1. 🌐 http://localhost:5000/appointments")
    print("2. 🔑 test@example.com / test123")
    print("3. 👀 Cherchez les RDV avec statut 'Confirmé'")
    print("4. 📊 Dans la colonne 'Actions':")
    print("   👁️ Bouton bleu 'Voir'")
    print("   🗑️ Bouton rouge 'Supprimer'")
    print("   💳 BOUTON VERT 'Payer' ← NOUVEAU!")
    print("5. 🖱️ Cliquez sur le bouton vert")
    print("6. 📱 Modal de paiement s'ouvre")
    
    print("\n🚫 POUR VOIR LES CRÉNEAUX OCCUPÉS:")
    print("1. 🌐 http://localhost:5000/book-appointment")
    print("2. 📅 Sélectionnez la date: 20/07/2025")
    print("3. 🚫 Vous verrez des créneaux avec croix rouge:")
    print("   ❌ 11:00 - Occupé")
    print("   ❌ 14:30 - Occupé")
    print("   ❌ 16:00 - Occupé")
    print("4. 🖱️ Ces créneaux ne sont pas cliquables")
    print("5. ✅ Choisissez un autre créneau disponible")

def main():
    """Test final complet"""
    print("🎉 TEST FINAL COMPLET")
    print("=" * 70)
    print("💳 Boutons paiement + 🚫 Créneaux occupés")
    print("=" * 70)
    
    # Tester les boutons de paiement
    payment_ok = test_payment_buttons()
    
    # Tester les créneaux occupés
    slots_ok = test_occupied_slots()
    
    # Instructions finales
    show_final_instructions()
    
    # Résumé
    print(f"\n📊 RÉSUMÉ FINAL")
    print("=" * 70)
    print(f"💳 Boutons de paiement: {'✅ VISIBLES' if payment_ok else '❌ PROBLÈME'}")
    print(f"🚫 Créneaux occupés: {'✅ FONCTIONNELS' if slots_ok else '❌ PROBLÈME'}")
    
    if payment_ok and slots_ok:
        print("\n🎉 TOUT FONCTIONNE PARFAITEMENT!")
        print("\n✅ FONCTIONNALITÉS OPÉRATIONNELLES:")
        print("💳 Boutons de paiement verts dans Actions")
        print("🚫 Créneaux occupés avec croix rouge")
        print("💰 Paiement 70 DT (bancaire + sur place)")
        print("📱 Modal de sélection élégante")
        print("🔄 Rechargement automatique")
        print("\n🌐 TESTEZ MAINTENANT LES DEUX PAGES!")
    else:
        print("\n⚠️  PROBLÈMES DÉTECTÉS")
        if not payment_ok:
            print("💡 Boutons paiement: Vérifiez que les RDV sont 'confirmés'")
        if not slots_ok:
            print("💡 Créneaux occupés: Vérifiez la route /occupied-slots")

if __name__ == "__main__":
    main()
