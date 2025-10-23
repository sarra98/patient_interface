import os
import sqlite3
from flask import Flask, jsonify, send_from_directory, render_template, request
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from config import Config
from database import db

def create_app():
    app = Flask(__name__, static_folder='dist', static_url_path='')
    app.config.from_object(Config)

    # Initialisation des extensions
    db.init_app(app)
    CORS(app, origins=["http://localhost:4200", "http://localhost:5000", "*"])
    JWTManager(app)

    # Enregistrement des blueprints
    from auth import auth_bp
    from appointment_routes import appointment_bp
    from document_routes import document_bp
    from payment_routes import payment_bp
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(appointment_bp, url_prefix='/api/appointments')
    app.register_blueprint(document_bp, url_prefix='/api/documents')
    app.register_blueprint(payment_bp, url_prefix='/api/payments')

    # Health check route
    @app.route('/api/health')
    def health_check():
        return jsonify({'status': 'healthy', 'message': 'Secrétaire Médicale API is running'})

    # Vérification de disponibilité d’un créneau
    @app.route('/api/check-availability', methods=['POST'])
    def check_availability():
        data = request.get_json()
        date = data.get('date')
        time = data.get('time')

        conn = sqlite3.connect('instance/secretaire_medicale.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM appointments WHERE date=? AND time=?", (date, time))
        appointment = cursor.fetchone()
        conn.close()

        return jsonify({'available': not appointment})

    # Routes HTML
    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/login')
    def login():
        return render_template('login.html')

    @app.route('/register')
    def register():
        return render_template('register.html')

    @app.route('/dashboard')
    def dashboard():
        return render_template('dashboard.html')

    @app.route('/appointments')
    def appointments():
        return render_template('appointments.html')

    @app.route('/book-appointment')
    def book_appointment():
        return render_template('book_appointment.html')

    @app.route('/profile')
    def profile():
        return render_template('profile.html')

    @app.route('/documents')
    def documents():
        return render_template('documents.html')

    @app.route('/static/<path:filename>')
    def serve_static(filename):
        return send_from_directory(os.path.join(app.root_path, 'dist'), filename)

    # Initialisation BDD
    with app.app_context():
        import models
        db.create_all()

        # Création automatique d’un médecin si aucun
        from models import Medecin
        doctor = Medecin.query.filter_by(nom='Samir', prenom='Ahmed').first()
        if not doctor:
            doctor = Medecin(
                nom='Samir',
                prenom='Ahmed',
                specialite='Médecin Généraliste',
                telephone='+33 1 23 45 67 89',
                email='ahmed.samir@clinique.com',
                horaires='Lun-Ven 8h-18h, Sam 9h-12h'
            )
            db.session.add(doctor)
            db.session.commit()

    return app

# Lancement de l'application
if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=True)
