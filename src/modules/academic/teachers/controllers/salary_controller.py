"""
Contrôleur de gestion des salaires des professeurs
Gestion complète basée sur les heures de cours dispensées
"""

import sqlite3
from database.connection import get_db_connection
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Tuple
import json

class SalaryController:
    """Contrôleur pour la gestion des salaires basés sur les heures"""
    
    def __init__(self, db_path: str):
        self.db_path = db_path
        try:
            self.init_tables()
        except Exception as e:
            print(f"⚠️ Impossible d'initialiser les tables SQLite: {e}")
    
    def init_tables(self):
        """Initialise les tables nécessaires pour la gestion des salaires"""
        # Tente d'initialiser côté SQL Server si possible
        try:
            conn_mssql = get_db_connection()
            if conn_mssql:
                cur = conn_mssql.cursor()
                # Créer les tables si elles n'existent pas (synonyme SQL Server)
                try:
                    cur.execute("""
                        IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='heures_cours' AND xtype='U')
                        CREATE TABLE heures_cours (
                            id INT IDENTITY(1,1) PRIMARY KEY,
                            professeur_id INT NOT NULL,
                            date_cours DATE NOT NULL,
                            nombre_heures FLOAT NOT NULL,
                            matiere NVARCHAR(255),
                            classe NVARCHAR(255),
                            statut NVARCHAR(50) DEFAULT 'effectue',
                            commentaire NVARCHAR(MAX),
                            created_at DATETIME DEFAULT GETDATE()
                        )
                    """)
                except Exception:
                    pass
                try:
                    cur.execute("""
                        IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='absences_professeurs' AND xtype='U')
                        CREATE TABLE absences_professeurs (
                            id INT IDENTITY(1,1) PRIMARY KEY,
                            professeur_id INT NOT NULL,
                            date_absence DATE NOT NULL,
                            heures_manquees FLOAT NOT NULL,
                            motif NVARCHAR(255),
                            justifie BIT DEFAULT 0,
                            heures_recuperees FLOAT DEFAULT 0,
                            created_at DATETIME DEFAULT GETDATE()
                        )
                    """)
                except Exception:
                    pass
                try:
                    cur.execute("""
                        IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='paiements_professeurs' AND xtype='U')
                        CREATE TABLE paiements_professeurs (
                            id INT IDENTITY(1,1) PRIMARY KEY,
                            professeur_id INT NOT NULL,
                            periode_debut DATE NOT NULL,
                            periode_fin DATE NOT NULL,
                            heures_total FLOAT NOT NULL,
                            taux_horaire FLOAT NOT NULL,
                            montant_total FLOAT NOT NULL,
                            statut_paiement NVARCHAR(50) DEFAULT 'en_attente',
                            date_paiement DATE,
                            commentaire NVARCHAR(MAX),
                            created_at DATETIME DEFAULT GETDATE()
                        )
                    """)
                except Exception:
                    pass
                conn_mssql.commit()
                conn_mssql.close()
        except Exception:
            pass

        # Toujours garder la compatibilité SQLite locale
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Table des heures de cours
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS heures_cours (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                professeur_id INTEGER NOT NULL,
                date_cours DATE NOT NULL,
                nombre_heures REAL NOT NULL,
                matiere TEXT,
                classe TEXT,
                statut TEXT DEFAULT 'effectue',
                commentaire TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (professeur_id) REFERENCES professeurs(id)
            )
        """)
        
        # Table des paiements
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS paiements_professeurs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                professeur_id INTEGER NOT NULL,
                periode_debut DATE NOT NULL,
                periode_fin DATE NOT NULL,
                heures_total REAL NOT NULL,
                taux_horaire REAL NOT NULL,
                montant_total REAL NOT NULL,
                statut_paiement TEXT DEFAULT 'en_attente',
                date_paiement DATE,
                commentaire TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (professeur_id) REFERENCES professeurs(id)
            )
        """)
        
        # Table des absences
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS absences_professeurs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                professeur_id INTEGER NOT NULL,
                date_absence DATE NOT NULL,
                heures_manquees REAL NOT NULL,
                motif TEXT,
                justifie BOOLEAN DEFAULT FALSE,
                heures_recuperees REAL DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (professeur_id) REFERENCES professeurs(id)
            )
        """)
        
        conn.commit()
        conn.close()

    # Helpers
    def _get_hours_prof_col(self) -> Optional[str]:
        """Detecte le nom de colonne qui relie une heure au professeur dans heures_cours."""
        try:
            conn = sqlite3.connect(self.db_path)
            cur = conn.cursor()
            cur.execute("PRAGMA table_info(heures_cours)")
            cols = [row[1] for row in cur.fetchall()]
            conn.close()
            for name in [
                "professeur_id", "prof_id", "id_prof", "teacher_id", "enseignant_id"
            ]:
                if name in cols:
                    return name
        except Exception:
            pass
        return None
    
    def add_course_hours(self, professeur_id: int, date_cours: str, 
                        nombre_heures: float, matiere: str = "", 
                        classe: str = "", commentaire: str = "") -> bool:
        """Ajoute des heures de cours pour un professeur"""
        try:
            # SQL Server d'abord
            try:
                mssql = get_db_connection()
                if mssql:
                    cur = mssql.cursor()
                    cur.execute(
                        """
                        INSERT INTO heures_cours (professeur_id, date_cours, nombre_heures, matiere, classe, commentaire)
                        VALUES (?, ?, ?, ?, ?, ?)
                        """,
                        (professeur_id, date_cours, nombre_heures, matiere, classe, commentaire)
                    )
                    mssql.commit()
                    mssql.close()
                    return True
            except Exception:
                pass

            # Fallback SQLite
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            prof_col = self._get_hours_prof_col()
            if prof_col:
                cursor.execute(
                    f"INSERT INTO heures_cours ({prof_col}, date_cours, nombre_heures, matiere, classe, commentaire) VALUES (?, ?, ?, ?, ?, ?)",
                    (professeur_id, date_cours, nombre_heures, matiere, classe, commentaire)
                )
            else:
                # Table heures_cours sans colonne de lien; on insère quand même
                cursor.execute(
                    "INSERT INTO heures_cours (date_cours, nombre_heures, matiere, classe, commentaire) VALUES (?, ?, ?, ?, ?)",
                    (date_cours, nombre_heures, matiere, classe, commentaire)
                )
            
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"❌ Erreur ajout heures: {e}")
            return False
    
    def get_professor_hours(self, professeur_id: int, month: int = None, year: int = None) -> List[Dict]:
        """Récupère les heures d'un professeur pour une période donnée"""
        try:
            # SQL Server d'abord
            try:
                mssql = get_db_connection()
                if mssql:
                    cur = mssql.cursor()
                    sql = (
                        "SELECT SUM(nombre_heures) as total_heures, COUNT(*) as nb_cours "
                        "FROM heures_cours WHERE professeur_id = ? "
                    )
                    params = [professeur_id]
                    if month and year:
                        sql += "AND MONTH(date_cours) = ? AND YEAR(date_cours) = ? "
                        params += [month, year]
                    sql += "AND statut = 'effectue' ORDER BY date_cours DESC"
                    cur.execute(sql, params)
                    # Pour rester proche de l'API, retourner les lignes détaillées si besoin
                    cur.execute(
                        """
                        SELECT id, professeur_id, date_cours, nombre_heures, matiere, classe, statut, commentaire, created_at
                        FROM heures_cours WHERE professeur_id = ?
                        """ + (" AND MONTH(date_cours) = ? AND YEAR(date_cours) = ?" if month and year else "") + " ORDER BY date_cours DESC",
                        params
                    )
                    columns = [d[0] for d in cur.description]
                    results = [dict(zip(columns, row)) for row in cur.fetchall()]
                    mssql.close()
                    return results
            except Exception:
                pass

            # Fallback SQLite
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            prof_col = self._get_hours_prof_col()
            if not prof_col:
                conn.close()
                return []
            if month and year:
                query = (
                    f"SELECT * FROM heures_cours WHERE {prof_col} = ? AND strftime('%m', date_cours) = ? AND strftime('%Y', date_cours) = ? ORDER BY date_cours DESC"
                )
                cursor.execute(query, (professeur_id, f"{month:02d}", str(year)))
            else:
                query = f"SELECT * FROM heures_cours WHERE {prof_col} = ? ORDER BY date_cours DESC"
                cursor.execute(query, (professeur_id,))
            
            columns = [description[0] for description in cursor.description]
            results = [dict(zip(columns, row)) for row in cursor.fetchall()]
            
            conn.close()
            return results
        except Exception as e:
            print(f"❌ Erreur récupération heures: {e}")
            return []
    
    def calculate_salary(self, professeur_id: int, periode_debut: str, 
                       periode_fin: str) -> Dict:
        """Calcule le salaire d'un professeur pour une période donnée"""
        try:
            # SQL Server d'abord
            try:
                mssql = get_db_connection()
                if mssql:
                    cur = mssql.cursor()
                    # Taux horaire
                    cur.execute("SELECT salaire_horaire FROM professeurs WHERE id_professeur = ?", (professeur_id,))
                    res = cur.fetchone()
                    if not res:
                        mssql.close()
                        return {"error": "Professeur non trouvé"}
                    taux_horaire = res[0] or 0
                    # Heures
                    cur.execute(
                        """
                        SELECT COALESCE(SUM(nombre_heures), 0) as total_heures, COUNT(*) as nb_cours
                        FROM heures_cours
                        WHERE professeur_id = ? AND date_cours BETWEEN ? AND ? AND statut = 'effectue'
                        """,
                        (professeur_id, periode_debut, periode_fin)
                    )
                    th, nb = cur.fetchone()
                    mssql.close()
                    return {
                        "professeur_id": professeur_id,
                        "periode_debut": periode_debut,
                        "periode_fin": periode_fin,
                        "total_heures": th or 0,
                        "nb_cours": nb or 0,
                        "taux_horaire": taux_horaire,
                        "montant_total": (th or 0) * taux_horaire
                    }
            except Exception:
                pass

            # Fallback SQLite
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Récupérer le taux horaire du professeur
            # Déterminer dynamiquement la colonne identifiant (id ou professeur_id)
            try:
                cursor.execute("SELECT salaire_horaire FROM professeurs WHERE id = ?", (professeur_id,))
            except Exception:
                try:
                    cursor.execute("SELECT salaire_horaire FROM professeurs WHERE professeur_id = ?", (professeur_id,))
                except Exception:
                    conn.close()
                    return {
                        "professeur_id": professeur_id,
                        "periode_debut": periode_debut,
                        "periode_fin": periode_fin,
                        "total_heures": 0,
                        "nb_cours": 0,
                        "taux_horaire": 0,
                        "montant_total": 0
                    }
            result = cursor.fetchone()
            if not result:
                return {"error": "Professeur non trouvé"}
            
            taux_horaire = result[0] or 0
            
            # Récupérer les heures pour la période
            cursor.execute("""
                SELECT SUM(nombre_heures) as total_heures, COUNT(*) as nb_cours
                FROM heures_cours 
                WHERE professeur_id = ? 
                AND date_cours BETWEEN ? AND ?
                AND statut = 'effectue'
            """, (professeur_id, periode_debut, periode_fin))
            
            result = cursor.fetchone()
            total_heures = result[0] or 0
            nb_cours = result[1] or 0
            
            # Calculer le montant
            montant_total = total_heures * taux_horaire
            
            conn.close()
            
            return {
                "professeur_id": professeur_id,
                "periode_debut": periode_debut,
                "periode_fin": periode_fin,
                "total_heures": total_heures,
                "nb_cours": nb_cours,
                "taux_horaire": taux_horaire,
                "montant_total": montant_total
            }
        except Exception as e:
            print(f"❌ Erreur calcul salaire: {e}")
            return {"error": str(e)}
    
    def get_monthly_summary(self, month: int, year: int) -> Dict:
        """Récupère un résumé mensuel de tous les professeurs"""
        try:
            # SQL Server d'abord
            try:
                mssql = get_db_connection()
                if mssql:
                    cur = mssql.cursor()
                    cur.execute(
                        """
                        SELECT 
                            p.id_professeur as id,
                            p.nom,
                            p.prenom,
                            p.specialite,
                            p.salaire_horaire,
                            COALESCE(SUM(h.nombre_heures), 0) as total_heures,
                            COUNT(h.id) as nb_cours,
                            COALESCE(SUM(h.nombre_heures) * p.salaire_horaire, 0) as montant_total
                        FROM professeurs p
                        LEFT JOIN heures_cours h ON p.id_professeur = h.professeur_id 
                            AND MONTH(h.date_cours) = ? 
                            AND YEAR(h.date_cours) = ?
                            AND h.statut = 'effectue'
                        GROUP BY p.id_professeur, p.nom, p.prenom, p.specialite, p.salaire_horaire
                        ORDER BY montant_total DESC
                        """,
                        (month, year)
                    )
                    columns = [d[0] for d in cur.description]
                    professeurs = [dict(zip(columns, row)) for row in cur.fetchall()]
                    total_heures = sum(p['total_heures'] for p in professeurs)
                    total_montant = sum(p['montant_total'] for p in professeurs)
                    mssql.close()
                    return {
                        "month": month,
                        "year": year,
                        "professeurs": professeurs,
                        "totals": {
                            "nb_professeurs": len(professeurs),
                            "total_heures": total_heures,
                            "total_montant": total_montant,
                            "moyenne_heures": total_heures / len(professeurs) if professeurs else 0,
                            "moyenne_montant": total_montant / len(professeurs) if professeurs else 0,
                        }
                    }
            except Exception:
                pass

            # Fallback SQLite
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Récupérer les données de tous les professeurs pour le mois
            # Tenter de joindre sur id, sinon regrouper uniquement sur heures
            try:
                cursor.execute("""
                    SELECT 
                        p.id as id,
                        p.nom,
                        p.prenom,
                        p.specialite,
                        p.salaire_horaire,
                        COALESCE(SUM(h.nombre_heures), 0) as total_heures,
                        COUNT(h.id) as nb_cours,
                        COALESCE(SUM(h.nombre_heures) * p.salaire_horaire, 0) as montant_total
                    FROM professeurs p
                    LEFT JOIN heures_cours h ON p.id = h.professeur_id 
                        AND strftime('%m', h.date_cours) = ? 
                        AND strftime('%Y', h.date_cours) = ?
                        AND h.statut = 'effectue'
                    GROUP BY p.id, p.nom, p.prenom, p.specialite, p.salaire_horaire
                    ORDER BY montant_total DESC
                """, (f"{month:02d}", str(year)))
            except Exception:
                prof_col = self._get_hours_prof_col()
                cursor.execute(f"""
                    SELECT 
                        COALESCE(h.{prof_col}, 0) as id,
                        '' as nom,
                        '' as prenom,
                        '' as specialite,
                        0 as salaire_horaire,
                        COALESCE(SUM(h.nombre_heures), 0) as total_heures,
                        COUNT(h.id) as nb_cours,
                        0 as montant_total
                    FROM heures_cours h
                    WHERE strftime('%m', h.date_cours) = ? 
                      AND strftime('%Y', h.date_cours) = ?
                      AND h.statut = 'effectue'
                    GROUP BY id
                    ORDER BY total_heures DESC
                """, (f"{month:02d}", str(year)))
            
            columns = [description[0] for description in cursor.description]
            professeurs = [dict(zip(columns, row)) for row in cursor.fetchall()]
            
            # Calculer les totaux
            total_heures = sum(p['total_heures'] for p in professeurs)
            total_montant = sum(p['montant_total'] for p in professeurs)
            nb_professeurs = len(professeurs)
            
            conn.close()
            
            return {
                "month": month,
                "year": year,
                "professeurs": professeurs,
                "totals": {
                    "nb_professeurs": nb_professeurs,
                    "total_heures": total_heures,
                    "total_montant": total_montant,
                    "moyenne_heures": total_heures / nb_professeurs if nb_professeurs > 0 else 0,
                    "moyenne_montant": total_montant / nb_professeurs if nb_professeurs > 0 else 0
                }
            }
        except Exception as e:
            print(f"❌ Erreur résumé mensuel: {e}")
            return {"error": str(e)}
    
    def get_academic_year_summary(self, year: int) -> Dict:
        """Récupère un résumé de l'année scolaire (septembre à mai)"""
        try:
            # SQL Server d'abord
            try:
                mssql = get_db_connection()
                if mssql:
                    cur = mssql.cursor()
                    periode_debut = f"{year-1}-09-01"
                    periode_fin = f"{year}-05-31"
                    cur.execute(
                        """
                        SELECT 
                            p.id_professeur as id,
                            p.nom,
                            p.prenom,
                            p.specialite,
                            p.salaire_horaire,
                            COALESCE(SUM(h.nombre_heures), 0) as total_heures,
                            COUNT(h.id) as nb_cours,
                            COALESCE(SUM(h.nombre_heures) * p.salaire_horaire, 0) as montant_total
                        FROM professeurs p
                        LEFT JOIN heures_cours h ON p.id_professeur = h.professeur_id 
                            AND h.date_cours BETWEEN ? AND ?
                            AND h.statut = 'effectue'
                        GROUP BY p.id_professeur, p.nom, p.prenom, p.specialite, p.salaire_horaire
                        ORDER BY montant_total DESC
                        """,
                        (periode_debut, periode_fin)
                    )
                    columns = [d[0] for d in cur.description]
                    professeurs = [dict(zip(columns, row)) for row in cur.fetchall()]
                    total_heures = sum(p['total_heures'] for p in professeurs)
                    total_montant = sum(p['montant_total'] for p in professeurs)
                    mssql.close()
                    return {
                        "academic_year": f"{year-1}-{year}",
                        "periode_debut": periode_debut,
                        "periode_fin": periode_fin,
                        "professeurs": professeurs,
                        "totals": {
                            "nb_professeurs": len(professeurs),
                            "total_heures": total_heures,
                            "total_montant": total_montant,
                            "moyenne_heures": total_heures / len(professeurs) if professeurs else 0,
                            "moyenne_montant": total_montant / len(professeurs) if professeurs else 0,
                        }
                    }
            except Exception:
                pass

            # Fallback SQLite
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Période académique : septembre de l'année précédente à mai de l'année actuelle
            periode_debut = f"{year-1}-09-01"
            periode_fin = f"{year}-05-31"
            
            try:
                cursor.execute("""
                    SELECT 
                        p.id as id,
                        p.nom,
                        p.prenom,
                        p.specialite,
                        p.salaire_horaire,
                        COALESCE(SUM(h.nombre_heures), 0) as total_heures,
                        COUNT(h.id) as nb_cours,
                        COALESCE(SUM(h.nombre_heures) * p.salaire_horaire, 0) as montant_total
                    FROM professeurs p
                    LEFT JOIN heures_cours h ON p.id = h.professeur_id 
                        AND h.date_cours BETWEEN ? AND ?
                        AND h.statut = 'effectue'
                    GROUP BY p.id, p.nom, p.prenom, p.specialite, p.salaire_horaire
                    ORDER BY montant_total DESC
                """, (periode_debut, periode_fin))
            except Exception:
                prof_col = self._get_hours_prof_col()
                cursor.execute(f"""
                    SELECT 
                        COALESCE(h.{prof_col}, 0) as id,
                        '' as nom,
                        '' as prenom,
                        '' as specialite,
                        0 as salaire_horaire,
                        COALESCE(SUM(h.nombre_heures), 0) as total_heures,
                        COUNT(h.id) as nb_cours,
                        0 as montant_total
                    FROM heures_cours h
                    WHERE h.date_cours BETWEEN ? AND ?
                      AND h.statut = 'effectue'
                    GROUP BY id
                    ORDER BY total_heures DESC
                """, (periode_debut, periode_fin))
            
            columns = [description[0] for description in cursor.description]
            professeurs = [dict(zip(columns, row)) for row in cursor.fetchall()]
            
            # Calculer les totaux
            total_heures = sum(p['total_heures'] for p in professeurs)
            total_montant = sum(p['montant_total'] for p in professeurs)
            nb_professeurs = len(professeurs)
            
            conn.close()
            
            return {
                "academic_year": f"{year-1}-{year}",
                "periode_debut": periode_debut,
                "periode_fin": periode_fin,
                "professeurs": professeurs,
                "totals": {
                    "nb_professeurs": nb_professeurs,
                    "total_heures": total_heures,
                    "total_montant": total_montant,
                    "moyenne_heures": total_heures / nb_professeurs if nb_professeurs > 0 else 0,
                    "moyenne_montant": total_montant / nb_professeurs if nb_professeurs > 0 else 0
                }
            }
        except Exception as e:
            print(f"❌ Erreur résumé année: {e}")
            return {"error": str(e)}
    
    def add_absence(self, professeur_id: int, date_absence: str, 
                   heures_manquees: float, motif: str = "", 
                   justifie: bool = False) -> bool:
        """Enregistre une absence d'un professeur"""
        try:
            # SQL Server d'abord
            try:
                mssql = get_db_connection()
                if mssql:
                    cur = mssql.cursor()
                    cur.execute(
                        """
                        INSERT INTO absences_professeurs (professeur_id, date_absence, heures_manquees, motif, justifie)
                        VALUES (?, ?, ?, ?, ?)
                        """,
                        (professeur_id, date_absence, heures_manquees, motif, justifie)
                    )
                    mssql.commit()
                    mssql.close()
                    return True
            except Exception:
                pass

            # Fallback SQLite
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT INTO absences_professeurs 
                (professeur_id, date_absence, heures_manquees, motif, justifie)
                VALUES (?, ?, ?, ?, ?)
            """, (professeur_id, date_absence, heures_manquees, motif, justifie))
            
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"❌ Erreur ajout absence: {e}")
            return False
    
    def get_absences(self, professeur_id: int, month: int = None, year: int = None) -> List[Dict]:
        """Récupère les absences d'un professeur"""
        try:
            # SQL Server d'abord
            try:
                mssql = get_db_connection()
                if mssql:
                    cur = mssql.cursor()
                    if month and year:
                        cur.execute(
                            """
                            SELECT * FROM absences_professeurs 
                            WHERE professeur_id = ? AND MONTH(date_absence) = ? AND YEAR(date_absence) = ?
                            ORDER BY date_absence DESC
                            """,
                            (professeur_id, month, year)
                        )
                    else:
                        cur.execute(
                            """
                            SELECT * FROM absences_professeurs 
                            WHERE professeur_id = ? ORDER BY date_absence DESC
                            """,
                            (professeur_id,)
                        )
                    columns = [d[0] for d in cur.description]
                    results = [dict(zip(columns, row)) for row in cur.fetchall()]
                    mssql.close()
                    return results
            except Exception:
                pass

            # Fallback SQLite
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            if month and year:
                query = """
                    SELECT * FROM absences_professeurs 
                    WHERE professeur_id = ? 
                    AND strftime('%m', date_absence) = ? 
                    AND strftime('%Y', date_absence) = ?
                    ORDER BY date_absence DESC
                """
                cursor.execute(query, (professeur_id, f"{month:02d}", str(year)))
            else:
                query = """
                    SELECT * FROM absences_professeurs 
                    WHERE professeur_id = ? 
                    ORDER BY date_absence DESC
                """
                cursor.execute(query, (professeur_id,))
            
            columns = [description[0] for description in cursor.description]
            results = [dict(zip(columns, row)) for row in cursor.fetchall()]
            
            conn.close()
            return results
        except Exception as e:
            print(f"❌ Erreur récupération absences: {e}")
            return []