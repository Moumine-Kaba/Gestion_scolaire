import sqlite3
from typing import Optional, Dict, Any, List

# Chemin DB
DB_PATH = r"C:\Users\Lenovo\Desktop\EduManager+\database\edumanager.db"

# Colonnes existantes (selon ta capture + lieu_naissance)
SCHEMA_COLUMNS = [
    "id", "nom", "prenom", "sexe", "date_naissance", "lieu_naissance",
    "adresse", "telephone_parent", "email_parent", "classe_id",
    "photo_path", "date_inscription", "statut",
    "telephone", "email",
    "nom_pere", "telephone_pere", "nom_mere", "telephone_mere"
]

# Colonnes qu'on gère via le formulaire (pour insert/update)
FORM_COLUMNS = [
    "nom", "prenom", "sexe", "date_naissance", "lieu_naissance",
    "adresse", "telephone", "email",
    "nom_pere", "telephone_pere", "nom_mere", "telephone_mere",
    "photo_path", "statut", "classe_id",
    # champs parents "globaux" si tu veux les remplir aussi depuis le form
    "telephone_parent", "email_parent",
    # date_inscription en plus (par défaut aujourd'hui si non fourni)
    "date_inscription"
]

def _connect():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

# ---------- SELECT (liste) ----------
def get_all_eleves(classe_id: Optional[int] = None) -> List[Dict[str, Any]]:
    """
    Retourne les élèves (optionnellement filtrés par classe_id) avec un sous-ensemble pour la liste.
    """
    with _connect() as conn:
        cur = conn.cursor()
        base_select = """
            SELECT e.id, e.nom, e.prenom, e.sexe, e.date_naissance, e.statut, e.classe_id
            FROM eleves e
        """
        if classe_id is not None:
            cur.execute(base_select + " WHERE e.classe_id=? ORDER BY e.nom, e.prenom", (classe_id,))
        else:
            cur.execute(base_select + " ORDER BY e.nom, e.prenom")
        rows = cur.fetchall()
        return [dict(r) for r in rows]

# ---------- SELECT (fiche complète) ----------
def get_eleve_complet(eleve_id: int) -> Optional[Dict[str, Any]]:
    """
    Retourne la fiche complète d’un élève (colonnes explicites, conformes à ta table).
    """
    with _connect() as conn:
        cur = conn.cursor()
        cur.execute("""
            SELECT
                id, nom, prenom, sexe, date_naissance, lieu_naissance,
                adresse, telephone_parent, email_parent, classe_id,
                photo_path, date_inscription, statut,
                telephone, email,
                nom_pere, telephone_pere, nom_mere, telephone_mere
            FROM eleves
            WHERE id=?
        """, (eleve_id,))
        row = cur.fetchone()
        return dict(row) if row else None

# ---------- INSERT ----------
def add_eleve(
    nom: str,
    prenom: Optional[str] = None,
    sexe: Optional[str] = None,
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
    classe_id: Optional[int] = None,
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
        "sexe": sexe,
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
        "classe_id": classe_id,
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
        with _connect() as conn:
            cur = conn.cursor()
            cur.execute(
                f"INSERT INTO eleves ({cols_sql}, date_inscription) VALUES ({placeholders}, date('now'))",
                [data[c] for c in cols if c != "date_inscription"]
            )
            conn.commit()
            return cur.lastrowid
    else:
        placeholders = ",".join(["?"] * len(cols))
        collist = ",".join(cols)
        with _connect() as conn:
            cur = conn.cursor()
            cur.execute(
                f"INSERT INTO eleves ({collist}) VALUES ({placeholders})",
                vals
            )
            conn.commit()
            return cur.lastrowid

# ---------- UPDATE ----------
def update_eleve(
    eleve_id: int,
    nom: Optional[str] = None,
    prenom: Optional[str] = None,
    sexe: Optional[str] = None,
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
    classe_id: Optional[int] = None,
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
        "sexe": sexe,
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
        "classe_id": classe_id,
        "telephone_parent": telephone_parent,
        "email_parent": email_parent,
        "date_inscription": date_inscription,
    }

    updates = [(k, v) for k, v in data.items() if v is not None]
    if not updates:
        return

    set_clause = ", ".join([f"{k}=?" for k, _ in updates])
    values = [v for _, v in updates] + [eleve_id]

    with _connect() as conn:
        cur = conn.cursor()
        cur.execute(f"UPDATE eleves SET {set_clause} WHERE id=?", values)
        conn.commit()

# ---------- DELETE ----------
def delete_eleve(eleve_id: int) -> None:
    with _connect() as conn:
        cur = conn.cursor()
        cur.execute("DELETE FROM eleves WHERE id=?", (eleve_id,))
        conn.commit()
