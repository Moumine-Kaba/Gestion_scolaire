import sqlite3
import os

# Le chemin de la base de données est correctement récupéré depuis l'historique de nos conversations.
DB_PATH = r"C:\Users\Lenovo\Desktop\EduManager+\database\edumanager.db"

def _connect():
    """
    Crée et retourne une connexion à la base de données SQLite.
    La connexion est configurée pour retourner des lignes sous forme de dictionnaires
    (objets sqlite3.Row) pour un accès par nom de colonne.
    """
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # Ligne cruciale pour retourner des dictionnaires
    return conn

def get_all_classes():
    """
    Liste toutes les classes en tant que dictionnaires.
    
    Returns:
        list: Une liste de dictionnaires, où chaque dictionnaire représente une classe.
    """
    try:
        with _connect() as conn:
            cur = conn.cursor()
            # Utilisation directe de 'c.*' pour récupérer toutes les colonnes,
            # ou lister les colonnes par leur nom d'origine.
            cur.execute("""
                SELECT c.id, c.nom, c.niveau, c.annee_scolaire, c.professeur_principal_id, c.salle_id
                FROM classe c
                ORDER BY c.nom
            """)
            rows = cur.fetchall()
            return [dict(row) for row in rows]
    except Exception as e:
        print(f"[Classe] Erreur get_all_classes: {e}")
        return []

def add_class(nom, niveau, annee_scolaire, prof_id, salle_id):
    """
    Ajoute une nouvelle classe à la base de données.

    Args:
        nom (str): Le nom de la classe.
        niveau (str): Le niveau de la classe.
        annee_scolaire (str): L'année scolaire.
        prof_id (int): L'ID du professeur principal.
        salle_id (int): L'ID de la salle de classe.
    """
    try:
        with _connect() as conn:
            cur = conn.cursor()
            cur.execute("""
                INSERT INTO classe (nom, niveau, annee_scolaire, professeur_principal_id, salle_id)
                VALUES (?, ?, ?, ?, ?)
            """, (nom, niveau, annee_scolaire, prof_id, salle_id))
            conn.commit()
    except Exception as e:
        print(f"[Classe] Erreur add_class: {e}")

def update_class_data(classe_id, nom, niveau, annee_scolaire, prof_id, salle_id):
    """
    Met à jour les informations d'une classe existante.

    Args:
        classe_id (int): L'ID de la classe à mettre à jour.
        nom (str): Le nouveau nom de la classe.
        niveau (str): Le nouveau niveau.
        annee_scolaire (str): La nouvelle année scolaire.
        prof_id (int): Le nouvel ID du professeur principal.
        salle_id (int): Le nouvel ID de la salle de classe.
    """
    try:
        with _connect() as conn:
            cur = conn.cursor()
            cur.execute("""
                UPDATE classe
                SET nom=?, niveau=?, annee_scolaire=?, professeur_principal_id=?, salle_id=?
                WHERE id=?
            """, (nom, niveau, annee_scolaire, prof_id, salle_id, classe_id))
            conn.commit()
    except Exception as e:
        print(f"[Classe] Erreur update_class_data: {e}")

def delete_class(classe_id):
    """
    Supprime une classe de la base de données.

    Args:
        classe_id (int): L'ID de la classe à supprimer.
    """
    try:
        with _connect() as conn:
            cur = conn.cursor()
            cur.execute("DELETE FROM classe WHERE id=?", (classe_id,))
            conn.commit()
    except Exception as e:
        print(f"[Classe] Erreur delete_class: {e}")

def get_classe_by_id(classe_id):
    """
    Retourne les informations d'une classe spécifique en fonction de son ID.

    Args:
        classe_id (int): L'ID de la classe à rechercher.

    Returns:
        dict: Un dictionnaire contenant les informations de la classe, ou None si non trouvée.
    """
    try:
        with _connect() as conn:
            cur = conn.cursor()
            cur.execute("""
                SELECT c.id, c.nom, c.niveau, c.annee_scolaire, c.professeur_principal_id, c.salle_id
                FROM classe c
                WHERE c.id=?
            """, (classe_id,))
            row = cur.fetchone()
            return dict(row) if row else None
    except Exception as e:
        print(f"[Classe] Erreur get_classe_by_id: {e}")
        return None