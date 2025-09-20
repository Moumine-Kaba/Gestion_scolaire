# Service principal pour la gestion des présences
from typing import List, Dict, Optional, Tuple
from datetime import datetime, timedelta
from ..controllers.attendance_controller import AttendanceController
from ..controllers.attendance_stats_controller import AttendanceStatsController
from ..controllers.attendance_history_controller import AttendanceHistoryController
from ..models.attendance_model import AttendanceModel, AttendanceStatsModel, AttendanceHistoryModel

class AttendanceService:
    """Service principal pour la gestion des présences"""
    
    def __init__(self):
        self.attendance_controller = AttendanceController()
        self.stats_controller = AttendanceStatsController()
        self.history_controller = AttendanceHistoryController()
    
    def get_students_with_attendance_status(self, classe_id: int, date_str: str, search_term: str = "", statut_filter: Optional[str] = None) -> List[Dict]:
        """Récupère les élèves d'une classe avec leur statut de présence pour une date donnée"""
        eleves = self.attendance_controller.get_students_by_class(classe_id, search_term, statut_filter, date_str)
        presences = self.attendance_controller.get_attendance_for_date_and_class(classe_id, date_str)
        
        for eleve in eleves:
            eleve_id = eleve["id_eleve"]
            eleve["statut"] = presences.get(eleve_id, {}).get("statut", "Présent")
            eleve["commentaire"] = presences.get(eleve_id, {}).get("commentaire", "")
            eleve["unjustified_absences"] = self.stats_controller.get_unjustified_absences_count(eleve_id)
        return eleves
    
    def get_class_attendance_summary_stats(self, classe_id: int, date_str: str) -> Dict[str, int]:
        """Récupère les statistiques de présence pour une classe et une date"""
        eleves = self.attendance_controller.get_students_by_class(classe_id)
        presences = self.attendance_controller.get_attendance_for_date_and_class(classe_id, date_str)
        
        counts = {"Présent": 0, "Absent": 0, "Retard": 0, "Justifié": 0}
        for eleve in eleves:
            statut = presences.get(eleve["id_eleve"], {}).get("statut", "Présent")
            counts[statut] = counts.get(statut, 0) + 1
        return counts
    
    def get_absence_threshold(self) -> int:
        """Récupère le seuil d'absence"""
        return self.stats_controller.get_absence_threshold()
    
    def get_student_full_history(self, eleve_id: int) -> List[Dict]:
        """Récupère l'historique complet d'un élève"""
        return self.history_controller.get_student_history(eleve_id)
    
    def get_student_stats(self, eleve_id: int) -> AttendanceStatsModel:
        """Récupère les statistiques d'un élève"""
        return self.stats_controller.get_student_attendance_stats(eleve_id)
    
    def validate_all_students_present(self, classe_id: int, date_str: str) -> bool:
        """Valide toutes les présences comme présentes"""
        return self.attendance_controller.bulk_update_attendance(classe_id, date_str, "Présent", "Validation en masse")
    
    def mark_all_students_absent(self, classe_id: int, date_str: str) -> bool:
        """Marque tous les élèves comme absents"""
        return self.attendance_controller.bulk_update_attendance(classe_id, date_str, "Absent", "Marquage en masse")
    
    def reset_all_students_attendance(self, classe_id: int, date_str: str) -> bool:
        """Réinitialise toutes les présences"""
        return self.attendance_controller.reset_all_attendance_for_date(classe_id, date_str)
    
    def update_student_attendance(self, eleve_id: int, classe_id: int, date_str: str, statut: str, commentaire: Optional[str], justificatif_path: Optional[str] = None):
        """Met à jour ou ajoute une présence pour un élève"""
        presences = self.attendance_controller.get_attendance_for_date_and_class(classe_id, date_str)
        if eleve_id in presences:
            self.attendance_controller.update_attendance(eleve_id, classe_id, date_str, statut, commentaire, justificatif_path)
        else:
            from ..models.attendance_model import AttendanceModel
            attendance_model = AttendanceModel(
                eleve_id=eleve_id,
                classe_id=classe_id,
                date=date_str,
                statut=statut,
                commentaire=commentaire
            )
            self.attendance_controller.add_attendance(attendance_model)
    
    def get_classes_for_dropdown(self) -> List[str]:
        """Récupère les noms des classes pour un menu déroulant"""
        classes = self.attendance_controller.get_all_classes()
        return [c["nom_classe"] for c in classes]
    
    def get_class_id_map(self) -> Dict[str, int]:
        """Récupère un mapping nom_classe -> id_classe"""
        classes = self.attendance_controller.get_all_classes()
        return {c["nom_classe"]: c["id_classe"] for c in classes}
    
    def get_classes_with_students(self) -> List[Dict]:
        """Récupère toutes les classes avec le nombre d'élèves"""
        classes = self.attendance_controller.get_all_classes()
        
        for classe in classes:
            students = self.attendance_controller.get_students_by_class(classe['id_classe'])
            classe['student_count'] = len(students)
        
        return classes
    
    def get_class_attendance_overview(self, classe_id: int, date: str) -> Dict:
        """Récupère un aperçu complet des présences d'une classe"""
        # Récupérer les élèves
        students = self.attendance_controller.get_students_by_class(classe_id)
        
        # Récupérer les présences existantes
        attendance_map = self.attendance_controller.get_attendance_for_date_and_class(classe_id, date)
        
        # Récupérer les statistiques
        stats = self.stats_controller.get_attendance_counts_by_status(classe_id, date)
        
        # Préparer les données des élèves avec leurs statuts
        students_with_attendance = []
        for student in students:
            eleve_id = student['id_eleve']
            attendance_data = attendance_map.get(eleve_id, {})
            
            students_with_attendance.append({
                **student,
                'statut': attendance_data.get('statut', 'Présent'),
                'commentaire': attendance_data.get('commentaire', ''),
                'has_attendance_record': eleve_id in attendance_map
            })
        
        return {
            'students': students_with_attendance,
            'stats': stats,
            'total_students': len(students),
            'date': date,
            'classe_id': classe_id
        }
    
    def validate_all_present(self, classe_id: int, date: str, commentaire: str = "Validation en masse") -> bool:
        """Valide toutes les présences comme Présent"""
        return self.attendance_controller.bulk_update_attendance(
            classe_id, date, "Présent", commentaire
        )
    
    def mark_all_absent(self, classe_id: int, date: str, commentaire: str = "Marquage en masse") -> bool:
        """Marque toutes les présences comme Absent"""
        return self.attendance_controller.bulk_update_attendance(
            classe_id, date, "Absent", commentaire
        )
    
    def reset_all_attendance(self, classe_id: int, date: str) -> bool:
        """Réinitialise toutes les présences"""
        return self.attendance_controller.delete_attendance_for_date(classe_id, date)
    
    def update_student_attendance(self, eleve_id: int, classe_id: int, date: str, 
                                 statut: str, commentaire: str = "") -> bool:
        """Met à jour la présence d'un élève"""
        attendance = AttendanceModel(
            eleve_id=eleve_id,
            classe_id=classe_id,
            date=date,
            statut=statut,
            commentaire=commentaire
        )
        
        # Vérifier si la présence existe déjà
        attendance_map = self.attendance_controller.get_attendance_for_date_and_class(classe_id, date)
        
        if eleve_id in attendance_map:
            return self.attendance_controller.update_attendance(attendance)
        else:
            return self.attendance_controller.add_attendance(attendance)
    
    def get_student_detailed_stats(self, eleve_id: int, start_date: str = None, 
                                  end_date: str = None) -> Dict:
        """Récupère les statistiques détaillées d'un élève"""
        stats = self.stats_controller.get_student_attendance_stats(eleve_id, start_date, end_date)
        history = self.history_controller.get_student_history(eleve_id)
        patterns = self.history_controller.get_absence_patterns(eleve_id)
        trends = self.history_controller.get_attendance_trends(eleve_id)
        
        return {
            'stats': stats.to_dict(),
            'history': [h.to_dict() for h in history],
            'patterns': patterns,
            'trends': trends
        }
    
    def get_class_performance_summary(self, classe_id: int, start_date: str = None, 
                                    end_date: str = None) -> Dict:
        """Récupère un résumé des performances de présence d'une classe"""
        summary = self.stats_controller.get_class_attendance_summary(classe_id, start_date, end_date)
        students = self.attendance_controller.get_students_by_class(classe_id)
        
        # Calculer les statistiques globales
        total_days = len(summary)
        total_presents = sum(day['presents'] for day in summary)
        total_absents = sum(day['absents'] for day in summary)
        total_retards = sum(day['retards'] for day in summary)
        total_justifies = sum(day['justifies'] for day in summary)
        
        if total_days > 0 and len(students) > 0:
            total_possible = total_days * len(students)
            overall_attendance_rate = (total_presents / total_possible) * 100
        else:
            overall_attendance_rate = 0
        
        return {
            'summary': summary,
            'overall_stats': {
                'total_days': total_days,
                'total_students': len(students),
                'total_presents': total_presents,
                'total_absents': total_absents,
                'total_retards': total_retards,
                'total_justifies': total_justifies,
                'overall_attendance_rate': overall_attendance_rate
            }
        }
    
    def search_attendance_records(self, search_term: str, classe_id: int = None, 
                                start_date: str = None, end_date: str = None) -> List[Dict]:
        """Recherche dans les enregistrements de présence"""
        results = self.history_controller.search_attendance_history(
            search_term, classe_id, start_date, end_date
        )
        return [r.to_dict() for r in results]
    
    def get_attendance_alerts(self, classe_id: int, threshold_days: int = 3) -> List[Dict]:
        """Récupère les alertes de présence (élèves avec trop d'absences)"""
        students = self.attendance_controller.get_students_by_class(classe_id)
        alerts = []
        
        for student in students:
            eleve_id = student['id_eleve']
            unjustified_absences = self.stats_controller.get_unjustified_absences_count(eleve_id)
            
            if unjustified_absences >= threshold_days:
                alerts.append({
                    'eleve_id': eleve_id,
                    'nom': f"{student['prenom']} {student['nom']}",
                    'unjustified_absences': unjustified_absences,
                    'alert_level': 'high' if unjustified_absences >= threshold_days * 2 else 'medium'
                })
        
        return alerts
