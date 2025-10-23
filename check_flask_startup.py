#!/usr/bin/env python3
"""
Vérifier que Flask peut démarrer sans erreur
"""

def check_imports():
    """Vérifier les imports"""
    print("🔍 VÉRIFICATION IMPORTS")
    print("=" * 50)
    
    try:
        from app import create_app
        print("✅ Import create_app OK")
        
        from document_routes import document_bp
        print("✅ Import document_bp OK")
        
        from models import DocumentMedical
        print("✅ Import DocumentMedical OK")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur import: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def check_app_creation():
    """Vérifier la création de l'app"""
    print("\n🔍 VÉRIFICATION CRÉATION APP")
    print("=" * 50)
    
    try:
        from app import create_app
        
        app = create_app()
        print("✅ App créée avec succès")
        
        # Vérifier les routes
        with app.app_context():
            routes = []
            for rule in app.url_map.iter_rules():
                if 'documents' in rule.rule:
                    routes.append(f"{rule.methods} {rule.rule}")
            
            print(f"📋 Routes documents ({len(routes)}):")
            for route in routes:
                print(f"  {route}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur création app: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def check_document_routes():
    """Vérifier les routes de documents"""
    print("\n🔍 VÉRIFICATION ROUTES DOCUMENTS")
    print("=" * 50)
    
    try:
        import document_routes
        
        # Lister les fonctions dans le module
        functions = [name for name in dir(document_routes) if not name.startswith('_')]
        print(f"📋 Fonctions dans document_routes:")
        for func in functions:
            if callable(getattr(document_routes, func)):
                print(f"  - {func}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur: {str(e)}")
        return False

def main():
    """Vérification principale"""
    print("🚀 VÉRIFICATION DÉMARRAGE FLASK")
    print("=" * 60)
    
    checks = [
        ("Imports", check_imports),
        ("Routes documents", check_document_routes),
        ("Création app", check_app_creation)
    ]
    
    success_count = 0
    for check_name, check_func in checks:
        try:
            if check_func():
                success_count += 1
                print(f"✅ {check_name} OK")
            else:
                print(f"❌ {check_name} échoué")
        except Exception as e:
            print(f"❌ Erreur {check_name}: {str(e)}")
    
    print(f"\n📊 RÉSUMÉ: {success_count}/{len(checks)} vérifications OK")
    
    if success_count == len(checks):
        print("🎉 FLASK PEUT DÉMARRER!")
        print("💡 Exécutez: python app.py")
    else:
        print("❌ PROBLÈMES DÉTECTÉS")
        print("💡 Corrigez les erreurs avant de démarrer Flask")

if __name__ == "__main__":
    main()
