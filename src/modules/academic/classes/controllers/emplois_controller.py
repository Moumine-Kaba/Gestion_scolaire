import sqlite3
# Note : Le chemin de la base de données est maintenant géré par l'instruction de l'utilisateur.
DB_PATH = r"C:\Users\Lenovo\Desktop\EduManager+\database\edumanager.db"

def get_all_emplois():
    """
    Récupère tous les emplois du temps avec les noms
    des matières, professeurs et salles associés.
    """
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
        SELECT e.id, e.jour, e.heure, m.nom, p.nom, s.nom
        FROM emplois_du_temps e
        JOIN matieres m ON e.matiere_id = m.id
        JOIN professeurs p ON e.professeur_id = p.id
        JOIN salles s ON e.salle_id = s.id
        ORDER BY e.jour, e.heure
    """)
    rows = cur.fetchall()
    conn.close()
    return rows

def get_edt_by_classe(classe_id):
    """
    Récupère les emplois du temps pour une classe spécifique.
    (Non utilisée directement dans la vue, mais utile pour d'autres fonctionnalités)
    """
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
        SELECT e.id, e.jour, e.heure, m.nom, p.nom, s.nom
        FROM emplois_du_temps e
        JOIN matieres m ON e.matiere_id = m.id
        JOIN professeurs p ON e.professeur_id = p.id
        JOIN salles s ON e.salle_id = s.id
        WHERE e.classe_id=? 
        ORDER BY e.jour, e.heure
    """, (classe_id,))
    rows = cur.fetchall()
    conn.close()
    return rows

def add_emploi(jour, heure, matiere, prof, salle):
    """
    Ajoute un nouvel emploi du temps à la base de données.
    """
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    
    # Récupérer les IDs à partir des noms
    cur.execute("SELECT id FROM matieres WHERE nom=?", (matiere,))
    matiere_id = cur.fetchone()[0]
    cur.execute("SELECT id FROM professeurs WHERE nom=?", (prof,))
    prof_id = cur.fetchone()[0]
    cur.execute("SELECT id FROM salles WHERE nom=?", (salle,))
    salle_id = cur.fetchone()[0]

    cur.execute("""
        INSERT INTO emplois_du_temps (jour, heure, matiere_id, professeur_id, salle_id)
        VALUES (?, ?, ?, ?, ?)
    """, (jour, heure, matiere_id, prof_id, salle_id))
    conn.commit()
    conn.close()

def update_emploi(emploi_id, jour, heure, matiere, prof, salle):
    """
    Met à jour un emploi du temps existant.
    """
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    # Récupérer les IDs à partir des noms
    cur.execute("SELECT id FROM matieres WHERE nom=?", (matiere,))
    matiere_id = cur.fetchone()[0]
    cur.execute("SELECT id FROM professeurs WHERE nom=?", (prof,))
    prof_id = cur.fetchone()[0]
    cur.execute("SELECT id FROM salles WHERE nom=?", (salle,))
    salle_id = cur.fetchone()[0]

    cur.execute("""
        UPDATE emplois_du_temps
        SET jour=?, heure=?, matiere_id=?, professeur_id=?, salle_id=?
        WHERE id=?
    """, (jour, heure, matiere_id, prof_id, salle_id, emploi_id))
    conn.commit()
    conn.close()

def delete_emploi(emploi_id):
    """
    Supprime un emploi du temps.
    """
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("DELETE FROM emplois_du_temps WHERE id=?", (emploi_id,))
    conn.commit()
    conn.close()