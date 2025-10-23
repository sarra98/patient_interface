#!/usr/bin/env python3
"""
Instructions pour déboguer la carte verte
"""

def main():
    print("🔍 DÉBOGAGE CARTE VERTE")
    print("=" * 50)
    
    print("📊 STATUTS CONFIRMÉS:")
    print("✅ 10 RDV avec statut='confirme' et statut_paiement='en_attente'")
    print("✅ Base de données correcte")
    
    print("\n🔧 ÉTAPES DE DÉBOGAGE:")
    print("1. 🌐 Allez sur: http://localhost:5000/appointments")
    print("2. 🔑 Connectez-vous: test@example.com / test123")
    print("3. 🔍 Ouvrez la console (F12 → Console)")
    print("4. 📋 Regardez les logs:")
    print("   • '📋 Appointments reçus: X'")
    print("   • 'RDV X: {statut: confirme, statut_paiement: en_attente}'")
    print("   • '💚 getPaymentButtons pour RDV X'")
    print("   • 'shouldShowGreenCard: true'")
    
    print("\n💡 SI VOUS VOYEZ LES LOGS:")
    print("✅ Les données arrivent correctement")
    print("✅ La fonction getPaymentButtons est appelée")
    print("✅ shouldShowGreenCard devrait être true")
    
    print("\n❌ SI PAS DE CARTE VERTE MALGRÉ LES LOGS:")
    print("🔧 Problème possible dans le CSS ou HTML")
    print("🔧 Vérifiez l'élément dans l'inspecteur")
    
    print("\n❌ SI PAS DE LOGS:")
    print("🔧 Problème avec l'API ou le JavaScript")
    print("🔧 Vérifiez les erreurs dans la console")
    
    print("\n🎯 RECHERCHEZ DANS LA CONSOLE:")
    print("• Erreurs JavaScript (en rouge)")
    print("• '💚 getPaymentButtons' pour chaque RDV")
    print("• 'shouldShowGreenCard: true' pour les RDV confirmés")
    
    print("\n📱 APRÈS DÉBOGAGE:")
    print("Si les logs montrent shouldShowGreenCard: true")
    print("mais pas de carte verte, c'est un problème CSS/HTML")
    
    print("\n🌐 TESTEZ MAINTENANT:")
    print("http://localhost:5000/appointments")
    print("Console ouverte (F12)")

if __name__ == "__main__":
    main()
