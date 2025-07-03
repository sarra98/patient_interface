from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from database import db

class Patient(db.Model):
    __tablename__ = 'patients'
    
    id = db.Column(db.Integer, primary_key=True)
    prenom = db.Column(db.String(100), nullable=False)
    nom = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    telephone = db.Column(db.String(20), nullable=False)
    date_naissance = db.Column(db.Date, nullable=False)
    adresse = db.Column(db.Text, nullable=True)
    antecedents_medicaux = db.Column(db.Text, nullable=True)
    contact_urgence_nom = db.Column(db.String(100), nullable=False)
    contact_urgence_telephone = db.Column(db.String(20), nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)
    
    # Relationship with appointments
    rendez_vous = db.relationship('RendezVous', backref='patient', lazy=True)
    
    def set_password(self, password):
        """Hash and set password"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Check if provided password matches hash"""
        return check_password_hash(self.password_hash, password)
    
    def to_dict(self):
        """Serialize patient data for API responses"""
        return {
            'id': self.id,
            'prenom': self.prenom,
            'nom': self.nom,
            'email': self.email,
            'telephone': self.telephone,
            'date_naissance': self.date_naissance.isoformat() if self.date_naissance else None,
            'adresse': self.adresse,
            'antecedents_medicaux': self.antecedents_medicaux,
            'contact_urgence_nom': self.contact_urgence_nom,
            'contact_urgence_telephone': self.contact_urgence_telephone,
            'created_at': self.created_at.isoformat(),
            'is_active': self.is_active
        }
    
    def __repr__(self):
        return f'<Patient {self.prenom} {self.nom}>'

class RendezVous(db.Model):
    __tablename__ = 'rendez_vous'
    
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id'), nullable=False)
    medecin_id = db.Column(db.Integer, db.ForeignKey('medecins.id'), nullable=False)
    date_rdv = db.Column(db.DateTime, nullable=False)
    duree = db.Column(db.Integer, default=30)  # Duration in minutes
    motif = db.Column(db.String(255), nullable=True)
    statut = db.Column(db.String(50), default='planifie')  # planifie, confirme, annule, termine
    notes = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'patient_id': self.patient_id,
            'date_rdv': self.date_rdv.isoformat(),
            'duree': self.duree,
            'motif': self.motif,
            'statut': self.statut,
            'notes': self.notes,
            'created_at': self.created_at.isoformat()
        }
    
    def __repr__(self):
        return f'<RendezVous {self.id} - {self.date_rdv}>'


class Medecin(db.Model):
    __tablename__ = 'medecins'
    
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), nullable=False)
    prenom = db.Column(db.String(100), nullable=False)
    specialite = db.Column(db.String(100), nullable=False)
    telephone = db.Column(db.String(20), nullable=True)
    email = db.Column(db.String(120), nullable=True)
    horaires = db.Column(db.String(200), nullable=True)  # Ex: "Lun-Ven 8h-18h"
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relation avec les rendez-vous
    rendez_vous = db.relationship('RendezVous', backref='medecin', lazy=True)
    
    def nom_complet(self):
        """Retourne le nom complet du médecin"""
        return f"Dr {self.prenom} {self.nom}"
    
    def to_dict(self):
        """Serialize médecin data for API responses"""
        return {
            'id': self.id,
            'nom': self.nom,
            'prenom': self.prenom,
            'nom_complet': self.nom_complet(),
            'specialite': self.specialite,
            'telephone': self.telephone,
            'email': self.email,
            'horaires': self.horaires,
            'is_active': self.is_active
        }
    
    def __repr__(self):
        return f'<Medecin {self.nom_complet()} - {self.specialite}>'
