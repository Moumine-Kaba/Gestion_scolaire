#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test de l'Organisation Complète du Projet
=========================================

Script pour vérifier que TOUS les fichiers sont correctement organisés.
"""

import os
import sys
from pathlib import Path


def test_complete_structure():
    """Teste la structure complète du projet"""
    print("📁 Test de la structure complète du projet...")
    
    expected_structure = {
        # Structure principale
        "src": {
            "core": ["app.py", "config.py", "exceptions.py", "app_legacy.py", "config_legacy.py"],
            "modules": {
                "auth": {
                    "models": ["auth.py", "role.py", "permissions.py", "permission_manager.py", "view_permissions.py", "view_access_manager.py", "auth_enhanced.py", "utilisateur.py"],
                    "controllers": ["user_controller.py"],
                    "views": ["login_view.py", "register_view.py", "splash_view.py", "login_enhanced.py", "dashboard_view.py", "utilisateurs_view.py", "view_manager.py"],
                    "services": []
                },
                "academic": {
                    "students": {
                        "models": ["eleve.py"],
                        "controllers": ["eleve_controller.py"],
                        "views": ["eleves_dashboard.py"],
                        "services": []
                    },
                    "teachers": {
                        "models": ["professeur.py"],
                        "controllers": ["professeur_controller.py"],
                        "views": ["professeurs_view.py"],
                        "services": []
                    },
                    "classes": {
                        "models": ["classe.py", "enseignement.py", "emploi_du_temps.py", "presence.py"],
                        "controllers": ["classe_controller.py", "enseignement_controller.py", "emplois_controller.py", "presence_controller.py"],
                        "views": ["classes_view.py", "enseignements_view.py", "emplois_view.py", "presences_view.py"],
                        "services": []
                    },
                    "subjects": {
                        "models": ["matiere.py", "competence.py", "objectif.py"],
                        "controllers": ["matiere_controller.py", "competence_controller.py", "objectif_controller.py", "subject_controller.py"],
                        "views": ["matieres_view.py", "competences_view.py", "objectifs_view.py"],
                        "services": []
                    },
                    "grades": {
                        "models": ["note.py", "bulletin.py"],
                        "controllers": ["notes_controller.py", "bulletin_controller.py"],
                        "views": ["notes_view.py", "bulletins_view.py"],
                        "services": []
                    }
                },
                "administrative": {
                    "personnel": {
                        "models": ["personnel.py", "carriere.py"],
                        "controllers": ["personnel_controller.py", "carriere_controller.py"],
                        "views": ["personnel_view.py", "carrieres_view.py"],
                        "services": []
                    },
                    "payments": {
                        "models": ["paiement.py"],
                        "controllers": ["paiement_controller.py"],
                        "views": ["paiements_view.py"],
                        "services": []
                    },
                    "maintenance": {
                        "models": ["maintenance.py", "salle.py", "tache.py"],
                        "controllers": ["maintenance_controller.py", "salle_controller.py", "tache_controller.py"],
                        "views": ["maintenances_view.py", "salles_view.py", "taches_view.py"],
                        "services": []
                    }
                },
                "communication": {
                    "messaging": {
                        "models": ["messagerie.py"],
                        "controllers": ["message_controller.py", "transfert_controller.py"],
                        "views": ["messagerie_view.py", "transfert_view.py"],
                        "services": []
                    },
                    "notifications": {
                        "models": ["notification.py"],
                        "controllers": ["notification_controller.py"],
                        "views": ["notifications_view.py"],
                        "services": []
                    },
                    "announcements": {
                        "models": ["actualite.py", "annonce.py", "bibliotheque.py", "document.py", "calendrier.py"],
                        "controllers": ["actualite_controller.py", "annonce_controller.py", "bibliotheque_controller.py", "document_controller.py", "calendrier_controller.py"],
                        "views": ["actualites_view.py", "annonces_view.py", "bibliotheque_view.py", "documents_view.py", "calendriers_view.py"],
                        "services": []
                    }
                }
            },
            "shared": {
                "components": [],
                "decorators": [],
                "mixins": [],
                "constants": ["theme.py"],
                "utils": ["preload_cache.py"]
            },
            "utils": {
                "helpers": ["db_utils.py"],
                "validators": ["validators.py"],
                "formatters": []
            }
        },
        "tests": {
            "legacy": ["test_*.py"],
            "unit": [],
            "integration": [],
            "fixtures": []
        },
        "docs": {
            "api": [],
            "user_guide": ["README.md"],
            "developer": ["SETUP.md", "TROUBLESHOOTING.md", "GUIDE_*.md", "SOLUTION_*.md", "RESUME_*.md"],
            "architecture": ["NOUVELLE_ORGANISATION.md", "ARCHITECTURE_NOUVELLE.md", "ORGANISATION_VUES_COMPLETE.md"]
        },
        "scripts": {
            "database": ["init_users.py", "init_roles_and_permissions.py", "init_roles_simple.py", "init_tables.py", "init_test_data.py", "init_admin.py", "assign_roles.py", "create_test_users.py", "show_connection_info.py", "show_users_and_roles.py"],
            "maintenance": ["repair_system.py"],
            "deployment": []
        },
        "resources": {
            "images": [],
            "icons": [],
            "themes": [],
            "locales": []
        },
        "data": ["eleves.csv"],
        "deployment": {
            "requirements": ["requirements.txt"]
        }
    }
    
    def check_structure(base_path: Path, structure: dict, level: int = 0) -> bool:
        """Vérifie récursivement la structure"""
        indent = "  " * level
        all_passed = True
        
        for item, expected in structure.items():
            item_path = base_path / item
            
            if isinstance(expected, list):
                # C'est une liste de fichiers
                if not item_path.exists():
                    print(f"{indent}❌ {item} (dossier manquant)")
                    all_passed = False
                    continue
                
                print(f"{indent}✅ {item}/")
                
                for expected_file in expected:
                    if expected_file.endswith("*"):
                        # Pattern wildcard
                        pattern = expected_file.replace("*", "")
                        matching_files = list(item_path.glob(f"{pattern}*"))
                        if matching_files:
                            for file in matching_files:
                                print(f"{indent}  ✅ {file.name}")
                        else:
                            print(f"{indent}  ⚠️  Aucun fichier trouvé pour le pattern: {expected_file}")
                    else:
                        # Fichier spécifique
                        file_path = item_path / expected_file
                        if file_path.exists():
                            print(f"{indent}  ✅ {expected_file}")
                        else:
                            print(f"{indent}  ❌ {expected_file} (manquant)")
                            all_passed = False
                            
            elif isinstance(expected, dict):
                # C'est un sous-dossier
                if not item_path.exists():
                    print(f"{indent}❌ {item}/ (dossier manquant)")
                    all_passed = False
                    continue
                
                print(f"{indent}✅ {item}/")
                if not check_structure(item_path, expected, level + 1):
                    all_passed = False
            else:
                # C'est un fichier simple
                if not item_path.exists():
                    print(f"{indent}❌ {item} (fichier manquant)")
                    all_passed = False
                else:
                    print(f"{indent}✅ {item}")
        
        return all_passed
    
    return check_structure(Path("."), expected_structure)


def test_imports():
    """Teste les imports des modules principaux"""
    print("\n🧪 Test des imports des modules principaux...")
    
    try:
        # Test du module core
        from src.core.config import get_config
        print("✅ Module core.config importé avec succès")
        
        # Test de la configuration
        config = get_config()
        print(f"✅ Configuration chargée: {config.app_name} v{config.version}")
        
        return True
        
    except ImportError as e:
        print(f"❌ Erreur d'import: {e}")
        return False
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False


def test_old_structure_removed():
    """Teste que l'ancienne structure a été supprimée"""
    print("\n🗑️  Test de suppression de l'ancienne structure...")
    
    old_items = [
        "models",
        "controllers", 
        "views",
        "utils"
    ]
    
    all_removed = True
    
    for item in old_items:
        item_path = Path(item)
        if item_path.exists():
            print(f"❌ L'ancien dossier '{item}' existe encore: {item_path}")
            all_removed = False
        else:
            print(f"✅ L'ancien dossier '{item}' a été supprimé")
    
    return all_removed


def main():
    """Fonction principale"""
    print("🏗️  Test de l'Organisation Complète du Projet EduManager+")
    print("=" * 80)
    
    # Tests
    tests = [
        ("Structure complète", test_complete_structure),
        ("Imports des modules", test_imports),
        ("Suppression ancienne structure", test_old_structure_removed)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n🔍 {test_name}...")
        result = test_func()
        results.append((test_name, result))
    
    # Résumé
    print("\n" + "=" * 80)
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
        print("   L'organisation complète du projet est correcte.")
        print("\n   Structure finale:")
        print("   📁 src/modules/* - Modules métier organisés")
        print("   📁 tests/* - Tests organisés par type")
        print("   📁 docs/* - Documentation organisée")
        print("   📁 scripts/* - Scripts organisés par fonction")
        print("   📁 resources/* - Ressources organisées")
        print("\n   Pour démarrer l'application:")
        print("   python scripts/start_app.py")
        print("   python -m src.core.app")
    else:
        print(f"\n⚠️  {total - passed} test(s) ont échoué.")
        print("   Vérifiez l'organisation et corrigez les problèmes.")
    
    return passed == total


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
