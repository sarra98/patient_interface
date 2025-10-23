#!/usr/bin/env python3
"""
Script pour initialiser les nouvelles tables de documents et paiements
"""

from app import create_app
from database import db
from models import DocumentMedical, Paiement
import os

def init_documents_and_payment_tables():
    """Initialiser les tables de documents et paiements"""
    print("🔧 Initialisation des tables de documents et paiements...")

    app = create_app()

    with app.app_context():
        try:
            # Créer les nouvelles tables
            db.create_all()
            print("✅ Tables créées avec succès")

            # Créer le dossier d'upload s'il n'existe pas
            upload_folder = 'uploads/documents'
            os.makedirs(upload_folder, exist_ok=True)
            print(f"✅ Dossier d'upload créé: {upload_folder}")

            print("\n🎉 Initialisation terminée avec succès!")
            print("\n📋 Nouvelles fonctionnalités disponibles:")
            print("- 📁 Gestion des documents médicaux")
            print("- 📤 Upload de fichiers (PDF, images, documents)")
            print("- 💳 Système de paiement complet")
            print("- 🏦 Paiement par carte bancaire")
            print("- 📮 Paiement par carte postale (CCP)")
            print("- 🧾 Génération de reçus")
            print("- 📊 Historique des paiements")

            return True

        except Exception as e:
            print(f"❌ Erreur lors de l'initialisation: {str(e)}")
            return False

if __name__ == "__main__":
    success = init_documents_and_payment_tables()
    if not success:
        exit(1)
