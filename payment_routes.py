from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from marshmallow import Schema, fields, validate
from datetime import datetime
import uuid
import random

from database import db
from models import Paiement, RendezVous, Patient

payment_bp = Blueprint('payments', __name__)

class PaymentSchema(Schema):
    rendez_vous_id = fields.Int(required=True)
    montant = fields.Float(required=True, validate=validate.Range(min=0.01))
    type_paiement = fields.Str(required=True, validate=validate.OneOf(['carte_bancaire', 'carte_postale']))
    
    # Données de carte bancaire
    numero_carte = fields.Str(required=False, validate=validate.Length(min=16, max=19))
    nom_porteur = fields.Str(required=False, validate=validate.Length(min=2, max=100))
    date_expiration = fields.Str(required=False, validate=validate.Regexp(r'^\d{2}/\d{2}$'))
    cvv = fields.Str(required=False, validate=validate.Length(min=3, max=4))
    
    # Données de carte postale (CCP)
    numero_ccp = fields.Str(required=False, validate=validate.Length(min=10, max=20))
    cle_ccp = fields.Str(required=False, validate=validate.Length(min=2, max=2))

def simulate_payment_processing(payment_data):
    """Simuler le traitement du paiement"""
    # Simulation d'un délai de traitement
    import time
    time.sleep(1)
    
    # Simuler un taux de succès de 95%
    success_rate = 0.95
    is_successful = random.random() < success_rate
    
    if is_successful:
        # Générer une référence de transaction
        reference = f"TXN_{uuid.uuid4().hex[:12].upper()}"
        return {
            'success': True,
            'reference': reference,
            'message': 'Paiement traité avec succès'
        }
    else:
        return {
            'success': False,
            'reference': None,
            'message': 'Paiement refusé. Vérifiez vos informations de carte.'
        }

@payment_bp.route('/', methods=['POST'])
@jwt_required()
def process_payment():
    """Traiter un paiement"""
    try:
        current_patient_id = get_jwt_identity()
        
        schema = PaymentSchema()
        data = schema.load(request.json)
        
        # Vérifier que le rendez-vous existe et appartient au patient
        rdv = RendezVous.query.filter_by(
            id=data['rendez_vous_id'],
            patient_id=current_patient_id
        ).first()
        
        if not rdv:
            return jsonify({'error': 'Rendez-vous non trouvé'}), 404
        
        # Vérifier que le rendez-vous est confirmé
        if rdv.statut != 'confirme':
            return jsonify({'error': 'Le rendez-vous doit être confirmé pour effectuer le paiement'}), 400
        
        # Vérifier qu'il n'y a pas déjà un paiement validé
        existing_payment = Paiement.query.filter_by(
            rendez_vous_id=data['rendez_vous_id'],
            statut='valide'
        ).first()
        
        if existing_payment:
            return jsonify({'error': 'Ce rendez-vous a déjà été payé'}), 400
        
        # Valider les données selon le type de paiement
        if data['type_paiement'] == 'carte_bancaire':
            required_fields = ['numero_carte', 'nom_porteur', 'date_expiration', 'cvv']
            for field in required_fields:
                if field not in data or not data[field]:
                    return jsonify({'error': f'Le champ {field} est requis pour le paiement par carte bancaire'}), 400
        
        elif data['type_paiement'] == 'carte_postale':
            required_fields = ['numero_ccp', 'cle_ccp']
            for field in required_fields:
                if field not in data or not data[field]:
                    return jsonify({'error': f'Le champ {field} est requis pour le paiement par carte postale'}), 400
        
        # Simuler le traitement du paiement
        payment_result = simulate_payment_processing(data)
        
        # Créer l'enregistrement de paiement
        paiement = Paiement(
            rendez_vous_id=data['rendez_vous_id'],
            patient_id=current_patient_id,
            montant=data['montant'],
            type_paiement=data['type_paiement'],
            statut='valide' if payment_result['success'] else 'echec',
            reference_transaction=payment_result['reference']
        )
        
        db.session.add(paiement)
        
        # Si le paiement est réussi, marquer le rendez-vous comme payé
        if payment_result['success']:
            rdv.statut = 'paye'
        
        db.session.commit()
        
        return jsonify({
            'message': payment_result['message'],
            'success': payment_result['success'],
            'paiement': paiement.to_dict() if payment_result['success'] else None
        }), 201 if payment_result['success'] else 400
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Erreur lors du traitement du paiement'}), 500

@payment_bp.route('/', methods=['GET'])
@jwt_required()
def get_payments():
    """Récupérer l'historique des paiements du patient"""
    try:
        current_patient_id = get_jwt_identity()
        
        paiements = Paiement.query.filter_by(patient_id=current_patient_id).order_by(
            Paiement.date_paiement.desc()
        ).all()
        
        # Enrichir avec les informations du rendez-vous
        paiements_data = []
        for paiement in paiements:
            paiement_dict = paiement.to_dict()
            if paiement.rendez_vous:
                paiement_dict['rendez_vous'] = {
                    'id': paiement.rendez_vous.id,
                    'date_rdv': paiement.rendez_vous.date_rdv.isoformat(),
                    'motif': paiement.rendez_vous.motif,
                    'medecin': {
                        'nom': paiement.rendez_vous.medecin.nom,
                        'prenom': paiement.rendez_vous.medecin.prenom,
                        'specialite': paiement.rendez_vous.medecin.specialite
                    } if paiement.rendez_vous.medecin else None
                }
            paiements_data.append(paiement_dict)
        
        return jsonify({'paiements': paiements_data}), 200
        
    except Exception as e:
        return jsonify({'error': 'Erreur lors de la récupération des paiements'}), 500

@payment_bp.route('/<int:payment_id>/receipt', methods=['GET'])
@jwt_required()
def get_payment_receipt(payment_id):
    """Générer un reçu de paiement"""
    try:
        current_patient_id = get_jwt_identity()
        
        paiement = Paiement.query.filter_by(
            id=payment_id,
            patient_id=current_patient_id,
            statut='valide'
        ).first()
        
        if not paiement:
            return jsonify({'error': 'Paiement non trouvé'}), 404
        
        # Générer les données du reçu
        receipt_data = {
            'numero_recu': f"REC_{paiement.id:06d}",
            'date_emission': datetime.utcnow().isoformat(),
            'paiement': paiement.to_dict(),
            'patient': {
                'nom': paiement.patient.nom,
                'prenom': paiement.patient.prenom,
                'email': paiement.patient.email
            },
            'rendez_vous': {
                'date': paiement.rendez_vous.date_rdv.isoformat(),
                'motif': paiement.rendez_vous.motif,
                'medecin': f"Dr {paiement.rendez_vous.medecin.prenom} {paiement.rendez_vous.medecin.nom}"
            } if paiement.rendez_vous else None
        }
        
        return jsonify({'recu': receipt_data}), 200
        
    except Exception as e:
        return jsonify({'error': 'Erreur lors de la génération du reçu'}), 500

@payment_bp.route('/tarifs', methods=['GET'])
@jwt_required()
def get_tarifs():
    """Récupérer les tarifs des consultations"""
    # Tarifs par défaut (peuvent être configurés en base de données)
    tarifs = {
        'consultation_generale': {
            'prix': 50.00,
            'description': 'Consultation générale'
        },
        'consultation_specialiste': {
            'prix': 80.00,
            'description': 'Consultation spécialisée'
        },
        'urgence': {
            'prix': 100.00,
            'description': 'Consultation d\'urgence'
        }
    }
    
    return jsonify({'tarifs': tarifs}), 200

@payment_bp.route('/rendez-vous/<int:rdv_id>/tarif', methods=['GET'])
@jwt_required()
def get_appointment_tarif(rdv_id):
    """Récupérer le tarif d'un rendez-vous spécifique"""
    try:
        current_patient_id = get_jwt_identity()
        
        rdv = RendezVous.query.filter_by(
            id=rdv_id,
            patient_id=current_patient_id
        ).first()
        
        if not rdv:
            return jsonify({'error': 'Rendez-vous non trouvé'}), 404
        
        # Déterminer le tarif selon le type de consultation
        if rdv.motif and 'urgence' in rdv.motif.lower():
            tarif = 100.00
            type_consultation = 'urgence'
        elif rdv.medecin and rdv.medecin.specialite != 'Médecine générale':
            tarif = 80.00
            type_consultation = 'consultation_specialiste'
        else:
            tarif = 50.00
            type_consultation = 'consultation_generale'
        
        return jsonify({
            'tarif': tarif,
            'type_consultation': type_consultation,
            'rendez_vous': {
                'id': rdv.id,
                'motif': rdv.motif,
                'medecin': f"Dr {rdv.medecin.prenom} {rdv.medecin.nom}" if rdv.medecin else None
            }
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Erreur lors de la récupération du tarif'}), 500
