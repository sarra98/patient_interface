#!/usr/bin/env python3
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
    print("\nTEST DOCUMENTS")
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
    print("\nTEST RENDEZ-VOUS")
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
    
    print("\nRESUME")
    print("=" * 50)
    print(f"Documents: {'OK' if docs_ok else 'ERREUR'}")
    print(f"Rendez-vous: {'OK' if appointments_ok else 'ERREUR'}")
    
    if docs_ok and appointments_ok:
        print("\nTOUTES LES CORRECTIONS REUSSIES!")
        print("Le systeme fonctionne parfaitement")
    else:
        print("\nCERTAINS PROBLEMES PERSISTENT")

if __name__ == "__main__":
    main()
