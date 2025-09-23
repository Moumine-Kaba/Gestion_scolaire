#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script pour supprimer et recréer toutes les classes
"""

import os
import sys
from datetime import datetime

# Ajouter le chemin du projet pour les imports
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '.'))
if project_root not in sys.path:
    sys.path.append(project_root)

from database.connection import get_db_connection

def _connect():
    """Crée une connexion à la base de données"""
    conn = get_db_connection()
    return conn

def delete_all_classes():
    """Supprime toutes les classes de la base de données"""
    try:
        conn = _connect()
        if not conn:
            print("❌ Impossible de se connecter à la base de données")
            return False
            
        cursor = conn.cursor()
        
        # Vérifier si la table classes existe
        cursor.execute("""
            SELECT COUNT(*) 
            FROM INFORMATION_SCHEMA.TABLES 
            WHERE TABLE_NAME = 'classes'
        """)
        
        table_exists = cursor.fetchone()[0] > 0
        
        if not table_exists:
            print("⚠️ Table 'classes' n'existe pas dans SQL Server")
            return False
        
        print("   - Suppression des références dans toutes les tables...")
        
        # Supprimer les références dans la table élèves
        try:
            cursor.execute("UPDATE eleves SET id_classe = NULL WHERE id_classe IS NOT NULL")
            print("   ✅ Références élèves supprimées")
        except Exception as e:
            print(f"   ⚠️ Erreur suppression références élèves: {e}")
        
        # Supprimer les références dans la table cours
        try:
            cursor.execute("UPDATE cours SET classe_id = NULL WHERE classe_id IS NOT NULL")
            print("   ✅ Références cours supprimées")
        except Exception as e:
            print(f"   ⚠️ Erreur suppression références cours: {e}")
        
        # Supprimer les références dans la table presences
        try:
            cursor.execute("UPDATE presences SET classe_id = NULL WHERE classe_id IS NOT NULL")
            print("   ✅ Références presences supprimées")
        except Exception as e:
            print(f"   ⚠️ Erreur suppression références presences: {e}")
        
        # Supprimer les références dans d'autres tables possibles
        try:
            # Vérifier et supprimer dans enseignements si elle existe
            cursor.execute("""
                SELECT COUNT(*) 
                FROM INFORMATION_SCHEMA.TABLES 
                WHERE TABLE_NAME = 'enseignements'
            """)
            if cursor.fetchone()[0] > 0:
                cursor.execute("UPDATE enseignements SET classe_id = NULL WHERE classe_id IS NOT NULL")
                print("   ✅ Références enseignements supprimées")
        except Exception as e:
            print(f"   ⚠️ Erreur suppression références enseignements: {e}")
        
        try:
            # Vérifier et supprimer dans emplois si elle existe
            cursor.execute("""
                SELECT COUNT(*) 
                FROM INFORMATION_SCHEMA.TABLES 
                WHERE TABLE_NAME = 'emplois'
            """)
            if cursor.fetchone()[0] > 0:
                cursor.execute("UPDATE emplois SET classe_id = NULL WHERE classe_id IS NOT NULL")
                print("   ✅ Références emplois supprimées")
        except Exception as e:
            print(f"   ⚠️ Erreur suppression références emplois: {e}")
        
        # Supprimer les références dans d'autres tables communes
        tables_to_check = ['bulletins', 'notes', 'competences', 'evaluations']
        for table_name in tables_to_check:
            try:
                cursor.execute(f"""
                    SELECT COUNT(*) 
                    FROM INFORMATION_SCHEMA.TABLES 
                    WHERE TABLE_NAME = '{table_name}'
                """)
                if cursor.fetchone()[0] > 0:
                    cursor.execute(f"UPDATE {table_name} SET classe_id = NULL WHERE classe_id IS NOT NULL")
                    print(f"   ✅ Références {table_name} supprimées")
            except Exception as e:
                print(f"   ⚠️ Erreur suppression références {table_name}: {e}")
        
        print("   - Suppression des classes...")
        # Ensuite supprimer toutes les classes
        cursor.execute("DELETE FROM classes")
        
        conn.commit()
        conn.close()
        print("✅ Toutes les classes supprimées avec succès")
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors de la suppression: {e}")
        return False

def create_sample_classes():
    """Crée des classes d'exemple"""
    try:
        conn = _connect()
        if not conn:
            print("❌ Impossible de se connecter à la base de données")
            return False
            
        cursor = conn.cursor()
        
        # Classes d'exemple organisées de la 1ère à TSM avec professeurs principaux
        classes_data = [
            # Primaire
            ("1°", "Primaire", 45, "active", "Mme. Dubois"),
            ("2°", "Primaire", 42, "active", "M. Martin"),
            ("3°", "Primaire", 48, "active", "Mme. Durand"),
            ("4°", "Primaire", 50, "active", "M. Bernard"),
            ("5°", "Primaire", 46, "active", "Mme. Petit"),
            ("6°", "Primaire", 44, "active", "M. Robert"),
            
            # Collège
            ("7°", "Collège", 52, "active", "Mme. Moreau"),
            ("8°", "Collège", 49, "active", "M. Simon"),
            ("9°", "Collège", 51, "active", "Mme. Laurent"),
            ("10°", "Collège", 47, "active", "M. Michel"),
            
            # Lycée
            ("11° SE", "Lycée", 53, "active", "Mme. Garcia"),
            ("11° SM", "Lycée", 52, "active", "M. David"),
            ("11° SS", "Lycée", 51, "active", "Mme. Rodriguez"),
            ("12° SE", "Lycée", 50, "active", "M. Thomas"),
            ("12° SM", "Lycée", 49, "active", "Mme. Herrera"),
            ("12° SS", "Lycée", 48, "active", "M. Martinez"),
            
            # Terminale
            ("TSE", "Terminale", 45, "active", "Mme. Lopez"),
            ("TSM", "Terminale", 47, "active", "M. Gonzalez"),
            ("TSS", "Terminale", 46, "active", "Mme. Wilson"),
        ]
        
        # Insérer chaque classe
        for nom, niveau, capacite, statut, professeur_principal in classes_data:
            cursor.execute("""
                INSERT INTO classes (nom_classe, niveau, capacite, statut, date_creation, professeur_principal)
                VALUES (?, ?, ?, ?, GETDATE(), ?)
            """, (nom, niveau, capacite, statut, professeur_principal))
        
        conn.commit()
        conn.close()
        
        print(f"✅ {len(classes_data)} classes créées avec succès")
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors de la création: {e}")
        return False

def main():
    """Fonction principale"""
    print("🔄 Réinitialisation des classes...")
    print("=" * 50)
    
    # Supprimer toutes les classes
    print("1. Suppression des classes existantes...")
    if not delete_all_classes():
        print("❌ Échec de la suppression")
        return
    
    # Créer de nouvelles classes
    print("\n2. Création des nouvelles classes...")
    if not create_sample_classes():
        print("❌ Échec de la création")
        return
    
    print("\n✅ Réinitialisation terminée avec succès!")
    print("🎯 Vous pouvez maintenant tester le nouveau formulaire")

if __name__ == "__main__":
    main()
