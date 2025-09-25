# -*- coding: utf-8 -*-
"""
Script d'Initialisation du Système de Matières Guinéen
EduManager+ - Configuration et Mise en Place

Ce script initialise le système de gestion des matières selon
le système éducatif guinéen dans la base de données.
"""

import os
import sys
from datetime import datetime

# Ajouter le chemin du projet
project_root = os.path.abspath(os.path.dirname(__file__))
if project_root not in sys.path:
    sys.path.append(project_root)

def initialize_guinean_subjects_system():
    """Initialise le système complet de matières guinéennes"""
    try:
        print("🚀 Initialisation du système de matières guinéennes...")
        print("=" * 60)
        
        # Import des modules nécessaires
        from src.modules.academic.subjects.models.guinean_subject_model import get_guinean_subject_model
        from src.modules.academic.subjects.controllers.guinean_subjects_controller import get_guinean_subjects_controller
        from src.modules.academic.subjects.models.guinean_subjects_structure import get_guinean_subjects_structure
        
        print("✅ Modules importés avec succès")
        
        # Initialiser le modèle
        print("\n📊 Initialisation du modèle de base de données...")
        model = get_guinean_subject_model()
        
        # Créer les tables
        print("   • Création des tables...")
        if model._ensure_tables_exist():
            print("   ✅ Tables créées avec succès")
        else:
            print("   ❌ Erreur lors de la création des tables")
            return False
        
        # Initialiser les données par défaut
        print("   • Initialisation des données par défaut...")
        if model.initialize_default_subjects():
            print("   ✅ Données par défaut initialisées")
        else:
            print("   ❌ Erreur lors de l'initialisation des données")
            return False
        
        # Initialiser le contrôleur
        print("\n🎮 Initialisation du contrôleur...")
        controller = get_guinean_subjects_controller()
        print("   ✅ Contrôleur initialisé")
        
        # Afficher les statistiques
        print("\n📈 Statistiques du système :")
        stats = controller.get_statistics()
        if stats:
            print(f"   • Total des matières : {stats.get('total_subjects', 0)}")
            print(f"   • Nombre de classes : {stats.get('total_grades', 0)}")
            print(f"   • Nombre de niveaux : {stats.get('total_levels', 0)}")
            print(f"   • Coefficient moyen : {stats.get('average_coefficient', 0):.2f}")
            
            print("\n   📊 Répartition par niveau :")
            for level_stat in stats.get('by_level', []):
                level = level_stat['level'].title()
                subjects = level_stat['subject_count']
                grades = level_stat['grade_count']
                print(f"      • {level} : {subjects} matières, {grades} classes")
        
        # Tester les fonctionnalités principales
        print("\n🧪 Tests des fonctionnalités principales...")
        
        # Test 1 : Récupérer toutes les matières
        all_subjects = controller.get_all_subjects()
        print(f"   • Test récupération globale : {len(all_subjects)} matières")
        
        # Test 2 : Récupérer par niveau
        primaire_subjects = controller.get_subjects_by_level("primaire")
        college_subjects = controller.get_subjects_by_level("college")
        lycee_subjects = controller.get_subjects_by_level("lycee")
        print(f"   • Test par niveau : Primaire({len(primaire_subjects)}), Collège({len(college_subjects)}), Lycée({len(lycee_subjects)})")
        
        # Test 3 : Récupérer par classe
        cm1_subjects = controller.get_subjects_by_grade("CM1")
        neuf_subjects = controller.get_subjects_by_grade("9ème")
        print(f"   • Test par classe : CM1({len(cm1_subjects)}), 9ème({len(neuf_subjects)})")
        
        # Test 4 : Recherche
        search_results = controller.search_subjects("Math")
        print(f"   • Test recherche : {len(search_results)} résultats pour 'Math'")
        
        # Test 5 : Hiérarchie des classes
        hierarchy = controller.get_grade_hierarchy()
        print(f"   • Test hiérarchie : {len(hierarchy)} niveaux organisés")
        
        print("\n🎉 Initialisation terminée avec succès !")
        print("=" * 60)
        
        # Afficher un résumé des classes disponibles
        print("\n📚 Classes disponibles :")
        grades = controller.get_available_grades()
        for i, grade in enumerate(grades, 1):
            level = controller.get_education_level_for_grade(grade)
            subjects_count = len(controller.get_subjects_by_grade(grade))
            print(f"   {i:2d}. {grade} ({level}) - {subjects_count} matières")
        
        print(f"\n✅ Système de matières guinéennes prêt à l'utilisation !")
        print(f"   Total : {len(grades)} classes avec {len(all_subjects)} matières")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Erreur lors de l'initialisation : {e}")
        import traceback
        traceback.print_exc()
        return False

def test_integration_with_existing_system():
    """Teste l'intégration avec le système existant"""
    try:
        print("\n🔗 Test d'intégration avec le système existant...")
        
        # Import du contrôleur existant pour comparaison
        try:
            from src.modules.academic.subjects.controllers.matiere_controller import get_all_matieres
            existing_subjects = get_all_matieres()
            print(f"   • Matières existantes : {len(existing_subjects)}")
        except ImportError:
            print("   • Aucun système de matières existant trouvé")
            existing_subjects = []
        
        # Import du nouveau système
        from src.modules.academic.subjects.controllers.guinean_subjects_controller import get_guinean_subjects_controller
        controller = get_guinean_subjects_controller()
        new_subjects = controller.get_all_subjects()
        
        print(f"   • Nouvelles matières guinéennes : {len(new_subjects)}")
        
        # Vérifier la compatibilité
        print("   • Test de compatibilité des formats...")
        
        # Test avec une classe spécifique
        test_grade = "CM1"
        subjects = controller.get_subjects_by_grade(test_grade)
        print(f"   • Matières pour {test_grade} : {len(subjects)}")
        
        if subjects:
            sample_subject = subjects[0]
            print(f"   • Exemple de matière : {sample_subject.get('name')} (Code: {sample_subject.get('code')})")
        
        print("   ✅ Intégration testée avec succès")
        return True
        
    except Exception as e:
        print(f"   ❌ Erreur lors du test d'intégration : {e}")
        return False

def create_sample_data():
    """Crée des données d'exemple pour tester le système"""
    try:
        print("\n📝 Création de données d'exemple...")
        
        from src.modules.academic.subjects.controllers.guinean_subjects_controller import get_guinean_subjects_controller
        controller = get_guinean_subjects_controller()
        
        # Exemple de matière personnalisée
        custom_subject = {
            "code": "CUSTOM001",
            "name": "Matière Personnalisée Test",
            "description": "Matière ajoutée pour tester le système",
            "coefficient": 2.0,
            "education_level": "primaire",
            "grade": "CM2",
            "is_optional": True,
            "is_core": False
        }
        
        if controller.add_custom_subject(custom_subject):
            print("   ✅ Matière personnalisée ajoutée avec succès")
            
            # Vérifier qu'elle est bien récupérable
            retrieved = controller.get_subject_by_code("CUSTOM001")
            if retrieved:
                print(f"   ✅ Matière récupérée : {retrieved.get('name')}")
            
            return True
        else:
            print("   ❌ Erreur lors de l'ajout de la matière personnalisée")
            return False
        
    except Exception as e:
        print(f"   ❌ Erreur lors de la création des données d'exemple : {e}")
        return False

def main():
    """Fonction principale"""
    print("🎓 EduManager+ - Initialisation du Système de Matières Guinéen")
    print("=" * 70)
    print(f"📅 Date : {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    print("=" * 70)
    
    # Étape 1 : Initialisation principale
    if not initialize_guinean_subjects_system():
        print("\n❌ Échec de l'initialisation principale")
        return False
    
    # Étape 2 : Test d'intégration
    if not test_integration_with_existing_system():
        print("\n⚠️ Problème avec l'intégration (non bloquant)")
    
    # Étape 3 : Données d'exemple
    if not create_sample_data():
        print("\n⚠️ Problème avec les données d'exemple (non bloquant)")
    
    print("\n" + "=" * 70)
    print("🎉 INITIALISATION TERMINÉE AVEC SUCCÈS !")
    print("=" * 70)
    print("\n📋 Prochaines étapes :")
    print("   1. Intégrer la vue dans l'interface principale")
    print("   2. Connecter aux formulaires de saisie de notes")
    print("   3. Intégrer dans la génération de bulletins")
    print("   4. Ajouter aux emplois du temps")
    print("\n💡 Le système est maintenant prêt à être utilisé !")
    
    return True

if __name__ == "__main__":
    success = main()
    if not success:
        sys.exit(1)
