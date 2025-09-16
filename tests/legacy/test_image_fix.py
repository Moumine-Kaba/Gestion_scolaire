#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test de la correction des images dans le login view
Vérifie que les erreurs d'images sont gérées correctement
"""

import sys
import os

# Ajouter le répertoire racine au path Python
project_root = os.path.abspath(os.path.dirname(__file__))
if project_root not in sys.path:
    sys.path.append(project_root)

def test_image_handling():
    """Test de la gestion des images."""
    try:
        print("🧪 Test de la gestion des images...")
        
        # Importer la vue de login
        from views.login_view import LoginView
        
        # Créer une instance
        app = LoginView()
        print("✅ Instance LoginView créée")
        
        # Vérifier que les composants sont créés sans erreur
        print("\n🔍 Vérification des composants:")
        
        # Vérifier les champs d'entrée
        if hasattr(app, 'username_entry') and app.username_entry:
            print("✅ Champ username créé")
        else:
            print("❌ Champ username manquant")
            return False
        
        if hasattr(app, 'password_entry') and app.password_entry:
            print("✅ Champ password créé")
        else:
            print("❌ Champ password manquant")
            return False
        
        # Vérifier le bouton de login
        if hasattr(app, 'login_button') and app.login_button:
            print("✅ Bouton login créé")
        else:
            print("❌ Bouton login manquant")
            return False
        
        # Vérifier le bouton de l'œil
        if hasattr(app, '_eye_btn') and app._eye_btn:
            print("✅ Bouton œil créé")
        else:
            print("❌ Bouton œil manquant")
            return False
        
        # Tester la saisie dans les champs
        print("\n🔍 Test de saisie dans les champs:")
        
        # Simuler la saisie
        app.username_entry.insert(0, "test_user")
        app.password_entry.insert(0, "test_pass")
        
        # Vérifier les valeurs
        username = app.username_entry.get()
        password = app.password_entry.get()
        
        if username == "test_user" and password == "test_pass":
            print("✅ Saisie dans les champs fonctionne")
        else:
            print("❌ Saisie dans les champs ne fonctionne pas")
            return False
        
        # Fermer l'application
        app.destroy()
        print("\n✅ Test de gestion des images terminé avec succès")
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors du test: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Fonction principale de test."""
    print("🚀 Test de la correction des images dans le login view...")
    print("=" * 60)
    
    if test_image_handling():
        print("\n🎉 La correction des images fonctionne !")
        print("\n💡 Les erreurs 'pyimage3 doesn't exist' devraient maintenant être évitées.")
        return True
    else:
        print("\n❌ La correction des images ne fonctionne pas encore.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
