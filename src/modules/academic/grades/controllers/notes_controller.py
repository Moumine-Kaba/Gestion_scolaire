from database.connection import get_db_connection
import os
import sys

# Ajouter le chemin du projet pour les imports
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../../..'))
if project_root not in sys.path:
    sys.path.append(project_root)

def connect_db():
    """Crée et retourne une connexion à la base de données SQL Server."""
    conn = get_db_connection()
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

def get_all_notes():
    """Récupère toutes les notes depuis SQL Server avec les noms associés."""
    try:
        conn = connect_db()
        if not conn:
            print("❌ Impossible de se connecter à la base de données")
            return []
        
        cursor = conn.cursor()
        
        # Vérifier si la table notes existe
        cursor.execute("""
            SELECT COUNT(*) 
            FROM INFORMATION_SCHEMA.TABLES 
            WHERE TABLE_NAME = 'notes'
        """)
        
        table_exists = cursor.fetchone()[0] > 0
        
        if not table_exists:
            print("⚠️ Table 'notes' n'existe pas dans SQL Server")
            return []
        
        # Récupérer toutes les notes avec jointures
        cursor.execute("""
            SELECT 
                n.id_note, n.id_eleve, n.id_matiere, n.note, n.coefficient,
                n.date_evaluation, n.type_evaluation, n.commentaire,
                e.nom as eleve_nom, e.prenom as eleve_prenom,
                m.nom_matiere as matiere_nom
            FROM notes n
            LEFT JOIN eleves e ON n.id_eleve = e.id_eleve
            LEFT JOIN matieres m ON n.id_matiere = m.id_matiere
            ORDER BY n.date_evaluation DESC, n.id_note DESC
        """)
        
        rows = cursor.fetchall()
        
        # Convertir les résultats en dictionnaires
        notes = []
        for row in rows:
            note_dict = {
                'id': row[0],  # id_note
                'id_eleve': row[1],  # id_eleve
                'id_matiere': row[2],  # id_matiere
                'note': float(row[3]) if row[3] else 0.0,  # note
                'coefficient': float(row[4]) if row[4] else 1.0,  # coefficient
                'date_evaluation': row[5],  # date_evaluation
                'type_evaluation': row[6],  # type_evaluation
                'commentaire': row[7],  # commentaire
                'eleve_nom': row[8],  # eleve_nom
                'eleve_prenom': row[9],  # eleve_prenom
                'matiere_nom': row[10]  # matiere_nom
            }
            notes.append(note_dict)
        
        conn.close()
        print(f"✅ {len(notes)} notes récupérées depuis SQL Server")
        return notes
        
    except Exception as e:
        print(f"❌ Erreur get_all_notes: {e}")
        return []

def add_note(data):
    """
    Ajoute une notes pour un élève et une matière.
    data : dict avec ('id_eleve', 'id_matiere', 'notes', 'coefficient', 'date_evaluation', 'commentaire')
    """
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO notes (id_eleve, id_matiere, note, coefficient, date_evaluation, commentaire)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        data.get('id_eleve') or data.get('eleve_id'),
        data.get('id_matiere') or data.get('matiere_id'),
        data.get('note') or data.get('notes'),
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
        SET id_eleve=?, id_matiere=?, note=?, coefficient=?, date_evaluation=?, commentaire=?
        WHERE id_note=?
    """, (
        data.get('id_eleve') or data.get('eleve_id'),
        data.get('id_matiere') or data.get('matiere_id'),
        data.get('note') or data.get('notes'),
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
    cur.execute("""
        SELECT n.id_note, n.id_eleve, n.id_matiere, n.note, n.coefficient, 
               n.date_evaluation, n.type_evaluation, n.commentaire,
               e.nom + ' ' + e.prenom as eleve_nom,
               m.nom_matiere
        FROM notes n
        LEFT JOIN eleves e ON n.id_eleve = e.id_eleve
        LEFT JOIN matieres m ON n.id_matiere = m.id_matiere
        ORDER BY n.date_evaluation DESC
    """)
    rows = cur.fetchall()
    conn.close()
    
    # Conversion en liste de dictionnaires
    notes = []
    for row in rows:
        note_dict = {
            'id_note': row[0],
            'id_eleve': row[1],
            'id_matiere': row[2],
            'note': row[3],
            'coefficient': row[4],
            'date_evaluation': row[5],
            'type_evaluation': row[6],
            'commentaire': row[7],
            'eleve_nom': row[8] if row[8] else 'Inconnu',
            'matiere_nom': row[9] if row[9] else 'Inconnu'
        }
        notes.append(note_dict)
    
    return notes

def get_notes_by_eleve(eleve_id, limit=50):
    """Retourne les notes pour un élève donné sous forme de liste de dictionnaires (limité pour les performances)."""
    conn = connect_db()
    cur = conn.cursor()
    
    # Construire la requête avec la limite fixe (SQL Server ne supporte pas TOP ?)
    query = f"""
        SELECT TOP {limit} n.id_note, n.id_eleve, n.id_matiere, n.note, n.coefficient, 
               n.date_evaluation, n.type_evaluation, n.commentaire,
               e.nom + ' ' + e.prenom as eleve_nom,
               m.nom_matiere
        FROM notes n
        LEFT JOIN eleves e ON n.id_eleve = e.id_eleve
        LEFT JOIN matieres m ON n.id_matiere = m.id_matiere
        WHERE n.id_eleve = ?
        ORDER BY n.date_evaluation DESC
    """
    
    cur.execute(query, (eleve_id,))
    rows = cur.fetchall()
    conn.close()
    
    # Conversion en liste de dictionnaires
    notes = []
    for row in rows:
        note_dict = {
            'id_note': row[0],
            'id_eleve': row[1],
            'id_matiere': row[2],
            'note': row[3],
            'coefficient': row[4],
            'date_evaluation': row[5],
            'type_evaluation': row[6],
            'commentaire': row[7],
            'eleve_nom': row[8] if row[8] else 'Inconnu',
            'matiere_nom': row[9] if row[9] else 'Inconnu'
        }
        notes.append(note_dict)
    
    return notes

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