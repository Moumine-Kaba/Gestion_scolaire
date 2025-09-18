from database.connection import get_db_connection
from database.connection import get_db_connection
from database.connection import get_db_connection
import os
import sys

# Ajouter le chemin du projet pour les imports
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../../..'))
if project_root not in sys.path:
    sys.path.append(project_root)

# Utiliser le gestionnaire de base de données unifié
from database.connection import get_db_connection

def get_all_users():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT id_utilisateur, username, prenom, nom, email, telephone
        FROM utilisateurs
        ORDER BY nom
    """)
    rows = cur.fetchall()
    conn.close()
    return rows

def add_user(username, prenom, nom, email, telephone, password, roles=None, niveau=None):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO utilisateurs (username, prenom, nom, email, telephone, password)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (username, prenom, nom, email, telephone, password))
    conn.commit()
    conn.close()

def update_user(user_id, username, prenom, nom, email, telephone, password, roles=None, niveau=None):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        UPDATE utilisateurs SET username=?, prenom=?, nom=?, email=?, telephone=?, password=?
        WHERE id_utilisateur=?
    """, (username, prenom, nom, email, telephone, password, user_id))
    conn.commit()
    conn.close()

def delete_user(user_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM utilisateurs WHERE id=?", (user_id,))
    conn.commit()
    conn.close()
