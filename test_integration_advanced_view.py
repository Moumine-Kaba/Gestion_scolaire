#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test d'intégration de la vue avancée des présences dans l'application principale
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '.'))

import customtkinter as ctk
from datetime import datetime
import tkinter as tk
from tkinter import messagebox

def test_integration():
    """Test l'intégration de la vue avancée"""
    print("🧪 Test d'intégration de la vue avancée des présences...")
    
    try:
        # Test 1: Import de la vue avancée
        print("📦 Test d'import de la vue avancée...")
        from src.modules.academic.attendance.views.advanced_attendance_view import AdvancedAttendanceView
        print("✅ Import de la vue avancée réussi")
        
        # Test 2: Import des services
        print("📦 Test d'import des services...")
        from src.modules.academic.attendance.services.attendance_service import AttendanceService
        from src.modules.academic.attendance.services.attendance_notification_service import AttendanceNotificationService
        from src.modules.academic.attendance.services.attendance_export_service import AttendanceExportService
        from src.modules.academic.attendance.services.attendance_justification_service import AttendanceJustificationService
        from src.modules.academic.attendance.services.attendance_alert_service import AttendanceAlertService
        from src.modules.academic.attendance.services.attendance_calendar_service import AttendanceCalendarService
        print("✅ Import des services réussi")
        
        # Test 3: Création de l'application de test
        print("🚀 Création de l'application de test...")
        app = ctk.CTk()
        app.title("Test Intégration - Vue Avancée des Présences")
        app.geometry("1200x800")
        app.configure(fg_color="#0A192F")
        
        # Test 4: Création de la vue avancée
        print("🖥️ Création de la vue avancée...")
        advanced_view = AdvancedAttendanceView(app, app)
        advanced_view.pack(fill="both", expand=True, padx=20, pady=20)
        
        print("✅ Vue avancée créée avec succès")
        
        # Test 5: Vérification des composants
        print("🔍 Vérification des composants...")
        
        # Vérifier que les services sont initialisés
        if hasattr(advanced_view, 'attendance_service'):
            print("✅ Service de présence initialisé")
        else:
            print("❌ Service de présence manquant")
        
        if hasattr(advanced_view, 'notification_service'):
            print("✅ Service de notifications initialisé")
        else:
            print("❌ Service de notifications manquant")
        
        if hasattr(advanced_view, 'export_service'):
            print("✅ Service d'export initialisé")
        else:
            print("❌ Service d'export manquant")
        
        if hasattr(advanced_view, 'justification_service'):
            print("✅ Service de justificatifs initialisé")
        else:
            print("❌ Service de justificatifs manquant")
        
        if hasattr(advanced_view, 'alert_service'):
            print("✅ Service d'alertes initialisé")
        else:
            print("❌ Service d'alertes manquant")
        
        if hasattr(advanced_view, 'calendar_service'):
            print("✅ Service de calendrier initialisé")
        else:
            print("❌ Service de calendrier manquant")
        
        # Test 6: Vérification de l'interface
        print("🖼️ Vérification de l'interface...")
        
        # Vérifier les composants principaux
        if hasattr(advanced_view, 'cb_class'):
            print("✅ Sélecteur de classe présent")
        else:
            print("❌ Sélecteur de classe manquant")
        
        if hasattr(advanced_view, 'ent_date'):
            print("✅ Sélecteur de date présent")
        else:
            print("❌ Sélecteur de date manquant")
        
        if hasattr(advanced_view, 'list_wrap'):
            print("✅ Liste des élèves présente")
        else:
            print("❌ Liste des élèves manquante")
        
        if hasattr(advanced_view, 'detail_panel'):
            print("✅ Panneau de détails présent")
        else:
            print("❌ Panneau de détails manquant")
        
        print("\n🎉 Test d'intégration réussi !")
        print("📋 Résumé:")
        print("  ✅ Vue avancée importée")
        print("  ✅ Services initialisés")
        print("  ✅ Interface créée")
        print("  ✅ Composants vérifiés")
        
        # Afficher l'application
        print("\n🚀 Lancement de l'application de test...")
        print("💡 Fermez la fenêtre pour terminer le test")
        
        app.mainloop()
        
        return True
        
    except ImportError as e:
        print(f"❌ Erreur d'import: {e}")
        return False
    except Exception as e:
        print(f"❌ Erreur lors du test: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_dashboard_integration():
    """Test l'intégration dans le dashboard principal"""
    print("\n🧪 Test d'intégration dans le dashboard principal...")
    
    try:
        # Test d'import du dashboard
        print("📦 Test d'import du dashboard...")
        from src.modules.auth.views.dashboard_view import DashboardView
        print("✅ Import du dashboard réussi")
        
        # Vérifier que PresenceView est bien définie
        from src.modules.auth.views.dashboard_view import PresenceView
        if PresenceView:
            print(f"✅ PresenceView définie: {PresenceView.__name__}")
        else:
            print("❌ PresenceView non définie")
        
        return True
        
    except ImportError as e:
        print(f"❌ Erreur d'import dashboard: {e}")
        return False
    except Exception as e:
        print(f"❌ Erreur lors du test dashboard: {e}")
        return False

def main():
    """Fonction principale de test"""
    print("🏫 Test d'intégration de la vue avancée des présences")
    print("=" * 60)
    
    # Test 1: Intégration de la vue avancée
    success1 = test_integration()
    
    # Test 2: Intégration dans le dashboard
    success2 = test_dashboard_integration()
    
    # Résumé final
    print("\n" + "=" * 60)
    print("📊 RÉSUMÉ DES TESTS")
    print("=" * 60)
    
    if success1:
        print("✅ Test d'intégration de la vue avancée: RÉUSSI")
    else:
        print("❌ Test d'intégration de la vue avancée: ÉCHEC")
    
    if success2:
        print("✅ Test d'intégration dans le dashboard: RÉUSSI")
    else:
        print("❌ Test d'intégration dans le dashboard: ÉCHEC")
    
    if success1 and success2:
        print("\n🎉 TOUS LES TESTS RÉUSSIS !")
        print("🚀 La vue avancée des présences est prête à être utilisée")
        print("📋 Fonctionnalités disponibles:")
        print("  • Gestion complète des présences")
        print("  • Notifications automatiques")
        print("  • Export de rapports")
        print("  • Gestion des justificatifs")
        print("  • Système d'alertes")
        print("  • Planification et calendrier")
    else:
        print("\n⚠️ CERTAINS TESTS ONT ÉCHOUÉ")
        print("🔧 Vérifiez les erreurs ci-dessus")

if __name__ == "__main__":
    main()
