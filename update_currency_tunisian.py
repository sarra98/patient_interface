#!/usr/bin/env python3
"""
Mettre à jour la devise vers dinars tunisiens (70 DT)
"""

import sqlite3

def update_currency_and_amount():
    """Mettre à jour le montant vers 70 dinars tunisiens"""
    print("💰 MISE À JOUR DEVISE TUNISIENNE")
    print("=" * 50)
    
    try:
        conn = sqlite3.connect('instance/secretaire_medicale.db')
        cursor = conn.cursor()
        
        # Mettre à jour le montant par défaut pour tous les RDV
        cursor.execute("UPDATE rendez_vous SET montant = 70.00 WHERE montant IS NULL OR montant = 50.00")
        updated_rows = cursor.rowcount
        print(f"✅ {updated_rows} rendez-vous mis à jour avec 70 DT")
        
        # Vérifier les montants
        cursor.execute("SELECT COUNT(*), montant FROM rendez_vous GROUP BY montant")
        amounts = cursor.fetchall()
        
        print("📊 Répartition des montants:")
        for count, amount in amounts:
            if amount:
                print(f"  {count} RDV à {amount} DT")
            else:
                print(f"  {count} RDV sans montant")
        
        conn.commit()
        conn.close()
        
        print("✅ Mise à jour terminée")
        return True
        
    except Exception as e:
        print(f"❌ Erreur: {str(e)}")
        return False

def main():
    """Mise à jour principale"""
    print("🇹🇳 MISE À JOUR DEVISE TUNISIENNE")
    print("=" * 60)
    print("💰 Changement: 50€ → 70 DT")
    print("=" * 60)
    
    success = update_currency_and_amount()
    
    if success:
        print("\n🎉 DEVISE MISE À JOUR!")
        print("\nCHANGEMENTS:")
        print("💰 Montant consultation: 70 DT")
        print("🇹🇳 Devise: Dinars Tunisiens")
        print("\nÉTAPES SUIVANTES:")
        print("1. Mise à jour du code (montant par défaut)")
        print("2. Mise à jour de l'interface (affichage DT)")
        print("3. Test du système de paiement")
    else:
        print("\n❌ MISE À JOUR ÉCHOUÉE")

if __name__ == "__main__":
    main()
