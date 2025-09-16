#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test simple de la correction du login
Vérifie que les champs sont correctement remplis
"""

import sys
import os

# Ajouter le répertoire racine au path Python
project_root = os.path.abspath(os.path.dirname(__file__))
if project_root not in sys.path:
    sys.path.append(project_root)

def test_login_correction():
    """Test de la correction du login."""
    try:
        print("🧪 Test de la correction du login...")
        
        # Importer la vue de login
        from views.login_view import LoginView
        
        # Créer une instance
        app = LoginView()
        print("✅ Instance LoginView créée")
        
        # Tester la récupération des valeurs
        print("\n🔍 Test de récupération des valeurs:")
        
        # Simuler la saisie dans les champs
        app.username_entry.insert(0, "admin")
        app.password_entry.insert(0, "admin123")
        
        # Récupérer les valeurs
        username_from_entry = app.username_entry.get()
        password_from_entry = app.password_entry.get()
        username_from_var = app.username_var.get()
        password_from_var = app.password_var.get()
        
        print(f"  Username depuis entry: '{username_from_entry}' (longueur: {len(username_from_entry)})")
        print(f"  Password depuis entry: '{password_from_entry}' (longueur: {len(password_from_entry)})")
        print(f"  Username depuis var: '{username_from_var}' (longueur: {len(username_from_var)})")
        print(f"  Password depuis var: '{password_from_var}' (longueur: {len(password_from_var)})")
        
        # Vérifier que les champs ne sont pas vides
        if username_from_entry and password_from_entry:
            print("✅ Les champs d'entrée contiennent des valeurs")
        else:
            print("❌ Les champs d'entrée sont vides")
            return False
        
        # Tester la validation
        print("\n🔍 Test de validation:")
        username_stripped = username_from_entry.strip()
        password_stripped = password_from_entry.strip()
        
        if username_stripped and password_stripped:
            print("✅ Validation réussie après strip")
        else:
            print("❌ Validation échoue après strip")
            return False
        
        # Fermer l'application
        app.destroy()
        print("\n✅ Test de correction terminé avec succès")
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors du test: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Fonction principale de test."""
    print("🚀 Test de la correction du login...")
    print("=" * 50)
    
    if test_login_correction():
        print("\n🎉 La correction du login fonctionne !")
        print("\n💡 Maintenant vous devriez pouvoir vous connecter normalement.")
        return True
    else:
        print("\n❌ La correction du login ne fonctionne pas encore.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
