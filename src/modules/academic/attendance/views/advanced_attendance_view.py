# Vue avancée complète pour la gestion des présences
import customtkinter as ctk
from tkinter import messagebox, filedialog
from tkcalendar import Calendar
from datetime import datetime, timedelta
import os
from PIL import Image

# Imports des services
from ..services.attendance_service import AttendanceService
from ..services.attendance_notification_service import AttendanceNotificationService
from ..services.attendance_export_service import AttendanceExportService
from ..services.attendance_justification_service import AttendanceJustificationService
from ..services.attendance_alert_service import AttendanceAlertService, AlertLevel
from ..services.attendance_calendar_service import AttendanceCalendarService

# Imports du thème
import sys
import os
root_path = os.path.join(os.path.dirname(__file__), '..', '..', '..', '..', '..')
sys.path.insert(0, root_path)

try:
    from resources.themes.theme import *
    from resources.fonts.fonts import *  # pyright: ignore[reportMissingImports]
    from resources.icons.icons import load_ctk_icon  # pyright: ignore[reportMissingImports]
    print("✅ Thème global EduManager+ importé pour les présences avancées")
except ImportError:
    # Fallback avec des constantes locales
    BG_MAIN = "#0A192F"
    BG_SIDEBAR = "#172A45"
    BG_CARD = "#0B2039"
    BORDER_COLOR = "#334155"
    ACCENT_BLUE = "#64FFDA"
    TEXT_PRIMARY = "#CCD6F6"
    TEXT_SECONDARY = "#8892B0"
    ERROR_RED = "#FF6363"
    SUCCESS_GREEN = "#4ECDC4"
    WARNING_YELLOW = "#FFA500"
    INFO_ORANGE = "#FF8C00"
    HOVER_SUCCESS = "#3CB371"
    HOVER_ERROR = "#E74C3C"
    HOVER_PRIMARY = "#4ECDC4"
    
    F_TITLE = ("Segoe UI", 20, "bold")
    F_SUB = ("Segoe UI", 14, "bold")
    F_TXT = ("Segoe UI", 12)
    F_SMALL = ("Segoe UI", 10)
    F_BOLD = ("Segoe UI", 12, "bold")
    
    def load_ctk_icon(icon_name, size):
        """Fonction de fallback pour les icônes"""
        try:
            from PIL import Image
            icon_path = os.path.join(root_path, 'resources', 'icons', icon_name)
            if os.path.exists(icon_path):
                return ctk.CTkImage(Image.open(icon_path), size=size)
        except:
            pass
        return None

STATUTS = ["Présent", "Absent", "Retard", "Justifié"]

class AdvancedAttendanceView(ctk.CTkFrame):
    """Vue avancée complète pour la gestion des présences"""
    
    def __init__(self, parent, app_instance=None):
        super().__init__(parent, fg_color=BG_MAIN)
        self.app_instance = app_instance
        
        # Initialiser tous les services
        self.attendance_service = AttendanceService()
        self.notification_service = AttendanceNotificationService()
        self.export_service = AttendanceExportService()
        self.justification_service = AttendanceJustificationService()
        self.alert_service = AttendanceAlertService()
        self.calendar_service = AttendanceCalendarService()
        
        # Variables
        self._classes = self.attendance_service.get_classes_for_dropdown()
        self._classe_name_to_id = self.attendance_service.get_class_id_map()
        self.selected_classe_id = None
        self.current_student_id = None
        self.eleves = []
        
        # Variables de contrôle
        self.search_var = ctk.StringVar()
        self.filter_var = ctk.StringVar(value="Tous")
        self.date_var = ctk.StringVar(value=datetime.now().strftime("%Y-%m-%d"))
        
        self._build_main_layout()
        
        # Initialiser avec la première classe
        if self._classes:
            self.cb_class.set(self._classes[0])
            self._reload()
    
    def _build_main_layout(self):
        """Construit l'interface principale"""
        # Configuration du layout principal avec sidebar encore plus large
        self.grid_columnconfigure(0, weight=3, uniform="group1")  # Sidebar plus large
        self.grid_columnconfigure(1, weight=2, uniform="group1")  # Panneau de détails
        self.grid_rowconfigure(0, weight=1)
        
        # Panneau de gauche (contrôles et liste)
        self._build_left_panel()
        
        # Panneau de droite (détails et actions)
        self._build_right_panel()
    
    def _build_left_panel(self):
        """Construit le panneau de gauche avec trois sections distinctes comme dans l'image"""
        left_panel = ctk.CTkFrame(self, fg_color=BG_CARD, corner_radius=12)
        left_panel.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        
        # Configuration des sections avec poids égaux
        left_panel.grid_rowconfigure(0, weight=0)  # En-tête
        left_panel.grid_rowconfigure(1, weight=0)  # Section 1: Sélection
        left_panel.grid_rowconfigure(2, weight=0)  # Section 2: Recherche et Actions
        left_panel.grid_rowconfigure(3, weight=1)  # Section 3: Liste et Statistiques
        
        # En-tête avec icône
        header_frame = ctk.CTkFrame(left_panel, fg_color="transparent")
        header_frame.grid(row=0, column=0, sticky="ew", padx=20, pady=(20, 15))
        
        # Titre avec icône
        title_container = ctk.CTkFrame(header_frame, fg_color="transparent")
        title_container.pack(anchor="w")
        
        # Icône de présences
        presence_icon = load_ctk_icon("check_circle.png", (24, 24))
        if presence_icon:
            ctk.CTkLabel(title_container, text="", image=presence_icon, fg_color="transparent").pack(side="left", padx=(0, 10))
        
        title_label = ctk.CTkLabel(title_container, text="Gestion des Présences", 
                                  font=F_TITLE, text_color=TEXT_PRIMARY)
        title_label.pack(side="left")
        
        # SECTION 1: SÉLECTION DE CLASSE ET DATE
        self._build_selection_section(left_panel)
        
        # SECTION 2: RECHERCHE ET ACTIONS EN MASSE
        self._build_search_actions_section(left_panel)
        
        # SECTION 3: LISTE DES ÉLÈVES ET STATISTIQUES
        self._build_list_stats_section(left_panel)
    
    def _build_selection_section(self, parent):
        """Section 1: Sélection de classe et date"""
        section_frame = ctk.CTkFrame(parent, fg_color=BG_SIDEBAR, corner_radius=8, border_width=1, border_color=BORDER_COLOR)
        section_frame.grid(row=1, column=0, sticky="ew", padx=20, pady=(0, 15))
        
        # Titre de la section
        section_title = ctk.CTkFrame(section_frame, fg_color="transparent")
        section_title.pack(fill="x", padx=15, pady=(12, 8))
        
        class_icon = load_ctk_icon("class.png", (16, 16))
        if class_icon:
            ctk.CTkLabel(section_title, text="", image=class_icon, fg_color="transparent").pack(side="left", padx=(0, 8))
        
        ctk.CTkLabel(section_title, text="Sélection", font=F_SUB, text_color=TEXT_PRIMARY).pack(side="left")
        
        # Contrôles
        controls_frame = ctk.CTkFrame(section_frame, fg_color="transparent")
        controls_frame.pack(fill="x", padx=15, pady=(0, 12))
        controls_frame.grid_columnconfigure(0, weight=1)
        controls_frame.grid_columnconfigure(1, weight=1)
        
        # Classe avec icône
        class_frame = ctk.CTkFrame(controls_frame, fg_color="transparent")
        class_frame.grid(row=0, column=0, sticky="ew", padx=(0, 8))
        
        ctk.CTkLabel(class_frame, text="Classe", font=F_SMALL, text_color=TEXT_SECONDARY).pack(anchor="w", pady=(0, 4))
        self.cb_class = ctk.CTkComboBox(class_frame, values=self._classes, 
                                       command=lambda *_: self._reload(),
                                       fg_color=BG_CARD, border_color=BORDER_COLOR,
                                       button_color=BG_CARD, button_hover_color=BG_CARD)
        self.cb_class.pack(fill="x")
        
        # Date avec calendrier et icône
        date_frame = ctk.CTkFrame(controls_frame, fg_color="transparent")
        date_frame.grid(row=0, column=1, sticky="ew", padx=(8, 0))
        
        ctk.CTkLabel(date_frame, text="Date", font=F_SMALL, text_color=TEXT_SECONDARY).pack(anchor="w", pady=(0, 4))
        
        date_input_frame = ctk.CTkFrame(date_frame, fg_color=BG_CARD, border_color=BORDER_COLOR, border_width=1)
        date_input_frame.pack(fill="x")
        date_input_frame.grid_columnconfigure(0, weight=1)
        
        self.ent_date = ctk.CTkEntry(date_input_frame, textvariable=self.date_var, 
                                    placeholder_text="AAAA-MM-JJ", border_width=0, 
                                    fg_color="transparent", font=F_TXT)
        self.ent_date.grid(row=0, column=0, sticky="ew", padx=(8, 0))
        
        calendar_btn = ctk.CTkButton(date_input_frame, text="", 
                                    image=load_ctk_icon("calendar.png", (18,18)), 
                                    width=32, fg_color="transparent",
                                    hover_color=BG_SIDEBAR, command=self._pick_date)
        calendar_btn.grid(row=0, column=1, padx=4, pady=4)
    
    def _build_search_actions_section(self, parent):
        """Section 2: Recherche et actions en masse"""
        section_frame = ctk.CTkFrame(parent, fg_color=BG_SIDEBAR, corner_radius=8, border_width=1, border_color=BORDER_COLOR)
        section_frame.grid(row=2, column=0, sticky="ew", padx=20, pady=(0, 15))
        
        # Titre de la section recherche
        search_title = ctk.CTkFrame(section_frame, fg_color="transparent")
        search_title.pack(fill="x", padx=15, pady=(12, 8))
        
        search_icon = load_ctk_icon("search.png", (16, 16))
        if search_icon:
            ctk.CTkLabel(search_title, text="", image=search_icon, fg_color="transparent").pack(side="left", padx=(0, 8))
        
        ctk.CTkLabel(search_title, text="Recherche et Actions", font=F_SUB, text_color=TEXT_PRIMARY).pack(side="left")
        
        # Contrôles de recherche
        search_controls = ctk.CTkFrame(section_frame, fg_color="transparent")
        search_controls.pack(fill="x", padx=15, pady=(0, 8))
        search_controls.grid_columnconfigure(0, weight=1)
        search_controls.grid_columnconfigure(1, weight=1)
        
        # Recherche
        search_frame = ctk.CTkFrame(search_controls, fg_color="transparent")
        search_frame.grid(row=0, column=0, sticky="ew", padx=(0, 8))
        
        ctk.CTkLabel(search_frame, text="Rechercher", font=F_SMALL, text_color=TEXT_SECONDARY).pack(anchor="w", pady=(0, 4))
        
        search_entry = ctk.CTkEntry(search_frame, textvariable=self.search_var, 
                                   placeholder_text="Nom ou prénom...",
                                   fg_color=BG_CARD, border_color=BORDER_COLOR)
        search_entry.pack(fill="x")
        search_entry.bind("<KeyRelease>", lambda *_: self._reload())
        
        # Filtre par statut
        filter_frame = ctk.CTkFrame(search_controls, fg_color="transparent")
        filter_frame.grid(row=0, column=1, sticky="ew", padx=(8, 0))
        
        ctk.CTkLabel(filter_frame, text="Statut", font=F_SMALL, text_color=TEXT_SECONDARY).pack(anchor="w", pady=(0, 4))
        
        self.filter_cb = ctk.CTkComboBox(filter_frame, values=["Tous"]+STATUTS, 
                                        variable=self.filter_var,
                                        fg_color=BG_CARD, border_color=BORDER_COLOR,
                                        button_color=BG_CARD, button_hover_color=BG_CARD,
                                        command=lambda *_: self._reload())
        self.filter_cb.pack(fill="x")
        
        # Actions en masse
        self._build_bulk_actions(section_frame)
    
    def _build_list_stats_section(self, parent):
        """Section 3: Liste des élèves"""
        section_frame = ctk.CTkFrame(parent, fg_color=BG_SIDEBAR, corner_radius=8, border_width=1, border_color=BORDER_COLOR)
        section_frame.grid(row=3, column=0, sticky="nsew", padx=20, pady=(0, 20))
        
        # Titre de la section
        section_title = ctk.CTkFrame(section_frame, fg_color="transparent")
        section_title.pack(fill="x", padx=15, pady=(12, 8))
        
        list_icon = load_ctk_icon("group.png", (16, 16))
        if list_icon:
            ctk.CTkLabel(section_title, text="", image=list_icon, fg_color="transparent").pack(side="left", padx=(0, 8))
        
        ctk.CTkLabel(section_title, text="Élèves", font=F_SUB, text_color=TEXT_PRIMARY).pack(side="left")
        
        # Contenu de la section
        content_frame = ctk.CTkFrame(section_frame, fg_color="transparent")
        content_frame.pack(fill="both", expand=True, padx=15, pady=(0, 12))
        
        # Liste des élèves
        self.list_wrap = ctk.CTkScrollableFrame(content_frame, fg_color="transparent", corner_radius=0)
        self.list_wrap.pack(fill="both", expand=True)
    
    def _build_bulk_actions(self, parent):
        """Construit la section des actions en masse avec icônes"""
        bulk_section = ctk.CTkFrame(parent, fg_color=BG_SIDEBAR, corner_radius=8, border_width=1, border_color=BORDER_COLOR)
        bulk_section.pack(fill="x", padx=20, pady=(0, 15))
        
        # Titre de la section
        bulk_title = ctk.CTkFrame(bulk_section, fg_color="transparent")
        bulk_title.pack(fill="x", padx=15, pady=(12, 8))
        
        actions_icon = load_ctk_icon("settings.png", (16, 16))
        if actions_icon:
            ctk.CTkLabel(bulk_title, text="", image=actions_icon, fg_color="transparent").pack(side="left", padx=(0, 8))
        
        ctk.CTkLabel(bulk_title, text="Actions en Masse", font=F_SUB, text_color=TEXT_PRIMARY).pack(side="left")
        
        # Boutons d'action
        buttons_frame = ctk.CTkFrame(bulk_section, fg_color="transparent")
        buttons_frame.pack(fill="x", padx=15, pady=(0, 12))
        buttons_frame.grid_columnconfigure((0, 1, 2), weight=1)
        
        # Valider tout Présent
        validate_btn = ctk.CTkButton(buttons_frame, text="Valider tout Présent", 
                                    image=load_ctk_icon("check.png", (18, 18)),
                                    fg_color="transparent", text_color=SUCCESS_GREEN, 
                                    hover_color=BG_CARD, font=F_BOLD,
                                    border_width=1, border_color=SUCCESS_GREEN,
                                    command=self._validate_all_present)
        validate_btn.grid(row=0, column=0, sticky="ew", padx=(0, 5))
        
        # Marquer tout Absent
        absent_btn = ctk.CTkButton(buttons_frame, text="Marquer tout Absent", 
                                  image=load_ctk_icon("close.png", (18, 18)),
                                  fg_color="transparent", text_color=ERROR_RED, 
                                  hover_color=BG_CARD, font=F_BOLD,
                                  border_width=1, border_color=ERROR_RED,
                                  command=self._mark_all_absent)
        absent_btn.grid(row=0, column=1, sticky="ew", padx=5)
        
        # Réinitialiser
        reset_btn = ctk.CTkButton(buttons_frame, text="Réinitialiser", 
                                  image=load_ctk_icon("refresh.png", (18, 18)),
                                  fg_color="transparent", text_color=WARNING_YELLOW, 
                                  hover_color=BG_CARD, font=F_BOLD,
                                  border_width=1, border_color=WARNING_YELLOW,
                                  command=self._reset_all)
        reset_btn.grid(row=0, column=2, sticky="ew", padx=(5, 0))
    
    def _build_statistics_section(self, parent):
        """Construit la section des statistiques comme en-tête proéminent"""
        # Section des statistiques avec fond et bordure (équilibrée)
        stats_section = ctk.CTkFrame(parent, fg_color=BG_SIDEBAR, corner_radius=6, border_width=1, border_color=BORDER_COLOR)
        stats_section.pack(fill="x", padx=20, pady=(15, 12))
        
        # En-tête des statistiques (équilibré)
        stats_header = ctk.CTkFrame(stats_section, fg_color="transparent")
        stats_header.pack(fill="x", padx=12, pady=(10, 6))
        
        stats_icon = load_ctk_icon("stats.png", (14, 14))
        if stats_icon:
            ctk.CTkLabel(stats_header, text="", image=stats_icon, fg_color="transparent").pack(side="left", padx=(0, 6))
        
        ctk.CTkLabel(stats_header, text="Statistiques", font=F_SUB, text_color=TEXT_PRIMARY).pack(side="left")
        
        # Chips des statistiques (équilibré)
        self.stats_chips_frame = ctk.CTkFrame(stats_section, fg_color="transparent")
        self.stats_chips_frame.pack(fill="x", padx=12, pady=(0, 10))
        self.stats_chips_frame.grid_columnconfigure((0, 1, 2, 3), weight=1)
        
        # Initialiser avec des valeurs par défaut
        self._update_statistics_display()
    
    def _update_statistics_display(self, eleve_id=None):
        """Met à jour l'affichage des statistiques"""
        # Supprimer les anciens chips
        for widget in self.stats_chips_frame.winfo_children():
            widget.destroy()
        
        if eleve_id:
            # Statistiques de l'élève sélectionné
            student_stats = self.attendance_service.get_student_stats(eleve_id)
            stats_data = [
                ("Total", getattr(student_stats, 'total_jours', 0), TEXT_PRIMARY, "stats.png"),
                ("Présents", getattr(student_stats, 'presents', 0), SUCCESS_GREEN, "check_circle.png"),
                ("Absents", getattr(student_stats, 'absents', 0), ERROR_RED, "close.png"),
                ("Retards", getattr(student_stats, 'retards', 0), WARNING_YELLOW, "clock_icon.png")
            ]
        else:
            # Statistiques globales de la classe
            counts = self.attendance_service.get_class_attendance_summary_stats(
                self.selected_classe_id, self.date_var.get().strip()
            )
            total_eleves = len(self.eleves) if self.eleves else 0
            stats_data = [
                ("Total", total_eleves, TEXT_PRIMARY, "stats.png"),
                ("Présents", counts.get("Présent", 0), SUCCESS_GREEN, "check_circle.png"),
                ("Absents", counts.get("Absent", 0), ERROR_RED, "close.png"),
                ("Retards", counts.get("Retard", 0), WARNING_YELLOW, "clock_icon.png")
            ]
        
        for i, (label, value, color, icon_name) in enumerate(stats_data):
            # Créer la carte avec le style du tableau de bord principal
            chip = ctk.CTkFrame(self.stats_chips_frame, fg_color=BG_CARD, corner_radius=12, 
                              border_width=1, border_color=BORDER_COLOR, height=100)
            chip.grid(row=0, column=i, sticky="ew", padx=2)
            chip.grid_propagate(False)
            
            # Header de la carte
            header_frame = ctk.CTkFrame(chip, fg_color="transparent")
            header_frame.pack(fill="x", padx=12, pady=(12, 8))
            
            # Icône avec contour seulement (sans fond coloré)
            icon_badge = ctk.CTkFrame(header_frame, fg_color="transparent", corner_radius=18, width=36, height=36, border_width=2, border_color=color)
            icon_badge.pack_propagate(False)
            icon_badge.pack(side="left")
            
            # Icône dans le badge
            chip_icon = load_ctk_icon(icon_name, (18, 18))
            if chip_icon:
                icon_label = ctk.CTkLabel(icon_badge, text="", image=chip_icon, fg_color="transparent")
                icon_label.pack(expand=True)
            else:
                # Icône de fallback
                fallback_icons = ["help.png", "info.png", "warning.png", "error.png"]
                fallback_icon = None
                for fallback_name in fallback_icons:
                    fallback_icon = load_ctk_icon(fallback_name, (18, 18))
                    if fallback_icon:
                        break
                
                if fallback_icon:
                    icon_label = ctk.CTkLabel(icon_badge, text="", image=fallback_icon, fg_color="transparent")
                    icon_label.pack(expand=True)
            
            # Contenu de la carte
            content_frame = ctk.CTkFrame(chip, fg_color="transparent")
            content_frame.pack(fill="both", expand=True, padx=12, pady=(0, 12))
            
            # Valeur principale
            value_label = ctk.CTkLabel(content_frame, text=str(value), 
                                     font=F_TITLE, text_color=TEXT_PRIMARY)
            value_label.pack(anchor="w")
            
            # Label descriptif
            label_label = ctk.CTkLabel(content_frame, text=label, 
                                      font=F_SMALL, text_color=TEXT_SECONDARY)
            label_label.pack(anchor="w", pady=(2, 0))
            
            # Effet hover
            def create_hover_effect(widget, original_color):
                def on_enter(event):
                    widget.configure(border_color=TEXT_ACCENT)
                def on_leave(event):
                    widget.configure(border_color=BORDER_COLOR)
                widget.bind("<Enter>", on_enter)
                widget.bind("<Leave>", on_leave)
            
            create_hover_effect(chip, color)
    
    def _build_right_panel(self):
        """Construit le panneau de droite"""
        self.detail_panel = ctk.CTkFrame(self, fg_color=BG_CARD, corner_radius=12)
        self.detail_panel.grid(row=0, column=1, sticky="nsew")
        self._build_detail_panel()
    
    def _build_detail_panel(self):
        """Construit le panneau de détails avec organisation améliorée"""
        # Construire une seule fois
        for widget in self.detail_panel.winfo_children():
            widget.destroy()
        
        self.detail_panel.grid_columnconfigure(0, weight=1)
        
        # Statistiques comme en-tête permanent
        self._build_statistics_section(self.detail_panel)
        
        # Zone de contenu pour les détails de l'élève
        self.content_area = ctk.CTkFrame(self.detail_panel, fg_color="transparent")
        self.content_area.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        # Message par défaut avec icône
        default_frame = ctk.CTkFrame(self.content_area, fg_color="transparent")
        default_frame.pack(expand=True, fill="both")
        
        # Icône de sélection
        select_icon = load_ctk_icon("person.png", (48, 48))
        if select_icon:
            ctk.CTkLabel(default_frame, text="", image=select_icon, fg_color="transparent").pack(pady=(40, 20))
        
        # Message
        ctk.CTkLabel(default_frame, text="Sélectionnez un élève", 
                    font=F_TITLE, text_color=TEXT_PRIMARY).pack(pady=(0, 10))
        
        ctk.CTkLabel(default_frame, text="pour voir les détails et modifier sa présence",
                    font=F_TXT, text_color=TEXT_SECONDARY).pack()
        
        # Initialiser avec les statistiques globales
        self._update_statistics_display()
    
    def _render_detail_for(self, eleve_id):
        """Affiche les détails d'un élève"""
        # S'assurer que content_area existe
        if not hasattr(self, 'content_area'):
            self._build_detail_panel()
        
        # Nettoyer seulement la zone de contenu
        for widget in self.content_area.winfo_children():
            widget.destroy()
        
        # Trouver l'élève
        eleve = next((e for e in self.eleves if e["id_eleve"] == eleve_id), None)
        if not eleve:
            self._build_detail_panel()
            return
        
        self.current_student_id = eleve_id
        
        # Récupérer les données de présence
        presences = self.attendance_service.attendance_controller.get_attendance_for_date_and_class(
            self.selected_classe_id, self.date_var.get().strip()
        )
        presence_data = presences.get(eleve_id, {})
        statut = presence_data.get("statut", "Présent")
        commentaire = presence_data.get("commentaire", "")
        
        # Mettre à jour les statistiques pour l'élève sélectionné
        self._update_statistics_display(eleve_id)
        
        # En-tête avec nom et boutons d'action
        header_section = ctk.CTkFrame(self.content_area, fg_color=BG_SIDEBAR, corner_radius=8, border_width=1, border_color=BORDER_COLOR)
        header_section.pack(fill="x", pady=(0, 8))
        
        header_frame = ctk.CTkFrame(header_section, fg_color="transparent")
        header_frame.pack(fill="x", padx=15, pady=12)
        
        # Nom de l'élève avec icône
        name_container = ctk.CTkFrame(header_frame, fg_color="transparent")
        name_container.pack(side="left", fill="x", expand=True)
        
        # Icône de l'élève
        student_icon = load_ctk_icon("person.png", (24, 24))
        if student_icon:
            ctk.CTkLabel(name_container, text="", image=student_icon, fg_color="transparent").pack(side="left", padx=(0, 10))
        
        ctk.CTkLabel(name_container, text=f"{eleve['prenom']} {eleve['nom']}", 
                    font=F_TITLE, text_color=TEXT_PRIMARY).pack(side="left")
        
        # Bouton Historique (icône seulement)
        history_btn = ctk.CTkButton(header_frame, text="", 
                                   image=load_ctk_icon("file.png", (18, 18)),
                                   fg_color="transparent", text_color=ACCENT_BLUE, 
                                   hover_color=BG_CARD, font=F_BOLD,
                                   border_width=1, border_color=ACCENT_BLUE,
                                   width=36, height=36,
                                   command=lambda: self._show_history(eleve_id))
        history_btn.pack(side="right", padx=(10, 0))
        
        
        # Bouton Appliquer (icône seulement)
        apply_btn = ctk.CTkButton(header_frame, text="", 
                                 image=load_ctk_icon("check.png", (18, 18)),
                                 fg_color="transparent", text_color=SUCCESS_GREEN, 
                                 hover_color=BG_CARD, font=F_BOLD,
                                 border_width=1, border_color=SUCCESS_GREEN,
                                 width=36, height=36,
                                 command=lambda: self._apply_student_changes(eleve_id, statut_var.get(), 
                                                                           commentaire_txt.get("1.0", "end-1c").strip()))
        apply_btn.pack(side="right", padx=(5, 0))
        
        # Bouton Annuler (icône seulement)
        cancel_btn = ctk.CTkButton(header_frame, text="", 
                                  image=load_ctk_icon("close.png", (18, 18)),
                                  fg_color="transparent", text_color=ERROR_RED, 
                                  hover_color=BG_CARD, font=F_BOLD,
                                  border_width=1, border_color=ERROR_RED,
                                  width=36, height=36,
                                  command=lambda: self._render_detail_for(eleve_id))
        cancel_btn.pack(side="right", padx=(5, 0))
        
        # Contenu principal avec sections organisées
        content_frame = ctk.CTkFrame(self.content_area, fg_color="transparent")
        content_frame.pack(fill="both", expand=True, pady=(0, 5))
        
        # Section statut (hauteur encore augmentée)
        status_section = ctk.CTkFrame(content_frame, fg_color=BG_SIDEBAR, corner_radius=8, border_width=1, border_color=BORDER_COLOR, height=140)
        status_section.pack(fill="x", pady=(0, 8))
        status_section.pack_propagate(False)
        
        status_header = ctk.CTkFrame(status_section, fg_color="transparent")
        status_header.pack(fill="x", padx=15, pady=(12, 8))
        
        status_icon = load_ctk_icon("check_circle.png", (16, 16))
        if status_icon:
            ctk.CTkLabel(status_header, text="", image=status_icon, fg_color="transparent").pack(side="left", padx=(0, 8))
        
        ctk.CTkLabel(status_header, text="Statut du jour", font=F_SUB, text_color=TEXT_PRIMARY).pack(side="left")
        
        status_content = ctk.CTkFrame(status_section, fg_color="transparent")
        status_content.pack(fill="x", padx=15, pady=(0, 12))
        
        statut_var = ctk.StringVar(value=statut)
        statut_seg = ctk.CTkSegmentedButton(status_content, values=STATUTS, 
                                           variable=statut_var,
                                           selected_color=ACCENT_BLUE, 
                                           selected_hover_color=ACCENT_BLUE,
                                           unselected_color=BG_CARD, 
                                           unselected_hover_color=BG_CARD,
                                           font=F_TXT, text_color=TEXT_PRIMARY)
        statut_seg.pack(fill="x")
        
        # Section commentaire (hauteur encore augmentée)
        comment_section = ctk.CTkFrame(content_frame, fg_color=BG_SIDEBAR, corner_radius=8, border_width=1, border_color=BORDER_COLOR, height=180)
        comment_section.pack(fill="x", pady=(0, 8))
        comment_section.pack_propagate(False)
        
        comment_header = ctk.CTkFrame(comment_section, fg_color="transparent")
        comment_header.pack(fill="x", padx=15, pady=(12, 8))
        
        comment_icon = load_ctk_icon("edit.png", (16, 16))
        if comment_icon:
            ctk.CTkLabel(comment_header, text="", image=comment_icon, fg_color="transparent").pack(side="left", padx=(0, 8))
        
        ctk.CTkLabel(comment_header, text="Commentaire", font=F_SUB, text_color=TEXT_PRIMARY).pack(side="left")
        
        comment_content = ctk.CTkFrame(comment_section, fg_color="transparent")
        comment_content.pack(fill="x", padx=15, pady=(0, 12))
        
        commentaire_txt = ctk.CTkTextbox(comment_content, height=140, 
                                       fg_color=BG_CARD, border_color=BORDER_COLOR, 
                                       font=F_TXT, text_color=TEXT_PRIMARY)
        commentaire_txt.pack(fill="x")
        if commentaire:
            commentaire_txt.insert("1.0", commentaire)
        
        # Justificatif
        self._build_justification_section(content_frame, eleve_id)
        
        # Boutons d'action maintenant dans l'en-tête
    
    def _build_justification_section(self, parent, eleve_id):
        """Construit la section des justificatifs avec organisation améliorée"""
        justification_section = ctk.CTkFrame(parent, fg_color=BG_SIDEBAR, corner_radius=8, border_width=1, border_color=BORDER_COLOR, height=140)
        justification_section.pack(fill="x", pady=(0, 8))
        justification_section.pack_propagate(False)
        
        # En-tête de la section
        justification_header = ctk.CTkFrame(justification_section, fg_color="transparent")
        justification_header.pack(fill="x", padx=15, pady=(12, 8))
        
        justification_icon = load_ctk_icon("file.png", (16, 16))
        if justification_icon:
            ctk.CTkLabel(justification_header, text="", image=justification_icon, fg_color="transparent").pack(side="left", padx=(0, 8))
        
        ctk.CTkLabel(justification_header, text="Justificatif", font=F_SUB, text_color=TEXT_PRIMARY).pack(side="left")
        
        # Contenu de la section
        justification_content = ctk.CTkFrame(justification_section, fg_color="transparent")
        justification_content.pack(fill="x", padx=15, pady=(0, 12))
        
        # Champ de chemin avec bouton
        path_frame = ctk.CTkFrame(justification_content, fg_color=BG_CARD, border_color=BORDER_COLOR, border_width=1)
        path_frame.pack(fill="x")
        path_frame.grid_columnconfigure(0, weight=1)
        
        self.justification_path_var = ctk.StringVar()
        path_entry = ctk.CTkEntry(path_frame, textvariable=self.justification_path_var, 
                                 placeholder_text="Chemin vers le fichier (PDF/JPG/PNG)…",
                                 border_width=0, fg_color="transparent", font=F_TXT)
        path_entry.grid(row=0, column=0, sticky="ew", padx=(8, 0))
        
        # Bouton de sélection de fichier sans fond
        file_btn = ctk.CTkButton(path_frame, text="", 
                                image=load_ctk_icon("upload.png", (18, 18)), 
                                width=36, fg_color="transparent", 
                                hover_color=BG_SIDEBAR,
                                command=lambda: self._pick_justification_file())
        file_btn.grid(row=0, column=1, padx=4, pady=4)
    
    def _build_detail_buttons(self, parent, eleve_id, statut_var, commentaire_txt):
        """Construit les boutons d'action du détail avec icônes sans fond"""
        buttons_section = ctk.CTkFrame(parent, fg_color=BG_CARD, corner_radius=10, border_width=2, border_color=ACCENT_BLUE, height=120)
        buttons_section.pack(fill="x", pady=(0, 20))
        buttons_section.pack_propagate(False)
        
        buttons_frame = ctk.CTkFrame(buttons_section, fg_color="transparent")
        buttons_frame.pack(fill="both", expand=True, padx=20, pady=25)
        buttons_frame.grid_columnconfigure((0, 1), weight=1)
        
        def apply_changes():
            self._apply_student_changes(eleve_id, statut_var.get(), 
                                      commentaire_txt.get("1.0", "end-1c").strip())
        
        # Bouton Appliquer avec fond visible
        apply_btn = ctk.CTkButton(buttons_frame, text="Appliquer", 
                                 image=load_ctk_icon("check.png", (20, 20)), 
                                 font=F_TITLE, fg_color=SUCCESS_GREEN, 
                                 text_color="white", hover_color="#00B894", 
                                 border_width=0,
                                 height=50,
                                 command=apply_changes)
        apply_btn.grid(row=0, column=0, sticky="ew", padx=(0, 10))
        
        # Bouton Annuler avec fond visible
        cancel_btn = ctk.CTkButton(buttons_frame, text="Annuler", 
                                 image=load_ctk_icon("close.png", (20, 20)), 
                                 font=F_TITLE, fg_color=ERROR_RED, 
                                 text_color="white", hover_color="#E17055", 
                                 border_width=0,
                                 height=50,
                                 command=lambda: self._render_detail_for(eleve_id))
        cancel_btn.grid(row=0, column=1, sticky="ew", padx=(8, 0))
    
    def _reload(self):
        """Recharge les données"""
        classe_name = self.cb_class.get()
        if not classe_name:
            return
        
        self.selected_classe_id = self._classe_name_to_id.get(classe_name)
        date_str = self.date_var.get().strip()
        
        if not date_str:
            messagebox.showwarning("Attention", "Indiquez la date.")
            return
        
        # Récupérer les élèves avec leur statut
        self.eleves = self.attendance_service.get_students_with_attendance_status(
            self.selected_classe_id, date_str, 
            self.search_var.get().strip(), self.filter_var.get()
        )
        
        # Nettoyer la liste
        for widget in self.list_wrap.winfo_children():
            widget.destroy()
        
        # Afficher les élèves
        for eleve in self.eleves:
            self._create_student_item(eleve)
        
        # Mettre à jour les statistiques
        self._update_statistics()
    
    def _create_student_item(self, eleve):
        """Crée un élément de liste pour un élève"""
        eleve_id = eleve["id_eleve"]
        statut = eleve["statut"]
        
        # Couleur de fond selon sélection
        item_bg = HOVER_PRIMARY if eleve_id == self.current_student_id else BG_CARD
        
        # Créer l'élément
        item = ctk.CTkFrame(self.list_wrap, fg_color=item_bg, corner_radius=8, cursor="hand2")
        item.pack(fill="x", padx=5, pady=4)
        item.bind("<Button-1>", lambda event, sid=eleve_id: self._render_detail_for(sid))
        
        # Contenu de l'élément
        content_frame = ctk.CTkFrame(item, fg_color="transparent")
        content_frame.pack(fill="x", padx=12, pady=10)
        
        # Icône de l'élève
        student_icon = load_ctk_icon("person.png", (20, 20))
        if student_icon:
            icon_label = ctk.CTkLabel(content_frame, text="", image=student_icon, fg_color="transparent")
            icon_label.pack(side="left", padx=(0, 10))
        
        # Informations de l'élève
        info_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        info_frame.pack(side="left", fill="x", expand=True)
        
        # Nom de l'élève
        name_label = ctk.CTkLabel(info_frame, text=f"{eleve['prenom']} {eleve['nom']}", 
                                 font=F_TXT, text_color=TEXT_PRIMARY)
        name_label.pack(anchor="w")
        
        # Statut avec icône
        status_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        status_frame.pack(side="right")
        
        # Icône selon le statut
        status_icon_name = {
            "Présent": "check_circle.png",
            "Absent": "close_circle.png", 
            "Retard": "time.png",
            "Justifié": "file.png"
        }.get(statut, "help.png")
        
        status_icon = load_ctk_icon(status_icon_name, (16, 16))
        if status_icon:
            status_icon_label = ctk.CTkLabel(status_frame, text="", image=status_icon, fg_color="transparent")
            status_icon_label.pack(side="left", padx=(0, 5))
        
        # Texte du statut avec couleur
        color_map = {
            "Présent": SUCCESS_GREEN,
            "Absent": ERROR_RED,
            "Retard": WARNING_YELLOW,
            "Justifié": ACCENT_BLUE
        }
        color = color_map.get(statut, TEXT_SECONDARY)
        
        statut_label = ctk.CTkLabel(status_frame, text=statut, 
                                   font=F_SMALL, text_color=color)
        statut_label.pack(side="left")
        
        # Absences injustifiées
        absences_count = eleve["unjustified_absences"]
        seuil = self.attendance_service.get_absence_threshold()
        if absences_count >= seuil:
            absences_label = ctk.CTkLabel(item, text=f"({absences_count} abs. injustifiées)", 
                                         text_color=ERROR_RED, font=F_SMALL)
            absences_label.pack(side="right", padx=5)
    
    def _update_statistics(self):
        """Met à jour les statistiques"""
        if not self.eleves:
            return
        
        # Utiliser la nouvelle méthode pour mettre à jour les statistiques
        self._update_statistics_display()
    
    # Méthodes d'action
    def _validate_all_present(self):
        """Valide toutes les présences comme présentes"""
        if not self.selected_classe_id:
            return
        
        success = self.attendance_service.validate_all_students_present(
            self.selected_classe_id, self.date_var.get().strip()
        )
        
        if success:
            messagebox.showinfo("Succès", "Tous les élèves ont été marqués comme présents")
            self._reload()
        else:
            messagebox.showerror("Erreur", "Erreur lors de la validation en masse")
    
    def _mark_all_absent(self):
        """Marque tous les élèves comme absents"""
        if not self.selected_classe_id:
            return
        
        success = self.attendance_service.mark_all_students_absent(
            self.selected_classe_id, self.date_var.get().strip()
        )
        
        if success:
            messagebox.showinfo("Succès", "Tous les élèves ont été marqués comme absents")
            self._reload()
        else:
            messagebox.showerror("Erreur", "Erreur lors du marquage en masse")
    
    def _reset_all(self):
        """Réinitialise toutes les présences"""
        if not self.selected_classe_id:
            return
        
        success = self.attendance_service.reset_all_students_attendance(
            self.selected_classe_id, self.date_var.get().strip()
        )
        
        if success:
            messagebox.showinfo("Succès", "Toutes les présences ont été réinitialisées")
            self._reload()
        else:
            messagebox.showerror("Erreur", "Erreur lors de la réinitialisation")
    
    def _apply_student_changes(self, eleve_id, statut, commentaire):
        """Applique les changements pour un élève"""
        try:
            self.attendance_service.update_student_attendance(
                eleve_id, self.selected_classe_id, 
                self.date_var.get().strip(), statut, commentaire
            )
            
            messagebox.showinfo("Succès", "Modifications enregistrées")
            self._reload()
            
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de l'enregistrement: {e}")
    
    def _pick_date(self):
        """Ouvre le sélecteur de date"""
        date_picker = ctk.CTkToplevel(self)
        date_picker.title("Sélectionner une date")
        date_picker.geometry("300x300")
        date_picker.configure(fg_color=BG_MAIN)
        date_picker.grab_set()
        
        cal = Calendar(date_picker, selectmode='day')
        cal.pack(pady=20)
        
        def select_date():
            selected_date = cal.get_date()
            self.date_var.set(selected_date)
            date_picker.destroy()
            self._reload()
        
        ctk.CTkButton(date_picker, text="Sélectionner", command=select_date).pack(pady=10)
    
    def _pick_justification_file(self):
        """Ouvre le sélecteur de fichier pour justificatif"""
        file_path = filedialog.askopenfilename(
            title="Sélectionner un justificatif",
            filetypes=[
                ("Documents PDF", "*.pdf"),
                ("Images", "*.jpg *.jpeg *.png"),
                ("Documents Word", "*.doc *.docx"),
                ("Tous les fichiers", "*.*")
            ]
        )
        
        if file_path:
            self.justification_path_var.set(file_path)
    
    def _show_history(self, eleve_id):
        """Affiche l'historique d'un élève"""
        history = self.attendance_service.get_student_full_history(eleve_id)
        
        if not history:
            messagebox.showinfo("Historique", "Aucun historique trouvé pour cet élève")
            return
        
        # Récupérer le nom de l'élève depuis les données actuelles
        eleve = next((e for e in self.eleves if e["id_eleve"] == eleve_id), None)
        if eleve:
            student_name = f"{eleve['prenom']} {eleve['nom']}"
        else:
            student_name = "Élève"
        
        # Créer une fenêtre d'historique avec design amélioré
        history_window = ctk.CTkToplevel(self)
        history_window.title("Historique des présences")
        history_window.geometry("900x700")
        history_window.configure(fg_color=BG_MAIN)
        history_window.grab_set()
        
        # En-tête avec design amélioré
        header_frame = ctk.CTkFrame(history_window, fg_color=BG_CARD, corner_radius=15, border_width=1, border_color=BORDER_COLOR)
        header_frame.pack(fill="x", padx=20, pady=20)
        
        # En-tête interne avec icône et titre
        header_content = ctk.CTkFrame(header_frame, fg_color="transparent")
        header_content.pack(fill="x", padx=20, pady=20)
        
        # Icône et titre
        title_container = ctk.CTkFrame(header_content, fg_color="transparent")
        title_container.pack(fill="x")
        
        # Icône historique
        history_icon = load_ctk_icon("file.png", (24, 24))
        if history_icon:
            ctk.CTkLabel(title_container, text="", image=history_icon, fg_color="transparent").pack(side="left", padx=(0, 10))
        
        ctk.CTkLabel(title_container, text=f"Historique des présences - {student_name}", 
                    font=F_TITLE, text_color=TEXT_PRIMARY).pack(side="left")
        
        # Statistiques avec design amélioré
        stats = self.attendance_service.get_student_stats(eleve_id)
        stats_frame = ctk.CTkFrame(header_frame, fg_color=BG_SIDEBAR, corner_radius=10, border_width=1, border_color=BORDER_COLOR)
        stats_frame.pack(fill="x", padx=20, pady=(0, 20))
        
        # En-tête des statistiques
        stats_header = ctk.CTkFrame(stats_frame, fg_color="transparent")
        stats_header.pack(fill="x", padx=15, pady=(12, 8))
        
        # Icône statistiques
        stats_icon = load_ctk_icon("stats.png", (16, 16))
        if stats_icon:
            ctk.CTkLabel(stats_header, text="", image=stats_icon, fg_color="transparent").pack(side="left", padx=(0, 8))
        
        ctk.CTkLabel(stats_header, text="Statistiques", font=F_SUB, text_color=TEXT_PRIMARY).pack(side="left")
        
        # Contenu des statistiques
        stats_content = ctk.CTkFrame(stats_frame, fg_color="transparent")
        stats_content.pack(fill="x", padx=15, pady=(0, 12))
        stats_content.grid_columnconfigure((0, 1, 2, 3), weight=1)
        
        # Données des statistiques avec icônes
        stats_data = [
            ("Total", stats.total_jours, TEXT_PRIMARY, "stats.png"),
            ("Présents", stats.presents, SUCCESS_GREEN, "check_circle.png"),
            ("Absents", stats.absents, ERROR_RED, "close.png"),
            ("Retards", stats.retards, WARNING_YELLOW, "clock_icon.png")
        ]
        
        for i, (label, value, color, icon_name) in enumerate(stats_data):
            stat_card = ctk.CTkFrame(stats_content, fg_color=BG_CARD, corner_radius=8, border_width=1, border_color=color, height=60)
            stat_card.grid(row=0, column=i, sticky="ew", padx=2)
            stat_card.grid_propagate(False)
            
            # Contenu de la carte
            card_content = ctk.CTkFrame(stat_card, fg_color="transparent")
            card_content.pack(fill="both", expand=True, padx=8, pady=8)
            
            # Icône
            icon_img = load_ctk_icon(icon_name, (14, 14))
            if icon_img:
                ctk.CTkLabel(card_content, text="", image=icon_img, fg_color="transparent").pack()
            
            # Valeur
            ctk.CTkLabel(card_content, text=str(value), font=F_BOLD, text_color=color).pack()
            
            # Label
            ctk.CTkLabel(card_content, text=label, font=F_SMALL, text_color=TEXT_SECONDARY).pack()
        
        # Liste des présences avec design amélioré
        list_frame = ctk.CTkScrollableFrame(history_window, fg_color=BG_CARD, corner_radius=15, border_width=1, border_color=BORDER_COLOR)
        list_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        # En-tête du tableau avec icônes
        header_row = ctk.CTkFrame(list_frame, fg_color=BG_SIDEBAR, corner_radius=10, border_width=1, border_color=BORDER_COLOR)
        header_row.pack(fill="x", padx=5, pady=(5, 10))
        
        header_inner = ctk.CTkFrame(header_row, fg_color="transparent")
        header_inner.pack(fill="x", padx=15, pady=12)
        
        # Colonnes avec icônes
        date_icon = load_ctk_icon("calendar.png", (14, 14))
        if date_icon:
            ctk.CTkLabel(header_inner, text="", image=date_icon, fg_color="transparent").pack(side="left", padx=(0, 5))
        ctk.CTkLabel(header_inner, text="Date", font=F_BOLD, text_color=TEXT_PRIMARY, width=120).pack(side="left")
        
        status_icon = load_ctk_icon("check_circle.png", (14, 14))
        if status_icon:
            ctk.CTkLabel(header_inner, text="", image=status_icon, fg_color="transparent").pack(side="left", padx=(10, 5))
        ctk.CTkLabel(header_inner, text="Statut", font=F_BOLD, text_color=TEXT_PRIMARY, width=100).pack(side="left")
        
        class_icon = load_ctk_icon("group.png", (14, 14))
        if class_icon:
            ctk.CTkLabel(header_inner, text="", image=class_icon, fg_color="transparent").pack(side="left", padx=(10, 5))
        ctk.CTkLabel(header_inner, text="Classe", font=F_BOLD, text_color=TEXT_PRIMARY, width=120).pack(side="left")
        
        comment_icon = load_ctk_icon("edit.png", (14, 14))
        if comment_icon:
            ctk.CTkLabel(header_inner, text="", image=comment_icon, fg_color="transparent").pack(side="left", padx=(10, 5))
        ctk.CTkLabel(header_inner, text="Commentaire", font=F_BOLD, text_color=TEXT_PRIMARY).pack(side="left")
        
        # Lignes de données avec design amélioré
        for record in history:
            row = ctk.CTkFrame(list_frame, fg_color=BG_SIDEBAR, corner_radius=10, border_width=1, border_color=BORDER_COLOR)
            row.pack(fill="x", padx=5, pady=3)
            
            row_inner = ctk.CTkFrame(row, fg_color="transparent")
            row_inner.pack(fill="x", padx=15, pady=10)
            
            # Date avec icône
            date_str = record.date.strftime("%d/%m/%Y") if hasattr(record.date, 'strftime') else str(record.date)
            date_container = ctk.CTkFrame(row_inner, fg_color="transparent")
            date_container.pack(side="left", padx=(0, 10))
            
            date_icon = load_ctk_icon("calendar.png", (12, 12))
            if date_icon:
                ctk.CTkLabel(date_container, text="", image=date_icon, fg_color="transparent").pack(side="left", padx=(0, 5))
            ctk.CTkLabel(date_container, text=date_str, font=F_TXT, text_color=TEXT_PRIMARY, width=120).pack(side="left")
            
            # Statut avec icône et couleur
            statut_color = {
                "Présent": SUCCESS_GREEN,
                "Absent": ERROR_RED,
                "Retard": WARNING_YELLOW,
                "Justifié": INFO_ORANGE
            }.get(record.statut, TEXT_SECONDARY)
            
            status_container = ctk.CTkFrame(row_inner, fg_color="transparent")
            status_container.pack(side="left", padx=(0, 10))
            
            # Icône selon le statut
            status_icon_name = {
                "Présent": "check_circle.png",
                "Absent": "close.png",
                "Retard": "clock_icon.png",
                "Justifié": "info.png"
            }.get(record.statut, "help.png")
            
            status_icon = load_ctk_icon(status_icon_name, (12, 12))
            if status_icon:
                ctk.CTkLabel(status_container, text="", image=status_icon, fg_color="transparent").pack(side="left", padx=(0, 5))
            
            statut_label = ctk.CTkLabel(status_container, text=record.statut, font=F_TXT, 
                                       text_color="white", fg_color=statut_color, 
                                       corner_radius=12, width=100)
            statut_label.pack(side="left")
            
            # Classe avec icône
            classe_name = getattr(record, 'classe_nom', 'N/A')
            class_container = ctk.CTkFrame(row_inner, fg_color="transparent")
            class_container.pack(side="left", padx=(0, 10))
            
            class_icon = load_ctk_icon("group.png", (12, 12))
            if class_icon:
                ctk.CTkLabel(class_container, text="", image=class_icon, fg_color="transparent").pack(side="left", padx=(0, 5))
            ctk.CTkLabel(class_container, text=classe_name, font=F_TXT, text_color=TEXT_SECONDARY, width=120).pack(side="left")
            
            # Commentaire avec icône
            commentaire = getattr(record, 'commentaire', '') or "-"
            comment_container = ctk.CTkFrame(row_inner, fg_color="transparent")
            comment_container.pack(side="left", fill="x", expand=True)
            
            comment_icon = load_ctk_icon("edit.png", (12, 12))
            if comment_icon:
                ctk.CTkLabel(comment_container, text="", image=comment_icon, fg_color="transparent").pack(side="left", padx=(0, 5))
            ctk.CTkLabel(comment_container, text=commentaire[:50] + "..." if len(commentaire) > 50 else commentaire, 
                        font=F_TXT, text_color=TEXT_PRIMARY).pack(side="left")
        
        # Boutons d'action avec design amélioré
        actions_frame = ctk.CTkFrame(history_window, fg_color="transparent")
        actions_frame.pack(fill="x", padx=20, pady=(0, 20))
        
        # Bouton Exporter PDF avec icône
        export_btn = ctk.CTkButton(actions_frame, text="Exporter PDF", 
                                  image=load_ctk_icon("file.png", (18, 18)),
                                  fg_color=ACCENT_BLUE, text_color="white", 
                                  hover_color="#4ECDC4", font=F_BOLD,
                                  height=40,
                                  command=lambda: self._export_student_history(eleve_id, student_name))
        export_btn.pack(side="left", padx=(0, 10))
        
        # Bouton Fermer avec icône
        close_btn = ctk.CTkButton(actions_frame, text="Fermer", 
                                 image=load_ctk_icon("close.png", (18, 18)),
                                 fg_color=ERROR_RED, text_color="white", 
                                 hover_color=HOVER_ERROR, font=F_BOLD,
                                 height=40,
                                 command=history_window.destroy)
        close_btn.pack(side="right")
    
    def _show_alerts(self, eleve_id):
        """Affiche les alertes pour un élève"""
        alerts = self.alert_service.check_student_alerts(eleve_id)
        
        if not alerts:
            messagebox.showinfo("Alertes", "Aucune alerte pour cet élève")
            return
        
        # Créer une fenêtre d'alertes
        alerts_window = ctk.CTkToplevel(self)
        alerts_window.title("Alertes de présence")
        alerts_window.geometry("600x400")
        alerts_window.configure(fg_color=BG_MAIN)
        alerts_window.grab_set()
        
        # En-tête
        header_frame = ctk.CTkFrame(alerts_window, fg_color=BG_CARD, corner_radius=12)
        header_frame.pack(fill="x", padx=15, pady=15)
        
        ctk.CTkLabel(header_frame, text="🚨 Alertes de Présence", 
                    font=F_TITLE, text_color=TEXT_PRIMARY).pack(pady=15)
        
        # Liste des alertes
        list_frame = ctk.CTkScrollableFrame(alerts_window, fg_color=BG_CARD, corner_radius=12)
        list_frame.pack(fill="both", expand=True, padx=15, pady=(0, 15))
        
        for alert in alerts:
            alert_frame = ctk.CTkFrame(list_frame, fg_color=BG_SIDEBAR, corner_radius=8)
            alert_frame.pack(fill="x", padx=5, pady=5)
            
            alert_inner = ctk.CTkFrame(alert_frame, fg_color="transparent")
            alert_inner.pack(fill="x", padx=10, pady=8)
            
            # Icône selon le niveau
            icon_map = {
                AlertLevel.INFO: "ℹ️",
                AlertLevel.WARNING: "⚠️",
                AlertLevel.CRITICAL: "🚨",
                AlertLevel.EMERGENCY: "🆘"
            }
            
            icon = icon_map.get(alert['level'], "ℹ️")
            ctk.CTkLabel(alert_inner, text=f"{icon} {alert['message']}", 
                        font=F_TXT, text_color=TEXT_PRIMARY).pack(anchor="w")
            
            # Détails
            if 'value' in alert and 'threshold' in alert:
                details = f"Valeur: {alert['value']} | Seuil: {alert['threshold']}"
                ctk.CTkLabel(alert_inner, text=details, 
                            font=F_SMALL, text_color=TEXT_SECONDARY).pack(anchor="w", pady=(2, 0))
        
        # Bouton fermer
        close_btn = ctk.CTkButton(alerts_window, text="❌ Fermer", 
                                 fg_color=ERROR_RED, text_color="white", 
                                 hover_color=HOVER_ERROR, font=F_BOLD,
                                 command=alerts_window.destroy)
        close_btn.pack(pady=15)
    
    def _export_student_history(self, eleve_id, student_name):
        """Exporte l'historique d'un élève en PDF"""
        try:
            file_path = filedialog.asksaveasfilename(
                title="Exporter l'historique",
                defaultextension=".pdf",
                filetypes=[("PDF", "*.pdf")]
            )
            
            if file_path:
                success = self.export_service.export_student_attendance_history_pdf(eleve_id, file_path)
                if success:
                    messagebox.showinfo("Succès", f"Historique exporté: {file_path}")
                else:
                    messagebox.showerror("Erreur", "Erreur lors de l'export")
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de l'export: {e}")
