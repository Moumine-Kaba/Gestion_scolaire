# -*- coding: utf-8 -*-
"""
Vue des Matières - Système Réorganisé
EduManager+ - Interface Moderne avec Formulaire Structuré

Cette vue présente les matières organisées par niveau et classe
avec un formulaire modal stylisé et des menus déroulants dépendants.
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

from src.modules.academic.subjects.controllers.matieres_controller import get_all_matieres, get_all_niveaux, get_classes_by_niveau
from src.modules.academic.classes.controllers.classe_controller import get_all_classes
from src.modules.academic.professors.controllers.professeur_controller import get_all_professeurs

# Import du thème global
try:
    from resources.themes.theme import *
    print("✅ Thème global EduManager+ importé pour les matières")
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
    FONT_SIZE_SUB = 14
    FONT_SIZE_TXT = 12
    FONT_SIZE_SMALL = 10
    FONT_BOLD = "Segoe UI Bold"

# Variables de police
F_TITLE = (FONT, FONT_SIZE_TITLE, "bold")
F_SUB = (FONT, FONT_SIZE_SUB, "bold")
F_TXT = (FONT, FONT_SIZE_TXT)
F_SMALL = (FONT, FONT_SIZE_SMALL)
F_BOLD = (FONT, FONT_SIZE_TXT, "bold")

# Icônes
ICON_MAP = {
    'add': 'resources/icons/add.png',
    'edit': 'resources/icons/edit.png',
    'delete': 'resources/icons/delete.png',
    'refresh': 'resources/icons/refresh.png',
    'search': 'resources/icons/search.png',
    'filter': 'resources/icons/filter.png',
    'book': 'resources/icons/book.png',
    'school': 'resources/icons/school.png',
    'person': 'resources/icons/person.png',
    'settings': 'resources/icons/settings.png'
}

def load_icon(icon_name, size=(20, 20)):
    """Charge une icône avec gestion d'erreur"""
    try:
        icon_path = ICON_MAP.get(icon_name)
        if icon_path and os.path.exists(icon_path):
            return ctk.CTkImage(Image.open(icon_path), size=size)
        else:
            print(f"⚠️ Icône '{icon_name}' non trouvée: {icon_path}")
            return None
    except Exception as e:
        print(f"❌ Erreur chargement icône '{icon_name}': {e}")
        return None

class MatieresView(ctk.CTkFrame):
    """Vue des Matières avec formulaire structuré"""
    
    def __init__(self, parent):
        super().__init__(parent, fg_color=BG_MAIN)
        
        # Variables de données
        self.matieres = {}
        self.niveaux = {}
        self.classes = {}
        self.professeurs = {}
        self.classe_matieres = {}
        
        # Variables de sélection
        self.selected_niveau = None
        self.selected_classe = None
        self.selected_matiere = None
        
        # Variables de pagination
        self.current_page = 1
        self.items_per_page = 20
        self.total_pages = 1
        
        # Cache des données
        self._data_cache = {}
        self._cache_timestamp = None
        self._cache_duration = 300  # 5 minutes
        
        # Interface
        self.table_frame = None
        self.form_modal = None
        
        # Charger les données
        self._load_data()
        
        # Construire l'interface
        self._build_main_ui()
        
        # Afficher le message initial
        self._show_no_selection_message()
    
    def _load_data(self):
        """Charge les données depuis la base"""
        try:
            print("🔄 Chargement des données matières...")
            
            # Charger les niveaux
            self.niveaux = get_all_niveaux()
            print(f"✅ {len(self.niveaux)} niveaux chargés")
            
            # Charger les classes
            self.classes = get_all_classes()
            print(f"✅ {len(self.classes)} classes chargées")
            
            # Charger les professeurs
            self.professeurs = get_all_professeurs()
            print(f"✅ {len(self.professeurs)} professeurs chargés")
            
            # Charger les matières
            self.matieres = get_all_matieres()
            print(f"✅ {len(self.matieres)} matières chargées")
            
            # Charger les associations classe-matière
            self._load_classe_matieres()
            
            print("✅ Données matières chargées avec succès")
            
        except Exception as e:
            print(f"❌ Erreur chargement données: {e}")
            messagebox.showerror("Erreur", f"Erreur lors du chargement des données:\n{str(e)}")
    
    def _load_classe_matieres(self):
        """Charge les associations classe-matière"""
        try:
            from database.connection import get_db_connection
            conn = get_db_connection()
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT cm.id_classe_matiere, cm.id_classe, cm.id_matiere, cm.id_professeur,
                       cm.coefficient_classe, cm.statut,
                       c.nom_classe, m.nom_matiere, p.nom + ' ' + p.prenom as professeur_nom
                FROM classe_matieres cm
                LEFT JOIN classes c ON cm.id_classe = c.id_classe
                LEFT JOIN matieres m ON cm.id_matiere = m.id_matiere
                LEFT JOIN professeurs p ON cm.id_professeur = p.id_professeur
                WHERE cm.statut = 'active'
                ORDER BY c.nom_classe, m.nom_matiere
            """)
            
            rows = cursor.fetchall()
            conn.close()
            
            self.classe_matieres = {}
            for row in rows:
                self.classe_matieres[row[0]] = {
                    'id_classe_matiere': row[0],
                    'id_classe': row[1],
                    'id_matiere': row[2],
                    'id_professeur': row[3],
                    'coefficient_classe': row[4],
                    'statut': row[5],
                    'classe_nom': row[6],
                    'matiere_nom': row[7],
                    'professeur_nom': row[8] if row[8] else 'Non assigné'
                }
            
            print(f"✅ {len(self.classe_matieres)} associations classe-matière chargées")
            
        except Exception as e:
            print(f"❌ Erreur chargement associations: {e}")
    
    def _build_main_ui(self):
        """Construit l'interface principale"""
        # Configuration de la grille
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=3)
        self.grid_rowconfigure(0, weight=1)
        
        # Panneau gauche - Sélection et filtres
        self._build_selection_panel()
        
        # Panneau droit - Tableau des matières
        self._build_matieres_dashboard()
    
    def _build_selection_panel(self):
        """Construit le panneau de sélection gauche"""
        # Frame principal du panneau gauche
        left_panel = ctk.CTkFrame(self, fg_color=BG_CARD, corner_radius=12)
        left_panel.grid(row=0, column=0, sticky="nsew", padx=(MARGIN_MEDIUM, MARGIN_SMALL), pady=MARGIN_MEDIUM)
        left_panel.grid_columnconfigure(0, weight=1)
        left_panel.grid_rowconfigure(4, weight=1)
        
        # Titre
        title_frame = ctk.CTkFrame(left_panel, fg_color="transparent")
        title_frame.grid(row=0, column=0, sticky="ew", padx=MARGIN_MEDIUM, pady=(MARGIN_MEDIUM, MARGIN_SMALL))
        title_frame.grid_columnconfigure(1, weight=1)
        
        book_icon = load_icon('book', (24, 24))
        title_label = ctk.CTkLabel(title_frame, text="MATIÈRES", font=F_TITLE, text_color=TEXT_ACCENT)
        title_label.grid(row=0, column=0, padx=(0, MARGIN_SMALL))
        
        refresh_icon = load_icon('refresh', (20, 20))
        refresh_btn = ctk.CTkButton(title_frame, image=refresh_icon, text="", width=30, height=30,
                                   command=self._refresh_all, fg_color="transparent", hover_color=BORDER_COLOR)
        refresh_btn.grid(row=0, column=1, sticky="e")
        
        # Filtres
        filters_frame = ctk.CTkFrame(left_panel, fg_color="transparent")
        filters_frame.grid(row=1, column=0, sticky="ew", padx=MARGIN_MEDIUM, pady=MARGIN_SMALL)
        filters_frame.grid_columnconfigure(0, weight=1)
        
        # Filtre niveau
        niveau_frame = ctk.CTkFrame(filters_frame, fg_color="transparent")
        niveau_frame.grid(row=0, column=0, sticky="ew", pady=(0, MARGIN_SMALL))
        niveau_frame.grid_columnconfigure(1, weight=1)
        
        ctk.CTkLabel(niveau_frame, text="Niveau:", font=F_TXT, text_color=TEXT_PRIMARY).grid(row=0, column=0, sticky="w")
        self.niveau_var = StringVar()
        self.niveau_dropdown = ctk.CTkComboBox(niveau_frame, variable=self.niveau_var, 
                                              values=["Tous les niveaux"] + list(self.niveaux.keys()),
                                              command=self._on_niveau_selected, state="readonly")
        self.niveau_dropdown.grid(row=0, column=1, sticky="ew", padx=(MARGIN_SMALL, 0))
        self.niveau_dropdown.set("Tous les niveaux")
        
        # Filtre classe
        classe_frame = ctk.CTkFrame(filters_frame, fg_color="transparent")
        classe_frame.grid(row=1, column=0, sticky="ew", pady=(0, MARGIN_SMALL))
        classe_frame.grid_columnconfigure(1, weight=1)
        
        ctk.CTkLabel(classe_frame, text="Classe:", font=F_TXT, text_color=TEXT_PRIMARY).grid(row=0, column=0, sticky="w")
        self.classe_var = StringVar()
        self.classe_dropdown = ctk.CTkComboBox(classe_frame, variable=self.classe_var,
                                              values=["Toutes les classes"], command=self._on_classe_selected, state="readonly")
        self.classe_dropdown.grid(row=0, column=1, sticky="ew", padx=(MARGIN_SMALL, 0))
        self.classe_dropdown.set("Toutes les classes")
        
        # Actions
        actions_frame = ctk.CTkFrame(left_panel, fg_color="transparent")
        actions_frame.grid(row=2, column=0, sticky="ew", padx=MARGIN_MEDIUM, pady=MARGIN_SMALL)
        actions_frame.grid_columnconfigure(0, weight=1)
        
        add_icon = load_icon('add', (20, 20))
        add_btn = ctk.CTkButton(actions_frame, image=add_icon, text="Ajouter Matière",
                               command=self._add_matiere, fg_color=SUCCESS_GREEN, hover_color="#80C7C5")
        add_btn.grid(row=0, column=0, sticky="ew", pady=(0, MARGIN_SMALL))
        
        # Statistiques
        stats_frame = ctk.CTkFrame(left_panel, fg_color="transparent")
        stats_frame.grid(row=3, column=0, sticky="ew", padx=MARGIN_MEDIUM, pady=MARGIN_SMALL)
        stats_frame.grid_columnconfigure(0, weight=1)
        
        self.stats_label = ctk.CTkLabel(stats_frame, text="Sélectionnez un niveau et une classe", 
                                       font=F_SMALL, text_color=TEXT_SECONDARY)
        self.stats_label.grid(row=0, column=0, sticky="ew")
    
    def _build_matieres_dashboard(self):
        """Construit le tableau des matières"""
        # Frame principal du panneau droit
        right_panel = ctk.CTkFrame(self, fg_color=BG_CARD, corner_radius=12)
        right_panel.grid(row=0, column=1, sticky="nsew", padx=(MARGIN_SMALL, MARGIN_MEDIUM), pady=MARGIN_MEDIUM)
        right_panel.grid_columnconfigure(0, weight=1)
        right_panel.grid_rowconfigure(1, weight=1)
        
        # Titre du tableau
        table_title = ctk.CTkLabel(right_panel, text="Matières par Classe", font=F_SUB, text_color=TEXT_PRIMARY)
        table_title.grid(row=0, column=0, sticky="ew", padx=MARGIN_MEDIUM, pady=(MARGIN_MEDIUM, MARGIN_SMALL))
        
        # Frame du tableau
        self.table_frame = ctk.CTkFrame(right_panel, fg_color=BG_CARD, corner_radius=12)
        self.table_frame.grid(row=1, column=0, sticky="nsew", padx=0, pady=0)
        self.table_frame.grid_columnconfigure(0, weight=1)
        self.table_frame.grid_rowconfigure(0, weight=1)
    
    def _on_niveau_selected(self, selected_niveau):
        """Gère la sélection d'un niveau"""
        if selected_niveau == "Tous les niveaux":
            self.selected_niveau = None
            # Réinitialiser la classe
            self.classe_dropdown.configure(values=["Toutes les classes"])
            self.classe_dropdown.set("Toutes les classes")
            self.selected_classe = None
        else:
            self.selected_niveau = selected_niveau
            # Mettre à jour les classes disponibles
            classes_niveau = get_classes_by_niveau(selected_niveau)
            classe_values = ["Toutes les classes"] + list(classes_niveau.keys())
            self.classe_dropdown.configure(values=classe_values)
            self.classe_dropdown.set("Toutes les classes")
            self.selected_classe = None
        
        print(f"🔄 Niveau sélectionné: {selected_niveau}")
        self._filter_matieres()
    
    def _on_classe_selected(self, selected_classe):
        """Gère la sélection d'une classe"""
        if selected_classe == "Toutes les classes":
            self.selected_classe = None
        else:
            self.selected_classe = selected_classe
        
        print(f"🔄 Classe sélectionnée: {selected_classe}")
        self._filter_matieres()
    
    def _filter_matieres(self):
        """Filtre les matières selon les sélections"""
        if not self.selected_niveau and not self.selected_classe:
            self._show_no_selection_message()
            return
        
        # Filtrer les associations
        filtered = []
        for assoc in self.classe_matieres.values():
            if self.selected_niveau:
                # Vérifier si la classe appartient au niveau sélectionné
                classe_data = self.classes.get(assoc['id_classe'], {})
                if classe_data.get('niveau') != self.selected_niveau:
                    continue
            
            if self.selected_classe:
                # Vérifier si c'est la classe sélectionnée
                if classe_data.get('nom_classe') != self.selected_classe:
                    continue
            
            filtered.append(assoc)
        
        # Trier par classe puis par matière
        filtered.sort(key=lambda x: (x['classe_nom'], x['matiere_nom']))
        
        # Mettre à jour la pagination
        self.current_page = 1
        self.total_pages = max(1, (len(filtered) + self.items_per_page - 1) // self.items_per_page)
        
        # Mettre à jour l'affichage
        self._update_matieres_table(filtered)
        self._update_stats(len(filtered))
    
    def _update_matieres_table(self, matieres):
        """Met à jour le tableau des matières"""
        if not self.table_frame:
            return
        
        # Nettoyer le frame
        for widget in self.table_frame.winfo_children():
            widget.destroy()
        
        if not matieres:
            self._show_no_selection_message()
            return
        
        # Pagination
        start_idx = (self.current_page - 1) * self.items_per_page
        end_idx = start_idx + self.items_per_page
        matieres_page = matieres[start_idx:end_idx]
        
        # En-têtes du tableau
        headers = ["Classe", "Matière", "Coefficient", "Professeur", "Statut"]
        data = [headers]
        
        # Données du tableau
        for matiere in matieres_page:
            data.append([
                matiere['classe_nom'],
                matiere['matiere_nom'],
                str(matiere['coefficient_classe']),
                matiere['professeur_nom'],
                matiere['statut']
            ])
        
        # Créer le tableau
        table = CTkTable(self.table_frame, row=len(data), column=len(headers), values=data,
                        header_color=ACCENT, header_text_color=BG_MAIN,
                        fg_color=BG_CARD, text_color=TEXT_PRIMARY,
                        font=F_TXT, corner_radius=8)
        table.grid(row=0, column=0, sticky="nsew", padx=MARGIN_MEDIUM, pady=MARGIN_MEDIUM)
        
        # Ajouter la pagination
        self._add_pagination_controls()
    
    def _add_pagination_controls(self):
        """Ajoute les contrôles de pagination"""
        if self.total_pages <= 1:
            return
        
        pagination_frame = ctk.CTkFrame(self.table_frame, fg_color="transparent")
        pagination_frame.grid(row=1, column=0, sticky="ew", padx=MARGIN_MEDIUM, pady=(0, MARGIN_MEDIUM))
        pagination_frame.grid_columnconfigure(1, weight=1)
        
        # Bouton précédent
        prev_btn = ctk.CTkButton(pagination_frame, text="◀ Précédent", command=self._go_to_previous_page,
                                fg_color=BORDER_COLOR, hover_color=ACCENT, width=100)
        prev_btn.grid(row=0, column=0, padx=(0, MARGIN_SMALL))
        
        # Informations de page
        page_info = ctk.CTkLabel(pagination_frame, text=f"Page {self.current_page}/{self.total_pages}",
                                font=F_SMALL, text_color=TEXT_SECONDARY)
        page_info.grid(row=0, column=1)
        
        # Bouton suivant
        next_btn = ctk.CTkButton(pagination_frame, text="Suivant ▶", command=self._go_to_next_page,
                                fg_color=BORDER_COLOR, hover_color=ACCENT, width=100)
        next_btn.grid(row=0, column=2, padx=(MARGIN_SMALL, 0))
    
    def _go_to_previous_page(self):
        """Va à la page précédente"""
        if self.current_page > 1:
            self.current_page -= 1
            self._filter_matieres()
    
    def _go_to_next_page(self):
        """Va à la page suivante"""
        if self.current_page < self.total_pages:
            self.current_page += 1
            self._filter_matieres()
    
    def _update_stats(self, count):
        """Met à jour les statistiques"""
        if self.selected_niveau and self.selected_classe:
            self.stats_label.configure(text=f"{count} matières pour {self.selected_classe} ({self.selected_niveau})")
        elif self.selected_niveau:
            self.stats_label.configure(text=f"{count} matières pour le niveau {self.selected_niveau}")
        else:
            self.stats_label.configure(text=f"{count} matières au total")
    
    def _show_no_selection_message(self):
        """Affiche un message quand aucune sélection"""
        if not self.table_frame:
            return
        
        # Nettoyer le frame
        for widget in self.table_frame.winfo_children():
            widget.destroy()
        
        # Message central
        message_frame = ctk.CTkFrame(self.table_frame, fg_color="transparent")
        message_frame.grid(row=0, column=0, sticky="nsew")
        message_frame.grid_columnconfigure(0, weight=1)
        message_frame.grid_rowconfigure(0, weight=1)
        
        # Icône et texte
        book_icon = load_icon('book', (64, 64))
        icon_label = ctk.CTkLabel(message_frame, image=book_icon, text="")
        icon_label.grid(row=0, column=0, pady=(0, MARGIN_MEDIUM))
        
        title_label = ctk.CTkLabel(message_frame, text="Sélectionnez un niveau et une classe", 
                                  font=F_SUB, text_color=TEXT_PRIMARY)
        title_label.grid(row=1, column=0, pady=(0, MARGIN_SMALL))
        
        desc_label = ctk.CTkLabel(message_frame, text="Choisissez un niveau pour voir les classes disponibles,\npuis sélectionnez une classe pour afficher ses matières.",
                                 font=F_SMALL, text_color=TEXT_SECONDARY)
        desc_label.grid(row=2, column=0)
    
    def _add_matiere(self):
        """Ouvre le formulaire d'ajout de matière"""
        if not self.selected_niveau:
            messagebox.showwarning("Sélection requise", "Veuillez d'abord sélectionner un niveau.")
            return
        
        self._open_matiere_form()
    
    def _open_matiere_form(self):
        """Ouvre le formulaire modal de matière"""
        if self.form_modal:
            self.form_modal.destroy()
        
        self.form_modal = Toplevel(self)
        self.form_modal.title("Ajouter une Matière")
        self.form_modal.geometry("500x600")
        self.form_modal.configure(bg=BG_MAIN)
        self.form_modal.resizable(False, False)
        
        # Centrer la fenêtre
        self.form_modal.transient(self)
        self.form_modal.grab_set()
        
        # Frame principal
        main_frame = ctk.CTkFrame(self.form_modal, fg_color=BG_CARD, corner_radius=12)
        main_frame.pack(fill="both", expand=True, padx=MARGIN_MEDIUM, pady=MARGIN_MEDIUM)
        main_frame.grid_columnconfigure(0, weight=1)
        
        # Titre
        title_label = ctk.CTkLabel(main_frame, text="Nouvelle Matière", font=F_TITLE, text_color=TEXT_ACCENT)
        title_label.grid(row=0, column=0, pady=(MARGIN_MEDIUM, MARGIN_LARGE))
        
        # Formulaire
        form_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        form_frame.grid(row=1, column=0, sticky="ew", padx=MARGIN_MEDIUM)
        form_frame.grid_columnconfigure(1, weight=1)
        
        # Nom de la matière
        ctk.CTkLabel(form_frame, text="Nom de la matière:", font=F_TXT, text_color=TEXT_PRIMARY).grid(row=0, column=0, sticky="w", pady=(0, MARGIN_SMALL))
        self.nom_var = StringVar()
        nom_entry = ctk.CTkEntry(form_frame, textvariable=self.nom_var, font=F_TXT, placeholder_text="Ex: Mathématiques")
        nom_entry.grid(row=0, column=1, sticky="ew", pady=(0, MARGIN_SMALL))
        
        # Niveau (déjà sélectionné)
        ctk.CTkLabel(form_frame, text="Niveau:", font=F_TXT, text_color=TEXT_PRIMARY).grid(row=1, column=0, sticky="w", pady=(0, MARGIN_SMALL))
        niveau_label = ctk.CTkLabel(form_frame, text=self.selected_niveau, font=F_TXT, text_color=TEXT_ACCENT)
        niveau_label.grid(row=1, column=1, sticky="w", pady=(0, MARGIN_SMALL))
        
        # Classes disponibles
        ctk.CTkLabel(form_frame, text="Classes:", font=F_TXT, text_color=TEXT_PRIMARY).grid(row=2, column=0, sticky="nw", pady=(0, MARGIN_SMALL))
        
        classes_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        classes_frame.grid(row=2, column=1, sticky="ew", pady=(0, MARGIN_SMALL))
        classes_frame.grid_columnconfigure(0, weight=1)
        
        # Liste des classes avec cases à cocher
        self.classes_selected = {}
        classes_niveau = get_classes_by_niveau(self.selected_niveau)
        
        for i, (classe_id, classe_data) in enumerate(classes_niveau.items()):
            var = ctk.BooleanVar()
            checkbox = ctk.CTkCheckBox(classes_frame, text=classe_data['nom_classe'], variable=var, font=F_SMALL)
            checkbox.grid(row=i, column=0, sticky="w", pady=2)
            self.classes_selected[classe_id] = var
        
        # Coefficient
        ctk.CTkLabel(form_frame, text="Coefficient:", font=F_TXT, text_color=TEXT_PRIMARY).grid(row=3, column=0, sticky="w", pady=(MARGIN_MEDIUM, MARGIN_SMALL))
        self.coefficient_var = StringVar(value="1.0")
        coefficient_entry = ctk.CTkEntry(form_frame, textvariable=self.coefficient_var, font=F_TXT, placeholder_text="1.0")
        coefficient_entry.grid(row=3, column=1, sticky="ew", pady=(MARGIN_MEDIUM, MARGIN_SMALL))
        
        # Professeur (optionnel)
        ctk.CTkLabel(form_frame, text="Professeur:", font=F_TXT, text_color=TEXT_PRIMARY).grid(row=4, column=0, sticky="w", pady=(0, MARGIN_SMALL))
        self.professeur_var = StringVar()
        professeur_dropdown = ctk.CTkComboBox(form_frame, variable=self.professeur_var,
                                             values=["Aucun"] + [f"{p['nom']} {p['prenom']}" for p in self.professeurs.values()],
                                             state="readonly")
        professeur_dropdown.grid(row=4, column=1, sticky="ew", pady=(0, MARGIN_SMALL))
        professeur_dropdown.set("Aucun")
        
        # Boutons
        buttons_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        buttons_frame.grid(row=2, column=0, sticky="ew", padx=MARGIN_MEDIUM, pady=MARGIN_LARGE)
        buttons_frame.grid_columnconfigure(0, weight=1)
        buttons_frame.grid_columnconfigure(1, weight=1)
        
        cancel_btn = ctk.CTkButton(buttons_frame, text="Annuler", command=self.form_modal.destroy,
                                  fg_color=BORDER_COLOR, hover_color=ERROR_RED)
        cancel_btn.grid(row=0, column=0, padx=(0, MARGIN_SMALL), sticky="ew")
        
        save_btn = ctk.CTkButton(buttons_frame, text="Enregistrer", command=self._save_matiere,
                                fg_color=SUCCESS_GREEN, hover_color="#80C7C5")
        save_btn.grid(row=0, column=1, padx=(MARGIN_SMALL, 0), sticky="ew")
    
    def _save_matiere(self):
        """Sauvegarde la nouvelle matière"""
        try:
            # Validation
            nom = self.nom_var.get().strip()
            if not nom:
                messagebox.showerror("Erreur", "Le nom de la matière est obligatoire.")
                return
            
            coefficient = float(self.coefficient_var.get() or "1.0")
            if coefficient <= 0:
                messagebox.showerror("Erreur", "Le coefficient doit être positif.")
                return
            
            # Vérifier qu'au moins une classe est sélectionnée
            classes_selected = [classe_id for classe_id, var in self.classes_selected.items() if var.get()]
            if not classes_selected:
                messagebox.showerror("Erreur", "Veuillez sélectionner au moins une classe.")
                return
            
            # Récupérer l'ID du professeur
            professeur_nom = self.professeur_var.get()
            professeur_id = None
            if professeur_nom != "Aucun":
                for prof_id, prof_data in self.professeurs.items():
                    if f"{prof_data['nom']} {prof_data['prenom']}" == professeur_nom:
                        professeur_id = prof_id
                        break
            
            # Sauvegarder en base
            from database.connection import get_db_connection
            conn = get_db_connection()
            cursor = conn.cursor()
            
            # Créer la matière
            cursor.execute("""
                INSERT INTO matieres (nom_matiere, coefficient, description)
                VALUES (?, ?, ?)
            """, (nom, coefficient, f"Matière {nom} - Niveau {self.selected_niveau}"))
            
            # Récupérer l'ID de la matière créée
            cursor.execute("SELECT @@IDENTITY")
            matiere_id = cursor.fetchone()[0]
            
            # Créer les associations classe-matière
            for classe_id in classes_selected:
                cursor.execute("""
                    INSERT INTO classe_matieres (id_classe, id_matiere, id_professeur, coefficient_classe)
                    VALUES (?, ?, ?, ?)
                """, (classe_id, matiere_id, professeur_id, coefficient))
            
            conn.commit()
            conn.close()
            
            # Fermer le formulaire
            self.form_modal.destroy()
            self.form_modal = None
            
            # Recharger les données
            self._load_data()
            self._filter_matieres()
            
            messagebox.showinfo("Succès", f"Matière '{nom}' créée avec succès pour {len(classes_selected)} classe(s).")
            
        except Exception as e:
            print(f"❌ Erreur sauvegarde matière: {e}")
            messagebox.showerror("Erreur", f"Erreur lors de la sauvegarde:\n{str(e)}")
    
    def _refresh_all(self):
        """Rafraîchit toutes les données"""
        print("🔄 Rafraîchissement des données matières...")
        self._load_data()
        self._filter_matieres()
        print("✅ Données matières rafraîchies")
