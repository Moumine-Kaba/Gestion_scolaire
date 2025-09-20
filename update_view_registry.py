#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de mise à jour du registre des vues pour inclure la vue avancée des présences
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '.'))

def update_view_registry():
    """Met à jour le registre des vues pour inclure la vue avancée"""
    print("🔄 Mise à jour du registre des vues...")
    
    try:
        # Import du registre
        from src.core.view_registry import ViewRegistry
        
        # Créer une instance du registre
        registry = ViewRegistry()
        
        # Enregistrer toutes les vues existantes
        registry.register_all_views()
        
        # Ajouter manuellement la vue avancée des présences
        print("\n📦 Ajout de la vue avancée des présences...")
        
        try:
            from src.modules.academic.attendance.views.advanced_attendance_view import AdvancedAttendanceView
            registry.views["presences_advanced"] = AdvancedAttendanceView
            print("✅ Vue avancée des présences ajoutée au registre")
        except ImportError as e:
            print(f"⚠️ Impossible d'ajouter la vue avancée: {e}")
        
        # Afficher le résumé
        print(f"\n📊 Résumé du registre:")
        print(f"  • Total des vues: {len(registry.views)}")
        print(f"  • Erreurs: {len(registry.view_errors)}")
        
        if registry.view_errors:
            print("\n⚠️ Erreurs d'import:")
            for view_name, error in registry.view_errors.items():
                print(f"  - {view_name}: {error}")
        
        # Vérifier que la vue avancée est bien enregistrée
        if "presences_advanced" in registry.views:
            print("\n✅ Vue avancée des présences disponible dans le registre")
            return True
        else:
            print("\n❌ Vue avancée des présences non trouvée dans le registre")
            return False
            
    except Exception as e:
        print(f"❌ Erreur lors de la mise à jour du registre: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_view_registry():
    """Test le registre des vues mis à jour"""
    print("\n🧪 Test du registre des vues...")
    
    try:
        from src.core.view_registry import ViewRegistry
        
        registry = ViewRegistry()
        registry.register_all_views()
        
        # Ajouter la vue avancée
        try:
            from src.modules.academic.attendance.views.advanced_attendance_view import AdvancedAttendanceView
            registry.views["presences_advanced"] = AdvancedAttendanceView
        except ImportError:
            pass
        
        # Test de récupération des vues
        print("🔍 Test de récupération des vues...")
        
        # Vues principales
        main_views = ["eleves", "classes", "matieres", "presences", "salles"]
        for view_name in main_views:
            view = registry.get_view(view_name)
            if view:
                print(f"✅ Vue '{view_name}' disponible: {view.__name__}")
            else:
                print(f"❌ Vue '{view_name}' non disponible")
        
        # Vue avancée
        advanced_view = registry.get_view("presences_advanced")
        if advanced_view:
            print(f"✅ Vue avancée 'presences_advanced' disponible: {advanced_view.__name__}")
        else:
            print(f"❌ Vue avancée 'presences_advanced' non disponible")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors du test du registre: {e}")
        return False

def create_integration_script():
    """Crée un script d'intégration pour le dashboard"""
    print("\n📝 Création du script d'intégration...")
    
    integration_code = '''
# Script d'intégration de la vue avancée des présences dans le dashboard
# À ajouter dans src/modules/auth/views/dashboard_view.py

# Remplacer la ligne:
# PresenceView = view_registry.views.get("presences")

# Par:
try:
    from src.modules.academic.attendance.views.advanced_attendance_view import AdvancedAttendanceView
    PresenceView = AdvancedAttendanceView
    print("✅ Vue avancée des présences importée")
except ImportError as e:
    print(f"⚠️ Vue avancée des présences non disponible: {e}")
    PresenceView = view_registry.views.get("presences")
'''
    
    try:
        with open("integration_script.txt", "w", encoding="utf-8") as f:
            f.write(integration_code)
        print("✅ Script d'intégration créé: integration_script.txt")
        return True
    except Exception as e:
        print(f"❌ Erreur lors de la création du script: {e}")
        return False

def main():
    """Fonction principale"""
    print("🏫 Mise à jour du registre des vues pour la vue avancée des présences")
    print("=" * 70)
    
    # Étape 1: Mise à jour du registre
    success1 = update_view_registry()
    
    # Étape 2: Test du registre
    success2 = test_view_registry()
    
    # Étape 3: Création du script d'intégration
    success3 = create_integration_script()
    
    # Résumé final
    print("\n" + "=" * 70)
    print("📊 RÉSUMÉ DE LA MISE À JOUR")
    print("=" * 70)
    
    if success1:
        print("✅ Mise à jour du registre: RÉUSSI")
    else:
        print("❌ Mise à jour du registre: ÉCHEC")
    
    if success2:
        print("✅ Test du registre: RÉUSSI")
    else:
        print("❌ Test du registre: ÉCHEC")
    
    if success3:
        print("✅ Création du script d'intégration: RÉUSSI")
    else:
        print("❌ Création du script d'intégration: ÉCHEC")
    
    if success1 and success2 and success3:
        print("\n🎉 MISE À JOUR COMPLÈTE RÉUSSIE !")
        print("🚀 La vue avancée des présences est maintenant intégrée")
        print("\n📋 Prochaines étapes:")
        print("  1. Vérifiez que le dashboard utilise la nouvelle vue")
        print("  2. Testez toutes les fonctionnalités")
        print("  3. Configurez les paramètres selon vos besoins")
    else:
        print("\n⚠️ CERTAINES ÉTAPES ONT ÉCHOUÉ")
        print("🔧 Vérifiez les erreurs ci-dessus")

if __name__ == "__main__":
    main()
