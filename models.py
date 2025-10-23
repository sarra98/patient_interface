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
    statut = db.Column(db.String(50), default='planifie')  # planifie, confirme, annule, termine, paye
    notes = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Champs de paiement
    statut_paiement = db.Column(db.String(20), default='en_attente')  # en_attente, paye, echec
    mode_paiement = db.Column(db.String(20), nullable=True)  # bancaire, sur_place
    montant = db.Column(db.Numeric(10, 2), default=70.00)  # Montant consultation en DT
    date_paiement = db.Column(db.DateTime, nullable=True)  # Date du paiement
    reference_paiement = db.Column(db.String(100), nullable=True)  # Référence transaction
    paiement_confirme = db.Column(db.Boolean, default=False)  # Confirmation paiement
    
    def to_dict(self):
        try:
            return {
                'id': self.id or 0,
                'patient_id': self.patient_id or 0,
                'medecin_id': self.medecin_id or 0,
                'date_rdv': self.date_rdv.isoformat() if self.date_rdv else None,
                'duree': self.duree or 30,
                'motif': self.motif or '',
                'statut': self.statut or 'planifie',
                'notes': self.notes or '',
                'created_at': self.created_at.isoformat() if self.created_at else None,
                # Champs de paiement
                'statut_paiement': getattr(self, 'statut_paiement', 'en_attente'),
                'mode_paiement': getattr(self, 'mode_paiement', None),
                'montant': float(self.montant) if getattr(self, 'montant', None) else 70.00,
                'date_paiement': self.date_paiement.isoformat() if getattr(self, 'date_paiement', None) else None,
                'reference_paiement': getattr(self, 'reference_paiement', None),
                'paiement_confirme': bool(getattr(self, 'paiement_confirme', False))
            }
        except Exception as e:
            return {
                'id': getattr(self, 'id', 0),
                'error': f'Erreur to_dict RendezVous: {str(e)}'
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


class DocumentMedical(db.Model):
    __tablename__ = 'documents_medicaux'

    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id'), nullable=False)
    type_document = db.Column(db.String(50), nullable=False)  # 'analyse', 'ordonnance', 'radio', 'autre'
    nom_document = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    nom_fichier = db.Column(db.String(255), nullable=False)
    chemin_fichier = db.Column(db.String(500), nullable=False)
    taille_fichier = db.Column(db.Integer)  # en bytes
    date_upload = db.Column(db.DateTime, default=datetime.utcnow)
    date_document = db.Column(db.Date)  # Date du document médical
    medecin_prescripteur = db.Column(db.String(255))  # Nom du médecin qui a prescrit

    # Relations
    patient = db.relationship('Patient', backref=db.backref('documents', lazy=True))

    def to_dict(self):
        try:
            # Gestion sécurisée du nom de fichier
            nom_fichier = self.nom_fichier
            if not nom_fichier and self.chemin_fichier:
                try:
                    nom_fichier = self.chemin_fichier.replace('\\', '/').split('/')[-1]
                except:
                    nom_fichier = str(self.chemin_fichier)

            # Gestion sécurisée du médecin
            medecin_info = None
            if hasattr(self, 'medecin_id') and self.medecin_id and hasattr(self, 'medecin') and self.medecin:
                try:
                    medecin_info = {
                        'id': self.medecin.id,
                        'nom': getattr(self.medecin, 'nom', ''),
                        'prenom': getattr(self.medecin, 'prenom', '')
                    }
                except:
                    medecin_info = {'id': self.medecin_id, 'nom': '', 'prenom': ''}

            return {
                'id': self.id,
                'patient_id': self.patient_id,
                'medecin_id': getattr(self, 'medecin_id', None),
                'rendez_vous_id': getattr(self, 'rendez_vous_id', None),
                'type_document': self.type_document or '',
                'nom_document': self.nom_document or '',
                'titre': self.nom_document or '',  # Mapping pour compatibilité
                'description': self.description or '',
                'contenu': self.description or '',  # Mapping pour compatibilité
                'fichier_path': self.chemin_fichier or '',
                'chemin_fichier': self.chemin_fichier or '',
                'nom_fichier': nom_fichier or '',
                'taille_fichier': getattr(self, 'taille_fichier', 0),
                'date_upload': self.date_creation.isoformat() if self.date_creation else None,
                'date_creation': self.date_creation.isoformat() if self.date_creation else None,
                'is_active': bool(getattr(self, 'is_active', True)),
                'medecin': medecin_info
            }
        except Exception as e:
            # En cas d'erreur, retourner un dictionnaire minimal
            return {
                'id': getattr(self, 'id', None),
                'patient_id': getattr(self, 'patient_id', None),
                'type_document': getattr(self, 'type_document', ''),
                'titre': getattr(self, 'titre', ''),
                'nom_document': getattr(self, 'titre', ''),
                'description': getattr(self, 'contenu', ''),
                'contenu': getattr(self, 'contenu', ''),
                'fichier_path': getattr(self, 'fichier_path', ''),
                'nom_fichier': '',
                'date_upload': None,
                'date_creation': None,
                'is_active': True,
                'medecin': None,
                'error': f'Erreur conversion: {str(e)}'
            }

    def __repr__(self):
        return f'<DocumentMedical {self.titre} - {self.type_document}>'


class Paiement(db.Model):
    __tablename__ = 'paiements'

    id = db.Column(db.Integer, primary_key=True)
    rendez_vous_id = db.Column(db.Integer, db.ForeignKey('rendez_vous.id'), nullable=False)
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id'), nullable=False)
    montant = db.Column(db.Float, nullable=False)
    type_paiement = db.Column(db.String(50), nullable=False)  # 'carte_bancaire', 'carte_postale', 'especes'
    statut = db.Column(db.String(50), default='en_attente')  # 'en_attente', 'valide', 'echec', 'rembourse'
    reference_transaction = db.Column(db.String(255))
    date_paiement = db.Column(db.DateTime, default=datetime.utcnow)

    # Relations
    rendez_vous = db.relationship('RendezVous', backref=db.backref('paiement', uselist=False))
    patient = db.relationship('Patient', backref=db.backref('paiements', lazy=True))

    def to_dict(self):
        return {
            'id': self.id,
            'rendez_vous_id': self.rendez_vous_id,
            'patient_id': self.patient_id,
            'montant': self.montant,
            'type_paiement': self.type_paiement,
            'statut': self.statut,
            'reference_transaction': self.reference_transaction,
            'date_paiement': self.date_paiement.isoformat() if self.date_paiement else None
        }

    def __repr__(self):
        return f'<Paiement {self.montant}€ - {self.statut}>'