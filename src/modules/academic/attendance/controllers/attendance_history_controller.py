# Contrôleur pour l'historique des présences
from database.connection import get_db_connection
from typing import List, Dict, Optional, Tuple
from datetime import datetime
from ..models.attendance_model import AttendanceHistoryModel

class AttendanceHistoryController:
    """Contrôleur pour l'historique des présences"""
    
    def __init__(self):
        self.conn = None
    
    def _connect(self):
        """Établit la connexion à la base de données"""
        return get_db_connection()
    
    def get_student_history(self, eleve_id: int) -> List[AttendanceHistoryModel]:
        """Récupère l'historique complet des présences d'un élève"""
        try:
            conn = self._connect()
            if not conn:
                return []
            
            cursor = conn.cursor()
            cursor.execute("""
                SELECT p.date, p.statut, p.commentaire, e.prenom, e.nom, c.nom_classe
                FROM presences p 
                JOIN eleves e ON p.eleve_id=e.id_eleve
                JOIN classes c ON p.classe_id=c.id_classe
                WHERE p.eleve_id=? 
                ORDER BY p.date DESC
            """, (eleve_id,))
            
            rows = cursor.fetchall()
            history = []
            
            for row in rows:
                history.append(AttendanceHistoryModel(
                    eleve_id=eleve_id,
                    eleve_nom=f"{row[3]} {row[4]}",
                    classe_nom=row[5],
                    date=row[0],
                    statut=row[1],
                    commentaire=row[2] or ""
                ))
            
            conn.close()
            return history
            
        except Exception as e:
            print(f"❌ Erreur get_student_history: {e}")
            return []
    
    def get_class_history(self, classe_id: int, start_date: str = None, 
                         end_date: str = None) -> List[AttendanceHistoryModel]:
        """Récupère l'historique des présences d'une classe"""
        try:
            conn = self._connect()
            if not conn:
                return []
            
            cursor = conn.cursor()
            query = """
                SELECT p.eleve_id, p.date, p.statut, p.commentaire, e.prenom, e.nom, c.nom_classe
                FROM presences p 
                JOIN eleves e ON p.eleve_id=e.id_eleve
                JOIN classes c ON p.classe_id=c.id_classe
                WHERE p.classe_id=?
            """
            params = [classe_id]
            
            if start_date:
                query += " AND p.date >= ?"
                params.append(start_date)
            if end_date:
                query += " AND p.date <= ?"
                params.append(end_date)
                
            query += " ORDER BY p.date DESC, e.nom, e.prenom"
            
            cursor.execute(query, params)
            rows = cursor.fetchall()
            history = []
            
            for row in rows:
                history.append(AttendanceHistoryModel(
                    eleve_id=row[0],
                    eleve_nom=f"{row[4]} {row[5]}",
                    classe_nom=row[6],
                    date=row[1],
                    statut=row[2],
                    commentaire=row[3] or ""
                ))
            
            conn.close()
            return history
            
        except Exception as e:
            print(f"❌ Erreur get_class_history: {e}")
            return []
    
    def get_attendance_trends(self, eleve_id: int, days: int = 30) -> List[Dict]:
        """Récupère les tendances de présence d'un élève sur les derniers jours"""
        try:
            conn = self._connect()
            if not conn:
                return []
            
            cursor = conn.cursor()
            cursor.execute("""
                SELECT 
                    p.date,
                    p.statut,
                    COUNT(*) as count
                FROM presences p
                WHERE p.eleve_id=? 
                AND p.date >= DATEADD(day, -?, GETDATE())
                GROUP BY p.date, p.statut
                ORDER BY p.date DESC
            """, (eleve_id, days))
            
            rows = cursor.fetchall()
            trends = []
            
            for row in rows:
                trends.append({
                    'date': row[0],
                    'statut': row[1],
                    'count': row[2]
                })
            
            conn.close()
            return trends
            
        except Exception as e:
            print(f"❌ Erreur get_attendance_trends: {e}")
            return []
    
    def get_absence_patterns(self, eleve_id: int) -> Dict:
        """Analyse les patterns d'absence d'un élève"""
        try:
            conn = self._connect()
            if not conn:
                return {}
            
            cursor = conn.cursor()
            
            # Absences par jour de la semaine
            cursor.execute("""
                SELECT 
                    DATEPART(weekday, p.date) as day_of_week,
                    COUNT(*) as absences
                FROM presences p
                WHERE p.eleve_id=? AND p.statut='Absent'
                GROUP BY DATEPART(weekday, p.date)
                ORDER BY day_of_week
            """, (eleve_id,))
            
            day_patterns = {}
            days = ['Dimanche', 'Lundi', 'Mardi', 'Mercredi', 'Jeudi', 'Vendredi', 'Samedi']
            
            for row in cursor.fetchall():
                day_patterns[days[row[0] - 1]] = row[1]
            
            # Absences consécutives
            cursor.execute("""
                WITH consecutive_absences AS (
                    SELECT 
                        p.date,
                        ROW_NUMBER() OVER (ORDER BY p.date) - 
                        ROW_NUMBER() OVER (PARTITION BY p.statut ORDER BY p.date) as grp
                    FROM presences p
                    WHERE p.eleve_id=? AND p.statut='Absent'
                )
                SELECT 
                    COUNT(*) as consecutive_count,
                    COUNT(DISTINCT grp) as periods
                FROM consecutive_absences
            """, (eleve_id,))
            
            consecutive_row = cursor.fetchone()
            consecutive_patterns = {
                'max_consecutive': consecutive_row[0] if consecutive_row else 0,
                'periods': consecutive_row[1] if consecutive_row else 0
            }
            
            conn.close()
            
            return {
                'day_patterns': day_patterns,
                'consecutive_patterns': consecutive_patterns
            }
            
        except Exception as e:
            print(f"❌ Erreur get_absence_patterns: {e}")
            return {}
    
    def search_attendance_history(self, search_term: str, classe_id: int = None, 
                                start_date: str = None, end_date: str = None) -> List[AttendanceHistoryModel]:
        """Recherche dans l'historique des présences"""
        try:
            conn = self._connect()
            if not conn:
                return []
            
            cursor = conn.cursor()
            query = """
                SELECT p.eleve_id, p.date, p.statut, p.commentaire, e.prenom, e.nom, c.nom_classe
                FROM presences p 
                JOIN eleves e ON p.eleve_id=e.id_eleve
                JOIN classes c ON p.classe_id=c.id_classe
                WHERE (e.nom LIKE ? OR e.prenom LIKE ? OR p.commentaire LIKE ?)
            """
            params = [f"%{search_term}%", f"%{search_term}%", f"%{search_term}%"]
            
            if classe_id:
                query += " AND p.classe_id=?"
                params.append(classe_id)
            
            if start_date:
                query += " AND p.date >= ?"
                params.append(start_date)
            if end_date:
                query += " AND p.date <= ?"
                params.append(end_date)
                
            query += " ORDER BY p.date DESC"
            
            cursor.execute(query, params)
            rows = cursor.fetchall()
            results = []
            
            for row in rows:
                results.append(AttendanceHistoryModel(
                    eleve_id=row[0],
                    eleve_nom=f"{row[4]} {row[5]}",
                    classe_nom=row[6],
                    date=row[1],
                    statut=row[2],
                    commentaire=row[3] or ""
                ))
            
            conn.close()
            return results
            
        except Exception as e:
            print(f"❌ Erreur search_attendance_history: {e}")
            return []
