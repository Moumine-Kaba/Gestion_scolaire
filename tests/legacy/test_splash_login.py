#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test de la vue Splash + Login combinée
Vérifie le bon fonctionnement de l'interface
"""

import sys
import os
import time
import threading

# Ajouter le répertoire racine au path Python
project_root = os.path.abspath(os.path.dirname(__file__))
if project_root not in sys.path:
    sys.path.append(project_root)

def test_splash_login_view():
    """Test de la vue SplashLoginView."""
    try:
        print("🧪 Test de SplashLoginView...")
        
        # Test d'import
        from views.splash_login_view import SplashLoginView
        print("✅ Import réussi")
        
        # Test de création d'instance
        app = SplashLoginView()
        print("✅ Instance créée avec succès")
        
        # Test des composants UI
        assert hasattr(app, 'splash_frame'), "Splash frame manquant"
        assert hasattr(app, 'login_frame'), "Login frame manquant"
        assert hasattr(app, 'username_entry'), "Champ username manquant"
        assert hasattr(app, 'password_entry'), "Champ password manquant"
        assert hasattr(app, 'login_button'), "Bouton login manquant"
        print("✅ Tous les composants UI sont présents")
        
        # Test des variables
        assert hasattr(app, 'username_var'), "Variable username manquante"
        assert hasattr(app, 'password_var'), "Variable password manquante"
        assert hasattr(app, 'remember_var'), "Variable remember manquante"
        print("✅ Toutes les variables sont présentes")
        
        # Test des méthodes
        assert hasattr(app, 'login'), "Méthode login manquante"
        assert hasattr(app, '_switch_to_login'), "Méthode switch_to_login manquante"
        print("✅ Toutes les méthodes principales sont présentes")
        
        # Fermer l'application
        app.destroy()
        print("✅ Test terminé avec succès")
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors du test: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_ui_components():
    """Test des composants UI individuels."""
    try:
        print("🧪 Test des composants UI...")
        
        from views.splash_login_view import SplashLoginView
        app = SplashLoginView()
        
        # Test du splash frame
        splash_visible = app.splash_frame.winfo_viewable()
        print(f"✅ Splash frame visible: {splash_visible}")
        
        # Test du login frame (doit être caché initialement)
        login_visible = app.login_frame.winfo_viewable()
        print(f"✅ Login frame visible: {login_visible}")
        
        # Test des champs de saisie
        username_placeholder = app.username_entry.cget("placeholder_text")
        password_show = app.password_entry.cget("show")
        print(f"✅ Username placeholder: {username_placeholder}")
        print(f"✅ Password show: {password_show}")
        
        # Test du bouton
        button_text = app.login_button.cget("text")
        print(f"✅ Bouton text: {button_text}")
        
        app.destroy()
        print("✅ Test des composants UI terminé")
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors du test UI: {e}")
        return False

def test_theme_and_colors():
    """Test du thème et des couleurs."""
    try:
        print("🧪 Test du thème et des couleurs...")
        
        from views.splash_login_view import (
            BG_MAIN, GLASS_BG, GLASS_TINT, BORDER, 
            TEXT, SUBTEXT, ACCENT, PRIMARY, PRIMARY_HOVER
        )
        
        # Vérifier que toutes les couleurs sont définies
        colors = [BG_MAIN, GLASS_BG, GLASS_TINT, BORDER, TEXT, SUBTEXT, ACCENT, PRIMARY, PRIMARY_HOVER]
        for color in colors:
            assert color.startswith('#'), f"Couleur invalide: {color}"
            assert len(color) == 7, f"Format couleur invalide: {color}"
        
        print("✅ Toutes les couleurs sont valides")
        
        # Vérifier que les couleurs sont différentes
        unique_colors = set(colors)
        assert len(unique_colors) == len(colors), "Couleurs dupliquées détectées"
        print("✅ Toutes les couleurs sont uniques")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors du test des couleurs: {e}")
        return False

def main():
    """Fonction principale de test."""
    print("🚀 Démarrage des tests de SplashLoginView...")
    print("=" * 50)
    
    tests = [
        ("Test de la vue principale", test_splash_login_view),
        ("Test des composants UI", test_ui_components),
        ("Test du thème et couleurs", test_theme_and_colors),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n🔍 {test_name}")
        print("-" * 30)
        if test_func():
            passed += 1
            print(f"✅ {test_name} - RÉUSSI")
        else:
            print(f"❌ {test_name} - ÉCHEC")
    
    print("\n" + "=" * 50)
    print(f"📊 Résultats: {passed}/{total} tests réussis")
    
    if passed == total:
        print("🎉 Tous les tests sont passés avec succès !")
        return True
    else:
        print("⚠️ Certains tests ont échoué")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
