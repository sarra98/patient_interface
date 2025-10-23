#!/usr/bin/env python3
"""
Configuration de la base de données
"""

from flask_sqlalchemy import SQLAlchemy

# Instance globale de SQLAlchemy
db = SQLAlchemy()

def init_db(app):
    """Initialiser la base de données avec l'application Flask"""
    db.init_app(app)
    
    with app.app_context():
        # Créer toutes les tables si elles n'existent pas
        db.create_all()
        print("✅ Base de données initialisée")

def get_db():
    """Obtenir l'instance de la base de données"""
    return db
