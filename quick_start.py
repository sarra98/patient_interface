#!/usr/bin/env python3
"""
Démarrage rapide et simple du système
"""

import os
import sys
import subprocess

def check_file_exists(filepath, description):
    """Vérifier qu'un fichier existe"""
    if os.path.exists(filepath):
        print(f"✅ {description}: {filepath}")
        return True
    else:
        print(f"❌ {description} manquant: {filepath}")
        return False

def create_missing_files():
    """Créer les fichiers manquants essentiels"""
    print("🔧 CRÉATION FICHIERS MANQUANTS")
    print("=" * 50)
    
    # Créer le dossier uploads si nécessaire
    upload_dir = "uploads/documents"
    if not os.path.exists(upload_dir):
        os.makedirs(upload_dir, exist_ok=True)
        print(f"✅ Dossier créé: {upload_dir}")
    
    # Créer le dossier instance si nécessaire
    instance_dir = "instance"
    if not os.path.exists(instance_dir):
        os.makedirs(instance_dir, exist_ok=True)
        print(f"✅ Dossier créé: {instance_dir}")

def install_missing_deps():
    """Installer les dépendances manquantes"""
    print("📦 INSTALLATION DÉPENDANCES CRITIQUES")
    print("=" * 50)
    
    critical_packages = [
        "flask-sqlalchemy",
        "flask-jwt-extended"
    ]
    
    for package in critical_packages:
        try:
            print(f"📦 Installation {package}...")
            subprocess.check_call([
                sys.executable, "-m", "pip", "install", package
            ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            print(f"✅ {package} installé")
        except:
            print(f"❌ Échec installation {package}")

def main():
    """Démarrage principal"""
    print("🚀 DÉMARRAGE RAPIDE SYSTÈME MÉDICAL")
    print("=" * 60)
    
    # Vérifier les fichiers essentiels
    essential_files = [
        ("app.py", "Application principale"),
        ("models.py", "Modèles de données"),
        ("instance/secretaire_medicale.db", "Base de données")
    ]
    
    print("🔍 VÉRIFICATION FICHIERS ESSENTIELS")
    print("=" * 50)
    
    missing_files = []
    for filepath, description in essential_files:
        if not check_file_exists(filepath, description):
            missing_files.append(filepath)
    
    if missing_files:
        print(f"\n⚠️  Fichiers manquants: {missing_files}")
        print("💡 Assurez-vous d'être dans le bon dossier")
        return False
    
    # Créer les dossiers manquants
    create_missing_files()
    
    # Installer les dépendances critiques
    install_missing_deps()
    
    # Essayer de démarrer Flask
    print("\n🚀 DÉMARRAGE FLASK")
    print("=" * 50)
    print("💡 Flask va démarrer sur http://localhost:5000")
    print("💡 Appuyez sur Ctrl+C pour arrêter")
    print("=" * 50)
    
    try:
        # Démarrer app.py
        subprocess.run([sys.executable, "app.py"])
    except KeyboardInterrupt:
        print("\n🛑 Arrêt demandé")
    except Exception as e:
        print(f"\n❌ Erreur démarrage: {str(e)}")
        print("\n💡 SOLUTIONS:")
        print("1. Exécutez: python install_dependencies.py")
        print("2. Puis: python app.py")
        return False
    
    return True

if __name__ == "__main__":
    main()
