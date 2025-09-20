from database.connection import get_db_connection
from typing import Optional, Dict, Any, List
import os
import sys

# Ajouter le chemin du projet pour les imports
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../../..'))
if project_root not in sys.path:
    sys.path.append(project_root)

# Chemin de base de données relatif

def _connect():
    """
    Crée et retourne une connexion à la base de données SQLite.
    La connexion est configurée pour retourner des lignes sous forme de dictionnaires
    (objets # sqlite3.Row  # Remplacé par SQL Server) pour un accès par nom de colonne.
    """
    conn = get_db_connection()
    # conn.row_factory = sqlite3.Row  # Remplacé par SQL Server  # Ligne cruciale pour retourner des dictionnaires
    # PRAGMA supprimés pour SQL Server
    return conn

# ====== CACHE MÉMOIRE ======

def preload_classes():
    """Précharge les classes en mémoire (supprimé - système de cache supprimé)"""
    try:
        pass  # Fonction supprimée car le système de cache a été supprimé
    except Exception as e:
        print(f"⚠️ Préchargement classes ignoré: {e}")

def get_all_classes():
    """
    Liste toutes les classes depuis SQL Server.
    
    Returns:
        list: Une liste de dictionnaires, où chaque dictionnaire représente une classe.
    """
    try:
        conn = _connect()
        if not conn:
            print("❌ Impossible de se connecter à la base de données")
            return []
        
        cursor = conn.cursor()
        
        # Vérifier si la table classes existe
        cursor.execute("""
            SELECT COUNT(*) 
            FROM INFORMATION_SCHEMA.TABLES 
            WHERE TABLE_NAME = 'classes'
        """)
        
        table_exists = cursor.fetchone()[0] > 0
        
        if not table_exists:
            print("⚠️ Table 'classes' n'existe pas dans SQL Server")
            return []
        
        # Récupérer toutes les classes
        cursor.execute("""
            SELECT id_classe, nom_classe, niveau, capacite, statut, date_creation
            FROM classes
            ORDER BY nom_classe
        """)
        
        rows = cursor.fetchall()
        
        # Convertir les résultats en dictionnaires
        classes = []
        for row in rows:
            classe_dict = {
                'id': row[0],  # id_classe
                'nom': row[1],  # nom_classe
                'niveau': row[2],  # niveau
                'capacite': row[3],  # capacite
                'statut': row[4],  # statut
                'date_creation': row[5]  # date_creation
            }
            classes.append(classe_dict)
        
        conn.close()
        print(f"✅ {len(classes)} classes récupérées depuis SQL Server")
        return classes
        
    except Exception as e:
        print(f"❌ Erreur get_all_classes: {e}")
        return []

def add_class(nom, niveau, annee_scolaire, prof_id, salle_id):
    """
    Ajoute une nouvelle classes à la base de données.

    Args:
        nom (str): Le nom de la classes.
        niveau (str): Le niveau de la classes.
        annee_scolaire (str): L'année scolaire.
        prof_id (int): L'ID du professeurs principal.
        salle_id (int): L'ID de la salles de classes.
    """
    try:
        conn = _connect()

        if not conn:

            print("❌ Impossible de se connecter à la base de données")

            return

            cur = conn.cursor()
            cur.execute("""INSERT INTO classes (nom, niveau, annee_scolaire, professeur_principal_id, salle_id)
                INSERT INTO classes (nom, niveau, annee_scolaire, professeur_principal_id, salle_id)
                VALUES (?, ?, ?, ?, ?)
            """, (nom, niveau, annee_scolaire, prof_id, salle_id))
            conn.commit()
            conn.close()
            conn.close()
            conn.close()
            conn.close()
            
    except Exception as e:
        print(f"[Classe] Erreur add_class: {e}")

def update_class_data(classe_id, nom, niveau, annee_scolaire, prof_id, salle_id):
    """
    Met à jour les informations d'une classes existante.

    Args:
        classe_id (int): L'ID de la classes à mettre à jour.
        nom (str): Le nouveau nom de la classes.
        niveau (str): Le nouveau niveau.
        annee_scolaire (str): La nouvelle année scolaire.
        prof_id (int): Le nouvel ID du professeurs principal.
        salle_id (int): Le nouvel ID de la salles de classes.
    """
    try:
        conn = _connect()

        if not conn:

            print("❌ Impossible de se connecter à la base de données")

            return

            cur = conn.cursor()
            cur.execute("""
                UPDATE classes
                SET nom=?, niveau=?, annee_scolaire=?, professeur_principal_id=?, salle_id=?
                WHERE id=?
            """, (nom, niveau, annee_scolaire, prof_id, salle_id, classe_id))
            conn.commit()
            conn.close()
            conn.close()
            conn.close()
            conn.close()
            
    except Exception as e:
        print(f"[Classe] Erreur update_class_data: {e}")

def delete_class(classe_id):
    """
    Supprime une classes de la base de données.

    Args:
        classe_id (int): L'ID de la classes à supprimer.
    """
    try:
        conn = _connect()
        if not conn:
            print("❌ Impossible de se connecter à la base de données")
            return
        cur = conn.cursor()
        cur.execute("DELETE FROM classes WHERE id_classe=?", (classe_id,))
        conn.commit()
        conn.close()
        
    except Exception as e:
        print(f"[Classe] Erreur delete_class: {e}")

def get_classe_by_id(classe_id: int) -> Optional[Dict[str, Any]]:
    """
    Retourne les informations d'une classes spécifique en fonction de son ID.

    Args:
        classe_id (int): L'ID de la classes à rechercher.

    Returns:
        dict: Un dictionnaire contenant les informations de la classes, ou None si non trouvée.
    """
    try:
        conn = _connect()

        if not conn:

            print("❌ Impossible de se connecter à la base de données")

            return

            cur = conn.cursor()
            cur.execute("""
                SELECT c.id_classe, c.nom_classe, c.niveau, c.annee_scolaire, c.id_professeur_principal, c.salle_id
                FROM classes c
                WHERE c.id_classe=?
            """, (classe_id,))
            row = cur.fetchone()
            return dict(row) if row else None
    except Exception as e:
        print(f"[Classe] Erreur get_classe_by_id: {e}")
        return None