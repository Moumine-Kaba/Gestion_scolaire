#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Initialisation des rôles & permissions (compatible avec ton schéma)
EduManager+ - Gestion Scolaire
"""

import os
import sqlite3
from typing import Iterable, Sequence

# ----------------------------- Helpers -----------------------------

def project_root() -> str:
    return os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

def pick_db_path() -> str:
    cands = [
        os.path.join(project_root(), "database", "edumanager.db"),
        os.path.join("database", "edumanager.db"),
        os.environ.get("EDUMANAGER_DB", "").strip(),
    ]
    for p in cands:
        if p and os.path.exists(p):
            return os.path.abspath(p)
    raise FileNotFoundError("edumanager.db introuvable")

def cols(conn: sqlite3.Connection, table: str) -> set:
    try:
        return {r[1] for r in conn.execute(f"PRAGMA table_info({table})").fetchall()}
    except sqlite3.Error:
        return set()

def run(conn: sqlite3.Connection, sql: str, params: Sequence = ()):
    try:
        conn.execute(sql, params)
    except sqlite3.Error as e:
        print(f"\n[SQL ERROR] {e}\n  -> SQL: {sql}\n  -> Params: {params}\n")
        raise

def run_many(conn: sqlite3.Connection, sql: str, rows: Iterable[Sequence]):
    try:
        conn.executemany(sql, rows)
    except sqlite3.Error as e:
        print(f"\n[SQL ERROR] {e}\n  -> SQL (executemany): {sql}\n")
        raise

# ------------------------- DDL (tables) --------------------------

def ensure_roles(conn: sqlite3.Connection):
    run(conn, """
        CREATE TABLE IF NOT EXISTS roles (
            id_role INTEGER PRIMARY KEY AUTOINCREMENT,
            nom TEXT UNIQUE NOT NULL,
            description TEXT,
            permissions TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    # Ajout optionnel de 'niveau' si tu veux l'utiliser plus tard
    if "niveau" not in cols(conn, "roles"):
        try:
            run(conn, "ALTER TABLE roles ADD COLUMN niveau INTEGER DEFAULT 1")
        except sqlite3.Error:
            pass

def ensure_user_roles(conn: sqlite3.Connection):
    # IMPORTANT: ta table existe déjà SANS assigned_by → on ne l’impose pas.
    run(conn, """
        CREATE TABLE IF NOT EXISTS user_roles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            role_id INTEGER NOT NULL,
            assigned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(user_id, role_id)
        )
    """)

def ensure_available_views(conn: sqlite3.Connection):
    run(conn, """
        CREATE TABLE IF NOT EXISTS available_views (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            view_name TEXT UNIQUE NOT NULL,
            view_title TEXT NOT NULL,
            view_description TEXT,
            module TEXT NOT NULL,
            is_active BOOLEAN DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

def ensure_user_view_access(conn: sqlite3.Connection):
    run(conn, """
        CREATE TABLE IF NOT EXISTS user_view_access (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            view_name TEXT NOT NULL,
            access_level TEXT DEFAULT 'read',
            granted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            granted_by INTEGER,
            UNIQUE(user_id, view_name)
        )
    """)

# ------------------------- Données par défaut ---------------------

DEFAULT_ROLES = [
    (1, "Super Administrateur", "Accès complet à tous les modules",              "read,write,delete,admin", 10),
    (2, "Administrateur",       "Gestion complète de l'établissement",           "read,write,delete",        9),
    (3, "Directeur",            "Gestion des classes, élèves et professeurs",    "read,write",               8),
    (4, "Professeur",           "Notes, présences, bulletins",                   "read,write",               7),
    (5, "Secrétaire",           "Gestion administrative & inscriptions",         "read,write",               6),
    (6, "Élève",                "Consultation des notes et bulletins",           "read",                     5),
    (7, "Parent",               "Consultation des infos de l'élève",             "read",                     4),
]

DEFAULT_VIEWS = [
    ("dashboard",   "Tableau de bord",  "Vue principale de l'application", "SCOLARITÉ"),
    ("eleves",      "Élèves",           "Gestion des élèves",              "SCOLARITÉ"),
    ("profs",       "Professeurs",      "Gestion des professeurs",         "SCOLARITÉ"),
    ("classes",     "Classes",          "Gestion des classes",             "SCOLARITÉ"),
    ("salles",      "Salles",           "Gestion des salles",              "SCOLARITÉ"),
    ("enseignements","Enseignements",   "Gestion des enseignements",       "PÉDAGOGIE"),
    ("matieres",    "Matières",         "Gestion des matières",            "PÉDAGOGIE"),
    ("notes",       "Notes",            "Gestion des notes",               "PÉDAGOGIE"),
    ("presences",   "Présences",        "Gestion des présences",           "PÉDAGOGIE"),
    ("bulletins",   "Bulletins",        "Gestion des bulletins",           "PÉDAGOGIE"),
    ("emplois",     "Emplois du temps", "Gestion des emplois du temps",    "PÉDAGOGIE"),
    ("paiements",   "Paiements",        "Gestion des paiements",           "FINANCES"),
    ("utilisateurs","Utilisateurs",     "Gestion des utilisateurs",        "ADMINISTRATION"),
    ("actualites",  "Actualités",       "Gestion des actualités",          "ADMINISTRATION"),
    ("annonces",    "Annonces",         "Gestion des annonces",            "ADMINISTRATION"),
    ("notifications","Notifications",   "Gestion des notifications",       "ADMINISTRATION"),
    ("taches",      "Tâches",           "Gestion des tâches",              "ADMINISTRATION"),
    ("biblio",      "Bibliothèque",     "Gestion de la bibliothèque",      "OUTILS"),
    ("calendriers", "Calendriers",      "Gestion des calendriers",         "OUTILS"),
    ("carrieres",   "Carrières",        "Gestion des carrières",           "OUTILS"),
    ("competences", "Compétences",      "Gestion des compétences",         "OUTILS"),
    ("documents",   "Documents",        "Gestion des documents",           "OUTILS"),
    ("maintenances","Maintenance",      "Gestion de la maintenance",       "OUTILS"),
    ("messagerie",  "Messagerie",       "Gestion de la messagerie",        "OUTILS"),
    ("objectifs",   "Objectifs",        "Gestion des objectifs",           "OUTILS"),
    ("personnel",   "Personnel",        "Gestion du personnel",            "OUTILS"),
    ("transfert",   "Transfert",        "Gestion des transferts",          "OUTILS"),
    ("settings",    "Paramètres",       "Paramètres du système",           "OUTILS"),
]

def seed_roles(conn: sqlite3.Connection):
    c = cols(conn, "roles")
    has_niveau = "niveau" in c
    for rid, nom, desc, perms, level in DEFAULT_ROLES:
        if has_niveau:
            run(conn, """
                INSERT OR IGNORE INTO roles (id_role, nom, description, permissions, niveau)
                VALUES (?, ?, ?, ?, ?)
            """, (rid, nom, desc, perms, level))
        else:
            run(conn, """
                INSERT OR IGNORE INTO roles (id_role, nom, description, permissions)
                VALUES (?, ?, ?, ?)
            """, (rid, nom, desc, perms))
    print(f"  ✅ Rôles par défaut prêts ({len(DEFAULT_ROLES)} entrées traitées)")

def seed_views(conn: sqlite3.Connection):
    run_many(conn, """
        INSERT OR IGNORE INTO available_views (view_name, view_title, view_description, module)
        VALUES (?, ?, ?, ?)
    """, DEFAULT_VIEWS)
    print(f"  ✅ Vues disponibles prêtes ({len(DEFAULT_VIEWS)} entrées)")

# ----------------------- Users & Assignations ----------------------

def utilisateurs_table(conn: sqlite3.Connection) -> str | None:
    # On préfère 'utilisateurs' s'il existe
    names = {r[0] for r in conn.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()}
    if "utilisateurs" in names:
        return "utilisateurs"
    if "users" in names:
        return "users"
    return None

def user_id_by_username(conn: sqlite3.Connection, table: str, username: str) -> int | None:
    row = conn.execute(f"SELECT rowid, * FROM {table} WHERE username = ?", (username,)).fetchone()
    if not row:
        return None
    # Essaye d'attraper la clé primaire par nom courant
    # 'id_utilisateur' (souvent) ou 'id'
    try:
        cur = conn.execute(f"PRAGMA table_info({table})").fetchall()
        id_col = None
        for cid, name, *_ in cur:
            if name in ("id_utilisateur", "id", "user_id"):
                id_col = name
                break
        if id_col:
            return conn.execute(f"SELECT {id_col} FROM {table} WHERE username = ?", (username,)).fetchone()[0]
    except:
        pass
    # fallback: rowid
    return conn.execute(f"SELECT rowid FROM {table} WHERE username = ?", (username,)).fetchone()[0]

def assign_role(conn: sqlite3.Connection, user_id: int, role_id: int):
    # S'adapte à ta table user_roles (sans assigned_by)
    if {"user_id", "role_id"} <= cols(conn, "user_roles"):
        run(conn, "INSERT OR IGNORE INTO user_roles (user_id, role_id) VALUES (?, ?)", (user_id, role_id))
    else:
        raise RuntimeError("Table user_roles invalide: colonnes requises manquantes")

# ----------------------------- Main --------------------------------

def init_roles_and_permissions() -> bool:
    db = pick_db_path()
    print("🚀 Initialisation des rôles & permissions")
    print("DB :", db)

    with sqlite3.connect(db) as conn:
        conn.execute("PRAGMA foreign_keys = ON")

        # 1) Schéma minimum requis
        ensure_roles(conn)
        ensure_user_roles(conn)
        ensure_available_views(conn)
        ensure_user_view_access(conn)

        # 2) Données par défaut
        seed_roles(conn)
        seed_views(conn)

        # 3) Assigner Super Administrateur à 'admin' s'il existe
        utable = utilisateurs_table(conn)
        if not utable:
            print("  ⚠️ Aucune table utilisateurs trouvée (utilisateurs/users). Assignations ignorées.")
            return True

        admin_id = user_id_by_username(conn, utable, "admin")
        if admin_id:
            try:
                assign_role(conn, admin_id, 1)
                print(f"  ✅ Rôle 'Super Administrateur' assigné à admin (id={admin_id})")
            except Exception as e:
                print(f"  ⚠️ Impossible d'assigner le rôle à admin: {e}")
        else:
            print("  ℹ️ Utilisateur 'admin' introuvable — crée-le puis relance ce script pour lui attribuer le rôle.")

        conn.commit()

    print("\n🎉 Initialisation terminée.")
    return True

if __name__ == "__main__":
    ok = init_roles_and_permissions()
    raise SystemExit(0 if ok else 1)
