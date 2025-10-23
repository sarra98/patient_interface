#!/usr/bin/env python3
"""
DÉMARRAGE FINAL AVEC VOTRE BASE
"""

import subprocess
import os

def main():
    print("🚀 DÉMARRAGE PROJET MÉDICAL FINAL")
    print("=" * 60)
    
    if not os.path.exists('instance/secretaire_medicale.db'):
        print("❌ Base manquante!")
        return
    
    print("✅ Base fonctionnelle détectée")
    print("🔥 Démarrage Flask...")
    print()
    print("🌐 ACCÈS:")
    print("   📱 http://localhost:5000")
    print("   🔐 http://localhost:5000/login")
    print("   📋 http://localhost:5000/register")
    print("   📄 http://localhost:5000/documents")
    print()
    print("👤 COMPTE TEST:")
    print("   📧 test@example.com")
    print("   🔑 test123")
    print()
    print("=" * 60)
    
    try:
        subprocess.run(['python', 'app.py'], check=True)
    except KeyboardInterrupt:
        print("\n👋 Arrêt")
    except Exception as e:
        print(f"❌ Erreur: {str(e)}")

if __name__ == "__main__":
    main()
