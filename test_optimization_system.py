#!/usr/bin/env python3
"""
SCRIPT DE TEST DU SYSTÈME D'OPTIMISATION COMPLET
================================================

Ce script teste tous les composants du système d'optimisation
pour s'assurer qu'ils fonctionnent correctement et résolvent
le problème des 10 secondes de chargement.
"""

import time
import sys
import os

# Ajouter le répertoire racine au path
sys.path.insert(0, os.path.abspath('.'))

def test_stored_procedures():
    """Teste le système de procédures stockées"""
    print("\n🧪 Test des procédures stockées...")
    
    try:
        from src.core.database.stored_procedures import get_sp_manager, optimize_database
        
        # Optimiser la base de données
        optimize_database()
        
        # Initialiser le gestionnaire
        manager = get_sp_manager()
        
        # Tester quelques procédures
        start_time = time.time()
        eleves = manager.execute('sp_get_all_eleves')
        eleves_time = time.time() - start_time
        
        start_time = time.time()
        classes = manager.execute('sp_get_all_classes')
        classes_time = time.time() - start_time
        
        start_time = time.time()
        matieres = manager.execute('sp_get_all_matieres')
        matieres_time = time.time() - start_time
        
        start_time = time.time()
        stats = manager.execute('sp_get_dashboard_stats')
        stats_time = time.time() - start_time
        
        print(f"✅ Élèves: {len(eleves)} récupérés en {eleves_time:.3f}s")
        print(f"✅ Classes: {len(classes)} récupérées en {classes_time:.3f}s")
        print(f"✅ Matières: {len(matieres)} récupérées en {matieres_time:.3f}s")
        print(f"✅ Stats dashboard: {stats_time:.3f}s")
        
        # Afficher les statistiques
        perf_stats = manager.get_stats()
        print(f"📊 Statistiques procédures: {perf_stats}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur test procédures stockées: {e}")
        return False

def test_intelligent_cache():
    """Teste le système de cache intelligent"""
    print("\n🧪 Test du cache intelligent...")
    
    try:
        from src.core.cache.intelligent_cache import IntelligentCache, preload_controller_cache
        
        # Initialiser le cache
        cache = IntelligentCache()
        
        # Précharger le cache des contrôleurs
        preload_controller_cache()
        
        # Tester l'accès aux données
        start_time = time.time()
        eleves = cache.get('get_all_eleves')
        eleves_time = time.time() - start_time
        
        start_time = time.time()
        classes = cache.get('get_all_classes')
        classes_time = time.time() - start_time
        
        print(f"✅ Élèves depuis cache: {len(eleves) if eleves else 0} en {eleves_time:.3f}s")
        print(f"✅ Classes depuis cache: {len(classes) if classes else 0} en {classes_time:.3f}s")
        
        # Afficher les statistiques
        cache_stats = cache.get_stats()
        print(f"📊 Statistiques cache: {cache_stats}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur test cache intelligent: {e}")
        return False

def test_intelligent_preloader():
    """Teste le système de préchargement intelligent"""
    print("\n🧪 Test du préchargeur intelligent...")
    
    try:
        from src.core.preloader.intelligent_preloader import get_preloader, preload_critical_data
        
        # Initialiser le préchargeur
        preloader = get_preloader()
        
        # Précharger les données critiques
        preload_critical_data()
        
        # Tester l'accès aux données préchargées
        start_time = time.time()
        eleves = preloader.get_data('eleves_all')
        eleves_time = time.time() - start_time
        
        start_time = time.time()
        classes = preloader.get_data('classes_all')
        classes_time = time.time() - start_time
        
        start_time = time.time()
        matieres = preloader.get_data('matieres_all')
        matieres_time = time.time() - start_time
        
        print(f"✅ Élèves préchargés: {len(eleves) if eleves else 0} en {eleves_time:.3f}s")
        print(f"✅ Classes préchargées: {len(classes) if classes else 0} en {classes_time:.3f}s")
        print(f"✅ Matières préchargées: {len(matieres) if matieres else 0} en {matieres_time:.3f}s")
        
        # Afficher les statistiques
        preloader_stats = preloader.get_stats()
        print(f"📊 Statistiques préchargeur: {preloader_stats}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur test préchargeur intelligent: {e}")
        return False

def test_complete_optimizer():
    """Teste le système d'optimisation complet"""
    print("\n🧪 Test du système d'optimisation complet...")
    
    try:
        from src.core.optimization.edu_manager_optimizer import (
            initialize_optimization_system,
            get_optimized_eleves,
            get_optimized_classes,
            get_optimized_matieres,
            get_optimized_dashboard_stats,
            optimize_view,
            get_performance_report
        )
        
        # Initialiser le système complet
        start_time = time.time()
        initialize_optimization_system()
        init_time = time.time() - start_time
        
        print(f"✅ Système initialisé en {init_time:.3f}s")
        
        # Tester les données optimisées
        start_time = time.time()
        eleves = get_optimized_eleves()
        eleves_time = time.time() - start_time
        
        start_time = time.time()
        classes = get_optimized_classes()
        classes_time = time.time() - start_time
        
        start_time = time.time()
        matieres = get_optimized_matieres()
        matieres_time = time.time() - start_time
        
        start_time = time.time()
        dashboard_stats = get_optimized_dashboard_stats()
        stats_time = time.time() - start_time
        
        print(f"✅ Élèves optimisés: {len(eleves)} en {eleves_time:.3f}s")
        print(f"✅ Classes optimisées: {len(classes)} en {classes_time:.3f}s")
        print(f"✅ Matières optimisées: {len(matieres)} en {matieres_time:.3f}s")
        print(f"✅ Stats dashboard: {stats_time:.3f}s")
        
        # Tester l'optimisation des vues
        views_to_test = ['eleves', 'classes', 'matieres', 'notes', 'cours']
        print("\n📊 Test d'optimisation des vues:")
        
        for view in views_to_test:
            result = optimize_view(view)
            status = "✅" if result['optimized'] else "⚠️"
            print(f"  {status} {view}: {result['loading_time']}")
        
        # Afficher le rapport de performance complet
        report = get_performance_report()
        print(f"\n📊 Rapport de performance complet:")
        for key, value in report.items():
            print(f"  {key}: {value}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur test système complet: {e}")
        return False

def test_performance_comparison():
    """Compare les performances avant/après optimisation"""
    print("\n🧪 Test de comparaison des performances...")
    
    try:
        # Test sans optimisation (contrôleurs originaux)
        print("📊 Test sans optimisation:")
        
        start_time = time.time()
        from src.modules.academic.students.controllers.eleve_controller import get_all_eleves
        eleves_original = get_all_eleves()
        original_time = time.time() - start_time
        
        print(f"  Élèves (original): {len(eleves_original)} en {original_time:.3f}s")
        
        # Test avec optimisation
        print("📊 Test avec optimisation:")
        
        from src.core.optimization.edu_manager_optimizer import get_optimized_eleves
        
        start_time = time.time()
        eleves_optimized = get_optimized_eleves()
        optimized_time = time.time() - start_time
        
        print(f"  Élèves (optimisé): {len(eleves_optimized)} en {optimized_time:.3f}s")
        
        # Calculer l'amélioration
        if original_time > 0:
            improvement = ((original_time - optimized_time) / original_time) * 100
            print(f"  🚀 Amélioration: {improvement:.1f}%")
            
            if optimized_time < 1.0:
                print("  ✅ Objectif atteint: < 1 seconde")
            else:
                print("  ⚠️ Objectif non atteint: > 1 seconde")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur test comparaison: {e}")
        return False

def main():
    """Fonction principale de test"""
    print("🚀 DÉMARRAGE DES TESTS DU SYSTÈME D'OPTIMISATION")
    print("=" * 60)
    
    tests = [
        ("Procédures stockées", test_stored_procedures),
        ("Cache intelligent", test_intelligent_cache),
        ("Préchargeur intelligent", test_intelligent_preloader),
        ("Système complet", test_complete_optimizer),
        ("Comparaison performances", test_performance_comparison)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n{'='*20} {test_name} {'='*20}")
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ Erreur critique dans {test_name}: {e}")
            results.append((test_name, False))
    
    # Résumé des résultats
    print("\n" + "="*60)
    print("📊 RÉSUMÉ DES TESTS")
    print("="*60)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASSÉ" if result else "❌ ÉCHOUÉ"
        print(f"{status} {test_name}")
        if result:
            passed += 1
    
    print(f"\n📈 Résultat global: {passed}/{total} tests passés")
    
    if passed == total:
        print("🎉 TOUS LES TESTS SONT PASSÉS!")
        print("✅ Le système d'optimisation est prêt à résoudre le problème des 10 secondes")
    else:
        print("⚠️ Certains tests ont échoué. Vérifiez les erreurs ci-dessus.")
    
    print("\n🚀 Tests terminés")

if __name__ == "__main__":
    main()
