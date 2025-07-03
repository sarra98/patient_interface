import os
from flask import Flask, jsonify, send_from_directory, render_template
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from config import Config
from database import db

def create_app():
    app = Flask(__name__, static_folder='dist', static_url_path='')
    app.config.from_object(Config)
    
    # Initialize extensions
    db.init_app(app)
    CORS(app, origins=["http://localhost:4200", "http://localhost:5000", "*"])
    JWTManager(app)
    
    # Register blueprints
    from auth import auth_bp
    from appointment_routes import appointment_bp
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(appointment_bp, url_prefix='/api/appointments')
    
    @app.route('/api/health')
    def health_check():
        return jsonify({'status': 'healthy', 'message': 'Secrétaire Médicale API is running'})
    
    # Serve HTML templates
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

    # Serve static files from dist directory if they exist
    @app.route('/static/<path:filename>')
    def serve_static(filename):
        return send_from_directory(os.path.join(app.root_path, 'dist'), filename)
    
    with app.app_context():
        # Import models to ensure they are registered
        import models
        db.create_all()
        
        # Setup default doctor if not exists
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

if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=True)
