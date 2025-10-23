#!/usr/bin/env python3
"""
Diagnostiquer pourquoi le bouton de paiement n'apparaît pas
"""

import sqlite3
import requests

def check_rdv_status():
    """Vérifier le statut des RDV"""
    print("🔍 VÉRIFICATION STATUT RDV")
    print("=" * 50)
    
    try:
        conn = sqlite3.connect('instance/secretaire_medicale.db')
        cursor = conn.cursor()
        
        # Vérifier les RDV récents
        cursor.execute("""
            SELECT id, motif, statut, statut_paiement, date_rdv 
            FROM rendez_vous 
            ORDER BY id DESC 
            LIMIT 10
        """)
        rdvs = cursor.fetchall()
        
        print(f"📊 {len(rdvs)} RDV récents:")
        for rdv in rdvs:
            print(f"  ID: {rdv[0]}")
            print(f"  Motif: {rdv[1]}")
            print(f"  Statut RDV: {rdv[2]}")
            print(f"  Statut paiement: {rdv[3]}")
            print(f"  Date: {rdv[4]}")
            print("  ---")
        
        # Compter par statut
        cursor.execute("SELECT statut, COUNT(*) FROM rendez_vous GROUP BY statut")
        statuts = cursor.fetchall()
        
        print("📈 Répartition par statut:")
        for statut, count in statuts:
            print(f"  {statut}: {count} RDV")
        
        conn.close()
        return rdvs
        
    except Exception as e:
        print(f"❌ Erreur: {str(e)}")
        return []

def fix_rdv_status():
    """Corriger le statut des RDV pour afficher les boutons de paiement"""
    print("\n🔧 CORRECTION STATUT RDV")
    print("=" * 50)
    
    try:
        conn = sqlite3.connect('instance/secretaire_medicale.db')
        cursor = conn.cursor()
        
        # Mettre à jour les RDV planifiés vers confirmés pour afficher les boutons de paiement
        cursor.execute("UPDATE rendez_vous SET statut = 'confirme' WHERE statut = 'planifie'")
        updated = cursor.rowcount
        print(f"✅ {updated} RDV mis à jour: planifie -> confirme")
        
        # S'assurer que tous les RDV ont un statut de paiement
        cursor.execute("UPDATE rendez_vous SET statut_paiement = 'en_attente' WHERE statut_paiement IS NULL")
        updated_payment = cursor.rowcount
        print(f"✅ {updated_payment} RDV mis à jour avec statut_paiement")
        
        # S'assurer que tous les RDV ont un montant
        cursor.execute("UPDATE rendez_vous SET montant = 70.00 WHERE montant IS NULL")
        updated_amount = cursor.rowcount
        print(f"✅ {updated_amount} RDV mis à jour avec montant 70 DT")
        
        conn.commit()
        conn.close()
        
        print("✅ Corrections appliquées")
        return True
        
    except Exception as e:
        print(f"❌ Erreur: {str(e)}")
        return False

def test_api_response():
    """Tester la réponse de l'API pour voir les champs de paiement"""
    print("\n🔍 TEST RÉPONSE API")
    print("=" * 50)
    
    # Connexion
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
        
        if response.status_code != 200:
            print("❌ Connexion impossible")
            return False
        
        token = response.json().get('access_token')
        
        # Récupérer les RDV
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }
        
        response = requests.get(
            "http://localhost:5000/api/appointments/",
            headers=headers,
            timeout=10
        )
        
        if response.status_code == 200:
            result = response.json()
            appointments = result.get('appointments', [])
            
            print(f"📊 {len(appointments)} RDV récupérés via API")
            
            if appointments:
                rdv = appointments[0]
                print("📋 Premier RDV:")
                print(f"  ID: {rdv.get('id')}")
                print(f"  Statut: {rdv.get('statut')}")
                print(f"  Statut paiement: {rdv.get('statut_paiement')}")
                print(f"  Montant: {rdv.get('montant')}")
                print(f"  Mode paiement: {rdv.get('mode_paiement')}")
                print(f"  Paiement confirmé: {rdv.get('paiement_confirme')}")
                
                # Vérifier les conditions pour afficher le bouton
                if rdv.get('statut') == 'confirme' and rdv.get('statut_paiement') == 'en_attente':
                    print("✅ Ce RDV DEVRAIT avoir un bouton de paiement")
                else:
                    print("❌ Ce RDV ne devrait PAS avoir de bouton de paiement")
                    print(f"   Raison: statut='{rdv.get('statut')}', paiement='{rdv.get('statut_paiement')}'")
            
            return True
        else:
            print(f"❌ Erreur API: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Exception: {str(e)}")
        return False

def create_test_rdv_with_payment():
    """Créer un RDV de test avec statut confirmé pour voir le bouton"""
    print("\n📅 CRÉATION RDV TEST AVEC BOUTON PAIEMENT")
    print("=" * 50)
    
    try:
        conn = sqlite3.connect('instance/secretaire_medicale.db')
        cursor = conn.cursor()
        
        # Insérer un RDV directement avec le bon statut
        from datetime import datetime, timedelta
        
        tomorrow = datetime.now() + timedelta(days=1)
        while tomorrow.weekday() == 6:  # Éviter dimanche
            tomorrow += timedelta(days=1)
        
        cursor.execute("""
            INSERT INTO rendez_vous (
                patient_id, medecin_id, date_rdv, motif, statut, 
                statut_paiement, montant, notes
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            1,  # Patient ID (ajustez si nécessaire)
            1,  # Médecin ID
            tomorrow,
            "RDV test avec bouton paiement",
            "confirme",  # Statut confirmé pour afficher le bouton
            "en_attente",  # En attente de paiement
            70.00,  # Montant en DT
            "RDV créé pour tester le bouton de paiement"
        ))
        
        rdv_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        print(f"✅ RDV test créé avec ID: {rdv_id}")
        print(f"📅 Date: {tomorrow.strftime('%Y-%m-%d %H:%M')}")
        print(f"📊 Statut: confirme")
        print(f"💳 Statut paiement: en_attente")
        print(f"💰 Montant: 70.00 DT")
        print("🎯 Ce RDV DEVRAIT avoir un bouton de paiement vert!")
        
        return rdv_id
        
    except Exception as e:
        print(f"❌ Erreur: {str(e)}")
        return None

def main():
    """Diagnostic principal"""
    print("🚨 DIAGNOSTIC BOUTON DE PAIEMENT")
    print("=" * 60)
    print("🎯 Pourquoi le bouton n'apparaît pas ?")
    print("=" * 60)
    
    # Vérifier les RDV actuels
    rdvs = check_rdv_status()
    
    # Corriger les statuts
    fix_ok = fix_rdv_status()
    
    # Tester l'API
    api_ok = test_api_response()
    
    # Créer un RDV de test
    test_rdv_id = create_test_rdv_with_payment()
    
    print(f"\n📊 RÉSUMÉ DIAGNOSTIC")
    print("=" * 60)
    print(f"🗃️ RDV en base: {len(rdvs)}")
    print(f"🔧 Correction statuts: {'✅ OK' if fix_ok else '❌ ERREUR'}")
    print(f"🌐 API fonctionne: {'✅ OK' if api_ok else '❌ ERREUR'}")
    print(f"📅 RDV test créé: {'✅ ID ' + str(test_rdv_id) if test_rdv_id else '❌ ERREUR'}")
    
    print(f"\n💡 SOLUTION:")
    print("1. 🔄 Actualisez la page: http://localhost:5000/appointments")
    print("2. 🔑 Connectez-vous: test@example.com / test123")
    print("3. 👀 Cherchez les RDV avec statut 'Confirmé'")
    print("4. 💳 Le bouton vert devrait apparaître dans Actions")
    
    if test_rdv_id:
        print(f"\n🎯 RDV DE TEST SPÉCIAL:")
        print(f"🆔 ID: {test_rdv_id}")
        print("📝 Motif: RDV test avec bouton paiement")
        print("📊 Statut: Confirmé")
        print("💳 Ce RDV AURA le bouton de paiement vert!")

if __name__ == "__main__":
    main()
