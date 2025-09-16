#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test de l'Organisation des Vues
================================

Script pour vérifier que toutes les vues sont correctement organisées.
"""

import os
import sys
from pathlib import Path


def test_views_structure():
    """Teste la structure des vues"""
    print("📁 Test de la structure des vues...")
    
    expected_structure = {
        "src/modules/auth/views": [
            "login_view.py", "register_view.py", "splash_view.py", 
            "login_enhanced.py", "dashboard_view.py", "utilisateurs_view.py", 
            "view_manager.py"
        ],
        "src/modules/academic/students/views": [
            "eleves_dashboard.py"
        ],
        "src/modules/academic/teachers/views": [
            "professeurs_view.py"
        ],
        "src/modules/academic/classes/views": [
            "classes_view.py", "enseignements_view.py", "emplois_view.py", 
            "presences_view.py"
        ],
        "src/modules/academic/subjects/views": [
            "matieres_view.py", "competences_view.py", "objectifs_view.py"
        ],
        "src/modules/academic/grades/views": [
            "notes_view.py", "bulletins_view.py"
        ],
        "src/modules/administrative/personnel/views": [
            "personnel_view.py", "carrieres_view.py"
        ],
        "src/modules/administrative/payments/views": [
            "paiements_view.py"
        ],
        "src/modules/administrative/maintenance/views": [
            "maintenances_view.py", "salles_view.py", "taches_view.py"
        ],
        "src/modules/communication/messaging/views": [
            "messagerie_view.py", "transfert_view.py"
        ],
        "src/modules/communication/notifications/views": [
            "notifications_view.py"
        ],
        "src/modules/communication/announcements/views": [
            "actualites_view.py", "annonces_view.py", "bibliotheque_view.py",
            "documents_view.py", "calendriers_view.py"
        ],
        "src/shared/utils": [
            "preload_cache.py"
        ]
    }
    
    all_passed = True
    
    for directory, expected_files in expected_structure.items():
        dir_path = Path(directory)
        if not dir_path.exists():
            print(f"❌ Dossier manquant: {directory}")
            all_passed = False
            continue
        
        print(f"✅ {directory}")
        
        for expected_file in expected_files:
            file_path = dir_path / expected_file
            if file_path.exists():
                print(f"  ✅ {expected_file}")
            else:
                print(f"  ❌ Fichier manquant: {expected_file}")
                all_passed = False
    
    return all_passed


def test_views_imports():
    """Teste les imports des vues"""
    print("\n🧪 Test des imports des vues...")
    
    try:
        # Test des vues d'authentification
        from src.modules.auth.views import (
            LoginView, RegisterView, SplashView, LoginEnhanced,
            DashboardView, UtilisateursView, ViewManager
        )
        print("✅ Vues d'authentification importées avec succès")
        
        # Test des vues académiques
        from src.modules.academic.students.views import ElevesDashboard
        from src.modules.academic.teachers.views import ProfesseursView
        from src.modules.academic.classes.views import ClassesView
        from src.modules.academic.subjects.views import MatieresView
        from src.modules.academic.grades.views import NotesView
        print("✅ Vues académiques importées avec succès")
        
        # Test des vues administratives
        from src.modules.administrative.personnel.views import PersonnelView
        from src.modules.administrative.payments.views import PaiementsView
        from src.modules.administrative.maintenance.views import SallesView
        print("✅ Vues administratives importées avec succès")
        
        # Test des vues de communication
        from src.modules.communication.messaging.views import MessagerieView
        from src.modules.communication.notifications.views import NotificationsView
        from src.modules.communication.announcements.views import ActualitesView
        print("✅ Vues de communication importées avec succès")
        
        return True
        
    except ImportError as e:
        print(f"❌ Erreur d'import: {e}")
        return False
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False


def test_old_views_removed():
    """Teste que les anciennes vues ont été supprimées"""
    print("\n🗑️  Test de suppression des anciennes vues...")
    
    old_views_dir = Path("views")
    if old_views_dir.exists():
        print(f"❌ L'ancien dossier 'views' existe encore: {old_views_dir}")
        return False
    else:
        print("✅ L'ancien dossier 'views' a été supprimé")
        return True


def main():
    """Fonction principale"""
    print("🏗️  Test de l'Organisation des Vues EduManager+")
    print("=" * 60)
    
    # Tests
    tests = [
        ("Structure des vues", test_views_structure),
        ("Imports des vues", test_views_imports),
        ("Suppression anciennes vues", test_old_views_removed)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n🔍 {test_name}...")
        result = test_func()
        results.append((test_name, result))
    
    # Résumé
    print("\n" + "=" * 60)
    print("📊 Résumé des tests:")
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASSÉ" if result else "❌ ÉCHOUÉ"
        print(f"  - {test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\n🎯 Résultat: {passed}/{total} tests passés")
    
    if passed == total:
        print("\n🎉 Tous les tests sont passés!")
        print("   L'organisation des vues est correcte.")
        print("\n   Structure finale:")
        print("   📁 src/modules/auth/views/ - Vues d'authentification")
        print("   📁 src/modules/academic/*/views/ - Vues académiques")
        print("   📁 src/modules/administrative/*/views/ - Vues administratives")
        print("   📁 src/modules/communication/*/views/ - Vues de communication")
        print("   📁 src/shared/utils/ - Utilitaires partagés")
    else:
        print(f"\n⚠️  {total - passed} test(s) ont échoué.")
        print("   Vérifiez l'organisation et corrigez les problèmes.")
    
    return passed == total


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
