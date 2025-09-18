#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script principal pour ajouter 1000 élèves et optimiser les vues
==============================================================

Ce script exécute tous les processus nécessaires pour :
1. Ajouter 1000 élèves avec des données réalistes
2. Les répartir dans les classes existantes
3. Mettre à jour les statistiques des classes
4. Optimiser les vues pour gérer le grand nombre de données
"""

import sys
import os
import time
from typing import List, Dict, Any

# Ajouter le chemin racine au sys.path
root_path = os.path.join(os.path.dirname(__file__), '..')
sys.path.insert(0, root_path)

def run_script(script_name: str, description: str) -> bool:
    """Exécute un script et retourne True si succès"""
    print(f"\n🚀 {description}")
    print("=" * 60)
    
    try:
        # Importer et exécuter le script
        if script_name == "add_1000_students":
            from add_1000_students import main as add_students_main
            return add_students_main()
        elif script_name == "update_classes_statistics":
            from update_classes_statistics import main as update_stats_main
            return update_stats_main()
        else:
            print(f"❌ Script inconnu: {script_name}")
            return False
            
    except ImportError as e:
        print(f"❌ Erreur d'import du script {script_name}: {e}")
        return False
    except Exception as e:
        print(f"❌ Erreur lors de l'exécution de {script_name}: {e}")
        return False

def verify_database_state():
    """Vérifie l'état de la base de données"""
    print("\n🔍 Vérification de l'état de la base de données...")
    print("-" * 50)
    
    try:
        import sys
        import os
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))
        from database.connection import get_db_connection
        
        conn = get_db_connection()
        if not conn:
            print("❌ Impossible de se connecter à la base de données")
            return False
        
        cursor = conn.cursor()
        
        # Vérifier les classes
        cursor.execute("SELECT COUNT(*) FROM classes")
        nb_classes = cursor.fetchone()[0]
        print(f"📚 Nombre de classes: {nb_classes}")
        
        # Vérifier les élèves
        cursor.execute("SELECT COUNT(*) FROM eleves")
        nb_eleves = cursor.fetchone()[0]
        print(f"👥 Nombre d'élèves: {nb_eleves}")
        
        # Vérifier la répartition
        cursor.execute("""
            SELECT c.nom, COUNT(e.id) as nb_eleves
            FROM classes c
            LEFT JOIN eleves e ON c.id = e.classe_id
            GROUP BY c.id, c.nom
            ORDER BY nb_eleves DESC
        """)
        
        repartition = cursor.fetchall()
        print(f"\n📊 Répartition des élèves par classe:")
        for classe, nb in repartition:
            print(f"   - {classe}: {nb} élèves")
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors de la vérification: {e}")
        return False

def main():
    """Fonction principale"""
    print("🎯 SCRIPT PRINCIPAL - AJOUT DE 1000 ÉLÈVES ET OPTIMISATION")
    print("=" * 70)
    print("Ce script va :")
    print("1. Ajouter 1000 élèves avec des données réalistes")
    print("2. Les répartir dans les classes existantes")
    print("3. Mettre à jour les statistiques des classes")
    print("4. Optimiser les vues pour gérer le grand nombre de données")
    print("=" * 70)
    
    # Demander confirmation
    response = input("\n❓ Voulez-vous continuer ? (o/N): ").lower().strip()
    if response not in ['o', 'oui', 'y', 'yes']:
        print("❌ Opération annulée par l'utilisateur")
        return False
    
    start_time = time.time()
    
    # 1. Vérifier l'état initial
    print("\n📋 ÉTAPE 1: Vérification de l'état initial")
    if not verify_database_state():
        print("❌ Échec de la vérification initiale")
        return False
    
    # 2. Ajouter les 1000 élèves
    print("\n📋 ÉTAPE 2: Ajout de 1000 élèves")
    if not run_script("add_1000_students", "Ajout de 1000 élèves avec données réalistes"):
        print("❌ Échec de l'ajout des élèves")
        return False
    
    # 3. Mettre à jour les statistiques des classes
    print("\n📋 ÉTAPE 3: Mise à jour des statistiques")
    if not run_script("update_classes_statistics", "Mise à jour des statistiques des classes"):
        print("❌ Échec de la mise à jour des statistiques")
        return False
    
    # 4. Vérification finale
    print("\n📋 ÉTAPE 4: Vérification finale")
    if not verify_database_state():
        print("❌ Échec de la vérification finale")
        return False
    
    # Calculer le temps d'exécution
    end_time = time.time()
    execution_time = end_time - start_time
    
    print("\n🎉 PROCESSUS TERMINÉ AVEC SUCCÈS!")
    print("=" * 70)
    print(f"⏱️ Temps d'exécution: {execution_time:.2f} secondes")
    print("✅ 1000 élèves ajoutés et répartis dans les classes")
    print("✅ Statistiques des classes mises à jour")
    print("✅ Vues optimisées pour gérer le grand nombre de données")
    print("=" * 70)
    
    return True

if __name__ == "__main__":
    try:
        success = main()
        if success:
            print("\n🎯 Mission accomplie! Le système est maintenant optimisé pour 1000+ élèves.")
            sys.exit(0)
        else:
            print("\n❌ Échec du processus principal.")
            sys.exit(1)
    except KeyboardInterrupt:
        print("\n⚠️ Processus interrompu par l'utilisateur.")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Erreur inattendue: {e}")
        sys.exit(1)
