#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de lancement rapide pour tester l'intégration de la vue avancée des présences
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '.'))

def quick_test():
    """Test rapide de l'intégration"""
    print("🚀 Test rapide de l'intégration de la vue avancée des présences")
    print("=" * 60)
    
    try:
        # Test d'import rapide
        print("📦 Test d'import...")
        from src.modules.academic.attendance.views.advanced_attendance_view import AdvancedAttendanceView
        print("✅ Vue avancée importée")
        
        # Test d'import des services
        from src.modules.academic.attendance.services.attendance_service import AttendanceService
        print("✅ Service de présence importé")
        
        # Test d'import du dashboard
        from src.modules.auth.views.dashboard_view import PresenceView
        print(f"✅ PresenceView dans le dashboard: {PresenceView.__name__}")
        
        print("\n🎉 Test rapide réussi !")
        print("🚀 La vue avancée est prête à être utilisée")
        
        return True
        
    except ImportError as e:
        print(f"❌ Erreur d'import: {e}")
        return False
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False

def launch_app():
    """Lance l'application avec la vue avancée"""
    print("\n🚀 Lancement de l'application...")
    
    try:
        import customtkinter as ctk
        from src.modules.academic.attendance.views.advanced_attendance_view import AdvancedAttendanceView
        
        # Créer l'application
        app = ctk.CTk()
        app.title("🏫 Vue Avancée des Présences - EduManager+")
        app.geometry("1400x900")
        app.configure(fg_color="#0A192F")
        
        # Créer la vue avancée
        advanced_view = AdvancedAttendanceView(app, app)
        advanced_view.pack(fill="both", expand=True, padx=20, pady=20)
        
        print("✅ Application lancée avec succès")
        print("💡 Fermez la fenêtre pour terminer")
        
        # Lancer l'application
        app.mainloop()
        
    except Exception as e:
        print(f"❌ Erreur lors du lancement: {e}")
        import traceback
        traceback.print_exc()

def main():
    """Fonction principale"""
    print("🏫 Lancement rapide de la vue avancée des présences")
    print("=" * 60)
    
    # Test rapide
    if quick_test():
        # Lancer l'application
        launch_app()
    else:
        print("\n❌ Test rapide échoué")
        print("🔧 Vérifiez les erreurs ci-dessus")

if __name__ == "__main__":
    main()
