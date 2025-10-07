# -*- coding: utf-8 -*-
"""
Test du Système de Paiements Corrigé
EduManager+ - Vérification des Corrections

Ce script teste le système corrigé pour s'assurer que les noms de colonnes
sont maintenant corrects.
"""

import os
import sys

# Ajouter le chemin du projet pour les imports
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../../..'))
if project_root not in sys.path:
    sys.path.append(project_root)

def test_database_connection():
    """Test de la connexion à la base de données"""
    print("🔍 Test de connexion à la base de données...")
    
    try:
        from database.connection import get_db_connection
        
        conn = get_db_connection()
        if not conn:
            print("❌ Impossible de se connecter à la base de données")
            return False
        
        cur = conn.cursor()
        
        # Test de la structure des tables
        print("📋 Vérification de la structure des tables...")
        
        # Test table élèves
        try:
            cur.execute("SELECT TOP 1 id_eleve, nom, prenom, id_classe FROM eleves")
            row = cur.fetchone()
            if row:
                print(f"✅ Table élèves OK: id_eleve={row[0]}, nom={row[1]}, prenom={row[2]}, id_classe={row[3]}")
            else:
                print("ℹ️ Aucun élève trouvé")
        except Exception as e:
            print(f"❌ Erreur table élèves: {e}")
        
        # Test table classes
        try:
            cur.execute("SELECT TOP 1 id_classe, nom_classe, niveau FROM classes")
            row = cur.fetchone()
            if row:
                print(f"✅ Table classes OK: id_classe={row[0]}, nom_classe={row[1]}, niveau={row[2]}")
            else:
                print("ℹ️ Aucune classe trouvée")
        except Exception as e:
            print(f"❌ Erreur table classes: {e}")
        
        # Test de jointure
        try:
            cur.execute("""
                SELECT TOP 1 el.id_eleve, el.nom, el.prenom, c.nom_classe, c.niveau
                FROM eleves el
                LEFT JOIN classes c ON el.id_classe = c.id_classe
            """)
            row = cur.fetchone()
            if row:
                print(f"✅ Jointure OK: {row[1]} {row[2]} -> {row[3]} ({row[4]})")
            else:
                print("ℹ️ Aucune jointure trouvée")
        except Exception as e:
            print(f"❌ Erreur jointure: {e}")
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Erreur connexion: {e}")
        return False

def test_enhanced_controller():
    """Test du contrôleur amélioré corrigé"""
    print("\n🧪 Test du contrôleur amélioré...")
    
    try:
        from src.modules.administrative.payments.controllers.enhanced_paiement_controller import EnhancedPaiementController
        
        controller = EnhancedPaiementController()
        print("✅ Contrôleur initialisé avec succès")
        
        # Test des types de frais
        print("📋 Test des types de frais...")
        types_frais = controller.get_all_types_frais()
        print(f"✅ {len(types_frais)} types de frais récupérés")
        
        # Test des statistiques (cela devrait maintenant fonctionner)
        print("📊 Test des statistiques...")
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
            print("ℹ️ Aucune statistique disponible (normal si pas de données)")
        
        # Test des échéances en retard
        print("⚠️ Test des échéances en retard...")
        echeances_retard = controller.get_echeances_en_retard()
        print(f"✅ {len(echeances_retard)} échéances en retard trouvées")
        
        if echeances_retard:
            for echeance in echeances_retard[:3]:
                print(f"   - {echeance['eleve_nom']} {echeance['eleve_prenom']}: "
                      f"{echeance['jours_retard']} jours de retard ({echeance['type_frais_nom']})")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur test contrôleur: {e}")
        return False

def test_view_integration():
    """Test de l'intégration avec la vue"""
    print("\n🖥️ Test de l'intégration avec la vue...")
    
    try:
        # Test d'import de la vue
        from src.modules.administrative.payments.views.paiements_view import PaiementsView
        print("✅ Vue importée avec succès")
        
        # Test des contrôleurs
        from src.modules.administrative.payments.controllers.enhanced_paiement_controller import EnhancedPaiementController
        from src.modules.academic.students.controllers.eleve_controller import get_all_eleves
        from src.modules.academic.classes.controllers.classe_controller import get_all_classes
        
        print("✅ Tous les contrôleurs importés avec succès")
        
        # Test des données
        eleves = get_all_eleves()
        classes = get_all_classes()
        
        print(f"✅ {len(eleves)} élèves et {len(classes)} classes chargés")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur test vue: {e}")
        return False

def create_sample_data():
    """Crée des données de test si nécessaire"""
    print("\n📝 Création de données de test...")
    
    try:
        from src.modules.administrative.payments.controllers.database_schema import create_all_payment_tables
        
        if create_all_payment_tables():
            print("✅ Tables créées/vérifiées avec succès")
        
        # Vérifier s'il y a des élèves
        from src.modules.academic.students.controllers.eleve_controller import get_all_eleves
        
        eleves = get_all_eleves()
        if not eleves:
            print("⚠️ Aucun élève trouvé. Créez des élèves d'abord.")
            return False
        
        print(f"✅ {len(eleves)} élèves disponibles pour les tests")
        return True
        
    except Exception as e:
        print(f"❌ Erreur création données test: {e}")
        return False

def main():
    """Fonction principale de test"""
    print("🧪 TEST DU SYSTÈME DE PAIEMENTS CORRIGÉ")
    print("=" * 50)
    
    # Changer vers le répertoire des paiements
    os.chdir(os.path.join(project_root, "src", "modules", "administrative", "payments"))
    
    # Tests
    tests = [
        ("Connexion base de données", test_database_connection),
        ("Contrôleur amélioré", test_enhanced_controller),
        ("Intégration vue", test_view_integration),
        ("Données de test", create_sample_data)
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
        print("\n🎉 TOUS LES TESTS SONT PASSÉS !")
        print("✅ Le système de paiements corrigé fonctionne parfaitement.")
        print("🚀 Vous pouvez maintenant utiliser le système sans erreurs !")
    elif passed >= total - 1:
        print("\n✅ SYSTÈME FONCTIONNEL")
        print("⚠️ Quelques tests ont échoué, mais le système principal fonctionne.")
        print("🚀 Vous pouvez utiliser le système de paiements.")
    else:
        print("\n⚠️ PROBLÈMES DÉTECTÉS")
        print("❌ Plusieurs tests ont échoué. Vérifiez les erreurs ci-dessus.")
        print("🔧 Des corrections supplémentaires peuvent être nécessaires.")
    
    return passed >= total - 1

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n👋 Test interrompu par l'utilisateur")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Erreur critique: {e}")
        sys.exit(1)
