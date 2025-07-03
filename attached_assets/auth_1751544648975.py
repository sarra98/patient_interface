from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity
from marshmallow import Schema, fields, ValidationError, validate
from datetime import datetime

auth_bp = Blueprint('auth', __name__)

class PatientRegistrationSchema(Schema):
    prenom = fields.Str(required=True, validate=validate.Length(min=2, max=100))
    nom = fields.Str(required=True, validate=validate.Length(min=2, max=100))
    email = fields.Email(required=True)
    telephone = fields.Str(required=True, validate=validate.Length(min=10, max=20))
    date_naissance = fields.Date(required=True)
    adresse = fields.Str(required=False, allow_none=True)
    antecedents_medicaux = fields.Str(required=False, allow_none=True)
    contact_urgence_nom = fields.Str(required=True, validate=validate.Length(min=2, max=100))
    contact_urgence_telephone = fields.Str(required=True, validate=validate.Length(min=10, max=20))
    password = fields.Str(required=True, validate=validate.Length(min=6))
    confirm_password = fields.Str(required=True)

class PatientLoginSchema(Schema):
    email = fields.Email(required=True)
    password = fields.Str(required=True)

@auth_bp.route('/register', methods=['POST'])
def register_patient():
    """Register a new patient"""
    try:
        # Import here to avoid circular imports
        from models import Patient
        from database import db
        
        schema = PatientRegistrationSchema()
        data = schema.load(request.json)
        
        # Check if passwords match
        if data['password'] != data['confirm_password']:
            return jsonify({'error': 'Les mots de passe ne correspondent pas'}), 400
        
        # Check if patient already exists
        existing_patient = Patient.query.filter_by(email=data['email']).first()
        if existing_patient:
            return jsonify({'error': 'Un compte avec cet email existe déjà'}), 409
        
        # Create new patient
        patient = Patient(
            prenom=data['prenom'],
            nom=data['nom'],
            email=data['email'],
            telephone=data['telephone'],
            date_naissance=data['date_naissance'],
            adresse=data.get('adresse'),
            antecedents_medicaux=data.get('antecedents_medicaux'),
            contact_urgence_nom=data['contact_urgence_nom'],
            contact_urgence_telephone=data['contact_urgence_telephone']
        )
        patient.set_password(data['password'])
        
        db.session.add(patient)
        db.session.commit()
        
        # Generate tokens
        access_token = create_access_token(identity=patient.id)
        refresh_token = create_refresh_token(identity=patient.id)
        
        return jsonify({
            'message': 'Compte créé avec succès',
            'patient': patient.to_dict(),
            'access_token': access_token,
            'refresh_token': refresh_token
        }), 201
        
    except ValidationError as err:
        return jsonify({'error': 'Données invalides', 'details': err.messages}), 400
    except Exception as e:
        from database import db
        db.session.rollback()
        print(f"Erreur lors de l'enregistrement: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': 'Erreur lors de la création du compte', 'details': str(e)}), 500

@auth_bp.route('/login', methods=['POST'])
def login_patient():
    """Authenticate a patient"""
    try:
        from models import Patient
        
        schema = PatientLoginSchema()
        data = schema.load(request.json)
        
        # Find patient by email
        patient = Patient.query.filter_by(email=data['email']).first()
        
        if not patient or not patient.check_password(data['password']):
            return jsonify({'error': 'Email ou mot de passe incorrect'}), 401
        
        if not patient.is_active:
            return jsonify({'error': 'Compte désactivé. Contactez l\'administration'}), 403
        
        # Generate tokens
        access_token = create_access_token(identity=patient.id)
        refresh_token = create_refresh_token(identity=patient.id)
        
        return jsonify({
            'message': 'Connexion réussie',
            'patient': patient.to_dict(),
            'access_token': access_token,
            'refresh_token': refresh_token
        }), 200
        
    except ValidationError as err:
        return jsonify({'error': 'Données invalides', 'details': err.messages}), 400
    except Exception as e:
        print(f"Erreur lors de la connexion: {str(e)}")
        return jsonify({'error': 'Erreur lors de la connexion'}), 500

@auth_bp.route('/profile', methods=['GET'])
@jwt_required()
def get_patient_profile():
    """Get current patient profile"""
    try:
        from models import Patient
        
        current_patient_id = get_jwt_identity()
        patient = Patient.query.get(current_patient_id)
        
        if not patient:
            return jsonify({'error': 'Patient non trouvé'}), 404
        
        return jsonify({
            'patient': patient.to_dict()
        }), 200
        
    except Exception as e:
        print(f"Erreur lors de la récupération du profil: {str(e)}")
        return jsonify({'error': 'Erreur lors de la récupération du profil'}), 500

@auth_bp.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh_token():
    """Refresh access token"""
    try:
        current_patient_id = get_jwt_identity()
        new_token = create_access_token(identity=current_patient_id)
        
        return jsonify({
            'access_token': new_token
        }), 200
        
    except Exception as e:
        print(f"Erreur lors du rafraîchissement du token: {str(e)}")
        return jsonify({'error': 'Erreur lors du rafraîchissement du token'}), 500