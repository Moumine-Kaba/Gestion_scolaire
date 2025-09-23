"""
Script de test pour vérifier l'affichage des données dans les bulletins
"""

import os
import sys

# Ajouter le chemin du projet pour les imports
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '.'))
if project_root not in sys.path:
    sys.path.append(project_root)

from src.modules.academic.grades.controllers.unified_grades_controller import get_student_complete_grades

def test_student_data():
    """Test des données d'un élève spécifique"""
    print("🧪 TEST DES DONNÉES D'UN ÉLÈVE")
    print("=" * 50)
    
    # Tester avec différents élèves
    test_students = [1, 2, 3, 72]  # IDs d'élèves à tester
    
    for student_id in test_students:
        print(f"\n🔍 Test de l'élève {student_id}")
        print("-" * 30)
        
        try:
            # Récupérer les données complètes
            complete_grades = get_student_complete_grades(student_id)
            
            if complete_grades:
                print(f"✅ {len(complete_grades)} matières trouvées")
                
                # Afficher les détails de chaque matière
                total_points = 0
                total_coefficients = 0
                
                for i, subject in enumerate(complete_grades, 1):
                    matiere = subject['nom_matiere']
                    coefficient = float(subject['coefficient']) if subject['coefficient'] else 1.0
                    note = float(subject['moyenne_matiere']) if subject['moyenne_matiere'] else 0.0
                    nb_notes = len(subject['notes'])
                    
                    print(f"   {i:2d}. {matiere:<20} | Coef: {coefficient:2.1f} | Note: {note:5.2f} | Nb notes: {nb_notes}")
                    print(f"       Debug - ID: {subject['id_matiere']}, Nom brut: '{subject.get('nom_matiere', 'N/A')}'")
                    
                    # Calculer pour la moyenne générale
                    if note > 0:
                        total_points += note * coefficient
                        total_coefficients += coefficient
                
                # Calculer la moyenne générale
                if total_coefficients > 0:
                    moyenne_generale = total_points / total_coefficients
                    print(f"\n📊 MOYENNE GÉNÉRALE: {moyenne_generale:.2f}/20")
                    
                    # Calculer la mention
                    if moyenne_generale >= 16:
                        mention = "EXCELLENT"
                    elif moyenne_generale >= 14:
                        mention = "TRÈS BIEN"
                    elif moyenne_generale >= 12:
                        mention = "BIEN"
                    elif moyenne_generale >= 10:
                        mention = "ASSEZ BIEN"
                    else:
                        mention = "INSUFFISANT"
                    
                    print(f"🏆 MENTION: {mention}")
                else:
                    print("\n⚠️ Aucune note valide trouvée")
                    
            else:
                print(f"⚠️ Aucune donnée trouvée pour l'élève {student_id}")
                
        except Exception as e:
            print(f"❌ Erreur pour l'élève {student_id}: {e}")
    
    print(f"\n🎉 TEST TERMINÉ")
    print("=" * 50)

if __name__ == "__main__":
    test_student_data()
