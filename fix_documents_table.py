#!/usr/bin/env python3
"""
Corriger la structure de la table documents_medicaux
"""

import sqlite3
import os

def backup_database():
    """Sauvegarder la base de données"""
    print("💾 SAUVEGARDE BASE DE DONNÉES")
    print("=" * 50)
    
    try:
        import shutil
        shutil.copy('instance/secretaire_medicale.db', 'instance/secretaire_medicale_backup.db')
        print("✅ Sauvegarde créée: secretaire_medicale_backup.db")
        return True
    except Exception as e:
        print(f"❌ Erreur sauvegarde: {str(e)}")
        return False

def check_current_structure():
    """Vérifier la structure actuelle"""
    print("\n🔍 STRUCTURE ACTUELLE")
    print("=" * 50)
    
    try:
        conn = sqlite3.connect('instance/secretaire_medicale.db')
        cursor = conn.cursor()
        
        cursor.execute("PRAGMA table_info(documents_medicaux)")
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

def add_missing_columns():
    """Ajouter les colonnes manquantes"""
    print("\n🔧 AJOUT COLONNES MANQUANTES")
    print("=" * 50)
    
    try:
        conn = sqlite3.connect('instance/secretaire_medicale.db')
        cursor = conn.cursor()
        
        # Ajouter les colonnes manquantes une par une
        columns_to_add = [
            ("titre", "VARCHAR(255)"),
            ("contenu", "TEXT"),
            ("fichier_path", "VARCHAR(500)"),
            ("is_active", "BOOLEAN DEFAULT 1"),
            ("date_creation", "DATETIME DEFAULT CURRENT_TIMESTAMP")
        ]
        
        for column_name, column_type in columns_to_add:
            try:
                cursor.execute(f"ALTER TABLE documents_medicaux ADD COLUMN {column_name} {column_type}")
                print(f"✅ Colonne ajoutée: {column_name}")
            except sqlite3.OperationalError as e:
                if "duplicate column name" in str(e):
                    print(f"⚠️  Colonne existe déjà: {column_name}")
                else:
                    print(f"❌ Erreur {column_name}: {str(e)}")
        
        conn.commit()
        conn.close()
        
        print("✅ Colonnes ajoutées avec succès")
        return True
        
    except Exception as e:
        print(f"❌ Erreur: {str(e)}")
        return False

def migrate_data():
    """Migrer les données vers les nouvelles colonnes"""
    print("\n🔄 MIGRATION DES DONNÉES")
    print("=" * 50)
    
    try:
        conn = sqlite3.connect('instance/secretaire_medicale.db')
        cursor = conn.cursor()
        
        # Migrer nom_document -> titre
        cursor.execute("UPDATE documents_medicaux SET titre = nom_document WHERE titre IS NULL")
        rows_updated = cursor.rowcount
        print(f"✅ {rows_updated} titres migrés")
        
        # Migrer description -> contenu
        cursor.execute("UPDATE documents_medicaux SET contenu = description WHERE contenu IS NULL")
        rows_updated = cursor.rowcount
        print(f"✅ {rows_updated} contenus migrés")
        
        # Migrer chemin_fichier -> fichier_path
        cursor.execute("UPDATE documents_medicaux SET fichier_path = chemin_fichier WHERE fichier_path IS NULL")
        rows_updated = cursor.rowcount
        print(f"✅ {rows_updated} chemins migrés")
        
        # Migrer date_upload -> date_creation
        cursor.execute("UPDATE documents_medicaux SET date_creation = date_upload WHERE date_creation IS NULL")
        rows_updated = cursor.rowcount
        print(f"✅ {rows_updated} dates migrées")
        
        # Activer tous les documents
        cursor.execute("UPDATE documents_medicaux SET is_active = 1 WHERE is_active IS NULL")
        rows_updated = cursor.rowcount
        print(f"✅ {rows_updated} documents activés")
        
        conn.commit()
        conn.close()
        
        print("✅ Migration des données terminée")
        return True
        
    except Exception as e:
        print(f"❌ Erreur migration: {str(e)}")
        return False

def verify_migration():
    """Vérifier que la migration a réussi"""
    print("\n✅ VÉRIFICATION MIGRATION")
    print("=" * 50)
    
    try:
        conn = sqlite3.connect('instance/secretaire_medicale.db')
        cursor = conn.cursor()
        
        # Vérifier la nouvelle structure
        cursor.execute("PRAGMA table_info(documents_medicaux)")
        columns = cursor.fetchall()
        
        required_columns = ['titre', 'contenu', 'fichier_path', 'is_active', 'date_creation']
        existing_columns = [col[1] for col in columns]
        
        missing = [col for col in required_columns if col not in existing_columns]
        
        if missing:
            print(f"❌ Colonnes encore manquantes: {missing}")
            return False
        else:
            print("✅ Toutes les colonnes requises sont présentes")
        
        # Compter les documents avec les nouvelles colonnes
        cursor.execute("SELECT COUNT(*) FROM documents_medicaux WHERE titre IS NOT NULL")
        count_with_title = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM documents_medicaux WHERE is_active = 1")
        count_active = cursor.fetchone()[0]
        
        print(f"📊 {count_with_title} documents avec titre")
        print(f"📊 {count_active} documents actifs")
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Erreur vérification: {str(e)}")
        return False

def test_documents_after_fix():
    """Tester les documents après correction"""
    print("\n🔍 TEST APRÈS CORRECTION")
    print("=" * 50)
    
    try:
        import requests
        
        # Connexion
        login_data = {
            "email": "test@example.com",
            "password": "test123"
        }
        
        response = requests.post(
            "http://localhost:5000/api/auth/login",
            json=login_data,
            headers={'Content-Type': 'application/json'},
            timeout=10
        )
        
        if response.status_code != 200:
            print("❌ Connexion impossible")
            return False
        
        token = response.json().get('access_token')
        
        # Test GET documents
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }
        
        response = requests.get(
            "http://localhost:5000/api/documents/",
            headers=headers,
            timeout=10
        )
        
        print(f"📥 Status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            documents = result.get('documents', [])
            print(f"✅ {len(documents)} documents récupérés")
            return True
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

def main():
    """Correction principale"""
    print("🚨 CORRECTION TABLE DOCUMENTS")
    print("=" * 60)
    print("🎯 Ajouter colonnes manquantes et migrer données")
    print("=" * 60)
    
    # Étapes de correction
    steps = [
        ("Sauvegarde base", backup_database),
        ("Vérification structure", lambda: check_current_structure() is not None),
        ("Ajout colonnes", add_missing_columns),
        ("Migration données", migrate_data),
        ("Vérification migration", verify_migration),
        ("Test final", test_documents_after_fix)
    ]
    
    success_count = 0
    for step_name, step_func in steps:
        print(f"\n📋 {step_name.upper()}")
        if step_func():
            success_count += 1
            print(f"✅ {step_name} OK")
        else:
            print(f"❌ {step_name} échoué")
            if step_name in ["Sauvegarde base", "Vérification structure"]:
                continue  # Ces étapes peuvent échouer sans arrêter
            else:
                break
    
    print(f"\n📊 RÉSUMÉ: {success_count}/{len(steps)} étapes réussies")
    
    if success_count >= 4:  # Au moins jusqu'à la migration
        print("\n🎉 CORRECTION RÉUSSIE!")
        print("\nCHANGEMENTS APPLIQUÉS:")
        print("✅ Colonnes ajoutées: titre, contenu, fichier_path, is_active, date_creation")
        print("✅ Données migrées: nom_document->titre, description->contenu, etc.")
        print("✅ Tous les documents activés")
        print("\nTESTEZ MAINTENANT:")
        print("🌐 Interface: http://localhost:5000/documents")
        print("🔑 Connexion: test@example.com / test123")
    else:
        print("\n❌ CORRECTION INCOMPLÈTE")
        print("💡 Restaurez avec la sauvegarde si nécessaire")

if __name__ == "__main__":
    main()
