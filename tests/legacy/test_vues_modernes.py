#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test des Vues Modernisées - EduManager+
Vérifie que les vues Bulletins, Utilisateurs, Enseignements et Classes fonctionnent
"""
import os
import sys
import customtkinter as ctk

def test_vue_bulletins():
    """Test de la vue Bulletins"""
    print("🔍 Test de la vue Bulletins...")
    try:
        from views.bulletins_view import BulletinsView
        
        # Créer une fenêtre de test
        root = ctk.CTk()
        root.withdraw()  # Cacher la fenêtre
        
        # Créer la vue
        vue = BulletinsView(root, {})
        print("✅ BulletinsView créée avec succès")
        
        # Vérifier les attributs essentiels
        assert hasattr(vue, 'tree'), "Vue doit avoir un tableau"
        assert hasattr(vue, 'search_entry'), "Vue doit avoir une barre de recherche"
        assert hasattr(vue, 'stats_labels'), "Vue doit avoir des statistiques"
        
        root.destroy()
        return True
        
    except Exception as e:
        print(f"❌ Erreur BulletinsView: {e}")
        return False

def test_vue_utilisateurs():
    """Test de la vue Utilisateurs"""
    print("🔍 Test de la vue Utilisateurs...")
    try:
        from views.utilisateurs_view import UtilisateursView
        
        # Créer une fenêtre de test
        root = ctk.CTk()
        root.withdraw()  # Cacher la fenêtre
        
        # Créer la vue
        vue = UtilisateursView(root, {})
        print("✅ UtilisateursView créée avec succès")
        
        # Vérifier les attributs essentiels
        assert hasattr(vue, 'tree'), "Vue doit avoir un tableau"
        assert hasattr(vue, 'search_entry'), "Vue doit avoir une barre de recherche"
        assert hasattr(vue, 'stats_labels'), "Vue doit avoir des statistiques"
        
        root.destroy()
        return True
        
    except Exception as e:
        print(f"❌ Erreur UtilisateursView: {e}")
        return False

def test_vue_enseignements():
    """Test de la vue Enseignements"""
    print("🔍 Test de la vue Enseignements...")
    try:
        from views.enseignements_view import EnseignementsView
        
        # Créer une fenêtre de test
        root = ctk.CTk()
        root.withdraw()  # Cacher la fenêtre
        
        # Créer la vue
        vue = EnseignementsView(root, {})
        print("✅ EnseignementsView créée avec succès")
        
        # Vérifier les attributs essentiels
        assert hasattr(vue, 'tree'), "Vue doit avoir un tableau"
        assert hasattr(vue, 'search_entry'), "Vue doit avoir une barre de recherche"
        assert hasattr(vue, 'stats_labels'), "Vue doit avoir des statistiques"
        
        root.destroy()
        return True
        
    except Exception as e:
        print(f"❌ Erreur EnseignementsView: {e}")
        return False

def test_vue_classes():
    """Test de la vue Classes"""
    print("🔍 Test de la vue Classes...")
    try:
        from views.classes_view import ClassesManagerView
        
        # Créer une fenêtre de test
        root = ctk.CTk()
        root.withdraw()  # Cacher la fenêtre
        
        # Créer la vue
        vue = ClassesManagerView(root, {})
        print("✅ ClassesManagerView créée avec succès")
        
        # Vérifier les attributs essentiels
        assert hasattr(vue, 'tree'), "Vue doit avoir un tableau"
        assert hasattr(vue, 'search_entry'), "Vue doit avoir une barre de recherche"
        assert hasattr(vue, 'stats_labels'), "Vue doit avoir des statistiques"
        
        root.destroy()
        return True
        
    except Exception as e:
        print(f"❌ Erreur ClassesManagerView: {e}")
        return False

def main():
    """Test principal des vues modernisées"""
    print("🧪 TEST DES VUES MODERNISÉES EDUMANAGER+")
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
    print("📊 RÉSULTATS DES TESTS DES VUES")
    print("=" * 60)
    
    passed = 0
    for vue_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} {vue_name}")
        if result:
            passed += 1
    
    print(f"\n🎯 Résultat: {passed}/{len(results)} vues fonctionnent")
    
    if passed == len(results):
        print("🎉 Toutes les vues modernisées fonctionnent parfaitement !")
        print("💡 Vous pouvez maintenant lancer l'application avec: python main.py")
    else:
        print("⚠️  Certaines vues ont encore des problèmes.")
        print("💡 Vérifiez les erreurs ci-dessus et corrigez-les")
    
    return passed == len(results)

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
