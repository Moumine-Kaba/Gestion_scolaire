# -*- coding: utf-8 -*-
"""
Script de Nettoyage de la Base de Données des Matières Guinéennes
EduManager+ - Réinitialisation Complète

Ce script nettoie la base de données pour permettre une réinitialisation
complète du système de matières guinéennes.
"""

import os
import sys

# Ajouter le chemin du projet
project_root = os.path.abspath(os.path.dirname(__file__))
if project_root not in sys.path:
    sys.path.append(project_root)

def clean_guinean_subjects_database():
    """Nettoie la base de données des matières guinéennes"""
    try:
        print("🧹 Nettoyage de la base de données des matières guinéennes...")
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
            
            # Compter les enregistrements existants
            cursor.execute("SELECT COUNT(*) FROM guinean_subjects")
            count = cursor.fetchone()[0]
            print(f"   • {count} enregistrements trouvés")
            
            # Supprimer tous les enregistrements
            cursor.execute("DELETE FROM guinean_subjects")
            print("   • Tous les enregistrements supprimés")
            
            # Réinitialiser l'identité (auto-increment)
            cursor.execute("DBCC CHECKIDENT('guinean_subjects', RESEED, 0)")
            print("   • Compteur d'identité réinitialisé")
            
        else:
            print("   • Table 'guinean_subjects' n'existe pas encore")
        
        conn.commit()
        conn.close()
        
        print("✅ Nettoyage terminé avec succès")
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors du nettoyage : {e}")
        return False

def main():
    """Fonction principale"""
    print("🧹 EduManager+ - Nettoyage de la Base de Données")
    print("=" * 50)
    
    if clean_guinean_subjects_database():
        print("\n✅ Base de données nettoyée avec succès !")
        print("   Vous pouvez maintenant réinitialiser le système.")
        return True
    else:
        print("\n❌ Échec du nettoyage")
        return False

if __name__ == "__main__":
    success = main()
    if not success:
        sys.exit(1)
