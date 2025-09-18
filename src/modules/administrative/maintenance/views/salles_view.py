import tkinter as tk
from tkinter import messagebox
import customtkinter as ctk
import os
# Remplacé par SQL Server  # Remplacé par SQL Server
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
from PIL import Image

# Import du thème global EduManager+
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..', '..'))
from resources.themes.theme import (
    BG_MAIN, BG_SIDEBAR, CARD_BG, BORDER_COLOR, LIGHT_BLUE, TEXT, MUTED,
    SUCCESS_GREEN, WARNING_YELLOW, ERROR_RED, INFO_ORANGE,
    HOVER_PRIMARY, FOCUS_PRIMARY, FONT_PRIMARY, FONT_TITLE, FONT_SUBTITLE,
    FONT_HERO, FONT_CARD_TITLE,
    GRADIENT_PRIMARY, GRADIENT_ACCENT, SHADOW_COLOR, SHADOW_GLOW
)

# Redéfinir les espacements pour un design plus compact
PADDING_MEDIUM = 3  # Marges externes compactes
PADDING_LARGE = 3   # Marges externes compactes
MARGIN_MEDIUM = 3   # Marges externes compactes

# Padding interne pour la respiration des éléments
INTERNAL_PADDING_SMALL = 8   # Petit padding interne
INTERNAL_PADDING_MEDIUM = 12 # Padding interne moyen
INTERNAL_PADDING_LARGE = 16  # Grand padding interne

# Couleur de survol personnalisée
HOVER_COLOR = "#4A90E2"  # Bleu moderne pour les effets de survol

# --- Paramètres de l'application et du thème ---
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# Le chemin de votre base de données (corrigé pour votre projet)
DB_PATH = os.path.join(os.path.dirname(__file__), '..', '..', '..', '..', '..', 'database', 'edumanager.db')

# Thème de couleurs utilisant le thème global EduManager+
THEME = {
    "bg_main": BG_MAIN,
    "header_bg": BG_SIDEBAR,
    "card_bg": CARD_BG,
    "border_color": BORDER_COLOR,
    "accent_blue": LIGHT_BLUE,
    "primary_text": TEXT,
    "secondary_text": MUTED,
    "error_red": ERROR_RED,
    "success_green": SUCCESS_GREEN,
    "warning_yellow": WARNING_YELLOW,
    "info_orange": INFO_ORANGE,
    "select_highlight": HOVER_PRIMARY,
    "hover_light": FOCUS_PRIMARY
}
FONT = FONT_PRIMARY[0]

# --- Contrôleur de données (Data Controller) avec base de données ---
# Import du contrôleur depuis le fichier séparé
from src.modules.administrative.maintenance.controllers.salle_controller import SalleController

# Initialisation du contrôleur
salle_controller = SalleController()

# --- Application principale (Main App) ---
class App(ctk.CTk):
    """Classe principale de l'application."""
    def __init__(self):
        super().__init__()
        self.title("EduManager+")
        self.geometry("1200x700")
        self.configure(fg_color=THEME["bg_main"])

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        # Le 'icons' est une dépendance que l'on doit passer si la classes l'attend
        # Création d'un dictionnaire d'icônes, ici il est vide, mais il pourrait être rempli
        self.icons = {} 

        # Créez la vue principale des salles en passant le parent et les icônes
        self.salles_view = SallesView(self, self.icons) # <-- Correction ici
        self.salles_view.grid(row=0, column=0, sticky="nsew")

# --- Vues de l'application (Main Views) ---
class SallesView(ctk.CTkFrame):
    """Vue principale pour la gestion des salles."""
    # La signature de la méthode __init__ a été corrigée ici
    def __init__(self, parent, icons):
        super().__init__(parent, fg_color=THEME["bg_main"])
        self.parent = parent
        self.icons = icons
        self.salle_controller = salle_controller
        self.search_var = tk.StringVar()
        self.sort_var = tk.StringVar(value="nom")
        self.selected_salle = None
        self.selected_salle_frame = None

        self.create_header()

        main_frame = ctk.CTkFrame(self, fg_color="transparent")
        main_frame.pack(fill="both", expand=True, padx=3, pady=3)
        main_frame.grid_columnconfigure(0, weight=1)
        main_frame.grid_columnconfigure(1, weight=2)
        main_frame.grid_rowconfigure(0, weight=1)

        self.create_salle_list_panel(main_frame)
        self.create_salle_details_panel(main_frame)

        self.refresh_salles_view()

    def create_header(self):
        """Crée l'en-tête de la vue avec le titre et le bouton d'ajout."""
        # Frame principal avec gradient effect
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.pack(fill="x", pady=3, padx=3)
        
        # Container avec effet de carte
        header_container = ctk.CTkFrame(header_frame, fg_color=THEME["card_bg"], corner_radius=20, 
                                       border_color=THEME["border_color"], border_width=1)
        header_container.pack(fill="x", padx=3, pady=3)
        
        # Titre principal avec icône
        title_frame = ctk.CTkFrame(header_container, fg_color="transparent")
        title_frame.pack(side="left", fill="x", expand=True, padx=INTERNAL_PADDING_LARGE, pady=INTERNAL_PADDING_MEDIUM)
        
        try:
            classroom_icon_path = os.path.join(os.path.dirname(__file__), '..', '..', '..', '..', '..', 'resources', 'icons', 'classroom.png')
            classroom_icon = ctk.CTkImage(Image.open(classroom_icon_path), size=(32, 32))
            icon_label = ctk.CTkLabel(title_frame, text="", image=classroom_icon)
            icon_label.pack(side="left", padx=(0, INTERNAL_PADDING_SMALL))
        except FileNotFoundError:
            print("Icône 'classroom.png' non trouvée.")
        
        # Titre avec style moderne
        title_label = ctk.CTkLabel(title_frame, text="Gestion des Salles", 
                                  font=FONT_HERO, text_color=THEME["accent_blue"])
        title_label.pack(side="left")
        
        # Sous-titre informatif
        subtitle_label = ctk.CTkLabel(title_frame, text="• Gestion complète des espaces pédagogiques", 
                                     font=FONT_PRIMARY, text_color=THEME["secondary_text"])
        subtitle_label.pack(side="left", padx=(INTERNAL_PADDING_SMALL, 0))

        # Boutons d'action avec design moderne
        btn_frame = ctk.CTkFrame(header_container, fg_color="transparent")
        btn_frame.pack(side="right", padx=INTERNAL_PADDING_LARGE, pady=INTERNAL_PADDING_MEDIUM)

        try:
            refresh_icon_path = os.path.join(os.path.dirname(__file__), '..', '..', '..', '..', '..', 'resources', 'icons', 'refresh.png')
            refresh_icon = ctk.CTkImage(Image.open(refresh_icon_path), size=(18, 18))
            refresh_btn = ctk.CTkButton(btn_frame, text="", image=refresh_icon, width=45, height=45,
                                         fg_color=THEME["header_bg"], hover_color=HOVER_COLOR,
                                         corner_radius=12, command=self.refresh_salles_view)
            refresh_btn.pack(side="left", padx=(0, INTERNAL_PADDING_SMALL))
        except FileNotFoundError:
            print("Icône 'refresh.png' non trouvée.")

        try:
            add_icon_path = os.path.join(os.path.dirname(__file__), '..', '..', '..', '..', '..', 'resources', 'icons', 'add.png')
            add_icon = ctk.CTkImage(Image.open(add_icon_path), size=(18, 18))
            add_btn = ctk.CTkButton(btn_frame, text="Nouvelle Salle", image=add_icon, compound="left", 
                                   font=FONT_PRIMARY, fg_color=THEME["header_bg"], hover_color=HOVER_COLOR, 
                                   text_color=THEME["primary_text"], command=self.ajouter_salle, 
                                   width=140, height=45, corner_radius=12,
                                   border_color=THEME["border_color"], border_width=2)
            add_btn.pack(side="left")
        except FileNotFoundError:
            add_btn = ctk.CTkButton(btn_frame, text="+ Nouvelle Salle", font=FONT_PRIMARY,
                                     fg_color=THEME["header_bg"], hover_color=HOVER_COLOR, text_color=THEME["primary_text"],
                                     command=self.ajouter_salle, width=140, height=45, corner_radius=12,
                                     border_color=THEME["border_color"], border_width=2)
            add_btn.pack(side="left")
            print("Icône 'add.png' non trouvée. Utilisation du texte par défaut.")

    def create_salle_list_panel(self, parent_frame):
        """Crée le panneau de gauche avec la liste des salles."""
        # Container principal avec design moderne
        list_panel = ctk.CTkFrame(parent_frame, fg_color=THEME["card_bg"], corner_radius=15, 
                                 border_color=THEME["border_color"], border_width=1)
        list_panel.grid(row=0, column=0, sticky="nsew", padx=(0, 3))

        # En-tête du panneau avec titre et statistiques
        panel_header = ctk.CTkFrame(list_panel, fg_color="transparent")
        panel_header.pack(fill="x", padx=INTERNAL_PADDING_MEDIUM, pady=INTERNAL_PADDING_MEDIUM)
        
        # Titre du panneau
        panel_title = ctk.CTkLabel(panel_header, text="Liste des Salles", 
                                   font=FONT_CARD_TITLE, text_color=THEME["primary_text"])
        panel_title.pack(side="left")
        
        # Compteur de salles
        self.salle_count_label = ctk.CTkLabel(panel_header, text="", 
                                             font=FONT_PRIMARY, text_color=THEME["accent_blue"])
        self.salle_count_label.pack(side="right")

        # Barre de recherche avec design amélioré
        search_frame = ctk.CTkFrame(list_panel, fg_color="transparent")
        search_frame.pack(fill="x", padx=INTERNAL_PADDING_MEDIUM, pady=(0, INTERNAL_PADDING_MEDIUM))

        try:
            search_icon_path = os.path.join(os.path.dirname(__file__), '..', '..', '..', '..', '..', 'resources', 'icons', 'search.png')
            search_icon = ctk.CTkImage(Image.open(search_icon_path), size=(16, 16))
            search_entry = ctk.CTkEntry(search_frame, placeholder_text="Rechercher une salles...",
                                       font=FONT_PRIMARY, height=40, corner_radius=10,
                                       fg_color=THEME["header_bg"], border_color=THEME["border_color"],
                                       textvariable=self.search_var)
            search_entry.pack(side="left", fill="x", expand=True)
        except FileNotFoundError:
            search_entry = ctk.CTkEntry(search_frame, placeholder_text="Rechercher une salles...",
                                       font=FONT_PRIMARY, height=40, corner_radius=10,
                                       fg_color=THEME["header_bg"], border_color=THEME["border_color"],
                                       textvariable=self.search_var)
            search_entry.pack(side="left", fill="x", expand=True)
        
        self.search_var.trace_add("write", self.filter_salles)

        # Menu de tri avec design moderne
        sort_options = ["nom", "capacite", "type"]
        sort_menu = ctk.CTkOptionMenu(search_frame, values=sort_options, variable=self.sort_var,
                                       font=FONT_PRIMARY, command=self.filter_salles, width=120, height=40,
                                       button_color=THEME["header_bg"], fg_color=THEME["header_bg"],
                                       corner_radius=10, dropdown_hover_color=HOVER_COLOR)
        sort_menu.pack(side="right", padx=(INTERNAL_PADDING_SMALL, 0))

        # Zone de liste avec scrollbar moderne
        self.salle_list_frame = ctk.CTkScrollableFrame(list_panel, fg_color="transparent", 
                                                      corner_radius=10, scrollbar_button_color=THEME["accent_blue"])
        self.salle_list_frame.pack(fill="both", expand=True, padx=INTERNAL_PADDING_MEDIUM, pady=(0, INTERNAL_PADDING_MEDIUM))

    def create_salle_details_panel(self, parent_frame):
        """Crée le panneau de droite pour afficher les détails et les stats d'une salles."""
        # Container principal avec design moderne
        self.details_panel = ctk.CTkFrame(parent_frame, fg_color=THEME["card_bg"], corner_radius=15,
                                         border_color=THEME["border_color"], border_width=1)
        self.details_panel.grid(row=0, column=1, sticky="nsew")

        self.clear_details_panel()

    def filter_salles(self, *args):
        """Filtre et trie les salles en fonction de la recherche et du tri."""
        search_term = self.search_var.get().lower()
        sort_by = self.sort_var.get()

        all_salles = self.salle_controller.get_all_salles()

        filtered_salles = [
            salles for salles in all_salles
            if search_term in salles['nom_salle'].lower() or
               search_term in str(salles['capacite']).lower() or
               search_term in salles['type_salle'].lower()
        ]

        if sort_by == "nom":
            filtered_salles.sort(key=lambda s: s['nom_salle'])
        elif sort_by == "capacite":
            filtered_salles.sort(key=lambda s: s['capacite'])
        elif sort_by == "type":
            filtered_salles.sort(key=lambda s: s['type_salle'])

        self.display_salle_list(filtered_salles)

    def display_salle_list(self, salles_to_display):
        """Affiche les salles sous forme de liste cliquable."""
        for w in self.salle_list_frame.winfo_children():
            w.destroy()

        # Mettre à jour le compteur de salles
        total_salles = len(salles_to_display)
        self.salle_count_label.configure(text=f"{total_salles} salles{'s' if total_salles > 1 else ''}")

        if not salles_to_display:
            # Message d'état vide avec design moderne
            empty_frame = ctk.CTkFrame(self.salle_list_frame, fg_color="transparent")
            empty_frame.pack(expand=True, fill="both", pady=PADDING_LARGE)
            
            try:
                search_icon_path = os.path.join(os.path.dirname(__file__), '..', '..', '..', '..', '..', 'resources', 'icons', 'search.png')
                search_icon = ctk.CTkImage(Image.open(search_icon_path), size=(48, 48))
                empty_icon = ctk.CTkLabel(empty_frame, text="", image=search_icon)
                empty_icon.pack(pady=PADDING_MEDIUM)
            except FileNotFoundError:
                pass
            
            empty_label = ctk.CTkLabel(empty_frame, text="Aucune salles trouvée",
                                      font=FONT_CARD_TITLE, text_color=THEME["secondary_text"])
            empty_label.pack(pady=PADDING_MEDIUM)
            
            empty_subtitle = ctk.CTkLabel(empty_frame, text="Essayez de modifier votre recherche",
                                         font=FONT_PRIMARY, text_color=THEME["secondary_text"])
            empty_subtitle.pack()
            
            self.clear_details_panel()
            return

        # Afficher les salles avec design amélioré
        for i, salles in enumerate(salles_to_display):
            salle_item_frame = SalleListItem(self.salle_list_frame, salles, self.show_salle_details)
            salle_item_frame.pack(fill="x", padx=PADDING_MEDIUM, pady=(MARGIN_MEDIUM if i == 0 else MARGIN_MEDIUM//2, MARGIN_MEDIUM//2))

    def show_salle_details(self, salles, item_frame):
        """Affiche les détails, les stats et le graphique d'une salles sélectionnée."""
        self.selected_salle = salles

        if self.selected_salle_frame:
            self.selected_salle_frame.deselect()
        self.selected_salle_frame = item_frame
        self.selected_salle_frame.select()

        # Effacez d'abord tout le contenu du panneau de détails existant.
        self.clear_details_panel(keep_placeholder=False)

        details_frame = ctk.CTkFrame(self.details_panel, fg_color="transparent")
        details_frame.pack(fill="both", expand=True, padx=PADDING_MEDIUM, pady=PADDING_MEDIUM)

        # Titre
        ctk.CTkLabel(details_frame, text=salles['nom_salle'], font=FONT_TITLE, text_color=THEME["primary_text"]).pack(pady=(0, PADDING_MEDIUM))

        # Détails de la salles
        details_card = ctk.CTkFrame(details_frame, fg_color=THEME["header_bg"], corner_radius=12)
        details_card.pack(fill="x", pady=(0, PADDING_MEDIUM), padx=PADDING_MEDIUM)

        def create_detail_row(parent, label, value):
            frame = ctk.CTkFrame(parent, fg_color="transparent")
            frame.pack(fill="x", pady=PADDING_MEDIUM)
            ctk.CTkLabel(frame, text=f"{label} :", font=FONT_SUBTITLE, text_color=THEME["secondary_text"], width=150, anchor="w").pack(side="left")
            ctk.CTkLabel(frame, text=value, font=FONT_SUBTITLE, text_color=THEME["primary_text"], anchor="w").pack(side="left", padx=PADDING_MEDIUM)

        create_detail_row(details_card, "Capacité", str(salles['capacite']))
        create_detail_row(details_card, "Type de salles", salles['type_salle'])

        # Panneau des stats et du graphique
        stats_frame = ctk.CTkFrame(details_frame, fg_color=THEME["header_bg"], corner_radius=12)
        stats_frame.pack(fill="both", expand=True, padx=PADDING_MEDIUM)

        self.create_stats_and_chart(stats_frame)

        # Boutons d'action
        btn_frame = ctk.CTkFrame(details_frame, fg_color="transparent")
        btn_frame.pack(pady=PADDING_MEDIUM)

        try:
            edit_icon_path = os.path.join(os.path.dirname(__file__), '..', '..', '..', '..', '..', 'resources', 'icons', 'edit.png')
            edit_icon = ctk.CTkImage(Image.open(edit_icon_path), size=(20, 20))
            edit_btn = ctk.CTkButton(btn_frame, text="Modifier", image=edit_icon, compound="left", font=FONT_PRIMARY,
                                      fg_color=THEME["header_bg"], hover_color=HOVER_COLOR, text_color=THEME["primary_text"],
                                      command=lambda: self.modifier_salle(salles), height=35,
                                      border_color=THEME["border_color"], border_width=2)
            edit_btn.pack(side="left", padx=PADDING_MEDIUM, fill="x", expand=True)
        except FileNotFoundError:
            edit_btn = ctk.CTkButton(btn_frame, text="Modifier", font=FONT_PRIMARY,
                                      fg_color=THEME["header_bg"], hover_color=HOVER_COLOR, text_color=THEME["primary_text"],
                                      command=lambda: self.modifier_salle(salles), height=35,
                                      border_color=THEME["border_color"], border_width=2)
            edit_btn.pack(side="left", padx=PADDING_MEDIUM, fill="x", expand=True)
            print("Icône 'edit.png' non trouvée. Utilisation du texte par défaut.")

        try:
            delete_icon_path = os.path.join(os.path.dirname(__file__), '..', '..', '..', '..', '..', 'resources', 'icons', 'delete.png')
            delete_icon = ctk.CTkImage(Image.open(delete_icon_path), size=(20, 20))
            delete_btn = ctk.CTkButton(btn_frame, text="Supprimer", image=delete_icon, compound="left", font=FONT_PRIMARY,
                                        fg_color=THEME["header_bg"], hover_color=HOVER_COLOR, text_color=THEME["primary_text"],
                                        command=lambda: self.supprimer_salle(salles), height=35,
                                        border_color=THEME["border_color"], border_width=2)
            delete_btn.pack(side="left", padx=PADDING_MEDIUM, fill="x", expand=True)
        except FileNotFoundError:
            delete_btn = ctk.CTkButton(btn_frame, text="Supprimer", font=FONT_PRIMARY,
                                        fg_color=THEME["header_bg"], hover_color=HOVER_COLOR, text_color=THEME["primary_text"],
                                        command=lambda: self.supprimer_salle(salles), height=35,
                                        border_color=THEME["border_color"], border_width=2)
            delete_btn.pack(side="left", padx=PADDING_MEDIUM, fill="x", expand=True)
            print("Icône 'delete.png' non trouvée. Utilisation du texte par défaut.")

    def create_stats_and_chart(self, parent_frame):
        """Crée le graphique et affiche les statistiques globales."""
        type_counts, total_capacite = self.salle_controller.get_salles_stats()

        stats_header = ctk.CTkLabel(parent_frame, text="Statistiques Globales des Salles", font=FONT_SUBTITLE, text_color=THEME["primary_text"])
        stats_header.pack(pady=(PADDING_MEDIUM, 0))

        if not type_counts:
            ctk.CTkLabel(parent_frame, text="Aucune donnée statistique disponible.", font=FONT_PRIMARY, text_color=THEME["secondary_text"]).pack(pady=PADDING_MEDIUM)
            return

        fig, ax = plt.subplots(facecolor=THEME["header_bg"], figsize=(5, 4))
        fig.patch.set_facecolor(THEME["header_bg"])
        
        types = list(type_counts.keys())
        counts = list(type_counts.values())
        
        bars = ax.bar(types, counts, color=THEME["accent_blue"])
        
        ax.set_title("Nombre de salles par type", color=THEME["primary_text"], font=FONT)
        ax.set_ylabel("Nombre de salles", color=THEME["secondary_text"])
        ax.set_facecolor(THEME["header_bg"])
        
        # Style des axes et des labels
        ax.tick_params(axis='x', colors=THEME["secondary_text"])
        ax.tick_params(axis='y', colors=THEME["secondary_text"])
        ax.spines['bottom'].set_color(THEME["secondary_text"])
        ax.spines['left'].set_color(THEME["secondary_text"])
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)
        
        # Ajouter des étiquettes de données sur les barres
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width() / 2, height, f'{height}',
                     ha='center', va='bottom', color=THEME["success_green"], fontsize=12)

        plt.tight_layout()

        canvas = FigureCanvasTkAgg(fig, master=parent_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True, pady=(PADDING_MEDIUM, PADDING_MEDIUM), padx=PADDING_MEDIUM)

        # Afficher la capacité totale
        total_capacite_label = ctk.CTkLabel(parent_frame, text=f"Capacité totale de l'établissement : {total_capacite}",
                                              font=FONT_PRIMARY, text_color=THEME["success_green"])
        total_capacite_label.pack(pady=(0, PADDING_MEDIUM))

    def clear_details_panel(self, keep_placeholder=True):
        """Efface le contenu du panneau de détails et affiche un message d'attente moderne."""
        for w in self.details_panel.winfo_children():
            w.destroy()

        if keep_placeholder:
            # Container pour le message d'attente
            placeholder_frame = ctk.CTkFrame(self.details_panel, fg_color="transparent")
            placeholder_frame.pack(expand=True, fill="both", pady=PADDING_LARGE)
            
            # Icône d'attente
            try:
                classroom_icon_path = os.path.join(os.path.dirname(__file__), '..', '..', '..', '..', '..', 'resources', 'icons', 'classroom.png')
                classroom_icon = ctk.CTkImage(Image.open(classroom_icon_path), size=(64, 64))
                icon_label = ctk.CTkLabel(placeholder_frame, text="", image=classroom_icon)
                icon_label.pack(pady=PADDING_LARGE)
            except FileNotFoundError:
                print("Icône 'classroom.png' non trouvée.")
            
            # Message principal
            main_label = ctk.CTkLabel(placeholder_frame, text="Sélectionnez une salles",
                                     font=FONT_HERO, text_color=THEME["primary_text"])
            main_label.pack(pady=PADDING_MEDIUM)
            
            # Message secondaire
            subtitle_label = ctk.CTkLabel(placeholder_frame, text="pour voir les détails et statistiques",
                                        font=FONT_SUBTITLE, text_color=THEME["secondary_text"])
            subtitle_label.pack(pady=PADDING_MEDIUM)
            
            # Message informatif
            info_label = ctk.CTkLabel(placeholder_frame, text="Cliquez sur une salles dans la liste à gauche",
                                     font=FONT_PRIMARY, text_color=THEME["secondary_text"])
            info_label.pack(pady=PADDING_MEDIUM)
            
            self.selected_salle = None

        if self.selected_salle_frame:
            self.selected_salle_frame.deselect()
            self.selected_salle_frame = None

    def refresh_salles_view(self):
        """Actualise la vue des salles après une action (ajout, modification, suppression)."""
        self.filter_salles()
        self.clear_details_panel()

    def ajouter_salle(self):
        """Ouvre le formulaire d'ajout de salles."""
        self._ouvrir_formulaire("Ajouter")

    def modifier_salle(self, salle_data):
        """Ouvre le formulaire de modification de salles."""
        self._ouvrir_formulaire("Modifier", salle_data)

    def supprimer_salle(self, salle_data):
        """Supprime une salles après confirmation."""
        if messagebox.askyesno("Confirmation", f"Voulez-vous vraiment supprimer la salles « {salle_data['nom_salle']} » ?"):
            if self.salle_controller.delete_salle(salle_data['id_salle']):
                messagebox.showinfo("Succès", f"La salles '{salle_data['nom_salle']}' a été supprimée.")
                self.refresh_salles_view()

    def _ouvrir_formulaire(self, mode, data=None):
        """Ouvre la fenêtre modale du formulaire."""
        form = SalleForm(self.parent, mode, data)
        form.wait_window()
        self.refresh_salles_view()

# --- Composants réutilisables (Reusable Components) ---
class SalleListItem(ctk.CTkFrame):
    """Un élément de liste cliquable pour une salles avec design moderne."""
    def __init__(self, parent, salle_data, command):
        super().__init__(parent, fg_color=THEME["card_bg"], height=60, corner_radius=12, 
                         border_color=THEME["border_color"], border_width=1)
        self.salle_data = salle_data
        self.command = command
        self.is_selected = False

        # Container principal
        main_frame = ctk.CTkFrame(self, fg_color="transparent")
        main_frame.pack(fill="both", expand=True, padx=INTERNAL_PADDING_MEDIUM, pady=INTERNAL_PADDING_MEDIUM)

        # Icône selon le type de salles
        try:
            if salle_data['type_salle'] == "Amphithéâtre":
                icon_name = "stacks.png"
            elif salle_data['type_salle'] == "Laboratoire":
                icon_name = "wrench.png"
            elif salle_data['type_salle'] == "Salle de conférence":
                icon_name = "megaphone.png"
            else:
                icon_name = "classroom.png"
            
            icon_path = os.path.join(os.path.dirname(__file__), '..', '..', '..', '..', '..', 'resources', 'icons', icon_name)
            salle_icon = ctk.CTkImage(Image.open(icon_path), size=(24, 24))
            icon_label = ctk.CTkLabel(main_frame, text="", image=salle_icon)
            icon_label.pack(side="left", padx=(0, INTERNAL_PADDING_SMALL))
        except FileNotFoundError:
            print(f"Icône '{icon_name}' non trouvée.")

        # Informations de la salles
        info_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        info_frame.pack(side="left", fill="both", expand=True)

        # Nom de la salles
        self.name_label = ctk.CTkLabel(info_frame, text=salle_data['nom_salle'], font=FONT_CARD_TITLE, 
                                       text_color=THEME["primary_text"], anchor="w")
        self.name_label.pack(side="left", fill="x", expand=True)

        # Capacité simplifiée
        cap_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        cap_frame.pack(side="right", padx=(INTERNAL_PADDING_SMALL, 0))

        self.cap_label = ctk.CTkLabel(cap_frame, text=f"{salle_data['capacite']}", 
                                     font=FONT_PRIMARY, text_color=THEME["secondary_text"])
        self.cap_label.pack(side="left")

        # Bindings pour l'interactivité
        self.bind("<Button-1>", self.on_click)
        main_frame.bind("<Button-1>", self.on_click)
        self.name_label.bind("<Button-1>", self.on_click)
        self.cap_label.bind("<Button-1>", self.on_click)
        
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)
        main_frame.bind("<Enter>", self.on_enter)
        main_frame.bind("<Leave>", self.on_leave)
        self.name_label.bind("<Enter>", self.on_enter)
        self.name_label.bind("<Leave>", self.on_leave)
        self.cap_label.bind("<Enter>", self.on_enter)
        self.cap_label.bind("<Leave>", self.on_leave)

    def on_click(self, event=None):
        self.command(self.salle_data, self)

    def on_enter(self, event=None):
        if not self.is_selected:
            self.configure(fg_color=HOVER_COLOR, border_color=THEME["accent_blue"])

    def on_leave(self, event=None):
        if not self.is_selected:
            self.configure(fg_color=THEME["card_bg"], border_color=THEME["border_color"])

    def select(self):
        self.is_selected = True
        self.configure(fg_color=THEME["select_highlight"], border_color=THEME["accent_blue"], border_width=2)

    def deselect(self):
        self.is_selected = False
        self.configure(fg_color=THEME["card_bg"], border_color=THEME["border_color"], border_width=1)

class SalleForm(ctk.CTkToplevel):
    """Fenêtre modale pour ajouter ou modifier une salles."""
    def __init__(self, parent, mode, data=None):
        super().__init__(parent)
        self.parent = parent
        self.mode = mode
        self.data = data

        self.title(f"{mode} une Salle")
        self.geometry("650x650")
        self.transient(parent)
        self.grab_set()
        self.configure(fg_color=THEME["bg_main"])

        self.update_idletasks()
        x = self.parent.winfo_rootx() + (self.parent.winfo_width() - self.winfo_width()) // 2
        y = self.parent.winfo_rooty() + (self.parent.winfo_height() - self.winfo_height()) // 2
        self.geometry(f"+{x}+{y}")

        self._create_widgets()

    def _create_widgets(self):
        """Crée les widgets du formulaire avec design moderne."""
        # Container principal avec design moderne
        form_frame = ctk.CTkFrame(self, fg_color=THEME["card_bg"], corner_radius=20, 
                                 border_color=THEME["border_color"], border_width=1)
        form_frame.pack(fill="both", expand=True, padx=INTERNAL_PADDING_LARGE, pady=INTERNAL_PADDING_LARGE)

        # En-tête du formulaire
        header_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        header_frame.pack(fill="x", padx=INTERNAL_PADDING_LARGE, pady=(INTERNAL_PADDING_LARGE, INTERNAL_PADDING_MEDIUM))

        # Icône du formulaire
        try:
            if self.mode == "Ajouter":
                icon_name = "add.png"
            else:
                icon_name = "edit.png"
            icon_path = os.path.join(os.path.dirname(__file__), '..', '..', '..', '..', '..', 'resources', 'icons', icon_name)
            form_icon = ctk.CTkImage(Image.open(icon_path), size=(32, 32))
            icon_label = ctk.CTkLabel(header_frame, text="", image=form_icon)
            icon_label.pack(side="left", padx=(0, INTERNAL_PADDING_SMALL))
        except FileNotFoundError:
            print(f"Icône '{icon_name}' non trouvée.")

        # Titre du formulaire
        title_label = ctk.CTkLabel(header_frame, text=f"{self.mode} une Salle", 
                                  font=FONT_HERO, text_color=THEME["accent_blue"])
        title_label.pack(side="left")

        # Sous-titre
        subtitle_label = ctk.CTkLabel(header_frame, text="Remplissez les informations ci-dessous", 
                                     font=FONT_PRIMARY, text_color=THEME["secondary_text"])
        subtitle_label.pack(side="left", padx=(INTERNAL_PADDING_SMALL, 0))

        # Champs du formulaire avec design amélioré
        fields_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        fields_frame.pack(fill="x", padx=INTERNAL_PADDING_LARGE, pady=INTERNAL_PADDING_MEDIUM)

        # Nom de la salles
        nom_label = ctk.CTkLabel(fields_frame, text="Nom de la salles", 
                                font=FONT_SUBTITLE, text_color=THEME["primary_text"])
        nom_label.pack(anchor="w", pady=(0, INTERNAL_PADDING_SMALL//2))
        
        self.nom_entry = ctk.CTkEntry(fields_frame, placeholder_text="Ex: A101, Lab1, Amphi1...", 
                                     font=FONT_PRIMARY, height=45, corner_radius=10,
                                     fg_color=THEME["header_bg"], border_color=THEME["border_color"])
        self.nom_entry.pack(fill="x", pady=(0, INTERNAL_PADDING_SMALL))
        if self.data: self.nom_entry.insert(0, self.data['nom_salle'])

        # Capacité
        capacite_label = ctk.CTkLabel(fields_frame, text="Capacité", 
                                    font=FONT_SUBTITLE, text_color=THEME["primary_text"])
        capacite_label.pack(anchor="w", pady=(0, INTERNAL_PADDING_SMALL//2))
        
        self.capacite_entry = ctk.CTkEntry(fields_frame, placeholder_text="Nombre de places (ex: 30)", 
                                          font=FONT_PRIMARY, height=45, corner_radius=10,
                                          fg_color=THEME["header_bg"], border_color=THEME["border_color"])
        self.capacite_entry.pack(fill="x", pady=(0, INTERNAL_PADDING_SMALL))
        if self.data: self.capacite_entry.insert(0, self.data['capacite'])

        # Type de salles
        type_label = ctk.CTkLabel(fields_frame, text="Type de salles", 
                                 font=FONT_SUBTITLE, text_color=THEME["primary_text"])
        type_label.pack(anchor="w", pady=(0, INTERNAL_PADDING_SMALL//2))
        
        salle_types = ["Général", "Amphithéâtre", "Laboratoire", "Salle de conférence"]
        self.type_optionmenu = ctk.CTkOptionMenu(fields_frame, values=salle_types, 
                                                font=FONT_PRIMARY, height=45, corner_radius=10,
                                                fg_color=THEME["header_bg"], button_color=THEME["header_bg"], 
                                                button_hover_color=HOVER_COLOR,
                                                dropdown_hover_color=HOVER_COLOR)
        self.type_optionmenu.pack(fill="x", pady=(0, INTERNAL_PADDING_SMALL))
        if self.data and self.data['type_salle'] in salle_types:
            self.type_optionmenu.set(self.data['type_salle'])
        else:
            self.type_optionmenu.set(salle_types[0])

        # Équipements
        equipements_label = ctk.CTkLabel(fields_frame, text="Équipements", 
                                        font=FONT_SUBTITLE, text_color=THEME["primary_text"])
        equipements_label.pack(anchor="w", pady=(0, INTERNAL_PADDING_SMALL//2))
        
        self.equipements_entry = ctk.CTkEntry(fields_frame, placeholder_text="Ex: Tableau, Projecteur, Ordinateurs...", 
                                              font=FONT_PRIMARY, height=45, corner_radius=10,
                                              fg_color=THEME["header_bg"], border_color=THEME["border_color"])
        self.equipements_entry.pack(fill="x", pady=(0, INTERNAL_PADDING_SMALL))
        if self.data: self.equipements_entry.insert(0, self.data['equipements'] or "")

        # Statut
        statut_label = ctk.CTkLabel(fields_frame, text="Statut", 
                                   font=FONT_SUBTITLE, text_color=THEME["primary_text"])
        statut_label.pack(anchor="w", pady=(0, INTERNAL_PADDING_SMALL//2))
        
        statut_options = ["Disponible", "Occupée", "Maintenance", "Hors service"]
        self.statut_optionmenu = ctk.CTkOptionMenu(fields_frame, values=statut_options, 
                                                   font=FONT_PRIMARY, height=45, corner_radius=10,
                                                   fg_color=THEME["header_bg"], button_color=THEME["header_bg"], 
                                                   button_hover_color=HOVER_COLOR,
                                                   dropdown_hover_color=HOVER_COLOR)
        self.statut_optionmenu.pack(fill="x", pady=(0, INTERNAL_PADDING_LARGE))
        if self.data and self.data['statut'] in statut_options:
            self.statut_optionmenu.set(self.data['statut'])
        else:
            self.statut_optionmenu.set(statut_options[0])

        # Boutons d'action avec design moderne
        btn_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        btn_frame.pack(fill="x", padx=INTERNAL_PADDING_LARGE, pady=(0, INTERNAL_PADDING_LARGE))

        # Bouton Enregistrer avec contour
        save_btn = ctk.CTkButton(btn_frame, text="Enregistrer", font=FONT_PRIMARY,
                                command=self._save_data, fg_color=THEME["header_bg"], 
                                hover_color=HOVER_COLOR, text_color=THEME["primary_text"],
                                height=45, corner_radius=12, width=140,
                                border_color=THEME["border_color"], border_width=2)
        save_btn.pack(side="left", padx=(0, INTERNAL_PADDING_SMALL))

        # Bouton Annuler avec contour
        cancel_btn = ctk.CTkButton(btn_frame, text="Annuler", font=FONT_PRIMARY,
                                  command=self.destroy, fg_color=THEME["header_bg"], 
                                  hover_color=HOVER_COLOR, text_color=THEME["primary_text"],
                                  height=45, corner_radius=12, width=140,
                                  border_color=THEME["border_color"], border_width=2)
        cancel_btn.pack(side="left")

    def _save_data(self):
        """Valide et enregistre les données du formulaire."""
        nom_salle = self.nom_entry.get().strip()
        capacite = self.capacite_entry.get().strip()
        type_salle = self.type_optionmenu.get()
        equipements = self.equipements_entry.get().strip()
        statut = self.statut_optionmenu.get()

        if not nom_salle:
            messagebox.showerror("Erreur de saisie", "Le nom de la salles est obligatoire.")
            return
        if not capacite or not capacite.isdigit() or int(capacite) <= 0:
            messagebox.showerror("Erreur de saisie", "La capacité doit être un nombre entier positif.")
            return

        try:
            if self.mode == "Ajouter":
                if salle_controller.add_salle(nom_salle, int(capacite), type_salle, equipements, statut):
                    messagebox.showinfo("Succès", f"La salles '{nom_salle}' a été ajoutée avec succès.")
            else: # mode == "Modifier"
                if salle_controller.update_salle(self.data['id_salle'], nom_salle, int(capacite), type_salle, equipements, statut):
                    messagebox.showinfo("Succès", f"La salles '{nom_salle}' a été mise à jour avec succès.")
            
            self.parent.refresh_salles_view()
            self.destroy()
        except Exception as e:
            messagebox.showerror("Erreur", f"Une erreur est survenue : {str(e)}")

if __name__ == "__main__":
    if salle_controller.conn:
        app = App()
        app.mainloop()
    else:
        print("L'application n'a pas pu démarrer en raison d'une erreur de connexion à la base de données.")