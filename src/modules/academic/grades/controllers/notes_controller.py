# Remplacé par SQL Server  # Remplacé par SQL Server  # Remplacé par SQL Server  # Remplacé par SQL Server  # Remplacé par SQL Server
from database.connection import get_db_connection
from database.connection import get_db_connection
from database.connection import get_db_connection
import os

# Le chemin de la base de données
DB_PATH = r"database/edumanager.db"

def connect_db():
    """Crée et retourne une connexion à la base de données."""
    conn = get_db_connection()
    # conn.row_factory = sqlite3.Row  # Remplacé par SQL Server
    return conn

def create_table_notes():
    """Crée la table notes si elle n'existe pas, avec les nouveaux champs."""
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS notes (
            id_note INTEGER PRIMARY KEY AUTOINCREMENT,
            id_eleve INTEGER NOT NULL,
            id_matiere INTEGER NOT NULL,
            id_professeur INTEGER,
            notes REAL NOT NULL,
            coefficient REAL DEFAULT 1,
            type_evaluation TEXT,
            date_evaluation DATE,
            commentaire TEXT,
            date_creation TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(id_eleve) REFERENCES eleves(id_eleve),
            FOREIGN KEY(id_matiere) REFERENCES matieres(id_matiere)
        )
    """)
    conn.commit()
    conn.close()

def add_note(data):
    """
    Ajoute une notes pour un élève et une matière.
    data : dict avec ('id_eleve', 'id_matiere', 'notes', 'coefficient', 'date_evaluation', 'commentaire')
    """
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO notes (id_eleve, id_matiere, notes, coefficient, date_evaluation, commentaire)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        data.get('id_eleve') or data.get('eleve_id'),
        data.get('id_matiere') or data.get('matiere_id'),
        data.get('notes'),
        data.get('coefficient'),
        data.get('date_evaluation') or data.get('date'),
        data.get('commentaire')
    ))
    conn.commit()
    conn.close()

def update_note(data):
    """
    Met à jour une notes existante.
    data : dict avec ('id_note', 'id_eleve', 'id_matiere', 'notes', 'coefficient', 'date_evaluation', 'commentaire')
    """
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("""
        UPDATE notes
        SET id_eleve=?, id_matiere=?, notes=?, coefficient=?, date_evaluation=?, commentaire=?
        WHERE id_note=?
    """, (
        data.get('id_eleve') or data.get('eleve_id'),
        data.get('id_matiere') or data.get('matiere_id'),
        data.get('notes'),
        data.get('coefficient'),
        data.get('date_evaluation') or data.get('date'),
        data.get('commentaire'),
        data.get('id_note') or data.get('id')
    ))
    conn.commit()
    conn.close()

def delete_note(note_id):
    """Supprime une notes selon son ID."""
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("DELETE FROM notes WHERE id_note=?", (note_id,))
    conn.commit()
    conn.close()

def get_all_notes():
    """Liste toutes les notes et les retourne sous forme de liste de dictionnaires."""
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM notes ORDER BY date_evaluation DESC")
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
        WHERE id_eleve = ?
        ORDER BY date_evaluation DESC
    """, (eleve_id,))
    rows = cur.fetchall()
    conn.close()
    
    # Conversion en liste de dictionnaires
    return [dict(row) for row in rows]

def get_notes_by_classe_and_matiere(classe_id, matiere_id):
    """
    Retourne les notes d'une matière pour une classes donnée, sous forme de liste de dictionnaires.
    """
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("""
        SELECT n.id_note, n.id_eleve, n.id_matiere, n.notes, n.date_evaluation, n.coefficient, n.commentaire
        FROM notes n
        JOIN eleves e ON n.id_eleve = e.id_eleve
        WHERE e.id_classe = ? AND n.id_matiere = ?
        ORDER BY e.nom, e.prenom
    """, (classe_id, matiere_id))
    rows = cur.fetchall()
    conn.close()
    
    # Conversion en liste de dictionnaires
    return [dict(row) for row in rows]

def get_note(note_id):
    """Retourne une notes précise (par son id) sous forme de dictionnaire, ou None si pas trouvée."""
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM notes WHERE id_note = ?", (note_id,))
    row = cur.fetchone()
    conn.close()
    
    # Conversion en dictionnaire si une ligne est trouvée
    return dict(row) if row else None

if __name__ == "__main__":
    create_table_notes()
    print("✅ Table 'notes' créée (ou vérifiée).")