#!/usr/bin/env python3
"""
Script pour réinitialiser complètement le système de matières guinéennes
- Supprime toutes les matières existantes
- Recrée la table avec la nouvelle structure
- Réinitialise avec les matières par défaut
"""

import sys
import os
sys.path.append('.')

from database.connection import get_db_connection
from src.modules.academic.subjects.models.guinean_subject_model import GuineanSubjectModel

def reset_guinean_subjects():
    """Réinitialise complètement le système de matières guinéennes"""
    print("🔄 Réinitialisation du système de matières guinéennes...")
    print("=" * 60)
    
    try:
        # Connexion à la base de données
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # 1. Supprimer toutes les matières existantes
        print("🗑️  Suppression de toutes les matières existantes...")
        cursor.execute("DELETE FROM guinean_subjects")
        deleted_count = cursor.rowcount
        print(f"✅ {deleted_count} matières supprimées")
        
        # 2. Réinitialiser l'identité de la table (pour SQL Server)
        print("🔄 Réinitialisation de l'identité de la table...")
        cursor.execute("DBCC CHECKIDENT ('guinean_subjects', RESEED, 0)")
        print("✅ Identité réinitialisée")
        
        # 3. Valider les changements
        conn.commit()
        print("✅ Changements validés")
        
        # 4. Recréer le modèle et initialiser les données
        print("🏗️  Recréation du modèle et initialisation...")
        model = GuineanSubjectModel()
        
        # Recréer la table (au cas où il y aurait des changements de structure)
        print("🔧 Recréation de la table...")
        model.create_table()
        
        # Initialiser avec les données par défaut
        print("📚 Initialisation des matières par défaut...")
        model.initialize_default_data()
        
        print("✅ Données par défaut initialisées")
        
        # 5. Vérifier le résultat
        print("🔍 Vérification du résultat...")
        subjects_count = model.get_all_subjects()
        print(f"✅ {len(subjects_count)} matières créées")
        
        # Statistiques par niveau
        stats = model.get_education_levels()
        print(f"📊 Niveaux disponibles: {len(stats)}")
        for level in stats:
            level_subjects = model.get_subjects_by_level(level)
            print(f"   • {level}: {len(level_subjects)} matières")
        
        conn.close()
        
        print("\n🎉 RÉINITIALISATION TERMINÉE AVEC SUCCÈS !")
        print("=" * 60)
        print("✅ Toutes les matières ont été supprimées")
        print("✅ Table réinitialisée")
        print("✅ Nouvelles matières créées avec la structure guinéenne")
        print("✅ Système prêt pour l'utilisation")
        
    except Exception as e:
        print(f"❌ Erreur lors de la réinitialisation: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return True

if __name__ == "__main__":
    success = reset_guinean_subjects()
    if success:
        print("\n🚀 Vous pouvez maintenant utiliser le système de matières mis à jour !")
    else:
        print("\n💥 Échec de la réinitialisation. Vérifiez les erreurs ci-dessus.")
