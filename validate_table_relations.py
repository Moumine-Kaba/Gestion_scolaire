"""
Script de validation et réparation des liaisons entre tables
Vérifie et corrige les incohérences dans les données
"""

import os
import sys

# Ajouter le chemin du projet pour les imports
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..'))
if project_root not in sys.path:
    sys.path.append(project_root)

from src.modules.academic.grades.controllers.unified_grades_controller import (
    validate_data_consistency, 
    repair_data_consistency,
    get_student_complete_grades,
    get_class_complete_bulletins,
    get_subject_statistics
)

def main():
    """Fonction principale de validation et réparation"""
    print("🔧 VALIDATION ET RÉPARATION DES LIAISONS ENTRE TABLES")
    print("=" * 60)
    
    # 1. Validation de la cohérence
    print("\n📊 1. VALIDATION DE LA COHÉRENCE DES DONNÉES")
    print("-" * 40)
    
    consistency_check = validate_data_consistency()
    
    if consistency_check:
        print(f"✅ Score de cohérence: {consistency_check.get('score_coherence', 0)}%")
        print(f"📈 Total des problèmes détectés: {consistency_check.get('total_problemes', 0)}")
        
        # Afficher les détails
        issues = [
            ('notes_orphelines', 'Notes sans matière'),
            ('notes_sans_eleve', 'Notes sans élève'),
            ('bulletins_orphelins', 'Bulletins sans élève'),
            ('eleves_sans_notes', 'Élèves sans notes'),
            ('eleves_sans_bulletins', 'Élèves sans bulletins'),
            ('matieres_sans_notes', 'Matières sans notes')
        ]
        
        for key, description in issues:
            count = consistency_check.get(key, 0)
            if count > 0:
                print(f"⚠️  {description}: {count}")
            else:
                print(f"✅ {description}: 0")
    
    # 2. Réparation si nécessaire
    if consistency_check and consistency_check.get('total_problemes', 0) > 0:
        print(f"\n🔧 2. RÉPARATION DES INCOHÉRENCES")
        print("-" * 40)
        
        repairs = repair_data_consistency()
        
        if repairs:
            print("✅ Réparations effectuées:")
            for key, count in repairs.items():
                if count > 0:
                    print(f"   - {key}: {count} éléments nettoyés")
        else:
            print("⚠️ Aucune réparation effectuée")
    
    # 3. Test des liaisons
    print(f"\n🧪 3. TEST DES LIAISONS")
    print("-" * 40)
    
    # Test avec un élève spécifique
    test_student_id = 1
    print(f"🔍 Test des données complètes pour l'élève {test_student_id}")
    
    student_grades = get_student_complete_grades(test_student_id)
    if student_grades:
        print(f"✅ {len(student_grades)} matières récupérées avec liaisons")
        for subject in student_grades[:3]:  # Afficher les 3 premières
            print(f"   - {subject['nom_matiere']}: {subject['moyenne_matiere']:.2f}/20")
    else:
        print("⚠️ Aucune donnée trouvée pour cet élève")
    
    # Test avec une classe spécifique
    test_classe_id = 1
    print(f"\n🔍 Test des bulletins complets pour la classe {test_classe_id}")
    
    class_bulletins = get_class_complete_bulletins(test_classe_id)
    if class_bulletins:
        print(f"✅ {len(class_bulletins)} bulletins récupérés avec liaisons")
        for bulletin in class_bulletins[:3]:  # Afficher les 3 premiers
            print(f"   - {bulletin['eleve_prenom']} {bulletin['eleve_nom']}: {bulletin['moyenne_generale']:.2f}/20")
    else:
        print("⚠️ Aucun bulletin trouvé pour cette classe")
    
    # Test des statistiques de matière
    test_matiere_id = 1
    print(f"\n🔍 Test des statistiques pour la matière {test_matiere_id}")
    
    subject_stats = get_subject_statistics(test_matiere_id)
    if subject_stats:
        print(f"✅ Statistiques récupérées pour {subject_stats['nom_matiere']}")
        print(f"   - Nombre de notes: {subject_stats['nombre_notes']}")
        print(f"   - Moyenne générale: {subject_stats['moyenne_generale']:.2f}/20")
        print(f"   - Nombre d'élèves: {subject_stats['nombre_eleves']}")
    else:
        print("⚠️ Aucune statistique trouvée pour cette matière")
    
    print(f"\n🎉 VALIDATION TERMINÉE")
    print("=" * 60)

if __name__ == "__main__":
    main()


