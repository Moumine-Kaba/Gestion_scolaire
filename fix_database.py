#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script pour corriger la base de données et créer les utilisateurs RBAC
"""

import sqlite3
import os
from pathlib import Path

def fix_database():
    """Corriger la base de données"""
    db_path = Path(__file__).parent / "database" / "edumanager.db"
    
    print("🔧 Correction de la base de données...")
    
    try:
        conn = sqlite3.connect(str(db_path), timeout=30)
        cursor = conn.cursor()
        
        # Vérifier si la table utilisateurs existe
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='utilisateurs'")
        if not cursor.fetchone():
            print("❌ Table utilisateurs manquante")
            return False
        
        # Vérifier la structure de la table
        cursor.execute("PRAGMA table_info(utilisateurs)")
        columns = cursor.fetchall()
        print("📋 Colonnes de la table utilisateurs:")
        for col in columns:
            print(f"  - {col[1]} ({col[2]})")
        
        # Créer les utilisateurs RBAC s'ils n'existent pas
        users_data = [
            ("directeur", "directeur123", "directeur@ecole.com", "Dupont", "Jean"),
            ("comptable", "comptable123", "comptable@ecole.com", "Martin", "Marie"),
            ("secretaire", "secretaire123", "secretaire@ecole.com", "Bernard", "Sophie"),
            ("surveillant", "surveillant123", "surveillant@ecole.com", "Petit", "Pierre"),
            ("admin", "admin123", "admin@ecole.com", "Administrateur", "Système")
        ]
        
        for username, password, email, nom, prenom in users_data:
            # Vérifier si l'utilisateur existe
            cursor.execute("SELECT id_utilisateur FROM utilisateurs WHERE nom_utilisateur = ?", (username,))
            if not cursor.fetchone():
                cursor.execute('''
                    INSERT INTO utilisateurs (nom_utilisateur, mot_de_passe, email, nom, prenom)
                    VALUES (?, ?, ?, ?, ?)
                ''', (username, password, email, nom, prenom))
                print(f"✅ Utilisateur créé: {username}")
            else:
                print(f"✅ Utilisateur existe déjà: {username}")
        
        conn.commit()
        conn.close()
        
        print("✅ Base de données corrigée avec succès")
        return True
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False

if __name__ == "__main__":
    fix_database()
