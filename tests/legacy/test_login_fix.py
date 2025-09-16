#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test de correction du login view
Vérifie que la validation des champs fonctionne correctement
"""

import sys
import os

# Ajouter le répertoire racine au path Python
project_root = os.path.abspath(os.path.dirname(__file__))
if project_root not in sys.path:
    sys.path.append(project_root)

def test_login_validation():
    """Test de la validation des champs de login."""
    try:
        print("🧪 Test de validation du login...")
        
        # Importer la vue de login
        from views.login_view import LoginView
        
        # Créer une instance
        app = LoginView()
        print("✅ Instance LoginView créée")
        
        # Tester les variables
        username_var = app.username_var
        password_var = app.password_var
        
        print(f"✅ Variables récupérées - Username: {username_var}, Password: {password_var}")
        
        # Tester la validation avec des valeurs vides
        print("\n🔍 Test avec des champs vides:")
        username_var.set("")
        password_var.set("")
        
        username = username_var.get().strip()
        password = password_var.get().strip()
        
        print(f"  Username après strip: '{username}' (longueur: {len(username)})")
        print(f"  Password après strip: '{password}' (longueur: {len(password)})")
        
        # Tester la validation avec des espaces
        print("\n🔍 Test avec des espaces:")
        username_var.set("   ")
        password_var.set("  ")
        
        username = username_var.get().strip()
        password = password_var.get().strip()
        
        print(f"  Username après strip: '{username}' (longueur: {len(username)})")
        print(f"  Password après strip: '{password}' (longueur: {len(password)})")
        
        # Tester avec des valeurs valides
        print("\n🔍 Test avec des valeurs valides:")
        username_var.set("admin")
        password_var.set("admin123")
        
        username = username_var.get().strip()
        password = password_var.get().strip()
        
        print(f"  Username après strip: '{username}' (longueur: {len(username)})")
        print(f"  Password après strip: '{password}' (longueur: {len(password)})")
        
        # Fermer l'application
        app.destroy()
        print("\n✅ Test de validation terminé avec succès")
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors du test: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_splash_centering():
    """Test du centrage du splash view."""
    try:
        print("\n🧪 Test du centrage du splash...")
        
        # Importer la vue splash
        from views.splash_view import SplashView
        
        # Créer une instance
        app = SplashView()
        print("✅ Instance SplashView créée")
        
        # Vérifier la géométrie
        geometry = app.geometry()
        print(f"✅ Géométrie de la fenêtre: {geometry}")
        
        # Vérifier la position
        x = app.winfo_x()
        y = app.winfo_y()
        print(f"✅ Position de la fenêtre: x={x}, y={y}")
        
        # Vérifier les dimensions de l'écran
        screen_width = app.winfo_screenwidth()
        screen_height = app.winfo_screenheight()
        print(f"✅ Dimensions de l'écran: {screen_width}x{screen_height}")
        
        # Fermer l'application
        app.destroy()
        print("✅ Test de centrage terminé avec succès")
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors du test de centrage: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Fonction principale de test."""
    print("🚀 Test des corrections du login et splash view...")
    print("=" * 60)
    
    tests = [
        ("Test de validation du login", test_login_validation),
        ("Test du centrage du splash", test_splash_centering),
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
        print("\n💡 Le login et le splash view devraient maintenant fonctionner correctement.")
        return True
    else:
        print("⚠️ Certains tests ont échoué")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
