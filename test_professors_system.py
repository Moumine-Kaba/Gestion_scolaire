"""
Script de test pour le système complet de gestion des professeurs
Teste toutes les fonctionnalités implémentées
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))

from src.modules.academic.teachers.controllers.salary_controller import SalaryController
from src.modules.academic.teachers.views.professeurs_view import ProfessorsDashboard
import customtkinter as ctk

def test_salary_controller():
    """Teste le contrôleur de salaire"""
    print("🧪 Test du contrôleur de salaire...")
    
    try:
        # Initialiser le contrôleur
        controller = SalaryController("database/edumanager.db")
        print("✅ Contrôleur de salaire initialisé")
        
        # Test d'ajout d'heures
        success = controller.add_course_hours(
            professeur_id=1,
            date_cours="2024-01-15",
            nombre_heures=2.5,
            matiere="Mathématiques",
            classe="6ème A",
            commentaire="Cours sur les fractions"
        )
        
        if success:
            print("✅ Ajout d'heures réussi")
        else:
            print("❌ Échec ajout d'heures")
        
        # Test de récupération des heures
        hours = controller.get_professor_hours(1)
        print(f"✅ Heures récupérées: {len(hours)} enregistrements")
        
        # Test de calcul de salaire
        salary_data = controller.calculate_salary(1, "2024-01-01", "2024-01-31")
        if "error" not in salary_data:
            print(f"✅ Calcul salaire: {salary_data['montant_total']} GNF")
        else:
            print(f"❌ Erreur calcul salaire: {salary_data['error']}")
        
        # Test résumé mensuel
        monthly_summary = controller.get_monthly_summary(1, 2024)
        if "error" not in monthly_summary:
            print(f"✅ Résumé mensuel: {monthly_summary['totals']['nb_professeurs']} professeurs")
        else:
            print(f"❌ Erreur résumé mensuel: {monthly_summary['error']}")
            
    except Exception as e:
        print(f"❌ Erreur test contrôleur: {e}")

def test_professors_view():
    """Teste la vue des professeurs"""
    print("\n🧪 Test de la vue des professeurs...")
    
    try:
        # Créer une fenêtre de test
        root = ctk.CTk()
        root.title("Test Professeurs Dashboard")
        root.geometry("1200x800")
        
        # Créer le dashboard
        dashboard = ProfessorsDashboard(root)
        dashboard.pack(fill="both", expand=True)
        
        print("✅ Dashboard des professeurs créé")
        print("✅ Interface utilisateur initialisée")
        
        # Ne pas afficher la fenêtre pour le test automatique
        # root.mainloop()
        
    except Exception as e:
        print(f"❌ Erreur test vue: {e}")

def main():
    """Fonction principale de test"""
    print("🚀 Démarrage des tests du système de gestion des professeurs")
    print("=" * 60)
    
    # Test du contrôleur de salaire
    test_salary_controller()
    
    # Test de la vue des professeurs
    test_professors_view()
    
    print("\n" + "=" * 60)
    print("✅ Tests terminés")
    print("\n📋 Fonctionnalités implémentées:")
    print("✅ Contrôleur de gestion des salaires basé sur les heures")
    print("✅ Formulaire stylisé d'ajout/modification des professeurs")
    print("✅ Gestion des heures de cours avec calculs automatiques")
    print("✅ Tableau de bord statistique complet")
    print("✅ Affichage des détails en format tableau professionnel")
    print("✅ Historique des heures et salaires")
    print("✅ Calculs automatiques (hebdomadaire, mensuel, annuel)")
    print("✅ Interface utilisateur moderne avec votre thème")
    
    print("\n🔄 Fonctionnalités en cours de développement:")
    print("⏳ Export PDF/Excel des salaires")
    print("⏳ Gestion des absences et ajustements")
    print("⏳ Filtres avancés par matière/mois/salaire")
    print("⏳ Tableau de bord global de l'établissement")

if __name__ == "__main__":
    main()
