from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from marshmallow import Schema, fields, ValidationError, validate
from datetime import datetime, timedelta
from models import RendezVous, Medecin, Patient
from database import db

appointment_bp = Blueprint('appointments', __name__)

class AppointmentSchema(Schema):
    medecin_id = fields.Int(required=True)
    date_rdv = fields.Str(required=True)  # Accepter comme string pour parsing manuel
    motif = fields.Str(required=True, validate=validate.Length(min=3, max=255))
    notes = fields.Str(required=False, allow_none=True)

class AppointmentUpdateSchema(Schema):
    statut = fields.Str(required=False, validate=validate.OneOf(['planifie', 'confirme', 'annule', 'termine']))
    notes = fields.Str(required=False, allow_none=True)


@appointment_bp.route('/medecins', methods=['GET'])
@jwt_required()
def get_medecins():
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

@appointment_bp.route('/occupied-slots', methods=['GET'])
@jwt_required()
def get_occupied_slots():
    """Récupérer les créneaux occupés pour une date donnée"""
    try:
        date_str = request.args.get('date')
        if not date_str:
            return jsonify({'error': 'Date requise'}), 400

        print(f"🔍 Vérification créneaux pour: {date_str}")

        # Convertir la date
        from datetime import datetime
        date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()

        # Récupérer tous les RDV pour cette date
        appointments = RendezVous.query.filter_by(
            date_rdv=date_obj,
            statut='confirmé'
        ).all()

        print(f"📋 {len(appointments)} RDV trouvés pour {date_str}")

        # Extraire les heures occupées
        occupied_slots = []
        for rdv in appointments:
            if rdv.heure_rdv:
                time_str = rdv.heure_rdv.strftime('%H:%M')
                occupied_slots.append(time_str)
                print(f"  ❌ Créneau occupé: {time_str}")

        return jsonify({'occupied_slots': occupied_slots}), 200

    except Exception as e:
        print(f"❌ Erreur récupération créneaux: {str(e)}")
        return jsonify({'error': 'Erreur lors de la récupération des créneaux'}), 500

@appointment_bp.route('/', methods=['POST'])
@jwt_required()
def create_appointment():
    try:
        current_patient_id = get_jwt_identity()

        print(f"🔍 CRÉATION RDV - Données reçues: {request.json}")

        schema = AppointmentSchema()
        data = schema.load(request.json)

        print(f"📋 Données validées: {data}")

        # Parser la date/heure
        try:
            date_rdv_str = data['date_rdv']
            if 'T' in date_rdv_str:
                # Format ISO: 2025-01-16T14:30:00
                date_rdv = datetime.fromisoformat(date_rdv_str.replace('Z', ''))
            else:
                # Format simple: 2025-01-16 14:30
                date_rdv = datetime.strptime(date_rdv_str, '%Y-%m-%d %H:%M')

            print(f"📅 Date parsée: {date_rdv}")

        except ValueError as e:
            print(f"❌ Erreur parsing date: {str(e)}")
            return jsonify({'error': f'Format de date invalide: {date_rdv_str}'}), 400

        medecin = Medecin.query.get(data['medecin_id'])
        if not medecin:
            print(f"❌ Médecin non trouvé: ID {data['medecin_id']}")
            return jsonify({'error': 'Médecin non trouvé'}), 404

        if date_rdv <= datetime.utcnow():
            return jsonify({'error': 'La date du rendez-vous doit être dans le futur'}), 400

        # Vérifier les créneaux existants
        existing_rdv = RendezVous.query.filter(
            RendezVous.medecin_id == data['medecin_id'],
            RendezVous.date_rdv.between(
                date_rdv - timedelta(minutes=30),
                date_rdv + timedelta(minutes=30)
            ),
            RendezVous.statut.in_(['planifie', 'confirme'])
        ).first()

        if existing_rdv:
            print(f"❌ Créneau occupé: {existing_rdv.date_rdv}")
            return jsonify({'error': 'Ce créneau est déjà occupé'}), 409

        # Créer le rendez-vous
        rdv = RendezVous(
            patient_id=current_patient_id,
            medecin_id=data['medecin_id'],
            date_rdv=date_rdv,
            motif=data['motif'],
            notes=data.get('notes'),
            statut='planifie'
        )

        print(f"📋 RDV créé: {rdv.motif} - {rdv.date_rdv}")

        db.session.add(rdv)
        db.session.commit()

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
    try:
        current_patient_id = get_jwt_identity()

        rdv = RendezVous.query.filter_by(id=appointment_id, patient_id=current_patient_id).first()
        if not rdv:
            return jsonify({'error': 'Rendez-vous non trouvé'}), 404

        schema = AppointmentUpdateSchema()
        data = schema.load(request.json)

        for field, value in data.items():
            setattr(rdv, field, value)

        rdv.updated_at = datetime.utcnow()
        db.session.commit()

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
def delete_appointment(appointment_id):
    """Supprimer définitivement un rendez-vous"""
    try:
        current_patient_id = get_jwt_identity()

        print(f"🗑️ Suppression RDV ID: {appointment_id} par patient: {current_patient_id}")

        rdv = RendezVous.query.filter_by(id=appointment_id, patient_id=current_patient_id).first()
        if not rdv:
            return jsonify({'error': 'Rendez-vous non trouvé'}), 404

        print(f"📋 RDV trouvé: {rdv.motif} - {rdv.date_rdv}")

        # Supprimer définitivement de la base de données
        db.session.delete(rdv)
        db.session.commit()

        print(f"✅ RDV supprimé avec succès")

        return jsonify({
            'message': 'Rendez-vous supprimé avec succès'
        }), 200

    except Exception as e:
        db.session.rollback()
        print(f"❌ Erreur suppression RDV: {str(e)}")
        return jsonify({'error': 'Erreur lors de la suppression du rendez-vous'}), 500

@appointment_bp.route('/<int:appointment_id>/cancel', methods=['PUT'])
@jwt_required()
def cancel_appointment(appointment_id):
    """Annuler un rendez-vous (changement de statut)"""
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
