#!/usr/bin/env python3
"""
Test spécifique pour la création de rendez-vous
"""

import requests
import json
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
            print("✅ Token obtenu")
            return token
        else:
            print(f"❌ Échec connexion: {response.status_code}")
            print(f"Réponse: {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ Erreur connexion: {str(e)}")
        return None

def check_medecins():
    """Vérifier les médecins disponibles"""
    print("\n🔍 VÉRIFICATION MÉDECINS")
    print("=" * 50)
    
    try:
        import sqlite3
        conn = sqlite3.connect('instance/secretaire_medicale.db')
        cursor = conn.cursor()
        
        cursor.execute("SELECT id, nom, prenom, specialite, is_active FROM medecins")
        medecins = cursor.fetchall()
        
        print(f"📋 {len(medecins)} médecins en base:")
        for medecin in medecins:
            status = "✅ Actif" if medecin[4] else "❌ Inactif"
            print(f"  ID {medecin[0]}: Dr {medecin[1]} {medecin[2]} ({medecin[3]}) - {status}")
        
        conn.close()
        
        if medecins:
            return medecins[0][0]  # Retourner l'ID du premier médecin
        else:
            return None
            
    except Exception as e:
        print(f"❌ Erreur: {str(e)}")
        return None

def test_appointment_creation_detailed(token, medecin_id):
    """Test détaillé de création de RDV"""
    print(f"\n🔍 TEST CRÉATION RDV DÉTAILLÉ")
    print("=" * 50)
    
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    
    # Créer un RDV pour demain à 14h30
    tomorrow = datetime.now() + timedelta(days=1)
    # S'assurer que ce n'est pas un dimanche
    while tomorrow.weekday() == 6:  # Dimanche
        tomorrow += timedelta(days=1)
    
    # Format exact comme envoyé par l'interface
    date_time = f"{tomorrow.strftime('%Y-%m-%d')}T14:30:00"
    
    appointment_data = {
        "medecin_id": medecin_id,
        "date_rdv": date_time,
        "motif": "Consultation de test",
        "notes": "Test de création depuis script"
    }
    
    print(f"📤 Données envoyées:")
    for key, value in appointment_data.items():
        print(f"  {key}: {value}")
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/appointments/",
            json=appointment_data,
            headers=headers,
            timeout=30
        )
        
        print(f"📥 Status: {response.status_code}")
        print(f"📄 Headers: {dict(response.headers)}")
        
        if response.status_code == 201:
            result = response.json()
            print("✅ RDV CRÉÉ AVEC SUCCÈS!")
            print(f"📋 Message: {result.get('message')}")
            
            appointment = result.get('appointment', {})
            print(f"🆔 ID: {appointment.get('id')}")
            print(f"📅 Date: {appointment.get('date_rdv')}")
            print(f"📝 Motif: {appointment.get('motif')}")
            
            return True
            
        elif response.status_code == 422:
            print("❌ ERREUR 422 - VALIDATION")
            try:
                error_data = response.json()
                print(f"💬 Erreur: {json.dumps(error_data, indent=2)}")
            except:
                print(f"💬 Réponse brute: {response.text}")
            return False
            
        elif response.status_code == 400:
            print("❌ ERREUR 400 - DONNÉES INVALIDES")
            try:
                error_data = response.json()
                print(f"💬 Erreur: {error_data}")
            except:
                print(f"💬 Réponse: {response.text}")
            return False
            
        elif response.status_code == 404:
            print("❌ ERREUR 404 - MÉDECIN NON TROUVÉ")
            try:
                error_data = response.json()
                print(f"💬 Erreur: {error_data}")
            except:
                print(f"💬 Réponse: {response.text}")
            return False
            
        else:
            print(f"❌ AUTRE ERREUR: {response.status_code}")
            try:
                error_data = response.json()
                print(f"💬 Erreur: {json.dumps(error_data, indent=2)}")
            except:
                print(f"💬 Réponse: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Erreur: {str(e)}")
        return False

def test_get_appointments(token):
    """Tester la récupération des RDV"""
    print(f"\n🔍 TEST RÉCUPÉRATION RDV")
    print("=" * 50)
    
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    
    try:
        response = requests.get(
            f"{BASE_URL}/api/appointments/",
            headers=headers,
            timeout=10
        )
        
        print(f"📥 Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            appointments = data.get('appointments', [])
            print(f"✅ {len(appointments)} RDV récupérés")
            
            for i, rdv in enumerate(appointments[:3]):
                print(f"  {i+1}. {rdv.get('motif', 'Sans motif')} - {rdv.get('date_rdv', 'Sans date')}")
            
            return True
        else:
            print(f"❌ Erreur récupération: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Erreur: {str(e)}")
        return False

def main():
    """Test principal de création RDV"""
    print("🚀 TEST CRÉATION RENDEZ-VOUS")
    print("=" * 70)
    print("🔧 Diagnostic complet du problème")
    print("=" * 70)
    
    # Vérifier les médecins
    medecin_id = check_medecins()
    if not medecin_id:
        print("❌ Aucun médecin disponible")
        print("💡 Ajoutez un médecin en base pour tester")
        return
    
    # Obtenir le token
    token = get_auth_token()
    if not token:
        print("❌ Impossible d'obtenir le token")
        return
    
    # Test récupération RDV
    get_ok = test_get_appointments(token)
    
    # Test création RDV
    create_ok = test_appointment_creation_detailed(token, medecin_id)
    
    # Résumé
    print(f"\n📊 RÉSUMÉ TEST RDV")
    print("=" * 70)
    print(f"👨‍⚕️ Médecin ID: {medecin_id}")
    print(f"📥 Récupération: {'✅ OK' if get_ok else '❌ ERREUR'}")
    print(f"📤 Création: {'✅ OK' if create_ok else '❌ ERREUR'}")
    
    if create_ok:
        print("\n🎉 CRÉATION RDV FONCTIONNE!")
        print("💡 Le problème était probablement temporaire")
        print("🌐 Testez dans l'interface: http://localhost:5000/book-appointment")
    else:
        print("\n❌ PROBLÈME CRÉATION RDV")
        print("💡 Vérifiez les logs Flask pour l'erreur exacte")
        print("💡 Le problème pourrait être:")
        print("  - Médecin inexistant")
        print("  - Format de date incorrect")
        print("  - Validation échouée")
        print("  - Problème de base de données")
    
    return create_ok

if __name__ == "__main__":
    main()
