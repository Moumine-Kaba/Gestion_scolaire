"""
Script simple pour tester les données d'un élève
"""

import os
import sys

# Ajouter le chemin du projet pour les imports
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '.'))
if project_root not in sys.path:
    sys.path.append(project_root)

try:
    from src.modules.academic.grades.controllers.unified_grades_controller import get_student_complete_grades
    
    print("🧪 TEST SIMPLE DES DONNÉES")
    print("=" * 40)
    
    # Tester avec l'élève 1
    student_id = 1
    print(f"🔍 Test de l'élève {student_id}")
    
    complete_grades = get_student_complete_grades(student_id)
    
    if complete_grades:
        print(f"✅ {len(complete_grades)} matières trouvées")
        
        for i, subject in enumerate(complete_grades[:3], 1):  # Afficher les 3 premières
            print(f"   {i}. ID: {subject['id_matiere']}")
            print(f"      Nom: '{subject['nom_matiere']}'")
            print(f"      Coef: {subject['coefficient']}")
            print(f"      Note: {subject['moyenne_matiere']}")
            print(f"      Nb notes: {len(subject['notes'])}")
            print()
    else:
        print("⚠️ Aucune donnée trouvée")
        
except Exception as e:
    print(f"❌ Erreur: {e}")
    import traceback
    traceback.print_exc()

print("🎉 TEST TERMINÉ")


