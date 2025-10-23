#!/usr/bin/env python3
"""
Installation automatique des dépendances
"""

import subprocess
import sys

def install_package(package):
    """Installer un package Python"""
    try:
        print(f"📦 Installation de {package}...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        print(f"✅ {package} installé avec succès")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Erreur installation {package}: {e}")
        return False

def main():
    """Installation principale"""
    print("🚀 INSTALLATION DÉPENDANCES SYSTÈME MÉDICAL")
    print("=" * 60)
    
    # Liste des packages requis
    packages = [
        "flask",
        "flask-sqlalchemy", 
        "flask-jwt-extended",
        "marshmallow",
        "werkzeug",
        "requests",
        "twilio"  # Pour les SMS (optionnel)
    ]
    
    print(f"📋 Installation de {len(packages)} packages...")
    
    success_count = 0
    for package in packages:
        if install_package(package):
            success_count += 1
        print()  # Ligne vide
    
    print("=" * 60)
    print(f"📊 RÉSULTAT: {success_count}/{len(packages)} packages installés")
    
    if success_count == len(packages):
        print("🎉 TOUTES LES DÉPENDANCES INSTALLÉES!")
        print("💡 Vous pouvez maintenant démarrer avec: python app.py")
    else:
        print("⚠️  CERTAINES INSTALLATIONS ONT ÉCHOUÉ")
        print("💡 Essayez d'installer manuellement les packages manquants")
    
    return success_count == len(packages)

if __name__ == "__main__":
    main()
