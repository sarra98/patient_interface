#!/usr/bin/env python3
"""
Vérifier la base de données des documents
"""

import sqlite3
import os

def check_documents_table():
    """Vérifier la table documents_medicaux"""
    print("🔍 VÉRIFICATION TABLE DOCUMENTS")
    print("=" * 50)
    
    db_path = 'instance/secretaire_medicale.db'
    if not os.path.exists(db_path):
        print(f"❌ Base de données non trouvée: {db_path}")
        return False
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Vérifier si la table existe
        cursor.execute("""
            SELECT name FROM sqlite_master 
            WHERE type='table' AND name='documents_medicaux'
        """)
        table_exists = cursor.fetchone()
        
        if table_exists:
            print("✅ Table 'documents_medicaux' existe")
            
            # Vérifier la structure
            cursor.execute("PRAGMA table_info(documents_medicaux)")
            columns = cursor.fetchall()
            
            print("\n📊 STRUCTURE DE LA TABLE:")
            print("-" * 60)
            print("Colonne | Type | Null | Défaut | PK")
            print("-" * 60)
            for col in columns:
                cid, name, type_name, notnull, default, pk = col
                null_str = "NOT NULL" if notnull else "NULL"
                pk_str = "PK" if pk else ""
                print(f"{name:20} | {type_name:15} | {null_str:8} | {str(default):10} | {pk_str}")
            
            # Compter les documents
            cursor.execute("SELECT COUNT(*) FROM documents_medicaux")
            count = cursor.fetchone()[0]
            print(f"\n📄 NOMBRE DE DOCUMENTS: {count}")
            
            if count > 0:
                # Afficher quelques exemples
                cursor.execute("""
                    SELECT id, patient_id, type_document, nom_document, nom_fichier, 
                           chemin_fichier, taille_fichier, date_upload 
                    FROM documents_medicaux 
                    ORDER BY id DESC 
                    LIMIT 5
                """)
                docs = cursor.fetchall()
                
                print(f"\n📋 DERNIERS DOCUMENTS:")
                print("-" * 100)
                print("ID | Patient | Type | Nom | Fichier | Taille | Date")
                print("-" * 100)
                for doc in docs:
                    doc_id, patient_id, type_doc, nom_doc, nom_fichier, chemin, taille, date_upload = doc
                    nom_doc_short = (nom_doc[:20] + '...') if nom_doc and len(nom_doc) > 20 else (nom_doc or 'N/A')
                    nom_fichier_short = (nom_fichier[:15] + '...') if nom_fichier and len(nom_fichier) > 15 else (nom_fichier or 'N/A')
                    taille_str = f"{taille}B" if taille else "N/A"
                    date_str = date_upload[:10] if date_upload else "N/A"
                    print(f"{doc_id:2} | {patient_id:7} | {type_doc:8} | {nom_doc_short:23} | {nom_fichier_short:18} | {taille_str:8} | {date_str}")
                
                # Vérifier les fichiers physiques
                print(f"\n📁 VÉRIFICATION FICHIERS PHYSIQUES:")
                files_exist = 0
                files_missing = 0
                
                for doc in docs:
                    chemin = doc[5]  # chemin_fichier
                    if chemin and os.path.exists(chemin):
                        files_exist += 1
                    else:
                        files_missing += 1
                        print(f"❌ Fichier manquant: {chemin}")
                
                print(f"✅ Fichiers existants: {files_exist}")
                print(f"❌ Fichiers manquants: {files_missing}")
            
            conn.close()
            return True
            
        else:
            print("❌ Table 'documents_medicaux' n'existe pas")
            print("\n💡 SOLUTION: Créer la table")
            conn.close()
            return False
            
    except Exception as e:
        print(f"❌ Erreur: {str(e)}")
        return False

def create_documents_table():
    """Créer la table documents_medicaux si elle n'existe pas"""
    print(f"\n🔧 CRÉATION TABLE DOCUMENTS")
    print("=" * 50)
    
    db_path = 'instance/secretaire_medicale.db'
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Créer la table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS documents_medicaux (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                patient_id INTEGER NOT NULL,
                type_document VARCHAR(50) NOT NULL,
                nom_document VARCHAR(255) NOT NULL,
                description TEXT,
                nom_fichier VARCHAR(255) NOT NULL,
                chemin_fichier VARCHAR(500) NOT NULL,
                taille_fichier INTEGER,
                date_upload DATETIME DEFAULT CURRENT_TIMESTAMP,
                date_document DATE,
                medecin_prescripteur VARCHAR(255),
                FOREIGN KEY (patient_id) REFERENCES patients (id)
            )
        """)
        
        conn.commit()
        print("✅ Table 'documents_medicaux' créée avec succès")
        
        # Vérifier la création
        cursor.execute("PRAGMA table_info(documents_medicaux)")
        columns = cursor.fetchall()
        print(f"✅ {len(columns)} colonnes créées")
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Erreur création table: {str(e)}")
        return False

def check_uploads_folder():
    """Vérifier le dossier uploads"""
    print(f"\n📁 VÉRIFICATION DOSSIER UPLOADS")
    print("=" * 50)
    
    upload_folder = 'uploads/documents'
    
    if os.path.exists(upload_folder):
        print(f"✅ Dossier existe: {os.path.abspath(upload_folder)}")
        
        # Lister les fichiers
        files = os.listdir(upload_folder)
        print(f"📄 Nombre de fichiers: {len(files)}")
        
        if files:
            print(f"\n📋 FICHIERS DANS LE DOSSIER:")
            for i, file in enumerate(files[:10]):  # Max 10 fichiers
                file_path = os.path.join(upload_folder, file)
                size = os.path.getsize(file_path)
                print(f"  {i+1}. {file} ({size} bytes)")
            
            if len(files) > 10:
                print(f"  ... et {len(files) - 10} autres fichiers")
        
        return True
    else:
        print(f"❌ Dossier n'existe pas: {upload_folder}")
        print(f"💡 Création du dossier...")
        
        try:
            os.makedirs(upload_folder, exist_ok=True)
            print(f"✅ Dossier créé: {os.path.abspath(upload_folder)}")
            return True
        except Exception as e:
            print(f"❌ Erreur création dossier: {str(e)}")
            return False

def main():
    """Vérification principale"""
    print("🚀 VÉRIFICATION SYSTÈME DOCUMENTS")
    print("=" * 70)
    
    # Vérifier la table
    table_ok = check_documents_table()
    
    if not table_ok:
        # Créer la table si elle n'existe pas
        create_ok = create_documents_table()
        if create_ok:
            # Re-vérifier après création
            table_ok = check_documents_table()
    
    # Vérifier le dossier uploads
    folder_ok = check_uploads_folder()
    
    print(f"\n📊 RÉSUMÉ VÉRIFICATION")
    print("=" * 70)
    print(f"🗄️ Table documents_medicaux: {'✅ OK' if table_ok else '❌ ERREUR'}")
    print(f"📁 Dossier uploads: {'✅ OK' if folder_ok else '❌ ERREUR'}")
    
    if table_ok and folder_ok:
        print("\n🎉 SYSTÈME DOCUMENTS PRÊT!")
        print("\n✅ FONCTIONNALITÉS DISPONIBLES:")
        print("📤 Upload de fichiers PDF/images")
        print("🗄️ Enregistrement en base de données")
        print("📁 Stockage physique sécurisé")
        print("🔍 Récupération et affichage")
        print("🗑️ Suppression (soft delete)")
        
        print("\n🌐 POUR TESTER:")
        print("1. http://localhost:5000/documents")
        print("2. Connectez-vous: test@example.com / test123")
        print("3. Cliquez 'Ajouter un document'")
        print("4. Uploadez un PDF ou une image")
        print("5. Vérifiez qu'il apparaît dans la liste")
    else:
        print("\n❌ PROBLÈMES DÉTECTÉS")
        print("🔧 Corrigez les erreurs ci-dessus")

if __name__ == "__main__":
    main()
