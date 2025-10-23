#!/usr/bin/env python3
"""
Correction d'urgence pour les erreurs 422
"""

def create_simple_document_routes():
    """Créer une version simplifiée de document_routes.py"""
    print("🔧 CRÉATION ROUTES DOCUMENTS SIMPLIFIÉES")
    print("=" * 50)
    
    content = '''from flask import Blueprint, request, jsonify, send_file
from flask_jwt_extended import jwt_required, get_jwt_identity
import os
import uuid
from werkzeug.utils import secure_filename

from models import DocumentMedical
from database import db

document_bp = Blueprint('documents', __name__)

UPLOAD_FOLDER = 'uploads/documents'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'doc', 'docx'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@document_bp.route('/', methods=['GET'])
@jwt_required()
def get_documents():
    """Récupérer tous les documents du patient connecté"""
    try:
        print("🔍 GET DOCUMENTS SIMPLIFIÉ")
        current_patient_id = get_jwt_identity()
        print(f"👤 Patient ID: {current_patient_id}")
        
        documents = DocumentMedical.query.filter_by(
            patient_id=current_patient_id,
            is_active=True
        ).order_by(DocumentMedical.date_creation.desc()).all()
        
        print(f"📋 {len(documents)} documents trouvés")
        
        # Conversion simple sans erreur
        documents_list = []
        for doc in documents:
            try:
                doc_dict = {
                    'id': doc.id,
                    'patient_id': doc.patient_id,
                    'type_document': doc.type_document or '',
                    'nom_document': doc.titre or '',
                    'titre': doc.titre or '',
                    'description': doc.contenu or '',
                    'contenu': doc.contenu or '',
                    'fichier_path': doc.fichier_path or '',
                    'nom_fichier': doc.fichier_path.split('/')[-1] if doc.fichier_path else '',
                    'date_upload': doc.date_creation.isoformat() if doc.date_creation else None,
                    'date_creation': doc.date_creation.isoformat() if doc.date_creation else None,
                    'is_active': bool(doc.is_active)
                }
                documents_list.append(doc_dict)
            except Exception as e:
                print(f"❌ Erreur doc {doc.id}: {str(e)}")
                continue
        
        print(f"✅ {len(documents_list)} documents convertis")
        
        return jsonify({'documents': documents_list}), 200
        
    except Exception as e:
        print(f"❌ Erreur GET: {str(e)}")
        return jsonify({'error': f'Erreur: {str(e)}'}), 500

@document_bp.route('/', methods=['POST'])
@jwt_required()
def upload_document():
    """Upload d'un document - VERSION SIMPLIFIÉE"""
    try:
        print("🔍 POST DOCUMENTS SIMPLIFIÉ")
        current_patient_id = get_jwt_identity()
        print(f"👤 Patient ID: {current_patient_id}")
        
        # Vérifier le fichier
        if 'file' not in request.files:
            return jsonify({'error': 'Aucun fichier fourni'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'Aucun fichier sélectionné'}), 400
        
        if not allowed_file(file.filename):
            return jsonify({'error': 'Type de fichier non autorisé'}), 400
        
        # Récupérer les données du formulaire SANS VALIDATION STRICTE
        type_document = request.form.get('type_document', 'autre')
        nom_document = request.form.get('nom_document', '')
        description = request.form.get('description', '')
        
        print(f"📋 Données reçues:")
        print(f"  type_document: {type_document}")
        print(f"  nom_document: {nom_document}")
        print(f"  description: {description}")
        
        # Validation minimale
        if not nom_document or len(nom_document) < 3:
            return jsonify({'error': 'Nom du document requis (min 3 caractères)'}), 400
        
        if type_document not in ['analyse', 'ordonnance', 'radio', 'autre']:
            type_document = 'autre'
        
        # Sauvegarder le fichier
        os.makedirs(UPLOAD_FOLDER, exist_ok=True)
        filename = secure_filename(file.filename)
        unique_filename = f"{uuid.uuid4()}_{filename}"
        file_path = os.path.join(UPLOAD_FOLDER, unique_filename)
        
        file.save(file_path)
        print(f"📁 Fichier sauvé: {file_path}")
        
        # Créer le document en base
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
        
        print(f"✅ Document créé avec ID: {document.id}")
        
        return jsonify({
            'message': 'Document uploadé avec succès',
            'document': {
                'id': document.id,
                'titre': document.titre,
                'type_document': document.type_document,
                'contenu': document.contenu
            }
        }), 201
        
    except Exception as e:
        print(f"❌ Erreur POST: {str(e)}")
        try:
            db.session.rollback()
        except:
            pass
        return jsonify({'error': f'Erreur: {str(e)}'}), 500

@document_bp.route('/<int:document_id>', methods=['GET'])
@jwt_required()
def download_document_file(document_id):
    """Télécharger un document"""
    try:
        current_patient_id = get_jwt_identity()
        
        document = DocumentMedical.query.filter_by(
            id=document_id,
            patient_id=current_patient_id,
            is_active=True
        ).first()
        
        if not document or not document.fichier_path:
            return jsonify({'error': 'Document non trouvé'}), 404
        
        if not os.path.exists(document.fichier_path):
            return jsonify({'error': 'Fichier non trouvé'}), 404
        
        filename = document.fichier_path.split('/')[-1]
        
        return send_file(
            document.fichier_path,
            as_attachment=True,
            download_name=filename
        )
        
    except Exception as e:
        print(f"❌ Erreur download: {str(e)}")
        return jsonify({'error': f'Erreur: {str(e)}'}), 500

@document_bp.route('/<int:document_id>', methods=['DELETE'])
@jwt_required()
def delete_document(document_id):
    """Supprimer un document"""
    try:
        current_patient_id = get_jwt_identity()
        
        document = DocumentMedical.query.filter_by(
            id=document_id,
            patient_id=current_patient_id
        ).first()
        
        if not document:
            return jsonify({'error': 'Document non trouvé'}), 404
        
        # Marquer comme inactif au lieu de supprimer
        document.is_active = False
        db.session.commit()
        
        return jsonify({'message': 'Document supprimé avec succès'}), 200
        
    except Exception as e:
        print(f"❌ Erreur delete: {str(e)}")
        return jsonify({'error': f'Erreur: {str(e)}'}), 500
'''
    
    try:
        with open('document_routes_simple.py', 'w') as f:
            f.write(content)
        print("✅ Fichier document_routes_simple.py créé")
        return True
    except Exception as e:
        print(f"❌ Erreur création: {str(e)}")
        return False

def backup_current_routes():
    """Sauvegarder les routes actuelles"""
    print("\n💾 SAUVEGARDE ROUTES ACTUELLES")
    print("=" * 50)
    
    try:
        import shutil
        shutil.copy('document_routes.py', 'document_routes_backup.py')
        print("✅ Sauvegarde créée: document_routes_backup.py")
        return True
    except Exception as e:
        print(f"❌ Erreur sauvegarde: {str(e)}")
        return False

def replace_routes():
    """Remplacer les routes par la version simplifiée"""
    print("\n🔄 REMPLACEMENT ROUTES")
    print("=" * 50)
    
    try:
        import shutil
        shutil.copy('document_routes_simple.py', 'document_routes.py')
        print("✅ Routes remplacées par la version simplifiée")
        return True
    except Exception as e:
        print(f"❌ Erreur remplacement: {str(e)}")
        return False

def main():
    """Correction d'urgence"""
    print("🚨 CORRECTION D'URGENCE ERREURS 422")
    print("=" * 70)
    print("🔧 Simplification complète des routes documents")
    print("=" * 70)
    
    steps = [
        ("Sauvegarde routes actuelles", backup_current_routes),
        ("Création routes simplifiées", create_simple_document_routes),
        ("Remplacement routes", replace_routes)
    ]
    
    success_count = 0
    for step_name, step_func in steps:
        print(f"\n📋 {step_name.upper()}")
        if step_func():
            success_count += 1
            print(f"✅ {step_name} OK")
        else:
            print(f"❌ {step_name} échoué")
            break
    
    print(f"\n📊 RÉSUMÉ: {success_count}/{len(steps)} étapes réussies")
    
    if success_count == len(steps):
        print("🎉 CORRECTION D'URGENCE APPLIQUÉE!")
        print("\n💡 CHANGEMENTS:")
        print("📋 Routes documents complètement simplifiées")
        print("🚫 Plus de schéma de validation complexe")
        print("✅ Validation minimale et robuste")
        print("🔄 Compatibilité totale avec l'interface")
        print("\n🚀 REDÉMARREZ FLASK:")
        print("python app.py")
    else:
        print("❌ CORRECTION INCOMPLÈTE")
        print("💡 Restaurez avec: cp document_routes_backup.py document_routes.py")

if __name__ == "__main__":
    main()
