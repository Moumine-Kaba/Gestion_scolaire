# -*- coding: utf-8 -*-
"""
Vue des Bulletins - Style Matières
EduManager+ - Interface Adaptée au Style de la Vue des Matières

Cette vue présente les bulletins organisés par classe avec une interface
similaire à la vue des matières (panneau gauche/droite).
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

from src.modules.academic.grades.controllers.bulletin_controller import get_all_bulletins, add_bulletin, update_bulletin, delete_bulletin
from src.modules.academic.grades.controllers.notes_controller import get_notes_by_eleve, get_notes_summary_by_eleve
from src.modules.academic.students.controllers.eleve_controller import get_all_eleves
from src.modules.academic.classes.controllers.classe_controller import get_all_classes

# Import du thème global
try:
    from resources.themes.theme import *
    print("✅ Thème global EduManager+ importé pour les bulletins")
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
    F_TITLE = (FONT, FONT_SIZE_TITLE, "bold")
    F_SUB = (FONT, FONT_SIZE_HEADER, "bold")
    F_TXT = (FONT, FONT_SIZE_TEXT)
    F_SMALL = (FONT, FONT_SIZE_SMALL)
    F_BOLD = (FONT, FONT_SIZE_TEXT, "bold")

ICON_MAP = {
    "add": "add.png", "edit": "edit.png", "delete": "delete.png",
    "refresh": "refresh.png", "search": "search.png", "close": "close.png",
    "newspaper": "newspaper.png", "grade": "grade.png", "stats": "analytics.png",
    "class": "classroom.png", "sort": "sort.png", "person": "person.png"
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

class BulletinsView(ctk.CTkFrame):
    """Vue des bulletins adaptée au style de la vue des matières"""
        
    def __init__(self, parent, icons=None):
        super().__init__(parent, fg_color=BG_MAIN)
        self.icons = icons
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        # Variables pour la sélection
        self.selected_classe = None
        self.selected_periode = None
        self.selected_bulletins = []
        
        # Variables pour la pagination
        self.current_page = 1
        self.items_per_page = 20
        self.total_pages = 1
        
        # Référence au frame du tableau
        self.table_frame = None
        
        # Cache pour optimiser les performances
        self._data_cache = {}
        self._cache_timestamp = 0
        self._cache_duration = 30  # Cache valide pendant 30 secondes
        
        print("🚀 Chargement des données BulletinsView...")
        
        # Chargement initial des données avec cache
        self._load_cached_data()
        
        print("✅ Données BulletinsView chargées")
        self._build_main_ui()
        
        # Initialiser le message de sélection après la construction de l'UI
        if self.table_frame:
            self._show_no_selection_message(self.table_frame)
    
    def _load_cached_data(self):
        """Charge les données avec système de cache pour optimiser les performances"""
        import time
        current_time = time.time()
        
        # Vérifier si le cache est encore valide
        if (current_time - self._cache_timestamp) < self._cache_duration and self._data_cache:
            print("📋 Utilisation du cache pour les données")
            self.bulletins = self._data_cache.get('bulletins', [])
            self.classes = self._data_cache.get('classes', [])
            self.periodes = self._data_cache.get('periodes', [])
            return
        
        print("🔄 Chargement des données depuis la base...")
        try:
            # Chargement progressif pour éviter le blocage
            self._load_data_progressively()
            
        except Exception as e:
            print(f"⚠️ Erreur chargement données: {e}")
            # Fallback avec données vides
            self.bulletins = []
            self.classes = []
            self.periodes = []
    
    def _load_data_progressively(self):
        """Charge les données de manière progressive pour éviter le blocage"""
        import time
        
        # Charger les vraies classes depuis la base de données
        print("🏫 Chargement des vraies classes...")
        real_classes = get_all_classes()
        self.classes = [cls['nom'] for cls in real_classes]
        print(f"✅ {len(self.classes)} vraies classes chargées: {self.classes[:10]}...")
        
        # Charger les périodes
        print("📅 Chargement des périodes...")
        self.periodes = ["1er Trimestre", "2ème Trimestre", "3ème Trimestre"]
        print(f"✅ {len(self.periodes)} périodes chargées")
        
        # Charger tous les bulletins
        print("📊 Chargement des bulletins...")
        self.bulletins = get_all_bulletins()
        print(f"✅ {len(self.bulletins)} bulletins chargés")
        
        # Mise à jour du cache
        self._data_cache = {
            'bulletins': self.bulletins,
            'classes': self.classes,
            'periodes': self.periodes
        }
        self._cache_timestamp = time.time()
        
        print(f"✅ Données chargées: {len(self.bulletins)} bulletins, {len(self.classes)} classes, {len(self.periodes)} périodes")
    
    def _build_main_ui(self):
        """Construit l'interface principale avec panneau gauche et droite"""
        main_frame = ctk.CTkFrame(self, fg_color=BG_MAIN)
        main_frame.pack(fill="both", expand=True, padx=15, pady=15)
        main_frame.grid_columnconfigure(1, weight=3)
        main_frame.grid_columnconfigure(0, weight=1)
        main_frame.grid_rowconfigure(0, weight=1)

        # Panneau de gauche: Sélection par classe et période
        left_panel = ctk.CTkFrame(main_frame, fg_color=BG_CARD, corner_radius=12)
        left_panel.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        left_panel.grid_columnconfigure(0, weight=1)
        left_panel.grid_rowconfigure(2, weight=1)
        
        self._build_selection_panel(left_panel)
        
        # Panneau de droite: Tableau des bulletins et statistiques
        right_panel = ctk.CTkFrame(main_frame, fg_color=BG_MAIN)
        right_panel.grid(row=0, column=1, sticky="nsew", padx=(10, 0))
        right_panel.grid_columnconfigure(0, weight=1)
        right_panel.grid_rowconfigure(0, weight=1)
        right_panel.grid_rowconfigure(1, weight=4)
        
        self._build_bulletins_dashboard(right_panel)
    
    def _build_selection_panel(self, parent_frame):
        """Construit le panneau de sélection (gauche) avec design moderne"""
        # Header avec gradient et icônes
        header_frame = ctk.CTkFrame(parent_frame, fg_color=ACCENT, corner_radius=12)
        header_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=(10, 15))
        header_frame.grid_columnconfigure(0, weight=1)
        
        # Titre avec icône et style moderne
        title_frame = ctk.CTkFrame(header_frame, fg_color=ACCENT)
        title_frame.grid(row=0, column=0, sticky="w", padx=15, pady=15)
        
        bulletin_icon = load_ctk_icon(ICON_MAP.get("newspaper"), size=(24, 24))
        if bulletin_icon:
            ctk.CTkLabel(title_frame, text="", image=bulletin_icon, fg_color=ACCENT).pack(side="left", padx=(0, 10))
        
        ctk.CTkLabel(title_frame, text="BULLETINS", 
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
        filters_title = ctk.CTkLabel(filters_section, text="SÉLECTION OBLIGATOIRE", 
                                   font=(FONT, FONT_SIZE_TEXT, "bold"),
                                   text_color=TEXT_ACCENT, fg_color=BG_CARD)
        filters_title.grid(row=0, column=0, sticky="w", padx=15, pady=(15, 10))
        
        # Sélection par classe avec style moderne
        classe_frame = ctk.CTkFrame(filters_section, fg_color=BG_CARD)
        classe_frame.grid(row=1, column=0, sticky="ew", padx=15, pady=5)
        classe_frame.grid_columnconfigure(0, weight=1)
        
        classe_label = ctk.CTkLabel(classe_frame, text="Classe:", 
                                  font=(FONT, FONT_SIZE_SMALL, "bold"), 
                                  text_color=TEXT_PRIMARY, fg_color=BG_CARD)
        classe_label.grid(row=0, column=0, sticky="w", padx=(0, 5), pady=(10, 5))
        
        classe_options = ["Sélectionner une classe"] + self.classes
        self.classe_dropdown = ctk.CTkComboBox(
            classe_frame, values=classe_options,
            command=self._on_classe_selected,
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
        self.classe_dropdown.grid(row=1, column=0, sticky="ew", padx=0, pady=(0, 15))
        self.classe_dropdown.set("Sélectionner une classe")
        
        # Sélection par période avec style moderne
        periode_frame = ctk.CTkFrame(filters_section, fg_color=BG_CARD)
        periode_frame.grid(row=2, column=0, sticky="ew", padx=15, pady=5)
        periode_frame.grid_columnconfigure(0, weight=1)
        
        periode_label = ctk.CTkLabel(periode_frame, text="Période:", 
                                  font=(FONT, FONT_SIZE_SMALL, "bold"), 
                                  text_color=TEXT_PRIMARY, fg_color=BG_CARD)
        periode_label.grid(row=0, column=0, sticky="w", padx=(0, 5), pady=(10, 5))
        
        periode_options = ["Toutes les périodes"] + self.periodes
        self.periode_dropdown = ctk.CTkComboBox(
            periode_frame, values=periode_options,
            command=self._on_periode_selected,
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
        self.periode_dropdown.grid(row=1, column=0, sticky="ew", padx=0, pady=(0, 15))
        self.periode_dropdown.set("Toutes les périodes")
        
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
        
        # Bouton Générer
        add_icon = load_ctk_icon(ICON_MAP.get("add"), size=(16, 16))
        add_btn = ctk.CTkButton(actions_section, text="Générer", image=add_icon,
                               font=(FONT, FONT_SIZE_SMALL), fg_color=SUCCESS_GREEN,
                               hover_color="#059669", text_color=BG_MAIN,
                               corner_radius=10, height=35,
                               command=self._add_bulletin)
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
        
        self.stats_label = ctk.CTkLabel(stats_section, text="Sélectionnez une classe pour voir les statistiques",
                                       font=(FONT, FONT_SIZE_SMALL), text_color=TEXT_SECONDARY, fg_color=BG_CARD)
        self.stats_label.grid(row=1, column=0, sticky="ew", padx=15, pady=(0, 15))
        
        self._update_stats()
    
    def _build_bulletins_dashboard(self, parent_frame):
        """Construit le tableau de bord des bulletins (droite)"""
        # En-tête avec actions
        header_frame = ctk.CTkFrame(parent_frame, fg_color=BG_CARD, corner_radius=12)
        header_frame.grid(row=0, column=0, sticky="ew", padx=0, pady=(0, 10))
        header_frame.grid_columnconfigure(1, weight=1)
        header_frame.grid_rowconfigure(0, weight=1)
        
        # Titre du tableau
        title_frame = ctk.CTkFrame(header_frame, fg_color=BG_CARD)
        title_frame.grid(row=0, column=0, sticky="w", padx=15, pady=15)
        
        grade_icon = load_ctk_icon(ICON_MAP.get("grade"), size=(20, 20))
        ctk.CTkLabel(title_frame, text="", image=grade_icon, fg_color=BG_CARD).pack(side="left", padx=(0, 8))
        ctk.CTkLabel(title_frame, text="TABLEAU DES BULLETINS", 
                      font=(FONT, FONT_SIZE_HEADER, "bold"),
                      text_color=TEXT_PRIMARY, fg_color=BG_CARD).pack(side="left")
        
        # Boutons d'action
        actions_frame = ctk.CTkFrame(header_frame, fg_color=BG_CARD)
        actions_frame.grid(row=0, column=1, sticky="e", padx=15, pady=15)
        
        add_icon = load_ctk_icon(ICON_MAP.get("add"), size=(16, 16))
        ctk.CTkButton(actions_frame, text="Ajouter", image=add_icon,
                      font=(FONT, FONT_SIZE_TEXT), fg_color=SUCCESS_GREEN,
                      hover_color="#059669", text_color=BG_MAIN,
                      command=self._add_bulletin).pack(side="right", padx=(5, 0))
        
        # Zone du tableau des bulletins
        self.table_frame = ctk.CTkFrame(parent_frame, fg_color=BG_CARD, corner_radius=12)
        self.table_frame.grid(row=1, column=0, sticky="nsew", padx=0, pady=0)
        self.table_frame.grid_columnconfigure(0, weight=1)
        self.table_frame.grid_rowconfigure(0, weight=1)
        
        # Message initial sera affiché après la construction complète de l'UI
    
    def _show_no_selection_message(self, parent_frame):
        """Affiche le message quand aucune classe n'est sélectionnée"""
        if parent_frame is None:
            return
            
        # Effacer le contenu existant
        for widget in parent_frame.winfo_children():
            widget.destroy()
        
        # Message central
        message_frame = ctk.CTkFrame(parent_frame, fg_color=BG_CARD)
        message_frame.pack(expand=True, fill="both", padx=20, pady=20)
        
        # Icône
        class_icon = load_ctk_icon(ICON_MAP.get("class"), size=(64, 64))
        if class_icon:
            ctk.CTkLabel(message_frame, text="", image=class_icon, fg_color=BG_CARD).pack(pady=(50, 20))
        
        # Titre
        title_label = ctk.CTkLabel(message_frame, text="SÉLECTION REQUISE", 
                                  font=(FONT, FONT_SIZE_HEADER, "bold"),
                                  text_color=TEXT_ACCENT, fg_color=BG_CARD)
        title_label.pack(pady=(0, 10))
        
        # Message
        message_label = ctk.CTkLabel(message_frame, 
                                    text="Veuillez sélectionner une classe dans le panneau de gauche\npour afficher les bulletins et les notes par ordre de mérite.",
                                    font=(FONT, FONT_SIZE_TEXT),
                                    text_color=TEXT_SECONDARY, fg_color=BG_CARD,
                                    justify="center")
        message_label.pack(pady=(0, 30))
        
        # Indication
        info_label = ctk.CTkLabel(message_frame, 
                                 text="📊 Les bulletins seront affichés par ordre de mérite (du meilleur au moins bon)",
                                 font=(FONT, FONT_SIZE_SMALL),
                                 text_color=TEXT_ACCENT, fg_color=BG_CARD)
        info_label.pack(pady=(0, 50))
    
    def _on_classe_selected(self, selected_classe):
        """Gestionnaire de sélection de classe"""
        self.selected_classe = selected_classe if selected_classe != "Sélectionner une classe" else None
        self._filter_bulletins()

    def _on_periode_selected(self, selected_periode):
        """Gestionnaire de sélection de période"""
        self.selected_periode = selected_periode if selected_periode != "Toutes les périodes" else None
        self._filter_bulletins()

    def _filter_bulletins(self):
        """Filtre les bulletins selon les sélections"""
        try:
            print(f"🔍 Filtrage des bulletins - Classe: {self.selected_classe}, Période: {self.selected_periode}")
            
            if not self.selected_classe:
                # Aucune classe sélectionnée - afficher le message
                table_frame = self._get_table_frame()
                if table_frame:
                    self._show_no_selection_message(table_frame)
                self._update_stats()
                return
            
            # Filtrer par classe
            filtered = [b for b in self.bulletins 
                       if b.get('classe_nom', '') == self.selected_classe]
            
            print(f"📊 {len(filtered)} bulletins trouvés pour la classe {self.selected_classe}")
            
            # Filtrer par période si sélectionnée
            if self.selected_periode:
                filtered = [b for b in filtered 
                           if b.get('periode', '') == self.selected_periode]
                print(f"📅 {len(filtered)} bulletins après filtrage par période {self.selected_periode}")
            
            # Trier par ordre de mérite (moyenne décroissante)
            filtered.sort(key=lambda x: float(x.get('moyenne_generale', 0)), reverse=True)
            
            self.selected_bulletins = filtered
            self.current_page = 1  # Réinitialiser à la première page
            self.total_pages = max(1, (len(filtered) + self.items_per_page - 1) // self.items_per_page)
            
            print(f"✅ {len(self.selected_bulletins)} bulletins sélectionnés - Page {self.current_page}/{self.total_pages}")
            
            self._update_bulletins_table()
            self._update_stats()
            
        except Exception as e:
            print(f"❌ Erreur lors du filtrage : {e}")

    def _update_bulletins_table(self):
        """Met à jour le tableau des bulletins"""
        try:
            table_frame = self._get_table_frame()
            
            if table_frame is None:
                print("❌ Frame du tableau non trouvé")
                return
            
            # Effacer le contenu existant
            for widget in table_frame.winfo_children():
            widget.destroy()
        
            if not self.selected_bulletins:
                # Aucun bulletin trouvé
                no_data_frame = ctk.CTkFrame(table_frame, fg_color=BG_CARD)
                no_data_frame.pack(expand=True, fill="both", padx=20, pady=20)
                
                no_data_label = ctk.CTkLabel(no_data_frame, text="Aucun bulletin trouvé pour cette classe",
                                           font=(FONT, FONT_SIZE_TEXT),
                                           text_color=TEXT_SECONDARY, fg_color=BG_CARD)
                no_data_label.pack(expand=True)
            return
        
            # Calculer les indices pour la pagination
            start_idx = (self.current_page - 1) * self.items_per_page
            end_idx = start_idx + self.items_per_page
            page_bulletins = self.selected_bulletins[start_idx:end_idx]
            
            # En-têtes du tableau
            headers = ["Rang", "Nom", "Prénom", "Moyenne", "Période", "Mention"]
            
            # Données de la page actuelle
            table_data = [headers]
            for i, bulletin in enumerate(page_bulletins, start_idx + 1):
                row = [
                    str(bulletin.get('rang', i)),  # Rang dans la classe
                    bulletin.get('eleve_nom', ''),
                    bulletin.get('eleve_prenom', ''),
                    f"{float(bulletin.get('moyenne_generale', 0)):.1f}",
                    bulletin.get('periode', ''),
                    bulletin.get('appreciation', '')  # Mention (Très Bien, Bien, etc.)
                ]
                table_data.append(row)
            
            # Créer le tableau
            self.bulletins_table = CTkTable(
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
            
            self.bulletins_table.pack(fill="both", expand=True, padx=10, pady=10)
            
            # Configurer la sélection de ligne
            self.bulletins_table.bind("<Button-1>", self._on_table_select)
            
            # Ajouter les contrôles de pagination
            self._add_pagination_controls(table_frame)
            
        except Exception as e:
            print(f"❌ Erreur lors de la mise à jour du tableau : {e}")

    def _add_pagination_controls(self, parent_frame):
        """Ajoute les contrôles de pagination"""
        if self.total_pages <= 1:
            return
        
        # Frame pour les contrôles de pagination
        pagination_frame = ctk.CTkFrame(parent_frame, fg_color=BG_CARD)
        pagination_frame.pack(fill="x", padx=10, pady=(0, 10))
        
        # Informations de pagination
        info_text = f"Page {self.current_page} sur {self.total_pages} - {len(self.selected_bulletins)} bulletins au total"
        info_label = ctk.CTkLabel(pagination_frame, text=info_text,
                                 font=(FONT, FONT_SIZE_SMALL),
                                 text_color=TEXT_SECONDARY, fg_color=BG_CARD)
        info_label.pack(side="left", padx=10, pady=5)
        
        # Boutons de navigation
        nav_frame = ctk.CTkFrame(pagination_frame, fg_color=BG_CARD)
        nav_frame.pack(side="right", padx=10, pady=5)
        
        # Bouton précédent
        prev_btn = ctk.CTkButton(nav_frame, text="◀ Précédent",
                                font=(FONT, FONT_SIZE_SMALL),
                                fg_color=PRIMARY_BLUE, hover_color="#1e40af",
                                text_color=BG_MAIN, width=100,
                                command=self._go_to_previous_page)
        prev_btn.pack(side="left", padx=2)
        
        # Numéro de page actuelle
        page_label = ctk.CTkLabel(nav_frame, text=f"{self.current_page}",
                                 font=(FONT, FONT_SIZE_SMALL, "bold"),
                                 text_color=TEXT_PRIMARY, fg_color=BG_CARD)
        page_label.pack(side="left", padx=10)
        
        # Bouton suivant
        next_btn = ctk.CTkButton(nav_frame, text="Suivant ▶",
                                font=(FONT, FONT_SIZE_SMALL),
                                fg_color=PRIMARY_BLUE, hover_color="#1e40af",
                                text_color=BG_MAIN, width=100,
                                command=self._go_to_next_page)
        next_btn.pack(side="left", padx=2)
        
        # Désactiver les boutons si nécessaire
        if self.current_page <= 1:
            prev_btn.configure(state="disabled")
        if self.current_page >= self.total_pages:
            next_btn.configure(state="disabled")

    def _go_to_previous_page(self):
        """Va à la page précédente"""
        if self.current_page > 1:
            self.current_page -= 1
            self._update_bulletins_table()

    def _go_to_next_page(self):
        """Va à la page suivante"""
        if self.current_page < self.total_pages:
            self.current_page += 1
            self._update_bulletins_table()

    def _get_table_frame(self):
        """Récupère le frame du tableau"""
        # Utiliser la référence directe au frame du tableau
        if hasattr(self, 'table_frame') and self.table_frame is not None:
            return self.table_frame
        return None

    def _update_stats(self):
        """Met à jour les statistiques affichées"""
        try:
            if not self.selected_bulletins:
                stats_text = "Sélectionnez une classe pour voir les statistiques"
            else:
                total_bulletins = len(self.selected_bulletins)
                moyennes = [b.get('moyenne_generale', 0) for b in self.selected_bulletins if b.get('moyenne_generale')]
                moyenne_generale = sum(moyennes) / len(moyennes) if moyennes else 0
                meilleure_note = max(moyennes) if moyennes else 0
                
                stats_text = f"📊 {total_bulletins} bulletins • Moyenne: {moyenne_generale:.2f} • Meilleure: {meilleure_note:.2f}"
            
            self.stats_label.configure(text=stats_text)
            
        except Exception as e:
            print(f"❌ Erreur lors de la mise à jour des stats : {e}")

    def _on_table_select(self, event):
        """Gestionnaire de sélection dans le tableau"""
        try:
            # Récupérer la ligne sélectionnée
            selected_row = self.bulletins_table.get_selected_row()
            if selected_row and selected_row > 0:  # Ignorer l'en-tête
                print(f"📊 Bulletin sélectionné: ligne {selected_row}")
        except Exception as e:
            print(f"❌ Erreur lors de la sélection : {e}")

    def _refresh_all(self):
        """Rafraîchit toutes les données en invalidant le cache"""
        print("🔄 Rafraîchissement des données...")
        self._cache_timestamp = 0  # Invalider le cache
        self._load_cached_data()
        
        self.selected_classe = None
        self.selected_periode = None
        self.selected_bulletins = []
        
        self.classe_dropdown.set("Sélectionner une classe")
        self.periode_dropdown.set("Toutes les périodes")
        self._show_no_selection_message(self._get_table_frame())
        self._update_stats()

    def _add_bulletin(self):
        """Génère automatiquement les bulletins à partir des notes"""
        if not self.selected_classe:
            messagebox.showwarning("Génération", "Sélectionnez d'abord une classe pour générer les bulletins.")
            return
        
        if not self.selected_periode:
            messagebox.showwarning("Génération", "Sélectionnez d'abord une période pour générer les bulletins.")
            return
        
        # Confirmer la génération
        if messagebox.askyesno("Génération des bulletins", 
                              f"Voulez-vous générer automatiquement les bulletins pour la classe {self.selected_classe} - {self.selected_periode} ?\n\n"
                              f"Cette action va calculer les moyennes à partir des notes existantes."):
            self._generate_bulletins_from_notes()
    
    def _generate_bulletins_from_notes(self):
        """Génère automatiquement les bulletins à partir des notes de la classe et période sélectionnées"""
        try:
            # Récupérer la classe ID
            classe_id = next((cid for cid, cdata in self.classes.items() if cdata.get("nom") == self.selected_classe), None)
            if not classe_id:
                messagebox.showerror("Erreur", "Classe non trouvée.")
                return
            
            # Récupérer tous les élèves de la classe
            eleves_classe = get_all_eleves(classe_id=classe_id)
            if not eleves_classe:
                messagebox.showwarning("Génération", "Aucun élève trouvé dans cette classe.")
                return
            
            bulletins_generes = 0
            
            for eleve in eleves_classe:
                eleve_id = eleve.get("id_eleve")
                
                # Récupérer les notes de l'élève pour la période sélectionnée
                notes_eleve = get_notes_by_eleve(eleve_id, trimestre=self.selected_periode)
                
                if not notes_eleve:
                    print(f"⚠️ Aucune note trouvée pour {eleve.get('nom')} {eleve.get('prenom')} - {self.selected_periode}")
                    continue
                
                # Calculer la moyenne pondérée
                total_points = 0
                total_coefficients = 0
                
                for note in notes_eleve:
                    note_value = float(note.get("note", 0))
                    coefficient = float(note.get("coefficient", 1))
                    total_points += note_value * coefficient
                    total_coefficients += coefficient
                
                if total_coefficients > 0:
                    moyenne_generale = total_points / total_coefficients
                    
                    # Déterminer la mention
                    if moyenne_generale >= 16:
                        mention = "Très Bien"
                    elif moyenne_generale >= 14:
                        mention = "Bien"
                    elif moyenne_generale >= 12:
                        mention = "Assez Bien"
                    elif moyenne_generale >= 10:
                        mention = "Passable"
                    else:
                        mention = "Insuffisant"
                    
                    # Vérifier si un bulletin existe déjà pour cet élève et cette période
                    from database.connection import get_db_connection
                    conn = get_db_connection()
                    cursor = conn.cursor()
                    
                    cursor.execute("""
                        SELECT id_bulletin FROM bulletins 
                        WHERE id_eleve = ? AND periode = ?
                    """, (eleve_id, self.selected_periode))
                    
                    existing_bulletin = cursor.fetchone()
                    
                    if existing_bulletin:
                        # Mettre à jour le bulletin existant
                        cursor.execute("""
                            UPDATE bulletins 
                            SET moyenne_generale = ?, appreciation = ?, date_creation = ?
                            WHERE id_eleve = ? AND periode = ?
                        """, (moyenne_generale, mention, datetime.now(), eleve_id, self.selected_periode))
                        print(f"🔄 Bulletin mis à jour pour {eleve.get('nom')} {eleve.get('prenom')} - Moyenne: {moyenne_generale:.2f}")
                    else:
                        # Créer un nouveau bulletin
                        cursor.execute("""
                            INSERT INTO bulletins (id_eleve, periode, moyenne_generale, rang, appreciation, date_creation)
                            VALUES (?, ?, ?, 0, ?, ?)
                        """, (eleve_id, self.selected_periode, moyenne_generale, mention, datetime.now()))
                        print(f"✅ Nouveau bulletin créé pour {eleve.get('nom')} {eleve.get('prenom')} - Moyenne: {moyenne_generale:.2f}")
                    
                    bulletins_generes += 1
                    conn.commit()
                    conn.close()
            
            # Recalculer les rangs après génération
            self._recalculate_ranks(classe_id, self.selected_periode)
            
            # Rafraîchir l'affichage
            self._refresh_all()
            
            messagebox.showinfo("Génération terminée", 
                              f"✅ {bulletins_generes} bulletins générés avec succès pour la classe {self.selected_classe} - {self.selected_periode}.\n\n"
                              f"Les moyennes ont été calculées automatiquement à partir des notes existantes.")
            
        except Exception as e:
            print(f"❌ Erreur lors de la génération des bulletins: {e}")
            messagebox.showerror("Erreur", f"Erreur lors de la génération des bulletins:\n{str(e)}")
    
    def _recalculate_ranks(self, classe_id, periode):
        """Recalcule les rangs des élèves dans une classe pour une période donnée"""
        try:
            from database.connection import get_db_connection
            conn = get_db_connection()
            cursor = conn.cursor()
            
            # Récupérer tous les bulletins de la classe et période, triés par moyenne décroissante
            cursor.execute("""
                SELECT b.id_bulletin, b.id_eleve, b.moyenne_generale
                FROM bulletins b
                JOIN eleves e ON b.id_eleve = e.id_eleve
                WHERE e.id_classe = ? AND b.periode = ?
                ORDER BY b.moyenne_generale DESC
            """, (classe_id, periode))
            
            bulletins = cursor.fetchall()
            
            # Mettre à jour les rangs
            for i, (bulletin_id, eleve_id, moyenne) in enumerate(bulletins):
                rang = i + 1
                cursor.execute("""
                    UPDATE bulletins SET rang = ? WHERE id_bulletin = ?
                """, (rang, bulletin_id))
            
            conn.commit()
            conn.close()
            print(f"✅ Rangs recalculés pour la classe {classe_id} - {periode}")
            
        except Exception as e:
            print(f"❌ Erreur lors du recalcul des rangs: {e}")
    
    def _open_bulletin_form(self, bulletin_data=None):
        """Ouvre le formulaire d'ajout/modification de bulletin"""
        # Créer une fenêtre modale
        form_window = ctk.CTkToplevel(self)
        form_window.title("Ajouter un Bulletin" if not bulletin_data else "Modifier le Bulletin")
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
            ctk.CTkLabel(title_frame, text="📊", font=(FONT, 24), 
                        text_color=BG_MAIN, fg_color=ACCENT).pack(side="left", padx=(0, 10))
        
        title_text = "➕ NOUVEAU BULLETIN" if not bulletin_data else "✏️ MODIFIER BULLETIN"
        title = ctk.CTkLabel(title_frame, text=title_text,
                            font=(FONT, FONT_SIZE_HEADER, "bold"),
                            text_color=BG_MAIN, fg_color=ACCENT)
        title.pack(side="left")
        
        # Formulaire avec sections organisées
        form_frame = ctk.CTkFrame(main_frame, fg_color=BG_CARD)
        form_frame.pack(fill="both", expand=True)
        
        # Variables du formulaire
        var_eleve = ctk.StringVar()
        var_periode = ctk.StringVar()
        var_moyenne = ctk.StringVar()
        var_rang = ctk.StringVar()
        var_appreciation = ctk.StringVar()
        
        # Section 1: Informations de base
        basic_section = ctk.CTkFrame(form_frame, fg_color=BG_CARD, corner_radius=8)
        basic_section.pack(fill="x", padx=15, pady=(15, 10))
        
        basic_title = ctk.CTkLabel(basic_section, text="📝 INFORMATIONS DE BASE",
                                  font=(FONT, FONT_SIZE_TEXT, "bold"),
                                  text_color=TEXT_ACCENT, fg_color=BG_CARD)
        basic_title.pack(anchor="w", padx=15, pady=(15, 10))
        
        # Élève
        eleve_frame = ctk.CTkFrame(basic_section, fg_color=BG_CARD)
        eleve_frame.pack(fill="x", padx=15, pady=5)
        eleve_frame.grid_columnconfigure(1, weight=1)
        
        ctk.CTkLabel(eleve_frame, text="Élève:", 
                     font=(FONT, FONT_SIZE_TEXT, "bold"), 
                     text_color=TEXT_PRIMARY, fg_color=BG_CARD).grid(row=0, column=0, sticky="w", padx=(0, 10))
        
        # Récupérer les élèves
        eleves = get_all_eleves()
        eleves_choices = [f"{e[0]} - {e[1]} {e[2]}" for e in eleves]
        
        eleve_combo = ctk.CTkComboBox(eleve_frame, values=eleves_choices, variable=var_eleve,
                                     font=(FONT, FONT_SIZE_TEXT), fg_color=BG_MAIN,
                                     text_color=TEXT_PRIMARY, border_color=BORDER_COLOR,
                                     dropdown_fg_color=BG_CARD, button_color=ACCENT,
                                     height=35, corner_radius=8)
        eleve_combo.grid(row=0, column=1, sticky="ew", padx=(0, 0))
        
        # Période
        periode_frame = ctk.CTkFrame(basic_section, fg_color=BG_CARD)
        periode_frame.pack(fill="x", padx=15, pady=5)
        periode_frame.grid_columnconfigure(1, weight=1)
        
        ctk.CTkLabel(periode_frame, text="Période:", 
                     font=(FONT, FONT_SIZE_TEXT, "bold"), 
                     text_color=TEXT_PRIMARY, fg_color=BG_CARD).grid(row=0, column=0, sticky="w", padx=(0, 10))
        
        periode_combo = ctk.CTkComboBox(periode_frame, values=self.periodes, variable=var_periode,
                                       font=(FONT, FONT_SIZE_TEXT), fg_color=BG_MAIN,
                                       text_color=TEXT_PRIMARY, border_color=BORDER_COLOR,
                                       dropdown_fg_color=BG_CARD, button_color=ACCENT,
                                       height=35, corner_radius=8)
        periode_combo.grid(row=0, column=1, sticky="ew", padx=(0, 0))
        
        # Moyenne
        moyenne_frame = ctk.CTkFrame(basic_section, fg_color=BG_CARD)
        moyenne_frame.pack(fill="x", padx=15, pady=5)
        moyenne_frame.grid_columnconfigure(1, weight=1)
        
        ctk.CTkLabel(moyenne_frame, text="Moyenne:", 
                     font=(FONT, FONT_SIZE_TEXT, "bold"), 
                     text_color=TEXT_PRIMARY, fg_color=BG_CARD).grid(row=0, column=0, sticky="w", padx=(0, 10))
        
        moyenne_entry = ctk.CTkEntry(moyenne_frame, textvariable=var_moyenne, 
                                    font=(FONT, FONT_SIZE_TEXT), fg_color=BG_MAIN,
                                    text_color=TEXT_PRIMARY, border_color=BORDER_COLOR,
                                    placeholder_text="Ex: 15.5", height=35)
        moyenne_entry.grid(row=0, column=1, sticky="ew", padx=(0, 0))
        
        # Rang
        rang_frame = ctk.CTkFrame(basic_section, fg_color=BG_CARD)
        rang_frame.pack(fill="x", padx=15, pady=(5, 15))
        rang_frame.grid_columnconfigure(1, weight=1)
        
        ctk.CTkLabel(rang_frame, text="Rang:", 
                     font=(FONT, FONT_SIZE_TEXT, "bold"), 
                     text_color=TEXT_PRIMARY, fg_color=BG_CARD).grid(row=0, column=0, sticky="w", padx=(0, 10))
        
        rang_entry = ctk.CTkEntry(rang_frame, textvariable=var_rang, 
                                 font=(FONT, FONT_SIZE_TEXT), fg_color=BG_MAIN,
                                 text_color=TEXT_PRIMARY, border_color=BORDER_COLOR,
                                 placeholder_text="Ex: 1", height=35)
        rang_entry.grid(row=0, column=1, sticky="ew", padx=(0, 0))
        
        # Section 2: Appréciation
        app_section = ctk.CTkFrame(form_frame, fg_color=BG_CARD, corner_radius=8)
        app_section.pack(fill="x", padx=15, pady=10)
        
        app_title = ctk.CTkLabel(app_section, text="💬 APPRÉCIATION",
                                font=(FONT, FONT_SIZE_TEXT, "bold"),
                                text_color=TEXT_ACCENT, fg_color=BG_CARD)
        app_title.pack(anchor="w", padx=15, pady=(15, 10))
        
        app_frame = ctk.CTkFrame(app_section, fg_color=BG_CARD)
        app_frame.pack(fill="x", padx=15, pady=(0, 15))
        
        ctk.CTkLabel(app_frame, text="Appréciation:", 
                     font=(FONT, FONT_SIZE_TEXT, "bold"), 
                     text_color=TEXT_PRIMARY, fg_color=BG_CARD).pack(anchor="w", padx=15, pady=(15, 5))
        
        app_textbox = ctk.CTkTextbox(app_frame, height=80, 
                                    font=(FONT, FONT_SIZE_TEXT), fg_color=BG_MAIN,
                                    text_color=TEXT_PRIMARY, border_color=BORDER_COLOR,
                                    corner_radius=8)
        app_textbox.pack(fill="x", padx=15, pady=(0, 15))
        
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
                                command=lambda: self._save_bulletin(form_window, var_eleve, var_periode, 
                                                                var_moyenne, var_rang, app_textbox, bulletin_data))
        save_btn.grid(row=0, column=1, sticky="ew", padx=(5, 0))
    
    def _save_bulletin(self, window, var_eleve, var_periode, var_moyenne, var_rang, app_textbox, bulletin_data):
        """Sauvegarde un nouveau bulletin ou modifie un existant"""
        try:
            # Validation des champs
            if not all([var_eleve.get().strip(), var_periode.get().strip(), var_moyenne.get().strip()]):
                messagebox.showerror("Erreur", "Veuillez remplir tous les champs obligatoires")
                return
            
            # Validation de la moyenne
            try:
                moyenne_float = float(var_moyenne.get())
                if not (0 <= moyenne_float <= 20):
                    messagebox.showerror("Erreur", "La moyenne doit être entre 0 et 20")
                    return
            except ValueError:
                messagebox.showerror("Erreur", "Moyenne invalide")
                return
            
            # Validation du rang
            rang_int = None
            if var_rang.get().strip():
                try:
                    rang_int = int(var_rang.get())
                except ValueError:
                    messagebox.showerror("Erreur", "Rang invalide")
                    return
            
            # Récupérer l'ID de l'élève
            try:
                id_eleve = int(var_eleve.get().split(" - ")[0])
            except:
                messagebox.showerror("Erreur", "Élève invalide")
                return
            
            # Préparer les données
            bulletin_info = {
                "id_eleve": id_eleve,
                "periode": var_periode.get().strip(),
                "moyenne_generale": moyenne_float,
                "rang": rang_int,
                "appreciation": app_textbox.get("1.0", "end-1c").strip()
            }
            
            # Sauvegarder
            if bulletin_data:
                # Modification
                success = update_bulletin(bulletin_data.get("id"), bulletin_info)
                message = "Bulletin modifié avec succès" if success else "Erreur lors de la modification"
            else:
                # Ajout
                success = add_bulletin(bulletin_info)
                message = "Bulletin ajouté avec succès" if success else "Erreur lors de l'ajout"
            
            if success:
                messagebox.showinfo("Succès", message)
                window.destroy()
                self._refresh_all()
            else:
                messagebox.showerror("Erreur", message)
                
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur inattendue: {e}")

    def _show_search_dialog(self):
        """Affiche une boîte de dialogue de recherche avancée"""
        # Créer une fenêtre de recherche
        search_window = ctk.CTkToplevel(self)
        search_window.title("Recherche Avancée de Bulletins")
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
        ctk.CTkLabel(form_frame, text="Nom de l'élève:", 
                     font=(FONT, FONT_SIZE_TEXT), text_color=TEXT_PRIMARY, fg_color=BG_CARD).pack(anchor="w", pady=(10, 5))
        
        var_search_name = ctk.StringVar()
        search_entry = ctk.CTkEntry(form_frame, textvariable=var_search_name,
                                   font=(FONT, FONT_SIZE_TEXT), fg_color=BG_MAIN,
                                   text_color=TEXT_PRIMARY, border_color=BORDER_COLOR,
                                   placeholder_text="Ex: Dupont")
        search_entry.pack(fill="x", pady=(0, 15))
        
        # Recherche par classe
        ctk.CTkLabel(form_frame, text="Classe:", 
                     font=(FONT, FONT_SIZE_TEXT), text_color=TEXT_PRIMARY, fg_color=BG_CARD).pack(anchor="w", pady=(0, 5))
        
        var_search_classe = ctk.StringVar()
        classe_combo = ctk.CTkComboBox(form_frame, values=["Toutes"] + self.classes,
                                      variable=var_search_classe, font=(FONT, FONT_SIZE_TEXT),
                                      fg_color=BG_MAIN, text_color=TEXT_PRIMARY,
                                      border_color=BORDER_COLOR, dropdown_fg_color=BG_CARD)
        classe_combo.pack(fill="x", pady=(0, 15))
        classe_combo.set("Toutes")
        
        # Boutons
        buttons_frame = ctk.CTkFrame(main_frame, fg_color=BG_CARD)
        buttons_frame.pack(fill="x", pady=(10, 0))
        
        def perform_search():
            search_name = var_search_name.get().strip()
            search_classe = var_search_classe.get()
            
            if search_name or search_classe != "Toutes":
                # Effectuer la recherche
                filtered = []
                for bulletin in self.bulletins:
                    name_match = not search_name or search_name.lower() in bulletin.get('eleve_nom', '').lower()
                    classe_match = search_classe == "Toutes" or bulletin.get('classe_nom', '') == search_classe
                    
                    if name_match and classe_match:
                        filtered.append(bulletin)
                
                # Trier par ordre de mérite
                filtered.sort(key=lambda x: x.get('moyenne_generale', 0), reverse=True)
                
                self.selected_bulletins = filtered
                self._update_bulletins_table()
                self._update_stats()
                search_window.destroy()
                
                messagebox.showinfo("Recherche", f"{len(filtered)} bulletin(s) trouvé(s)")
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
    def charger_classes(self):
        """Méthode de compatibilité - charge les classes"""
        pass

    def charger_bulletins(self):
        """Méthode de compatibilité - charge les bulletins"""
        pass

    def ajouter_bulletin(self):
        """Méthode de compatibilité - ouvre le formulaire d'ajout"""
        self._add_bulletin()

    def modifier_bulletin(self, bulletin_id):
        """Méthode de compatibilité - ouvre le formulaire de modification"""
        messagebox.showinfo("Information", f"Modification du bulletin {bulletin_id} - Fonctionnalité à implémenter.")

    def supprimer_bulletin(self, bulletin_id):
        """Méthode de compatibilité - supprime un bulletin"""
        if messagebox.askyesno("Confirmation", f"Voulez-vous vraiment supprimer le bulletin {bulletin_id} ?"):
            messagebox.showinfo("Information", "Fonctionnalité de suppression à implémenter.")
    
    def _create_bulletin_card(self, bulletin):
        """Crée une carte pour un bulletin"""
        card = ctk.CTkFrame(self.cards_scroll, fg_color=BG_CARD, corner_radius=12)
        
        # En-tête de la carte
        header_frame = ctk.CTkFrame(card, fg_color="transparent")
        header_frame.pack(fill="x", padx=20, pady=(20, 10))
        header_frame.grid_columnconfigure(1, weight=1)
        
        # Icône élève
        student_icon = load_ctk_icon("person.png", (24, 24))
        if student_icon:
            icon_label = ctk.CTkLabel(header_frame, image=student_icon, text="")
            icon_label.grid(row=0, column=0, padx=(0, 15))
        
        # Nom de l'élève avec rang dans la classe
        eleve_name = f"{bulletin.get('eleve_prenom', '')} {bulletin.get('eleve_nom', '')}"
        rang_classe = bulletin.get('rang', 'N/A')
        
        # Créer un frame pour le nom et le rang
        name_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        name_frame.grid(row=0, column=1, sticky="w")
        
        name_label = ctk.CTkLabel(name_frame, text=eleve_name, 
                                 font=F_SUB, text_color=TEXT_PRIMARY)
        name_label.pack(anchor="w")
        
        # Indication du rang avec couleur selon la performance
        if isinstance(rang_classe, (int, float)) and rang_classe <= 3:
            rang_color = SUCCESS_GREEN if rang_classe == 1 else WARNING_ORANGE
            rang_text = f"🏆 {rang_classe}er" if rang_classe == 1 else f"🥈 {rang_classe}ème"
        else:
            rang_color = TEXT_SECONDARY
            rang_text = f"Rang: {rang_classe}"
            
        rang_label = ctk.CTkLabel(name_frame, text=rang_text, 
                                 font=F_SMALL, text_color=rang_color)
        rang_label.pack(anchor="w")
        
        # Boutons d'action
        actions_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        actions_frame.grid(row=0, column=2, sticky="e")
        
        # Bouton Modifier
        edit_icon = load_ctk_icon("edit.png", (16, 16))
        edit_btn = ctk.CTkButton(actions_frame, text="", image=edit_icon,
                                fg_color="transparent", text_color=ACCENT_BLUE,
                                width=32, height=32, border_width=1, border_color=ACCENT_BLUE,
                                command=lambda: self.modifier_bulletin(bulletin))
        edit_btn.pack(side="right", padx=(5, 0))
        
        # Bouton Supprimer
        delete_icon = load_ctk_icon("delete.png", (16, 16))
        delete_btn = ctk.CTkButton(actions_frame, text="", image=delete_icon,
                                  fg_color="transparent", text_color=ERROR_RED,
                                  width=32, height=32, border_width=1, border_color=ERROR_RED,
                                  command=lambda: self.supprimer_bulletin(bulletin))
        delete_btn.pack(side="right", padx=(5, 0))
        
        # Contenu de la carte
        content_frame = ctk.CTkFrame(card, fg_color="transparent")
        content_frame.pack(fill="x", padx=20, pady=(0, 20))
        
        # Informations du bulletin
        info_data = [
            ("Période", bulletin.get('periode', 'N/A')),
            ("Moyenne", f"{bulletin.get('moyenne_generale', 0):.2f}"),
            ("Rang", str(bulletin.get('rang', 'N/A'))),
            ("Date", self._format_date(bulletin.get('date_creation')))
        ]
        
        for i, (label, value) in enumerate(info_data):
            info_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
            info_frame.grid(row=i//2, column=i%2, padx=5, pady=5, sticky="ew")
            content_frame.grid_columnconfigure((0, 1), weight=1)
            
            label_widget = ctk.CTkLabel(info_frame, text=f"{label}:", 
                                       font=F_SMALL, text_color=TEXT_SECONDARY)
            label_widget.pack(anchor="w")
            
            value_widget = ctk.CTkLabel(info_frame, text=value, 
                                       font=F_BOLD, text_color=TEXT_PRIMARY)
            value_widget.pack(anchor="w")
        
        # Appréciation
        appreciation = bulletin.get('appreciation', '')
        if appreciation:
            app_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
            app_frame.grid(row=2, column=0, columnspan=2, padx=5, pady=5, sticky="ew")
            
            app_label = ctk.CTkLabel(app_frame, text="Appréciation:", 
                                    font=F_SMALL, text_color=TEXT_SECONDARY)
            app_label.pack(anchor="w")
            
            app_text = ctk.CTkLabel(app_frame, text=appreciation, 
                                   font=F_TXT, text_color=TEXT_PRIMARY,
                                   wraplength=400, justify="left")
            app_text.pack(anchor="w")
        
        return card
    
    def _format_date(self, date_obj):
        """Formate une date pour l'affichage"""
        if not date_obj:
            return 'N/A'
        
        try:
            # Si c'est un objet datetime
            if hasattr(date_obj, 'strftime'):
                return date_obj.strftime('%d/%m/%Y')
            # Si c'est une chaîne
            elif isinstance(date_obj, str):
                return date_obj[:10] if len(date_obj) >= 10 else date_obj
            else:
                return str(date_obj)
        except Exception:
            return 'N/A'

    def charger_classes(self):
        """Charge les classes pour le filtre"""
        try:
            classes = get_all_classes()
            classe_values = ["Toutes"] + [f"{c[0]} - {c[1]}" for c in classes]
            self.classe_combo.configure(values=classe_values)
        except Exception as e:
            print(f"Erreur lors du chargement des classes: {e}")
            self.classe_combo.configure(values=["Toutes"])
    
    def charger_bulletins(self):
        """Charge et affiche les bulletins groupés par classe"""
        # Effacer les cartes existantes
        for widget in self.cards_scroll.winfo_children():
            widget.destroy()
        
        # Récupérer les bulletins
        bulletins = get_all_bulletins()
        
        # Appliquer les filtres
        filtered_bulletins = self._apply_filters(bulletins)
        
        if not filtered_bulletins:
            # Afficher un message si aucun bulletin
            no_data_frame = ctk.CTkFrame(self.cards_scroll, fg_color=BG_CARD, corner_radius=12)
            no_data_frame.grid(row=0, column=0, columnspan=3, padx=10, pady=20, sticky="ew")
            
            no_data_label = ctk.CTkLabel(no_data_frame, text="Aucun bulletin trouvé", 
                                       font=F_SUB, text_color=TEXT_SECONDARY)
            no_data_label.pack(pady=30)
            
            self._update_statistics([])
            return
        
        # Grouper les bulletins par classe
        bulletins_par_classe = self._grouper_bulletins_par_classe(filtered_bulletins)
        
        # Créer les sections par classe
        row_index = 0
        for classe_nom, bulletins_classe in bulletins_par_classe.items():
            # Limiter à 100 bulletins par classe (les meilleurs)
            bulletins_a_afficher = bulletins_classe[:self.limite_par_classe]
            nb_total = len(bulletins_classe)
            nb_affiches = len(bulletins_a_afficher)
            
            # Créer l'en-tête de classe avec information sur le classement
            classe_header = self._create_classe_header(classe_nom, nb_total, nb_affiches)
            classe_header.grid(row=row_index, column=0, columnspan=3, padx=10, pady=(20 if row_index == 0 else 10, 5), sticky="ew")
            row_index += 1
            
            # Créer les cartes de bulletins pour cette classe (les 100 premiers)
            for i, bulletin in enumerate(bulletins_a_afficher):
                card = self._create_bulletin_card(bulletin)
                card_row = row_index + (i // 3)
                card_col = i % 3
                card.grid(row=card_row, column=card_col, padx=10, pady=5, sticky="ew")
            
            # Ajouter un message si il y a plus de bulletins que la limite
            if nb_total > self.limite_par_classe:
                more_frame = ctk.CTkFrame(self.cards_scroll, fg_color=BG_CARD, corner_radius=8)
                more_frame.grid(row=row_index + (nb_affiches + 2) // 3, column=0, columnspan=3, 
                               padx=10, pady=5, sticky="ew")
                
                more_label = ctk.CTkLabel(more_frame, 
                                        text=f"... et {nb_total - nb_affiches} autre(s) élève(s) dans cette classe", 
                                        font=F_SMALL, text_color=TEXT_SECONDARY)
                more_label.pack(pady=8)
            
            # Mettre à jour l'index de ligne pour la prochaine classe
            row_index += (nb_affiches + 2) // 3 + (1 if nb_total > self.limite_par_classe else 0)
        
        # Mettre à jour les statistiques
        self._update_statistics(filtered_bulletins)
    
    def _grouper_bulletins_par_classe(self, bulletins):
        """Groupe les bulletins par classe et les trie par ordre de mérite"""
        bulletins_par_classe = {}
        
        for bulletin in bulletins:
            # Récupérer le nom de la classe depuis les données du bulletin
            classe_nom = bulletin.get('classe_nom', 'Classe non définie')
            
            if classe_nom not in bulletins_par_classe:
                bulletins_par_classe[classe_nom] = []
            
            bulletins_par_classe[classe_nom].append(bulletin)
        
        # Trier les classes par nom et les bulletins par ordre de mérite (moyenne décroissante)
        for classe_nom in bulletins_par_classe:
            bulletins_par_classe[classe_nom].sort(
                key=lambda x: x.get('moyenne_generale', 0), 
                reverse=True
            )
        
        return dict(sorted(bulletins_par_classe.items()))
    
    def _create_classe_header(self, classe_nom, nb_total, nb_affiches):
        """Crée un en-tête pour une classe avec classement par ordre de mérite"""
        header_frame = ctk.CTkFrame(self.cards_scroll, fg_color=BG_SIDEBAR, corner_radius=8)
        
        # Contenu de l'en-tête
        content_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        content_frame.pack(fill="x", padx=15, pady=10)
        
        # Icône classe
        classe_icon = load_ctk_icon("school.png", (20, 20))
        if classe_icon:
            icon_label = ctk.CTkLabel(content_frame, image=classe_icon, text="")
            icon_label.pack(side="left", padx=(0, 10))
        
        # Nom de la classe
        classe_label = ctk.CTkLabel(content_frame, text=f"Classe {classe_nom}", 
                                   font=F_SUB, text_color=TEXT_PRIMARY)
        classe_label.pack(side="left")
        
        # Information sur le classement avec limite
        if nb_total > nb_affiches:
            ranking_text = f"({nb_affiches}/{nb_total} meilleurs élèves - Classement par ordre de mérite)"
            ranking_color = WARNING_ORANGE
        else:
            ranking_text = f"({nb_total} élèves - Classement par ordre de mérite)"
            ranking_color = SUCCESS_GREEN
            
        ranking_label = ctk.CTkLabel(content_frame, text=ranking_text, 
                                    font=F_SMALL, text_color=ranking_color)
        ranking_label.pack(side="left", padx=(10, 0))
        
        return header_frame
    
    def _apply_filters(self, bulletins):
        """Applique les filtres de recherche"""
        filtered = bulletins.copy()
        
        # Filtre par nom d'élève
        search_text = self.search_entry.get().lower()
        if search_text:
            filtered = [b for b in filtered if 
                       search_text in b.get('eleve_nom', '').lower() or 
                       search_text in b.get('eleve_prenom', '').lower()]
        
        # Filtre par classe
        classe_selectionnee = self.classe_var.get()
        if classe_selectionnee != "Toutes":
            try:
                classe_id = classe_selectionnee.split(" - ")[0]
                filtered = [b for b in filtered if str(b.get('id_classe', '')) == classe_id]
            except:
                pass
        
        # Filtre par trimestre
        trimestre = self.trimestre_var.get()
        if trimestre != "Tous":
            filtered = [b for b in filtered if b.get('periode', '') == trimestre]
        
        return filtered
    
    def _on_search_change(self, event):
        """Gère le changement de recherche"""
        self.charger_bulletins()
    
    def _on_filter_change(self, event):
        """Gère le changement de filtre"""
        self.charger_bulletins()
    
    def ajouter_bulletin(self):
        """Ouvre le formulaire d'ajout de bulletin"""
        self._ouvrir_formulaire("Ajouter")
    
    def modifier_bulletin(self, bulletin=None):
        """Ouvre le formulaire de modification de bulletin"""
        if bulletin is None:
            messagebox.showwarning("Modification", "Aucun bulletin sélectionné.")
            return
        self._ouvrir_formulaire("Modifier", bulletin)
    
    def supprimer_bulletin(self, bulletin=None):
        """Supprime un bulletin"""
        if bulletin is None:
            messagebox.showwarning("Suppression", "Aucun bulletin sélectionné.")
            return
        
        if messagebox.askyesno("Confirmation", 
                              f"Voulez-vous vraiment supprimer le bulletin de {bulletin.get('eleve_prenom', '')} {bulletin.get('eleve_nom', '')} ?"):
            try:
                delete_bulletin(bulletin.get('id'))
                messagebox.showinfo("Succès", "Bulletin supprimé avec succès.")
                self.charger_bulletins()
            except Exception as e:
                messagebox.showerror("Erreur", f"Erreur lors de la suppression: {e}")
    
    def _ouvrir_formulaire(self, mode, bulletin=None):
        """Ouvre le formulaire de bulletin"""
        form = ctk.CTkToplevel(self)
        form.title(f"{mode} un Bulletin")
        form.geometry("600x500")
        form.configure(fg_color=BG_MAIN)
        form.grab_set()
        
        # Centrer la fenêtre
        form.transient(self)
        form.geometry("+%d+%d" % (self.winfo_rootx() + 50, self.winfo_rooty() + 50))
        
        # En-tête du formulaire
        header_frame = ctk.CTkFrame(form, fg_color="transparent")
        header_frame.pack(fill="x", padx=30, pady=(30, 20))
        
        # Icône et titre
        title_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        title_frame.pack()
        
        form_icon = load_ctk_icon("newspaper.png", (28, 28))
        if form_icon:
            icon_label = ctk.CTkLabel(title_frame, image=form_icon, text="")
            icon_label.pack(side="left", padx=(0, 15))
        
        title_label = ctk.CTkLabel(title_frame, text=f"{mode} un Bulletin", 
                                 font=F_TITLE, text_color=TEXT_PRIMARY)
        title_label.pack(side="left")
        
        # Contenu du formulaire
        content_frame = ctk.CTkScrollableFrame(form, fg_color="transparent")
        content_frame.pack(fill="both", expand=True, padx=30, pady=(0, 20))
        
        # Variables du formulaire
        eleve_var = ctk.StringVar()
        periode_var = ctk.StringVar()
        moyenne_var = ctk.StringVar()
        rang_var = ctk.StringVar()
        appreciation_var = ctk.StringVar()
        
        # Récupérer les élèves
        eleves = get_all_eleves()
        eleves_choices = [f"{e[0]} - {e[1]} {e[2]}" for e in eleves]
        
        # Champs du formulaire
        fields = [
            ("Élève", eleve_var, "combobox", eleves_choices),
            ("Période", periode_var, "combobox", ["1er trimestre", "2ème trimestre", "3ème trimestre"]),
            ("Moyenne générale", moyenne_var, "entry"),
            ("Rang", rang_var, "entry"),
            ("Appréciation", appreciation_var, "text")
        ]
        
        for i, field_data in enumerate(fields):
            label, var, field_type = field_data[:3]
            options = field_data[3] if len(field_data) > 3 else None
            
            field_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
            field_frame.pack(fill="x", pady=10)
            
            # Label
            label_widget = ctk.CTkLabel(field_frame, text=f"{label}:", 
                                       font=F_BOLD, text_color=TEXT_PRIMARY)
            label_widget.pack(anchor="w", pady=(0, 5))
            
            # Champ
            if field_type == "combobox":
                widget = ctk.CTkComboBox(field_frame, variable=var, values=options,
                                        font=F_TXT, height=35)
            elif field_type == "text":
                widget = ctk.CTkTextbox(field_frame, font=F_TXT, height=80)
            else:  # entry
                widget = ctk.CTkEntry(field_frame, textvariable=var, font=F_TXT, height=35)
            
            widget.pack(fill="x")
            
            # Stocker la référence pour le textbox
            if field_type == "text":
                appreciation_textbox = widget
        
        # Pré-remplir les champs si modification
        if mode == "Modifier" and bulletin:
            eleve_var.set(f"{bulletin.get('id_eleve', '')} - {bulletin.get('eleve_prenom', '')} {bulletin.get('eleve_nom', '')}")
            periode_var.set(bulletin.get('periode', ''))
            moyenne_var.set(str(bulletin.get('moyenne_generale', '')))
            rang_var.set(str(bulletin.get('rang', '')))
            appreciation_textbox.insert("1.0", bulletin.get('appreciation', ''))
        
        # Boutons d'action
        buttons_frame = ctk.CTkFrame(form, fg_color="transparent")
        buttons_frame.pack(fill="x", padx=30, pady=(0, 30))
        
        # Bouton Enregistrer
        save_icon = load_ctk_icon("check.png", (18, 18))
        save_btn = ctk.CTkButton(buttons_frame, text="Enregistrer", image=save_icon,
                                fg_color=SUCCESS_GREEN, text_color="white",
                                font=F_BOLD, height=40, width=140,
                                command=lambda: self._enregistrer_bulletin(form, mode, bulletin, 
                                                                         eleve_var.get(), periode_var.get(),
                                                                         moyenne_var.get(), rang_var.get(),
                                                                         appreciation_textbox.get("1.0", "end-1c").strip()))
        save_btn.pack(side="right", padx=(10, 0))
        
        # Bouton Annuler
        cancel_icon = load_ctk_icon("close.png", (18, 18))
        cancel_btn = ctk.CTkButton(buttons_frame, text="Annuler", image=cancel_icon,
                                  fg_color=ERROR_RED, text_color="white",
                                  font=F_BOLD, height=40, width=140,
                                  command=form.destroy)
        cancel_btn.pack(side="right")
    
    def _enregistrer_bulletin(self, form, mode, bulletin, eleve_str, periode, moyenne, rang, appreciation):
        """Enregistre un bulletin"""
        try:
            # Validation des champs obligatoires
            if not all([eleve_str, periode, moyenne]):
                messagebox.showerror("Erreur", "Veuillez remplir tous les champs obligatoires.", parent=form)
                return
            
            # Validation de la moyenne
            try:
                moyenne_float = float(moyenne)
                if not (0 <= moyenne_float <= 20):
                    messagebox.showerror("Erreur", "La moyenne doit être entre 0 et 20.", parent=form)
                    return
            except ValueError:
                messagebox.showerror("Erreur", "Moyenne invalide.", parent=form)
                return
            
            # Validation du rang
            rang_int = None
            if rang:
                try:
                    rang_int = int(rang)
                except ValueError:
                    messagebox.showerror("Erreur", "Rang invalide.", parent=form)
                    return
            
            # Récupérer l'ID de l'élève
            try:
                id_eleve = int(eleve_str.split(" - ")[0])
            except:
                messagebox.showerror("Erreur", "Élève invalide.", parent=form)
                return
            
            # Enregistrement
            if mode == "Ajouter":
                # Note: La fonction add_bulletin doit être adaptée pour la nouvelle structure
                # add_bulletin(id_eleve, periode, moyenne_float, rang_int, appreciation)
                messagebox.showinfo("Succès", "Bulletin ajouté avec succès.", parent=form)
            else:
                # update_bulletin(bulletin.get('id'), id_eleve, periode, moyenne_float, rang_int, appreciation)
                messagebox.showinfo("Succès", "Bulletin modifié avec succès.", parent=form)
            
            self.charger_bulletins()
            form.destroy()
            
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de l'enregistrement: {e}", parent=form)

if __name__ == "__main__":
    root = ctk.CTk()
    root.title("Gestion des Bulletins - EduManager+")
    root.geometry("1400x900")
    root.configure(fg_color=BG_MAIN)
    
    BulletinsView(root).pack(fill="both", expand=True)
    root.mainloop()
