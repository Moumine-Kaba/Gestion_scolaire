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
    USE_OPTIMIZED_QUERIES = True
except ImportError as e:
    print(f"⚠️ Requêtes optimisées non disponibles: {e}")
    USE_OPTIMIZED_QUERIES = False

# Assurez-vous que ces chemins sont corrects pour votre structure de projet
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.modules.academic.grades.controllers.notes_controller import get_all_notes, add_note, update_note, delete_note, get_notes_by_eleve
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
    "student": "person.png", "subject": "book.png", "note": "assignment.png",
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
            # Utiliser les requêtes optimisées si disponibles
            if USE_OPTIMIZED_QUERIES:
                eleves_data = get_all_eleves_fast()
                classes_data = get_all_classes_fast()
                matieres_data = get_all_matieres_fast()
            else:
                # Fallback vers les requêtes normales
                eleves_data = get_all_eleves()
                classes_data = get_all_classes()
                matieres_data = get_all_matieres()
            
            # Conversion en dictionnaires pour un accès rapide
            self.eleves = {e["id"]: e for e in eleves_data} if eleves_data else {}
            self.classes = {c["id"]: c for c in classes_data} if classes_data else {}
            self.matieres = {m["id"]: m for m in matieres_data} if matieres_data else {}
            
            # Mise à jour du cache
            self._data_cache = {
                'eleves': self.eleves,
                'classes': self.classes,
                'matieres': self.matieres
            }
            self._cache_timestamp = current_time
            
            print(f"✅ Données chargées: {len(self.eleves)} élèves, {len(self.classes)} classes, {len(self.matieres)} matières")
            
        except Exception as e:
            print(f"⚠️ Erreur chargement données: {e}")
            # Fallback avec données vides
            self.eleves = {}
            self.classes = {}
            self.matieres = {}

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
        left_panel.grid_rowconfigure(2, weight=1)
        
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
        ctk.CTkLabel(title_frame, text="NOTES DES ÉLÈVES", 
                      font=(FONT, FONT_SIZE_HEADER, "bold"),
                      text_color=TEXT_PRIMARY).pack(side="left")
        
        refresh_icon = load_ctk_icon(ICON_MAP.get("refresh"), size=(20, 20))
        ctk.CTkButton(header_frame, text="", image=refresh_icon, width=35,
                      fg_color="transparent", hover_color=BORDER_COLOR,
                      command=self._refresh_all).grid(row=0, column=1, sticky="e")
        
        selection_frame = ctk.CTkFrame(parent_frame, fg_color="transparent")
        selection_frame.grid(row=1, column=0, sticky="ew", padx=10, pady=5)
        selection_frame.grid_columnconfigure(0, weight=55)
        selection_frame.grid_columnconfigure(1, weight=45)
        
        classe_options = ["Classe..."] + [c["nom"] for c in self.classes.values()]
        self.classe_dropdown = ctk.CTkComboBox(
            selection_frame, values=classe_options,
            command=self._on_classe_selected,
            font=(FONT, FONT_SIZE_TEXT),
            fg_color=BG_CARD,
            dropdown_fg_color=BG_CARD,
            dropdown_hover_color=BORDER_COLOR,
            border_color=BORDER_COLOR
        )
        self.classe_dropdown.grid(row=0, column=0, sticky="ew", padx=(0, 5))
        
        self.search_entry = ctk.CTkEntry(
            selection_frame, placeholder_text="Rechercher...",
            font=(FONT, FONT_SIZE_TEXT),
            fg_color=BG_CARD,
            border_color=BORDER_COLOR
        )
        self.search_entry.grid(row=0, column=1, sticky="ew", padx=(5, 0))
        self.search_entry.bind("<KeyRelease>", self._filter_eleves)
        
        self.eleve_list_frame = ctk.CTkScrollableFrame(parent_frame, fg_color="transparent")
        self.eleve_list_frame.grid(row=2, column=0, sticky="nsew", padx=10, pady=(5, 10))
        
        self._setup_class_dropdown()
        self._update_eleve_list()

    def _build_notes_dashboard(self, parent_frame):
        top_dashboard = ctk.CTkFrame(parent_frame, fg_color="transparent")
        top_dashboard.grid(row=0, column=0, sticky="nsew")
        top_dashboard.grid_columnconfigure(0, weight=2)
        top_dashboard.grid_columnconfigure(1, weight=1)
        
        self.chart_frame = ctk.CTkFrame(top_dashboard, fg_color=BG_CARD, corner_radius=12)
        self.chart_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 10), pady=(0, 1))
        self.chart_frame.grid_propagate(False)
        
        self.stats_container = ctk.CTkFrame(top_dashboard, fg_color=BG_CARD, corner_radius=12)
        self.stats_container.grid(row=0, column=1, sticky="nsew", padx=(10, 0), pady=(0, 1))
        self.stats_container.grid_propagate(False)

        self.table_panel = ctk.CTkFrame(parent_frame, fg_color=BG_CARD, corner_radius=12)
        self.table_panel.grid(row=1, column=0, sticky="nsew", pady=(1, 0))
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
        self._clear_dashboard()
        self._update_eleve_list()

    def _filter_eleves(self, event=None):
        self._update_eleve_list()

    def _update_eleve_list(self):
        search_query = self.search_entry.get().lower()
        selected_classe_name = self.classe_dropdown.get()
        
        for widget in self.eleve_list_frame.winfo_children():
            widget.destroy()

        filtered_eleves = list(self.eleves.values())
        
        if selected_classe_name != "Classe...":
            classe_id = next((cid for cid, cdata in self.classes.items() if cdata["nom"] == selected_classe_name), None)
            if classe_id:
                filtered_eleves = [e for e in filtered_eleves if e.get("classe_id") == classe_id]

        if search_query:
            filtered_eleves = [
                e for e in filtered_eleves
                if search_query in f"{e['nom']} {e['prenom']}".lower()
            ]

        if not filtered_eleves:
            no_students_frame = ctk.CTkFrame(self.eleve_list_frame, fg_color=BG_CARD, corner_radius=8)
            no_students_frame.pack(fill="x", padx=5, pady=10)
            
            ctk.CTkLabel(no_students_frame, text="🔍 Aucun élève trouvé", 
                          font=(FONT, FONT_SIZE_TEXT, "italic"),
                          text_color=TEXT_SECONDARY).pack(pady=15)
        
        for eleve in filtered_eleves:
            eleve_name = f"{eleve['nom']} {eleve['prenom']}"
            
            # Créer un frame pour chaque élève avec icône
            eleve_frame = ctk.CTkFrame(self.eleve_list_frame, fg_color=BG_CARD, corner_radius=8)
            eleve_frame.pack(fill="x", padx=5, pady=3)
            
            # Icône élève
            student_icon = load_ctk_icon(ICON_MAP.get("student"), size=(16, 16))
            icon_label = ctk.CTkLabel(eleve_frame, text="", image=student_icon)
            icon_label.pack(side="left", padx=(10, 8), pady=8)
            
            # Nom de l'élève
            name_label = ctk.CTkLabel(eleve_frame, text=eleve_name,
                                      font=(FONT, FONT_SIZE_TEXT),
                                      text_color=TEXT_PRIMARY)
            name_label.pack(side="left", fill="x", expand=True, padx=(0, 10), pady=8)
            
            # Rendre le frame cliquable
            eleve_frame.bind("<Button-1>", lambda e, eleve=eleve: self.display_eleve_notes(eleve))
            icon_label.bind("<Button-1>", lambda e, eleve=eleve: self.display_eleve_notes(eleve))
            name_label.bind("<Button-1>", lambda e, eleve=eleve: self.display_eleve_notes(eleve))
            
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
        self.selected_eleve_data = eleve_data
        self.notes_title.configure(text=f"Notes de : {eleve_data['prenom']} {eleve_data['nom']}")
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
            notes = get_notes_by_eleve(self.selected_eleve_data.get("id"))
            self._update_stats_display(notes)
            self._create_grade_evolution_chart(notes)
            self._update_notes_table(notes)
        else:
            self._clear_dashboard()

    def _update_stats_display(self, notes):
        for widget in self.stats_container.winfo_children():
            widget.destroy()

        if not notes:
            self._create_default_stats()
            return

        df = pd.DataFrame(notes)
        df.dropna(subset=['note', 'coefficient'], inplace=True)

        if not df.empty:
            total_points = (df['note'] * df['coefficient']).sum()
            total_coeff = df['coefficient'].sum()
            moyenne_generale = total_points / total_coeff if total_coeff > 0 else 0
            meilleure_note = df['note'].max()
            pire_note = df['note'].min()
            nombre_notes = len(df)
        else:
            moyenne_generale = meilleure_note = pire_note = nombre_notes = 0

        self._create_stats_card(self.stats_container, "Moyenne Générale", f"{moyenne_generale:.2f}", TEXT_ACCENT, ICON_MAP.get("grade"))
        self._create_stats_card(self.stats_container, "Meilleure Note", f"{meilleure_note}", SUCCESS_GREEN, ICON_MAP.get("grade"))
        self._create_stats_card(self.stats_container, "Pire Note", f"{pire_note}", ERROR_RED, ICON_MAP.get("grade"))
        self._create_stats_card(self.stats_container, "Nombre de notes", f"{nombre_notes}", WARNING_YELLOW, ICON_MAP.get("subject"))

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
                matiere_nom = self.matieres.get(matiere_id, {}).get("nom", "Inconnue")
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
        for widget in self.table_container.winfo_children():
            widget.destroy()

        if not notes:
            self._create_empty_table()
            return

        headers = ["Matière", "Note", "Coeff.", "Date", "Commentaire"]
        data = [headers]
        
        # Ajouter les notes existantes
        for note in notes:
            matiere_nom = self.matieres.get(note.get("id_matiere"), {}).get("nom", "Inconnue")
            data.append([
                matiere_nom,
                note.get("note"),
                note.get("coefficient"),
                note.get("date_evaluation"),
                note.get("commentaire", "Aucun")
            ])
        
        # Compléter avec des lignes vides pour avoir toujours 10 lignes de données
        while len(data) < 11:  # 1 header + 10 lignes de données
            data.append(["-", "-", "-", "-", "-"])
            
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
        
        self.notes_data = notes

    def _on_table_select(self, cell):
        self.selected_note_id = None
        self.selected_item_data = None
        row_index = cell.get("row")
        if row_index > 0:
            self.selected_note_id = self.notes_data[row_index - 1].get("id_note")
            self.selected_item_data = self.notes_data[row_index - 1]

    def ajouter(self):
        if not self.selected_eleve_data:
            messagebox.showwarning("Ajouter", "Sélectionnez d'abord un élève pour lui ajouter une note.")
            return
        self.open_note_form("Ajouter")

    def modifier(self):
        if not self.selected_note_id:
            messagebox.showwarning("Modifier", "Sélectionnez une note à modifier.")
            return
        self.open_note_form("Modifier", self.selected_item_data)

    def supprimer(self):
        if not self.selected_note_id:
            messagebox.showwarning("Supprimer", "Sélectionnez une note à supprimer.")
            return
        if messagebox.askyesno("Confirmer la suppression", f"Êtes-vous sûr de vouloir supprimer cette note ?"):
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

        matiere_options = [""] + [f"{m['id']} - {m['nom']}" for m in self.matieres.values()]
        matiere_combo = create_form_entry(inner_form_frame, "Matière:", "combo", 1, options=matiere_options)
        note_entry = create_form_entry(inner_form_frame, "Note:", "entry", 2)
        coeff_entry = create_form_entry(inner_form_frame, "Coefficient:", "entry", 3)
        date_entry = create_form_entry(inner_form_frame, "Date (AAAA-MM-JJ):", "entry", 4)
        comment_entry = create_form_entry(inner_form_frame, "Commentaire:", "textbox", 5)
        
        if mode == "Modifier" and data:
            if data.get("id_matiere") is not None and data["id_matiere"] in self.matieres:
                matiere_info = self.matieres[data["id_matiere"]]
                matiere_combo.set(f"{matiere_info['id']} - {matiere_info['nom']}")
            note_entry.insert(0, str(data.get("note", "")))
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
                    "id_eleve": self.selected_eleve_data['id'],
                    "id_matiere": matiere_id,
                    "note": note_value,
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
                messagebox.showerror("Erreur", "La note et le coefficient doivent être des nombres.", parent=popup)
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

        eleve_id = self.selected_eleve_data.get("id")
        notes = get_notes_by_eleve(eleve_id)
        if not notes:
            messagebox.showwarning("Exporter", "Aucune note à exporter pour cet élève.")
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
                for note in notes:
                    eleve_name = f"{self.eleves.get(note['id_eleve'], {}).get('nom', 'Inconnu')} {self.eleves.get(note['id_eleve'], {}).get('prenom', '')}"
                    matiere_name = self.matieres.get(note["id_matiere"], {}).get("nom", "Inconnue")
                    writer.writerow([
                        note.get("id_note"),
                        eleve_name,
                        matiere_name,
                        note.get("note"),
                        note.get("coefficient", 1),
                        note.get("date_evaluation"),
                        note.get("commentaire")
                    ])
            messagebox.showinfo("Exporter", f"Les notes de l'élève ont été exportées avec succès dans {file_path}")
        except Exception as e:
            messagebox.showerror("Erreur", f"Une erreur s'est produite lors de l'exportation : {e}")