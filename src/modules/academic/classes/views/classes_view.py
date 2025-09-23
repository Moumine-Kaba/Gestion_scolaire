#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gestion des Classes - Vue Manager
=================================

Interface de gestion des classes scolaires avec design moderne.
"""

import customtkinter as ctk
from tkinter import messagebox, ttk
from PIL import Image
import os
import sys
from datetime import datetime, timedelta

# Import du thème global
try:
    import sys
    import os
    # Ajouter le chemin racine au sys.path
    root_path = os.path.join(os.path.dirname(__file__), '../../../../..')
    sys.path.insert(0, root_path)
    
    from resources.themes.theme import *
    print("✅ Thème global importé pour ClassesManagerView")
except ImportError as e:
    print(f"⚠️ Erreur import thème: {e}")
    # Fallback avec constantes locales
    PRIMARY_BLUE = "#00D4FF"
    DARK_BLUE = "#0D1117"
    DEEPER_BLUE = "#010409"
    NAVY_BLUE = "#161B22"
    DARKER_BLUE = "#21262D"
    LIGHT_BLUE = "#58A6FF"
    ACCENT_BLUE = "#00D4FF"
    SOFT_BLUE = "#F0F6FC"
    PALE_BLUE = "#8B949E"
    MUTED_BLUE = "#6E7681"
    DARK_GRAY = "#21262D"
    MEDIUM_GRAY = "#30363D"
    LIGHT_GRAY = "#484F58"
    WHITE = "#FFFFFF"
    OFF_WHITE = "#F0F6FC"
    PURE_WHITE = "#FFFFFF"
    SUCCESS_GREEN = "#3FB950"
    WARNING_YELLOW = "#D29922"
    WARNING_ORANGE = "#FF7B00"
    ERROR_RED = "#F85149"
    INFO_ORANGE = "#FF7B00"

# Import des contrôleurs
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.modules.academic.classes.controllers.classe_controller import (
    get_all_classes, add_classe, update_classe, delete_classe, get_classe_by_id
)
from src.modules.academic.teachers.controllers.professeur_controller import get_all_professeurs
from src.modules.academic.students.controllers.eleve_controller import get_all_eleves

def load_icon(icon_path, size=(20, 20)):
    """Charge une icône avec gestion d'erreur"""
    try:
        if not icon_path:
            return None
            
        # Construire le chemin complet depuis la racine du projet
        if not os.path.isabs(icon_path):
            # Si le chemin n'est pas absolu, l'ajouter depuis la racine du projet
            project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../../..'))
            icon_path = os.path.join(project_root, icon_path)
            
        if not os.path.exists(icon_path):
            print(f"⚠️ Fichier icône introuvable: {icon_path}")
            return None
            
        image = Image.open(icon_path)
        if isinstance(size, int):
            size = (size, size)
        
        image = image.resize(size, Image.Resampling.LANCZOS)
        return ctk.CTkImage(light_image=image, dark_image=image, size=size)
        
    except Exception as e:
        print(f"⚠️ Erreur chargement icône {icon_path}: {e}")
        return None

class ClassesManagerView(ctk.CTkFrame):
    """
    Vue de gestion des classes scolaires
    """
    
    def __init__(self, parent, icons=None):
        super().__init__(parent)
        
        self.icons = icons or {}
        self.setup_ui()
        self.load_classes()
        
    def setup_ui(self):
        """Configure l'interface utilisateur"""
        # Configuration du frame principal avec le style des cartes
        self.configure(fg_color=DARK_BLUE)
        
        # Container principal avec style carte
        main_container = ctk.CTkFrame(self, fg_color=BG_CARD, corner_radius=20, border_width=2, border_color=BORDER_COLOR)
        main_container.pack(fill="both", expand=True, padx=3, pady=3)
        
        # Header avec titre et contrôles
        self.create_header(main_container)
        
        # Section des cartes sans pagination
        self.create_cards_section(main_container)
        
        # Variables (pagination désactivée)
        self.all_classes = []
        self.cards = []
        
    def create_header(self, parent):
        """Crée l'en-tête avec titre et contrôles"""
        header_frame = ctk.CTkFrame(parent, fg_color="transparent")
        header_frame.pack(fill="x", padx=15, pady=15)
        
        # Section gauche - Titre
        left_section = ctk.CTkFrame(header_frame, fg_color="transparent")
        left_section.pack(side="left", fill="y")
        
        # Logo et titre
        logo_icon = load_icon("resources/icons/classroom.png", 24)
        if logo_icon:
            logo_label = ctk.CTkLabel(left_section, image=logo_icon, text="")
            logo_label.pack(side="left", padx=(0, 10))
        
        title_label = ctk.CTkLabel(
            left_section,
            text="Gestion des Classes",
            font=("Segoe UI", 20, "bold"),
            text_color=TEXT_PRIMARY,
            fg_color="transparent"
        )
        title_label.pack(side="left")
        
        # Section droite - Contrôles
        right_section = ctk.CTkFrame(header_frame, fg_color="transparent")
        right_section.pack(side="right", fill="y")
        
        # Bouton d'ajout
        add_icon = load_icon("resources/icons/add.png", 16)
        add_btn = ctk.CTkButton(
            right_section,
            text="Ajouter",
            image=add_icon,
            fg_color="transparent",
            text_color=TEXT_PRIMARY,
            hover_color=HOVER_SUCCESS,
            command=self.add_classe,
            corner_radius=10,
            height=40,
            width=100,
            border_width=2,
            border_color=BORDER_COLOR,
            font=("Segoe UI", 12, "bold")
        )
        add_btn.pack(side="right", padx=(10, 0))
        
        # Bouton actualiser
        refresh_icon = load_icon("resources/icons/refresh.png", 16)
        refresh_btn = ctk.CTkButton(
            right_section,
            text="Actualiser",
            image=refresh_icon,
            fg_color="transparent",
            text_color=TEXT_PRIMARY,
            hover_color=BG_CARD_HOVER,
            command=self.load_classes,
            corner_radius=10,
            height=40,
            width=100,
            border_width=2,
            border_color=BORDER_COLOR,
            font=("Segoe UI", 12, "bold")
        )
        refresh_btn.pack(side="right", padx=(10, 0))
        
    def create_cards_section(self, parent):
        """Crée la section des cartes de classes avec scroll"""
        # Container principal avec scroll
        self.scrollable_frame = ctk.CTkScrollableFrame(
            parent, 
            fg_color="transparent",
            scrollbar_button_color=BORDER_COLOR,
            scrollbar_button_hover_color=TEXT_SECONDARY
        )
        self.scrollable_frame.pack(fill="both", expand=True, padx=15, pady=(0, 15))
        
        # Frame pour les cartes dans le scroll
        self.cards_frame = ctk.CTkFrame(self.scrollable_frame, fg_color="transparent")
        self.cards_frame.pack(fill="both", expand=True)
        
        # Configuration de la grille pour 6 cartes par ligne (flexible selon le nombre de classes)
        self.cards_frame.grid_columnconfigure((0, 1, 2, 3, 4, 5), weight=1)
        
        
    def load_classes(self):
        """Charge la liste des classes et affiche les cartes"""
        try:
            # Charger les classes
            classes = get_all_classes()
            
            if classes:
                # Trier les classes de manière ordonnée (1ère à TSM)
                self.all_classes = self.sort_classes_by_order(classes)
            else:
                self.all_classes = []
                
            # Afficher toutes les classes sans pagination
            self.display_cards()
                
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors du chargement des classes: {str(e)}")
            
    def sort_classes_by_order(self, classes):
        """Trie les classes de manière ordonnée de la 1ère à TSM"""
        def get_class_order(classe):
            nom = classe.get('nom', '').upper()
            
            # Ordre des niveaux : Primaire -> Collège -> Lycée -> Terminale
            order_map = {
                # Primaire
                '1ERE': 1, '1°': 1, '1ER': 1, '1ÈRE': 1,
                '2EME': 2, '2°': 2, '2ÈME': 2,
                '3EME': 3, '3°': 3, '3ÈME': 3,
                '4EME': 4, '4°': 4, '4ÈME': 4,
                '5EME': 5, '5°': 5, '5ÈME': 5,
                '6EME': 6, '6°': 6, '6ÈME': 6,
                
                # Collège
                '7EME': 7, '7°': 7, '7ÈME': 7,
                '8EME': 8, '8°': 8, '8ÈME': 8,
                '9EME': 9, '9°': 9, '9ÈME': 9,
                '10EME': 10, '10°': 10, '10ÈME': 10,
                
                # Lycée
                '11EME': 11, '11°': 11, '11ÈME': 11,
                '12EME': 12, '12°': 12, '12ÈME': 12,
                
                # Terminale
                'TLE': 13, 'TERMINALE': 13, 'T': 13,
                'TSM': 14, 'TSE': 15, 'TSS': 16
            }
            
            # Chercher le niveau dans le nom
            for key, order in order_map.items():
                if key in nom:
                    # Pour les terminales, ajouter un sous-ordre basé sur la spécialité
                    if order == 13:  # Terminale générale
                        if 'TSM' in nom or 'SM' in nom:
                            return 14  # TSM
                        elif 'TSE' in nom or 'SE' in nom:
                            return 15  # TSE  
                        elif 'TSS' in nom or 'SS' in nom:
                            return 16  # TSS
                        else:
                            return 13  # Terminale générale
                    return order
            
            # Si pas trouvé, essayer d'extraire un numéro
            import re
            numbers = re.findall(r'\d+', nom)
            if numbers:
                return int(numbers[0])
                
            # Par défaut, mettre à la fin
            return 999
            
        # Trier les classes
        sorted_classes = sorted(classes, key=get_class_order)
        return sorted_classes
            
    def display_cards(self):
        """Affiche toutes les cartes de classes avec scroll"""
        # Supprimer les cartes existantes
        for widget in self.cards_frame.winfo_children():
            widget.destroy()
        self.cards.clear()
        
        if not self.all_classes:
            # Afficher message si aucune classe
            no_data_label = ctk.CTkLabel(
                self.cards_frame,
                text="Aucune classe trouvée",
                font=("Segoe UI", 16),
                text_color=TEXT_SECONDARY
            )
            no_data_label.pack(pady=50)
            return
        
        # Afficher TOUTES les classes avec scroll
        for i, classe in enumerate(self.all_classes):
            row = i // 6  # 6 cartes par ligne
            col = i % 6   # Colonnes de 0 à 5
            
            card = self.create_classe_card(classe)
            card.grid(row=row, column=col, padx=8, pady=8, sticky="nsew")
            self.cards.append(card)
            
    def create_classe_card(self, classe):
        """Crée une carte pour une classe"""
        card = ctk.CTkFrame(
            self.cards_frame,
            fg_color=BG_CARD,
            corner_radius=12,
            border_width=1,
            border_color=BORDER_COLOR,
            height=160
        )
        
        # Header de la carte
        header_frame = ctk.CTkFrame(card, fg_color="transparent")
        header_frame.pack(fill="x", padx=15, pady=(15, 10))
        
        # Icône et nom de la classe
        icon_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        icon_frame.pack(side="left")
        
        class_icon = load_icon("resources/icons/classroom.png", 20)
        if class_icon:
            icon_label = ctk.CTkLabel(icon_frame, image=class_icon, text="")
            icon_label.pack(side="left", padx=(0, 8))
        
        # Nom de la classe
        name_label = ctk.CTkLabel(
            header_frame,
            text=classe.get('nom', 'Classe sans nom'),
            font=("Segoe UI", 14, "bold"),
            text_color=TEXT_PRIMARY
        )
        name_label.pack(side="left")
        
        # Contenu de la carte
        content_frame = ctk.CTkFrame(card, fg_color="transparent")
        content_frame.pack(fill="both", expand=True, padx=15, pady=(0, 10))
        
        # Niveau
        level_label = ctk.CTkLabel(
            content_frame,
            text=f"Niveau: {classe.get('niveau', 'Non défini')}",
            font=("Segoe UI", 11),
            text_color=TEXT_SECONDARY
        )
        level_label.pack(anchor="w", pady=(0, 3))
        
        # Capacité
        capacite_label = ctk.CTkLabel(
            content_frame,
            text=f"Capacité: {classe.get('capacite', 0)} élèves",
            font=("Segoe UI", 11),
            text_color=TEXT_SECONDARY
        )
        capacite_label.pack(anchor="w", pady=(0, 3))
        
        # Statut
        statut = classe.get('statut', 'active')
        statut_color = SUCCESS_GREEN if statut == 'active' else WARNING_ORANGE if statut == 'inactive' else ERROR_RED
        statut_label = ctk.CTkLabel(
            content_frame,
            text=f"Statut: {statut.upper()}",
            font=("Segoe UI", 11, "bold"),
            text_color=statut_color
        )
        statut_label.pack(anchor="w", pady=(0, 3))
        
        # Professeur principal
        prof_principal = classe.get('professeur_principal', 'Non assigné')
        prof_label = ctk.CTkLabel(
            content_frame,
            text=f"Prof. Principal: {prof_principal}",
            font=("Segoe UI", 11),
            text_color=TEXT_SECONDARY
        )
        prof_label.pack(anchor="w", pady=(0, 3))
        
        # Nombre d'élèves dans la classe
        eleves_count = self.get_eleves_count(classe.get('id'))
        eleves_label = ctk.CTkLabel(
            content_frame,
            text=f"Élèves inscrits: {eleves_count}",
            font=("Segoe UI", 11),
            text_color=TEXT_SECONDARY
        )
        eleves_label.pack(anchor="w", pady=(0, 8))
        
        # Boutons d'action
        buttons_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        buttons_frame.pack(fill="x", pady=(5, 0))
        
        # Bouton Modifier
        edit_icon = load_icon("resources/icons/edit.png", 12)
        edit_btn = ctk.CTkButton(
            buttons_frame,
            text="Modifier",
            image=edit_icon,
            command=lambda: self.edit_classe(classe.get('id')),
            fg_color="transparent",
            text_color=TEXT_ACCENT,
            hover_color=BG_CARD_HOVER,
            corner_radius=8,
            height=28,
            width=75,
            border_width=1,
            border_color=BORDER_COLOR,
            font=("Segoe UI", 9, "bold")
        )
        edit_btn.pack(side="left", padx=(0, 5))
        
        # Bouton Supprimer
        delete_icon = load_icon("resources/icons/delete.png", 12)
        delete_btn = ctk.CTkButton(
            buttons_frame,
            text="Supprimer",
            image=delete_icon,
            command=lambda: self.delete_classe(classe.get('id')),
            fg_color="transparent",
            text_color=ERROR_RED,
            hover_color=BG_CARD_HOVER,
            corner_radius=8,
            height=28,
            width=75,
            border_width=1,
            border_color=ERROR_RED,
            font=("Segoe UI", 9, "bold")
        )
        delete_btn.pack(side="left")
        
        return card
        
    def get_eleves_count(self, classe_id):
        """Retourne le nombre d'élèves dans une classe"""
        try:
            if not classe_id:
                return 0
            
            # Utiliser une requête directe plus efficace
            from database.connection import get_db_connection
            
            conn = get_db_connection()
            if not conn:
                return 0
                
            cursor = conn.cursor()
            cursor.execute("""
                SELECT COUNT(*) 
                FROM eleves 
                WHERE id_classe = ?
            """, (classe_id,))
            
            count = cursor.fetchone()[0]
            conn.close()
            
            return count
            
        except Exception as e:
            print(f"⚠️ Erreur comptage élèves: {e}")
            return 0
            
    def add_classe(self):
        """Ouvre la fenêtre d'ajout de classe"""
        dialog = ClasseDialog(self, title="Ajouter une Classe")
        if dialog.result:
            self.load_classes()
            
    def edit_classe(self, classe_id):
        """Ouvre la fenêtre d'édition de classe"""
        if classe_id:
            dialog = ClasseDialog(self, title="Modifier la Classe", classe_id=classe_id)
            if dialog.result:
                self.load_classes()
                    
    def delete_classe(self, classe_id):
        """Supprime la classe sélectionnée"""
        if classe_id and messagebox.askyesno("Confirmation", "Voulez-vous vraiment supprimer cette classe ?"):
            try:
                delete_classe(classe_id)
                self.load_classes()
                messagebox.showinfo("Succès", "Classe supprimée avec succès")
            except Exception as e:
                messagebox.showerror("Erreur", f"Erreur lors de la suppression: {str(e)}")

class ClasseDialog(ctk.CTkToplevel):
    """Dialogue pour ajouter/modifier une classe"""
    
    def __init__(self, parent, title="Classe", classe_id=None):
        super().__init__(parent)
        
        self.classe_id = classe_id
        self.result = None
        
        self.setup_dialog(title)
        self.load_professeurs()
        self.load_data()
        
    def setup_dialog(self, title):
        """Configure le dialogue"""
        self.title(title)
        self.geometry("600x650")
        self.configure(fg_color=DARK_BLUE)
        
        # Container principal avec style carte
        main_container = ctk.CTkFrame(self, fg_color=BG_CARD, corner_radius=20, border_width=2, border_color=BORDER_COLOR)
        main_container.pack(fill="both", expand=True, padx=15, pady=15)
        
        # En-tête
        header_frame = ctk.CTkFrame(main_container, fg_color="transparent")
        header_frame.pack(fill="x", padx=25, pady=(25, 20))
        
        title_label = ctk.CTkLabel(
            header_frame,
            text=title,
            font=("Segoe UI", 20, "bold"),
            text_color=TEXT_PRIMARY
        )
        title_label.pack()
        
        # Formulaire
        form_frame = ctk.CTkFrame(main_container, fg_color="transparent")
        form_frame.pack(fill="x", padx=25, pady=(0, 20))
        
        # Nom de la classe
        nom_label = ctk.CTkLabel(
            form_frame, 
            text="Nom de la Classe", 
            font=("Segoe UI", 14, "bold"), 
            text_color=TEXT_PRIMARY
        )
        nom_label.pack(anchor="w", pady=(0, 5))
        
        self.nom_entry = ctk.CTkEntry(
            form_frame, 
            placeholder_text="Ex: 6ème A, 11° SM, TSE",
            font=("Segoe UI", 12),
            fg_color=BG_CARD,
            text_color=TEXT_PRIMARY,
            border_color=BORDER_COLOR,
            corner_radius=10,
            height=40
        )
        self.nom_entry.pack(fill="x", pady=(0, 15))
        
        # Niveau
        niveau_label = ctk.CTkLabel(
            form_frame, 
            text="Niveau", 
            font=("Segoe UI", 14, "bold"), 
            text_color=TEXT_PRIMARY
        )
        niveau_label.pack(anchor="w", pady=(0, 5))
        
        self.niveau_combo = ctk.CTkComboBox(
            form_frame,
            values=["Primaire", "Collège", "Lycée", "Terminale"],
            font=("Segoe UI", 12),
            fg_color=BG_CARD,
            text_color=TEXT_PRIMARY,
            border_color=BORDER_COLOR,
            button_color=TEXT_ACCENT,
            button_hover_color=HOVER_SUCCESS,
            dropdown_hover_color=BG_CARD_HOVER,
            corner_radius=10,
            height=40,
            state="readonly"
        )
        self.niveau_combo.pack(fill="x", pady=(0, 15))
        
        # Capacité (Effectif)
        capacite_label = ctk.CTkLabel(
            form_frame, 
            text="Capacité (Effectif)", 
            font=("Segoe UI", 14, "bold"), 
            text_color=TEXT_PRIMARY
        )
        capacite_label.pack(anchor="w", pady=(0, 5))
        
        self.capacite_entry = ctk.CTkEntry(
            form_frame, 
            placeholder_text="Nombre maximum d'élèves (ex: 50)",
            font=("Segoe UI", 12),
            fg_color=BG_CARD,
            text_color=TEXT_PRIMARY,
            border_color=BORDER_COLOR,
            corner_radius=10,
            height=40
        )
        self.capacite_entry.pack(fill="x", pady=(0, 15))
        
        # Statut
        statut_label = ctk.CTkLabel(
            form_frame, 
            text="Statut", 
            font=("Segoe UI", 14, "bold"), 
            text_color=TEXT_PRIMARY
        )
        statut_label.pack(anchor="w", pady=(0, 5))
        
        self.statut_combo = ctk.CTkComboBox(
            form_frame,
            values=["active", "inactive", "archived"],
            font=("Segoe UI", 12),
            fg_color=BG_CARD,
            text_color=TEXT_PRIMARY,
            border_color=BORDER_COLOR,
            button_color=TEXT_ACCENT,
            button_hover_color=HOVER_SUCCESS,
            dropdown_hover_color=BG_CARD_HOVER,
            corner_radius=10,
            height=40,
            state="readonly"
        )
        self.statut_combo.set("active")  # Valeur par défaut
        self.statut_combo.pack(fill="x", pady=(0, 15))
        
        # Professeur Principal
        prof_label = ctk.CTkLabel(
            form_frame, 
            text="Professeur Principal", 
            font=("Segoe UI", 14, "bold"), 
            text_color=TEXT_PRIMARY
        )
        prof_label.pack(anchor="w", pady=(0, 5))
        
        self.prof_combo = ctk.CTkComboBox(
            form_frame,
            values=["Aucun professeur assigné"],
            font=("Segoe UI", 12),
            fg_color=BG_CARD,
            text_color=TEXT_PRIMARY,
            border_color=BORDER_COLOR,
            button_color=TEXT_ACCENT,
            button_hover_color=HOVER_SUCCESS,
            dropdown_hover_color=BG_CARD_HOVER,
            corner_radius=10,
            height=40,
            state="readonly"
        )
        self.prof_combo.set("Aucun professeur assigné")
        self.prof_combo.pack(fill="x", pady=(0, 25))
        
        # Boutons
        buttons_frame = ctk.CTkFrame(main_container, fg_color="transparent")
        buttons_frame.pack(fill="x", padx=25, pady=(0, 25))
        
        # Bouton Annuler
        cancel_btn = ctk.CTkButton(
            buttons_frame,
            text="Annuler",
            command=self.cancel,
            fg_color="transparent",
            text_color=TEXT_PRIMARY,
            hover_color=BG_CARD_HOVER,
            corner_radius=12,
            height=45,
            width=120,
            border_width=2,
            border_color=BORDER_COLOR,
            font=("Segoe UI", 12, "bold")
        )
        cancel_btn.pack(side="right", padx=(10, 0))
        
        # Bouton Sauvegarder
        save_btn = ctk.CTkButton(
            buttons_frame,
            text="Sauvegarder",
            command=self.save,
            fg_color=TEXT_ACCENT,
            hover_color=HOVER_SUCCESS,
            corner_radius=12,
            height=45,
            width=140,
            font=("Segoe UI", 12, "bold")
        )
        save_btn.pack(side="right")
        
        # Centrer la fenêtre
        self.transient(self.master)
        self.grab_set()
        self.center_window()
        
    def load_professeurs(self):
        """Charge la liste des professeurs dans la ComboBox"""
        try:
            professeurs = get_all_professeurs()
            prof_values = ["Aucun professeur assigné"]
            
            if professeurs:
                for prof in professeurs:
                    nom_complet = f"{prof.get('nom', '')} {prof.get('prenom', '')}".strip()
                    if nom_complet:
                        prof_values.append(nom_complet)
            
            self.prof_combo.configure(values=prof_values)
            
        except Exception as e:
            print(f"⚠️ Erreur chargement professeurs: {e}")
        
    def center_window(self):
        """Centre la fenêtre sur l'écran"""
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f"{width}x{height}+{x}+{y}")
        
    def load_data(self):
        """Charge les données de la classe si en mode édition"""
        if self.classe_id:
            try:
                classe = get_classe_by_id(self.classe_id)
                if classe:
                    self.nom_entry.insert(0, classe.get('nom', ''))
                    self.niveau_combo.set(classe.get('niveau', 'Primaire'))
                    self.capacite_entry.insert(0, str(classe.get('capacite', 0)))
                    self.statut_combo.set(classe.get('statut', 'active'))
                    prof_principal = classe.get('professeur_principal', '')
                    if prof_principal and prof_principal != 'Non assigné':
                        self.prof_combo.set(prof_principal)
                    else:
                        self.prof_combo.set("Aucun professeur assigné")
            except Exception as e:
                messagebox.showerror("Erreur", f"Erreur lors du chargement: {str(e)}")
                
    def save(self):
        """Sauvegarde la classe"""
        try:
            nom = self.nom_entry.get().strip()
            niveau = self.niveau_combo.get().strip()
            capacite = self.capacite_entry.get().strip()
            statut = self.statut_combo.get().strip()
            professeur_principal = self.prof_combo.get()
            if professeur_principal == "Aucun professeur assigné":
                professeur_principal = ""
            
            if not nom:
                messagebox.showerror("Erreur", "Le nom de la classe est obligatoire")
                return
                
            if not niveau:
                messagebox.showerror("Erreur", "Le niveau est obligatoire")
                return
                
            if not capacite.isdigit():
                messagebox.showerror("Erreur", "La capacité doit être un nombre")
                return
                
            if int(capacite) <= 0:
                messagebox.showerror("Erreur", "La capacité doit être supérieure à 0")
                return
                
            classe_data = {
                'nom': nom,
                'niveau': niveau,
                'capacite': int(capacite),
                'statut': statut,
                'professeur_principal': professeur_principal
            }
            
            if self.classe_id:
                update_classe(self.classe_id, classe_data)
                messagebox.showinfo("Succès", "Classe modifiée avec succès")
            else:
                add_classe(classe_data)
                messagebox.showinfo("Succès", "Classe ajoutée avec succès")
                
            self.result = True
            self.destroy()
            
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de la sauvegarde: {str(e)}")
            
    def cancel(self):
        """Annule et ferme le dialogue"""
        self.result = False
        self.destroy()
