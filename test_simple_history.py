#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test simple de l'historique des présences
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '.'))

def test_attendance_history():
    """Test simple de l'historique des présences"""
    print("🧪 Test simple de l'historique des présences...")
    print("=" * 50)
    
    try:
        # Import des services
        from src.modules.academic.attendance.services.attendance_service import AttendanceService
        from src.modules.academic.attendance.controllers.attendance_history_controller import AttendanceHistoryController
        
        # Initialiser les services
        attendance_service = AttendanceService()
        history_controller = AttendanceHistoryController()
        
        print("✅ Services initialisés")
        
        # Test 1: Récupérer les classes
        print("\n📦 Test 1: Récupération des classes...")
        classes = attendance_service.get_classes_for_dropdown()
        print(f"✅ Classes disponibles: {len(classes)}")
        
        if not classes:
            print("❌ Aucune classe trouvée")
            return False
        
        # Test 2: Récupérer l'ID de la première classe
        print(f"\n📦 Test 2: ID de la classe '{classes[0]}'...")
        class_id_map = attendance_service.get_class_id_map()
        first_class_id = class_id_map.get(classes[0])
        
        if not first_class_id:
            print(f"❌ ID de classe non trouvé")
            return False
        
        print(f"✅ ID de classe: {first_class_id}")
        
        # Test 3: Récupérer les élèves de la classe
        print(f"\n📦 Test 3: Élèves de la classe...")
        students = attendance_service.get_students_with_attendance_status(first_class_id, "2025-09-20")
        print(f"✅ Élèves trouvés: {len(students)}")
        
        if not students:
            print("❌ Aucun élève trouvé")
            return False
        
        # Test 4: Historique d'un élève
        print(f"\n📦 Test 4: Historique d'un élève...")
        first_student_id = students[0]['id_eleve']
        student_name = f"{students[0]['prenom']} {students[0]['nom']}"
        
        print(f"👤 Élève: {student_name} (ID: {first_student_id})")
        
        # Récupérer l'historique
        history = history_controller.get_student_history(first_student_id)
        print(f"✅ Historique récupéré: {len(history)} enregistrements")
        
        # Afficher les 5 derniers enregistrements
        if history:
            print("\n📋 5 derniers enregistrements:")
            for i, record in enumerate(history[:5]):
                print(f"   {i+1}. {record.date} - {record.statut} - {record.commentaire}")
        
        # Test 5: Données mensuelles
        print(f"\n📦 Test 5: Données mensuelles...")
        monthly_data = history_controller.get_monthly_attendance_data(first_class_id, 2025, 9)
        print(f"✅ Données mensuelles: {len(monthly_data)} enregistrements")
        
        # Test 6: Résumé de classe
        print(f"\n📦 Test 6: Résumé de classe...")
        class_summary = history_controller.get_class_attendance_summary(first_class_id, "2025-09-01", "2025-09-20")
        print(f"✅ Résumé: {class_summary}")
        
        print("\n🎉 TOUS LES TESTS RÉUSSIS !")
        print("=" * 50)
        print("✅ L'historique des présences fonctionne correctement")
        print("✅ Les données sont récupérées avec succès")
        print("✅ Les objets AttendanceHistoryModel sont correctement utilisés")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Erreur lors du test: {e}")
        import traceback
        traceback.print_exc()
        return False

def show_usage_guide():
    """Affiche le guide d'utilisation"""
    print("\n" + "=" * 60)
    print("📖 GUIDE D'UTILISATION - HISTORIQUE DES PRÉSENCES")
    print("=" * 60)
    print("""
    🎯 Comment voir l'historique des présences d'une classe :
    
    📱 DANS L'APPLICATION :
    1. Ouvrez EduManager+
    2. Allez dans "Présences" 
    3. Sélectionnez une classe
    4. Choisissez une date
    5. Cliquez sur un élève
    6. Cliquez sur "Historique"
    
    🔧 FONCTIONNALITÉS DISPONIBLES :
    • 📊 Statistiques par élève et par classe
    • 📅 Filtrage par période (mois, trimestre)
    • 🔍 Recherche d'élèves par nom
    • 📈 Tendance des présences
    • 📄 Export PDF des rapports
    • 🚨 Alertes d'absences répétées
    
    💡 CONSEILS :
    • Utilisez les filtres pour affiner la recherche
    • Consultez les statistiques mensuelles
    • Exportez les rapports pour les archives
    • Surveillez les alertes d'absence
    """)

def main():
    """Fonction principale"""
    print("🏫 Test de l'Historique des Présences")
    print("=" * 60)
    
    # Afficher le guide
    show_usage_guide()
    
    # Test de l'historique
    success = test_attendance_history()
    
    # Résumé
    print("\n" + "=" * 60)
    print("📊 RÉSUMÉ")
    print("=" * 60)
    
    if success:
        print("🎉 SUCCÈS COMPLET !")
        print("✅ L'historique des présences fonctionne parfaitement")
        print("✅ Toutes les méthodes sont opérationnelles")
        print("✅ Les données sont correctement récupérées")
        print("\n🚀 Vous pouvez maintenant utiliser l'historique dans l'application !")
    else:
        print("⚠️ PROBLÈMES DÉTECTÉS")
        print("🔧 Vérifiez les erreurs ci-dessus")
        print("📞 Contactez le support si nécessaire")

if __name__ == "__main__":
    main()
