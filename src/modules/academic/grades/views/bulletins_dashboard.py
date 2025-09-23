"""
Dashboard moderne et professionnel pour la gestion des bulletins
Interface utilisateur avancée avec statistiques et visualisations
"""

import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox, ttk
from PIL import Image, ImageTk
import os
import sys
from typing import List, Dict, Optional
from datetime import datetime, date

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
    from theme import *  # pyright: ignore[reportMissingImports]
    sys.path.insert(0, os.path.join(resources_path, "fonts"))
    from fonts import *  # pyright: ignore[reportMissingImports]
    sys.path.insert(0, icons_path)
    from icons import *  # pyright: ignore[reportMissingImports]  # pyright: ignore[reportMissingImports]
except ImportError:
    # Fallback si les imports échouent
    BG_MAIN = "#0A192F"
    BG_CARD = "#1E293B"
    BG_SIDEBAR = "#0F172A"
    TEXT_PRIMARY = "#F1F5F9"
    TEXT_SECONDARY = "#94A3B8"
    ACCENT_BLUE = "#3B82F6"
    SUCCESS_GREEN = "#10B981"
    ERROR_RED = "#EF4444"
    WARNING_ORANGE = "#F59E0B"
    F_TITLE = ("Segoe UI", 18, "bold")
    F_SUB = ("Segoe UI", 14, "bold")
    F_TXT = ("Segoe UI", 12)
    F_SMALL = ("Segoe UI", 10)
    F_BOLD = ("Segoe UI", 12, "bold")

def load_ctk_icon(icon_name, size=(20, 20)):
    """Charge une icône depuis le dossier resources/icons"""
    try:
        icon_path = os.path.join(icons_path, icon_name)
        
        if os.path.exists(icon_path):
            return ctk.CTkImage(Image.open(icon_path), size=size)
        else:
            print(f"⚠️ Icône non trouvée: {icon_path}")
            return None
    except Exception as e:
        print(f"❌ Erreur chargement icône {icon_name}: {e}")
        return None

class BulletinsDashboard(ctk.CTkFrame):
    """Dashboard moderne pour la gestion des bulletins"""
    
    def __init__(self, parent):
        super().__init__(parent, fg_color=BG_MAIN)
        
        # Configuration de la grille
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        
        # Variables
        self.current_periode = None
        self.current_classe = None
        self.bulletins_data = []
        
        # Construire l'interface
        self._build_header()
        self._build_main_content()
        
        # Charger les données initiales
        self.charger_periodes()
        self.charger_classes()
        self.charger_statistiques()
    
    def _build_header(self):
        """Construit l'en-tête du dashboard"""
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.grid(row=0, column=0, sticky="ew", padx=20, pady=(20, 10))
        header_frame.grid_columnconfigure(1, weight=1)
        
        # Titre et icône
        title_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        title_frame.grid(row=0, column=0, sticky="w")
        
        # Icône bulletins
        bulletin_icon = load_ctk_icon("newspaper.png", (32, 32))
        if bulletin_icon:
            icon_label = ctk.CTkLabel(title_frame, image=bulletin_icon, text="")
            icon_label.pack(side="left", padx=(0, 15))
        
        # Titre
        title_label = ctk.CTkLabel(title_frame, text="Dashboard Bulletins", 
                                 font=F_TITLE, text_color=TEXT_PRIMARY)
        title_label.pack(side="left")
        
        # Actions principales
        actions_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        actions_frame.grid(row=0, column=1, sticky="e")
        
        # Bouton Générer Bulletins
        generate_icon = load_ctk_icon("add.png", (18, 18))
        generate_btn = ctk.CTkButton(actions_frame, text="Générer Bulletins", image=generate_icon,
                                   fg_color=SUCCESS_GREEN, text_color="white",
                                   font=F_BOLD, height=40, width=150,
                                   command=self.generer_bulletins)
        generate_btn.pack(side="right", padx=(5, 0))
        
        # Bouton Rapports
        report_icon = load_ctk_icon("chart.png", (18, 18))
        report_btn = ctk.CTkButton(actions_frame, text="Rapports", image=report_icon,
                                  fg_color=ACCENT_BLUE, text_color="white",
                                  font=F_BOLD, height=40, width=120,
                                  command=self.ouvrir_rapports)
        report_btn.pack(side="right", padx=(5, 0))
        
        # Bouton Actualiser
        refresh_icon = load_ctk_icon("refresh.png", (18, 18))
        refresh_btn = ctk.CTkButton(actions_frame, text="Actualiser", image=refresh_icon,
                                   fg_color=WARNING_ORANGE, text_color="white",
                                   font=F_BOLD, height=40, width=120,
                                   command=self.actualiser_dashboard)
        refresh_btn.pack(side="right", padx=(5, 0))
    
    def _build_main_content(self):
        """Construit le contenu principal du dashboard"""
        main_frame = ctk.CTkFrame(self, fg_color="transparent")
        main_frame.grid(row=1, column=0, sticky="nsew", padx=20, pady=(0, 20))
        main_frame.grid_columnconfigure(0, weight=1)
        main_frame.grid_rowconfigure(1, weight=1)
        
        # Section des filtres et contrôles
        self._build_controls_section(main_frame)
        
        # Section principale avec statistiques et bulletins
        self._build_content_section(main_frame)
    
    def _build_controls_section(self, parent):
        """Construit la section des contrôles et filtres"""
        controls_frame = ctk.CTkFrame(parent, fg_color=BG_CARD, corner_radius=12)
        controls_frame.grid(row=0, column=0, sticky="ew", pady=(0, 15))
        controls_frame.grid_columnconfigure((0, 1, 2, 3), weight=1)
        
        # Filtre par période
        periode_label = ctk.CTkLabel(controls_frame, text="Période:", 
                                   font=F_BOLD, text_color=TEXT_PRIMARY)
        periode_label.grid(row=0, column=0, padx=20, pady=15, sticky="w")
        
        self.periode_var = ctk.StringVar(value="Sélectionner une période")
        self.periode_combo = ctk.CTkComboBox(controls_frame, values=["Sélectionner une période"],
                                           variable=self.periode_var, font=F_TXT, height=35, width=200)
        self.periode_combo.grid(row=0, column=1, padx=(0, 20), pady=15, sticky="w")
        self.periode_combo.bind("<<ComboboxSelected>>", self._on_periode_change)
        
        # Filtre par classe
        classe_label = ctk.CTkLabel(controls_frame, text="Classe:", 
                                   font=F_BOLD, text_color=TEXT_PRIMARY)
        classe_label.grid(row=0, column=2, padx=(20, 5), pady=15, sticky="w")
        
        self.classe_var = ctk.StringVar(value="Toutes les classes")
        self.classe_combo = ctk.CTkComboBox(controls_frame, values=["Toutes les classes"],
                                          variable=self.classe_var, font=F_TXT, height=35, width=200)
        self.classe_combo.grid(row=0, column=3, padx=(0, 20), pady=15, sticky="w")
        self.classe_combo.bind("<<ComboboxSelected>>", self._on_classe_change)
    
    def _build_content_section(self, parent):
        """Construit la section principale du contenu"""
        content_frame = ctk.CTkFrame(parent, fg_color="transparent")
        content_frame.grid(row=1, column=0, sticky="nsew")
        content_frame.grid_columnconfigure(0, weight=2)
        content_frame.grid_columnconfigure(1, weight=1)
        content_frame.grid_rowconfigure(0, weight=1)
        
        # Section des bulletins (gauche)
        self._build_bulletins_section(content_frame)
        
        # Section des statistiques (droite)
        self._build_statistics_section(content_frame)
    
    def _build_bulletins_section(self, parent):
        """Construit la section des bulletins"""
        bulletins_frame = ctk.CTkFrame(parent, fg_color=BG_CARD, corner_radius=12)
        bulletins_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        bulletins_frame.grid_columnconfigure(0, weight=1)
        bulletins_frame.grid_rowconfigure(1, weight=1)
        
        # En-tête de la section
        header_frame = ctk.CTkFrame(bulletins_frame, fg_color="transparent")
        header_frame.pack(fill="x", padx=20, pady=(20, 10))
        
        bulletins_title = ctk.CTkLabel(header_frame, text="Bulletins par Classe", 
                                      font=F_SUB, text_color=TEXT_PRIMARY)
        bulletins_title.pack(side="left")
        
        # Zone scrollable pour les bulletins
        self.bulletins_scroll = ctk.CTkScrollableFrame(bulletins_frame, fg_color="transparent")
        self.bulletins_scroll.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        self.bulletins_scroll.grid_columnconfigure((0, 1, 2), weight=1)
    
    def _build_statistics_section(self, parent):
        """Construit la section des statistiques"""
        stats_frame = ctk.CTkFrame(parent, fg_color=BG_CARD, corner_radius=12)
        stats_frame.grid(row=0, column=1, sticky="nsew", padx=(10, 0))
        stats_frame.grid_columnconfigure(0, weight=1)
        stats_frame.grid_rowconfigure(1, weight=1)
        
        # En-tête des statistiques
        stats_header = ctk.CTkFrame(stats_frame, fg_color="transparent")
        stats_header.pack(fill="x", padx=20, pady=(20, 10))
        
        stats_title = ctk.CTkLabel(stats_header, text="Statistiques", 
                                  font=F_SUB, text_color=TEXT_PRIMARY)
        stats_title.pack(side="left")
        
        # Zone des statistiques
        self.stats_content = ctk.CTkScrollableFrame(stats_frame, fg_color="transparent")
        self.stats_content.pack(fill="both", expand=True, padx=20, pady=(0, 20))
    
    def charger_periodes(self):
        """Charge les périodes scolaires"""
        try:
            # Simuler le chargement des périodes
            periodes = [
                "1er Trimestre 2023-2024",
                "2ème Trimestre 2023-2024", 
                "3ème Trimestre 2023-2024",
                "1er Semestre 2023-2024",
                "2ème Semestre 2023-2024",
                "Année 2023-2024"
            ]
            
            self.periode_combo.configure(values=["Sélectionner une période"] + periodes)
        except Exception as e:
            print(f"Erreur chargement périodes: {e}")
    
    def charger_classes(self):
        """Charge les classes"""
        try:
            # Simuler le chargement des classes
            classes = [
                "6ème A", "6ème B", "6ème C",
                "5ème A", "5ème B", "5ème C", 
                "4ème A", "4ème B", "4ème C",
                "3ème A", "3ème B", "3ème C"
            ]
            
            self.classe_combo.configure(values=["Toutes les classes"] + classes)
        except Exception as e:
            print(f"Erreur chargement classes: {e}")
    
    def charger_statistiques(self):
        """Charge et affiche les statistiques"""
        # Effacer les anciennes statistiques
        for widget in self.stats_content.winfo_children():
            widget.destroy()
        
        # Statistiques globales
        stats_data = [
            ("Total Bulletins", "1,247", "newspaper.png", ACCENT_BLUE),
            ("Moyenne Générale", "13.2/20", "trending_up.png", SUCCESS_GREEN),
            ("Taux de Réussite", "78.5%", "check_circle.png", SUCCESS_GREEN),
            ("Classes Actives", "12", "school.png", WARNING_ORANGE),
            ("Périodes", "6", "calendar.png", ERROR_RED),
            ("Meilleure Classe", "3ème A", "star.png", SUCCESS_GREEN)
        ]
        
        for i, (label, value, icon_name, color) in enumerate(stats_data):
            stat_card = self._create_stat_card(label, value, icon_name, color)
            stat_card.pack(fill="x", pady=5)
    
    def _create_stat_card(self, label, value, icon_name, color):
        """Crée une carte de statistique"""
        card = ctk.CTkFrame(self.stats_content, fg_color=BG_SIDEBAR, corner_radius=8)
        
        # Contenu de la carte
        content_frame = ctk.CTkFrame(card, fg_color="transparent")
        content_frame.pack(fill="x", padx=15, pady=10)
        
        # Icône
        icon = load_ctk_icon(icon_name, (20, 20))
        if icon:
            icon_label = ctk.CTkLabel(content_frame, image=icon, text="")
            icon_label.pack(side="left", padx=(0, 10))
        
        # Texte
        text_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        text_frame.pack(side="left", fill="x", expand=True)
        
        value_label = ctk.CTkLabel(text_frame, text=value, 
                                  font=F_SUB, text_color=color)
        value_label.pack(anchor="w")
        
        label_label = ctk.CTkLabel(text_frame, text=label, 
                                  font=F_SMALL, text_color=TEXT_SECONDARY)
        label_label.pack(anchor="w")
        
        return card
    
    def _create_classe_section(self, classe_nom, bulletins):
        """Crée une section pour une classe"""
        section_frame = ctk.CTkFrame(self.bulletins_scroll, fg_color=BG_SIDEBAR, corner_radius=8)
        
        # En-tête de classe
        header_frame = ctk.CTkFrame(section_frame, fg_color="transparent")
        header_frame.pack(fill="x", padx=15, pady=(15, 10))
        
        # Icône classe
        classe_icon = load_ctk_icon("school.png", (20, 20))
        if classe_icon:
            icon_label = ctk.CTkLabel(header_frame, image=classe_icon, text="")
            icon_label.pack(side="left", padx=(0, 10))
        
        # Nom de classe
        classe_label = ctk.CTkLabel(header_frame, text=f"Classe {classe_nom}", 
                                   font=F_SUB, text_color=TEXT_PRIMARY)
        classe_label.pack(side="left")
        
        # Statistiques de classe
        stats_label = ctk.CTkLabel(header_frame, text=f"({len(bulletins)} élèves - Moyenne: 13.5/20)", 
                                  font=F_SMALL, text_color=TEXT_SECONDARY)
        stats_label.pack(side="left", padx=(10, 0))
        
        # Top 3 élèves
        top_frame = ctk.CTkFrame(section_frame, fg_color="transparent")
        top_frame.pack(fill="x", padx=15, pady=(0, 15))
        
        top_label = ctk.CTkLabel(top_frame, text="🏆 Top 3:", 
                                font=F_BOLD, text_color=SUCCESS_GREEN)
        top_label.pack(anchor="w")
        
        for i, bulletin in enumerate(bulletins[:3]):
            rank_icon = "🥇" if i == 0 else "🥈" if i == 1 else "🥉"
            eleve_text = f"{rank_icon} {bulletin['eleve_prenom']} {bulletin['eleve_nom']} - {bulletin['moyenne_generale']:.2f}/20"
            
            eleve_label = ctk.CTkLabel(top_frame, text=eleve_text, 
                                      font=F_SMALL, text_color=TEXT_PRIMARY)
            eleve_label.pack(anchor="w", padx=(20, 0), pady=2)
        
        return section_frame
    
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
    
    def charger_bulletins(self):
        """Charge et affiche les bulletins"""
        # Effacer les anciens bulletins
        for widget in self.bulletins_scroll.winfo_children():
            widget.destroy()
        
        if not self.current_periode:
            return
        
        # Simuler des données de bulletins
        classes_data = {
            "6ème A": [
                {"eleve_nom": "Dupont", "eleve_prenom": "Marie", "moyenne_generale": 15.5},
                {"eleve_nom": "Martin", "eleve_prenom": "Pierre", "moyenne_generale": 14.2},
                {"eleve_nom": "Bernard", "eleve_prenom": "Sophie", "moyenne_generale": 13.8}
            ],
            "5ème B": [
                {"eleve_nom": "Leroy", "eleve_prenom": "Thomas", "moyenne_generale": 16.1},
                {"eleve_nom": "Moreau", "eleve_prenom": "Emma", "moyenne_generale": 15.7},
                {"eleve_nom": "Petit", "eleve_prenom": "Lucas", "moyenne_generale": 14.9}
            ],
            "3ème A": [
                {"eleve_nom": "Roux", "eleve_prenom": "Camille", "moyenne_generale": 17.2},
                {"eleve_nom": "Simon", "eleve_prenom": "Antoine", "moyenne_generale": 16.8},
                {"eleve_nom": "Laurent", "eleve_prenom": "Chloé", "moyenne_generale": 16.3}
            ]
        }
        
        # Filtrer par classe si sélectionnée
        if self.current_classe and self.current_classe != "Toutes les classes":
            classes_data = {self.current_classe: classes_data.get(self.current_classe, [])}
        
        # Créer les sections de classes
        for classe_nom, bulletins in classes_data.items():
            if bulletins:  # Seulement si la classe a des bulletins
                section = self._create_classe_section(classe_nom, bulletins)
                section.pack(fill="x", pady=5)
    
    def generer_bulletins(self):
        """Ouvre la fenêtre de génération de bulletins"""
        messagebox.showinfo("Génération", "Fonctionnalité de génération de bulletins en cours de développement")
    
    def ouvrir_rapports(self):
        """Ouvre la fenêtre des rapports"""
        messagebox.showinfo("Rapports", "Fonctionnalité de rapports en cours de développement")
    
    def actualiser_dashboard(self):
        """Actualise le dashboard"""
        self.charger_statistiques()
        self.charger_bulletins()

if __name__ == "__main__":
    root = ctk.CTk()
    root.title("Dashboard Bulletins - EduManager+")
    root.geometry("1400x900")
    root.configure(fg_color=BG_MAIN)
    
    BulletinsDashboard(root).pack(fill="both", expand=True)
    root.mainloop()


