#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Assignation des rôles aux utilisateurs (compatible avec ton schéma)
EduManager+ - Gestion Scolaire

• S'adapte automatiquement :
  - Table 'utilisateurs' (ou 'users' si absente)
  - Clé primaire: id_utilisateur / id / user_id (détection auto)
  - Table 'user_roles' SANS colonne 'assigned_by'
• INSERT OR IGNORE pour éviter les doublons
"""

import os
import sys
import json
import sqlite3
from typing import Optional, Dict, Tuple

# -------------------------------------------------------------------
# Helpers
# -------------------------------------------------------------------

def project_root() -> str:
    return os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

def pick_db_path(cli_db: Optional[str] = None) -> str:
    cands = [cli_db,
             os.path.join(project_root(), "database", "edumanager.db"),
             os.path.join("database", "edumanager.db"),
             os.environ.get("EDUMANAGER_DB", "").strip()]
    for p in cands:
        if p and os.path.exists(p):
            return os.path.abspath(p)
    raise FileNotFoundError("Base edumanager.db introuvable")

def table_exists(conn: sqlite3.Connection, name: str) -> bool:
    return conn.execute(
        "SELECT 1 FROM sqlite_master WHERE type='table' AND name=?",
        (name,)
    ).fetchone() is not None

def table_columns(conn: sqlite3.Connection, table: str) -> Dict[str, Tuple]:
    """Retourne {col_name: (cid, name, type, notnull, dflt_value, pk)}"""
    return {row[1]: row for row in conn.execute(f"PRAGMA table_info({table})").fetchall()}

def utilisateurs_table(conn: sqlite3.Connection) -> Optional[str]:
    if table_exists(conn, "utilisateurs"):
        return "utilisateurs"
    if table_exists(conn, "users"):
        return "users"
    return None

def utilisateurs_pk_name(conn: sqlite3.Connection, table: str) -> str:
    cols = table_columns(conn, table)
    for name in ("id_utilisateur", "id", "user_id"):
        if name in cols:
            return name
    # fallback: prendre la colonne marquée PK
    for name, meta in cols.items():
        if meta[-1] == 1:
            return name
    return "rowid"

def ensure_user_roles(conn: sqlite3.Connection):
    # Ta base a déjà 'user_roles' sans assigned_by ; on respecte ce schéma.
    conn.execute("""
        CREATE TABLE IF NOT EXISTS user_roles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            role_id INTEGER NOT NULL,
            assigned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(user_id, role_id)
        )
    """)

def role_id_by_name(conn: sqlite3.Connection, role_name: str) -> Optional[int]:
    row = conn.execute("SELECT id_role FROM roles WHERE nom = ?", (role_name,)).fetchone()
    return row[0] if row else None

def user_id_by_username(conn: sqlite3.Connection, table: str, pk_col: str, username: str) -> Optional[int]:
    row = conn.execute(f"SELECT {pk_col} FROM {table} WHERE username = ?", (username,)).fetchone()
    return row[0] if row else None

def assign_role(conn: sqlite3.Connection, user_id: int, role_id: int):
    conn.execute(
        "INSERT OR IGNORE INTO user_roles (user_id, role_id) VALUES (?, ?)",
        (user_id, role_id)
    )

# -------------------------------------------------------------------
# Logique principale
# -------------------------------------------------------------------

DEFAULT_MAPPING = {
    # username         # nom du rôle dans la table 'roles'
    "admin":        "Super Administrateur",
    "directeur":    "Directeur",
    "professeur":   "Professeur",
    "secretaire":   "Secrétaire",
    "eleve":        "Élève",
    # ajoute/édite ici selon tes comptes existants
    # "parent":     "Parent",
}

def assign_roles(db_path: Optional[str] = None, mapping: Optional[Dict[str, str]] = None) -> bool:
    db = pick_db_path(db_path)
    print("🔐 Assignation des rôles")
    print("DB :", db)

    if mapping is None:
        mapping = DEFAULT_MAPPING

    with sqlite3.connect(db) as conn:
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON")

        # Tables nécessaires
        if not table_exists(conn, "roles"):
            print("❌ Table 'roles' introuvable. Lance d'abord scripts/init_roles_and_permissions.py")
            return False
        ensure_user_roles(conn)

        utable = utilisateurs_table(conn)
        if not utable:
            print("❌ Table 'utilisateurs' (ou 'users') introuvable.")
            return False
        pk_col = utilisateurs_pk_name(conn, utable)

        # Récapitulatif des utilisateurs
        all_users = conn.execute(f"SELECT {pk_col} AS id, username FROM {utable} ORDER BY username").fetchall()
        print(f"👥 Utilisateurs trouvés : {len(all_users)}")

        assigned = 0
        skipped = 0

        for username, role_name in mapping.items():
            uid = user_id_by_username(conn, utable, pk_col, username)
            if uid is None:
                print(f"  ⚠️ Utilisateur '{username}' introuvable → ignoré")
                skipped += 1
                continue

            rid = role_id_by_name(conn, role_name)
            if rid is None:
                print(f"  ⚠️ Rôle '{role_name}' introuvable → ignoré (username: {username})")
                skipped += 1
                continue

            try:
                assign_role(conn, uid, rid)
                print(f"  ✅ {username} → {role_name}")
                assigned += 1
            except sqlite3.Error as e:
                print(f"  ❌ Échec assignation {username}: {e}")
                skipped += 1

        conn.commit()

        print(f"\n🎯 Récapitulatif: {assigned} assignations, {skipped} ignorées/échouées")

        # Vérification (aperçu)
        print("\n📊 Vérification des assignations (user_roles):")
        try:
            rows = conn.execute("""
                SELECT u.username, r.nom AS role
                FROM user_roles ur
                JOIN roles r ON r.id_role = ur.role_id
                JOIN {table} u ON u.{pk} = ur.user_id
                ORDER BY u.username, r.nom
            """.format(table=utable, pk=pk_col)).fetchall()
            if rows:
                for r in rows:
                    print(f"  - {r['username']} → {r['role']}")
            else:
                print("  (aucune assignation)")
        except sqlite3.Error as e:
            print(f"  ⚠️ Impossible d'afficher les assignations: {e}")

    print("\n✅ Terminé.")
    return True

# -------------------------------------------------------------------
# Entrée
# -------------------------------------------------------------------

if __name__ == "__main__":
    # Options rapides via variables d'environnement (facultatif) :
    #   EDUMANAGER_DB  : chemin custom de la DB
    #   ROLE_MAP_JSON  : JSON dict username->role_name
    db_arg = os.environ.get("EDUMANAGER_DB", "").strip() or None
    map_json = os.environ.get("ROLE_MAP_JSON", "").strip()

    if map_json:
        try:
            user_map = json.loads(map_json)
        except Exception as e:
            print(f"⚠️ ROLE_MAP_JSON invalide, on utilise le mapping par défaut : {e}")
            user_map = None
    else:
        user_map = None

    ok = assign_roles(db_path=db_arg, mapping=user_map)
    sys.exit(0 if ok else 1)
