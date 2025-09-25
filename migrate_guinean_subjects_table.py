# -*- coding: utf-8 -*-
"""
Script de Migration de la Table des Matières Guinéennes
EduManager+ - Mise à Jour de la Structure

Ce script met à jour la structure de la table pour supporter
des codes de matières plus longs.
"""

import os
import sys

# Ajouter le chemin du projet
project_root = os.path.abspath(os.path.dirname(__file__))
if project_root not in sys.path:
    sys.path.append(project_root)

def migrate_guinean_subjects_table():
    """Met à jour la structure de la table guinean_subjects"""
    try:
        print("🔄 Migration de la table des matières guinéennes...")
        print("=" * 60)
        
        # Import du module de base de données
        from database.connection import get_db_connection
        
        conn = get_db_connection()
        if not conn:
            print("❌ Impossible de se connecter à la base de données")
            return False
        
        cursor = conn.cursor()
        
        # Vérifier si la table existe
        cursor.execute("""
            SELECT COUNT(*) 
            FROM INFORMATION_SCHEMA.TABLES 
            WHERE TABLE_NAME = 'guinean_subjects'
        """)
        
        table_exists = cursor.fetchone()[0] > 0
        
        if table_exists:
            print("   • Table 'guinean_subjects' trouvée")
            
            # Vérifier la taille actuelle de la colonne code
            cursor.execute("""
                SELECT CHARACTER_MAXIMUM_LENGTH 
                FROM INFORMATION_SCHEMA.COLUMNS 
                WHERE TABLE_NAME = 'guinean_subjects' AND COLUMN_NAME = 'code'
            """)
            
            current_size = cursor.fetchone()
            if current_size:
                print(f"   • Taille actuelle de la colonne 'code' : {current_size[0]}")
                
                if current_size[0] < 100:
                    print("   • Mise à jour de la taille de la colonne 'code'...")
                    
                    # Modifier la taille de la colonne
                    cursor.execute("ALTER TABLE guinean_subjects ALTER COLUMN code NVARCHAR(100) NOT NULL")
                    print("   ✅ Colonne 'code' mise à jour vers NVARCHAR(100)")
                else:
                    print("   • Colonne 'code' déjà à la bonne taille")
            else:
                print("   • Colonne 'code' non trouvée")
        
        else:
            print("   • Table 'guinean_subjects' n'existe pas encore")
            print("   • Création de la table avec la nouvelle structure...")
            
            # Créer la table avec la bonne structure
            cursor.execute("""
                CREATE TABLE guinean_subjects (
                    id INT IDENTITY(1,1) PRIMARY KEY,
                    code NVARCHAR(100) NOT NULL UNIQUE,
                    name NVARCHAR(200) NOT NULL,
                    description NVARCHAR(500),
                    coefficient DECIMAL(3,2) DEFAULT 1.0,
                    education_level NVARCHAR(20) NOT NULL,
                    grade NVARCHAR(50) NOT NULL,
                    series NVARCHAR(100),
                    is_optional BIT DEFAULT 0,
                    is_core BIT DEFAULT 1,
                    is_active BIT DEFAULT 1,
                    date_created DATETIME DEFAULT GETDATE(),
                    date_updated DATETIME DEFAULT GETDATE()
                )
            """)
            
            # Créer les index
            cursor.execute("""
                CREATE INDEX IX_guinean_subjects_level_grade 
                ON guinean_subjects (education_level, grade)
            """)
            
            cursor.execute("""
                CREATE INDEX IX_guinean_subjects_code 
                ON guinean_subjects (code)
            """)
            
            print("   ✅ Table créée avec la nouvelle structure")
        
        conn.commit()
        conn.close()
        
        print("✅ Migration terminée avec succès")
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors de la migration : {e}")
        return False

def main():
    """Fonction principale"""
    print("🔄 EduManager+ - Migration de la Table des Matières")
    print("=" * 55)
    
    if migrate_guinean_subjects_table():
        print("\n✅ Migration terminée avec succès !")
        print("   La table est maintenant prête pour les données.")
        return True
    else:
        print("\n❌ Échec de la migration")
        return False

if __name__ == "__main__":
    success = main()
    if not success:
        sys.exit(1)
