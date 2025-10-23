#!/usr/bin/env python3
"""
Vérifier le statut des RDV pour diagnostiquer pourquoi la carte verte n'apparaît pas
"""

import sqlite3

def check_rdv_status():
    """Vérifier le statut des RDV"""
    print("🔍 DIAGNOSTIC STATUT RDV")
    print("=" * 50)
    
    try:
        conn = sqlite3.connect('instance/secretaire_medicale.db')
        cursor = conn.cursor()
        
        # Vérifier tous les RDV
        cursor.execute("""
            SELECT id, motif, statut, statut_paiement, montant, date_rdv 
            FROM rendez_vous 
            ORDER BY id DESC 
            LIMIT 10
        """)
        rdvs = cursor.fetchall()
        
        print(f"📊 {len(rdvs)} RDV récents:")
        print("-" * 80)
        print("ID | Motif | Statut RDV | Statut Paiement | Montant | Date")
        print("-" * 80)
        
        for rdv in rdvs:
            rdv_id, motif, statut, statut_paiement, montant, date_rdv = rdv
            motif_short = (motif[:20] + '...') if motif and len(motif) > 20 else (motif or 'N/A')
            print(f"{rdv_id:2} | {motif_short:23} | {statut:10} | {statut_paiement:15} | {montant:7} | {date_rdv}")
        
        # Compter par statut
        cursor.execute("SELECT statut, COUNT(*) FROM rendez_vous GROUP BY statut")
        statuts = cursor.fetchall()
        
        print(f"\n📈 RÉPARTITION PAR STATUT RDV:")
        for statut, count in statuts:
            print(f"  {statut}: {count} RDV")
        
        # Compter par statut de paiement
        cursor.execute("SELECT statut_paiement, COUNT(*) FROM rendez_vous GROUP BY statut_paiement")
        paiements = cursor.fetchall()
        
        print(f"\n💳 RÉPARTITION PAR STATUT PAIEMENT:")
        for statut, count in paiements:
            statut_display = statut if statut else 'NULL'
            print(f"  {statut_display}: {count} RDV")
        
        # Vérifier les conditions pour la carte verte
        cursor.execute("""
            SELECT COUNT(*) 
            FROM rendez_vous 
            WHERE statut = 'confirme' AND statut_paiement = 'en_attente'
        """)
        green_card_count = cursor.fetchone()[0]
        
        print(f"\n💚 RDV QUI DEVRAIENT AVOIR LA CARTE VERTE:")
        print(f"   (statut='confirme' ET statut_paiement='en_attente')")
        print(f"   Nombre: {green_card_count}")
        
        if green_card_count == 0:
            print("\n❌ PROBLÈME IDENTIFIÉ:")
            print("   Aucun RDV n'a les bons statuts pour la carte verte!")
            print("\n💡 SOLUTION:")
            print("   Il faut mettre à jour les statuts des RDV")
        else:
            print(f"\n✅ {green_card_count} RDV devraient avoir la carte verte")
        
        conn.close()
        return green_card_count > 0
        
    except Exception as e:
        print(f"❌ Erreur: {str(e)}")
        return False

def fix_rdv_status():
    """Corriger les statuts des RDV pour afficher la carte verte"""
    print(f"\n🔧 CORRECTION STATUTS RDV")
    print("=" * 50)
    
    try:
        conn = sqlite3.connect('instance/secretaire_medicale.db')
        cursor = conn.cursor()
        
        # Mettre tous les RDV en statut confirmé avec paiement en attente
        cursor.execute("""
            UPDATE rendez_vous 
            SET statut = 'confirme', 
                statut_paiement = 'en_attente', 
                montant = 70.00 
            WHERE statut != 'annule'
        """)
        
        updated = cursor.rowcount
        print(f"✅ {updated} RDV mis à jour")
        
        conn.commit()
        
        # Vérifier après correction
        cursor.execute("""
            SELECT COUNT(*) 
            FROM rendez_vous 
            WHERE statut = 'confirme' AND statut_paiement = 'en_attente'
        """)
        green_card_count = cursor.fetchone()[0]
        
        print(f"✅ {green_card_count} RDV ont maintenant les bons statuts")
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Erreur: {str(e)}")
        return False

def main():
    """Diagnostic principal"""
    print("🚨 DIAGNOSTIC CARTE VERTE MANQUANTE")
    print("=" * 60)
    
    # Vérifier les statuts actuels
    has_green_cards = check_rdv_status()
    
    if not has_green_cards:
        print("\n🔧 CORRECTION AUTOMATIQUE...")
        fix_ok = fix_rdv_status()
        
        if fix_ok:
            print("\n✅ CORRECTION TERMINÉE!")
            print("\n🌐 MAINTENANT TESTEZ:")
            print("1. Actualisez la page: http://localhost:5000/appointments")
            print("2. Connectez-vous: test@example.com / test123")
            print("3. Vous devriez voir les CARTES VERTES!")
        else:
            print("\n❌ CORRECTION ÉCHOUÉE")
    else:
        print("\n✅ LES STATUTS SONT CORRECTS")
        print("\n💡 SI VOUS NE VOYEZ PAS LA CARTE VERTE:")
        print("1. Actualisez la page (F5)")
        print("2. Vérifiez la console JavaScript (F12)")
        print("3. Reconnectez-vous si nécessaire")

if __name__ == "__main__":
    main()
