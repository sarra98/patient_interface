#!/usr/bin/env python3
"""
DÉMARRAGE RAPIDE DU PROJET
"""

import os
import subprocess
import time

def main():
    print("🚀 DÉMARRAGE PROJET MÉDICAL")
    print("=" * 50)
    
    # Vérifier que la base existe
    if not os.path.exists('instance/secretaire_medicale.db'):
        print("❌ Base de données manquante")
        return
    
    print("✅ Base de données trouvée")
    
    # Démarrer Flask
    print("🔥 Démarrage Flask...")
    print("💡 Accès:")
    print("   🌐 Interface: http://localhost:5000")
    print("   📋 Inscription: http://localhost:5000/register")
    print("   🔐 Connexion: http://localhost:5000/login")
    print("   📄 Documents: http://localhost:5000/documents")
    print("   👤 Test: test@example.com / test123")
    print("=" * 50)
    
    try:
        subprocess.run(['python', 'app.py'], check=True)
    except KeyboardInterrupt:
        print("\n👋 Arrêt du serveur")
    except Exception as e:
        print(f"❌ Erreur: {str(e)}")

if __name__ == "__main__":
    main()
