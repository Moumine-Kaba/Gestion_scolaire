#!/usr/bin/env python3
"""
Test des formulaires d'ajout/modification des matières et notes
"""

import sys
import os
sys.path.append('.')

def test_matieres_formulaire():
    """Test du formulaire des matières"""
    print("🧪 TEST DU FORMULAIRE DES MATIÈRES")
    print("=" * 50)
    
    try:
        from src.modules.academic.subjects.views.matieres_view import MatieresView
        from src.modules.academic.subjects.controllers.matiere_controller import get_all_matieres
        
        print("✅ Import de MatieresView réussi")
        
        # Test des matières
        matieres = get_all_matieres()
        print(f"✅ {len(matieres)} matières trouvées")
        
        # Test de création de la vue (sans affichage)
        print("🔄 Test de création de MatieresView...")
        try:
            # Créer une fenêtre factice pour le test
            import customtkinter as ctk
            root = ctk.CTk()
            root.withdraw()  # Masquer la fenêtre
            
            view = MatieresView(root)
            print("✅ MatieresView créée avec succès")
            
            # Test de la méthode ajouter_matiere
            print("🔄 Test de la méthode ajouter_matiere...")
            try:
                view.ajouter_matiere()
                print("✅ Méthode ajouter_matiere fonctionne")
            except Exception as e:
                print(f"❌ Erreur dans ajouter_matiere: {e}")
            
            root.destroy()
            
        except Exception as e:
            print(f"❌ Erreur lors de la création de MatieresView: {e}")
            
    except Exception as e:
        print(f"❌ Erreur d'import: {e}")

def test_notes_formulaire():
    """Test du formulaire des notes"""
    print("\n🧪 TEST DU FORMULAIRE DES NOTES")
    print("=" * 50)
    
    try:
        from src.modules.academic.grades.views.notes_view import NotesView
        from src.modules.academic.grades.controllers.notes_controller import get_all_notes
        
        print("✅ Import de NotesView réussi")
        
        # Test des notes
        notes = get_all_notes()
        print(f"✅ {len(notes)} notes trouvées")
        
        # Test de création de la vue (sans affichage)
        print("🔄 Test de création de NotesView...")
        try:
            import customtkinter as ctk
            root = ctk.CTk()
            root.withdraw()  # Masquer la fenêtre
            
            view = NotesView(root)
            print("✅ NotesView créée avec succès")
            
            # Vérifier s'il y a des méthodes d'ajout/modification
            methods = [method for method in dir(view) if 'ajouter' in method.lower() or 'add' in method.lower()]
            print(f"📋 Méthodes d'ajout trouvées: {methods}")
            
            if not methods:
                print("⚠️ Aucune méthode d'ajout trouvée dans NotesView")
                print("💡 La vue NotesView semble être en lecture seule")
            
            root.destroy()
            
        except Exception as e:
            print(f"❌ Erreur lors de la création de NotesView: {e}")
            
    except Exception as e:
        print(f"❌ Erreur d'import: {e}")

def test_controllers():
    """Test des contrôleurs"""
    print("\n🧪 TEST DES CONTRÔLEURS")
    print("=" * 50)
    
    try:
        from src.modules.academic.subjects.controllers.matiere_controller import add_matiere, update_matiere
        from src.modules.academic.grades.controllers.notes_controller import add_note, update_note
        
        print("✅ Import des contrôleurs réussi")
        
        # Test des fonctions d'ajout
        print("🔄 Test des fonctions d'ajout...")
        print("✅ add_matiere disponible")
        print("✅ add_note disponible")
        print("✅ update_matiere disponible")
        print("✅ update_note disponible")
        
    except Exception as e:
        print(f"❌ Erreur d'import des contrôleurs: {e}")

if __name__ == "__main__":
    print("🚀 DÉMARRAGE DES TESTS DE FORMULAIRES")
    print("=" * 60)
    
    test_matieres_formulaire()
    test_notes_formulaire()
    test_controllers()
    
    print("\n🎯 TESTS TERMINÉS")
    print("=" * 60)
