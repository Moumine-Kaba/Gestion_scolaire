# -*- coding: utf-8 -*-
"""
Configuration centralisée de la base de données
"""

from database.connection import get_db_connection
from database.connection import get_db_connection
from database.connection import get_db_connection
import os
# Remplacé par SQL Server  # Remplacé par SQL Server
from pathlib import Path

# Chemin vers la base de données (relatif au projet)
PROJECT_ROOT = Path(__file__).parent.parent.parent
DB_PATH = PROJECT_ROOT / "database" / "edumanager.db"

def get_db_path():
    """Retourne le chemin absolu vers la base de données"""
    return str(DB_PATH.absolute())

def connect_db():
    """Crée une connexion à la base de données"""
    try:
        conn = get_db_connection())
        return conn
    except Exception as e:
        print(f"Erreur de connexion à la base de données: {e}")
        return None

def get_stats_count(table_name: str) -> int:
    """Retourne le nombre d'enregistrements dans une table"""
    try:
        conn = connect_db()
        if not conn:
            return 0
        cursor = conn.cursor()
        cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
        count = cursor.fetchone()[0]
        conn.close()
        return int(count or 0)
    except Exception as e:
        print(f"Erreur lors du comptage de {table_name}: {e}")
        return 0

def get_moyennes_par_matiere():
    """Retourne les moyennes par matière pour le graphique"""
    try:
        conn = connect_db()
        if not conn:
            return []
        cursor = conn.cursor()
        cursor.execute("""
            SELECT m.nom, AVG(n.notes) as moyenne
            FROM matieres m
            LEFT JOIN notes n ON m.id = n.matiere_id
            GROUP BY m.id, m.nom
            HAVING moyenne IS NOT NULL
            ORDER BY moyenne DESC
            LIMIT 6
        """)
        result = cursor.fetchall()
        conn.close()
        return [(row[0], float(row[1])) for row in result]
    except Exception as e:
        print(f"Erreur lors de la récupération des moyennes: {e}")
        return []

def get_recent_events():
    """Retourne les événements récents pour le tableau de bord"""
    try:
        conn = connect_db()
        if not conn:
            return []
        cursor = conn.cursor()
        cursor.execute("""
            SELECT titre, description, date_debut
            FROM calendriers
            WHERE date_debut >= date('now')
            ORDER BY date_debut ASC
            LIMIT 5
        """)
        result = cursor.fetchall()
        conn.close()
        return result
    except Exception as e:
        print(f"Erreur lors de la récupération des événements: {e}")
        return []

def get_user_info(user_id: int = None):
    """Retourne les informations d'un utilisateurs"""
    try:
        conn = connect_db()
        if not conn:
            return None
        cursor = conn.cursor()
        if user_id:
            cursor.execute("SELECT id, username, prenom, nom, roles FROM utilisateurs WHERE id = ?", (user_id,))
        else:
            cursor.execute("SELECT id, username, prenom, nom, roles FROM utilisateurs LIMIT 1")
        result = cursor.fetchone()
        conn.close()
        if result:
            return {
                "id": result[0],
                "username": result[1],
                "prenom": result[2],
                "nom": result[3],
                "roles": result[4]
            }
        return None
    except Exception as e:
        print(f"Erreur lors de la récupération des infos utilisateurs: {e}")
        return None

