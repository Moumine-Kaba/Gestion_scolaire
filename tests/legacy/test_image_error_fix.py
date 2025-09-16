#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test de correction de l'erreur 'pyimage3 doesn't exist'
Vérifie que la transition entre login et dashboard fonctionne sans erreur d'image
"""

import sys
import os
import time

# Ajouter le répertoire racine au path Python
project_root = os.path.abspath(os.path.dirname(__file__))
if project_root not in sys.path:
    sys.path.append(project_root)

def test_image_error_fix():
    """Test de la correction de l'erreur d'image"""
    print("🧪 Test de la correction de l'erreur d'image...")
    print("=" * 50)
    
    try:
        # Importer les vues nécessaires
        from views.login_view import LoginView
        print("✅ Import LoginView réussi")
        
        # Créer une instance de LoginView
        login_app = LoginView()
        print("✅ Instance LoginView créée")
        
        # Vérifier que les méthodes de nettoyage sont présentes
        if hasattr(login_app, '_cleanup_images'):
            print("✅ Méthode _cleanup_images présente")
        else:
            print("❌ Méthode _cleanup_images manquante")
            return False
        
        if hasattr(login_app, '_transition_to_dashboard'):
            print("✅ Méthode _transition_to_dashboard présente")
        else:
            print("❌ Méthode _transition_to_dashboard manquante")
            return False
        
        if hasattr(login_app, '_create_dashboard'):
            print("✅ Méthode _create_dashboard présente")
        else:
            print("❌ Méthode _create_dashboard manquante")
            return False
        
        # Tester la méthode de nettoyage
        print("\n🧹 Test de la méthode de nettoyage...")
        try:
            login_app._cleanup_images()
            print("✅ Méthode de nettoyage fonctionne")
        except Exception as e:
            print(f"❌ Erreur dans la méthode de nettoyage: {e}")
            return False
        
        # Fermer l'application
        login_app.destroy()
        print("✅ Application fermée proprement")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors du test: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_image_cache_robustness():
    """Test de la robustesse du cache d'images"""
    print("\n🖼️ Test de la robustesse du cache d'images...")
    print("=" * 50)
    
    try:
        from views.login_view import _ctk_from_pil, _CTK_CACHE
        from PIL import Image
        
        # Créer une image de test
        test_image = Image.new('RGB', (100, 100), color='red')
        
        # Tester la création d'image CTk
        ctk_image = _ctk_from_pil("test", test_image, (50, 50))
        
        if ctk_image is not None:
            print("✅ Création d'image CTk réussie")
        else:
            print("❌ Échec création d'image CTk")
            return False
        
        # Vérifier le cache
        if len(_CTK_CACHE) > 0:
            print("✅ Image mise en cache")
        else:
            print("❌ Image non mise en cache")
            return False
        
        # Tester la récupération depuis le cache
        cached_image = _ctk_from_pil("test", test_image, (50, 50))
        
        if cached_image is not None:
            print("✅ Récupération depuis le cache réussie")
        else:
            print("❌ Échec récupération depuis le cache")
            return False
        
        # Nettoyer le cache
        _CTK_CACHE.clear()
        print("✅ Cache nettoyé")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors du test du cache: {e}")
        return False

def main():
    """Fonction principale de test"""
    print("🚀 Test de la correction de l'erreur 'pyimage3 doesn't exist'")
    print("=" * 60)
    
    tests = [
        ("Test de correction de l'erreur d'image", test_image_error_fix),
        ("Test de robustesse du cache d'images", test_image_cache_robustness),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n🔍 {test_name}")
        print("-" * 40)
        if test_func():
            passed += 1
            print(f"✅ {test_name} - RÉUSSI")
        else:
            print(f"❌ {test_name} - ÉCHEC")
    
    print("\n" + "=" * 60)
    print(f"📊 Résultats: {passed}/{total} tests réussis")
    
    if passed == total:
        print("🎉 Tous les tests sont passés avec succès !")
        print("💡 L'erreur 'pyimage3 doesn't exist' devrait être corrigée")
        return True
    else:
        print("⚠️ Certains tests ont échoué")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
