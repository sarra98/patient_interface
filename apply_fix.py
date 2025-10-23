#!/usr/bin/env python3
"""
Appliquer la correction simple
"""

import shutil
import os

def main():
    print("CORRECTION SIMPLE ERREURS 422")
    print("=" * 50)
    
    try:
        # Sauvegarder l'ancien fichier
        if os.path.exists('document_routes.py'):
            shutil.copy('document_routes.py', 'document_routes_backup.py')
            print("Sauvegarde creee: document_routes_backup.py")
        
        # Remplacer par la version corrigee
        if os.path.exists('document_routes_fixed.py'):
            shutil.copy('document_routes_fixed.py', 'document_routes.py')
            print("Routes remplacees par la version simplifiee")
            print("CORRECTION APPLIQUEE!")
            print("")
            print("REDEMARREZ FLASK:")
            print("python app.py")
            print("")
            print("PUIS TESTEZ:")
            print("python test_upload_simple.py")
        else:
            print("Erreur: document_routes_fixed.py non trouve")
            
    except Exception as e:
        print(f"Erreur: {str(e)}")

if __name__ == "__main__":
    main()
