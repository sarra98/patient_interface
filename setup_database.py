#!/usr/bin/env python3
"""Setup database with default doctor Ahmed Samir"""

from app import create_app
from database import db
from models import Medecin

def setup_database():
    """Initialize database and create default doctor"""
    app = create_app()
    
    with app.app_context():
        print("Creating database tables...")
        db.create_all()
        
        # Check if Ahmed Samir already exists
        doctor = Medecin.query.filter_by(nom='Samir', prenom='Ahmed').first()
        
        if not doctor:
            print("Creating default doctor: Ahmed Samir...")
            doctor = Medecin(
                nom='Samir',
                prenom='Ahmed',
                specialite='Médecin Généraliste',
                telephone='+33 1 23 45 67 89',
                email='ahmed.samir@clinique.com',
                horaires='Lun-Ven 8h-18h, Sam 9h-12h',
                is_active=True
            )
            db.session.add(doctor)
            db.session.commit()
            print(f"Doctor created with ID: {doctor.id}")
        else:
            print(f"Doctor Ahmed Samir already exists with ID: {doctor.id}")
        
        print("Database setup complete!")
        return doctor

if __name__ == '__main__':
    setup_database()
