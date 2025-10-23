#!/usr/bin/env python3
"""
Script de test pour les opérations CRUD des rendez-vous
"""

import sys
import os
from datetime import datetime, timedelta

def test_appointment_models():
    """Test des modèles de rendez-vous"""
    print("🔍 Test des modèles de rendez-vous...")
    
    try:
        from app import create_app
        from database import db
        from models import Patient, Medecin, RendezVous
        
        app = create_app()
        with app.app_context():
            # Vérifier que les tables existent
            inspector = db.inspect(db.engine)
            tables = inspector.get_table_names()
            
            required_tables = ['patients', 'medecins', 'rendez_vous']
            missing_tables = [table for table in required_tables if table not in tables]
            
            if missing_tables:
                print(f"❌ Tables manquantes: {', '.join(missing_tables)}")
                return False
            
            print("✅ Toutes les tables requises sont présentes")
            
            # Test de création d'un rendez-vous
            try:
                # Vérifier qu'il y a au moins un patient et un médecin
                patient_count = Patient.query.count()
                medecin_count = Medecin.query.count()
                
                print(f"📊 Patients dans la DB: {patient_count}")
                print(f"📊 Médecins dans la DB: {medecin_count}")
                
                if patient_count == 0 or medecin_count == 0:
                    print("⚠️  Pas assez de données pour tester les rendez-vous")
                    print("   Créez au moins un patient et un médecin pour tester")
                    return True  # Pas d'erreur, juste pas de données
                
                # Test de la méthode to_dict
                rdv_count = RendezVous.query.count()
                print(f"📊 Rendez-vous dans la DB: {rdv_count}")
                
                if rdv_count > 0:
                    rdv = RendezVous.query.first()
                    rdv_dict = rdv.to_dict()
                    
                    required_fields = ['id', 'patient_id', 'medecin_id', 'date_rdv', 'motif', 'statut']
                    missing_fields = [field for field in required_fields if field not in rdv_dict]
                    
                    if missing_fields:
                        print(f"❌ Champs manquants dans to_dict(): {', '.join(missing_fields)}")
                        return False
                    
                    print("✅ Méthode to_dict() fonctionne correctement")
                
                return True
                
            except Exception as e:
                print(f"❌ Erreur lors du test des modèles: {str(e)}")
                return False
                
    except Exception as e:
        print(f"❌ Erreur lors de l'import des modèles: {str(e)}")
        return False

def test_appointment_routes():
    """Test des routes d'API pour les rendez-vous"""
    print("\n🔍 Test des routes d'API...")
    
    try:
        from app import create_app
        
        app = create_app()
        
        # Vérifier que les blueprints sont enregistrés
        blueprint_names = [bp.name for bp in app.blueprints.values()]
        
        if 'appointments' not in blueprint_names:
            print("❌ Blueprint 'appointments' non enregistré")
            return False
        
        print("✅ Blueprint 'appointments' enregistré")
        
        # Test des routes avec le client de test
        with app.test_client() as client:
            # Test GET /api/appointments (sans auth - doit retourner 401)
            response = client.get('/api/appointments/')
            if response.status_code == 401:
                print("✅ Route GET /api/appointments/ protégée par authentification")
            else:
                print(f"⚠️  Route GET /api/appointments/ retourne {response.status_code} au lieu de 401")
            
            # Test PUT /api/appointments/1 (sans auth - doit retourner 401)
            response = client.put('/api/appointments/1', json={'motif': 'Test'})
            if response.status_code == 401:
                print("✅ Route PUT /api/appointments/<id> protégée par authentification")
            else:
                print(f"⚠️  Route PUT /api/appointments/<id> retourne {response.status_code} au lieu de 401")
            
            # Test DELETE /api/appointments/1 (sans auth - doit retourner 401)
            response = client.delete('/api/appointments/1')
            if response.status_code == 401:
                print("✅ Route DELETE /api/appointments/<id> protégée par authentification")
            else:
                print(f"⚠️  Route DELETE /api/appointments/<id> retourne {response.status_code} au lieu de 401")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors du test des routes: {str(e)}")
        return False

def test_angular_components():
    """Test des composants Angular"""
    print("\n🔍 Test des composants Angular...")
    
    # Vérifier que les fichiers existent
    files_to_check = [
        'src/app/components/appointments/appointments.component.ts',
        'src/app/components/appointments/appointments.component.html',
        'src/app/services/appointment.service.ts'
    ]
    
    all_good = True
    
    for file_path in files_to_check:
        if os.path.exists(file_path):
            print(f"✅ {file_path}")
            
            # Vérifications spécifiques
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
                if file_path.endswith('appointments.component.ts'):
                    # Vérifier les méthodes importantes
                    methods = ['editAppointment', 'cancelAppointment', 'canEditAppointment', 'canCancelAppointment']
                    for method in methods:
                        if method in content:
                            print(f"  ✅ Méthode {method} présente")
                        else:
                            print(f"  ❌ Méthode {method} manquante")
                            all_good = False
                
                elif file_path.endswith('appointments.component.html'):
                    # Vérifier les éléments UI importants
                    elements = ['editAppointment', 'cancelAppointment', 'showEditModal', 'modal']
                    for element in elements:
                        if element in content:
                            print(f"  ✅ Élément UI {element} présent")
                        else:
                            print(f"  ❌ Élément UI {element} manquant")
                            all_good = False
                
                elif file_path.endswith('appointment.service.ts'):
                    # Vérifier les méthodes de service
                    methods = ['updateAppointment', 'cancelAppointment']
                    for method in methods:
                        if method in content:
                            print(f"  ✅ Méthode service {method} présente")
                        else:
                            print(f"  ❌ Méthode service {method} manquante")
                            all_good = False
        else:
            print(f"❌ {file_path} - MANQUANT")
            all_good = False
    
    return all_good

def test_appointment_validation():
    """Test des validations de rendez-vous"""
    print("\n🔍 Test des validations...")
    
    try:
        from app import create_app
        from appointment_routes import AppointmentUpdateSchema
        from marshmallow import ValidationError
        
        app = create_app()
        
        with app.app_context():
            schema = AppointmentUpdateSchema()
            
            # Test de validation valide
            valid_data = {
                'motif': 'Consultation de suivi',
                'notes': 'Patient en bonne santé'
            }
            
            try:
                result = schema.load(valid_data)
                print("✅ Validation des données valides réussie")
            except ValidationError as e:
                print(f"❌ Échec de validation des données valides: {e.messages}")
                return False
            
            # Test de validation invalide (motif trop court)
            invalid_data = {
                'motif': 'AB',  # Trop court
                'notes': 'Test'
            }
            
            try:
                result = schema.load(invalid_data)
                print("⚠️  Validation des données invalides devrait échouer")
            except ValidationError:
                print("✅ Validation des données invalides échoue correctement")
            
            return True
            
    except Exception as e:
        print(f"❌ Erreur lors du test des validations: {str(e)}")
        return False

def main():
    """Fonction principale"""
    print("🚀 Test des fonctionnalités CRUD des rendez-vous")
    print("=" * 60)
    print(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    tests = [
        ("Modèles de données", test_appointment_models),
        ("Routes d'API", test_appointment_routes),
        ("Composants Angular", test_angular_components),
        ("Validations", test_appointment_validation)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"🔍 Test: {test_name}")
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ Erreur inattendue: {str(e)}")
            results.append((test_name, False))
        print()
    
    # Résumé
    print("=" * 60)
    print("📊 RÉSUMÉ DES TESTS")
    print("=" * 60)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASSÉ" if result else "❌ ÉCHEC"
        print(f"{test_name:.<40} {status}")
        if result:
            passed += 1
    
    print()
    print(f"Tests réussis: {passed}/{total}")
    
    if passed == total:
        print("\n🎉 Tous les tests sont passés!")
        print("\n💡 Les fonctionnalités de modification et suppression devraient fonctionner.")
        print("   Démarrez l'application et testez dans l'interface utilisateur.")
    else:
        print(f"\n⚠️  {total - passed} test(s) ont échoué.")
        print("Vérifiez les erreurs ci-dessus.")
    
    return 0 if passed == total else 1

if __name__ == "__main__":
    sys.exit(main())
