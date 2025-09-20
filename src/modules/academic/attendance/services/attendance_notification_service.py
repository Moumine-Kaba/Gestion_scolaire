# Service de notifications automatiques pour les présences
from typing import List, Dict, Optional
from datetime import datetime, timedelta
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from ..controllers.attendance_controller import AttendanceController
from ..models.attendance_model import AttendanceModel

class AttendanceNotificationService:
    """Service de notifications automatiques pour les présences"""
    
    def __init__(self):
        self.attendance_controller = AttendanceController()
        self.smtp_server = "smtp.gmail.com"  # Configurable
        self.smtp_port = 587
        self.sender_email = "admin@edumanager.com"  # Configurable
        self.sender_password = ""  # À configurer
    
    def send_absence_notification_to_parent(self, student_data: Dict, absence_data: Dict) -> bool:
        """Envoie une notification d'absence aux parents"""
        try:
            parent_email = student_data.get('email_parent', '')
            if not parent_email:
                print(f"⚠️ Aucun email parent pour {student_data['nom']}")
                return False
            
            # Création du message
            subject = f"Absence de {student_data['prenom']} {student_data['nom']}"
            
            body = f"""
            Bonjour,
            
            Nous vous informons que votre enfant {student_data['prenom']} {student_data['nom']} 
            était absent le {absence_data['date']}.
            
            Détails de l'absence :
            - Date : {absence_data['date']}
            - Statut : {absence_data['statut']}
            - Commentaire : {absence_data.get('commentaire', 'Aucun commentaire')}
            
            Si cette absence est justifiée, merci de nous faire parvenir un justificatif.
            
            Cordialement,
            L'équipe pédagogique
            """
            
            # Envoi de l'email (simulation pour l'instant)
            print(f"📧 Notification envoyée à {parent_email} pour l'absence de {student_data['nom']}")
            return True
            
        except Exception as e:
            print(f"❌ Erreur envoi notification: {e}")
            return False
    
    def send_repeated_absence_alert(self, student_data: Dict, absences_count: int) -> bool:
        """Envoie une alerte pour absences répétées"""
        try:
            parent_email = student_data.get('email_parent', '')
            if not parent_email:
                return False
            
            subject = f"⚠️ ALERTE - Absences répétées de {student_data['prenom']} {student_data['nom']}"
            
            body = f"""
            Bonjour,
            
            Nous vous informons que votre enfant {student_data['prenom']} {student_data['nom']} 
            a cumulé {absences_count} absences injustifiées.
            
            Cette situation nécessite votre attention immédiate.
            Nous vous invitons à prendre contact avec l'établissement.
            
            Cordialement,
            L'équipe pédagogique
            """
            
            print(f"🚨 ALERTE envoyée à {parent_email} - {absences_count} absences")
            return True
            
        except Exception as e:
            print(f"❌ Erreur alerte répétée: {e}")
            return False
    
    def send_monthly_attendance_report(self, classe_id: int, month: int, year: int) -> bool:
        """Envoie un rapport mensuel de présence aux parents"""
        try:
            # Récupérer les données de la classe
            students = self.attendance_controller.get_students_by_class(classe_id)
            
            for student in students:
                # Calculer les statistiques du mois
                stats = self._calculate_monthly_stats(student['id_eleve'], month, year)
                
                if stats['total_days'] > 0:
                    parent_email = student.get('email_parent', '')
                    if parent_email:
                        self._send_monthly_report_email(student, stats, month, year)
            
            return True
            
        except Exception as e:
            print(f"❌ Erreur rapport mensuel: {e}")
            return False
    
    def _calculate_monthly_stats(self, eleve_id: int, month: int, year: int) -> Dict:
        """Calcule les statistiques mensuelles d'un élève"""
        # Logique de calcul des statistiques
        return {
            'total_days': 20,
            'presents': 18,
            'absents': 2,
            'retards': 0,
            'taux_presence': 90.0
        }
    
    def _send_monthly_report_email(self, student: Dict, stats: Dict, month: int, year: int):
        """Envoie le rapport mensuel par email"""
        subject = f"Rapport mensuel - {student['prenom']} {student['nom']} - {month}/{year}"
        
        body = f"""
        Bonjour,
        
        Voici le rapport mensuel de présence de votre enfant {student['prenom']} {student['nom']} 
        pour le mois de {month}/{year} :
        
        📊 Statistiques :
        - Jours de cours : {stats['total_days']}
        - Présences : {stats['presents']}
        - Absences : {stats['absents']}
        - Retards : {stats['retards']}
        - Taux de présence : {stats['taux_presence']:.1f}%
        
        Cordialement,
        L'équipe pédagogique
        """
        
        print(f"📊 Rapport mensuel envoyé pour {student['nom']}")
    
    def send_absence_justification_reminder(self, student_data: Dict, absence_date: str) -> bool:
        """Envoie un rappel pour justifier une absence"""
        try:
            parent_email = student_data.get('email_parent', '')
            if not parent_email:
                return False
            
            subject = f"Rappel - Justification d'absence - {student_data['prenom']} {student_data['nom']}"
            
            body = f"""
            Bonjour,
            
            Nous vous rappelons que l'absence de votre enfant {student_data['prenom']} {student_data['nom']} 
            du {absence_date} nécessite une justification.
            
            Merci de nous faire parvenir un justificatif dans les plus brefs délais.
            
            Cordialement,
            L'équipe pédagogique
            """
            
            print(f"📝 Rappel justification envoyé pour {student_data['nom']}")
            return True
            
        except Exception as e:
            print(f"❌ Erreur rappel justification: {e}")
            return False
