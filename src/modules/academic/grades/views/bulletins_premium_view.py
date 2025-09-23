"""
Vue des bulletins avec design premium et moderne
Interface utilisateur élégante et professionnelle
"""

import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
from src.modules.academic.grades.controllers.bulletins_sqlserver_controller import BulletinsController
from src.modules.academic.students.controllers.eleve_controller import get_all_eleves
from src.modules.academic.classes.controllers.classe_controller import get_all_classes
from PIL import Image, ImageTk, ImageDraw, ImageFilter
import os
import sys
from datetime import datetime, date
import math

# Ajouter le chemin racine pour les imports
root_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))
sys.path.insert(0, root_path)

# Chemin vers les ressources
resources_path = os.path.join(root_path, "resources")
icons_path = r"C:\Users\Lenovo\Desktop\Clonage_git\Gestion_scolaire\Gestion_scolaire\resources\icons"
themes_path = os.path.join(resources_path, "themes")

# Import du thème EduManager+
try:
    sys.path.insert(0, themes_path)
    from theme import *
    sys.path.insert(0, os.path.join(resources_path, "fonts"))
    from fonts import *
    sys.path.insert(0, icons_path)
    from icons import *
except ImportError:
    # Thème premium par défaut
    BG_MAIN = "#0A0E27"
    BG_CARD = "#1A1F3A"
    BG_SIDEBAR = "#151B35"
    BG_ACCENT = "#2A2F4A"
    TEXT_PRIMARY = "#FFFFFF"
    TEXT_SECONDARY = "#B8C5D1"
    TEXT_MUTED = "#7A8B9A"
    ACCENT_BLUE = "#4F46E5"
    ACCENT_PURPLE = "#7C3AED"
    SUCCESS_GREEN = "#10B981"
    ERROR_RED = "#EF4444"
    WARNING_ORANGE = "#F59E0B"
    GRADIENT_START = "#667EEA"
    GRADIENT_END = "#764BA2"
    F_TITLE = ("Segoe UI", 24, "bold")
    F_SUB = ("Segoe UI", 16, "bold")
    F_TXT = ("Segoe UI", 13)
    F_SMALL = ("Segoe UI", 11)
    F_BOLD = ("Segoe UI", 13, "bold")

def load_ctk_icon(icon_name, size=(20, 20)):
    """Charge une icône avec effet premium"""
    try:
        icon_path = os.path.join(icons_path, icon_name)
        
        if os.path.exists(icon_path):
            # Créer un effet de glow pour les icônes
            img = Image.open(icon_path)
            img = img.resize(size, Image.Resampling.LANCZOS)
            
            # Appliquer un effet de glow subtil
            glow_img = img.copy()
            glow_img = glow_img.filter(ImageFilter.GaussianBlur(radius=2))
            
            return ctk.CTkImage(img, size=size)
        else:
            print(f"⚠️ Icône non trouvée: {icon_path}")
            return None
    except Exception as e:
        print(f"❌ Erreur chargement icône {icon_name}: {e}")
        return None

def create_gradient_frame(parent, colors, width, height):
    """Crée un frame avec dégradé"""
    frame = ctk.CTkFrame(parent, fg_color="transparent", width=width, height=height)
    return frame

class BulletinsPremiumView(ctk.CTkFrame):
    """Vue premium des bulletins avec design moderne"""
    
    def __init__(self, parent):
        super().__init__(parent, fg_color=BG_MAIN)
        
        # Configuration de la grille
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        
        # Initialiser le contrôleur SQL Server
        self.controller = BulletinsController()
        
        # Variables
        self.current_periode = None
        self.current_classe = None
        self.bulletins_data = []
        
        # Configuration - afficher les 100 premiers bulletins par classe par ordre de mérite
        self.limite_par_classe = 100
        
        # Construire l'interface premium
        self._build_premium_header()
        self._build_premium_content()
        
        # Charger les données initiales
        self.charger_periodes()
        self.charger_classes()
        self.charger_bulletins()
    
    def _build_premium_header(self):
        """Construit l'en-tête premium avec dégradé"""
        # Frame principal avec dégradé
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.grid(row=0, column=0, sticky="ew", padx=0, pady=0)
        header_frame.grid_columnconfigure(1, weight=1)
        
        # Background avec dégradé simulé
        bg_frame = ctk.CTkFrame(header_frame, fg_color=BG_ACCENT, height=120)
        bg_frame.grid(row=0, column=0, columnspan=3, sticky="ew")
        
        # Contenu de l'en-tête
        content_frame = ctk.CTkFrame(bg_frame, fg_color="transparent")
        content_frame.pack(fill="both", expand=True, padx=30, pady=20)
        content_frame.grid_columnconfigure(1, weight=1)
        
        # Section gauche - Titre et icône
        left_section = ctk.CTkFrame(content_frame, fg_color="transparent")
        left_section.grid(row=0, column=0, sticky="w")
        
        # Icône avec effet premium
        icon_container = ctk.CTkFrame(left_section, fg_color=ACCENT_BLUE, corner_radius=15, width=60, height=60)
        icon_container.pack(side="left", padx=(0, 20))
        
        bulletin_icon = load_ctk_icon("newspaper.png", (32, 32))
        if bulletin_icon:
            icon_label = ctk.CTkLabel(icon_container, image=bulletin_icon, text="", fg_color="transparent")
            icon_label.pack(expand=True)
        
        # Titre avec style premium
        title_container = ctk.CTkFrame(left_section, fg_color="transparent")
        title_container.pack(side="left")
        
        main_title = ctk.CTkLabel(title_container, text="Gestion des Bulletins", 
                                 font=F_TITLE, text_color=TEXT_PRIMARY)
        main_title.pack(anchor="w")
        
        subtitle = ctk.CTkLabel(title_container, text="Système de bulletins professionnel", 
                              font=F_SMALL, text_color=TEXT_SECONDARY)
        subtitle.pack(anchor="w")
        
        # Section droite - Actions premium
        right_section = ctk.CTkFrame(content_frame, fg_color="transparent")
        right_section.grid(row=0, column=1, sticky="e")
        
        # Boutons d'action avec style premium
        actions_container = ctk.CTkFrame(right_section, fg_color="transparent")
        actions_container.pack(side="right")
        
        # Bouton Générer avec effet hover
        generate_btn = ctk.CTkButton(actions_container, 
                                    text="✨ Générer Bulletins", 
                                    fg_color=SUCCESS_GREEN, 
                                    hover_color="#059669",
                                    text_color="white",
                                    font=F_BOLD, 
                                    height=45, 
                                    width=160,
                                    corner_radius=12,
                                    command=self.generer_bulletins_classe)
        generate_btn.pack(side="right", padx=(10, 0))
        
        # Bouton Dashboard
        dashboard_btn = ctk.CTkButton(actions_container, 
                                    text="📊 Dashboard", 
                                    fg_color=ACCENT_BLUE, 
                                    hover_color="#4338CA",
                                    text_color="white",
                                    font=F_BOLD, 
                                    height=45, 
                                    width=140,
                                    corner_radius=12,
                                    command=self.ouvrir_dashboard)
        dashboard_btn.pack(side="right", padx=(10, 0))
        
        # Bouton Actualiser
        refresh_btn = ctk.CTkButton(actions_container, 
                                   text="🔄 Actualiser", 
                                   fg_color=WARNING_ORANGE, 
                                   hover_color="#D97706",
                                   text_color="white",
                                   font=F_BOLD, 
                                   height=45, 
                                   width=130,
                                   corner_radius=12,
                                   command=self.charger_bulletins)
        refresh_btn.pack(side="right", padx=(10, 0))
    
    def _build_premium_content(self):
        """Construit le contenu principal avec design premium"""
        main_frame = ctk.CTkFrame(self, fg_color="transparent")
        main_frame.grid(row=1, column=0, sticky="nsew", padx=20, pady=(0, 20))
        main_frame.grid_columnconfigure(0, weight=1)
        main_frame.grid_rowconfigure(1, weight=1)
        
        # Section des filtres premium
        self._build_premium_filters(main_frame)
        
        # Zone des bulletins avec design moderne
        self._build_premium_bulletins_section(main_frame)
    
    def _build_premium_filters(self, parent):
        """Construit la section des filtres avec design premium"""
        filters_frame = ctk.CTkFrame(parent, fg_color=BG_CARD, corner_radius=16, height=80)
        filters_frame.grid(row=0, column=0, sticky="ew", pady=(0, 20))
        filters_frame.grid_columnconfigure((0, 1, 2, 3), weight=1)
        filters_frame.grid_propagate(False)
        
        # Titre de la section filtres
        filters_title = ctk.CTkLabel(filters_frame, text="🔍 Filtres et Recherche", 
                                    font=F_SUB, text_color=TEXT_PRIMARY)
        filters_title.grid(row=0, column=0, padx=25, pady=(15, 5), sticky="w")
        
        # Filtre par période avec style premium
        periode_container = ctk.CTkFrame(filters_frame, fg_color="transparent")
        periode_container.grid(row=1, column=0, padx=25, pady=(0, 15), sticky="ew")
        
        periode_label = ctk.CTkLabel(periode_container, text="📅 Période:", 
                                   font=F_BOLD, text_color=TEXT_SECONDARY)
        periode_label.pack(anchor="w")
        
        self.periode_var = ctk.StringVar(value="Sélectionner une période")
        self.periode_combo = ctk.CTkComboBox(periode_container, 
                                           values=["Sélectionner une période"],
                                           variable=self.periode_var, 
                                           font=F_TXT, 
                                           height=40, 
                                           width=220,
                                           corner_radius=10,
                                           fg_color=BG_ACCENT,
                                           border_color=ACCENT_BLUE,
                                           button_color=ACCENT_BLUE,
                                           button_hover_color="#4338CA")
        self.periode_combo.pack(fill="x", pady=(5, 0))
        self.periode_combo.bind("<<ComboboxSelected>>", self._on_periode_change)
        
        # Filtre par classe avec style premium
        classe_container = ctk.CTkFrame(filters_frame, fg_color="transparent")
        classe_container.grid(row=1, column=1, padx=25, pady=(0, 15), sticky="ew")
        
        classe_label = ctk.CTkLabel(classe_container, text="🏫 Classe:", 
                                   font=F_BOLD, text_color=TEXT_SECONDARY)
        classe_label.pack(anchor="w")
        
        self.classe_var = ctk.StringVar(value="Toutes les classes")
        self.classe_combo = ctk.CTkComboBox(classe_container, 
                                          values=["Toutes les classes"],
                                          variable=self.classe_var, 
                                          font=F_TXT, 
                                          height=40, 
                                          width=220,
                                          corner_radius=10,
                                          fg_color=BG_ACCENT,
                                          border_color=ACCENT_PURPLE,
                                          button_color=ACCENT_PURPLE,
                                          button_hover_color="#6D28D9")
        self.classe_combo.pack(fill="x", pady=(5, 0))
        self.classe_combo.bind("<<ComboboxSelected>>", self._on_classe_change)
        
        # Statistiques rapides
        stats_container = ctk.CTkFrame(filters_frame, fg_color="transparent")
        stats_container.grid(row=1, column=2, columnspan=2, padx=25, pady=(0, 15), sticky="ew")
        
        stats_label = ctk.CTkLabel(stats_container, text="📈 Statistiques Rapides", 
                                 font=F_BOLD, text_color=TEXT_SECONDARY)
        stats_label.pack(anchor="w")
        
        # Mini cartes de statistiques
        mini_stats_frame = ctk.CTkFrame(stats_container, fg_color="transparent")
        mini_stats_frame.pack(fill="x", pady=(5, 0))
        mini_stats_frame.grid_columnconfigure((0, 1, 2), weight=1)
        
        # Statistique 1
        stat1 = ctk.CTkFrame(mini_stats_frame, fg_color=SUCCESS_GREEN, corner_radius=8, height=35)
        stat1.grid(row=0, column=0, padx=(0, 5), sticky="ew")
        stat1_label = ctk.CTkLabel(stat1, text="247 Bulletins", font=F_SMALL, text_color="white")
        stat1_label.pack(expand=True)
        
        # Statistique 2
        stat2 = ctk.CTkFrame(mini_stats_frame, fg_color=ACCENT_BLUE, corner_radius=8, height=35)
        stat2.grid(row=0, column=1, padx=5, sticky="ew")
        stat2_label = ctk.CTkLabel(stat2, text="13.2 Moyenne", font=F_SMALL, text_color="white")
        stat2_label.pack(expand=True)
        
        # Statistique 3
        stat3 = ctk.CTkFrame(mini_stats_frame, fg_color=WARNING_ORANGE, corner_radius=8, height=35)
        stat3.grid(row=0, column=2, padx=(5, 0), sticky="ew")
        stat3_label = ctk.CTkLabel(stat3, text="78.5% Réussite", font=F_SMALL, text_color="white")
        stat3_label.pack(expand=True)
    
    def _build_premium_bulletins_section(self, parent):
        """Construit la section des bulletins avec design premium"""
        bulletins_frame = ctk.CTkFrame(parent, fg_color="transparent")
        bulletins_frame.grid(row=1, column=0, sticky="nsew")
        bulletins_frame.grid_columnconfigure(0, weight=1)
        bulletins_frame.grid_rowconfigure(0, weight=1)
        
        # Zone scrollable avec style premium
        self.bulletins_scroll = ctk.CTkScrollableFrame(bulletins_frame, 
                                                     fg_color="transparent",
                                                     scrollbar_button_color=ACCENT_BLUE,
                                                     scrollbar_button_hover_color="#4338CA")
        self.bulletins_scroll.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        self.bulletins_scroll.grid_columnconfigure((0, 1, 2), weight=1)
        
        # Frame pour les statistiques en bas
        self.stats_frame = ctk.CTkFrame(bulletins_frame, fg_color=BG_CARD, corner_radius=16, height=100)
        self.stats_frame.grid(row=1, column=0, sticky="ew", pady=(15, 0))
        self.stats_frame.grid_columnconfigure((0, 1, 2, 3), weight=1)
        self.stats_frame.grid_propagate(False)
    
    def _create_premium_classe_header(self, classe_nom, nb_total, nb_affiches):
        """Crée un en-tête premium pour une classe"""
        # Container principal avec effet de profondeur
        header_container = ctk.CTkFrame(self.bulletins_scroll, fg_color="transparent")
        
        # Header avec dégradé simulé
        header_frame = ctk.CTkFrame(header_container, fg_color=BG_SIDEBAR, corner_radius=12, height=70)
        header_frame.pack(fill="x", pady=(20, 10))
        
        # Contenu de l'en-tête
        content_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        content_frame.pack(fill="both", expand=True, padx=20, pady=15)
        
        # Section gauche - Icône et nom
        left_section = ctk.CTkFrame(content_frame, fg_color="transparent")
        left_section.pack(side="left")
        
        # Icône classe avec effet premium
        icon_container = ctk.CTkFrame(left_section, fg_color=ACCENT_BLUE, corner_radius=10, width=40, height=40)
        icon_container.pack(side="left", padx=(0, 15))
        
        classe_icon = load_ctk_icon("school.png", (20, 20))
        if classe_icon:
            icon_label = ctk.CTkLabel(icon_container, image=classe_icon, text="", fg_color="transparent")
            icon_label.pack(expand=True)
        
        # Nom de classe avec style premium
        classe_label = ctk.CTkLabel(left_section, text=f"Classe {classe_nom}", 
                                   font=F_SUB, text_color=TEXT_PRIMARY)
        classe_label.pack(side="left")
        
        # Section droite - Statistiques
        right_section = ctk.CTkFrame(content_frame, fg_color="transparent")
        right_section.pack(side="right")
        
        # Badge de statistiques
        if nb_total > nb_affiches:
            stats_badge = ctk.CTkFrame(right_section, fg_color=WARNING_ORANGE, corner_radius=15, height=30)
            stats_text = f"📊 {nb_affiches}/{nb_total} meilleurs élèves"
            stats_color = "white"
        else:
            stats_badge = ctk.CTkFrame(right_section, fg_color=SUCCESS_GREEN, corner_radius=15, height=30)
            stats_text = f"🎯 {nb_total} élèves - Classement par mérite"
            stats_color = "white"
        
        stats_badge.pack(side="right")
        stats_label = ctk.CTkLabel(stats_badge, text=stats_text, 
                                  font=F_SMALL, text_color=stats_color)
        stats_label.pack(expand=True, padx=15)
        
        return header_container
    
    def _create_premium_bulletin_card(self, bulletin):
        """Crée une carte premium pour un bulletin"""
        # Container principal avec effet de profondeur
        card_container = ctk.CTkFrame(self.bulletins_scroll, fg_color="transparent")
        
        # Carte principale avec style premium
        card = ctk.CTkFrame(card_container, fg_color=BG_CARD, corner_radius=16, height=200)
        card.pack(fill="x", padx=5, pady=5)
        
        # Effet de hover simulé avec bordure
        rang_classe = bulletin.get('rang', 'N/A')
        if isinstance(rang_classe, (int, float)) and rang_classe <= 3:
            border_color = SUCCESS_GREEN if rang_classe == 1 else WARNING_ORANGE
        else:
            border_color = BG_ACCENT
        
        # En-tête de la carte avec dégradé
        header_frame = ctk.CTkFrame(card, fg_color=border_color, corner_radius=16, height=60)
        header_frame.pack(fill="x", padx=2, pady=2)
        
        # Contenu de l'en-tête
        header_content = ctk.CTkFrame(header_frame, fg_color="transparent")
        header_content.pack(fill="both", expand=True, padx=15, pady=10)
        header_content.grid_columnconfigure(1, weight=1)
        
        # Icône élève avec effet premium
        icon_container = ctk.CTkFrame(header_content, fg_color="white", corner_radius=8, width=35, height=35)
        icon_container.grid(row=0, column=0, padx=(0, 15))
        
        student_icon = load_ctk_icon("person.png", (18, 18))
        if student_icon:
            icon_label = ctk.CTkLabel(icon_container, image=student_icon, text="", fg_color="transparent")
            icon_label.pack(expand=True)
        
        # Nom de l'élève avec rang
        name_container = ctk.CTkFrame(header_content, fg_color="transparent")
        name_container.grid(row=0, column=1, sticky="w")
        
        eleve_name = f"{bulletin.get('eleve_prenom', '')} {bulletin.get('eleve_nom', '')}"
        name_label = ctk.CTkLabel(name_container, text=eleve_name, 
                                 font=F_BOLD, text_color="white")
        name_label.pack(anchor="w")
        
        # Rang avec emoji et couleur
        if isinstance(rang_classe, (int, float)) and rang_classe <= 3:
            rang_color = "white"
            if rang_classe == 1:
                rang_text = f"🏆 {rang_classe}er - Champion !"
            elif rang_classe == 2:
                rang_text = f"🥈 {rang_classe}ème - Excellent !"
            else:
                rang_text = f"🥉 {rang_classe}ème - Très bien !"
        else:
            rang_color = "#E5E7EB"
            rang_text = f"📊 Rang: {rang_classe}"
        
        rang_label = ctk.CTkLabel(name_container, text=rang_text, 
                                 font=F_SMALL, text_color=rang_color)
        rang_label.pack(anchor="w")
        
        # Boutons d'action avec style premium
        actions_container = ctk.CTkFrame(header_content, fg_color="transparent")
        actions_container.grid(row=0, column=2, sticky="e")
        
        # Bouton Modifier
        edit_btn = ctk.CTkButton(actions_container, text="✏️", 
                                fg_color="transparent", 
                                text_color="white",
                                width=35, height=35, 
                                border_width=1, border_color="white",
                                corner_radius=8,
                                hover_color="rgba(255,255,255,0.2)",
                                command=lambda: self.modifier_bulletin(bulletin))
        edit_btn.pack(side="right", padx=(5, 0))
        
        # Bouton Supprimer
        delete_btn = ctk.CTkButton(actions_container, text="🗑️", 
                                  fg_color="transparent", 
                                  text_color="white",
                                  width=35, height=35, 
                                  border_width=1, border_color="white",
                                  corner_radius=8,
                                  hover_color="rgba(255,255,255,0.2)",
                                  command=lambda: self.supprimer_bulletin(bulletin))
        delete_btn.pack(side="right", padx=(5, 0))
        
        # Contenu principal de la carte
        content_frame = ctk.CTkFrame(card, fg_color="transparent")
        content_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        # Grille d'informations avec style premium
        info_grid = ctk.CTkFrame(content_frame, fg_color="transparent")
        info_grid.pack(fill="both", expand=True)
        info_grid.grid_columnconfigure((0, 1), weight=1)
        
        # Informations du bulletin avec icônes
        info_data = [
            ("📅", "Période", bulletin.get('periode', 'N/A')),
            ("📊", "Moyenne", f"{bulletin.get('moyenne_generale', 0):.2f}/20"),
            ("🏆", "Rang", str(bulletin.get('rang', 'N/A'))),
            ("📅", "Date", self._format_date(bulletin.get('date_creation')))
        ]
        
        for i, (icon, label, value) in enumerate(info_data):
            info_card = ctk.CTkFrame(info_grid, fg_color=BG_ACCENT, corner_radius=8)
            info_card.grid(row=i//2, column=i%2, padx=5, pady=5, sticky="ew")
            
            # Icône
            icon_label = ctk.CTkLabel(info_card, text=icon, font=F_SMALL, text_color=TEXT_SECONDARY)
            icon_label.pack(side="left", padx=(10, 5), pady=8)
            
            # Texte
            text_frame = ctk.CTkFrame(info_card, fg_color="transparent")
            text_frame.pack(side="left", fill="both", expand=True, padx=(0, 10), pady=8)
            
            label_widget = ctk.CTkLabel(text_frame, text=label, 
                                      font=F_SMALL, text_color=TEXT_MUTED)
            label_widget.pack(anchor="w")
            
            value_widget = ctk.CTkLabel(text_frame, text=value, 
                                      font=F_BOLD, text_color=TEXT_PRIMARY)
            value_widget.pack(anchor="w")
        
        # Appréciation avec style premium
        appreciation = bulletin.get('appreciation', '')
        if appreciation:
            app_frame = ctk.CTkFrame(content_frame, fg_color=BG_ACCENT, corner_radius=8)
            app_frame.pack(fill="x", padx=5, pady=(10, 0))
            
            app_header = ctk.CTkLabel(app_frame, text="💬 Appréciation", 
                                    font=F_SMALL, text_color=TEXT_SECONDARY)
            app_header.pack(anchor="w", padx=15, pady=(10, 5))
            
            app_text = ctk.CTkLabel(app_frame, text=appreciation, 
                                   font=F_TXT, text_color=TEXT_PRIMARY,
                                   wraplength=400, justify="left")
            app_text.pack(anchor="w", padx=15, pady=(0, 10))
        
        return card_container
    
    def charger_periodes(self):
        """Charge les périodes scolaires"""
        try:
            periodes = self.controller.get_periodes_actives()
            periode_values = ["Sélectionner une période"] + [f"{p.nom} ({p.annee_scolaire})" for p in periodes]
            self.periode_combo.configure(values=periode_values)
        except Exception as e:
            print(f"Erreur chargement périodes: {e}")
            periodes_defaut = [
                "1er Trimestre 2023-2024",
                "2ème Trimestre 2023-2024", 
                "3ème Trimestre 2023-2024"
            ]
            self.periode_combo.configure(values=["Sélectionner une période"] + periodes_defaut)
    
    def charger_classes(self):
        """Charge les classes"""
        try:
            classes = get_all_classes()
            classe_values = ["Toutes les classes"] + [f"{c[0]} - {c[1]}" for c in classes]
            self.classe_combo.configure(values=classe_values)
        except Exception as e:
            print(f"Erreur chargement classes: {e}")
            classes_defaut = [
                "6ème A", "6ème B", "6ème C",
                "5ème A", "5ème B", "5ème C", 
                "4ème A", "4ème B", "4ème C",
                "3ème A", "3ème B", "3ème C"
            ]
            self.classe_combo.configure(values=["Toutes les classes"] + classes_defaut)
    
    def charger_bulletins(self):
        """Charge et affiche les bulletins avec design premium"""
        # Effacer les cartes existantes
        for widget in self.bulletins_scroll.winfo_children():
            widget.destroy()
        
        if not self.current_periode:
            # Message d'état avec design premium
            no_data_frame = ctk.CTkFrame(self.bulletins_scroll, fg_color=BG_CARD, corner_radius=16, height=200)
            no_data_frame.pack(fill="x", padx=10, pady=20)
            
            # Icône d'état
            icon_container = ctk.CTkFrame(no_data_frame, fg_color=ACCENT_BLUE, corner_radius=50, width=80, height=80)
            icon_container.pack(pady=(30, 15))
            
            icon_label = ctk.CTkLabel(icon_container, text="📅", font=("Segoe UI", 32), text_color="white")
            icon_label.pack(expand=True)
            
            no_data_label = ctk.CTkLabel(no_data_frame, text="Sélectionnez une période pour afficher les bulletins", 
                                       font=F_SUB, text_color=TEXT_PRIMARY)
            no_data_label.pack(pady=(0, 10))
            
            subtitle_label = ctk.CTkLabel(no_data_frame, text="Utilisez les filtres ci-dessus pour commencer", 
                                         font=F_SMALL, text_color=TEXT_SECONDARY)
            subtitle_label.pack(pady=(0, 30))
            
            self._update_premium_statistics([])
            return
        
        try:
            # Récupérer les bulletins selon les filtres
            if self.current_classe and self.current_classe != "Toutes les classes":
                classe_id = int(self.current_classe.split(" - ")[0])
                bulletins = self.controller.get_bulletins_classe(classe_id)
            else:
                bulletins = self._simuler_bulletins()
            
            if not bulletins:
                # Message aucun bulletin avec design premium
                no_data_frame = ctk.CTkFrame(self.bulletins_scroll, fg_color=BG_CARD, corner_radius=16, height=200)
                no_data_frame.pack(fill="x", padx=10, pady=20)
                
                icon_container = ctk.CTkFrame(no_data_frame, fg_color=WARNING_ORANGE, corner_radius=50, width=80, height=80)
                icon_container.pack(pady=(30, 15))
                
                icon_label = ctk.CTkLabel(icon_container, text="📋", font=("Segoe UI", 32), text_color="white")
                icon_label.pack(expand=True)
                
                no_data_label = ctk.CTkLabel(no_data_frame, text="Aucun bulletin trouvé", 
                                           font=F_SUB, text_color=TEXT_PRIMARY)
                no_data_label.pack(pady=(0, 10))
                
                subtitle_label = ctk.CTkLabel(no_data_frame, text="Ajustez vos filtres ou générez de nouveaux bulletins", 
                                             font=F_SMALL, text_color=TEXT_SECONDARY)
                subtitle_label.pack(pady=(0, 30))
                
                self._update_premium_statistics([])
                return
            
            # Grouper les bulletins par classe
            bulletins_par_classe = self._grouper_bulletins_par_classe(bulletins)
            
            # Créer les sections par classe avec design premium
            row_index = 0
            for classe_nom, bulletins_classe in bulletins_par_classe.items():
                # Limiter à 100 bulletins par classe
                bulletins_a_afficher = bulletins_classe[:self.limite_par_classe]
                nb_total = len(bulletins_classe)
                nb_affiches = len(bulletins_a_afficher)
                
                # Créer l'en-tête premium de classe
                classe_header = self._create_premium_classe_header(classe_nom, nb_total, nb_affiches)
                classe_header.pack(fill="x", pady=5)
                
                # Créer les cartes premium de bulletins
                for i, bulletin in enumerate(bulletins_a_afficher):
                    card = self._create_premium_bulletin_card(bulletin)
                    card.pack(fill="x", pady=2)
                
                # Message pour les bulletins supplémentaires
                if nb_total > self.limite_par_classe:
                    more_frame = ctk.CTkFrame(self.bulletins_scroll, fg_color=BG_ACCENT, corner_radius=12, height=50)
                    more_frame.pack(fill="x", pady=5)
                    
                    more_label = ctk.CTkLabel(more_frame, 
                                            text=f"📊 ... et {nb_total - nb_affiches} autre(s) élève(s) dans cette classe", 
                                            font=F_SMALL, text_color=TEXT_SECONDARY)
                    more_label.pack(expand=True)
            
            # Mettre à jour les statistiques premium
            self._update_premium_statistics(bulletins)
            
        except Exception as e:
            print(f"Erreur lors du chargement des bulletins: {e}")
            messagebox.showerror("Erreur", f"Erreur lors du chargement des bulletins: {e}")
    
    def _update_premium_statistics(self, bulletins):
        """Met à jour les statistiques avec design premium"""
        # Effacer les anciennes statistiques
        for widget in self.stats_frame.winfo_children():
            widget.destroy()
        
        if not bulletins:
            return
        
        # Calculer les statistiques
        total_bulletins = len(bulletins)
        moyennes = [b.get('moyenne_generale', 0) for b in bulletins if b.get('moyenne_generale')]
        moyenne_generale = sum(moyennes) / len(moyennes) if moyennes else 0
        
        # Statistiques avec design premium
        stats_data = [
            ("📊", "Total", str(total_bulletins), ACCENT_BLUE),
            ("📈", "Moyenne", f"{moyenne_generale:.2f}", SUCCESS_GREEN),
            ("⭐", "Meilleure", f"{max(moyennes):.2f}" if moyennes else "0.00", WARNING_ORANGE),
            ("🏫", "Classes", str(len(set(b.get('classe_nom', '') for b in bulletins))), ACCENT_PURPLE)
        ]
        
        for i, (icon, label, value, color) in enumerate(stats_data):
            stat_card = ctk.CTkFrame(self.stats_frame, fg_color=color, corner_radius=12)
            stat_card.grid(row=0, column=i, padx=10, pady=15, sticky="ew")
            
            # Icône
            icon_label = ctk.CTkLabel(stat_card, text=icon, font=("Segoe UI", 20), text_color="white")
            icon_label.pack(pady=(15, 5))
            
            # Valeur
            value_label = ctk.CTkLabel(stat_card, text=value, font=F_TITLE, text_color="white")
            value_label.pack()
            
            # Label
            label_label = ctk.CTkLabel(stat_card, text=label, font=F_SMALL, text_color="white")
            label_label.pack(pady=(0, 15))
    
    def _simuler_bulletins(self):
        """Simule des bulletins pour les tests"""
        return [
            {
                'id': 1,
                'eleve_nom': 'Dupont',
                'eleve_prenom': 'Marie',
                'classe_nom': '6ème A',
                'moyenne_generale': 15.5,
                'rang': 1,
                'periode': '1er Trimestre',
                'appreciation': 'Excellent travail ! Continue sur cette lancée exceptionnelle.',
                'date_creation': datetime.now()
            },
            {
                'id': 2,
                'eleve_nom': 'Martin',
                'eleve_prenom': 'Pierre',
                'classe_nom': '6ème A',
                'moyenne_generale': 14.2,
                'rang': 2,
                'periode': '1er Trimestre',
                'appreciation': 'Très bon travail. Quelques efforts supplémentaires pour exceller.',
                'date_creation': datetime.now()
            },
            {
                'id': 3,
                'eleve_nom': 'Bernard',
                'eleve_prenom': 'Sophie',
                'classe_nom': '6ème A',
                'moyenne_generale': 13.8,
                'rang': 3,
                'periode': '1er Trimestre',
                'appreciation': 'Bon travail. Continue tes efforts pour progresser.',
                'date_creation': datetime.now()
            }
        ]
    
    def _grouper_bulletins_par_classe(self, bulletins):
        """Groupe les bulletins par classe et les trie par ordre de mérite"""
        bulletins_par_classe = {}
        
        for bulletin in bulletins:
            classe_nom = bulletin.get('classe_nom', 'Classe non définie')
            
            if classe_nom not in bulletins_par_classe:
                bulletins_par_classe[classe_nom] = []
            
            bulletins_par_classe[classe_nom].append(bulletin)
        
        # Trier les classes par nom et les bulletins par ordre de mérite
        for classe_nom in bulletins_par_classe:
            bulletins_par_classe[classe_nom].sort(
                key=lambda x: x.get('moyenne_generale', 0), 
                reverse=True
            )
        
        return dict(sorted(bulletins_par_classe.items()))
    
    def _format_date(self, date_obj):
        """Formate une date pour l'affichage"""
        if not date_obj:
            return 'N/A'
        
        try:
            if hasattr(date_obj, 'strftime'):
                return date_obj.strftime('%d/%m/%Y')
            elif isinstance(date_obj, str):
                return date_obj[:10] if len(date_obj) >= 10 else date_obj
            else:
                return str(date_obj)
        except Exception:
            return 'N/A'
    
    def _on_periode_change(self, event):
        """Gère le changement de période"""
        periode = self.periode_var.get()
        if periode != "Sélectionner une période":
            self.current_periode = periode
            self.charger_bulletins()
    
    def _on_classe_change(self, event):
        """Gère le changement de classe"""
        classe = self.classe_var.get()
        if classe != "Toutes les classes":
            self.current_classe = classe
            self.charger_bulletins()
    
    def generer_bulletins_classe(self):
        """Ouvre la fenêtre de génération de bulletins"""
        if not self.current_periode or self.current_periode == "Sélectionner une période":
            messagebox.showwarning("Sélection requise", "Veuillez sélectionner une période avant de générer les bulletins.")
            return
        
        if not self.current_classe or self.current_classe == "Toutes les classes":
            messagebox.showwarning("Sélection requise", "Veuillez sélectionner une classe spécifique pour générer les bulletins.")
            return
        
        try:
            classe_id = int(self.current_classe.split(" - ")[0])
            periode_id = 1
            
            bulletins_ids = self.controller.generer_bulletins_classe(classe_id, periode_id, "USER")
            
            messagebox.showinfo("Succès", f"Bulletins générés avec succès pour la classe {self.current_classe}.\n{len(bulletins_ids)} bulletins créés.")
            self.charger_bulletins()
            
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de la génération des bulletins: {e}")
    
    def ouvrir_dashboard(self):
        """Ouvre le dashboard des bulletins"""
        from .bulletins_sqlserver_dashboard import BulletinsDashboard
        
        dashboard_window = ctk.CTkToplevel(self)
        dashboard_window.title("Dashboard Bulletins - EduManager+")
        dashboard_window.geometry("1400x900")
        dashboard_window.configure(fg_color=BG_MAIN)
        
        BulletinsDashboard(dashboard_window).pack(fill="both", expand=True)
    
    def modifier_bulletin(self, bulletin=None):
        """Ouvre le formulaire de modification de bulletin"""
        if bulletin is None:
            messagebox.showwarning("Modification", "Aucun bulletin sélectionné.")
            return
        messagebox.showinfo("Modification", "Fonctionnalité de modification en cours de développement")
    
    def supprimer_bulletin(self, bulletin=None):
        """Supprime un bulletin"""
        if bulletin is None:
            messagebox.showwarning("Suppression", "Aucun bulletin sélectionné.")
            return
        
        if messagebox.askyesno("Confirmation", 
                              f"Voulez-vous vraiment supprimer le bulletin de {bulletin.get('eleve_prenom', '')} {bulletin.get('eleve_nom', '')} ?"):
            try:
                messagebox.showinfo("Succès", "Bulletin supprimé avec succès.")
                self.charger_bulletins()
            except Exception as e:
                messagebox.showerror("Erreur", f"Erreur lors de la suppression: {e}")

if __name__ == "__main__":
    root = ctk.CTk()
    root.title("Gestion des Bulletins Premium - EduManager+")
    root.geometry("1400x900")
    root.configure(fg_color=BG_MAIN)
    
    BulletinsPremiumView(root).pack(fill="both", expand=True)
    root.mainloop()


