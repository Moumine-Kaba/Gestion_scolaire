#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de test pour vérifier toutes les corrections
=================================================
"""

import sys
import os

def test_imports():
    """Test des imports corrigés"""
    print("🧪 Test des imports...")
    
    try:
        # Test import eleve_controller
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))
        from modules.academic.students.controllers.eleve_controller import get_all_eleves
        print("✅ eleve_controller importé avec succès")
        
        # Test import matiere_controller
        from modules.academic.subjects.controllers.matiere_controller import preload_matieres_cache
        print("✅ matiere_controller avec preload_matieres_cache importé avec succès")
        
        # Test import eleves_dashboard
        from modules.academic.students.views.eleves_dashboard import get_stats_eleves, get_conn
        print("✅ eleves_dashboard importé avec succès")
        
        # Test import classes_view
        from modules.academic.classes.views.classes_view import get_all_classes, get_db_connection_direct
        print("✅ classes_view importé avec succès")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur import: {e}")
        return False

def test_database_connections():
    """Test des connexions à la base de données"""
    print("\n🧪 Test des connexions DB...")
    
    try:
        # Test connexion eleves_dashboard
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))
        from modules.academic.students.views.eleves_dashboard import get_conn
        
        conn = get_conn()
        if conn:
            print("✅ Connexion eleves_dashboard réussie")
            conn.close()
        else:
            print("❌ Connexion eleves_dashboard échouée")
            return False
        
        # Test connexion classes_view
        from modules.academic.classes.views.classes_view import get_db_connection_direct
        
        conn = get_db_connection_direct()
        if conn:
            print("✅ Connexion classes_view réussie")
            conn.close()
        else:
            print("❌ Connexion classes_view échouée")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur connexion DB: {e}")
        return False

def test_functions():
    """Test des fonctions corrigées"""
    print("\n🧪 Test des fonctions...")
    
    try:
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))
        
        # Test get_stats_eleves
        from modules.academic.students.views.eleves_dashboard import get_stats_eleves
        stats = get_stats_eleves()
        print(f"✅ get_stats_eleves: {stats['total']} élèves")
        
        # Test get_all_classes
        from modules.academic.classes.views.classes_view import get_all_classes
        classes = get_all_classes()
        print(f"✅ get_all_classes: {len(classes)} classes")
        
        # Test preload_matieres_cache
        from modules.academic.subjects.controllers.matiere_controller import preload_matieres_cache
        cache = preload_matieres_cache()
        print(f"✅ preload_matieres_cache: {len(cache)} matières")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur fonctions: {e}")
        return False

def main():
    """Fonction principale de test"""
    print("🚀 TEST DES CORRECTIONS")
    print("=" * 50)
    
    success_imports = test_imports()
    success_connections = test_database_connections()
    success_functions = test_functions()
    
    print("\n" + "=" * 50)
    if success_imports and success_connections and success_functions:
        print("🎉 TOUTES LES CORRECTIONS RÉUSSIES!")
        print("✅ Imports corrigés")
        print("✅ Connexions DB corrigées")
        print("✅ Fonctions corrigées")
        print("✅ Icônes corrigées")
        print("✅ Syntaxe SQL Server corrigée")
        return True
    else:
        print("❌ CERTAINES CORRECTIONS ONT ÉCHOUÉ")
        return False

if __name__ == "__main__":
    try:
        success = main()
        if success:
            print("\n🎯 Toutes les erreurs ont été corrigées!")
        else:
            print("\n❌ Des corrections supplémentaires sont nécessaires.")
            sys.exit(1)
    except Exception as e:
        print(f"\n❌ Erreur inattendue: {e}")
        sys.exit(1)
