from flask import Blueprint, request, jsonify, send_file
from flask_jwt_extended import jwt_required, get_jwt_identity
import os
import uuid
from werkzeug.utils import secure_filename
from models import DocumentMedical
from database import db

document_bp = Blueprint('documents', __name__)

UPLOAD_FOLDER = 'uploads/documents'

@document_bp.route('/', methods=['GET'])
@jwt_required()
def get_documents():
    """GET documents ultra-simple"""
    try:
        current_patient_id = int(get_jwt_identity())
        print(f"📋 Récupération documents pour patient {current_patient_id}")
        documents = DocumentMedical.query.filter_by(patient_id=current_patient_id).all()
        print(f"📄 {len(documents)} documents trouvés")
        
        # Conversion ultra-simple - utiliser les vrais champs du modèle
        result = []
        for doc in documents:
            result.append({
                'id': doc.id,
                'patient_id': doc.patient_id,
                'nom_document': doc.nom_document or '',
                'titre': doc.nom_document or '',  # Mapping pour compatibilité
                'type_document': doc.type_document or 'autre',
                'description': doc.description or '',
                'contenu': doc.description or '',  # Mapping pour compatibilité
                'nom_fichier': doc.nom_fichier or '',
                'chemin_fichier': doc.chemin_fichier or '',
                'taille_fichier': doc.taille_fichier or 0,
                'date_upload': str(doc.date_upload) if doc.date_upload else None,
                'date_document': str(doc.date_document) if doc.date_document else None,
                'medecin_prescripteur': doc.medecin_prescripteur or ''
            })
            print(f"📄 Document {doc.id}: {doc.nom_document} ({doc.type_document})")
        
        return jsonify({'documents': result}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@document_bp.route('/', methods=['POST'])
@jwt_required()
def upload_document():
    """POST document ultra-simple"""
    try:
        print("🔍 POST /api/documents/ - Début upload")
        current_patient_id = int(get_jwt_identity())
        print(f"👤 Patient ID: {current_patient_id}")
        
        # Créer le dossier uploads s'il n'existe pas
        if not os.path.exists(UPLOAD_FOLDER):
            os.makedirs(UPLOAD_FOLDER)
            print(f"📁 Dossier créé: {UPLOAD_FOLDER}")

        print(f"📁 Dossier upload: {os.path.abspath(UPLOAD_FOLDER)}")

        # Fichier
        if 'file' not in request.files:
            return jsonify({'error': 'Fichier requis'}), 400

        file = request.files['file']
        if not file or file.filename == '':
            return jsonify({'error': 'Fichier vide'}), 400
        
        # Données
        nom_document = request.form.get('nom_document', 'Document')
        type_document = request.form.get('type_document', 'autre')
        description = request.form.get('description', '')
        
        # Sauvegarder fichier
        os.makedirs(UPLOAD_FOLDER, exist_ok=True)
        filename = secure_filename(file.filename)
        unique_filename = f"{uuid.uuid4()}_{filename}"
        file_path = os.path.join(UPLOAD_FOLDER, unique_filename)

        # Sauvegarder le fichier et obtenir sa taille
        file.save(file_path)
        file_size = os.path.getsize(file_path)

        print(f"📄 Fichier sauvé: {file_path}")
        print(f"📏 Taille: {file_size} bytes")

        # Créer document avec les bons champs du modèle
        document = DocumentMedical(
            patient_id=current_patient_id,
            type_document=type_document,
            nom_document=nom_document,
            description=description,
            nom_fichier=filename,
            chemin_fichier=file_path,
            taille_fichier=file_size
        )
        
        db.session.add(document)
        db.session.commit()
        
        return jsonify({
            'message': 'Document uploade',
            'document': {
                'id': document.id,
                'titre': document.nom_document,
                'nom_document': document.nom_document,
                'type_document': document.type_document
            }
        }), 201
        
    except Exception as e:
        try:
            db.session.rollback()
        except:
            pass
        return jsonify({'error': str(e)}), 500

@document_bp.route('/<int:document_id>', methods=['GET'])
@jwt_required()
def download_document(document_id):
    """Download ultra-simple"""
    try:
        current_patient_id = int(get_jwt_identity())
        document = DocumentMedical.query.filter_by(id=document_id, patient_id=current_patient_id).first()
        
        if not document:
            return jsonify({'error': 'Document non trouve'}), 404
        
        if not os.path.exists(document.chemin_fichier):
            return jsonify({'error': 'Fichier non trouve'}), 404

        return send_file(document.chemin_fichier, as_attachment=True)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@document_bp.route('/<int:document_id>', methods=['DELETE'])
@jwt_required()
def delete_document(document_id):
    """Delete ultra-simple"""
    try:
        current_patient_id = int(get_jwt_identity())
        document = DocumentMedical.query.filter_by(id=document_id, patient_id=current_patient_id).first()
        
        if not document:
            return jsonify({'error': 'Document non trouve'}), 404
        
        # Suppression physique du document
        db.session.delete(document)
        db.session.commit()

        # Supprimer aussi le fichier physique si possible
        try:
            if os.path.exists(document.chemin_fichier):
                os.remove(document.chemin_fichier)
                print(f"🗑️ Fichier physique supprimé: {document.chemin_fichier}")
        except Exception as e:
            print(f"⚠️ Erreur suppression fichier: {str(e)}")
        
        return jsonify({'message': 'Document supprime'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
