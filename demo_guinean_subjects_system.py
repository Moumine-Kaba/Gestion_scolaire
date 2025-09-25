# -*- coding: utf-8 -*-
"""
Démonstration du Système de Matières Guinéen
EduManager+ - Exemples d'Utilisation

Ce script démontre les fonctionnalités du système de gestion
des matières organisées selon le système éducatif guinéen.
"""

import os
import sys

# Ajouter le chemin du projet
project_root = os.path.abspath(os.path.dirname(__file__))
if project_root not in sys.path:
    sys.path.append(project_root)

def demo_guinean_subjects_system():
    """Démonstration complète du système de matières guinéen"""
    try:
        print("🎓 EduManager+ - Démonstration du Système de Matières Guinéen")
        print("=" * 70)
        
        # Import du contrôleur
        from src.modules.academic.subjects.controllers.guinean_subjects_controller import get_guinean_subjects_controller
        controller = get_guinean_subjects_controller()
        
        print("✅ Contrôleur chargé avec succès")
        
        # 1. Statistiques générales
        print("\n📊 1. STATISTIQUES GÉNÉRALES")
        print("-" * 40)
        stats = controller.get_statistics()
        if stats:
            print(f"   • Total des matières : {stats.get('total_subjects', 0)}")
            print(f"   • Nombre de classes : {stats.get('total_grades', 0)}")
            print(f"   • Nombre de niveaux : {stats.get('total_levels', 0)}")
            print(f"   • Coefficient moyen : {stats.get('average_coefficient', 0):.2f}")
            
            print("\n   📈 Répartition par niveau :")
            for level_stat in stats.get('by_level', []):
                level = level_stat['level'].title()
                subjects = level_stat['subject_count']
                grades = level_stat['grade_count']
                print(f"      • {level} : {subjects} matières, {grades} classes")
        
        # 2. Classes disponibles
        print("\n📚 2. CLASSES DISPONIBLES")
        print("-" * 40)
        grades = controller.get_available_grades()
        print(f"   Total : {len(grades)} classes")
        
        # Afficher quelques exemples par niveau
        hierarchy = controller.get_grade_hierarchy()
        for level, level_grades in hierarchy.items():
            print(f"\n   🎒 {level.title()} :")
            for grade in level_grades[:3]:  # Afficher les 3 premières
                subjects_count = len(controller.get_subjects_by_grade(grade))
                print(f"      • {grade} ({subjects_count} matières)")
            if len(level_grades) > 3:
                print(f"      • ... et {len(level_grades) - 3} autres classes")
        
        # 3. Exemple : Matières d'une classe primaire
        print("\n🎒 3. EXEMPLE : MATIÈRES DU PRIMAIRE (CM1)")
        print("-" * 40)
        cm1_subjects = controller.get_subjects_by_grade("CM1")
        print(f"   Total : {len(cm1_subjects)} matières")
        
        for subject in cm1_subjects:
            optional_marker = " (OPTIONNEL)" if subject.get("is_optional") else ""
            core_marker = " (FONDAMENTAL)" if subject.get("is_core") else ""
            print(f"   • {subject.get('name')} - Coeff: {subject.get('coefficient')}{optional_marker}{core_marker}")
        
        # 4. Exemple : Matières d'une classe du collège
        print("\n🎓 4. EXEMPLE : MATIÈRES DU COLLÈGE (9ème)")
        print("-" * 40)
        neuf_subjects = controller.get_subjects_by_grade("9ème")
        print(f"   Total : {len(neuf_subjects)} matières")
        
        # Séparer matières fondamentales et optionnelles
        core_subjects = [s for s in neuf_subjects if s.get("is_core")]
        optional_subjects = [s for s in neuf_subjects if s.get("is_optional")]
        
        print(f"   📖 Matières fondamentales ({len(core_subjects)}) :")
        for subject in core_subjects[:5]:  # Afficher les 5 premières
            print(f"      • {subject.get('name')} - Coeff: {subject.get('coefficient')}")
        if len(core_subjects) > 5:
            print(f"      • ... et {len(core_subjects) - 5} autres")
        
        if optional_subjects:
            print(f"   🔧 Matières optionnelles ({len(optional_subjects)}) :")
            for subject in optional_subjects:
                print(f"      • {subject.get('name')} - Coeff: {subject.get('coefficient')}")
        
        # 5. Exemple : Matières du lycée
        print("\n🎯 5. EXEMPLE : MATIÈRES DU LYCÉE (11ème Sciences Mathématiques)")
        print("-" * 40)
        lycee_grade = "11ème Sciences Mathématiques"
        lycee_subjects = controller.get_subjects_by_grade(lycee_grade)
        print(f"   Total : {len(lycee_subjects)} matières")
        
        # Grouper par type
        core_lycee = [s for s in lycee_subjects if s.get("is_core")]
        specialized_lycee = [s for s in lycee_subjects if not s.get("is_core") and not s.get("is_optional")]
        optional_lycee = [s for s in lycee_subjects if s.get("is_optional")]
        
        print(f"   📖 Matières communes ({len(core_lycee)}) :")
        for subject in core_lycee:
            print(f"      • {subject.get('name')} - Coeff: {subject.get('coefficient')}")
        
        print(f"   🔬 Matières spécialisées ({len(specialized_lycee)}) :")
        for subject in specialized_lycee:
            print(f"      • {subject.get('name')} - Coeff: {subject.get('coefficient')}")
        
        if optional_lycee:
            print(f"   🔧 Matières optionnelles ({len(optional_lycee)}) :")
            for subject in optional_lycee:
                print(f"      • {subject.get('name')} - Coeff: {subject.get('coefficient')}")
        
        # 6. Fonctionnalités de recherche
        print("\n🔍 6. FONCTIONNALITÉS DE RECHERCHE")
        print("-" * 40)
        
        # Recherche par nom
        math_results = controller.search_subjects("Math")
        print(f"   Recherche 'Math' : {len(math_results)} résultats")
        for subject in math_results[:3]:
            print(f"      • {subject.get('name')} ({subject.get('grade')})")
        if len(math_results) > 3:
            print(f"      • ... et {len(math_results) - 3} autres")
        
        # Recherche par niveau
        primaire_results = controller.search_subjects("", level="primaire")
        print(f"   Recherche par niveau 'primaire' : {len(primaire_results)} matières")
        
        # 7. Fonctionnalités d'export
        print("\n📤 7. EXPORT DE LA STRUCTURE")
        print("-" * 40)
        export_data = controller.export_subjects_structure()
        print(f"   Structure exportée : {len(export_data)} niveaux")
        for level, grades_data in export_data.items():
            total_subjects = sum(len(subjects) for subjects in grades_data.values())
            print(f"   • {level.title()} : {len(grades_data)} classes, {total_subjects} matières")
        
        # 8. Test d'ajout de matière personnalisée
        print("\n➕ 8. TEST D'AJOUT DE MATIÈRE PERSONNALISÉE")
        print("-" * 40)
        
        # Code unique basé sur le timestamp pour éviter les doublons
        import time
        timestamp = int(time.time()) % 10000
        custom_subject = {
            "code": f"DEMO{timestamp:04d}",
            "name": "Démonstration - Informatique Avancée",
            "description": "Matière ajoutée pour démonstration du système",
            "coefficient": 3.0,
            "education_level": "college",
            "grade": "10ème",
            "is_optional": True,
            "is_core": False
        }
        
        if controller.add_custom_subject(custom_subject):
            print("   ✅ Matière personnalisée ajoutée avec succès")
            
            # Vérifier qu'elle est récupérable
            demo_code = f"DEMO{timestamp:04d}"
            retrieved = controller.get_subject_by_code(demo_code)
            if retrieved:
                print(f"   ✅ Matière récupérée : {retrieved.get('name')} (Coeff: {retrieved.get('coefficient')})")
            
            # Vérifier qu'elle apparaît dans les matières de la classe
            grade_subjects = controller.get_subjects_by_grade("10ème")
            demo_found = any(s.get("code") == demo_code for s in grade_subjects)
            if demo_found:
                print("   ✅ Matière visible dans les matières de la 10ème")
        else:
            print("   ❌ Échec de l'ajout de la matière personnalisée")
        
        print("\n" + "=" * 70)
        print("🎉 DÉMONSTRATION TERMINÉE AVEC SUCCÈS !")
        print("=" * 70)
        
        print("\n💡 RÉSUMÉ DES FONCTIONNALITÉS DÉMONTRÉES :")
        print("   ✅ Gestion par niveaux (Primaire, Collège, Lycée)")
        print("   ✅ Organisation par classes et séries")
        print("   ✅ Distinction matières fondamentales/optionnelles")
        print("   ✅ Recherche avancée par nom et niveau")
        print("   ✅ Export de la structure complète")
        print("   ✅ Ajout de matières personnalisées")
        print("   ✅ Statistiques détaillées")
        
        print(f"\n📊 RÉSULTATS :")
        print(f"   • {stats.get('total_subjects', 0)} matières organisées")
        print(f"   • {stats.get('total_grades', 0)} classes gérées")
        print(f"   • {stats.get('total_levels', 0)} niveaux d'éducation")
        print(f"   • Système prêt pour l'intégration dans EduManager+")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Erreur lors de la démonstration : {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Fonction principale"""
    success = demo_guinean_subjects_system()
    if not success:
        sys.exit(1)
    return success

if __name__ == "__main__":
    main()
