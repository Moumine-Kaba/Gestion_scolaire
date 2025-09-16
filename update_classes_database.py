#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script pour mettre à jour la table classes dans la base de données
Supprime les classes existantes et insère la nouvelle structure PRIMAIRE/COLLÈGE/LYCÉE
"""

import sqlite3
import os

# Chemin vers la base de données
DB_PATH = r"C:\Users\Lenovo\Desktop\Clonage_git\Gestion_scolaire\Gestion_scolaire\database\edumanager.db"

def update_classes_table():
    """Met à jour la table classes avec la nouvelle structure"""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        print("🔄 Mise à jour de la table classes...")
        
        # Supprimer toutes les classes existantes
        cursor.execute("DELETE FROM classes")
        print("✅ Classes existantes supprimées")
        
        # Structure des nouvelles classes
        classes_data = [
            # PRIMAIRE
            ("1°", "1° Année", "PRIMAIRE"),
            ("2°", "2° Année", "PRIMAIRE"),
            ("3°", "3° Année", "PRIMAIRE"),
            ("4°", "4° Année", "PRIMAIRE"),
            ("5°", "5° Année", "PRIMAIRE"),
            ("6°", "6° Année", "PRIMAIRE"),
            
            # COLLÈGE
            ("7°", "7° Année", "COLLÈGE"),
            ("8°", "8° Année", "COLLÈGE"),
            ("9°", "9° Année", "COLLÈGE"),
            ("10°", "10° Année (BEPC)", "COLLÈGE"),
            
            # LYCÉE
            ("11 SE", "11° Sciences Exactes", "LYCÉE"),
            ("11 SM", "11° Sciences Mathématiques", "LYCÉE"),
            ("11 SS", "11° Sciences Sociales", "LYCÉE"),
            ("12 SE", "12° Sciences Exactes", "LYCÉE"),
            ("12 SM", "12° Sciences Mathématiques", "LYCÉE"),
            ("12 SS", "12° Sciences Sociales", "LYCÉE"),
            ("TSE", "Terminale Sciences Exactes", "LYCÉE"),
            ("TSM", "Terminale Sciences Mathématiques", "LYCÉE"),
            ("TSS", "Terminale Sciences Sociales", "LYCÉE")
        ]
        
        # Insérer les nouvelles classes
        for code, nom, niveau in classes_data:
            cursor.execute("""
                INSERT INTO classes (nom_classe, niveau, effectif, annee_scolaire, statut, date_creation)
                VALUES (?, ?, 0, '2024-2025', 'Active', datetime('now'))
            """, (nom, niveau))
        
        # Valider les changements
        conn.commit()
        print(f"✅ {len(classes_data)} nouvelles classes insérées")
        
        # Vérifier le résultat
        cursor.execute("SELECT COUNT(*) FROM classes")
        count = cursor.fetchone()[0]
        print(f"📊 Total des classes dans la base: {count}")
        
        # Afficher les classes par niveau
        cursor.execute("SELECT niveau, COUNT(*) FROM classes GROUP BY niveau ORDER BY niveau")
        niveaux = cursor.fetchall()
        
        print("\n📚 Répartition par niveau:")
        for niveau, count in niveaux:
            print(f"   {niveau}: {count} classe(s)")
        
        conn.close()
        print("\n🎉 Mise à jour terminée avec succès!")
        
    except Exception as e:
        print(f"❌ Erreur lors de la mise à jour: {e}")
        if conn:
            conn.rollback()
            conn.close()

if __name__ == "__main__":
    print("🏫 Mise à jour de la structure des classes")
    print("=" * 50)
    update_classes_table()
