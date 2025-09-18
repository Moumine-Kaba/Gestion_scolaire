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

from typing import Optional, Dict, Any, List

# Chemin DB
DB_PATH = r"database/edumanager.db"

# Colonnes existantes (selon ta capture)
SCHEMA_COLUMNS = [
    "id_eleve", "nom", "prenom", "genre", "date_naissance",
    "adresse", "telephone_parent", "email_parent", "id_classe",
    "photo_path", "date_inscription", "statut",
    "telephone", "email",
    "nom_pere", "telephone_pere", "nom_mere", "telephone_mere"
]

# Colonnes qu'on gère via le formulaire (pour insert/update)
FORM_COLUMNS = [
    "nom", "prenom", "genre", "date_naissance",
    "adresse", "telephone", "email",
    "nom_pere", "telephone_pere", "nom_mere", "telephone_mere",
    "photo_path", "statut", "id_classe",
    # champs parents "globaux" si tu veux les remplir aussi depuis le form
    "telephone_parent", "email_parent",
    # date_inscription en plus (par défaut aujourd'hui si non fourni)
    "date_inscription"
]

def _connect():
    conn = get_db_connection()
    # conn.row_factory = sqlite3.Row  # Remplacé par SQL Server
    return conn

# ====== CACHE MÉMOIRE ======

def preload_eleves():
    """Précharge les élèves en mémoire (supprimé - système de cache supprimé)"""
    try:
        pass  # Fonction supprimée car le système de cache a été supprimé
    except Exception as e:
        print(f"⚠️ Préchargement élèves ignoré: {e}")

# ---------- SELECT (liste) ----------
def get_all_eleves(classe_id: Optional[int] = None) -> List[Dict[str, Any]]:
    """
    Retourne les élèves (optionnellement filtrés par classe_id) avec un sous-ensemble pour la liste.
    """
    if classe_id is None and None is not None:
        return _CACHE["eleves_all"]
    conn = _connect()

    if not conn:

        print("❌ Impossible de se connecter à la base de données")

        return

        cur = conn.cursor()
        base_select = """
            SELECT e.id_eleve as id, e.nom, e.prenom, e.genre as sexe, e.date_naissance, e.statut, e.id_classe as classe_id
            FROM eleves e
        """
        if classe_id is not None:
            cur.execute(base_select + " WHERE e.id_classe=? ORDER BY e.nom, e.prenom", (classe_id,))
        else:
            cur.execute(base_select + " ORDER BY e.nom, e.prenom")
        rows = cur.fetchall()
        data = [dict(r) for r in rows]
        if classe_id is None:
            pass  # Pas d'action spéciale pour toutes les classes
        
        return data

# ---------- SELECT (fiche complète) ----------
def get_eleve_complet(eleve_id: int) -> Optional[Dict[str, Any]]:
    """
    Retourne la fiche complète d’un élève (colonnes explicites, conformes à ta table).
    """
    conn = _connect()

    if not conn:

        print("❌ Impossible de se connecter à la base de données")

        return

        cur = conn.cursor()
        cur.execute("""
            SELECT
                id_eleve as id, nom, prenom, genre as sexe, date_naissance,
                adresse, telephone_parent, email_parent, id_classe as classe_id,
                photo_path, date_inscription, statut,
                telephone, email,
                nom_pere, telephone_pere, nom_mere, telephone_mere
            FROM eleves
            WHERE id_eleve=?
        """, (eleve_id,))
        row = cur.fetchone()
        return dict(row) if row else None

# ---------- INSERT ----------
def add_eleve(
    nom: str,
    prenom: Optional[str] = None,
    genre: Optional[str] = None,
    date_naissance: Optional[str] = None,
    lieu_naissance: Optional[str] = None,
    adresse: Optional[str] = None,
    telephone: Optional[str] = None,
    email: Optional[str] = None,
    nom_pere: Optional[str] = None,
    telephone_pere: Optional[str] = None,
    nom_mere: Optional[str] = None,
    telephone_mere: Optional[str] = None,
    photo_path: Optional[str] = None,
    statut: Optional[str] = None,
    id_classe: Optional[int] = None,
    telephone_parent: Optional[str] = None,
    email_parent: Optional[str] = None,
    date_inscription: Optional[str] = None,  # si None -> date('now')
) -> int:
    """
    Ajoute un élève. Retourne l'ID inséré.
    """
    data = {
        "nom": nom,
        "prenom": prenom,
        "genre": genre,
        "date_naissance": date_naissance,
        "lieu_naissance": lieu_naissance,
        "adresse": adresse,
        "telephone": telephone,
        "email": email,
        "nom_pere": nom_pere,
        "telephone_pere": telephone_pere,
        "nom_mere": nom_mere,
        "telephone_mere": telephone_mere,
        "photo_path": photo_path,
        "statut": statut,
        "id_classe": id_classe,
        "telephone_parent": telephone_parent,
        "email_parent": email_parent,
        "date_inscription": date_inscription
    }

    cols = [c for c in FORM_COLUMNS if c in data]
    vals = [data[c] for c in cols]

    # gérer la valeur par défaut de date_inscription
    if "date_inscription" in cols and data["date_inscription"] is None:
        # on remplace par la fonction SQLite
        cols_sql = ",".join([c for c in cols if c != "date_inscription"])
        placeholders = ",".join(["?"] * (len(cols) - 1))
        conn = _connect()

        if not conn:

            print("❌ Impossible de se connecter à la base de données")

            return

            cur = conn.cursor()
            cur.execute(f"INSERT INTO eleves ({cols_sql}, date_inscription) VALUES ({placeholders}, date('now'))",
                [data[c] for c in cols if c != "date_inscription"]
            )
            conn.commit()
            conn.close()
            
            return cur.lastrowid
    else:
        placeholders = ",".join(["?"] * len(cols))
        collist = ",".join(cols)
        conn = _connect()

        if not conn:

            print("❌ Impossible de se connecter à la base de données")

            return

            cur = conn.cursor()
            cur.execute(f"INSERT INTO eleves ({collist}) VALUES ({placeholders})",
                f"INSERT INTO eleves ({collist}) VALUES ({placeholders})",
                vals
            )
            conn.commit()
            conn.close()
            
            return cur.lastrowid

# ---------- UPDATE ----------
def update_eleve(
    eleve_id: int,
    nom: Optional[str] = None,
    prenom: Optional[str] = None,
    genre: Optional[str] = None,
    date_naissance: Optional[str] = None,
    lieu_naissance: Optional[str] = None,
    adresse: Optional[str] = None,
    telephone: Optional[str] = None,
    email: Optional[str] = None,
    nom_pere: Optional[str] = None,
    telephone_pere: Optional[str] = None,
    nom_mere: Optional[str] = None,
    telephone_mere: Optional[str] = None,
    photo_path: Optional[str] = None,
    statut: Optional[str] = None,
    id_classe: Optional[int] = None,
    telephone_parent: Optional[str] = None,
    email_parent: Optional[str] = None,
    date_inscription: Optional[str] = None,  # on évite de le modifier en général
) -> None:
    """
    Met à jour un élève. Les paramètres None ne modifient pas la colonne.
    """
    data = {
        "nom": nom,
        "prenom": prenom,
        "genre": genre,
        "date_naissance": date_naissance,
        "lieu_naissance": lieu_naissance,
        "adresse": adresse,
        "telephone": telephone,
        "email": email,
        "nom_pere": nom_pere,
        "telephone_pere": telephone_pere,
        "nom_mere": nom_mere,
        "telephone_mere": telephone_mere,
        "photo_path": photo_path,
        "statut": statut,
        "id_classe": id_classe,
        "telephone_parent": telephone_parent,
        "email_parent": email_parent,
        "date_inscription": date_inscription,
    }

    updates = [(k, v) for k, v in data.items() if v is not None]
    if not updates:
        return

    set_clause = ", ".join([f"{k}=?" for k, _ in updates])
    values = [v for _, v in updates] + [eleve_id]

    conn = _connect()

    if not conn:

        print("❌ Impossible de se connecter à la base de données")

        return

        cur = conn.cursor()
        cur.execute(f"UPDATE eleves SET {set_clause} WHERE id_eleve=?", values)
        conn.commit()
        conn.close()

# ---------- DELETE ----------
def delete_eleve(eleve_id: int) -> None:
    conn = _connect()

    if not conn:

        print("❌ Impossible de se connecter à la base de données")

        return

        cur = conn.cursor()
        cur.execute("DELETE FROM eleves WHERE id_eleve=?", (eleve_id,))
        conn.commit()
        conn.close()
    
    _invalidate_cache()
