#!/usr/bin/env python3
"""
Corriger les statuts des RDV pour afficher les boutons de paiement
"""

import sqlite3

def main():
    print("CORRECTION STATUTS RDV")
    print("=" * 40)
    
    try:
        conn = sqlite3.connect('instance/secretaire_medicale.db')
        cursor = conn.cursor()
        
        # Corriger tous les RDV
        cursor.execute("UPDATE rendez_vous SET statut = 'confirme', statut_paiement = 'en_attente', montant = 70.00")
        updated = cursor.rowcount
        print(f"RDV mis a jour: {updated}")
        
        conn.commit()
        
        # Vérifier
        cursor.execute("SELECT id, motif, statut, statut_paiement FROM rendez_vous LIMIT 5")
        rdvs = cursor.fetchall()
        
        print("RDV apres correction:")
        for rdv in rdvs:
            print(f"ID: {rdv[0]}, Statut: {rdv[2]}, Paiement: {rdv[3]}")
        
        conn.close()
        
        print("CORRECTION TERMINEE!")
        print("Actualisez la page: http://localhost:5000/appointments")
        
    except Exception as e:
        print(f"Erreur: {str(e)}")

if __name__ == "__main__":
    main()
