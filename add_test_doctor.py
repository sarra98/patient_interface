#!/usr/bin/env python3
"""
Ajouter un médecin de test si nécessaire
"""

import sqlite3
import os

def check_database():
    """Vérifier la base de données"""
    print("🔍 VÉRIFICATION BASE DE DONNÉES")
    print("=" * 50)
    
    db_path = 'instance/secretaire_medicale.db'
    
    if not os.path.exists(db_path):
        print(f"❌ Base de données non trouvée: {db_path}")
        return False
    
    print(f"✅ Base de données trouvée: {db_path}")
    return True

def check_medecins_table():
    """Vérifier la table médecins"""
    print("\n🔍 VÉRIFICATION TABLE MÉDECINS")
    print("=" * 50)
    
    try:
        conn = sqlite3.connect('instance/secretaire_medicale.db')
        cursor = conn.cursor()
        
        # Vérifier si la table existe
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='medecins'")
        table_exists = cursor.fetchone()
        
        if not table_exists:
            print("❌ Table médecins n'existe pas")
            conn.close()
            return False
        
        print("✅ Table médecins existe")
        
        # Compter les médecins
        cursor.execute("SELECT COUNT(*) FROM medecins")
        count = cursor.fetchone()[0]
        print(f"📊 {count} médecins en base")
        
        # Lister les médecins
        cursor.execute("SELECT id, nom, prenom, specialite, is_active FROM medecins")
        medecins = cursor.fetchall()
        
        print(f"📋 Liste des médecins:")
        for medecin in medecins:
            status = "✅ Actif" if medecin[4] else "❌ Inactif"
            print(f"  ID {medecin[0]}: Dr {medecin[1]} {medecin[2]} ({medecin[3]}) - {status}")
        
        conn.close()
        return len(medecins) > 0
        
    except Exception as e:
        print(f"❌ Erreur: {str(e)}")
        return False

def create_medecins_table():
    """Créer la table médecins si elle n'existe pas"""
    print("\n🔧 CRÉATION TABLE MÉDECINS")
    print("=" * 50)
    
    try:
        conn = sqlite3.connect('instance/secretaire_medicale.db')
        cursor = conn.cursor()
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS medecins (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nom VARCHAR(100) NOT NULL,
                prenom VARCHAR(100) NOT NULL,
                specialite VARCHAR(100) NOT NULL,
                telephone VARCHAR(20),
                email VARCHAR(100),
                adresse TEXT,
                is_active BOOLEAN DEFAULT 1,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        conn.commit()
        conn.close()
        
        print("✅ Table médecins créée")
        return True
        
    except Exception as e:
        print(f"❌ Erreur création table: {str(e)}")
        return False

def add_test_doctor():
    """Ajouter un médecin de test"""
    print("\n👨‍⚕️ AJOUT MÉDECIN DE TEST")
    print("=" * 50)
    
    try:
        conn = sqlite3.connect('instance/secretaire_medicale.db')
        cursor = conn.cursor()
        
        # Vérifier si Dr Ahmed Samir existe déjà
        cursor.execute("SELECT id FROM medecins WHERE nom = 'Samir' AND prenom = 'Ahmed'")
        existing = cursor.fetchone()
        
        if existing:
            print(f"✅ Dr Ahmed Samir existe déjà (ID: {existing[0]})")
            conn.close()
            return existing[0]
        
        # Ajouter le médecin de test
        cursor.execute("""
            INSERT INTO medecins (nom, prenom, specialite, telephone, email, is_active)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            'Samir',
            'Ahmed', 
            'Médecine Générale',
            '+213555123456',
            'ahmed.samir@medical.dz',
            1
        ))
        
        medecin_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        print(f"✅ Dr Ahmed Samir ajouté avec ID: {medecin_id}")
        return medecin_id
        
    except Exception as e:
        print(f"❌ Erreur ajout médecin: {str(e)}")
        return None

def check_patients_table():
    """Vérifier qu'il y a au moins un patient de test"""
    print("\n👤 VÉRIFICATION PATIENTS")
    print("=" * 50)
    
    try:
        conn = sqlite3.connect('instance/secretaire_medicale.db')
        cursor = conn.cursor()
        
        cursor.execute("SELECT COUNT(*) FROM patients")
        count = cursor.fetchone()[0]
        print(f"📊 {count} patients en base")
        
        if count == 0:
            print("⚠️  Aucun patient - Créez un compte via /register")
        else:
            cursor.execute("SELECT id, email FROM patients LIMIT 3")
            patients = cursor.fetchall()
            print(f"📋 Patients:")
            for patient in patients:
                print(f"  ID {patient[0]}: {patient[1]}")
        
        conn.close()
        return count > 0
        
    except Exception as e:
        print(f"❌ Erreur: {str(e)}")
        return False

def main():
    """Configuration principale"""
    print("🚀 CONFIGURATION MÉDECIN DE TEST")
    print("=" * 60)
    print("👨‍⚕️ Ajout Dr Ahmed Samir pour les tests")
    print("=" * 60)
    
    # Vérifications
    if not check_database():
        print("❌ Base de données inaccessible")
        return
    
    # Vérifier/créer table médecins
    medecins_exist = check_medecins_table()
    if not medecins_exist:
        print("🔧 Table médecins manquante ou vide")
        if create_medecins_table():
            medecin_id = add_test_doctor()
        else:
            print("❌ Impossible de créer la table")
            return
    else:
        print("✅ Médecins déjà présents")
        medecin_id = 1  # Supposer que le premier médecin a l'ID 1
    
    # Vérifier patients
    patients_exist = check_patients_table()
    
    # Résumé
    print(f"\n📊 RÉSUMÉ CONFIGURATION")
    print("=" * 60)
    print(f"👨‍⚕️ Médecins: {'✅ OK' if medecins_exist else '✅ AJOUTÉ'}")
    print(f"👤 Patients: {'✅ OK' if patients_exist else '⚠️  MANQUANTS'}")
    
    if medecin_id and patients_exist:
        print("\n🎉 CONFIGURATION COMPLÈTE!")
        print("💡 Vous pouvez maintenant:")
        print("1. Tester la création de RDV: python test_rdv_creation.py")
        print("2. Utiliser l'interface: http://localhost:5000/book-appointment")
        print("3. Vous connecter avec: test@example.com / test123")
    elif not patients_exist:
        print("\n⚠️  CONFIGURATION INCOMPLÈTE")
        print("💡 Créez un patient de test:")
        print("1. Allez sur: http://localhost:5000/register")
        print("2. Créez un compte: test@example.com / test123")
        print("3. Puis testez: python test_rdv_creation.py")
    else:
        print("\n❌ PROBLÈMES DE CONFIGURATION")
        print("💡 Vérifiez la base de données")

if __name__ == "__main__":
    main()
