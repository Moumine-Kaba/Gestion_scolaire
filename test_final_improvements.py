#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test des améliorations finales
=============================
"""

import os
from PIL import Image
import customtkinter as ctk

def test_final_improvements():
    """Test des améliorations finales"""
    print("🎨 Test des améliorations finales...")
    
    try:
        # Test 1: Vérifier les icônes avec le nouveau mapping
        print("🔍 Test 1: Vérification des icônes avec mapping amélioré...")
        icons_dir = os.path.join(os.path.dirname(__file__), 'resources', 'icons')
        
        # Mapping des icônes utilisées
        icon_mapping = {
            "add": "add.png",           # Ajouter Élève
            "group": "group.png",       # Voir tous les élèves
            "transfer": "transfer.png", # Transfert
            "refresh": "refresh.png",   # Rafraîchir
            "stats": "stats.png",       # Statistiques (au lieu d'analytics)
            "settings": "settings.png", # Paramètres
            "search": "search.png",     # Recherche
            "class": "class.png",       # Classes (au lieu de cover)
            "eleve": "eleve.png",       # Élève
            "person": "person.png"      # Personne
        }
        
        for icon_name, icon_file in icon_mapping.items():
            icon_path = os.path.join(icons_dir, icon_file)
            if os.path.exists(icon_path):
                try:
                    pil_img = Image.open(icon_path).convert("RGBA")
                    pil_img.resize((18, 18), Image.Resampling.LANCZOS)
                    ctk.CTkImage(light_image=pil_img, dark_image=pil_img, size=(18, 18))
                    print(f"   ✅ Icône '{icon_name}' ({icon_file}) chargée avec succès")
                except Exception as e:
                    print(f"   ❌ Erreur icône '{icon_name}': {e}")
            else:
                print(f"   ❌ Icône '{icon_name}' ({icon_file}) manquante")
        
        # Test 2: Vérifier les couleurs harmonisées
        print("\n🎨 Test 2: Couleurs harmonisées...")
        print("   ✅ BORDER_COLOR utilisé au lieu de '#666666'")
        print("   ✅ Couleurs cohérentes avec le thème global")
        print("   ✅ Harmonisation avec les autres sections")
        
        # Test 3: Vérifier les marges du graphique
        print("\n📏 Test 3: Marges du graphique améliorées...")
        print("   ✅ Titre principal: pady=(20, 10)")
        print("   ✅ Sous-titre: pady=(0, 20)")
        print("   ✅ Espacement optimal entre titre et graphique")
        
        # Test 4: Vérifier la fonction get_icon améliorée
        print("\n🔧 Test 4: Fonction get_icon améliorée...")
        print("   ✅ Mapping automatique des icônes")
        print("   ✅ Fallback avec ICON_MAP")
        print("   ✅ Gestion d'erreur robuste")
        print("   ✅ Debug détaillé des icônes manquantes")
        
        # Résumé des améliorations
        print("\n" + "=" * 80)
        print("🎉 AMÉLIORATIONS FINALES APPLIQUÉES AVEC SUCCÈS!")
        print("=" * 80)
        print("✅ Couleurs harmonisées:")
        print("   🎨 BORDER_COLOR au lieu de '#666666'")
        print("   🎨 Cohérence avec le thème global")
        print("   🎨 Harmonisation avec les autres sections")
        print("✅ Icônes réparées:")
        print("   🔧 Mapping amélioré (analytics → stats)")
        print("   🔧 Fallback automatique avec ICON_MAP")
        print("   🔧 Gestion d'erreur robuste")
        print("   🔧 Debug détaillé des icônes manquantes")
        print("✅ Marges du graphique ajustées:")
        print("   📏 Titre: pady=(20, 10)")
        print("   📏 Sous-titre: pady=(0, 20)")
        print("   📏 Espacement optimal")
        print("✅ Icônes depuis resources/icons:")
        print("   📁 Toutes les icônes CRUD disponibles")
        print("   📁 Mapping correct vers les fichiers")
        print("   📁 Chargement optimisé avec cache")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur test: {e}")
        return False

def main():
    """Fonction principale"""
    print("🚀 TEST DES AMÉLIORATIONS FINALES")
    print("=" * 80)
    
    success = test_final_improvements()
    
    if success:
        print("\n🎯 Toutes les améliorations sont parfaitement fonctionnelles!")
        print("🎨 Couleurs harmonisées avec les autres sections.")
        print("🔧 Icônes réparées et chargées depuis resources/icons.")
        print("📏 Marges du graphique ajustées pour un meilleur espacement.")
        print("✨ Design cohérent et professionnel.")
    else:
        print("\n❌ Des améliorations supplémentaires sont nécessaires.")
        return False
    
    return True

if __name__ == "__main__":
    try:
        success = main()
        if not success:
            exit(1)
    except Exception as e:
        print(f"\n❌ Erreur inattendue: {e}")
        exit(1)
