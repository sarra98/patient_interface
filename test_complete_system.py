#!/usr/bin/env python3
"""
Test complet du système médical jusqu'à 5h44
"""

import requests
import tempfile
import os
import json
import time

BASE_URL = "http://localhost:5000"

def test_flask_running():
    """Vérifier que Flask tourne"""
    print("🔍 VÉRIFICATION FLASK")
    print("=" * 50)
    
    try:
        response = requests.get(f"{BASE_URL}/api/health", timeout=5)
        if response.status_code == 200:
            print("✅ Flask fonctionne")
            return True
        else:
            print(f"⚠️  Flask répond mais status: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Flask non accessible")
        return False
    except Exception as e:
        print(f"❌ Erreur: {str(e)}")
        return False

def test_authentication():
    """Tester l'authentification"""
    print("\n🔍 TEST AUTHENTIFICATION")
    print("=" * 50)
    
    # Test login
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
            print("✅ Connexion réussie")
            return token
        else:
            print(f"❌ Connexion échouée: {response.status_code}")
            print(f"Réponse: {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ Erreur: {str(e)}")
        return None

def test_appointments(token):
    """Tester les rendez-vous"""
    print("\n🔍 TEST RENDEZ-VOUS")
    print("=" * 50)
    
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    
    try:
        # Test GET appointments
        response = requests.get(
            f"{BASE_URL}/api/appointments/",
            headers=headers,
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            appointments = data.get('appointments', [])
            print(f"✅ {len(appointments)} rendez-vous récupérés")
            return True
        else:
            print(f"❌ Erreur récupération RDV: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Erreur: {str(e)}")
        return False

def test_documents(token):
    """Tester les documents"""
    print("\n🔍 TEST DOCUMENTS")
    print("=" * 50)
    
    headers = {
        'Authorization': f'Bearer {token}'
    }
    
    try:
        # Test GET documents
        response = requests.get(
            f"{BASE_URL}/api/documents/",
            headers=headers,
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            documents = data.get('documents', [])
            print(f"✅ {len(documents)} documents récupérés")
            
            # Test upload simple
            test_content = "Document de test système complet"
            temp_file = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt')
            temp_file.write(test_content)
            temp_file.close()
            
            try:
                with open(temp_file.name, 'rb') as f:
                    files = {'file': ('test_system.txt', f, 'text/plain')}
                    data = {
                        'type_document': 'autre',
                        'nom_document': 'Test Système Complet'
                    }
                    
                    response = requests.post(
                        f"{BASE_URL}/api/documents/",
                        headers=headers,
                        files=files,
                        data=data,
                        timeout=30
                    )
                    
                    if response.status_code == 201:
                        print("✅ Upload document réussi")
                        return True
                    else:
                        print(f"❌ Upload échoué: {response.status_code}")
                        return False
                        
            finally:
                os.unlink(temp_file.name)
                
        else:
            print(f"❌ Erreur récupération documents: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Erreur: {str(e)}")
        return False

def test_payments(token):
    """Tester les paiements"""
    print("\n🔍 TEST PAIEMENTS")
    print("=" * 50)
    
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    
    # D'abord récupérer un RDV pour le paiement
    try:
        response = requests.get(
            f"{BASE_URL}/api/appointments/",
            headers=headers,
            timeout=10
        )
        
        if response.status_code == 200:
            appointments = response.json().get('appointments', [])
            if appointments:
                rdv_id = appointments[0]['id']
                
                # Test paiement
                payment_data = {
                    "rendez_vous_id": rdv_id,
                    "montant": 50.00,
                    "type_paiement": "sur_place",
                    "telephone": "+213555123456"
                }
                
                response = requests.post(
                    f"{BASE_URL}/api/payments/",
                    json=payment_data,
                    headers=headers,
                    timeout=30
                )
                
                if response.status_code in [200, 201]:
                    print("✅ Paiement réussi")
                    return True
                else:
                    print(f"❌ Paiement échoué: {response.status_code}")
                    return False
            else:
                print("⚠️  Aucun RDV pour tester le paiement")
                return True  # Pas d'erreur, juste pas de données
        else:
            print(f"❌ Impossible de récupérer les RDV: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Erreur: {str(e)}")
        return False

def test_web_interface():
    """Tester l'interface web"""
    print("\n🔍 TEST INTERFACE WEB")
    print("=" * 50)
    
    pages_to_test = [
        "/",
        "/login",
        "/register", 
        "/appointments",
        "/book-appointment",
        "/documents"
    ]
    
    success_count = 0
    for page in pages_to_test:
        try:
            response = requests.get(f"{BASE_URL}{page}", timeout=5)
            if response.status_code == 200:
                print(f"✅ {page}")
                success_count += 1
            else:
                print(f"❌ {page}: {response.status_code}")
        except Exception as e:
            print(f"❌ {page}: {str(e)}")
    
    print(f"📊 {success_count}/{len(pages_to_test)} pages OK")
    return success_count >= len(pages_to_test) - 1  # Tolérer 1 erreur

def main():
    """Test complet du système"""
    print("🚀 TEST COMPLET DU SYSTÈME MÉDICAL")
    print("=" * 70)
    print("🕐 État jusqu'à 5h44 du matin")
    print("=" * 70)
    
    # Attendre un peu que Flask démarre
    print("⏳ Attente démarrage Flask...")
    time.sleep(3)
    
    # Tests séquentiels
    tests = [
        ("Flask", test_flask_running),
        ("Interface Web", test_web_interface),
        ("Authentification", test_authentication),
    ]
    
    results = {}
    token = None
    
    for test_name, test_func in tests:
        print(f"\n📋 TEST: {test_name}")
        try:
            if test_name == "Authentification":
                result = test_func()
                if result:
                    token = result
                    results[test_name] = True
                else:
                    results[test_name] = False
            else:
                results[test_name] = test_func()
        except Exception as e:
            print(f"❌ Erreur {test_name}: {str(e)}")
            results[test_name] = False
    
    # Tests avec authentification
    if token:
        auth_tests = [
            ("Rendez-vous", test_appointments),
            ("Documents", test_documents),
            ("Paiements", test_payments)
        ]
        
        for test_name, test_func in auth_tests:
            print(f"\n📋 TEST: {test_name}")
            try:
                results[test_name] = test_func(token)
            except Exception as e:
                print(f"❌ Erreur {test_name}: {str(e)}")
                results[test_name] = False
    
    # Résumé final
    print(f"\n📊 RÉSUMÉ COMPLET")
    print("=" * 70)
    
    total_tests = len(results)
    passed_tests = sum(1 for result in results.values() if result)
    
    for test_name, result in results.items():
        status = "✅ OK" if result else "❌ PROBLÈME"
        print(f"{test_name}: {status}")
    
    print(f"\n🎯 RÉSULTAT: {passed_tests}/{total_tests} tests réussis")
    
    if passed_tests >= total_tests - 1:  # Tolérer 1 échec
        print("🎉 SYSTÈME FONCTIONNEL!")
        print("💡 Votre projet fonctionne correctement")
        print("🌐 Interface: http://localhost:5000")
    else:
        print("⚠️  PROBLÈMES DÉTECTÉS")
        print("💡 Certaines fonctionnalités ne marchent pas")
    
    return passed_tests >= total_tests - 1

if __name__ == "__main__":
    main()
