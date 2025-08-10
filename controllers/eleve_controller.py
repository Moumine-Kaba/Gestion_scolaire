import sqlite3

# Le chemin de la base de données est celui que vous avez spécifié.
# This path is stored in the user's instructions for recall.
DB_PATH = r"C:\Users\Lenovo\Desktop\EduManager+\database\edumanager.db"

def get_all_eleves(classe_id=None):
    """
    Returns a list of all students, or students from a specific class.
    Each student is returned as a dictionary with keys matching the column names.
    """
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # This allows us to access columns by name
    cur = conn.cursor()

    if classe_id:
        cur.execute("""
            SELECT e.id, e.nom, e.prenom, e.sexe, e.date_naissance, e.statut, e.classe_id
            FROM eleves e
            WHERE e.classe_id=?
            ORDER BY e.nom
        """, (classe_id,))
    else:
        cur.execute("""
            SELECT e.id, e.nom, e.prenom, e.sexe, e.date_naissance, e.statut, e.classe_id
            FROM eleves e
            ORDER BY e.nom
        """)

    rows = cur.fetchall()
    conn.close()

    # Convert each sqlite3.Row object into a dictionary before returning
    return [dict(row) for row in rows]

def get_eleve_complet(eleve_id):
    """
    Returns all information about a student by their ID as a dictionary.
    """
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    
    # It's good practice to list columns explicitly
    cur.execute("""
        SELECT id, nom, prenom, sexe, date_naissance, adresse, telephone_parent, 
               email_parent, classe_id, photo_path, date_inscription, statut
        FROM eleves WHERE id=?
    """, (eleve_id,))
    
    row = cur.fetchone()
    conn.close()

    # If a row is found, convert it to a dictionary. Otherwise, return None.
    return dict(row) if row else None

def add_eleve(nom, prenom, sexe, date_naissance, adresse, telephone_parent, email_parent, classe_id, photo_path, date_inscription, statut):
    """
    Adds a new student to the database.
    """
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO eleves (nom, prenom, sexe, date_naissance, adresse, telephone_parent,
        email_parent, classe_id, photo_path, date_inscription, statut)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (nom, prenom, sexe, date_naissance, adresse, telephone_parent, email_parent, classe_id, photo_path, date_inscription, statut))
    conn.commit()
    conn.close()

def update_eleve(eleve_id, nom, prenom, sexe, date_naissance, adresse, telephone_parent, email_parent, classe_id, photo_path, date_inscription, statut):
    """
    Updates an existing student's information in the database.
    """
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
        UPDATE eleves SET nom=?, prenom=?, sexe=?, date_naissance=?, adresse=?, telephone_parent=?,
        email_parent=?, classe_id=?, photo_path=?, date_inscription=?, statut=?
        WHERE id=?
    """, (nom, prenom, sexe, date_naissance, adresse, telephone_parent, email_parent, classe_id, photo_path, date_inscription, statut, eleve_id))
    conn.commit()
    conn.close()

def delete_eleve(eleve_id):
    """
    Deletes a student from the database by their ID.
    """
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("DELETE FROM eleves WHERE id=?", (eleve_id,))
    conn.commit()
    conn.close()