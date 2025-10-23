#!/usr/bin/env python3
"""
Ajouter colonnes paiement - version simple
"""

import sqlite3

def main():
    print("AJOUT COLONNES PAIEMENT")
    print("=" * 40)
    
    try:
        conn = sqlite3.connect('instance/secretaire_medicale.db')
        cursor = conn.cursor()
        
        # Ajouter les colonnes une par une
        columns = [
            "statut_paiement VARCHAR(20) DEFAULT 'en_attente'",
            "mode_paiement VARCHAR(20)",
            "montant DECIMAL(10,2) DEFAULT 50.00",
            "date_paiement DATETIME",
            "reference_paiement VARCHAR(100)",
            "paiement_confirme BOOLEAN DEFAULT 0"
        ]
        
        for column in columns:
            try:
                cursor.execute(f"ALTER TABLE rendez_vous ADD COLUMN {column}")
                print(f"Colonne ajoutee: {column.split()[0]}")
            except sqlite3.OperationalError as e:
                if "duplicate column name" in str(e):
                    print(f"Existe deja: {column.split()[0]}")
                else:
                    print(f"Erreur: {str(e)}")
        
        conn.commit()
        conn.close()
        
        print("COLONNES PAIEMENT AJOUTEES!")
        print("Redemarrez Flask: python app.py")
        
    except Exception as e:
        print(f"Erreur: {str(e)}")

if __name__ == "__main__":
    main()
