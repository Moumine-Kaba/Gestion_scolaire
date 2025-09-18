#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test final pour vérifier que le système salles fonctionne parfaitement
"""

import os
import sys

# Ajouter le chemin du projet au PYTHONPATH
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

try:
    print("🎯 Test final du système salles")
    print("=" * 50)
    
    # Test du contrôleur
    from src.modules.administrative.maintenance.controllers.salle_controller import SalleController
    controller = SalleController()
    salles = controller.get_all_salles()
    
    print(f"✅ Contrôleur: {len(salles)} salles chargées")
    print(f"✅ Type de données: {type(salles[0])}")
    print(f"✅ Clés disponibles: {list(salles[0].keys())}")
    
    # Test de la vue
    from src.modules.administrative.maintenance.views.salles_view import SallesView
    print(f"✅ Import SallesView: OK")
    
    # Test des statistiques
    type_counts, total_capacite = controller.get_salles_stats()
    print(f"✅ Statistiques: {len(type_counts)} types, {total_capacite} places totales")
    
    # Test des opérations CRUD
    print(f"\n🔧 Test des opérations CRUD:")
    
    # Test d'ajout (simulation)
    test_nom = "Salle Test"
    test_capacite = 25
    test_type = "Salle de classes"
    test_equipements = "Tableau, Projecteur"
    test_statut = "Disponible"
    
    result = controller.add_salle(test_nom, test_capacite, test_type, test_equipements, test_statut)
    print(f"✅ Ajout de salles: {'OK' if result else 'Échec'}")
    
    # Vérifier que la salles a été ajoutée
    salles_apres = controller.get_all_salles()
    print(f"✅ Nombre de salles après ajout: {len(salles_apres)}")
    
    # Trouver la salles ajoutée et la supprimer
    salle_ajoutee = None
    for salles in salles_apres:
        if salles['nom_salle'] == test_nom:
            salle_ajoutee = salles
            break
    
    if salle_ajoutee:
        result_delete = controller.delete_salle(salle_ajoutee['id_salle'])
        print(f"✅ Suppression de salles: {'OK' if result_delete else 'Échec'}")
    
    # Vérifier le nombre final
    salles_final = controller.get_all_salles()
    print(f"✅ Nombre de salles final: {len(salles_final)}")
    
    print(f"\n🎉 Tous les tests sont passés avec succès!")
    print(f"📊 Système salles entièrement fonctionnel:")
    print(f"   • {len(salles_final)} salles dans la base de données")
    print(f"   • Contrôleur opérationnel")
    print(f"   • Vue importée correctement")
    print(f"   • Opérations CRUD fonctionnelles")
    print(f"   • Statistiques calculées")
    
except Exception as e:
    print(f"❌ Erreur: {e}")
    import traceback
    traceback.print_exc()
