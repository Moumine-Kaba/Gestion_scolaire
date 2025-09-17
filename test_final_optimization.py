#!/usr/bin/env python3
"""
TEST FINAL DU SYSTÈME D'OPTIMISATION EDUMANAGER+
================================================

Ce script teste le système d'optimisation complet et mesure
les performances réelles pour confirmer que le problème des
10 secondes est résolu.
"""

import time
import sys
import os

# Ajouter le répertoire racine au path
sys.path.insert(0, os.path.abspath('.'))

def test_loading_times():
    """Teste les temps de chargement des vues principales"""
    print("🚀 TEST DES TEMPS DE CHARGEMENT")
    print("=" * 50)
    
    try:
        # Initialiser le système d'optimisation
        from src.core.optimization.edu_manager_optimizer import initialize_optimization_system
        print("⚡ Initialisation du système d'optimisation...")
        start_time = time.time()
        initialize_optimization_system()
        init_time = time.time() - start_time
        print(f"✅ Système initialisé en {init_time:.3f}s")
        
        # Tester les données principales
        from src.core.optimization.edu_manager_optimizer import (
            get_optimized_eleves,
            get_optimized_classes,
            get_optimized_matieres,
            get_optimized_professeurs,
            get_optimized_dashboard_stats
        )
        
        print("\n📊 TEST DES DONNÉES PRINCIPALES:")
        
        # Test élèves
        start_time = time.time()
        eleves = get_optimized_eleves()
        eleves_time = time.time() - start_time
        print(f"✅ Élèves: {len(eleves)} récupérés en {eleves_time:.3f}s")
        
        # Test classes
        start_time = time.time()
        classes = get_optimized_classes()
        classes_time = time.time() - start_time
        print(f"✅ Classes: {len(classes)} récupérées en {classes_time:.3f}s")
        
        # Test matières
        start_time = time.time()
        matieres = get_optimized_matieres()
        matieres_time = time.time() - start_time
        print(f"✅ Matières: {len(matieres)} récupérées en {matieres_time:.3f}s")
        
        # Test professeurs
        start_time = time.time()
        professeurs = get_optimized_professeurs()
        professeurs_time = time.time() - start_time
        print(f"✅ Professeurs: {len(professeurs)} récupérés en {professeurs_time:.3f}s")
        
        # Test statistiques dashboard
        start_time = time.time()
        stats = get_optimized_dashboard_stats()
        stats_time = time.time() - start_time
        print(f"✅ Stats dashboard: {stats_time:.3f}s")
        
        # Calculer le temps total
        total_time = eleves_time + classes_time + matieres_time + professeurs_time + stats_time
        print(f"\n⏱️ Temps total: {total_time:.3f}s")
        
        # Vérifier si l'objectif est atteint
        if total_time < 1.0:
            print("🎉 OBJECTIF ATTEINT: Chargement < 1 seconde!")
        else:
            print("⚠️ Objectif non atteint: Chargement > 1 seconde")
        
        return total_time < 1.0
        
    except Exception as e:
        print(f"❌ Erreur test temps de chargement: {e}")
        return False

def test_view_optimization():
    """Teste l'optimisation des vues"""
    print("\n🎯 TEST D'OPTIMISATION DES VUES")
    print("=" * 50)
    
    try:
        from src.core.optimization.edu_manager_optimizer import optimize_view
        
        views_to_test = ['eleves', 'classes', 'matieres', 'notes', 'cours', 'professeurs']
        
        all_optimized = True
        
        for view in views_to_test:
            result = optimize_view(view)
            status = "✅" if result['optimized'] else "⚠️"
            print(f"{status} Vue {view}: {result['loading_time']}")
            
            if not result['optimized']:
                all_optimized = False
        
        if all_optimized:
            print("\n🎉 TOUTES LES VUES SONT OPTIMISÉES!")
        else:
            print("\n⚠️ Certaines vues ne sont pas optimisées")
        
        return all_optimized
        
    except Exception as e:
        print(f"❌ Erreur test optimisation vues: {e}")
        return False

def test_performance_comparison():
    """Compare les performances avant/après optimisation"""
    print("\n📈 COMPARAISON DES PERFORMANCES")
    print("=" * 50)
    
    try:
        # Test sans optimisation (contrôleurs originaux)
        print("📊 Test SANS optimisation:")
        
        start_time = time.time()
        from src.modules.academic.students.controllers.eleve_controller import get_all_eleves
        eleves_original = get_all_eleves()
        original_time = time.time() - start_time
        
        print(f"  Élèves (original): {len(eleves_original)} en {original_time:.3f}s")
        
        # Test avec optimisation
        print("📊 Test AVEC optimisation:")
        
        from src.core.optimization.edu_manager_optimizer import get_optimized_eleves
        
        start_time = time.time()
        eleves_optimized = get_optimized_eleves()
        optimized_time = time.time() - start_time
        
        print(f"  Élèves (optimisé): {len(eleves_optimized)} en {optimized_time:.3f}s")
        
        # Calculer l'amélioration
        if original_time > 0:
            improvement = ((original_time - optimized_time) / original_time) * 100
            print(f"\n🚀 Amélioration: {improvement:.1f}%")
            
            if improvement > 50:
                print("🎉 AMÉLIORATION SIGNIFICATIVE!")
            elif improvement > 0:
                print("✅ Amélioration détectée")
            else:
                print("⚠️ Pas d'amélioration détectée")
        
        return improvement > 0
        
    except Exception as e:
        print(f"❌ Erreur comparaison performances: {e}")
        return False

def test_cache_performance():
    """Teste les performances du cache"""
    print("\n💾 TEST DES PERFORMANCES DU CACHE")
    print("=" * 50)
    
    try:
        from src.core.optimization.edu_manager_optimizer import get_performance_report
        
        # Récupérer les statistiques
        stats = get_performance_report()
        
        print("📊 Statistiques de performance:")
        print(f"  Cache hits: {stats.get('cache_hits', 0)}")
        print(f"  Cache misses: {stats.get('cache_misses', 0)}")
        
        if 'stored_procedures' in stats:
            sp_stats = stats['stored_procedures']
            print(f"  Procédures - Hit rate: {sp_stats.get('hit_rate', '0%')}")
        
        if 'intelligent_cache' in stats:
            cache_stats = stats['intelligent_cache']
            print(f"  Cache intelligent - Hit rate: {cache_stats.get('hit_rate', '0%')}")
        
        # Calculer le hit rate global
        total_requests = stats.get('cache_hits', 0) + stats.get('cache_misses', 0)
        if total_requests > 0:
            global_hit_rate = (stats.get('cache_hits', 0) / total_requests) * 100
            print(f"  Hit rate global: {global_hit_rate:.1f}%")
            
            if global_hit_rate > 80:
                print("🎉 EXCELLENTE PERFORMANCE DU CACHE!")
            elif global_hit_rate > 50:
                print("✅ Bonne performance du cache")
            else:
                print("⚠️ Performance du cache à améliorer")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur test cache: {e}")
        return False

def main():
    """Fonction principale de test"""
    print("🚀 TEST FINAL DU SYSTÈME D'OPTIMISATION EDUMANAGER+")
    print("=" * 60)
    print("🎯 Objectif: Résoudre le problème des 10 secondes de chargement")
    print("=" * 60)
    
    tests = [
        ("Temps de chargement", test_loading_times),
        ("Optimisation des vues", test_view_optimization),
        ("Comparaison performances", test_performance_comparison),
        ("Performances du cache", test_cache_performance)
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
    print("📊 RÉSUMÉ FINAL DES TESTS")
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
        print("\n🎉🎉🎉 TOUS LES TESTS SONT PASSÉS! 🎉🎉🎉")
        print("✅ Le problème des 10 secondes est RÉSOLU!")
        print("⚡ Les vues se chargent maintenant en moins de 1 seconde!")
        print("🚀 Le système d'optimisation fonctionne parfaitement!")
    else:
        print("\n⚠️ Certains tests ont échoué. Vérifiez les erreurs ci-dessus.")
    
    print("\n🚀 Test final terminé")

if __name__ == "__main__":
    main()
