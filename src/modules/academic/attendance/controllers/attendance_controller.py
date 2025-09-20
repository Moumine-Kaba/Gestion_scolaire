# Contrôleur principal pour la gestion des présences
from database.connection import get_db_connection
from typing import List, Dict, Optional, Tuple
from datetime import datetime
from ..models.attendance_model import AttendanceModel, AttendanceStatsModel, AttendanceHistoryModel

class AttendanceController:
    """Contrôleur principal pour la gestion des présences"""
    
    def __init__(self):
        self.conn = None
    
    def _connect(self):
        """Établit la connexion à la base de données"""
        return get_db_connection()
    
    def get_all_classes(self) -> List[Dict]:
        """Récupère toutes les classes"""
        try:
            conn = self._connect()
            if not conn:
                return []
            
            cursor = conn.cursor()
            cursor.execute("SELECT id_classe, nom_classe FROM classes ORDER BY nom_classe")
            rows = cursor.fetchall()
            
            classes = []
            for row in rows:
                classes.append({
                    'id_classe': row[0],
                    'nom_classe': row[1]
                })
            
            conn.close()
            return classes
            
        except Exception as e:
            print(f"❌ Erreur get_all_classes: {e}")
            return []
    
    def get_students_by_class(self, classe_id: int, search_term: str = "", 
                            statut_filter: str = None, date: str = None) -> List[Dict]:
        """Récupère les élèves d'une classe avec filtres"""
        try:
            conn = self._connect()
            if not conn:
                return []
            
            cursor = conn.cursor()
            query = "SELECT e.id_eleve, e.nom, e.prenom, e.email FROM eleves e WHERE e.id_classe=?"
            params = [classe_id]
            
            if search_term:
                search_pattern = f"%{search_term}%"
                query += " AND (e.nom LIKE ? OR e.prenom LIKE ?)"
                params.extend([search_pattern, search_pattern])
            
            if statut_filter and statut_filter != "Tous" and date:
                query += " AND e.id_eleve IN (SELECT eleve_id FROM presences WHERE classe_id=? AND statut=? AND date=?)"
                params.extend([classe_id, statut_filter, date])
            
            query += " ORDER BY e.nom, e.prenom"
            
            cursor.execute(query, params)
            rows = cursor.fetchall()
            
            students = []
            for row in rows:
                students.append({
                    'id_eleve': row[0],
                    'nom': row[1],
                    'prenom': row[2],
                    'email': row[3]
                })
            
            conn.close()
            return students
            
        except Exception as e:
            print(f"❌ Erreur get_students_by_class: {e}")
            return []
    
    def get_attendance_for_date_and_class(self, classe_id: int, date: str) -> Dict:
        """Récupère les présences pour une classe et une date"""
        try:
            conn = self._connect()
            if not conn:
                return {}
            
            cursor = conn.cursor()
            cursor.execute("""
                SELECT eleve_id, statut, commentaire
                FROM presences
                WHERE classe_id=? AND date=?
            """, (classe_id, date))
            
            rows = cursor.fetchall()
            attendance_map = {}
            
            for row in rows:
                attendance_map[row[0]] = {
                    'eleve_id': row[0],
                    'statut': row[1],
                    'commentaire': row[2]
                }
            
            conn.close()
            return attendance_map
            
        except Exception as e:
            print(f"❌ Erreur get_attendance_for_date_and_class: {e}")
            return {}
    
    def add_attendance(self, attendance: AttendanceModel) -> bool:
        """Ajoute une nouvelle présence"""
        try:
            conn = self._connect()
            if not conn:
                return False
            
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO presences (eleve_id, classe_id, date, statut, commentaire)
                VALUES (?,?,?,?,?)
            """, (attendance.eleve_id, attendance.classe_id, attendance.date, 
                  attendance.statut, attendance.commentaire))
            
            conn.commit()
            conn.close()
            return True
            
        except Exception as e:
            print(f"❌ Erreur add_attendance: {e}")
            return False
    
    def update_attendance(self, attendance: AttendanceModel) -> bool:
        """Met à jour une présence existante"""
        try:
            conn = self._connect()
            if not conn:
                return False
            
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE presences
                SET statut=?, commentaire=?
                WHERE eleve_id=? AND classe_id=? AND date=?
            """, (attendance.statut, attendance.commentaire, 
                  attendance.eleve_id, attendance.classe_id, attendance.date))
            
            conn.commit()
            conn.close()
            return True
            
        except Exception as e:
            print(f"❌ Erreur update_attendance: {e}")
            return False
    
    def bulk_update_attendance(self, classe_id: int, date: str, 
                              statut: str, commentaire: str = "") -> bool:
        """Met à jour toutes les présences d'une classe pour une date"""
        try:
            conn = self._connect()
            if not conn:
                return False
            
            cursor = conn.cursor()
            
            # Récupérer tous les élèves de la classe
            students = self.get_students_by_class(classe_id)
            
            for student in students:
                eleve_id = student["id_eleve"]
                
                # Vérifier si la présence existe déjà
                cursor.execute("""
                    SELECT COUNT(*) FROM presences 
                    WHERE eleve_id=? AND classe_id=? AND date=?
                """, (eleve_id, classe_id, date))
                
                exists = cursor.fetchone()[0] > 0
                
                if exists:
                    # Mettre à jour
                    cursor.execute("""
                        UPDATE presences 
                        SET statut=?, commentaire=?
                        WHERE eleve_id=? AND classe_id=? AND date=?
                    """, (statut, commentaire, eleve_id, classe_id, date))
                else:
                    # Insérer
                    cursor.execute("""
                        INSERT INTO presences (eleve_id, classe_id, date, statut, commentaire)
                        VALUES (?,?,?,?,?)
                    """, (eleve_id, classe_id, date, statut, commentaire))
            
            conn.commit()
            conn.close()
            return True
            
        except Exception as e:
            print(f"❌ Erreur bulk_update_attendance: {e}")
            return False
    
    def reset_all_attendance_for_date(self, classe_id: int, date_str: str) -> bool:
        """Supprime toutes les présences d'une classe pour une date donnée"""
        try:
            conn = self._connect()
            if not conn:
                return False
            cursor = conn.cursor()
            cursor.execute("""
                DELETE FROM presences 
                WHERE classe_id=? AND date=?
            """, (classe_id, date_str))
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"❌ Erreur reset_all_attendance_for_date: {e}")
            return False
    
    def delete_attendance_for_date(self, classe_id: int, date: str) -> bool:
        """Supprime toutes les présences d'une classe pour une date"""
        try:
            conn = self._connect()
            if not conn:
                return False
            
            cursor = conn.cursor()
            cursor.execute("""
                DELETE FROM presences 
                WHERE classe_id=? AND date=?
            """, (classe_id, date))
            
            conn.commit()
            conn.close()
            return True
            
        except Exception as e:
            print(f"❌ Erreur delete_attendance_for_date: {e}")
            return False
