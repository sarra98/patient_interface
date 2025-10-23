#!/usr/bin/env python3
"""
Vérifier le nom et l'emplacement de la base de données
"""

import os
import sqlite3

def check_database_info():
    """Vérifier les informations de la base de données"""
    print("🗄️ INFORMATIONS BASE DE DONNÉES")
    print("=" * 50)
    
    # Chemins possibles
    possible_paths = [
        'instance/secretaire_medicale.db',
        'secretaire_medicale.db',
        'instance/medical_scheduler.db',
        'medical_scheduler.db',
        'secretaire_medicale copy 2.db'
    ]
    
    print("🔍 RECHERCHE DE LA BASE DE DONNÉES:")
    found_databases = []
    
    for db_path in possible_paths:
        if os.path.exists(db_path):
            size = os.path.getsize(db_path)
            modified = os.path.getmtime(db_path)
            import datetime
            modified_str = datetime.datetime.fromtimestamp(modified).strftime('%Y-%m-%d %H:%M:%S')
            
            print(f"✅ TROUVÉE: {db_path}")
            print(f"   📏 Taille: {size:,} bytes")
            print(f"   📅 Modifiée: {modified_str}")
            print(f"   📍 Chemin absolu: {os.path.abspath(db_path)}")
            
            found_databases.append(db_path)
            
            # Vérifier le contenu
            try:
                conn = sqlite3.connect(db_path)
                cursor = conn.cursor()
                
                # Lister les tables
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
                tables = cursor.fetchall()
                
                print(f"   📋 Tables ({len(tables)}):")
                for table in tables:
                    cursor.execute(f"SELECT COUNT(*) FROM {table[0]}")
                    count = cursor.fetchone()[0]
                    print(f"      • {table[0]}: {count} enregistrements")
                
                conn.close()
                
            except Exception as e:
                print(f"   ❌ Erreur lecture: {str(e)}")
            
            print()
        else:
            print(f"❌ Non trouvée: {db_path}")
    
    if not found_databases:
        print("\n❌ AUCUNE BASE DE DONNÉES TROUVÉE!")
        return None
    
    # Base principale utilisée
    main_db = found_databases[0] if found_databases else None
    
    print(f"\n📊 RÉSUMÉ:")
    print(f"🗄️ Base principale: {main_db}")
    print(f"📁 Dossier: {os.path.dirname(os.path.abspath(main_db)) if main_db else 'N/A'}")
    print(f"📄 Nom fichier: {os.path.basename(main_db) if main_db else 'N/A'}")
    
    return main_db

def check_app_config():
    """Vérifier la configuration de l'application"""
    print(f"\n⚙️ CONFIGURATION APPLICATION")
    print("=" * 50)
    
    # Chercher les fichiers de configuration
    config_files = ['app.py', 'config.py', 'database.py']
    
    for config_file in config_files:
        if os.path.exists(config_file):
            print(f"📄 Lecture de {config_file}:")
            try:
                with open(config_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    
                # Chercher les références à la base de données
                lines = content.split('\n')
                for i, line in enumerate(lines, 1):
                    if any(keyword in line.lower() for keyword in ['database', 'db', 'sqlite', '.db']):
                        if not line.strip().startswith('#'):  # Ignorer les commentaires
                            print(f"   Ligne {i}: {line.strip()}")
                            
            except Exception as e:
                print(f"   ❌ Erreur lecture: {str(e)}")
            print()

def show_database_usage():
    """Afficher comment utiliser la base de données"""
    print(f"\n💡 UTILISATION DE LA BASE DE DONNÉES")
    print("=" * 50)
    
    print("🔧 POUR ACCÉDER À LA BASE:")
    print("1. 📍 Chemin: instance/secretaire_medicale.db")
    print("2. 🛠️ Outil: SQLite Browser, DBeaver, ou ligne de commande")
    print("3. 📝 Commande: sqlite3 instance/secretaire_medicale.db")
    
    print(f"\n📋 TABLES PRINCIPALES:")
    print("• patients - Informations des patients")
    print("• medecins - Informations des médecins")
    print("• rendez_vous - Rendez-vous médicaux")
    print("• documents_medicaux - Documents uploadés")
    
    print(f"\n🔍 REQUÊTES UTILES:")
    print("• SELECT * FROM patients;")
    print("• SELECT * FROM rendez_vous ORDER BY date_rdv DESC;")
    print("• SELECT * FROM documents_medicaux ORDER BY date_upload DESC;")
    
    print(f"\n💾 SAUVEGARDE:")
    print("• Copiez le fichier instance/secretaire_medicale.db")
    print("• Ou utilisez: sqlite3 instance/secretaire_medicale.db '.backup backup.db'")

def main():
    """Vérification principale"""
    print("🚀 VÉRIFICATION BASE DE DONNÉES")
    print("=" * 60)
    
    # Vérifier la base de données
    main_db = check_database_info()
    
    # Vérifier la configuration
    check_app_config()
    
    # Afficher les instructions
    show_database_usage()
    
    if main_db:
        print(f"\n🎯 RÉSULTAT FINAL:")
        print(f"📍 Votre base de données: {main_db}")
        print(f"🌐 Chemin complet: {os.path.abspath(main_db)}")
        print(f"✅ Statut: Opérationnelle")
    else:
        print(f"\n❌ PROBLÈME:")
        print("Base de données non trouvée!")

if __name__ == "__main__":
    main()
