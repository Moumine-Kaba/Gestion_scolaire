# -*- coding: utf-8 -*-
"""
Vue des Matières du Système Éducatif Guinéen
EduManager+ - Interface Moderne par Niveaux et Séries

Cette vue présente les matières organisées selon le système éducatif guinéen
avec une navigation par niveaux et une gestion intuitive.
"""

import customtkinter as ctk
from tkinter import messagebox, StringVar, ttk
import tkinter.font as tkfont
import os
import sys
from typing import List, Dict, Optional

# Import du thème global EduManager+
try:
    root_path = os.path.join(os.path.dirname(__file__), '../../../../..')
    sys.path.insert(0, root_path)
    from resources.themes.theme import *
    print("✅ Thème global EduManager+ importé pour les matières guinéennes")
except ImportError as e:
    print(f"⚠️ Erreur import thème: {e}")
    # Fallback avec constantes locales
    BG_MAIN = "#0A192F"
    CARD_BG = "#0b1d34"
    ACCENT = "#64FFDA"
    TEXT = "#E2E8F0"
    MUTED = "#8aa0b8"
    SUCCESS_GREEN = "#059669"
    ERROR_RED = "#DC2626"
    WARNING_YELLOW = "#D97706"

# Import du contrôleur guinéen
try:
    from src.modules.academic.subjects.controllers.guinean_subjects_controller import (
        get_guinean_subjects_controller, get_subjects_for_grade, 
        get_core_subjects_for_grade, get_optional_subjects_for_grade,
        get_all_available_grades, get_grade_education_level
    )
    print("✅ Contrôleur des matières guinéennes importé")
except ImportError as e:
    print(f"⚠️ Erreur import contrôleur guinéen: {e}")

def load_ctk_icon(icon_name, size=(22, 22)):
    """Charge une icône depuis le pack utilisateurs"""
    try:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.join(current_dir, '../../../../..')
        icons_path = os.path.join(project_root, 'resources', 'icons')
        icon_path = os.path.join(icons_path, icon_name)
        
        if os.path.exists(icon_path):
            from PIL import Image
            image = Image.open(icon_path)
            icon = ctk.CTkImage(light_image=image, dark_image=image, size=size)
            return icon
    except Exception as e:
        print(f"⚠️ Erreur chargement icône {icon_name}: {e}")
        return None

class GuineanSubjectsView(ctk.CTkFrame):
    """Vue principale des matières guinéennes avec navigation par niveaux"""

    def __init__(self, parent, icons=None):
        super().__init__(parent, fg_color=BG_MAIN)
        self.grid_columnconfigure(0, weight=1)
        
        self.controller = get_guinean_subjects_controller()
        self.current_level = None
        self.current_grade = None
        self.filtered_subjects = []
        
        self.var_search = StringVar()
        self.var_level_filter = StringVar()
        self.var_grade_filter = StringVar()
        
        self._build_interface()
        self._load_initial_data()

    def _build_interface(self):
        """Construit l'interface utilisateur complète"""
        # Header principal
        self._build_header()
        
        # Panneau de navigation et filtres
        self._build_navigation_panel()
        
        # Zone de contenu principal
        self._build_content_area()
        
        # Bindings
        self.var_search.trace_add("write", self._on_search_change)
        self.var_level_filter.trace_add("write", self._on_level_filter_change)
        self.var_grade_filter.trace_add("write", self._on_grade_filter_change)

    def _build_header(self):
        """Header avec titre et description"""
        header_frame = ctk.CTkFrame(self, fg_color=BG_SIDEBAR, corner_radius=20, 
                                   border_width=1, border_color=BORDER_COLOR)
        header_frame.pack(fill="x", padx=12, pady=(12, 6))
        
        header_content = ctk.CTkFrame(header_frame, fg_color="transparent")
        header_content.pack(fill="x", padx=PADDING_CARD, pady=PADDING_CARD)
        
        # Section gauche - Titre et description
        left_section = ctk.CTkFrame(header_content, fg_color="transparent")
        left_section.pack(side="left", fill="x", expand=True)
        
        title_container = ctk.CTkFrame(left_section, fg_color="transparent")
        title_container.pack(anchor="w")
        
        # Icône principale
        main_icon = load_ctk_icon("book.png", (24, 24)) or load_ctk_icon("stacks.png", (24, 24))
        if main_icon:
            ctk.CTkLabel(title_container, text="", image=main_icon, 
                        fg_color="transparent").pack(side="left", padx=(0, MARGIN_MEDIUM))
        else:
            ctk.CTkLabel(title_container, text="📚", font=FONT_TITLE, 
                        text_color=TEXT_PRIMARY).pack(side="left", padx=(0, MARGIN_MEDIUM))
        
        # Titre
        title_text = ctk.CTkLabel(title_container, text="Matières du Système Éducatif Guinéen",
                                 font=FONT_TITLE, text_color=TEXT_PRIMARY)
        title_text.pack(side="left")
        
        # Description
        desc_text = ctk.CTkLabel(left_section, text="Organisées par niveaux : Primaire, Collège, Lycée",
                                font=FONT_SECONDARY, text_color=TEXT_SECONDARY)
        desc_text.pack(anchor="w", pady=(MARGIN_SMALL, 0))
        
        # Section droite - Actions
        right_section = ctk.CTkFrame(header_content, fg_color="transparent")
        right_section.pack(side="right", fill="y")
        
        # Bouton actualiser
        refresh_icon = load_ctk_icon("refresh.png", (18, 18))
        refresh_btn = ctk.CTkButton(right_section, text="Actualiser", image=refresh_icon, 
                                   compound="left", font=FONT_BUTTON, fg_color="transparent", 
                                   text_color=TEXT_PRIMARY, hover_color=HOVER_PRIMARY,
                                   command=self._refresh_data, corner_radius=10, height=40,
                                   border_width=2, border_color=BORDER_COLOR)
        refresh_btn.pack(side="right")

    def _build_navigation_panel(self):
        """Panneau de navigation avec filtres"""
        nav_frame = ctk.CTkFrame(self, fg_color=CARD_BG, corner_radius=16,
                                border_width=1, border_color=BORDER_COLOR)
        nav_frame.pack(fill="x", padx=12, pady=(0, 6))
        
        nav_content = ctk.CTkFrame(nav_frame, fg_color="transparent")
        nav_content.pack(fill="x", padx=PADDING_CARD, pady=PADDING_CARD)
        
        # Filtres en ligne
        filters_frame = ctk.CTkFrame(nav_content, fg_color="transparent")
        filters_frame.pack(fill="x")
        
        # Filtre par niveau
        ctk.CTkLabel(filters_frame, text="Niveau:", font=FONT_BUTTON, 
                    text_color=TEXT_PRIMARY).pack(side="left", padx=(0, MARGIN_SMALL))
        
        self.level_combo = ctk.CTkComboBox(filters_frame, values=["Tous les niveaux"],
                                          variable=self.var_level_filter, font=FONT_PRIMARY,
                                          fg_color=BG_MAIN, text_color=TEXT_PRIMARY,
                                          border_color=BORDER_COLOR, corner_radius=12,
                                          height=35, width=150, command=self._on_level_filter_change)
        self.level_combo.pack(side="left", padx=(0, MARGIN_MEDIUM))
        
        # Filtre par classe
        ctk.CTkLabel(filters_frame, text="Classe:", font=FONT_BUTTON, 
                    text_color=TEXT_PRIMARY).pack(side="left", padx=(0, MARGIN_SMALL))
        
        self.grade_combo = ctk.CTkComboBox(filters_frame, values=["Toutes les classes"],
                                          variable=self.var_grade_filter, font=FONT_PRIMARY,
                                          fg_color=BG_MAIN, text_color=TEXT_PRIMARY,
                                          border_color=BORDER_COLOR, corner_radius=12,
                                          height=35, width=150, command=self._on_grade_filter_change)
        self.grade_combo.pack(side="left", padx=(0, MARGIN_MEDIUM))
        
        # Barre de recherche
        search_frame = ctk.CTkFrame(filters_frame, fg_color=BG_MAIN, corner_radius=15,
                                   border_width=2, border_color=BORDER_COLOR)
        search_frame.pack(side="right")
        
        search_inner = ctk.CTkFrame(search_frame, fg_color="transparent")
        search_inner.pack(fill="both", expand=True, padx=PADDING_MEDIUM, pady=PADDING_MEDIUM)
        
        search_icon = load_ctk_icon("search.png", (16, 16))
        if search_icon:
            ctk.CTkLabel(search_inner, text="", image=search_icon, 
                        fg_color="transparent").pack(side="left", padx=(0, MARGIN_SMALL))
        
        self.entry_search = ctk.CTkEntry(search_inner, placeholder_text="Rechercher une matière...",
                                        textvariable=self.var_search, font=FONT_PRIMARY,
                                        fg_color="transparent", text_color=TEXT_PRIMARY,
                                        border_color="transparent", corner_radius=10,
                                        height=30, width=250)
        self.entry_search.pack(side="left", padx=(0, MARGIN_SMALL))

    def _build_content_area(self):
        """Zone de contenu principal avec onglets"""
        # Conteneur principal
        content_container = ctk.CTkFrame(self, fg_color="transparent")
        content_container.pack(fill="both", expand=True, padx=12, pady=(0, 8))
        
        # Zone des statistiques
        self._build_stats_section(content_container)
        
        # Zone des matières
        self._build_subjects_area(content_container)

    def _build_stats_section(self):
        """Section des statistiques"""
        self.stats_frame = ctk.CTkFrame(self, fg_color=CARD_BG, corner_radius=16,
                                       border_width=1, border_color=BORDER_COLOR)
        self.stats_frame.pack(fill="x", padx=12, pady=(0, 6))
        
        stats_content = ctk.CTkFrame(self.stats_frame, fg_color="transparent")
        stats_content.pack(fill="x", padx=PADDING_CARD, pady=PADDING_CARD)
        
        # Statistiques principales
        stats_left = ctk.CTkFrame(stats_content, fg_color="transparent")
        stats_left.pack(side="left", fill="x", expand=True)
        
        stats_icon = load_ctk_icon("stats.png", (20, 20))
        if stats_icon:
            ctk.CTkLabel(stats_left, text="", image=stats_icon, 
                        fg_color="transparent").pack(side="left", padx=(0, MARGIN_MEDIUM))
        
        self.lbl_stats = ctk.CTkLabel(stats_left, text="Chargement des statistiques...",
                                     font=FONT_METRIC, text_color=TEXT_ACCENT)
        self.lbl_stats.pack(side="left")
        
        # Informations de filtre
        self.lbl_filter_info = ctk.CTkLabel(stats_content, text="",
                                           font=FONT_SECONDARY, text_color=TEXT_SECONDARY)
        self.lbl_filter_info.pack(side="right")

    def _build_subjects_area(self):
        """Zone d'affichage des matières"""
        # Zone scrollable pour les matières
        self.subjects_area = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.subjects_area.pack(fill="both", expand=True, padx=8, pady=(0, 8))
        self.subjects_area.grid_columnconfigure((0, 1, 2), weight=1, uniform="col")

    def _load_initial_data(self):
        """Charge les données initiales"""
        try:
            # Charger les niveaux disponibles
            levels = self.controller.get_education_levels()
            level_values = ["Tous les niveaux"] + [level.title() for level in levels]
            self.level_combo.configure(values=level_values)
            
            # Charger les classes disponibles
            grades = self.controller.get_available_grades()
            grade_values = ["Toutes les classes"] + grades
            self.grade_combo.configure(values=grade_values)
            
            # Charger les statistiques
            self._update_statistics()
            
            # Charger toutes les matières initialement
            self._load_all_subjects()
            
        except Exception as e:
            print(f"❌ Erreur lors du chargement initial : {e}")
            self._show_error_state("Erreur lors du chargement des données")

    def _load_all_subjects(self):
        """Charge toutes les matières"""
        try:
            self.filtered_subjects = self.controller.get_all_subjects()
            self._render_subjects()
            self._update_filter_info()
        except Exception as e:
            print(f"❌ Erreur lors du chargement des matières : {e}")
            self._show_error_state("Erreur lors du chargement des matières")

    def _load_subjects_by_level(self, level: str):
        """Charge les matières d'un niveau spécifique"""
        try:
            self.filtered_subjects = self.controller.get_subjects_by_level(level.lower())
            self._render_subjects()
            self._update_filter_info()
        except Exception as e:
            print(f"❌ Erreur lors du chargement des matières du niveau {level} : {e}")
            self._show_error_state(f"Erreur pour le niveau {level}")

    def _load_subjects_by_grade(self, grade: str):
        """Charge les matières d'une classe spécifique"""
        try:
            self.filtered_subjects = self.controller.get_subjects_by_grade(grade)
            self._render_subjects()
            self._update_filter_info()
        except Exception as e:
            print(f"❌ Erreur lors du chargement des matières de la classe {grade} : {e}")
            self._show_error_state(f"Erreur pour la classe {grade}")

    def _search_subjects(self, query: str):
        """Recherche des matières"""
        try:
            if query.strip():
                level = self.var_level_filter.get().lower() if self.var_level_filter.get() != "Tous les niveaux" else None
                grade = self.var_grade_filter.get() if self.var_grade_filter.get() != "Toutes les classes" else None
                self.filtered_subjects = self.controller.search_subjects(query, level, grade)
            else:
                self._apply_filters()
            self._render_subjects()
            self._update_filter_info()
        except Exception as e:
            print(f"❌ Erreur lors de la recherche : {e}")
            self._show_error_state("Erreur lors de la recherche")

    def _apply_filters(self):
        """Applique les filtres sélectionnés"""
        level = self.var_level_filter.get()
        grade = self.var_grade_filter.get()
        
        if grade != "Toutes les classes":
            self._load_subjects_by_grade(grade)
        elif level != "Tous les niveaux":
            self._load_subjects_by_level(level)
        else:
            self._load_all_subjects()

    def _render_subjects(self):
        """Affiche les matières dans l'interface"""
        # Nettoyer la zone d'affichage
        for widget in self.subjects_area.winfo_children():
            widget.destroy()
        
        if not self.filtered_subjects:
            self._render_empty_state()
            return
        
        # Grouper les matières par niveau et classe
        grouped_subjects = self._group_subjects_by_level_grade()
        
        row = 0
        for level, grades in grouped_subjects.items():
            # En-tête du niveau
            level_header = self._create_level_header(level)
            level_header.grid(row=row, column=0, columnspan=3, sticky="ew", padx=4, pady=(8, 4))
            row += 1
            
            for grade, subjects in grades.items():
                # En-tête de la classe
                grade_header = self._create_grade_header(grade, len(subjects))
                grade_header.grid(row=row, column=0, columnspan=3, sticky="ew", padx=8, pady=(4, 2))
                row += 1
                
                # Matières de la classe
                for i, subject in enumerate(subjects):
                    col = i % 3
                    card = self._create_subject_card(subject)
                    card.grid(row=row, column=col, sticky="ew", padx=4, pady=2)
                    if col == 2:  # Nouvelle ligne après 3 colonnes
                        row += 1
                
                if len(subjects) % 3 != 0:  # Passer à la ligne suivante si nécessaire
                    row += 1

    def _group_subjects_by_level_grade(self) -> Dict[str, Dict[str, List[Dict]]]:
        """Groupe les matières par niveau puis par classe"""
        grouped = {}
        
        for subject in self.filtered_subjects:
            level = subject.get("education_level", "inconnu")
            grade = subject.get("grade", "inconnu")
            
            if level not in grouped:
                grouped[level] = {}
            if grade not in grouped[level]:
                grouped[level][grade] = []
            
            grouped[level][grade].append(subject)
        
        # Trier les matières dans chaque groupe
        for level in grouped:
            for grade in grouped[level]:
                grouped[level][grade].sort(key=lambda x: (not x.get("is_core", True), x.get("name", "")))
        
        return grouped

    def _create_level_header(self, level: str) -> ctk.CTkFrame:
        """Crée l'en-tête d'un niveau"""
        level_names = {
            "primaire": "🎒 Primaire (CP1 → CM2)",
            "college": "🎓 Collège (7ème → 10ème année)",
            "lycee": "🎯 Lycée (11ème → 12ème année)"
        }
        
        header = ctk.CTkFrame(self.subjects_area, fg_color=ACCENT, corner_radius=12)
        header.pack_propagate(False)
        header.configure(height=50)
        
        content = ctk.CTkFrame(header, fg_color="transparent")
        content.pack(fill="both", expand=True, padx=PADDING_MEDIUM, pady=PADDING_MEDIUM)
        
        title = ctk.CTkLabel(content, text=level_names.get(level, level.title()),
                            font=FONT_SUBTITLE, text_color=BG_MAIN)
        title.pack(anchor="w")
        
        return header

    def _create_grade_header(self, grade: str, subject_count: int) -> ctk.CTkFrame:
        """Crée l'en-tête d'une classe"""
        header = ctk.CTkFrame(self.subjects_area, fg_color=SUCCESS_GREEN, corner_radius=10)
        header.pack_propagate(False)
        header.configure(height=40)
        
        content = ctk.CTkFrame(header, fg_color="transparent")
        content.pack(fill="both", expand=True, padx=PADDING_MEDIUM, pady=PADDING_SMALL)
        
        title = ctk.CTkLabel(content, text=f"{grade} ({subject_count} matière{'s' if subject_count > 1 else ''})",
                            font=FONT_BUTTON, text_color=BG_MAIN)
        title.pack(anchor="w")
        
        return header

    def _create_subject_card(self, subject: Dict) -> ctk.CTkFrame:
        """Crée une carte de matière"""
        card = ctk.CTkFrame(self.subjects_area, fg_color=CARD_BG, corner_radius=16,
                           border_width=1, border_color=BORDER_COLOR, height=120)
        card.pack_propagate(False)
        
        # Barre latérale colorée selon le type
        sidebar_color = SUCCESS_GREEN if subject.get("is_core", True) else WARNING_YELLOW
        sidebar = ctk.CTkFrame(card, fg_color=sidebar_color, corner_radius=16, width=6)
        sidebar.pack(side="left", fill="y", padx=(0, 0), pady=0)
        
        content = ctk.CTkFrame(card, fg_color="transparent")
        content.pack(fill="both", expand=True, padx=PADDING_MEDIUM, pady=PADDING_MEDIUM)
        
        # Nom de la matière
        name_label = ctk.CTkLabel(content, text=subject.get("name", "Sans nom"),
                                 font=FONT_CARD_TITLE, text_color=TEXT_PRIMARY)
        name_label.pack(anchor="w")
        
        # Code et coefficient
        info_text = f"{subject.get('code', '')} • Coeff: {subject.get('coefficient', 1.0)}"
        info_label = ctk.CTkLabel(content, text=info_text,
                                 font=FONT_SECONDARY, text_color=TEXT_SECONDARY)
        info_label.pack(anchor="w", pady=(MARGIN_SMALL, 0))
        
        # Badge optionnel/fondamental
        if subject.get("is_optional", False):
            badge = ctk.CTkLabel(content, text="OPTIONNEL", font=FONT_SECONDARY,
                               text_color=BG_MAIN, fg_color=WARNING_YELLOW,
                               corner_radius=8, height=20)
            badge.pack(anchor="w", pady=(MARGIN_SMALL, 0))
        
        # Effet hover
        def _enter(_):
            card.configure(border_color=ACCENT)
            sidebar.configure(fg_color=ACCENT)
        def _leave(_):
            card.configure(border_color=BORDER_COLOR)
            sidebar.configure(fg_color=sidebar_color)
        
        card.bind("<Enter>", _enter)
        card.bind("<Leave>", _leave)
        
        return card

    def _render_empty_state(self):
        """Affiche l'état vide"""
        empty_frame = ctk.CTkFrame(self.subjects_area, fg_color=CARD_BG, corner_radius=20,
                                  border_width=1, border_color=BORDER_COLOR)
        empty_frame.grid(row=0, column=0, padx=12, pady=12, 
                        sticky="nsew", columnspan=3)
        
        empty_icon = load_ctk_icon("folder.png", (64, 64))
        if empty_icon:
            ctk.CTkLabel(empty_frame, text="", image=empty_icon, 
                        fg_color="transparent").pack(pady=(MARGIN_HERO, MARGIN_LARGE))
        
        ctk.CTkLabel(empty_frame, text="Aucune matière trouvée",
                    font=FONT_SUBTITLE, text_color=TEXT_PRIMARY).pack(pady=(0, MARGIN_SMALL))
        
        ctk.CTkLabel(empty_frame, text="Essayez de modifier vos filtres ou votre recherche",
                    font=FONT_SECONDARY, text_color=TEXT_SECONDARY).pack(pady=(0, MARGIN_LARGE))

    def _show_error_state(self, message: str):
        """Affiche un état d'erreur"""
        for widget in self.subjects_area.winfo_children():
            widget.destroy()
        
        error_frame = ctk.CTkFrame(self.subjects_area, fg_color=ERROR_RED, corner_radius=20)
        error_frame.grid(row=0, column=0, padx=12, pady=12, 
                        sticky="nsew", columnspan=3)
        
        ctk.CTkLabel(error_frame, text="❌ Erreur",
                    font=FONT_SUBTITLE, text_color=BG_MAIN).pack(pady=(MARGIN_LARGE, MARGIN_SMALL))
        
        ctk.CTkLabel(error_frame, text=message,
                    font=FONT_SECONDARY, text_color=BG_MAIN).pack(pady=(0, MARGIN_LARGE))

    def _update_statistics(self):
        """Met à jour les statistiques"""
        try:
            stats = self.controller.get_statistics()
            if stats:
                total = stats.get("total_subjects", 0)
                levels = stats.get("total_levels", 0)
                grades = stats.get("total_grades", 0)
                
                stats_text = f"{total} matières • {levels} niveaux • {grades} classes"
                self.lbl_stats.configure(text=stats_text)
        except Exception as e:
            print(f"❌ Erreur lors de la mise à jour des statistiques : {e}")

    def _update_filter_info(self):
        """Met à jour les informations de filtre"""
        count = len(self.filtered_subjects)
        search_text = self.var_search.get()
        
        if search_text.strip():
            info_text = f"{count} résultat{'s' if count > 1 else ''} pour '{search_text}'"
        else:
            info_text = f"{count} matière{'s' if count > 1 else ''} affichée{'s' if count > 1 else ''}"
        
        self.lbl_filter_info.configure(text=info_text)

    def _on_search_change(self, *_):
        """Gestion du changement de recherche avec debounce"""
        if hasattr(self, "_search_after_id") and self._search_after_id:
            try:
                self.after_cancel(self._search_after_id)
            except:
                pass
        self._search_after_id = self.after(300, self._on_search_change_delayed)

    def _on_search_change_delayed(self):
        """Recherche avec délai"""
        self._search_subjects(self.var_search.get())

    def _on_level_filter_change(self, *_):
        """Gestion du changement de filtre niveau"""
        level = self.var_level_filter.get()
        if level != "Tous les niveaux":
            # Mettre à jour les classes disponibles pour ce niveau
            grades = self.controller.get_available_grades()
            level_grades = [g for g in grades if self.controller.get_education_level_for_grade(g).lower() == level.lower()]
            grade_values = ["Toutes les classes"] + level_grades
            self.grade_combo.configure(values=grade_values)
            self.var_grade_filter.set("Toutes les classes")
        
        self._apply_filters()

    def _on_grade_filter_change(self, *_):
        """Gestion du changement de filtre classe"""
        self._apply_filters()

    def _refresh_data(self):
        """Actualise toutes les données"""
        try:
            self.var_search.set("")
            self.var_level_filter.set("Tous les niveaux")
            self.var_grade_filter.set("Toutes les classes")
            self._load_initial_data()
        except Exception as e:
            print(f"❌ Erreur lors de l'actualisation : {e}")
            messagebox.showerror("Erreur", "Impossible d'actualiser les données")

# Instance globale pour l'utilisation dans l'application
def create_guinean_subjects_view(parent, icons=None):
    """Factory function pour créer la vue des matières guinéennes"""
    return GuineanSubjectsView(parent, icons)
