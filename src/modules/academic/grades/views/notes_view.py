import customtkinter as ctk
from tkinter import messagebox, filedialog
import os
import sys
import csv
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
from tkinter import Toplevel
from CTkTable import CTkTable
from datetime import datetime

# Import du système d'optimisation
try:
    from src.core.database.optimized_queries import (
        get_all_eleves_fast, get_all_classes_fast, get_all_matieres_fast, 
        get_notes_by_eleve_fast
    )
    print("✅ Requêtes optimisées importées pour NotesView")
    USE_OPTIMIZED_QUERIES = False
except ImportError as e:
    print(f"⚠️ Requêtes optimisées non disponibles: {e}")
    USE_OPTIMIZED_QUERIES = False

# Assurez-vous que ces chemins sont corrects pour votre structure de projet
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.modules.academic.grades.controllers.notes_controller import get_all_notes, add_note, update_note, delete_note, get_notes_by_eleve, get_notes_by_trimestre, get_notes_summary_by_eleve
from src.modules.academic.students.controllers.eleve_controller import get_all_eleves
from src.modules.academic.subjects.controllers.matiere_controller import get_all_matieres
from src.modules.academic.classes.controllers.classe_controller import get_all_classes

# Import du thème global
try:
    from resources.themes.theme import *
    print("✅ Thème global importé pour les notes")
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
    MARGIN_SMALL = 8
    MARGIN_MEDIUM = 12
    MARGIN_LARGE = 20
    FONT = "Segoe UI"
    FONT_SIZE_TITLE = 24
    FONT_SIZE_HEADER = 18
    FONT_SIZE_TEXT = 14
    FONT_SIZE_SMALL = 12

def load_ctk_icon(icon_name, size=(20, 20)):
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
            print(f"⚠️ Icône non trouvée: {icon_path}")
            return None
    except Exception as e:
        print(f"⚠️ Erreur chargement icône {icon_name}: {e}")
        return None

ICON_MAP = {
    "add": "add.png", "edit": "edit.png", "delete": "delete.png",
    "refresh": "refresh.png", "search": "search.png", "close": "close.png",
    "student": "person.png", "subject": "book.png", "notes": "assignment.png",
    "date": "calendar.png", "export": "csv.png", "stats": "analytics.png",
    "grade": "grade.png", "class": "classroom.png", "sort": "sort.png"
}
    
class NotesView(ctk.CTkFrame):
    def __init__(self, parent, icons):
        super().__init__(parent, fg_color=BG_MAIN)
        self.icons = icons
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.selected_item_data = None
        self.selected_eleve_data = None
        self.selected_note_id = None
        self.selected_trimestre = "1er Trimestre"  # Valeur par défaut
        
        # Variables pour la pagination
        self.current_page = 1
        self.items_per_page = 10
        self.total_pages = 1
        
        # Cache pour optimiser les performances
        self._data_cache = {}
        self._cache_timestamp = 0
        self._cache_duration = 30  # Cache valide pendant 30 secondes
        
        print("🚀 Chargement des données NotesView...")
        
        # Chargement initial des données avec cache
        self._load_cached_data()
        
        print("✅ Données NotesView chargées")
        self._build_main_ui()

    def _load_cached_data(self):
        """Charge les données avec système de cache pour optimiser les performances"""
        import time
        current_time = time.time()
        
        # Vérifier si le cache est encore valide
        if (current_time - self._cache_timestamp) < self._cache_duration and self._data_cache:
            print("📋 Utilisation du cache pour les données")
            self.eleves = self._data_cache.get('eleves', {})
            self.classes = self._data_cache.get('classes', {})
            self.matieres = self._data_cache.get('matieres', {})
            return
        
        print("🔄 Chargement des données depuis la base...")
        try:
            # Chargement progressif pour éviter le blocage
            self._load_data_progressively()
            
        except Exception as e:
            print(f"⚠️ Erreur chargement données: {e}")
            # Fallback avec données vides
            self.eleves = {}
            self.classes = {}
            self.matieres = {}
    
    def _load_data_progressively(self):
        """Charge les données de manière progressive pour éviter le blocage"""
        import time
        
        # Charger d'abord les matières (plus légères)
        print("📚 Chargement des matières...")
        self.matieres = {}
        try:
            matieres_data = get_all_matieres()
            self.matieres = {m.get("id_matiere", m.get("id", 0)): m for m in matieres_data} if matieres_data else {}
            print(f"✅ {len(self.matieres)} matières guinéennes chargées")
        except Exception as e:
            print(f"⚠️ Erreur chargement matières: {e}")
        
        # Charger les classes
        print("🏫 Chargement des classes...")
        self.classes = {}
        try:
            classes_data = get_all_classes()
            self.classes = {c.get("id", 0): c for c in classes_data} if classes_data else {}
            print(f"✅ {len(self.classes)} classes chargées")
        except Exception as e:
            print(f"⚠️ Erreur chargement classes: {e}")
        
        # Charger les élèves par lots (limité à 100 pour éviter le blocage)
        print("👥 Chargement des élèves (lot limité)...")
        self.eleves = {}
        try:
            eleves_data = get_all_eleves()
            # Limiter à 100 élèves pour éviter le blocage
            limited_eleves = eleves_data[:100] if eleves_data else []
            self.eleves = {e.get("id_eleve", e.get("id", 0)): e for e in limited_eleves}
            print(f"✅ {len(self.eleves)} élèves chargés (limité à 100)")
        except Exception as e:
            print(f"⚠️ Erreur chargement élèves: {e}")
        
        # Mise à jour du cache
        self._data_cache = {
            'eleves': self.eleves,
            'classes': self.classes,
            'matieres': self.matieres
        }
        self._cache_timestamp = time.time()
        
        print(f"✅ Données chargées: {len(self.eleves)} élèves, {len(self.classes)} classes, {len(self.matieres)} matières guinéennes")

    def _refresh_all(self):
        """Rafraîchit toutes les données en invalidant le cache"""
        print("🔄 Rafraîchissement des données...")
        self._cache_timestamp = 0  # Invalider le cache
        self._load_cached_data()
        
        self.selected_eleve_data = None
        self.selected_note_id = None
        
        self._setup_class_dropdown()
        self._clear_dashboard()
        self._update_eleve_list()
        
    def _build_main_ui(self):
        main_frame = ctk.CTkFrame(self, fg_color="transparent")
        main_frame.pack(fill="both", expand=True, padx=15, pady=15)
        main_frame.grid_columnconfigure(1, weight=3)
        main_frame.grid_columnconfigure(0, weight=1)
        main_frame.grid_rowconfigure(0, weight=1)

        # Panneau de gauche: Sélection des élèves
        left_panel = ctk.CTkFrame(main_frame, fg_color=BG_CARD, corner_radius=12)
        left_panel.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        left_panel.grid_columnconfigure(0, weight=1)
        left_panel.grid_rowconfigure(3, weight=1)
        
        self._build_student_selection_panel(left_panel)
        
        # Panneau de droite: Graphique, stats et tableau des notes
        right_panel = ctk.CTkFrame(main_frame, fg_color="transparent")
        right_panel.grid(row=0, column=1, sticky="nsew", padx=(10, 0))
        right_panel.grid_columnconfigure(0, weight=1)
        right_panel.grid_rowconfigure(0, weight=1)
        right_panel.grid_rowconfigure(1, weight=4)
        
        self._build_notes_dashboard(right_panel)
        
    def _build_student_selection_panel(self, parent_frame):
        header_frame = ctk.CTkFrame(parent_frame, fg_color="transparent")
        header_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=(10, 5))
        header_frame.grid_columnconfigure(0, weight=1)
        
        # Titre avec icône
        title_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        title_frame.grid(row=0, column=0, sticky="w")
        
        student_icon = load_ctk_icon(ICON_MAP.get("student"), size=(20, 20))
        ctk.CTkLabel(title_frame, text="", image=student_icon).pack(side="left", padx=(0, 8))
        ctk.CTkLabel(title_frame, text="NOTES ÉLÈVES", 
                      font=(FONT, FONT_SIZE_HEADER, "bold"),
                      text_color=TEXT_PRIMARY).pack(side="left")
        
        refresh_icon = load_ctk_icon(ICON_MAP.get("refresh"), size=(20, 20))
        ctk.CTkButton(header_frame, text="", image=refresh_icon, width=35,
                      fg_color="transparent", hover_color=BORDER_COLOR,
                      command=self._refresh_all).grid(row=0, column=1, sticky="e")
        
        selection_frame = ctk.CTkFrame(parent_frame, fg_color="transparent")
        selection_frame.grid(row=1, column=0, sticky="ew", padx=10, pady=2)
        selection_frame.grid_columnconfigure(0, weight=1)
        selection_frame.grid_rowconfigure(0, weight=1)
        selection_frame.grid_rowconfigure(1, weight=1)
        
        # Sélection de classe
        classe_frame = ctk.CTkFrame(selection_frame, fg_color="transparent")
        classe_frame.grid(row=0, column=0, sticky="ew", pady=1)
        classe_frame.grid_columnconfigure(1, weight=1)
        
        ctk.CTkLabel(classe_frame, text="Classe:", 
                     font=(FONT, FONT_SIZE_TEXT), 
                     text_color=TEXT_PRIMARY).grid(row=0, column=0, sticky="w", padx=(0, 5))
        
        classe_options = ["Classe..."] + [c["nom"] for c in self.classes.values()]
        self.classe_dropdown = ctk.CTkComboBox(
            classe_frame, values=classe_options,
            command=self._on_classe_selected,
            font=(FONT, FONT_SIZE_TEXT),
            fg_color=BG_CARD,
            dropdown_fg_color=BG_CARD,
            dropdown_hover_color=BORDER_COLOR,
            border_color=BORDER_COLOR
        )
        self.classe_dropdown.grid(row=0, column=1, sticky="ew", padx=(5, 0))
        
        # Sélection de trimestre
        trimestre_frame = ctk.CTkFrame(selection_frame, fg_color="transparent")
        trimestre_frame.grid(row=1, column=0, sticky="ew", pady=1)
        trimestre_frame.grid_columnconfigure(1, weight=1)
        
        ctk.CTkLabel(trimestre_frame, text="Trimestre:", 
                     font=(FONT, FONT_SIZE_TEXT), 
                     text_color=TEXT_PRIMARY).grid(row=0, column=0, sticky="w", padx=(0, 5))
        
        trimestre_options = ["Trimestres...", "1er Trimestre", "2ème Trimestre", "3ème Trimestre"]
        self.trimestre_dropdown = ctk.CTkComboBox(
            trimestre_frame, values=trimestre_options,
            command=self._on_trimestre_selected,
            font=(FONT, FONT_SIZE_TEXT),
            fg_color=BG_CARD,
            dropdown_fg_color=BG_CARD,
            dropdown_hover_color=BORDER_COLOR,
            border_color=BORDER_COLOR
        )
        self.trimestre_dropdown.grid(row=0, column=1, sticky="ew", padx=(5, 0))
        self.trimestre_dropdown.set("1er Trimestre")
        
        # Recherche d'élève
        search_frame = ctk.CTkFrame(selection_frame, fg_color="transparent")
        search_frame.grid(row=2, column=0, sticky="ew", pady=1)
        search_frame.grid_columnconfigure(0, weight=1)
        
        self.search_entry = ctk.CTkEntry(
            search_frame, placeholder_text="Rechercher un élève...",
            font=(FONT, FONT_SIZE_TEXT),
            fg_color=BG_CARD,
            border_color=BORDER_COLOR
        )
        self.search_entry.grid(row=0, column=0, sticky="ew")
        self.search_entry.bind("<KeyRelease>", self._filter_eleves)
        
        self.eleve_list_frame = ctk.CTkScrollableFrame(parent_frame, fg_color=BG_CARD)
        self.eleve_list_frame.grid(row=3, column=0, sticky="nsew", padx=10, pady=(2, 10))
        
        self._setup_class_dropdown()
        self._update_eleve_list()

    def _on_trimestre_selected(self, selected_trimestre):
        """Gère la sélection d'un trimestre"""
        if selected_trimestre == "Tous les trimestres":
            self.selected_trimestre = None
        else:
            self.selected_trimestre = selected_trimestre
        
        print(f"🔄 Trimestre sélectionné: {selected_trimestre}")
        print(f"🔍 Filtre trimestre appliqué: {self.selected_trimestre}")
        
        # Recharger les notes de l'élève sélectionné avec le filtre trimestre
        if self.selected_eleve_data:
            self.rafraichir_liste()

    def _build_notes_dashboard(self, parent_frame):
        top_dashboard = ctk.CTkFrame(parent_frame, fg_color="transparent")
        top_dashboard.grid(row=0, column=0, sticky="nsew")
        top_dashboard.grid_columnconfigure(0, weight=2)
        top_dashboard.grid_columnconfigure(1, weight=1)
        
        self.chart_frame = ctk.CTkFrame(top_dashboard, fg_color=BG_CARD, corner_radius=12)
        self.chart_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 10), pady=(0, 1))
        self.chart_frame.grid_propagate(False)
        
        self.stats_container = ctk.CTkFrame(top_dashboard, fg_color=BG_CARD, corner_radius=12)
        self.stats_container.grid(row=0, column=1, sticky="nsew", padx=(10, 0), pady=(0, 15))
        self.stats_container.grid_propagate(False)

        self.table_panel = ctk.CTkFrame(parent_frame, fg_color=BG_CARD, corner_radius=12)
        self.table_panel.grid(row=1, column=0, sticky="nsew", pady=(15, 0))
        self.table_panel.grid_columnconfigure(0, weight=1)
        self.table_panel.grid_rowconfigure(1, weight=1)
        
        self._build_table_header(self.table_panel)
        self.table_container = ctk.CTkFrame(self.table_panel, fg_color="transparent")
        self.table_container.grid(row=1, column=0, sticky="nsew", padx=10, pady=(0, 10))
        
        self._clear_dashboard()
    
    def _build_table_header(self, parent_frame):
        header_frame = ctk.CTkFrame(parent_frame, fg_color="transparent")
        header_frame.grid(row=0, column=0, sticky="ew", padx=15, pady=3)
        header_frame.grid_columnconfigure(0, weight=1)
        
        self.notes_title = ctk.CTkLabel(header_frame, text="Détails des notes",
                                        font=(FONT, FONT_SIZE_HEADER, "bold"),
                                        text_color=TEXT_PRIMARY)
        self.notes_title.grid(row=0, column=0, sticky="w")
        
        actions_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        actions_frame.grid(row=0, column=1, sticky="e")
        
        add_icon = load_ctk_icon(ICON_MAP.get("add"), size=(18, 18))
        edit_icon = load_ctk_icon(ICON_MAP.get("edit"), size=(18, 18))
        delete_icon = load_ctk_icon(ICON_MAP.get("delete"), size=(18, 18))
        export_icon = load_ctk_icon(ICON_MAP.get("export"), size=(18, 18))

        ctk.CTkButton(actions_frame, text="", image=add_icon,
                      fg_color="transparent", hover_color=BORDER_COLOR,
                      width=35, height=35, command=self.ajouter).pack(side="left", padx=3)
        ctk.CTkButton(actions_frame, text="", image=edit_icon,
                      fg_color="transparent", hover_color=BORDER_COLOR,
                      width=35, height=35, command=self.modifier).pack(side="left", padx=3)
        ctk.CTkButton(actions_frame, text="", image=delete_icon,
                      fg_color="transparent", hover_color=BORDER_COLOR,
                      width=35, height=35, command=self.supprimer).pack(side="left", padx=3)
        ctk.CTkButton(actions_frame, text="", image=export_icon,
                      fg_color="transparent", hover_color=BORDER_COLOR,
                      width=35, height=35, command=self.exporter_notes).pack(side="left", padx=3)
    
    def _setup_class_dropdown(self):
        classe_options = ["Classe..."] + [c["nom"] for c in self.classes.values()]
        self.classe_dropdown.configure(values=classe_options)
        self.classe_dropdown.set("Classe...")

    def _on_classe_selected(self, selected_class_name):
        self.selected_eleve_data = None
        self.selected_trimestre = None
        self._clear_dashboard()
        
        # Recharger les élèves de la classe sélectionnée
        if selected_class_name != "Classe...":
            classe_id = next((cid for cid, cdata in self.classes.items() if cdata.get("nom") == selected_class_name), None)
            if classe_id:
                print(f"🔄 Chargement des élèves de la classe {selected_class_name} (ID: {classe_id})")
                try:
                    # Charger TOUS les élèves de cette classe spécifique
                    eleves_classe = get_all_eleves(classe_id=classe_id)
                    
                    # Filtrer pour ne garder que les élèves qui ont des notes (approche optimisée)
                    from database.connection import get_db_connection
                    conn = get_db_connection()
                    cur = conn.cursor()
                    
                    # Requête pour récupérer TOUS les élèves de la classe (avec ou sans notes)
                    cur.execute("""
                        SELECT e.id_eleve, e.nom, e.prenom, e.genre, e.date_naissance, e.statut, e.id_classe,
                               CASE WHEN n.id_note IS NOT NULL THEN 'Avec notes' ELSE 'Sans notes' END as statut_notes
                        FROM eleves e
                        LEFT JOIN notes n ON e.id_eleve = n.id_eleve
                        WHERE e.id_classe = ?
                        ORDER BY statut_notes DESC, e.nom, e.prenom
                    """, (classe_id,))
                    
                    eleves_avec_notes_data = cur.fetchall()
                    conn.close()
                    
                    # Convertir en dictionnaires
                    eleves_avec_notes = []
                    for row in eleves_avec_notes_data:
                        eleve_dict = {
                            'id_eleve': row[0],
                            'nom': row[1],
                            'prenom': row[2],
                            'genre': row[3] if row[3] else 'Non spécifié',
                            'date_naissance': row[4] if row[4] else None,
                            'statut': row[5] if row[5] else 'Actif',
                            'id_classe': row[6] if row[6] else None,
                            'statut_notes': row[7] if len(row) > 7 else 'Sans notes'
                        }
                        eleves_avec_notes.append(eleve_dict)
                    
                    # Mettre à jour le cache des élèves (avec et sans notes)
                    self.eleves = {e.get("id_eleve", e.get("id", 0)): e for e in eleves_avec_notes}
                    
                    # Compter les élèves avec et sans notes
                    eleves_avec_notes_count = sum(1 for e in eleves_avec_notes if e.get('statut_notes') == 'Avec notes')
                    eleves_sans_notes_count = sum(1 for e in eleves_avec_notes if e.get('statut_notes') == 'Sans notes')
                    
                    print(f"✅ {len(self.eleves)} élèves chargés pour la classe {selected_class_name}")
                    print(f"   📝 {eleves_avec_notes_count} élèves avec des notes")
                    print(f"   📝 {eleves_sans_notes_count} élèves sans notes")
                        
                except Exception as e:
                    print(f"❌ Erreur lors du chargement des élèves de la classe: {e}")
        
        self._update_eleve_list()

    def _filter_eleves(self, event=None):
        self._update_eleve_list()

    def _update_eleve_list(self):
        search_query = self.search_entry.get().lower()
        
        for widget in self.eleve_list_frame.winfo_children():
            widget.destroy()

        # Les élèves sont déjà filtrés par classe dans _on_classe_selected
        filtered_eleves = list(self.eleves.values())
        
        # Appliquer seulement le filtre de recherche
        if search_query:
            filtered_eleves = [
                e for e in filtered_eleves
                if search_query in f"{e['nom']} {e['prenom']}".lower()
            ]

        if not filtered_eleves:
            no_students_frame = ctk.CTkFrame(self.eleve_list_frame, fg_color="transparent", corner_radius=8)
            no_students_frame.pack(fill="x", padx=5, pady=10)
            
            ctk.CTkLabel(no_students_frame, text="🔍 Aucun élève trouvé", 
                          font=(FONT, FONT_SIZE_TEXT, "italic"),
                          text_color=TEXT_SECONDARY).pack(pady=15)
        
        for eleves in filtered_eleves:
            eleve_name = f"{eleves['nom']} {eleves['prenom']}"
            
            # Créer un frame pour chaque élève avec icône
            eleve_frame = ctk.CTkFrame(self.eleve_list_frame, fg_color="transparent", corner_radius=8)
            eleve_frame.pack(fill="x", padx=5, pady=3)
            
            # Icône élève
            student_icon = load_ctk_icon(ICON_MAP.get("student"), size=(16, 16))
            icon_label = ctk.CTkLabel(eleve_frame, text="", image=student_icon)
            icon_label.pack(side="left", padx=(10, 8), pady=8)
            
            # Nom de l'élève avec indication du statut des notes
            statut_notes = eleves.get('statut_notes', 'Sans notes')
            if statut_notes == 'Sans notes':
                eleve_name_display = f"{eleve_name} (Sans notes)"
                text_color = TEXT_SECONDARY
                font_size = FONT_SIZE_TEXT - 1
            else:
                eleve_name_display = eleve_name
                text_color = TEXT_PRIMARY
                font_size = FONT_SIZE_TEXT
                
            name_label = ctk.CTkLabel(eleve_frame, text=eleve_name_display,
                                      font=(FONT, font_size),
                                      text_color=text_color)
            name_label.pack(side="left", fill="x", expand=True, padx=(0, 10), pady=8)
            
            # Rendre le frame cliquable
            eleve_frame.bind("<Button-1>", lambda e, eleves=eleves: self.display_eleve_notes(eleves))
            icon_label.bind("<Button-1>", lambda e, eleves=eleves: self.display_eleve_notes(eleves))
            name_label.bind("<Button-1>", lambda e, eleves=eleves: self.display_eleve_notes(eleves))
            
            # Effet de survol
            def on_enter(event, frame=eleve_frame):
                frame.configure(fg_color=BORDER_COLOR)
            def on_leave(event, frame=eleve_frame):
                frame.configure(fg_color=BG_CARD)
                
            eleve_frame.bind("<Enter>", on_enter)
            eleve_frame.bind("<Leave>", on_leave)
            icon_label.bind("<Enter>", on_enter)
            icon_label.bind("<Leave>", on_leave)
            name_label.bind("<Enter>", on_enter)
            name_label.bind("<Leave>", on_leave)

    def display_eleve_notes(self, eleve_data):
        statut_notes = eleve_data.get('statut_notes', 'Sans notes')
        print(f"🎯 Sélection de l'élève: {eleve_data.get('prenom', '')} {eleve_data.get('nom', '')} (ID: {eleve_data.get('id_eleve', '')}) - {statut_notes}")
        self.selected_eleve_data = eleve_data
        
        if statut_notes == 'Sans notes':
            self.notes_title.configure(text=f"Notes de : {eleve_data['prenom']} {eleve_data['nom']} (Aucune note)")
            # Afficher un message pour les élèves sans notes
            self._clear_dashboard()
            self._show_no_notes_message()
        else:
            self.notes_title.configure(text=f"Notes de : {eleve_data['prenom']} {eleve_data['nom']}")
            print(f"🔍 Filtre trimestre avant rafraîchissement: {self.selected_trimestre}")
            self.rafraichir_liste()

    def _clear_dashboard(self):
        for widget in self.stats_container.winfo_children():
            widget.destroy()
        for widget in self.chart_frame.winfo_children():
            widget.destroy()
        for widget in self.table_container.winfo_children():
            widget.destroy()
        
        # Message dans le graphique
        ctk.CTkLabel(self.chart_frame, text="📊 Évolution des notes",
                      font=(FONT, FONT_SIZE_HEADER, "bold"),
                      text_color=TEXT_PRIMARY).pack(pady=(20, 10))
        ctk.CTkLabel(self.chart_frame, text="cliquez sur un élève",
                      font=(FONT, FONT_SIZE_TEXT, "italic"),
                      text_color=TEXT_SECONDARY).pack(pady=(0, 20))
        
        # Statistiques par défaut
        self._create_default_stats()
        
        # Tableau vide par défaut
        self._create_empty_table()

    def _create_default_stats(self):
        """Crée les statistiques par défaut avec des valeurs vides"""
        stats_frame = ctk.CTkFrame(self.stats_container, fg_color="transparent")
        stats_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Titre des statistiques
        ctk.CTkLabel(stats_frame, text="📈 Statistiques",
                      font=(FONT, FONT_SIZE_HEADER, "bold"),
                      text_color=TEXT_PRIMARY).pack(pady=(0, 15))
        
        # Statistiques vides
        stats_data = [
            ("Moyenne Générale", "0.00", TEXT_SECONDARY),
            ("Meilleure Note", "0.00", TEXT_SECONDARY),
            ("Pire Note", "0.00", TEXT_SECONDARY),
            ("Nombre de notes", "0", TEXT_SECONDARY)
        ]
        
        for label, value, color in stats_data:
            stat_frame = ctk.CTkFrame(stats_frame, fg_color=BG_CARD, corner_radius=8)
            stat_frame.pack(fill="x", pady=5)
            
            ctk.CTkLabel(stat_frame, text=label,
                          font=(FONT, FONT_SIZE_TEXT - 2),
                          text_color=TEXT_SECONDARY).pack(side="left", padx=10, pady=8)
            
            ctk.CTkLabel(stat_frame, text=value,
                          font=(FONT, FONT_SIZE_TEXT, "bold"),
                          text_color=color).pack(side="right", padx=10, pady=8)

    def _create_empty_table(self):
        """Crée un tableau vide par défaut"""
        # En-têtes du tableau
        headers = ["Matière", "Note", "Coeff.", "Date", "Commentaire"]
        
        # Créer le tableau fixe avec les en-têtes et 10 lignes vides
        self.notes_table = CTkTable(
            master=self.table_container,
            values=[headers] + [["-", "-", "-", "-", "-"]] * 10,  # 10 lignes vides fixes
            colors=[["#2b2952", "#2b2952"], ["#2b2952", "#2b2952"]],
            header_color="#1a1a2e",
            hover_color="#40546c",
            text_color="#E0E6F0",
            font=(FONT, FONT_SIZE_TEXT - 2),
            command=self._on_table_select,
            corner_radius=8
        )
        self.notes_table.pack(fill="both", expand=True, padx=10, pady=10)

    def rafraichir_liste(self):
        self.selected_note_id = None
        self.selected_item_data = None
        
        if self.selected_eleve_data:
            print(f"🔍 Récupération des notes pour l'élève {self.selected_eleve_data.get('id_eleve')} avec filtre trimestre: {self.selected_trimestre}")
            notes = get_notes_by_eleve(self.selected_eleve_data.get("id_eleve"), trimestre=self.selected_trimestre)
            print(f"📊 {len(notes)} notes récupérées")
            self._update_stats_display(notes)
            self._create_grade_evolution_chart(notes)
            self._update_notes_table(notes)
        else:
            self._clear_dashboard()

    def _update_stats_display(self, notes):
        print(f"🔄 Mise à jour des statistiques avec {len(notes)} notes")
        
        for widget in self.stats_container.winfo_children():
            widget.destroy()

        if not notes:
            print("⚠️ Aucune note trouvée, affichage des statistiques par défaut")
            self._create_default_stats()
            return

        try:
            # Convertir les données pour pandas
            notes_for_df = []
            for note in notes:
                note_dict = {
                    'note': float(note.get('note', 0)) if note.get('note') else 0,
                    'coefficient': float(note.get('coefficient', 1)) if note.get('coefficient') else 1
                }
                notes_for_df.append(note_dict)
            
            df = pd.DataFrame(notes_for_df)
            df.dropna(subset=['note', 'coefficient'], inplace=True)

            if not df.empty:
                total_points = (df['note'] * df['coefficient']).sum()
                total_coeff = df['coefficient'].sum()
                moyenne_generale = total_points / total_coeff if total_coeff > 0 else 0
                meilleure_note = df['note'].max()
                pire_note = df['note'].min()
                nombre_notes = len(df)
                
                print(f"✅ Statistiques calculées: Moyenne={moyenne_generale:.2f}, Meilleure={meilleure_note}, Pire={pire_note}, Nb={nombre_notes}")
            else:
                moyenne_generale = meilleure_note = pire_note = nombre_notes = 0
                print("⚠️ DataFrame vide après nettoyage")

            self._create_stats_card(self.stats_container, "Moyenne Générale", f"{moyenne_generale:.2f}", TEXT_ACCENT, ICON_MAP.get("grade"))
            self._create_stats_card(self.stats_container, "Meilleure Note", f"{meilleure_note}", SUCCESS_GREEN, ICON_MAP.get("grade"))
            self._create_stats_card(self.stats_container, "Pire Note", f"{pire_note}", ERROR_RED, ICON_MAP.get("grade"))
            self._create_stats_card(self.stats_container, "Nombre de notes", f"{nombre_notes}", WARNING_YELLOW, ICON_MAP.get("subject"))
            
        except Exception as e:
            print(f"❌ Erreur lors du calcul des statistiques: {e}")
            self._create_default_stats()

    def _create_stats_card(self, parent, title, value, color, icon_name):
        card = ctk.CTkFrame(parent, fg_color=BG_CARD, corner_radius=10, height=60)
        card.pack(fill="x", pady=4, padx=8)
        card.grid_columnconfigure(1, weight=1)
        
        icon = load_ctk_icon(icon_name)
        if icon:
            ctk.CTkLabel(card, text="", image=icon, fg_color="transparent").grid(row=0, column=0, rowspan=2, padx=10, pady=8)
            
        ctk.CTkLabel(card, text=title, font=(FONT, FONT_SIZE_TEXT-2), text_color=TEXT_SECONDARY).grid(row=0, column=1, sticky="w")
        ctk.CTkLabel(card, text=value, font=(FONT, FONT_SIZE_HEADER-2, "bold"), text_color=color).grid(row=1, column=1, sticky="w")

    def _create_grade_evolution_chart(self, notes):
        for widget in self.chart_frame.winfo_children():
            widget.destroy()

        if not notes:
            ctk.CTkLabel(self.chart_frame, text="Aucune donnée à afficher.",
                          font=(FONT, FONT_SIZE_HEADER, "italic"),
                          text_color=TEXT_SECONDARY).pack(expand=True, padx=20, pady=20)
            return

        df = pd.DataFrame(notes)
        df['date'] = pd.to_datetime(df['date_evaluation'], errors='coerce')
        df.sort_values(by='date', inplace=True)
        df.dropna(subset=['date', 'note', 'coefficient'], inplace=True)
        
        fig, ax = plt.subplots(figsize=(6, 4), facecolor=BG_CARD)
        fig.patch.set_facecolor(BG_CARD)
        
        if not df.empty:
            colors = plt.cm.viridis(np.linspace(0, 1, len(df['id_matiere'].unique())))
            for i, (matiere_id, group) in enumerate(df.groupby('id_matiere')):
                matiere_nom = self.matieres.get(matiere_id, {}).get("nom_matiere", "Inconnue")
                ax.plot(group['date'], group['note'], marker='o', linestyle='-', label=matiere_nom, color=colors[i])
            
            # Ajout de la moyenne mobile
            window_size = 3
            df['rolling_avg'] = df['note'].rolling(window=window_size).mean()
            ax.plot(df['date'], df['rolling_avg'], color='red', linestyle='--', label=f'Moyenne mobile ({window_size})', linewidth=2)

        ax.set_title("Évolution des notes", color=TEXT_PRIMARY, font=FONT, fontsize=FONT_SIZE_HEADER)
        ax.set_xlabel("Date", color=TEXT_SECONDARY, font=FONT, fontsize=FONT_SIZE_TEXT-2)
        ax.set_ylabel("Note", color=TEXT_SECONDARY, font=FONT, fontsize=FONT_SIZE_TEXT-2)
        
        ax.tick_params(axis='x', colors=TEXT_SECONDARY, rotation=45, labelsize=10)
        ax.tick_params(axis='y', colors=TEXT_SECONDARY, labelsize=10)
        
        ax.set_facecolor(BG_CARD)
        ax.spines['bottom'].set_color(BORDER_COLOR)
        ax.spines['left'].set_color(BORDER_COLOR)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.legend(facecolor=BG_CARD, edgecolor=BORDER_COLOR, labelcolor=TEXT_SECONDARY, fontsize=10)

        plt.tight_layout()
        
        canvas = FigureCanvasTkAgg(fig, master=self.chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True, padx=10, pady=10)

    def _update_notes_table(self, notes):
        print(f"🔄 Mise à jour du tableau avec {len(notes)} notes")
        
        for widget in self.table_container.winfo_children():
            widget.destroy()
    
    def _show_no_notes_message(self):
        """Affiche un message pour les élèves sans notes"""
        # Message dans les statistiques
        no_stats_frame = ctk.CTkFrame(self.stats_container, fg_color="transparent")
        no_stats_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        ctk.CTkLabel(no_stats_frame, text="📝 Aucune note disponible", 
                     font=(FONT, FONT_SIZE_HEADER), 
                     text_color=TEXT_SECONDARY).pack(pady=10)
        
        ctk.CTkLabel(no_stats_frame, text="Cet élève n'a pas encore de notes", 
                     font=(FONT, FONT_SIZE_TEXT), 
                     text_color=TEXT_SECONDARY).pack()
        
        # Message dans le graphique
        no_chart_frame = ctk.CTkFrame(self.chart_frame, fg_color="transparent")
        no_chart_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        ctk.CTkLabel(no_chart_frame, text="📊 Pas de données à afficher", 
                     font=(FONT, FONT_SIZE_HEADER), 
                     text_color=TEXT_SECONDARY).pack(pady=10)
        
        # Message dans le tableau
        no_table_frame = ctk.CTkFrame(self.table_container, fg_color="transparent")
        no_table_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        ctk.CTkLabel(no_table_frame, text="📋 Tableau vide", 
                     font=(FONT, FONT_SIZE_HEADER), 
                     text_color=TEXT_SECONDARY).pack(pady=10)
        
        ctk.CTkLabel(no_table_frame, text="Aucune note à afficher pour cet élève", 
                     font=(FONT, FONT_SIZE_TEXT), 
                     text_color=TEXT_SECONDARY).pack()

    def _update_notes_table(self, notes):
        print(f"🔄 Mise à jour du tableau avec {len(notes)} notes")
        
        for widget in self.table_container.winfo_children():
            widget.destroy()

        if not notes:
            print("⚠️ Aucune note trouvée, création d'un tableau vide")
            self._create_empty_table()
            return

        # Calculer la pagination
        self.total_pages = max(1, (len(notes) + self.items_per_page - 1) // self.items_per_page)
        start_idx = (self.current_page - 1) * self.items_per_page
        end_idx = start_idx + self.items_per_page
        notes_page = notes[start_idx:end_idx]

        headers = ["Matière", "Note", "Coeff.", "Date", "Trimestre", "Commentaire"]
        data = [headers]
        
        # Ajouter les notes de la page actuelle
        for note in notes_page:
            matiere_id = note.get("id_matiere")
            matiere_nom = self.matieres.get(matiere_id, {}).get("nom_matiere", "Inconnue")
            data.append([
                matiere_nom,
                str(note.get("note", "")),
                str(note.get("coefficient", "")),
                str(note.get("date_evaluation", "")),
                str(note.get("trimestre", "Inconnu")),
                str(note.get("commentaire", "Aucun"))
            ])
        
        print(f"✅ Tableau mis à jour avec {len(data)-1} lignes de notes (page {self.current_page}/{self.total_pages})")
        
        # Compléter avec des lignes vides pour avoir toujours 10 lignes de données
        while len(data) < 11:  # 1 header + 10 lignes de données
            data.append(["-", "-", "-", "-", "-", "-"])
            
        self.note_table = CTkTable(
            self.table_container, 
            values=data, 
            header_color=BG_CARD,
            fg_color=BG_CARD,
            hover_color=BORDER_COLOR,
            text_color=TEXT_PRIMARY,
            font=(FONT, FONT_SIZE_TEXT),
            command=self._on_table_select,
            corner_radius=10,
            wraplength=150
        )
        self.note_table.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Ajouter les contrôles de pagination
        self._add_pagination_controls()
        
        self.notes_data = notes

    def _add_pagination_controls(self):
        """Ajoute les contrôles de pagination"""
        pagination_frame = ctk.CTkFrame(self.table_container, fg_color="transparent")
        pagination_frame.pack(fill="x", padx=10, pady=5)
        
        # Bouton précédent
        prev_btn = ctk.CTkButton(
            pagination_frame,
            text="◀ Précédent",
            width=100,
            height=30,
            command=self._go_to_previous_page,
            state="normal" if self.current_page > 1 else "disabled"
        )
        prev_btn.pack(side="left", padx=5)
        
        # Informations de pagination
        page_info = ctk.CTkLabel(
            pagination_frame,
            text=f"Page {self.current_page} sur {self.total_pages}",
            font=(FONT, FONT_SIZE_TEXT),
            text_color=TEXT_PRIMARY
        )
        page_info.pack(side="left", padx=20)
        
        # Bouton suivant
        next_btn = ctk.CTkButton(
            pagination_frame,
            text="Suivant ▶",
            width=100,
            height=30,
            command=self._go_to_next_page,
            state="normal" if self.current_page < self.total_pages else "disabled"
        )
        next_btn.pack(side="left", padx=5)

    def _go_to_previous_page(self):
        """Va à la page précédente"""
        if self.current_page > 1:
            self.current_page -= 1
            if hasattr(self, 'selected_eleve_data') and self.selected_eleve_data:
                self.rafraichir_liste()

    def _go_to_next_page(self):
        """Va à la page suivante"""
        if self.current_page < self.total_pages:
            self.current_page += 1
            if hasattr(self, 'selected_eleve_data') and self.selected_eleve_data:
                self.rafraichir_liste()

    def _on_table_select(self, cell):
        self.selected_note_id = None
        self.selected_item_data = None
        row_index = cell.get("row")
        if row_index > 0:
            self.selected_note_id = self.notes_data[row_index - 1].get("id_note")
            self.selected_item_data = self.notes_data[row_index - 1]

    def ajouter(self):
        if not self.selected_eleve_data:
            messagebox.showwarning("Ajouter", "Sélectionnez d'abord un élève pour lui ajouter une notes.")
            return
        self.open_note_form("Ajouter")

    def modifier(self):
        if not self.selected_note_id:
            messagebox.showwarning("Modifier", "Sélectionnez une notes à modifier.")
            return
        self.open_note_form("Modifier", self.selected_item_data)

    def supprimer(self):
        if not self.selected_note_id:
            messagebox.showwarning("Supprimer", "Sélectionnez une notes à supprimer.")
            return
        if messagebox.askyesno("Confirmer la suppression", f"Êtes-vous sûr de vouloir supprimer cette notes ?"):
            if delete_note(self.selected_note_id):
                messagebox.showinfo("Succès", "Note supprimée avec succès.")
                self.rafraichir_liste()
            else:
                messagebox.showerror("Erreur", "Échec de la suppression.")

    def open_note_form(self, mode, data=None):
        popup = ctk.CTkToplevel(self)
        popup.title(f"{mode} une Note")
        popup.geometry("450x550")
        popup.configure(fg_color=BG_MAIN)
        popup.grab_set()

        ctk.CTkLabel(popup, text=f"{mode} une Note",
                      font=(FONT, FONT_SIZE_HEADER, "bold"),
                      text_color=TEXT_ACCENT).pack(pady=(20, 10))
        
        form_frame = ctk.CTkFrame(popup, fg_color=BG_CARD, corner_radius=12)
        form_frame.pack(fill="both", expand=True, padx=20, pady=(10, 20))
        form_frame.grid_columnconfigure(0, weight=1)

        # Rendre l'intérieur du formulaire plus compact et aligné
        inner_form_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        inner_form_frame.pack(fill="x", padx=30, pady=20)
        inner_form_frame.grid_columnconfigure(1, weight=1)

        def create_form_entry(parent, label_text, widget_type, row, default_value=None, options=None):
            ctk.CTkLabel(parent, text=label_text,
                          font=(FONT, FONT_SIZE_TEXT),
                          text_color=TEXT_SECONDARY).grid(row=row, column=0, sticky="w", pady=5)
            
            if widget_type == "entry":
                widget = ctk.CTkEntry(parent, font=(FONT, FONT_SIZE_TEXT), fg_color=BG_CARD, border_color=BORDER_COLOR)
                if default_value is not None:
                    widget.insert(0, default_value)
            elif widget_type == "combo":
                widget = ctk.CTkComboBox(parent, values=options, state="readonly",
                                          font=(FONT, FONT_SIZE_TEXT), fg_color=BG_CARD,
                                          border_color=BORDER_COLOR, dropdown_fg_color=BG_CARD,
                                          dropdown_hover_color=BORDER_COLOR)
                if default_value is not None:
                    widget.set(default_value)
            elif widget_type == "textbox":
                widget = ctk.CTkTextbox(parent, height=80, font=(FONT, FONT_SIZE_TEXT), fg_color=BG_CARD, border_color=BORDER_COLOR)
                if default_value is not None:
                    widget.insert("0.0", default_value)
            
            widget.grid(row=row, column=1, sticky="ew", padx=(10, 0), pady=5)
            return widget

        eleve_display_name = f"{self.selected_eleve_data['nom']} {self.selected_eleve_data['prenom']}"
        create_form_entry(inner_form_frame, "Élève:", "entry", 0, default_value=eleve_display_name).configure(state="disabled")

        matiere_options = [""] + [f"{m['id_matiere']} - {m['nom_matiere']}" for m in self.matieres.values()]
        matiere_combo = create_form_entry(inner_form_frame, "Matière:", "combo", 1, options=matiere_options)
        note_entry = create_form_entry(inner_form_frame, "Note:", "entry", 2)
        coeff_entry = create_form_entry(inner_form_frame, "Coefficient:", "entry", 3)
        date_entry = create_form_entry(inner_form_frame, "Date (AAAA-MM-JJ):", "entry", 4)
        comment_entry = create_form_entry(inner_form_frame, "Commentaire:", "textbox", 5)
        
        if mode == "Modifier" and data:
            if data.get("id_matiere") is not None and data["id_matiere"] in self.matieres:
                matiere_info = self.matieres[data["id_matiere"]]
                matiere_combo.set(f"{matiere_info['id_matiere']} - {matiere_info['nom_matiere']}")
            note_entry.insert(0, str(data.get("notes", "")))
            coeff_entry.insert(0, str(data.get("coefficient", "1")))
            date_entry.insert(0, data.get("date_evaluation", ""))
            commentaire_text = data.get("commentaire", "")
            if commentaire_text is not None:
                comment_entry.insert("0.0", str(commentaire_text))

        def save():
            try:
                matiere_str = matiere_combo.get()
                matiere_id = int(matiere_str.split(" - ")[0]) if matiere_str and " - " in matiere_str else None
                note_value = float(note_entry.get())
                coefficient = float(coeff_entry.get())
                date_note = date_entry.get()
                commentaire = comment_entry.get("1.0", "end-1c")
                
                if not matiere_id or note_value is None:
                    messagebox.showerror("Erreur", "Les champs Matière et Note sont obligatoires.", parent=popup)
                    return

                note_data = {
                    "id_eleve": self.selected_eleve_data['id_eleve'],
                    "id_matiere": matiere_id,
                    "notes": note_value,
                    "coefficient": coefficient,
                    "date_evaluation": date_note,
                    "commentaire": commentaire
                }
                
                if mode == "Ajouter":
                    add_note(note_data)
                    messagebox.showinfo("Succès", "Note ajoutée avec succès.", parent=popup)
                else:
                    note_data["id_note"] = data.get("id_note")
                    update_note(note_data)
                    messagebox.showinfo("Succès", "Note mise à jour avec succès.", parent=popup)
                
                self.rafraichir_liste()
                popup.destroy()

            except ValueError:
                messagebox.showerror("Erreur", "La notes et le coefficient doivent être des nombres.", parent=popup)
            except Exception as e:
                messagebox.showerror("Erreur", f"Une erreur s'est produite : {e}", parent=popup)

        btn_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        btn_frame.pack(pady=(10, 20))
        ctk.CTkButton(btn_frame, text="Annuler", command=popup.destroy,
                      fg_color="gray", hover_color="#6e6e6e",
                      font=(FONT, FONT_SIZE_TEXT, "bold")).pack(side="left", padx=10)
        ctk.CTkButton(btn_frame, text="Enregistrer", command=save,
                      fg_color=TEXT_ACCENT, text_color=BG_MAIN,
                      hover_color="#45b69c",
                      font=(FONT, FONT_SIZE_TEXT, "bold")).pack(side="left", padx=10)

    def exporter_notes(self):
        if not self.selected_eleve_data:
            messagebox.showwarning("Exporter", "Sélectionnez un élève pour exporter ses notes.")
            return

        eleve_id = self.selected_eleve_data.get("id_eleve")
        notes = get_notes_by_eleve(eleve_id, trimestre=self.selected_trimestre)
        if not notes:
            messagebox.showwarning("Exporter", "Aucune notes à exporter pour cet élève.")
            return

        file_path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("Fichiers CSV", "*.csv")],
            title="Enregistrer les notes de l'élève"
        )
        if not file_path:
            return

        try:
            with open(file_path, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(["ID", "Élève", "Matière", "Note", "Coefficient", "Date", "Commentaire"])
                for notes in notes:
                    eleve_name = f"{self.eleves.get(notes['id_eleve'], {}).get('nom', 'Inconnu')} {self.eleves.get(notes['id_eleve'], {}).get('prenom', '')}"
                    matiere_name = self.matieres.get(notes["id_matiere"], {}).get("nom", "Inconnue")
                    writer.writerow([
                        notes.get("id_note"),
                        eleve_name,
                        matiere_name,
                        notes.get("notes"),
                        notes.get("coefficient", 1),
                        notes.get("date_evaluation"),
                        notes.get("commentaire")
                    ])
            messagebox.showinfo("Exporter", f"Les notes de l'élève ont été exportées avec succès dans {file_path}")
        except Exception as e:
            messagebox.showerror("Erreur", f"Une erreur s'est produite lors de l'exportation : {e}")