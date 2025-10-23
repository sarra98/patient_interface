#!/usr/bin/env python3
"""
Créer un utilisateur de test pour résoudre le problème de connexion
"""

import sqlite3
import hashlib
from datetime import datetime, date

def hash_password(password):
    """Hasher le mot de passe comme dans l'application"""
    # Utiliser le même hachage que werkzeug.security
    from werkzeug.security import generate_password_hash
    return generate_password_hash(password)

def check_existing_users():
    """Vérifier les utilisateurs existants"""
    print("🔍 VÉRIFICATION UTILISATEURS EXISTANTS")
    print("=" * 50)
    
    try:
        conn = sqlite3.connect('instance/secretaire_medicale.db')
        cursor = conn.cursor()
        
        cursor.execute("SELECT id, email, prenom, nom FROM patients")
        users = cursor.fetchall()
        
        print(f"📊 {len(users)} utilisateurs en base:")
        for user in users:
            print(f"  ID {user[0]}: {user[1]} ({user[2]} {user[3]})")
        
        conn.close()
        return users
        
    except Exception as e:
        print(f"❌ Erreur: {str(e)}")
        return []

def create_test_user():
    """Créer un utilisateur de test"""
    print("\n👤 CRÉATION UTILISATEUR DE TEST")
    print("=" * 50)
    
    try:
        conn = sqlite3.connect('instance/secretaire_medicale.db')
        cursor = conn.cursor()
        
        # Vérifier si l'utilisateur existe déjà
        cursor.execute("SELECT id FROM patients WHERE email = ?", ('test@example.com',))
        existing = cursor.fetchone()
        
        if existing:
            print(f"✅ Utilisateur test@example.com existe déjà (ID: {existing[0]})")
            conn.close()
            return True
        
        # Créer l'utilisateur de test
        password_hash = hash_password('test123')
        
        cursor.execute("""
            INSERT INTO patients (
                prenom, nom, email, telephone, date_naissance, 
                adresse, contact_urgence_nom, contact_urgence_telephone, 
                password_hash, is_active
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            'Test',
            'User',
            'test@example.com',
            '+213555000000',
            date(1990, 1, 1),
            '123 Rue Test, Alger',
            'Contact Urgence',
            '+213555000001',
            password_hash,
            1
        ))
        
        user_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        print(f"✅ Utilisateur créé avec ID: {user_id}")
        print(f"📧 Email: test@example.com")
        print(f"🔑 Mot de passe: test123")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur création: {str(e)}")
        return False

def test_login_with_new_user():
    """Tester la connexion avec le nouvel utilisateur"""
    print("\n🔍 TEST CONNEXION NOUVEL UTILISATEUR")
    print("=" * 50)
    
    import requests
    
    login_data = {
        "email": "test@example.com",
        "password": "test123"
    }
    
    try:
        response = requests.post(
            "http://localhost:5000/api/auth/login",
            json=login_data,
            headers={'Content-Type': 'application/json'},
            timeout=10
        )
        
        print(f"📥 Status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            token = result.get('access_token')
            print(f"✅ Connexion réussie!")
            print(f"🔑 Token obtenu: {token[:20]}..." if token else "❌ Pas de token")
            return token
        else:
            print(f"❌ Erreur: {response.status_code}")
            try:
                error = response.json()
                print(f"💬 Détails: {error}")
            except:
                print(f"💬 Réponse: {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ Exception: {str(e)}")
        return None

def test_appointment_creation_direct(token):
    """Test direct de création de RDV"""
    print("\n🔍 TEST CRÉATION RDV DIRECT")
    print("=" * 50)
    
    if not token:
        print("❌ Pas de token")
        return False
    
    import requests
    
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    
    appointment_data = {
        "medecin_id": 1,
        "date_rdv": "2025-07-18T14:30:00",
        "motif": "Test creation directe",
        "notes": "Test"
    }
    
    print(f"📤 Données: {appointment_data}")
    
    try:
        response = requests.post(
            "http://localhost:5000/api/appointments/",
            json=appointment_data,
            headers=headers,
            timeout=30
        )
        
        print(f"📥 Status: {response.status_code}")
        
        if response.status_code == 201:
            result = response.json()
            print(f"✅ RDV créé avec succès!")
            print(f"📋 Message: {result.get('message')}")
            return True
        else:
            print(f"❌ Erreur: {response.status_code}")
            try:
                error = response.json()
                print(f"💬 Détails: {error}")
            except:
                print(f"💬 Réponse: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Exception: {str(e)}")
        return False

def main():
    """Création utilisateur et test complet"""
    print("🚀 CRÉATION UTILISATEUR DE TEST ET DIAGNOSTIC")
    print("=" * 70)
    print("🎯 Résoudre le problème de connexion et RDV")
    print("=" * 70)
    
    # Vérifier utilisateurs existants
    existing_users = check_existing_users()
    
    # Créer utilisateur de test
    user_created = create_test_user()
    
    if not user_created:
        print("❌ Impossible de créer l'utilisateur de test")
        return
    
    # Tester la connexion
    token = test_login_with_new_user()
    
    if not token:
        print("❌ Connexion impossible même avec le nouvel utilisateur")
        print("💡 Problème dans la route /api/auth/login")
        return
    
    # Tester la création de RDV
    rdv_created = test_appointment_creation_direct(token)
    
    # Résumé
    print(f"\n📊 RÉSUMÉ COMPLET")
    print("=" * 70)
    print(f"👤 Utilisateur test: ✅ Créé")
    print(f"🔑 Connexion: {'✅ OK' if token else '❌ ERREUR'}")
    print(f"📅 Création RDV: {'✅ OK' if rdv_created else '❌ ERREUR'}")
    
    if rdv_created:
        print("\n🎉 PROBLÈME RÉSOLU!")
        print("💡 Vous pouvez maintenant:")
        print("  1. Vous connecter avec: test@example.com / test123")
        print("  2. Créer des rendez-vous dans l'interface")
        print("  3. Utiliser: http://localhost:5000/book-appointment")
    else:
        print("\n❌ PROBLÈME PERSISTE")
        print("💡 Le problème vient des routes API")
        print("💡 Exécutez: python fix_422_final.py")
    
    return rdv_created

if __name__ == "__main__":
    main()
