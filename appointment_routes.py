from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime, timedelta
import uuid
from models import RendezVous, Medecin
from database import db

appointment_bp = Blueprint('appointments', __name__)

def send_payment_sms(phone_number, payment_info):
    """
    Envoyer un SMS de confirmation de paiement
    En production, intégrer avec un service SMS réel (Twilio, etc.)
    """
    try:
        # Simulation d'envoi SMS
        print(f"📱 ENVOI SMS vers {phone_number}")
        print("=" * 50)

        message = f"""🏥 SECRÉTAIRE MÉDICALE - Confirmation de paiement

✅ Paiement réussi!
💰 Montant: {payment_info['montant']} DT
💳 Carte: **** **** **** {payment_info['card_last4']}
🔗 Référence: {payment_info['reference']}
📅 RDV: {payment_info['date_rdv']}
👤 Patient: {payment_info['patient_name']}

Merci pour votre confiance!
Dr Ahmed Samir - Médecin Généraliste"""

        print("📄 CONTENU SMS:")
        print(message)
        print("=" * 50)

        # En production, remplacer par un vrai service SMS
        # Exemple avec Twilio:
        # from twilio.rest import Client
        # client = Client(account_sid, auth_token)
        # client.messages.create(
        #     body=message,
        #     from_='+1234567890',
        #     to=phone_number
        # )

        print(f"✅ SMS simulé envoyé vers {phone_number}")
        return True

    except Exception as e:
        print(f"❌ Erreur envoi SMS: {str(e)}")
        return False

@appointment_bp.route('/', methods=['GET'])
@jwt_required()
def get_appointments():
    """GET appointments ultra-simple"""
    try:
        current_patient_id = int(get_jwt_identity())
        appointments = RendezVous.query.filter_by(patient_id=current_patient_id).all()
        
        # Conversion ultra-simple
        result = []
        for rdv in appointments:
            result.append({
                'id': rdv.id,
                'date_rdv': str(rdv.date_rdv),
                'motif': rdv.motif or '',
                'statut': rdv.statut or 'planifie'
            })
        
        return jsonify({'appointments': result}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@appointment_bp.route('/', methods=['POST'])
@jwt_required()
def create_appointment():
    """POST appointment ultra-simple"""
    try:
        current_patient_id = int(get_jwt_identity())
        data = request.json
        
        # Validation minimale
        medecin_id = data.get('medecin_id', 1)
        date_rdv_str = data.get('date_rdv')
        motif = data.get('motif', 'Consultation')
        
        if not date_rdv_str:
            return jsonify({'error': 'Date requise'}), 400
        
        # Parser la date
        try:
            if 'T' in date_rdv_str:
                date_rdv = datetime.fromisoformat(date_rdv_str.replace('Z', ''))
            else:
                date_rdv = datetime.strptime(date_rdv_str, '%Y-%m-%d %H:%M')
        except:
            return jsonify({'error': 'Format de date invalide'}), 400
        
        # Créer le RDV
        rdv = RendezVous(
            patient_id=current_patient_id,
            medecin_id=medecin_id,
            date_rdv=date_rdv,
            motif=motif,
            statut='planifie'
        )
        
        db.session.add(rdv)
        db.session.commit()
        
        return jsonify({
            'message': 'Rendez-vous cree',
            'appointment': {
                'id': rdv.id,
                'date_rdv': str(rdv.date_rdv),
                'motif': rdv.motif
            }
        }), 201
        
    except Exception as e:
        try:
            db.session.rollback()
        except:
            pass
        return jsonify({'error': str(e)}), 500

@appointment_bp.route('/occupied-slots', methods=['GET'])
@jwt_required()
def get_occupied_slots():
    """Récupérer les créneaux occupés pour une date donnée"""
    try:
        date_str = request.args.get('date')
        if not date_str:
            return jsonify({'error': 'Date requise'}), 400

        print(f"🔍 Vérification créneaux occupés pour: {date_str}")

        # Convertir la date string en objet date
        try:
            date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()
        except ValueError:
            return jsonify({'error': 'Format de date invalide (YYYY-MM-DD)'}), 400

        # Récupérer tous les RDV confirmés pour cette date
        appointments = RendezVous.query.filter(
            RendezVous.date_rdv >= datetime.combine(date_obj, datetime.min.time()),
            RendezVous.date_rdv < datetime.combine(date_obj, datetime.min.time()) + timedelta(days=1),
            RendezVous.statut.in_(['confirme', 'planifie'])
        ).all()

        print(f"📊 {len(appointments)} RDV trouvés pour {date_str}")

        # Extraire les heures occupées
        occupied_slots = []
        for rdv in appointments:
            if rdv.date_rdv:
                time_str = rdv.date_rdv.strftime('%H:%M')
                occupied_slots.append(time_str)
                print(f"  🚫 Créneau occupé: {time_str} - {rdv.motif}")

        print(f"✅ Retour de {len(occupied_slots)} créneaux occupés")

        return jsonify({'occupied_slots': occupied_slots}), 200

    except Exception as e:
        print(f"❌ Erreur récupération créneaux: {str(e)}")
        return jsonify({'error': str(e)}), 500

@appointment_bp.route('/medecins', methods=['GET'])
@jwt_required()
def get_medecins():
    """GET medecins ultra-simple"""
    try:
        medecins = Medecin.query.filter_by(is_active=True).all()
        result = []
        for medecin in medecins:
            result.append({
                'id': medecin.id,
                'nom': medecin.nom or '',
                'prenom': medecin.prenom or '',
                'specialite': medecin.specialite or ''
            })
        return jsonify({'medecins': result}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@appointment_bp.route('/<int:appointment_id>', methods=['PUT'])
@jwt_required()
def update_appointment(appointment_id):
    """Modifier un rendez-vous (date/heure)"""
    try:
        current_user_id = int(get_jwt_identity())
        data = request.get_json()

        print(f"✏️ Modification RDV {appointment_id} par utilisateur {current_user_id}")
        print(f"📋 Données reçues: {data}")

        # Récupérer le rendez-vous
        rdv = RendezVous.query.filter_by(id=appointment_id, patient_id=current_user_id).first()

        if not rdv:
            return jsonify({'error': 'Rendez-vous non trouvé'}), 404

        # Vérifier que le RDV peut être modifié
        if rdv.statut not in ['planifie', 'confirme']:
            return jsonify({'error': 'Ce rendez-vous ne peut plus être modifié'}), 400

        # Mettre à jour la date/heure si fournie
        if 'date_rdv' in data:
            try:
                nouvelle_date = datetime.fromisoformat(data['date_rdv'].replace('Z', '+00:00'))

                # Vérifier que la nouvelle date est dans le futur
                if nouvelle_date <= datetime.now():
                    return jsonify({'error': 'La date doit être dans le futur'}), 400

                # Vérifier les restrictions (pas dimanche, samedi limité)
                if nouvelle_date.weekday() == 6:  # Dimanche
                    return jsonify({'error': 'Pas de rendez-vous le dimanche'}), 400

                if nouvelle_date.weekday() == 5:  # Samedi
                    if nouvelle_date.hour < 8 or nouvelle_date.hour >= 12:
                        return jsonify({'error': 'Samedi: rendez-vous seulement de 8h à 12h'}), 400

                # Vérifier si le créneau est libre
                conflit = RendezVous.query.filter(
                    RendezVous.id != appointment_id,
                    RendezVous.date_rdv == nouvelle_date,
                    RendezVous.statut.in_(['planifie', 'confirme'])
                ).first()

                if conflit:
                    return jsonify({'error': 'Ce créneau est déjà occupé'}), 400

                rdv.date_rdv = nouvelle_date
                print(f"✏️ RDV {appointment_id} modifié: nouvelle date {nouvelle_date}")

            except ValueError:
                return jsonify({'error': 'Format de date invalide'}), 400

        db.session.commit()

        return jsonify({
            'message': 'Rendez-vous modifié avec succès',
            'appointment': rdv.to_dict()
        }), 200

    except Exception as e:
        print(f"❌ Erreur modification RDV: {str(e)}")
        return jsonify({'error': str(e)}), 500

@appointment_bp.route('/<int:appointment_id>', methods=['DELETE'])
@jwt_required()
def delete_appointment(appointment_id):
    """DELETE appointment ultra-simple"""
    try:
        current_patient_id = int(get_jwt_identity())
        rdv = RendezVous.query.filter_by(id=appointment_id, patient_id=current_patient_id).first()
        
        if not rdv:
            return jsonify({'error': 'RDV non trouve'}), 404
        
        db.session.delete(rdv)
        db.session.commit()
        
        return jsonify({'message': 'RDV supprime'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@appointment_bp.route('/<int:appointment_id>/payment', methods=['POST'])
@jwt_required()
def process_payment(appointment_id):
    """Traiter le paiement d'un rendez-vous"""
    try:
        current_patient_id = int(get_jwt_identity())
        data = request.json

        # Récupérer le RDV
        rdv = RendezVous.query.filter_by(id=appointment_id, patient_id=current_patient_id).first()
        if not rdv:
            return jsonify({'error': 'Rendez-vous non trouve'}), 404

        # Vérifier que le RDV n'est pas déjà payé
        if getattr(rdv, 'statut_paiement', 'en_attente') == 'paye':
            return jsonify({'error': 'Ce rendez-vous est deja paye'}), 400

        mode_paiement = data.get('mode_paiement')  # 'bancaire' ou 'sur_place'

        if mode_paiement not in ['bancaire', 'sur_place']:
            return jsonify({'error': 'Mode de paiement invalide'}), 400

        # Traitement selon le mode de paiement
        if mode_paiement == 'bancaire':
            # Récupérer les données de la carte
            card_data = data.get('card_data', {})
            card_number = card_data.get('number', '')
            card_name = card_data.get('name', '')
            phone_number = card_data.get('phone', '')

            print(f"💳 Traitement paiement carte pour RDV {appointment_id}")
            print(f"📱 Téléphone: {phone_number}")
            print(f"💳 Carte: **** **** **** {card_number[-4:] if card_number else 'XXXX'}")
            print(f"👤 Nom: {card_name}")

            # Simulation du traitement bancaire (délai réaliste)
            import time, uuid
            time.sleep(2)  # Simuler le temps de traitement bancaire

            # Générer référence de paiement
            reference = f"PAY_{uuid.uuid4().hex[:8].upper()}"

            # Mettre à jour le RDV - PAIEMENT CONFIRME LE RDV
            ancien_statut = rdv.statut
            rdv.statut_paiement = 'paye'
            rdv.mode_paiement = 'bancaire'
            rdv.date_paiement = datetime.now()
            rdv.reference_paiement = reference
            rdv.paiement_confirme = True
            rdv.statut = 'confirme'  # PAIEMENT CONFIRME AUTOMATIQUEMENT LE RDV

            print(f"✅ RDV {appointment_id}: {ancien_statut} → confirme (paiement bancaire)")

            db.session.commit()

            # Envoyer SMS de confirmation
            sms_sent = send_payment_sms(phone_number, {
                'reference': reference,
                'montant': float(rdv.montant) if rdv.montant else 70.00,
                'date_rdv': rdv.date_rdv.strftime('%d/%m/%Y à %H:%M') if rdv.date_rdv else 'N/A',
                'card_last4': card_number[-4:] if card_number else 'XXXX',
                'patient_name': card_name
            })

            print(f"💳 Paiement bancaire réussi pour RDV {appointment_id}: {reference}")
            print(f"📱 SMS envoyé: {sms_sent}")

            # Masquer le numéro de téléphone pour la réponse
            phone_masked = phone_number[:3] + '*' * (len(phone_number) - 6) + phone_number[-3:] if len(phone_number) > 6 else phone_number

            return jsonify({
                'message': 'Paiement par carte bancaire reussi',
                'reference': reference,
                'montant': float(rdv.montant) if rdv.montant else 70.00,
                'devise': 'DT',
                'mode': 'bancaire',
                'sms_envoye': sms_sent,
                'phone_masked': phone_masked,
                'card_last4': card_number[-4:] if card_number else 'XXXX',
                'transaction_time': datetime.now().strftime('%d/%m/%Y %H:%M:%S')
            }), 200

        elif mode_paiement == 'sur_place':
            # Paiement sur place - CONFIRME LE RDV IMMÉDIATEMENT
            ancien_statut = rdv.statut
            rdv.mode_paiement = 'sur_place'
            rdv.statut_paiement = 'en_attente'  # Paiement en attente mais RDV confirmé
            rdv.paiement_confirme = False
            rdv.statut = 'confirme'  # PAIEMENT SUR PLACE CONFIRME LE RDV

            print(f"✅ RDV {appointment_id}: {ancien_statut} → confirme (paiement sur place programmé)")

            db.session.commit()

            return jsonify({
                'message': 'RDV confirme - Paiement sur place programme',
                'mode': 'sur_place',
                'montant': float(rdv.montant) if rdv.montant else 70.00,
                'devise': 'DT',
                'note': 'RDV confirme - Paiement a effectuer lors de la consultation',
                'statut_rdv': 'confirme',
                'statut_change': f'{ancien_statut} → confirme'
            }), 200

    except Exception as e:
        try:
            db.session.rollback()
        except:
            pass
        return jsonify({'error': f'Erreur paiement: {str(e)}'}), 500

@appointment_bp.route('/<int:appointment_id>/payment/confirm', methods=['POST'])
@jwt_required()
def confirm_payment(appointment_id):
    """Confirmer un paiement sur place"""
    try:
        current_patient_id = int(get_jwt_identity())

        rdv = RendezVous.query.filter_by(id=appointment_id, patient_id=current_patient_id).first()
        if not rdv:
            return jsonify({'error': 'Rendez-vous non trouve'}), 404

        if rdv.mode_paiement != 'sur_place':
            return jsonify({'error': 'Ce RDV n\'est pas en paiement sur place'}), 400

        # Confirmer le paiement sur place
        rdv.statut_paiement = 'paye'
        rdv.date_paiement = datetime.now()
        rdv.paiement_confirme = True
        rdv.reference_paiement = f"PLACE_{rdv.id}_{datetime.now().strftime('%Y%m%d')}"

        db.session.commit()

        return jsonify({
            'message': 'Paiement sur place confirme',
            'reference': rdv.reference_paiement
        }), 200

    except Exception as e:
        try:
            db.session.rollback()
        except:
            pass
        return jsonify({'error': f'Erreur confirmation: {str(e)}'}), 500
