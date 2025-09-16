#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test des Vues Restaurées - EduManager+
Vérifie que les vues Bulletins, Utilisateurs, Enseignements et Classes ont été restaurées
"""
import os
import sys
import tkinter as tk

def test_vue_bulletins():
    """Test de la vue Bulletins restaurée"""
    print("🔍 Test de la vue Bulletins (restaurée)...")
    try:
        from views.bulletins_view import BulletinsView
        
        # Créer une fenêtre de test
        root = tk.Tk()
        root.withdraw()  # Cacher la fenêtre
        
        # Créer la vue
        vue = BulletinsView(root)
        print("✅ BulletinsView restaurée avec succès")
        
        # Vérifier les attributs essentiels
        assert hasattr(vue, 'tree'), "Vue doit avoir un tableau"
        assert hasattr(vue, 'charger_bulletins'), "Vue doit avoir la méthode charger_bulletins"
        assert hasattr(vue, 'ajouter_bulletin'), "Vue doit avoir la méthode ajouter_bulletin"
        
        root.destroy()
        return True
        
    except Exception as e:
        print(f"❌ Erreur BulletinsView: {e}")
        return False

def test_vue_utilisateurs():
    """Test de la vue Utilisateurs restaurée"""
    print("🔍 Test de la vue Utilisateurs (restaurée)...")
    try:
        from views.utilisateurs_view import UtilisateursView
        
        # Créer une fenêtre de test
        root = tk.Tk()
        root.withdraw()  # Cacher la fenêtre
        
        # Créer la vue
        vue = UtilisateursView(root)
        print("✅ UtilisateursView restaurée avec succès")
        
        # Vérifier les attributs essentiels
        assert hasattr(vue, 'tree'), "Vue doit avoir un tableau"
        assert hasattr(vue, 'charger_users'), "Vue doit avoir la méthode charger_users"
        assert hasattr(vue, 'ajouter_user'), "Vue doit avoir la méthode ajouter_user"
        
        root.destroy()
        return True
        
    except Exception as e:
        print(f"❌ Erreur UtilisateursView: {e}")
        return False

def test_vue_enseignements():
    """Test de la vue Enseignements restaurée"""
    print("🔍 Test de la vue Enseignements (restaurée)...")
    try:
        from views.enseignements_view import EnseignementsView
        
        # Créer une fenêtre de test
        root = tk.Tk()
        root.withdraw()  # Cacher la fenêtre
        
        # Créer la vue
        vue = EnseignementsView(root)
        print("✅ EnseignementsView restaurée avec succès")
        
        # Vérifier les attributs essentiels
        assert hasattr(vue, 'tree'), "Vue doit avoir un tableau"
        assert hasattr(vue, 'charger_enseignements'), "Vue doit avoir la méthode charger_enseignements"
        assert hasattr(vue, 'ajouter_enseignement'), "Vue doit avoir la méthode ajouter_enseignement"
        
        root.destroy()
        return True
        
    except Exception as e:
        print(f"❌ Erreur EnseignementsView: {e}")
        return False

def test_vue_classes():
    """Test de la vue Classes restaurée"""
    print("🔍 Test de la vue Classes (restaurée)...")
    try:
        from views.classes_view import ClassesManagerView
        
        # Créer une fenêtre de test
        root = tk.Tk()
        root.withdraw()  # Cacher la fenêtre
        
        # Créer la vue
        vue = ClassesManagerView(root)
        print("✅ ClassesManagerView restaurée avec succès")
        
        # Vérifier les attributs essentiels
        assert hasattr(vue, 'tree'), "Vue doit avoir un tableau"
        assert hasattr(vue, 'charger_classes'), "Vue doit avoir la méthode charger_classes"
        assert hasattr(vue, 'ajouter_classe'), "Vue doit avoir la méthode ajouter_classe"
        
        root.destroy()
        return True
        
    except Exception as e:
        print(f"❌ Erreur ClassesManagerView: {e}")
        return False

def main():
    """Test principal des vues restaurées"""
    print("🧪 TEST DES VUES RESTAURÉES EDUMANAGER+")
    print("=" * 60)

    tests = [
        ("Bulletins", test_vue_bulletins),
        ("Utilisateurs", test_vue_utilisateurs),
        ("Enseignements", test_vue_enseignements),
        ("Classes", test_vue_classes)
    ]

    results = []
    for vue_name, test_func in tests:
        print(f"\n📋 Test de la vue {vue_name}")
        try:
            result = test_func()
            results.append((vue_name, result))
        except Exception as e:
            print(f"❌ Erreur lors du test: {e}")
            results.append((vue_name, False))

    # Résumé
    print("\n" + "=" * 60)
    print("📊 RÉSULTATS DES TESTS DES VUES RESTAURÉES")
    print("=" * 60)

    passed = 0
    for vue_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} {vue_name}")
        if result:
            passed += 1

    print(f"\n🎯 Résultat: {passed}/{len(results)} vues restaurées fonctionnent")

    if passed == len(results):
        print("🎉 Toutes les vues ont été restaurées avec succès !")
        print("💡 Vous pouvez maintenant lancer l'application avec: python main.py")
    else:
        print("⚠️  Certaines vues ont encore des problèmes.")
        print("💡 Vérifiez les erreurs ci-dessus et corrigez-les")

    return passed == len(results)

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
