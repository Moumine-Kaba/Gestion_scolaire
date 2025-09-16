#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test de la Nouvelle Architecture
================================

Script simple pour tester que la nouvelle architecture fonctionne.
"""

import os
import sys
from pathlib import Path

def test_imports():
    """Teste les imports de la nouvelle architecture"""
    print("🧪 Test des imports de la nouvelle architecture...")
    
    try:
        # Test du module core
        from src.core.config import get_config
        print("✅ Module core.config importé avec succès")
        
        # Test de la configuration
        config = get_config()
        print(f"✅ Configuration chargée: {config.app_name} v{config.version}")
        
        return True
        
    except ImportError as e:
        print(f"❌ Erreur d'import: {e}")
        return False
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False

def test_structure():
    """Teste la structure des dossiers"""
    print("\n📁 Test de la structure des dossiers...")
    
    required_dirs = [
        "src",
        "src/core",
        "src/modules",
        "src/modules/auth",
        "src/shared",
        "src/utils",
        "tests",
        "config",
        "scripts",
        "docs",
        "resources",
        "deployment"
    ]
    
    missing_dirs = []
    
    for dir_path in required_dirs:
        if not Path(dir_path).exists():
            missing_dirs.append(dir_path)
        else:
            print(f"✅ {dir_path}")
    
    if missing_dirs:
        print(f"❌ Dossiers manquants: {missing_dirs}")
        return False
    
    return True

def test_files():
    """Teste l'existence des fichiers clés"""
    print("\n📄 Test des fichiers clés...")
    
    required_files = [
        "src/core/app.py",
        "src/core/config.py",
        "src/core/exceptions.py",
        "src/modules/auth/__init__.py",
        "scripts/start_app.py",
        "tests/conftest.py",
        "deployment/requirements/requirements.txt"
    ]
    
    missing_files = []
    
    for file_path in required_files:
        if not Path(file_path).exists():
            missing_files.append(file_path)
        else:
            print(f"✅ {file_path}")
    
    if missing_files:
        print(f"❌ Fichiers manquants: {missing_files}")
        return False
    
    return True

def main():
    """Fonction principale de test"""
    print("🏗️  Test de la Nouvelle Architecture EduManager+")
    print("=" * 60)
    
    # Tests
    tests = [
        ("Structure des dossiers", test_structure),
        ("Fichiers clés", test_files),
        ("Imports", test_imports)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n🔍 {test_name}...")
        result = test_func()
        results.append((test_name, result))
    
    # Résumé
    print("\n" + "=" * 60)
    print("📊 Résumé des tests:")
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASSÉ" if result else "❌ ÉCHOUÉ"
        print(f"  - {test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\n🎯 Résultat: {passed}/{total} tests passés")
    
    if passed == total:
        print("\n🎉 Tous les tests sont passés!")
        print("   La nouvelle architecture est prête à être utilisée.")
        print("\n   Pour démarrer l'application:")
        print("   python scripts/start_app.py")
    else:
        print(f"\n⚠️  {total - passed} test(s) ont échoué.")
        print("   Vérifiez la structure et corrigez les problèmes.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

