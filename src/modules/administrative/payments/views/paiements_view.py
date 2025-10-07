import tkinter as tk
from tkinter import ttk, messagebox
import customtkinter as ctk
from datetime import datetime, timedelta
import os
import sys

# Ajouter le chemin du projet pour les imports
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../../..'))
src_root = os.path.join(project_root, 'Gestion_scolaire')
if project_root not in sys.path:
    sys.path.insert(0, project_root)
if src_root not in sys.path:
    sys.path.insert(0, src_root)

# Imports des contrôleurs
from src.modules.administrative.payments.controllers.paiement_controller import (
    get_all_paiements, add_paiement, update_paiement, delete_paiement, 
    create_table_paiements, insert_sample_payments
)
from src.modules.administrative.payments.controllers.enhanced_paiement_controller import (
    EnhancedPaiementController, get_all_paiements_enhanced
)
from src.modules.administrative.payments.controllers.database_schema import (
    create_all_payment_tables
)
from src.modules.academic.students.controllers.eleve_controller import get_all_eleves
from src.modules.academic.classes.controllers.classe_controller import get_all_classes

# Import du thème EduManager+ avec gestion d'erreur
try:
    from Gestion_scolaire.resources.themes.theme import (
    # Couleurs principales
    BG_MAIN, BG_SIDEBAR, CARD_BG, BORDER_COLOR, ACCENT, TEXT, MUTED,
    BG_CARD, BG_CARD_HOVER, BG_SECONDARY,
    TEXT_PRIMARY, TEXT_SECONDARY, TEXT_MUTED, TEXT_ACCENT,
    BORDER_LIGHT, BORDER_ACCENT,
    BTN_PRIMARY, BTN_SECONDARY, BTN_SUCCESS, BTN_WARNING, BTN_DANGER, BTN_INFO,
    STATE_SUCCESS, STATE_WARNING, STATE_ERROR, STATE_INFO,
    SUCCESS_GREEN, WARNING_YELLOW, WARNING_ORANGE, ERROR_RED, INFO_ORANGE,
    HOVER_PRIMARY, HOVER_SECONDARY, HOVER_SUCCESS, HOVER_WARNING, HOVER_ERROR, HOVER_INFO,
    # Couleurs EduManager+
    PRIMARY_BLUE, DARK_BLUE, DEEPER_BLUE, NAVY_BLUE, DARKER_BLUE,
    LIGHT_BLUE, ACCENT_BLUE, SOFT_BLUE, PALE_BLUE, MUTED_BLUE,
    DARK_GRAY, MEDIUM_GRAY, LIGHT_GRAY, WHITE, OFF_WHITE, PURE_WHITE,
    # Polices
    FONT, FONT_SIZE_TITLE, FONT_SIZE_HEADER, FONT_SIZE_SUB, FONT_SIZE_TXT, FONT_SIZE_TEXT, FONT_SIZE_SMALL,
    FONT_PRIMARY, FONT_SECONDARY, FONT_TITLE, FONT_SUBTITLE, FONT_SMALL, FONT_BUTTON, FONT_CARD_TITLE,
    # Espacements
    MARGIN_SMALL, MARGIN_MEDIUM, MARGIN_LARGE, MARGIN_CARD, MARGIN_SECTION,
    PADDING_SMALL, PADDING_MEDIUM, PADDING_LARGE, PADDING_CARD, PADDING_BUTTON,
    # Fonctions utilitaires
    apply_theme_to_app, get_font_config, get_spacing_config
)
except ImportError:
    # Fallback avec valeurs par défaut
    print("ATTENTION - Thème non trouvé, utilisation des valeurs par défaut")
    # Couleurs par défaut
    BG_MAIN = "#0A192F"
    BG_SIDEBAR = "#0E1C36"
    CARD_BG = "#0b1d34"
    BORDER_COLOR = "#1f3b5a"
    ACCENT = "#3B82F6"
    TEXT = "#E2E8F0"
    MUTED = "#8aa0b8"
    BG_CARD = "#0b1d34"
    BG_CARD_HOVER = "#1a2332"
    BG_SECONDARY = "#0E1C36"
    TEXT_PRIMARY = "#E2E8F0"
    TEXT_SECONDARY = "#8aa0b8"
    TEXT_MUTED = "#8aa0b8"
    TEXT_ACCENT = "#3B82F6"
    
    # Couleurs EduManager+
    PRIMARY_BLUE = "#0A192F"
    DARK_BLUE = "#0A192F"
    DEEPER_BLUE = "#0E1C36"
    NAVY_BLUE = "#0b1d34"
    DARKER_BLUE = "#1f3b5a"
    LIGHT_BLUE = "#64FFDA"
    ACCENT_BLUE = "#64FFDA"
    SOFT_BLUE = "#E2E8F0"
    PALE_BLUE = "#8aa0b8"
    MUTED_BLUE = "#8aa0b8"
    DARK_GRAY = "#1f3b5a"
    MEDIUM_GRAY = "#8aa0b8"
    LIGHT_GRAY = "#64FFDA"
    WHITE = "#E2E8F0"
    OFF_WHITE = "#8aa0b8"
    PURE_WHITE = "#FFFFFF"
    BORDER_LIGHT = "#666666"
    BORDER_ACCENT = "#3498db"
    BTN_PRIMARY = "#3498db"
    BTN_SECONDARY = "#95a5a6"
    BTN_SUCCESS = "#27ae60"
    BTN_WARNING = "#f39c12"
    BTN_DANGER = "#e74c3c"
    BTN_INFO = "#3498db"
    STATE_SUCCESS = "#27ae60"
    STATE_WARNING = "#f39c12"
    STATE_ERROR = "#e74c3c"
    STATE_INFO = "#3498db"
    SUCCESS_GREEN = "#27ae60"
    WARNING_YELLOW = "#f39c12"
    WARNING_ORANGE = "#e67e22"
    ERROR_RED = "#e74c3c"
    INFO_ORANGE = "#e67e22"
    HOVER_PRIMARY = "#2980b9"
    HOVER_SECONDARY = "#7f8c8d"
    HOVER_SUCCESS = "#229954"
    HOVER_WARNING = "#e67e22"
    HOVER_ERROR = "#c0392b"
    HOVER_INFO = "#2980b9"
    
    # Polices par défaut
    FONT = "Segoe UI"
    FONT_SIZE_TITLE = 24
    FONT_SIZE_HEADER = 20
    FONT_SIZE_SUB = 16
    FONT_SIZE_TXT = 14
    FONT_SIZE_TEXT = 12
    FONT_SIZE_SMALL = 10
    FONT_PRIMARY = (FONT, FONT_SIZE_TEXT)
    FONT_SECONDARY = (FONT, FONT_SIZE_SMALL)
    FONT_TITLE = (FONT, FONT_SIZE_TITLE, "bold")
    FONT_SUBTITLE = (FONT, FONT_SIZE_HEADER, "bold")
    FONT_SMALL = (FONT, FONT_SIZE_SMALL)
    FONT_BUTTON = (FONT, FONT_SIZE_TEXT, "bold")
    FONT_CARD_TITLE = (FONT, FONT_SIZE_SUB, "bold")
    
    # Espacements par défaut
    MARGIN_SMALL = 5
    MARGIN_MEDIUM = 10
    MARGIN_LARGE = 20
    MARGIN_CARD = 8
    MARGIN_SECTION = 15
    PADDING_SMALL = 5
    PADDING_MEDIUM = 10
    PADDING_LARGE = 20
    PADDING_CARD = 15
    PADDING_BUTTON = 10
    
    # Fonctions par défaut
    def apply_theme_to_app(root):
        root.configure(bg=BG_MAIN)
    
    def get_font_config():
        return {"font": FONT, "size": FONT_SIZE_TEXT}
    
    def get_spacing_config():
        return {"margin": MARGIN_MEDIUM, "padding": PADDING_MEDIUM}

# Configuration des icônes avec chemin exact
ICON_PATH = r"C:\Users\Lenovo\Desktop\Clonage_git\Gestion_scolaire\Gestion_scolaire\resources\icons"
print(f"Chemin des icônes: {ICON_PATH}")
print(f"Le dossier existe: {os.path.exists(ICON_PATH)}")

# Si le dossier n'existe pas, essayer le chemin relatif
if not os.path.exists(ICON_PATH):
    alt_icon_path = os.path.join(src_root, "resources", "icons")
    if os.path.exists(alt_icon_path):
        ICON_PATH = alt_icon_path
        print(f"Utilisation du chemin relatif: {ICON_PATH}")
    else:
        print("ATTENTION - Aucun dossier d'icônes trouvé")
ICON_MAP = {
    'add': 'add.png',
    'edit': 'edit.png',
    'delete': 'delete.png',
    'refresh': 'refresh.png',
    'search': 'search.png',
    'home': 'home.png',
    'person': 'person.png',
    'group': 'group.png',
    'book': 'book.png',
    'notes': 'notes.png',
    'check': 'check.png',
    'file': 'file.png',
    'bell': 'bell.png',
    'calendar': 'calendar.png',
    'money': 'money.png',
    'logout': 'logout.png',
    'close': 'close.png',
    'filter': 'filter.png',
    'export': 'upload.png',
    'stats': 'stats.png',
    'analytics': 'analytics.png',
    'trending_up': 'trending-up.png',
    'assignment': 'assignment.png',
    'autorenew': 'autorenew.png',
    'sort': 'sort.png',
    'view': 'view.png',
    'detail': 'detail.png'
}

def load_icon(icon_name, size=(20, 20)):
    """Charge une icône depuis le dossier resources/icons ou utilise des icônes Unicode"""
    try:
        if icon_name in ICON_MAP:
            icon_path = os.path.join(ICON_PATH, ICON_MAP[icon_name])
            if os.path.exists(icon_path):
                from PIL import Image
                pil_image = Image.open(icon_path)
                return ctk.CTkImage(light_image=pil_image, 
                                  dark_image=pil_image, 
                                  size=size)
        
        # Si l'icône n'existe pas, créer une icône Unicode
        return create_unicode_icon(icon_name, size)
        
    except Exception as e:
        print(f"ERREUR - Chargement icône {icon_name}: {e}")
        return create_unicode_icon(icon_name, size)

def create_unicode_icon(icon_name, size=(20, 20)):
    """Crée une icône Unicode en cas de fichier manquant"""
    try:
        from PIL import Image, ImageDraw, ImageFont
        
        # Mapping des icônes Unicode avec caractères plus simples
        unicode_icons = {
            'money': '$',
            'clock': '⏰',
            'view': '👁',
            'chevron_left': '◀',
            'chevron_right': '▶',
            'add': '+',
            'edit': '✎',
            'delete': '✗',
            'refresh': '↻',
            'search': '🔍',
            'home': '⌂',
            'person': '👤',
            'group': '👥',
            'book': '📖',
            'notes': '📝',
            'check': '✓',
            'file': '📄',
            'bell': '🔔',
            'calendar': '📅',
            'logout': '→',
            'close': '✕',
            'filter': '↓',
            'export': '↑',
            'stats': '📊',
            'analytics': '📈',
            'trending_up': '↗',
            'assignment': '📋',
            'autorenew': '↻',
            'sort': '↕',
            'detail': '👁'
        }
        
        icon_char = unicode_icons.get(icon_name, '❓')
        
        # Créer une image avec l'icône Unicode
        img = Image.new('RGBA', size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        
        try:
            # Essayer d'utiliser une police système avec support Unicode
            font_size = min(size) - 2
            try:
                font = ImageFont.truetype("seguiemj.ttf", font_size)  # Police avec support emoji
            except:
                try:
                    font = ImageFont.truetype("arial.ttf", font_size)
                except:
                    try:
                        font = ImageFont.truetype("calibri.ttf", font_size)
                    except:
                        font = ImageFont.load_default()
        except:
            font = ImageFont.load_default()
        
        # Calculer la position pour centrer l'icône
        bbox = draw.textbbox((0, 0), icon_char, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        
        x = (size[0] - text_width) // 2
        y = (size[1] - text_height) // 2
        
        # Dessiner l'icône avec une couleur visible
        draw.text((x, y), icon_char, fill=(255, 255, 255, 255), font=font)
        
        return ctk.CTkImage(light_image=img, dark_image=img, size=size)
        
    except Exception as e:
        print(f"ERREUR - Création icône Unicode {icon_name}: {e}")
        return None

def load_ctk_icon(icon_name, size=(20, 20)):
    """Charge une icône pour CustomTkinter"""
    return load_icon(icon_name, size)

class PaiementsView(ctk.CTkFrame):
    """Vue moderne des Paiements avec Dashboard inspirée de Myschool"""
    
    def __init__(self, parent):
        super().__init__(parent, fg_color=BG_MAIN)
        
        # Variables de pagination
        self.current_page = 1
        self.items_per_page = 20
        self.total_pages = 1
        
        # Variables de filtrage
        self.selected_classe = None
        self.selected_statut = None
        self.search_text = ""
        
        # Cache des données
        self.paiements = []
        self.eleves = []
        self.classes = []
        self.types_frais = []
        self.echeances = []
        
        # Contrôleur amélioré
        self.enhanced_controller = EnhancedPaiementController()
        
        # Initialisation
        self._initialize_database()
        self._load_data()
        self._build_interface()
        self._update_dashboard()
    
        # Ajouter des effets visuels modernes
        self._add_modern_effects()
    
    def _initialize_database(self):
        """Initialise la base de données"""
        try:
            # Créer toutes les tables du système de paiements
            if create_all_payment_tables():
                print("SUCCES - Tables de paiements créées avec succès")
            
            # Recréer la table paiements pour compatibilité
            if create_table_paiements():
                # Insérer des données de test
                insert_sample_payments()
        except Exception as e:
            print(f"ERREUR initialisation base de donnees: {e}")
    
    def _load_data(self):
        """Charge les données depuis la base"""
        try:
            # Charger les paiements
            try:
                self.paiements = get_all_paiements()
                print(f"SUCCES - {len(self.paiements)} paiements charges")
            except Exception as e:
                print(f"ERREUR chargement paiements: {e}")
                self.paiements = []
            
            # Charger les élèves
            try:
                self.eleves = get_all_eleves()
                print(f"SUCCES - {len(self.eleves)} élèves chargés")
            except Exception as e:
                print(f"ERREUR - Erreur chargement élèves: {e}")
                self.eleves = []
            
            # Charger les classes
            try:
                self.classes = get_all_classes()
                print(f"SUCCES - {len(self.classes)} classes chargées")
            except Exception as e:
                print(f"ERREUR - Erreur chargement classes: {e}")
                self.classes = []
            # Charger les types de frais
            try:
                self.types_frais = self.enhanced_controller.get_all_types_frais()
                print(f"SUCCES - {len(self.types_frais)} types de frais chargés")
            except Exception as e:
                print(f"ERREUR - Erreur chargement types de frais: {e}")
                self.types_frais = []
                self.types_frais = []
        
            # Charger les échéances en retard
            try:
                self.echeances = self.enhanced_controller.get_echeances_en_retard()
                print(f"SUCCES - {len(self.echeances)} échéances en retard trouvées")
            except Exception as e:
                print(f"ERREUR - Erreur chargement échéances: {e}")
                self.echeances = []
                
        except Exception as e:
            print(f"ERREUR generale chargement donnees: {e}")
            self.paiements = []
            self.eleves = []
            self.classes = []
        
        # Mettre à jour le statut
        self._update_status()
    
    def _update_status(self):
        """Met à jour le statut des données"""
        if hasattr(self, 'status_label'):
            total_paiements = len(self.paiements)
            total_eleves = len(self.eleves)
            total_classes = len(self.classes)
            
            status_text = f" {total_paiements} paiements • {total_eleves} élèves • {total_classes} classes"
            self.status_label.configure(text=status_text)
    
    def _build_interface(self):
        """Construit l'interface moderne avec sidebar comme le dashboard principal"""
        # Configuration de la grille principale
        self.grid_columnconfigure(0, weight=0, minsize=280)  # Sidebar fixe
        self.grid_columnconfigure(1, weight=1)  # Contenu principal
        self.grid_rowconfigure(0, weight=1)
        
        # Header avec titre et breadcrumbs
        self._build_header()
        
        # Sidebar moderne
        self._build_modern_sidebar()
        
        # Contenu principal
        self._build_main_content()
    
    def _build_header(self):
        """Construit l'en-tête avec titre moderne et boutons d'action"""
        header_frame = ctk.CTkFrame(self, fg_color="transparent", height=50)
        header_frame.grid(row=0, column=0, columnspan=2, sticky="ew", padx=5, pady=(5, 5))
        header_frame.grid_columnconfigure(0, weight=1)
        header_frame.grid_propagate(False)
        
        # Ligne principale avec titre et boutons d'action
        main_row = ctk.CTkFrame(header_frame, fg_color="transparent")
        main_row.grid(row=0, column=0, sticky="ew", pady=5)
        main_row.grid_columnconfigure(1, weight=1)
        
        # Titre principal avec icône
        title_frame = ctk.CTkFrame(main_row, fg_color="transparent")
        title_frame.grid(row=0, column=0, sticky="w")
        
        # Icône pour le titre
        money_icon = load_icon('money', (28, 28))
        if money_icon:
            ctk.CTkLabel(title_frame, text="", image=money_icon, fg_color="transparent").pack(side="left", padx=(0, 10))
        
        # Titre principal
        ctk.CTkLabel(title_frame, text="Tableau de bord des paiements", 
                    font=(FONT, 20, "bold"), text_color=TEXT_PRIMARY).pack(side="left")
        
        # Boutons d'action rapide dans l'en-tête
        actions_frame = ctk.CTkFrame(main_row, fg_color="transparent")
        actions_frame.grid(row=0, column=2, sticky="e")
        
        # Boutons d'action avec design contours uniquement (sans doublons)
        action_buttons = [
            ("Voir", BTN_PRIMARY, self._show_all_payments, "view"),
            ("Valider", BTN_SUCCESS, self._validate_payments, "check"),
            ("Relances", BTN_WARNING, self._show_relances, "bell"),
            ("Actualiser", BTN_INFO, self._refresh_data, "refresh")
        ]
        
        for i, (text, color, command, icon_name) in enumerate(action_buttons):
            # Charger l'icône
            icon = load_icon(icon_name, (16, 16))
            
            btn = ctk.CTkButton(
                actions_frame,
                text=text,
                image=icon,
                command=command,
                font=FONT_BUTTON,
                width=80,
                height=35,
                corner_radius=8,
                fg_color="transparent",
                hover_color=HOVER_PRIMARY,
                border_width=2,
                border_color=color,
                text_color=color
            )
            btn.grid(row=0, column=i, padx=3)
        
        # Sous-titre avec statut
        subtitle_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        subtitle_frame.grid(row=1, column=0, sticky="w", pady=(2, 0))
        
        ctk.CTkLabel(subtitle_frame, text="Gestion complète des paiements scolaires", 
                    font=FONT_SECONDARY, text_color=TEXT_SECONDARY).pack(side="left")
        
        # Statut des données
        self.status_label = ctk.CTkLabel(subtitle_frame, text="", 
                                        font=FONT_SMALL, text_color=TEXT_ACCENT)
        self.status_label.pack(side="left", padx=(20, 0))
    
    def _build_modern_sidebar(self):
        """Construit une belle sidebar moderne comme le dashboard principal"""
        # Sidebar principale
        self.sidebar_frame = ctk.CTkFrame(self, fg_color=BG_SIDEBAR, width=280, corner_radius=15, border_width=1, border_color=BORDER_COLOR)
        self.sidebar_frame.grid(row=1, column=0, sticky="ns", padx=(5, 0), pady=(0, 5))
        self.sidebar_frame.grid_propagate(False)
        self.sidebar_frame.grid_rowconfigure(2, weight=1)
        
        # En-tête de la sidebar
        self._build_sidebar_header()
        
        # Navigation scrollable
        self._build_sidebar_navigation()
        
        # Footer de la sidebar
        self._build_sidebar_footer()
    
    def _build_sidebar_header(self):
        """Construit l'en-tête de la sidebar"""
        # En-tête avec logo et titre
        header_frame = ctk.CTkFrame(self.sidebar_frame, fg_color=NAVY_BLUE, corner_radius=12, height=80)
        header_frame.pack(fill="x", padx=10, pady=10)
        header_frame.pack_propagate(False)
        
        # Container pour le contenu
        content_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        content_frame.pack(expand=True, fill="both", padx=15, pady=10)
        
        # Icône principale
        money_icon = load_icon("money", (32, 32))
        if money_icon:
            icon_label = ctk.CTkLabel(content_frame, text="", image=money_icon, fg_color="transparent")
            icon_label.pack(pady=(0, 8))
        
        # Titre principal
        ctk.CTkLabel(content_frame, text="PAIEMENTS", 
                    font=(FONT, 18, "bold"), text_color=ACCENT_BLUE).pack()
        
        # Sous-titre
        ctk.CTkLabel(content_frame, text="Gestion Financière", 
                    font=(FONT, 10), text_color=PALE_BLUE).pack()
    
    def _build_sidebar_navigation(self):
        """Construit la navigation de la sidebar"""
        # Frame scrollable pour la navigation
        nav_scroll = ctk.CTkScrollableFrame(self.sidebar_frame, fg_color="transparent")
        nav_scroll.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        
        # Sections de navigation
        nav_sections = {
            "📊 STATISTIQUES": [
                ("Vue d'ensemble", self._show_overview, "stats"),
                ("Rapports", self._show_reports, "analytics"),
                ("Graphiques", self._show_charts, "trending_up")
            ],
            "💰 GESTION": [
                ("Nouveau Paiement", self._show_add_payment_dialog, "add"),
                ("Échéancier", self._show_echeancier, "calendar"),
                ("Remises", self._show_remises, "assignment"),
                ("Relances", self._show_relances, "bell")
            ],
            "🔍 FILTRES": [
                ("Tous les paiements", self._filter_all_payments, "view"),
                ("Validés", self._filter_validated_payments, "check"),
                ("En attente", self._filter_pending_payments, "clock"),
                ("En retard", self._filter_overdue_payments, "bell")
            ],
            "⚙️ PARAMÈTRES": [
                ("Types de frais", self._show_fee_types, "file"),
                ("Configuration", self._show_settings, "file"),
                ("Export", self._export_payments, "export")
            ]
        }
        
        # Créer les sections
        for section_title, items in nav_sections.items():
            self._create_nav_section(nav_scroll, section_title, items)
    
    def _create_nav_section(self, parent, title, items):
        """Crée une section de navigation"""
        # Titre de la section
        section_frame = ctk.CTkFrame(parent, fg_color="transparent")
        section_frame.pack(fill="x", pady=(15, 5))
        
        ctk.CTkLabel(section_frame, text=title, 
                    font=(FONT, 11, "bold"), text_color=ACCENT_BLUE).pack(anchor="w", padx=10)
        
        # Items de la section
        for text, command, icon_name in items:
            self._create_nav_button(parent, text, command, icon_name)
    
    def _create_nav_button(self, parent, text, command, icon_name):
        """Crée un bouton de navigation"""
        # Charger l'icône
        icon = load_icon(icon_name, (18, 18))
        
        # Bouton de navigation
        btn = ctk.CTkButton(
            parent,
            text=text,
            image=icon,
            command=command,
            font=(FONT, 11),
            height=40,
            corner_radius=10,
            fg_color="transparent",
            hover_color=HOVER_PRIMARY,
            border_width=1,
            border_color=BORDER_COLOR,
            text_color=TEXT_PRIMARY,
            anchor="w"
        )
        btn.pack(fill="x", padx=5, pady=2)
    
    def _build_sidebar_footer(self):
        """Construit le footer de la sidebar"""
        # Footer avec informations
        footer_frame = ctk.CTkFrame(self.sidebar_frame, fg_color=NAVY_BLUE, corner_radius=12, height=60)
        footer_frame.pack(fill="x", padx=10, pady=(0, 10))
        footer_frame.pack_propagate(False)
        
        # Container pour le contenu
        content_frame = ctk.CTkFrame(footer_frame, fg_color="transparent")
        content_frame.pack(expand=True, fill="both", padx=15, pady=10)
        
        # Statut
        ctk.CTkLabel(content_frame, text="🟢 Système actif", 
                    font=(FONT, 10, "bold"), text_color=SUCCESS_GREEN).pack(anchor="w")
        
        # Version
        ctk.CTkLabel(content_frame, text="EduManager+ v2.0", 
                    font=(FONT, 9), text_color=PALE_BLUE).pack(anchor="w", pady=(2, 0))
    
    def _show_overview(self):
        """Affiche la vue d'ensemble"""
        print("Affichage vue d'ensemble")
        messagebox.showinfo("Information", "Vue d'ensemble des paiements - À implémenter")
    
    def _show_charts(self):
        """Affiche les graphiques"""
        print("Affichage graphiques")
        messagebox.showinfo("Information", "Graphiques des paiements - À implémenter")
    
    def _show_fee_types(self):
        """Affiche les types de frais"""
        print("Affichage types de frais")
        messagebox.showinfo("Information", "Gestion des types de frais - À implémenter")
    
    def _build_quick_filters_bar(self, parent):
        """Construit la barre de filtres rapides avec design moderne et cartes de statistiques"""
        # Container pour les filtres rapides
        quick_filters_frame = ctk.CTkFrame(parent, fg_color="transparent")
        quick_filters_frame.pack(fill="x", padx=5, pady=(0, 15))
        
        # Titre de la section
        title_frame = ctk.CTkFrame(quick_filters_frame, fg_color="transparent")
        title_frame.pack(fill="x", padx=10, pady=(0, 15))
        
        ctk.CTkLabel(title_frame, text="📊 STATISTIQUES RAPIDES", 
                    font=(FONT, 16, "bold"), text_color=ACCENT_BLUE).pack(anchor="w")
        
        # Container pour les cartes de statistiques
        stats_container = ctk.CTkFrame(quick_filters_frame, fg_color="transparent")
        stats_container.pack(fill="x")
        
        # Calculer les statistiques
        stats_data = self._calculate_statistics()
        
        # Créer les cartes de statistiques modernes
        self._create_quick_stats_cards(stats_container, stats_data)
        
        # Container pour les filtres rapides
        filters_container = ctk.CTkFrame(quick_filters_frame, fg_color=CARD_BG, corner_radius=12)
        filters_container.pack(fill="x", pady=(15, 0))
        
        # Titre des filtres
        filters_title = ctk.CTkFrame(filters_container, fg_color="transparent")
        filters_title.pack(fill="x", padx=15, pady=(10, 5))
        
        ctk.CTkLabel(filters_title, text="⚡ FILTRES RAPIDES", 
                    font=(FONT, 12, "bold"), text_color=ACCENT_BLUE).pack(anchor="w")
        
        # Boutons de filtres rapides avec design moderne
        filter_buttons = [
            ("Tous", BTN_PRIMARY, self._filter_all_payments, "all"),
            ("Validés", BTN_SUCCESS, self._filter_validated_payments, "check"),
            ("En attente", BTN_WARNING, self._filter_pending_payments, "clock"),
            ("Relances", BTN_DANGER, self._filter_overdue_payments, "bell")
        ]
        
        # Container pour les boutons en ligne
        buttons_frame = ctk.CTkFrame(filters_container, fg_color="transparent")
        buttons_frame.pack(fill="x", padx=15, pady=(0, 10))
        
        for i, (text, color, command, icon_name) in enumerate(filter_buttons):
            # Charger l'icône
            icon = load_icon(icon_name, (16, 16))
            
            btn = ctk.CTkButton(
                buttons_frame,
                text=text,
                image=icon,
                command=command,
                font=(FONT, 10, "bold"),
                height=35,
                corner_radius=18,
                fg_color=color,
                hover_color=self._darken_color(color),
                text_color="white",
                border_width=0
            )
            btn.pack(side="left", fill="both", expand=True, padx=5)
    
    def _create_quick_stats_cards(self, parent, stats_data):
        """Crée des cartes de statistiques rapides avec design moderne"""
        # Données des cartes avec icônes et couleurs
        cards_data = [
            {
                "title": "Paiements Validés",
                "value": f"{stats_data.get('total_validated', 0):,} GNF",
                "subtitle": "Ce mois",
                "icon": "check",
                "color": "#27ae60",
                "bg_color": "#1e3a2e",
                "border_color": "#27ae60"
            },
            {
                "title": "Total Paiements",
                "value": str(stats_data.get('total_payments', 0)),
                "subtitle": "Transactions",
                "icon": "money",
                "color": "#3498db",
                "bg_color": "#1e2a3a",
                "border_color": "#3498db"
            },
            {
                "title": "Élèves en Retard",
                "value": str(stats_data.get('students_overdue', 0)),
                "subtitle": "À relancer",
                "icon": "bell",
                "color": "#f39c12",
                "bg_color": "#3a2e1e",
                "border_color": "#f39c12"
            },
            {
                "title": "En Attente",
                "value": str(stats_data.get('pending_payments', 0)),
                "subtitle": "À valider",
                "icon": "clock",
                "color": "#e74c3c",
                "bg_color": "#3a1e1e",
                "border_color": "#e74c3c"
            }
        ]
        
        # Container pour les cartes en ligne
        cards_container = ctk.CTkFrame(parent, fg_color="transparent")
        cards_container.pack(fill="x")
        
        # Créer chaque carte avec pack
        for i, card_data in enumerate(cards_data):
            card = self._create_quick_stat_card(cards_container, card_data)
            card.pack(side="left", fill="both", expand=True, padx=(0, 10) if i < 3 else 0)
    
    def _create_quick_stat_card(self, parent, card_data):
        """Crée une carte de statistique rapide avec design attrayant"""
        # Frame principal de la carte
        card = ctk.CTkFrame(parent, fg_color=card_data["bg_color"], 
                           corner_radius=12, border_width=2, 
                           border_color=card_data["border_color"], height=80)
        card.pack_propagate(False)
        
        # Contenu de la carte
        content_frame = ctk.CTkFrame(card, fg_color="transparent")
        content_frame.pack(fill="both", expand=True, padx=15, pady=10)
        
        # En-tête avec icône et titre
        header_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        header_frame.pack(fill="x", pady=(0, 8))
        
        # Icône
        icon = load_icon(card_data["icon"], (20, 20))
        if icon:
            icon_label = ctk.CTkLabel(header_frame, text="", image=icon, 
                                    fg_color="transparent")
            icon_label.pack(side="left")
        
        # Titre
        title_label = ctk.CTkLabel(header_frame, text=card_data["title"],
                                 font=(FONT, 10, "bold"), 
                                 text_color=card_data["color"])
        title_label.pack(side="left", padx=(8, 0))
        
        # Valeur principale
        value_label = ctk.CTkLabel(content_frame, text=card_data["value"],
                                 font=(FONT, 18, "bold"), 
                                 text_color=card_data["color"])
        value_label.pack(anchor="w", pady=(0, 2))
        
        # Sous-titre
        subtitle_label = ctk.CTkLabel(content_frame, text=card_data["subtitle"],
                                    font=(FONT, 9), 
                                    text_color=TEXT_SECONDARY)
        subtitle_label.pack(anchor="w")
        
        return card
    
    def _filter_all_payments(self):
        """Filtre pour afficher tous les paiements"""
        self.selected_statut = "Tous les paiements"
        self._display_payments()
    
    def _filter_validated_payments(self):
        """Filtre pour afficher les paiements validés"""
        self.selected_statut = "Élèves soldés"
        self._display_payments()
    
    def _filter_pending_payments(self):
        """Filtre pour afficher les paiements en attente"""
        self.selected_statut = "En attente"
        self._display_payments()
    
    def _filter_overdue_payments(self):
        """Filtre pour afficher les paiements en relance"""
        self.selected_statut = "Relances"
        self._display_payments()
    
    def _build_main_content(self):
        """Construit le contenu principal avec design moderne avec sidebar"""
        # Frame principal du contenu
        main_content_frame = ctk.CTkFrame(self, fg_color=BG_MAIN, corner_radius=15, border_width=1, border_color=BORDER_COLOR)
        main_content_frame.grid(row=1, column=1, sticky="nsew", padx=(0, 5), pady=(0, 5))
        main_content_frame.grid_columnconfigure(0, weight=1)
        main_content_frame.grid_rowconfigure(1, weight=1)
        
        # Container scrollable pour le contenu
        content_scroll = ctk.CTkScrollableFrame(main_content_frame, fg_color="transparent")
        content_scroll.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)
        content_scroll.grid_columnconfigure(0, weight=1)
        
        # Barre de filtres rapides
        self._build_quick_filters_bar(content_scroll)
        
        # Dashboard principal moderne
        self._build_modern_dashboard(content_scroll)
    
    def _build_modern_dashboard(self, parent):
        """Construit un dashboard moderne sans sidebar avec filtres et tableau"""
        # Frame principal du dashboard
        dashboard_frame = ctk.CTkFrame(parent, fg_color="transparent")
        dashboard_frame.pack(fill="both", expand=True, pady=(10, 0))
        
        # Section principale avec filtres et tableau
        self._build_main_section(dashboard_frame)
    
    def _build_statistics_section(self, parent):
        """Construit la section des statistiques avec cartes modernes"""
        # Frame des statistiques
        stats_frame = ctk.CTkFrame(parent, fg_color="transparent")
        stats_frame.pack(fill="x", padx=5, pady=(0, 20))
        
        # Calculer les statistiques
        stats_data = self._calculate_statistics()
        
        # Créer les cartes de statistiques modernes
        self.modern_stats_cards = []
        self._create_modern_stat_cards(stats_frame, stats_data)
    
    def _create_modern_stat_cards(self, parent, stats_data):
        """Crée des cartes de statistiques modernes et visuelles"""
        # Données des cartes avec icônes et couleurs
        cards_data = [
            {
                "title": "Paiements Validés",
                "value": f"{stats_data.get('total_validated', 0):,} GNF",
                "subtitle": "Ce mois",
                "icon": "check",
                "color": "#27ae60",
                "bg_color": "#1e3a2e",
                "border_color": "#27ae60"
            },
            {
                "title": "Total Paiements",
                "value": str(stats_data.get('total_payments', 0)),
                "subtitle": "Transactions",
                "icon": "money",
                "color": "#3498db",
                "bg_color": "#1e2a3a",
                "border_color": "#3498db"
            },
            {
                "title": "Élèves en Retard",
                "value": str(stats_data.get('students_overdue', 0)),
                "subtitle": "À relancer",
                "icon": "bell",
                "color": "#f39c12",
                "bg_color": "#3a2e1e",
                "border_color": "#f39c12"
            },
            {
                "title": "En Attente",
                "value": str(stats_data.get('pending_payments', 0)),
                "subtitle": "À valider",
                "icon": "clock",
                "color": "#e74c3c",
                "bg_color": "#3a1e1e",
                "border_color": "#e74c3c"
            }
        ]
        
        # Container pour les cartes en ligne
        cards_container = ctk.CTkFrame(parent, fg_color="transparent")
        cards_container.pack(fill="x")
        
        # Créer chaque carte avec pack
        for i, card_data in enumerate(cards_data):
            card = self._create_modern_card(cards_container, card_data)
            card.pack(side="left", fill="both", expand=True, padx=(0, 10) if i < 3 else 0)
            self.modern_stats_cards.append(card)
    
    def _create_modern_card(self, parent, card_data):
        """Crée une carte moderne avec design attrayant"""
        # Frame principal de la carte
        card = ctk.CTkFrame(parent, fg_color=card_data["bg_color"], 
                           corner_radius=15, border_width=2, 
                           border_color=card_data["border_color"])
        card.grid_columnconfigure(0, weight=1)
        
        # Contenu de la carte
        content_frame = ctk.CTkFrame(card, fg_color="transparent")
        content_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # En-tête avec icône et titre
        header_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        header_frame.pack(fill="x", pady=(0, 15))
        
        # Icône
        icon = load_icon(card_data["icon"], (24, 24))
        if icon:
            icon_label = ctk.CTkLabel(header_frame, text="", image=icon, 
                                    fg_color="transparent")
            icon_label.pack(side="left")
        
        # Titre
        title_label = ctk.CTkLabel(header_frame, text=card_data["title"],
                                 font=(FONT, 12, "bold"), 
                                 text_color=card_data["color"])
        title_label.pack(side="left", padx=(10, 0))
        
        # Valeur principale
        value_label = ctk.CTkLabel(content_frame, text=card_data["value"],
                                 font=(FONT, 24, "bold"), 
                                 text_color=card_data["color"])
        value_label.pack(anchor="w", pady=(0, 5))
        
        # Sous-titre
        subtitle_label = ctk.CTkLabel(content_frame, text=card_data["subtitle"],
                                    font=(FONT, 10), 
                                    text_color=TEXT_SECONDARY)
        subtitle_label.pack(anchor="w")
        
        return card
    
    def _add_visual_effects(self, widget, effect_type="hover"):
        """Ajoute des effets visuels modernes aux widgets"""
        if effect_type == "hover":
            # Effet de survol avec changement de couleur
            original_color = widget.cget("fg_color")
            def on_enter(event):
                widget.configure(fg_color=self._lighten_color(original_color))
            def on_leave(event):
                widget.configure(fg_color=original_color)
            
            widget.bind("<Enter>", on_enter)
            widget.bind("<Leave>", on_leave)
    
    def _lighten_color(self, color):
        """Éclaircit une couleur hexadécimale"""
        if color.startswith("#"):
            # Convertir en RGB
            r = int(color[1:3], 16)
            g = int(color[3:5], 16)
            b = int(color[5:7], 16)
            
            # Éclaircir de 20%
            r = min(255, int(r * 1.2))
            g = min(255, int(g * 1.2))
            b = min(255, int(b * 1.2))
            
            return f"#{r:02x}{g:02x}{b:02x}"
        return color
    
    def _build_main_section(self, parent):
        """Construit la section principale avec filtres et tableau"""
        # Frame principal
        main_section = ctk.CTkFrame(parent, fg_color="transparent")
        main_section.pack(fill="both", expand=True, pady=(0, 10))
        
        # Section des filtres et actions
        self._build_filters_and_actions_section(main_section)
        
        # Section du tableau
        self._build_table_section(main_section)
    
    def _build_filters_and_actions_section(self, parent):
        """Construit la section des filtres et actions modernes"""
        # Frame des filtres et actions
        filters_frame = ctk.CTkFrame(parent, fg_color=CARD_BG, corner_radius=15)
        filters_frame.pack(fill="x", padx=5, pady=(0, 20))
        
        # Titre de la section
        title_frame = ctk.CTkFrame(filters_frame, fg_color="transparent")
        title_frame.pack(fill="x", padx=20, pady=(20, 15))
        
        ctk.CTkLabel(title_frame, text="🔍 FILTRES ET ACTIONS", 
                    font=(FONT, 16, "bold"), text_color=ACCENT_BLUE).pack(anchor="w")
        
        # Filtres dans une ligne
        self._build_modern_filters_row(filters_frame)
        
        # Actions rapides dans une ligne
        self._build_modern_actions_row(filters_frame)
    
    def _build_modern_filters_row(self, parent):
        """Construit une ligne de filtres modernes"""
        # Frame des filtres
        filters_row = ctk.CTkFrame(parent, fg_color="transparent")
        filters_row.pack(fill="x", padx=20, pady=(0, 15))
        
        # Container pour les filtres en ligne
        filters_container = ctk.CTkFrame(filters_row, fg_color="transparent")
        filters_container.pack(fill="x")
        
        # Filtre par classe
        classe_frame = ctk.CTkFrame(filters_container, fg_color="transparent")
        classe_frame.pack(side="left", fill="both", expand=True, padx=(0, 10))
        
        ctk.CTkLabel(classe_frame, text="Classe", 
                    font=(FONT, 11, "bold"), text_color=TEXT_PRIMARY).pack(anchor="w")
        
        self.classe_var = ctk.StringVar(value="Toutes les classes")
        classe_values = ["Toutes les classes"] + [classe.get('nom', '') for classe in self.classes]
        self.classe_dropdown = ctk.CTkComboBox(classe_frame, variable=self.classe_var,
                                              values=classe_values, command=self._on_classe_selected,
                                              font=FONT_SMALL, dropdown_font=FONT_SMALL,
                                              corner_radius=10, border_width=1, border_color=BORDER_COLOR,
                                              fg_color=BG_MAIN, button_color=ACCENT_BLUE, 
                                              button_hover_color=HOVER_PRIMARY, height=40)
        self.classe_dropdown.pack(fill="x", pady=(5, 0))
        
        # Filtre par statut
        statut_frame = ctk.CTkFrame(filters_container, fg_color="transparent")
        statut_frame.pack(side="left", fill="both", expand=True, padx=5)
        
        ctk.CTkLabel(statut_frame, text="Statut", 
                    font=(FONT, 11, "bold"), text_color=TEXT_PRIMARY).pack(anchor="w")
        
        self.statut_var = ctk.StringVar(value="Tous les paiements")
        statut_values = ["Tous les paiements", "Élèves soldés", "En attente", "Relances"]
        self.statut_dropdown = ctk.CTkComboBox(statut_frame, variable=self.statut_var,
                                              values=statut_values, command=self._on_statut_selected,
                                              font=FONT_SMALL, dropdown_font=FONT_SMALL,
                                              corner_radius=10, border_width=1, border_color=BORDER_COLOR,
                                              fg_color=BG_MAIN, button_color=ACCENT_BLUE, 
                                              button_hover_color=HOVER_PRIMARY, height=40)
        self.statut_dropdown.pack(fill="x", pady=(5, 0))
        
        # Barre de recherche
        search_frame = ctk.CTkFrame(filters_container, fg_color="transparent")
        search_frame.pack(side="left", fill="both", expand=True, padx=(10, 0))
        
        ctk.CTkLabel(search_frame, text="Recherche", 
                    font=(FONT, 11, "bold"), text_color=TEXT_PRIMARY).pack(anchor="w")
        
        self.search_entry = ctk.CTkEntry(search_frame, placeholder_text="Nom, classe, montant...",
                                        font=FONT_SMALL, height=40,
                                        corner_radius=10, border_width=1, border_color=BORDER_COLOR,
                                        fg_color=BG_MAIN, text_color=TEXT_PRIMARY)
        self.search_entry.pack(fill="x", pady=(5, 0))
        self.search_entry.bind("<KeyRelease>", self._on_search_change)
    
    def _build_modern_actions_row(self, parent):
        """Construit une ligne d'actions modernes"""
        # Frame des actions
        actions_row = ctk.CTkFrame(parent, fg_color="transparent")
        actions_row.pack(fill="x", padx=20, pady=(0, 20))
        
        # Container pour les boutons d'action
        actions_container = ctk.CTkFrame(actions_row, fg_color="transparent")
        actions_container.pack(fill="x")
        
        # Actions avec design moderne
        actions_data = [
            ("Nouveau Paiement", BTN_SUCCESS, self._show_add_payment_dialog, "add"),
            ("Échéancier", BTN_PRIMARY, self._show_echeancier, "calendar"),
            ("Rapports", BTN_WARNING, self._show_reports, "stats"),
            ("Relances", BTN_DANGER, self._show_relances, "bell"),
            ("Actualiser", BTN_INFO, self._refresh_data, "refresh")
        ]
        
        for i, (text, color, command, icon_name) in enumerate(actions_data):
            # Charger l'icône
            icon = load_icon(icon_name, (18, 18))
            
            btn = ctk.CTkButton(
                actions_container,
                text=text,
                image=icon,
                command=command,
                font=(FONT, 11, "bold"),
                height=45,
                corner_radius=12,
                fg_color=color,
                hover_color=self._darken_color(color),
                text_color="white",
                border_width=0
            )
            btn.pack(side="left", fill="both", expand=True, padx=5)
    
    def _build_table_section(self, parent):
        """Construit la section du tableau moderne"""
        # Frame du tableau
        table_section = ctk.CTkFrame(parent, fg_color=CARD_BG, corner_radius=15)
        table_section.pack(fill="both", expand=True, padx=5)
        
        # En-tête du tableau
        table_header = ctk.CTkFrame(table_section, fg_color="transparent")
        table_header.pack(fill="x", padx=20, pady=(20, 15))
        
        # Titre du tableau avec icône
        title_frame = ctk.CTkFrame(table_header, fg_color="transparent")
        title_frame.pack(side="left")
        
        recent_icon = load_icon('clock', (20, 20))
        if recent_icon:
            ctk.CTkLabel(title_frame, text="", image=recent_icon, 
                        fg_color="transparent").pack(side="left", padx=(0, 10))
        
        ctk.CTkLabel(title_frame, text="PAIEMENTS RÉCENTS", 
                    font=(FONT, 16, "bold"), text_color=ACCENT_BLUE).pack(side="left")
        
        # Bouton voir tout
        view_all_icon = load_icon('view', (16, 16))
        ctk.CTkButton(table_header, text="", 
                     image=view_all_icon,
                     width=40, height=40,
                     fg_color="transparent",
                     hover_color=HOVER_PRIMARY,
                     border_width=2,
                     border_color=ACCENT_BLUE,
                     text_color=ACCENT_BLUE,
                     command=self._view_all_payments).pack(side="right")
        
        # Tableau des paiements
        self._build_payments_table(table_section)
    
    def _build_payments_table(self, parent):
        """Construit le tableau des paiements avec le nouveau design"""
        # Frame du tableau avec scroll
        table_frame = ctk.CTkScrollableFrame(parent, fg_color="transparent")
        table_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        # Tableau des paiements
        self.table_frame = table_frame
        
        # Afficher les paiements
        self._display_payments()
    
    def _create_modern_table_header(self, parent, headers):
        """Crée un en-tête de tableau moderne"""
        # Frame de l'en-tête avec design moderne
        header_frame = ctk.CTkFrame(parent, fg_color="#2c3e50", corner_radius=10, height=50)
        header_frame.pack(fill="x", pady=(0, 10))
        header_frame.pack_propagate(False)
        
        # Créer les en-têtes avec style moderne
        for i, header in enumerate(headers):
            header_label = ctk.CTkLabel(
                header_frame,
                text=header,
                font=(FONT, 12, "bold"),
                text_color="#ffffff",
                fg_color="#2c3e50"
            )
            header_label.pack(side="left", fill="both", expand=True, padx=15, pady=15)
        
        return header_frame
    
    def _create_modern_table_row(self, parent, data, row_index, colors=None):
        """Crée une ligne de tableau moderne"""
        if colors is None:
            colors = ["#34495e", "#2c3e50"]  # Couleurs par défaut
        
        # Couleur alternée
        row_color = colors[row_index % len(colors)]
        
        # Frame de la ligne avec design moderne
        row_frame = ctk.CTkFrame(parent, fg_color=row_color, corner_radius=8, height=45)
        row_frame.pack(fill="x", pady=(0, 5))
        row_frame.pack_propagate(False)
        
        # Créer les cellules
        for i, value in enumerate(data):
            cell_label = ctk.CTkLabel(
                row_frame,
                text=str(value),
                font=(FONT, 11),
                text_color="#ffffff",
                fg_color=row_color
            )
            cell_label.pack(side="left", fill="both", expand=True, padx=15, pady=12)
        
        return row_frame
    
    def _add_modern_effects(self):
        """Ajoute des effets visuels modernes à l'interface"""
        try:
            # Effet de fade-in pour les cartes de statistiques
            if hasattr(self, 'modern_stats_cards'):
                for i, card in enumerate(self.modern_stats_cards):
                    # Animation d'apparition progressive
                    card.after(i * 100, lambda c=card: self._animate_card_appearance(c))
            
            # Effet de survol pour les boutons d'action
            self._add_button_hover_effects()
            
        except Exception as e:
            print(f"Erreur lors de l'ajout des effets modernes: {e}")
    
    def _animate_card_appearance(self, card):
        """Anime l'apparition d'une carte"""
        try:
            # Effet de fade-in simple
            original_alpha = card.cget("fg_color")
            # L'effet sera géré par CustomTkinter automatiquement
            pass
        except Exception as e:
            print(f"Erreur animation carte: {e}")
    
    def _add_button_hover_effects(self):
        """Ajoute des effets de survol aux boutons"""
        try:
            # Effet de survol pour les boutons de filtres rapides
            for widget in self.winfo_children():
                if isinstance(widget, ctk.CTkButton):
                    self._add_modern_hover_effect(widget)
        except Exception as e:
            print(f"Erreur effets boutons: {e}")
    
    def _add_modern_hover_effect(self, button):
        """Ajoute un effet de survol moderne à un bouton"""
        try:
            original_color = button.cget("fg_color")
            
            def on_enter(event):
                # Effet de zoom léger
                button.configure(cursor="hand2")
            
            def on_leave(event):
                button.configure(cursor="arrow")
            
            button.bind("<Enter>", on_enter)
            button.bind("<Leave>", on_leave)
            
        except Exception as e:
            print(f"Erreur effet survol: {e}")
    
    def _build_sidebar(self, parent):
        """Construit la sidebar avec les actions - Design moderne avec le thème EduManager+"""
        sidebar = ctk.CTkFrame(parent, fg_color=BG_SIDEBAR, corner_radius=15)
        sidebar.grid(row=1, column=0, sticky="nsew", padx=(0, 5))
        
        # En-tête moderne avec le thème
        header_frame = ctk.CTkFrame(sidebar, fg_color=NAVY_BLUE, corner_radius=12, height=80)
        header_frame.pack(fill="x", padx=10, pady=10)
        header_frame.pack_propagate(False)
        
        # Titre avec icône
        title_container = ctk.CTkFrame(header_frame, fg_color="transparent")
        title_container.pack(expand=True, fill="both")
        
        # Icône pour les paiements
        money_icon = load_icon("money", (24, 24))
        icon_label = ctk.CTkLabel(title_container, text="$" if money_icon is None else "", 
                                image=money_icon,
                                font=FONT_TITLE, text_color=ACCENT_BLUE)
        icon_label.pack(pady=(10, 5))
        
        # Titre principal
        ctk.CTkLabel(title_container, text="GESTION PAIEMENTS", 
                    font=FONT_SUBTITLE, text_color=SOFT_BLUE).pack()
        
        # Sous-titre
        ctk.CTkLabel(title_container, text="Tableau de bord", 
                    font=FONT_SMALL, text_color=PALE_BLUE).pack(pady=(0, 10))
        
        # Section des actions avec design moderne
        actions_section = ctk.CTkFrame(sidebar, fg_color="transparent")
        actions_section.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        
        # Filtres avec design amélioré
        self._build_modern_filters(actions_section)
        
        # Boutons d'action avec design moderne
        self._build_modern_action_buttons(actions_section)
    
    def _build_modern_filters(self, parent):
        """Construit les filtres avec design moderne et le thème EduManager+"""
        # Section des filtres
        filters_section = ctk.CTkFrame(parent, fg_color=NAVY_BLUE, corner_radius=10)
        filters_section.pack(fill="x", pady=(0, 15))
        
        # Titre des filtres
        ctk.CTkLabel(filters_section, text=" FILTRES", 
                    font=FONT_BUTTON, text_color=ACCENT_BLUE).pack(pady=(10, 5))
        
        # Filtre par classe
        ctk.CTkLabel(filters_section, text="Classe:", 
                    font=FONT_SMALL, text_color=SOFT_BLUE).pack(anchor="w", padx=15)
        
        self.classe_var = ctk.StringVar(value="Toutes les classes")
        classe_values = ["Toutes les classes"] + [classe.get('nom', '') for classe in self.classes]
        self.classe_dropdown = ctk.CTkComboBox(filters_section, variable=self.classe_var,
                                              values=classe_values, command=self._on_classe_selected,
                                              font=FONT_SMALL, dropdown_font=FONT_SMALL,
                                              corner_radius=8, border_width=1, border_color=BORDER_COLOR,
                                              fg_color=BG_MAIN, button_color=ACCENT, 
                                              button_hover_color=HOVER_PRIMARY, height=35)
        self.classe_dropdown.pack(fill="x", padx=15, pady=(5, 10))
        
        # Filtre par statut
        ctk.CTkLabel(filters_section, text="Statut:", 
                    font=FONT_SMALL, text_color=SOFT_BLUE).pack(anchor="w", padx=15)
        
        self.statut_var = ctk.StringVar(value="Tous les paiements")
        statut_values = ["Tous les paiements", "Élèves soldés", "En attente", "Relances"]
        self.statut_dropdown = ctk.CTkComboBox(filters_section, variable=self.statut_var,
                                              values=statut_values, command=self._on_statut_selected,
                                              font=FONT_SMALL, dropdown_font=FONT_SMALL,
                                              corner_radius=8, border_width=1, border_color=BORDER_COLOR,
                                              fg_color=BG_MAIN, button_color=ACCENT, 
                                              button_hover_color=HOVER_PRIMARY, height=35)
        self.statut_dropdown.pack(fill="x", padx=15, pady=(5, 10))
        
        # Barre de recherche
        ctk.CTkLabel(filters_section, text="Recherche:", 
                    font=FONT_SMALL, text_color=SOFT_BLUE).pack(anchor="w", padx=15)
        
        self.search_entry = ctk.CTkEntry(filters_section, placeholder_text="Nom, classe, montant...",
                                        font=FONT_SMALL, height=35,
                                        corner_radius=8, border_width=1, border_color=BORDER_COLOR,
                                        fg_color=BG_MAIN, text_color=TEXT_PRIMARY)
        self.search_entry.pack(fill="x", padx=15, pady=(5, 15))
        self.search_entry.bind("<KeyRelease>", self._on_search_change)

    def _build_modern_action_buttons(self, parent):
        """Construit les boutons d'action avec design moderne et le thème EduManager+"""
        # Section des actions
        actions_section = ctk.CTkFrame(parent, fg_color=NAVY_BLUE, corner_radius=10)
        actions_section.pack(fill="x", pady=(0, 10))
        
        # Titre des actions
        ctk.CTkLabel(actions_section, text=" ACTIONS RAPIDES", 
                    font=FONT_BUTTON, text_color=ACCENT_BLUE).pack(pady=(10, 10))
        
        # Boutons d'action avec design moderne et icônes (sans doublon Actualiser)
        buttons_data = [
            ("Nouveau Paiement", "#27ae60", self._show_add_payment_dialog, "add"),
            ("Échéancier", "#3498db", self._show_echeancier, "calendar"),
            ("Remises", "#e74c3c", self._show_remises, "assignment"),
            ("Rapports", "#f39c12", self._show_reports, "stats"),
            ("Paramètres", "#95a5a6", self._show_settings, "file")
        ]
        
        for i, (text, color, command, icon_name) in enumerate(buttons_data):
            # Charger l'icône
            icon = load_icon(icon_name, (16, 16))
            
            btn = ctk.CTkButton(
                actions_section,
                text=text,
                image=icon,
                command=command,
                font=(FONT, 11, "bold"),
                height=40,
                corner_radius=8,
                fg_color=color,
                hover_color=self._darken_color(color),
                text_color="white",
                border_width=0
            )
            btn.pack(fill="x", padx=15, pady=3)

    def _darken_color(self, color):
        """Assombrit une couleur hexadécimale"""
        color_map = {
            "#27ae60": "#229954",  # Vert
            "#3498db": "#2980b9",  # Bleu
            "#e74c3c": "#c0392b",  # Rouge
            "#f39c12": "#e67e22",  # Orange
            "#9b59b6": "#8e44ad",  # Violet
            "#95a5a6": "#7f8c8d"   # Gris
        }
        return color_map.get(color, color)
    
    def _build_filters(self, parent):
        """Construit les filtres"""
        # Titre des filtres
        ctk.CTkLabel(parent, text="Filtres", 
                    font=(FONT, FONT_SIZE_TEXT, "bold"), text_color=TEXT_PRIMARY).pack(anchor="w", pady=(MARGIN_MEDIUM, MARGIN_SMALL))
        
        # Filtre par classe
        ctk.CTkLabel(parent, text="Classe:", 
                    font=(FONT, FONT_SIZE_SMALL), text_color=TEXT_SECONDARY).pack(anchor="w")
        
        self.classe_var = ctk.StringVar(value="Toutes les classes")
        classe_values = ["Toutes les classes"] + [classe.get('nom', '') for classe in self.classes]
        self.classe_dropdown = ctk.CTkComboBox(parent, variable=self.classe_var,
                                              values=classe_values, command=self._on_classe_selected,
                                              font=(FONT, FONT_SIZE_SMALL), dropdown_font=(FONT, FONT_SIZE_SMALL),
                                              corner_radius=8, border_width=1, border_color=BORDER_COLOR,
                                              fg_color=BG_CARD, button_color=ACCENT, 
                                              button_hover_color="#2563eb", height=35)
        self.classe_dropdown.pack(fill="x", pady=(MARGIN_SMALL, MARGIN_MEDIUM))
        
        # Filtre par statut
        ctk.CTkLabel(parent, text="Statut:", 
                    font=(FONT, FONT_SIZE_SMALL), text_color=TEXT_SECONDARY).pack(anchor="w")
        
        self.statut_var = ctk.StringVar(value="Tous les paiements")
        statut_values = ["Tous les paiements", "Élèves soldés", "En attente", "Relances"]
        self.statut_dropdown = ctk.CTkComboBox(parent, variable=self.statut_var,
                                              values=statut_values, command=self._on_statut_selected,
                                              font=(FONT, FONT_SIZE_SMALL), dropdown_font=(FONT, FONT_SIZE_SMALL),
                                              corner_radius=8, border_width=1, border_color=BORDER_COLOR,
                                              fg_color=BG_CARD, button_color=ACCENT, 
                                              button_hover_color="#2563eb", height=35)
        self.statut_dropdown.pack(fill="x", pady=(MARGIN_SMALL, MARGIN_MEDIUM))
        
        # Barre de recherche
        ctk.CTkLabel(parent, text="Recherche:", 
                    font=(FONT, FONT_SIZE_SMALL), text_color=TEXT_SECONDARY).pack(anchor="w")
        
        self.search_entry = ctk.CTkEntry(parent, placeholder_text="Nom, classe, montant...",
                                        font=(FONT, FONT_SIZE_SMALL), height=35,
                                        corner_radius=8, border_width=1, border_color=BORDER_COLOR)
        self.search_entry.pack(fill="x", pady=(MARGIN_SMALL, MARGIN_MEDIUM))
        self.search_entry.bind("<KeyRelease>", self._on_search_change)
    
    def _build_remaining_actions(self, parent):
        """Construit les boutons d'action restants dans la sidebar"""
        # Titre des actions
        ctk.CTkLabel(parent, text="Actions Avancées", 
                    font=FONT_BUTTON, text_color=TEXT_PRIMARY).pack(anchor="w", pady=(MARGIN_MEDIUM, MARGIN_SMALL))
        
        # Bouton Statistiques (icône uniquement)
        stats_icon = load_icon('stats', (20, 20))
        stats_btn = ctk.CTkButton(
            parent, 
            text="",
            image=stats_icon,
            command=self._show_statistics,
            fg_color=BTN_INFO,
            hover_color=HOVER_INFO,
            width=50,
            height=40, 
            corner_radius=8
        )
        stats_btn.pack(fill="x", pady=(0, MARGIN_SMALL))
        
        # Bouton Dépenses (icône uniquement)
        expenses_icon = load_icon('trending_up', (20, 20))
        expenses_btn = ctk.CTkButton(
            parent, 
            text="",
            image=expenses_icon,
            command=self._show_expenses,
            fg_color=BTN_WARNING,
            hover_color=HOVER_WARNING,
            width=50,
            height=40, 
            corner_radius=8
        )
        expenses_btn.pack(fill="x", pady=(0, MARGIN_SMALL))
        
        # Bouton Recréer Table (icône uniquement)
        recreate_icon = load_icon('autorenew', (20, 20))
        recreate_btn = ctk.CTkButton(
            parent, 
            text="",
            image=recreate_icon,
            command=self._recreate_table,
            fg_color=BTN_DANGER,
            hover_color=HOVER_ERROR,
            width=50,
            height=40, 
            corner_radius=8
        )
        recreate_btn.pack(fill="x")
    
    def _build_dashboard(self, parent):
        """Méthode obsolète - remplacée par _build_modern_dashboard"""
        pass
    
    def _build_management_filters(self, parent):
        """Construit les filtres dans la section de gestion"""
        # Titre FILTRES
        ctk.CTkLabel(parent, text="FILTRES", 
                    font=FONT_BUTTON, text_color=ACCENT_BLUE).pack(anchor="w", padx=15, pady=(15, 10))
        
        # Filtre par classe
        ctk.CTkLabel(parent, text="Classe:", 
                    font=FONT_SMALL, text_color=SOFT_BLUE).pack(anchor="w", padx=15)
        
        self.classe_var = ctk.StringVar(value="Toutes les classes")
        classe_values = ["Toutes les classes"] + [classe.get('nom', '') for classe in self.classes]
        self.classe_dropdown = ctk.CTkComboBox(parent, variable=self.classe_var,
                                              values=classe_values, command=self._on_classe_selected,
                                              font=FONT_SMALL, dropdown_font=FONT_SMALL,
                                              corner_radius=8, border_width=1, border_color=BORDER_COLOR,
                                              fg_color=BG_MAIN, button_color=ACCENT_BLUE, 
                                              button_hover_color=HOVER_PRIMARY, height=35)
        self.classe_dropdown.pack(fill="x", padx=15, pady=(5, 10))
        
        # Filtre par statut
        ctk.CTkLabel(parent, text="Statut:", 
                    font=FONT_SMALL, text_color=SOFT_BLUE).pack(anchor="w", padx=15)
        
        self.statut_var = ctk.StringVar(value="Tous les paiements")
        statut_values = ["Tous les paiements", "Élèves soldés", "En attente", "Relances"]
        self.statut_dropdown = ctk.CTkComboBox(parent, variable=self.statut_var,
                                              values=statut_values, command=self._on_statut_selected,
                                              font=FONT_SMALL, dropdown_font=FONT_SMALL,
                                              corner_radius=8, border_width=1, border_color=BORDER_COLOR,
                                              fg_color=BG_MAIN, button_color=ACCENT_BLUE, 
                                              button_hover_color=HOVER_PRIMARY, height=35)
        self.statut_dropdown.pack(fill="x", padx=15, pady=(5, 10))
        
        # Barre de recherche
        ctk.CTkLabel(parent, text="Recherche:", 
                    font=FONT_SMALL, text_color=SOFT_BLUE).pack(anchor="w", padx=15)
        
        self.search_entry = ctk.CTkEntry(parent, placeholder_text="Nom, classe, montant...",
                                        font=FONT_SMALL, height=35,
                                        corner_radius=8, border_width=1, border_color=BORDER_COLOR,
                                        fg_color=BG_MAIN, text_color=SOFT_BLUE)
        self.search_entry.pack(fill="x", padx=15, pady=(5, 15))
        self.search_entry.bind("<KeyRelease>", self._on_search_change)
    
    def _build_management_actions(self, parent):
        """Construit les actions rapides dans la section de gestion"""
        # Titre ACTIONS RAPIDES
        ctk.CTkLabel(parent, text="ACTIONS RAPIDES", 
                    font=FONT_BUTTON, text_color=ACCENT_BLUE).pack(anchor="w", padx=15, pady=(15, 10))
        
        # Boutons d'action avec design moderne
        buttons_data = [
            ("Nouveau Paiement", BTN_SUCCESS, self._show_add_payment_dialog, "add"),
            ("Échéancier", BTN_PRIMARY, self._show_echeancier, "calendar"),
            ("Remises", BTN_DANGER, self._show_remises, "discount"),
            ("Rapports", BTN_WARNING, self._show_rapports, "chart")
        ]
        
        for text, color, command, icon_name in buttons_data:
            # Charger l'icône
            icon = load_icon(icon_name, (16, 16))
            
            btn = ctk.CTkButton(
                parent,
                text=text,
                image=icon,
                command=command,
                font=FONT_SMALL,
                height=40,
                corner_radius=8,
                fg_color=color,
                hover_color=self._get_hover_color(color),
                text_color="white"
            )
            btn.pack(fill="x", padx=15, pady=5)
    
    def _build_payments_table_section(self, parent):
        """Méthode obsolète - remplacée par _build_table_section"""
        pass
    
    def _build_statistics_cards(self, parent):
        """Méthode obsolète - remplacée par _create_modern_stat_cards"""
        pass
    
    def _create_statistics_cards(self, parent):
        """Méthode obsolète - remplacée par _create_modern_stat_cards"""
        pass
    
    def _create_stat_card(self, parent, title, value, subtitle, color):
        """Méthode obsolète - remplacée par _create_modern_card"""
        pass
    
    def _build_payments_table_old(self, parent):
        """Méthode obsolète - remplacée par _build_payments_table"""
        pass
    
    def _get_hover_color(self, color):
        """Retourne la couleur de survol correspondante"""
        hover_map = {
            BTN_SUCCESS: HOVER_SUCCESS,
            BTN_PRIMARY: HOVER_PRIMARY,
            BTN_DANGER: HOVER_ERROR,
            BTN_WARNING: HOVER_WARNING
        }
        return hover_map.get(color, HOVER_PRIMARY)
    
    def _show_add_payment_dialog(self):
        """Affiche le dialogue d'ajout de paiement"""
        print("Ouverture dialogue nouveau paiement")
    
    def _show_echeancier(self):
        """Affiche l'échéancier"""
        print("Ouverture échéancier")
    
    def _show_remises(self):
        """Affiche les remises"""
        print("Ouverture remises")
    
    def _show_rapports(self):
        """Affiche les rapports"""
        print("Ouverture rapports")
    
    def _view_all_payments(self):
        """Voir tous les paiements"""
        print("Voir tous les paiements")
    
    def _calculate_statistics(self):
        """Calcule les statistiques des paiements avec le contrôleur amélioré"""
        try:
            # Utiliser le contrôleur amélioré pour les statistiques
            stats = self.enhanced_controller.get_statistiques_paiements()
            
            if stats:
                return {
                    'total_validated': int(stats.get('montant_recouvre', 0)),
                    'total_payments': stats.get('payees', 0),
                    'students_overdue': stats.get('en_retard', 0),
                    'pending_payments': stats.get('en_attente', 0),
                    'taux_recouvrement': stats.get('taux_recouvrement', 0)
                }
            else:
                # Fallback vers l'ancienne méthode
                current_month = datetime.now().month
                current_year = datetime.now().year

                # Filtrer les paiements du mois courant
                monthly_payments = []
            for paiement in self.paiements:
                try:
                    # Assumer que la date est au format string
                    if len(paiement) >= 4:  # Vérifier qu'on a assez d'éléments
                        date_str = paiement[3]  # Index 3 pour la date
                        if isinstance(date_str, str):
                            # Essayer de parser la date
                            if '-' in date_str:
                                date_obj = datetime.strptime(date_str, '%Y-%m-%d')
                            else:
                                date_obj = datetime.strptime(date_str, '%d/%m/%Y')
                            
                            if date_obj.month == current_month and date_obj.year == current_year:
                                monthly_payments.append(paiement)
                except:
                    continue
            
            # Calculer les statistiques
            total_validated = sum(float(p[2]) for p in monthly_payments if len(p) > 2 and p[5] == 'validé')  # Montant validé
            total_payments = len(monthly_payments)
            
            # Compter les paiements en attente
            pending_payments = len([p for p in monthly_payments if len(p) > 5 and p[5] == 'en_attente'])
            # Statistiques simplifiées (à améliorer selon les besoins)
            students_overdue = len(self.echeances)  # Utiliser les échéances en retard

            return {
                'total_validated': int(total_validated),
                'total_payments': total_payments,
                'students_overdue': students_overdue,
                    'pending_payments': pending_payments,
                    'taux_recouvrement': 0
            }
            
        except Exception as e:
            print(f"Erreur calcul statistiques: {e}")
            return {
                'total_validated': 0,
                'total_payments': 0,
                'students_overdue': 0,
                'pending_payments': 0,
                'taux_recouvrement': 0
            }
    
    def _display_payments(self):
        """Affiche les paiements dans le tableau"""
        if not self.table_frame:
            return
        
        # Nettoyer le frame
        for widget in self.table_frame.winfo_children():
            widget.destroy()
        
        # Filtrer les paiements
        filtered_payments = self._filter_payments()
        
        if not filtered_payments:
            # Afficher un message moderne si aucun paiement
            self._show_no_data_message()
            return
        
        # Créer le tableau avec CTkTable
        print("Utilisation du CTkTable avec design moderne")
        self._create_ctktable_modern(filtered_payments)
        
        # Ajouter la pagination
        self._add_pagination(len(filtered_payments))
    
    def _create_ctktable_modern(self, payments):
        """Crée un tableau CTkTable moderne avec design amélioré"""
        try:
            # Importer CTkTable
            from CTkTable import CTkTable
            
            # Nettoyer le frame
            for widget in self.table_frame.winfo_children():
                widget.destroy()
            
            # Préparer les données pour CTkTable
            headers = ["Élève", "Montant", "Date", "Mode", "Statut", "Référence"]
            
            # Données avec pagination
            start_idx = (self.current_page - 1) * self.items_per_page
            end_idx = start_idx + self.items_per_page
            paginated_payments = payments[start_idx:end_idx]
            
            # Préparer les lignes de données
            table_data = [headers]  # Première ligne = en-têtes
            
            for payment in paginated_payments:
                # Récupérer le nom de l'élève
                eleve_nom = self._get_eleve_name(payment[1] if len(payment) > 1 else None)
                montant = f"{payment[2]:,} GNF" if len(payment) > 2 else "0 GNF"
                date = payment[3] if len(payment) > 3 else ""
                mode = payment[4] if len(payment) > 4 else ""
                statut = payment[5] if len(payment) > 5 else "validé"
                reference = payment[6] if len(payment) > 6 else ""
                
                # Formater le statut avec emoji
                if statut == "validé":
                    statut_display = "✅ Validé"
                elif statut == "en_attente":
                    statut_display = "⏳ En attente"
                else:
                    statut_display = f"📋 {statut}"
                
                row_data = [eleve_nom, montant, date, mode, statut_display, reference]
                table_data.append(row_data)
            
            # Créer le tableau CTkTable avec design moderne
            self.table = CTkTable(
                master=self.table_frame,
                row=len(table_data),
                column=len(headers),
                values=table_data,
                # Configuration du design moderne
                header_color="#2c3e50",
                colors=["#34495e", "#2c3e50"],  # Alternance des couleurs
                hover_color="#3498db",
                text_color="#ffffff",
                font=(FONT, 11),
                corner_radius=8,
                border_width=1,
                border_color="#34495e",
                command=self._on_table_select
            )
            
            # Centrer le tableau
            self.table.pack(fill="both", expand=True, padx=10, pady=10)
            
            print(f"SUCCES - CTkTable créé avec {len(table_data)-1} lignes de données")
            
        except ImportError:
            print("ERREUR - CTkTable non disponible, utilisation du tableau simple")
            self._create_modern_table(payments)
        except Exception as e:
            print(f"ERREUR - Création CTkTable: {e}")
            self._create_modern_table(payments)
    
    def _create_modern_table(self, payments):
        """Crée un tableau moderne avec design amélioré"""
        # En-têtes du tableau
        headers = ["Élève", "Montant", "Date", "Mode", "Statut", "Référence"]
        self._create_modern_table_header(self.table_frame, headers)
        
        # Données avec pagination
        start_idx = (self.current_page - 1) * self.items_per_page
        end_idx = start_idx + self.items_per_page
        paginated_payments = payments[start_idx:end_idx]
        
        # Couleurs modernes pour les lignes
        row_colors = ["#34495e", "#2c3e50"]
        
        for i, payment in enumerate(paginated_payments):
            # Récupérer le nom de l'élève
            eleve_nom = self._get_eleve_name(payment[1] if len(payment) > 1 else None)
            montant = f"{payment[2]:,} GNF" if len(payment) > 2 else "0 GNF"
            date = payment[3] if len(payment) > 3 else ""
            mode = payment[4] if len(payment) > 4 else ""
            statut = payment[5] if len(payment) > 5 else "validé"
            reference = payment[6] if len(payment) > 6 else ""
            
            # Formater le statut avec couleur moderne
            if statut == "validé":
                statut_display = "✅ Validé"
            elif statut == "en_attente":
                statut_display = "⏳ En attente"
            else:
                statut_display = f"📋 {statut}"
            
            data = [eleve_nom, montant, date, mode, statut_display, reference]
            
            # Créer la ligne avec design moderne
            row_frame = self._create_modern_table_row(self.table_frame, data, i, row_colors)
            
            # Ajouter des effets visuels à la ligne
            self._add_row_hover_effect(row_frame)
    
    def _create_ctktable(self, payments):
        """Crée un tableau CTkTable exactement comme pour les bulletins avec le bon thème"""
        try:
            # Importer CTkTable depuis le bon module
            from CTkTable import CTkTable
            
            # Nettoyer le frame
            for widget in self.table_frame.winfo_children():
                widget.destroy()
            
            # Préparer les données pour CTkTable
            headers = ["Élève", "Montant", "Date", "Mode", "Statut", "Référence"]
            
            # Données avec pagination
            start_idx = (self.current_page - 1) * self.items_per_page
            end_idx = start_idx + self.items_per_page
            paginated_payments = payments[start_idx:end_idx]
            
            # Préparer les lignes de données
            table_data = [headers]  # Première ligne = en-têtes
            
            for payment in paginated_payments:
                # Récupérer le nom de l'élève
                eleve_nom = self._get_eleve_name(payment[1] if len(payment) > 1 else None)
                montant = f"{payment[2]:,} GNF" if len(payment) > 2 else "0 GNF"
                date = payment[3] if len(payment) > 3 else ""
                mode = payment[4] if len(payment) > 4 else ""
                statut = payment[5] if len(payment) > 5 else "validé"
                reference = payment[6] if len(payment) > 6 else ""
                
                # Formater le statut
                if statut == "validé":
                    statut_display = "Validé"
                elif statut == "en_attente":
                    statut_display = "En attente"
                else:
                    statut_display = statut
                
                row_data = [eleve_nom, montant, date, mode, statut_display, reference]
                table_data.append(row_data)
            
            # Créer le tableau CTkTable avec le bon thème EduManager+
            self.table = CTkTable(
                master=self.table_frame,
                row=len(table_data),
                column=len(headers),
                values=table_data,
                # Configuration du thème EduManager+ (comme dans les autres vues)
                header_color=BG_SIDEBAR,
                colors=[CARD_BG, BG_MAIN],  # Alternance des couleurs de fond du thème
                hover_color=BORDER_COLOR,
                text_color=TEXT_PRIMARY,
                font=(FONT, FONT_SIZE_TEXT),
                corner_radius=8,
                border_width=1,
                border_color=BORDER_COLOR,
                command=self._on_table_select
            )
            
            # Centrer le tableau avec plus d'espacement
            self.table.pack(fill="both", expand=True, padx=15, pady=15)
            
            print(f"SUCCES - CTkTable créé avec {len(table_data)-1} lignes de données")
            
        except ImportError:
            print("ERREUR - CTkTable non disponible, utilisation du tableau simple")
            self._create_simple_table(payments)
        except Exception as e:
            print(f"ERREUR - Création CTkTable: {e}")
            self._create_simple_table(payments)
    
    def _create_simple_table(self, payments):
        """Crée un tableau moderne avec design attrayant"""
        # Frame scrollable avec design moderne
        scrollable_frame = ctk.CTkScrollableFrame(self.table_frame, fg_color="transparent")
        scrollable_frame.pack(fill="both", expand=True, padx=15, pady=15)
        
        # En-têtes avec design moderne
        headers = ["Élève", "Montant", "Date", "Mode", "Statut", "Référence"]
        self._create_modern_table_header(scrollable_frame, headers)
        
        # Données avec pagination
        start_idx = (self.current_page - 1) * self.items_per_page
        end_idx = start_idx + self.items_per_page
        paginated_payments = payments[start_idx:end_idx]
        
        # Couleurs modernes pour les lignes
        row_colors = ["#34495e", "#2c3e50", "#34495e", "#2c3e50"]
        
        for i, payment in enumerate(paginated_payments):
            # Récupérer le nom de l'élève
            eleve_nom = self._get_eleve_name(payment[1] if len(payment) > 1 else None)
            montant = f"{payment[2]:,} GNF" if len(payment) > 2 else "0 GNF"
            date = payment[3] if len(payment) > 3 else ""
            mode = payment[4] if len(payment) > 4 else ""
            statut = payment[5] if len(payment) > 5 else "validé"
            reference = payment[6] if len(payment) > 6 else ""
            
            # Formater le statut avec couleur moderne
            if statut == "validé":
                statut_display = "✅ Validé"
                statut_color = "#27ae60"
            elif statut == "en_attente":
                statut_display = "⏳ En attente"
                statut_color = "#f39c12"
            else:
                statut_display = f"📋 {statut}"
                statut_color = "#95a5a6"
            
            data = [eleve_nom, montant, date, mode, statut_display, reference]
            
            # Créer la ligne avec design moderne
            row_frame = self._create_modern_table_row(scrollable_frame, data, i, row_colors)
            
            # Ajouter des effets visuels à la ligne
            self._add_row_hover_effect(row_frame)
    
    def _add_row_hover_effect(self, row_frame):
        """Ajoute un effet de survol moderne aux lignes du tableau"""
        try:
            original_color = row_frame.cget("fg_color")
            
            def on_enter(event):
                # Effet de survol avec couleur plus claire
                row_frame.configure(fg_color=self._lighten_color(original_color))
                row_frame.configure(cursor="hand2")
            
            def on_leave(event):
                row_frame.configure(fg_color=original_color)
                row_frame.configure(cursor="arrow")
            
            row_frame.bind("<Enter>", on_enter)
            row_frame.bind("<Leave>", on_leave)
            
        except Exception as e:
            print(f"Erreur effet survol ligne: {e}")
    
    def _show_no_data_message(self):
        """Affiche un message moderne quand il n'y a pas de données"""
        # Container pour le contenu
        content_frame = ctk.CTkFrame(self.table_frame, fg_color=CARD_BG, corner_radius=20)
        content_frame.pack(expand=True, fill="both", padx=50, pady=50)
        
        # Icône moderne
        icon_label = ctk.CTkLabel(content_frame, text="💳", 
                                font=(FONT, 48), text_color=ACCENT_BLUE)
        icon_label.pack(pady=(30, 20))
        
        # Titre principal
        title_label = ctk.CTkLabel(content_frame, text="Aucun paiement trouvé", 
                                 font=(FONT, 24, "bold"), text_color=TEXT_PRIMARY)
        title_label.pack(pady=(0, 10))
        
        # Message descriptif
        desc_label = ctk.CTkLabel(content_frame, 
                                text="Aucun paiement ne correspond à vos critères de recherche.\n"
                                     "Essayez de modifier vos filtres ou ajoutez un nouveau paiement.",
                                font=(FONT, 14), text_color=TEXT_SECONDARY,
                                justify="center")
        desc_label.pack(pady=(0, 30))
        
        # Bouton d'action
        action_btn = ctk.CTkButton(content_frame, text="➕ Ajouter un paiement",
                                 font=(FONT, 14, "bold"), height=40,
                                 fg_color=BTN_SUCCESS, hover_color=HOVER_SUCCESS,
                                 command=self._show_add_payment_dialog)
        action_btn.pack(pady=(0, 30))
    
    def _get_eleve_name(self, eleve_id):
        """Récupère le nom d'un élève par son ID"""
        if not eleve_id:
            return "Inconnu"
        
        try:
            for eleve in self.eleves:
                # Vérifier si c'est un tuple ou une liste
                if isinstance(eleve, (tuple, list)) and len(eleve) > 0:
                    if eleve[0] == eleve_id:
                        if len(eleve) >= 3:
                            return f"{eleve[1]} {eleve[2]}"  # nom prenom
                        elif len(eleve) >= 2:
                            return str(eleve[1])
                # Vérifier si c'est un dictionnaire
                elif isinstance(eleve, dict):
                    if eleve.get('id_eleve') == eleve_id:
                        nom = eleve.get('nom', '')
                        prenom = eleve.get('prenom', '')
                        if nom and prenom:
                            return f"{nom} {prenom}"
                        elif nom:
                            return nom
        except Exception as e:
            print(f"Erreur récupération nom élève {eleve_id}: {e}")
        
        return f"Élève {eleve_id}"
    
    def _get_eleve_classe_name(self, eleve_id):
        """Récupère le nom de la classe d'un élève"""
        if not eleve_id:
            return "Classe inconnue"
        
        try:
            for eleve in self.eleves:
                # Vérifier si c'est un tuple ou une liste
                if isinstance(eleve, (tuple, list)) and len(eleve) > 0:
                    if eleve[0] == eleve_id:
                        # Chercher la classe dans la liste des classes
                        if len(eleve) > 3:  # Si l'ID classe est disponible
                            classe_id = eleve[3]
                            for classe in self.classes:
                                if isinstance(classe, dict) and classe.get('id') == classe_id:
                                    return classe.get('nom', 'Classe inconnue')
                        return "Classe non définie"
                # Vérifier si c'est un dictionnaire
                elif isinstance(eleve, dict):
                    if eleve.get('id_eleve') == eleve_id:
                        classe_id = eleve.get('id_classe')
                        if classe_id:
                            for classe in self.classes:
                                if isinstance(classe, dict) and classe.get('id') == classe_id:
                                    return classe.get('nom', 'Classe inconnue')
                        return "Classe non définie"
        except Exception as e:
            print(f"Erreur récupération classe élève {eleve_id}: {e}")
        
        return "Classe inconnue"
    
    def _filter_payments(self):
        """Filtre les paiements selon les critères"""
        filtered = self.paiements.copy()
        
        # Filtrer par classe
        if self.selected_classe and self.selected_classe != "Toutes les classes":
            # Logique de filtrage par classe (à implémenter selon la structure des données)
            pass
        
        # Filtrer par statut
        if self.selected_statut and self.selected_statut != "Tous les paiements":
            # Logique de filtrage par statut (à implémenter)
            pass
        
        # Filtrer par recherche textuelle
        if self.search_text:
            search_lower = self.search_text.lower()
            filtered = [p for p in filtered if 
                       search_lower in str(p).lower()]
        
        return filtered
    
    def _add_pagination(self, total_items):
        """Ajoute la pagination sous le tableau avec meilleur espacement"""
        # Calculer le nombre total de pages
        self.total_pages = max(1, (total_items + self.items_per_page - 1) // self.items_per_page)
        
        # Frame de pagination avec le thème EduManager+
        pagination_frame = ctk.CTkFrame(self.table_frame, fg_color=CARD_BG, corner_radius=12, height=70)
        pagination_frame.pack(fill="x", padx=15, pady=(15, 15))
        pagination_frame.pack_propagate(False)
        
        # Container principal pour la pagination
        main_container = ctk.CTkFrame(pagination_frame, fg_color="transparent")
        main_container.pack(expand=True, fill="both", padx=20, pady=15)
        
        # Informations de pagination avec le thème
        start_item = (self.current_page - 1) * self.items_per_page + 1
        end_item = min(self.current_page * self.items_per_page, total_items)
        info_text = f"Affichage {start_item}-{end_item} sur {total_items} paiements"
        
        info_label = ctk.CTkLabel(main_container, text=info_text, 
                                 font=FONT_SMALL, text_color=TEXT_PRIMARY)
        info_label.pack(side="left")
        
        # Contrôles de pagination avec le thème
        controls_frame = ctk.CTkFrame(main_container, fg_color="transparent")
        controls_frame.pack(side="right")
        
        # Bouton précédent avec le thème
        prev_icon = load_icon('chevron_left', (18, 18))
        prev_btn = ctk.CTkButton(controls_frame, text="◀" if prev_icon is None else "",
                                image=prev_icon,
                                command=self._prev_page, 
                                fg_color=BTN_PRIMARY,
                                hover_color=HOVER_PRIMARY, 
                                width=45, height=40,
                                corner_radius=8,
                                border_width=1,
                                border_color=BORDER_COLOR)
        prev_btn.pack(side="left", padx=(0, 10))
        
        # Numéro de page avec le thème
        page_frame = ctk.CTkFrame(controls_frame, fg_color=BG_SIDEBAR, corner_radius=8, width=60, height=40)
        page_frame.pack(side="left", padx=5)
        page_frame.pack_propagate(False)
        
        page_label = ctk.CTkLabel(page_frame, text=f"{self.current_page}/{self.total_pages}",
                                 font=FONT_SMALL, text_color=TEXT_PRIMARY)
        page_label.pack(expand=True, fill="both")
        
        # Bouton suivant avec le thème
        next_icon = load_icon('chevron_right', (18, 18))
        next_btn = ctk.CTkButton(controls_frame, text="▶" if next_icon is None else "",
                                image=next_icon,
                                command=self._next_page, 
                                fg_color=BTN_PRIMARY,
                                hover_color=HOVER_PRIMARY, 
                                width=45, height=40,
                                corner_radius=8,
                                border_width=1,
                                border_color=BORDER_COLOR)
        next_btn.pack(side="left", padx=(10, 0))
        
        # Désactiver les boutons si nécessaire
        prev_btn.configure(state="disabled" if self.current_page <= 1 else "normal")
        next_btn.configure(state="disabled" if self.current_page >= self.total_pages else "normal")
    
    def _prev_page(self):
        """Page précédente"""
        if self.current_page > 1:
            self.current_page -= 1
            self._display_payments()
    
    def _next_page(self):
        """Page suivante"""
        if self.current_page < self.total_pages:
            self.current_page += 1
            self._display_payments()
    
    def _on_table_select(self, data):
        """Gestionnaire de sélection sur le tableau CTkTable"""
        if data["row"] > 0:  # Ignorer l'en-tête
            row_index = data["row"] - 1  # Ajuster pour l'index des données
            col_index = data["column"]
            
            # Récupérer les paiements filtrés
            filtered_payments = self._filter_payments()
            
            # Calculer l'index avec pagination
            start_idx = (self.current_page - 1) * self.items_per_page
            actual_index = start_idx + row_index
            
            if 0 <= actual_index < len(filtered_payments):
                payment = filtered_payments[actual_index]
                print(f"Paiement sélectionné: {payment}")
                
                # Afficher les détails du paiement
                self._show_payment_details(payment)
    
    def _show_payment_details(self, payment):
        """Affiche les détails d'un paiement sélectionné"""
        try:
            # Créer une fenêtre de détails
            details_window = ctk.CTkToplevel(self)
            details_window.title("Détails du Paiement")
            details_window.geometry("500x400")
            details_window.transient(self)
            details_window.grab_set()
            
            # Centrer la fenêtre
            details_window.update_idletasks()
            x = (details_window.winfo_screenwidth() // 2) - (500 // 2)
            y = (details_window.winfo_screenheight() // 2) - (400 // 2)
            details_window.geometry(f"500x400+{x}+{y}")
            
            # Frame principal
            main_frame = ctk.CTkFrame(details_window, fg_color=CARD_BG, corner_radius=12)
            main_frame.pack(fill="both", expand=True, padx=15, pady=15)
            
            # Titre
            title_frame = ctk.CTkFrame(main_frame, fg_color=ACCENT_BLUE, corner_radius=8)
            title_frame.pack(fill="x", pady=(0, 20))
            
            ctk.CTkLabel(title_frame, text="📋 DÉTAILS DU PAIEMENT", 
                        font=(FONT, 16, "bold"), text_color="white", fg_color=ACCENT_BLUE).pack(pady=15)
            
            # Contenu des détails
            content_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
            content_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))
            
            # Informations du paiement
            eleve_nom = self._get_eleve_name(payment[1] if len(payment) > 1 else None)
            montant = f"{payment[2]:,} GNF" if len(payment) > 2 else "0 GNF"
            date = payment[3] if len(payment) > 3 else ""
            mode = payment[4] if len(payment) > 4 else ""
            statut = payment[5] if len(payment) > 5 else "validé"
            reference = payment[6] if len(payment) > 6 else ""
            
            # Afficher les détails
            details = [
                ("👤 Élève:", eleve_nom),
                ("💰 Montant:", montant),
                ("📅 Date:", date),
                ("💳 Mode:", mode),
                ("📊 Statut:", statut),
                ("🔗 Référence:", reference)
            ]
            
            for label, value in details:
                detail_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
                detail_frame.pack(fill="x", pady=5)
                
                ctk.CTkLabel(detail_frame, text=label, 
                           font=(FONT, 12, "bold"), text_color=TEXT_PRIMARY).pack(side="left")
                ctk.CTkLabel(detail_frame, text=value, 
                           font=(FONT, 12), text_color=TEXT_SECONDARY).pack(side="right")
            
            # Boutons d'action
            buttons_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
            buttons_frame.pack(fill="x", pady=(20, 0))
            
            # Bouton Modifier
            edit_btn = ctk.CTkButton(buttons_frame, text="✏️ Modifier",
                                   font=(FONT, 12, "bold"), height=35,
                                   fg_color=BTN_WARNING, hover_color=HOVER_WARNING,
                                   command=lambda: self._edit_payment(payment, details_window))
            edit_btn.pack(side="left", padx=(0, 10))
            
            # Bouton Fermer
            close_btn = ctk.CTkButton(buttons_frame, text="❌ Fermer",
                                    font=(FONT, 12, "bold"), height=35,
                                    fg_color=BTN_SECONDARY, hover_color=HOVER_SECONDARY,
                                    command=details_window.destroy)
            close_btn.pack(side="right")
            
        except Exception as e:
            print(f"Erreur affichage détails paiement: {e}")
            messagebox.showerror("Erreur", f"Erreur lors de l'affichage des détails:\n{str(e)}")
    
    def _edit_payment(self, payment, parent_window):
        """Ouvre le formulaire de modification d'un paiement"""
        parent_window.destroy()
        self._open_payment_form("Modifier", payment)
    
    def _on_table_click(self, data):
        """Gestionnaire de clic sur le tableau"""
        if data["row"] > 0:  # Ignorer l'en-tête
            print(f"Paiement sélectionné: ligne {data['row']}, colonne {data['column']}")
    
    # Méthodes de gestion des événements
    def _on_classe_selected(self, choice):
        """Gestionnaire de sélection de classe"""
        self.selected_classe = choice
        self.current_page = 1
        self._display_payments()
    
    def _on_statut_selected(self, choice):
        """Gestionnaire de sélection de statut"""
        self.selected_statut = choice
        self.current_page = 1
        self._display_payments()
    
    def _on_search_change(self, event):
        """Gestionnaire de changement de recherche"""
        self.search_text = self.search_entry.get()
        self.current_page = 1
        self._display_payments()
    
    def _apply_quick_filter(self, filter_type):
        """Applique un filtre rapide"""
        # Mettre à jour les variables de filtre
        if filter_type == "all":
            self.selected_statut = None
        elif filter_type == "paid":
            self.selected_statut = "Élèves soldés"
        elif filter_type == "reminders":
            self.selected_statut = "Relances"
        
        # Mettre à jour les dropdowns
        self.statut_dropdown.set(self.selected_statut or "Tous les paiements")
        
        # Réinitialiser la pagination et afficher
        self.current_page = 1
        self._display_payments()
    
    # Méthodes d'action
    def _add_payment(self):
        """Ouvre le formulaire d'ajout de paiement"""
        self._open_payment_form("Ajouter")
    
    def _export_payments(self):
        """Exporte les paiements"""
        messagebox.showinfo("Information", "Export des paiements - À implémenter")
    
    def _refresh_data(self):
        """Actualise les données"""
        try:
            self._load_data()
            self._update_dashboard()
            self._display_payments()
            print("SUCCES - Données actualisées avec succès !")
        except Exception as e:
            print(f"ERREUR - Erreur lors de l'actualisation : {str(e)}")
    
    def _show_statistics(self):
        """Affiche les statistiques détaillées"""
        messagebox.showinfo("Information", "Statistiques détaillées - À implémenter")
    
    def _show_all_payments(self):
        """Affiche tous les paiements"""
        messagebox.showinfo("Information", "Vue complète des paiements - À implémenter")
    
    def _recreate_table(self):
        """Recrée la table paiements avec des données de test"""
        result = messagebox.askyesno(
            "Recréer la table", 
            "Voulez-vous recréer la table paiements ?\n\n"
            "Cette action va :\n"
            "• Supprimer la table existante\n"
            "• Créer une nouvelle table\n"
            "• Insérer des données de test\n\n"
            "ATTENTION - Toutes les données existantes seront perdues !"
        )
        
        if result:
            try:
                # Recréer la table
                if create_table_paiements():
                    # Insérer des données de test
                    insert_sample_payments()
                    
                    # Actualiser les données
                    self._refresh_data()
                    
                    messagebox.showinfo("Succès", 
                                      "Table paiements recréée avec succès !\n"
                                      "Des données de test ont été ajoutées.")
                else:
                    messagebox.showerror("Erreur", "Erreur lors de la recréation de la table.")
                    
            except Exception as e:
                messagebox.showerror("Erreur", f"Erreur lors de la recréation:\n{str(e)}")
    
    def _show_echeancier(self):
        """Affiche la vue des échéanciers"""
        # Créer une fenêtre pour les échéanciers
        echeancier_window = ctk.CTkToplevel(self)
        echeancier_window.title("Gestion des Échéanciers")
        echeancier_window.geometry("1200x800")
        echeancier_window.transient(self)
        echeancier_window.grab_set()
        
        # Centrer la fenêtre
        echeancier_window.update_idletasks()
        x = (echeancier_window.winfo_screenwidth() // 2) - (1200 // 2)
        y = (echeancier_window.winfo_screenheight() // 2) - (800 // 2)
        echeancier_window.geometry(f"1200x800+{x}+{y}")
        
        # Frame principal
        main_frame = ctk.CTkFrame(echeancier_window, fg_color=BG_MAIN)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Titre
        title_frame = ctk.CTkFrame(main_frame, fg_color=ACCENT, corner_radius=8)
        title_frame.pack(fill="x", pady=(0, 20))
        
        calendar_icon = load_icon('calendar', (24, 24))
        if calendar_icon:
            ctk.CTkLabel(title_frame, text="", image=calendar_icon, fg_color=ACCENT).pack(side="left", padx=(0, 10))
        
        ctk.CTkLabel(title_frame, text="Gestion des Échéanciers", 
                    font=FONT_SUBTITLE, text_color="white", fg_color=ACCENT).pack(side="left")
        
        # Contenu des échéanciers
        content_frame = ctk.CTkFrame(main_frame, fg_color=CARD_BG, corner_radius=12)
        content_frame.pack(fill="both", expand=True)
        
        # Message d'information
        info_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        info_frame.pack(expand=True, fill="both")
        
        ctk.CTkLabel(info_frame, text="📅 Échéanciers de Paiement", 
                    font=FONT_TITLE, text_color=TEXT_PRIMARY).pack(pady=(50, 20))
        
        ctk.CTkLabel(info_frame, text="Cette section permet de gérer :", 
                    font=FONT_SECONDARY, text_color=TEXT_SECONDARY).pack(pady=(0, 20))
        
        # Liste des fonctionnalités
        features = [
            "• Génération automatique des échéances",
            "• Suivi des paiements par élève",
            "• Gestion des retards et pénalités",
            "• Relances automatiques",
            "• Rapports de recouvrement",
            "• Échéanciers par classe et niveau"
        ]
        
        for feature in features:
            ctk.CTkLabel(info_frame, text=feature, 
                        font=FONT_SECONDARY, text_color=TEXT_PRIMARY).pack(pady=5)
        
        # Bouton de fermeture (icône uniquement)
        close_icon = load_icon('close', (18, 18))
        close_btn = ctk.CTkButton(info_frame, text="", image=close_icon,
                                 command=echeancier_window.destroy,
                                 fg_color=BTN_SECONDARY, hover_color=HOVER_SECONDARY,
                                 width=45, height=40, corner_radius=8)
        close_btn.pack(pady=(30, 0))
    
    def _show_remises(self):
        """Affiche la vue des remises et bourses"""
        # Créer une fenêtre pour les remises
        remises_window = ctk.CTkToplevel(self)
        remises_window.title("Gestion des Remises et Bourses")
        remises_window.geometry("1000x700")
        remises_window.transient(self)
        remises_window.grab_set()
        
        # Centrer la fenêtre
        remises_window.update_idletasks()
        x = (remises_window.winfo_screenwidth() // 2) - (1000 // 2)
        y = (remises_window.winfo_screenheight() // 2) - (700 // 2)
        remises_window.geometry(f"1000x700+{x}+{y}")
        
        # Frame principal
        main_frame = ctk.CTkFrame(remises_window, fg_color=BG_MAIN)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Titre
        title_frame = ctk.CTkFrame(main_frame, fg_color=ACCENT, corner_radius=8)
        title_frame.pack(fill="x", pady=(0, 20))
        
        analytics_icon = load_icon('analytics', (24, 24))
        if analytics_icon:
            ctk.CTkLabel(title_frame, text="", image=analytics_icon, fg_color=ACCENT).pack(side="left", padx=(0, 10))
        
        ctk.CTkLabel(title_frame, text="Gestion des Remises et Bourses", 
                    font=FONT_SUBTITLE, text_color="white", fg_color=ACCENT).pack(side="left")
        
        # Contenu des remises
        content_frame = ctk.CTkFrame(main_frame, fg_color=CARD_BG, corner_radius=12)
        content_frame.pack(fill="both", expand=True)
        
        # Message d'information
        info_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        info_frame.pack(expand=True, fill="both")
        
        ctk.CTkLabel(info_frame, text=" Remises et Bourses", 
                    font=FONT_TITLE, text_color=TEXT_PRIMARY).pack(pady=(50, 20))
        
        ctk.CTkLabel(info_frame, text="Cette section permet de gérer :", 
                    font=FONT_SECONDARY, text_color=TEXT_SECONDARY).pack(pady=(0, 20))
        
        # Liste des fonctionnalités
        features = [
            "• Bourses d'excellence",
            "• Réductions pour familles nombreuses",
            "• Aides sociales",
            "• Exonérations temporaires",
            "• Remises par pourcentage ou montant fixe",
            "• Suivi des justificatifs"
        ]
        
        for feature in features:
            ctk.CTkLabel(info_frame, text=feature, 
                        font=FONT_SECONDARY, text_color=TEXT_PRIMARY).pack(pady=5)
        
        # Bouton de fermeture (icône uniquement)
        close_icon = load_icon('close', (18, 18))
        close_btn = ctk.CTkButton(info_frame, text="", image=close_icon,
                                 command=remises_window.destroy,
                                 fg_color=BTN_SECONDARY, hover_color=HOVER_SECONDARY,
                                 width=45, height=40, corner_radius=8)
        close_btn.pack(pady=(30, 0))
    
    def _show_expenses(self):
        """Affiche la vue des dépenses (sorties d'argent)"""
        # Créer une fenêtre pour les dépenses
        expenses_window = ctk.CTkToplevel(self)
        expenses_window.title("Gestion des Dépenses")
        expenses_window.geometry("1000x700")
        expenses_window.transient(self)
        expenses_window.grab_set()
        
        # Centrer la fenêtre
        expenses_window.update_idletasks()
        x = (expenses_window.winfo_screenwidth() // 2) - (1000 // 2)
        y = (expenses_window.winfo_screenheight() // 2) - (700 // 2)
        expenses_window.geometry(f"1000x700+{x}+{y}")
        
        # Frame principal
        main_frame = ctk.CTkFrame(expenses_window, fg_color=BG_MAIN)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Titre
        title_frame = ctk.CTkFrame(main_frame, fg_color=ACCENT, corner_radius=8)
        title_frame.pack(fill="x", pady=(0, 20))
        
        expenses_icon = load_icon('trending_up', (24, 24))
        if expenses_icon:
            ctk.CTkLabel(title_frame, text="", image=expenses_icon, fg_color=ACCENT).pack(side="left", padx=(0, 10))
        
        ctk.CTkLabel(title_frame, text="Gestion des Dépenses", 
                    font=FONT_SUBTITLE, text_color="white", fg_color=ACCENT).pack(side="left")
        
        # Contenu des dépenses
        content_frame = ctk.CTkFrame(main_frame, fg_color=CARD_BG, corner_radius=12)
        content_frame.pack(fill="both", expand=True)
        
        # Message d'information
        info_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        info_frame.pack(expand=True, fill="both")
        
        ctk.CTkLabel(info_frame, text=" Gestion des Dépenses", 
                    font=FONT_TITLE, text_color=TEXT_PRIMARY).pack(pady=(50, 20))
        
        ctk.CTkLabel(info_frame, text="Cette section permettra de gérer :", 
                    font=FONT_SECONDARY, text_color=TEXT_SECONDARY).pack(pady=(0, 20))
        
        # Liste des fonctionnalités
        features = [
            "• Salaires du personnel",
            "• Frais de maintenance",
            "• Achat de matériel scolaire",
            "• Frais de transport",
            "• Dépenses administratives",
            "• Autres charges"
        ]
        
        for feature in features:
            ctk.CTkLabel(info_frame, text=feature, 
                        font=FONT_SECONDARY, text_color=TEXT_PRIMARY).pack(pady=5)
        
        # Bouton de fermeture (icône uniquement)
        close_icon = load_icon('close', (18, 18))
        close_btn = ctk.CTkButton(info_frame, text="", image=close_icon,
                                 command=expenses_window.destroy,
                                 fg_color=BTN_SECONDARY, hover_color=HOVER_SECONDARY,
                                 width=45, height=40, corner_radius=8)
        close_btn.pack(pady=(30, 0))

    def _show_reports(self):
        """Affiche la fenêtre des rapports"""
        reports_window = ctk.CTkToplevel(self)
        reports_window.title("Rapports Financiers")
        reports_window.geometry("900x700")
        reports_window.transient(self)
        reports_window.grab_set()
        
        # Centrer la fenêtre
        reports_window.update_idletasks()
        x = (reports_window.winfo_screenwidth() // 2) - (900 // 2)
        y = (reports_window.winfo_screenheight() // 2) - (700 // 2)
        reports_window.geometry(f"900x700+{x}+{y}")
        
        # Titre
        title_label = ctk.CTkLabel(reports_window, text=" Rapports Financiers", 
                                 font=(FONT, FONT_SIZE_TITLE, "bold"), text_color=TEXT_PRIMARY)
        title_label.pack(pady=20)
        
        # Contenu temporaire
        content_label = ctk.CTkLabel(reports_window, 
                                   text="Cette fonctionnalité sera disponible dans une prochaine version.\n\n"
                                        "Elle permettra de générer :\n"
                                        "• Rapports de recouvrement\n"
                                        "• Statistiques par classe\n"
                                        "• Historique des paiements\n"
                                        "• Échéances en retard",
                                   font=(FONT, FONT_SIZE_TEXT), text_color=TEXT_SECONDARY,
                                   justify="left")
        content_label.pack(pady=20, padx=40)
        
        # Bouton fermer
        close_btn = ctk.CTkButton(reports_window, text="Fermer", command=reports_window.destroy,
                                font=(FONT, FONT_SIZE_TEXT), height=35)
        close_btn.pack(pady=20)

    def _show_settings(self):
        """Affiche la fenêtre des paramètres"""
        settings_window = ctk.CTkToplevel(self)
        settings_window.title("Paramètres du Système")
        settings_window.geometry("600x500")
        settings_window.transient(self)
        settings_window.grab_set()
        
        # Centrer la fenêtre
        settings_window.update_idletasks()
        x = (settings_window.winfo_screenwidth() // 2) - (600 // 2)
        y = (settings_window.winfo_screenheight() // 2) - (500 // 2)
        settings_window.geometry(f"600x500+{x}+{y}")
        
        # Titre
        title_label = ctk.CTkLabel(settings_window, text=" Paramètres du Système", 
                                 font=(FONT, FONT_SIZE_TITLE, "bold"), text_color=TEXT_PRIMARY)
        title_label.pack(pady=20)
        
        # Contenu temporaire
        content_label = ctk.CTkLabel(settings_window, 
                                   text="Cette fonctionnalité sera disponible dans une prochaine version.\n\n"
                                        "Elle permettra de configurer :\n"
                                        "• Types de frais scolaires\n"
                                        "• Paramètres de relances\n"
                                        "• Configuration des rapports\n"
                                        "• Préférences d'affichage",
                                   font=(FONT, FONT_SIZE_TEXT), text_color=TEXT_SECONDARY,
                                   justify="left")
        content_label.pack(pady=20, padx=40)
        
        # Bouton fermer
        close_btn = ctk.CTkButton(settings_window, text="Fermer", command=settings_window.destroy,
                                font=(FONT, FONT_SIZE_TEXT), height=35)
        close_btn.pack(pady=20)

    def _validate_payments(self):
        """Valide les paiements en attente"""
        try:
            # Logique de validation des paiements
            print("SUCCES - Validation des paiements en cours...")
            messagebox.showinfo("Information", "Fonctionnalité de validation en cours de développement")
        except Exception as e:
            print(f"ERREUR - Erreur validation: {str(e)}")

    def _show_relances(self):
        """Affiche la fenêtre des relances"""
        relances_window = ctk.CTkToplevel(self)
        relances_window.title("Gestion des Relances")
        relances_window.geometry("800x600")
        relances_window.transient(self)
        relances_window.grab_set()
        
        # Centrer la fenêtre
        relances_window.update_idletasks()
        x = (relances_window.winfo_screenwidth() // 2) - (800 // 2)
        y = (relances_window.winfo_screenheight() // 2) - (600 // 2)
        relances_window.geometry(f"800x600+{x}+{y}")
        
        # Titre
        title_label = ctk.CTkLabel(relances_window, text=" Gestion des Relances", 
                                 font=(FONT, FONT_SIZE_TITLE, "bold"), text_color=TEXT_PRIMARY)
        title_label.pack(pady=20)
        
        # Contenu temporaire
        content_label = ctk.CTkLabel(relances_window, 
                                   text="Cette fonctionnalité sera disponible dans une prochaine version.\n\n"
                                        "Elle permettra de :\n"
                                        "• Envoyer des relances automatiques\n"
                                        "• Gérer les échéances en retard\n"
                                        "• Configurer les délais de paiement\n"
                                        "• Suivre l'historique des relances",
                                   font=(FONT, FONT_SIZE_TEXT), text_color=TEXT_SECONDARY,
                                   justify="left")
        content_label.pack(pady=20, padx=40)
        
        # Bouton fermer
        close_btn = ctk.CTkButton(relances_window, text="Fermer", command=relances_window.destroy,
                                font=(FONT, FONT_SIZE_TEXT), height=35)
        close_btn.pack(pady=20)

    def _show_add_payment_dialog(self):
        """Affiche la fenêtre d'ajout de paiement"""
        try:
            # Utiliser la méthode existante _open_payment_form
            self._open_payment_form("add")
        except Exception as e:
            print(f"ERREUR - Erreur ouverture dialogue paiement: {str(e)}")
            # Fallback simple
            messagebox.showinfo("Information", "Fonctionnalité d'ajout de paiement en cours de développement")
    
    def _update_dashboard(self):
        """Met à jour le dashboard avec les nouvelles statistiques"""
        # Recalculer les statistiques
        stats_data = self._calculate_statistics()
        
        # Mettre à jour les cartes de statistiques modernes
        if hasattr(self, 'modern_stats_cards') and self.modern_stats_cards:
            # Détruire les anciennes cartes
            for card in self.modern_stats_cards:
                card.destroy()
            
            # Recréer les cartes avec les nouvelles données
            cards_frame = self.modern_stats_cards[0].master if self.modern_stats_cards else None
            if cards_frame:
                self.modern_stats_cards = []
                self._create_modern_stat_cards(cards_frame, stats_data)

    # Méthodes de compatibilité pour l'ancienne interface
    def charger_paiements(self):
        """Méthode de compatibilité - charge les paiements"""
        self._refresh_data()

    def ajouter_paiement(self):
        """Méthode de compatibilité - ouvre le formulaire d'ajout"""
        self._add_payment()

    def modifier_paiement(self):
        """Méthode de compatibilité - ouvre le formulaire de modification"""
        messagebox.showinfo("Information", "Sélectionnez un paiement dans le tableau pour le modifier.")

    def supprimer_paiement(self):
        """Méthode de compatibilité - supprime un paiement"""
        messagebox.showinfo("Information", "Sélectionnez un paiement dans le tableau pour le supprimer.")
    
    def _open_payment_form(self, mode, payment_data=None):
        """Ouvre le formulaire d'ajout/modification de paiement"""
        # Créer une fenêtre modale
        form_window = ctk.CTkToplevel(self)
        form_window.title(f"{mode} un Paiement")
        form_window.geometry("500x600")
        form_window.resizable(False, False)
        form_window.transient(self)
        form_window.grab_set()
        
        # Centrer la fenêtre
        form_window.update_idletasks()
        x = (form_window.winfo_screenwidth() // 2) - (500 // 2)
        y = (form_window.winfo_screenheight() // 2) - (600 // 2)
        form_window.geometry(f"500x600+{x}+{y}")
        
        # Frame principal avec scroll
        main_frame = ctk.CTkScrollableFrame(form_window, fg_color=CARD_BG, corner_radius=12)
        main_frame.pack(fill="both", expand=True, padx=15, pady=15)
        
        # En-tête avec design moderne
        header_frame = ctk.CTkFrame(main_frame, fg_color=ACCENT, corner_radius=12)
        header_frame.pack(fill="x", pady=(0, 20))
        
        # Titre avec icône
        title_frame = ctk.CTkFrame(header_frame, fg_color=ACCENT)
        title_frame.pack(expand=True, fill="x", padx=20, pady=15)
        
        # Icône du formulaire
        add_icon = load_icon('add', (24, 24))
        if add_icon:
            ctk.CTkLabel(title_frame, text="", image=add_icon, fg_color=ACCENT).pack(side="left", padx=(0, 10))
        
        title_text = "NOUVEAU PAIEMENT" if mode == "Ajouter" else "MODIFIER PAIEMENT"
        title = ctk.CTkLabel(title_frame, text=title_text,
                            font=FONT_SUBTITLE, text_color="white", fg_color=ACCENT)
        title.pack(side="left")
        
        # Formulaire avec sections organisées
        form_frame = ctk.CTkFrame(main_frame, fg_color=CARD_BG)
        form_frame.pack(fill="both", expand=True)
        
        # Variables du formulaire
        var_eleve = ctk.StringVar()
        var_montant = ctk.StringVar()
        var_date = ctk.StringVar()
        var_mode = ctk.StringVar()
        var_description = ctk.StringVar()
        
        # Section 1: Informations de base
        basic_section = ctk.CTkFrame(form_frame, fg_color=CARD_BG, corner_radius=8)
        basic_section.pack(fill="x", padx=15, pady=(15, 10))
        
        basic_title = ctk.CTkLabel(basic_section, text="INFORMATIONS DE BASE",
                                  font=FONT_BUTTON, text_color=TEXT_ACCENT, fg_color=CARD_BG)
        basic_title.pack(anchor="w", padx=15, pady=(15, 10))
        
        # Élève
        ctk.CTkLabel(basic_section, text="Élève *", 
                    font=FONT_SECONDARY, text_color=TEXT_PRIMARY).pack(anchor="w", padx=15)
        
        # Récupérer les élèves avec leurs classes
        eleves_choices = ["Sélectionner un élève..."]
        try:
            for eleve in self.eleves:
                if isinstance(eleve, (tuple, list)) and len(eleve) >= 3:
                    # Format: "Nom Prénom (Classe) - ID: X"
                    classe_nom = self._get_eleve_classe_name(eleve[0])
                    eleves_choices.append(f"{eleve[1]} {eleve[2]} ({classe_nom}) - ID: {eleve[0]}")
                elif isinstance(eleve, dict):
                    nom = eleve.get('nom', '')
                    prenom = eleve.get('prenom', '')
                    eleve_id = eleve.get('id_eleve', '')
                    classe_nom = self._get_eleve_classe_name(eleve_id)
                    if nom and prenom:
                        eleves_choices.append(f"{nom} {prenom} ({classe_nom}) - ID: {eleve_id}")
        except Exception as e:
            print(f"Erreur récupération élèves pour formulaire: {e}")
            pass
        
        eleve_dropdown = ctk.CTkComboBox(basic_section, variable=var_eleve,
                                        values=eleves_choices, state="readonly",
                                        font=FONT_SECONDARY, dropdown_font=FONT_SECONDARY,
                                        corner_radius=8, border_width=1, border_color=BORDER_COLOR,
                                        fg_color=CARD_BG, button_color=ACCENT, 
                                        button_hover_color=HOVER_PRIMARY, height=35)
        eleve_dropdown.pack(fill="x", padx=15, pady=(5, 15))
        
        # Montant
        ctk.CTkLabel(basic_section, text="Montant (GNF) *", 
                    font=FONT_SECONDARY, text_color=TEXT_PRIMARY).pack(anchor="w", padx=15)
        
        montant_entry = ctk.CTkEntry(basic_section, textvariable=var_montant,
                                    placeholder_text="Ex: 500000",
                                    font=FONT_SECONDARY, height=35,
                                    corner_radius=8, border_width=1, border_color=BORDER_COLOR)
        montant_entry.pack(fill="x", padx=15, pady=(5, 15))
        
        # Date
        ctk.CTkLabel(basic_section, text="Date de paiement *", 
                    font=FONT_SECONDARY, text_color=TEXT_PRIMARY).pack(anchor="w", padx=15)
        
        date_entry = ctk.CTkEntry(basic_section, textvariable=var_date,
                                 placeholder_text="YYYY-MM-DD",
                                 font=FONT_SECONDARY, height=35,
                                 corner_radius=8, border_width=1, border_color=BORDER_COLOR)
        date_entry.pack(fill="x", padx=15, pady=(5, 15))
        
        # Mode de paiement
        ctk.CTkLabel(basic_section, text="Mode de paiement *", 
                    font=FONT_SECONDARY, text_color=TEXT_PRIMARY).pack(anchor="w", padx=15)
        
        mode_dropdown = ctk.CTkComboBox(basic_section, variable=var_mode,
                                       values=["Espèces", "Chèque", "Mobile Money", "Carte Bancaire", "Virement"],
                                       state="readonly",
                                       font=FONT_SECONDARY, dropdown_font=FONT_SECONDARY,
                                       corner_radius=8, border_width=1, border_color=BORDER_COLOR,
                                       fg_color=CARD_BG, button_color=ACCENT, 
                                       button_hover_color=HOVER_PRIMARY, height=35)
        mode_dropdown.pack(fill="x", padx=15, pady=(5, 15))
        
        # Description
        ctk.CTkLabel(basic_section, text="Description", 
                    font=FONT_SECONDARY, text_color=TEXT_PRIMARY).pack(anchor="w", padx=15)
        
        desc_entry = ctk.CTkTextbox(basic_section, height=80,
                                   font=FONT_SECONDARY,
                                   corner_radius=8, border_width=1, border_color=BORDER_COLOR)
        desc_entry.pack(fill="x", padx=15, pady=(5, 15))
        
        # Boutons d'action
        buttons_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        buttons_frame.pack(fill="x", padx=15, pady=(20, 15))
        
        # Bouton Annuler (icône uniquement)
        cancel_icon = load_icon('close', (18, 18))
        cancel_btn = ctk.CTkButton(buttons_frame, text="", image=cancel_icon,
                                  command=form_window.destroy,
                                  fg_color=BTN_SECONDARY, hover_color=HOVER_SECONDARY,
                                  width=45, height=40, corner_radius=8)
        cancel_btn.pack(side="left", padx=(0, 10))
        
        # Bouton Enregistrer (icône uniquement)
        save_icon = load_icon('check', (18, 18))
        save_btn = ctk.CTkButton(buttons_frame, text="", image=save_icon,
                                command=lambda: self._save_payment(form_window, var_eleve, var_montant, 
                                                                 var_date, var_mode, desc_entry, payment_data),
                                fg_color=BTN_SUCCESS, hover_color=HOVER_SUCCESS,
                                width=45, height=40, corner_radius=8)
        save_btn.pack(side="right")
        
        # Pré-remplir les champs si modification
        if payment_data and mode == "Modifier":
            # Pré-remplir les champs avec les données existantes
            pass
    
    def _save_payment(self, window, var_eleve, var_montant, var_date, var_mode, desc_entry, payment_data):
        """Sauvegarde un nouveau paiement ou modifie un existant"""
        try:
            # Validation des champs
            eleve_str = var_eleve.get()
            montant = var_montant.get().strip()
            date = var_date.get().strip()
            mode_p = var_mode.get()
            description = desc_entry.get("1.0", "end-1c").strip()
            
            # Vérifications
            if not all([eleve_str, montant, date, mode_p]):
                messagebox.showerror("Erreur", "Veuillez remplir tous les champs obligatoires (*).")
                return
            
            if eleve_str == "Sélectionner un élève...":
                messagebox.showerror("Erreur", "Veuillez sélectionner un élève.")
                return
            
            # Extraire l'ID de l'élève
            try:
                # Format: "Nom Prénom (Classe) - ID: X"
                if "- ID: " in eleve_str:
                    eleve_id = int(eleve_str.split("- ID: ")[1])
                else:
                    messagebox.showerror("Erreur", "Format d'élève invalide.")
                    return
            except:
                messagebox.showerror("Erreur", "Erreur lors de la récupération de l'ID élève.")
                return
            
            # Validation du montant
            try:
                montant_float = float(montant)
                if montant_float <= 0:
                    raise ValueError("Montant invalide")
            except ValueError:
                messagebox.showerror("Erreur", "Montant invalide. Veuillez entrer un nombre positif.")
                return
            
            # Validation de la date
            try:
                datetime.strptime(date, '%Y-%m-%d')
            except ValueError:
                messagebox.showerror("Erreur", "Format de date invalide. Utilisez YYYY-MM-DD.")
                return
            
            # Sauvegarder
            if payment_data:
                # Modification
                update_paiement(payment_data[0], eleve_id, montant_float, date, mode_p, description)
                messagebox.showinfo("Succès", "Paiement modifié avec succès.")
            else:
                # Ajout
                add_paiement(eleve_id, montant_float, date, mode_p, description)
                messagebox.showinfo("Succès", "Paiement ajouté avec succès.")
            
            # Actualiser les données
            self._refresh_data()
            
            # Fermer la fenêtre
            window.destroy()
            
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de la sauvegarde:\n{str(e)}")

if __name__ == "__main__":
    # Configuration de CustomTkinter avec le thème EduManager+
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")
    
    # Créer la fenêtre principale
    root = ctk.CTk()
    root.title("Tableau de bord des paiements - EduManager+")
    root.geometry("1400x900")
    
    # Appliquer le thème EduManager+
    apply_theme_to_app(root)
    
    # Créer et afficher la vue
    paiements_view = PaiementsView(root)
    paiements_view.pack(fill="both", expand=True, padx=5, pady=5)
    
    # Lancer l'application
    root.mainloop()
