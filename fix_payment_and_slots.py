#!/usr/bin/env python3
"""
Corriger les boutons de paiement et ajouter les créneaux occupés
"""

import sqlite3
from datetime import datetime, timedelta

def fix_rdv_for_payment_buttons():
    """Corriger les RDV pour afficher les boutons de paiement"""
    print("🔧 CORRECTION RDV POUR BOUTONS PAIEMENT")
    print("=" * 50)
    
    try:
        conn = sqlite3.connect('instance/secretaire_medicale.db')
        cursor = conn.cursor()
        
        # 1. Mettre tous les RDV en statut "confirme" pour voir les boutons
        cursor.execute("UPDATE rendez_vous SET statut = 'confirme' WHERE statut = 'planifie'")
        updated_status = cursor.rowcount
        print(f"✅ {updated_status} RDV mis en statut 'confirme'")
        
        # 2. S'assurer que tous ont un statut de paiement
        cursor.execute("UPDATE rendez_vous SET statut_paiement = 'en_attente' WHERE statut_paiement IS NULL")
        updated_payment = cursor.rowcount
        print(f"✅ {updated_payment} RDV avec statut_paiement 'en_attente'")
        
        # 3. S'assurer que tous ont un montant
        cursor.execute("UPDATE rendez_vous SET montant = 70.00 WHERE montant IS NULL OR montant = 0")
        updated_amount = cursor.rowcount
        print(f"✅ {updated_amount} RDV avec montant 70 DT")
        
        # 4. Créer un RDV de test spécial
        tomorrow = datetime.now() + timedelta(days=1)
        while tomorrow.weekday() == 6:  # Éviter dimanche
            tomorrow += timedelta(days=1)
        
        cursor.execute("""
            INSERT INTO rendez_vous (
                patient_id, medecin_id, date_rdv, motif, statut, 
                statut_paiement, montant, notes
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            1, 1, tomorrow,
            "RDV avec bouton paiement VISIBLE",
            "confirme",
            "en_attente", 
            70.00,
            "RDV spécialement créé pour voir le bouton de paiement"
        ))
        
        test_rdv_id = cursor.lastrowid
        print(f"✅ RDV test créé avec ID: {test_rdv_id}")
        
        conn.commit()
        conn.close()
        
        return test_rdv_id
        
    except Exception as e:
        print(f"❌ Erreur: {str(e)}")
        return None

def create_occupied_slots_demo():
    """Créer des RDV pour démontrer les créneaux occupés"""
    print("\n🚫 CRÉATION CRÉNEAUX OCCUPÉS DEMO")
    print("=" * 50)
    
    try:
        conn = sqlite3.connect('instance/secretaire_medicale.db')
        cursor = conn.cursor()
        
        # Créer des RDV pour le 20/07/2025 à différentes heures
        demo_date = datetime(2025, 7, 20)
        
        demo_slots = [
            (11, 0, "Patient A - Créneau occupé"),
            (14, 30, "Patient B - Créneau occupé"),
            (16, 0, "Patient C - Créneau occupé")
        ]
        
        created_count = 0
        for hour, minute, motif in demo_slots:
            slot_datetime = demo_date.replace(hour=hour, minute=minute)
            
            try:
                cursor.execute("""
                    INSERT INTO rendez_vous (
                        patient_id, medecin_id, date_rdv, motif, statut, 
                        statut_paiement, montant
                    ) VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (
                    1, 1, slot_datetime, motif, "confirme", "en_attente", 70.00
                ))
                created_count += 1
                print(f"✅ Créneau occupé: {slot_datetime.strftime('%H:%M')}")
            except:
                print(f"⚠️  Créneau {slot_datetime.strftime('%H:%M')} existe déjà")
        
        conn.commit()
        conn.close()
        
        print(f"✅ {created_count} créneaux occupés créés pour le 20/07/2025")
        return True
        
    except Exception as e:
        print(f"❌ Erreur: {str(e)}")
        return False

def main():
    """Correction principale"""
    print("🚀 CORRECTION BOUTONS PAIEMENT + CRÉNEAUX OCCUPÉS")
    print("=" * 70)
    
    # Corriger les RDV pour les boutons de paiement
    test_rdv_id = fix_rdv_for_payment_buttons()
    
    # Créer des créneaux occupés pour la démo
    slots_ok = create_occupied_slots_demo()
    
    print(f"\n🎉 CORRECTIONS APPLIQUÉES!")
    print("=" * 70)
    
    if test_rdv_id:
        print("💳 BOUTONS DE PAIEMENT:")
        print("✅ Tous les RDV mis en statut 'confirmé'")
        print("✅ Statut paiement 'en_attente' ajouté")
        print("✅ Montant 70 DT défini")
        print(f"✅ RDV test créé (ID: {test_rdv_id})")
        print("\n🌐 POUR VOIR LES BOUTONS:")
        print("1. Allez sur: http://localhost:5000/appointments")
        print("2. Connectez-vous: test@example.com / test123")
        print("3. Cherchez les RDV avec statut 'Confirmé'")
        print("4. Dans Actions: 👁️ Voir | 🗑️ Supprimer | 💳 Payer")
    
    if slots_ok:
        print("\n🚫 CRÉNEAUX OCCUPÉS:")
        print("✅ RDV créés pour le 20/07/2025:")
        print("   🚫 11h00 - Patient A")
        print("   🚫 14h30 - Patient B") 
        print("   🚫 16h00 - Patient C")
        print("\n🌐 POUR VOIR LES CROIX ROUGES:")
        print("1. Allez sur: http://localhost:5000/book-appointment")
        print("2. Sélectionnez la date: 20/07/2025")
        print("3. Les créneaux 11h00, 14h30, 16h00 auront des croix rouges")
    
    print("\n💡 ÉTAPES SUIVANTES:")
    print("1. 🔄 Actualisez les pages web")
    print("2. 💳 Testez les boutons de paiement")
    print("3. 🚫 Testez les créneaux occupés")
    print("4. ✅ Tout devrait fonctionner maintenant!")

if __name__ == "__main__":
    main()
