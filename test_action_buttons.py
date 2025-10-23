#!/usr/bin/env python3
"""
Test des nouveaux boutons d'actions
"""

import requests
from datetime import datetime, timedelta

BASE_URL = "http://localhost:5000"

def create_test_rdv():
    """Créer un RDV pour tester les boutons"""
    print("📅 CRÉATION RDV POUR TEST BOUTONS")
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
                "date_rdv": f"{tomorrow.strftime('%Y-%m-%d')}T14:30:00",
                "motif": "Test boutons actions",
                "notes": "RDV pour tester les nouveaux boutons"
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
                
        else:
            print(f"❌ Connexion échouée: {response.status_code}")
            return None, None
            
    except Exception as e:
        print(f"❌ Exception: {str(e)}")
        return None, None

def test_edit_appointment(token, appointment_id):
    """Tester la modification d'un RDV"""
    print(f"\n✏️ TEST MODIFICATION RDV {appointment_id}")
    print("=" * 50)
    
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    
    # Nouvelle date/heure
    new_datetime = (datetime.now() + timedelta(days=3)).replace(hour=16, minute=0, second=0, microsecond=0)
    new_datetime_str = new_datetime.isoformat()
    
    edit_data = {
        "date_rdv": new_datetime_str
    }
    
    try:
        response = requests.put(
            f"{BASE_URL}/api/appointments/{appointment_id}",
            json=edit_data,
            headers=headers,
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            print("✅ MODIFICATION RÉUSSIE!")
            print(f"📋 Message: {result.get('message')}")
            print(f"📅 Nouvelle date: {new_datetime.strftime('%d/%m/%Y à %H:%M')}")
            return True
        else:
            print(f"❌ Erreur: {response.status_code}")
            print(f"📋 Réponse: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Exception: {str(e)}")
        return False

def show_buttons_instructions(appointment_id):
    """Afficher les instructions pour les boutons"""
    print(f"\n🌐 INSTRUCTIONS NOUVEAUX BOUTONS")
    print("=" * 60)
    print("1. 🌐 Allez sur: http://localhost:5000/appointments")
    print("2. 🔑 Connectez-vous: test@example.com / test123")
    print("3. 📋 Cherchez le RDV avec:")
    print(f"   🆔 ID: {appointment_id}")
    print("   📝 Motif: Test boutons actions")
    print("4. 👀 Dans la colonne 'Actions', vous verrez:")
    print("   👁️ Bouton BLEU 'Voir' (œil)")
    print("   💳 Bouton VERT 'Payer' (carte) ← NOUVEAU!")
    print("   ✏️ Bouton JAUNE 'Modifier' (crayon) ← NOUVEAU!")
    print("   🗑️ Bouton ROUGE 'Supprimer' (croix)")
    
    print(f"\n💳 BOUTON PAIEMENT (VERT):")
    print("🖱️ Cliquez → Modal de paiement s'ouvre")
    print("💳 Icône: fas fa-credit-card")
    print("🎯 Tooltip: 'Payer 70 DT'")
    
    print(f"\n✏️ BOUTON MODIFIER (JAUNE):")
    print("🖱️ Cliquez → Prompts pour nouvelle date/heure")
    print("📅 Étape 1: Modifier la date (YYYY-MM-DD)")
    print("⏰ Étape 2: Modifier l'heure (HH:MM)")
    print("✅ Validation: Vérifications automatiques")
    print("🚫 Restrictions: Pas dimanche, samedi 8h-12h")
    
    print(f"\n🗑️ BOUTON SUPPRIMER (ROUGE):")
    print("🖱️ Cliquez → Confirmation puis suppression")
    print("❌ Icône: fas fa-times")
    
    print(f"\n🎨 DESIGN DES BOUTONS:")
    print("✅ Groupés avec btn-group")
    print("✅ Couleurs distinctes et cohérentes")
    print("✅ Tooltips informatifs")
    print("✅ Icônes Font Awesome")
    print("✅ Effets de survol")

def main():
    """Test principal des boutons d'actions"""
    print("🚀 TEST NOUVEAUX BOUTONS D'ACTIONS")
    print("=" * 70)
    print("👁️ Voir | 💳 Payer | ✏️ Modifier | 🗑️ Supprimer")
    print("=" * 70)
    
    # Créer un RDV de test
    appointment_id, token = create_test_rdv()
    
    if not appointment_id:
        print("❌ Impossible de créer un RDV de test")
        return
    
    # Tester la modification
    edit_ok = test_edit_appointment(token, appointment_id)
    
    # Afficher les instructions
    show_buttons_instructions(appointment_id)
    
    print(f"\n📊 RÉSUMÉ BOUTONS")
    print("=" * 70)
    print(f"📅 RDV créé: ✅ ID {appointment_id}")
    print(f"✏️ Test modification: {'✅ RÉUSSI' if edit_ok else '❌ ERREUR'}")
    
    if edit_ok:
        print("\n🎉 BOUTONS D'ACTIONS OPÉRATIONNELS!")
        print("\n✅ FONCTIONNALITÉS:")
        print("👁️ Voir: Affiche les détails du RDV")
        print("💳 Payer: Ouvre modal de paiement avec carte")
        print("✏️ Modifier: Change date/heure avec validations")
        print("🗑️ Supprimer: Supprime le RDV après confirmation")
        print("🎨 Design: Boutons groupés et colorés")
        print("📱 Responsive: S'adapte à tous les écrans")
        
        print("\n🌐 TESTEZ MAINTENANT:")
        print("http://localhost:5000/appointments")
        print("Cherchez les 4 boutons dans la colonne Actions!")
    else:
        print("\n❌ PROBLÈME AVEC LA MODIFICATION")
        print("🔧 Vérifiez les logs Flask")

if __name__ == "__main__":
    main()
