#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script pour mettre à jour la table classes avec les nouvelles statistiques
=======================================================================

Ce script met à jour la table classes avec les statistiques des élèves
après l'ajout des 1000 nouveaux élèves.
"""

import sys
import os
from typing import List, Dict, Any

# Ajouter le chemin racine au sys.path
root_path = os.path.join(os.path.dirname(__file__), '..')
sys.path.insert(0, root_path)

from database.connection import get_db_connection

def update_classes_with_statistics():
    """Met à jour la table classes avec les statistiques des élèves"""
    conn = get_db_connection()
    if not conn:
        print("❌ Impossible de se connecter à la base de données")
        return False
    
    try:
        cursor = conn.cursor()
        
        # Vérifier si la colonne nb_eleves existe, sinon l'ajouter
        cursor.execute("""
            SELECT COLUMN_NAME 
            FROM INFORMATION_SCHEMA.COLUMNS 
            WHERE TABLE_NAME = 'classes' AND COLUMN_NAME = 'nb_eleves'
        """)
        
        if not cursor.fetchone():
            print("📝 Ajout de la colonne nb_eleves à la table classes...")
            cursor.execute("ALTER TABLE classes ADD COLUMN nb_eleves INTEGER DEFAULT 0")
            print("✅ Colonne nb_eleves ajoutée")
        
        # Vérifier si la colonne nb_garcons existe, sinon l'ajouter
        cursor.execute("""
            SELECT COLUMN_NAME 
            FROM INFORMATION_SCHEMA.COLUMNS 
            WHERE TABLE_NAME = 'classes' AND COLUMN_NAME = 'nb_garcons'
        """)
        
        if not cursor.fetchone():
            print("📝 Ajout de la colonne nb_garcons à la table classes...")
            cursor.execute("ALTER TABLE classes ADD COLUMN nb_garcons INTEGER DEFAULT 0")
            print("✅ Colonne nb_garcons ajoutée")
        
        # Vérifier si la colonne nb_filles existe, sinon l'ajouter
        cursor.execute("""
            SELECT COLUMN_NAME 
            FROM INFORMATION_SCHEMA.COLUMNS 
            WHERE TABLE_NAME = 'classes' AND COLUMN_NAME = 'nb_filles'
        """)
        
        if not cursor.fetchone():
            print("📝 Ajout de la colonne nb_filles à la table classes...")
            cursor.execute("ALTER TABLE classes ADD COLUMN nb_filles INTEGER DEFAULT 0")
            print("✅ Colonne nb_filles ajoutée")
        
        # Mettre à jour les statistiques pour chaque classe
        print("📊 Mise à jour des statistiques des classes...")
        
        cursor.execute("""
            UPDATE classes 
            SET 
                nb_eleves = (
                    SELECT COUNT(*) 
                    FROM eleves 
                    WHERE eleves.classe_id = classes.id
                ),
                nb_garcons = (
                    SELECT COUNT(*) 
                    FROM eleves 
                    WHERE eleves.classe_id = classes.id AND eleves.genre = 'M'
                ),
                nb_filles = (
                    SELECT COUNT(*) 
                    FROM eleves 
                    WHERE eleves.classe_id = classes.id AND eleves.genre = 'F'
                )
        """)
        
        rows_updated = cursor.rowcount
        print(f"✅ {rows_updated} classes mises à jour")
        
        # Afficher les statistiques finales
        cursor.execute("""
            SELECT nom, niveau, nb_eleves, nb_garcons, nb_filles
            FROM classes 
            ORDER BY niveau, nom
        """)
        
        classes_stats = cursor.fetchall()
        print("\n📈 Statistiques finales des classes:")
        print("-" * 80)
        print(f"{'Classe':<20} {'Niveau':<10} {'Total':<8} {'Garçons':<10} {'Filles':<10}")
        print("-" * 80)
        
        total_eleves = 0
        total_garcons = 0
        total_filles = 0
        
        for classe in classes_stats:
            nom, niveau, nb_eleves, nb_garcons, nb_filles = classe
            print(f"{nom:<20} {niveau:<10} {nb_eleves:<8} {nb_garcons:<10} {nb_filles:<10}")
            total_eleves += nb_eleves or 0
            total_garcons += nb_garcons or 0
            total_filles += nb_filles or 0
        
        print("-" * 80)
        print(f"{'TOTAL':<20} {'':<10} {total_eleves:<8} {total_garcons:<10} {total_filles:<10}")
        print("-" * 80)
        
        conn.commit()
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors de la mise à jour des classes: {e}")
        conn.rollback()
        return False
    finally:
        conn.close()

def verify_data_integrity():
    """Vérifie l'intégrité des données"""
    conn = get_db_connection()
    if not conn:
        print("❌ Impossible de se connecter à la base de données")
        return False
    
    try:
        cursor = conn.cursor()
        
        # Vérifier que tous les élèves ont une classe assignée
        cursor.execute("SELECT COUNT(*) FROM eleves WHERE classe_id IS NULL")
        eleves_sans_classe = cursor.fetchone()[0]
        
        if eleves_sans_classe > 0:
            print(f"⚠️ {eleves_sans_classe} élèves sans classe assignée")
        else:
            print("✅ Tous les élèves ont une classe assignée")
        
        # Vérifier la cohérence des statistiques
        cursor.execute("""
            SELECT c.nom, c.nb_eleves, COUNT(e.id) as real_count
            FROM classes c
            LEFT JOIN eleves e ON c.id = e.classe_id
            GROUP BY c.id, c.nom, c.nb_eleves
            HAVING c.nb_eleves != COUNT(e.id)
        """)
        
        inconsistencies = cursor.fetchall()
        if inconsistencies:
            print("⚠️ Incohérences détectées dans les statistiques:")
            for inc in inconsistencies:
                print(f"   Classe {inc[0]}: statistique={inc[1]}, réel={inc[2]}")
        else:
            print("✅ Statistiques cohérentes")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors de la vérification: {e}")
        return False
    finally:
        conn.close()

def main():
    """Fonction principale"""
    print("🚀 Mise à jour de la table classes avec les nouvelles statistiques...")
    print("=" * 70)
    
    # 1. Mettre à jour les statistiques
    print("📊 Mise à jour des statistiques des classes...")
    success = update_classes_with_statistics()
    
    if not success:
        print("❌ Échec de la mise à jour des statistiques")
        return False
    
    # 2. Vérifier l'intégrité des données
    print("\n🔍 Vérification de l'intégrité des données...")
    verify_data_integrity()
    
    print("\n🎉 Mise à jour terminée avec succès!")
    print("=" * 70)
    
    return True

if __name__ == "__main__":
    try:
        success = main()
        if success:
            print("\n🎯 Mission accomplie! La table classes a été mise à jour.")
        else:
            print("\n❌ Échec de la mise à jour de la table classes.")
            sys.exit(1)
    except KeyboardInterrupt:
        print("\n⚠️ Processus interrompu par l'utilisateur.")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Erreur inattendue: {e}")
        sys.exit(1)
