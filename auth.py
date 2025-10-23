from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from datetime import datetime

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register_patient():
    """Register ultra-simple"""
    try:
        from models import Patient
        from database import db
        
        data = request.json
        
        # Validation minimale
        email = data.get('email', '').strip()
        password = data.get('password', '')
        prenom = data.get('prenom', '').strip()
        nom = data.get('nom', '').strip()
        telephone = data.get('telephone', '').strip()
        date_naissance = data.get('date_naissance')
        contact_urgence_nom = data.get('contact_urgence_nom', '').strip()
        contact_urgence_telephone = data.get('contact_urgence_telephone', '').strip()
        
        if not email or not password or not prenom or not nom:
            return jsonify({'error': 'Champs requis manquants'}), 400
        
        if len(password) < 6:
            return jsonify({'error': 'Mot de passe trop court (min 6 caracteres)'}), 400
        
        # Vérifier si l'email existe déjà
        existing_patient = Patient.query.filter_by(email=email).first()
        if existing_patient:
            return jsonify({'error': 'Cet email est deja utilise'}), 409
        
        # Parser la date de naissance
        try:
            if date_naissance:
                if isinstance(date_naissance, str):
                    date_naissance = datetime.strptime(date_naissance, '%Y-%m-%d').date()
            else:
                date_naissance = datetime(1990, 1, 1).date()
        except:
            date_naissance = datetime(1990, 1, 1).date()
        
        # Créer le patient
        patient = Patient(
            prenom=prenom,
            nom=nom,
            email=email,
            telephone=telephone or '+213555000000',
            date_naissance=date_naissance,
            adresse=data.get('adresse', ''),
            antecedents_medicaux=data.get('antecedents_medicaux', ''),
            contact_urgence_nom=contact_urgence_nom or 'Contact Urgence',
            contact_urgence_telephone=contact_urgence_telephone or '+213555000001'
        )
        
        patient.set_password(password)
        
        db.session.add(patient)
        db.session.commit()
        
        return jsonify({
            'message': 'Patient enregistre avec succes',
            'patient_id': patient.id
        }), 201
        
    except Exception as e:
        try:
            db.session.rollback()
        except:
            pass
        return jsonify({'error': f'Erreur: {str(e)}'}), 500

@auth_bp.route('/login', methods=['POST'])
def login_patient():
    """Login ultra-simple"""
    try:
        from models import Patient
        
        data = request.json
        
        email = data.get('email', '').strip()
        password = data.get('password', '')
        
        if not email or not password:
            return jsonify({'error': 'Email et mot de passe requis'}), 400
        
        # Trouver le patient
        patient = Patient.query.filter_by(email=email, is_active=True).first()
        
        if not patient:
            return jsonify({'error': 'Email ou mot de passe incorrect'}), 401
        
        # Vérifier le mot de passe
        if not patient.check_password(password):
            return jsonify({'error': 'Email ou mot de passe incorrect'}), 401
        
        # Créer le token avec l'ID en string
        access_token = create_access_token(identity=str(patient.id))
        
        return jsonify({
            'message': 'Connexion reussie',
            'access_token': access_token,
            'patient': {
                'id': patient.id,
                'prenom': patient.prenom,
                'nom': patient.nom,
                'email': patient.email
            }
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'Erreur: {str(e)}'}), 500

@auth_bp.route('/profile', methods=['GET'])
@jwt_required()
def get_profile():
    """Profile ultra-simple"""
    try:
        from models import Patient
        
        current_patient_id = int(get_jwt_identity())
        patient = Patient.query.get(current_patient_id)
        
        if not patient:
            return jsonify({'error': 'Patient non trouve'}), 404
        
        return jsonify({
            'patient': {
                'id': patient.id,
                'prenom': patient.prenom,
                'nom': patient.nom,
                'email': patient.email,
                'telephone': patient.telephone
            }
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'Erreur: {str(e)}'}), 500

@auth_bp.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    """Logout ultra-simple"""
    return jsonify({'message': 'Deconnexion reussie'}), 200
