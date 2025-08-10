from utils.db_utils import get_connection

def get_all_classes():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, nom, annee_scolaire, professeur_principal_id, salle_id, capacite
        FROM classe
        ORDER BY nom
    """)
    result = cursor.fetchall()
    conn.close()
    return result

def add_class(nom, annee_scolaire, professeur_principal_id=None, salle_id=None, capacite=None):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO classe (nom, annee_scolaire, professeur_principal_id, salle_id, capacite)
            VALUES (?, ?, ?, ?, ?)
        """, (nom, annee_scolaire, professeur_principal_id, salle_id, capacite))
        conn.commit()
        return True
    except Exception as e:
        print(f"[Classe] Erreur add_class : {e}")
        return False
    finally:
        conn.close()

def update_class(id, nom, annee_scolaire, professeur_principal_id, salle_id, capacite):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            UPDATE classe
            SET nom=?, annee_scolaire=?, professeur_principal_id=?, salle_id=?, capacite=?
            WHERE id=?
        """, (nom, annee_scolaire, professeur_principal_id, salle_id, capacite, id))
        conn.commit()
        return True
    except Exception as e:
        print(f"[Classe] Erreur update_class : {e}")
        return False
    finally:
        conn.close()

def delete_class(id):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM classe WHERE id=?", (id,))
        conn.commit()
        return True
    except Exception as e:
        print(f"[Classe] Erreur delete_class : {e}")
        return False
    finally:
        conn.close()
