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
from src.modules.academic.teachers.controllers.professeur_controller import get_all_professeurs

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
            
            # Charger les classes et les convertir en dictionnaire
            classes_list = get_all_classes()
            self.classes = {classe['id']: classe for classe in classes_list}
            print(f"✅ {len(self.classes)} classes chargées")
            
            # Charger les professeurs
            self.professeurs = get_all_professeurs()
            print(f"✅ {len(self.professeurs)} professeurs chargés")
            print(f"🔍 DEBUG: Type de self.professeurs = {type(self.professeurs)}")
            if self.professeurs:
                print(f"🔍 DEBUG: Premier professeur = {list(self.professeurs.values())[0] if isinstance(self.professeurs, dict) else self.professeurs[0]}")
            
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
                    'coefficient_classe': float(row[4]) if row[4] is not None else 1.0,
                    'statut': row[5] if row[5] else 'active',
                    'classe_nom': str(row[6]) if row[6] else 'Sans nom',
                    'matiere_nom': str(row[7]) if row[7] else 'Sans nom',
                    'professeur_nom': str(row[8]) if row[8] else 'Non assigné'
                }
            
            print(f"✅ {len(self.classe_matieres)} associations classe-matière chargées")
            # Debug: afficher les 3 premières associations
            for i, (key, assoc) in enumerate(list(self.classe_matieres.items())[:3]):
                print(f"🔍 DEBUG: Association {i+1} - ID: {key}, Professeur: {assoc['professeur_nom']} (ID: {assoc['id_professeur']})")
            
        except Exception as e:
            print(f"❌ Erreur chargement associations: {e}")
        
    def _build_main_ui(self):
        """Construit l'interface principale"""
        # Configuration de la grille
        self.grid_columnconfigure(0, weight=0, minsize=280)  # Sidebar réduite
        self.grid_columnconfigure(1, weight=1)  # Contenu principal
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
        left_panel.grid_rowconfigure(5, weight=1)  # Ajusté pour les boutons CRUD
        
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
        # Utiliser les noms des niveaux au lieu des IDs
        niveau_values = ["Tous les niveaux"] + [niveau_data['nom_niveau'] for niveau_data in self.niveaux.values()]
        self.niveau_dropdown = ctk.CTkComboBox(niveau_frame, variable=self.niveau_var, 
                                              values=niveau_values,
                                              command=self._on_niveau_selected, state="readonly")
        self.niveau_dropdown.grid(row=0, column=1, sticky="ew", padx=(MARGIN_SMALL, 0))
        self.niveau_dropdown.set("Tous les niveaux")
        print(f"🔍 DEBUG: Dropdown niveau initialisé avec: {niveau_values}")
        print(f"🔍 DEBUG: Valeur par défaut: {self.niveau_dropdown.get()}")
        
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
        print(f"🔍 DEBUG: Dropdown classe initialisé avec: ['Toutes les classes']")
        print(f"🔍 DEBUG: Valeur par défaut: {self.classe_dropdown.get()}")
        
        # Actions CRUD
        actions_frame = ctk.CTkFrame(left_panel, fg_color="transparent")
        actions_frame.grid(row=2, column=0, sticky="ew", padx=MARGIN_MEDIUM, pady=MARGIN_SMALL)
        actions_frame.grid_columnconfigure(0, weight=1)
        actions_frame.grid_columnconfigure(1, weight=1)
        
        # Bouton Ajouter
        add_icon = load_icon('add', (16, 16))
        add_btn = ctk.CTkButton(actions_frame, image=add_icon, text="Ajouter",
                               command=self._add_matiere, fg_color=SUCCESS_GREEN, hover_color="#80C7C5",
                               width=80, height=32, font=F_SMALL)
        add_btn.grid(row=0, column=0, sticky="ew", padx=(0, MARGIN_SMALL), pady=(0, MARGIN_SMALL))
        
        # Bouton Modifier
        edit_icon = load_icon('edit', (16, 16))
        edit_btn = ctk.CTkButton(actions_frame, image=edit_icon, text="Modifier",
                                command=self._edit_matiere, fg_color=ACCENT, hover_color="#4A90E2",
                                width=80, height=32, font=F_SMALL)
        edit_btn.grid(row=0, column=1, sticky="ew", padx=(MARGIN_SMALL, 0), pady=(0, MARGIN_SMALL))
        
        # Bouton Supprimer
        delete_icon = load_icon('delete', (16, 16))
        delete_btn = ctk.CTkButton(actions_frame, image=delete_icon, text="Supprimer",
                                  command=self._delete_matiere, fg_color=ERROR_RED, hover_color="#D32F2F",
                                  width=80, height=32, font=F_SMALL)
        delete_btn.grid(row=1, column=0, sticky="ew", padx=(0, MARGIN_SMALL), pady=(0, MARGIN_SMALL))
        
        # Bouton Actualiser
        refresh_icon = load_icon('refresh', (16, 16))
        refresh_btn = ctk.CTkButton(actions_frame, image=refresh_icon, text="Actualiser",
                                   command=self._refresh_all, fg_color=BORDER_COLOR, hover_color="#666666",
                                   width=80, height=32, font=F_SMALL)
        refresh_btn.grid(row=1, column=1, sticky="ew", padx=(MARGIN_SMALL, 0), pady=(0, MARGIN_SMALL))
        
        # Statistiques
        stats_frame = ctk.CTkFrame(left_panel, fg_color="transparent")
        stats_frame.grid(row=4, column=0, sticky="ew", padx=MARGIN_MEDIUM, pady=MARGIN_SMALL)
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
        print(f"🔍 DEBUG: _on_niveau_selected appelé avec: '{selected_niveau}'")
        
        if selected_niveau == "Tous les niveaux":
            print("🔍 DEBUG: Sélection 'Tous les niveaux' - réinitialisation")
            self.selected_niveau = None
            # Réinitialiser la classe
            self.classe_dropdown.configure(values=["Toutes les classes"])
            self.classe_dropdown.set("Toutes les classes")
            self.selected_classe = None
        else:
            print(f"🔍 DEBUG: Sélection niveau spécifique: '{selected_niveau}'")
            self.selected_niveau = selected_niveau
            
            # Mettre à jour les classes disponibles
            print(f"🔍 DEBUG: Appel get_classes_by_niveau('{selected_niveau}')")
            classes_niveau = get_classes_by_niveau(selected_niveau)
            print(f"🔍 DEBUG: get_classes_by_niveau retourne: {len(classes_niveau)} classes")
            print(f"🔍 DEBUG: Contenu classes_niveau: {classes_niveau}")
            
            # Utiliser les noms des classes au lieu des IDs
            classe_values = ["Toutes les classes"] + [classe_data['nom_classe'] for classe_data in classes_niveau.values()]
            print(f"🔍 DEBUG: classe_values générées: {classe_values}")
            
            self.classe_dropdown.configure(values=classe_values)
            self.classe_dropdown.set("Toutes les classes")
            self.selected_classe = None
            
            print(f"🔍 DEBUG: Dropdown configuré avec {len(classe_values)} valeurs")
            print(f"🔍 DEBUG: Valeurs actuelles du dropdown: {self.classe_dropdown.cget('values')}")
        
        print(f"🔄 Niveau sélectionné: {selected_niveau}")
        self._filter_matieres()
    
    def _on_classe_selected(self, selected_classe):
        """Gère la sélection d'une classe"""
        print(f"🔍 DEBUG: _on_classe_selected appelé avec: '{selected_classe}'")
        
        if selected_classe == "Toutes les classes":
            print("🔍 DEBUG: Sélection 'Toutes les classes' - réinitialisation")
            self.selected_classe = None
        else:
            print(f"🔍 DEBUG: Sélection classe spécifique: '{selected_classe}'")
            self.selected_classe = selected_classe
        
        print(f"🔄 Classe sélectionnée: {selected_classe}")
        self._filter_matieres()
    
    def _filter_matieres(self):
        """Filtre les matières selon les sélections"""
        print(f"🔍 DEBUG: _filter_matieres appelé - niveau: '{self.selected_niveau}', classe: '{self.selected_classe}'")
        
        if not self.selected_niveau and not self.selected_classe:
            print("🔍 DEBUG: Aucune sélection - affichage message")
            self._show_no_selection_message()
            return
        
        # Filtrer les associations
        print(f"🔍 DEBUG: Filtrage de {len(self.classe_matieres)} associations")
        print(f"🔍 DEBUG: Exemple d'association: {list(self.classe_matieres.values())[0] if self.classe_matieres else 'Aucune'}")
        filtered = []
        for assoc in self.classe_matieres.values():
            # Si une classe est sélectionnée, afficher uniquement cette classe
            if self.selected_classe:
                print(f"🔍 DEBUG: Classe {assoc['id_classe']} - nom: {assoc.get('classe_nom')} vs sélectionné: {self.selected_classe}")
                if assoc.get('classe_nom') != self.selected_classe:
                    continue
            # Sinon, filtrer par niveau
            elif self.selected_niveau:
                # Vérifier si la classe appartient au niveau sélectionné
                classe_data = self.classes.get(assoc['id_classe'], {})
                print(f"🔍 DEBUG: Classe {assoc['id_classe']} - niveau: {classe_data.get('niveau')} vs sélectionné: {self.selected_niveau}")
                if classe_data.get('niveau') != self.selected_niveau:
                    continue
            
            filtered.append(assoc)
        
        print(f"🔍 DEBUG: {len(filtered)} associations après filtrage")
        if filtered:
            print(f"🔍 DEBUG: Premier élément filtré - Professeur: {filtered[0].get('professeur_nom')}")
        
        # Trier par classe puis par matière
        filtered.sort(key=lambda x: (x['classe_nom'], x['matiere_nom']))
        
        # Mettre à jour l'affichage (pagination désactivée - tableau fixe à 10 lignes)
        self._update_matieres_table(filtered)
        self._update_stats(len(filtered))
    
    def _update_matieres_table(self, matieres):
        """Met à jour le tableau des matières - MAXIMUM 10 LIGNES"""
        if not self.table_frame:
            return
        
        # Nettoyer le frame
        for widget in self.table_frame.winfo_children():
            widget.destroy()
        
            # En-têtes du tableau
        headers = ["Classe", "Matière", "Coefficient", "Professeur", "Statut"]
        data = [headers]
        
        # Limiter à 10 matières maximum
        max_matieres = 10
        matieres_limitees = matieres[:max_matieres]
        
        # Ajouter les données (maximum 10 lignes)
        for matiere in matieres_limitees:
            # S'assurer que toutes les valeurs sont des strings
            classe_nom = str(matiere.get('classe_nom', 'N/A'))
            matiere_nom = str(matiere.get('matiere_nom', 'N/A'))
            coefficient = str(matiere.get('coefficient_classe', '1.0'))
            professeur = str(matiere.get('professeur_nom', 'Non assigné'))
            statut = str(matiere.get('statut', 'active'))
            
            data.append([classe_nom, matiere_nom, coefficient, professeur, statut])
        
        # Compléter avec des lignes vides si moins de 10 matières
        while len(data) < max_matieres + 1:  # +1 pour l'en-tête
            data.append(["", "", "", "", ""])
        
        # Créer le tableau avec exactement 11 lignes (1 en-tête + 10 données)
        try:
            table = CTkTable(self.table_frame, row=11, column=len(headers), values=data,
                            header_color=ACCENT,
                            fg_color=BG_CARD, text_color=TEXT_PRIMARY,
                            font=F_TXT, corner_radius=8)
        except Exception as e:
            print(f"❌ Erreur création tableau: {e}")
            # Fallback: afficher un message d'erreur
            error_label = ctk.CTkLabel(self.table_frame, text=f"Erreur d'affichage: {str(e)}", 
                                     font=F_TXT, text_color=ERROR_RED)
            error_label.grid(row=0, column=0, pady=MARGIN_MEDIUM)
            return
        table.grid(row=0, column=0, sticky="nsew", padx=MARGIN_MEDIUM, pady=MARGIN_MEDIUM)
        
        # Ajouter la gestion de sélection des lignes
        table.bind("<Button-1>", lambda event: self._on_table_click(event, table, matieres_limitees))
        
        # Stocker la référence du tableau et des données pour la sélection
        self.current_table = table
        self.current_matieres = matieres_limitees
        
        # Message d'information si plus de 10 matières
        if len(matieres) > max_matieres:
            info_label = ctk.CTkLabel(self.table_frame, 
                                     text=f"⚠️ {len(matieres)} matières trouvées. Affichage des 10 premières.",
                                     font=ctk.CTkFont(size=12), text_color=WARNING_YELLOW)
            info_label.grid(row=1, column=0, pady=(0, MARGIN_MEDIUM))
    
    def _on_table_click(self, event, table, matieres):
        """Gère le clic sur une ligne du tableau"""
        try:
            # Utiliser les coordonnées de l'événement pour calculer la ligne
            y = event.y
            row_height = 35  # Hauteur approximative d'une ligne
            row = int(y // row_height)
            
            print(f"🔍 DEBUG: Clic à Y={y}, ligne calculée={row}, total matières={len(matieres)}")
            
            if row <= 0:  # Ignorer l'en-tête (ligne 0)
                print("🔍 DEBUG: Clic sur l'en-tête - ignoré")
            return
        
            # Ajuster l'index pour les données (row-1 car l'en-tête est à l'index 0)
            data_index = row - 1
            
            # Vérifier si l'index est valide
            if 0 <= data_index < len(matieres):
                matiere = matieres[data_index]
                self.selected_matiere = matiere.get('id_classe_matiere')
                print(f"🔍 DEBUG: Matière sélectionnée - ID: {self.selected_matiere}, Nom: {matiere.get('matiere_nom')}")
                
                # Mettre à jour l'apparence de la ligne sélectionnée
                try:
                    # Désélectionner toutes les lignes
                    for i in range(1, 11):  # Lignes 1 à 10 (ignorer l'en-tête)
                        table.deselect(i, 0)
                except:
                    pass
                
                try:
                    # Sélectionner la ligne cliquée
                    table.select_row(row)
                except:
                    pass
            else:
                # Ligne vide, désélectionner
                self.selected_matiere = None
                try:
                    # Désélectionner toutes les lignes
                    for i in range(1, 11):  # Lignes 1 à 10 (ignorer l'en-tête)
                        table.deselect(i, 0)
                except:
                    pass
                print("🔍 DEBUG: Ligne vide cliquée - désélection")
                
        except Exception as e:
            print(f"❌ Erreur lors du clic sur le tableau: {e}")

    def _add_pagination_controls(self):
        """Ajoute les contrôles de pagination - DÉSACTIVÉ (tableau fixe à 10 lignes)"""
        # Pagination désactivée car le tableau est maintenant fixé à 10 lignes maximum
        pass
    
    def _go_to_previous_page(self):
        """Va à la page précédente"""
        if self.current_page > 1:
            self.current_page -= 1
            # Recharger les données filtrées
            filtered = []
            for assoc in self.classe_matieres.values():
                if self.selected_niveau:
                    classe_data = self.classes.get(assoc['id_classe'], {})
                    if classe_data.get('niveau') != self.selected_niveau:
                        continue
                if self.selected_classe:
                    classe_data = self.classes.get(assoc['id_classe'], {})
                    if classe_data.get('nom') != self.selected_classe:
                        continue
                filtered.append(assoc)
            
            filtered.sort(key=lambda x: (x['classe_nom'], x['matiere_nom']))
            self._update_matieres_table(filtered)
            self._update_stats(len(filtered))
    
    def _go_to_next_page(self):
        """Va à la page suivante"""
        if self.current_page < self.total_pages:
            self.current_page += 1
            # Recharger les données filtrées
            filtered = []
            for assoc in self.classe_matieres.values():
                if self.selected_niveau:
                    classe_data = self.classes.get(assoc['id_classe'], {})
                    if classe_data.get('niveau') != self.selected_niveau:
                        continue
                if self.selected_classe:
                    classe_data = self.classes.get(assoc['id_classe'], {})
                    if classe_data.get('nom') != self.selected_classe:
                        continue
                filtered.append(assoc)
            
            filtered.sort(key=lambda x: (x['classe_nom'], x['matiere_nom']))
            self._update_matieres_table(filtered)
            self._update_stats(len(filtered))
    
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
        """Ouvre le formulaire modal de matière - VERSION SIMPLIFIÉE PACK()"""
        print(f"🔍 DEBUG: _open_matiere_form appelé - selected_niveau = {self.selected_niveau}")
        
        if self.form_modal:
            self.form_modal.destroy()
        
        self.form_modal = Toplevel(self)
        self.form_modal.title("Ajouter une Matière")
        self.form_modal.geometry("900x800")  # FORMULAIRE ENCORE PLUS GRAND
        self.form_modal.configure(bg=BG_MAIN)
        self.form_modal.resizable(True, True)
        
        # Centrer la fenêtre
        self.form_modal.transient(self)
        self.form_modal.grab_set()
        
        # Centrage automatique
        self.form_modal.update_idletasks()
        x = self.winfo_rootx() + (self.winfo_width() - 900) // 2
        y = self.winfo_rooty() + (self.winfo_height() - 800) // 2
        self.form_modal.geometry(f"+{x}+{y}")
        
        # Frame principal avec design moderne
        main_frame = ctk.CTkFrame(self.form_modal, fg_color=BG_CARD, corner_radius=20, 
                                 border_width=1, border_color=BORDER_COLOR)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # En-tête avec boutons
        header_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        header_frame.pack(fill="x", padx=20, pady=(20, 10))
        
        # Titre à gauche
        title_label = ctk.CTkLabel(header_frame, text="Ajouter une Matière", 
                                  font=ctk.CTkFont(size=24, weight="bold"), 
                                  text_color=ACCENT)
        title_label.pack(side="left")
        
        # Boutons à droite
        buttons_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        buttons_frame.pack(side="right")
        
        # Charger les icônes
        def load_icon(name, size=(20, 20)):
            try:
                icon_path = os.path.join(project_root, "resources", "icons", f"{name}.png")
                if os.path.exists(icon_path):
                    return ctk.CTkImage(Image.open(icon_path), size=size)
            except Exception as e:
                print(f"❌ Erreur chargement icône {name}: {e}")
            return None
        
        save_icon = load_icon("check")
        cancel_icon = load_icon("close")
        
        # Bouton Enregistrer avec icône - STYLE CONTOUR
        def on_save_click():
            print("🔍 DEBUG: Bouton Enregistrer cliqué!")
            self._save_matiere()
        
        save_btn = ctk.CTkButton(buttons_frame, text="Enregistrer", 
                                command=on_save_click,
                                image=save_icon,
                                compound="left",
                                fg_color="transparent",
                                border_color=SUCCESS_GREEN,
                                border_width=2,
                                hover_color=SUCCESS_GREEN,
                                text_color=SUCCESS_GREEN,
                                height=40, corner_radius=8, width=140,
                                font=ctk.CTkFont(size=14, weight="bold"))
        save_btn.pack(side="left", padx=(0, 10))
        
        # Bouton Annuler avec icône - STYLE CONTOUR
        cancel_btn = ctk.CTkButton(buttons_frame, text="Annuler", 
                                  command=self.form_modal.destroy,
                                  image=cancel_icon,
                                  compound="left",
                                  fg_color="transparent",
                                  border_color=ERROR_RED,
                                  border_width=2,
                                  hover_color=ERROR_RED,
                                  text_color=ERROR_RED,
                                  height=40, corner_radius=8, width=120,
                                  font=ctk.CTkFont(size=14, weight="bold"))
        cancel_btn.pack(side="left")
        
        
        # Frame de contenu
        content_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        content_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Nom de la matière
        nom_label = ctk.CTkLabel(content_frame, text="Nom de la matière", 
                                font=ctk.CTkFont(size=14, weight="bold"), 
                                text_color=TEXT_PRIMARY)
        nom_label.pack(anchor="w", pady=(0, 5))
        
        self.nom_var = StringVar()
        nom_entry = ctk.CTkEntry(content_frame, textvariable=self.nom_var, 
                                font=ctk.CTkFont(size=12), 
                                placeholder_text="Ex: Mathématiques, Français, Sciences...",
                                height=40, corner_radius=8,
                                fg_color=BG_SIDEBAR, border_color=BORDER_COLOR)
        nom_entry.pack(fill="x", pady=(0, 15))
        
        # Coefficient
        coeff_label = ctk.CTkLabel(content_frame, text="Coefficient", 
                                  font=ctk.CTkFont(size=14, weight="bold"), 
                                  text_color=TEXT_PRIMARY)
        coeff_label.pack(anchor="w", pady=(0, 5))
        
        self.coefficient_var = StringVar(value="1.0")
        coefficient_entry = ctk.CTkEntry(content_frame, textvariable=self.coefficient_var, 
                                        font=ctk.CTkFont(size=12), 
                                        placeholder_text="1.0",
                                        height=40, corner_radius=8,
                                        fg_color=BG_SIDEBAR, border_color=BORDER_COLOR)
        coefficient_entry.pack(fill="x", pady=(0, 15))
        
        # Classes disponibles
        classes_label = ctk.CTkLabel(content_frame, text="Classes concernées", 
                                    font=ctk.CTkFont(size=14, weight="bold"), 
                                    text_color=TEXT_PRIMARY)
        classes_label.pack(anchor="w", pady=(0, 5))
        
        classes_frame = ctk.CTkScrollableFrame(content_frame, fg_color=BG_SIDEBAR,
                                    corner_radius=8, height=160)
        classes_frame.pack(fill="x", pady=(0, 15))
        
        # Liste des classes avec cases à cocher - HORIZONTAL
        self.classes_selected = {}
        try:
            classes_niveau = get_classes_by_niveau(self.selected_niveau)
            print(f"🔍 DEBUG: classes_niveau = {classes_niveau}")
            
            if not classes_niveau:
                print("⚠️ Aucune classe trouvée pour ce niveau")
                no_classes_label = ctk.CTkLabel(classes_frame, text="Aucune classe disponible", 
                                               font=ctk.CTkFont(size=12), text_color=TEXT_SECONDARY)
                no_classes_label.pack(anchor="w", pady=5, padx=10)
            else:
                # Zone cases à cocher scrollable en grille (wrap automatique)
                classes_frame.grid_columnconfigure(0, weight=1)
                classes_frame.grid_columnconfigure(1, weight=1)
                classes_frame.grid_columnconfigure(2, weight=1)
                classes_frame.grid_columnconfigure(3, weight=1)
                
                for i, (classe_id, classe_data) in enumerate(classes_niveau.items()):
                    # Vérifier le nombre de matières existantes pour cette classe
                    from database.connection import get_db_connection
                    conn = get_db_connection()
                    cursor = conn.cursor()
                    cursor.execute("""
                        SELECT COUNT(*) FROM classe_matieres 
                        WHERE id_classe = ? AND statut = 'active'
                    """, (classe_id,))
                    nb_matieres = cursor.fetchone()[0]
                    conn.close()
                    
                    var = ctk.BooleanVar()
                    # Désactiver la checkbox si la classe a déjà 10 matières
                    is_disabled = nb_matieres >= 10
                    
                    # Texte avec indication du nombre de matières
                    classe_text = f"{classe_data['nom_classe']} ({nb_matieres}/10)"
                    
                    checkbox = ctk.CTkCheckBox(classes_frame, text=classe_text,
                                      variable=var, font=ctk.CTkFont(size=12),
                                      fg_color=ACCENT, hover_color="#4A90E2",
                                      state="disabled" if is_disabled else "normal")
                    row_idx = i // 4
                    col_idx = i % 4
                    checkbox.grid(row=row_idx, column=col_idx, padx=(10, 10), pady=6, sticky="w")
                    self.classes_selected[classe_id] = var
                    
                    # Ajouter un tooltip ou indication visuelle si saturée
                    if is_disabled:
                        checkbox.configure(text_color=TEXT_SECONDARY)
                    
                    print(f"✅ Checkbox créée pour {classe_data['nom_classe']} - {nb_matieres}/10 matières")
        except Exception as e:
            print(f"❌ Erreur lors du chargement des classes: {e}")
            error_label = ctk.CTkLabel(classes_frame, text=f"Erreur: {str(e)}", 
                                      font=ctk.CTkFont(size=12), text_color=ERROR_RED)
            error_label.pack(anchor="w", pady=5, padx=10)
        
        # Professeur
        prof_label = ctk.CTkLabel(content_frame, text="Professeur assigné", 
                                 font=ctk.CTkFont(size=14, weight="bold"), 
                                 text_color=TEXT_PRIMARY)
        prof_label.pack(anchor="w", pady=(0, 5))
        
        self.professeur_var = StringVar()
        try:
            print(f"🔍 DEBUG: self.professeurs type = {type(self.professeurs)}")
            print(f"🔍 DEBUG: self.professeurs content = {self.professeurs}")
            
            # Vérifier si self.professeurs est une liste ou un dictionnaire
            if isinstance(self.professeurs, list):
                professeur_values = ["Aucun"] + [f"{p.get('nom', '')} {p.get('prenom', '')}" for p in self.professeurs if p.get('nom') and p.get('prenom')]
            else:
                professeur_values = ["Aucun"] + [f"{p.get('nom', '')} {p.get('prenom', '')}" for p in self.professeurs.values() if p.get('nom') and p.get('prenom')]
            
            print(f"🔍 DEBUG: professeur_values = {professeur_values}")
            
            professeur_dropdown = ctk.CTkComboBox(content_frame, values=professeur_values, 
                                                variable=self.professeur_var,
                                                font=ctk.CTkFont(size=12),
                                                fg_color=BG_CARD, border_color=BORDER_COLOR,
                                                dropdown_fg_color=BG_CARD, dropdown_hover_color=BORDER_COLOR)
            professeur_dropdown.pack(fill="x", pady=(0, 15))
            professeur_dropdown.set("Aucun")
        except Exception as e:
            print(f"❌ Erreur lors du chargement des professeurs: {e}")
            error_label = ctk.CTkLabel(content_frame, text="Erreur professeurs", 
                                      font=ctk.CTkFont(size=12), text_color=ERROR_RED)
            error_label.pack(anchor="w", pady=5)
        
        
        # Forcer l'affichage
        self.form_modal.update_idletasks()
        print("🔍 DEBUG: Formulaire créé avec pack() - boutons visibles")
    
    
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
            
            # Vérifier la limite de 10 matières par classe
            from database.connection import get_db_connection
            conn = get_db_connection()
            cursor = conn.cursor()
            
            classes_saturees = []
            for classe_id in classes_selected:
                # Compter les matières existantes pour cette classe
                cursor.execute("""
                    SELECT COUNT(*) FROM classe_matieres 
                    WHERE id_classe = ? AND statut = 'active'
                """, (classe_id,))
                nb_matieres = cursor.fetchone()[0]
                
                print(f"🔍 DEBUG: Classe {classe_id} a {nb_matieres} matières")
                
                if nb_matieres >= 10:
                    # Récupérer le nom de la classe
                    cursor.execute("SELECT nom_classe FROM classes WHERE id_classe = ?", (classe_id,))
                    classe_nom = cursor.fetchone()[0]
                    classes_saturees.append(classe_nom)
                    print(f"🚫 Classe {classe_nom} saturée ({nb_matieres}/10)")
            
            conn.close()
            
            if classes_saturees:
                print(f"🚫 BLOCAGE: {len(classes_saturees)} classes saturées")
                messagebox.showerror("Limite atteinte", 
                    f"Les classes suivantes ont déjà 10 matières (limite maximum) :\n\n" + 
                    "\n".join(classes_saturees) + 
                    "\n\nVeuillez supprimer une matière existante avant d'en ajouter une nouvelle.")
                return
            
            print("✅ Vérification OK: toutes les classes ont moins de 10 matières")
            
            # Récupérer l'ID du professeur
            professeur_nom = self.professeur_var.get()
            professeur_id = None
            if professeur_nom != "Aucun":
                try:
                    if isinstance(self.professeurs, dict):
                        for prof_id, prof_data in self.professeurs.items():
                            if f"{prof_data['nom']} {prof_data['prenom']}" == professeur_nom:
                                professeur_id = prof_id
                                break
                    else:
                        for prof_data in self.professeurs:
                            if f"{prof_data['nom']} {prof_data['prenom']}" == professeur_nom:
                                professeur_id = prof_data.get('id')  # 'id' si liste d'objets
                                break
                except Exception as e:
                    print(f"❌ Erreur lors de la recherche du professeur: {e}")
                    professeur_id = None
            
            # Sauvegarder en base
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
                # Vérifier une dernière fois avant l'insertion
                cursor.execute("""
                    SELECT COUNT(*) FROM classe_matieres 
                    WHERE id_classe = ? AND statut = 'active'
                """, (classe_id,))
                nb_matieres_avant = cursor.fetchone()[0]
                
                if nb_matieres_avant >= 10:
                    # Récupérer le nom de la classe
                    cursor.execute("SELECT nom_classe FROM classes WHERE id_classe = ?", (classe_id,))
                    classe_nom = cursor.fetchone()[0]
                    print(f"🚫 ERREUR: Classe {classe_nom} a atteint 10 matières pendant l'insertion")
                    conn.rollback()
                    conn.close()
                    messagebox.showerror("Erreur", f"La classe {classe_nom} a atteint la limite de 10 matières.")
                    return
                
                cursor.execute("""
                    INSERT INTO classe_matieres (id_classe, id_matiere, id_professeur, coefficient_classe)
                    VALUES (?, ?, ?, ?)
                """, (classe_id, matiere_id, professeur_id, coefficient))
                print(f"✅ Matière {nom} ajoutée à la classe {classe_id}")
            
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
    
    def _edit_matiere(self):
        """Modifie une matière sélectionnée"""
        if not self.selected_niveau:
            messagebox.showwarning("Sélection requise", "Veuillez d'abord sélectionner un niveau.")
            return
            
        if not self.selected_classe:
            messagebox.showwarning("Sélection requise", "Veuillez d'abord sélectionner une classe.")
            return
            
        # Vérifier s'il y a des matières à modifier
        filtered_matieres = []
        for assoc in self.classe_matieres.values():
            classe_data = self.classes.get(assoc['id_classe'], {})
            if classe_data.get('niveau') == self.selected_niveau and classe_data.get('nom') == self.selected_classe:
                filtered_matieres.append(assoc)
        
        if not filtered_matieres:
            messagebox.showinfo("Information", f"Aucune matière trouvée pour la classe {self.selected_classe}.")
            return
        
        # Ouvrir le sélecteur de matière
        self._open_matiere_selector(filtered_matieres)
    def _delete_matiere(self):
        """Supprime une matière sélectionnée"""
        if not self.selected_niveau:
            messagebox.showwarning("Sélection requise", "Veuillez d'abord sélectionner un niveau.")
            return
        
        if not self.selected_classe:
            messagebox.showwarning("Sélection requise", "Veuillez d'abord sélectionner une classe.")
            return
            
        # Vérifier s'il y a des matières à supprimer
        filtered_matieres = []
        for assoc in self.classe_matieres.values():
            classe_data = self.classes.get(assoc['id_classe'], {})
            if classe_data.get('niveau') == self.selected_niveau and classe_data.get('nom') == self.selected_classe:
                filtered_matieres.append(assoc)
        
        if not filtered_matieres:
            messagebox.showinfo("Information", f"Aucune matière trouvée pour la classe {self.selected_classe}.")
            return
        
        # Ouvrir le sélecteur de matière pour suppression
        self._open_matiere_selector_for_delete(filtered_matieres)
    
    def _open_matiere_selector_for_delete(self, matieres):
        """Ouvre le sélecteur de matière pour suppression"""
        if self.form_modal:
            self.form_modal.destroy()
        
        self.form_modal = Toplevel(self)
        self.form_modal.title("Supprimer une Matière")
        self.form_modal.geometry("900x800")
        self.form_modal.configure(bg=BG_MAIN)
        self.form_modal.resizable(True, True)
        
        # Centrer la fenêtre
        self.form_modal.transient(self)
        self.form_modal.grab_set()
        
        # Centrage automatique
        self.form_modal.update_idletasks()
        x = self.winfo_rootx() + (self.winfo_width() - 900) // 2
        y = self.winfo_rooty() + (self.winfo_height() - 800) // 2
        self.form_modal.geometry(f"+{x}+{y}")
        
        # Frame principal avec design moderne
        main_frame = ctk.CTkFrame(self.form_modal, fg_color=BG_CARD, corner_radius=20,
                                 border_width=1, border_color=BORDER_COLOR)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # En-tête
        header_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        header_frame.pack(fill="x", padx=20, pady=(20, 10))
        
        # Titre
        title_label = ctk.CTkLabel(header_frame, text="Supprimer une Matière", 
                                  font=ctk.CTkFont(size=24, weight="bold"), 
                                  text_color=ERROR_RED)
        title_label.pack(side="left")
        
        # Boutons en haut
        buttons_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        buttons_frame.pack(side="right")
        
        # Charger l'icône
        def load_icon(name, size=(20, 20)):
            try:
                icon_path = os.path.join(project_root, "resources", "icons", f"{name}.png")
                if os.path.exists(icon_path):
                    return ctk.CTkImage(Image.open(icon_path), size=size)
            except Exception as e:
                print(f"❌ Erreur chargement icône {name}: {e}")
            return None
        
        cancel_icon = load_icon("close")
        
        cancel_btn = ctk.CTkButton(buttons_frame, text="Annuler", 
                                  command=self.form_modal.destroy,
                                  image=cancel_icon,
                                  compound="left",
                                  fg_color="transparent",
                                  border_color=ERROR_RED,
                                  border_width=2,
                                  hover_color=ERROR_RED,
                                  text_color=ERROR_RED,
                                  height=40, corner_radius=8, width=120,
                                  font=ctk.CTkFont(size=14, weight="bold"))
        cancel_btn.pack(side="right")
        
        # Frame de contenu
        content_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        content_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Sous-titre
        subtitle_label = ctk.CTkLabel(content_frame, text="Sélectionnez la matière à supprimer :", 
                                     font=ctk.CTkFont(size=16, weight="bold"), 
                                     text_color=TEXT_PRIMARY)
        subtitle_label.pack(anchor="w", pady=(0, 20))
        
        # Liste des matières
        matieres_frame = ctk.CTkScrollableFrame(content_frame, fg_color=BG_SIDEBAR, corner_radius=12)
        matieres_frame.pack(fill="both", expand=True)
        
        for matiere in matieres:
            matiere_frame = ctk.CTkFrame(matieres_frame, fg_color=BG_CARD, corner_radius=10,
                                        border_width=1, border_color=BORDER_COLOR)
            matiere_frame.pack(fill="x", pady=5)
            
            # Contenu de la matière
            matiere_content = ctk.CTkFrame(matiere_frame, fg_color="transparent")
            matiere_content.pack(fill="x", padx=15, pady=10)
            
            # Nom de la matière
            nom_label = ctk.CTkLabel(matiere_content, text=matiere['matiere_nom'], 
                                    font=ctk.CTkFont(size=16, weight="bold"), 
                                    text_color=TEXT_PRIMARY)
            nom_label.pack(anchor="w")
            
            # Détails
            details_label = ctk.CTkLabel(matiere_content, 
                                        text=f"Coefficient: {matiere['coefficient_classe']} | Professeur: {matiere['professeur_nom']}", 
                                        font=ctk.CTkFont(size=12), 
                                        text_color=TEXT_SECONDARY)
            details_label.pack(anchor="w", pady=(2, 0))
            
            # Bouton Supprimer
            def on_delete_click(matiere_data=matiere):
                print("🔍 DEBUG: Bouton Supprimer cliqué!")
                self._confirm_delete_matiere(matiere_data)
            
            delete_btn = ctk.CTkButton(matiere_content, text="Supprimer", 
                                      command=on_delete_click,
                                      fg_color=ERROR_RED, 
                                      hover_color="#D32F2F",
                                      text_color="white",
                                      height=35, corner_radius=8, width=100,
                                      font=ctk.CTkFont(size=12, weight="bold"))
            delete_btn.pack(anchor="e", pady=(5, 0))
    
    def _confirm_delete_matiere(self, matiere_data):
        """Confirme et supprime la matière"""
        matiere_nom = matiere_data.get('matiere_nom', 'Inconnue')
        classe_nom = matiere_data.get('classe_nom', 'Inconnue')
        
        result = messagebox.askyesno(
            "Confirmation de suppression",
            f"Êtes-vous sûr de vouloir supprimer la matière :\n\n"
            f"• Matière : {matiere_nom}\n"
            f"• Classe : {classe_nom}\n"
            f"• Coefficient : {matiere_data.get('coefficient_classe', 'N/A')}\n\n"
            f"⚠️ Cette action est irréversible !"
        )
        
        if result:
            try:
                # Supprimer de la base de données
                from database.connection import get_db_connection
                conn = get_db_connection()
                cursor = conn.cursor()
                
                # Supprimer l'association classe-matière
                print(f"🔍 DEBUG: Suppression de l'association ID: {matiere_data['id_classe_matiere']}")
                cursor.execute("""
                    DELETE FROM classe_matieres 
                    WHERE id_classe_matiere = ?
                """, (matiere_data['id_classe_matiere'],))
                print(f"🔍 DEBUG: Requête DELETE exécutée, rowcount: {cursor.rowcount}")
                
                if cursor.rowcount > 0:
                    conn.commit()
                    conn.close()
                    
                    messagebox.showinfo("Succès", f"La matière '{matiere_nom}' a été supprimée avec succès.")
                    
                    # Fermer le modal
                    self.form_modal.destroy()
                    self.form_modal = None
                    
                    # Recharger les données
                    self._load_data()
                    self._filter_matieres()
                    
                    print(f"✅ Matière '{matiere_nom}' supprimée avec succès")
                else:
                    conn.close()
                    messagebox.showerror("Erreur", "Aucune matière n'a été supprimée.")
                    
            except Exception as e:
                print(f"❌ Erreur lors de la suppression: {e}")
                messagebox.showerror("Erreur", f"Erreur lors de la suppression:\n{str(e)}")
    
    def _open_matiere_selector(self, matieres):
        """Ouvre le sélecteur de matière pour modification"""
        if self.form_modal:
            self.form_modal.destroy()
        
        self.form_modal = Toplevel(self)
        self.form_modal.title("Sélectionner une Matière")
        self.form_modal.geometry("900x800")  # MÊME TAILLE QUE LES AUTRES
        self.form_modal.configure(bg=BG_MAIN)
        self.form_modal.resizable(True, True)
        
        # Centrer la fenêtre
        self.form_modal.transient(self)
        self.form_modal.grab_set()
        
        # Centrage automatique
        self.form_modal.update_idletasks()
        x = self.winfo_rootx() + (self.winfo_width() - 900) // 2
        y = self.winfo_rooty() + (self.winfo_height() - 800) // 2
        self.form_modal.geometry(f"+{x}+{y}")
        
        # Frame principal avec design moderne
        main_frame = ctk.CTkFrame(self.form_modal, fg_color=BG_CARD, corner_radius=20,
                                 border_width=1, border_color=BORDER_COLOR)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        main_frame.grid_columnconfigure(0, weight=1)
        
        # Header avec design moderne
        header_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        header_frame.pack(fill="x", padx=20, pady=(20, 10))
        
        # Titre à gauche
        title_label = ctk.CTkLabel(header_frame, text="Sélectionner une Matière", 
                                  font=ctk.CTkFont(size=24, weight="bold"), 
                                  text_color=ACCENT)
        title_label.pack(side="left")
        
        # Sous-titre avec marge
        subtitle_label = ctk.CTkLabel(header_frame, text=f"Classe: {self.selected_classe}", 
                                     font=ctk.CTkFont(size=12), 
                                     text_color=TEXT_SECONDARY)
        subtitle_label.pack(anchor="w", pady=(15, 0), padx=(0, 0))
        
        # Frame de contenu
        content_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        content_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Liste des matières avec design moderne
        list_frame = ctk.CTkScrollableFrame(content_frame, fg_color=BG_SIDEBAR, corner_radius=12)
        list_frame.pack(fill="both", expand=True, pady=(0, 15))
        list_frame.grid_columnconfigure(0, weight=1)
        
        # Titre de la liste
        list_title = ctk.CTkLabel(list_frame, text="Matières disponibles", 
                                 font=ctk.CTkFont(size=16, weight="bold"), 
                                 text_color=TEXT_PRIMARY)
        list_title.grid(row=0, column=0, sticky="w", pady=(10, 15), padx=15)
        
        # Boutons pour chaque matière
        for i, matiere in enumerate(matieres):
            matiere_btn = ctk.CTkButton(
                list_frame,
                text=f"{matiere['matiere_nom']} (Coeff: {matiere['coefficient_classe']})",
                command=lambda m=matiere: self._open_edit_form(m),
                fg_color=BG_CARD,
                hover_color=ACCENT,
                text_color=TEXT_PRIMARY,
                height=50,
                corner_radius=10,
                font=ctk.CTkFont(size=14, weight="bold"),
                border_width=1,
                border_color=BORDER_COLOR
            )
            matiere_btn.grid(row=i+1, column=0, sticky="ew", pady=8, padx=15)
        
        # Boutons en bas
        buttons_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        buttons_frame.pack(side="bottom", fill="x", padx=20, pady=(10, 20))
        
        # Charger l'icône
        def load_icon(name, size=(20, 20)):
            try:
                icon_path = os.path.join(project_root, "resources", "icons", f"{name}.png")
                if os.path.exists(icon_path):
                    return ctk.CTkImage(Image.open(icon_path), size=size)
            except Exception as e:
                print(f"❌ Erreur chargement icône {name}: {e}")
            return None
        
        cancel_icon = load_icon("close")
        
        cancel_btn = ctk.CTkButton(buttons_frame, text="Annuler", 
                                  command=self.form_modal.destroy,
                                  image=cancel_icon,
                                  compound="left",
                                  fg_color="transparent",
                                  border_color=ERROR_RED,
                                  border_width=2,
                                  hover_color=ERROR_RED,
                                  text_color=ERROR_RED,
                                  height=40, corner_radius=8, width=120,
                                  font=ctk.CTkFont(size=14, weight="bold"))
        cancel_btn.pack(side="right")
    
    def _open_edit_form(self, matiere_data):
        """Ouvre le formulaire modal de modification de matière - VERSION SIMPLIFIÉE PACK()"""
        if self.form_modal:
            self.form_modal.destroy()
        
        self.form_modal = Toplevel(self)
        self.form_modal.title("Modifier une Matière")
        self.form_modal.geometry("900x800")  # FORMULAIRE ENCORE PLUS GRAND
        self.form_modal.configure(bg=BG_MAIN)
        self.form_modal.resizable(True, True)
        
        # Centrer la fenêtre
        self.form_modal.transient(self)
        self.form_modal.grab_set()
        
        # Centrage automatique
        self.form_modal.update_idletasks()
        x = self.winfo_rootx() + (self.winfo_width() - 900) // 2
        y = self.winfo_rooty() + (self.winfo_height() - 800) // 2
        self.form_modal.geometry(f"+{x}+{y}")
        
        # Frame principal avec design moderne
        main_frame = ctk.CTkFrame(self.form_modal, fg_color=BG_CARD, corner_radius=20, 
                                 border_width=1, border_color=BORDER_COLOR)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # En-tête avec boutons
        header_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        header_frame.pack(fill="x", padx=20, pady=(20, 10))
        
        # Titre à gauche
        title_label = ctk.CTkLabel(header_frame, text=f"Modifier {matiere_data['matiere_nom']}", 
                                  font=ctk.CTkFont(size=24, weight="bold"), 
                                  text_color=ACCENT)
        title_label.pack(side="left")
        
        # Boutons à droite
        buttons_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        buttons_frame.pack(side="right")
        
        # Charger les icônes
        def load_icon(name, size=(20, 20)):
            try:
                icon_path = os.path.join(project_root, "resources", "icons", f"{name}.png")
                if os.path.exists(icon_path):
                    return ctk.CTkImage(Image.open(icon_path), size=size)
            except Exception as e:
                print(f"❌ Erreur chargement icône {name}: {e}")
            return None
        
        save_icon = load_icon("check")
        cancel_icon = load_icon("close")
        
        # Bouton Modifier avec icône - STYLE CONTOUR
        def on_modifier_click():
            print("🔍 DEBUG: Bouton Modifier cliqué!")
            self._update_matiere(matiere_data['id_classe_matiere'])
        
        save_btn = ctk.CTkButton(buttons_frame, text="Modifier", 
                                command=on_modifier_click,
                                image=save_icon,
                                compound="left",
                                fg_color="transparent", 
                                border_color=WARNING_YELLOW, 
                                border_width=2,
                                hover_color=WARNING_YELLOW,
                                text_color=WARNING_YELLOW,
                                height=40, corner_radius=8, width=130,
                                font=ctk.CTkFont(size=14, weight="bold"))
        save_btn.pack(side="left", padx=(0, 10))
        
        # Bouton Annuler avec icône - STYLE CONTOUR
        cancel_btn = ctk.CTkButton(buttons_frame, text="Annuler", 
                                  command=self.form_modal.destroy,
                                  image=cancel_icon,
                                  compound="left",
                                  fg_color="transparent",
                                  border_color=ERROR_RED,
                                  border_width=2,
                                  hover_color=ERROR_RED,
                                  text_color=ERROR_RED,
                                  height=40, corner_radius=8, width=120,
                                  font=ctk.CTkFont(size=14, weight="bold"))
        cancel_btn.pack(side="left")
        
        
        # Frame de contenu
        content_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        content_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Nom de la matière
        nom_label = ctk.CTkLabel(content_frame, text="Nom de la matière", 
                                font=ctk.CTkFont(size=14, weight="bold"), 
                                text_color=TEXT_PRIMARY)
        nom_label.pack(anchor="w", pady=(0, 5))
        
        self.nom_var = StringVar(value=matiere_data['matiere_nom'])
        nom_entry = ctk.CTkEntry(content_frame, textvariable=self.nom_var, 
                                font=ctk.CTkFont(size=12), 
                                placeholder_text="Ex: Mathématiques, Français, Sciences...",
                                height=40, corner_radius=8,
                                fg_color=BG_SIDEBAR, border_color=BORDER_COLOR)
        nom_entry.pack(fill="x", pady=(0, 15))
        
        # Coefficient
        coeff_label = ctk.CTkLabel(content_frame, text="Coefficient", 
                                  font=ctk.CTkFont(size=14, weight="bold"), 
                                  text_color=TEXT_PRIMARY)
        coeff_label.pack(anchor="w", pady=(0, 5))
        
        self.coefficient_var = StringVar(value=str(matiere_data['coefficient_classe']))
        coefficient_entry = ctk.CTkEntry(content_frame, textvariable=self.coefficient_var, 
                                        font=ctk.CTkFont(size=12), 
                                        placeholder_text="1.0",
                                        height=40, corner_radius=8,
                                        fg_color=BG_SIDEBAR, border_color=BORDER_COLOR)
        coefficient_entry.pack(fill="x", pady=(0, 15))
        
        # Professeur - AMÉLIORÉ
        prof_label = ctk.CTkLabel(content_frame, text="Professeur assigné", 
                                 font=ctk.CTkFont(size=14, weight="bold"), 
                                 text_color=TEXT_PRIMARY)
        prof_label.pack(anchor="w", pady=(0, 5))
        
        self.professeur_var = StringVar()
        print(f"🔍 DEBUG: Formulaire modification - self.professeurs type: {type(self.professeurs)}")
        print(f"🔍 DEBUG: Formulaire modification - self.professeurs contenu: {self.professeurs}")
        try:
            if isinstance(self.professeurs, dict):
                professeur_values = ["Aucun"] + [f"{p['nom']} {p['prenom']}" for p in self.professeurs.values()]
            else:
                professeur_values = ["Aucun"] + [f"{p['nom']} {p['prenom']}" for p in self.professeurs]
            print(f"🔍 DEBUG: Formulaire modification - professeur_values: {professeur_values}")
        except Exception as e:
            print(f"❌ Erreur lors du chargement des professeurs: {e}")
            professeur_values = ["Aucun"]
        
        professeur_dropdown = ctk.CTkComboBox(content_frame, variable=self.professeur_var,
                                             values=professeur_values,
                                             state="readonly", height=40, corner_radius=8,
                                             font=ctk.CTkFont(size=12),
                                             fg_color=BG_SIDEBAR, border_color=BORDER_COLOR)
        professeur_dropdown.pack(fill="x", pady=(0, 15))
        
        # Définir la valeur actuelle
        current_prof = matiere_data.get('professeur_nom', 'Non assigné')
        if current_prof and current_prof != 'Non assigné':
            professeur_dropdown.set(current_prof)
        else:
            professeur_dropdown.set("Aucun")
        
        
        # Forcer l'affichage
        self.form_modal.update_idletasks()
        print("🔍 DEBUG: Formulaire de modification créé avec pack() - boutons visibles")
    
    def _update_matiere(self, id_classe_matiere):
        """Met à jour une matière"""
        print(f"🔍 DEBUG: _update_matiere appelé avec id_classe_matiere: {id_classe_matiere}")
        try:
            # Validation des champs
            nom_matiere = self.nom_var.get().strip()
            print(f"🔍 DEBUG: nom_matiere: '{nom_matiere}'")
            if not nom_matiere:
                messagebox.showerror("Erreur", "Le nom de la matière est obligatoire.")
                return
            
            coefficient = float(self.coefficient_var.get())
            professeur_nom = self.professeur_var.get()
            
            print(f"🔍 DEBUG: Modification - professeur_nom sélectionné: '{professeur_nom}'")
            print(f"🔍 DEBUG: self.professeurs type: {type(self.professeurs)}")
            print(f"🔍 DEBUG: self.professeurs contenu: {self.professeurs}")
            
            # Trouver l'ID du professeur
            professeur_id = None
            if professeur_nom != "Aucun":
                try:
                    if isinstance(self.professeurs, dict):
                        for prof_id, prof_data in self.professeurs.items():
                            prof_full_name = f"{prof_data['nom']} {prof_data['prenom']}"
                            print(f"🔍 DEBUG: Comparaison - '{prof_full_name}' vs '{professeur_nom}'")
                            if prof_full_name == professeur_nom:
                                professeur_id = prof_id
                                print(f"🔍 DEBUG: Professeur trouvé - ID: {professeur_id}")
                                break
                    else:
                        for prof_data in self.professeurs:
                            prof_full_name = f"{prof_data['nom']} {prof_data['prenom']}"
                            print(f"🔍 DEBUG: Comparaison - '{prof_full_name}' vs '{professeur_nom}'")
                            if prof_full_name == professeur_nom:
                                professeur_id = prof_data.get('id')
                                print(f"🔍 DEBUG: Professeur trouvé - ID: {professeur_id}")
                                break
                except Exception as e:
                    print(f"❌ Erreur lors de la recherche du professeur: {e}")
                    professeur_id = None

            print(f"🔍 DEBUG: professeur_id final: {professeur_id}")
            # Mettre à jour en base
            from database.connection import get_db_connection
            conn = get_db_connection()
            cursor = conn.cursor()
            
            # Récupérer l'ID de la matière
            cursor.execute("SELECT id_matiere FROM classe_matieres WHERE id_classe_matiere = ?", (int(id_classe_matiere),))
            id_matiere = cursor.fetchone()[0]
            
            # Mettre à jour le nom de la matière
            cursor.execute("""
                UPDATE matieres 
                SET nom_matiere = ?
                WHERE id_matiere = ?
            """, (nom_matiere, id_matiere))
            
            # Mettre à jour l'association classe-matière
            print(f"🔍 DEBUG: Mise à jour - professeur_id: {professeur_id}, coefficient: {coefficient}, id_classe_matiere: {id_classe_matiere}")
            cursor.execute("""
                UPDATE classe_matieres 
                SET coefficient_classe = ?, id_professeur = ?
                WHERE id_classe_matiere = ?
            """, (coefficient, professeur_id if professeur_id else None, int(id_classe_matiere)))
            
            # Vérifier que la mise à jour a bien eu lieu
            cursor.execute("SELECT id_professeur FROM classe_matieres WHERE id_classe_matiere = ?", (int(id_classe_matiere),))
            updated_prof = cursor.fetchone()
            print(f"🔍 DEBUG: Professeur après mise à jour: {updated_prof[0] if updated_prof else 'None'}")
            
            conn.commit()
            conn.close()
            
            messagebox.showinfo("Succès", "Matière modifiée avec succès!")
            self.form_modal.destroy()
            self.form_modal = None
            
            # Recharger les données pour mettre à jour le tableau
            print("🔄 Rechargement des données après modification...")
            self._load_data()
            print(f"✅ Données rechargées: {len(self.classe_matieres)} associations")
            
            # Debug: vérifier les données rechargées
            for key, assoc in list(self.classe_matieres.items())[:3]:
                print(f"🔍 DEBUG: Après rechargement - ID: {key}, Professeur: {assoc['professeur_nom']} (ID: {assoc['id_professeur']})")
            
            self._filter_matieres()
            print("✅ Tableau mis à jour")
            
        except ValueError as e:
            print(f"❌ Erreur ValueError: {e}")
            messagebox.showerror("Erreur", "Le coefficient doit être un nombre valide.")
        except Exception as e:
            print(f"❌ Erreur Exception: {e}")
            messagebox.showerror("Erreur", f"Erreur lors de la modification:\n{str(e)}")

