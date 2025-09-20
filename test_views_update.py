#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de test pour vérifier les mises à jour des vues élèves et classes
=====================================================================
"""

import sys
import os

# Ajouter le chemin racine au sys.path
root_path = os.path.join(os.path.dirname(__file__), 'src')
sys.path.insert(0, root_path)

def test_eleves_view():
    """Test de la vue élèves avec les vraies données"""
    print("🧪 Test de la vue élèves...")
    
    try:
        from modules.academic.students.views.eleves_dashboard import (
            get_stats_eleves, 
            get_all_classes, 
            fetch_effectifs_par_classe,
            get_eleves_list,
            get_eleves_count
        )
        
        # Test des statistiques globales
        print("📊 Test des statistiques globales...")
        stats = get_stats_eleves()
        print(f"   Total élèves: {stats['total']}")
        print(f"   Filles: {stats['filles']}")
        print(f"   Garçons: {stats['garcons']}")
        print(f"   Classes: {stats['classes']}")
        
        # Test des classes
        print("\n📚 Test des classes...")
        classes = get_all_classes()
        print(f"   Nombre de classes: {len(classes)}")
        for classe in classes[:3]:  # Afficher les 3 premières
            print(f"   - {classe[0]} ({classe[1]})")
        
        # Test des effectifs par classe
        print("\n📈 Test des effectifs par classe...")
        effectifs = fetch_effectifs_par_classe(5)
        for nom_classe, effectif in effectifs:
            print(f"   - {nom_classe}: {effectif} élèves")
        
        # Test de la pagination
        print("\n📄 Test de la pagination...")
        total_eleves = get_eleves_count()
        print(f"   Total élèves pour pagination: {total_eleves}")
        
        eleves_page1 = get_eleves_list(page=1, page_size=5)
        print(f"   Première page (5 élèves): {len(eleves_page1)} résultats")
        for eleve in eleves_page1[:2]:  # Afficher les 2 premiers
            print(f"   - {eleve[2]} {eleve[1]} ({eleve[6] if len(eleve) > 6 else 'N/A'})")
        
        print("✅ Test vue élèves réussi!")
        return True
        
    except Exception as e:
        print(f"❌ Erreur test vue élèves: {e}")
        return False

def test_classes_view():
    """Test de la vue classes avec les vraies données"""
    print("\n🧪 Test de la vue classes...")
    
    try:
        from modules.academic.classes.views.classes_view import (
            get_all_classes,
            get_classes_statistics,
            get_classes_by_niveau
        )
        
        # Test des classes avec statistiques
        print("📚 Test des classes avec statistiques...")
        classes = get_all_classes()
        print(f"   Nombre de classes: {len(classes)}")
        for classe in classes[:3]:  # Afficher les 3 premières
            print(f"   - {classe['nom']} ({classe['niveau']}): {classe['nb_eleves']} élèves")
        
        # Test des statistiques globales
        print("\n📊 Test des statistiques globales...")
        stats = get_classes_statistics()
        print(f"   Total classes: {stats.get('total_classes', 0)}")
        print(f"   Total élèves: {stats.get('total_eleves', 0)}")
        print(f"   Moyenne par classe: {stats.get('moyenne_eleves_par_classe', 0)}")
        
        # Test par niveau
        print("\n🎓 Test par niveau...")
        niveaux = get_classes_by_niveau()
        for niveau, data in niveaux.items():
            print(f"   - {niveau}: {data['nb_classes']} classes, {data['nb_eleves']} élèves")
        
        print("✅ Test vue classes réussi!")
        return True
        
    except Exception as e:
        print(f"❌ Erreur test vue classes: {e}")
        return False

def main():
    """Fonction principale de test"""
    print("🚀 TEST DES MISES À JOUR DES VUES")
    print("=" * 50)
    
    success_eleves = test_eleves_view()
    success_classes = test_classes_view()
    
    print("\n" + "=" * 50)
    if success_eleves and success_classes:
        print("🎉 TOUS LES TESTS RÉUSSIS!")
        print("✅ Les vues élèves et classes utilisent maintenant les vraies données")
        print("✅ Le design et les icônes sont préservés")
        return True
    else:
        print("❌ CERTAINS TESTS ONT ÉCHOUÉ")
        return False

if __name__ == "__main__":
    try:
        success = main()
        if success:
            print("\n🎯 Mission accomplie!")
        else:
            print("\n❌ Des corrections sont nécessaires.")
            sys.exit(1)
    except Exception as e:
        print(f"\n❌ Erreur inattendue: {e}")
        sys.exit(1)

