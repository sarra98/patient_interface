import os
from flask import Flask, jsonify, send_from_directory
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
    
    # Serve Angular app
    @app.route('/')
    def serve_angular():
        return send_from_directory(app.static_folder, 'index.html')
    
    @app.route('/<path:path>')
    def serve_angular_routes(path):
        if path.startswith('api/'):
            return jsonify({'error': 'API endpoint not found'}), 404
        try:
            return send_from_directory(app.static_folder, path)
        except:
            return send_from_directory(app.static_folder, 'index.html')
    
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
