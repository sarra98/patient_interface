from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime, timedelta

from models import RendezVous, Medecin
from database import db

appointment_bp = Blueprint('appointments', __name__)

@appointment_bp.route('/medecins', methods=['GET'])
@jwt_required()
def get_medecins():
    """Recuperer la liste des medecins disponibles"""
    try:
        medecins = Medecin.query.filter_by(is_active=True).all()
        return jsonify({
            'medecins': [medecin.to_dict() for medecin in medecins]
        }), 200
    except Exception as e:
        print(f"Erreur lors de la recuperation des medecins: {str(e)}")
        return jsonify({'error': 'Erreur lors de la recuperation des medecins'}), 500

@appointment_bp.route('/', methods=['GET'])
@jwt_required()
def get_appointments():
    """Recuperer tous les rendez-vous du patient connecte"""
    try:
        current_patient_id = get_jwt_identity()
        print(f"Recuperation RDV pour patient: {current_patient_id}")
        
        appointments = RendezVous.query.filter_by(
            patient_id=current_patient_id
        ).order_by(RendezVous.date_rdv.desc()).all()
        
        print(f"{len(appointments)} rendez-vous trouves")
        
        return jsonify({'appointments': [rdv.to_dict() for rdv in appointments]}), 200
        
    except Exception as e:
        print(f"Erreur lors de la recuperation des rendez-vous: {str(e)}")
        return jsonify({'error': 'Erreur lors de la recuperation des rendez-vous'}), 500

@appointment_bp.route('/occupied-slots', methods=['GET'])
@jwt_required()
def get_occupied_slots():
    """Recuperer les creneaux occupes pour une date donnee"""
    try:
        date_str = request.args.get('date')
        if not date_str:
            return jsonify({'error': 'Date requise'}), 400
        
        print(f"Verification creneaux pour: {date_str}")
        
        # Convertir la date
        date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()
        
        # Recuperer tous les RDV pour cette date
        appointments = RendezVous.query.filter_by(
            date_rdv=date_obj,
            statut='confirme'
        ).all()
        
        print(f"{len(appointments)} RDV trouves pour {date_str}")
        
        # Extraire les heures occupees
        occupied_slots = []
        for rdv in appointments:
            if rdv.heure_rdv:
                time_str = rdv.heure_rdv.strftime('%H:%M')
                occupied_slots.append(time_str)
                print(f"  Creneau occupe: {time_str}")
        
        return jsonify({'occupied_slots': occupied_slots}), 200
        
    except Exception as e:
        print(f"Erreur recuperation creneaux: {str(e)}")
        return jsonify({'error': 'Erreur lors de la recuperation des creneaux'}), 500

@appointment_bp.route('/', methods=['POST'])
@jwt_required()
def create_appointment():
    """Creer un nouveau rendez-vous - VERSION SIMPLIFIEE"""
    try:
        print("CREATION RDV SIMPLIFIE")
        current_patient_id = get_jwt_identity()
        print(f"Patient ID: {current_patient_id}")
        
        data = request.json
        print(f"Donnees recues: {data}")
        
        # Validation minimale
        medecin_id = data.get('medecin_id')
        date_rdv_str = data.get('date_rdv')
        motif = data.get('motif', '')
        notes = data.get('notes', '')
        
        if not medecin_id:
            return jsonify({'error': 'Medecin requis'}), 400
        
        if not date_rdv_str:
            return jsonify({'error': 'Date et heure requises'}), 400
        
        if not motif or len(motif) < 3:
            return jsonify({'error': 'Motif requis (min 3 caracteres)'}), 400
        
        # Parser la date/heure
        try:
            if 'T' in date_rdv_str:
                # Format ISO: 2025-01-16T14:30:00
                date_rdv = datetime.fromisoformat(date_rdv_str.replace('Z', ''))
            else:
                # Format simple: 2025-01-16 14:30
                date_rdv = datetime.strptime(date_rdv_str, '%Y-%m-%d %H:%M')
            
            print(f"Date parsee: {date_rdv}")
            
        except ValueError as e:
            print(f"Erreur parsing date: {str(e)}")
            return jsonify({'error': f'Format de date invalide: {date_rdv_str}'}), 400

        # Verifier que le medecin existe
        medecin = Medecin.query.get(medecin_id)
        if not medecin:
            print(f"Medecin non trouve: ID {medecin_id}")
            return jsonify({'error': 'Medecin non trouve'}), 404

        # Verifier que la date est dans le futur
        if date_rdv <= datetime.now():
            return jsonify({'error': 'La date du rendez-vous doit etre dans le futur'}), 400
        
        # Verifier les restrictions de jour
        day_of_week = date_rdv.weekday()  # 0=lundi, 6=dimanche
        if day_of_week == 6:  # Dimanche
            return jsonify({'error': 'Les rendez-vous ne sont pas autorises le dimanche'}), 400
        
        # Verifier les horaires du samedi
        if day_of_week == 5:  # Samedi
            if date_rdv.hour < 8 or date_rdv.hour >= 12:
                return jsonify({'error': 'Le samedi, les rendez-vous sont uniquement de 8h a 12h'}), 400

        # Verifier les creneaux existants
        existing_rdv = RendezVous.query.filter(
            RendezVous.medecin_id == medecin_id,
            RendezVous.date_rdv.between(
                date_rdv - timedelta(minutes=30),
                date_rdv + timedelta(minutes=30)
            ),
            RendezVous.statut.in_(['planifie', 'confirme'])
        ).first()

        if existing_rdv:
            print(f"Creneau occupe: {existing_rdv.date_rdv}")
            return jsonify({'error': 'Ce creneau est deja occupe'}), 409

        # Creer le rendez-vous
        rdv = RendezVous(
            patient_id=current_patient_id,
            medecin_id=medecin_id,
            date_rdv=date_rdv,
            motif=motif,
            notes=notes,
            statut='planifie'
        )
        
        print(f"RDV cree: {rdv.motif} - {rdv.date_rdv}")

        db.session.add(rdv)
        db.session.commit()

        print(f"RDV sauvegarde avec ID: {rdv.id}")

        return jsonify({
            'message': 'Rendez-vous cree avec succes',
            'appointment': rdv.to_dict()
        }), 201

    except Exception as e:
        print(f"Erreur creation RDV: {str(e)}")
        try:
            db.session.rollback()
        except:
            pass
        return jsonify({'error': f'Erreur lors de la creation du rendez-vous: {str(e)}'}), 500

@appointment_bp.route('/<int:appointment_id>', methods=['PUT'])
@jwt_required()
def update_appointment(appointment_id):
    """Mettre a jour un rendez-vous"""
    try:
        current_patient_id = get_jwt_identity()
        
        rdv = RendezVous.query.filter_by(
            id=appointment_id,
            patient_id=current_patient_id
        ).first()
        
        if not rdv:
            return jsonify({'error': 'Rendez-vous non trouve'}), 404

        data = request.json
        
        # Mise a jour simple des champs autorises
        if 'statut' in data:
            if data['statut'] in ['planifie', 'confirme', 'annule', 'termine']:
                rdv.statut = data['statut']
        
        if 'notes' in data:
            rdv.notes = data['notes']
        
        if 'date_rdv' in data:
            try:
                new_date = datetime.fromisoformat(data['date_rdv'].replace('Z', ''))
                rdv.date_rdv = new_date
            except:
                return jsonify({'error': 'Format de date invalide'}), 400

        rdv.updated_at = datetime.now()
        db.session.commit()

        return jsonify({
            'message': 'Rendez-vous mis a jour avec succes',
            'appointment': rdv.to_dict()
        }), 200

    except Exception as e:
        print(f"Erreur lors de la mise a jour du rendez-vous: {str(e)}")
        return jsonify({'error': 'Erreur lors de la mise a jour du rendez-vous'}), 500

@appointment_bp.route('/<int:appointment_id>', methods=['DELETE'])
@jwt_required()
def delete_appointment(appointment_id):
    """Supprimer definitivement un rendez-vous"""
    try:
        current_patient_id = get_jwt_identity()
        
        print(f"Suppression RDV ID: {appointment_id} par patient: {current_patient_id}")

        rdv = RendezVous.query.filter_by(id=appointment_id, patient_id=current_patient_id).first()
        if not rdv:
            return jsonify({'error': 'Rendez-vous non trouve'}), 404

        print(f"RDV trouve: {rdv.motif} - {rdv.date_rdv}")

        # Supprimer definitivement de la base de donnees
        db.session.delete(rdv)
        db.session.commit()
        
        print(f"RDV supprime avec succes")

        return jsonify({
            'message': 'Rendez-vous supprime avec succes'
        }), 200

    except Exception as e:
        db.session.rollback()
        print(f"Erreur suppression RDV: {str(e)}")
        return jsonify({'error': 'Erreur lors de la suppression du rendez-vous'}), 500

@appointment_bp.route('/<int:appointment_id>/cancel', methods=['PUT'])
@jwt_required()
def cancel_appointment(appointment_id):
    """Annuler un rendez-vous (changement de statut)"""
    try:
        current_patient_id = get_jwt_identity()

        rdv = RendezVous.query.filter_by(id=appointment_id, patient_id=current_patient_id).first()
        if not rdv:
            return jsonify({'error': 'Rendez-vous non trouve'}), 404

        if rdv.statut in ['annule', 'termine']:
            return jsonify({'error': 'Ce rendez-vous ne peut pas etre annule'}), 400

        rdv.statut = 'annule'
        rdv.updated_at = datetime.now()
        db.session.commit()

        return jsonify({
            'message': 'Rendez-vous annule avec succes'
        }), 200

    except Exception as e:
        db.session.rollback()
        print(f"Erreur lors de l'annulation du rendez-vous: {str(e)}")
        return jsonify({'error': 'Erreur lors de l\'annulation du rendez-vous'}), 500
