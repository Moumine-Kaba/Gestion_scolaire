import customtkinter as ctk
from tkinter import messagebox
from PIL import Image
import os
import sys
import sqlite3

# -*- coding: utf-8 -*-
"""
Gestion des Classes - Utilise le thème global EduManager+
- Thème sombre parfait avec couleurs harmonieuses
- Design moderne et professionnel
- Interface utilisateur optimisée
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
    # Couleurs principales
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
    INFO_CYAN = "#00D4FF"
    PURPLE_ACCENT = "#A855F7"
    PINK_ACCENT = "#FF6B9D"
    GOLD_ACCENT = "#FFD700"
    SILVER_ACCENT = "#C0C0C0"
    EMERALD_ACCENT = "#10B981"
    CORAL_ACCENT = "#FF6B6B"
    HOVER_PRIMARY = "#1F6FEB"
    HOVER_SECONDARY = "#21262D"
    HOVER_SUCCESS = "#2EA043"
    HOVER_WARNING = "#BF8700"
    HOVER_ERROR = "#DA3633"
    HOVER_INFO = "#FF7B00"
    FOCUS_PRIMARY = "#1F6FEB"
    FOCUS_SUCCESS = "#2EA043"
    FOCUS_WARNING = "#BF8700"
    FOCUS_ERROR = "#DA3633"
    
    # Couleurs EduManager
    BG_MAIN = DARK_BLUE
    BG_SIDEBAR = DEEPER_BLUE
    BG_CARD = NAVY_BLUE
    BG_CARD_HOVER = DARKER_BLUE
    BG_SECONDARY = MEDIUM_GRAY
    TEXT_PRIMARY = SOFT_BLUE
    TEXT_SECONDARY = PALE_BLUE
    TEXT_MUTED = MUTED_BLUE
    TEXT_ACCENT = ACCENT_BLUE
    BORDER_COLOR = DARK_GRAY
    BORDER_LIGHT = ACCENT_BLUE
    BORDER_ACCENT = ACCENT_BLUE
    BTN_PRIMARY = PRIMARY_BLUE
    BTN_SECONDARY = DARKER_BLUE
    BTN_SUCCESS = SUCCESS_GREEN
    BTN_WARNING = WARNING_YELLOW
    BTN_DANGER = ERROR_RED
    BTN_INFO = INFO_ORANGE
    BTN_TRANSFER = ACCENT_BLUE
    STATE_SUCCESS = SUCCESS_GREEN
    STATE_WARNING = WARNING_YELLOW
    STATE_ERROR = ERROR_RED
    STATE_INFO = INFO_ORANGE
    
    # Polices
    FONT_PRIMARY = ("Segoe UI", 14)
    FONT_SECONDARY = ("Segoe UI", 12)
    FONT_TITLE = ("Segoe UI", 24, "bold")
    FONT_SMALL = ("Segoe UI", 11)
    PADDING_MEDIUM = 3
    PADDING_SMALL = 3
    MARGIN_MEDIUM = 3
    MARGIN_SMALL = 3

# Configuration des icônes
ICONS_PATH = {
    "add": "resources/icons/add.png",
    "edit": "resources/icons/edit.png",
    "delete": "resources/icons/delete.png",
    "search": "resources/icons/search.png",
    "classroom": "resources/icons/classroom.png",
    "person": "resources/icons/person.png",
    "door": "resources/icons/door.png",
    "book": "resources/icons/book.png",
    "logo": "resources/icons/logo.png"
}

# --- Fonctions utilitaires ---

def get_icon_path(icon_name):
    return ICONS_PATH.get(icon_name, "")

def get_db_connection():
    try:
        conn = sqlite3.connect("database/edumanager.db")
        conn.row_factory = sqlite3.Row
        return conn
    except sqlite3.Error as e:
        print(f"⚠️ Erreur connexion DB: {e}")
        return None

def get_all_classes():
    """Récupère toutes les classes depuis la base de données centralisée"""
    conn = get_db_connection()
    if conn is None: 
        return []
    try:
        cursor = conn.cursor()
        # Utiliser les noms de colonnes corrects selon la structure de la DB
        cursor.execute("""
            SELECT c.id_classe as id, c.nom_classe as nom, c.niveau, c.annee_scolaire as annee,
                   c.id_professeur_principal as prof_id, c.salle_id
            FROM classes c
            ORDER BY c.nom_classe
        """)
        classes = cursor.fetchall()
        return [dict(row) for row in classes]
    except sqlite3.Error as e:
        print(f"Erreur lors de la récupération des classes : {e}")
        return []
    finally:
        if conn: 
            conn.close()

def add_class(nom, prof_id, salle_id, niveau, annee):
    """Ajoute une nouvelle classe dans la base de données centralisée"""
    conn = get_db_connection()
    if conn is None: 
        return False
    try:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO classes (nom_classe, niveau, annee_scolaire, id_professeur_principal, salle_id, effectif) 
            VALUES (?, ?, ?, ?, ?, 0)
        """, (nom, niveau, annee, prof_id, salle_id))
        conn.commit()
        return True
    except sqlite3.Error as e:
        print(f"Erreur lors de l'ajout de la classe : {e}")
        return False
    finally:
        if conn: 
            conn.close()

def update_class_data(classe_id, nom, prof_id, salle_id, niveau, annee):
    """Met à jour une classe existante dans la base de données centralisée"""
    conn = get_db_connection()
    if conn is None: 
        return False
    try:
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE classes 
            SET nom_classe = ?, niveau = ?, annee_scolaire = ?, 
                id_professeur_principal = ?, salle_id = ? 
            WHERE id_classe = ?
        """, (nom, niveau, annee, prof_id, salle_id, classe_id))
        conn.commit()
        return True
    except sqlite3.Error as e:
        print(f"Erreur lors de la mise à jour de la classe : {e}")
        return False
    finally:
        if conn: 
            conn.close()

def delete_class(classe_id):
    """Supprime une classe et ses élèves associés"""
    conn = get_db_connection()
    if conn is None: 
        return False
    try:
        cursor = conn.cursor()
        # Mettre à jour les élèves pour les désassocier de la classe
        cursor.execute("UPDATE eleves SET id_classe = NULL WHERE id_classe = ?", (classe_id,))
        # Supprimer la classe
        cursor.execute("DELETE FROM classes WHERE id_classe = ?", (classe_id,))
        conn.commit()
        return True
    except sqlite3.Error as e:
        print(f"Erreur lors de la suppression de la classe : {e}")
        if conn: 
            conn.rollback()
        return False
    finally:
        if conn: 
            conn.close()

def get_classe_by_id(classe_id):
    """Récupère une classe par son ID"""
    conn = get_db_connection()
    if conn is None: 
        return None
    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT c.id_classe as id, c.nom_classe as nom, c.niveau, c.annee_scolaire as annee,
                   c.id_professeur_principal as prof_id, c.salle_id
            FROM classes c 
            WHERE c.id_classe = ?
        """, (classe_id,))
        row = cursor.fetchone()
        return dict(row) if row else None
    except sqlite3.Error as e:
        print(f"Erreur lors de la récupération de la classe par ID : {e}")
        return None
    finally:
        if conn: 
            conn.close()

def get_all_professeurs():
    """Récupère tous les professeurs"""
    conn = get_db_connection()
    if conn is None: 
        return []
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT id_professeur as id, nom, prenom FROM professeurs ORDER BY nom, prenom")
        profs = cursor.fetchall()
        return [dict(p) for p in profs]
    except sqlite3.Error as e:
        print(f"Erreur lors de la récupération des professeurs : {e}")
        return []
    finally:
        if conn: 
            conn.close()

def get_all_salles():
    """Récupère toutes les salles"""
    conn = get_db_connection()
    if conn is None: 
        return []
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT id_salle as id, nom_salle as nom FROM salles ORDER BY nom_salle")
        salles = cursor.fetchall()
        return [dict(s) for s in salles]
    except sqlite3.Error as e:
        print(f"Erreur lors de la récupération des salles : {e}")
        return []
    finally:
        if conn: 
            conn.close()
        
def setup_database():
    conn = get_db_connection()
    if conn is None: return
    try:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS professeurs (
                id INTEGER PRIMARY KEY,
                nom TEXT NOT NULL,
                prenom TEXT NOT NULL
            );
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS salle (
                id INTEGER PRIMARY KEY,
                nom TEXT NOT NULL UNIQUE
            );
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS classe (
                id INTEGER PRIMARY KEY,
                nom TEXT NOT NULL UNIQUE,
                niveau TEXT,
                annee TEXT,
                prof_id INTEGER,
                salle_id INTEGER,
                FOREIGN KEY (prof_id) REFERENCES professeurs (id),
                FOREIGN KEY (salle_id) REFERENCES salle (id)
            );
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS eleves (
                id INTEGER PRIMARY KEY,
                nom TEXT NOT NULL,
                prenom TEXT NOT NULL,
                classe_id INTEGER,
                FOREIGN KEY (classe_id) REFERENCES classe (id) ON DELETE CASCADE
            );
        """)
        conn.commit()
    except sqlite3.Error as e:
        print(f"Erreur de configuration de la base de données : {e}")
    finally:
        if conn: conn.close()

# =================== CONFIGURATION DU THÈME EDUMANAGER+ PREMIUM =====================
# Configuration CustomTkinter avec le thème centralisé
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# Thème centralisé EduManager+ Premium avec gradients et effets améliorés
THEME = {
    "bg_main": BG_MAIN,
    "header_bg": BG_SIDEBAR,
    "card_bg": CARD_BG,
    "border_color": BORDER_COLOR,
    "accent_blue": ACCENT,
    "primary_text": TEXT,
    "secondary_text": MUTED,
    "error_red": ERROR_RED,
    "success_green": SUCCESS_GREEN,
    "warning_yellow": WARNING_YELLOW,
    "info_orange": INFO_ORANGE,
    "hover_light": HOVER_PRIMARY,
    # Couleurs premium améliorées avec palette moderne
    "gradient_start": "#0A192F",
    "gradient_end": "#1A2B4A",
    "card_shadow": "#000000",
    "glass_effect": "#FFFFFF",
    "premium_accent": "#00D4FF",
    "premium_gold": "#FFD700",
    "premium_purple": "#8B5CF6",
    # Nouvelles couleurs modernes
    "neon_blue": "#00BFFF",
    "electric_purple": "#9D4EDD",
    "cyber_green": "#00FF88",
    "sunset_orange": "#FF6B35",
    "deep_blue": "#1E3A8A",
    "light_blue": "#3B82F6",
    "dark_gray": "#1F2937",
    "medium_gray": "#374151",
    "light_gray": "#6B7280",
    "card_hover": "#1E293B",
    "glass_bg": "#0F172A",
    "accent_gradient_1": "#667EEA",
    "accent_gradient_2": "#764BA2",
    "success_gradient_1": "#4FACFE",
    "success_gradient_2": "#00F2FE",
    "warning_gradient_1": "#F093FB",
    "warning_gradient_2": "#F5576C"
}

# Polices premium du thème centralisé
FONT = FONT_PRIMARY[0]  # Utilise "Segoe UI" du thème centralisé
FONT_PREMIUM = ("Segoe UI", 16, "bold")
FONT_HEADER = ("Segoe UI", 20, "bold")
FONT_CARD_TITLE = ("Segoe UI", 18, "bold")

# =================== CONFIGURATION DES ICÔNES CENTRALISÉES =====================
# Utilise le système centralisé d'icônes
ICONS_PATH = {
    "edit": get_icon_path("edit"),
    "delete": get_icon_path("delete"),
    "view": get_icon_path("view"),
    "add": get_icon_path("add"),
    "import": get_icon_path("upload"),
    "export": get_icon_path("csv"),
    "search": get_icon_path("search"),
    "pdf": get_icon_path("file"),
    "reload": get_icon_path("refresh"),
    "class": get_icon_path("classroom"),
    "student": get_icon_path("eleve"),
    "teacher": get_icon_path("person"),
    "settings": get_icon_path("settings"),
    "home": get_icon_path("home"),
    "stats": get_icon_path("stats"),
    "calendar": get_icon_path("calendar"),
    "bell": get_icon_path("bell"),
    "close": get_icon_path("close"),
    "check": get_icon_path("check")
}

def load_icon(path_or_img, size=14):
    """Charge une icône à partir d'un chemin ou d'un CTkImage avec gestion d'erreur améliorée."""
    if isinstance(path_or_img, ctk.CTkImage):
        return path_or_img
    
    # Vérifie si le fichier existe
    if not path_or_img or not os.path.exists(path_or_img):
        # Crée une icône transparente si le fichier n'existe pas
        img = Image.new("RGBA", (size, size), (255, 255, 255, 0))
        return ctk.CTkImage(light_image=img, dark_image=img, size=(size, size))
    
    try:
        image = Image.open(path_or_img).resize((size, size), Image.Resampling.LANCZOS)
        return ctk.CTkImage(light_image=image, dark_image=image, size=(size, size))
    except Exception as e:
        print(f"⚠️ Erreur chargement icône {path_or_img}: {e}")
        # Crée une icône transparente en cas d'erreur
        img = Image.new("RGBA", (size, size), (255, 255, 255, 0))
        return ctk.CTkImage(light_image=img, dark_image=img, size=(size, size))

class PremiumBadge(ctk.CTkFrame):
    """Badge premium avec effets visuels avancés et design moderne"""
    def __init__(self, parent, text, color=THEME["premium_accent"], bg=THEME["card_bg"], font_size=10):
        super().__init__(
            parent,
            fg_color=bg,
            corner_radius=16,
            border_width=1,
            border_color=color,
            width=80,
            height=32
        )
        
        # Label avec effet de glow
        self.label = ctk.CTkLabel(
            self,
            text=text,
            font=(FONT, font_size, "bold"),
            fg_color="transparent",
            text_color=color
        )
        self.label.pack(expand=True)
        
        # Effet de survol
        self.bind("<Enter>", self.on_hover)
        self.bind("<Leave>", self.on_leave)
        self.label.bind("<Enter>", self.on_hover)
        self.label.bind("<Leave>", self.on_leave)
    
    def on_hover(self, event):
        """Effet de survol avec changement de couleur"""
        self.configure(fg_color=THEME["card_hover"])
        self.label.configure(text_color=THEME["neon_blue"])
    
    def on_leave(self, event):
        """Retour à l'état normal"""
        self.configure(fg_color=THEME["card_bg"])
        self.label.configure(text_color=THEME["premium_accent"])

class GlassCard(ctk.CTkFrame):
    """Carte avec effet de verre premium et design moderne"""
    def __init__(self, parent, **kwargs):
        default_kwargs = {
            "fg_color": THEME["glass_bg"],
            "corner_radius": 24,
            "border_width": 2,
            "border_color": THEME["neon_blue"]
        }
        default_kwargs.update(kwargs)
        super().__init__(parent, **default_kwargs)

        # Effet de survol amélioré
        self.bind("<Enter>", self.on_hover)
        self.bind("<Leave>", self.on_leave)
        self.is_hovered = False
    
    def on_hover(self, event):
        """Effet de survol avec animation"""
        if not self.is_hovered:
            self.is_hovered = True
            self.configure(
                fg_color=THEME["card_hover"],
                border_color=THEME["electric_purple"]
            )
    
    def on_leave(self, event):
        """Retour à l'état normal"""
        if self.is_hovered:
            self.is_hovered = False
            self.configure(
                fg_color=THEME["glass_bg"],
                border_color=THEME["neon_blue"]
            )



class ModernClassesView(ctk.CTkFrame):
    """Vue moderne des cartes de classes avec vos icônes personnalisées"""
    def __init__(self, parent, on_edit, on_delete, notif_bar, icons):
        super().__init__(parent, fg_color="transparent")
        self.on_edit = on_edit
        self.on_delete = on_delete
        self.notif_bar = notif_bar
        self.icons = icons
        
        # Cache pour optimiser les performances
        self._cached_classes = None
        self._last_refresh_time = 0
        self._refresh_throttle = 0.1  # 100ms minimum entre les rafraîchissements
        self._filter_cache = {}
        
        # Barre d'outils moderne
        self.create_toolbar()
        
        # Container des cartes
        self.card_container = ctk.CTkScrollableFrame(self, fg_color="transparent", corner_radius=20)
        self.card_container.pack(fill="both", expand=True, padx=3, pady=(0, 3))
        
        self.refresh_view()
    
    def create_toolbar(self):
        """Crée la barre d'outils moderne"""
        toolbar = ctk.CTkFrame(self, fg_color=BG_CARD, corner_radius=25, border_width=2, border_color=BORDER_COLOR)
        toolbar.pack(fill="x", padx=3, pady=(3, 3))
        
        # Section gauche - Titre avec logo et design moderne
        left_section = ctk.CTkFrame(toolbar, fg_color="transparent")
        left_section.pack(side="left", padx=15, pady=15)
        
        # Logo principal sans fond circulaire
        classroom_icon = load_icon(self.icons.get("classroom"), 28)
        if classroom_icon:
            logo_label = ctk.CTkLabel(left_section, image=classroom_icon, text="", fg_color="transparent")
            logo_label.pack(side="left", padx=(0, 15))
        
        # Container du titre avec design moderne
        title_container = ctk.CTkFrame(left_section, fg_color="transparent")
        title_container.pack(side="left", fill="y", expand=True)
        
        # Titre principal avec gradient effect
        title_text = ctk.CTkLabel(
            title_container,
            text="Gestion des Classes",
            font=("Segoe UI", 22, "bold"),
            text_color=TEXT_PRIMARY,
            fg_color="transparent"
        )
        title_text.pack(anchor="w")
        
        # Sous-titre élégant
        subtitle_text = ctk.CTkLabel(
            title_container,
            text="Interface Moderne • Gestion Complète",
            font=("Segoe UI", 11),
            text_color=TEXT_SECONDARY,
            fg_color="transparent"
        )
        subtitle_text.pack(anchor="w", pady=(2, 0))
        
        # Section droite - Bouton ajouter et recherche
        right_section = ctk.CTkFrame(toolbar, fg_color="transparent")
        right_section.pack(side="right", padx=15, pady=15)
        
        # Bouton Ajouter sans fond avec contour gris
        add_btn = ctk.CTkButton(
            right_section,
            text="Nouvelle Classe",
            image=load_icon(self.icons.get("add"), 20),
            fg_color="transparent",
            hover_color=HOVER_SUCCESS,
            text_color=TEXT_PRIMARY,
            font=("Segoe UI", 13, "bold"),
            corner_radius=20,
            height=45,
            width=160,
            border_width=2,
            border_color=BORDER_COLOR,
            command=lambda: self.on_edit(None)
        )
        add_btn.pack(side="right", padx=(0, 12))
        
        # Barre de recherche avec contour gris
        search_frame = ctk.CTkFrame(right_section, fg_color=BG_CARD_HOVER, corner_radius=20, border_width=2, border_color=BORDER_COLOR)
        search_frame.pack(side="right", padx=(0, 12))
        
        # Container interne pour la recherche
        search_inner = ctk.CTkFrame(search_frame, fg_color="transparent")
        search_inner.pack(fill="both", expand=True, padx=8, pady=8)
        
        self.search_var = ctk.StringVar()
        self.search_entry = ctk.CTkEntry(
            search_inner,
            textvariable=self.search_var,
            width=200,
            height=40,
            placeholder_text="🔍 Rechercher...",
            fg_color=BG_CARD,
            border_width=1,
            border_color=BORDER_COLOR,
            text_color=TEXT_PRIMARY,
            font=("Segoe UI", 13),
            corner_radius=15
        )
        self.search_entry.pack(side="left", fill="x", expand=True, padx=(0, 8))
        self.search_entry.bind("<KeyRelease>", self.filter_view)
        
        # Filtre par niveau
        self.level_var = ctk.StringVar(value="Tous les niveaux")
        level_filter = ctk.CTkComboBox(
            search_inner,
            values=["Tous les niveaux", "Lycée", "Collège", "Primaire"],
            variable=self.level_var,
            font=("Segoe UI", 12),
            fg_color=BG_CARD,
            text_color=TEXT_PRIMARY,
            border_color=BORDER_COLOR,
            button_color=BORDER_COLOR,
            corner_radius=15,
            height=40,
            width=140,
            command=self.filter_view
        )
        level_filter.pack(side="left", padx=(0, 8))
        
        # Bouton de recherche sans fond avec contour gris
        search_btn = ctk.CTkButton(
            search_inner,
            text="",
            image=load_icon(self.icons.get("search"), 20),
            fg_color="transparent",
            hover_color=HOVER_PRIMARY,
            text_color=TEXT_PRIMARY,
            width=40,
            height=40,
            corner_radius=15,
            border_width=2,
            border_color=BORDER_COLOR,
            command=self.refresh_view
        )
        search_btn.pack(side="right")
    
    def refresh_view(self):
        """Rafraîchit la vue avec les nouvelles cartes modernes - Version optimisée"""
        import time
        
        # Throttling pour éviter les rafraîchissements trop fréquents
        current_time = time.time()
        if current_time - self._last_refresh_time < self._refresh_throttle:
            return
        self._last_refresh_time = current_time
        
        # Nettoyer le container
        for widget in self.card_container.winfo_children():
            widget.destroy()
        
        # Utiliser le cache si disponible
        if self._cached_classes is None:
            self._cached_classes = get_all_classes()
        
        # Filtrer les classes avec cache
        search = self.search_var.get().lower().strip()
        level_filter = self.level_var.get()
        
        # Créer une clé de cache pour le filtre
        cache_key = f"{search}_{level_filter}"
        
        # Vérifier le cache de filtres
        if cache_key in self._filter_cache:
            filtered_classes = self._filter_cache[cache_key]
        else:
            # Filtrage optimisé par recherche textuelle
            if search:
                filtered_classes = [
                    c for c in self._cached_classes 
                    if search in (c['nom'] or '').lower() or 
                       search in (c['niveau'] or '').lower() or 
                       search in (c['annee'] or '').lower()
                ]
            else:
                filtered_classes = self._cached_classes.copy()
            
            # Filtrage par niveau avec cache
            if level_filter != "Tous les niveaux":
                level_key = f"level_{level_filter}"
                if level_key not in self._filter_cache:
                    if level_filter == "Lycée":
                        lycee_levels = ['1ère', 'TSM', 'Terminale', '2nde']
                        self._filter_cache[level_key] = [c for c in self._cached_classes if c['niveau'] in lycee_levels]
                    elif level_filter == "Collège":
                        college_levels = ['6ème', '5ème', '4ème', '3ème']
                        self._filter_cache[level_key] = [c for c in self._cached_classes if c['niveau'] in college_levels]
                    elif level_filter == "Primaire":
                        primaire_levels = ['CP', 'CE1', 'CE2', 'CM1', 'CM2']
                        self._filter_cache[level_key] = [c for c in self._cached_classes if c['niveau'] in primaire_levels]
                
                filtered_classes = [c for c in filtered_classes if c in self._filter_cache[level_key]]
            
            # Mettre en cache le résultat
            self._filter_cache[cache_key] = filtered_classes
        
        # Tri optimisé
        order_map = {"1ère": 1, "TSM": 2, "Terminale": 3, "2nde": 4, "6ème": 5, "5ème": 6, "4ème": 7, "3ème": 8}
        filtered_classes.sort(key=lambda classe: order_map.get(classe['nom'], float('inf')))
        
        # Récupérer les données associées avec cache
        if not hasattr(self, '_cached_profs') or not hasattr(self, '_cached_salles'):
            self._cached_profs = {p['id']: f"{p['nom']} {p['prenom']}" for p in get_all_professeurs()}
            self._cached_salles = {s['id']: s['nom'] for s in get_all_salles()}
        
        # Créer les cartes en lot pour de meilleures performances
        self._create_cards_batch(filtered_classes)
    
    def _create_cards_batch(self, filtered_classes):
        """Crée les cartes en lot pour de meilleures performances"""
        # Créer les cartes modernes en format paysage (2 colonnes)
        num_columns = 2
        cards_to_create = []
        
        # Préparer toutes les cartes
        for idx, row in enumerate(filtered_classes):
            prof_name = self._cached_profs.get(row['prof_id'], '—')
            salle_name = self._cached_salles.get(row['salle_id'], '—')
            
            card = ModernClassCard(self.card_container, row, prof_name, salle_name, self.on_edit, self.on_delete, self.icons)
            cards_to_create.append((card, idx))
        
        # Créer toutes les cartes en une seule fois
        for card, idx in cards_to_create:
            card.grid(row=idx // num_columns, column=idx % num_columns, padx=12, pady=12, sticky="nsew")
        
        # Configurer les colonnes pour le format paysage
        for i in range(num_columns):
            self.card_container.grid_columnconfigure(i, weight=1)
    
    def filter_view(self, event=None):
        """Filtre la vue en temps réel avec throttling"""
        # Utiliser after() pour éviter les appels trop fréquents
        if hasattr(self, '_filter_timer'):
            self.after_cancel(self._filter_timer)
        
        self._filter_timer = self.after(150, self.refresh_view)  # 150ms de délai
    
    def invalidate_cache(self):
        """Invalide le cache pour forcer un rafraîchissement complet"""
        self._cached_classes = None
        self._filter_cache.clear()
        if hasattr(self, '_cached_profs'):
            delattr(self, '_cached_profs')
        if hasattr(self, '_cached_salles'):
            delattr(self, '_cached_salles')

class ModernClassCard(ctk.CTkFrame):
    """Carte de classe moderne avec design premium et effets visuels"""
    def __init__(self, parent, classe_data, prof_name, salle_name, on_edit, on_delete, icons):
        super().__init__(parent, fg_color=BG_CARD, corner_radius=25, 
                         border_width=2, border_color=BORDER_COLOR)
        self.classe_id = classe_data['id']
        self.on_edit = on_edit
        self.on_delete = on_delete
        self.icons = icons
        self.is_hovered = False

        # Container principal en format paysage
        main_container = ctk.CTkFrame(self, fg_color="transparent")
        main_container.pack(fill="both", expand=True, padx=15, pady=15)
        
        # Header avec icône et titre
        self.create_card_header(main_container, classe_data)
        
        # Layout horizontal pour les sections Informations et Actions
        sections_container = ctk.CTkFrame(main_container, fg_color="transparent")
        sections_container.pack(fill="x", pady=(0, 10))
        
        # Section gauche - Informations
        info_section = ctk.CTkFrame(sections_container, fg_color="transparent")
        info_section.pack(side="left", fill="both", expand=True, padx=(0, 10))
        
        # Section droite - Actions
        actions_section = ctk.CTkFrame(sections_container, fg_color="transparent")
        actions_section.pack(side="right", fill="y")
        
        # Informations principales dans la section gauche
        self.create_main_info(info_section, classe_data, prof_name, salle_name)
        
        # Actions avec boutons modernes dans la section droite
        self.create_action_buttons(actions_section)
        
        # Effets de survol
        self.bind_events()
    
    def create_card_header(self, parent, classe_data):
        """Crée le header de la carte en format paysage"""
        header_frame = ctk.CTkFrame(parent, fg_color="transparent")
        header_frame.pack(fill="x", pady=(0, 15))
        
        # Layout horizontal pour le header
        title_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        title_frame.pack(side="left", fill="x", expand=True)
        
        # Icône de classe sans fond circulaire
        classroom_icon = load_icon(self.icons.get("classroom"), 20)
        if classroom_icon:
            icon_label = ctk.CTkLabel(title_frame, image=classroom_icon, text="", fg_color="transparent")
            icon_label.pack(side="left", padx=(0, 12))
        
        # Titre de la classe avec style moderne
        title_label = ctk.CTkLabel(
            title_frame, 
            text=classe_data['nom'], 
            font=("Segoe UI", 16, "bold"),
            text_color=TEXT_PRIMARY,
            fg_color="transparent"
        )
        title_label.pack(side="left", fill="x", expand=True)
        
        # Badge du niveau à droite
        level_badge = ctk.CTkFrame(header_frame, fg_color=BG_CARD_HOVER, corner_radius=10, height=22)
        level_badge.pack(side="right")
        
        level_text = ctk.CTkLabel(
            level_badge,
            text=f"{classe_data['niveau'] or 'Non spécifié'}",
            font=("Segoe UI", 9, "bold"),
            text_color=TEXT_SECONDARY,
            fg_color="transparent"
        )
        level_text.pack(padx=10, pady=3)
    
    def create_main_info(self, parent, classe_data, prof_name, salle_name):
        """Crée les informations principales alignées avec les actions"""
        # Container des informations avec design moderne
        info_container = ctk.CTkFrame(parent, fg_color=BG_CARD_HOVER, corner_radius=12, border_width=1, border_color=BORDER_COLOR)
        info_container.pack(fill="both", expand=True)
        
        # Header des informations
        info_header = ctk.CTkFrame(info_container, fg_color="transparent")
        info_header.pack(fill="x", padx=12, pady=(10, 8))
        
        info_title = ctk.CTkLabel(
            info_header,
            text="Informations",
            font=("Segoe UI", 11, "bold"),
            text_color=TEXT_PRIMARY,
            fg_color="transparent"
        )
        info_title.pack(anchor="w")
        
        # Séparateur décoratif
        separator = ctk.CTkFrame(info_header, fg_color=TEXT_ACCENT, height=2, corner_radius=1)
        separator.pack(fill="x", pady=(3, 0))
        
        # Informations détaillées en layout vertical compact
        details_container = ctk.CTkFrame(info_container, fg_color="transparent")
        details_container.pack(fill="both", expand=True, padx=12, pady=(0, 10))
        
        # Information professeur
        prof_frame = ctk.CTkFrame(details_container, fg_color="transparent")
        prof_frame.pack(fill="x", pady=(0, 8))
        
        # Icône professeur sans fond circulaire
        person_icon = load_icon(self.icons.get("person"), 12)
        if person_icon:
            prof_icon_label = ctk.CTkLabel(prof_frame, image=person_icon, text="", fg_color="transparent")
            prof_icon_label.pack(side="left", padx=(0, 8))
        
        prof_text = ctk.CTkLabel(
            prof_frame,
            text=f"Prof: {prof_name}",
            font=("Segoe UI", 10, "bold"),
            text_color=TEXT_PRIMARY,
            fg_color="transparent"
        )
        prof_text.pack(side="left", fill="x", expand=True)
        
        # Information salle
        room_frame = ctk.CTkFrame(details_container, fg_color="transparent")
        room_frame.pack(fill="x")
        
        # Icône salle sans fond circulaire
        door_icon = load_icon(self.icons.get("door"), 12)
        if door_icon:
            room_icon_label = ctk.CTkLabel(room_frame, image=door_icon, text="", fg_color="transparent")
            room_icon_label.pack(side="left", padx=(0, 8))
        
        room_text = ctk.CTkLabel(
            room_frame,
            text=f"Salle: {salle_name}",
            font=("Segoe UI", 10, "bold"),
            text_color=TEXT_PRIMARY,
            fg_color="transparent"
        )
        room_text.pack(side="left", fill="x", expand=True)
    
    def create_action_buttons(self, parent):
        """Crée les boutons d'action alignés avec les informations"""
        # Container des boutons avec design moderne
        buttons_container = ctk.CTkFrame(parent, fg_color=BG_CARD_HOVER, corner_radius=12, border_width=1, border_color=BORDER_COLOR)
        buttons_container.pack(fill="both", expand=True)
        
        # Header des actions
        actions_header = ctk.CTkFrame(buttons_container, fg_color="transparent")
        actions_header.pack(fill="x", padx=12, pady=(10, 8))
        
        actions_title = ctk.CTkLabel(
            actions_header,
            text="Actions",
            font=("Segoe UI", 11, "bold"),
            text_color=TEXT_PRIMARY,
            fg_color="transparent"
        )
        actions_title.pack(anchor="w")
        
        # Séparateur décoratif
        separator = ctk.CTkFrame(actions_header, fg_color=TEXT_ACCENT, height=2, corner_radius=1)
        separator.pack(fill="x", pady=(3, 0))
        
        # Container des boutons en vertical
        buttons_inner = ctk.CTkFrame(buttons_container, fg_color="transparent")
        buttons_inner.pack(fill="both", expand=True, padx=12, pady=(0, 10))
        
        # Bouton Modifier sans fond avec contour gris
        edit_btn = ctk.CTkButton(
            buttons_inner, 
            text="Modifier", 
            image=load_icon(self.icons.get("edit"), 16),
            fg_color="transparent",
            text_color=TEXT_PRIMARY,
            hover_color=HOVER_SUCCESS,
            command=lambda: self.on_edit(self.classe_id),
            corner_radius=10,
            height=35,
            width=100,
            border_width=2,
            border_color=BORDER_COLOR,
            font=("Segoe UI", 11, "bold")
        )
        edit_btn.pack(fill="x", pady=(0, 8))
        
        # Bouton Supprimer sans fond avec contour gris
        delete_btn = ctk.CTkButton(
            buttons_inner, 
            text="Supprimer", 
            image=load_icon(self.icons.get("delete"), 16),
            fg_color="transparent",
            text_color=TEXT_PRIMARY,
            hover_color=HOVER_ERROR,
            command=lambda: self.on_delete(self.classe_id),
            corner_radius=10,
            height=35,
            width=100,
            border_width=2,
            border_color=BORDER_COLOR,
            font=("Segoe UI", 11, "bold")
        )
        delete_btn.pack(fill="x")
    
    def bind_events(self):
        """Lie les événements de survol modernes"""
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)
        
        # Appliquer aux enfants
        for child in self.winfo_children():
            child.bind("<Enter>", self.on_enter)
            child.bind("<Leave>", self.on_leave)
            self.bind_child_events(child)
    
    def bind_child_events(self, widget):
        """Lie les événements aux widgets enfants"""
        for child in widget.winfo_children():
            child.bind("<Enter>", self.on_enter)
            child.bind("<Leave>", self.on_leave)
            if hasattr(child, 'winfo_children'):
                self.bind_child_events(child)
    
    def on_enter(self, event):
        """Effet de survol moderne avec animation"""
        if not self.is_hovered:
            self.is_hovered = True
            self.configure(
                fg_color=BG_CARD_HOVER,
                border_color=BORDER_COLOR,
                border_width=3
            )
    
    def on_leave(self, event):
        """Retour à l'état normal avec transition fluide"""
        if self.is_hovered:
            self.is_hovered = False
            self.configure(
                fg_color=BG_CARD,
                border_color=BORDER_COLOR,
                border_width=2
            )
    
    
    def create_card_content(self, classe_data, prof_name, salle_name):
        """Crée le contenu principal de la carte inspiré du dashboard"""
        # Valeur principale (nombre d'élèves simulé)
        effectif = self.get_classe_effectif()
        
        value_label = ctk.CTkLabel(self, text=str(effectif), 
                                 font=("Segoe UI", 18, "bold"), text_color=TEXT_PRIMARY)
        value_label.pack(anchor="w", padx=PADDING_SMALL)
        
        # Sous-texte avec informations
        info_text = f"Niveau: {classe_data['niveau'] or 'Non spécifié'}"
        subtext_label = ctk.CTkLabel(self, text=info_text, 
                                   font=("Segoe UI", 9), text_color=TEXT_SECONDARY)
        subtext_label.pack(anchor="w", padx=PADDING_SMALL, pady=(0, MARGIN_SMALL))
        
        # Informations détaillées
        details_frame = ctk.CTkFrame(self, fg_color="transparent")
        details_frame.pack(fill="x", padx=PADDING_SMALL, pady=(0, MARGIN_SMALL))
        
        # Professeur
        prof_frame = ctk.CTkFrame(details_frame, fg_color="transparent")
        prof_frame.pack(fill="x", pady=(0, 4))
        
        prof_icon = load_icon(self.icons.get("person"), 12)
        if prof_icon:
            prof_icon_label = ctk.CTkLabel(prof_frame, text="", image=prof_icon, 
                                         text_color=TEXT_SECONDARY)
            prof_icon_label.pack(side="left", padx=(0, 6))
        
        prof_text = ctk.CTkLabel(prof_frame, text=f"Prof: {prof_name}", 
                               font=("Segoe UI", 8), text_color=TEXT_SECONDARY)
        prof_text.pack(side="left")
        
        # Salle
        room_frame = ctk.CTkFrame(details_frame, fg_color="transparent")
        room_frame.pack(fill="x")
        
        room_icon = load_icon(self.icons.get("door"), 12)
        if room_icon:
            room_icon_label = ctk.CTkLabel(room_frame, text="", image=room_icon, 
                                         text_color=TEXT_SECONDARY)
            room_icon_label.pack(side="left", padx=(0, 6))
        
        room_text = ctk.CTkLabel(room_frame, text=f"Salle: {salle_name}", 
                               font=("Segoe UI", 8), text_color=TEXT_SECONDARY)
        room_text.pack(side="left")
    
    def get_classe_effectif(self):
        """Récupère l'effectif de la classe"""
        conn = get_db_connection()
        if not conn:
            return 0
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM eleves WHERE id_classe = ?", (self.classe_id,))
            result = cursor.fetchone()
            return result[0] if result else 0
        except sqlite3.Error:
            return 0
        finally:
            if conn:
                conn.close()
    
    def create_progress_bar(self):
        """Crée la barre de progression inspirée du dashboard"""
        # Container pour la barre de progression
        progress_frame = ctk.CTkFrame(self, fg_color="transparent")
        progress_frame.pack(fill="x", padx=PADDING_SMALL, pady=(MARGIN_SMALL, PADDING_SMALL))
        
        # Barre de progression avec fond
        pb_bg = ctk.CTkFrame(progress_frame, fg_color=BG_CARD_HOVER, corner_radius=8, 
                           height=8, border_width=1, border_color=BORDER_COLOR)
        pb_bg.pack(fill="x")
        
        # Calcul du ratio de progression (simulé)
        effectif = self.get_classe_effectif()
        max_effectif = 30  # Effectif maximum théorique
        ratio = max(0.05, min(1.0, effectif / max_effectif))
        
        # Couleurs pour les barres de progression
        progress_colors = [
            SUCCESS_GREEN,    # Vert succès
            PRIMARY_BLUE,     # Bleu primaire
            WARNING_ORANGE,   # Orange warning
            ERROR_RED,        # Rouge erreur
            PURPLE_ACCENT,    # Violet accent
            GOLD_ACCENT       # Or accent
        ]
        
        color_index = self.classe_id % len(progress_colors)
        selected_color = progress_colors[color_index]
        
        # Barre de progression colorée
        pb_fg = ctk.CTkFrame(pb_bg, fg_color=selected_color, corner_radius=8, height=6)
        pb_fg.place(relx=0, rely=0.5, anchor="w", relwidth=ratio, relheight=0.7)
    

class PremiumClassesCardView(ctk.CTkFrame):
    """Vue premium des cartes de classes avec effets visuels avancés"""
    def __init__(self, parent, on_edit, on_delete, notif_bar, icons):
        super().__init__(parent, fg_color="transparent")
        self.on_edit = on_edit
        self.on_delete = on_delete
        self.notif_bar = notif_bar
        self.icons = icons
        
        # Cache pour optimiser les performances
        self._cached_classes = None
        self._last_refresh_time = 0
        self._refresh_throttle = 0.1  # 100ms minimum entre les rafraîchissements
        self._filter_cache = {}
        
        # Barre d'outils premium avec design moderne
        top_bar = GlassCard(self, fg_color=THEME["glass_bg"], corner_radius=24, border_color=THEME["neon_blue"])
        top_bar.pack(fill="x", padx=24, pady=(20, 16))
        
        # Titre de section avec design moderne et icônes personnalisées
        title_frame = ctk.CTkFrame(top_bar, fg_color="transparent")
        title_frame.pack(side="left", padx=24, pady=20)
        
        # Icône avec container circulaire moderne
        icon_container = ctk.CTkFrame(title_frame, fg_color=THEME["electric_purple"], corner_radius=20, width=44, height=44)
        icon_container.pack(side="left", padx=(0, 16))
        icon_container.pack_propagate(False)
        
        # Icône personnalisée du projet
        section_icon = load_icon(self.icons.get("book"), 24)
        icon_label = ctk.CTkLabel(
            icon_container, 
            image=section_icon, 
            text="", 
            fg_color="transparent"
        )
        icon_label.pack(expand=True)
        
        title_text = ctk.CTkFrame(title_frame, fg_color="transparent")
        title_text.pack(side="left")
        
        ctk.CTkLabel(title_text, text="Gestion des Classes", font=("Segoe UI", 22, "bold"), 
                     text_color=THEME["primary_text"], fg_color="transparent").pack(anchor="w")
        ctk.CTkLabel(title_text, text="Interface Moderne avec Icônes Personnalisées", font=("Segoe UI", 12, "bold"), 
                     text_color=THEME["electric_purple"], fg_color="transparent").pack(anchor="w")
        
        # Bouton "Ajouter" sans fond avec contour gris
        add_btn = ctk.CTkButton(
            top_bar, 
            text="Nouvelle Classe", 
            image=load_icon(self.icons["add"], 20), 
            fg_color="transparent", 
            hover_color=THEME["success_gradient_1"], 
            text_color=THEME["primary_text"], 
            font=("Segoe UI", 14, "bold"), 
            corner_radius=16, 
            height=44,
            border_width=2,
            border_color=BORDER_COLOR,
            command=lambda: self.on_edit(None)
        )
        add_btn.pack(side="right", padx=24, pady=20)
        
        # Barre de recherche avec contour gris
        search_frame = GlassCard(top_bar, fg_color=THEME["card_bg"], corner_radius=16, border_color=BORDER_COLOR)
        search_frame.pack(side="right", padx=(0, 24), pady=20)
        
        self.search_var = ctk.StringVar()
        self.search_entry = ctk.CTkEntry(
            search_frame, 
            textvariable=self.search_var, 
            width=200, 
            height=40, 
            placeholder_text="🔍 Rechercher...", 
            fg_color=THEME["glass_bg"], 
            border_width=0, 
            text_color=THEME["primary_text"], 
            font=("Segoe UI", 13), 
            corner_radius=16
        )
        self.search_entry.pack(side="left", padx=(12, 0), pady=8)
        self.search_entry.bind("<KeyRelease>", self.filter_view)
        
        # Filtre par niveau dans la vue premium
        self.level_var = ctk.StringVar(value="Tous les niveaux")
        level_filter = ctk.CTkComboBox(
            search_frame,
            values=["Tous les niveaux", "Lycée", "Collège", "Primaire"],
            variable=self.level_var,
            font=("Segoe UI", 12),
            fg_color=THEME["glass_bg"],
            text_color=THEME["primary_text"],
            border_color=THEME["electric_purple"],
            button_color=THEME["electric_purple"],
            corner_radius=16,
            height=40,
            width=140,
            command=self.filter_view
        )
        level_filter.pack(side="left", padx=(8, 0), pady=8)

        # Bouton de recherche sans fond avec contour gris
        search_btn = ctk.CTkButton(
            search_frame, 
            text="", 
            image=load_icon(self.icons["search"], 18), 
            fg_color="transparent", 
            hover_color=THEME["premium_purple"], 
            text_color=THEME["primary_text"], 
            font=("Segoe UI", 13), 
            width=40, 
            corner_radius=12, 
            height=36,
            border_width=2,
            border_color=BORDER_COLOR,
            command=self.refresh_view
        )
        search_btn.pack(side="right", padx=(0, 8), pady=8)

        # Conteneur de cartes moderne avec design premium
        self.card_container = ctk.CTkScrollableFrame(self, fg_color="transparent", corner_radius=20)
        self.card_container.pack(fill="both", expand=True, padx=24, pady=(0, 20))
        
        self.refresh_view()

    def refresh_view(self):
        """Rafraîchit la vue premium avec optimisations de performance"""
        import time
        
        # Throttling pour éviter les rafraîchissements trop fréquents
        current_time = time.time()
        if current_time - self._last_refresh_time < self._refresh_throttle:
            return
        self._last_refresh_time = current_time
        
        # Nettoyer le container
        for w in self.card_container.winfo_children(): 
            w.destroy()
        
        # Utiliser le cache si disponible
        if self._cached_classes is None:
            self._cached_classes = get_all_classes()
        
        # Filtrer les classes avec cache
        search = self.search_var.get().lower().strip()
        level_filter = self.level_var.get()
        
        # Créer une clé de cache pour le filtre
        cache_key = f"{search}_{level_filter}"
        
        # Vérifier le cache de filtres
        if cache_key in self._filter_cache:
            filtered_classes = self._filter_cache[cache_key]
        else:
            # Filtrage optimisé par recherche textuelle
            if search:
                filtered_classes = [
                    c for c in self._cached_classes 
                    if search in (c['nom'] or '').lower() or 
                       search in (c['niveau'] or '').lower() or 
                       search in (c['annee'] or '').lower()
                ]
            else:
                filtered_classes = self._cached_classes.copy()
            
            # Filtrage par niveau avec cache
            if level_filter != "Tous les niveaux":
                level_key = f"level_{level_filter}"
                if level_key not in self._filter_cache:
                    if level_filter == "Lycée":
                        lycee_levels = ['1ère', 'TSM', 'Terminale', '2nde']
                        self._filter_cache[level_key] = [c for c in self._cached_classes if c['niveau'] in lycee_levels]
                    elif level_filter == "Collège":
                        college_levels = ['6ème', '5ème', '4ème', '3ème']
                        self._filter_cache[level_key] = [c for c in self._cached_classes if c['niveau'] in college_levels]
                    elif level_filter == "Primaire":
                        primaire_levels = ['CP', 'CE1', 'CE2', 'CM1', 'CM2']
                        self._filter_cache[level_key] = [c for c in self._cached_classes if c['niveau'] in primaire_levels]
                
                filtered_classes = [c for c in filtered_classes if c in self._filter_cache[level_key]]
            
            # Mettre en cache le résultat
            self._filter_cache[cache_key] = filtered_classes
        
        # Tri optimisé
        order_map = {"1ère": 1, "TSM": 2, "Terminale": 3, "2nde": 4, "6ème": 5, "5ème": 6, "4ème": 7, "3ème": 8}
        filtered_classes.sort(key=lambda classe: order_map.get(classe['nom'], float('inf')))
        
        # Récupérer les données associées avec cache
        if not hasattr(self, '_cached_profs') or not hasattr(self, '_cached_salles'):
            self._cached_profs = {p['id']: f"{p['nom']} {p['prenom']}" for p in get_all_professeurs()}
            self._cached_salles = {s['id']: s['nom'] for s in get_all_salles()}
        
        # Créer les cartes premium en lot
        self._create_premium_cards_batch(filtered_classes)
    
    def _create_premium_cards_batch(self, filtered_classes):
        """Crée les cartes premium en lot pour de meilleures performances"""
        num_columns = 2  # Format paysage avec 2 colonnes
        cards_to_create = []
        
        # Préparer toutes les cartes
        for idx, row in enumerate(filtered_classes):
            prof_name = self._cached_profs.get(row['prof_id'], '—')
            salle_name = self._cached_salles.get(row['salle_id'], '—')
            
            card = PremiumClassCard(self.card_container, row, prof_name, salle_name, self.on_edit, self.on_delete, self.icons)
            cards_to_create.append((card, idx))
        
        # Créer toutes les cartes en une seule fois
        for card, idx in cards_to_create:
            card.grid(row=idx // num_columns, column=idx % num_columns, padx=16, pady=16, sticky="nsew")
        
        # Configurer les colonnes pour le format paysage
        for i in range(num_columns):
            self.card_container.grid_columnconfigure(i, weight=1)
    
    def filter_view(self, event=None):
        """Filtre la vue premium en temps réel avec throttling"""
        # Utiliser after() pour éviter les appels trop fréquents
        if hasattr(self, '_filter_timer'):
            self.after_cancel(self._filter_timer)
        
        self._filter_timer = self.after(150, self.refresh_view)  # 150ms de délai
    
    def invalidate_cache(self):
        """Invalide le cache pour forcer un rafraîchissement complet"""
        self._cached_classes = None
        self._filter_cache.clear()
        if hasattr(self, '_cached_profs'):
            delattr(self, '_cached_profs')
        if hasattr(self, '_cached_salles'):
            delattr(self, '_cached_salles')

class ClassesManagerView(ctk.CTkFrame):
    """Vue principale moderne de gestion des classes avec le thème EduManager+"""
    def __init__(self, parent, icons):
        super().__init__(parent, fg_color=BG_MAIN)

        # Configuration des icônes avec gestion d'erreur améliorée
        _required_icon_keys = {"add","edit","delete","search","export","import","pdf","reload","view","class","teacher","settings"}
        _default_icons = {k: ICONS_PATH.get(k, "") for k in _required_icon_keys}
        incoming = icons or {}
        self.icons = {**_default_icons, **incoming}
        for k in _required_icon_keys:
            if k not in self.icons or not self.icons[k]:
                self.icons[k] = ""

        # Frame principal avec design moderne et élégant
        main_frame = ctk.CTkFrame(self, fg_color=BG_CARD, corner_radius=25, border_width=2, border_color=BORDER_COLOR)
        main_frame.pack(fill="both", expand=True, padx=3, pady=3)
        
        # Contenu principal
        main_content_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        main_content_frame.pack(fill="both", expand=True)

        # Vue des cartes modernes
        self.card_view = ModernClassesView(main_content_frame, self.open_edit_modal, self.delete_classe, None, self.icons)
        self.card_view.pack(fill="both", expand=True)


    def open_edit_modal(self, classe_id=None):
        """Modal moderne pour ajouter/modifier une classe - Design professionnel amélioré"""
        popup = ctk.CTkToplevel(self)
        popup.title("Ajouter une Classe" if classe_id is None else "Modifier la Classe")
        popup.geometry("900x700")
        popup.minsize(800, 600)
        popup.configure(fg_color=BG_MAIN)
        popup.grab_set()
        
        # Centrer la fenêtre au milieu de l'écran
        popup.update_idletasks()
        width = popup.winfo_width()
        height = popup.winfo_height()
        x = (popup.winfo_screenwidth() // 2) - (width // 2)
        y = (popup.winfo_screenheight() // 2) - (height // 2)
        popup.geometry(f"{width}x{height}+{x}+{y}")

        # Header moderne avec gradient et icône
        header_frame = ctk.CTkFrame(popup, fg_color=BG_SIDEBAR, corner_radius=0, height=90)
        header_frame.pack(fill="x")
        header_frame.pack_propagate(False)
        
        # Container du header avec padding
        header_content = ctk.CTkFrame(header_frame, fg_color="transparent")
        header_content.pack(fill="both", expand=True, padx=40, pady=20)
        
        # Icône principale avec effet
        main_icon = load_icon(self.icons.get("add" if classe_id is None else "edit"), 36)
        if main_icon:
            icon_container = ctk.CTkFrame(header_content, fg_color=BG_CARD_HOVER, width=60, height=60, corner_radius=30)
            icon_container.pack(side="left", padx=(0, 25))
            icon_container.pack_propagate(False)
            
            icon_label = ctk.CTkLabel(icon_container, image=main_icon, text="", fg_color="transparent")
            icon_label.pack(expand=True)
        
        # Titre et sous-titre
        title_frame = ctk.CTkFrame(header_content, fg_color="transparent")
        title_frame.pack(side="left", fill="y", expand=True)
        
        title_text = "Ajouter une nouvelle classe" if classe_id is None else "Modifier la classe"
        title_label = ctk.CTkLabel(title_frame, text=title_text, 
                                  font=(FONT_PRIMARY[0], 22, "bold"), text_color=WHITE, 
                                  fg_color="transparent", anchor="w")
        title_label.pack(anchor="w")
        
        subtitle_text = "Remplissez les informations de la classe" if classe_id is None else "Modifiez les informations de la classe"
        subtitle_label = ctk.CTkLabel(title_frame, text=subtitle_text, 
                                    font=(FONT_PRIMARY[0], 13), text_color=TEXT_SECONDARY, 
                                    fg_color="transparent", anchor="w")
        subtitle_label.pack(anchor="w", pady=(3, 0))
        
        # Container principal avec design moderne
        root = ctk.CTkFrame(popup, fg_color=BG_MAIN)
        root.pack(fill="both", expand=True, padx=25, pady=25)
        
        # Layout avec sidebar et contenu principal
        # Sidebar à droite avec navigation et actions - Design amélioré
        sidebar = ctk.CTkFrame(root, fg_color=BG_CARD, width=220, corner_radius=18, 
                              border_width=1, border_color=BORDER_COLOR)
        sidebar.pack(side="right", fill="y", padx=(25, 0))
        sidebar.pack_propagate(False)
        
        # Section principale avec le formulaire (à gauche)
        main_panel = ctk.CTkFrame(root, fg_color="transparent")
        main_panel.pack(side="left", fill="both", expand=True)
        
        # Navigation par sections dans le sidebar
        nav_items = [("infos", "Informations", "classroom"), 
                    ("details", "Détails", "person")]
        self.sections = {}
        self.tab_buttons = {}
        self.current_tab = ctk.StringVar(value="infos")
        
        # Container pour les boutons de navigation dans le sidebar
        nav_container = ctk.CTkFrame(sidebar, fg_color="transparent")
        nav_container.pack(fill="x", padx=20, pady=(20, 25))
        
        for key, label_text, icon_key in nav_items:
            # Charger l'icône pour le bouton
            nav_icon = load_icon(self.icons.get(icon_key), 20)
            
            # Container pour chaque bouton avec effet de profondeur
            btn_container = ctk.CTkFrame(nav_container, fg_color="transparent")
            btn_container.pack(fill="x", pady=(0, 12))
            
            btn = ctk.CTkButton(btn_container, text=label_text, 
                               fg_color=(TEXT_ACCENT if key == "infos" else BG_CARD_HOVER),
                               text_color=WHITE if key == "infos" else TEXT_PRIMARY,
                               font=(FONT_PRIMARY[0], 13, "bold"), hover_color=TEXT_ACCENT, 
                               corner_radius=15, height=50, image=nav_icon,
                               border_width=2 if key == "infos" else 1,
                               border_color=TEXT_ACCENT if key == "infos" else BORDER_COLOR,
                               command=lambda t=key: self.switch_tab(t, popup))
            btn.pack(fill="x")
            self.tab_buttons[key] = btn
        
        # Boutons d'action dans le sidebar
        actions_container = ctk.CTkFrame(sidebar, fg_color="transparent")
        actions_container.pack(fill="x", padx=20, pady=(0, 20))
        
        # Séparateur décoratif
        separator = ctk.CTkFrame(actions_container, fg_color=BORDER_COLOR, height=2, corner_radius=1)
        separator.pack(fill="x", pady=(0, 20))
        
        # Bouton Enregistrer sans fond avec contour gris
        save_btn_text = "Enregistrer" if classe_id else "Ajouter"
        save_icon = load_icon(self.icons.get("add" if classe_id is None else "edit"), 20)
        save_btn = ctk.CTkButton(actions_container, text=save_btn_text, 
                                font=(FONT_PRIMARY[0], 14, "bold"),
                                fg_color="transparent", text_color=TEXT_PRIMARY, hover_color=HOVER_PRIMARY,
                                corner_radius=15, command=lambda: self.save_class(classe_id, popup), 
                                height=55, image=save_icon, border_width=2, border_color=BORDER_COLOR)
        save_btn.pack(fill="x", pady=(0, 15))
        
        # Bouton Fermer avec design élégant
        close_icon = load_icon(self.icons.get("close"), 20)
        cancel_btn = ctk.CTkButton(actions_container, text="Fermer", 
                                  font=(FONT_PRIMARY[0], 13, "bold"),
                                  fg_color="transparent", text_color=TEXT_PRIMARY, hover_color=BORDER_COLOR,
                                  corner_radius=12, command=popup.destroy, 
                                  height=50, image=close_icon, border_width=1, border_color=BORDER_COLOR)
        cancel_btn.pack(fill="x")

        # Sections avec design amélioré (sans scroll) dans le panel principal
        self.sections["infos"] = ctk.CTkFrame(main_panel, fg_color="transparent", corner_radius=0)
        self.sections["details"] = ctk.CTkFrame(main_panel, fg_color="transparent", corner_radius=0)

        # Configuration des champs par section avec icônes personnalisées et design moderne
        self.fields_config = {
            "infos": [
                ("Nom de la classe", "nom", "entry", True, "classroom"),
                ("Niveau scolaire", "niveau", "entry", True, "book"),
                ("Année scolaire", "annee", "entry", True, "calendar"),
            ],
            "details": [
                ("Professeur principal", "prof_id", "combo", True, "person"),
                ("Salle de classe", "salle_id", "combo", True, "door"),
            ],
        }
        
        # Récupération des données
        profs_list = get_all_professeurs()
        profs_map = {p['id']: f"{p['nom']} {p['prenom']}" for p in profs_list}
        profs_values = ["Choisir un professeur..."] + list(profs_map.values())

        salles_list = get_all_salles()
        salles_map = {s['id']: f"{s['nom']}" for s in salles_list}
        salles_values = ["Choisir une salle..."] + list(salles_map.values())

        self.values_dict = {
            "prof_id": profs_values,
            "salle_id": salles_values,
        }
        
        data = {}
        if classe_id:
            row = get_classe_by_id(classe_id)
            if row:
                data = dict(row)

        self.data = data
        self.widgets = {}
        self.err_labels = {}

        # Construction des sections
        for section_key in self.fields_config:
            self.build_section(section_key, popup)
        
        # Initialisation
        self.switch_tab("infos", popup)

    def switch_tab(self, tab_key, popup):
        """Change d'onglet dans le formulaire avec transitions fluides."""
        # Mise à jour des boutons de navigation
        for key, btn in self.tab_buttons.items():
            is_active = (key == tab_key)
            fg_color = TEXT_ACCENT if is_active else BG_CARD_HOVER
            text_color = WHITE if is_active else TEXT_PRIMARY
            
            # Animation de transition des couleurs
            btn.configure(fg_color=fg_color, text_color=text_color)
            
            # Masquer toutes les sections
            if key in self.sections:
                self.sections[key].pack_forget()
        
        # Afficher la section active avec effet
        if tab_key in self.sections:
            self.sections[tab_key].pack(fill="both", expand=True, padx=0, pady=0)

    def build_section(self, section_key, popup):
        """Crée les widgets pour une section spécifique avec design moderne amélioré."""
        frame = self.sections[section_key]
        
        # Titre de section élégant avec icône
        section_titles = {
            "infos": "📋 Informations de base",
            "details": "👥 Détails de la classe"
        }
        
        # Container du titre avec design moderne
        title_container = ctk.CTkFrame(frame, fg_color="transparent")
        title_container.pack(fill="x", pady=(25, 30))
        
        section_title = ctk.CTkLabel(title_container, text=section_titles.get(section_key, "Section"), 
                                   font=(FONT_PRIMARY[0], 18, "bold"), text_color=TEXT_PRIMARY, 
                                   fg_color="transparent", anchor="w")
        section_title.pack(anchor="w")
        
        # Ligne décorative sous le titre
        separator = ctk.CTkFrame(title_container, fg_color=TEXT_ACCENT, height=3, corner_radius=2)
        separator.pack(fill="x", pady=(8, 0))
        
        # Container principal pour les champs avec disposition en grille (2 colonnes)
        fields_container = ctk.CTkFrame(frame, fg_color="transparent")
        fields_container.pack(fill="both", expand=True)
        
        # Créer les champs avec design moderne en disposition 2 par ligne
        fields = self.fields_config[section_key]
        for i in range(0, len(fields), 2):
            # Container pour une ligne de 2 champs
            row_container = ctk.CTkFrame(fields_container, fg_color="transparent")
            row_container.pack(fill="x", pady=(0, 15))
            
            # Premier champ de la ligne
            if i < len(fields):
                spec = fields[i]
                field_widget = self.create_field_widget(spec, row_container, side="left")
            
            # Deuxième champ de la ligne (si il existe)
            if i + 1 < len(fields):
                spec = fields[i + 1]
                field_widget = self.create_field_widget(spec, row_container, side="right")
    
    def create_field_widget(self, spec, parent, side):
        """Crée un widget de champ avec design amélioré."""
        label, key, wtype, required, icon_key = spec
        value = self.data.get(key, '')
        
        # Container pour chaque champ avec design amélioré
        field_container = ctk.CTkFrame(parent, fg_color=BG_CARD, corner_radius=12, 
                                     border_width=1, border_color=BORDER_COLOR)
        field_container.pack(side=side, fill="both", expand=True, padx=(0, 10) if side == "left" else (10, 0))
        
        # Header du champ avec icône et label
        field_header = ctk.CTkFrame(field_container, fg_color="transparent")
        field_header.pack(fill="x", padx=15, pady=(15, 10))
        
        # Icône du champ avec container circulaire
        icon_container = ctk.CTkFrame(field_header, fg_color=BG_CARD_HOVER, width=32, height=32, 
                                    corner_radius=16)
        icon_container.pack(side="left", padx=(0, 10))
        icon_container.pack_propagate(False)
        
        field_icon = load_icon(self.icons.get(icon_key), 16)
        if field_icon:
            icon_label = ctk.CTkLabel(icon_container, image=field_icon, text="", fg_color="transparent")
            icon_label.pack(expand=True)
        
        # Label du champ
        label_widget = ctk.CTkLabel(field_header, text=f"{label}{' *' if required else ''}", 
                                   font=(FONT_PRIMARY[0], 12, "bold"), text_color=TEXT_PRIMARY, 
                                   fg_color="transparent", anchor="w")
        label_widget.pack(side="left", fill="x", expand=True)
        
        # Champ de saisie avec design amélioré
        if wtype == "combo":
            w = ctk.CTkComboBox(field_container, values=self.values_dict[key], state="readonly", 
                              font=(FONT_PRIMARY[0], 12), fg_color=BG_CARD_HOVER, text_color=TEXT_PRIMARY,
                              border_color=TEXT_ACCENT, button_color=TEXT_ACCENT,
                              corner_radius=8, border_width=1, height=42,
                              dropdown_font=(FONT_PRIMARY[0], 12))
            
            if value and key in self.values_dict:
                if key == "prof_id":
                    prof_id = value
                    profs_map = {p['id']: f"{p['nom']} {p['prenom']}" for p in get_all_professeurs()}
                    selected_value = next((v for k, v in profs_map.items() if k == prof_id), "Choisir un professeur...")
                    w.set(selected_value)
                elif key == "salle_id":
                    salle_id = value
                    salles_map = {s['id']: s['nom'] for s in get_all_salles()}
                    selected_value = next((v for k, v in salles_map.items() if k == salle_id), "Choisir une salle...")
                    w.set(selected_value)
            else:
                w.set(self.values_dict[key][0])
        else:
            w = ctk.CTkEntry(field_container, font=(FONT_PRIMARY[0], 12), fg_color=BG_CARD_HOVER, 
                            text_color=TEXT_PRIMARY, border_color=TEXT_ACCENT, corner_radius=8, 
                            border_width=1, height=42)
            w.insert(0, value)

        w.pack(fill="x", padx=15, pady=(0, 15))
        
        # Label d'erreur
        error_lbl = ctk.CTkLabel(field_container, text="", font=(FONT_PRIMARY[0], 10), 
                                text_color=ERROR_RED, fg_color="transparent")
        error_lbl.pack(anchor="w", padx=15, pady=(0, 10))
        
        self.widgets[key] = w
        self.err_labels[key] = error_lbl
        
        return field_container

    def save_class(self, classe_id, popup):
        """Sauvegarde la classe avec validation élégante."""
        # Validation des champs requis
        errors = {}
        for section in self.fields_config.values():
            for spec in section:
                key = spec[1]
                required = spec[3]
                value = self.widgets[key].get().strip()
                
                if required and not value:
                    errors[key] = "Champ obligatoire."
                elif key in ["prof_id", "salle_id"] and value in ["Choisir un professeur...", "Choisir une salle..."]:
                    errors[key] = "Veuillez faire un choix."
        
        # Affichage des erreurs avec style élégant
        for key, error_msg in errors.items():
            if key in self.err_labels:
                self.err_labels[key].configure(text=error_msg)
                if key in self.widgets:
                    self.widgets[key].configure(border_color=ERROR_RED)
        
        # Effacement des erreurs pour les champs valides
        for key in self.widgets:
            if key not in errors:
                if key in self.err_labels:
                    self.err_labels[key].configure(text="")
                if key in self.widgets:
                    self.widgets[key].configure(border_color=BORDER_COLOR)
        
        if errors:
            messagebox.showerror("Erreur de validation", 
                                f"Veuillez corriger {len(errors)} erreur(s) avant de continuer.", 
                                parent=popup)
            return
        
        # Récupération des données
        nom = self.widgets["nom"].get().strip()
        niveau = self.widgets["niveau"].get().strip()
        annee = self.widgets["annee"].get().strip()
        
        prof_str = self.widgets["prof_id"].get()
        prof_id = next((k for k, v in {p['id']: f"{p['nom']} {p['prenom']}" for p in get_all_professeurs()}.items() if v == prof_str), None)
        
        salle_str = self.widgets["salle_id"].get()
        salle_id = next((k for k, v in {s['id']: s['nom'] for s in get_all_salles()}.items() if v == salle_str), None)
        
        # Sauvegarde avec messages élégants
        if classe_id:
            success = update_class_data(classe_id, nom, prof_id, salle_id, niveau, annee)
            if success:
                messagebox.showinfo("Succès", f"La classe '{nom}' a été modifiée avec succès !", parent=popup)
            else:
                messagebox.showerror("Erreur", "Une erreur est survenue lors de la modification.", parent=popup)
        else:
            success = add_class(nom, prof_id, salle_id, niveau, annee)
            if success:
                messagebox.showinfo("Succès", f"La classe '{nom}' a été ajoutée avec succès !", parent=popup)
            else:
                messagebox.showerror("Erreur", "Une erreur est survenue lors de l'ajout.", parent=popup)
                
        if success:
            popup.destroy()
            self.card_view.refresh_view()
            if hasattr(self, 'statsbar'):
                    self.statsbar.refresh()

    def delete_classe(self, classe_id):
        classe_data = get_classe_by_id(classe_id)
        classe_name = classe_data['nom'] if classe_data else "cette classe"

        confirmation = messagebox.askyesno(
            "Confirmation de suppression",
            f"Voulez-vous vraiment supprimer la classe '{classe_name}' et TOUS les élèves qui en font partie ?\n"
            "Cette action est irréversible."
        )

        if confirmation:
            if delete_class(classe_id):
                self.notif_bar.show("Classe et élèves supprimés avec succès.", SUCCESS_GREEN)
                self.card_view.refresh_view()
                self.statsbar.refresh()
            else:
                self.notif_bar.show("Erreur lors de la suppression.", ERROR_RED)

if __name__ == "__main__":
    # Configuration du thème global (si disponible)
    pass
    
    # Configuration de la base de données
    try:
        from database.connection import create_all_tables
        create_all_tables()
    except ImportError:
        # Création des tables de base si le module n'est pas disponible
        setup_database()
    
    # Création de la fenêtre principale
    root = ctk.CTk()
    root.title("EduManager+ : Gestion des Classes Moderne")
    root.state('zoomed')
    root.minsize(1000, 700)
    root.configure(fg_color=BG_MAIN)

    # Configuration des icônes
    icons_to_load = {}
    for key, path in ICONS_PATH.items():
        icons_to_load[key] = path

    # Lancement de l'application
    ClassesManagerView(root, icons_to_load).pack(fill="both", expand=True)
    
    print("🚀 EduManager+ - Gestion des Classes v6.0 Moderne lancée avec succès !")
    print(f"📊 Thème: {BG_MAIN} (sombre moderne avec thème global)")
    print(f"🎨 Icônes: {len(icons_to_load)} icônes personnalisées chargées")
    print("✨ Design moderne avec cartes élégantes et en-tête comme les autres vues")
    print("🎯 Utilisation exclusive de vos icônes dans resources/icons")
    
    root.mainloop()