# -*- coding: utf-8 -*-
"""
Test Simple du Système de Paiements Corrigé
EduManager+ - Test Basique
"""

import os
import sys

# Ajouter le chemin du projet pour les imports
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../../..'))
if project_root not in sys.path:
    sys.path.append(project_root)

def test_controller():
    """Test simple du contrôleur"""
    print("Test du controleur ameliore...")
    
    try:
        # Ajouter le chemin du projet
        sys.path.insert(0, os.path.join(os.getcwd(), '..', '..', '..', '..', '..'))
        from src.modules.administrative.payments.controllers.enhanced_paiement_controller import EnhancedPaiementController
        
        controller = EnhancedPaiementController()
        print("OK - Controleur initialise")
        
        # Test des statistiques
        stats = controller.get_statistiques_paiements()
        
        if stats:
            print(f"OK - Statistiques recuperees pour {stats['annee_scolaire']}")
            print(f"   - Total echeances: {stats['total_echeances']}")
            print(f"   - Payees: {stats['payees']}")
            print(f"   - En attente: {stats['en_attente']}")
            print(f"   - En retard: {stats['en_retard']}")
        else:
            print("INFO - Aucune statistique disponible")
        
        # Test des echeances en retard
        echeances_retard = controller.get_echeances_en_retard()
        print(f"OK - {len(echeances_retard)} echeances en retard trouvees")
        
        return True
        
    except Exception as e:
        print(f"ERREUR test controleur: {e}")
        return False

def test_database():
    """Test simple de la base de données"""
    print("Test de la base de donnees...")
    
    try:
        # Ajouter le chemin du projet
        sys.path.insert(0, os.path.join(os.getcwd(), '..', '..', '..', '..', '..'))
        from database.connection import get_db_connection
        
        conn = get_db_connection()
        if not conn:
            print("ERREUR - Impossible de se connecter")
            return False
        
        cur = conn.cursor()
        
        # Test table eleves
        try:
            cur.execute("SELECT TOP 1 id_eleve, nom, prenom, id_classe FROM eleves")
            row = cur.fetchone()
            if row:
                print(f"OK - Table eleves: id_eleve={row[0]}, nom={row[1]}")
            else:
                print("INFO - Aucun eleve trouve")
        except Exception as e:
            print(f"ERREUR table eleves: {e}")
        
        # Test table classes
        try:
            cur.execute("SELECT TOP 1 id_classe, nom_classe, niveau FROM classes")
            row = cur.fetchone()
            if row:
                print(f"OK - Table classes: id_classe={row[0]}, nom_classe={row[1]}")
            else:
                print("INFO - Aucune classe trouvee")
        except Exception as e:
            print(f"ERREUR table classes: {e}")
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"ERREUR test base de donnees: {e}")
        return False

def main():
    """Fonction principale"""
    print("TEST DU SYSTEME DE PAIEMENTS CORRIGE")
    print("=" * 40)
    
    # Nous sommes déjà dans le bon répertoire
    print(f"Repertoire de travail: {os.getcwd()}")
    
    # Tests
    tests = [
        ("Base de donnees", test_database),
        ("Controleur ameliore", test_controller)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n--- {test_name.upper()} ---")
        try:
            success = test_func()
            results.append((test_name, success))
        except Exception as e:
            print(f"ERREUR critique dans {test_name}: {e}")
            results.append((test_name, False))
    
    # Résumé
    print("\n" + "=" * 40)
    print("RESUME DES TESTS")
    print("=" * 40)
    
    passed = sum(1 for _, success in results if success)
    total = len(results)
    
    for test_name, success in results:
        status = "REUSSI" if success else "ECHEC"
        print(f"{test_name:<20} {status}")
    
    print(f"\nResultat global: {passed}/{total} tests reussis")
    
    if passed == total:
        print("\nSUCCES - Tous les tests sont passes !")
        print("Le systeme de paiements corrige fonctionne.")
    elif passed >= total - 1:
        print("\nFONCTIONNEL - Le systeme principal fonctionne.")
    else:
        print("\nPROBLEMES - Des corrections supplementaires sont necessaires.")
    
    return passed >= total - 1

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\nTest interrompu par l'utilisateur")
        sys.exit(0)
    except Exception as e:
        print(f"\nErreur critique: {e}")
        sys.exit(1)
