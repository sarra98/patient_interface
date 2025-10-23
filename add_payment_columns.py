#!/usr/bin/env python3
"""
Ajouter les colonnes de paiement à la table rendez-vous
"""

import sqlite3
import os

def backup_database():
    """Sauvegarder la base de données"""
    print("💾 SAUVEGARDE BASE DE DONNÉES")
    print("=" * 50)
    
    try:
        import shutil
        shutil.copy('instance/secretaire_medicale.db', 'instance/secretaire_medicale_payment_backup.db')
        print("✅ Sauvegarde créée: secretaire_medicale_payment_backup.db")
        return True
    except Exception as e:
        print(f"❌ Erreur sauvegarde: {str(e)}")
        return False

def check_rendez_vous_table():
    """Vérifier la structure actuelle de la table rendez-vous"""
    print("\n🔍 STRUCTURE TABLE RENDEZ-VOUS")
    print("=" * 50)
    
    try:
        conn = sqlite3.connect('instance/secretaire_medicale.db')
        cursor = conn.cursor()
        
        cursor.execute("PRAGMA table_info(rendez_vous)")
        columns = cursor.fetchall()
        
        print(f"📋 Colonnes actuelles ({len(columns)}):")
        current_columns = []
        for col in columns:
            current_columns.append(col[1])
            print(f"  - {col[1]} ({col[2]})")
        
        conn.close()
        return current_columns
        
    except Exception as e:
        print(f"❌ Erreur: {str(e)}")
        return []

def add_payment_columns():
    """Ajouter les colonnes de paiement"""
    print("\n💳 AJOUT COLONNES PAIEMENT")
    print("=" * 50)
    
    try:
        conn = sqlite3.connect('instance/secretaire_medicale.db')
        cursor = conn.cursor()
        
        # Colonnes de paiement à ajouter
        payment_columns = [
            ("statut_paiement", "VARCHAR(20) DEFAULT 'en_attente'"),  # en_attente, paye, echec
            ("mode_paiement", "VARCHAR(20)"),  # bancaire, sur_place
            ("montant", "DECIMAL(10,2) DEFAULT 50.00"),  # Montant consultation
            ("date_paiement", "DATETIME"),  # Date du paiement
            ("reference_paiement", "VARCHAR(100)"),  # Référence transaction
            ("details_paiement", "TEXT"),  # Détails supplémentaires
            ("paiement_confirme", "BOOLEAN DEFAULT 0")  # Confirmation paiement
        ]
        
        for column_name, column_type in payment_columns:
            try:
                cursor.execute(f"ALTER TABLE rendez_vous ADD COLUMN {column_name} {column_type}")
                print(f"✅ Colonne ajoutée: {column_name}")
            except sqlite3.OperationalError as e:
                if "duplicate column name" in str(e):
                    print(f"⚠️  Colonne existe déjà: {column_name}")
                else:
                    print(f"❌ Erreur {column_name}: {str(e)}")
        
        conn.commit()
        conn.close()
        
        print("✅ Colonnes de paiement ajoutées")
        return True
        
    except Exception as e:
        print(f"❌ Erreur: {str(e)}")
        return False

def verify_payment_columns():
    """Vérifier que les colonnes de paiement ont été ajoutées"""
    print("\n✅ VÉRIFICATION COLONNES PAIEMENT")
    print("=" * 50)
    
    try:
        conn = sqlite3.connect('instance/secretaire_medicale.db')
        cursor = conn.cursor()
        
        cursor.execute("PRAGMA table_info(rendez_vous)")
        columns = cursor.fetchall()
        
        payment_columns = ['statut_paiement', 'mode_paiement', 'montant', 'date_paiement', 'reference_paiement', 'details_paiement', 'paiement_confirme']
        existing_columns = [col[1] for col in columns]
        
        missing = [col for col in payment_columns if col not in existing_columns]
        
        if missing:
            print(f"❌ Colonnes manquantes: {missing}")
            return False
        else:
            print("✅ Toutes les colonnes de paiement sont présentes")
            
            # Afficher les nouvelles colonnes
            for col in columns:
                if col[1] in payment_columns:
                    print(f"  💳 {col[1]} ({col[2]})")
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Erreur: {str(e)}")
        return False

def update_existing_appointments():
    """Mettre à jour les RDV existants avec les valeurs par défaut"""
    print("\n🔄 MISE À JOUR RDV EXISTANTS")
    print("=" * 50)
    
    try:
        conn = sqlite3.connect('instance/secretaire_medicale.db')
        cursor = conn.cursor()
        
        # Compter les RDV existants
        cursor.execute("SELECT COUNT(*) FROM rendez_vous")
        total_rdv = cursor.fetchone()[0]
        print(f"📊 {total_rdv} rendez-vous en base")
        
        if total_rdv > 0:
            # Mettre à jour les RDV sans statut de paiement
            cursor.execute("""
                UPDATE rendez_vous 
                SET statut_paiement = 'en_attente', 
                    montant = 50.00,
                    paiement_confirme = 0
                WHERE statut_paiement IS NULL
            """)
            
            updated = cursor.rowcount
            print(f"✅ {updated} RDV mis à jour avec statut paiement")
        
        conn.commit()
        conn.close()
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur: {str(e)}")
        return False

def main():
    """Ajout principal des colonnes de paiement"""
    print("🚀 AJOUT SYSTÈME DE PAIEMENT")
    print("=" * 60)
    print("💳 Colonnes paiement pour rendez-vous")
    print("=" * 60)
    
    # Étapes
    steps = [
        ("Sauvegarde base", backup_database),
        ("Vérification structure", lambda: check_rendez_vous_table() is not None),
        ("Ajout colonnes paiement", add_payment_columns),
        ("Vérification colonnes", verify_payment_columns),
        ("Mise à jour RDV existants", update_existing_appointments)
    ]
    
    success_count = 0
    for step_name, step_func in steps:
        print(f"\n📋 {step_name.upper()}")
        if step_func():
            success_count += 1
            print(f"✅ {step_name} OK")
        else:
            print(f"❌ {step_name} échoué")
            if step_name not in ["Sauvegarde base", "Vérification structure"]:
                break
    
    print(f"\n📊 RÉSUMÉ: {success_count}/{len(steps)} étapes réussies")
    
    if success_count >= 3:  # Au moins jusqu'à l'ajout des colonnes
        print("\n🎉 COLONNES PAIEMENT AJOUTÉES!")
        print("\nCOLONNES AJOUTÉES:")
        print("💳 statut_paiement: en_attente, paye, echec")
        print("💳 mode_paiement: bancaire, sur_place")
        print("💳 montant: Montant de la consultation")
        print("💳 date_paiement: Date du paiement")
        print("💳 reference_paiement: Référence transaction")
        print("💳 details_paiement: Détails supplémentaires")
        print("💳 paiement_confirme: Confirmation paiement")
        print("\nÉTAPE SUIVANTE:")
        print("🔧 Mise à jour du modèle RendezVous")
        print("🌐 Ajout interface de paiement")
    else:
        print("\n❌ AJOUT INCOMPLET")
        print("💡 Vérifiez les erreurs ci-dessus")

if __name__ == "__main__":
    main()
