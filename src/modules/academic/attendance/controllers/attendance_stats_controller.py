# Contrôleur pour les statistiques de présence
from database.connection import get_db_connection
from typing import List, Dict, Optional, Tuple
from datetime import datetime
from ..models.attendance_model import AttendanceStatsModel

class AttendanceStatsController:
    """Contrôleur pour les statistiques de présence"""
    
    def __init__(self):
        self.conn = None
    
    def _connect(self):
        """Établit la connexion à la base de données"""
        return get_db_connection()
    
    def get_absence_threshold(self) -> int:
        """Retourne le seuil d'absence injustifiée (valeur par défaut pour SQL Server)"""
        return 3  # Valeur par défaut
    
    def get_student_attendance_stats(self, eleve_id: int, start_date: str = None, 
                                   end_date: str = None) -> AttendanceStatsModel:
        """Récupère les statistiques de présence d'un élève"""
        try:
            conn = self._connect()
            if not conn:
                return AttendanceStatsModel()
            
            cursor = conn.cursor()
            query = """
                SELECT 
                    COUNT(*) as total_jours,
                    SUM(CASE WHEN statut = 'Présent' THEN 1 ELSE 0 END) as presents,
                    SUM(CASE WHEN statut = 'Absent' THEN 1 ELSE 0 END) as absents,
                    SUM(CASE WHEN statut = 'Retard' THEN 1 ELSE 0 END) as retards,
                    SUM(CASE WHEN statut = 'Justifié' THEN 1 ELSE 0 END) as justifies
                FROM presences
                WHERE eleve_id=?
            """
            params = [eleve_id]
            
            if start_date:
                query += " AND date >= ?"
                params.append(start_date)
            if end_date:
                query += " AND date <= ?"
                params.append(end_date)
            
            cursor.execute(query, params)
            row = cursor.fetchone()
            
            conn.close()
            
            if row:
                return AttendanceStatsModel(
                    total_jours=row[0] or 0,
                    presents=row[1] or 0,
                    absents=row[2] or 0,
                    retards=row[3] or 0,
                    justifies=row[4] or 0
                )
            else:
                return AttendanceStatsModel()
                
        except Exception as e:
            print(f"❌ Erreur get_student_attendance_stats: {e}")
            return AttendanceStatsModel()
    
    def get_class_attendance_summary(self, classe_id: int, start_date: str = None, 
                                   end_date: str = None) -> List[Dict]:
        """Récupère un résumé des présences d'une classe sur une période"""
        try:
            conn = self._connect()
            if not conn:
                return []
            
            cursor = conn.cursor()
            query = """
                SELECT 
                    p.date,
                    COUNT(*) as total_eleves,
                    SUM(CASE WHEN p.statut = 'Présent' THEN 1 ELSE 0 END) as presents,
                    SUM(CASE WHEN p.statut = 'Absent' THEN 1 ELSE 0 END) as absents,
                    SUM(CASE WHEN p.statut = 'Retard' THEN 1 ELSE 0 END) as retards,
                    SUM(CASE WHEN p.statut = 'Justifié' THEN 1 ELSE 0 END) as justifies
                FROM presences p
                WHERE p.classe_id=?
            """
            params = [classe_id]
            
            if start_date:
                query += " AND p.date >= ?"
                params.append(start_date)
            if end_date:
                query += " AND p.date <= ?"
                params.append(end_date)
                
            query += " GROUP BY p.date ORDER BY p.date DESC"
            
            cursor.execute(query, params)
            rows = cursor.fetchall()
            
            summary = []
            for row in rows:
                summary.append({
                    'date': row[0],
                    'total_eleves': row[1],
                    'presents': row[2],
                    'absents': row[3],
                    'retards': row[4],
                    'justifies': row[5]
                })
            
            conn.close()
            return summary
            
        except Exception as e:
            print(f"❌ Erreur get_class_attendance_summary: {e}")
            return []
    
    def get_monthly_attendance_data(self, classe_id: int, year: int, month: int) -> List[Dict]:
        """Récupère les données de présence mensuelles"""
        try:
            conn = self._connect()
            if not conn:
                return []
            
            cursor = conn.cursor()
            cursor.execute("""
                SELECT e.prenom, e.nom, p.statut, p.date, p.commentaire
                FROM presences p 
                JOIN eleves e ON p.eleve_id=e.id_eleve
                WHERE p.classe_id=? AND YEAR(p.date)=? AND MONTH(p.date)=?
                ORDER BY e.nom, e.prenom, p.date
            """, (classe_id, year, month))
            
            rows = cursor.fetchall()
            data = []
            
            for row in rows:
                data.append({
                    'prenom': row[0],
                    'nom': row[1],
                    'statut': row[2],
                    'date': row[3],
                    'commentaire': row[4]
                })
            
            conn.close()
            return data
            
        except Exception as e:
            print(f"❌ Erreur get_monthly_attendance_data: {e}")
            return []
    
    def get_attendance_counts_by_status(self, classe_id: int, date: str) -> Dict[str, int]:
        """Récupère le nombre de présences par statut pour une classe et une date"""
        try:
            conn = self._connect()
            if not conn:
                return {"Présent": 0, "Absent": 0, "Retard": 0, "Justifié": 0}
            
            cursor = conn.cursor()
            cursor.execute("""
                SELECT statut, COUNT(*) as count
                FROM presences
                WHERE classe_id=? AND date=?
                GROUP BY statut
            """, (classe_id, date))
            
            rows = cursor.fetchall()
            counts = {"Présent": 0, "Absent": 0, "Retard": 0, "Justifié": 0}
            
            for row in rows:
                counts[row[0]] = row[1]
            
            conn.close()
            return counts
            
        except Exception as e:
            print(f"❌ Erreur get_attendance_counts_by_status: {e}")
            return {"Présent": 0, "Absent": 0, "Retard": 0, "Justifié": 0}
    
    def get_unjustified_absences_count(self, eleve_id: int) -> int:
        """Récupère le nombre d'absences injustifiées d'un élève"""
        try:
            conn = self._connect()
            if not conn:
                return 0
            
            cursor = conn.cursor()
            cursor.execute("""
                SELECT COUNT(*) as count
                FROM presences
                WHERE eleve_id=? AND statut='Absent' AND commentaire IS NULL
            """, (eleve_id,))
            
            row = cursor.fetchone()
            conn.close()
            
            return row[0] if row else 0
            
        except Exception as e:
            print(f"❌ Erreur get_unjustified_absences_count: {e}")
            return 0
