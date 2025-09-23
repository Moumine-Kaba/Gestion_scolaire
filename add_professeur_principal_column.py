#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script pour ajouter la colonne professeur_principal à la table classes
"""

import os
import sys

# Ajouter le chemin du projet pour les imports
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '.'))
if project_root not in sys.path:
    sys.path.append(project_root)

from database.connection import get_db_connection

def _connect():
    """Crée une connexion à la base de données"""
    conn = get_db_connection()
    return conn

def check_and_add_professeur_principal_column():
    """Vérifie et ajoute la colonne professeur_principal si elle n'existe pas"""
    try:
        conn = _connect()
        if not conn:
            print("❌ Impossible de se connecter à la base de données")
            return False
            
        cursor = conn.cursor()
        
        # Vérifier si la colonne existe
        cursor.execute("""
            SELECT COLUMN_NAME 
            FROM INFORMATION_SCHEMA.COLUMNS 
            WHERE TABLE_NAME = 'classes' AND COLUMN_NAME = 'professeur_principal'
        """)
        
        column_exists = cursor.fetchone() is not None
        
        if not column_exists:
            print("📝 Ajout de la colonne professeur_principal...")
            cursor.execute("""
                ALTER TABLE classes 
                ADD professeur_principal NVARCHAR(255) NULL
            """)
            conn.commit()
            print("✅ Colonne professeur_principal ajoutée avec succès")
        else:
            print("✅ Colonne professeur_principal existe déjà")
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False

def main():
    """Fonction principale"""
    print("🔍 Vérification de la colonne professeur_principal...")
    print("=" * 50)
    
    if check_and_add_professeur_principal_column():
        print("\n✅ Vérification terminée avec succès!")
    else:
        print("\n❌ Échec de la vérification")

if __name__ == "__main__":
    main()

