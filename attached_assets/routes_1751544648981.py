from flask import Blueprint, render_template, request, redirect, url_for, flash, session, jsonify
from werkzeug.security import check_password_hash
from models import Patient, Medecin, RendezVous
from database import db
from datetime import datetime

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    """Page d'accueil"""
    return render_template('index.html')

@main_bp.route('/login', methods=['GET', 'POST'])
def login():
    """Page de connexion"""
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        if not email or not password:
            flash('Veuillez remplir tous les champs.', 'error')
            return render_template('login.html')
        
        # Vérifier les identifiants
        patient = Patient.query.filter_by(email=email).first()
        
        if patient and patient.check_password(password):
            if not patient.is_active:
                flash('Votre compte est désactivé. Contactez l\'administration.', 'error')
                return render_template('login.html')
            
            # Connecter l'utilisateur
            session['patient_id'] = patient.id
            session['patient_nom'] = f"{patient.prenom} {patient.nom}"
            flash('Connexion réussie !', 'success')
            return redirect(url_for('main.dashboard'))
        else:
            flash('Email ou mot de passe incorrect.', 'error')
    
    return render_template('login.html')

@main_bp.route('/register', methods=['GET', 'POST'])
def register():
    """Page d'inscription"""
    if request.method == 'POST':
        # Récupérer les données du formulaire
        prenom = request.form.get('prenom')
        nom = request.form.get('nom')
        email = request.form.get('email')
        telephone = request.form.get('telephone')
        date_naissance = request.form.get('date_naissance')
        adresse = request.form.get('adresse')
        antecedents_medicaux = request.form.get('antecedents_medicaux')
        contact_urgence_nom = request.form.get('contact_urgence_nom')
        contact_urgence_telephone = request.form.get('contact_urgence_telephone')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        # Validation des champs requis
        required_fields = {
            'prenom': prenom,
            'nom': nom,
            'email': email,
            'telephone': telephone,
            'date_naissance': date_naissance,
            'contact_urgence_nom': contact_urgence_nom,
            'contact_urgence_telephone': contact_urgence_telephone,
            'password': password,
            'confirm_password': confirm_password
        }
        
        missing_fields = [field for field, value in required_fields.items() if not value]
        if missing_fields:
            flash('Veuillez remplir tous les champs obligatoires.', 'error')
            return render_template('register.html')
        
        # Vérifier que les mots de passe correspondent
        if password != confirm_password:
            flash('Les mots de passe ne correspondent pas.', 'error')
            return render_template('register.html')
        
        # Vérifier si l'email existe déjà
        existing_patient = Patient.query.filter_by(email=email).first()
        if existing_patient:
            flash('Un compte avec cet email existe déjà.', 'error')
            return render_template('register.html')
        
        try:
            # Créer le nouveau patient
            patient = Patient()
            patient.prenom = prenom
            patient.nom = nom
            patient.email = email
            patient.telephone = telephone
            patient.date_naissance = datetime.strptime(date_naissance, '%Y-%m-%d').date()
            patient.adresse = adresse if adresse else None
            patient.antecedents_medicaux = antecedents_medicaux if antecedents_medicaux else None
            patient.contact_urgence_nom = contact_urgence_nom
            patient.contact_urgence_telephone = contact_urgence_telephone
            patient.set_password(password)
            
            db.session.add(patient)
            db.session.commit()
            
            # Connecter automatiquement l'utilisateur
            session['patient_id'] = patient.id
            session['patient_nom'] = f"{patient.prenom} {patient.nom}"
            flash('Compte créé avec succès ! Bienvenue !', 'success')
            return redirect(url_for('main.dashboard'))
            
        except Exception as e:
            db.session.rollback()
            print(f"Erreur lors de l'inscription: {str(e)}")
            flash('Erreur lors de la création du compte. Veuillez réessayer.', 'error')
    
    return render_template('register.html')

@main_bp.route('/dashboard')
def dashboard():
    """Tableau de bord patient"""
    if 'patient_id' not in session:
        flash('Vous devez être connecté pour accéder à cette page.', 'error')
        return redirect(url_for('main.login'))
    
    patient = Patient.query.get(session['patient_id'])
    if not patient:
        session.clear()
        flash('Session expirée. Veuillez vous reconnecter.', 'error')
        return redirect(url_for('main.login'))
    
    return render_template('dashboard.html', patient=patient)

@main_bp.route('/profile')
def profile():
    """Page de profil"""
    if 'patient_id' not in session:
        flash('Vous devez être connecté pour accéder à cette page.', 'error')
        return redirect(url_for('main.login'))
    
    patient = Patient.query.get(session['patient_id'])
    if not patient:
        session.clear()
        flash('Session expirée. Veuillez vous reconnecter.', 'error')
        return redirect(url_for('main.login'))
    
    return render_template('profile.html', patient=patient)

@main_bp.route('/appointments')
def appointments():
    """Page des rendez-vous"""
    if 'patient_id' not in session:
        flash('Vous devez être connecté pour accéder à cette page.', 'error')
        return redirect(url_for('main.login'))
    
    patient = Patient.query.get(session['patient_id'])
    if not patient:
        session.clear()
        flash('Session expirée. Veuillez vous reconnecter.', 'error')
        return redirect(url_for('main.login'))
    
    # Récupérer les rendez-vous du patient
    rdv_list = patient.rendez_vous if hasattr(patient, 'rendez_vous') else []
    
    return render_template('appointments.html', patient=patient, appointments=rdv_list)

@main_bp.route('/book_appointment', methods=['GET', 'POST'])
def book_appointment():
    """Prendre un nouveau rendez-vous"""
    if 'patient_id' not in session:
        flash('Vous devez être connecté pour accéder à cette page.', 'error')
        return redirect(url_for('main.login'))
    
    patient = Patient.query.get(session['patient_id'])
    if not patient:
        session.clear()
        flash('Session expirée. Veuillez vous reconnecter.', 'error')
        return redirect(url_for('main.login'))
    
    # Récupérer la liste des médecins actifs
    medecins = Medecin.query.filter_by(is_active=True).order_by(Medecin.specialite, Medecin.nom).all()
    
    # Types de consultation disponibles
    appointment_types = [
        'Consultation générale',
        'Consultation de suivi',
        'Consultation d\'urgence',
        'Visite de contrôle',
        'Consultation spécialisée',
        'Consultation préopératoire',
        'Consultation postopératoire'
    ]
    
    if request.method == 'POST':
        # Logique pour créer un rendez-vous (à implémenter plus tard)
        flash('Fonction de prise de rendez-vous en cours de développement.', 'info')
    
    return render_template('book_appointment.html', patient=patient, medecins=medecins, appointment_types=appointment_types)

@main_bp.route('/logout')
def logout():
    """Déconnexion"""
    session.clear()
    flash('Vous avez été déconnecté avec succès.', 'success')
    return redirect(url_for('main.index'))