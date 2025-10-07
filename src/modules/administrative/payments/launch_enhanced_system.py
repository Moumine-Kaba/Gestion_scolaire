# -*- coding: utf-8 -*-
"""
Lanceur du Système de Paiements Amélioré
EduManager+ - Initialisation Complète

Ce script lance et initialise le système de paiements amélioré.
"""

import os
import sys
from datetime import datetime

# Ajouter le chemin du projet pour les imports
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../../..'))
if project_root not in sys.path:
    sys.path.append(project_root)

def check_environment():
    """Vérifie l'environnement et les dépendances"""
    print("🔍 Vérification de l'environnement...")
    
    try:
        # Vérifier Python
        python_version = sys.version_info
        print(f"✅ Python {python_version.major}.{python_version.minor}.{python_version.micro}")
        
        # Vérifier les modules requis
        required_modules = [
            'tkinter',
            'customtkinter',
            'pyodbc',
            'PIL'
        ]
        
        missing_modules = []
        for module in required_modules:
            try:
                __import__(module)
                print(f"✅ Module {module} disponible")
            except ImportError:
                missing_modules.append(module)
                print(f"❌ Module {module} manquant")
        
        if missing_modules:
            print(f"\n⚠️ Modules manquants: {', '.join(missing_modules)}")
            print("💡 Installez-les avec: pip install " + " ".join(missing_modules))
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur vérification environnement: {e}")
        return False

def initialize_database():
    """Initialise la base de données"""
    print("\n🗄️ Initialisation de la base de données...")
    
    try:
        from src.modules.administrative.payments.controllers.database_schema import create_all_payment_tables
        
        if create_all_payment_tables():
            print("✅ Base de données initialisée avec succès")
            return True
        else:
            print("❌ Erreur lors de l'initialisation de la base de données")
            return False
            
    except Exception as e:
        print(f"❌ Erreur initialisation base de données: {e}")
        return False

def test_system():
    """Teste le système"""
    print("\n🧪 Test du système...")
    
    try:
        from src.modules.administrative.payments.controllers.enhanced_paiement_controller import EnhancedPaiementController
        
        controller = EnhancedPaiementController()
        
        # Test des types de frais
        types_frais = controller.get_all_types_frais()
        print(f"✅ {len(types_frais)} types de frais chargés")
        
        # Test des statistiques
        stats = controller.get_statistiques_paiements()
        if stats:
            print(f"✅ Statistiques disponibles pour {stats['annee_scolaire']}")
        else:
            print("ℹ️ Aucune statistique disponible (normal si pas de données)")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur test système: {e}")
        return False

def launch_interface():
    """Lance l'interface utilisateur"""
    print("\n🚀 Lancement de l'interface...")
    
    try:
        # Configuration de CustomTkinter
        import customtkinter as ctk
        
        # Créer la fenêtre principale
        root = ctk.CTk()
        root.title("EduManager+ - Système de Paiements Amélioré")
        root.geometry("1400x900")
        
        # Appliquer le thème
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        # Importer et créer la vue
        from src.modules.administrative.payments.views.paiements_view import PaiementsView
        from resources.themes.theme import apply_theme_to_app, MARGIN_LARGE
        
        # Appliquer le thème EduManager+
        apply_theme_to_app(root)
        
        # Créer et afficher la vue
        paiements_view = PaiementsView(root)
        paiements_view.pack(fill="both", expand=True, padx=MARGIN_LARGE, pady=MARGIN_LARGE)
        
        print("✅ Interface lancée avec succès")
        print("🎉 Le système de paiements amélioré est maintenant actif !")
        print("\n💡 Fonctionnalités disponibles:")
        print("   • Tableau de bord moderne")
        print("   • Gestion des types de frais")
        print("   • Échéanciers automatiques")
        print("   • Système de remises")
        print("   • Rapports financiers")
        print("   • Statistiques en temps réel")
        
        # Lancer l'application
        root.mainloop()
        
    except Exception as e:
        print(f"❌ Erreur lancement interface: {e}")
        return False

def show_menu():
    """Affiche le menu principal"""
    print("\n" + "="*60)
    print("🎪 SYSTÈME DE PAIEMENTS AMÉLIORÉ - EduManager+")
    print("="*60)
    print("Choisissez une option:")
    print()
    print("1. 🚀 Lancer l'interface complète")
    print("2. 🧪 Tester le système")
    print("3. 📊 Voir la démonstration")
    print("4. 🔧 Migrer la base de données")
    print("5. ❌ Quitter")
    print()
    
    while True:
        try:
            choice = input("Votre choix (1-5): ").strip()
            
            if choice == "1":
                return "launch"
            elif choice == "2":
                return "test"
            elif choice == "3":
                return "demo"
            elif choice == "4":
                return "migrate"
            elif choice == "5":
                return "quit"
            else:
                print("❌ Choix invalide. Veuillez choisir entre 1 et 5.")
                
        except KeyboardInterrupt:
            print("\n👋 Au revoir !")
            return "quit"

def main():
    """Fonction principale"""
    print("🎯 Initialisation du Système de Paiements Amélioré")
    print(f"📅 {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    
    # Vérifier l'environnement
    if not check_environment():
        print("\n❌ Environnement non compatible. Arrêt du programme.")
        return False
    
    # Initialiser la base de données
    if not initialize_database():
        print("\n❌ Impossible d'initialiser la base de données. Arrêt du programme.")
        return False
    
    # Tester le système
    if not test_system():
        print("\n⚠️ Le système présente des problèmes, mais peut continuer.")
    
    # Menu principal
    while True:
        choice = show_menu()
        
        if choice == "launch":
            launch_interface()
        elif choice == "test":
            try:
                exec(open("test_enhanced_system.py").read())
            except FileNotFoundError:
                print("❌ Fichier de test non trouvé")
        elif choice == "demo":
            try:
                exec(open("demo_enhanced_features.py").read())
            except FileNotFoundError:
                print("❌ Fichier de démonstration non trouvé")
        elif choice == "migrate":
            try:
                exec(open("migrate_database.py").read())
            except FileNotFoundError:
                print("❌ Fichier de migration non trouvé")
        elif choice == "quit":
            print("\n👋 Merci d'avoir utilisé EduManager+ !")
            break
    
    return True

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n👋 Arrêt demandé par l'utilisateur")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Erreur critique: {e}")
        sys.exit(1)

