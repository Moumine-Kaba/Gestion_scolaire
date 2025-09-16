import sqlite3
import os

# Le chemin de la base de données est celui que vous avez fourni
DB_PATH = r"C:\Users\Lenovo\Desktop\EduManager+\database\edumanager.db"

def connect_db():
    """Crée et retourne une connexion à la base de données."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def create_table_notes():
    """Crée la table notes si elle n'existe pas, avec les nouveaux champs."""
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            eleve_id INTEGER NOT NULL,
            matiere_id INTEGER NOT NULL,
            note REAL NOT NULL,
            coefficient REAL DEFAULT 1,
            date TEXT,
            commentaire TEXT,
            FOREIGN KEY(eleve_id) REFERENCES eleves(id),
            FOREIGN KEY(matiere_id) REFERENCES matieres(id)
        )
    """)
    conn.commit()
    conn.close()

def add_note(data):
    """
    Ajoute une note pour un élève et une matière.
    data : dict avec ('eleve_id', 'matiere_id', 'note', 'coefficient', 'date', 'commentaire')
    """
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO notes (eleve_id, matiere_id, note, coefficient, date, commentaire)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        data.get('eleve_id'),
        data.get('matiere_id'),
        data.get('note'),
        data.get('coefficient'),
        data.get('date'),
        data.get('commentaire')
    ))
    conn.commit()
    conn.close()

def update_note(data):
    """
    Met à jour une note existante.
    data : dict avec ('id', 'eleve_id', 'matiere_id', 'note', 'coefficient', 'date', 'commentaire')
    """
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("""
        UPDATE notes
        SET eleve_id=?, matiere_id=?, note=?, coefficient=?, date=?, commentaire=?
        WHERE id=?
    """, (
        data.get('eleve_id'),
        data.get('matiere_id'),
        data.get('note'),
        data.get('coefficient'),
        data.get('date'),
        data.get('commentaire'),
        data.get('id')
    ))
    conn.commit()
    conn.close()

def delete_note(note_id):
    """Supprime une note selon son ID."""
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("DELETE FROM notes WHERE id=?", (note_id,))
    conn.commit()
    conn.close()

def get_all_notes():
    """Liste toutes les notes et les retourne sous forme de liste de dictionnaires."""
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM notes ORDER BY date DESC")
    rows = cur.fetchall()
    conn.close()
    
    # Conversion en liste de dictionnaires
    return [dict(row) for row in rows]

def get_notes_by_eleve(eleve_id):
    """Retourne toutes les notes pour un élève donné sous forme de liste de dictionnaires."""
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("""
        SELECT *
        FROM notes
        WHERE eleve_id = ?
        ORDER BY date DESC
    """, (eleve_id,))
    rows = cur.fetchall()
    conn.close()
    
    # Conversion en liste de dictionnaires
    return [dict(row) for row in rows]

def get_notes_by_classe_and_matiere(classe_id, matiere_id):
    """
    Retourne les notes d'une matière pour une classe donnée, sous forme de liste de dictionnaires.
    """
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("""
        SELECT n.id, n.eleve_id, n.matiere_id, n.note, n.date, n.coefficient, n.commentaire
        FROM notes n
        JOIN eleves e ON n.eleve_id = e.id
        WHERE e.classe_id = ? AND n.matiere_id = ?
        ORDER BY e.nom, e.prenom
    """, (classe_id, matiere_id))
    rows = cur.fetchall()
    conn.close()
    
    # Conversion en liste de dictionnaires
    return [dict(row) for row in rows]

def get_note(note_id):
    """Retourne une note précise (par son id) sous forme de dictionnaire, ou None si pas trouvée."""
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM notes WHERE id = ?", (note_id,))
    row = cur.fetchone()
    conn.close()
    
    # Conversion en dictionnaire si une ligne est trouvée
    return dict(row) if row else None

if __name__ == "__main__":
    create_table_notes()
    print("✅ Table 'notes' créée (ou vérifiée).")