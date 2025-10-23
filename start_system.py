#!/usr/bin/env python3
"""
Démarrage rapide du système médical
"""

import subprocess
import sys
import time
import os

def check_dependencies():
    """Vérifier les dépendances"""
    print("🔍 VÉRIFICATION DÉPENDANCES")
    print("=" * 50)
    
    required_modules = [
        'flask', 'flask_sqlalchemy', 'flask_jwt_extended', 
        'marshmallow', 'werkzeug', 'requests'
    ]
    
    missing = []
    for module in required_modules:
        try:
            __import__(module.replace('_', '.'))
            print(f"✅ {module}")
        except ImportError:
            print(f"❌ {module}")
            missing.append(module)
    
    if missing:
        print(f"\n⚠️  Modules manquants: {missing}")
        return False
    else:
        print("✅ Toutes les dépendances sont installées")
        return True

def check_database():
    """Vérifier la base de données"""
    print("\n🔍 VÉRIFICATION BASE DE DONNÉES")
    print("=" * 50)
    
    db_path = 'instance/secretaire_medicale.db'
    
    if os.path.exists(db_path):
        print(f"✅ Base de données trouvée: {db_path}")
        
        # Vérifier la taille
        size = os.path.getsize(db_path)
        print(f"📊 Taille: {size} bytes")
        
        if size > 1000:  # Au moins 1KB
            print("✅ Base de données semble valide")
            return True
        else:
            print("⚠️  Base de données très petite")
            return False
    else:
        print(f"❌ Base de données manquante: {db_path}")
        return False

def check_uploads_folder():
    """Vérifier le dossier uploads"""
    print("\n🔍 VÉRIFICATION DOSSIER UPLOADS")
    print("=" * 50)
    
    upload_dir = 'uploads/documents'
    
    if not os.path.exists(upload_dir):
        print(f"🔧 Création du dossier: {upload_dir}")
        os.makedirs(upload_dir, exist_ok=True)
    
    if os.path.exists(upload_dir):
        print(f"✅ Dossier uploads OK: {upload_dir}")
        return True
    else:
        print(f"❌ Impossible de créer: {upload_dir}")
        return False

def start_flask():
    """Démarrer Flask"""
    print("\n🚀 DÉMARRAGE FLASK")
    print("=" * 50)
    
    try:
        print("📍 Démarrage de app.py...")
        print("💡 Flask va démarrer sur http://localhost:5000")
        print("💡 Appuyez sur Ctrl+C pour arrêter")
        print("=" * 50)
        
        # Démarrer Flask
        subprocess.run([sys.executable, "app.py"], check=True)
        
    except KeyboardInterrupt:
        print("\n🛑 Arrêt demandé par l'utilisateur")
    except subprocess.CalledProcessError as e:
        print(f"❌ Erreur démarrage Flask: {e}")
        return False
    except Exception as e:
        print(f"❌ Erreur: {str(e)}")
        return False
    
    return True

def main():
    """Démarrage principal"""
    print("🚀 DÉMARRAGE SYSTÈME MÉDICAL")
    print("=" * 60)
    print("🕐 Restauration état 5h44 du matin")
    print("=" * 60)
    
    # Vérifications préalables
    checks = [
        ("Dépendances", check_dependencies),
        ("Base de données", check_database),
        ("Dossier uploads", check_uploads_folder)
    ]
    
    all_ok = True
    for check_name, check_func in checks:
        try:
            if not check_func():
                all_ok = False
        except Exception as e:
            print(f"❌ Erreur {check_name}: {str(e)}")
            all_ok = False
    
    if all_ok:
        print("\n🎉 TOUTES LES VÉRIFICATIONS OK!")
        print("🚀 Démarrage du serveur...")
        
        # Démarrer Flask
        start_flask()
    else:
        print("\n❌ PROBLÈMES DÉTECTÉS")
        print("💡 Corrigez les erreurs avant de démarrer")
        
        # Proposer des solutions
        print("\n💡 SOLUTIONS POSSIBLES:")
        print("1. Installer les dépendances: pip install flask flask-sqlalchemy flask-jwt-extended marshmallow")
        print("2. Vérifier que la base de données existe")
        print("3. Créer les dossiers manquants")

if __name__ == "__main__":
    main()
