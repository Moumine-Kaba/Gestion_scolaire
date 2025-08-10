import sqlite3
import os

# --- Chemin de la base de données (adapte si besoin) ---
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
DB_PATH = os.path.join(project_root, "database", "edumanager.db")

def connect_db():
    """Crée et retourne une connexion à la base de données."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def create_table():
    """Crée la table des professeurs si elle n'existe pas."""
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS professeurs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nom TEXT NOT NULL,
            prenom TEXT NOT NULL,
            sexe TEXT,
            telephone TEXT,
            email TEXT,
            specialite TEXT,
            photo_path TEXT,
            date_embauche TEXT
        )
    """)
    conn.commit()
    conn.close()

def get_all_professeurs():
    """
    Liste tous les professeurs de la base de données.
    Retourne une liste de dictionnaires.
    """
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("""
        SELECT id, nom, prenom, sexe, telephone, email, specialite, photo_path, date_embauche
        FROM professeurs
        ORDER BY nom
    """)
    rows = cur.fetchall()
    conn.close()
    return [dict(row) for row in rows]

def add_professeur(data):
    """
    Ajoute un nouveau professeur.
    data : dict avec les clés ('nom', 'prenom', 'sexe', 'telephone', 'email', 'specialite', 'photo_path', 'date_embauche')
    """
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO professeurs (nom, prenom, sexe, telephone, email, specialite, photo_path, date_embauche)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        data.get('nom', ''),
        data.get('prenom', ''),
        data.get('sexe', ''),
        data.get('telephone', ''),
        data.get('email', ''),
        data.get('specialite', ''),
        data.get('photo_path', ''),
        data.get('date_embauche', ''),
    ))
    conn.commit()
    conn.close()

def update_professeur(data):
    """
    Met à jour un professeur existant.
    data : dict avec les mêmes clés que add_professeur + 'id'
    """
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("""
        UPDATE professeurs
        SET nom=?, prenom=?, sexe=?, telephone=?, email=?, specialite=?, photo_path=?, date_embauche=?
        WHERE id=?
    """, (
        data.get('nom', ''),
        data.get('prenom', ''),
        data.get('sexe', ''),
        data.get('telephone', ''),
        data.get('email', ''),
        data.get('specialite', ''),
        data.get('photo_path', ''),
        data.get('date_embauche', ''),
        data.get('id', ''),
    ))
    conn.commit()
    conn.close()

def delete_professeur(prof_id):
    """Supprime un professeur selon son ID."""
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("DELETE FROM professeurs WHERE id=?", (prof_id,))
    conn.commit()
    conn.close()

def get_professeur(prof_id):
    """Récupère un professeur par son ID. Retourne un dictionnaire ou None."""
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("""
        SELECT id, nom, prenom, sexe, telephone, email, specialite, photo_path, date_embauche
        FROM professeurs
        WHERE id = ?
    """, (prof_id,))
    row = cur.fetchone()
    conn.close()
    return dict(row) if row else None
