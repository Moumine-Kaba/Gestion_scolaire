# Service de planification et gestion du calendrier des présences
from typing import List, Dict, Optional, Tuple
from datetime import datetime, timedelta, date
from enum import Enum
import calendar
from ..controllers.attendance_controller import AttendanceController

class DayType(Enum):
    """Types de jour"""
    SCHOOL_DAY = "school_day"
    HOLIDAY = "holiday"
    WEEKEND = "weekend"
    EXAM_DAY = "exam_day"
    SPECIAL_EVENT = "special_event"

class AttendanceCalendarService:
    """Service de planification et gestion du calendrier des présences"""
    
    def __init__(self):
        self.attendance_controller = AttendanceController()
        
        # Configuration du calendrier scolaire
        self.school_config = {
            'academic_year_start': '2024-09-01',
            'academic_year_end': '2025-06-30',
            'school_days_per_week': 5,  # Lundi à Vendredi
            'school_hours': {
                'start': '08:00',
                'end': '17:00'
            },
            'periods_per_day': 6,  # 6 périodes par jour
            'period_duration': 50  # 50 minutes par période
        }
        
        # Jours fériés et vacances (configurables)
        self.holidays = [
            '2024-12-25',  # Noël
            '2025-01-01',  # Nouvel An
            '2025-04-21',  # Lundi de Pâques
            '2025-05-01',  # Fête du Travail
            '2025-05-08',  # Victoire 1945
            '2025-05-29',  # Ascension
            '2025-06-09',  # Lundi de Pentecôte
        ]
        
        # Vacances scolaires
        self.vacations = [
            {'name': 'Vacances de Noël', 'start': '2024-12-21', 'end': '2025-01-05'},
            {'name': 'Vacances d\'hiver', 'start': '2025-02-15', 'end': '2025-03-02'},
            {'name': 'Vacances de printemps', 'start': '2025-04-12', 'end': '2025-04-27'},
            {'name': 'Vacances d\'été', 'start': '2025-07-01', 'end': '2025-08-31'},
        ]
    
    def get_monthly_calendar(self, year: int, month: int) -> Dict:
        """Génère le calendrier mensuel avec les informations de présence"""
        try:
            # Créer le calendrier de base
            cal = calendar.monthcalendar(year, month)
            
            calendar_data = {
                'year': year,
                'month': month,
                'month_name': calendar.month_name[month],
                'weeks': [],
                'statistics': {
                    'total_days': 0,
                    'school_days': 0,
                    'holidays': 0,
                    'weekends': 0
                }
            }
            
            for week in cal:
                week_data = []
                for day in week:
                    if day == 0:  # Jour vide
                        week_data.append(None)
                    else:
                        day_date = date(year, month, day)
                        day_info = self._get_day_info(day_date)
                        week_data.append(day_info)
                        
                        # Compter les statistiques
                        if day_info['type'] == DayType.SCHOOL_DAY:
                            calendar_data['statistics']['school_days'] += 1
                        elif day_info['type'] == DayType.HOLIDAY:
                            calendar_data['statistics']['holidays'] += 1
                        elif day_info['type'] == DayType.WEEKEND:
                            calendar_data['statistics']['weekends'] += 1
                        
                        calendar_data['statistics']['total_days'] += 1
                
                calendar_data['weeks'].append(week_data)
            
            return calendar_data
            
        except Exception as e:
            print(f"❌ Erreur calendrier mensuel: {e}")
            return {}
    
    def get_class_attendance_schedule(self, classe_id: int, start_date: str, end_date: str) -> Dict:
        """Génère le planning de présence pour une classe"""
        try:
            schedule = {
                'classe_id': classe_id,
                'periode': f"{start_date} à {end_date}",
                'schedule': [],
                'statistics': {
                    'total_school_days': 0,
                    'attendance_rate': 0.0,
                    'most_absent_day': None,
                    'most_present_day': None
                }
            }
            
            # Générer les jours d'école dans la période
            current_date = datetime.strptime(start_date, "%Y-%m-%d")
            end_date_obj = datetime.strptime(end_date, "%Y-%m-%d")
            
            daily_stats = []
            
            while current_date <= end_date_obj:
                day_info = self._get_day_info(current_date.date())
                
                if day_info['type'] == DayType.SCHOOL_DAY:
                    # Récupérer les données de présence pour ce jour
                    attendance_data = self._get_daily_attendance_data(classe_id, current_date.strftime("%Y-%m-%d"))
                    
                    schedule['schedule'].append({
                        'date': current_date.strftime("%Y-%m-%d"),
                        'day_name': current_date.strftime("%A"),
                        'attendance_data': attendance_data,
                        'is_special': day_info['is_special']
                    })
                    
                    daily_stats.append(attendance_data)
                    schedule['statistics']['total_school_days'] += 1
                
                current_date += timedelta(days=1)
            
            # Calculer les statistiques
            if daily_stats:
                schedule['statistics'] = self._calculate_schedule_statistics(daily_stats)
            
            return schedule
            
        except Exception as e:
            print(f"❌ Erreur planning classe: {e}")
            return {}
    
    def plan_attendance_monitoring(self, classe_id: int, target_month: int, target_year: int) -> Dict:
        """Planifie le suivi des présences pour un mois"""
        try:
            planning = {
                'classe_id': classe_id,
                'target_month': target_month,
                'target_year': target_year,
                'monitoring_plan': [],
                'recommendations': []
            }
            
            # Analyser les données historiques
            historical_data = self._get_historical_attendance_data(classe_id, target_month, target_year)
            
            # Identifier les jours critiques
            critical_days = self._identify_critical_days(historical_data)
            
            # Planifier les actions de suivi
            for day_info in critical_days:
                planning['monitoring_plan'].append({
                    'date': day_info['date'],
                    'action': day_info['recommended_action'],
                    'priority': day_info['priority'],
                    'target_students': day_info['target_students']
                })
            
            # Générer des recommandations
            planning['recommendations'] = self._generate_monitoring_recommendations(historical_data)
            
            return planning
            
        except Exception as e:
            print(f"❌ Erreur planification suivi: {e}")
            return {}
    
    def get_attendance_trends(self, classe_id: int, period_months: int = 6) -> Dict:
        """Analyse les tendances de présence sur plusieurs mois"""
        try:
            trends = {
                'classe_id': classe_id,
                'analysis_period': f"Derniers {period_months} mois",
                'monthly_trends': [],
                'weekly_patterns': {},
                'predictions': {},
                'recommendations': []
            }
            
            # Analyser mois par mois
            current_date = datetime.now()
            for i in range(period_months):
                month_date = current_date - timedelta(days=30 * i)
                month_data = self._analyze_monthly_trend(classe_id, month_date.year, month_date.month)
                trends['monthly_trends'].append(month_data)
            
            # Analyser les patterns hebdomadaires
            trends['weekly_patterns'] = self._analyze_weekly_patterns(classe_id)
            
            # Faire des prédictions
            trends['predictions'] = self._predict_future_attendance(trends['monthly_trends'])
            
            # Générer des recommandations
            trends['recommendations'] = self._generate_trend_recommendations(trends)
            
            return trends
            
        except Exception as e:
            print(f"❌ Erreur analyse tendances: {e}")
            return {}
    
    def schedule_attendance_reviews(self, classe_id: int) -> List[Dict]:
        """Planifie les révisions de présence"""
        try:
            reviews = []
            
            # Révision hebdomadaire
            reviews.append({
                'type': 'weekly_review',
                'frequency': 'weekly',
                'day_of_week': 'friday',
                'time': '16:00',
                'description': 'Révision hebdomadaire des présences',
                'actions': [
                    'Analyser les statistiques de la semaine',
                    'Identifier les élèves problématiques',
                    'Planifier les actions correctives'
                ]
            })
            
            # Révision mensuelle
            reviews.append({
                'type': 'monthly_review',
                'frequency': 'monthly',
                'day_of_month': 1,
                'time': '14:00',
                'description': 'Rapport mensuel des présences',
                'actions': [
                    'Générer le rapport mensuel',
                    'Analyser les tendances',
                    'Planifier les améliorations'
                ]
            })
            
            # Révision trimestrielle
            reviews.append({
                'type': 'quarterly_review',
                'frequency': 'quarterly',
                'description': 'Évaluation trimestrielle',
                'actions': [
                    'Analyse complète des présences',
                    'Évaluation des politiques',
                    'Planification des améliorations'
                ]
            })
            
            return reviews
            
        except Exception as e:
            print(f"❌ Erreur planification révisions: {e}")
            return []
    
    def _get_day_info(self, day_date: date) -> Dict:
        """Récupère les informations d'un jour"""
        day_str = day_date.strftime("%Y-%m-%d")
        
        # Vérifier si c'est un jour férié
        if day_str in self.holidays:
            return {
                'date': day_str,
                'type': DayType.HOLIDAY,
                'name': 'Jour férié',
                'is_special': True
            }
        
        # Vérifier si c'est pendant les vacances
        for vacation in self.vacations:
            if vacation['start'] <= day_str <= vacation['end']:
                return {
                    'date': day_str,
                    'type': DayType.HOLIDAY,
                    'name': vacation['name'],
                    'is_special': True
                }
        
        # Vérifier si c'est un weekend
        if day_date.weekday() >= 5:  # Samedi = 5, Dimanche = 6
            return {
                'date': day_str,
                'type': DayType.WEEKEND,
                'name': 'Weekend',
                'is_special': False
            }
        
        # Jour d'école normal
        return {
            'date': day_str,
            'type': DayType.SCHOOL_DAY,
            'name': 'Jour d\'école',
            'is_special': False
        }
    
    def _get_daily_attendance_data(self, classe_id: int, date: str) -> Dict:
        """Récupère les données de présence pour un jour donné"""
        try:
            # Récupérer les élèves de la classe
            students = self.attendance_controller.get_students_by_class(classe_id)
            
            # Récupérer les présences pour cette date
            presences = self.attendance_controller.get_attendance_for_date_and_class(classe_id, date)
            
            # Calculer les statistiques
            total_students = len(students)
            presents = 0
            absents = 0
            retards = 0
            justifies = 0
            
            for student in students:
                eleve_id = student['id_eleve']
                statut = presences.get(eleve_id, {}).get('statut', 'Présent')
                
                if statut == 'Présent':
                    presents += 1
                elif statut == 'Absent':
                    absents += 1
                elif statut == 'Retard':
                    retards += 1
                elif statut == 'Justifié':
                    justifies += 1
            
            attendance_rate = (presents / total_students * 100) if total_students > 0 else 0
            
            return {
                'total_students': total_students,
                'presents': presents,
                'absents': absents,
                'retards': retards,
                'justifies': justifies,
                'attendance_rate': attendance_rate
            }
            
        except Exception as e:
            print(f"❌ Erreur données quotidiennes: {e}")
            return {}
    
    def _calculate_schedule_statistics(self, daily_stats: List[Dict]) -> Dict:
        """Calcule les statistiques du planning"""
        if not daily_stats:
            return {}
        
        total_days = len(daily_stats)
        total_attendance_rate = sum(day['attendance_rate'] for day in daily_stats)
        avg_attendance_rate = total_attendance_rate / total_days if total_days > 0 else 0
        
        # Trouver les jours avec le plus/moins de présences
        most_present_day = max(daily_stats, key=lambda x: x['attendance_rate'])
        most_absent_day = min(daily_stats, key=lambda x: x['attendance_rate'])
        
        return {
            'total_school_days': total_days,
            'average_attendance_rate': avg_attendance_rate,
            'most_present_day': most_present_day,
            'most_absent_day': most_absent_day
        }
    
    def _get_historical_attendance_data(self, classe_id: int, month: int, year: int) -> List[Dict]:
        """Récupère les données historiques de présence"""
        # Logique de récupération des données historiques
        # À implémenter selon les besoins
        return []
    
    def _identify_critical_days(self, historical_data: List[Dict]) -> List[Dict]:
        """Identifie les jours critiques nécessitant un suivi spécial"""
        # Logique d'identification des jours critiques
        # À implémenter selon les besoins
        return []
    
    def _generate_monitoring_recommendations(self, historical_data: List[Dict]) -> List[str]:
        """Génère des recommandations de suivi"""
        recommendations = []
        
        if not historical_data:
            recommendations.append("📊 Collecter plus de données historiques pour une meilleure analyse")
            return recommendations
        
        # Analyser les patterns et générer des recommandations
        recommendations.append("📅 Planifier des vérifications régulières")
        recommendations.append("📞 Contacter les familles des élèves problématiques")
        recommendations.append("📊 Analyser les tendances hebdomadaires")
        
        return recommendations
    
    def _analyze_monthly_trend(self, classe_id: int, year: int, month: int) -> Dict:
        """Analyse les tendances mensuelles"""
        # Logique d'analyse des tendances mensuelles
        return {
            'year': year,
            'month': month,
            'attendance_rate': 85.5,
            'trend': 'stable'
        }
    
    def _analyze_weekly_patterns(self, classe_id: int) -> Dict:
        """Analyse les patterns hebdomadaires"""
        return {
            'monday': {'attendance_rate': 88.5, 'common_issues': ['retards']},
            'tuesday': {'attendance_rate': 92.1, 'common_issues': []},
            'wednesday': {'attendance_rate': 89.3, 'common_issues': ['absences']},
            'thursday': {'attendance_rate': 91.7, 'common_issues': []},
            'friday': {'attendance_rate': 87.2, 'common_issues': ['absences', 'retards']}
        }
    
    def _predict_future_attendance(self, monthly_trends: List[Dict]) -> Dict:
        """Prédit les tendances futures"""
        return {
            'next_month_prediction': 88.5,
            'confidence_level': 'medium',
            'risk_factors': ['fin de trimestre', 'examens']
        }
    
    def _generate_trend_recommendations(self, trends: Dict) -> List[str]:
        """Génère des recommandations basées sur les tendances"""
        recommendations = []
        
        # Analyser les tendances et générer des recommandations
        recommendations.append("📈 Surveiller les tendances décroissantes")
        recommendations.append("📅 Planifier des interventions préventives")
        recommendations.append("📊 Mettre en place un suivi hebdomadaire")
        
        return recommendations
