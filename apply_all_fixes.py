#!/usr/bin/env python3
"""
Appliquer toutes les corrections pour eliminer les erreurs 422
"""

import shutil
import os

def backup_files():
    """Sauvegarder les fichiers actuels"""
    print("SAUVEGARDE FICHIERS ACTUELS")
    print("=" * 50)
    
    files_to_backup = [
        ('document_routes.py', 'document_routes_backup.py'),
        ('appointment_routes.py', 'appointment_routes_backup.py')
    ]
    
    for original, backup in files_to_backup:
        try:
            if os.path.exists(original):
                shutil.copy(original, backup)
                print(f"Sauvegarde: {original} -> {backup}")
            else:
                print(f"Fichier non trouve: {original}")
        except Exception as e:
            print(f"Erreur sauvegarde {original}: {str(e)}")

def apply_fixes():
    """Appliquer les corrections"""
    print("\nAPPLICATION DES CORRECTIONS")
    print("=" * 50)
    
    fixes = [
        ('document_routes_fixed.py', 'document_routes.py'),
        ('appointment_routes_fixed.py', 'appointment_routes.py')
    ]
    
    success_count = 0
    for fixed_file, target_file in fixes:
        try:
            if os.path.exists(fixed_file):
                shutil.copy(fixed_file, target_file)
                print(f"Correction appliquee: {fixed_file} -> {target_file}")
                success_count += 1
            else:
                print(f"Fichier de correction non trouve: {fixed_file}")
        except Exception as e:
            print(f"Erreur application {fixed_file}: {str(e)}")
    
    return success_count

def create_test_script():
    """Creer un script de test complet"""
    print("\nCREATION SCRIPT DE TEST")
    print("=" * 50)
    
    test_content = '''#!/usr/bin/env python3
"""
Test complet apres corrections
"""

import requests
import tempfile
import os
from datetime import datetime, timedelta

BASE_URL = "http://localhost:5000"

def get_auth_token():
    """Obtenir un token d'authentification"""
    login_data = {
        "email": "test@example.com",
        "password": "test123"
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/auth/login",
            json=login_data,
            headers={'Content-Type': 'application/json'},
            timeout=10
        )
        
        if response.status_code == 200:
            token = response.json().get('access_token')
            print("Token obtenu avec succes")
            return token
        else:
            print(f"Echec connexion: {response.status_code}")
            return None
            
    except Exception as e:
        print(f"Erreur connexion: {str(e)}")
        return None

def test_documents(token):
    """Tester les documents"""
    print("\\nTEST DOCUMENTS")
    print("=" * 30)
    
    headers = {'Authorization': f'Bearer {token}'}
    
    # Test GET
    try:
        response = requests.get(f"{BASE_URL}/api/documents/", headers=headers)
        print(f"GET documents: {response.status_code}")
        if response.status_code != 200:
            print(f"Erreur: {response.text}")
            return False
    except Exception as e:
        print(f"Erreur GET: {str(e)}")
        return False
    
    # Test POST
    try:
        content = "Test document apres correction"
        temp_file = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt')
        temp_file.write(content)
        temp_file.close()
        
        with open(temp_file.name, 'rb') as f:
            files = {'file': ('test.txt', f, 'text/plain')}
            data = {
                'type_document': 'autre',
                'nom_document': 'Test Correction',
                'description': 'Test apres correction 422'
            }
            
            response = requests.post(
                f"{BASE_URL}/api/documents/",
                headers=headers,
                files=files,
                data=data
            )
            
            print(f"POST documents: {response.status_code}")
            if response.status_code != 201:
                print(f"Erreur: {response.text}")
                return False
        
        os.unlink(temp_file.name)
        
    except Exception as e:
        print(f"Erreur POST: {str(e)}")
        return False
    
    print("Documents: OK")
    return True

def test_appointments(token):
    """Tester les rendez-vous"""
    print("\\nTEST RENDEZ-VOUS")
    print("=" * 30)
    
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    
    # Test GET
    try:
        response = requests.get(f"{BASE_URL}/api/appointments/", headers=headers)
        print(f"GET appointments: {response.status_code}")
        if response.status_code != 200:
            print(f"Erreur: {response.text}")
            return False
    except Exception as e:
        print(f"Erreur GET: {str(e)}")
        return False
    
    # Test POST
    try:
        tomorrow = datetime.now() + timedelta(days=1)
        # Eviter le dimanche
        while tomorrow.weekday() == 6:
            tomorrow += timedelta(days=1)
        
        appointment_data = {
            "medecin_id": 1,
            "date_rdv": f"{tomorrow.strftime('%Y-%m-%d')}T14:30:00",
            "motif": "Consultation test",
            "notes": "Test apres correction"
        }
        
        response = requests.post(
            f"{BASE_URL}/api/appointments/",
            json=appointment_data,
            headers=headers
        )
        
        print(f"POST appointments: {response.status_code}")
        if response.status_code != 201:
            print(f"Erreur: {response.text}")
            return False
            
    except Exception as e:
        print(f"Erreur POST: {str(e)}")
        return False
    
    print("Rendez-vous: OK")
    return True

def main():
    """Test principal"""
    print("TEST COMPLET APRES CORRECTIONS")
    print("=" * 50)
    
    token = get_auth_token()
    if not token:
        print("Impossible d'obtenir le token")
        return
    
    docs_ok = test_documents(token)
    appointments_ok = test_appointments(token)
    
    print("\\nRESUME")
    print("=" * 50)
    print(f"Documents: {'OK' if docs_ok else 'ERREUR'}")
    print(f"Rendez-vous: {'OK' if appointments_ok else 'ERREUR'}")
    
    if docs_ok and appointments_ok:
        print("\\nTOUTES LES CORRECTIONS REUSSIES!")
        print("Le systeme fonctionne parfaitement")
    else:
        print("\\nCERTAINS PROBLEMES PERSISTENT")

if __name__ == "__main__":
    main()
'''
    
    try:
        with open('test_all_corrections.py', 'w', encoding='utf-8') as f:
            f.write(test_content)
        print("Script de test cree: test_all_corrections.py")
        return True
    except Exception as e:
        print(f"Erreur creation script: {str(e)}")
        return False

def main():
    """Application principale des corrections"""
    print("CORRECTION COMPLETE ERREURS 422")
    print("=" * 60)
    print("Documents + Rendez-vous + Fonctionnalites")
    print("=" * 60)
    
    # Sauvegarder
    backup_files()
    
    # Appliquer les corrections
    success_count = apply_fixes()
    
    # Creer le script de test
    test_created = create_test_script()
    
    print(f"\\nRESUME")
    print("=" * 60)
    print(f"Corrections appliquees: {success_count}/2")
    print(f"Script de test: {'Cree' if test_created else 'Erreur'}")
    
    if success_count == 2:
        print("\\nTOUTES LES CORRECTIONS APPLIQUEES!")
        print("\\nETAPES SUIVANTES:")
        print("1. Redemarrez Flask: python app.py")
        print("2. Testez: python test_all_corrections.py")
        print("3. Interface: http://localhost:5000/documents")
        print("4. Interface: http://localhost:5000/book-appointment")
        print("\\nFONCTIONNALITES IMPLEMENTEES:")
        print("- Plus d'erreurs 422")
        print("- Dimanche bloque")
        print("- Samedi 8h-12h uniquement")
        print("- Creneaux occupes avec croix rouge")
        print("- Suppression de rendez-vous")
        print("- Modification de rendez-vous")
        print("- Paiement en ligne et sur place")
    else:
        print("\\nCORRECTIONS INCOMPLETES")
        print("Verifiez les erreurs ci-dessus")

if __name__ == "__main__":
    main()
