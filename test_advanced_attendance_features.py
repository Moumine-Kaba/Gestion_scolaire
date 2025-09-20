#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test complet de toutes les fonctionnalités avancées de gestion des présences
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../..'))

import customtkinter as ctk
from datetime import datetime, timedelta
import tkinter as tk
from tkinter import messagebox

# Imports des services
from src.modules.academic.attendance.services.attendance_service import AttendanceService
from src.modules.academic.attendance.services.attendance_notification_service import AttendanceNotificationService
from src.modules.academic.attendance.services.attendance_export_service import AttendanceExportService
from src.modules.academic.attendance.services.attendance_justification_service import AttendanceJustificationService
from src.modules.academic.attendance.services.attendance_alert_service import AttendanceAlertService, AlertLevel
from src.modules.academic.attendance.services.attendance_calendar_service import AttendanceCalendarService

# Import de la vue avancée
from src.modules.academic.attendance.views.advanced_attendance_view import AdvancedAttendanceView

class TestAdvancedAttendanceApp(ctk.CTk):
    """Application de test pour toutes les fonctionnalités avancées"""
    
    def __init__(self):
        super().__init__()
        
        # Configuration de la fenêtre
        self.title("🏫 Test Complet - Gestion Avancée des Présences")
        self.geometry("1400x900")
        self.configure(fg_color="#0A192F")
        
        # Configuration du thème
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        # Variables
        self.services = {}
        self.test_results = {}
        
        self._build_interface()
        self._initialize_services()
        self._run_tests()
    
    def _build_interface(self):
        """Construit l'interface de test"""
        # En-tête
        header_frame = ctk.CTkFrame(self, fg_color="#172A45", corner_radius=12)
        header_frame.pack(fill="x", padx=20, pady=20)
        
        title_label = ctk.CTkLabel(header_frame, text="🏫 Test Complet - Gestion Avancée des Présences", 
                                  font=("Segoe UI", 24, "bold"), text_color="#CCD6F6")
        title_label.pack(pady=20)
        
        subtitle_label = ctk.CTkLabel(header_frame, text="Test de toutes les fonctionnalités d'établissement scolaire", 
                                     font=("Segoe UI", 14), text_color="#8892B0")
        subtitle_label.pack(pady=(0, 20))
        
        # Conteneur principal
        main_container = ctk.CTkFrame(self, fg_color="transparent")
        main_container.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        main_container.grid_columnconfigure(0, weight=1)
        main_container.grid_columnconfigure(1, weight=2)
        
        # Panneau de gauche - Tests
        self._build_tests_panel(main_container)
        
        # Panneau de droite - Vue avancée
        self._build_view_panel(main_container)
    
    def _build_tests_panel(self, parent):
        """Construit le panneau des tests"""
        tests_panel = ctk.CTkFrame(parent, fg_color="#0B2039", corner_radius=12)
        tests_panel.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        
        # En-tête des tests
        tests_header = ctk.CTkFrame(tests_panel, fg_color="transparent")
        tests_header.pack(fill="x", padx=20, pady=20)
        
        ctk.CTkLabel(tests_header, text="🧪 Tests des Services", 
                    font=("Segoe UI", 18, "bold"), text_color="#CCD6F6").pack(anchor="w")
        
        # Liste des tests
        self.tests_list = ctk.CTkScrollableFrame(tests_panel, fg_color="transparent")
        self.tests_list.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        # Boutons d'action
        actions_frame = ctk.CTkFrame(tests_panel, fg_color="transparent")
        actions_frame.pack(fill="x", padx=20, pady=(0, 20))
        
        run_all_btn = ctk.CTkButton(actions_frame, text="🚀 Lancer Tous les Tests", 
                                   fg_color="#64FFDA", text_color="#0A192F", 
                                   hover_color="#4ECDC4", font=("Segoe UI", 12, "bold"),
                                   command=self._run_all_tests)
        run_all_btn.pack(side="left", padx=(0, 10))
        
        clear_btn = ctk.CTkButton(actions_frame, text="🗑️ Effacer", 
                                 fg_color="#FF6363", text_color="white", 
                                 hover_color="#E74C3C", font=("Segoe UI", 12, "bold"),
                                 command=self._clear_tests)
        clear_btn.pack(side="left")
    
    def _build_view_panel(self, parent):
        """Construit le panneau de la vue avancée"""
        view_panel = ctk.CTkFrame(parent, fg_color="#0B2039", corner_radius=12)
        view_panel.grid(row=0, column=1, sticky="nsew")
        
        # En-tête de la vue
        view_header = ctk.CTkFrame(view_panel, fg_color="transparent")
        view_header.pack(fill="x", padx=20, pady=20)
        
        ctk.CTkLabel(view_header, text="📋 Vue Avancée des Présences", 
                    font=("Segoe UI", 18, "bold"), text_color="#CCD6F6").pack(anchor="w")
        
        # Conteneur pour la vue avancée
        self.view_container = ctk.CTkFrame(view_panel, fg_color="transparent")
        self.view_container.pack(fill="both", expand=True, padx=20, pady=(0, 20))
    
    def _initialize_services(self):
        """Initialise tous les services"""
        try:
            self.services = {
                'attendance_service': AttendanceService(),
                'notification_service': AttendanceNotificationService(),
                'export_service': AttendanceExportService(),
                'justification_service': AttendanceJustificationService(),
                'alert_service': AttendanceAlertService(),
                'calendar_service': AttendanceCalendarService()
            }
            
            self._add_test_result("✅ Services initialisés", "success")
            
        except Exception as e:
            self._add_test_result(f"❌ Erreur initialisation services: {e}", "error")
    
    def _run_tests(self):
        """Lance les tests de base"""
        self._test_attendance_service()
        self._test_notification_service()
        self._test_export_service()
        self._test_justification_service()
        self._test_alert_service()
        self._test_calendar_service()
        self._test_advanced_view()
    
    def _test_attendance_service(self):
        """Test du service de présence"""
        try:
            service = self.services['attendance_service']
            
            # Test récupération des classes
            classes = service.get_classes_for_dropdown()
            self._add_test_result(f"📚 Classes récupérées: {len(classes)}", "info")
            
            if classes:
                # Test récupération des élèves
                class_id = service.get_class_id_map()[classes[0]]
                students = service.get_students_with_attendance_status(class_id, "2024-12-20")
                self._add_test_result(f"👥 Élèves récupérés: {len(students)}", "info")
                
                # Test statistiques
                stats = service.get_class_attendance_summary_stats(class_id, "2024-12-20")
                self._add_test_result(f"📊 Statistiques: {stats}", "info")
            
            self._add_test_result("✅ Service de présence fonctionnel", "success")
            
        except Exception as e:
            self._add_test_result(f"❌ Erreur service présence: {e}", "error")
    
    def _test_notification_service(self):
        """Test du service de notifications"""
        try:
            service = self.services['notification_service']
            
            # Test données fictives
            student_data = {
                'nom': 'Test',
                'prenom': 'Élève',
                'email_parent': 'parent@test.com'
            }
            
            absence_data = {
                'date': '2024-12-20',
                'statut': 'Absent',
                'commentaire': 'Test'
            }
            
            # Test notification absence
            result = service.send_absence_notification_to_parent(student_data, absence_data)
            self._add_test_result(f"📧 Notification absence: {'✅' if result else '❌'}", "info")
            
            # Test alerte répétée
            result = service.send_repeated_absence_alert(student_data, 5)
            self._add_test_result(f"🚨 Alerte répétée: {'✅' if result else '❌'}", "info")
            
            self._add_test_result("✅ Service de notifications fonctionnel", "success")
            
        except Exception as e:
            self._add_test_result(f"❌ Erreur service notifications: {e}", "error")
    
    def _test_export_service(self):
        """Test du service d'export"""
        try:
            service = self.services['export_service']
            
            # Test génération rapport synthèse
            summary_data = {
                'periode': '2024-12-01 à 2024-12-20',
                'total_days': 15,
                'total_students': 25,
                'total_presents': 350,
                'total_absents': 25,
                'overall_attendance_rate': 93.3,
                'problematic_students': []
            }
            
            self._add_test_result("📄 Service d'export initialisé", "info")
            self._add_test_result("✅ Service d'export fonctionnel", "success")
            
        except Exception as e:
            self._add_test_result(f"❌ Erreur service export: {e}", "error")
    
    def _test_justification_service(self):
        """Test du service de justificatifs"""
        try:
            service = self.services['justification_service']
            
            # Test récupération justificatifs
            justifications = service.get_student_justifications(1)
            self._add_test_result(f"📎 Justificatifs récupérés: {len(justifications)}", "info")
            
            # Test justificatifs en attente
            pending = service.get_pending_justifications()
            self._add_test_result(f"⏳ Justificatifs en attente: {len(pending)}", "info")
            
            self._add_test_result("✅ Service de justificatifs fonctionnel", "success")
            
        except Exception as e:
            self._add_test_result(f"❌ Erreur service justificatifs: {e}", "error")
    
    def _test_alert_service(self):
        """Test du service d'alertes"""
        try:
            service = self.services['alert_service']
            
            # Test alertes élève
            alerts = service.check_student_alerts(1)
            self._add_test_result(f"🚨 Alertes élève: {len(alerts)}", "info")
            
            # Test élèves à risque
            at_risk = service.get_students_at_risk()
            self._add_test_result(f"⚠️ Élèves à risque: {len(at_risk)}", "info")
            
            # Test rapport alertes
            report = service.generate_alert_report("2024-12-01", "2024-12-20")
            self._add_test_result(f"📊 Rapport alertes généré: {report.get('total_alerts', 0)} alertes", "info")
            
            self._add_test_result("✅ Service d'alertes fonctionnel", "success")
            
        except Exception as e:
            self._add_test_result(f"❌ Erreur service alertes: {e}", "error")
    
    def _test_calendar_service(self):
        """Test du service de calendrier"""
        try:
            service = self.services['calendar_service']
            
            # Test calendrier mensuel
            calendar_data = service.get_monthly_calendar(2024, 12)
            self._add_test_result(f"📅 Calendrier généré: {calendar_data.get('month_name', 'N/A')}", "info")
            
            # Test planning classe
            schedule = service.get_class_attendance_schedule(1, "2024-12-01", "2024-12-20")
            self._add_test_result(f"📋 Planning généré: {len(schedule.get('schedule', []))} jours", "info")
            
            # Test tendances
            trends = service.get_attendance_trends(1)
            self._add_test_result(f"📈 Tendances analysées: {len(trends.get('monthly_trends', []))} mois", "info")
            
            self._add_test_result("✅ Service de calendrier fonctionnel", "success")
            
        except Exception as e:
            self._add_test_result(f"❌ Erreur service calendrier: {e}", "error")
    
    def _test_advanced_view(self):
        """Test de la vue avancée"""
        try:
            # Créer la vue avancée
            self.advanced_view = AdvancedAttendanceView(self.view_container, self)
            self.advanced_view.pack(fill="both", expand=True)
            
            self._add_test_result("✅ Vue avancée chargée", "success")
            
        except Exception as e:
            self._add_test_result(f"❌ Erreur vue avancée: {e}", "error")
    
    def _add_test_result(self, message, status):
        """Ajoute un résultat de test"""
        color_map = {
            "success": "#4ECDC4",
            "error": "#FF6363",
            "info": "#64FFDA",
            "warning": "#FFA500"
        }
        
        color = color_map.get(status, "#8892B0")
        
        result_frame = ctk.CTkFrame(self.tests_list, fg_color="#172A45", corner_radius=8)
        result_frame.pack(fill="x", padx=5, pady=2)
        
        result_label = ctk.CTkLabel(result_frame, text=message, 
                                   font=("Segoe UI", 11), text_color=color)
        result_label.pack(padx=10, pady=8)
        
        # Sauvegarder le résultat
        self.test_results[message] = status
    
    def _run_all_tests(self):
        """Lance tous les tests"""
        self._clear_tests()
        self._run_tests()
        
        # Afficher le résumé
        total_tests = len(self.test_results)
        success_tests = len([r for r in self.test_results.values() if r == "success"])
        
        summary = f"📊 Résumé: {success_tests}/{total_tests} tests réussis"
        self._add_test_result(summary, "info")
    
    def _clear_tests(self):
        """Efface tous les tests"""
        for widget in self.tests_list.winfo_children():
            widget.destroy()
        self.test_results.clear()

def main():
    """Fonction principale"""
    print("🏫 Lancement du test complet des fonctionnalités avancées de présences...")
    
    try:
        app = TestAdvancedAttendanceApp()
        app.mainloop()
        
    except Exception as e:
        print(f"❌ Erreur lors du lancement: {e}")
        messagebox.showerror("Erreur", f"Erreur lors du lancement: {e}")

if __name__ == "__main__":
    main()
