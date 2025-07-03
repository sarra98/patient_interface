from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from marshmallow import Schema, fields, ValidationError, validate
from datetime import datetime, timedelta
from models import RendezVous, Medecin, Patient
from database import db

appointment_bp = Blueprint('appointments', __name__)

class AppointmentSchema(Schema):
    medecin_id = fields.Int(required=True)
    date_rdv = fields.DateTime(required=True)
    motif = fields.Str(required=True, validate=validate.Length(min=3, max=255))
    notes = fields.Str(required=False, allow_none=True)

class AppointmentUpdateSchema(Schema):
    statut = fields.Str(required=False, validate=validate.OneOf(['planifie', 'confirme', 'annule', 'termine']))
    notes = fields.Str(required=False, allow_none=True)

@appointment_bp.route('/medecins', methods=['GET'])
@jwt_required()
def get_medecins():
    """Get all active doctors"""
    try:
        medecins = Medecin.query.filter_by(is_active=True).all()
        return jsonify({
            'medecins': [medecin.to_dict() for medecin in medecins]
        }), 200
    except Exception as e:
        print(f"Erreur lors de la récupération des médecins: {str(e)}")
        return jsonify({'error': 'Erreur lors de la récupération des médecins'}), 500

@appointment_bp.route('/', methods=['GET'])
@jwt_required()
def get_appointments():
    """Get patient's appointments"""
    try:
        current_patient_id = get_jwt_identity()
        patient = Patient.query.get(current_patient_id)
        
        if not patient:
            return jsonify({'error': 'Patient non trouvé'}), 404
        
        appointments = RendezVous.query.filter_by(patient_id=current_patient_id).order_by(RendezVous.date_rdv.desc()).all()
        
        appointments_data = []
        for rdv in appointments:
            rdv_dict = rdv.to_dict()
            rdv_dict['medecin'] = rdv.medecin.to_dict() if rdv.medecin else None
            rdv_dict['patient'] = {
                'id': patient.id,
                'nom': patient.nom,
                'prenom': patient.prenom
            }
            appointments_data.append(rdv_dict)
        
        return jsonify({
            'appointments': appointments_data
        }), 200
        
    except Exception as e:
        print(f"Erreur lors de la récupération des rendez-vous: {str(e)}")
        return jsonify({'error': 'Erreur lors de la récupération des rendez-vous'}), 500

@appointment_bp.route('/', methods=['POST'])
@jwt_required()
def create_appointment():
    """Create a new appointment"""
    try:
        current_patient_id = get_jwt_identity()
        
        schema = AppointmentSchema()
        data = schema.load(request.json)
        
        # Verify doctor exists and is active
        medecin = Medecin.query.get(data['medecin_id'])
        if not medecin or not medecin.is_active:
            return jsonify({'error': 'Médecin non trouvé ou non disponible'}), 404
        
        # Check if appointment time is in the future
        if data['date_rdv'] <= datetime.utcnow():
            return jsonify({'error': 'La date du rendez-vous doit être dans le futur'}), 400
        
        # Check for conflicting appointments (same doctor, overlapping time)
        existing_rdv = RendezVous.query.filter(
            RendezVous.medecin_id == data['medecin_id'],
            RendezVous.date_rdv.between(
                data['date_rdv'] - timedelta(minutes=30),
                data['date_rdv'] + timedelta(minutes=30)
            ),
            RendezVous.statut.in_(['planifie', 'confirme'])
        ).first()
        
        if existing_rdv:
            return jsonify({'error': 'Ce créneau est déjà occupé'}), 409
        
        # Create new appointment
        rdv = RendezVous(
            patient_id=current_patient_id,
            medecin_id=data['medecin_id'],
            date_rdv=data['date_rdv'],
            motif=data['motif'],
            notes=data.get('notes'),
            statut='planifie'
        )
        
        db.session.add(rdv)
        db.session.commit()
        
        # Return appointment with related data
        rdv_dict = rdv.to_dict()
        rdv_dict['medecin'] = medecin.to_dict()
        
        return jsonify({
            'message': 'Rendez-vous créé avec succès',
            'appointment': rdv_dict
        }), 201
        
    except ValidationError as err:
        return jsonify({'error': 'Données invalides', 'details': err.messages}), 400
    except Exception as e:
        db.session.rollback()
        print(f"Erreur lors de la création du rendez-vous: {str(e)}")
        return jsonify({'error': 'Erreur lors de la création du rendez-vous'}), 500

@appointment_bp.route('/<int:appointment_id>', methods=['PUT'])
@jwt_required()
def update_appointment(appointment_id):
    """Update an appointment"""
    try:
        current_patient_id = get_jwt_identity()
        
        rdv = RendezVous.query.filter_by(id=appointment_id, patient_id=current_patient_id).first()
        if not rdv:
            return jsonify({'error': 'Rendez-vous non trouvé'}), 404
        
        schema = AppointmentUpdateSchema()
        data = schema.load(request.json)
        
        # Update fields
        for field, value in data.items():
            setattr(rdv, field, value)
        
        rdv.updated_at = datetime.utcnow()
        db.session.commit()
        
        # Return updated appointment with related data
        rdv_dict = rdv.to_dict()
        rdv_dict['medecin'] = rdv.medecin.to_dict() if rdv.medecin else None
        
        return jsonify({
            'message': 'Rendez-vous mis à jour avec succès',
            'appointment': rdv_dict
        }), 200
        
    except ValidationError as err:
        return jsonify({'error': 'Données invalides', 'details': err.messages}), 400
    except Exception as e:
        db.session.rollback()
        print(f"Erreur lors de la mise à jour du rendez-vous: {str(e)}")
        return jsonify({'error': 'Erreur lors de la mise à jour du rendez-vous'}), 500

@appointment_bp.route('/<int:appointment_id>', methods=['DELETE'])
@jwt_required()
def cancel_appointment(appointment_id):
    """Cancel an appointment"""
    try:
        current_patient_id = get_jwt_identity()
        
        rdv = RendezVous.query.filter_by(id=appointment_id, patient_id=current_patient_id).first()
        if not rdv:
            return jsonify({'error': 'Rendez-vous non trouvé'}), 404
        
        if rdv.statut in ['annule', 'termine']:
            return jsonify({'error': 'Ce rendez-vous ne peut pas être annulé'}), 400
        
        rdv.statut = 'annule'
        rdv.updated_at = datetime.utcnow()
        db.session.commit()
        
        return jsonify({
            'message': 'Rendez-vous annulé avec succès'
        }), 200
        
    except Exception as e:
        db.session.rollback()
        print(f"Erreur lors de l'annulation du rendez-vous: {str(e)}")
        return jsonify({'error': 'Erreur lors de l\'annulation du rendez-vous'}), 500
