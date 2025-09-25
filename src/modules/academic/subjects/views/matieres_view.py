# -*- coding: utf-8 -*-
"""
Vue des Matières du Système Éducatif Guinéen - Style Notes
EduManager+ - Interface Adaptée au Style de la Vue des Notes

Cette vue présente les matières organisées selon le système éducatif guinéen
avec une interface similaire à la vue des notes (panneau gauche/droite).
"""

import customtkinter as ctk
from tkinter import messagebox, StringVar, Toplevel
import os
import sys
from PIL import Image
from CTkTable import CTkTable
from datetime import datetime
from typing import List, Dict, Optional

# Ajouter le chemin du projet pour les imports
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../../..'))
if project_root not in sys.path:
    sys.path.append(project_root)

from src.modules.academic.subjects.controllers.guinean_subjects_controller import get_guinean_subjects_controller
from src.modules.academic.classes.controllers.classe_controller import get_all_classes

# Import du thème global
try:
    from resources.themes.theme import *
    print("✅ Thème global EduManager+ importé pour les matières guinéennes")
except ImportError as e:
    print(f"⚠️ Thème global non trouvé: {e}")
    # Thème de fallback
    BG_MAIN = "#233146"
    BG_CARD = "#2b2952"
    TEXT_PRIMARY = "#E0E6F0"
    TEXT_SECONDARY = "#AAB5C6"
    TEXT_ACCENT = "#64FFDA"
    BORDER_COLOR = "#40546c"
    SUCCESS_GREEN = "#A0E7E5"
    WARNING_YELLOW = "#FFD700"
    ERROR_RED = "#FF6363"
    ACCENT = "#64FFDA"
    BG_SIDEBAR = "#1E2332"
    MARGIN_SMALL = 8
    MARGIN_MEDIUM = 12
    MARGIN_LARGE = 20
    FONT = "Segoe UI"
    FONT_SIZE_TITLE = 24
    FONT_SIZE_HEADER = 18
    FONT_SIZE_TEXT = 14
    FONT_SIZE_SMALL = 12

ICON_MAP = {
    "add": "add.png", "edit": "edit.png", "delete": "delete.png",
    "refresh": "refresh.png", "search": "search.png", "close": "close.png",
    "book": "book.png", "subject": "stacks.png", "stats": "analytics.png",
    "grade": "grade.png", "class": "classroom.png", "sort": "sort.png"
}

def load_ctk_icon(icon_name, size=(20, 20)):
    """Charge une icône pour CustomTkinter"""
    try:
        from PIL import Image
        # Chemin vers les icônes dans resources/icons
        current_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(current_dir)))))
        icon_path = os.path.join(project_root, "resources", "icons", icon_name)
        
        if os.path.exists(icon_path):
            image = Image.open(icon_path).resize(size, Image.Resampling.LANCZOS)
            return ctk.CTkImage(light_image=image, dark_image=image)
        else:
            return None
    except Exception as e:
        print(f"⚠️ Erreur chargement icône {icon_name}: {e}")
        return None

class MatieresView(ctk.CTkFrame):
    """Vue des matières adaptée au style de la vue des notes"""

    def __init__(self, parent, icons=None):
        super().__init__(parent, fg_color=BG_MAIN)
        self.icons = icons
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        # Variables pour la sélection
        self.selected_level = None
        self.selected_grade = None
        self.selected_subjects = []
        
        # Cache pour optimiser les performances
        self._data_cache = {}
        self._cache_timestamp = 0
        self._cache_duration = 30  # Cache valide pendant 30 secondes
        
        print("🚀 Chargement des données MatieresView...")
        
        # Chargement initial des données avec cache
        self._load_cached_data()
        
        print("✅ Données MatieresView chargées")
        self._build_main_ui()

    def _load_cached_data(self):
        """Charge les données avec système de cache pour optimiser les performances"""
        import time
        current_time = time.time()
        
        # Vérifier si le cache est encore valide
        if (current_time - self._cache_timestamp) < self._cache_duration and self._data_cache:
            print("📋 Utilisation du cache pour les données")
            self.subjects = self._data_cache.get('subjects', [])
            self.grades = self._data_cache.get('grades', [])
            self.levels = self._data_cache.get('levels', [])
            return
        
        print("🔄 Chargement des données depuis la base...")
        try:
            # Chargement progressif pour éviter le blocage
            self._load_data_progressively()
            
        except Exception as e:
            print(f"⚠️ Erreur chargement données: {e}")
            # Fallback avec données vides
            self.subjects = []
            self.grades = []
            self.levels = []
    
    def _load_data_progressively(self):
        """Charge les données de manière progressive pour éviter le blocage"""
        import time
        
        # Initialiser le contrôleur
        self.controller = get_guinean_subjects_controller()
        
        # Charger les vraies classes depuis la base de données
        print("🏫 Chargement des vraies classes...")
        real_classes = get_all_classes()
        self.classes = {cls['nom']: cls for cls in real_classes}
        
        # Extraire les niveaux uniques des vraies classes
        self.levels = list(set([cls['niveau'] for cls in real_classes]))
        print(f"✅ {len(self.levels)} niveaux d'éducation chargés: {self.levels}")
        
        # Extraire les noms des classes
        self.grades = [cls['nom'] for cls in real_classes]
        print(f"✅ {len(self.grades)} vraies classes chargées: {self.grades[:10]}...")
        
        # Charger toutes les matières
        print("📖 Chargement des matières...")
        self.subjects = self.controller.get_all_subjects()
        print(f"✅ {len(self.subjects)} matières chargées")
        
        # Mise à jour du cache
        self._data_cache = {
            'subjects': self.subjects,
            'grades': self.grades,
            'levels': self.levels,
            'classes': self.classes
        }
        self._cache_timestamp = time.time()
        
        print(f"✅ Données chargées: {len(self.subjects)} matières, {len(self.grades)} vraies classes, {len(self.levels)} niveaux")

    def _refresh_all(self):
        """Rafraîchit toutes les données en invalidant le cache"""
        print("🔄 Rafraîchissement des données...")
        self._cache_timestamp = 0  # Invalider le cache
        self._load_cached_data()
        
        self.selected_level = None
        self.selected_grade = None
        self.selected_subjects = []
        
        self._setup_level_dropdown()
        self._setup_grade_dropdown()
        self._clear_subjects_table()
        self._update_subjects_table()
        self._update_stats()

    def _setup_level_dropdown(self):
        """Configure le dropdown des niveaux"""
        try:
            if hasattr(self, 'level_dropdown'):
                level_options = ["Tous les niveaux"] + self.levels
                self.level_dropdown.configure(values=level_options)
                self.level_dropdown.set("Tous les niveaux")
        except Exception as e:
            print(f"❌ Erreur configuration niveau dropdown: {e}")

    def _setup_grade_dropdown(self):
        """Configure le dropdown des classes"""
        try:
            if hasattr(self, 'grade_dropdown'):
                grade_options = ["Toutes les classes"] + self.grades
                self.grade_dropdown.configure(values=grade_options)
                self.grade_dropdown.set("Toutes les classes")
        except Exception as e:
            print(f"❌ Erreur configuration classe dropdown: {e}")
        
    def _build_main_ui(self):
        """Construit l'interface principale avec panneau gauche et droite"""
        main_frame = ctk.CTkFrame(self, fg_color=BG_MAIN)
        main_frame.pack(fill="both", expand=True, padx=15, pady=15)
        main_frame.grid_columnconfigure(1, weight=3)
        main_frame.grid_columnconfigure(0, weight=1)
        main_frame.grid_rowconfigure(0, weight=1)

        # Panneau de gauche: Sélection par niveau et classe
        left_panel = ctk.CTkFrame(main_frame, fg_color=BG_CARD, corner_radius=12)
        left_panel.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        left_panel.grid_columnconfigure(0, weight=1)
        left_panel.grid_rowconfigure(2, weight=1)
        
        self._build_selection_panel(left_panel)
        
        # Panneau de droite: Tableau des matières et statistiques
        right_panel = ctk.CTkFrame(main_frame, fg_color=BG_MAIN)
        right_panel.grid(row=0, column=1, sticky="nsew", padx=(10, 0))
        right_panel.grid_columnconfigure(0, weight=1)
        right_panel.grid_rowconfigure(0, weight=1)
        right_panel.grid_rowconfigure(1, weight=4)
        
        self._build_subjects_dashboard(right_panel)

    def _build_selection_panel(self, parent_frame):
        """Construit le panneau de sélection (gauche) avec design moderne"""
        # Header avec gradient et icônes
        header_frame = ctk.CTkFrame(parent_frame, fg_color=ACCENT, corner_radius=12)
        header_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=(10, 15))
        header_frame.grid_columnconfigure(0, weight=1)
        
        # Titre avec icône et style moderne
        title_frame = ctk.CTkFrame(header_frame, fg_color=ACCENT)
        title_frame.grid(row=0, column=0, sticky="w", padx=15, pady=15)
        
        subject_icon = load_ctk_icon(ICON_MAP.get("subject"), size=(24, 24))
        if subject_icon:
            ctk.CTkLabel(title_frame, text="", image=subject_icon, fg_color=ACCENT).pack(side="left", padx=(0, 10))
        
        ctk.CTkLabel(title_frame, text="MATIÈRES", 
                      font=(FONT, FONT_SIZE_HEADER, "bold"),
                      text_color=BG_MAIN, fg_color=ACCENT).pack(side="left")
        
        # Bouton refresh moderne
        refresh_icon = load_ctk_icon(ICON_MAP.get("refresh"), size=(18, 18))
        refresh_btn = ctk.CTkButton(header_frame, text="", image=refresh_icon, width=40, height=40,
                      fg_color=BG_MAIN, hover_color=TEXT_SECONDARY,
                      text_color=TEXT_PRIMARY, corner_radius=20,
                      command=self._refresh_all)
        refresh_btn.grid(row=0, column=1, sticky="e", padx=15, pady=15)
        
        # Section des filtres avec design moderne
        filters_section = ctk.CTkFrame(parent_frame, fg_color=BG_CARD, corner_radius=12)
        filters_section.grid(row=1, column=0, sticky="ew", padx=10, pady=5)
        filters_section.grid_columnconfigure(0, weight=1)
        
        # Titre de la section filtres
        filters_title = ctk.CTkLabel(filters_section, text="FILTRES", 
                                   font=(FONT, FONT_SIZE_TEXT, "bold"),
                                   text_color=TEXT_ACCENT, fg_color=BG_CARD)
        filters_title.grid(row=0, column=0, sticky="w", padx=15, pady=(15, 10))
        
        # Sélection par niveau avec style moderne
        level_frame = ctk.CTkFrame(filters_section, fg_color=BG_CARD)
        level_frame.grid(row=1, column=0, sticky="ew", padx=15, pady=5)
        level_frame.grid_columnconfigure(0, weight=1)
        
        level_label = ctk.CTkLabel(level_frame, text="Niveau d'Éducation:", 
                                  font=(FONT, FONT_SIZE_SMALL, "bold"), 
                                  text_color=TEXT_PRIMARY, fg_color=BG_CARD)
        level_label.grid(row=0, column=0, sticky="w", padx=(0, 5), pady=(10, 5))
        
        level_options = ["Tous les niveaux"] + self.levels
        self.level_dropdown = ctk.CTkComboBox(
            level_frame, values=level_options,
            command=self._on_level_selected,
            font=(FONT, FONT_SIZE_TEXT),
            fg_color=BG_MAIN,
            dropdown_fg_color=BG_CARD,
            dropdown_hover_color=ACCENT,
            text_color=TEXT_PRIMARY,
            button_color=ACCENT,
            button_hover_color=SUCCESS_GREEN,
            border_color=ACCENT,
            border_width=2,
            corner_radius=10,
            state="readonly"
        )
        self.level_dropdown.grid(row=1, column=0, sticky="ew", padx=0, pady=(0, 15))
        self.level_dropdown.set("Tous les niveaux")
        
        # Sélection par classe avec style moderne
        grade_frame = ctk.CTkFrame(filters_section, fg_color=BG_CARD)
        grade_frame.grid(row=2, column=0, sticky="ew", padx=15, pady=5)
        grade_frame.grid_columnconfigure(0, weight=1)
        
        grade_label = ctk.CTkLabel(grade_frame, text="Classe:", 
                                  font=(FONT, FONT_SIZE_SMALL, "bold"), 
                                  text_color=TEXT_PRIMARY, fg_color=BG_CARD)
        grade_label.grid(row=0, column=0, sticky="w", padx=(0, 5), pady=(10, 5))
        
        grade_options = ["Toutes les classes"] + self.grades
        self.grade_dropdown = ctk.CTkComboBox(
            grade_frame, values=grade_options,
            command=self._on_grade_selected,
            font=(FONT, FONT_SIZE_TEXT),
            fg_color=BG_MAIN,
            dropdown_fg_color=BG_CARD,
            dropdown_hover_color=ACCENT,
            text_color=TEXT_PRIMARY,
            button_color=ACCENT,
            button_hover_color=SUCCESS_GREEN,
            border_color=ACCENT,
            border_width=2,
            corner_radius=10,
            state="readonly"
        )
        self.grade_dropdown.grid(row=1, column=0, sticky="ew", padx=0, pady=(0, 15))
        self.grade_dropdown.set("Toutes les classes")
        
        # Section des actions rapides
        actions_section = ctk.CTkFrame(parent_frame, fg_color=BG_CARD, corner_radius=12)
        actions_section.grid(row=3, column=0, sticky="ew", padx=10, pady=5)
        actions_section.grid_columnconfigure(0, weight=1)
        actions_section.grid_columnconfigure(1, weight=1)
        
        # Titre de la section actions
        actions_title = ctk.CTkLabel(actions_section, text="ACTIONS RAPIDES", 
                                    font=(FONT, FONT_SIZE_TEXT, "bold"),
                                    text_color=TEXT_ACCENT, fg_color=BG_CARD)
        actions_title.grid(row=0, column=0, columnspan=2, sticky="w", padx=15, pady=(15, 10))
        
        # Bouton Ajouter
        add_icon = load_ctk_icon(ICON_MAP.get("add"), size=(16, 16))
        add_btn = ctk.CTkButton(actions_section, text="Ajouter", image=add_icon,
                               font=(FONT, FONT_SIZE_SMALL), fg_color=SUCCESS_GREEN,
                               hover_color="#059669", text_color=BG_MAIN,
                               corner_radius=10, height=35,
                               command=self._add_subject)
        add_btn.grid(row=1, column=0, sticky="ew", padx=(15, 5), pady=(0, 10))
        
        # Bouton Rechercher
        search_icon = load_ctk_icon(ICON_MAP.get("search"), size=(16, 16))
        search_btn = ctk.CTkButton(actions_section, text="Rechercher", image=search_icon,
                                  font=(FONT, FONT_SIZE_SMALL), fg_color=ACCENT,
                                  hover_color="#4DD0E1", text_color=BG_MAIN,
                                  corner_radius=10, height=35,
                                  command=self._show_search_dialog)
        search_btn.grid(row=1, column=1, sticky="ew", padx=(5, 15), pady=(0, 10))
        
        # Statistiques rapides avec design moderne
        stats_section = ctk.CTkFrame(parent_frame, fg_color=BG_CARD, corner_radius=12)
        stats_section.grid(row=4, column=0, sticky="ew", padx=10, pady=5)
        stats_section.grid_columnconfigure(0, weight=1)
        
        # Titre de la section stats
        stats_title = ctk.CTkLabel(stats_section, text="STATISTIQUES", 
                                  font=(FONT, FONT_SIZE_TEXT, "bold"),
                                  text_color=TEXT_ACCENT, fg_color=BG_CARD)
        stats_title.grid(row=0, column=0, sticky="w", padx=15, pady=(15, 10))
        
        self.stats_label = ctk.CTkLabel(stats_section, text="Chargement des statistiques...",
                                       font=(FONT, FONT_SIZE_SMALL), text_color=TEXT_SECONDARY, fg_color=BG_CARD)
        self.stats_label.grid(row=1, column=0, sticky="ew", padx=15, pady=(0, 15))
        
        self._update_stats()

    def _build_subjects_dashboard(self, parent_frame):
        """Construit le tableau de bord des matières (droite)"""
        # En-tête avec actions
        header_frame = ctk.CTkFrame(parent_frame, fg_color=BG_CARD, corner_radius=12)
        header_frame.grid(row=0, column=0, sticky="ew", padx=0, pady=(0, 10))
        header_frame.grid_columnconfigure(1, weight=1)
        header_frame.grid_rowconfigure(0, weight=1)
        
        # Titre du tableau
        title_frame = ctk.CTkFrame(header_frame, fg_color=BG_CARD)
        title_frame.grid(row=0, column=0, sticky="w", padx=15, pady=15)
        
        book_icon = load_ctk_icon(ICON_MAP.get("book"), size=(20, 20))
        ctk.CTkLabel(title_frame, text="", image=book_icon, fg_color=BG_CARD).pack(side="left", padx=(0, 8))
        ctk.CTkLabel(title_frame, text="TABLEAU DES MATIÈRES", 
                      font=(FONT, FONT_SIZE_HEADER, "bold"),
                      text_color=TEXT_PRIMARY, fg_color=BG_CARD).pack(side="left")
        
        # Boutons d'action
        actions_frame = ctk.CTkFrame(header_frame, fg_color=BG_CARD)
        actions_frame.grid(row=0, column=1, sticky="e", padx=15, pady=15)
        
        add_icon = load_ctk_icon(ICON_MAP.get("add"), size=(16, 16))
        ctk.CTkButton(actions_frame, text="Ajouter", image=add_icon,
                      font=(FONT, FONT_SIZE_TEXT), fg_color=SUCCESS_GREEN,
                      hover_color="#059669", text_color=BG_MAIN,
                      command=self._add_subject).pack(side="right", padx=(5, 0))
        
        # Zone du tableau des matières
        table_frame = ctk.CTkFrame(parent_frame, fg_color=BG_CARD, corner_radius=12)
        table_frame.grid(row=1, column=0, sticky="nsew", padx=0, pady=0)
        table_frame.grid_columnconfigure(0, weight=1)
        table_frame.grid_rowconfigure(0, weight=1)
        
        # En-têtes du tableau
        headers = ["Code", "Matière", "Niveau", "Classe", "Coefficient", "Type"]
        
        # Données initiales (toutes les matières)
        table_data = [headers]
        for subject in self.subjects[:20]:  # Limiter à 20 pour les performances
            # Mapper le niveau et la classe
            level = self._map_subject_level(subject)
            grade = self._map_subject_grade(subject)
            
            row = [
                subject.get("code", ""),
                subject.get("name", ""),
                level,
                grade,
                str(subject.get("coefficient", 1.0)),
                "Fondamentale" if subject.get("is_core", True) else "Optionnelle"
            ]
            table_data.append(row)
        
        # Créer le tableau
        self.subjects_table = CTkTable(
            master=table_frame,
            row=len(table_data),
            column=len(headers),
            values=table_data,
            header_color=BORDER_COLOR,
            colors=["#2b2952", "#233146"],
            hover_color=BORDER_COLOR,
            text_color=TEXT_PRIMARY,
            font=(FONT, FONT_SIZE_SMALL),
            corner_radius=8,
            border_width=1,
            border_color=BORDER_COLOR
        )
        
        self.subjects_table.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Configurer la sélection de ligne
        self.subjects_table.bind("<Button-1>", self._on_table_select)

    def _setup_level_dropdown(self):
        """Configure le dropdown des niveaux"""
        level_options = ["Tous les niveaux"] + self.levels
        self.level_dropdown.configure(values=level_options)
        self.level_dropdown.set("Tous les niveaux")

    def _setup_grade_dropdown(self):
        """Configure le dropdown des classes"""
        grade_options = ["Toutes les classes"] + self.grades
        self.grade_dropdown.configure(values=grade_options)
        self.grade_dropdown.set("Toutes les classes")

    def _on_level_selected(self, selected_level):
        """Gestionnaire de sélection de niveau"""
        self.selected_level = selected_level if selected_level != "Tous les niveaux" else None
        self._filter_subjects()

    def _on_grade_selected(self, selected_grade):
        """Gestionnaire de sélection de classe"""
        self.selected_grade = selected_grade if selected_grade != "Toutes les classes" else None
        self._filter_subjects()

    def _filter_subjects(self):
        """Filtre les matières selon les sélections"""
        try:
            if self.selected_level and self.selected_grade:
                # Filtrer par niveau et classe réelle
                filtered = [s for s in self.subjects 
                           if s.get("education_level", "").lower() == self.selected_level.lower()
                           and s.get("grade", "") == self.selected_grade]
            elif self.selected_level:
                # Filtrer par niveau seulement - mapper les niveaux
                level_mapping = {
                    'primaire': ['1°', '2°', '3°', '4°', '5°', '6°'],
                    'college': ['7°', '8°', '9°', '10°'],
                    'lycee': ['11° SE', '11° SM', '11° SS', '12° SE', '12° SM', '12° SS'],
                    'terminale': ['TSE', 'TSM', 'TSS']
                }
                
                if self.selected_level.lower() in level_mapping:
                    target_classes = level_mapping[self.selected_level.lower()]
                    filtered = [s for s in self.subjects 
                               if s.get("grade", "") in target_classes]
                else:
                    filtered = [s for s in self.subjects 
                               if s.get("education_level", "").lower() == self.selected_level.lower()]
            elif self.selected_grade:
                # Filtrer par classe réelle seulement
                filtered = [s for s in self.subjects 
                           if s.get("grade", "") == self.selected_grade]
            else:
                # Aucun filtre - montrer toutes les matières
                filtered = self.subjects
            
            self.selected_subjects = filtered
            self._update_subjects_table()
            self._update_stats()
            
        except Exception as e:
            print(f"❌ Erreur lors du filtrage : {e}")

    def _update_subjects_table(self):
        """Met à jour le tableau des matières"""
        try:
            # En-têtes du tableau
            headers = ["Code", "Matière", "Niveau", "Classe", "Coefficient", "Type"]
            
            # Données filtrées
            table_data = [headers]
            for subject in self.selected_subjects[:50]:  # Limiter à 50 pour les performances
                # Mapper le niveau et la classe
                level = self._map_subject_level(subject)
                grade = self._map_subject_grade(subject)
                
                row = [
                    subject.get("code", ""),
                    subject.get("name", ""),
                    level,
                    grade,
                    str(subject.get("coefficient", 1.0)),
                    "Fondamentale" if subject.get("is_core", True) else "Optionnelle"
                ]
                table_data.append(row)
            
            # Mettre à jour le tableau
            self.subjects_table.update_values(table_data)
            
        except Exception as e:
            print(f"❌ Erreur lors de la mise à jour du tableau : {e}")

    def _update_stats(self):
        """Met à jour les statistiques affichées"""
        try:
            total_subjects = len(self.selected_subjects) if self.selected_subjects else len(self.subjects)
            core_subjects = len([s for s in (self.selected_subjects or self.subjects) if s.get("is_core", True)])
            optional_subjects = total_subjects - core_subjects
            
            stats_text = f"📊 {total_subjects} matières • {core_subjects} fondamentales • {optional_subjects} optionnelles"
            self.stats_label.configure(text=stats_text)
            
        except Exception as e:
            print(f"❌ Erreur lors de la mise à jour des stats : {e}")

    def _clear_subjects_table(self):
        """Vide le tableau des matières"""
        try:
            headers = ["Code", "Matière", "Niveau", "Classe", "Coefficient", "Type"]
            empty_data = [headers]
            self.subjects_table.update_values(empty_data)
        except Exception as e:
            print(f"❌ Erreur lors du vidage du tableau : {e}")

    def _on_table_select(self, event):
        """Gestionnaire de sélection dans le tableau"""
        try:
            # Récupérer la ligne sélectionnée
            selected_row = self.subjects_table.get_selected_row()
            if selected_row and selected_row > 0:  # Ignorer l'en-tête
                print(f"📖 Matière sélectionnée: ligne {selected_row}")
        except Exception as e:
            print(f"❌ Erreur lors de la sélection : {e}")

    def _map_subject_level(self, subject):
        """Mappe le niveau d'éducation d'une matière vers les vrais niveaux"""
        original_level = subject.get("education_level", "").lower()
        original_grade = subject.get("grade", "")
        
        # Mapping des niveaux fictifs vers les vrais niveaux
        if original_level == "primaire" or original_grade in ["CP1", "CP2", "CE1", "CE2", "CM1", "CM2"]:
            return "Primaire"
        elif original_level == "college" or "ème" in original_grade:
            return "Collège"
        elif original_level == "lycee" or "Sciences" in original_grade:
            return "Lycée"
        else:
            return original_level.title() if original_level else "Non défini"
    
    def _map_subject_grade(self, subject):
        """Mappe la classe d'une matière vers les vraies classes"""
        original_grade = subject.get("grade", "")
        
        # Mapping des classes fictives vers les vraies classes
        grade_mapping = {
            # Primaire
            "CP1": "1°", "CP2": "2°", "CE1": "3°", "CE2": "4°", "CM1": "5°", "CM2": "6°",
            # Collège
            "7ème": "7°", "8ème": "8°", "9ème": "9°", "10ème": "10°",
            # Lycée
            "11ème Sciences Mathématiques": "11° SM",
            "12ème Sciences Mathématiques": "12° SM",
            "11ème Sciences Expérimentales": "11° SE",
            "12ème Sciences Expérimentales": "12° SE",
            "11ème Lettres / Sciences Sociales": "11° SS",
            "12ème Lettres / Sciences Sociales": "12° SS",
            # Terminale
            "Terminale Sciences Mathématiques": "TSM",
            "Terminale Sciences Expérimentales": "TSE",
            "Terminale Lettres / Sciences Sociales": "TSS"
        }
        
        # Vérifier si c'est déjà une vraie classe
        if original_grade in ["1°", "2°", "3°", "4°", "5°", "6°", "7°", "8°", "9°", "10°", 
                             "11° SE", "11° SM", "11° SS", "12° SE", "12° SM", "12° SS",
                             "TSE", "TSM", "TSS"]:
            return original_grade
        
        # Mapper si possible
        return grade_mapping.get(original_grade, original_grade)

    def _add_subject(self):
        """Ouvre le formulaire d'ajout de matière"""
        self._open_subject_form()
    
    def _open_subject_form(self, subject_data=None):
        """Ouvre le formulaire d'ajout/modification de matière avec design amélioré"""
        # Créer une fenêtre modale
        form_window = ctk.CTkToplevel(self)
        form_window.title("Ajouter une Matière" if not subject_data else "Modifier la Matière")
        form_window.geometry("600x700")
        form_window.resizable(False, False)
        form_window.transient(self)
        form_window.grab_set()
        
        # Centrer la fenêtre
        form_window.update_idletasks()
        x = (form_window.winfo_screenwidth() // 2) - (600 // 2)
        y = (form_window.winfo_screenheight() // 2) - (700 // 2)
        form_window.geometry(f"600x700+{x}+{y}")
        
        # Frame principal avec scroll
        main_frame = ctk.CTkScrollableFrame(form_window, fg_color=BG_CARD, corner_radius=12)
        main_frame.pack(fill="both", expand=True, padx=15, pady=15)
        
        # En-tête avec design moderne
        header_frame = ctk.CTkFrame(main_frame, fg_color=ACCENT, corner_radius=12)
        header_frame.pack(fill="x", pady=(0, 20))
        
        # Titre avec icône
        title_frame = ctk.CTkFrame(header_frame, fg_color=ACCENT)
        title_frame.pack(expand=True, fill="x", padx=20, pady=15)
        
        # Icône du formulaire
        add_icon = load_ctk_icon(ICON_MAP.get("add"), size=(24, 24))
        if add_icon:
            ctk.CTkLabel(title_frame, text="", image=add_icon, fg_color=ACCENT).pack(side="left", padx=(0, 10))
        else:
            ctk.CTkLabel(title_frame, text="📚", font=(FONT, 24), 
                        text_color=BG_MAIN, fg_color=ACCENT).pack(side="left", padx=(0, 10))
        
        title_text = "➕ NOUVELLE MATIÈRE" if not subject_data else "✏️ MODIFIER MATIÈRE"
        title = ctk.CTkLabel(title_frame, text=title_text,
                            font=(FONT, FONT_SIZE_HEADER, "bold"),
                            text_color=BG_MAIN, fg_color=ACCENT)
        title.pack(side="left")
        
        # Formulaire avec sections organisées
        form_frame = ctk.CTkFrame(main_frame, fg_color=BG_CARD)
        form_frame.pack(fill="both", expand=True)
        
        # Variables du formulaire
        var_name = ctk.StringVar(value=subject_data.get("name", "") if subject_data else "")
        var_code = ctk.StringVar(value=subject_data.get("code", "") if subject_data else "")
        var_description = ctk.StringVar(value=subject_data.get("description", "") if subject_data else "")
        var_coefficient = ctk.StringVar(value=str(subject_data.get("coefficient", 1.0)) if subject_data else "1.0")
        var_level = ctk.StringVar(value=subject_data.get("education_level", "") if subject_data else "")
        var_grade = ctk.StringVar(value=subject_data.get("grade", "") if subject_data else "")
        var_is_core = ctk.BooleanVar(value=subject_data.get("is_core", True) if subject_data else True)
        var_is_optional = ctk.BooleanVar(value=subject_data.get("is_optional", False) if subject_data else False)
        
        # Section 1: Informations de base
        basic_section = ctk.CTkFrame(form_frame, fg_color=BG_CARD, corner_radius=8)
        basic_section.pack(fill="x", padx=15, pady=(15, 10))
        
        basic_title = ctk.CTkLabel(basic_section, text="📝 INFORMATIONS DE BASE",
                                  font=(FONT, FONT_SIZE_TEXT, "bold"),
                                  text_color=TEXT_ACCENT, fg_color=BG_CARD)
        basic_title.pack(anchor="w", padx=15, pady=(15, 10))
        
        # Nom de la matière
        name_frame = ctk.CTkFrame(basic_section, fg_color=BG_CARD)
        name_frame.pack(fill="x", padx=15, pady=5)
        name_frame.grid_columnconfigure(1, weight=1)
        
        ctk.CTkLabel(name_frame, text="Nom de la matière:", 
                     font=(FONT, FONT_SIZE_TEXT, "bold"), 
                     text_color=TEXT_PRIMARY, fg_color=BG_CARD).grid(row=0, column=0, sticky="w", padx=(0, 10))
        name_entry = ctk.CTkEntry(name_frame, textvariable=var_name, 
                                 font=(FONT, FONT_SIZE_TEXT), fg_color=BG_MAIN,
                                 text_color=TEXT_PRIMARY, border_color=BORDER_COLOR,
                                 placeholder_text="Ex: Mathématiques", height=35)
        name_entry.grid(row=0, column=1, sticky="ew", padx=(0, 0))
        
        # Code de la matière
        code_frame = ctk.CTkFrame(basic_section, fg_color=BG_CARD)
        code_frame.pack(fill="x", padx=15, pady=5)
        code_frame.grid_columnconfigure(1, weight=1)
        
        ctk.CTkLabel(code_frame, text="Code de la matière:", 
                     font=(FONT, FONT_SIZE_TEXT, "bold"), 
                     text_color=TEXT_PRIMARY, fg_color=BG_CARD).grid(row=0, column=0, sticky="w", padx=(0, 10))
        code_entry = ctk.CTkEntry(code_frame, textvariable=var_code, 
                                 font=(FONT, FONT_SIZE_TEXT), fg_color=BG_MAIN,
                                 text_color=TEXT_PRIMARY, border_color=BORDER_COLOR,
                                 placeholder_text="Ex: MATH", height=35)
        code_entry.grid(row=0, column=1, sticky="ew", padx=(0, 0))
        
        # Coefficient
        coeff_frame = ctk.CTkFrame(basic_section, fg_color=BG_CARD)
        coeff_frame.pack(fill="x", padx=15, pady=5)
        coeff_frame.grid_columnconfigure(1, weight=1)
        
        ctk.CTkLabel(coeff_frame, text="Coefficient:", 
                     font=(FONT, FONT_SIZE_TEXT, "bold"), 
                     text_color=TEXT_PRIMARY, fg_color=BG_CARD).grid(row=0, column=0, sticky="w", padx=(0, 10))
        coeff_entry = ctk.CTkEntry(coeff_frame, textvariable=var_coefficient, 
                                  font=(FONT, FONT_SIZE_TEXT), fg_color=BG_MAIN,
                                  text_color=TEXT_PRIMARY, border_color=BORDER_COLOR,
                                  placeholder_text="Ex: 4.0", height=35)
        coeff_entry.grid(row=0, column=1, sticky="ew", padx=(0, 0))
        
        # Description
        desc_frame = ctk.CTkFrame(basic_section, fg_color=BG_CARD)
        desc_frame.pack(fill="x", padx=15, pady=(5, 15))
        
        ctk.CTkLabel(desc_frame, text="Description:", 
                     font=(FONT, FONT_SIZE_TEXT, "bold"), 
                     text_color=TEXT_PRIMARY, fg_color=BG_CARD).pack(anchor="w", padx=15, pady=(15, 5))
        desc_entry = ctk.CTkTextbox(desc_frame, height=80, 
                                   font=(FONT, FONT_SIZE_TEXT), fg_color=BG_MAIN,
                                   text_color=TEXT_PRIMARY, border_color=BORDER_COLOR,
                                   corner_radius=8)
        desc_entry.pack(fill="x", padx=15, pady=(0, 15))
        if var_description.get():
            desc_entry.insert("1.0", var_description.get())
        
        # Section 2: Classification
        class_section = ctk.CTkFrame(form_frame, fg_color=BG_CARD, corner_radius=8)
        class_section.pack(fill="x", padx=15, pady=10)
        
        class_title = ctk.CTkLabel(class_section, text="🎓 CLASSIFICATION",
                                  font=(FONT, FONT_SIZE_TEXT, "bold"),
                                  text_color=TEXT_ACCENT, fg_color=BG_CARD)
        class_title.pack(anchor="w", padx=15, pady=(15, 10))
        
        # Niveau d'éducation
        level_frame = ctk.CTkFrame(class_section, fg_color=BG_CARD)
        level_frame.pack(fill="x", padx=15, pady=5)
        level_frame.grid_columnconfigure(1, weight=1)
        
        ctk.CTkLabel(level_frame, text="Niveau d'éducation:", 
                     font=(FONT, FONT_SIZE_TEXT, "bold"), 
                     text_color=TEXT_PRIMARY, fg_color=BG_CARD).grid(row=0, column=0, sticky="w", padx=(0, 10))
        level_combo = ctk.CTkComboBox(level_frame, values=["Primaire", "Collège", "Lycée", "Terminale"],
                                     variable=var_level, font=(FONT, FONT_SIZE_TEXT),
                                     fg_color=BG_MAIN, text_color=TEXT_PRIMARY,
                                     border_color=BORDER_COLOR, dropdown_fg_color=BG_CARD,
                                     button_color=ACCENT, button_hover_color=SUCCESS_GREEN,
                                     height=35, corner_radius=8)
        level_combo.grid(row=0, column=1, sticky="ew", padx=(0, 0))
        
        # Classe
        grade_frame = ctk.CTkFrame(class_section, fg_color=BG_CARD)
        grade_frame.pack(fill="x", padx=15, pady=(5, 15))
        grade_frame.grid_columnconfigure(1, weight=1)
        
        ctk.CTkLabel(grade_frame, text="Classe:", 
                     font=(FONT, FONT_SIZE_TEXT, "bold"), 
                     text_color=TEXT_PRIMARY, fg_color=BG_CARD).grid(row=0, column=0, sticky="w", padx=(0, 10))
        grade_combo = ctk.CTkComboBox(grade_frame, values=self.grades,
                                     variable=var_grade, font=(FONT, FONT_SIZE_TEXT),
                                     fg_color=BG_MAIN, text_color=TEXT_PRIMARY,
                                     border_color=BORDER_COLOR, dropdown_fg_color=BG_CARD,
                                     button_color=ACCENT, button_hover_color=SUCCESS_GREEN,
                                     height=35, corner_radius=8)
        grade_combo.grid(row=0, column=1, sticky="ew", padx=(0, 0))
        
        # Section 3: Options
        options_section = ctk.CTkFrame(form_frame, fg_color=BG_CARD, corner_radius=8)
        options_section.pack(fill="x", padx=15, pady=10)
        
        options_title = ctk.CTkLabel(options_section, text="⚙️ OPTIONS",
                                    font=(FONT, FONT_SIZE_TEXT, "bold"),
                                    text_color=TEXT_ACCENT, fg_color=BG_CARD)
        options_title.pack(anchor="w", padx=15, pady=(15, 10))
        
        options_frame = ctk.CTkFrame(options_section, fg_color=BG_CARD)
        options_frame.pack(fill="x", padx=15, pady=(0, 15))
        
        ctk.CTkCheckBox(options_frame, text="Matière fondamentale", variable=var_is_core,
                       font=(FONT, FONT_SIZE_TEXT, "bold"), text_color=TEXT_PRIMARY,
                       fg_color=SUCCESS_GREEN, hover_color="#059669",
                       checkmark_color=BG_MAIN, corner_radius=6).pack(anchor="w", padx=15, pady=8)
        
        ctk.CTkCheckBox(options_frame, text="Matière optionnelle", variable=var_is_optional,
                       font=(FONT, FONT_SIZE_TEXT, "bold"), text_color=TEXT_PRIMARY,
                       fg_color=WARNING_YELLOW, hover_color="#D97706",
                       checkmark_color=BG_MAIN, corner_radius=6).pack(anchor="w", padx=15, pady=8)
        
        # Boutons avec design moderne
        buttons_frame = ctk.CTkFrame(form_frame, fg_color=BG_CARD)
        buttons_frame.pack(fill="x", padx=15, pady=(10, 15))
        buttons_frame.grid_columnconfigure(0, weight=1)
        buttons_frame.grid_columnconfigure(1, weight=1)
        
        cancel_btn = ctk.CTkButton(buttons_frame, text="❌ Annuler", 
                                  font=(FONT, FONT_SIZE_TEXT, "bold"), 
                                  fg_color=ERROR_RED, hover_color="#DC2626", 
                                  text_color=BG_MAIN, height=40, corner_radius=10,
                                  command=form_window.destroy)
        cancel_btn.grid(row=0, column=0, sticky="ew", padx=(0, 5))
        
        save_btn = ctk.CTkButton(buttons_frame, text="✅ Enregistrer", 
                                font=(FONT, FONT_SIZE_TEXT, "bold"), 
                                fg_color=SUCCESS_GREEN, hover_color="#059669", 
                                text_color=BG_MAIN, height=40, corner_radius=10,
                                command=lambda: self._save_subject(form_window, var_name, var_code, 
                                                                desc_entry, var_coefficient, var_level, 
                                                                var_grade, var_is_core, var_is_optional, subject_data))
        save_btn.grid(row=0, column=1, sticky="ew", padx=(5, 0))
    
    def _save_subject(self, window, var_name, var_code, desc_entry, var_coefficient, var_level, var_grade, var_is_core, var_is_optional, subject_data):
        """Sauvegarde une nouvelle matière ou modifie une existante"""
        try:
            # Validation des champs
            if not var_name.get().strip():
                messagebox.showerror("Erreur", "Le nom de la matière est obligatoire")
                return
            
            if not var_code.get().strip():
                messagebox.showerror("Erreur", "Le code de la matière est obligatoire")
                return
            
            if not var_level.get():
                messagebox.showerror("Erreur", "Le niveau d'éducation est obligatoire")
                return
            
            if not var_grade.get():
                messagebox.showerror("Erreur", "La classe est obligatoire")
                return
            
            # Préparer les données
            subject_info = {
                "name": var_name.get().strip(),
                "code": var_code.get().strip(),
                "description": desc_entry.get("1.0", "end-1c"),
                "coefficient": float(var_coefficient.get()) if var_coefficient.get() else 1.0,
                "education_level": var_level.get().lower(),
                "grade": var_grade.get(),
                "is_core": var_is_core.get(),
                "is_optional": var_is_optional.get()
            }
            
            # Sauvegarder
            if subject_data:
                # Modification
                success = self.controller.update_subject(subject_data.get("id"), subject_info)
                message = "Matière modifiée avec succès" if success else "Erreur lors de la modification"
            else:
                # Ajout
                success = self.controller.add_custom_subject(subject_info)
                message = "Matière ajoutée avec succès" if success else "Erreur lors de l'ajout"
            
            if success:
                messagebox.showinfo("Succès", message)
                window.destroy()
                self._refresh_all()
            else:
                messagebox.showerror("Erreur", message)
                
        except ValueError:
            messagebox.showerror("Erreur", "Le coefficient doit être un nombre valide")
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur inattendue: {e}")
    
    def _show_search_dialog(self):
        """Affiche une boîte de dialogue de recherche avancée"""
        # Créer une fenêtre de recherche
        search_window = ctk.CTkToplevel(self)
        search_window.title("Recherche Avancée de Matières")
        search_window.geometry("400x300")
        search_window.resizable(False, False)
        search_window.transient(self)
        search_window.grab_set()
        
        # Centrer la fenêtre
        search_window.update_idletasks()
        x = (search_window.winfo_screenwidth() // 2) - (400 // 2)
        y = (search_window.winfo_screenheight() // 2) - (300 // 2)
        search_window.geometry(f"400x300+{x}+{y}")
        
        # Frame principal
        main_frame = ctk.CTkFrame(search_window, fg_color=BG_CARD)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # En-tête
        header_frame = ctk.CTkFrame(main_frame, fg_color=BG_CARD)
        header_frame.pack(fill="x", pady=(0, 20))
        
        search_icon = load_ctk_icon(ICON_MAP.get("search"), size=(24, 24))
        title_frame = ctk.CTkFrame(header_frame, fg_color=BG_CARD)
        title_frame.pack()
        
        if search_icon:
            ctk.CTkLabel(title_frame, text="", image=search_icon, fg_color=BG_CARD).pack(side="left", padx=(0, 10))
        else:
            ctk.CTkLabel(title_frame, text="🔍", font=(FONT, 20), 
                        text_color=TEXT_ACCENT, fg_color=BG_CARD).pack(side="left", padx=(0, 10))
        
        ctk.CTkLabel(title_frame, text="RECHERCHE AVANCÉE", 
                    font=(FONT, FONT_SIZE_HEADER, "bold"),
                    text_color=TEXT_PRIMARY, fg_color=BG_CARD).pack(side="left")
        
        # Formulaire de recherche
        form_frame = ctk.CTkFrame(main_frame, fg_color=BG_CARD)
        form_frame.pack(fill="both", expand=True)
        
        # Recherche par nom
        ctk.CTkLabel(form_frame, text="Nom de la matière:", 
                     font=(FONT, FONT_SIZE_TEXT), text_color=TEXT_PRIMARY, fg_color=BG_CARD).pack(anchor="w", pady=(10, 5))
        
        var_search_name = ctk.StringVar()
        search_entry = ctk.CTkEntry(form_frame, textvariable=var_search_name,
                                   font=(FONT, FONT_SIZE_TEXT), fg_color=BG_MAIN,
                                   text_color=TEXT_PRIMARY, border_color=BORDER_COLOR,
                                   placeholder_text="Ex: Mathématiques")
        search_entry.pack(fill="x", pady=(0, 15))
        
        # Recherche par niveau
        ctk.CTkLabel(form_frame, text="Niveau d'éducation:", 
                     font=(FONT, FONT_SIZE_TEXT), text_color=TEXT_PRIMARY, fg_color=BG_CARD).pack(anchor="w", pady=(0, 5))
        
        var_search_level = ctk.StringVar()
        level_combo = ctk.CTkComboBox(form_frame, values=["Tous", "Primaire", "Collège", "Lycée", "Terminale"],
                                     variable=var_search_level, font=(FONT, FONT_SIZE_TEXT),
                                     fg_color=BG_MAIN, text_color=TEXT_PRIMARY,
                                     border_color=BORDER_COLOR, dropdown_fg_color=BG_CARD)
        level_combo.pack(fill="x", pady=(0, 15))
        level_combo.set("Tous")
        
        # Boutons
        buttons_frame = ctk.CTkFrame(main_frame, fg_color=BG_CARD)
        buttons_frame.pack(fill="x", pady=(10, 0))
        
        def perform_search():
            search_name = var_search_name.get().strip()
            search_level = var_search_level.get()
            
            if search_name or search_level != "Tous":
                # Effectuer la recherche
                filtered = []
                for subject in self.subjects:
                    name_match = not search_name or search_name.lower() in subject.get("name", "").lower()
                    level_match = search_level == "Tous" or self._map_subject_level(subject) == search_level
                    
                    if name_match and level_match:
                        filtered.append(subject)
                
                self.selected_subjects = filtered
                self._update_subjects_table()
                self._update_stats()
                search_window.destroy()
                
                messagebox.showinfo("Recherche", f"{len(filtered)} matière(s) trouvée(s)")
            else:
                messagebox.showwarning("Attention", "Veuillez saisir au moins un critère de recherche")
        
        cancel_btn = ctk.CTkButton(buttons_frame, text="Annuler", 
                                  font=(FONT, FONT_SIZE_TEXT), fg_color=ERROR_RED,
                                  hover_color="#DC2626", text_color=BG_MAIN,
                                  command=search_window.destroy)
        cancel_btn.pack(side="right", padx=(10, 0))
        
        search_btn = ctk.CTkButton(buttons_frame, text="Rechercher", 
                                  font=(FONT, FONT_SIZE_TEXT), fg_color=SUCCESS_GREEN,
                                  hover_color="#059669", text_color=BG_MAIN,
                                  command=perform_search)
        search_btn.pack(side="right")

    # Méthodes de compatibilité avec l'ancienne interface
    def charger_matieres(self, q=""):
        """Méthode de compatibilité - charge les matières avec recherche"""
        if q.strip():
            # Recherche simple dans les matières
            filtered = [s for s in self.subjects if q.lower() in s.get("name", "").lower()]
            self.selected_subjects = filtered
            self._update_subjects_table()
            self._update_stats()
        else:
            self.selected_subjects = self.subjects
            self._update_subjects_table()
            self._update_stats()

    def ajouter_matiere(self):
        """Méthode de compatibilité - ouvre le formulaire d'ajout"""
        self._add_subject()

    def modifier_matiere(self, subject_id):
        """Méthode de compatibilité - ouvre le formulaire de modification"""
        messagebox.showinfo("Information", f"Modification de la matière {subject_id} - Fonctionnalité à implémenter.")

    def supprimer_matiere(self, subject_id):
        """Méthode de compatibilité - supprime une matière"""
        if messagebox.askyesno("Confirmation", f"Voulez-vous vraiment supprimer la matière {subject_id} ?"):
            messagebox.showinfo("Information", "Fonctionnalité de suppression à implémenter.")
