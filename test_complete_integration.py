#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test complet de l'intégration de la vue avancée des présences
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '.'))

import customtkinter as ctk
from datetime import datetime
import tkinter as tk
from tkinter import messagebox

def test_complete_integration():
    """Test complet de l'intégration"""
    print("🧪 Test complet de l'intégration de la vue avancée des présences")
    print("=" * 70)
    
    results = {}
    
    # Test 1: Import des services
    print("\n📦 Test 1: Import des services...")
    try:
        from src.modules.academic.attendance.services.attendance_service import AttendanceService
        from src.modules.academic.attendance.services.attendance_notification_service import AttendanceNotificationService
        from src.modules.academic.attendance.services.attendance_export_service import AttendanceExportService
        from src.modules.academic.attendance.services.attendance_justification_service import AttendanceJustificationService
        from src.modules.academic.attendance.services.attendance_alert_service import AttendanceAlertService
        from src.modules.academic.attendance.services.attendance_calendar_service import AttendanceCalendarService
        results["services_import"] = True
        print("✅ Tous les services importés avec succès")
    except Exception as e:
        results["services_import"] = False
        print(f"❌ Erreur import services: {e}")
    
    # Test 2: Import de la vue avancée
    print("\n📦 Test 2: Import de la vue avancée...")
    try:
        from src.modules.academic.attendance.views.advanced_attendance_view import AdvancedAttendanceView
        results["view_import"] = True
        print("✅ Vue avancée importée avec succès")
    except Exception as e:
        results["view_import"] = False
        print(f"❌ Erreur import vue avancée: {e}")
    
    # Test 3: Création de l'application de test
    print("\n🚀 Test 3: Création de l'application de test...")
    try:
        app = ctk.CTk()
        app.title("Test Intégration Complète - Vue Avancée des Présences")
        app.geometry("1400x900")
        app.configure(fg_color="#0A192F")
        results["app_creation"] = True
        print("✅ Application de test créée")
    except Exception as e:
        results["app_creation"] = False
        print(f"❌ Erreur création application: {e}")
        return results
    
    # Test 4: Création de la vue avancée
    print("\n🖥️ Test 4: Création de la vue avancée...")
    try:
        advanced_view = AdvancedAttendanceView(app, app)
        advanced_view.pack(fill="both", expand=True, padx=20, pady=20)
        results["view_creation"] = True
        print("✅ Vue avancée créée avec succès")
    except Exception as e:
        results["view_creation"] = False
        print(f"❌ Erreur création vue avancée: {e}")
        return results
    
    # Test 5: Vérification des composants
    print("\n🔍 Test 5: Vérification des composants...")
    components = {
        "attendance_service": "Service de présence",
        "notification_service": "Service de notifications",
        "export_service": "Service d'export",
        "justification_service": "Service de justificatifs",
        "alert_service": "Service d'alertes",
        "calendar_service": "Service de calendrier"
    }
    
    for component, description in components.items():
        if hasattr(advanced_view, component):
            print(f"✅ {description} présent")
            results[f"component_{component}"] = True
        else:
            print(f"❌ {description} manquant")
            results[f"component_{component}"] = False
    
    # Test 6: Vérification de l'interface
    print("\n🖼️ Test 6: Vérification de l'interface...")
    interface_components = {
        "cb_class": "Sélecteur de classe",
        "ent_date": "Sélecteur de date",
        "list_wrap": "Liste des élèves",
        "detail_panel": "Panneau de détails",
        "search_var": "Variable de recherche",
        "filter_var": "Variable de filtre"
    }
    
    for component, description in interface_components.items():
        if hasattr(advanced_view, component):
            print(f"✅ {description} présent")
            results[f"interface_{component}"] = True
        else:
            print(f"❌ {description} manquant")
            results[f"interface_{component}"] = False
    
    # Test 7: Test des fonctionnalités
    print("\n⚙️ Test 7: Test des fonctionnalités...")
    try:
        # Test de récupération des classes
        classes = advanced_view.attendance_service.get_classes_for_dropdown()
        print(f"✅ Classes récupérées: {len(classes)}")
        results["functionality_classes"] = True
        
        # Test de récupération des élèves (si des classes existent)
        if classes:
            class_id = advanced_view.attendance_service.get_class_id_map()[classes[0]]
            students = advanced_view.attendance_service.get_students_with_attendance_status(class_id, "2024-12-20")
            print(f"✅ Élèves récupérés: {len(students)}")
            results["functionality_students"] = True
        else:
            print("⚠️ Aucune classe trouvée pour le test des élèves")
            results["functionality_students"] = False
        
        # Test des statistiques
        if classes:
            stats = advanced_view.attendance_service.get_class_attendance_summary_stats(class_id, "2024-12-20")
            print(f"✅ Statistiques récupérées: {stats}")
            results["functionality_stats"] = True
        else:
            results["functionality_stats"] = False
        
    except Exception as e:
        print(f"❌ Erreur test fonctionnalités: {e}")
        results["functionality_classes"] = False
        results["functionality_students"] = False
        results["functionality_stats"] = False
    
    # Test 8: Test de l'intégration dans le dashboard
    print("\n🏠 Test 8: Test de l'intégration dans le dashboard...")
    try:
        # Test d'import du dashboard
        from src.modules.auth.views.dashboard_view import PresenceView
        if PresenceView:
            print(f"✅ PresenceView définie: {PresenceView.__name__}")
            results["dashboard_integration"] = True
        else:
            print("❌ PresenceView non définie")
            results["dashboard_integration"] = False
    except Exception as e:
        print(f"❌ Erreur test dashboard: {e}")
        results["dashboard_integration"] = False
    
    # Afficher l'application de test
    print("\n🚀 Lancement de l'application de test...")
    print("💡 Fermez la fenêtre pour terminer le test")
    
    try:
        app.mainloop()
        results["app_execution"] = True
    except Exception as e:
        print(f"❌ Erreur exécution application: {e}")
        results["app_execution"] = False
    
    return results

def display_results(results):
    """Affiche les résultats des tests"""
    print("\n" + "=" * 70)
    print("📊 RÉSULTATS DES TESTS")
    print("=" * 70)
    
    # Compter les succès et échecs
    total_tests = len(results)
    successful_tests = sum(1 for success in results.values() if success)
    failed_tests = total_tests - successful_tests
    
    print(f"📈 Total des tests: {total_tests}")
    print(f"✅ Tests réussis: {successful_tests}")
    print(f"❌ Tests échoués: {failed_tests}")
    print(f"📊 Taux de réussite: {(successful_tests/total_tests)*100:.1f}%")
    
    # Détail des résultats
    print("\n📋 Détail des résultats:")
    for test_name, success in results.items():
        status = "✅" if success else "❌"
        print(f"  {status} {test_name}")
    
    # Recommandations
    print("\n💡 Recommandations:")
    if failed_tests == 0:
        print("🎉 Tous les tests sont réussis !")
        print("🚀 La vue avancée des présences est prête à être utilisée")
        print("📋 Fonctionnalités disponibles:")
        print("  • Gestion complète des présences")
        print("  • Notifications automatiques")
        print("  • Export de rapports")
        print("  • Gestion des justificatifs")
        print("  • Système d'alertes")
        print("  • Planification et calendrier")
    else:
        print("⚠️ Certains tests ont échoué")
        print("🔧 Actions recommandées:")
        
        if not results.get("services_import", False):
            print("  • Vérifiez l'installation des dépendances")
        if not results.get("view_import", False):
            print("  • Vérifiez les imports de la vue avancée")
        if not results.get("dashboard_integration", False):
            print("  • Vérifiez l'intégration dans le dashboard")
        if not results.get("functionality_classes", False):
            print("  • Vérifiez la connexion à la base de données")

def main():
    """Fonction principale"""
    print("🏫 Test complet de l'intégration de la vue avancée des présences")
    print("=" * 70)
    
    # Lancer les tests
    results = test_complete_integration()
    
    # Afficher les résultats
    display_results(results)
    
    # Message final
    print("\n" + "=" * 70)
    if all(results.values()):
        print("🎉 INTÉGRATION COMPLÈTE RÉUSSIE !")
        print("🚀 La vue avancée des présences est maintenant intégrée et fonctionnelle")
    else:
        print("⚠️ INTÉGRATION PARTIELLE")
        print("🔧 Certains composants nécessitent une attention particulière")

if __name__ == "__main__":
    main()
