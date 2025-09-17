#!/usr/bin/env python3
"""
TEST SIMPLE ET DIRECT DU SYSTÈME D'OPTIMISATION
===============================================

Test rapide pour vérifier que le système d'optimisation fonctionne
et résout le problème des 10 secondes de chargement.
"""

import time
import sys
import os

# Ajouter le répertoire racine au path
sys.path.insert(0, os.path.abspath('.'))

def test_simple_performance():
    """Test simple des performances"""
    print("🚀 TEST SIMPLE DES PERFORMANCES")
    print("=" * 40)
    
    try:
        # Test 1: Contrôleurs originaux
        print("📊 Test SANS optimisation:")
        start_time = time.time()
        
        from src.modules.academic.students.controllers.eleve_controller import get_all_eleves
        eleves_original = get_all_eleves()
        original_time = time.time() - start_time
        
        print(f"✅ Élèves (original): {len(eleves_original)} en {original_time:.3f}s")
        
        # Test 2: Avec optimisation
        print("\n📊 Test AVEC optimisation:")
        start_time = time.time()
        
        from src.core.optimization.edu_manager_optimizer import get_optimized_eleves
        eleves_optimized = get_optimized_eleves()
        optimized_time = time.time() - start_time
        
        print(f"✅ Élèves (optimisé): {len(eleves_optimized)} en {optimized_time:.3f}s")
        
        # Calculer l'amélioration
        if original_time > 0:
            improvement = ((original_time - optimized_time) / original_time) * 100
            print(f"\n🚀 Amélioration: {improvement:.1f}%")
            
            if optimized_time < 1.0:
                print("🎉 OBJECTIF ATTEINT: < 1 seconde!")
            else:
                print("⚠️ Objectif non atteint: > 1 seconde")
        
        return optimized_time < 1.0
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False

def test_cache_system():
    """Test du système de cache"""
    print("\n💾 TEST DU SYSTÈME DE CACHE")
    print("=" * 40)
    
    try:
        from src.core.cache.intelligent_cache import IntelligentCache
        
        cache = IntelligentCache()
        
        # Test cache mémoire
        start_time = time.time()
        eleves_cached = cache.get('get_all_eleves')
        cache_time = time.time() - start_time
        
        if eleves_cached:
            print(f"✅ Cache hit: {len(eleves_cached)} élèves en {cache_time:.3f}s")
            print("🎉 Cache fonctionne parfaitement!")
            return True
        else:
            print("⚠️ Cache miss")
            return False
            
    except Exception as e:
        print(f"❌ Erreur cache: {e}")
        return False

def test_stored_procedures():
    """Test des procédures stockées"""
    print("\n⚡ TEST DES PROCÉDURES STOCKÉES")
    print("=" * 40)
    
    try:
        from src.core.database.stored_procedures import get_sp_manager
        
        manager = get_sp_manager()
        
        # Test procédure élèves
        start_time = time.time()
        eleves_sp = manager.execute('sp_get_all_eleves')
        sp_time = time.time() - start_time
        
        print(f"✅ Procédure élèves: {len(eleves_sp)} en {sp_time:.3f}s")
        
        # Test procédure classes
        start_time = time.time()
        classes_sp = manager.execute('sp_get_all_classes')
        sp_time = time.time() - start_time
        
        print(f"✅ Procédure classes: {len(classes_sp)} en {sp_time:.3f}s")
        
        print("🎉 Procédures stockées fonctionnent!")
        return True
        
    except Exception as e:
        print(f"❌ Erreur procédures: {e}")
        return False

def main():
    """Fonction principale"""
    print("🚀 TEST SIMPLE DU SYSTÈME D'OPTIMISATION")
    print("=" * 50)
    
    tests = [
        ("Performances", test_simple_performance),
        ("Cache", test_cache_system),
        ("Procédures stockées", test_stored_procedures)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ Erreur dans {test_name}: {e}")
            results.append((test_name, False))
    
    # Résumé
    print("\n" + "="*50)
    print("📊 RÉSUMÉ")
    print("="*50)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅" if result else "❌"
        print(f"{status} {test_name}")
    
    print(f"\n📈 {passed}/{total} tests passés")
    
    if passed == total:
        print("\n🎉 SYSTÈME D'OPTIMISATION FONCTIONNEL!")
        print("✅ Le problème des 10 secondes est RÉSOLU!")
    else:
        print("\n⚠️ Certains tests ont échoué")

if __name__ == "__main__":
    main()
