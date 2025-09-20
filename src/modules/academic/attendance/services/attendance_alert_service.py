# Service de gestion des alertes et seuils de présence
from typing import List, Dict, Optional, Tuple
from datetime import datetime, timedelta
from enum import Enum
from ..controllers.attendance_controller import AttendanceController
from ..controllers.attendance_stats_controller import AttendanceStatsController

class AlertLevel(Enum):
    """Niveaux d'alerte"""
    INFO = "info"
    WARNING = "warning"
    CRITICAL = "critical"
    EMERGENCY = "emergency"

class AttendanceAlertService:
    """Service de gestion des alertes et seuils de présence"""
    
    def __init__(self):
        self.attendance_controller = AttendanceController()
        self.stats_controller = AttendanceStatsController()
        
        # Seuils configurables
        self.thresholds = {
            'absence_warning': 3,      # Alerte après 3 absences
            'absence_critical': 5,     # Critique après 5 absences
            'absence_emergency': 10,   # Urgence après 10 absences
            'attendance_rate_warning': 85,  # Alerte si taux < 85%
            'attendance_rate_critical': 75,  # Critique si taux < 75%
            'consecutive_absences': 3,  # Alerte après 3 absences consécutives
            'late_arrivals': 5         # Alerte après 5 retards
        }
    
    def check_student_alerts(self, eleve_id: int, period_days: int = 30) -> List[Dict]:
        """Vérifie les alertes pour un élève"""
        try:
            alerts = []
            end_date = datetime.now().strftime("%Y-%m-%d")
            start_date = (datetime.now() - timedelta(days=period_days)).strftime("%Y-%m-%d")
            
            # Récupérer les statistiques
            stats = self.stats_controller.get_student_attendance_stats(eleve_id, start_date, end_date)
            
            # Vérifier les seuils d'absence
            if stats.absents >= self.thresholds['absence_emergency']:
                alerts.append({
                    'type': 'absence_count',
                    'level': AlertLevel.EMERGENCY,
                    'message': f"URGENCE: {stats.absents} absences en {period_days} jours",
                    'value': stats.absents,
                    'threshold': self.thresholds['absence_emergency']
                })
            elif stats.absents >= self.thresholds['absence_critical']:
                alerts.append({
                    'type': 'absence_count',
                    'level': AlertLevel.CRITICAL,
                    'message': f"CRITIQUE: {stats.absents} absences en {period_days} jours",
                    'value': stats.absents,
                    'threshold': self.thresholds['absence_critical']
                })
            elif stats.absents >= self.thresholds['absence_warning']:
                alerts.append({
                    'type': 'absence_count',
                    'level': AlertLevel.WARNING,
                    'message': f"ATTENTION: {stats.absents} absences en {period_days} jours",
                    'value': stats.absents,
                    'threshold': self.thresholds['absence_warning']
                })
            
            # Vérifier le taux de présence
            if stats.taux_presence < self.thresholds['attendance_rate_critical']:
                alerts.append({
                    'type': 'attendance_rate',
                    'level': AlertLevel.CRITICAL,
                    'message': f"Taux de présence critique: {stats.taux_presence:.1f}%",
                    'value': stats.taux_presence,
                    'threshold': self.thresholds['attendance_rate_critical']
                })
            elif stats.taux_presence < self.thresholds['attendance_rate_warning']:
                alerts.append({
                    'type': 'attendance_rate',
                    'level': AlertLevel.WARNING,
                    'message': f"Taux de présence faible: {stats.taux_presence:.1f}%",
                    'value': stats.taux_presence,
                    'threshold': self.thresholds['attendance_rate_warning']
                })
            
            # Vérifier les retards répétés
            if stats.retards >= self.thresholds['late_arrivals']:
                alerts.append({
                    'type': 'late_arrivals',
                    'level': AlertLevel.WARNING,
                    'message': f"Retards répétés: {stats.retards} en {period_days} jours",
                    'value': stats.retards,
                    'threshold': self.thresholds['late_arrivals']
                })
            
            # Vérifier les absences consécutives
            consecutive_absences = self._check_consecutive_absences(eleve_id)
            if consecutive_absences >= self.thresholds['consecutive_absences']:
                alerts.append({
                    'type': 'consecutive_absences',
                    'level': AlertLevel.CRITICAL,
                    'message': f"Absences consécutives: {consecutive_absences} jours",
                    'value': consecutive_absences,
                    'threshold': self.thresholds['consecutive_absences']
                })
            
            return alerts
            
        except Exception as e:
            print(f"❌ Erreur vérification alertes: {e}")
            return []
    
    def check_class_alerts(self, classe_id: int) -> List[Dict]:
        """Vérifie les alertes pour une classe entière"""
        try:
            alerts = []
            students = self.attendance_controller.get_students_by_class(classe_id)
            
            # Statistiques globales de la classe
            total_students = len(students)
            students_with_alerts = 0
            critical_alerts = 0
            
            for student in students:
                student_alerts = self.check_student_alerts(student['id_eleve'])
                if student_alerts:
                    students_with_alerts += 1
                    critical_alerts += len([a for a in student_alerts if a['level'] == AlertLevel.CRITICAL])
            
            # Alerte si trop d'élèves ont des problèmes
            alert_percentage = (students_with_alerts / total_students * 100) if total_students > 0 else 0
            
            if alert_percentage > 30:  # Plus de 30% d'élèves avec alertes
                alerts.append({
                    'type': 'class_alert_percentage',
                    'level': AlertLevel.CRITICAL,
                    'message': f"{alert_percentage:.1f}% des élèves ont des problèmes de présence",
                    'value': alert_percentage,
                    'students_affected': students_with_alerts,
                    'total_students': total_students
                })
            
            if critical_alerts > 0:
                alerts.append({
                    'type': 'critical_alerts_count',
                    'level': AlertLevel.CRITICAL,
                    'message': f"{critical_alerts} alertes critiques dans la classe",
                    'value': critical_alerts
                })
            
            return alerts
            
        except Exception as e:
            print(f"❌ Erreur alertes classe: {e}")
            return []
    
    def get_students_at_risk(self, classe_id: int = None) -> List[Dict]:
        """Récupère la liste des élèves à risque"""
        try:
            at_risk_students = []
            
            if classe_id:
                students = self.attendance_controller.get_students_by_class(classe_id)
            else:
                # Récupérer tous les élèves de toutes les classes
                classes = self.attendance_controller.get_all_classes()
                students = []
                for classe in classes:
                    students.extend(self.attendance_controller.get_students_by_class(classe['id_classe']))
            
            for student in students:
                alerts = self.check_student_alerts(student['id_eleve'])
                critical_alerts = [a for a in alerts if a['level'] in [AlertLevel.CRITICAL, AlertLevel.EMERGENCY]]
                
                if critical_alerts:
                    stats = self.stats_controller.get_student_attendance_stats(student['id_eleve'])
                    
                    at_risk_students.append({
                        'eleve_id': student['id_eleve'],
                        'nom': f"{student['prenom']} {student['nom']}",
                        'email': student['email'],
                        'taux_presence': stats.taux_presence,
                        'absents': stats.absents,
                        'retards': stats.retards,
                        'alerts': critical_alerts,
                        'risk_level': self._calculate_risk_level(critical_alerts)
                    })
            
            # Trier par niveau de risque
            return sorted(at_risk_students, key=lambda x: x['risk_level'], reverse=True)
            
        except Exception as e:
            print(f"❌ Erreur élèves à risque: {e}")
            return []
    
    def generate_alert_report(self, start_date: str, end_date: str) -> Dict:
        """Génère un rapport des alertes sur une période"""
        try:
            report = {
                'periode': f"{start_date} à {end_date}",
                'total_alerts': 0,
                'by_level': {
                    'info': 0,
                    'warning': 0,
                    'critical': 0,
                    'emergency': 0
                },
                'by_type': {},
                'students_at_risk': 0,
                'classes_affected': 0,
                'recommendations': []
            }
            
            # Analyser toutes les classes
            classes = self.attendance_controller.get_all_classes()
            classes_with_alerts = 0
            
            for classe in classes:
                class_alerts = self.check_class_alerts(classe['id_classe'])
                if class_alerts:
                    classes_with_alerts += 1
                
                # Analyser les élèves de la classe
                students = self.attendance_controller.get_students_by_class(classe['id_classe'])
                for student in students:
                    student_alerts = self.check_student_alerts(student['id_eleve'])
                    
                    for alert in student_alerts:
                        report['total_alerts'] += 1
                        report['by_level'][alert['level'].value] += 1
                        
                        alert_type = alert['type']
                        report['by_type'][alert_type] = report['by_type'].get(alert_type, 0) + 1
            
            report['classes_affected'] = classes_with_alerts
            report['students_at_risk'] = len(self.get_students_at_risk())
            
            # Générer des recommandations
            report['recommendations'] = self._generate_recommendations(report)
            
            return report
            
        except Exception as e:
            print(f"❌ Erreur rapport alertes: {e}")
            return {}
    
    def update_thresholds(self, new_thresholds: Dict) -> bool:
        """Met à jour les seuils d'alerte"""
        try:
            self.thresholds.update(new_thresholds)
            print("✅ Seuils d'alerte mis à jour")
            return True
        except Exception as e:
            print(f"❌ Erreur mise à jour seuils: {e}")
            return False
    
    def _check_consecutive_absences(self, eleve_id: int) -> int:
        """Vérifie le nombre d'absences consécutives"""
        try:
            # Récupérer l'historique récent
            from ..controllers.attendance_history_controller import AttendanceHistoryController
            history_controller = AttendanceHistoryController()
            history = history_controller.get_student_history(eleve_id)
            
            consecutive_count = 0
            current_date = datetime.now().date()
            
            # Compter les absences consécutives depuis aujourd'hui
            for record in history:
                record_date = record.date.date() if hasattr(record.date, 'date') else datetime.strptime(str(record.date), "%Y-%m-%d").date()
                
                if record_date == current_date - timedelta(days=consecutive_count):
                    if record.statut == 'Absent':
                        consecutive_count += 1
                        current_date = record_date
                    else:
                        break
                else:
                    break
            
            return consecutive_count
            
        except Exception as e:
            print(f"❌ Erreur absences consécutives: {e}")
            return 0
    
    def _calculate_risk_level(self, alerts: List[Dict]) -> int:
        """Calcule le niveau de risque d'un élève"""
        risk_score = 0
        
        for alert in alerts:
            if alert['level'] == AlertLevel.EMERGENCY:
                risk_score += 4
            elif alert['level'] == AlertLevel.CRITICAL:
                risk_score += 3
            elif alert['level'] == AlertLevel.WARNING:
                risk_score += 2
            else:
                risk_score += 1
        
        return min(risk_score, 10)  # Score max de 10
    
    def _generate_recommendations(self, report: Dict) -> List[str]:
        """Génère des recommandations basées sur le rapport"""
        recommendations = []
        
        if report['by_level']['emergency'] > 0:
            recommendations.append("🚨 Actions immédiates requises pour les cas d'urgence")
        
        if report['by_level']['critical'] > 5:
            recommendations.append("⚠️ Renforcer le suivi des élèves avec alertes critiques")
        
        if report['by_type'].get('consecutive_absences', 0) > 0:
            recommendations.append("📞 Contacter les familles des élèves avec absences consécutives")
        
        if report['by_type'].get('attendance_rate', 0) > 3:
            recommendations.append("📊 Mettre en place un suivi personnalisé pour les élèves à faible taux de présence")
        
        if report['classes_affected'] > report['classes_affected'] * 0.5:
            recommendations.append("🏫 Organiser une réunion avec les équipes pédagogiques")
        
        return recommendations
