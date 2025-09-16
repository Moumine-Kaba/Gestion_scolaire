
# -*- coding: utf-8 -*-
"""
Dashboard des Élèves - Utilise le thème global EduManager+
- Thème sombre parfait avec couleurs harmonieuses
- Design moderne et professionnel
- Interface utilisateur optimisée
"""

import os
import sys
import datetime
import sqlite3
import tkinter as tk
from tkinter import messagebox, ttk, filedialog
import customtkinter as ctk
from PIL import Image, ImageTk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk

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
    FONT_PRIMARY = ("Segoe UI", 16)
    FONT_SECONDARY = ("Segoe UI", 14)
    FONT_TITLE = ("Segoe UI", 28, "bold")
    FONT_SUBTITLE = ("Segoe UI", 22, "bold")
    FONT_SMALL = ("Segoe UI", 13)
    FONT_BUTTON = ("Segoe UI", 15, "bold")
    FONT_CARD_TITLE = ("Segoe UI", 20, "bold")
    FONT_METRIC = ("Segoe UI", 24, "bold")
    FONT_PREMIUM = ("Segoe UI", 21, "bold")
    FONT_ACCENT = ("Segoe UI", 15, "bold")
    FONT_HERO = ("Segoe UI", 32, "bold")
    
    # Espacements
    PADDING_SMALL = 10
    PADDING_MEDIUM = 18
    PADDING_LARGE = 28
    PADDING_XLARGE = 36
    PADDING_CARD = 24
    PADDING_BUTTON = 18
    PADDING_PREMIUM = 32
    PADDING_HERO = 40
    MARGIN_SMALL = 8
    MARGIN_MEDIUM = 16
    MARGIN_LARGE = 24
    MARGIN_CARD = 18
    MARGIN_SECTION = 24
    MARGIN_PREMIUM = 32
    MARGIN_HERO = 40

# =================== CHEMINS =====================
# DB - Chemin absolu vers la base de données
DB_PATH = r"C:\Users\Lenovo\Desktop\Clonage_git\Gestion_scolaire\Gestion_scolaire\database\edumanager.db"

# ICÔNES (absolu demandé + fallback relatif)
ICONS_DIR_ABS = r"C:\Users\Lenovo\Desktop\Clonage_git\Gestion_scolaire\Gestion_scolaire\resources\icons"
ICONS_DIR_REL = os.path.normpath(
    os.path.join(os.path.dirname(__file__), "..", "..", "..", "..", "resources", "icons")
)
ICONS_DIR = ICONS_DIR_ABS if os.path.isdir(ICONS_DIR_ABS) else ICONS_DIR_REL

# =================== CACHE ICÔNES =====================
_ICON_CACHE = {}

def get_icon(name: str, size=(24, 24)):
    """Cache d'icônes PIL → CTkImage optimisé."""
    key = f"{name}_{size[0]}x{size[1]}"
    if key in _ICON_CACHE:
        return _ICON_CACHE[key]
    
    icon_path = os.path.join(ICONS_DIR, f"{name}.png")
    if not os.path.exists(icon_path):
        # Retourner une icône par défaut simple
        return None
    
    try:
        pil_img = Image.open(icon_path).convert("RGBA")
        # Optimiser la taille pour réduire la charge
        pil_img = pil_img.resize(size, Image.Resampling.LANCZOS)
        ctk_img = ctk.CTkImage(light_image=pil_img, dark_image=pil_img, size=size)
        _ICON_CACHE[key] = ctk_img
        return ctk_img
    except Exception as e:
        print(f"⚠️ Erreur icône {name}: {e}")
        return None

# =================== MAPPING ICONES =====================
ICON_MAP = {
    "eleve": "eleve", "filles": "eleve", "garcons": "person", "classes": "cover",
    "profs": "profs", "ajouter": "add", "edit": "edit", "delete": "delete",
    "detail": "detail", "transferer": "transfer", "refresh": "refresh", "search": "search",
    "group": "group", "person": "person", "home": "home", "logout": "logout"
}

# =================== SQLITE HELPERS =====================
def get_conn():
    """Connexion SQLite avec timeout + WAL + row_factory."""
    try:
        conn = sqlite3.connect(DB_PATH, timeout=10, check_same_thread=False)
        conn.row_factory = sqlite3.Row
        try:
            conn.execute("PRAGMA journal_mode=WAL;")
            conn.execute("PRAGMA busy_timeout=10000;")
        except Exception:
            pass
        return conn
    except Exception as e:
        print(f"⚠️ Connexion DB échouée: {e}")
        return None

def get_stats_count_any(*table_candidates) -> int:
    """Renvoie COUNT(*) pour la première table existante parmi table_candidates."""
    conn = get_conn()
    if not conn:
        return 0
    try:
        cur = conn.cursor()
        table_name = None
        for t in table_candidates:
            cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND lower(name)=lower(?)", (t,))
            if cur.fetchone():
                table_name = t
                break
        if not table_name:
            return 0
        cur.execute(f"SELECT COUNT(*) FROM {table_name}")
        r = cur.fetchone()
        return int((r[0] if not isinstance(r, sqlite3.Row) else r[0]) or 0)
    except Exception as e:
        print(f"⚠️ get_stats_count_any: {e}")
        return 0
    finally:
        try:
            conn.close()
        except:
            pass

def get_stats_eleves(classe_id=None):
    """Récupère les statistiques des élèves avec les vraies données."""
    conn = get_conn()
    if not conn:
        return {"total": 0, "filles": 0, "garcons": 0, "classes": 0, "profs": 0}
    
    try:
        cur = conn.cursor()
        stats = {}
        
        if classe_id is None:
            # Statistiques globales
            cur.execute("SELECT COUNT(*) FROM eleves")
            stats["total"] = cur.fetchone()[0] or 0
            
            cur.execute("SELECT COUNT(*) FROM eleves WHERE genre LIKE 'F%' OR genre LIKE 'f%'")
            stats["filles"] = cur.fetchone()[0] or 0
            
            cur.execute("SELECT COUNT(*) FROM eleves WHERE genre LIKE 'M%' OR genre LIKE 'm%'")
            stats["garcons"] = cur.fetchone()[0] or 0
            
            cur.execute("SELECT COUNT(*) FROM classes")
            stats["classes"] = cur.fetchone()[0] or 0
            
            # Compter les professeurs (table professeurs si elle existe)
            try:
                cur.execute("SELECT COUNT(*) FROM professeurs")
                stats["profs"] = cur.fetchone()[0] or 0
            except:
                stats["profs"] = 0
        else:
            # Statistiques pour une classe spécifique
            cur.execute("SELECT COUNT(*) FROM eleves WHERE id_classe=?", (classe_id,))
            stats["total"] = cur.fetchone()[0] or 0
            
            cur.execute("SELECT COUNT(*) FROM eleves WHERE (genre LIKE 'F%' OR genre LIKE 'f%') AND id_classe=?", (classe_id,))
            stats["filles"] = cur.fetchone()[0] or 0
            
            cur.execute("SELECT COUNT(*) FROM eleves WHERE (genre LIKE 'M%' OR genre LIKE 'm%') AND id_classe=?", (classe_id,))
            stats["garcons"] = cur.fetchone()[0] or 0
            
            stats["classes"] = 1
            stats["profs"] = 1
        
        return stats
    except Exception as e:
        print(f"⚠️ get_stats_eleves: {e}")
        return {"total": 0, "filles": 0, "garcons": 0, "classes": 0, "profs": 0}
    finally:
        try:
            conn.close()
        except:
            pass

def fetch_effectifs_par_classe(limit: int = 10):
    """Retourne [(nom_classe, effectif)] sur base classes et eleves."""
    conn = get_conn()
    if not conn:
        return []
    try:
        cur = conn.cursor()
        cur.execute("""
            SELECT c.nom_classe, COUNT(e.id_eleve) as effectif
            FROM classes c
            LEFT JOIN eleves e ON c.id_classe = e.id_classe
            GROUP BY c.id_classe, c.nom_classe
            ORDER BY effectif DESC
            LIMIT ?
        """, (limit,))
        return [(r[0], r[1]) for r in cur.fetchall()]
    except Exception as e:
        print(f"⚠️ fetch_effectifs_par_classe: {e}")
        return []
    finally:
        try:
            conn.close()
        except:
            pass

def get_all_classes():
    """Récupère toutes les classes depuis la base de données"""
    conn = get_conn()
    if not conn:
        return []
    try:
        cur = conn.cursor()
        cur.execute("SELECT nom_classe, niveau FROM classes ORDER BY niveau, nom_classe")
        return cur.fetchall()
    except Exception as e:
        print(f"⚠️ get_all_classes: {e}")
        return []
    finally:
        try:
            conn.close()
        except:
            pass

def get_eleves_list(classe_id=None):
    """Récupère la liste des élèves avec les vraies données - Optimisé."""
    conn = get_conn()
    if not conn:
        return []
    try:
        cur = conn.cursor()
        if classe_id is None:
            cur.execute("""
                SELECT id_eleve, nom, prenom, genre, date_naissance, statut, id_classe 
                FROM eleves 
                ORDER BY nom, prenom
                LIMIT 1000
            """)
        else:
            cur.execute("""
                SELECT id_eleve, nom, prenom, genre, date_naissance, statut, id_classe 
                FROM eleves 
                WHERE id_classe=? 
                ORDER BY nom, prenom
            """, (classe_id,))
        return cur.fetchall()
    except Exception as e:
        print(f"⚠️ get_eleves_list: {e}")
        return []
    finally:
        try:
            conn.close()
        except:
            pass

def get_classe_name(classe_id):
    """Récupère le nom d'une classe."""
    if classe_id is None:
        return None
    conn = get_conn()
    if not conn:
        return None
    try:
        cur = conn.cursor()
        cur.execute("SELECT nom_classe FROM classes WHERE id_classe=?", (classe_id,))
        row = cur.fetchone()
        return row[0] if row else None
    except Exception as e:
        print(f"⚠️ get_classe_name: {e}")
        return None
    finally:
        try:
            conn.close()
        except:
            pass

def get_classe_id_by_name(classe_name):
    """Récupère l'ID d'une classe par son nom."""
    if classe_name is None:
        return None
    conn = get_conn()
    if not conn:
        return None
    try:
        cur = conn.cursor()
        cur.execute("SELECT id_classe FROM classes WHERE nom_classe=?", (classe_name,))
        row = cur.fetchone()
        return row[0] if row else None
    except Exception as e:
        print(f"⚠️ get_classe_id_by_name: {e}")
        return None
    finally:
        try:
            conn.close()
        except:
            pass

def get_eleve_complet(eleve_id):
    """Récupère les détails complets d'un élève."""
    conn = get_conn()
    if not conn:
        return None
    try:
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("""
            SELECT 
                id_eleve, matricule, nom, prenom, date_naissance, genre, adresse, 
                telephone, email, id_classe, statut, date_inscription,
                parent_nom, parent_prenom, parent_telephone, parent_email, 
                parent_adresse, parent_profession
            FROM eleves 
            WHERE id_eleve=?
        """, (eleve_id,))
        row = cur.fetchone()
        return dict(row) if row else None
    except Exception as e:
        print(f"⚠️ get_eleve_complet: {e}")
        return None
    finally:
        try:
            conn.close()
        except:
            pass

def compute_age(date_str: str):
    """Calcule l'âge à partir de la date de naissance."""
    if not date_str:
        return "—"
    try:
        y, m, d = (int(x) for x in date_str.split("-"))
        today = datetime.date.today()
        age = today.year - y - ((today.month, today.day) < (m, d))
        return str(age)
    except Exception:
        return "—"

# =================== APPLICATION PRINCIPALE =====================
class DashboardEleves(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color=BG_MAIN)
        self.selected_classe = None
        self.selected_classe_id = None
        self.classes_map = {}
        self.last_action_time = None
        self.last_action_type = None

        # Configuration de la grille principale
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=0, minsize=250)

        # Création des sections principales
        self._create_main_content()
        self._create_sidebar()
        
        # Initialisation
        self.update_classes_sidebar()
        self.refresh_dashboard()

    def _create_main_content(self):
        """Crée le contenu principal avec le design du dashboard principal"""
        main_frame = ctk.CTkFrame(self, fg_color="transparent")
        main_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 10), pady=10)
        main_frame.grid_rowconfigure(3, weight=1)
        main_frame.grid_columnconfigure(0, weight=1)

        # Création des sections
        self._create_header(main_frame)
        self._create_stats_cards(main_frame)
        self._create_chart_section(main_frame)
        self._create_crud_buttons_section(main_frame)

    def _create_header(self, parent):
        """Header moderne avec thème global et marges optimisées"""
        header_frame = ctk.CTkFrame(parent, fg_color="transparent")
        header_frame.pack(fill="x", pady=(0, PADDING_MEDIUM))
        header_frame.grid_columnconfigure(0, weight=1)
        header_frame.grid_columnconfigure(1, weight=1)

        # Section gauche - Titre principal avec meilleures marges
        greetings_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        greetings_frame.grid(row=0, column=0, sticky="w", padx=(PADDING_MEDIUM, 0))

        greeting_content = ctk.CTkFrame(greetings_frame, fg_color="transparent")
        greeting_content.pack(anchor="w", pady=(PADDING_SMALL, 0))

        greeting_icon = get_icon("eleve", (32, 32))
        if greeting_icon:
            glb = ctk.CTkLabel(greeting_content, text="", image=greeting_icon, text_color=TEXT_ACCENT)
            glb._imgref = greeting_icon
            glb.pack(side="left", padx=(0, PADDING_SMALL))

        ctk.CTkLabel(greeting_content, text="Gestion des Élèves",
                     font=FONT_HERO, text_color=TEXT_ACCENT).pack(side="left")

        ctk.CTkLabel(greetings_frame, text="Tableau de bord intelligent des élèves de l'établissement",
                     font=FONT_SECONDARY, text_color=TEXT_SECONDARY).pack(anchor="w", pady=(MARGIN_SMALL, 0))

        # Section droite - Recherche et rafraîchissement avec meilleures marges
        search_refresh_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        search_refresh_frame.grid(row=0, column=1, sticky="e", padx=(0, PADDING_MEDIUM))

        self.search_var = ctk.StringVar()
        self.search_entry = ctk.CTkEntry(search_refresh_frame, placeholder_text="Rechercher un élève...", width=250,
                         fg_color=BG_CARD, text_color=TEXT_PRIMARY, border_color=BORDER_COLOR,
                         corner_radius=12, font=FONT_SECONDARY, textvariable=self.search_var,
                         placeholder_text_color=TEXT_MUTED)
        self.search_entry.pack(side="left", padx=(0, PADDING_SMALL))

        refresh_icon = get_icon("refresh", (20, 20))
        btn_refresh = ctk.CTkButton(search_refresh_frame, text="", image=refresh_icon, width=45, height=45,
                                    fg_color=BG_CARD, hover_color=BG_CARD_HOVER, corner_radius=12,
                                    command=self.refresh_dashboard, border_width=1, border_color=BORDER_COLOR)
        if refresh_icon:
            btn_refresh._imgref = refresh_icon
        btn_refresh.pack(side="left")

    def _create_stats_cards(self, parent):
        """Cartes de statistiques inspirées du dashboard principal"""
        self.stats_frame = ctk.CTkFrame(parent, fg_color="transparent")
        self.stats_frame.pack(fill="x", pady=(5, 8))
        
        # Initialiser les listes pour les références
        self.stats_cards = []
        self.stats_subtexts = []
        
        # Créer les cartes de statistiques
        stats_data = [
            ("Total Élèves", "eleve", SUCCESS_GREEN),
            ("Filles", "filles", WARNING_ORANGE),
            ("Garçons", "garcons", ERROR_RED),
            ("Classes", "classes", PRIMARY_BLUE)
        ]
        
        for i, (title, icon_name, color) in enumerate(stats_data):
            card = ctk.CTkFrame(self.stats_frame, fg_color=BG_CARD, corner_radius=15, border_width=1, border_color=BORDER_COLOR)
            card.pack(side="left", fill="both", expand=True, padx=(0, 8) if i < 3 else 0)
            
            # Header de la carte
            header_frame = ctk.CTkFrame(card, fg_color="transparent")
            header_frame.pack(fill="x", padx=PADDING_SMALL, pady=(PADDING_SMALL, MARGIN_SMALL))
            
            # Icône avec badge coloré
            icon_badge = ctk.CTkFrame(header_frame, fg_color=color, corner_radius=18, width=36, height=36)
            icon_badge.pack_propagate(False)
            icon_badge.pack(side="left")
            
            icon = get_icon(icon_name, (18, 18))
            if icon:
                icon_label = ctk.CTkLabel(icon_badge, text="", image=icon, text_color=WHITE)
                icon_label.pack(expand=True)
            
            # Titre
            title_label = ctk.CTkLabel(header_frame, text=title, font=FONT_SECONDARY, text_color=TEXT_SECONDARY)
            title_label.pack(side="right")
            
            # Valeur principale
            value_label = ctk.CTkLabel(card, text="0", font=FONT_METRIC, text_color=TEXT_PRIMARY)
            value_label.pack(pady=(0, MARGIN_SMALL))
            self.stats_cards.append(value_label)
            
            # Sous-texte
            subtext_label = ctk.CTkLabel(card, text="Mise à jour en temps réel", font=FONT_SMALL, text_color=TEXT_MUTED)
            subtext_label.pack(pady=(0, PADDING_SMALL))
            self.stats_subtexts.append(subtext_label)
            
            # Barre de progression
            progress_frame = ctk.CTkFrame(card, fg_color="transparent")
            progress_frame.pack(fill="x", padx=PADDING_SMALL, pady=(0, PADDING_SMALL))
            
            progress_bar = ctk.CTkProgressBar(progress_frame, progress_color=color, height=8, corner_radius=4)
            progress_bar.pack(fill="x")
            progress_bar.set(0.7)  # Valeur par défaut
        
        self.refresh_stats()

    def refresh_dashboard(self):
        """Rafraîchit le dashboard"""
        self.update_last_action("Rafraîchissement", "Actualisation des données")
        self.update_dashboard_for_classe(self.selected_classe)

    def refresh_stats_for_classe(self, classe_id):
        """Met à jour les statistiques pour une classe spécifique"""
        try:
            # Utiliser la fonction refresh_stats qui gère correctement la recréation des cartes
            self.refresh_stats()
        except Exception as e:
            print(f"⚠️ Erreur mise à jour stats pour classe: {e}")

    def refresh_stats(self):
        """Met à jour les statistiques avec le style du dashboard principal"""
        # Utiliser la fonction adaptée aux vraies données
        stats = get_stats_eleves(self.selected_classe_id)
        
        eleves = stats["total"]
        filles = stats["filles"]
        garcons = stats["garcons"]
        classes = stats["classes"]

        maxv = max(1, eleves, classes)

        data = [
            ("Total Élèves", eleves, "eleves", SUCCESS_GREEN, eleves/maxv),
            ("Filles", filles, "filles", PRIMARY_BLUE, filles/maxv),
            ("Garçons", garcons, "garcons", WARNING_ORANGE, garcons/maxv),
            ("Classes", classes, "classes", ERROR_RED, classes/maxv),
        ]

        # Détruire les anciennes cartes
        for w in self.stats_frame.winfo_children():
            w.destroy()

        # Réinitialiser les listes de références
        self.stats_cards = []
        self.stats_subtexts = []

        # Recréer les cartes
        for i, (t, v, ic, col, ratio) in enumerate(data):
            card_widget, value_label, subtext_label = self.stat_card(self.stats_frame, t, v, ic, col, ratio)
            card_widget.grid(row=0, column=i, padx=6, sticky="nsew")
            self.stats_frame.grid_columnconfigure(i, weight=1)
            
            # Stocker les références des labels
            self.stats_cards.append(value_label)
            self.stats_subtexts.append(subtext_label)

    def stat_card(self, parent, title, value, icon_key, color, ratio=0.0):
        """Carte stat premium (badge, sous-texte, mini progress, hover glow)."""
        wrap = ctk.CTkFrame(parent, fg_color=BG_CARD, corner_radius=16, border_width=1, border_color=BORDER_COLOR)
        wrap.grid_columnconfigure(0, weight=1)

        header = ctk.CTkFrame(wrap, fg_color="transparent")
        header.pack(fill="x", padx=PADDING_SMALL, pady=(PADDING_SMALL, MARGIN_SMALL))

        badge = ctk.CTkFrame(header, fg_color=BG_CARD_HOVER, corner_radius=999, width=30, height=30,
                             border_width=1, border_color=BORDER_COLOR)
        badge.pack_propagate(False); badge.pack(side="left")

        icon_img = get_icon(ICON_MAP.get(icon_key, "home"), (14, 14))
        if icon_img:
            lbl = ctk.CTkLabel(badge, text="", image=icon_img, text_color=color)
            lbl._imgref = icon_img
            lbl.pack(expand=True)

        ctk.CTkLabel(header, text=title, font=FONT_SMALL, text_color=TEXT_SECONDARY)\
            .pack(side="left", padx=PADDING_SMALL)

        # Créer les labels et les stocker dans les listes
        value_label = ctk.CTkLabel(wrap, text=str(value), font=("Segoe UI", 18, "bold"), text_color=TEXT_PRIMARY)
        value_label.pack(anchor="w", padx=PADDING_SMALL)
        
        subtext_label = ctk.CTkLabel(wrap, text="Mise à jour en temps réel", font=("Segoe UI", 9), text_color=TEXT_SECONDARY)
        subtext_label.pack(anchor="w", padx=PADDING_SMALL, pady=(0, MARGIN_SMALL))

        pb_bg = ctk.CTkFrame(wrap, fg_color=BG_CARD_HOVER, corner_radius=8, height=8, border_width=1, border_color=BORDER_COLOR)
        pb_bg.pack(fill="x", padx=PADDING_SMALL, pady=(MARGIN_SMALL, PADDING_SMALL))
        pb_fg = ctk.CTkFrame(pb_bg, fg_color=color, corner_radius=8, height=6)
        pb_fg.place(relx=0, rely=0.5, anchor="w", relwidth=max(0.05, min(1.0, ratio)), relheight=0.7)

        def _enter(_): wrap.configure(border_color=TEXT_ACCENT)
        def _leave(_): wrap.configure(border_color=BORDER_COLOR)
        wrap.bind("<Enter>", _enter); wrap.bind("<Leave>", _leave)
        for w in wrap.winfo_children():
            w.bind("<Enter>", _enter); w.bind("<Leave>", _leave)
        
        # Retourner les références des widgets
        return wrap, value_label, subtext_label

    def _create_chart_section(self, parent):
        """Section de graphique inspirée du dashboard principal"""
        self.chart_container = ctk.CTkFrame(
            parent, 
            fg_color=BG_CARD, 
            corner_radius=10, 
            border_width=1, 
            border_color=BORDER_COLOR
        )
        self.chart_container.pack(fill="x", pady=(0, 8))
        
        ctk.CTkLabel(self.chart_container, text="Répartition des Élèves par Classe",
                     font=("Segoe UI", 22, "bold"), text_color=TEXT_PRIMARY).pack(padx=10, pady=(10, 4), anchor="w")
        ctk.CTkLabel(self.chart_container, text="Distribution des effectifs par classe",
                     font=("Segoe UI", 11), text_color=TEXT_SECONDARY).pack(padx=10, pady=(0, 8), anchor="w")

    def _create_crud_buttons_section(self, parent):
        """Section des boutons CRUD juste après le graphique"""
        crud_container = ctk.CTkFrame(
            parent, 
            fg_color=BG_CARD, 
            corner_radius=12,
            border_width=1,
            border_color=BORDER_COLOR
        )
        crud_container.pack(fill="x", pady=(PADDING_SMALL, 0))
        
        # Conteneur des boutons avec espacement optimisé
        buttons_frame = ctk.CTkFrame(crud_container, fg_color="transparent")
        buttons_frame.pack(fill="x", padx=PADDING_MEDIUM, pady=(PADDING_MEDIUM, PADDING_MEDIUM))
        
        # Configuration de la grille pour centrer les boutons (3 colonnes seulement)
        for i in range(3):
            buttons_frame.grid_columnconfigure(i, weight=1)
        
        # Bouton Ajouter
        add_icon = get_icon("add", (20, 20))
        btn_add = ctk.CTkButton(
            buttons_frame, 
            text="Ajouter Élève", 
            image=add_icon,
            fg_color=SUCCESS_GREEN, 
            text_color=WHITE, 
            hover_color=HOVER_SUCCESS,
            command=self.ajouter_eleve,
            corner_radius=15, 
            height=50,
            width=150,
            border_width=2,
            border_color=SUCCESS_GREEN,
            font=("Segoe UI", 14, "bold")
        )
        if add_icon:
            btn_add._imgref = add_icon
        btn_add.grid(row=0, column=0, padx=PADDING_SMALL, pady=PADDING_SMALL)
        
        # Bouton Afficher tous les élèves
        show_all_icon = get_icon("group", (20, 20))
        btn_show_all = ctk.CTkButton(
            buttons_frame, 
            text="Voir tous les élèves", 
            image=show_all_icon,
            fg_color="transparent", 
            text_color=TEXT_ACCENT, 
            hover_color=BG_CARD_HOVER,
            command=self.afficher_tous_eleves_classe,
            corner_radius=15, 
            height=50,
            width=180,
            border_width=2,
            border_color=TEXT_ACCENT,
            font=("Segoe UI", 14, "bold")
        )
        if show_all_icon:
            btn_show_all._imgref = show_all_icon
        btn_show_all.grid(row=0, column=1, padx=PADDING_SMALL, pady=PADDING_SMALL)
        
        # Bouton Transfert
        transfer_icon = get_icon("transfer", (20, 20))
        btn_transfer = ctk.CTkButton(
            buttons_frame, 
            text="Transfert", 
            image=transfer_icon,
            fg_color=WARNING_ORANGE, 
            text_color=WHITE, 
            hover_color=HOVER_WARNING,
            command=self.transferer_eleve,
            corner_radius=15, 
            height=50,
            width=130,
            border_width=2,
            border_color=WARNING_ORANGE,
            font=("Segoe UI", 14, "bold")
        )
        if transfer_icon:
            btn_transfer._imgref = transfer_icon
        btn_transfer.grid(row=0, column=2, padx=PADDING_SMALL, pady=PADDING_SMALL)
        
        # Affichage des actions récentes
        self.action_info_frame = ctk.CTkFrame(crud_container, fg_color="transparent")
        self.action_info_frame.pack(fill="x", padx=PADDING_MEDIUM, pady=(0, PADDING_SMALL))
        
        # Label pour les actions récentes
        self.action_label = ctk.CTkLabel(
            self.action_info_frame,
            text="Dernière action : Aucune",
            font=("Segoe UI", 10),
            text_color=TEXT_SECONDARY
        )
        self.action_label.pack(side="left")
        
        # Initialiser l'heure actuelle
        self.update_last_action("Initialisation", "Dashboard chargé")


    def _create_sidebar(self):
        """Sidebar magnifique avec thème global et design premium"""
        sidebar = ctk.CTkFrame(
            self, 
            fg_color=BG_SIDEBAR, 
            width=180, 
            corner_radius=20,
            border_width=2, 
            border_color=BORDER_COLOR
        )
        sidebar.grid(row=0, column=1, sticky="nsew", padx=(0, PADDING_SMALL), pady=PADDING_SMALL)
        sidebar.grid_propagate(False)
        sidebar.grid_rowconfigure(1, weight=1)

        # En-tête premium de la sidebar
        sidebar_header = ctk.CTkFrame(sidebar, fg_color="transparent")
        sidebar_header.pack(fill="x", pady=(PADDING_SMALL, MARGIN_SMALL), padx=PADDING_SMALL)
        
        # Header avec icône et titre stylé
        header_content = ctk.CTkFrame(sidebar_header, fg_color="transparent")
        header_content.pack(fill="x")
        
        # Icône avec fond accent
        icon_container = ctk.CTkFrame(header_content, fg_color=TEXT_ACCENT, corner_radius=12, width=40, height=40)
        icon_container.pack_propagate(False)
        icon_container.pack(side="left")
        
        class_icon = get_icon("group", (20, 20))
        icon_label = ctk.CTkLabel(icon_container, text="", image=class_icon, text_color=BG_SIDEBAR)
        icon_label.pack(expand=True)
        
        # Titre avec style premium
        title_frame = ctk.CTkFrame(header_content, fg_color="transparent")
        title_frame.pack(side="left", fill="x", expand=True, padx=(PADDING_SMALL, 0))
        
        ctk.CTkLabel(title_frame, text="Classes", 
                     font=FONT_SUBTITLE, text_color=TEXT_ACCENT).pack(anchor="w")
        
        ctk.CTkLabel(title_frame, text="Sélectionnez une classe", 
                     font=FONT_SMALL, text_color=TEXT_SECONDARY).pack(anchor="w", pady=(MARGIN_SMALL, 0))
        
        # Séparateur élégant avec gradient
        separator_container = ctk.CTkFrame(sidebar, fg_color="transparent")
        separator_container.pack(fill="x", padx=PADDING_SMALL, pady=(0, MARGIN_SMALL))
        
        separator = ctk.CTkFrame(separator_container, height=2, fg_color=TEXT_ACCENT, corner_radius=1)
        separator.pack(fill="x")

        # Conteneur des boutons de classe avec scroll élégant
        self.classe_btns_frame = ctk.CTkScrollableFrame(sidebar, fg_color="transparent")
        self.classe_btns_frame.pack(fill="both", expand=True, padx=PADDING_SMALL, pady=(0, PADDING_SMALL))
        self.classe_btns = []

    def _separator(self, parent, pad=(8, 6)):
        """Séparateur comme dans le dashboard principal"""
        sep = ctk.CTkFrame(parent, height=1, fg_color=BORDER_COLOR)
        sep.pack(fill="x", padx=pad[0], pady=(pad[1], pad[1]))
        return sep


    # Méthodes fonctionnelles
    def update_classes_sidebar(self):
        """Met à jour la sidebar des classes avec structure PRIMAIRE/COLLÈGE/LYCÉE"""
        for w in self.classe_btns_frame.winfo_children(): 
            w.destroy()
        self.classe_btns = []

        # Bouton "Tous les élèves" simplifié
        btn_tous = ctk.CTkButton(
            self.classe_btns_frame, text="Tous les élèves", 
            font=FONT_BUTTON,
            fg_color="transparent", text_color=TEXT_ACCENT, 
            hover_color=BG_CARD_HOVER,
            command=lambda: self.update_dashboard_for_classe(None),
            corner_radius=15, height=45,
            image=get_icon("group", (18, 18)),
            border_width=2,
            border_color=TEXT_ACCENT
        )
        btn_tous.pack(fill="x", pady=(0, 4))
        self.classe_btns.append((btn_tous, None))

        # Séparateur élégant
        separator_classes = ctk.CTkFrame(self.classe_btns_frame, height=2, fg_color=BORDER_COLOR, corner_radius=1)
        separator_classes.pack(fill="x", pady=MARGIN_SMALL)

        # Récupérer les classes depuis la base de données
        classes = get_all_classes()
        
        if not classes:
            no_classes_label = ctk.CTkLabel(
                self.classe_btns_frame, 
                text="Aucune classe trouvée", 
                text_color=TEXT_MUTED,
                font=FONT_SECONDARY
            )
            no_classes_label.pack(pady=PADDING_MEDIUM)
        else:
            # Organiser les classes par niveau
            classes_par_niveau = {}
            for nom, niveau in classes:
                if niveau not in classes_par_niveau:
                    classes_par_niveau[niveau] = []
                classes_par_niveau[niveau].append(nom)
            
            # Créer les sections dans l'ordre souhaité
            niveaux_order = ["PRIMAIRE", "COLLÈGE", "LYCÉE"]
            
            for niveau in niveaux_order:
                if niveau in classes_par_niveau:
                    # Titre de section
                    section_title = ctk.CTkLabel(
                        self.classe_btns_frame,
                        text=niveau,
                        font=FONT_BUTTON,
                        text_color=TEXT_ACCENT,
                        fg_color="transparent"
                    )
                    section_title.pack(anchor="w", pady=(PADDING_MEDIUM, MARGIN_SMALL), padx=PADDING_SMALL)
                    
                    # Boutons des classes de cette section
                    for nom in classes_par_niveau[niveau]:
                        btn = ctk.CTkButton(
                            self.classe_btns_frame, 
                            text=nom, 
                            font=FONT_SMALL,
                            fg_color=BG_CARD, 
                            text_color=TEXT_PRIMARY, 
                            hover_color=BG_CARD_HOVER,
                            command=lambda c=nom: self.update_dashboard_for_classe(c),
                            corner_radius=10, 
                            height=35,
                            image=get_icon("group", (14, 14)),
                            border_width=1,
                            border_color=BORDER_COLOR
                        )
                        btn.pack(fill="x", pady=4, padx=PADDING_SMALL)
                        self.classe_btns.append((btn, nom))
        
        self.update_btn_states(self.selected_classe)

    def update_btn_states(self, classe_id):
        """Met à jour l'état des boutons de classe avec design premium"""
        for btn, cid in self.classe_btns:
            if classe_id == cid:
                # Classe sélectionnée - style accent
                btn.configure(fg_color=TEXT_ACCENT, text_color=BG_SIDEBAR, hover_color=HOVER_PRIMARY,
                             border_color=TEXT_ACCENT, border_width=2)
            elif cid is None and classe_id is None:
                # "Tous les élèves" sélectionné - style accent
                btn.configure(fg_color=TEXT_ACCENT, text_color=BG_SIDEBAR, hover_color=HOVER_PRIMARY,
                             border_color=TEXT_ACCENT, border_width=2)
            else:
                # Classe non sélectionnée - style normal
                btn.configure(fg_color=BG_CARD, text_color=TEXT_PRIMARY, hover_color=BG_CARD_HOVER,
                             border_color=BORDER_COLOR, border_width=1)

    def update_dashboard_for_classe(self, classe_name):
        """Met à jour le dashboard pour une classe spécifique"""
        try:
            # Convertir le nom de classe en ID si nécessaire
            classe_id = None
            if classe_name is not None:
                classe_id = get_classe_id_by_name(classe_name)
                if classe_id is None:
                    print(f"⚠️ Classe '{classe_name}' introuvable")
                    return
            
            self.selected_classe = classe_name  # Garder le nom pour l'affichage
            self.selected_classe_id = classe_id  # Stocker l'ID pour les requêtes DB
            self.update_btn_states(classe_name)
            
            # Mise à jour des statistiques avec données de la classe
            self.refresh_stats_for_classe(classe_id)
            
            # Mise à jour du graphique
            graph_data = fetch_effectifs_par_classe()
            self.update_chart(graph_data)
            
            print(f"✅ Dashboard mis à jour pour la classe: {classe_name} (ID: {classe_id})")
        except Exception as e:
            print(f"⚠️ Erreur mise à jour dashboard: {e}")

    def update_chart(self, data):
        """Met à jour le graphique avec les données - Graphique en aires avec gradient amélioré"""
        # Détruire l'ancien canvas s'il existe pour mise à jour instantanée
        for widget in self.chart_container.winfo_children()[2:]:
            widget.destroy()

        cls_names = [x[0] for x in data]
        counts = [x[1] for x in data]

        if not cls_names or all(c == 0 for c in counts):
            ctk.CTkLabel(
                self.chart_container, 
                text="📊 Aucune donnée à afficher",
                font=("Segoe UI", 16, "bold"),
                text_color=TEXT_MUTED
            ).pack(pady=50)
            return

        # Filtrer les données non nulles
        filtered_data = [(name, count) for name, count in zip(cls_names, counts) if count > 0]
        if not filtered_data:
            ctk.CTkLabel(
                self.chart_container, 
                text="📊 Aucune donnée à afficher",
                font=("Segoe UI", 16, "bold"),
                text_color=TEXT_MUTED
            ).pack(pady=50)
            return

        chart_names = [x[0] for x in filtered_data]
        chart_counts = [x[1] for x in filtered_data]

        # Création du graphique en aires avec gradient (hauteur optimisée)
        fig = plt.Figure(figsize=(8, 3.8), dpi=100)
        ax = fig.add_subplot(111)
        
        # Créer le graphique en aires avec gradient
        x_pos = range(len(chart_names))
        
        # Graphique en aires avec gradient amélioré
        ax.fill_between(x_pos, chart_counts, alpha=0.4, color=ACCENT_BLUE, label='Effectifs')
        ax.plot(x_pos, chart_counts, color=ACCENT_BLUE, linewidth=3, marker='o', markersize=8, 
                markerfacecolor=WHITE, markeredgecolor=ACCENT_BLUE, markeredgewidth=3)
        
        # Ajouter des points de données avec des couleurs différentes et améliorées
        colors = [ACCENT_BLUE, SUCCESS_GREEN, WARNING_ORANGE, ERROR_RED, PRIMARY_BLUE, 
                 "#8b5cf6", "#06b6d4", "#84cc16", "#f59e0b", "#ef4444", "#10b981", "#3b82f6"]
        for i, (x, y) in enumerate(zip(x_pos, chart_counts)):
            if y > 0:
                ax.scatter(x, y, s=100, c=colors[i % len(colors)], alpha=0.9, 
                          edgecolors=WHITE, linewidth=3, zorder=5)
                # Ajouter les valeurs avec style amélioré
                ax.annotate(str(y), (x, y), textcoords="offset points", xytext=(0,12), 
                           ha='center', va='bottom', color=TEXT_PRIMARY, 
                           fontweight='bold', fontsize=9, 
                           bbox=dict(boxstyle="round,pad=0.2", facecolor=BG_CARD, 
                                   edgecolor=BORDER_COLOR, alpha=0.8))
        
        # Configuration des axes avec noms abrégés
        ax.set_xticks(x_pos)
        
        # Abréger les noms des classes pour le graphique (version ultra-courte)
        abbreviated_names = []
        for name in chart_names:
            if "Terminale" in name:
                # "Terminale Sciences Exactes" -> "TSE"
                if "Terminale Sciences Exactes" in name:
                    abbreviated_names.append("TSE")
                elif "Terminale Sciences Mathématiques" in name:
                    abbreviated_names.append("TSM")
                elif "Terminale Sciences Sociales" in name:
                    abbreviated_names.append("TSS")
                else:
                    abbreviated_names.append("T")
            elif "Année" in name:
                # Extraire juste le numéro : "1° Année" -> "1°"
                abbreviated_name = name.split("°")[0] + "°"
                abbreviated_names.append(abbreviated_name)
            elif "Sciences" in name:
                # Extraire le numéro et l'abréviation : "11° Sciences Exactes" -> "11°SE"
                if "Exactes" in name:
                    num = name.split("°")[0] + "°"
                    abbreviated_names.append(num + "SE")
                elif "Mathématiques" in name:
                    num = name.split("°")[0] + "°"
                    abbreviated_names.append(num + "SM")
                elif "Sociales" in name:
                    num = name.split("°")[0] + "°"
                    abbreviated_names.append(num + "SS")
                else:
                    abbreviated_names.append(name)
            else:
                abbreviated_names.append(name)
        
        ax.set_xticklabels(abbreviated_names, rotation=45, ha='right', color=TEXT_PRIMARY, fontsize=9)
        ax.set_ylabel("Nombre d'élèves", color=TEXT_PRIMARY, fontsize=11, fontweight='bold')
        ax.set_title("Répartition des Élèves par Classe", color=TEXT_PRIMARY, fontsize=13, fontweight='bold', pad=15)
        
        # Style des axes amélioré
        ax.tick_params(axis='y', colors=TEXT_PRIMARY, labelsize=10)
        ax.spines['bottom'].set_color(BORDER_COLOR)
        ax.spines['left'].set_color(BORDER_COLOR)
        ax.spines['right'].set_color(BG_CARD)
        ax.spines['top'].set_color(BG_CARD)
        
        # Grille subtile améliorée
        ax.grid(True, alpha=0.3, color=BORDER_COLOR, linestyle='-', linewidth=0.5)
        
        # Fond sombre
        fig.patch.set_facecolor(BG_CARD)
        ax.set_facecolor(BG_CARD)
        
        # Ajuster les marges pour éviter la coupure des labels
        fig.tight_layout()
        
        # Intégration dans CustomTkinter avec mise à jour instantanée
        canvas = FigureCanvasTkAgg(fig, self.chart_container)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True, padx=PADDING_SMALL, pady=PADDING_SMALL)

        # Stocker la référence du canvas pour mise à jour future
        self.chart_canvas = canvas


    def update_last_action(self, action_type, details=""):
        """Met à jour l'affichage de la dernière action"""
        from datetime import datetime
        self.last_action_time = datetime.now()
        self.last_action_type = action_type
        
        # Calculer le temps écoulé
        now = datetime.now()
        diff = now - self.last_action_time
        
        if diff.total_seconds() < 60:
            time_str = "à l'instant"
        elif diff.total_seconds() < 3600:
            minutes = int(diff.total_seconds() / 60)
            time_str = f"il y a {minutes} min"
        else:
            hours = int(diff.total_seconds() / 3600)
            time_str = f"il y a {hours}h"
        
        # Mettre à jour le label
        if hasattr(self, 'action_label'):
            self.action_label.configure(text=f"Dernière action : {action_type} - {time_str}")
    
    def export_to_pdf(self):
        """Exporte les données des élèves en PDF"""
        self.update_last_action("Export PDF", "Génération du PDF")
        messagebox.showinfo("Export PDF", "Fonctionnalité d'export PDF - À implémenter\n\nCette fonction exportera la liste des élèves de la classe sélectionnée au format PDF.")
    
    def export_to_excel(self):
        """Exporte les données des élèves en Excel"""
        self.update_last_action("Export Excel", "Génération du fichier Excel")
        messagebox.showinfo("Export Excel", "Fonctionnalité d'export Excel - À implémenter\n\nCette fonction exportera la liste des élèves de la classe sélectionnée au format Excel (.xlsx).")



    def _center_window(self, window):
        """Centre une fenêtre sur l'écran comme le login view"""
        window.update_idletasks()
        width = window.winfo_width()
        height = window.winfo_height()
        x = (window.winfo_screenwidth() // 2) - (width // 2)
        y = (window.winfo_screenheight() // 2) - (height // 2)
        window.geometry(f"{width}x{height}+{x}+{y}")

    def afficher_tous_eleves_classe(self):
        """Affiche tous les élèves de la classe sélectionnée avec le thème personnalisé"""
        self.update_last_action("Affichage", "Ouverture de la liste des élèves")
        if self.selected_classe is None:
            messagebox.showinfo("Information", "Veuillez d'abord sélectionner une classe dans la sidebar.")
            return
        
        # Récupérer tous les élèves de la classe sélectionnée en utilisant l'ID
        eleves_classe = get_eleves_list(self.selected_classe_id)
        
        if not eleves_classe:
            messagebox.showinfo("Information", f"Aucun élève trouvé dans la classe '{self.selected_classe}'.")
            return
        
        # Créer une fenêtre avec le thème personnalisé
        self.show_all_window = ctk.CTkToplevel(self)
        self.show_all_window.title(f"Gestion des élèves - {self.selected_classe}")
        self.show_all_window.geometry("700x500")
        self.show_all_window.configure(fg_color=BG_MAIN)  # Utilise le thème
        self.show_all_window.resizable(True, True)
        
        # Centrer la fenêtre
        self.show_all_window.transient(self)
        self.show_all_window.grab_set()
        self._center_window(self.show_all_window)
        
        # Créer l'interface avec le thème personnalisé
        self.create_themed_interface(eleves_classe)

    def create_themed_interface(self, eleves_classe):
        """Crée l'interface avec le thème personnalisé"""
        # Barre de menu moderne
        menubar = tk.Menu(self.show_all_window)
        self.show_all_window.config(menu=menubar)
        
        # Menu Fichier
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Fichier", menu=file_menu)
        file_menu.add_command(label="Nouvel élève", command=self.ajouter_eleve)
        file_menu.add_command(label="Importer", command=lambda: messagebox.showinfo("Info", "Fonctionnalité d'importation à venir"))
        file_menu.add_command(label="Exporter", command=lambda: messagebox.showinfo("Info", "Fonctionnalité d'exportation à venir"))
        file_menu.add_separator()
        file_menu.add_command(label="Fermer", command=self.show_all_window.destroy)
        
        # Menu Édition
        edit_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Édition", menu=edit_menu)
        edit_menu.add_command(label="Modifier élève", command=self.modifier_eleve)
        edit_menu.add_command(label="Supprimer élève", command=self.supprimer_eleve)
        edit_menu.add_separator()
        edit_menu.add_command(label="Actualiser", command=lambda: self.refresh_dashboard())
        
        # Menu Aide
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Aide", menu=help_menu)
        help_menu.add_command(label="À propos", command=lambda: messagebox.showinfo("À propos", "Gestion des élèves - EduManager+"))
        help_menu.add_command(label="Guide d'utilisation", command=lambda: messagebox.showinfo("Guide", "Guide d'utilisation à venir"))
        
        # En-tête moderne avec le thème neon
        header_frame = ctk.CTkFrame(self.show_all_window, fg_color=CARD_BG, corner_radius=0, border_width=2, border_color=ACCENT)
        header_frame.pack(fill="x", padx=0, pady=0)
        
        # Titre principal avec icône
        title_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        title_frame.pack(fill="x", padx=20, pady=15)
        
        # Icône et titre
        title_inner = ctk.CTkFrame(title_frame, fg_color="transparent")
        title_inner.pack(side="left")
        
        # Charger l'icône élève depuis les ressources
        try:
            eleve_icon = ctk.CTkImage(light_image=Image.open("resources/icons/eleve.png"), size=(32, 32))
            icon_label = ctk.CTkLabel(title_inner, image=eleve_icon, text="")
            icon_label.pack(side="left", padx=(0, 10))
        except:
            # Fallback si l'icône n'est pas trouvée
            icon_label = ctk.CTkLabel(title_inner, text="👨‍🎓", font=("Segoe UI", 24), text_color=ACCENT)
            icon_label.pack(side="left", padx=(0, 10))
        
        title_label = ctk.CTkLabel(title_inner, text="Gestion des élèves", 
                                 font=("Segoe UI", 32, "bold"), text_color=ACCENT)
        title_label.pack(side="left")
        
        # Informations sur la classe
        info_frame = ctk.CTkFrame(header_frame, fg_color=BG_SIDEBAR, corner_radius=8, border_width=2, border_color=ACCENT)
        info_frame.pack(fill="x", padx=20, pady=(0, 15))
        
        info_text = f"Classe {self.selected_classe} - {len(eleves_classe)} élève(s)"
        info_label = ctk.CTkLabel(info_frame, text=info_text, 
                                font=("Segoe UI", 16, "bold"), text_color=ACCENT)
        info_label.pack(pady=10)
        
        # Zone principale avec recherche et boutons
        main_frame = ctk.CTkFrame(self.show_all_window, fg_color=BG_MAIN)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Barre d'actions (recherche + boutons)
        actions_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        actions_frame.pack(fill="x", pady=(0, 20))
        
        # Zone de recherche (à gauche) avec style neon
        search_frame = ctk.CTkFrame(actions_frame, fg_color=BG_SIDEBAR, corner_radius=12, border_width=3, border_color=ACCENT)
        search_frame.pack(side="left", fill="x", expand=True, padx=(0, 10))
        
        search_inner = ctk.CTkFrame(search_frame, fg_color="transparent")
        search_inner.pack(fill="x", padx=15, pady=10)
        
        # Icône de recherche
        try:
            search_icon = ctk.CTkImage(light_image=Image.open("resources/icons/search.png"), size=(16, 16))
            search_icon_label = ctk.CTkLabel(search_inner, image=search_icon, text="")
            search_icon_label.pack(side="left", padx=(0, 8))
        except:
            search_icon_label = ctk.CTkLabel(search_inner, text="🔍", font=("Segoe UI", 14, "bold"), text_color=ACCENT)
            search_icon_label.pack(side="left", padx=(0, 8))
        
        # Champ de recherche avec style neon
        self.search_entry = ctk.CTkEntry(search_inner, placeholder_text="Rechercher un élève par nom, prénom ou statut...",
                                       fg_color=BG_SIDEBAR, text_color=ACCENT, border_color=ACCENT,
                                       font=("Segoe UI", 12, "bold"), height=35, border_width=2)
        self.search_entry.pack(side="left", fill="x", expand=True)
        self.search_entry.bind("<KeyRelease>", self.filter_eleves)
        
        # Boutons d'action (à droite)
        buttons_frame = ctk.CTkFrame(actions_frame, fg_color="transparent")
        buttons_frame.pack(side="right")
        
        # Bouton Ajouter avec style neon
        try:
            add_icon = ctk.CTkImage(light_image=Image.open("resources/icons/add.png"), size=(20, 20))
            btn_add = ctk.CTkButton(buttons_frame, text="Ajouter", image=add_icon, command=self.ajouter_eleve,
                                  fg_color="transparent", hover_color=ACCENT, text_color=ACCENT,
                                  corner_radius=12, height=45, width=120, font=("Segoe UI", 13, "bold"), border_width=3, border_color=ACCENT)
        except:
            btn_add = ctk.CTkButton(buttons_frame, text="Ajouter", command=self.ajouter_eleve,
                                  fg_color="transparent", hover_color=ACCENT, text_color=ACCENT,
                                  corner_radius=12, height=45, width=120, font=("Segoe UI", 13, "bold"), border_width=3, border_color=ACCENT)
        btn_add.pack(side="left", padx=(0, 8))
        
        # Bouton Actualiser avec style neon
        try:
            refresh_icon = ctk.CTkImage(light_image=Image.open("resources/icons/refresh.png"), size=(20, 20))
            btn_refresh = ctk.CTkButton(buttons_frame, text="Actualiser", image=refresh_icon, command=lambda: self.refresh_dashboard(),
                                      fg_color="transparent", hover_color=ACCENT, text_color=ACCENT,
                                      corner_radius=12, height=45, width=120, font=("Segoe UI", 13, "bold"), border_width=3, border_color=ACCENT)
        except:
            btn_refresh = ctk.CTkButton(buttons_frame, text="Actualiser", command=lambda: self.refresh_dashboard(),
                                      fg_color="transparent", hover_color=ACCENT, text_color=ACCENT,
                                      corner_radius=12, height=45, width=120, font=("Segoe UI", 13, "bold"), border_width=3, border_color=ACCENT)
        btn_refresh.pack(side="left", padx=(0, 8))
        
        # Bouton Modifier avec style neon
        try:
            edit_icon = ctk.CTkImage(light_image=Image.open("resources/icons/edit.png"), size=(20, 20))
            btn_edit = ctk.CTkButton(buttons_frame, text="Modifier", image=edit_icon, command=self.modifier_eleve,
                                   fg_color="transparent", hover_color=ACCENT, text_color=ACCENT,
                                   corner_radius=12, height=45, width=120, font=("Segoe UI", 13, "bold"), border_width=3, border_color=ACCENT)
        except:
            btn_edit = ctk.CTkButton(buttons_frame, text="Modifier", command=self.modifier_eleve,
                                   fg_color="transparent", hover_color=ACCENT, text_color=ACCENT,
                                   corner_radius=12, height=45, width=120, font=("Segoe UI", 13, "bold"), border_width=3, border_color=ACCENT)
        btn_edit.pack(side="left", padx=(0, 8))
        
        # Bouton Supprimer avec style neon
        try:
            delete_icon = ctk.CTkImage(light_image=Image.open("resources/icons/delete.png"), size=(20, 20))
            btn_delete = ctk.CTkButton(buttons_frame, text="Supprimer", image=delete_icon, command=self.supprimer_eleve,
                                     fg_color="transparent", hover_color=ACCENT, text_color=ACCENT,
                                     corner_radius=12, height=45, width=120, font=("Segoe UI", 13, "bold"), border_width=3, border_color=ACCENT)
        except:
            btn_delete = ctk.CTkButton(buttons_frame, text="Supprimer", command=self.supprimer_eleve,
                                     fg_color="transparent", hover_color=ACCENT, text_color=ACCENT,
                                     corner_radius=12, height=45, width=120, font=("Segoe UI", 13, "bold"), border_width=3, border_color=ACCENT)
        btn_delete.pack(side="left")
        
        # Message contextuel
        self.context_message = ctk.CTkLabel(main_frame, text="Sélectionnez un élève pour modifier ou supprimer",
                                          font=("Segoe UI", 12, "bold"), text_color=ACCENT)
        self.context_message.pack(pady=(0, 10))
        
        # Conteneur du tableau avec le thème
        table_container = ctk.CTkFrame(main_frame, fg_color=CARD_BG, corner_radius=12, border_width=3, border_color=ACCENT)
        table_container.pack(fill="both", expand=True)
        
        # Configuration du style Treeview avec le thème
        style = ttk.Style()
        style.theme_use('clam')
        
        # Style des en-têtes avec bordures uniquement (pas de fond coloré)
        style.configure("Treeview.Heading", 
                       background="transparent", 
                       foreground=ACCENT, 
                       font=("Segoe UI", 14, "bold"), 
                       padding=(20, 15),
                       borderwidth=2,
                       relief="solid")
        
        # Style des lignes avec le thème
        style.configure("Treeview", 
                       background=CARD_BG, 
                       foreground=ACCENT, 
                       font=("Segoe UI", 12, "bold"), 
                       rowheight=50,
                       borderwidth=0,
                       fieldbackground=CARD_BG)
        
        # Créer le tableau avec le thème
        columns = ("Nom", "Prénom", "Genre", "Naissance", "Âge", "Statut")
        self.table = ttk.Treeview(table_container, columns=columns, show="headings", style="Treeview")
        
        # Configuration des colonnes
        column_widths = {"Nom": 150, "Prénom": 150, "Genre": 80, "Naissance": 120, "Âge": 60, "Statut": 100}
        for col in columns:
            self.table.heading(col, text=col)
            self.table.column(col, width=column_widths[col], anchor="center")
        
        # Barre de défilement avec le thème
        scrollbar = ctk.CTkScrollbar(table_container, orientation="vertical", command=self.table.yview,
                                   fg_color=ACCENT, button_color=CARD_BG, button_hover_color=ACCENT)
        self.table.configure(yscrollcommand=scrollbar.set)
        
        # Pack du tableau et de la barre de défilement
        self.table.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        scrollbar.pack(side="right", fill="y", padx=(0, 10), pady=10)
        
        # Stocker les données des élèves
        self.eleves_data = eleves_classe
        
        # Remplir le tableau avec les données
        self.populate_table_with_theme()
        
        # Bind des événements
        self.table.bind("<<TreeviewSelect>>", self.on_table_select)
        
        # Focus sur le tableau
        self.table.focus_set()
        
        # Message de fermeture
        self.show_all_window.protocol("WM_DELETE_WINDOW", self.on_close_show_all)

    def populate_table_with_theme(self):
        """Remplit le tableau avec les données en utilisant le thème"""
        # Ajouter les données avec lignes alternées et indicateurs de statut
        
        # Informations de la classe avec style moderne
        info_frame = ctk.CTkFrame(title_frame, fg_color="#34495E", corner_radius=8)
        info_frame.pack(fill="x", pady=(0, 15))
        
        info_label = ctk.CTkLabel(
            info_frame,
            text=f"Classe {self.selected_classe} - {len(eleves_classe)} élève(s)",
            font=("Segoe UI", 16),
            text_color="white"
        )
        info_label.pack(padx=20, pady=15)
        
        # Barre d'actions et recherche moderne
        actions_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        actions_frame.pack(fill="x", padx=30, pady=(0, 25))
        
        # Barre de recherche moderne (à gauche)
        search_frame = ctk.CTkFrame(actions_frame, fg_color="white", corner_radius=10, border_width=1, border_color="#BDC3C7")
        search_frame.pack(side="left", fill="x", expand=True, padx=(0, 20))
        
        # Conteneur interne pour l'icône et le champ
        search_inner = ctk.CTkFrame(search_frame, fg_color="transparent")
        search_inner.pack(fill="x", padx=15, pady=12)
        
        # Icône de recherche
        search_icon = get_icon("search", (18, 18))
        if search_icon:
            icon_label = ctk.CTkLabel(search_inner, text="", image=search_icon, text_color="#7F8C8D")
            icon_label.pack(side="left", padx=(0, 10))
            icon_label._imgref = search_icon
        
        # Champ de recherche moderne
        self.search_modal_var = ctk.StringVar()
        search_entry = ctk.CTkEntry(
            search_inner,
            placeholder_text="Rechercher un élève par nom, prénom ou statut...",
            textvariable=self.search_modal_var,
            fg_color="white",
            text_color="#2C3E50",
            border_color="#BDC3C7",
            corner_radius=0,
            height=28,
            font=("Segoe UI", 13),
            placeholder_text_color="#95A5A6"
        )
        search_entry.pack(side="left", fill="x", expand=True)
        
        # Boutons d'action modernes (à droite)
        buttons_frame = ctk.CTkFrame(actions_frame, fg_color="transparent")
        buttons_frame.pack(side="right")
        
        # Bouton Ajouter élève avec style moderne
        add_icon = get_icon("add", (18, 18))
        btn_add = ctk.CTkButton(
            buttons_frame,
            text="Ajouter",
            image=add_icon,
            fg_color="#27AE60",
            text_color="white",
            hover_color="#229954",
            command=self.ajouter_eleve,
            corner_radius=8,
            height=45,
            width=120,
            font=("Segoe UI", 12, "bold"),
            border_width=0
        )
        if add_icon:
            btn_add._imgref = add_icon
        btn_add.pack(side="left", padx=(0, 10))
        
        # Bouton Modifier avec style moderne
        edit_icon = get_icon("edit", (18, 18))
        btn_modifier = ctk.CTkButton(
            buttons_frame,
            text="Modifier",
            image=edit_icon,
            fg_color="#3498DB",
            text_color="white",
            hover_color="#2980B9",
            command=self.modifier_eleve,
            corner_radius=8,
            height=45,
            width=120,
            font=("Segoe UI", 12, "bold"),
            border_width=0
        )
        if edit_icon:
            btn_modifier._imgref = edit_icon
        btn_modifier.pack(side="left", padx=(0, 10))
        
        # Bouton Supprimer avec style moderne
        delete_icon = get_icon("delete", (18, 18))
        btn_supprimer = ctk.CTkButton(
            buttons_frame,
            text="Supprimer",
            image=delete_icon,
            fg_color="#E74C3C",
            text_color="white",
            hover_color="#C0392B",
            command=self.supprimer_eleve,
            corner_radius=8,
            height=45,
            width=120,
            font=("Segoe UI", 12, "bold"),
            border_width=0
        )
        if delete_icon:
            btn_supprimer._imgref = delete_icon
        btn_supprimer.pack(side="left", padx=(0, 10))
        
        # Bouton Actualiser avec style moderne
        refresh_icon = get_icon("refresh", (18, 18))
        btn_refresh = ctk.CTkButton(
            buttons_frame,
            text="Actualiser",
            image=refresh_icon,
            fg_color="#95A5A6",
            text_color="white",
            hover_color="#7F8C8D",
            command=self.refresh_dashboard,
            corner_radius=8,
            height=45,
            width=120,
            font=("Segoe UI", 12, "bold"),
            border_width=0
        )
        if refresh_icon:
            btn_refresh._imgref = refresh_icon
        btn_refresh.pack(side="left")
        
        # Conteneur principal pour le tableau moderne
        main_container = ctk.CTkFrame(self.show_all_window, fg_color="#ECF0F1", corner_radius=0)
        main_container.pack(fill="both", expand=True, padx=0, pady=0)
        
        # Tableau moderne avec design professionnel
        table_container = ctk.CTkFrame(
            main_container, 
            fg_color="white", 
            corner_radius=0,
            border_width=0
        )
        table_container.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Configuration du tableau moderne
        columns = ("Nom", "Prénom", "Genre", "Naissance", "Âge", "Statut")
        table = ttk.Treeview(table_container, columns=columns, show="headings", height=15)
        
        # Style moderne et professionnel pour le tableau
        style = ttk.Style()
        style.configure("Treeview", 
                        background="white",
                        foreground="#2C3E50",
                        fieldbackground="white",
                       borderwidth=0,
                        font=("Segoe UI", 12),
                        rowheight=50)
        style.configure("Treeview.Heading",
                        background="#34495E",  # Fond sombre pour les en-têtes
                        foreground="white",     # Texte blanc pour le contraste
                        font=("Segoe UI", 14, "bold"),
                       borderwidth=0,
                        padding=(25, 20))
        
        # Effet de survol pour les en-têtes
        style.map("Treeview.Heading",
                  background=[('active', "#2C3E50")])  # Fond plus sombre au survol
        
        # Configuration des colonnes optimisées
        column_widths = {
            "Nom": 200, "Prénom": 200, "Genre": 120, 
            "Naissance": 150, "Âge": 100, "Statut": 150
        }
        
        column_anchors = {
            "Nom": "w", "Prénom": "w", "Genre": "center",
            "Naissance": "center", "Âge": "center", "Statut": "center"
        }
        
        for col in columns:
            table.heading(col, text=col)
            table.column(col, width=column_widths[col], anchor=column_anchors[col])
        
        # Scrollbar moderne
        scrollbar = ctk.CTkScrollbar(
            table_container,
            orientation="vertical",
            command=table.yview,
            fg_color="#BDC3C7",
            button_color="#34495E",
            button_hover_color="#2C3E50",
            corner_radius=8
        )
        table.configure(yscrollcommand=scrollbar.set)
        
        # Pack du tableau et scrollbar
        table.pack(side="left", fill="both", expand=True, padx=20, pady=20)
        scrollbar.pack(side="right", fill="y", padx=(0, 20), pady=20)
        
        # Stocker les données des élèves pour les boutons
        self.eleves_data = eleves_classe
        
        # Ajouter les données avec lignes alternées et indicateurs de statut
        for i, eleve in enumerate(eleves_classe):
            _id, nom, prenom, genre, naissance, statut, cid = eleve
            age = compute_age(naissance)
            
            # Insérer la ligne avec les données
            values = (nom, prenom, genre or "—", naissance or "—", age, statut or "—")
            item = table.insert("", "end", values=values)
            
            # Lignes alternées avec couleurs distinctes
            if i % 2 == 0:
                table.tag_configure("even", background="#F8F9FA")  # Blanc cassé
                table.item(item, tags=("even",))
            else:
                table.tag_configure("odd", background="#E9ECEF")   # Gris très clair
                table.item(item, tags=("odd",))
            
            # Indicateurs visuels pour le statut
            if statut == "Actif":
                table.tag_configure("actif", foreground="#27AE60")  # Vert pour actif
                table.item(item, tags=(table.item(item, "tags")[0], "actif"))
            elif statut == "Inactif":
                table.tag_configure("inactif", foreground="#E74C3C")  # Rouge pour inactif
                table.item(item, tags=(table.item(item, "tags")[0], "inactif"))
        
        # Sélectionner la première ligne par défaut
        if eleves_classe:
            first_item = table.get_children()[0]
            table.selection_set(first_item)
            table.focus(first_item)

    def create_themed_interface(self, eleves_classe):
        """Crée l'interface avec le thème personnalisé"""
        # Barre de menu moderne
        menubar = tk.Menu(self.show_all_window)
        self.show_all_window.config(menu=menubar)
        
        # Menu Fichier
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Fichier", menu=file_menu)
        file_menu.add_command(label="Nouvel élève", command=self.ajouter_eleve)
        file_menu.add_command(label="Importer", command=lambda: messagebox.showinfo("Info", "Fonctionnalité d'importation à venir"))
        file_menu.add_command(label="Exporter", command=lambda: messagebox.showinfo("Info", "Fonctionnalité d'exportation à venir"))
        file_menu.add_separator()
        file_menu.add_command(label="Fermer", command=self.show_all_window.destroy)
        
        # Menu Édition
        edit_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Édition", menu=edit_menu)
        edit_menu.add_command(label="Modifier élève", command=self.modifier_eleve)
        edit_menu.add_command(label="Supprimer élève", command=self.supprimer_eleve)
        edit_menu.add_separator()
        edit_menu.add_command(label="Actualiser", command=lambda: self.refresh_dashboard())
        
        # Menu Aide
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Aide", menu=help_menu)
        help_menu.add_command(label="À propos", command=lambda: messagebox.showinfo("À propos", "Gestion des élèves - EduManager+"))
        help_menu.add_command(label="Guide d'utilisation", command=lambda: messagebox.showinfo("Guide", "Guide d'utilisation à venir"))
        
        # En-tête moderne avec le thème
        header_frame = ctk.CTkFrame(self.show_all_window, fg_color="#2C3E50", corner_radius=0)
        header_frame.pack(fill="x", padx=0, pady=0)
        
        # Titre principal avec icône
        title_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        title_frame.pack(fill="x", padx=20, pady=15)
        
        # Icône et titre
        title_inner = ctk.CTkFrame(title_frame, fg_color="transparent")
        title_inner.pack(side="left")
        
        # Charger l'icône élève depuis les ressources
        try:
            eleve_icon = ctk.CTkImage(light_image=Image.open("resources/icons/eleve.png"), size=(32, 32))
            icon_label = ctk.CTkLabel(title_inner, image=eleve_icon, text="")
            icon_label.pack(side="left", padx=(0, 10))
        except:
            # Fallback si l'icône n'est pas trouvée
            icon_label = ctk.CTkLabel(title_inner, text="👨‍🎓", font=("Segoe UI", 24))
            icon_label.pack(side="left", padx=(0, 10))
        
        title_label = ctk.CTkLabel(title_inner, text="Gestion des élèves", 
                                 font=("Segoe UI", 32, "bold"), text_color="white")
        title_label.pack(side="left")
        
        # Informations sur la classe
        info_frame = ctk.CTkFrame(header_frame, fg_color="#34495E", corner_radius=8)
        info_frame.pack(fill="x", padx=20, pady=(0, 15))
        
        info_text = f"Classe {self.selected_classe} - {len(eleves_classe)} élève(s)"
        info_label = ctk.CTkLabel(info_frame, text=info_text, 
                                font=("Segoe UI", 16), text_color="white")
        info_label.pack(pady=10)
        
        # Zone principale avec recherche et boutons
        main_frame = ctk.CTkFrame(self.show_all_window, fg_color=BG_MAIN)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Barre d'actions (recherche + boutons)
        actions_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        actions_frame.pack(fill="x", pady=(0, 20))
        
        # Zone de recherche (à gauche)
        search_frame = ctk.CTkFrame(actions_frame, fg_color="white", corner_radius=8, border_width=1, border_color="#BDC3C7")
        search_frame.pack(side="left", fill="x", expand=True, padx=(0, 10))
        
        search_inner = ctk.CTkFrame(search_frame, fg_color="transparent")
        search_inner.pack(fill="x", padx=15, pady=10)
        
        # Icône de recherche
        try:
            search_icon = ctk.CTkImage(light_image=Image.open("resources/icons/search.png"), size=(16, 16))
            search_icon_label = ctk.CTkLabel(search_inner, image=search_icon, text="")
            search_icon_label.pack(side="left", padx=(0, 8))
        except:
            search_icon_label = ctk.CTkLabel(search_inner, text="🔍", font=("Segoe UI", 14))
            search_icon_label.pack(side="left", padx=(0, 8))
        
        # Champ de recherche
        self.search_entry = ctk.CTkEntry(search_inner, placeholder_text="Rechercher un élève par nom, prénom ou statut...",
                                       fg_color="white", text_color="#2C3E50", border_color="#BDC3C7",
                                       font=("Segoe UI", 12), height=35)
        self.search_entry.pack(side="left", fill="x", expand=True)
        self.search_entry.bind("<KeyRelease>", self.filter_eleves)
        
        # Boutons d'action (à droite)
        buttons_frame = ctk.CTkFrame(actions_frame, fg_color="transparent")
        buttons_frame.pack(side="right")
        
        # Bouton Ajouter
        try:
            add_icon = ctk.CTkImage(light_image=Image.open("resources/icons/add.png"), size=(20, 20))
            btn_add = ctk.CTkButton(buttons_frame, text="Ajouter", image=add_icon, command=self.ajouter_eleve,
                                  fg_color="#27AE60", hover_color="#229954", text_color="white",
                                  corner_radius=8, height=45, width=120, font=("Segoe UI", 13, "bold"), border_width=0)
        except:
            btn_add = ctk.CTkButton(buttons_frame, text="Ajouter", command=self.ajouter_eleve,
                                  fg_color="#27AE60", hover_color="#229954", text_color="white",
                                  corner_radius=8, height=45, width=120, font=("Segoe UI", 13, "bold"), border_width=0)
        btn_add.pack(side="left", padx=(0, 8))
        
        # Bouton Actualiser
        try:
            refresh_icon = ctk.CTkImage(light_image=Image.open("resources/icons/refresh.png"), size=(20, 20))
            btn_refresh = ctk.CTkButton(buttons_frame, text="Actualiser", image=refresh_icon, command=lambda: self.refresh_dashboard(),
                                      fg_color="#95A5A6", hover_color="#7F8C8D", text_color="white",
                                      corner_radius=8, height=45, width=120, font=("Segoe UI", 13, "bold"), border_width=0)
        except:
            btn_refresh = ctk.CTkButton(buttons_frame, text="Actualiser", command=lambda: self.refresh_dashboard(),
                                      fg_color="#95A5A6", hover_color="#7F8C8D", text_color="white",
                                      corner_radius=8, height=45, width=120, font=("Segoe UI", 13, "bold"), border_width=0)
        btn_refresh.pack(side="left", padx=(0, 8))
        
        # Bouton Modifier
        try:
            edit_icon = ctk.CTkImage(light_image=Image.open("resources/icons/edit.png"), size=(20, 20))
            btn_edit = ctk.CTkButton(buttons_frame, text="Modifier", image=edit_icon, command=self.modifier_eleve,
                                   fg_color="#3498DB", hover_color="#2980B9", text_color="white",
                                   corner_radius=8, height=45, width=120, font=("Segoe UI", 13, "bold"), border_width=0)
        except:
            btn_edit = ctk.CTkButton(buttons_frame, text="Modifier", command=self.modifier_eleve,
                                   fg_color="#3498DB", hover_color="#2980B9", text_color="white",
                                   corner_radius=8, height=45, width=120, font=("Segoe UI", 13, "bold"), border_width=0)
        btn_edit.pack(side="left", padx=(0, 8))
        
        # Bouton Supprimer
        try:
            delete_icon = ctk.CTkImage(light_image=Image.open("resources/icons/delete.png"), size=(20, 20))
            btn_delete = ctk.CTkButton(buttons_frame, text="Supprimer", image=delete_icon, command=self.supprimer_eleve,
                                     fg_color="#E74C3C", hover_color="#C0392B", text_color="white",
                                     corner_radius=8, height=45, width=120, font=("Segoe UI", 13, "bold"), border_width=0)
        except:
            btn_delete = ctk.CTkButton(buttons_frame, text="Supprimer", command=self.supprimer_eleve,
                                     fg_color="#E74C3C", hover_color="#C0392B", text_color="white",
                                     corner_radius=8, height=45, width=120, font=("Segoe UI", 13, "bold"), border_width=0)
        btn_delete.pack(side="left")
        
        # Message contextuel
        self.context_message = ctk.CTkLabel(main_frame, text="Sélectionnez un élève pour modifier ou supprimer",
                                          font=("Segoe UI", 12, "bold"), text_color=ACCENT)
        self.context_message.pack(pady=(0, 10))
        
        # Conteneur du tableau avec le thème
        table_container = ctk.CTkFrame(main_frame, fg_color=CARD_BG, corner_radius=12, border_width=3, border_color=ACCENT)
        table_container.pack(fill="both", expand=True)
        
        # Configuration du style Treeview avec le thème
        style = ttk.Style()
        style.theme_use('clam')
        
        # Style des en-têtes avec bordures uniquement (pas de fond coloré)
        style.configure("Treeview.Heading", 
                       background="transparent", 
                       foreground=ACCENT, 
                       font=("Segoe UI", 14, "bold"), 
                       padding=(20, 15),
                       borderwidth=2,
                       relief="solid")
        
        # Style des lignes avec le thème
        style.configure("Treeview", 
                       background=CARD_BG, 
                       foreground=ACCENT, 
                       font=("Segoe UI", 12, "bold"), 
                       rowheight=50,
                       borderwidth=0,
                       fieldbackground=CARD_BG)
        
        # Créer le tableau avec le thème
        columns = ("Nom", "Prénom", "Genre", "Naissance", "Âge", "Statut")
        self.table = ttk.Treeview(table_container, columns=columns, show="headings", style="Treeview")
        
        # Configuration des colonnes
        column_widths = {"Nom": 150, "Prénom": 150, "Genre": 80, "Naissance": 120, "Âge": 60, "Statut": 100}
        for col in columns:
            self.table.heading(col, text=col)
            self.table.column(col, width=column_widths[col], anchor="center")
        
        # Barre de défilement avec le thème
        scrollbar = ctk.CTkScrollbar(table_container, orientation="vertical", command=self.table.yview,
                                   fg_color="#BDC3C7", button_color="#34495E", button_hover_color="#2C3E50")
        self.table.configure(yscrollcommand=scrollbar.set)
        
        # Pack du tableau et de la barre de défilement
        self.table.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        scrollbar.pack(side="right", fill="y", padx=(0, 10), pady=10)
        
        # Stocker les données des élèves
        self.eleves_data = eleves_classe
        
        # Remplir le tableau avec les données
        self.populate_table_with_theme()
        
        # Bind des événements
        self.table.bind("<<TreeviewSelect>>", self.on_table_select)
        
        # Focus sur le tableau
        self.table.focus_set()
        
        # Message de fermeture
        self.show_all_window.protocol("WM_DELETE_WINDOW", self.on_close_show_all)

    def populate_table_with_theme(self):
        """Remplit le tableau avec les données en utilisant le thème neon"""
        # Ajouter les données avec lignes alternées et indicateurs de statut
        for i, eleve in enumerate(self.eleves_data):
            _id, nom, prenom, genre, naissance, statut, cid = eleve
            age = compute_age(naissance)
            
            # Insérer la ligne avec les données
            values = (nom, prenom, genre or "—", naissance or "—", age, statut or "—")
            item = self.table.insert("", "end", values=values)
            
            # Lignes alternées avec couleurs neon du thème
            if i % 2 == 0:
                self.table.tag_configure("even", background=CARD_BG, foreground=ACCENT)  # Fond sombre avec texte neon
                self.table.item(item, tags=("even",))
            else:
                self.table.tag_configure("odd", background=BG_SIDEBAR, foreground=ACCENT)   # Fond plus sombre avec texte neon
                self.table.item(item, tags=("odd",))
            
            # Indicateurs visuels pour le statut avec couleurs neon
            if statut == "Actif":
                self.table.tag_configure("actif", foreground=SUCCESS_GREEN)  # Vert neon pour actif
                self.table.item(item, tags=(self.table.item(item, "tags")[0], "actif"))
            elif statut == "Inactif":
                self.table.tag_configure("inactif", foreground=ERROR_RED)  # Rouge neon pour inactif
                self.table.item(item, tags=(self.table.item(item, "tags")[0], "inactif"))
        
        # Sélectionner la première ligne par défaut
        if self.eleves_data:
            first_item = self.table.get_children()[0]
            self.table.selection_set(first_item)
            self.table.focus(first_item)

    def on_table_select(self, event):
        """Gère la sélection dans le tableau"""
        selected_items = self.table.selection()
        if selected_items:
            self.context_message.configure(text="Élève sélectionné - Vous pouvez maintenant modifier ou supprimer")
        else:
            self.context_message.configure(text="Sélectionnez un élève pour modifier ou supprimer")

    def filter_eleves(self, event):
        """Filtre les élèves selon le texte de recherche avec couleurs neon"""
        search_text = self.search_entry.get().lower()
        
        # Effacer le tableau
        for item in self.table.get_children():
            self.table.delete(item)
        
        # Réinsérer les éléments filtrés avec couleurs neon
        for i, eleve in enumerate(self.eleves_data):
            _id, nom, prenom, genre, naissance, statut, cid = eleve
            
            # Vérifier si l'élève correspond au critère de recherche
            if (search_text in nom.lower() or 
                search_text in prenom.lower() or 
                search_text in (statut or "").lower()):
                
                age = compute_age(naissance)
                values = (nom, prenom, genre or "—", naissance or "—", age, statut or "—")
                item = self.table.insert("", "end", values=values)
                
                # Appliquer les tags de couleur neon
                if i % 2 == 0:
                    self.table.tag_configure("even", background=CARD_BG, foreground=ACCENT)
                    self.table.item(item, tags=("even",))
                else:
                    self.table.tag_configure("odd", background=BG_SIDEBAR, foreground=ACCENT)
                    self.table.item(item, tags=("odd",))
                
                if statut == "Actif":
                    self.table.tag_configure("actif", foreground=SUCCESS_GREEN)
                    self.table.item(item, tags=(self.table.item(item, "tags")[0], "actif"))
                elif statut == "Inactif":
                    self.table.tag_configure("inactif", foreground=ERROR_RED)
                    self.table.item(item, tags=(self.table.item(item, "tags")[0], "inactif"))

    def on_close_show_all(self):
        """Gère la fermeture de la fenêtre de liste des élèves"""
        self.show_all_window.destroy()
        self.show_all_window = None

    def ajouter_eleve(self):
        """Ouvre le formulaire d'ajout d'élève"""
        self.update_last_action("Ajout", "Ouverture du formulaire d'ajout")
        self.formulaire_eleve(mode="Ajouter")

    def modifier_eleve(self):
        """Modifie l'élève sélectionné dans le tableau"""
        try:
            # Obtenir l'élève sélectionné depuis le tableau
            selected_eleve = self.get_selected_eleve_from_table()
            if selected_eleve:
                self.update_last_action("Modification", f"Modification de {selected_eleve[1]} {selected_eleve[2]}")
                self.formulaire_eleve(mode="Modifier", eleve={
                    'id': selected_eleve[0],
                    'nom': selected_eleve[1],
                    'prenom': selected_eleve[2],
                    'genre': selected_eleve[3],
                    'date_naissance': selected_eleve[4],
                    'statut': selected_eleve[5],
                    'classe_id': selected_eleve[6]
                })
            else:
                messagebox.showwarning("Aucune sélection", "Veuillez sélectionner un élève dans le tableau pour le modifier.")
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de la modification : {str(e)}")

    def supprimer_eleve(self):
        """Supprime l'élève sélectionné dans le tableau"""
        try:
            # Obtenir l'élève sélectionné depuis le tableau
            selected_eleve = self.get_selected_eleve_from_table()
            if selected_eleve:
                _id, nom, prenom, genre, naissance, statut, cid = selected_eleve
                
                # Confirmation de suppression
                result = messagebox.askyesno(
                    "Confirmer la suppression",
                    f"Êtes-vous sûr de vouloir supprimer l'élève :\n\n"
                    f"• Nom : {nom}\n"
                    f"• Prénom : {prenom}\n"
                    f"• Genre : {genre or 'Non spécifié'}\n\n"
                    f"⚠️ Cette action est irréversible !"
                )
                
                if result:
                    # Supprimer de la base de données
                    conn = get_conn()
                    if conn:
                        cur = conn.cursor()
                        cur.execute("DELETE FROM eleves WHERE id_eleve=?", (_id,))
                        conn.commit()
                        conn.close()
                        
                        self.update_last_action("Suppression", f"Suppression de {nom} {prenom}")
                        messagebox.showinfo("Succès", f"L'élève {nom} {prenom} a été supprimé avec succès.")
                        
                        # Rafraîchir le tableau
                        self.refresh_dashboard()
                    else:
                        messagebox.showerror("Erreur", "Impossible de se connecter à la base de données.")
            else:
                messagebox.showwarning("Aucune sélection", "Veuillez sélectionner un élève dans le tableau pour le supprimer.")
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de la suppression : {str(e)}")
    
    def get_selected_eleve_from_table(self):
        """Récupère l'élève sélectionné depuis le tableau simple"""
        try:
            # Obtenir la fenêtre du tableau si elle existe
            if hasattr(self, 'show_all_window') and self.show_all_window.winfo_exists():
                # Trouver le tableau dans la fenêtre
                for widget in self.show_all_window.winfo_children():
                    if isinstance(widget, ctk.CTkFrame):
                        for child in widget.winfo_children():
                            if isinstance(child, ttk.Treeview):
                                table = child
                                break
                
                if 'table' in locals():
                    # Obtenir l'élément sélectionné
                    selected_items = table.selection()
                    if selected_items:
                        selected_item = selected_items[0]
                        values = table.item(selected_item)['values']
                        
                        if values and len(values) >= 6:
                            # Trouver l'index de la ligne sélectionnée
                            all_items = table.get_children()
                            row_index = all_items.index(selected_item)
                            
                            # Récupérer les données de l'élève depuis self.eleves_data
                            if hasattr(self, 'eleves_data') and row_index < len(self.eleves_data):
                                return self.eleves_data[row_index]
            
            return None
        except Exception as e:
            print(f"Erreur lors de la récupération de l'élève sélectionné : {e}")
            return None

    def supprimer_eleve_specific(self, eleve):
        """Supprime un élève spécifique"""
        _id, nom, prenom, genre, naissance, statut, cid = eleve
        result = messagebox.askyesno(
            "Confirmer la suppression",
            f"Êtes-vous sûr de vouloir supprimer l'élève {nom} {prenom} ?\n\nCette action est irréversible."
        )
        
        if result:
            try:
                conn = get_conn()
                if conn:
                    cur = conn.cursor()
                    cur.execute("DELETE FROM eleves WHERE id_eleve=?", (_id,))
                    conn.commit()
                    conn.close()
                    
                    messagebox.showinfo("Succès", f"L'élève {nom} {prenom} a été supprimé avec succès.")
                    self.refresh_dashboard()
                    
                    # Fermer et rouvrir la fenêtre modale pour actualiser
                    if hasattr(self, 'show_all_window'):
                        self.show_all_window.destroy()
                        self.afficher_tous_eleves_classe()
            except Exception as e:
                messagebox.showerror("Erreur", f"Erreur lors de la suppression : {e}")
    
    def modifier_eleve_selectionne(self, eleve_id, nom, prenom):
        """Modifier un élève sélectionné depuis le tableau modal"""
        # Ouvrir la fenêtre de modification
        self._open_eleve_details_card(eleve_id, nom, prenom)
    
    def supprimer_eleve_selectionne(self, eleve_id, nom, prenom):
        """Supprimer un élève sélectionné depuis le tableau modal"""
        # Confirmation
        if messagebox.askyesno("Confirmer la suppression", 
                              f"Êtes-vous sûr de vouloir supprimer {nom} {prenom} ?"):
            try:
                # Supprimer de la base de données
                conn = get_conn()
                if conn:
                    cursor = conn.cursor()
                    cursor.execute("DELETE FROM eleves WHERE id_eleve = ?", (eleve_id,))
                    conn.commit()
                    conn.close()
                    
                    # Fermer la fenêtre modale et rafraîchir
                    if hasattr(self, 'show_all_window') and self.show_all_window:
                        self.show_all_window.destroy()
                    
                    # Rafraîchir le dashboard
                    self.refresh_dashboard()
                    
                    messagebox.showinfo("Succès", f"{nom} {prenom} a été supprimé avec succès.")
                
            except Exception as e:
                messagebox.showerror("Erreur", f"Erreur lors de la suppression : {str(e)}")

    def transferer_eleve(self):
        """Transfert l'élève sélectionné vers une autre classe"""
        self.update_last_action("Transfert", "Ouverture du formulaire de transfert")
        messagebox.showinfo("Transfert", "Fonctionnalité de transfert d'élève - À implémenter")

    def details_eleve(self):
        """Affiche les détails de l'élève sélectionné"""
        messagebox.showinfo("Détails", "Fonctionnalité de détails d'élève - À implémenter")

    def ouvrir_transfert(self):
        """Ouvre la fenêtre de transfert d'élève"""
        messagebox.showinfo("Transfert", "Fonctionnalité de transfert d'élève - À implémenter")

    def formulaire_eleve(self, mode="Ajouter", eleve=None):
        """Ouvre le formulaire d'élève avec design moderne"""
        popup = ctk.CTkToplevel(self)
        popup.title(f"{mode} Élève")
        popup.geometry("700x500")  # Même taille que le login
        popup.minsize(600, 400)
        popup.transient(self.winfo_toplevel())
        popup.grab_set()
        popup.configure(fg_color=BG_MAIN)
        
        # Centrer la fenêtre comme le login
        self._center_window(popup)
        
        # Contenu principal
        main_container = ctk.CTkFrame(popup, fg_color="transparent")
        main_container.pack(fill="both", expand=True, padx=20, pady=20)
        
        # En-tête du formulaire
        header = ctk.CTkFrame(main_container, fg_color=BG_CARD, corner_radius=12)
        header.pack(fill="x", pady=(0, 15))
        
        title_text = "Nouveau Profil Élève" if mode == "Ajouter" else f"Modification de {eleve.get('nom','')} {eleve.get('prenom','')}"
        ctk.CTkLabel(
            header, 
            text=title_text, 
            font=("Segoe UI", 24, "bold"),
            text_color=ACCENT_BLUE
        ).pack(pady=20)

        # Corps du formulaire
        body = ctk.CTkScrollableFrame(main_container, fg_color=BG_CARD, corner_radius=12)
        body.pack(fill="both", expand=True, pady=(0, 15))
        
        # Champs du formulaire
        fields = [
            ("Matricule", "matricule"),
            ("Nom *", "nom"),
            ("Prénom *", "prenom"),
            ("Date de naissance", "date_naissance"),
            ("Genre", "genre"),
            ("Statut", "statut"),
            ("Téléphone", "telephone"),
            ("Email", "email"),
            ("Adresse", "adresse"),
            ("Nom Parent", "parent_nom"),
            ("Prénom Parent", "parent_prenom"),
            ("Téléphone Parent", "parent_telephone"),
            ("Email Parent", "parent_email"),
            ("Adresse Parent", "parent_adresse"),
            ("Profession Parent", "parent_profession"),
        ]
        
        self.form_entries = {}
        for i, (label, key) in enumerate(fields):
            row = i // 2
            col = i % 2
            
            # Label
            ctk.CTkLabel(
                body, 
                text=label,
                font=("Segoe UI", 12, "bold"),
                text_color=TEXT_PRIMARY
            ).grid(row=row*2, column=col, sticky="w", padx=10, pady=(10, 5))
            
            # Champ de saisie
            if key in ["genre", "statut"]:
                widget = ctk.CTkOptionMenu(
                    body,
                    values=["Masculin", "Féminin"] if key == "genre" else ["Actif", "Inactif"],
                    fg_color=BG_CARD_HOVER,
                    button_color=ACCENT_BLUE,
                    button_hover_color=BORDER_ACCENT,
                    height=35
                )
            else:
                widget = ctk.CTkEntry(
                    body,
                    font=("Segoe UI", 12),
                    fg_color=BG_CARD_HOVER,
                    border_color=BORDER_COLOR,
                    height=35
                )
            
            widget.grid(row=row*2+1, column=col, sticky="ew", padx=10, pady=(0, 10))
            self.form_entries[key] = widget
        
        # Configuration des colonnes
        body.grid_columnconfigure(0, weight=1)
        body.grid_columnconfigure(1, weight=1)

        # Boutons d'action
        footer = ctk.CTkFrame(main_container, fg_color=BG_CARD, corner_radius=8)
        footer.pack(fill="x")
        
        if mode == "Ajouter":
            ctk.CTkButton(
                footer, 
                text="Enregistrer",
                command=lambda: self.save_eleve(popup, mode),
                fg_color=SUCCESS_GREEN, 
                hover_color="#059669",
                height=40,
                font=("Segoe UI", 12, "bold")
            ).pack(side="left", padx=(0, 10), pady=15)
        elif mode == "Modifier":
            ctk.CTkButton(
                footer, 
                text="Mettre à jour",
                command=lambda: self.save_eleve(popup, mode, eleve.get('id_eleve')),
                fg_color=WARNING_ORANGE, 
                hover_color="#d97706",
                height=40,
                font=("Segoe UI", 12, "bold")
            ).pack(side="left", padx=(0, 10), pady=15)

        ctk.CTkButton(
            footer, 
            text="Fermer", 
            command=popup.destroy,
            fg_color=ERROR_RED, 
            hover_color="#dc2626",
            height=40,
            font=("Segoe UI", 12, "bold")
        ).pack(side="right", pady=15)

        # Pré-remplissage si modification
        if isinstance(eleve, dict):
            self.fill_form(eleve)

    def fill_form(self, eleve: dict):
        """Pré-remplit le formulaire avec les données de l'élève"""
        data_map = {
            "matricule": eleve.get("matricule"),
            "nom": eleve.get("nom"),
            "prenom": eleve.get("prenom"),
            "genre": eleve.get("genre"),
            "date_naissance": eleve.get("date_naissance"),
            "statut": eleve.get("statut"),
            "telephone": eleve.get("telephone"),
            "email": eleve.get("email"),
            "adresse": eleve.get("adresse"),
            "parent_nom": eleve.get("parent_nom"),
            "parent_prenom": eleve.get("parent_prenom"),
            "parent_telephone": eleve.get("parent_telephone"),
            "parent_email": eleve.get("parent_email"),
            "parent_adresse": eleve.get("parent_adresse"),
            "parent_profession": eleve.get("parent_profession"),
        }
        
        for key, value in data_map.items():
            w = self.form_entries.get(key)
            if not w or value is None: 
                continue
            try:
                if isinstance(w, ctk.CTkOptionMenu):
                    w.set(value)
                else:
                    w.delete(0, "end")
                    w.insert(0, value)
            except Exception:
                pass

    def save_eleve(self, popup, mode, eleve_id=None):
        """Sauvegarde les données de l'élève"""
        def _get(key):
            w = self.form_entries.get(key)
            return w.get().strip() if w and hasattr(w, "get") else None

        data = {
            "matricule": _get("matricule"),
            "nom": _get("nom"),
            "prenom": _get("prenom"),
            "genre": _get("genre"),
            "date_naissance": _get("date_naissance"),
            "statut": _get("statut"),
            "telephone": _get("telephone"),
            "email": _get("email"),
            "adresse": _get("adresse"),
            "parent_nom": _get("parent_nom"),
            "parent_prenom": _get("parent_prenom"),
            "parent_telephone": _get("parent_telephone"),
            "parent_email": _get("parent_email"),
            "parent_adresse": _get("parent_adresse"),
            "parent_profession": _get("parent_profession"),
        }

        # Validation
        if not all([data.get("nom"), data.get("prenom")]):
            messagebox.showerror("Erreur", "Nom et Prénom sont obligatoires.")
            return

        conn = get_conn()
        if not conn: 
            return
            
        try:
            cur = conn.cursor()
            if mode == "Ajouter":
                cur.execute("""
                    INSERT INTO eleves 
                    (matricule, nom, prenom, genre, date_naissance, statut, telephone, email, adresse, 
                     id_classe, date_inscription, parent_nom, parent_prenom, parent_telephone, 
                     parent_email, parent_adresse, parent_profession)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, date('now'), ?, ?, ?, ?, ?, ?)
                """, (
                    data["matricule"], data["nom"], data["prenom"], data["genre"], data["date_naissance"],
                    data["statut"], data["telephone"], data["email"], data["adresse"], self.selected_classe_id,
                    data["parent_nom"], data["parent_prenom"], data["parent_telephone"],
                    data["parent_email"], data["parent_adresse"], data["parent_profession"]
                ))
                messagebox.showinfo("Succès", "Élève ajouté avec succès.")
            elif mode == "Modifier" and eleve_id:
                cur.execute("""
                    UPDATE eleves SET 
                        matricule=?, nom=?, prenom=?, genre=?, date_naissance=?, statut=?, 
                        telephone=?, email=?, adresse=?, parent_nom=?, parent_prenom=?, 
                        parent_telephone=?, parent_email=?, parent_adresse=?, parent_profession=?
                    WHERE id_eleve=?
                """, (
                    data["matricule"], data["nom"], data["prenom"], data["genre"], data["date_naissance"],
                    data["statut"], data["telephone"], data["email"], data["adresse"],
                    data["parent_nom"], data["parent_prenom"], data["parent_telephone"],
                    data["parent_email"], data["parent_adresse"], data["parent_profession"], eleve_id
                ))
                messagebox.showinfo("Succès", "Élève mis à jour avec succès.")

            conn.commit()
            self.refresh_dashboard()
            popup.destroy()
        except sqlite3.Error as e:
            messagebox.showerror("Erreur de base de données", f"Une erreur est survenue : {e}")
        finally:
            conn.close()

    def _open_eleve_details_card(self, eleve):
        """Ouvre la carte de détails de l'élève"""
        popup = ctk.CTkToplevel(self)
        popup.title(f"Détails - {eleve.get('nom', '')} {eleve.get('prenom', '')}")
        popup.geometry("700x500")
        popup.transient(self.winfo_toplevel())
        popup.grab_set()
        popup.configure(fg_color=BG_MAIN)
        
        # Contenu principal
        main_container = ctk.CTkFrame(popup, fg_color="transparent")
        main_container.pack(fill="both", expand=True, padx=20, pady=20)
        
        # En-tête avec design moderne
        header = ctk.CTkFrame(main_container, fg_color=ACCENT_BLUE, corner_radius=15)
        header.pack(fill="x", pady=(0, 15))
        
        # Contenu de l'en-tête avec icône
        header_content = ctk.CTkFrame(header, fg_color="transparent")
        header_content.pack(fill="x", padx=20, pady=15)
        
        # Icône élève
        eleve_icon = get_icon("eleve", (40, 40))
        if eleve_icon:
            icon_label = ctk.CTkLabel(header_content, text="", image=eleve_icon, text_color=WHITE)
            icon_label._imgref = eleve_icon
            icon_label.pack(side="left", padx=(0, 15))
        
        # Titre principal
        title_label = ctk.CTkLabel(
            header_content, 
            text=f"Détails de {eleve.get('nom', '')} {eleve.get('prenom', '')}",
            font=("Segoe UI", 28, "bold"),
            text_color=WHITE
        )
        title_label.pack(side="left")
        
        # Badge du statut à droite
        statut = eleve.get('statut', 'Inconnu')
        statut_color = SUCCESS_GREEN if statut.lower() == 'actif' else ERROR_RED
        statut_badge = ctk.CTkFrame(header_content, fg_color=statut_color, corner_radius=20)
        statut_badge.pack(side="right", padx=(15, 0))
        
        statut_label = ctk.CTkLabel(
            statut_badge,
            text=f"Statut: {statut}",
            font=("Segoe UI", 14, "bold"),
            text_color=WHITE
        )
        statut_label.pack(padx=15, pady=8)

        # Corps des détails
        body = ctk.CTkScrollableFrame(main_container, fg_color=BG_CARD, corner_radius=12)
        body.pack(fill="both", expand=True, pady=(0, 15))
        
        # Affichage des informations
        details = [
            ("Matricule", eleve.get("matricule", "—")),
            ("Nom", eleve.get("nom", "—")),
            ("Prénom", eleve.get("prenom", "—")),
            ("Date de naissance", eleve.get("date_naissance", "—")),
            ("Genre", eleve.get("genre", "—")),
            ("Statut", eleve.get("statut", "—")),
            ("Téléphone", eleve.get("telephone", "—")),
            ("Email", eleve.get("email", "—")),
            ("Adresse", eleve.get("adresse", "—")),
            ("Classe", get_classe_name(eleve.get("id_classe")) or "—"),
            ("Date d'inscription", eleve.get("date_inscription", "—")),
            ("Nom Parent", eleve.get("parent_nom", "—")),
            ("Prénom Parent", eleve.get("parent_prenom", "—")),
            ("Téléphone Parent", eleve.get("parent_telephone", "—")),
            ("Email Parent", eleve.get("parent_email", "—")),
            ("Adresse Parent", eleve.get("parent_adresse", "—")),
            ("Profession Parent", eleve.get("parent_profession", "—")),
        ]
        
        for i, (label, value) in enumerate(details):
            row = i // 2
            col = i % 2
            
            # Conteneur pour chaque champ avec badge coloré
            field_container = ctk.CTkFrame(body, fg_color="transparent")
            field_container.grid(row=row*2, column=col, sticky="ew", padx=10, pady=8)
            
            # Couleurs pour les badges selon le type de champ
            badge_colors = {
                "Matricule": PRIMARY_BLUE,
                "Nom": SUCCESS_GREEN,
                "Prénom": SUCCESS_GREEN,
                "Date de naissance": WARNING_ORANGE,
                "Genre": ACCENT_BLUE,
                "Statut": ERROR_RED if str(value).lower() == 'inactif' else SUCCESS_GREEN,
                "Téléphone": PRIMARY_BLUE,
                "Email": ACCENT_BLUE,
                "Adresse": WARNING_ORANGE,
                "Classe": SUCCESS_GREEN,
                "Date d'inscription": PRIMARY_BLUE,
                "Nom Parent": WARNING_ORANGE,
                "Prénom Parent": WARNING_ORANGE,
                "Téléphone Parent": PRIMARY_BLUE,
                "Email Parent": ACCENT_BLUE,
                "Adresse Parent": WARNING_ORANGE,
                "Profession Parent": PRIMARY_BLUE,
            }
            
            badge_color = badge_colors.get(label, ACCENT_BLUE)
            
            # Label avec badge coloré
            label_badge = ctk.CTkFrame(field_container, fg_color=badge_color, corner_radius=8)
            label_badge.pack(fill="x", pady=(0, 5))
            
            ctk.CTkLabel(
                label_badge, 
                text=f"{label}:",
                font=("Segoe UI", 11, "bold"),
                text_color=WHITE
            ).pack(padx=10, pady=5)
            
            # Valeur dans un cadre stylé
            value_frame = ctk.CTkFrame(field_container, fg_color=BG_CARD_HOVER, corner_radius=8)
            value_frame.pack(fill="x")
            
            ctk.CTkLabel(
                value_frame, 
                text=str(value),
                font=("Segoe UI", 12),
                text_color=TEXT_PRIMARY
            ).pack(padx=10, pady=8)
        
        # Configuration des colonnes
        body.grid_columnconfigure(0, weight=1)
        body.grid_columnconfigure(1, weight=1)

        # Boutons d'action
        footer = ctk.CTkFrame(main_container, fg_color=BG_CARD, corner_radius=8)
        footer.pack(fill="x")
        
        # Conteneur des boutons d'action
        buttons_container = ctk.CTkFrame(footer, fg_color="transparent")
        buttons_container.pack(fill="x", padx=20, pady=15)
        
        # Bouton Modifier
        edit_icon = get_icon("edit", (20, 20))
        btn_edit = ctk.CTkButton(
            buttons_container,
            text="Modifier",
            image=edit_icon,
            fg_color=ACCENT_BLUE,
            text_color=WHITE,
            hover_color=HOVER_PRIMARY,
            command=lambda: self.formulaire_eleve("Modifier", eleve),
            corner_radius=10,
            height=40,
            width=120,
            font=("Segoe UI", 12, "bold"),
            border_width=1,
            border_color=ACCENT_BLUE
        )
        if edit_icon:
            btn_edit._imgref = edit_icon
        btn_edit.pack(side="left", padx=(0, 10))
        
        # Bouton Supprimer
        delete_icon = get_icon("delete", (20, 20))
        btn_delete = ctk.CTkButton(
            buttons_container,
            text="Supprimer",
            image=delete_icon,
            fg_color=WARNING_ORANGE,
            text_color=WHITE,
            hover_color=HOVER_WARNING,
            command=self.supprimer_eleve,
            corner_radius=10,
            height=40,
            width=120,
            font=("Segoe UI", 12, "bold"),
            border_width=1,
            border_color=WARNING_ORANGE
        )
        if delete_icon:
            btn_delete._imgref = delete_icon
        btn_delete.pack(side="left", padx=(0, 10))
        
        # Bouton Fermer
        btn_close = ctk.CTkButton(
            buttons_container,
            text="Fermer",
            command=popup.destroy,
            fg_color=SUCCESS_GREEN,
            text_color=WHITE,
            hover_color=HOVER_SUCCESS,
            corner_radius=10,
            height=40,
            width=120,
            font=("Segoe UI", 12, "bold"),
            border_width=1,
            border_color=SUCCESS_GREEN
        )
        btn_close.pack(side="right")

# ============ Exécution directe ============
if __name__ == "__main__":
    app = ctk.CTk()
    app.title("Dashboard des Élèves - Inspiré du Design Principal")
    app.geometry("1400x900")
    app.configure(fg_color=BG_MAIN)
    app.grid_rowconfigure(0, weight=1)
    app.grid_columnconfigure(0, weight=1)
    
    dashboard = DashboardEleves(app)
    dashboard.pack(fill="both", expand=True)

    app.mainloop()
