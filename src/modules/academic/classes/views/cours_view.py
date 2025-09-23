import customtkinter as ctk
from tkinter import messagebox, ttk
from PIL import Image
import os
import sys
from datetime import datetime, timedelta
# Remplacé par SQL Server  # Remplacé par SQL Server
import time

# -*- coding: utf-8 -*-
"""
Gestion des Cours - Vue Unifiée Simplifiée
- Interface moderne avec table unifiée
- Design cohérent avec le thème EduManager+
"""

# Import du thème global depuis resources/themes/theme.py
try:
    import sys
    import os
    # Ajouter le chemin racine au sys.path
    root_path = os.path.join(os.path.dirname(__file__), '../../../../..')
    sys.path.insert(0, root_path)
    
    from resources.themes.theme import *
    print("✅ Thème global importé depuis resources/themes/theme.py")
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

# Import du système de minuteur
from src.modules.academic.classes.utils.course_timer import timer_manager, NotificationManager, CourseHistoryWindow

# Importations des contrôleurs unifiés
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.modules.academic.classes.controllers.cours_controller import (
    get_all_cours, add_cours, update_cours, delete_cours, get_cours_by_id,
    get_all_enseignements, add_enseignement, update_enseignement, delete_enseignement,
    get_all_emplois, add_emploi, update_emploi, delete_emploi,
    get_enseignement_by_id, get_emploi_by_id, get_cours_stats
)
from src.modules.academic.teachers.controllers.professeur_controller import get_all_professeurs
from src.modules.academic.classes.controllers.classe_controller import get_all_classes
from src.modules.academic.subjects.controllers.matiere_controller import get_all_matieres
from src.modules.administrative.maintenance.controllers.salle_controller import get_all_salles

def load_icon(icon_path, size=(20, 20)):
    """Charge une icône avec gestion d'erreur et fallback"""
    try:
        if not icon_path:
            return None
            
        # Vérifier si le fichier existe
        if not os.path.exists(icon_path):
            print(f"⚠️ Fichier icône introuvable: {icon_path}")
            return None
            
        # Charger l'image
        image = Image.open(icon_path)
        if isinstance(size, int):
            size = (size, size)
        
        # Redimensionner avec anti-aliasing
        image = image.resize(size, Image.Resampling.LANCZOS)
        
        # Créer l'image CTk avec gestion des couleurs
        return ctk.CTkImage(light_image=image, dark_image=image, size=size)
        
    except Exception as e:
        print(f"⚠️ Erreur chargement icône {icon_path}: {e}")
        return None

def get_icon_with_fallback(icons_dict, icon_key, size=(20, 20)):
    """Récupère une icône PNG uniquement, sans fallback emoji"""
    icon_path = icons_dict.get(icon_key)
    if icon_path:
        icon = load_icon(icon_path, size)
        if icon:
            return icon
    
    # Pas de fallback emoji - retourner None si l'icône n'existe pas
    print(f"⚠️ Icône '{icon_key}' non trouvée dans le dictionnaire")
    return None

class CoursManagerView(ctk.CTkFrame):
    """Vue unifiée simplifiée pour la gestion des cours"""
    
    def __init__(self, parent, icons):
        super().__init__(parent, fg_color="transparent")
        
        print("🚀 Initialisation CoursManagerView...")
        
        # S'assurer que toutes les icônes nécessaires sont présentes
        self.icons = icons
        self._ensure_required_icons()
        
        print("✅ Icônes configurées")
        
        self.current_mode = "enseignements"  # Mode par défaut
        
        # Variables
        self.search_var = ctk.StringVar()
        self.mode_var = ctk.StringVar(value="Enseignements")
        
        # Variables de pagination
        self.current_page = 1
        self.courses_per_page = 8  # 2 lignes de 4 cartes chacune
        self.total_courses = 0
        self.total_pages = 0
        self.all_courses_data = []  # Stockage de toutes les données
        
        # Cache pour optimiser les performances
        self._cached_data = None
        self._last_refresh_time = 0
        self._refresh_throttle = 0.5  # 500ms de throttling
        
        print("🚀 Initialisation du gestionnaire de minuteurs...")
        # Gestionnaire de minuteurs avec notifications
        self.timer_manager = timer_manager
        if not hasattr(timer_manager, 'notification_manager') or timer_manager.notification_manager is None:
            timer_manager.notification_manager = timer_manager.notification_manager = NotificationManager(self)
        
        # Fenêtre d'historique des cours terminés + compteur badge
        self.history_window = CourseHistoryWindow(self, timer_manager.history_manager)
        self._completed_count = len(self.timer_manager.history_manager.get_completed_courses())
        # S'abonner aux fins de cours pour incrémenter le badge
        try:
            self.timer_manager.add_listener(self._on_course_completed)
        except Exception as e:
            print(f"⚠️ Impossible d'abonner le listener fin de cours: {e}")
        
        print("✅ Gestionnaire de minuteurs initialisé")
        
        print("🚀 Configuration de l'interface...")
        self.setup_ui()
        self.refresh_view()
        
        print("✅ CoursManagerView initialisée")
    
    def destroy(self):
        """Nettoie les ressources lors de la destruction de la vue"""
        # Nettoyer tous les minuteurs actifs
        if hasattr(self, 'timer_manager'):
            self.timer_manager.cleanup_all()
        super().destroy()
    
    def _ensure_required_icons(self):
        """S'assure que toutes les icônes nécessaires sont présentes dans le dictionnaire"""
        required_icons = {
            "book": "resources/icons/book.png",
            "person": "resources/icons/person.png", 
            "class": "resources/icons/class.png",
            "door": "resources/icons/door.png",
            "calendar": "resources/icons/calendar.png",
            "edit": "resources/icons/edit.png",
            "delete": "resources/icons/delete.png",
            "add": "resources/icons/add.png",
            "search": "resources/icons/search.png",
            "clock": "resources/icons/clock.png",
            "check": "resources/icons/check.png",
            "close": "resources/icons/close.png",
            "bell": "resources/icons/bell.png"
        }
        
        # Ajouter les icônes manquantes
        for key, path in required_icons.items():
            if key not in self.icons:
                self.icons[key] = path
                print(f"✅ Icône '{key}' ajoutée au dictionnaire: {path}")
    
    def setup_ui(self):
        """Configure l'interface utilisateurs"""
        # Container principal
        main_container = ctk.CTkFrame(self, fg_color=BG_CARD, corner_radius=20, border_width=2, border_color=BORDER_COLOR)
        main_container.pack(fill="both", expand=True, padx=3, pady=3)
        
        # Header avec titre et contrôles
        self.create_header(main_container)
        
        # Table unifiée avec pagination
        self.create_unified_table(main_container)
        
        # Contrôles de pagination
        self.create_pagination_controls(main_container)
    
    def create_header(self, parent):
        """Crée l'en-tête avec titre et contrôles"""
        header_frame = ctk.CTkFrame(parent, fg_color="transparent")
        header_frame.pack(fill="x", padx=15, pady=15)
        
        # Section gauche - Titre
        left_section = ctk.CTkFrame(header_frame, fg_color="transparent")
        left_section.pack(side="left", fill="y")
        
        # Logo et titre
        logo_icon = load_icon(self.icons.get("class"), 24)
        if logo_icon:
            logo_label = ctk.CTkLabel(left_section, image=logo_icon, text="")
            logo_label.pack(side="left", padx=(0, 10))
        
        title_label = ctk.CTkLabel(
            left_section,
            text="Gestion des Cours",
            font=("Segoe UI", 20, "bold"),
            text_color=TEXT_PRIMARY,
            fg_color="transparent"
        )
        title_label.pack(side="left")
        
        # Section droite - Contrôles
        right_section = ctk.CTkFrame(header_frame, fg_color="transparent")
        right_section.pack(side="right", fill="y")
        
        # Bouton d'ajout
        add_icon = load_icon(self.icons.get("add"), 16)
        add_btn = ctk.CTkButton(
            right_section,
            text="Ajouter",
            image=add_icon,
            fg_color="transparent",
            text_color=TEXT_PRIMARY,
            hover_color=HOVER_SUCCESS,
            command=self.add_cours,
            corner_radius=10,
            height=40,
            width=100,
            border_width=2,
            border_color=BORDER_COLOR,
            font=("Segoe UI", 12, "bold")
        )
        add_btn.pack(side="right", padx=(10, 0))
        
        # Bouton notifications style "sans fond" avec badge incrémental
        self._notif_btn_container = ctk.CTkFrame(right_section, fg_color="transparent")
        self._notif_btn_container.pack(side="right", padx=(10, 0))

        bell_icon = load_icon(self.icons.get("bell"), 18)
        self._notif_btn = ctk.CTkButton(
            self._notif_btn_container,
            text="",
            image=bell_icon,
            fg_color="transparent",
            text_color=TEXT_PRIMARY,
            hover_color=BG_CARD_HOVER,
            command=self.show_course_history,
            corner_radius=10,
            height=40,
            width=40,
            border_width=2,
            border_color=BORDER_COLOR
        )
        self._notif_btn.pack(side="left")

        # Badge
        self._badge_frame = ctk.CTkFrame(self._notif_btn_container, fg_color=TEXT_ACCENT, corner_radius=12)
        self._badge_label = ctk.CTkLabel(self._badge_frame, text=str(self._completed_count), font=("Segoe UI", 10, "bold"), text_color=WHITE)
        self._badge_label.pack(padx=6, pady=2)
        # positionner badge en haut à droite du bouton
        self._badge_frame.place(in_=self._notif_btn, relx=1, rely=0, x=-6, y=-6, anchor="ne")
        # Masquer si 0
        if (self._completed_count or 0) <= 0:
            try:
                self._badge_frame.place_forget()
            except Exception:
                pass
        
        # Champ de recherche
        search_frame = ctk.CTkFrame(right_section, fg_color=BG_CARD_HOVER, corner_radius=15, border_width=1, border_color=BORDER_COLOR)
        search_frame.pack(side="right", padx=(0, 10))
        
        search_inner = ctk.CTkFrame(search_frame, fg_color="transparent")
        search_inner.pack(fill="both", expand=True, padx=12, pady=8)
        
        self.search_entry = ctk.CTkEntry(
            search_inner,
            placeholder_text="Rechercher...",
            textvariable=self.search_var,
            font=("Segoe UI", 12),
            fg_color=BG_CARD,
            text_color=TEXT_PRIMARY,
            border_color=BORDER_COLOR,
            corner_radius=10,
            height=40,
            width=200
        )
        self.search_entry.pack(side="left", padx=(0, 8))
        self.search_entry.bind("<KeyRelease>", self.filter_view)
        
        # Bouton de recherche
        search_icon = load_icon(self.icons.get("search"), 16)
        search_btn = ctk.CTkButton(
            search_inner,
            text="",
            image=search_icon,
            fg_color="transparent",
            text_color=TEXT_PRIMARY,
            hover_color=HOVER_SUCCESS,
            command=self.refresh_view,
            corner_radius=10,
            height=40,
            width=40,
            border_width=2,
            border_color=BORDER_COLOR
        )
        search_btn.pack(side="right")
    
    def create_unified_table(self, parent):
        """Crée la vue avec des cartes au lieu d'un tableau"""
        # Frame pour les cartes
        self.cards_frame = ctk.CTkFrame(parent, fg_color="transparent")
        self.cards_frame.pack(fill="both", expand=True, padx=15, pady=(0, 15))
        
        # Configuration de la grille pour 4 cartes par ligne (2 lignes = 8 cours)
        self.cards_frame.grid_columnconfigure((0, 1, 2, 3), weight=1)
        
        # Liste pour stocker les cartes
        self.cards = []
        
        # Initialiser l'affichage
        self.refresh_view()
    
    def create_pagination_controls(self, parent):
        """Crée les contrôles de pagination"""
        self.pagination_frame = ctk.CTkFrame(parent, fg_color="transparent")
        self.pagination_frame.pack(fill="x", padx=15, pady=(0, 15))
        
        # Section gauche - Informations de pagination
        info_frame = ctk.CTkFrame(self.pagination_frame, fg_color="transparent")
        info_frame.pack(side="left", fill="y")
        
        self.pagination_info_label = ctk.CTkLabel(
            info_frame,
            text="Page 1 sur 1",
            font=("Segoe UI", 12),
            text_color=TEXT_SECONDARY,
            fg_color="transparent"
        )
        self.pagination_info_label.pack(side="left")
        
        # Section droite - Boutons de navigation
        nav_frame = ctk.CTkFrame(self.pagination_frame, fg_color="transparent")
        nav_frame.pack(side="right", fill="y")
        
        # Bouton Précédent
        self.prev_btn = ctk.CTkButton(
            nav_frame,
            text="◀ Précédent",
            fg_color="transparent",
            text_color=TEXT_PRIMARY,
            hover_color=BG_CARD_HOVER,
            command=self.go_to_previous_page,
            corner_radius=10,
            height=35,
            width=100,
            border_width=2,
            border_color=BORDER_COLOR,
            font=("Segoe UI", 11, "bold")
        )
        self.prev_btn.pack(side="left", padx=(0, 10))
        
        # Indicateur de page actuelle
        self.page_indicator = ctk.CTkLabel(
            nav_frame,
            text="1",
            font=("Segoe UI", 12, "bold"),
            text_color=TEXT_ACCENT,
            fg_color=BG_CARD,
            corner_radius=15,
            width=30,
            height=30
        )
        self.page_indicator.pack(side="left", padx=(0, 10))
        
        # Bouton Suivant
        self.next_btn = ctk.CTkButton(
            nav_frame,
            text="Suivant ▶",
            fg_color="transparent",
            text_color=TEXT_PRIMARY,
            hover_color=BG_CARD_HOVER,
            command=self.go_to_next_page,
            corner_radius=10,
            height=35,
            width=100,
            border_width=2,
            border_color=BORDER_COLOR,
            font=("Segoe UI", 11, "bold")
        )
        self.next_btn.pack(side="left")
    
    def refresh_view(self):
        """Actualise la vue avec des cartes de manière optimisée"""
        try:
            # Nettoyage des anciens minuteurs
            self.timer_manager.cleanup_all()
            
            # Nettoyage des anciennes cartes
            for card in self.cards:
                card.destroy()
            self.cards.clear()
            
            # Chargement direct des données
            self._load_courses_async()
                    
        except Exception as e:
            print(f"❌ Erreur refresh_view: {e}")
            messagebox.showerror("Erreur", f"Erreur lors du chargement des données: {e}")
    
    def go_to_previous_page(self):
        """Va à la page précédente"""
        if self.current_page > 1:
            self.current_page -= 1
            self._display_current_page()
    
    def go_to_next_page(self):
        """Va à la page suivante"""
        if self.current_page < self.total_pages:
            self.current_page += 1
            self._display_current_page()
    
    def _display_current_page(self):
        """Affiche la page actuelle"""
        try:
            # Nettoyage des anciennes cartes
            for card in self.cards:
                card.destroy()
            self.cards.clear()
            
            # Calculer les indices de début et fin pour la page actuelle
            start_index = (self.current_page - 1) * self.courses_per_page
            end_index = start_index + self.courses_per_page
            
            # Récupérer les cours de la page actuelle
            courses_to_display = self.all_courses_data[start_index:end_index]
            
            # Créer les cartes pour cette page
            for i, item in enumerate(courses_to_display):
                card = self.create_course_card(item, i)
                self.cards.append(card)
            
            # Mettre à jour les contrôles de pagination
            self._update_pagination_controls()
            
            print(f"✅ Page {self.current_page}/{self.total_pages} affichée ({len(courses_to_display)} cours)")
                    
        except Exception as e:
            print(f"❌ Erreur _display_current_page: {e}")
    
    def _update_pagination_controls(self):
        """Met à jour les contrôles de pagination"""
        try:
            # Mettre à jour les informations de pagination
            self.pagination_info_label.configure(
                text=f"Page {self.current_page} sur {self.total_pages} ({self.total_courses} cours au total)"
            )
            
            # Mettre à jour l'indicateur de page
            self.page_indicator.configure(text=str(self.current_page))
            
            # Activer/désactiver les boutons selon la page actuelle
            self.prev_btn.configure(state="normal" if self.current_page > 1 else "disabled")
            self.next_btn.configure(state="normal" if self.current_page < self.total_pages else "disabled")
            
        except Exception as e:
            print(f"⚠️ Erreur _update_pagination_controls: {e}")
    
    
    def _load_courses_async(self):
        """Charge les cours de manière asynchrone avec pagination"""
        try:
            # Récupération de tous les cours
            print("🔄 Chargement des cours...")
            all_data = get_all_cours()
            
            # Stocker toutes les données
            self.all_courses_data = all_data if all_data else []
            self.total_courses = len(self.all_courses_data)
            
            # Calculer le nombre total de pages
            self.total_pages = max(1, (self.total_courses + self.courses_per_page - 1) // self.courses_per_page)
            
            # Réinitialiser à la page 1
            self.current_page = 1
            
            # Supprimer l'indicateur de chargement s'il existe
            if hasattr(self, 'loading_frame'):
                self.loading_frame.destroy()
            
            # Afficher la première page
            self._display_current_page()
            
            print(f"✅ {self.total_courses} cours chargés en {self.total_pages} pages")
                    
        except Exception as e:
            print(f"❌ Erreur _load_courses_async: {e}")
            # Supprimer l'indicateur de chargement s'il existe
            if hasattr(self, 'loading_frame'):
                self.loading_frame.destroy()
    
    def show_course_history(self):
        """Affiche l'historique des cours terminés"""
        self.history_window.show_history()

    def _on_course_completed(self, course_data):
        """Incrémente le badge quand un cours se termine."""
        try:
            self._completed_count = len(self.timer_manager.history_manager.get_completed_courses())
            if hasattr(self, "_badge_label"):
                self._badge_label.configure(text=str(self._completed_count))
                # Afficher/Masquer
                if (self._completed_count or 0) > 0:
                    try:
                        self._badge_frame.place(in_=self._notif_btn, relx=1, rely=0, x=-6, y=-6, anchor="ne")
                    except Exception:
                        pass
                else:
                    try:
                        self._badge_frame.place_forget()
                    except Exception:
                        pass
        except Exception as e:
            print(f"⚠️ Erreur mise à jour badge: {e}")
    
    def _parse_course_time(self, time_str):
        """Parse une heure au format HH:MM"""
        try:
            hour, minute = map(int, time_str.split(':'))
            today = datetime.now().date()
            return datetime.combine(today, datetime.min.time().replace(hour=hour, minute=minute))
        except:
            return datetime.now().replace(hour=8, minute=0, second=0, microsecond=0)
    
    def create_course_card(self, item, index):
        """Crée une carte pour un cours"""
        # Calculer la position dans la grille (4 colonnes pour 8 cours par page)
        row = index // 4
        col = index % 4
        
        # Créer la carte optimisée pour 4 colonnes
        card = ctk.CTkFrame(
            self.cards_frame,
            fg_color=BG_CARD,
            corner_radius=12,
            border_width=1,
            border_color=BORDER_COLOR,
            height=200
        )
        card.grid(row=row, column=col, padx=8, pady=8, sticky="ew")
        
        # Header de la carte avec icône et titre
        header_frame = ctk.CTkFrame(card, fg_color="transparent")
        header_frame.pack(fill="x", padx=15, pady=(15, 10))
        
        # Icône du cours PNG uniquement
        course_icon_result = get_icon_with_fallback(self.icons, "book", 24)
        if course_icon_result:
            icon_label = ctk.CTkLabel(
                header_frame, 
                image=course_icon_result, 
                text="",
                fg_color="transparent"
            )
            icon_label.pack(side="left", padx=(0, 10))
        
        # Titre du cours (sans ID)
        title_text = f"Cours"
        title_label = ctk.CTkLabel(
            header_frame,
            text=title_text,
            font=("Segoe UI", 14, "bold"),
            text_color=TEXT_PRIMARY,
            fg_color="transparent"
        )
        title_label.pack(side="left")
        
        # Badge de statut
        statut = item.get("statut", "Actif")
        statut_color = SUCCESS_GREEN if statut == "Actif" else WARNING_ORANGE
        statut_badge = ctk.CTkLabel(
            header_frame,
            text=statut,
            font=("Segoe UI", 10, "bold"),
            text_color=WHITE,
            fg_color=statut_color,
            corner_radius=10,
            width=60,
            height=25
        )
        statut_badge.pack(side="right")
        
        # Contenu principal vertical
        content_frame = ctk.CTkFrame(card, fg_color="transparent")
        content_frame.pack(fill="both", expand=True, padx=15, pady=(0, 15))
        
        # Informations du cours organisées verticalement
        info_items = [
            ("person", "Professeur", item.get("professeur_nom", "Inconnu")),
            ("class", "Classe", item.get("classe_nom", "Inconnue")),
            ("book", "Matière", item.get("matiere_nom", "Inconnue")),
            ("door", "Salle", item.get("salle_nom", "Non spécifiée")),
        ]
        
        # Affichage vertical de toutes les informations
        for icon_key, label, value in info_items:
            info_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
            info_frame.pack(fill="x", pady=2)
            
            # Icône spécifique PNG uniquement
            icon_result = get_icon_with_fallback(self.icons, icon_key, 16)
            if icon_result:
                icon_label = ctk.CTkLabel(
                    info_frame, 
                    image=icon_result, 
                    text="",
                    fg_color="transparent"
                )
                icon_label.pack(side="left", padx=(0, 8))
            
            # Label et valeur
            label_text = f"{label}:"
            label_widget = ctk.CTkLabel(
                info_frame,
                text=label_text,
                font=("Segoe UI", 9, "bold"),
                text_color=TEXT_SECONDARY,
                fg_color="transparent",
                anchor="w"
            )
            label_widget.pack(side="left", padx=(0, 4))
            
            value_widget = ctk.CTkLabel(
                info_frame,
                text=value,
                font=("Segoe UI", 10),
                text_color=TEXT_PRIMARY,
                fg_color="transparent",
                anchor="w"
            )
            value_widget.pack(side="left")
        
        # Footer avec horaire et actions - marges optimisées
        footer_frame = ctk.CTkFrame(card, fg_color="transparent")
        footer_frame.pack(fill="x", padx=15, pady=(0, 15))
        
        # Section minuteur dynamique - AMÉLIORÉE
        timer_section = ctk.CTkFrame(footer_frame, fg_color="transparent")
        timer_section.pack(side="left", fill="x", expand=True)
        
        # Créer le minuteur pour ce cours avec un design amélioré
        course_id = item.get('id', index)
        timer_widget = self.timer_manager.add_timer(course_id, timer_section, item)
        
        # Badge de statut du cours (plus visible)
        status_badge_frame = ctk.CTkFrame(timer_section, fg_color="transparent")
        status_badge_frame.pack(fill="x", pady=(5, 0))
        
        # Déterminer le statut et la couleur
        current_time = datetime.now()
        start_time = self._parse_course_time(item.get('heure', '08:00'))
        end_time = start_time + timedelta(minutes=item.get('duree', 60))
        
        if current_time < start_time:
            status_text = "⏳ En attente"
            status_color = "#3FB950"  # Vert
        elif current_time < end_time:
            status_text = "▶️ En cours"
            status_color = "#00D4FF"  # Bleu
        else:
            status_text = "✅ Terminé"
            status_color = "#F85149"  # Rouge
        
        status_badge = ctk.CTkLabel(
            status_badge_frame,
            text=status_text,
            font=("Segoe UI", 10, "bold"),
            text_color=status_color,
            fg_color="transparent"
        )
        status_badge.pack(side="left")
        
        # Informations horaires statiques (en dessous du minuteur)
        horaire_info_frame = ctk.CTkFrame(timer_section, fg_color="transparent")
        horaire_info_frame.pack(fill="x", pady=(5, 0))
        
        # Icône calendrier PNG uniquement
        calendar_icon_result = get_icon_with_fallback(self.icons, "calendar", 16)
        if calendar_icon_result:
            calendar_label = ctk.CTkLabel(
                horaire_info_frame, 
                image=calendar_icon_result, 
                text="",
                fg_color="transparent"
            )
            calendar_label.pack(side="left", padx=(0, 6))
        
        # Texte combiné pour jour, heure et durée
        horaire_text = f"{item.get('jour', 'Non spécifié')} {item.get('heure', '')} - {item.get('duree', 60)} min"
        horaire_label = ctk.CTkLabel(
            horaire_info_frame,
            text=horaire_text,
            font=("Segoe UI", 9),
            text_color=TEXT_SECONDARY,
            fg_color="transparent"
        )
        horaire_label.pack(side="left")
        
        # Boutons d'action
        actions_frame = ctk.CTkFrame(footer_frame, fg_color="transparent")
        actions_frame.pack(side="right")
        
        # Bouton modifier PNG uniquement
        edit_icon_result = get_icon_with_fallback(self.icons, "edit", 18)
        if edit_icon_result:
            edit_btn = ctk.CTkButton(
                actions_frame,
                text="",
                image=edit_icon_result,
                fg_color="transparent",
                text_color=TEXT_PRIMARY,
                hover_color=HOVER_SUCCESS,
                command=lambda: self.edit_cours(item.get('id')),
                corner_radius=8,
                height=36,
                width=36,
                border_width=2,
                border_color=BORDER_COLOR
            )
            edit_btn.pack(side="left", padx=(0, 8))
        
        # Bouton supprimer PNG uniquement
        delete_icon_result = get_icon_with_fallback(self.icons, "delete", 18)
        if delete_icon_result:
            delete_btn = ctk.CTkButton(
                actions_frame,
                text="",
                image=delete_icon_result,
                fg_color="transparent",
                text_color=TEXT_PRIMARY,
                hover_color=ERROR_RED,
                command=lambda: self.delete_cours(item.get('id')),
                corner_radius=8,
                height=36,
                width=36,
                border_width=2,
                border_color=BORDER_COLOR
            )
            delete_btn.pack(side="left")
        
        return card
    
    def edit_cours(self, cours_id):
        """Modifie un cours"""
        try:
            # Récupérer les données du cours
            cours_data = get_cours_by_id(cours_id)
            if cours_data:
                # Ouvrir le formulaire de modification
                form = CoursForm(self, "Modifier", cours_data)
                form.wait_window()
                self.refresh_view()
            else:
                messagebox.showerror("Erreur", "Cours introuvable")
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de la récupération du cours: {e}")
    
    def delete_cours(self, cours_id):
        """Supprime un cours"""
        if messagebox.askyesno("Confirmation", f"Supprimer le cours ID: {cours_id}?"):
            try:
                delete_cours(cours_id)
                self.refresh_view()
                messagebox.showinfo("Succès", "Cours supprimé avec succès")
            except Exception as e:
                messagebox.showerror("Erreur", f"Erreur lors de la suppression: {e}")
    
    def filter_view(self, event=None):
        """Filtre la vue selon le terme de recherche avec pagination"""
        search_term = self.search_var.get().lower()
        
        if not search_term:
            # Si pas de recherche, afficher tous les cours
            self.all_courses_data = get_all_cours() if get_all_cours() else []
        else:
            # Filtrer les cours selon le terme de recherche
            all_courses = get_all_cours() if get_all_cours() else []
            filtered_courses = []
            
            for course in all_courses:
                # Créer une chaîne de recherche à partir des données du cours
                search_text = f"{course.get('professeur_nom', '')} {course.get('classe_nom', '')} {course.get('matiere_nom', '')} {course.get('salle_nom', '')} {course.get('jour', '')}".lower()
                
                if search_term in search_text:
                    filtered_courses.append(course)
            
            self.all_courses_data = filtered_courses
        
        # Recalculer la pagination
        self.total_courses = len(self.all_courses_data)
        self.total_pages = max(1, (self.total_courses + self.courses_per_page - 1) // self.courses_per_page)
        self.current_page = 1
        
        # Afficher la première page des résultats filtrés
        self._display_current_page()
        
        print(f"🔍 Recherche '{search_term}': {self.total_courses} cours trouvés en {self.total_pages} pages")
    
    def open_add_modal(self):
        """Ouvre le formulaire d'ajout de cours avec design similaire aux salles"""
        form = CoursForm(self, "Ajouter")
        form.wait_window()
        self.refresh_view()
    
    def add_cours(self):
        """Ajoute un nouveau cours"""
        self.open_add_modal()

class CoursForm(ctk.CTkToplevel):
    """Fenêtre modale pour ajouter ou modifier un cours avec design moderne."""
    def __init__(self, parent, mode, data=None):
        super().__init__(parent)
        self.parent = parent
        self.mode = mode
        self.data = data

        self.title(f"{mode} un Cours")
        self.geometry("700x750")
        self.transient(parent)
        self.grab_set()
        self.configure(fg_color=BG_MAIN)

        self.update_idletasks()
        x = parent.winfo_rootx() + (parent.winfo_width() - self.winfo_width()) // 2
        y = parent.winfo_rooty() + (parent.winfo_height() - self.winfo_height()) // 2
        self.geometry(f"+{x}+{y}")

        self._create_widgets()

    def _create_widgets(self):
        """Crée les widgets du formulaire avec design moderne."""
        # Container principal avec design moderne
        form_frame = ctk.CTkFrame(self, fg_color=BG_CARD, corner_radius=20, 
                                 border_color=BORDER_COLOR, border_width=1)
        form_frame.pack(fill="both", expand=True, padx=25, pady=25)

        # En-tête du formulaire
        header_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        header_frame.pack(fill="x", padx=25, pady=(25, 15))

        # Icône du formulaire
        try:
            if self.mode == "Ajouter":
                icon_name = "add.png"
            else:
                icon_name = "edit.png"
            icon_path = os.path.join(os.path.dirname(__file__), '..', '..', '..', '..', '..', 'resources', 'icons', icon_name)
            form_icon = ctk.CTkImage(Image.open(icon_path), size=(32, 32))
            icon_label = ctk.CTkLabel(header_frame, text="", image=form_icon)
            icon_label.pack(side="left", padx=(0, 10))
        except FileNotFoundError:
            print(f"Icône '{icon_name}' non trouvée.")

        # Titre du formulaire
        title_label = ctk.CTkLabel(header_frame, text=f"{self.mode} un Cours", 
                                  font=("Segoe UI", 20, "bold"), text_color=TEXT_ACCENT)
        title_label.pack(side="left")

        # Sous-titre
        subtitle_label = ctk.CTkLabel(header_frame, text="Remplissez les informations ci-dessous", 
                                     font=("Segoe UI", 12), text_color=TEXT_SECONDARY)
        subtitle_label.pack(side="left", padx=(10, 0))

        # Scrollable frame pour le formulaire
        scrollable_frame = ctk.CTkScrollableFrame(form_frame, fg_color="transparent")
        scrollable_frame.pack(fill="both", expand=True, padx=25, pady=15)

        # Champs du formulaire avec design amélioré
        fields_frame = ctk.CTkFrame(scrollable_frame, fg_color="transparent")
        fields_frame.pack(fill="x")

        # Professeur
        prof_label = ctk.CTkLabel(fields_frame, text="Professeur", 
                                font=("Segoe UI", 14, "bold"), text_color=TEXT_PRIMARY)
        prof_label.pack(anchor="w", pady=(0, 5))
        
        self.prof_var = ctk.StringVar()
        try:
            profs = get_all_professeurs()
            prof_names = [f"{p.get('nom', '')} {p.get('prenom', '')}" for p in profs]
            self.profs_data = profs
            print(f"✅ {len(profs)} professeurs chargés")
        except Exception as e:
            print(f"⚠️ Erreur chargement professeurs: {e}")
            prof_names = ["Professeur 1", "Professeur 2", "Professeur 3"]
            self.profs_data = []
        
        self.prof_combo = ctk.CTkComboBox(fields_frame, values=prof_names, variable=self.prof_var,
                                        font=("Segoe UI", 12), height=45, corner_radius=10,
                                        fg_color=BG_CARD, border_color=BORDER_COLOR,
                                        button_color=TEXT_ACCENT, button_hover_color=HOVER_SUCCESS,
                                        dropdown_hover_color=BG_CARD_HOVER)
        self.prof_combo.pack(fill="x", pady=(0, 15))

        # Classe
        classe_label = ctk.CTkLabel(fields_frame, text="Classe", 
                                  font=("Segoe UI", 14, "bold"), text_color=TEXT_PRIMARY)
        classe_label.pack(anchor="w", pady=(0, 5))
        
        self.classe_var = ctk.StringVar()
        try:
            classes = get_all_classes()
            classe_names = [c.get('nom_classe', '') for c in classes]
            self.classes_data = classes
            print(f"✅ {len(classes)} classes chargées")
        except Exception as e:
            print(f"⚠️ Erreur chargement classes: {e}")
            classe_names = ["6ème", "5ème", "4ème", "3ème", "2nde", "1ère", "Terminale"]
            self.classes_data = []
        
        self.classe_combo = ctk.CTkComboBox(fields_frame, values=classe_names, variable=self.classe_var,
                                          font=("Segoe UI", 12), height=45, corner_radius=10,
                                          fg_color=BG_CARD, border_color=BORDER_COLOR,
                                          button_color=TEXT_ACCENT, button_hover_color=HOVER_SUCCESS,
                                          dropdown_hover_color=BG_CARD_HOVER)
        self.classe_combo.pack(fill="x", pady=(0, 15))

        # Matière
        matiere_label = ctk.CTkLabel(fields_frame, text="Matière", 
                                   font=("Segoe UI", 14, "bold"), text_color=TEXT_PRIMARY)
        matiere_label.pack(anchor="w", pady=(0, 5))
        
        self.matiere_var = ctk.StringVar()
        try:
            matieres = get_all_matieres()
            matiere_names = [m.get('nom_matiere', '') for m in matieres]
            self.matieres_data = matieres
            print(f"✅ {len(matieres)} matières chargées")
        except Exception as e:
            print(f"⚠️ Erreur chargement matières: {e}")
            matiere_names = ["Mathématiques", "Français", "Anglais", "Histoire", "Sciences"]
            self.matieres_data = []
        
        self.matiere_combo = ctk.CTkComboBox(fields_frame, values=matiere_names, variable=self.matiere_var,
                                           font=("Segoe UI", 12), height=45, corner_radius=10,
                                           fg_color=BG_CARD, border_color=BORDER_COLOR,
                                           button_color=TEXT_ACCENT, button_hover_color=HOVER_SUCCESS,
                                           dropdown_hover_color=BG_CARD_HOVER)
        self.matiere_combo.pack(fill="x", pady=(0, 15))

        # Salle
        salle_label = ctk.CTkLabel(fields_frame, text="Salle", 
                                 font=("Segoe UI", 14, "bold"), text_color=TEXT_PRIMARY)
        salle_label.pack(anchor="w", pady=(0, 5))
        
        self.salle_var = ctk.StringVar()
        try:
            salles = get_all_salles()
            salle_names = [s.get('nom_salle', '') for s in salles]
            self.salles_data = salles
            print(f"✅ {len(salles)} salles chargées")
        except Exception as e:
            print(f"⚠️ Erreur chargement salles: {e}")
            salle_names = ["Salle 101", "Salle 102", "Salle 103", "Salle 201", "Salle 202"]
            self.salles_data = []
        
        self.salle_combo = ctk.CTkComboBox(fields_frame, values=salle_names, variable=self.salle_var,
                                         font=("Segoe UI", 12), height=45, corner_radius=10,
                                         fg_color=BG_CARD, border_color=BORDER_COLOR,
                                         button_color=TEXT_ACCENT, button_hover_color=HOVER_SUCCESS,
                                         dropdown_hover_color=BG_CARD_HOVER)
        self.salle_combo.pack(fill="x", pady=(0, 15))

        # Jour
        jour_label = ctk.CTkLabel(fields_frame, text="Jour", 
                                font=("Segoe UI", 14, "bold"), text_color=TEXT_PRIMARY)
        jour_label.pack(anchor="w", pady=(0, 5))
        
        self.jour_var = ctk.StringVar(value="Lundi")
        jour_options = ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi"]
        self.jour_combo = ctk.CTkComboBox(fields_frame, values=jour_options, variable=self.jour_var,
                                        font=("Segoe UI", 12), height=45, corner_radius=10,
                                        fg_color=BG_CARD, border_color=BORDER_COLOR,
                                        button_color=TEXT_ACCENT, button_hover_color=HOVER_SUCCESS,
                                        dropdown_hover_color=BG_CARD_HOVER)
        self.jour_combo.pack(fill="x", pady=(0, 15))

        # Heure
        heure_label = ctk.CTkLabel(fields_frame, text="Heure", 
                                 font=("Segoe UI", 14, "bold"), text_color=TEXT_PRIMARY)
        heure_label.pack(anchor="w", pady=(0, 5))
        
        self.heure_var = ctk.StringVar(value="08:00")
        self.heure_entry = ctk.CTkEntry(fields_frame, textvariable=self.heure_var,
                                       placeholder_text="HH:MM", font=("Segoe UI", 12), 
                                       height=45, corner_radius=10,
                                       fg_color=BG_CARD, border_color=BORDER_COLOR)
        self.heure_entry.pack(fill="x", pady=(0, 15))

        # Durée
        duree_label = ctk.CTkLabel(fields_frame, text="Durée (minutes)", 
                                 font=("Segoe UI", 14, "bold"), text_color=TEXT_PRIMARY)
        duree_label.pack(anchor="w", pady=(0, 5))
        
        self.duree_var = ctk.StringVar(value="60")
        self.duree_entry = ctk.CTkEntry(fields_frame, textvariable=self.duree_var,
                                       placeholder_text="60", font=("Segoe UI", 12), 
                                       height=45, corner_radius=10,
                                       fg_color=BG_CARD, border_color=BORDER_COLOR)
        self.duree_entry.pack(fill="x", pady=(0, 25))

        # Pré-remplir les champs en mode modification
        if self.mode == "Modifier" and self.data:
            self._populate_fields()

        # Boutons d'action avec design moderne
        btn_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        btn_frame.pack(fill="x", padx=25, pady=(0, 25))

        # Bouton Enregistrer avec contour
        save_btn = ctk.CTkButton(btn_frame, text="Enregistrer", font=("Segoe UI", 12, "bold"),
                                command=self._save_data, fg_color=TEXT_ACCENT, 
                                hover_color=HOVER_SUCCESS, text_color=WHITE,
                                height=45, corner_radius=12, width=140,
                                border_color=BORDER_COLOR, border_width=2)
        save_btn.pack(side="left", padx=(0, 10))

        # Bouton Annuler avec contour
        cancel_btn = ctk.CTkButton(btn_frame, text="Annuler", font=("Segoe UI", 12, "bold"),
                                  command=self.destroy, fg_color=BG_CARD, 
                                  hover_color=BG_CARD_HOVER, text_color=TEXT_PRIMARY,
                                  height=45, corner_radius=12, width=140,
                                  border_color=BORDER_COLOR, border_width=2)
        cancel_btn.pack(side="left")

    def _populate_fields(self):
        """Pré-remplit les champs avec les données du cours en mode modification"""
        try:
            if not self.data:
                return
                
            # Professeur
            if self.data.get('professeur_nom'):
                self.prof_var.set(self.data['professeur_nom'])
            
            # Classe
            if self.data.get('classe_nom'):
                self.classe_var.set(self.data['classe_nom'])
            
            # Matière
            if self.data.get('matiere_nom'):
                self.matiere_var.set(self.data['matiere_nom'])
            
            # Salle
            if self.data.get('salle_nom'):
                self.salle_var.set(self.data['salle_nom'])
            
            # Jour
            if self.data.get('jour'):
                self.jour_var.set(self.data['jour'])
            
            # Heure
            if self.data.get('heure'):
                self.heure_var.set(self.data['heure'])
            
            # Durée
            if self.data.get('duree'):
                self.duree_var.set(str(self.data['duree']))
                
            print(f"✅ Champs pré-remplis pour le cours ID: {self.data.get('id')}")
            
        except Exception as e:
            print(f"⚠️ Erreur pré-remplissage des champs: {e}")

    def _save_data(self):
        """Valide et enregistre les données du formulaire."""
        prof_name = self.prof_var.get()
        classe_name = self.classe_var.get()
        matiere_name = self.matiere_var.get()
        salle_name = self.salle_var.get()
        jour = self.jour_var.get()
        heure = self.heure_var.get()
        duree = self.duree_var.get()

        # Validation des champs obligatoires
        if not prof_name:
            messagebox.showerror("Erreur", "Veuillez sélectionner un professeurs")
            return
        if not classe_name:
            messagebox.showerror("Erreur", "Veuillez sélectionner une classes")
            return
        if not matiere_name:
            messagebox.showerror("Erreur", "Veuillez sélectionner une matière")
            return
        if not salle_name:
            messagebox.showerror("Erreur", "Veuillez sélectionner une salles")
            return
        if not jour:
            messagebox.showerror("Erreur", "Veuillez sélectionner un jour")
            return
        if not heure:
            messagebox.showerror("Erreur", "Veuillez saisir une heure")
            return
        
        # Récupération des IDs depuis les vraies données
        prof_id = None
        for prof in getattr(self, 'profs_data', []):
            if f"{prof.get('nom', '')} {prof.get('prenom', '')}" == prof_name:
                prof_id = prof.get('id_professeur')
                break
        
        classe_id = None
        for classes in getattr(self, 'classes_data', []):
            if classes.get('nom_classe', '') == classe_name:
                classe_id = classes.get('id_classe')
                break
        
        matiere_id = None
        for matieres in getattr(self, 'matieres_data', []):
            if matieres.get('nom_matiere', '') == matiere_name:
                matiere_id = matieres.get('id_matiere')
                break
        
        salle_id = None
        for salles in getattr(self, 'salles_data', []):
            if salles.get('nom_salle', '') == salle_name:
                salle_id = salles.get('id_salle')
                break
        
        # Utiliser des IDs par défaut si pas trouvés
        if not prof_id:
            prof_id = 1
            print(f"⚠️ Professeur '{prof_name}' non trouvé, utilisation ID par défaut: {prof_id}")
        if not classe_id:
            classe_id = 1
            print(f"⚠️ Classe '{classe_name}' non trouvée, utilisation ID par défaut: {classe_id}")
        if not matiere_id:
            matiere_id = 1
            print(f"⚠️ Matière '{matiere_name}' non trouvée, utilisation ID par défaut: {matiere_id}")
        if not salle_id:
            salle_id = 1
            print(f"⚠️ Salle '{salle_name}' non trouvée, utilisation ID par défaut: {salle_id}")
        
        # Conversion de la durée
        try:
            duree_int = int(duree or "60")
        except ValueError:
            duree_int = 60
        
        # Ajout ou modification du cours via le contrôleur cours
        try:
            from src.modules.academic.classes.controllers.cours_controller import add_cours, update_cours
            
            if self.mode == "Ajouter":
                # Ajout d'un nouveau cours
                if add_cours(
                    professeur_id=prof_id,
                    classe_id=classe_id,
                    matiere_id=matiere_id,
                    salle_id=salle_id,
                    jour=jour,
                    heure=heure,
                    duree=duree_int
                ):
                    messagebox.showinfo("Succès", "Cours ajouté avec succès!")
                    self.parent.refresh_view()
                    self.destroy()
                else:
                    messagebox.showerror("Erreur", "Erreur lors de l'ajout du cours")
            else:
                # Modification d'un cours existant
                if self.data and self.data.get('id'):
                    if update_cours(
                        id=self.data['id'],
                        professeur_id=prof_id,
                        classe_id=classe_id,
                        matiere_id=matiere_id,
                        salle_id=salle_id,
                        jour=jour,
                        heure=heure,
                        duree=duree_int,
                        statut="Actif"
                    ):
                        messagebox.showinfo("Succès", "Cours modifié avec succès!")
                        self.parent.refresh_view()
                        self.destroy()
                    else:
                        messagebox.showerror("Erreur", "Erreur lors de la modification du cours")
                else:
                    messagebox.showerror("Erreur", "Données du cours manquantes pour la modification")
                
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de la sauvegarde du cours: {e}")
            print(f"❌ Erreur save_cours: {e}")

# Classes de compatibilité pour les anciennes vues
class EnseignementsView(CoursManagerView):
    def __init__(self, parent, icons):
        super().__init__(parent, icons)
        self.current_mode = "enseignements"

class EmploisView(CoursManagerView):
    def __init__(self, parent, icons):
        super().__init__(parent, icons)
        self.current_mode = "emplois"

# Pour la compatibilité avec le registre des vues
if __name__ == "__main__":
    class MockApp(ctk.CTk):
        def __init__(self):
            super().__init__()
            self.geometry("1200x800")
            self.title("Gestion des Cours - Vue Unifiée")
            
            # Simuler un dictionnaire d'icônes complet
            mock_icons = {
                "add": "resources/icons/add.png",
                "edit": "resources/icons/edit.png",
                "delete": "resources/icons/delete.png",
                "search": "resources/icons/search.png",
                "class": "resources/icons/class.png",
                "person": "resources/icons/person.png",
                "book": "resources/icons/book.png",
                "door": "resources/icons/door.png",
                "calendar": "resources/icons/calendar.png",
                "clock": "resources/icons/clock.png",
                "assignment": "resources/icons/assignment.png",
                "classroom": "resources/icons/classroom.png",
                "view": "resources/icons/view.png",
                "print": "resources/icons/print.png",
                "upload": "resources/icons/upload.png",
                "download": "resources/icons/download.png",
                "menu": "resources/icons/menu.png",
                "close": "resources/icons/close.png",
                "envelope": "resources/icons/envelope.png",
                "phone": "resources/icons/phone.png",
                "email": "resources/icons/email.png",
                "folder": "resources/icons/folder.png",
                "file": "resources/icons/file.png",
                "csv": "resources/icons/csv.png",
                "star": "resources/icons/star.png",
                "award": "resources/icons/award.png",
                "target": "resources/icons/target.png",
                "trending_up": "resources/icons/trending_up.png",
                "analytics": "resources/icons/analytics.png",
                "newspaper": "resources/icons/newspaper.png",
                "megaphone": "resources/icons/megaphone.png",
                "protect": "resources/icons/protect.png",
                "wrench": "resources/icons/wrench.png",
                "stacks": "resources/icons/stacks.png",
                "filter": "resources/icons/filter.png",
                "sort": "resources/icons/sort.png",
                "detail": "resources/icons/detail.png",
                "cover": "resources/icons/cover.png",
                "chevron_right": "resources/icons/chevron_right.png",
                "check_circle": "resources/icons/check_circle.png",
                "autorenew": "resources/icons/autorenew.png",
                "briefcase": "resources/icons/briefcase.png",
                "user_avatar": "resources/icons/user_avatar.png",
                "logo": "resources/icons/logo.png",
                "bell": "resources/icons/bell.png",
            }
            
            view = CoursManagerView(self, mock_icons)
            view.pack(fill="both", expand=True)
        
        def run(self):
            self.mainloop()
    
    app = MockApp()
    app.run()
