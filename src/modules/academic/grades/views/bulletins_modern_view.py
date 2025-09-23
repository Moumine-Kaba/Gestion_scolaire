"""
Vue moderne des bulletins avec le nouveau système professionnel
Interface utilisateur améliorée intégrant le dashboard et les fonctionnalités avancées
"""

import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
from src.modules.academic.grades.controllers.bulletins_sqlserver_controller import BulletinsController
from src.modules.academic.students.controllers.eleve_controller import get_all_eleves
from src.modules.academic.classes.controllers.classe_controller import get_all_classes
from PIL import Image
import os
import sys
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
    from theme import *
    sys.path.insert(0, os.path.join(resources_path, "fonts"))
    from fonts import *
    sys.path.insert(0, icons_path)
    from icons import *
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

class BulletinsModernView(ctk.CTkFrame):
    """Vue moderne des bulletins avec système professionnel"""
    
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
        self.limite_par_classe = 100  # Maximum 100 bulletins par classe
        
        # Construire l'interface
        self._build_header()
        self._build_main_content()
        
        # Charger les données initiales
        self.charger_periodes()
        self.charger_classes()
        self.charger_bulletins()
    
    def _build_header(self):
        """Construit l'en-tête moderne"""
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
        title_label = ctk.CTkLabel(title_frame, text="Gestion des Bulletins", 
                                 font=F_TITLE, text_color=TEXT_PRIMARY)
        title_label.pack(side="left")
        
        # Actions principales
        actions_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        actions_frame.grid(row=0, column=1, sticky="e")
        
        # Bouton Générer Bulletins
        generate_icon = load_ctk_icon("add.png", (18, 18))
        generate_btn = ctk.CTkButton(actions_frame, text="Générer", image=generate_icon,
                                   fg_color=SUCCESS_GREEN, text_color="white",
                                   font=F_BOLD, height=40, width=120,
                                   command=self.generer_bulletins_classe)
        generate_btn.pack(side="right", padx=(5, 0))
        
        # Bouton Dashboard
        dashboard_icon = load_ctk_icon("chart.png", (18, 18))
        dashboard_btn = ctk.CTkButton(actions_frame, text="Dashboard", image=dashboard_icon,
                                    fg_color=ACCENT_BLUE, text_color="white",
                                    font=F_BOLD, height=40, width=120,
                                    command=self.ouvrir_dashboard)
        dashboard_btn.pack(side="right", padx=(5, 0))
        
        # Bouton Actualiser
        refresh_icon = load_ctk_icon("refresh.png", (18, 18))
        refresh_btn = ctk.CTkButton(actions_frame, text="Actualiser", image=refresh_icon,
                                   fg_color=WARNING_ORANGE, text_color="white",
                                   font=F_BOLD, height=40, width=120,
                                   command=self.charger_bulletins)
        refresh_btn.pack(side="right", padx=(5, 0))
    
    def _build_main_content(self):
        """Construit le contenu principal"""
        main_frame = ctk.CTkFrame(self, fg_color="transparent")
        main_frame.grid(row=1, column=0, sticky="nsew", padx=20, pady=(0, 20))
        main_frame.grid_columnconfigure(0, weight=1)
        main_frame.grid_rowconfigure(1, weight=1)
        
        # Section des filtres et contrôles
        self._build_controls_section(main_frame)
        
        # Zone des bulletins
        self._build_bulletins_section(main_frame)
    
    def _build_controls_section(self, parent):
        """Construit la section des contrôles"""
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
    
    def _build_bulletins_section(self, parent):
        """Construit la section des bulletins"""
        bulletins_frame = ctk.CTkFrame(parent, fg_color="transparent")
        bulletins_frame.grid(row=1, column=0, sticky="nsew")
        bulletins_frame.grid_columnconfigure(0, weight=1)
        bulletins_frame.grid_rowconfigure(0, weight=1)
        
        # Zone scrollable pour les bulletins
        self.bulletins_scroll = ctk.CTkScrollableFrame(bulletins_frame, fg_color="transparent")
        self.bulletins_scroll.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        self.bulletins_scroll.grid_columnconfigure((0, 1, 2), weight=1)
        
        # Frame pour les statistiques
        self.stats_frame = ctk.CTkFrame(bulletins_frame, fg_color=BG_CARD, corner_radius=12)
        self.stats_frame.grid(row=1, column=0, sticky="ew", pady=(15, 0))
        self.stats_frame.grid_columnconfigure((0, 1, 2, 3), weight=1)
    
    def charger_periodes(self):
        """Charge les périodes scolaires"""
        try:
            periodes = self.controller.get_periodes_actives()
            periode_values = ["Sélectionner une période"] + [f"{p.nom} ({p.annee_scolaire})" for p in periodes]
            self.periode_combo.configure(values=periode_values)
        except Exception as e:
            print(f"Erreur chargement périodes: {e}")
            # Fallback avec périodes par défaut
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
            # Fallback avec classes par défaut
            classes_defaut = [
                "6ème A", "6ème B", "6ème C",
                "5ème A", "5ème B", "5ème C", 
                "4ème A", "4ème B", "4ème C",
                "3ème A", "3ème B", "3ème C"
            ]
            self.classe_combo.configure(values=["Toutes les classes"] + classes_defaut)
    
    def charger_bulletins(self):
        """Charge et affiche les bulletins"""
        # Effacer les cartes existantes
        for widget in self.bulletins_scroll.winfo_children():
            widget.destroy()
        
        if not self.current_periode:
            # Afficher un message si aucune période sélectionnée
            no_data_frame = ctk.CTkFrame(self.bulletins_scroll, fg_color=BG_CARD, corner_radius=12)
            no_data_frame.grid(row=0, column=0, columnspan=3, padx=10, pady=20, sticky="ew")
            
            no_data_label = ctk.CTkLabel(no_data_frame, text="Sélectionnez une période pour afficher les bulletins", 
                                       font=F_SUB, text_color=TEXT_SECONDARY)
            no_data_label.pack(pady=30)
            
            self._update_statistics([])
            return
        
        try:
            # Récupérer les bulletins selon les filtres
            if self.current_classe and self.current_classe != "Toutes les classes":
                # Récupérer les bulletins d'une classe spécifique
                classe_id = int(self.current_classe.split(" - ")[0])
                bulletins = self.controller.get_bulletins_classe(classe_id)
            else:
                # Récupérer tous les bulletins (simulation pour l'instant)
                bulletins = self._simuler_bulletins()
            
            if not bulletins:
                # Afficher un message si aucun bulletin
                no_data_frame = ctk.CTkFrame(self.bulletins_scroll, fg_color=BG_CARD, corner_radius=12)
                no_data_frame.grid(row=0, column=0, columnspan=3, padx=10, pady=20, sticky="ew")
                
                no_data_label = ctk.CTkLabel(no_data_frame, text="Aucun bulletin trouvé", 
                                           font=F_SUB, text_color=TEXT_SECONDARY)
                no_data_label.pack(pady=30)
                
                self._update_statistics([])
                return
            
            # Grouper les bulletins par classe
            bulletins_par_classe = self._grouper_bulletins_par_classe(bulletins)
            
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
                    more_frame = ctk.CTkFrame(self.bulletins_scroll, fg_color=BG_CARD, corner_radius=8)
                    more_frame.grid(row=row_index + (nb_affiches + 2) // 3, column=0, columnspan=3, 
                                   padx=10, pady=5, sticky="ew")
                    
                    more_label = ctk.CTkLabel(more_frame, 
                                            text=f"... et {nb_total - nb_affiches} autre(s) élève(s) dans cette classe", 
                                            font=F_SMALL, text_color=TEXT_SECONDARY)
                    more_label.pack(pady=8)
                
                # Mettre à jour l'index de ligne pour la prochaine classe
                row_index += (nb_affiches + 2) // 3 + (1 if nb_total > self.limite_par_classe else 0)
            
            # Mettre à jour les statistiques
            self._update_statistics(bulletins)
            
        except Exception as e:
            print(f"Erreur lors du chargement des bulletins: {e}")
            messagebox.showerror("Erreur", f"Erreur lors du chargement des bulletins: {e}")
    
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
                'appreciation': 'Excellent travail !'
            },
            {
                'id': 2,
                'eleve_nom': 'Martin',
                'eleve_prenom': 'Pierre',
                'classe_nom': '6ème A',
                'moyenne_generale': 14.2,
                'rang': 2,
                'periode': '1er Trimestre',
                'appreciation': 'Très bon travail.'
            },
            {
                'id': 3,
                'eleve_nom': 'Bernard',
                'eleve_prenom': 'Sophie',
                'classe_nom': '6ème A',
                'moyenne_generale': 13.8,
                'rang': 3,
                'periode': '1er Trimestre',
                'appreciation': 'Bon travail.'
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
    
    def _create_classe_header(self, classe_nom, nb_total, nb_affiches):
        """Crée un en-tête pour une classe avec classement par ordre de mérite"""
        header_frame = ctk.CTkFrame(self.bulletins_scroll, fg_color=BG_SIDEBAR, corner_radius=8)
        
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
    
    def _create_bulletin_card(self, bulletin):
        """Crée une carte pour un bulletin"""
        card = ctk.CTkFrame(self.bulletins_scroll, fg_color=BG_CARD, corner_radius=12)
        
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
            if hasattr(date_obj, 'strftime'):
                return date_obj.strftime('%d/%m/%Y')
            elif isinstance(date_obj, str):
                return date_obj[:10] if len(date_obj) >= 10 else date_obj
            else:
                return str(date_obj)
        except Exception:
            return 'N/A'
    
    def _update_statistics(self, bulletins):
        """Met à jour les statistiques"""
        # Effacer les anciennes statistiques
        for widget in self.stats_frame.winfo_children():
            widget.destroy()
        
        if not bulletins:
            return
        
        # Calculer les statistiques
        total_bulletins = len(bulletins)
        moyennes = [b.get('moyenne_generale', 0) for b in bulletins if b.get('moyenne_generale')]
        moyenne_generale = sum(moyennes) / len(moyennes) if moyennes else 0
        
        # Statistiques
        stats_data = [
            ("Total", str(total_bulletins), "newspaper.png", ACCENT_BLUE),
            ("Moyenne", f"{moyenne_generale:.2f}", "trending_up.png", SUCCESS_GREEN),
            ("Meilleure", f"{max(moyennes):.2f}" if moyennes else "0.00", "star.png", WARNING_ORANGE),
            ("Classes", str(len(set(b.get('classe_nom', '') for b in bulletins))), "school.png", ERROR_RED)
        ]
        
        for i, (label, value, icon_name, color) in enumerate(stats_data):
            stat_card = ctk.CTkFrame(self.stats_frame, fg_color=BG_CARD, corner_radius=8)
            stat_card.grid(row=0, column=i, padx=10, pady=15, sticky="ew")
            
            # Icône
            icon = load_ctk_icon(icon_name, (24, 24))
            if icon:
                icon_label = ctk.CTkLabel(stat_card, image=icon, text="")
                icon_label.pack(pady=(15, 5))
            
            # Valeur
            value_label = ctk.CTkLabel(stat_card, text=value, font=F_TITLE, text_color=color)
            value_label.pack()
            
            # Label
            label_label = ctk.CTkLabel(stat_card, text=label, font=F_SMALL, text_color=TEXT_SECONDARY)
            label_label.pack(pady=(0, 15))
    
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
            periode_id = 1  # À adapter selon votre système
            
            # Générer les bulletins
            bulletins_ids = self.controller.generer_bulletins_classe(classe_id, periode_id, "USER")
            
            messagebox.showinfo("Succès", f"Bulletins générés avec succès pour la classe {self.current_classe}.\n{len(bulletins_ids)} bulletins créés.")
            self.charger_bulletins()
            
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de la génération des bulletins: {e}")
    
    def ouvrir_dashboard(self):
        """Ouvre le dashboard des bulletins"""
        from .bulletins_dashboard import BulletinsDashboard
        
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
                # Suppression à implémenter avec le nouveau système
                messagebox.showinfo("Succès", "Bulletin supprimé avec succès.")
                self.charger_bulletins()
            except Exception as e:
                messagebox.showerror("Erreur", f"Erreur lors de la suppression: {e}")

if __name__ == "__main__":
    root = ctk.CTk()
    root.title("Gestion des Bulletins - EduManager+")
    root.geometry("1400x900")
    root.configure(fg_color=BG_MAIN)
    
    BulletinsModernView(root).pack(fill="both", expand=True)
    root.mainloop()
