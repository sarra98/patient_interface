#!/usr/bin/env python3
"""
Réparation d'urgence complète
"""

import os
import shutil

def create_ultra_simple_document_routes():
    """Créer des routes ultra-simples sans aucune complexité"""
    content = '''from flask import Blueprint, request, jsonify, send_file
from flask_jwt_extended import jwt_required, get_jwt_identity
import os
import uuid
from werkzeug.utils import secure_filename

from models import DocumentMedical
from database import db

document_bp = Blueprint('documents', __name__)

UPLOAD_FOLDER = 'uploads/documents'

def allowed_file(filename):
    return True  # Accepter tous les fichiers pour le test

@document_bp.route('/', methods=['GET'])
@jwt_required()
def get_documents():
    """GET ultra-simple"""
    try:
        current_patient_id = get_jwt_identity()
        
        documents = DocumentMedical.query.filter_by(
            patient_id=current_patient_id,
            is_active=True
        ).all()
        
        docs_list = []
        for doc in documents:
            docs_list.append({
                'id': doc.id,
                'nom_document': doc.titre or '',
                'titre': doc.titre or '',
                'type_document': doc.type_document or 'autre',
                'description': doc.contenu or '',
                'contenu': doc.contenu or '',
                'date_upload': doc.date_creation.isoformat() if doc.date_creation else None
            })
        
        return jsonify({'documents': docs_list}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@document_bp.route('/', methods=['POST'])
@jwt_required()
def upload_document():
    """POST ultra-simple"""
    try:
        current_patient_id = get_jwt_identity()
        
        # Fichier
        if 'file' not in request.files:
            return jsonify({'error': 'Fichier requis'}), 400
        
        file = request.files['file']
        if not file or file.filename == '':
            return jsonify({'error': 'Fichier vide'}), 400
        
        # Données
        nom_document = request.form.get('nom_document', 'Document sans nom')
        type_document = request.form.get('type_document', 'autre')
        description = request.form.get('description', '')
        
        # Sauvegarder fichier
        os.makedirs(UPLOAD_FOLDER, exist_ok=True)
        filename = secure_filename(file.filename)
        file_path = os.path.join(UPLOAD_FOLDER, f"{uuid.uuid4()}_{filename}")
        file.save(file_path)
        
        # Créer document
        document = DocumentMedical(
            patient_id=current_patient_id,
            type_document=type_document,
            titre=nom_document,
            contenu=description,
            fichier_path=file_path,
            is_active=True
        )
        
        db.session.add(document)
        db.session.commit()
        
        return jsonify({
            'message': 'Document uploade',
            'document': {
                'id': document.id,
                'titre': document.titre
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
    """Download simple"""
    try:
        current_patient_id = get_jwt_identity()
        
        document = DocumentMedical.query.filter_by(
            id=document_id,
            patient_id=current_patient_id
        ).first()
        
        if not document:
            return jsonify({'error': 'Document non trouve'}), 404
        
        if not os.path.exists(document.fichier_path):
            return jsonify({'error': 'Fichier non trouve'}), 404
        
        return send_file(document.fichier_path, as_attachment=True)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@document_bp.route('/<int:document_id>', methods=['DELETE'])
@jwt_required()
def delete_document(document_id):
    """Delete simple"""
    try:
        current_patient_id = get_jwt_identity()
        
        document = DocumentMedical.query.filter_by(
            id=document_id,
            patient_id=current_patient_id
        ).first()
        
        if not document:
            return jsonify({'error': 'Document non trouve'}), 404
        
        document.is_active = False
        db.session.commit()
        
        return jsonify({'message': 'Document supprime'}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
'''
    
    return content

def main():
    """Réparation d'urgence"""
    print("🚨 RÉPARATION D'URGENCE")
    print("=" * 40)
    
    try:
        # Sauvegarder
        if os.path.exists('document_routes.py'):
            shutil.copy('document_routes.py', 'document_routes_emergency_backup.py')
            print("Sauvegarde créée")
        
        # Créer version ultra-simple
        content = create_ultra_simple_document_routes()
        
        with open('document_routes.py', 'w', encoding='utf-8') as f:
            f.write(content)
        
        print("Routes ultra-simples créées")
        print("")
        print("REDÉMARREZ FLASK:")
        print("python app.py")
        print("")
        print("TESTEZ:")
        print("python debug_422_direct.py")
        
    except Exception as e:
        print(f"Erreur: {str(e)}")

if __name__ == "__main__":
    main()
