#!/usr/bin/env python3
"""
DÉMARRAGE RAPIDE AVEC VOTRE BASE FONCTIONNELLE
"""

import subprocess
import os

def main():
    print("🚀 DÉMARRAGE PROJET AVEC BASE FONCTIONNELLE")
    print("=" * 60)
    
    if not os.path.exists('instance/secretaire_medicale.db'):
        print("❌ Base de données non trouvée!")
        print("💡 Exécutez d'abord: python use_working_db.py")
        return
    
    print("✅ Base de données fonctionnelle détectée")
    print("🔥 Démarrage du serveur Flask...")
    print()
    print("🌐 ACCÈS AU PROJET:")
    print("   📱 Interface principale: http://localhost:5000")
    print("   🔐 Page de connexion: http://localhost:5000/login")
    print("   📋 Page d'inscription: http://localhost:5000/register")
    print("   📄 Gestion documents: http://localhost:5000/documents")
    print("   📅 Rendez-vous: http://localhost:5000/appointments")
    print()
    print("👤 COMPTES EXISTANTS:")
    print("   Utilisez les comptes de votre base de données")
    print("   Ou créez un nouveau compte via l'inscription")
    print()
    print("=" * 60)
    print("🛑 Appuyez sur Ctrl+C pour arrêter le serveur")
    print("=" * 60)
    
    try:
        subprocess.run(['python', 'app.py'], check=True)
    except KeyboardInterrupt:
        print("\n👋 Serveur arrêté")
    except Exception as e:
        print(f"❌ Erreur: {str(e)}")

if __name__ == "__main__":
    main()
