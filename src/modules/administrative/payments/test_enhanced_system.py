# -*- coding: utf-8 -*-
"""
Script de Test pour le Système de Paiements Amélioré
EduManager+ - Test des Nouvelles Fonctionnalités

Ce script teste toutes les nouvelles fonctionnalités du système de paiements.
"""

import os
import sys
from datetime import datetime, timedelta

# Ajouter le chemin du projet pour les imports
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../../..'))
if project_root not in sys.path:
    sys.path.append(project_root)

from src.modules.administrative.payments.controllers.database_schema import (
    create_all_payment_tables, get_current_academic_year, generate_echeancier_for_student
)
from src.modules.administrative.payments.controllers.enhanced_paiement_controller import (
    EnhancedPaiementController
)

def test_database_schema():
    """Test de création des tables"""
    print("🧪 Test de création des tables...")
    
    try:
        # Créer toutes les tables
        success = create_all_payment_tables()
        
        if success:
            print("✅ Toutes les tables créées avec succès")
            
            # Tester l'année scolaire
            current_year = get_current_academic_year()
            print(f"📅 Année scolaire actuelle: {current_year}")
            
            return True
        else:
            print("❌ Erreur lors de la création des tables")
            return False
            
    except Exception as e:
        print(f"❌ Erreur test schema: {e}")
        return False

def test_enhanced_controller():
    """Test du contrôleur amélioré"""
    print("\n🧪 Test du contrôleur amélioré...")
    
    try:
        controller = EnhancedPaiementController()
        
        # Test des types de frais
        print("📋 Test des types de frais...")
        types_frais = controller.get_all_types_frais()
        print(f"✅ {len(types_frais)} types de frais récupérés")
        
        for tf in types_frais[:3]:  # Afficher les 3 premiers
            print(f"   - {tf['nom']}: {tf['montant_standard']:,} GNF ({tf['periodicite']})")
        
        # Test des statistiques
        print("\n📊 Test des statistiques...")
        stats = controller.get_statistiques_paiements()
        
        if stats:
            print(f"✅ Statistiques récupérées pour {stats['annee_scolaire']}")
            print(f"   - Total échéances: {stats['total_echeances']}")
            print(f"   - Paiées: {stats['payees']}")
            print(f"   - En attente: {stats['en_attente']}")
            print(f"   - En retard: {stats['en_retard']}")
            print(f"   - Montant recouvré: {stats['montant_recouvre']:,} GNF")
            print(f"   - Taux de recouvrement: {stats['taux_recouvrement']:.1f}%")
        else:
            print("⚠️ Aucune statistique disponible")
        
        # Test des échéances en retard
        print("\n⚠️ Test des échéances en retard...")
        echeances_retard = controller.get_echeances_en_retard()
        print(f"✅ {len(echeances_retard)} échéances en retard trouvées")
        
        for echeance in echeances_retard[:3]:  # Afficher les 3 premiers
            print(f"   - {echeance['eleve_nom']} {echeance['eleve_prenom']}: "
                  f"{echeance['jours_retard']} jours de retard ({echeance['type_frais_nom']})")
        
        # Test du rapport de trésorerie
        print("\n💰 Test du rapport de trésorerie...")
        date_debut = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')
        date_fin = datetime.now().strftime('%Y-%m-%d')
        
        rapport = controller.get_rapport_tresorerie(date_debut, date_fin)
        
        if rapport:
            print(f"✅ Rapport de trésorerie généré pour {rapport['periode']['debut']} à {rapport['periode']['fin']}")
            print(f"   - Total recettes: {rapport['total_recettes']:,} GNF")
            print(f"   - Recettes par jour: {len(rapport['recettes_par_jour'])} jours")
            print(f"   - Modes de paiement: {len(rapport['recettes_par_mode'])} types")
        else:
            print("⚠️ Aucun rapport de trésorerie disponible")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur test contrôleur: {e}")
        return False

def test_echeancier_generation():
    """Test de génération d'échéancier"""
    print("\n🧪 Test de génération d'échéancier...")
    
    try:
        # Récupérer le premier élève disponible
        from src.modules.academic.students.controllers.eleve_controller import get_all_eleves
        
        eleves = get_all_eleves()
        if not eleves:
            print("⚠️ Aucun élève trouvé pour tester la génération d'échéancier")
            return False
        
        # Prendre le premier élève
        premier_eleve = eleves[0]
        if isinstance(premier_eleve, (tuple, list)):
            eleve_id = premier_eleve[0]
            eleve_nom = f"{premier_eleve[1]} {premier_eleve[2]}"
        else:
            eleve_id = premier_eleve.get('id_eleve')
            eleve_nom = f"{premier_eleve.get('nom')} {premier_eleve.get('prenom')}"
        
        print(f"📅 Génération d'échéancier pour: {eleve_nom} (ID: {eleve_id})")
        
        # Générer l'échéancier
        success = generate_echeancier_for_student(eleve_id)
        
        if success:
            print("✅ Échéancier généré avec succès")
            
            # Récupérer l'échéancier
            controller = EnhancedPaiementController()
            echeancier = controller.get_echeancier_eleve(eleve_id)
            
            print(f"📋 {len(echeancier)} échéances créées:")
            for echeance in echeancier[:5]:  # Afficher les 5 premières
                print(f"   - {echeance['type_frais_nom']}: "
                      f"{echeance['montant_final']:,} GNF "
                      f"({echeance['date_echeance']}) - {echeance['statut']}")
            
            return True
        else:
            print("❌ Erreur lors de la génération d'échéancier")
            return False
            
    except Exception as e:
        print(f"❌ Erreur test échéancier: {e}")
        return False

def test_penalites():
    """Test du système de pénalités"""
    print("\n🧪 Test du système de pénalités...")
    
    try:
        controller = EnhancedPaiementController()
        
        # Appliquer les pénalités automatiquement
        penalites_appliquees = controller.appliquer_penalites_retard()
        
        print(f"✅ {penalites_appliquees} pénalités appliquées automatiquement")
        
        # Récupérer les échéances en retard mises à jour
        echeances_retard = controller.get_echeances_en_retard()
        
        total_penalites = sum(echeance['penalites'] for echeance in echeances_retard)
        print(f"💰 Total des pénalités: {total_penalites:,} GNF")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur test pénalités: {e}")
        return False

def main():
    """Fonction principale de test"""
    print("🚀 TEST DU SYSTÈME DE PAIEMENTS AMÉLIORÉ")
    print("=" * 50)
    
    tests = [
        ("Création des tables", test_database_schema),
        ("Contrôleur amélioré", test_enhanced_controller),
        ("Génération d'échéancier", test_echeancier_generation),
        ("Système de pénalités", test_penalites)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n{'='*20} {test_name.upper()} {'='*20}")
        try:
            success = test_func()
            results.append((test_name, success))
        except Exception as e:
            print(f"❌ Erreur critique dans {test_name}: {e}")
            results.append((test_name, False))
    
    # Résumé des tests
    print("\n" + "="*50)
    print("📊 RÉSUMÉ DES TESTS")
    print("="*50)
    
    passed = sum(1 for _, success in results if success)
    total = len(results)
    
    for test_name, success in results:
        status = "✅ RÉUSSI" if success else "❌ ÉCHEC"
        print(f"{test_name:<30} {status}")
    
    print(f"\n🎯 Résultat global: {passed}/{total} tests réussis")
    
    if passed == total:
        print("🎉 Tous les tests sont passés avec succès !")
        print("✅ Le système de paiements amélioré est prêt à être utilisé.")
    else:
        print("⚠️ Certains tests ont échoué. Vérifiez les erreurs ci-dessus.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

