# Vue principale moderne pour la gestion des présences
import customtkinter as ctk
from tkinter import messagebox
from datetime import datetime
from typing import List, Dict, Optional
import os
import sys

# Import du thème global EduManager+
try:
    root_path = os.path.join(os.path.dirname(__file__), '../../../../..')
    sys.path.insert(0, root_path)
    from resources.themes.theme import *
    print("✅ Thème global EduManager+ importé pour les présences")
except ImportError as e:
    print(f"⚠️ Erreur import thème: {e}")
    # Fallback avec constantes locales
    BG_MAIN = "#0A192F"
    BG_SIDEBAR = "#172A45"
    BG_CARD = "#0B2039"
    BORDER_COLOR = "#334155"
    ACCENT_BLUE = "#64FFDA"
    TEXT_PRIMARY = "#CCD6F6"
    TEXT_SECONDARY = "#8892B0"
    ERROR_RED = "#FF6363"
    SUCCESS_GREEN = "#A0E7E5"
    WARNING_YELLOW = "#FFD700"
    INFO_ORANGE = "#F97316"
    HOVER_SUCCESS = "#8cd5d3"
    HOVER_ERROR = "#e55252"
    HOVER_PRIMARY = "#2A456C"

# Import des services
from ..services.attendance_service import AttendanceService

# Polices
FONT = "Segoe UI"
F_TITLE = (FONT, 20, "bold")
F_SUB = (FONT, 14, "bold")
F_TXT = (FONT, 12)
F_SMALL = (FONT, 10)
F_BOLD = (FONT, 12, "bold")

STATUTS = ["Présent", "Absent", "Retard", "Justifié"]

class ModernAttendanceView(ctk.CTkFrame):
    """Vue moderne pour la gestion des présences"""
    
    def __init__(self, parent, icons):
        super().__init__(parent, fg_color=BG_MAIN)
        self.icons = icons
        self.ic = lambda k: self.icons.get(k)
        
        # Service principal
        self.attendance_service = AttendanceService()
        
        # Variables d'état
        self.selected_classe_id = None
        self.selected_date = datetime.now().strftime("%Y-%m-%d")
        self.current_student_id = None
        self.students_data = []
        self.attendance_data = {}
        
        # Variables de contrôle
        self.search_var = ctk.StringVar()
        self.filter_var = ctk.StringVar(value="Tous")
        
        # Configuration du layout
        self.grid_columnconfigure(0, weight=1, uniform="group1")
        self.grid_columnconfigure(1, weight=2, uniform="group1")
        self.grid_rowconfigure(0, weight=1)
        
        self._build_interface()
        self._load_initial_data()
    
    def _build_interface(self):
        """Construit l'interface utilisateur"""
        # Panneau de gauche (Contrôles et liste)
        self.left_panel = ctk.CTkFrame(self, fg_color=BG_CARD, corner_radius=12)
        self.left_panel.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        self.left_panel.grid_rowconfigure(4, weight=1)
        
        # Panneau de droite (Détails)
        self.right_panel = ctk.CTkFrame(self, fg_color=BG_CARD, corner_radius=12)
        self.right_panel.grid(row=0, column=1, sticky="nsew")
        
        self._build_left_panel()
        self._build_right_panel()
    
    def _build_left_panel(self):
        """Construit le panneau de gauche"""
        # Header
        header_frame = ctk.CTkFrame(self.left_panel, fg_color="transparent")
        header_frame.pack(fill="x", padx=20, pady=(20, 10))
        
        title_label = ctk.CTkLabel(header_frame, text="📋 Gestion des Présences", 
                                 font=F_TITLE, text_color=TEXT_PRIMARY)
        title_label.pack(anchor="w")
        
        subtitle_label = ctk.CTkLabel(header_frame, text="Sélectionnez une classe et une date", 
                                     font=F_SMALL, text_color=TEXT_SECONDARY)
        subtitle_label.pack(anchor="w", pady=(5, 0))
        
        # Contrôles de sélection
        self._build_selection_controls()
        
        # Actions en masse
        self._build_bulk_actions()
        
        # Recherche et filtres
        self._build_search_filters()
        
        # Liste des élèves
        self._build_students_list()
        
        # Statistiques
        self._build_statistics()
    
    def _build_selection_controls(self):
        """Construit les contrôles de sélection"""
        controls_frame = ctk.CTkFrame(self.left_panel, fg_color="transparent")
        controls_frame.pack(fill="x", padx=20, pady=(0, 10))
        controls_frame.grid_columnconfigure(0, weight=1)
        controls_frame.grid_columnconfigure(1, weight=1)
        
        # Sélection de classe
        self.class_combo = ctk.CTkComboBox(controls_frame, values=[], 
                                          fg_color=BG_SIDEBAR, border_color=BORDER_COLOR, 
                                          text_color=TEXT_PRIMARY, command=self._on_class_change)
        self.class_combo.grid(row=0, column=0, sticky="ew", padx=(0, 5))
        
        # Sélection de date
        date_frame = ctk.CTkFrame(controls_frame, fg_color=BG_SIDEBAR, 
                                 border_color=BORDER_COLOR, border_width=1)
        date_frame.grid(row=0, column=1, sticky="ew", padx=(5, 0))
        date_frame.grid_columnconfigure(0, weight=1)
        
        self.date_entry = ctk.CTkEntry(date_frame, placeholder_text="AAAA-MM-JJ", 
                                       border_width=0, fg_color="transparent", 
                                       font=F_TXT, text_color=TEXT_PRIMARY)
        self.date_entry.grid(row=0, column=0, sticky="ew", padx=(8, 0))
        self.date_entry.insert(0, self.selected_date)
        self.date_entry.bind("<KeyRelease>", lambda e: self._on_date_change())
        
        # Bouton calendrier
        calendar_btn = ctk.CTkButton(date_frame, text="📅", width=30, 
                                     fg_color="transparent", hover_color=BG_CARD,
                                     command=self._pick_date)
        calendar_btn.grid(row=0, column=1, padx=4, pady=4)
    
    def _build_bulk_actions(self):
        """Construit les actions en masse"""
        actions_frame = ctk.CTkFrame(self.left_panel, fg_color="transparent")
        actions_frame.pack(fill="x", padx=20, pady=(0, 10))
        
        # Titre des actions
        actions_title = ctk.CTkLabel(actions_frame, text="⚡ Actions Rapides", 
                                    font=F_SUB, text_color=TEXT_PRIMARY)
        actions_title.pack(anchor="w", pady=(0, 8))
        
        # Boutons d'action
        buttons_frame = ctk.CTkFrame(actions_frame, fg_color="transparent")
        buttons_frame.pack(fill="x")
        buttons_frame.grid_columnconfigure((0, 1, 2), weight=1)
        
        # Bouton Valider tout Présent
        validate_btn = ctk.CTkButton(buttons_frame, text="✅ Tous Présents", 
                                    fg_color=SUCCESS_GREEN, text_color=BG_MAIN, 
                                    hover_color=HOVER_SUCCESS, font=F_BOLD,
                                    command=self._validate_all_present)
        validate_btn.grid(row=0, column=0, sticky="ew", padx=(0, 5))
        
        # Bouton Marquer tout Absent
        absent_btn = ctk.CTkButton(buttons_frame, text="❌ Tous Absents", 
                                  fg_color=ERROR_RED, text_color="white", 
                                  hover_color=HOVER_ERROR, font=F_BOLD,
                                  command=self._mark_all_absent)
        absent_btn.grid(row=0, column=1, sticky="ew", padx=5)
        
        # Bouton Réinitialiser
        reset_btn = ctk.CTkButton(buttons_frame, text="🔄 Reset", 
                                 fg_color=WARNING_YELLOW, text_color=BG_MAIN, 
                                 hover_color="#FFA500", font=F_BOLD,
                                 command=self._reset_all)
        reset_btn.grid(row=0, column=2, sticky="ew", padx=(5, 0))
    
    def _build_search_filters(self):
        """Construit les contrôles de recherche et filtres"""
        search_frame = ctk.CTkFrame(self.left_panel, fg_color="transparent")
        search_frame.pack(fill="x", padx=20, pady=(0, 10))
        search_frame.grid_columnconfigure(0, weight=1)
        
        # Barre de recherche
        search_entry = ctk.CTkEntry(search_frame, textvariable=self.search_var, 
                                   placeholder_text="🔍 Rechercher un élève...",
                                   fg_color=BG_SIDEBAR, border_color=BORDER_COLOR,
                                   text_color=TEXT_PRIMARY)
        search_entry.grid(row=0, column=0, sticky="ew", padx=(0, 5))
        search_entry.bind("<KeyRelease>", lambda e: self._on_search_change())
        
        # Filtre par statut
        self.filter_combo = ctk.CTkComboBox(search_frame, values=["Tous"] + STATUTS, 
                                           variable=self.filter_var, fg_color=BG_SIDEBAR, 
                                           border_color=BORDER_COLOR, text_color=TEXT_PRIMARY,
                                           command=lambda *_: self._on_filter_change())
        self.filter_combo.grid(row=0, column=1, sticky="ew", padx=(5, 0))
    
    def _build_students_list(self):
        """Construit la liste des élèves"""
        # Container pour la liste
        self.students_container = ctk.CTkScrollableFrame(self.left_panel, 
                                                        fg_color=BG_MAIN, corner_radius=0)
        self.students_container.pack(fill="both", expand=True, padx=20, pady=(0, 10))
    
    def _build_statistics(self):
        """Construit la section des statistiques"""
        self.stats_frame = ctk.CTkFrame(self.left_panel, fg_color=BG_CARD, 
                                       corner_radius=12, border_width=1, border_color=BORDER_COLOR)
        self.stats_frame.pack(fill="x", padx=20, pady=(0, 20))
    
    def _build_right_panel(self):
        """Construit le panneau de droite"""
        # Header du panneau de droite
        header_frame = ctk.CTkFrame(self.right_panel, fg_color="transparent")
        header_frame.pack(fill="x", padx=20, pady=(20, 10))
        
        self.detail_title = ctk.CTkLabel(header_frame, text="👤 Sélectionnez un élève", 
                                        font=F_TITLE, text_color=TEXT_PRIMARY)
        self.detail_title.pack(anchor="w")
        
        # Contenu principal
        self.detail_content = ctk.CTkFrame(self.right_panel, fg_color="transparent")
        self.detail_content.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        self._show_empty_details()
    
    def _load_initial_data(self):
        """Charge les données initiales"""
        # Charger les classes
        classes = self.attendance_service.get_classes_with_students()
        class_names = [f"{c['nom_classe']} ({c['student_count']} élèves)" for c in classes]
        
        self.class_combo.configure(values=class_names)
        self.classes_data = classes
        
        if classes:
            self.class_combo.set(class_names[0])
            self._on_class_change(class_names[0])
    
    def _on_class_change(self, selected_class):
        """Gère le changement de classe"""
        if not selected_class:
            return
        
        # Extraire l'ID de la classe
        class_name = selected_class.split(" (")[0]
        for classe in self.classes_data:
            if classe['nom_classe'] == class_name:
                self.selected_classe_id = classe['id_classe']
                break
        
        self._refresh_students_list()
        self._refresh_statistics()
    
    def _on_date_change(self):
        """Gère le changement de date"""
        self.selected_date = self.date_entry.get().strip()
        self._refresh_students_list()
        self._refresh_statistics()
    
    def _on_search_change(self):
        """Gère le changement de recherche"""
        self._refresh_students_list()
    
    def _on_filter_change(self):
        """Gère le changement de filtre"""
        self._refresh_students_list()
    
    def _refresh_students_list(self):
        """Actualise la liste des élèves"""
        if not self.selected_classe_id:
            return
        
        # Nettoyer la liste
        for widget in self.students_container.winfo_children():
            widget.destroy()
        
        # Récupérer les données
        overview = self.attendance_service.get_class_attendance_overview(
            self.selected_classe_id, self.selected_date
        )
        
        self.students_data = overview['students']
        self.attendance_data = overview['stats']
        
        # Filtrer les données
        filtered_students = self._filter_students(self.students_data)
        
        # Afficher les élèves
        for student in filtered_students:
            self._create_student_item(student)
    
    def _filter_students(self, students):
        """Filtre les élèves selon les critères"""
        filtered = students
        
        # Filtre par recherche
        search_term = self.search_var.get().lower()
        if search_term:
            filtered = [s for s in filtered if 
                       search_term in s['nom'].lower() or 
                       search_term in s['prenom'].lower()]
        
        # Filtre par statut
        status_filter = self.filter_var.get()
        if status_filter != "Tous":
            filtered = [s for s in filtered if s['statut'] == status_filter]
        
        return filtered
    
    def _create_student_item(self, student):
        """Crée un élément de liste pour un élève"""
        # Couleur selon le statut
        statut_colors = {
            "Présent": SUCCESS_GREEN,
            "Absent": ERROR_RED,
            "Retard": WARNING_YELLOW,
            "Justifié": INFO_ORANGE
        }
        
        statut_color = statut_colors.get(student['statut'], TEXT_SECONDARY)
        
        # Item principal
        item_frame = ctk.CTkFrame(self.students_container, fg_color=BG_SIDEBAR, 
                                 corner_radius=8, border_width=1, border_color=statut_color)
        item_frame.pack(fill="x", padx=5, pady=2)
        
        # Contenu de l'item
        content_frame = ctk.CTkFrame(item_frame, fg_color="transparent")
        content_frame.pack(fill="x", padx=12, pady=8)
        
        # Icône élève
        icon_label = ctk.CTkLabel(content_frame, text="👤", font=("Segoe UI", 16))
        icon_label.pack(side="left", padx=(0, 10))
        
        # Informations de l'élève
        info_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        info_frame.pack(side="left", fill="x", expand=True)
        
        # Nom complet
        name_label = ctk.CTkLabel(info_frame, text=f"{student['prenom']} {student['nom']}", 
                                 font=F_TXT, text_color=TEXT_PRIMARY)
        name_label.pack(anchor="w")
        
        # Email
        email_label = ctk.CTkLabel(info_frame, text=student['email'], 
                                  font=F_SMALL, text_color=TEXT_SECONDARY)
        email_label.pack(anchor="w")
        
        # Badge de statut
        statut_badge = ctk.CTkLabel(content_frame, text=student['statut'], 
                                   font=F_SMALL, text_color="white", 
                                   fg_color=statut_color, corner_radius=12, 
                                   width=80, height=24)
        statut_badge.pack(side="right", padx=(10, 0))
        
        # Bindings pour la sélection
        def select_student():
            self._select_student(student)
        
        for widget in [item_frame, content_frame, info_frame, name_label, email_label]:
            widget.bind("<Button-1>", lambda e: select_student())
            widget.configure(cursor="hand2")
    
    def _select_student(self, student):
        """Sélectionne un élève et affiche ses détails"""
        self.current_student_id = student['id_eleve']
        self._show_student_details(student)
    
    def _show_student_details(self, student):
        """Affiche les détails d'un élève"""
        # Nettoyer le contenu
        for widget in self.detail_content.winfo_children():
            widget.destroy()
        
        # Mettre à jour le titre
        self.detail_title.configure(text=f"👤 {student['prenom']} {student['nom']}")
        
        # Contenu des détails
        details_frame = ctk.CTkFrame(self.detail_content, fg_color="transparent")
        details_frame.pack(fill="both", expand=True)
        
        # Informations de base
        info_card = ctk.CTkFrame(details_frame, fg_color=BG_SIDEBAR, corner_radius=12)
        info_card.pack(fill="x", pady=(0, 15))
        
        info_inner = ctk.CTkFrame(info_card, fg_color="transparent")
        info_inner.pack(fill="x", padx=15, pady=15)
        
        # Email
        email_label = ctk.CTkLabel(info_inner, text=f"📧 {student['email']}", 
                                  font=F_TXT, text_color=TEXT_PRIMARY)
        email_label.pack(anchor="w", pady=(0, 5))
        
        # Statut actuel
        statut_colors = {
            "Présent": SUCCESS_GREEN,
            "Absent": ERROR_RED,
            "Retard": WARNING_YELLOW,
            "Justifié": INFO_ORANGE
        }
        
        current_statut = student['statut']
        statut_color = statut_colors.get(current_statut, TEXT_SECONDARY)
        
        statut_label = ctk.CTkLabel(info_inner, text=f"Statut: {current_statut}", 
                                   font=F_BOLD, text_color=statut_color)
        statut_label.pack(anchor="w", pady=(0, 10))
        
        # Contrôles de modification
        controls_card = ctk.CTkFrame(details_frame, fg_color=BG_SIDEBAR, corner_radius=12)
        controls_card.pack(fill="x", pady=(0, 15))
        
        controls_inner = ctk.CTkFrame(controls_card, fg_color="transparent")
        controls_inner.pack(fill="x", padx=15, pady=15)
        
        # Titre des contrôles
        controls_title = ctk.CTkLabel(controls_inner, text="✏️ Modifier le statut", 
                                      font=F_SUB, text_color=TEXT_PRIMARY)
        controls_title.pack(anchor="w", pady=(0, 10))
        
        # Sélecteur de statut
        statut_var = ctk.StringVar(value=current_statut)
        statut_combo = ctk.CTkComboBox(controls_inner, values=STATUTS, 
                                      variable=statut_var, fg_color=BG_CARD, 
                                      border_color=BORDER_COLOR, text_color=TEXT_PRIMARY)
        statut_combo.pack(fill="x", pady=(0, 10))
        
        # Zone de commentaire
        comment_label = ctk.CTkLabel(controls_inner, text="💬 Commentaire", 
                                     font=F_TXT, text_color=TEXT_PRIMARY)
        comment_label.pack(anchor="w", pady=(0, 5))
        
        comment_text = ctk.CTkTextbox(controls_inner, height=80, fg_color=BG_CARD, 
                                     border_color=BORDER_COLOR, font=F_TXT, 
                                     text_color=TEXT_PRIMARY)
        comment_text.pack(fill="x", pady=(0, 15))
        
        if student['commentaire']:
            comment_text.insert("1.0", student['commentaire'])
        
        # Boutons d'action
        buttons_frame = ctk.CTkFrame(controls_inner, fg_color="transparent")
        buttons_frame.pack(fill="x")
        buttons_frame.grid_columnconfigure((0, 1), weight=1)
        
        # Bouton Appliquer
        apply_btn = ctk.CTkButton(buttons_frame, text="✅ Appliquer", 
                                 fg_color=SUCCESS_GREEN, text_color=BG_MAIN, 
                                 hover_color=HOVER_SUCCESS, font=F_BOLD,
                                 command=lambda: self._apply_student_changes(
                                     student, statut_var.get(), comment_text.get("1.0", "end-1c").strip()
                                 ))
        apply_btn.grid(row=0, column=0, sticky="ew", padx=(0, 5))
        
        # Bouton Historique
        history_btn = ctk.CTkButton(buttons_frame, text="📋 Historique", 
                                   fg_color=ACCENT_BLUE, text_color="white", 
                                   hover_color="#4ECDC4", font=F_BOLD,
                                   command=lambda: self._show_student_history(student))
        history_btn.grid(row=0, column=1, sticky="ew", padx=(5, 0))
    
    def _show_empty_details(self):
        """Affiche l'état vide des détails"""
        empty_frame = ctk.CTkFrame(self.detail_content, fg_color="transparent")
        empty_frame.pack(expand=True)
        
        empty_label = ctk.CTkLabel(empty_frame, text="👈 Sélectionnez un élève pour voir ses détails", 
                                  font=F_SUB, text_color=TEXT_SECONDARY)
        empty_label.pack(expand=True)
    
    def _apply_student_changes(self, student, new_statut, commentaire):
        """Applique les modifications à un élève"""
        success = self.attendance_service.update_student_attendance(
            student['id_eleve'], self.selected_classe_id, self.selected_date, 
            new_statut, commentaire
        )
        
        if success:
            messagebox.showinfo("Succès", f"Statut de {student['prenom']} {student['nom']} mis à jour.")
            self._refresh_students_list()
            self._refresh_statistics()
        else:
            messagebox.showerror("Erreur", "Erreur lors de la mise à jour.")
    
    def _show_student_history(self, student):
        """Affiche l'historique d'un élève"""
        # TODO: Implémenter la vue d'historique
        messagebox.showinfo("Historique", f"Historique de {student['prenom']} {student['nom']} - À implémenter")
    
    def _refresh_statistics(self):
        """Actualise les statistiques"""
        # Nettoyer les statistiques
        for widget in self.stats_frame.winfo_children():
            widget.destroy()
        
        if not self.selected_classe_id:
            return
        
        # Récupérer les statistiques
        overview = self.attendance_service.get_class_attendance_overview(
            self.selected_classe_id, self.selected_date
        )
        
        stats = overview['stats']
        total_students = overview['total_students']
        
        # Header des statistiques
        stats_header = ctk.CTkFrame(self.stats_frame, fg_color="transparent")
        stats_header.pack(fill="x", padx=15, pady=(12, 8))
        
        classe_name = self.class_combo.get().split(" (")[0] if self.class_combo.get() else "Aucune classe"
        
        stats_title = ctk.CTkLabel(stats_header, text=f"📊 {classe_name} - {self.selected_date}", 
                                  font=F_SUB, text_color=TEXT_PRIMARY)
        stats_title.pack(side="left")
        
        total_label = ctk.CTkLabel(stats_header, text=f"Total: {total_students} élèves", 
                                  font=F_SMALL, text_color=TEXT_SECONDARY)
        total_label.pack(side="right")
        
        # Chips des statistiques
        chips_frame = ctk.CTkFrame(self.stats_frame, fg_color="transparent")
        chips_frame.pack(fill="x", padx=15, pady=(0, 12))
        chips_frame.grid_columnconfigure((0, 1, 2, 3), weight=1)
        
        def create_stat_chip(label, count, color, col, icon=""):
            chip_frame = ctk.CTkFrame(chips_frame, fg_color=BG_SIDEBAR, corner_radius=8, 
                                     border_width=1, border_color=color)
            chip_frame.grid(row=0, column=col, sticky="ew", padx=5)
            
            chip_header = ctk.CTkFrame(chip_frame, fg_color="transparent")
            chip_header.pack(fill="x", padx=8, pady=(6, 2))
            
            ctk.CTkLabel(chip_header, text=f"{icon} {label}", font=F_SMALL, text_color=color).pack(side="left")
            
            ctk.CTkLabel(chip_frame, text=str(count), font=("Segoe UI", 16, "bold"), 
                        text_color=TEXT_PRIMARY).pack(pady=(0, 6))
            
            if total_students > 0:
                percentage = (count / total_students) * 100
                ctk.CTkLabel(chip_frame, text=f"{percentage:.1f}%", font=F_SMALL, 
                            text_color=TEXT_SECONDARY).pack(pady=(0, 4))
        
        create_stat_chip("Présents", stats.get("Présent", 0), SUCCESS_GREEN, 0, "✅")
        create_stat_chip("Absents", stats.get("Absent", 0), ERROR_RED, 1, "❌")
        create_stat_chip("Retards", stats.get("Retard", 0), WARNING_YELLOW, 2, "⏰")
        create_stat_chip("Justifiés", stats.get("Justifié", 0), INFO_ORANGE, 3, "📝")
    
    def _validate_all_present(self):
        """Valide toutes les présences comme Présent"""
        if not self.selected_classe_id:
            messagebox.showwarning("Attention", "Sélectionnez une classe.")
            return
        
        if messagebox.askyesno("Confirmation", 
                              f"Valider toutes les présences comme 'Présent' pour le {self.selected_date} ?"):
            
            success = self.attendance_service.validate_all_present(
                self.selected_classe_id, self.selected_date
            )
            
            if success:
                messagebox.showinfo("Succès", "Toutes les présences ont été validées comme 'Présent'.")
                self._refresh_students_list()
                self._refresh_statistics()
            else:
                messagebox.showerror("Erreur", "Erreur lors de la validation en masse.")
    
    def _mark_all_absent(self):
        """Marque toutes les présences comme Absent"""
        if not self.selected_classe_id:
            messagebox.showwarning("Attention", "Sélectionnez une classe.")
            return
        
        if messagebox.askyesno("Confirmation", 
                              f"Marquer toutes les présences comme 'Absent' pour le {self.selected_date} ?"):
            
            success = self.attendance_service.mark_all_absent(
                self.selected_classe_id, self.selected_date
            )
            
            if success:
                messagebox.showinfo("Succès", "Toutes les présences ont été marquées comme 'Absent'.")
                self._refresh_students_list()
                self._refresh_statistics()
            else:
                messagebox.showerror("Erreur", "Erreur lors du marquage en masse.")
    
    def _reset_all(self):
        """Réinitialise toutes les présences"""
        if not self.selected_classe_id:
            messagebox.showwarning("Attention", "Sélectionnez une classe.")
            return
        
        if messagebox.askyesno("Confirmation", 
                              f"Réinitialiser toutes les présences pour le {self.selected_date} ?\n\nCela supprimera tous les enregistrements de présence pour cette date."):
            
            success = self.attendance_service.reset_all_attendance(
                self.selected_classe_id, self.selected_date
            )
            
            if success:
                messagebox.showinfo("Succès", "Toutes les présences ont été réinitialisées.")
                self._refresh_students_list()
                self._refresh_statistics()
            else:
                messagebox.showerror("Erreur", "Erreur lors de la réinitialisation.")
    
    def _pick_date(self):
        """Ouvre le sélecteur de date"""
        # TODO: Implémenter le sélecteur de date
        messagebox.showinfo("Sélecteur de date", "Sélecteur de date - À implémenter")
