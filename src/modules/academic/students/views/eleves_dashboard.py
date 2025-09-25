# -*- coding: utf-8 -*-
"""
Dashboard des Élèves - Utilise le thème global EduManager+
- Thème sombre parfait avec couleurs harmonieuses
- Design moderne et professionnel
- Interface utilisateurs optimisée
"""

from database.connection import get_db_connection
from database.connection import get_db_connection
from database.connection import get_db_connection
import os
import sys
import datetime
# Remplacé par SQL Server  # Remplacé par SQL Server
import tkinter as tk
from tkinter import messagebox, ttk, filedialog
import customtkinter as ctk
from PIL import Image, ImageTk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from CTkTable import CTkTable

from resources.themes.theme import DARK_ACCENT_COOL

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
ICONS_DIR_REL = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", "..", "..", "..", "resources", "icons"))

# Vérifier quel répertoire existe
if os.path.isdir(ICONS_DIR_ABS):
    ICONS_DIR = ICONS_DIR_ABS
elif os.path.isdir(ICONS_DIR_REL):
    ICONS_DIR = ICONS_DIR_REL
else:
    # Essayer le répertoire courant
    ICONS_DIR = os.path.join(os.getcwd(), "resources", "icons")
    if not os.path.isdir(ICONS_DIR):
        print(f"⚠️ Répertoire d'icônes non trouvé. Chemins testés:")
        print(f"   - Absolu: {ICONS_DIR_ABS}")
        print(f"   - Relatif: {ICONS_DIR_REL}")
        print(f"   - Courant: {ICONS_DIR}")
        ICONS_DIR = ICONS_DIR_REL  # Fallback vers le relatif

# =================== CACHE ICÔNES =====================
_ICON_CACHE = {}  # Cache des icônes PIL → CTkImage

# Debug: confirmer le répertoire des icônes
print(f"📁 Répertoire d'icônes détecté: {ICONS_DIR}")
print(f"📁 Répertoire existe: {os.path.exists(ICONS_DIR)}")
if os.path.exists(ICONS_DIR):
    icon_count = len([f for f in os.listdir(ICONS_DIR) if f.endswith('.png')])
    print(f"📁 Nombre d'icônes disponibles: {icon_count}")

def get_icon(name: str, size=(24, 24)):
    """Cache d'icônes PIL → CTkImage optimisé avec gestion d'erreur améliorée."""
    try:
        key = f"{name}_{size[0]}x{size[1]}"
        if key in _ICON_CACHE:
            return _ICON_CACHE[key]
        
        # Essayer d'abord le nom exact
        icon_path = os.path.join(ICONS_DIR, f"{name}.png")
        
        # Si pas trouvé, essayer avec le mapping
        if not os.path.exists(icon_path) and name in ICON_MAP:
            mapped_name = ICON_MAP[name]
            icon_path = os.path.join(ICONS_DIR, f"{mapped_name}.png")
        
        if not os.path.exists(icon_path):
            print(f"⚠️ Icône '{name}' non trouvée: {icon_path}")
            print(f"📁 Répertoire icônes: {ICONS_DIR}")
            print(f"📁 Répertoire existe: {os.path.exists(ICONS_DIR)}")
            if os.path.exists(ICONS_DIR):
                available_icons = [f for f in os.listdir(ICONS_DIR) if f.endswith('.png')]
                print(f"📁 Icônes disponibles: {available_icons[:10]}...")  # Afficher les 10 premières
            return None
        
        pil_img = Image.open(icon_path).convert("RGBA")
        # Optimiser la taille pour réduire la charge
        pil_img = pil_img.resize(size, Image.Resampling.LANCZOS)
        ctk_img = ctk.CTkImage(light_image=pil_img, dark_image=pil_img, size=size)
        _ICON_CACHE[key] = ctk_img
        print(f"✅ Icône '{name}' chargée avec succès: {icon_path}")
        return ctk_img
    except Exception as e:
        print(f"⚠️ Erreur icône {name}: {e}")
        return None

# =================== HELPERS =====================
def calculate_age(date_naissance):
    """Calcule l'âge à partir de la date de naissance"""
    if not date_naissance:
        return "—"
    try:
        today = datetime.date.today()
        age = today.year - date_naissance.year - ((today.month, today.day) < (date_naissance.month, date_naissance.day))
        return str(age)
    except:
        return "—"

# =================== MAPPING ICONES =====================
ICON_MAP = {
    "eleves": "eleve", "filles": "eleve", "garcons": "person", "classes": "class",
    "profs": "person", "ajouter": "add", "edit": "edit", "delete": "delete",
    "detail": "detail", "transferer": "transfer", "refresh": "refresh", "search": "search",
    "group": "group", "person": "person", "home": "home", "logout": "logout",
    "analytics": "stats", "settings": "settings", "stats": "stats", "csv": "csv",
    "info": "detail"
}

# =================== SQLITE HELPERS =====================
def get_conn():
    """Connexion SQL Server avec gestion d'erreurs."""
    try:
        import pyodbc
        connection_string = (
            "DRIVER={ODBC Driver 17 for SQL Server};"
            "SERVER=.;"
            "DATABASE=EduManager;"
            "Trusted_Connection=yes;"
        )
        conn = pyodbc.connect(connection_string)
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
            cur.execute("SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = ?", (t,))
            if cur.fetchone():
                table_name = t
                break
        if not table_name:
            return 0
        cur.execute(f"SELECT COUNT(*) FROM {table_name}")
        r = cur.fetchone()
        return int((r[0] if not isinstance(r, dict) else r[0]) or 0)
    except Exception as e:
        print(f"⚠️ get_stats_count_any: {e}")
        return 0
    finally:
        try:
            conn.close()
        except:
            pass

def get_stats_eleves(classe_id=None):
    """Récupère les statistiques des élèves avec les vraies données de la base."""
    conn = get_conn()
    if not conn:
        return {"total": 0, "filles": 0, "garcons": 0, "classes": 0, "profs": 0}
    
    try:
        cur = conn.cursor()
        stats = {}
        
        if classe_id is None:
            # Statistiques globales avec les vraies données
            cur.execute("SELECT COUNT(*) FROM eleves")
            stats["total"] = cur.fetchone()[0] or 0
            
            cur.execute("SELECT COUNT(*) FROM eleves WHERE genre = 'F'")
            stats["filles"] = cur.fetchone()[0] or 0
            
            cur.execute("SELECT COUNT(*) FROM eleves WHERE genre = 'M'")
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
            # Statistiques pour une classe spécifique avec les vraies données
            cur.execute("SELECT COUNT(*) FROM eleves WHERE id_classe=?", (classe_id,))
            stats["total"] = cur.fetchone()[0] or 0
            
            cur.execute("SELECT COUNT(*) FROM eleves WHERE genre = 'F' AND id_classe=?", (classe_id,))
            stats["filles"] = cur.fetchone()[0] or 0
            
            cur.execute("SELECT COUNT(*) FROM eleves WHERE genre = 'M' AND id_classe=?", (classe_id,))
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
    """Retourne [(nom_classe, effectif)] avec les vraies données de la base."""
    conn = get_conn()
    if not conn:
        return []
    try:
        cur = conn.cursor()
        cur.execute("""SELECT c.nom_classe, COUNT(e.id_eleve) as effectif
            FROM classes c
            LEFT JOIN eleves e ON c.id_classe = e.id_classe
            GROUP BY c.id_classe, c.nom_classe
            ORDER BY effectif DESC
            OFFSET 0 ROWS FETCH NEXT ? ROWS ONLY
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
    """Récupère toutes les classes avec les vraies données de la base."""
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

def get_eleves_list(classe_id=None, search_term="", page=1, page_size=50):
    """Récupère la liste des élèves avec pagination et recherche - Optimisé pour 1000+ élèves."""
    conn = get_conn()
    if not conn:
        return []
    try:
        cur = conn.cursor()
        
        # Calculer l'offset pour la pagination
        offset = (page - 1) * page_size
        
        # Construire la requête avec recherche et pagination
        base_query = """
            SELECT e.id_eleve, e.nom, e.prenom, e.genre, e.date_naissance, e.id_classe, c.nom_classe as classe_nom
            FROM eleves e
            LEFT JOIN classes c ON e.id_classe = c.id_classe
        """
        
        where_conditions = []
        params = []
        
        # Filtre par classe
        if classe_id is not None:
            where_conditions.append("e.id_classe = ?")
            params.append(classe_id)
        
        # Filtre par terme de recherche
        if search_term:
            where_conditions.append("(e.nom LIKE ? OR e.prenom LIKE ? OR c.nom_classe LIKE ?)")
            search_pattern = f"%{search_term}%"
            params.extend([search_pattern, search_pattern, search_pattern])
        
        # Construire la requête finale
        if where_conditions:
            query = base_query + " WHERE " + " AND ".join(where_conditions)
        else:
            query = base_query
        
        query += " ORDER BY e.nom, e.prenom OFFSET ? ROWS FETCH NEXT ? ROWS ONLY"
        params.extend([offset, page_size])
        
        cur.execute(query, params)
        return cur.fetchall()
        
    except Exception as e:
        print(f"⚠️ get_eleves_list: {e}")
        return []
    finally:
        try:
            conn.close()
        except:
            pass

def get_eleves_count(classe_id=None, search_term=""):
    """Récupère le nombre total d'élèves pour la pagination."""
    conn = get_conn()
    if not conn:
        return 0
    try:
        cur = conn.cursor()
        
        base_query = """
            SELECT COUNT(*)
            FROM eleves e
            LEFT JOIN classes c ON e.id_classe = c.id_classe
        """
        
        where_conditions = []
        params = []
        
        # Filtre par classe
        if classe_id is not None:
            where_conditions.append("e.id_classe = ?")
            params.append(classe_id)
        
        # Filtre par terme de recherche
        if search_term:
            where_conditions.append("(e.nom LIKE ? OR e.prenom LIKE ? OR c.nom_classe LIKE ?)")
            search_pattern = f"%{search_term}%"
            params.extend([search_pattern, search_pattern, search_pattern])
        
        # Construire la requête finale
        if where_conditions:
            query = base_query + " WHERE " + " AND ".join(where_conditions)
        else:
            query = base_query
        
        cur.execute(query, params)
        return cur.fetchone()[0] or 0
        
    except Exception as e:
        print(f"⚠️ get_eleves_count: {e}")
        return 0
    finally:
        try:
            conn.close()
        except:
            pass

def get_classe_name(classe_id):
    """Récupère le nom d'une classes."""
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
        return row[0] if row and len(row) > 0 else None
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
        # conn.row_factory = sqlite3.Row  # Remplacé par SQL Server
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
        
        # Variables pour la pagination et la recherche
        self.current_page = 1
        self.page_size = 50
        self.total_pages = 1
        self.search_term = ""
        self.total_eleves = 0
        
        # Variables pour la navigation Windows 11 style
        self.current_view = "classes"  # "classes" ou "students"
        self.navigation_stack = []  # Pour gérer l'historique de navigation

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
        self.main_content_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.main_content_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 4), pady=(0, 0))
        self.main_content_frame.grid_rowconfigure(3, weight=1)  # Le graphique prendra l'espace restant
        self.main_content_frame.grid_columnconfigure(0, weight=1)

        # Création des sections (sans breadcrumb)
        self._create_header(self.main_content_frame)
        self._create_stats_cards(self.main_content_frame)
        self._create_chart_section(self.main_content_frame)

    def _create_breadcrumb(self, parent):
        """Crée le breadcrumb de navigation style Windows 11"""
        self.breadcrumb_frame = ctk.CTkFrame(parent, fg_color="transparent")
        self.breadcrumb_frame.pack(fill="x", pady=(0, PADDING_SMALL))
        
        # Conteneur pour le breadcrumb
        breadcrumb_container = ctk.CTkFrame(self.breadcrumb_frame, fg_color="transparent")
        breadcrumb_container.pack(side="left")
        
        # Bouton retour (visible seulement quand on est dans la vue étudiants)
        self.back_button = ctk.CTkButton(
            breadcrumb_container, 
            text="←", 
            width=30, 
            height=30,
            fg_color="transparent", 
            hover_color=BG_CARD_HOVER,
            text_color=TEXT_ACCENT,
            font=("Segoe UI", 16, "bold"),
            command=self.navigate_back,
            corner_radius=6
        )
        self.back_button.pack(side="left", padx=(0, 8))
        
        # Texte du breadcrumb
        self.breadcrumb_label = ctk.CTkLabel(
            breadcrumb_container,
            text="Élèves",
            font=("Segoe UI", 14, "bold"),
            text_color=TEXT_ACCENT
        )
        self.breadcrumb_label.pack(side="left")
        
        # Initialiser l'état
        self.update_breadcrumb()

    def update_breadcrumb(self):
        """Met à jour le breadcrumb selon la vue actuelle (méthode désactivée)"""
        # Breadcrumb supprimé - méthode désactivée
        pass

    def navigate_back(self):
        """Retourne à la vue précédente"""
        if self.current_view == "students":
            self.show_classes_view()

    def show_classes_view(self):
        """Affiche la vue des classes"""
        self.current_view = "classes"
        self.selected_classe = None
        self.selected_classe_id = None
        self.update_breadcrumb()
        
        # Restaurer le contenu original
        self.clear_main_content()
        self._create_header(self.main_content_frame)
        self._create_stats_cards(self.main_content_frame)
        self._create_chart_section(self.main_content_frame)
        
        # Rafraîchir les données sans appeler refresh_dashboard pour éviter la boucle
        self.load_eleves_data()
        graph_data = fetch_effectifs_par_classe(limit=50)
        self.update_chart(graph_data)

    def show_students_view(self, classe_name, classe_id):
        """Affiche la vue des étudiants d'une classe"""
        self.current_view = "students"
        self.selected_classe = classe_name
        self.selected_classe_id = classe_id
        self.update_breadcrumb()
        self.refresh_dashboard()

    def _create_header(self, parent):
        """Header moderne en deux sections avec boutons sans fond élégants"""
        header_frame = ctk.CTkFrame(parent, fg_color="transparent")
        header_frame.pack(fill="x", pady=(0, PADDING_MEDIUM))
        header_frame.grid_columnconfigure(0, weight=1)
        header_frame.grid_columnconfigure(1, weight=1)

        # =================== SECTION GAUCHE - TITRE ET DESCRIPTION ===================
        left_section = ctk.CTkFrame(header_frame, fg_color="transparent")
        left_section.grid(row=0, column=0, sticky="w", padx=(PADDING_MEDIUM, 0))

        # Titre principal avec icône
        title_frame = ctk.CTkFrame(left_section, fg_color="transparent")
        title_frame.pack(anchor="w", pady=(PADDING_SMALL, 0))

        # Icône principale
        main_icon = get_icon("eleve", (32, 32))
        if main_icon:
            icon_label = ctk.CTkLabel(title_frame, text="", image=main_icon, text_color=TEXT_ACCENT)
            icon_label._imgref = main_icon
            icon_label.pack(side="left", padx=(0, PADDING_SMALL))

        # Titre principal
        ctk.CTkLabel(title_frame, text="Élèves", font=FONT_HERO, text_color=TEXT_ACCENT).pack(side="left")
        
        # Description
        ctk.CTkLabel(left_section, text="statistiques des élèves", 
                     font=("Segoe UI", 14), text_color=TEXT_SECONDARY).pack(anchor="w", pady=(MARGIN_SMALL, 0))

        # =================== SECTION DROITE - ACTIONS ET RECHERCHE ===================
        right_section = ctk.CTkFrame(header_frame, fg_color="transparent")
        right_section.grid(row=0, column=1, sticky="e", padx=(0, PADDING_MEDIUM))

        # Conteneur principal pour les actions
        actions_container = ctk.CTkFrame(right_section, fg_color="transparent")
        actions_container.pack(side="right")

        # Barre de recherche
        search_frame = ctk.CTkFrame(actions_container, fg_color="transparent")
        search_frame.pack(side="left", padx=(0, PADDING_MEDIUM))

        self.search_var = ctk.StringVar()
        self.search_entry = ctk.CTkEntry(search_frame, placeholder_text="Rechercher un élève...", 
                                        width=220, fg_color=BG_CARD, text_color=TEXT_PRIMARY, 
                                        border_color=BORDER_COLOR, corner_radius=10, font=FONT_SECONDARY, 
                                        textvariable=self.search_var, placeholder_text_color=TEXT_MUTED)
        self.search_entry.pack(side="left", padx=(0, PADDING_SMALL))
        self.search_entry.bind("<KeyRelease>", self.on_search_change)

        # Icône de recherche
        search_icon = get_icon("search", (20, 20))
        if search_icon:
            search_btn = ctk.CTkButton(search_frame, text="", image=search_icon, width=40, height=40,
                                      fg_color="transparent", hover_color=BG_CARD_HOVER, corner_radius=8,
                                      command=self.on_search_change, border_width=0)
            search_btn._imgref = search_icon
            search_btn.pack(side="left")

        # Boutons d'action avec couleurs harmonisées
        buttons_frame = ctk.CTkFrame(actions_container, fg_color="transparent")
        buttons_frame.pack(side="left")

        # Bouton Ajouter Élève
        add_icon = get_icon("add", (22, 22))
        btn_add = ctk.CTkButton(buttons_frame, text="", width=45, height=45,
                               fg_color="transparent", hover_color=BG_CARD_HOVER, corner_radius=8,
                               command=self.ajouter_eleve, border_width=1, border_color=BORDER_COLOR,
                               image=add_icon if add_icon else None)
        if add_icon:
            btn_add._imgref = add_icon
        btn_add.pack(side="left", padx=(0, 8))

        # Bouton Voir tous les élèves
        group_icon = get_icon("group", (22, 22))
        btn_group = ctk.CTkButton(buttons_frame, text="", width=45, height=45,
                                 fg_color="transparent", hover_color=BG_CARD_HOVER, corner_radius=8,
                                 command=self.afficher_tous_eleves_classe, border_width=1, border_color=BORDER_COLOR,
                                 image=group_icon if group_icon else None)
        if group_icon:
            btn_group._imgref = group_icon
        btn_group.pack(side="left", padx=(0, 8))

        # Bouton Rafraîchir
        refresh_icon = get_icon("refresh", (22, 22))
        btn_refresh = ctk.CTkButton(buttons_frame, text="", width=45, height=45,
                                   fg_color="transparent", hover_color=BG_CARD_HOVER, corner_radius=8,
                                   command=self.refresh_dashboard, border_width=1, border_color=BORDER_COLOR,
                                   image=refresh_icon if refresh_icon else None)
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
            ("Total Élèves", "eleves", SUCCESS_GREEN),
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
        """Rafraîchit le dashboard selon la vue actuelle"""
        self.update_last_action("Rafraîchissement", "Actualisation des données")
        
        if self.current_view == "classes":
            # Vue des classes - afficher les statistiques générales
            # Ne pas appeler update_dashboard_for_classe pour éviter la boucle infinie
            # Charger les données des élèves avec pagination
            self.load_eleves_data()
            # Mise à jour du graphique avec toutes les classes
            graph_data = fetch_effectifs_par_classe(limit=50)
            self.update_chart(graph_data)
        elif self.current_view == "students":
            # Vue des étudiants - afficher la liste des étudiants de la classe sélectionnée
            self.show_students_list()

    def show_students_list(self):
        """Affiche la liste des étudiants de la classe sélectionnée dans la zone principale"""
        if not self.selected_classe_id:
            return
            
        if not hasattr(self, 'main_content_frame') or not self.main_content_frame.winfo_exists():
            return
            
        # Stocker le nom de la classe pour l'affichage
        self.current_classe_nom = self.selected_classe
            
        # Récupérer les étudiants de la classe
        eleves_classe = get_eleves_list(self.selected_classe_id)
        
        if not eleves_classe:
            # Afficher un message si aucun étudiant
            self.clear_main_content()
            no_students_frame = ctk.CTkFrame(self.main_content_frame, fg_color=BG_CARD, corner_radius=12)
            no_students_frame.pack(fill="both", expand=True, padx=4, pady=4)
            
            no_students_label = ctk.CTkLabel(
                no_students_frame,
                text=f"Aucun élève trouvé dans la classe {self.selected_classe}",
                font=("Segoe UI", 16),
                text_color=TEXT_MUTED
            )
            no_students_label.pack(expand=True)
            return
        
        # Nettoyer le contenu principal
        self.clear_main_content()
        
        # Créer directement le tableau des étudiants (sans en-tête)
        self.create_students_cards(eleves_classe)

    def clear_main_content(self):
        """Nettoie complètement le contenu principal"""
        if not hasattr(self, 'main_content_frame') or not self.main_content_frame.winfo_exists():
            return
            
        # Supprimer TOUS les enfants du main_content_frame
        children = list(self.main_content_frame.winfo_children())
        for widget in children:
            try:
                widget.destroy()
            except:
                pass  # Ignorer les erreurs de destruction

    def create_students_cards(self, eleves_classe):
        """Crée un tableau d'élèves qui monte au niveau de la section Classes"""
        # Conteneur principal - tableau qui monte au niveau des classes
        main_container = ctk.CTkFrame(self.main_content_frame, fg_color="transparent")
        main_container.pack(fill="both", expand=True, padx=0, pady=(0, 0))
        
        # Panneau du tableau qui monte au niveau de la section Classes
        self.students_table_frame = ctk.CTkFrame(main_container, fg_color=BG_CARD, corner_radius=12)
        self.students_table_frame.pack(fill="both", expand=True, padx=0, pady=(0, 0))
        
        # Stocker les données des élèves
        self.eleves_data = eleves_classe
        self.selected_student = None
        
        # Créer le tableau des élèves avec en-tête intégré
        self.create_students_table(eleves_classe)

    def create_students_table(self, eleves_classe):
        """Crée le tableau des élèves avec section titre, recherche et boutons"""
        # Section titre et recherche au-dessus du tableau
        header_section = ctk.CTkFrame(self.students_table_frame, fg_color="transparent")
        header_section.pack(fill="x", padx=10, pady=(2, 2))
        
        # Titre de la section avec nom de classe
        classe_nom = getattr(self, 'current_classe_nom', 'Classe')
        title_label = ctk.CTkLabel(
            header_section,
            text=f"Élèves de la classe {classe_nom}",
            font=("Segoe UI", 18, "bold"),
            text_color=TEXT_PRIMARY
        )
        title_label.pack(side="left", padx=(0, 20))
        
        # Barre de recherche (diminuée)
        search_frame = ctk.CTkFrame(header_section, fg_color=BG_CARD, corner_radius=8, border_width=1, border_color=BORDER_COLOR)
        search_frame.pack(side="left")
        
        search_entry = ctk.CTkEntry(
            search_frame,
            placeholder_text="Rechercher...",
            width=200,
            height=32,
            font=("Segoe UI", 12),
            fg_color="transparent",
            border_width=0
        )
        search_entry.pack(side="left", padx=8, pady=4)
        
        # Icône de recherche
        search_icon = get_icon("search", (16, 16))
        if search_icon:
            search_btn = ctk.CTkButton(
                search_frame,
                text="",
                image=search_icon,
                width=32,
                height=32,
                fg_color="transparent",
                hover_color=BG_CARD_HOVER,
                corner_radius=8
            )
            search_btn.pack(side="right", padx=4, pady=4)
        
        # Boutons d'action à droite
        actions_frame = ctk.CTkFrame(header_section, fg_color="transparent")
        actions_frame.pack(side="right")
        
        # Bouton Retour
        back_icon = get_icon("arrow-right", (18, 18))
        if back_icon:
            back_btn = ctk.CTkButton(
                actions_frame,
                text="",
                image=back_icon,
                width=40,
                height=32,
                fg_color="transparent",
                hover_color=BG_CARD_HOVER,
                corner_radius=8,
                border_width=1,
                border_color=BORDER_COLOR,
                command=self._go_back_to_classes
            )
            back_btn.pack(side="left", padx=(0, 5))
        
        # Bouton Modifier
        edit_icon = get_icon("edit", (18, 18))
        if edit_icon:
            edit_btn = ctk.CTkButton(
                actions_frame,
                text="",
                image=edit_icon,
                width=40,
                height=32,
                fg_color="transparent",
                hover_color=BG_CARD_HOVER,
                corner_radius=8,
                border_width=1,
                border_color=BORDER_COLOR,
                command=self._edit_selected_student
            )
            edit_btn.pack(side="left", padx=(0, 5))
        
        # Bouton Supprimer
        delete_icon = get_icon("delete", (18, 18))
        if delete_icon:
            delete_btn = ctk.CTkButton(
                actions_frame,
                text="",
                image=delete_icon,
                width=40,
                height=32,
                fg_color="transparent",
                hover_color=ERROR_RED,
                corner_radius=8,
                border_width=1,
            border_color=BORDER_COLOR,
                command=self._delete_selected_student
            )
            delete_btn.pack(side="left", padx=(0, 5))
        
        # Bouton Exporter
        export_icon = get_icon("csv", (18, 18))
        if export_icon:
            export_btn = ctk.CTkButton(
                actions_frame,
                text="",
                image=export_icon,
                width=40,
                height=32,
                fg_color="transparent",
                hover_color=BG_CARD_HOVER,
                corner_radius=8,
                border_width=1,
                border_color=BORDER_COLOR,
                command=self._export_students
            )
            export_btn.pack(side="left")
        
        # Conteneur du tableau avec scroll (dimensions intactes)
        table_scroll_container = ctk.CTkScrollableFrame(self.students_table_frame, fg_color="transparent")
        table_scroll_container.pack(fill="both", expand=True, padx=5, pady=(0, 5))
        
        if not eleves_classe:
            # Message si aucun élève
            empty_label = ctk.CTkLabel(
                table_scroll_container,
                text="Aucun élève trouvé dans cette classe",
                font=("Segoe UI", 14),
                text_color=TEXT_MUTED
            )
            empty_label.pack(expand=True)
            return
        
        # Préparer les données du tableau avec en-têtes
        headers = ["Nom", "Prénom", "Genre", "Âge", "Classe", "Statut"]
        table_data = [headers]  # Ajouter les en-têtes comme première ligne
        
        for eleve in eleves_classe:
            if len(eleve) >= 7:
                _id, nom, prenom, genre, naissance, classe_id, classe_nom = eleve
                age = calculate_age(naissance)
                
                # Déterminer le statut (actif par défaut)
                statut = "Actif"
                
                # Créer une ligne de données (sans ID, avec classe)
                row = [
                    nom or "",
                    prenom or "",
                    genre or "",
                    f"{age} ans",
                    classe_nom or "Non assigné",
                    statut
                ]
                table_data.append(row)
        
        # Créer le tableau CTkTable avec le thème complet
        self.students_table = CTkTable(
            master=table_scroll_container,
            row=len(table_data),
            column=len(headers),
            values=table_data,
            # Configuration du thème complet
            header_color=BG_SIDEBAR,
            header_text_color=TEXT_PRIMARY,
            colors=[BG_CARD, BG_MAIN],  # Alternance des couleurs de fond
            hover_color=ACCENT_BLUE,
            selected_row_color=ACCENT_BLUE,
            selected_row_text_color=WHITE,
            text_color=TEXT_PRIMARY,
            font=("Segoe UI", 12),
            corner_radius=8,
            border_width=1,
            border_color=BORDER_COLOR
        )
        
        self.students_table.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Configurer la sélection de ligne
        self.students_table.bind("<Button-1>", self._on_student_table_select)

    def _on_student_table_select(self, event):
        """Gestionnaire de sélection dans le tableau des élèves"""
        try:
            # Obtenir la ligne sélectionnée
            selected_row_info = self.students_table.get_selected_row()
            if selected_row_info is None:
                print("⚠️ Aucune ligne sélectionnée")
                return
            
            print(f"🔍 Informations de sélection: {selected_row_info}")
            
            # Extraire l'index de la ligne sélectionnée
            if isinstance(selected_row_info, dict):
                selected_row_index = selected_row_info.get('row', 0)
            else:
                selected_row_index = selected_row_info
            
            # Récupérer les données de l'élève sélectionné (nom et prénom)
            # CTkTable.get() retourne TOUTES les données du tableau
            all_table_data = self.students_table.get(selected_row_info)
            if not all_table_data or len(all_table_data) < 2:
                print("⚠️ Données de tableau invalides")
                return
                
            print(f"🔍 Données complètes du tableau: {len(all_table_data)} lignes")
            print(f"🔍 Index de ligne sélectionnée: {selected_row_index}")
            
            # La première ligne (index 0) contient les en-têtes
            # La ligne sélectionnée est à l'index selected_row_index + 1 (car on a ajouté les en-têtes)
            if selected_row_index + 1 < len(all_table_data):
                student_data = all_table_data[selected_row_index + 1]
                print(f"🔍 Données de l'élève sélectionné: {student_data}")
                
                # Extraire nom et prénom (index 0 et 1 des données élève)
                nom = str(student_data[0]) if student_data[0] else ""
                prenom = str(student_data[1]) if student_data[1] else ""
                if not nom or not prenom:
                    print("⚠️ Nom ou prénom élève vide")
                    return
                    
                print(f"🎯 Sélection de l'élève: {prenom} {nom}")
                
                # Trouver l'élève dans les données par nom et prénom
                selected_student = None
                for eleve in self.eleves_data:
                    if len(eleve) >= 7 and str(eleve[1]) == nom and str(eleve[2]) == prenom:
                        _id, nom, prenom, genre, naissance, classe_id, classe_nom = eleve
                        age = calculate_age(naissance)
                        selected_student = {
                            'id': _id,
                            'nom': nom,
                            'prenom': prenom,
                            'genre': genre,
                            'naissance': naissance,
                            'age': age,
                            'classe': classe_nom or "Non assigné"
                        }
                        break
            
            if selected_student:
                self.selected_student = selected_student
                print(f"✅ Élève sélectionné: {selected_student['prenom']} {selected_student['nom']}")
                
                # Forcer la mise à jour visuelle de la sélection
                self.students_table.update()
                self.students_table.see(selected_row_index + 1)  # +1 car la première ligne est les en-têtes
                
                # Note: show_student_details_from_table n'existe plus dans cette vue
                # La sélection est juste stockée pour les boutons CRUD
            else:
                print(f"❌ Élève {prenom} {nom} non trouvé dans les données")
                
        except Exception as e:
            print(f"❌ Erreur lors de la sélection d'un élève: {e}")

    def _go_back_to_classes(self):
        """Retour à la vue des classes"""
        try:
            print("🔄 Retour à la vue des classes...")
            
            # Réinitialiser les variables de sélection
            self.selected_student = None
            self.current_classe_nom = None
            self.current_view = "classes"
            self.selected_classe = None
            self.selected_classe_id = None
            
            # Nettoyer complètement le contenu
            self.clear_main_content()
            
            # Attendre un peu pour que la destruction soit complète
            self.after(100, self._recreate_dashboard_content)
            
            print("✅ Retour aux classes réussi")
        except Exception as e:
            print(f"❌ Erreur lors du retour aux classes: {e}")
            messagebox.showerror("Erreur", f"Erreur lors du retour: {str(e)}")
    
    def _recreate_dashboard_content(self):
        """Recrée le contenu du dashboard après nettoyage"""
        try:
            # Recréer les sections du dashboard (sans breadcrumb)
            self._create_header(self.main_content_frame)
            self._create_stats_cards(self.main_content_frame)
            self._create_chart_section(self.main_content_frame)
            
            # Rafraîchir les données
            self.load_eleves_data()
            graph_data = fetch_effectifs_par_classe(limit=50)
            self.update_chart(graph_data)
            
            print("✅ Contenu du dashboard recréé (sans breadcrumb)")
        except Exception as e:
            print(f"❌ Erreur lors de la recréation: {e}")

    def _edit_selected_student(self):
        """Modifier l'élève sélectionné"""
        if not self.selected_student:
            messagebox.showwarning("Aucune sélection", "Veuillez sélectionner un élève à modifier.")
            return
        
        try:
            print(f"✏️ Modification de l'élève: {self.selected_student['prenom']} {self.selected_student['nom']}")
            # Ouvrir le formulaire de modification
            self.formulaire_eleve("Modifier", self.selected_student)
            print("✅ Formulaire de modification ouvert")
        except Exception as e:
            print(f"❌ Erreur lors de la modification: {e}")
            messagebox.showerror("Erreur", f"Erreur lors de la modification: {str(e)}")

    def _delete_selected_student(self):
        """Supprimer l'élève sélectionné"""
        if not self.selected_student:
            messagebox.showwarning("Aucune sélection", "Veuillez sélectionner un élève à supprimer.")
            return
        
        try:
            print(f"🗑️ Suppression de l'élève: {self.selected_student['prenom']} {self.selected_student['nom']}")
            
            # Confirmation de suppression
            result = messagebox.askyesno(
                "Confirmation de suppression",
                f"Êtes-vous sûr de vouloir supprimer l'élève {self.selected_student['prenom']} {self.selected_student['nom']} ?\n\nCette action est irréversible."
            )
            
            if result:
                # Supprimer l'élève de la base de données
                conn = get_db_connection()
                cursor = conn.cursor()
                cursor.execute("DELETE FROM eleves WHERE id_eleve = ?", (self.selected_student['id'],))
                
                if cursor.rowcount > 0:
                    conn.commit()
                    conn.close()
                    
                    messagebox.showinfo("Succès", "Élève supprimé avec succès.")
                    print("✅ Élève supprimé de la base de données")
                    
                    # Réinitialiser la sélection
                    self.selected_student = None
                    
                    # Rafraîchir la vue
                    self.show_students_list()
                    print("✅ Vue rafraîchie après suppression")
                else:
                    conn.close()
                    messagebox.showerror("Erreur", "Aucun élève n'a été supprimé.")
                
        except Exception as e:
            print(f"❌ Erreur lors de la suppression: {e}")
            messagebox.showerror("Erreur", f"Erreur lors de la suppression: {str(e)}")

    def _export_students(self):
        """Exporter la liste des élèves"""
        try:
            if not self.eleves_data:
                messagebox.showwarning("Aucune donnée", "Aucun élève à exporter.")
                return
            
            print(f"📊 Export de {len(self.eleves_data)} élèves...")
            
            # Demander le nom du fichier
            filename = filedialog.asksaveasfilename(
                defaultextension=".csv",
                filetypes=[("Fichiers CSV", "*.csv"), ("Tous les fichiers", "*.*")],
                title="Exporter la liste des élèves"
            )
            
            if filename:
                import csv
                with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
                    writer = csv.writer(csvfile)
                    # En-têtes
                    writer.writerow(['ID', 'Nom', 'Prénom', 'Genre', 'Date de naissance', 'Classe'])
                    
                    # Données
                    for eleve in self.eleves_data:
                        if len(eleve) >= 7:
                            writer.writerow(eleve[:6])  # Exclure classe_nom dupliqué
                
                messagebox.showinfo("Succès", f"Élèves exportés vers {filename}")
                print(f"✅ Export réussi: {len(self.eleves_data)} élèves vers {filename}")
                
        except Exception as e:
            print(f"❌ Erreur lors de l'export: {e}")
            messagebox.showerror("Erreur", f"Erreur lors de l'export: {str(e)}")

    def display_students_list(self, eleves_to_display):
        """Affiche les élèves sous forme de liste cliquable comme la vue des salles"""
        for w in self.students_list_frame.winfo_children():
            w.destroy()

        if not eleves_to_display:
            # Message d'état vide
            empty_frame = ctk.CTkFrame(self.students_list_frame, fg_color="transparent")
            empty_frame.pack(expand=True, fill="both", pady=20)
            
            empty_label = ctk.CTkLabel(empty_frame, text="Aucun élève trouvé",
                                      font=("Segoe UI", 14, "bold"), text_color=TEXT_SECONDARY)
            empty_label.pack(pady=10)
            
            self.show_empty_details()
            return

        # Afficher les élèves avec design moderne
        for i, eleve in enumerate(eleves_to_display):
            if len(eleve) >= 7:
                _id, nom, prenom, genre, naissance, classe_id, classe_nom = eleve
                age = calculate_age(naissance)
                
                # Créer l'élément de liste pour l'élève
                student_item_frame = StudentListItem(self.students_list_frame, {
                    'id': _id,
                    'nom': nom,
                    'prenom': prenom,
                    'genre': genre,
                    'naissance': naissance,
                    'age': age,
                    'classe': classe_nom or "Non assigné"
                }, self.show_student_details)
                student_item_frame.pack(fill="x", padx=3, pady=(3 if i == 0 else 1, 1))

    def show_empty_details(self):
        """Affiche le panneau de détails vide"""
        for w in self.student_details_panel.winfo_children():
            w.destroy()
            
        empty_frame = ctk.CTkFrame(self.student_details_panel, fg_color="transparent")
        empty_frame.pack(expand=True, fill="both", pady=50)
        
        empty_label = ctk.CTkLabel(empty_frame, text="Sélectionnez un élève",
                                  font=("Segoe UI", 16, "bold"), text_color=TEXT_SECONDARY)
        empty_label.pack(pady=20)
        
        empty_subtitle = ctk.CTkLabel(empty_frame, text="pour voir ses informations détaillées",
                                     font=("Segoe UI", 12), text_color=TEXT_SECONDARY)
        empty_subtitle.pack()

    def show_student_details(self, student_data, item_frame):
        """Affiche les détails d'un élève sélectionné"""
        self.selected_student = student_data

        if self.selected_student_frame:
            self.selected_student_frame.deselect()
        self.selected_student_frame = item_frame
        self.selected_student_frame.select()

        # Effacer le contenu du panneau de détails
        for w in self.student_details_panel.winfo_children():
            w.destroy()

        details_frame = ctk.CTkFrame(self.student_details_panel, fg_color="transparent")
        details_frame.pack(fill="both", expand=True, padx=8, pady=8)

        # Titre avec nom complet et design premium amélioré
        title_container = ctk.CTkFrame(details_frame, fg_color=BG_SIDEBAR, corner_radius=15, 
                                     border_width=2, border_color=ACCENT_BLUE)
        title_container.pack(fill="x", pady=(0, 8))
        
        # Container interne pour le titre avec gradient effect
        title_inner = ctk.CTkFrame(title_container, fg_color="transparent")
        title_inner.pack(fill="x", padx=15, pady=12)
        
        full_name = f"{student_data['prenom']} {student_data['nom']}"
        title_label = ctk.CTkLabel(title_inner, text=full_name, 
                                  font=("Segoe UI", 20, "bold"), text_color=TEXT_PRIMARY)
        title_label.pack(side="left")
        
        # Badge de statut à droite
        status_badge = ctk.CTkFrame(title_inner, fg_color=ACCENT_BLUE, corner_radius=20)
        status_badge.pack(side="right")
        
        status_label = ctk.CTkLabel(status_badge, text="ACTIF", 
                                  font=("Segoe UI", 10, "bold"), text_color="white")
        status_label.pack(padx=12, pady=4)

        # Détails de l'élève avec design premium amélioré
        details_card = ctk.CTkFrame(details_frame, fg_color=BG_SIDEBAR, corner_radius=15, 
                                   border_width=1, border_color=BORDER_COLOR)
        details_card.pack(fill="both", expand=True, pady=(0, 8))

        def create_detail_row(parent, label, value, icon_name=None):
            # Container principal ultra compact
            frame = ctk.CTkFrame(parent, fg_color="transparent", corner_radius=6)
            frame.pack(fill="x", pady=1, padx=2)
            
            # Container pour l'icône et le label ultra compact
            label_container = ctk.CTkFrame(frame, fg_color=BG_CARD, corner_radius=6)
            label_container.pack(side="left", padx=(0, 2), pady=1)
            
            # Icône si fournie ultra compacte
            if icon_name:
                try:
                    icon_path = os.path.join(os.path.dirname(__file__), '..', '..', '..', '..', '..', 'resources', 'icons', f"{icon_name}.png")
                    icon = ctk.CTkImage(Image.open(icon_path), size=(12, 12))
                    icon_label = ctk.CTkLabel(label_container, text="", image=icon, fg_color="transparent")
                    icon_label.pack(side="left", padx=(4, 2))
                except:
                    pass
            
            ctk.CTkLabel(label_container, text=f"{label} :", font=("Segoe UI", 11, "bold"), 
                        text_color=TEXT_SECONDARY, anchor="w").pack(side="left", padx=(0, 2))
            
            # Valeur ultra compacte
            value_frame = ctk.CTkFrame(frame, fg_color=BG_MAIN, corner_radius=6, 
                                     border_width=1, border_color=BORDER_COLOR)
            value_frame.pack(side="right", fill="x", expand=True, padx=(2, 0), pady=1)
            
            ctk.CTkLabel(value_frame, text=str(value), font=("Segoe UI", 11), 
                        text_color=TEXT_PRIMARY, anchor="w").pack(padx=6, pady=3)

        # Container principal avec layout en deux colonnes et marges ultra réduites
        main_content = ctk.CTkFrame(details_card, fg_color="transparent")
        main_content.pack(fill="both", expand=True, padx=4, pady=4)
        
        # Configuration des colonnes
        main_content.grid_columnconfigure(0, weight=1)
        main_content.grid_columnconfigure(1, weight=1)
        
        # Colonne gauche - Informations personnelles et scolaires avec marges ultra réduites
        left_column = ctk.CTkFrame(main_content, fg_color=BG_CARD, corner_radius=10, 
                                 border_width=1, border_color=BORDER_COLOR)
        left_column.grid(row=0, column=0, sticky="nsew", padx=(0, 2))
        
        # Informations personnelles
        personal_section = ctk.CTkFrame(left_column, fg_color="transparent")
        personal_section.pack(fill="x", pady=(6, 4))
        
        section_title = ctk.CTkLabel(personal_section, text="📋 Informations Personnelles", 
                                   font=("Segoe UI", 13, "bold"), text_color=TEXT_ACCENT)
        section_title.pack(anchor="w", pady=(0, 4))
        
        create_detail_row(personal_section, "Nom", student_data['nom'], "person")
        create_detail_row(personal_section, "Prénom", student_data['prenom'], "person")
        create_detail_row(personal_section, "Genre", student_data['genre'], "person")
        create_detail_row(personal_section, "Date de naissance", student_data['naissance'], "calendar")
        create_detail_row(personal_section, "Âge", f"{student_data['age']} ans", "calendar")
        
        # Informations scolaires
        school_section = ctk.CTkFrame(left_column, fg_color="transparent")
        school_section.pack(fill="x", pady=(4, 6))
        
        section_title2 = ctk.CTkLabel(school_section, text="🎓 Informations Scolaires", 
                                     font=("Segoe UI", 13, "bold"), text_color=TEXT_ACCENT)
        section_title2.pack(anchor="w", pady=(0, 4))
        
        create_detail_row(school_section, "Classe", student_data['classe'], "class")
        create_detail_row(school_section, "Statut", "Actif", "check")
        
        # Colonne droite - Informations familiales et autres avec marges ultra réduites
        right_column = ctk.CTkFrame(main_content, fg_color=BG_CARD, corner_radius=10, 
                                  border_width=1, border_color=BORDER_COLOR)
        right_column.grid(row=0, column=1, sticky="nsew", padx=(2, 0))
        
        # Informations familiales
        family_section = ctk.CTkFrame(right_column, fg_color="transparent")
        family_section.pack(fill="x", pady=(6, 4))
        
        section_title3 = ctk.CTkLabel(family_section, text="👨‍👩‍👧‍👦 Informations Familiales", 
                                     font=("Segoe UI", 13, "bold"), text_color=TEXT_ACCENT)
        section_title3.pack(anchor="w", pady=(0, 4))
        
        create_detail_row(family_section, "Nom du père", "Non renseigné", "person")
        create_detail_row(family_section, "Nom de la mère", "Non renseigné", "person")
        create_detail_row(family_section, "Téléphone", "Non renseigné", "phone")
        create_detail_row(family_section, "Adresse", "Non renseignée", "location")
        
        # Informations supplémentaires
        additional_section = ctk.CTkFrame(right_column, fg_color="transparent")
        additional_section.pack(fill="x", pady=(4, 6))
        
        section_title4 = ctk.CTkLabel(additional_section, text="📊 Informations Supplémentaires", 
                                     font=("Segoe UI", 13, "bold"), text_color=TEXT_ACCENT)
        section_title4.pack(anchor="w", pady=(0, 4))
        
        create_detail_row(additional_section, "ID Élève", student_data['id'], "id")
        create_detail_row(additional_section, "Date d'inscription", "2024-01-01", "calendar")
        create_detail_row(additional_section, "Moyenne générale", "15.5/20", "chart")
        create_detail_row(additional_section, "Absences", "2 jours", "warning")

        # Boutons d'action avec design premium amélioré
        btn_frame = ctk.CTkFrame(details_frame, fg_color="transparent")
        btn_frame.pack(pady=8)

        # Bouton Modifier avec design premium
        edit_btn = ctk.CTkButton(btn_frame, text="Modifier", 
                                font=("Segoe UI", 13, "bold"),
                                fg_color=ACCENT_BLUE, hover_color=HOVER_WARNING, 
                                text_color="white",
                                command=lambda: self.modifier_eleve(student_data['id']), 
                                height=45, width=140,
                                border_width=2, border_color=BORDER_COLOR,
                                corner_radius=15)
        edit_btn.pack(side="left", padx=(0, 12))

        # Bouton Supprimer avec design premium
        delete_btn = ctk.CTkButton(btn_frame, text="Supprimer", 
                                 font=("Segoe UI", 13, "bold"),
                                 fg_color="#E74C3C", hover_color=HOVER_ERROR, 
                                 text_color="white",
                                 command=lambda: self.supprimer_eleve(student_data['id']), 
                                 height=45, width=140,
                                 border_width=2, border_color=BORDER_COLOR,
                                 corner_radius=15)
        delete_btn.pack(side="left")

    def create_student_card(self, parent, index, eleve_data):
        """Crée une carte individuelle élégante pour un élève avec design premium"""
        row = index // 4
        col = index % 4
        
        # Carte principale avec design premium
        card = ctk.CTkFrame(parent, fg_color=BG_CARD, corner_radius=20, border_width=2, border_color=BORDER_COLOR)
        card.grid(row=row, column=col, padx=4, pady=4, sticky="nsew")
        
        # Effet hover avec animation
        def on_enter(event):
            card.configure(fg_color=BG_CARD_HOVER, border_color=ACCENT_BLUE, border_width=3)
            
        def on_leave(event):
            card.configure(fg_color=BG_CARD, border_color=BORDER_COLOR, border_width=2)
            
        card.bind("<Enter>", on_enter)
        card.bind("<Leave>", on_leave)
        
        # En-tête de la carte avec gradient et icônes
        header_frame = ctk.CTkFrame(card, fg_color=ACCENT_BLUE, corner_radius=18)
        header_frame.pack(fill="x", padx=12, pady=(12, 8))
        
        # Contenu de l'en-tête
        header_content = ctk.CTkFrame(header_frame, fg_color="transparent")
        header_content.pack(fill="x", padx=15, pady=12)
        
        # Avatar avec icône de personne
        avatar_container = ctk.CTkFrame(header_content, fg_color=WHITE, corner_radius=30, width=60, height=60)
        avatar_container.pack(side="left")
        avatar_container.pack_propagate(False)
        
        # Icône de personne dans l'avatar
        person_icon = get_icon("person", (24, 24))
        if person_icon:
            avatar_label = ctk.CTkLabel(avatar_container, text="", image=person_icon, text_color=ACCENT_BLUE)
            avatar_label._imgref = person_icon
            avatar_label.pack(expand=True)
        else:
            # Fallback avec initiales
            initiales = f"{eleve_data['prenom'][0]}{eleve_data['nom'][0]}".upper()
            avatar_label = ctk.CTkLabel(avatar_container, text=initiales, font=("Segoe UI", 14, "bold"), text_color=ACCENT_BLUE)
            avatar_label.pack(expand=True)
        
        # Informations principales avec icônes
        info_frame = ctk.CTkFrame(header_content, fg_color="transparent")
        info_frame.pack(side="left", fill="x", expand=True, padx=(4, 0))
        
        # Nom complet avec icône utilisateur
        nom_frame = ctk.CTkFrame(info_frame, fg_color="transparent")
        nom_frame.pack(fill="x")
        
        user_icon = get_icon("person", (16, 16))
        if user_icon:
            user_label = ctk.CTkLabel(nom_frame, text="", image=user_icon, text_color=WHITE)
            user_label._imgref = user_icon
            user_label.pack(side="left")
        
        nom_complet = f"{eleve_data['prenom']} {eleve_data['nom']}"
        nom_label = ctk.CTkLabel(nom_frame, text=nom_complet, font=("Segoe UI", 16, "bold"), text_color=WHITE)
        nom_label.pack(side="left", padx=(8, 0))
        
        # Classe et âge avec icône de groupe
        classe_frame = ctk.CTkFrame(info_frame, fg_color="transparent")
        classe_frame.pack(fill="x", pady=(5, 0))
        
        group_icon = get_icon("group", (14, 14))
        if group_icon:
            group_label = ctk.CTkLabel(classe_frame, text="", image=group_icon, text_color=WHITE)
            group_label._imgref = group_icon
            group_label.pack(side="left")
        
        classe_age = f"{eleve_data['classe']} • {eleve_data['age']} ans"
        classe_label = ctk.CTkLabel(classe_frame, text=classe_age, font=("Segoe UI", 12), text_color=WHITE)
        classe_label.pack(side="left", padx=(8, 0))
        
        # Corps de la carte avec informations détaillées
        body_frame = ctk.CTkFrame(card, fg_color="transparent")
        body_frame.pack(fill="x", padx=12, pady=(0, 12))
        
        # Section des informations avec design moderne
        info_section = ctk.CTkFrame(body_frame, fg_color=BG_CARD_HOVER, corner_radius=12)
        info_section.pack(fill="x", pady=(0, 4))
        
        # Genre avec icône et statut
        genre_statut_frame = ctk.CTkFrame(info_section, fg_color="transparent")
        genre_statut_frame.pack(fill="x", padx=12, pady=10)
        
        # Genre avec icône
        genre_container = ctk.CTkFrame(genre_statut_frame, fg_color="transparent")
        genre_container.pack(side="left")
        
        # Icône genre (homme/femme)
        gender_icon = "👨" if eleve_data['genre'] == 'M' else "👩"
        genre_label = ctk.CTkLabel(genre_container, text=f"{gender_icon} {eleve_data['genre']}", 
                                 font=("Segoe UI", 12, "bold"), text_color=TEXT_PRIMARY)
        genre_label.pack(side="left")
        
        # Statut avec icône et couleur
        statut_container = ctk.CTkFrame(genre_statut_frame, fg_color="transparent")
        statut_container.pack(side="right")
        
        # Icône de statut
        status_icon = get_icon("check_circle", (14, 14)) if eleve_data['statut'] == 'Actif' else get_icon("close", (14, 14))
        if status_icon:
            status_label = ctk.CTkLabel(statut_container, text="", image=status_icon, text_color=SUCCESS_GREEN if eleve_data['statut'] == 'Actif' else ERROR_RED)
            status_label._imgref = status_icon
            status_label.pack(side="left")
        
        statut_color = SUCCESS_GREEN if eleve_data['statut'] == 'Actif' else ERROR_RED
        statut_text = ctk.CTkLabel(statut_container, text=eleve_data['statut'], 
                                  font=("Segoe UI", 11, "bold"), text_color=statut_color)
        statut_text.pack(side="left", padx=(5, 0))
        
        # Date de naissance avec icône calendrier
        naissance_container = ctk.CTkFrame(info_section, fg_color="transparent")
        naissance_container.pack(fill="x", padx=12, pady=(0, 4))
        
        calendar_icon = get_icon("calendar", (14, 14))
        if calendar_icon:
            calendar_label = ctk.CTkLabel(naissance_container, text="", image=calendar_icon, text_color=TEXT_SECONDARY)
            calendar_label._imgref = calendar_icon
            calendar_label.pack(side="left")
        
        naissance_label = ctk.CTkLabel(naissance_container, text=eleve_data['naissance'], 
                                      font=("Segoe UI", 11), text_color=TEXT_SECONDARY)
        naissance_label.pack(side="left", padx=(8, 0))
        
        # Boutons d'action avec icônes et design premium
        actions_frame = ctk.CTkFrame(card, fg_color="transparent")
        actions_frame.pack(fill="x", padx=12, pady=(0, 12))
        
        # Bouton Modifier avec icône
        edit_icon = get_icon("edit", (16, 16))
        edit_btn = ctk.CTkButton(actions_frame, text="Modifier", width=85, height=32,
                                fg_color=ACCENT_BLUE, hover_color=BORDER_ACCENT,
                                font=("Segoe UI", 10, "bold"), text_color=WHITE,
                                image=edit_icon if edit_icon else None,
                                command=lambda: self.edit_student_from_card(eleve_data))
        if edit_icon:
            edit_btn._imgref = edit_icon
        edit_btn.pack(side="left", padx=(0, 6))
        
        # Bouton Détails avec icône
        details_icon = get_icon("detail", (16, 16))
        details_btn = ctk.CTkButton(actions_frame, text="Détails", width=85, height=32,
                                   fg_color=WARNING_ORANGE, hover_color="#d97706",
                                   font=("Segoe UI", 10, "bold"), text_color=WHITE,
                                   image=details_icon if details_icon else None,
                                   command=lambda: self.show_student_details_from_card(eleve_data))
        if details_icon:
            details_btn._imgref = details_icon
        details_btn.pack(side="left", padx=(0, 6))
        
        # Bouton Supprimer avec icône
        delete_icon = get_icon("delete", (16, 16))
        delete_btn = ctk.CTkButton(actions_frame, text="Supprimer", width=85, height=32,
                                  fg_color=ERROR_RED, hover_color="#dc2626",
                                  font=("Segoe UI", 10, "bold"), text_color=WHITE,
                                  image=delete_icon if delete_icon else None,
                                  command=lambda: self.delete_student_from_card(eleve_data))
        if delete_icon:
            delete_btn._imgref = delete_icon
        delete_btn.pack(side="right")
        
        return card

    def edit_student_from_card(self, eleve_data):
        """Ouvre le formulaire de modification depuis une carte"""
        self.formulaire_eleve(mode="Modifier", eleves=eleve_data)

    def show_student_details_from_card(self, eleve_data):
        """Affiche les détails d'un élève depuis une carte avec design premium"""
        # Créer la fenêtre de détails
        details_window = ctk.CTkToplevel(self)
        details_window.title(f"Détails - {eleve_data['nom']} {eleve_data['prenom']}")
        details_window.geometry("700x600")
        details_window.minsize(600, 500)
        details_window.transient(self.winfo_toplevel())
        details_window.grab_set()
        details_window.configure(fg_color=BG_MAIN)
        
        # Centrer la fenêtre
        self._center_window(details_window)
        
        # Contenu principal
        main_container = ctk.CTkFrame(details_window, fg_color="transparent")
        main_container.pack(fill="both", expand=True, padx=4, pady=4)
        
        # En-tête avec avatar et gradient
        header = ctk.CTkFrame(main_container, fg_color=ACCENT_BLUE, corner_radius=20)
        header.pack(fill="x", pady=(0, 4))
        
        header_content = ctk.CTkFrame(header, fg_color="transparent")
        header_content.pack(fill="x", padx=25, pady=25)
        
        # Avatar grand avec icône
        avatar_frame = ctk.CTkFrame(header_content, fg_color=WHITE, corner_radius=50, width=100, height=100)
        avatar_frame.pack(side="left")
        avatar_frame.pack_propagate(False)
        
        # Icône de personne dans l'avatar
        person_icon = get_icon("person", (40, 40))
        if person_icon:
            avatar_label = ctk.CTkLabel(avatar_frame, text="", image=person_icon, text_color=ACCENT_BLUE)
            avatar_label._imgref = person_icon
            avatar_label.pack(expand=True)
        else:
            # Fallback avec initiales
            initiales = f"{eleve_data['prenom'][0]}{eleve_data['nom'][0]}".upper()
            avatar_label = ctk.CTkLabel(avatar_frame, text=initiales, font=("Segoe UI", 28, "bold"), text_color=ACCENT_BLUE)
            avatar_label.pack(expand=True)
        
        # Informations principales avec icônes
        info_frame = ctk.CTkFrame(header_content, fg_color="transparent")
        info_frame.pack(side="left", fill="x", expand=True, padx=(25, 0))
        
        # Nom complet avec icône
        nom_frame = ctk.CTkFrame(info_frame, fg_color="transparent")
        nom_frame.pack(fill="x")
        
        user_icon = get_icon("person", (20, 20))
        if user_icon:
            user_label = ctk.CTkLabel(nom_frame, text="", image=user_icon, text_color=WHITE)
            user_label._imgref = user_icon
            user_label.pack(side="left")
        
        nom_complet = f"{eleve_data['prenom']} {eleve_data['nom']}"
        nom_label = ctk.CTkLabel(nom_frame, text=nom_complet, font=("Segoe UI", 28, "bold"), text_color=WHITE)
        nom_label.pack(side="left", padx=(4, 0))
        
        # Classe et âge avec icône
        classe_frame = ctk.CTkFrame(info_frame, fg_color="transparent")
        classe_frame.pack(fill="x", pady=(10, 0))
        
        group_icon = get_icon("group", (18, 18))
        if group_icon:
            group_label = ctk.CTkLabel(classe_frame, text="", image=group_icon, text_color=WHITE)
            group_label._imgref = group_icon
            group_label.pack(side="left")
        
        classe_age = f"{eleve_data['classe']} • {eleve_data['age']} ans"
        classe_label = ctk.CTkLabel(classe_frame, text=classe_age, font=("Segoe UI", 16), text_color=WHITE)
        classe_label.pack(side="left", padx=(4, 0))
        
        # Corps des détails avec design moderne
        body = ctk.CTkScrollableFrame(main_container, fg_color=BG_CARD, corner_radius=15)
        body.pack(fill="both", expand=True, pady=(0, 4))
        
        # Section informations personnelles
        info_personnelles = ctk.CTkFrame(body, fg_color=BG_CARD_HOVER, corner_radius=12)
        info_personnelles.pack(fill="x", pady=15, padx=15)
        
        # Titre de section avec icône
        title_frame = ctk.CTkFrame(info_personnelles, fg_color="transparent")
        title_frame.pack(fill="x", padx=20, pady=(20, 10))
        
        detail_icon = get_icon("detail", (20, 20))
        if detail_icon:
            detail_label = ctk.CTkLabel(title_frame, text="", image=detail_icon, text_color=TEXT_PRIMARY)
            detail_label._imgref = detail_icon
            detail_label.pack(side="left")
        
        ctk.CTkLabel(title_frame, text="Informations Personnelles", 
                    text_color=TEXT_PRIMARY, font=("Segoe UI", 18, "bold")).pack(side="left", padx=(4, 0))
        
        # Grille d'informations avec icônes
        info_grid = ctk.CTkFrame(info_personnelles, fg_color="transparent")
        info_grid.pack(fill="x", padx=20, pady=(0, 4))
        
        # Informations avec icônes
        infos = [
            ("Matricule", eleve_data.get('matricule', 'Non renseigné'), "assignment"),
            ("Genre", eleve_data['genre'], "person"),
            ("Date de naissance", eleve_data['naissance'], "calendar"),
            ("Classe", eleve_data['classe'], "class"),
            ("Statut", eleve_data['statut'], "check_circle" if eleve_data['statut'] == 'Actif' else "close")
        ]
        
        for i, (label, value, icon_name) in enumerate(infos):
            row = i // 2
            col = i % 2
            
            # Conteneur pour chaque information
            info_container = ctk.CTkFrame(info_grid, fg_color="transparent")
            info_container.grid(row=row, column=col, sticky="ew", padx=4, pady=4)
            
            # Icône
            icon = get_icon(icon_name, (16, 16))
            if icon:
                icon_label = ctk.CTkLabel(info_container, text="", image=icon, text_color=TEXT_SECONDARY)
                icon_label._imgref = icon
                icon_label.pack(side="left")
            
            # Label
            label_widget = ctk.CTkLabel(info_container, text=label, text_color=TEXT_SECONDARY, 
                                      font=("Segoe UI", 12))
            label_widget.pack(side="left", padx=(8, 0))
            
            # Valeur
            value_color = SUCCESS_GREEN if label == "Statut" and value == "Actif" else TEXT_PRIMARY
            value_widget = ctk.CTkLabel(info_container, text=value, text_color=value_color, 
                                       font=("Segoe UI", 12, "bold"))
            value_widget.pack(side="right")
        
        # Configuration de la grille
        info_grid.grid_columnconfigure(0, weight=1)
        info_grid.grid_columnconfigure(1, weight=1)
        
        # Boutons d'action
        footer = ctk.CTkFrame(main_container, fg_color=BG_CARD, corner_radius=12)
        footer.pack(fill="x")
        
        buttons_frame = ctk.CTkFrame(footer, fg_color="transparent")
        buttons_frame.pack(side="right", padx=20, pady=15)
        
        # Bouton Modifier
        edit_icon = get_icon("edit", (18, 18))
        edit_btn = ctk.CTkButton(buttons_frame, text="Modifier", width=100, height=40,
                                fg_color=ACCENT_BLUE, hover_color=BORDER_ACCENT,
                                font=("Segoe UI", 12, "bold"), text_color=WHITE,
                                image=edit_icon if edit_icon else None,
                                command=lambda: [self.edit_student_from_card(eleve_data), details_window.destroy()])
        if edit_icon:
            edit_btn._imgref = edit_icon
        edit_btn.pack(side="left", padx=(0, 2))
        
        # Bouton Fermer
        close_icon = get_icon("close", (18, 18))
        close_btn = ctk.CTkButton(buttons_frame, text="Fermer", width=100, height=40,
                                 fg_color=ERROR_RED, hover_color="#dc2626",
                                 font=("Segoe UI", 12, "bold"), text_color=WHITE,
                                 image=close_icon if close_icon else None,
                                 command=details_window.destroy)
        if close_icon:
            close_btn._imgref = close_icon
        close_btn.pack(side="left")

    def delete_student_from_card(self, eleve_data):
        """Supprime un élève depuis une carte"""
        result = messagebox.askyesno("Confirmation", 
                                   f"Êtes-vous sûr de vouloir supprimer l'élève {eleve_data['prenom']} {eleve_data['nom']} ?")
        if result:
            try:
                conn = get_db_connection()
                cursor = conn.cursor()
                cursor.execute("DELETE FROM eleves WHERE id_eleve = ?", (eleve_data['id'],))
                conn.commit()
                conn.close()
                messagebox.showinfo("Succès", "Élève supprimé avec succès.")
                self.refresh_dashboard()
            except Exception as e:
                messagebox.showerror("Erreur", f"Erreur lors de la suppression : {e}")

    def on_students_table_select(self, event):
        """Gère la sélection d'un élève dans le tableau"""
        try:
            selected_items = self.students_table.selection()
            if selected_items:
                selected_item = selected_items[0]
                values = self.students_table.item(selected_item)['values']
        except Exception as e:
            print(f"⚠️ Erreur sélection tableau: {e}")
            return

    def on_students_table_double_click(self, event):
        """Gère le double-clic sur un élève pour le modifier"""
        try:
            selected_items = self.students_table.selection()
            if selected_items:
                selected_item = selected_items[0]
                values = self.students_table.item(selected_item)['values']
                
                if values and len(values) >= 6:
                    # Trouver l'index de la ligne sélectionnée
                    all_items = self.students_table.get_children()
                    row_index = all_items.index(selected_item)
                    
                    # Récupérer les données de l'élève depuis self.eleves_data
                    if hasattr(self, 'eleves_data') and row_index < len(self.eleves_data):
                        eleve_data = self.eleves_data[row_index]
                        _id, nom, prenom, genre, naissance, classe_id, classe_nom = eleve_data
                        
                        # Ouvrir le formulaire de modification
                        self.formulaire_eleve(mode="Modifier", eleves={
                            'id': _id,
                            'nom': nom,
                            'prenom': prenom,
                            'genre': genre,
                            'date_naissance': naissance,
                            'classe': classe_nom,
                            'statut': 'Actif'
                        })
        except Exception as e:
            print(f"⚠️ Erreur double-clic tableau: {e}")

    def refresh_stats_for_classe(self, classe_id):
        """Met à jour les statistiques pour une classes spécifique"""
        try:
            # Utiliser la fonction refresh_stats qui gère correctement la recréation des cartes
            self.refresh_stats()
        except Exception as e:
            print(f"⚠️ Erreur mise à jour stats pour classes: {e}")

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

        badge = ctk.CTkFrame(header, fg_color=BG_CARD_HOVER, corner_radius=999, width=30, height=30, border_width=1, border_color=BORDER_COLOR)
        badge.pack_propagate(False); badge.pack(side="left")

        icon_img = get_icon(ICON_MAP.get(icon_key, "home"), (14, 14))
        if icon_img:
            lbl = ctk.CTkLabel(badge, text="", image=icon_img, text_color=color)
            lbl._imgref = icon_img
            lbl.pack(expand=True)

        ctk.CTkLabel(header, text=title, font=FONT_SMALL, text_color=TEXT_SECONDARY)\
            .pack(side="left", padx=PADDING_SMALL)

        # Créer les labels et les stocker dans les listes
        value_label = ctk.CTkLabel(wrap, text=str(value), font=("Segoe UI", 22, "bold"), text_color=TEXT_PRIMARY)
        value_label.pack(anchor="w", padx=PADDING_SMALL)
        
        subtext_label = ctk.CTkLabel(wrap, text="Mise à jour en temps réel", font=("Segoe UI", 11), text_color=TEXT_SECONDARY)
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
            parent, fg_color=BG_CARD,
            corner_radius=10, border_width=1, border_color=BORDER_COLOR
        )
        self.chart_container.pack(fill="both", expand=True, pady=(0, 0))
        
        # Header du graphique avec icône et titre
        chart_header = ctk.CTkFrame(self.chart_container, fg_color="transparent")
        chart_header.pack(fill="x", padx=15, pady=(20, 10))
        
        # Titre avec icône
        title_frame = ctk.CTkFrame(chart_header, fg_color="transparent")
        title_frame.pack(anchor="w")
        
        # Icône pour le graphique
        chart_icon = get_icon("stats", (28, 28))
        if chart_icon:
            icon_label = ctk.CTkLabel(title_frame, text="", image=chart_icon, text_color=TEXT_ACCENT)
            icon_label._imgref = chart_icon
            icon_label.pack(side="left", padx=(0, 4))
        
        # Titre principal
        ctk.CTkLabel(title_frame, text="Répartition des Élèves par Classe", font=("Segoe UI", 26, "bold"), text_color=TEXT_PRIMARY).pack(side="left")
        
        # Description avec plus d'espace
        ctk.CTkLabel(self.chart_container, text="Distribution des effectifs par classes", font=("Segoe UI", 13), text_color=TEXT_SECONDARY).pack(padx=15, pady=(0, 30), anchor="w")

    def _create_sidebar(self):
        """Sidebar magnifique avec thème global et design premium"""
        sidebar = ctk.CTkFrame(
            self, fg_color=BG_SIDEBAR,
            width=180, 
            corner_radius=20, border_width=2, border_color=BORDER_COLOR
        )
        sidebar.grid(row=0, column=1, sticky="nsew", padx=(0, PADDING_SMALL), pady=(0, 0))
        sidebar.grid_propagate(False)
        sidebar.grid_rowconfigure(1, weight=1)

        # En-tête premium de la sidebar
        sidebar_header = ctk.CTkFrame(sidebar, fg_color="transparent")
        sidebar_header.pack(fill="x", pady=(2, MARGIN_SMALL), padx=PADDING_SMALL)
        
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
        
        ctk.CTkLabel(title_frame, text="Classes", font=FONT_SUBTITLE, text_color=TEXT_ACCENT).pack(anchor="w")
        ctk.CTkLabel(title_frame, text="Sélectionnez une classes", font=FONT_SMALL, text_color=TEXT_SECONDARY).pack(anchor="w", pady=(MARGIN_SMALL, 0))
        
        # Séparateur élégant avec gradient
        separator_container = ctk.CTkFrame(sidebar, fg_color="transparent")
        separator_container.pack(fill="x", padx=PADDING_SMALL, pady=(0, MARGIN_SMALL))
        
        separator = ctk.CTkFrame(separator_container, height=2, fg_color=TEXT_ACCENT, corner_radius=1)
        separator.pack(fill="x")

        # Conteneur des boutons de classes avec scroll élégant
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
            self.classe_btns_frame, text="Tous les élèves", font=FONT_BUTTON, fg_color="transparent", text_color=TEXT_ACCENT, hover_color=BG_CARD_HOVER,
            command=lambda: self.update_dashboard_for_classe(None),
            corner_radius=15, height=45,
            image=get_icon("group", (18, 18)), border_width=2, border_color=TEXT_ACCENT
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
                text="Aucune classes trouvée", text_color=TEXT_MUTED, font=FONT_SECONDARY
            )
            no_classes_label.pack(pady=PADDING_MEDIUM)
        else:
            # Organiser les classes par niveau
            classes_par_niveau = {}
            for classe in classes:
                if len(classe) >= 2:
                    nom = classe[0]  # nom_classe
                    niveau = classe[1]  # niveau
                    if niveau not in classes_par_niveau:
                        classes_par_niveau[niveau] = []
                    classes_par_niveau[niveau].append(nom)
            
            # Créer les sections dans l'ordre logique du système français
            niveaux_order = ["Primaire", "Collège", "Lycée"]
            
            for niveau in niveaux_order:
                if niveau in classes_par_niveau:
                    # Titre de section
                    section_title = ctk.CTkLabel(
                        self.classe_btns_frame,
                        text=niveau, font=FONT_BUTTON, text_color=TEXT_ACCENT, fg_color="transparent"
                    )
                    section_title.pack(anchor="w", pady=(PADDING_MEDIUM, MARGIN_SMALL), padx=PADDING_SMALL)
                    
                    # Boutons des classes de cette section (triées par ordre logique)
                    classes_sorted = sorted(classes_par_niveau[niveau], key=lambda x: (
                        int(x.split('°')[0]) if '°' in x and x.split('°')[0].isdigit() else 999,
                        x
                    ))
                    for nom in classes_sorted:
                        btn = ctk.CTkButton(
                            self.classe_btns_frame, 
                            text=nom, font=FONT_SMALL, fg_color=BG_CARD, text_color=TEXT_PRIMARY, hover_color=BG_CARD_HOVER,
                            command=lambda c=nom: self.update_dashboard_for_classe(c),
                            corner_radius=10, 
                            height=35,
                            image=get_icon("group", (14, 14)), border_width=1, border_color=BORDER_COLOR
                        )
                        btn.pack(fill="x", pady=4, padx=PADDING_SMALL)
                        self.classe_btns.append((btn, nom))
        
        self.update_btn_states(self.selected_classe)

    def update_btn_states(self, classe_id):
        """Met à jour l'état des boutons de classes avec design premium"""
        for btn, cid in self.classe_btns:
            if classe_id == cid:
                # Classe sélectionnée - style accent
                btn.configure(fg_color=TEXT_ACCENT, text_color=BG_SIDEBAR, hover_color=HOVER_PRIMARY, border_color=TEXT_ACCENT, border_width=2)
            elif cid is None and classe_id is None:
                # "Tous les élèves" sélectionné - style accent
                btn.configure(fg_color=TEXT_ACCENT, text_color=BG_SIDEBAR, hover_color=HOVER_PRIMARY, border_color=TEXT_ACCENT, border_width=2)
            else:
                # Classe non sélectionnée - style normal
                btn.configure(fg_color=BG_CARD, text_color=TEXT_PRIMARY, hover_color=BG_CARD_HOVER, border_color=BORDER_COLOR, border_width=1)

    def update_dashboard_for_classe(self, classe_name):
        """Met à jour le dashboard pour une classes spécifique"""
        try:
            if classe_name is None:
                # Retour à la vue des classes
                self.show_classes_view()
                return
                
            # Convertir le nom de classes en ID si nécessaire
            classe_id = get_classe_id_by_name(classe_name)
            if classe_id is None:
                print(f"⚠️ Classe '{classe_name}' introuvable")
                return
            
            # Naviguer vers la vue des étudiants de cette classe
            self.show_students_view(classe_name, classe_id)
            
            print(f"✅ Navigation vers la classe: {classe_name} (ID: {classe_id})")
        except Exception as e:
            print(f"⚠️ Erreur navigation: {e}")

    def on_search_change(self, event=None):
        """Gère les changements dans la recherche"""
        self.search_term = self.search_var.get()
        self.current_page = 1  # Retour à la première page
        self.load_eleves_data()

    def load_eleves_data(self):
        """Charge les données des élèves avec pagination"""
        try:
            # Récupérer le nombre total d'élèves
            self.total_eleves = get_eleves_count(self.selected_classe_id, self.search_term)
            
            # Calculer le nombre total de pages
            self.total_pages = max(1, (self.total_eleves + self.page_size - 1) // self.page_size)
            
            # S'assurer que la page actuelle est valide
            if self.current_page > self.total_pages:
                self.current_page = self.total_pages
            
            # Charger les élèves de la page actuelle
            eleves_data = get_eleves_list(
                classe_id=self.selected_classe_id,
                search_term=self.search_term,
                page=self.current_page,
                page_size=self.page_size
            )
            
            # Mettre à jour l'affichage des élèves
            self.update_eleves_display(eleves_data)
            
            # Mettre à jour les contrôles de pagination
            self.update_pagination_controls()
            
        except Exception as e:
            print(f"⚠️ Erreur lors du chargement des données: {e}")

    def update_eleves_display(self, eleves_data):
        """Met à jour l'affichage de la liste des élèves"""
        # Cette méthode sera implémentée selon l'interface existante
        # Pour l'instant, on affiche juste les données dans la console
        print(f"📊 Affichage de {len(eleves_data)} élèves (page {self.current_page}/{self.total_pages})")
        for eleve in eleves_data[:5]:  # Afficher seulement les 5 premiers
            print(f"   - {eleve[2]} {eleve[1]} ({eleve[6] if len(eleve) > 6 else 'N/A'})")

    def update_pagination_controls(self):
        """Met à jour les contrôles de pagination"""
        # Cette méthode créera les boutons de pagination
        # Pour l'instant, on affiche juste les informations
        print(f"📄 Page {self.current_page} sur {self.total_pages} ({self.total_eleves} élèves au total)")

    def go_to_page(self, page):
        """Va à une page spécifique"""
        if 1 <= page <= self.total_pages:
            self.current_page = page
            self.load_eleves_data()

    def next_page(self):
        """Va à la page suivante"""
        if self.current_page < self.total_pages:
            self.go_to_page(self.current_page + 1)

    def previous_page(self):
        """Va à la page précédente"""
        if self.current_page > 1:
            self.go_to_page(self.current_page - 1)

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
                text="📊 Aucune donnée à afficher", text_color=TEXT_MUTED
            ).pack(pady=50)
            return

        # Filtrer les données non nulles
        filtered_data = [(name, count) for name, count in zip(cls_names, counts) if count > 0]
        if not filtered_data:
            ctk.CTkLabel(
                self.chart_container, 
                text="📊 Aucune donnée à afficher", text_color=TEXT_MUTED
            ).pack(pady=50)
            return

        chart_names = [x[0] for x in filtered_data]
        chart_counts = [x[1] for x in filtered_data]

        # Création du graphique en barres horizontales moderne
        fig = plt.Figure(figsize=(10, 6), dpi=100, facecolor=BG_CARD)
        ax = fig.add_subplot(111, facecolor=BG_CARD)
        
        # Couleurs du thème EduManager+
        colors = [
            ACCENT_BLUE, SUCCESS_GREEN, WARNING_ORANGE, ERROR_RED, 
            LIGHT_BLUE, PURPLE_ACCENT, EMERALD_ACCENT, CORAL_ACCENT,
            GOLD_ACCENT, SILVER_ACCENT, PINK_ACCENT, DARK_ACCENT_COOL,
            HOVER_SUCCESS, HOVER_WARNING, HOVER_ERROR, HOVER_INFO
        ]
        
        # Trier les données par effectif décroissant pour un meilleur affichage
        sorted_data = sorted(zip(chart_names, chart_counts), key=lambda x: x[1], reverse=True)
        chart_names, chart_counts = zip(*sorted_data)
        
        # Créer le graphique en barres horizontales
        y_pos = range(len(chart_names))
        bars = ax.barh(y_pos, chart_counts, color=colors[:len(chart_names)], 
                      alpha=0.8, edgecolor=BORDER_COLOR, linewidth=1.5, height=0.7)
        
        # Ajouter les valeurs sur les barres avec style moderne
        for i, (y, count) in enumerate(zip(y_pos, chart_counts)):
            ax.text(count + 0.5, y, f'{count}', va='center', ha='left', 
                   fontsize=11, fontweight='bold', color=TEXT_PRIMARY,
                   bbox=dict(boxstyle="round,pad=0.3", facecolor=colors[i % len(colors)], 
                           alpha=0.9, edgecolor=BORDER_COLOR, linewidth=1))
        
        # Configuration des axes pour le graphique horizontal
        ax.set_yticks(y_pos)
        
        # Abréger les noms des classes pour le graphique
        abbreviated_names = []
        for name in chart_names:
            if "Terminale" in name:
                if "Terminale Sciences Exactes" in name:
                    abbreviated_names.append("TSE")
                elif "Terminale Sciences Mathématiques" in name:
                    abbreviated_names.append("TSM")
                elif "Terminale Sciences Sociales" in name:
                    abbreviated_names.append("TSS")
                else:
                    abbreviated_names.append("T°")
            elif "Année" in name:
                abbreviated_name = name.split("°")[0] + "°"
                abbreviated_names.append(abbreviated_name)
            elif "Sciences" in name:
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
        
        ax.set_yticklabels(abbreviated_names, fontsize=11, fontweight='bold', color=TEXT_PRIMARY)
        ax.set_xlabel("Nombre d'élèves", color=TEXT_PRIMARY, fontsize=13, fontweight='bold')
        ax.set_title("📊 Répartition des Effectifs par Classe", color=TEXT_PRIMARY, fontsize=16, fontweight='bold', pad=20)
        
        # Style moderne du graphique
        ax.tick_params(axis='both', colors=TEXT_PRIMARY, labelsize=11)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_visible(False)
        ax.spines['bottom'].set_color(MUTED)
        
        # Grille subtile horizontale seulement
        ax.grid(True, alpha=0.2, color=MUTED, axis='x', linestyle='-', linewidth=0.5)
        
        # Inverser l'ordre des y pour avoir les plus grandes valeurs en haut
        ax.invert_yaxis()
        
        # Ajuster les marges
        fig.tight_layout(pad=2.0)
        
        # Intégration dans CustomTkinter avec mise à jour instantanée et meilleur espacement
        canvas = FigureCanvasTkAgg(fig, self.chart_container)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True, padx=PADDING_SMALL, pady=(0, PADDING_SMALL))

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
        messagebox.showinfo("Export PDF", "Fonctionnalité d'export PDF - À implémenter\n\nCette fonction exportera la liste des élèves de la classes sélectionnée au format PDF.")
    
    def export_to_excel(self):
        """Exporte les données des élèves en Excel"""
        self.update_last_action("Export Excel", "Génération du fichier Excel")
        messagebox.showinfo("Export Excel", "Fonctionnalité d'export Excel - À implémenter\n\nCette fonction exportera la liste des élèves de la classes sélectionnée au format Excel (.xlsx).")

    def _center_window(self, window):
        """Centre une fenêtre sur l'écran comme le login view"""
        window.update_idletasks()
        width = window.winfo_width()
        height = window.winfo_height()
        x = (window.winfo_screenwidth() // 2) - (width // 2)
        y = (window.winfo_screenheight() // 2) - (height // 2)
        window.geometry(f"{width}x{height}+{x}+{y}")

    def afficher_tous_eleves_classe(self):
        """Affiche tous les élèves de la classes sélectionnée avec le thème personnalisé"""
        self.update_last_action("Affichage", "Ouverture de la liste des élèves")
        if self.selected_classe is None:
            messagebox.showinfo("Information", "Veuillez d'abord sélectionner une classes dans la sidebar.")
            return
        
        # Récupérer tous les élèves de la classes sélectionnée en utilisant l'ID
        eleves_classe = get_eleves_list(self.selected_classe_id)
        
        if not eleves_classe:
            messagebox.showinfo("Information", f"Aucun élève trouvé dans la classes '{self.selected_classe}'.")
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
        print(f"🔧 Création de l'interface pour {len(eleves_classe)} élèves")
        
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
        
        # En-tête moderne avec le thème depuis la racine
        header_frame = ctk.CTkFrame(self.show_all_window, fg_color=BG_CARD, corner_radius=0, border_width=2, border_color=TEXT_ACCENT)
        header_frame.pack(fill="x", padx=0, pady=0)
        
        # Titre principal avec icône
        title_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        title_frame.pack(fill="x", padx=20, pady=15)
        
        # Icône et titre
        title_inner = ctk.CTkFrame(title_frame, fg_color="transparent")
        title_inner.pack(side="left")
        
        # Charger l'icône élève depuis les ressources
        try:
            eleve_icon = get_icon("person", (32, 32))
            if eleve_icon:
                icon_label = ctk.CTkLabel(title_inner, image=eleve_icon, text="")
                icon_label._imgref = eleve_icon
                icon_label.pack(side="left", padx=(0, 4))
            else:
                raise Exception("Icône non trouvée")
        except:
            # Fallback si l'icône n'est pas trouvée
            icon_label = ctk.CTkLabel(title_inner, text="👨‍🎓", font=("Segoe UI", 24), text_color=ACCENT_BLUE)
            icon_label.pack(side="left", padx=(0, 4))
        
        title_label = ctk.CTkLabel(title_inner, text="Gestion des élèves",font=("Segoe UI", 32, "bold"), text_color=TEXT_ACCENT)
        title_label.pack(side="left")
        
        # Informations sur la classes
        info_frame = ctk.CTkFrame(header_frame, fg_color=BG_SIDEBAR, corner_radius=8, border_width=2, border_color=TEXT_ACCENT)
        info_frame.pack(fill="x", padx=20, pady=(0, 4))
        
        info_text = f"Classe {self.selected_classe} - {len(eleves_classe)} élève(s)"
        info_label = ctk.CTkLabel(info_frame, text=info_text,font=("Segoe UI", 16, "bold"), text_color=TEXT_ACCENT)
        info_label.pack(pady=10)
        
        # Zone principale avec recherche et boutons
        main_frame = ctk.CTkFrame(self.show_all_window, fg_color=BG_MAIN)
        main_frame.pack(fill="both", expand=True, padx=4, pady=4)
        
        # Barre d'actions (recherche + boutons)
        actions_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        actions_frame.pack(fill="x", pady=(0, 4))
        
        # Zone de recherche (à gauche) avec le thème cohérent
        search_frame = ctk.CTkFrame(actions_frame, fg_color=BG_CARD, corner_radius=12, border_width=1, border_color=BORDER_COLOR)
        search_frame.pack(side="left", fill="x", expand=True, padx=(0, 4))
        
        search_inner = ctk.CTkFrame(search_frame, fg_color="transparent")
        search_inner.pack(fill="x", padx=15, pady=10)
        
        # Icône de recherche
        search_icon = get_icon("search", (18, 18))
        if search_icon:
            search_icon_label = ctk.CTkLabel(search_inner, image=search_icon, text="")
            search_icon_label.pack(side="left", padx=(0, 8))
            search_icon_label._imgref = search_icon
        else:
            search_icon_label = ctk.CTkLabel(search_inner, text="🔍", font=("Segoe UI", 14, "bold"), text_color=TEXT_ACCENT)
            search_icon_label.pack(side="left", padx=(0, 8))
        
        # Champ de recherche avec le thème cohérent
        self.search_entry = ctk.CTkEntry(search_inner, placeholder_text="Rechercher un élève par nom, prénom ou statut...", 
                                        fg_color=BG_CARD, text_color=TEXT_PRIMARY, border_color=BORDER_COLOR, 
                                        width=300, placeholder_text_color=TEXT_MUTED)
        self.search_entry.pack(side="left", fill="x", expand=True)
        self.search_entry.bind("<KeyRelease>", self.filter_eleves)
        
        # Boutons d'action (à droite) - seulement modifier, supprimer et exporter
        buttons_frame = ctk.CTkFrame(actions_frame, fg_color="transparent")
        buttons_frame.pack(side="right")
        print("🔧 Création des boutons CRUD...")
        
        # Bouton Modifier sans fond
        edit_icon = get_icon("edit", (20, 20))
        btn_edit = ctk.CTkButton(buttons_frame, text="Modifier", image=edit_icon if edit_icon else None, command=self.modifier_eleve, 
                                fg_color="transparent", hover_color=BG_CARD_HOVER, text_color=TEXT_ACCENT,
                                corner_radius=8, height=45, width=120, font=("Segoe UI", 13, "bold"), 
                                border_width=1, border_color=BORDER_COLOR)
        if edit_icon:
            btn_edit._imgref = edit_icon
        btn_edit.pack(side="left", padx=(0, 8))
        
        # Bouton Détails sans fond
        details_icon = get_icon("info", (20, 20))
        btn_details = ctk.CTkButton(buttons_frame, text="Détails", image=details_icon if details_icon else None, command=self.afficher_details_eleve, 
                                   fg_color="transparent", hover_color=BG_CARD_HOVER, text_color=TEXT_ACCENT,
                                   corner_radius=8, height=45, width=120, font=("Segoe UI", 13, "bold"), 
                                   border_width=1, border_color=BORDER_COLOR)
        if details_icon:
            btn_details._imgref = details_icon
        btn_details.pack(side="left", padx=(0, 8))
        
        # Bouton Supprimer sans fond
        delete_icon = get_icon("delete", (20, 20))
        btn_delete = ctk.CTkButton(buttons_frame, text="Supprimer", image=delete_icon if delete_icon else None, command=self.supprimer_eleve, 
                                 fg_color="transparent", hover_color=BG_CARD_HOVER, text_color=TEXT_ACCENT,
                                 corner_radius=8, height=45, width=120, font=("Segoe UI", 13, "bold"), 
                                 border_width=1, border_color=BORDER_COLOR)
        if delete_icon:
            btn_delete._imgref = delete_icon
        btn_delete.pack(side="left", padx=(0, 8))
        
        # Bouton Exporter sans fond
        export_icon = get_icon("csv", (20, 20))
        btn_export = ctk.CTkButton(buttons_frame, text="Exporter", image=export_icon if export_icon else None, command=self.exporter_eleves, 
                                 fg_color="transparent", hover_color=BG_CARD_HOVER, text_color=TEXT_ACCENT,
                                 corner_radius=8, height=45, width=120, font=("Segoe UI", 13, "bold"), 
                                 border_width=1, border_color=BORDER_COLOR)
        if export_icon:
            btn_export._imgref = export_icon
        btn_export.pack(side="left")
        
        # Message contextuel
        self.context_message = ctk.CTkLabel(main_frame, text="Sélectionnez un élève pour modifier ou supprimer",font=("Segoe UI", 12, "bold"), text_color=TEXT_ACCENT)
        self.context_message.pack(pady=(0, 4))
        
        # Conteneur du tableau avec le thème cohérent
        table_container = ctk.CTkFrame(main_frame, fg_color=BG_CARD, corner_radius=12, border_width=1, border_color=BORDER_COLOR)
        table_container.pack(fill="both", expand=True)
        
        # Configuration du style Treeview avec le thème
        style = ttk.Style()
        style.theme_use('clam')
        
        # Style des en-têtes avec le thème cohérent
        style.configure("Treeview.Heading", 
                       background="transparent", 
                       foreground=TEXT_ACCENT, 
                       padding=(20, 15),
                       borderwidth=1,
                       relief="solid")
        
        # Style des lignes avec le thème cohérent
        style.configure("Treeview", 
                       background=BG_CARD, 
                       foreground=TEXT_PRIMARY, 
                       rowheight=50,
                       borderwidth=0,
                       fieldbackground=BG_CARD)
        
        # Créer le tableau avec le thème
        columns = ("Nom", "Prénom", "Genre", "Naissance", "Âge", "Statut")
        self.table = ttk.Treeview(table_container, columns=columns, show="headings", style="Treeview")
        
        # Configuration des colonnes
        column_widths = {"Nom": 150, "Prénom": 150, "Genre": 80, "Naissance": 120, "Âge": 60, "Statut": 100}
        for col in columns:
            self.table.heading(col, text=col)
            self.table.column(col, width=column_widths[col], anchor="center")
        
        # Barre de défilement avec le thème cohérent
        scrollbar = ctk.CTkScrollbar(table_container, orientation="vertical", command=self.table.yview,
                                    fg_color=BORDER_COLOR, button_color=BG_CARD, button_hover_color=TEXT_ACCENT)
        self.table.configure(yscrollcommand=scrollbar.set)
        
        # Pack du tableau et de la barre de défilement
        self.table.pack(side="left", fill="both", expand=True, padx=4, pady=4)
        scrollbar.pack(side="right", fill="y", padx=(0, 4), pady=10)
        
        # Stocker les données des élèves
        self.eleves_data = eleves_classe
        print(f"🔧 Remplissage du tableau avec {len(eleves_classe)} élèves...")
        
        # Remplir le tableau avec les données
        for eleve in eleves_classe:
            _id, nom, prenom, genre, naissance, statut, cid = eleve
            age = calculate_age(naissance)
            
            # Insérer dans le tableau
            item = self.table.insert("", "end", values=(nom, prenom, genre, naissance, age, statut))
            
            # Appliquer les couleurs selon le statut
            if statut == "Actif":
                self.table.tag_configure("actif", foreground="#27AE60")  # Vert pour actif
                self.table.item(item, tags=(self.table.item(item, "tags")[0], "actif"))
            elif statut == "Inactif":
                self.table.tag_configure("inactif", foreground="#E74C3C")  # Rouge pour inactif
                self.table.item(item, tags=(self.table.item(item, "tags")[0], "inactif"))
        
        # Bind des événements
        self.table.bind("<<TreeviewSelect>>", self.on_table_select)
        
        # Focus sur le tableau
        self.table.focus_set()
        
        # Message de fermeture
        self.show_all_window.protocol("WM_DELETE_WINDOW", self.on_close_show_all)
        
        print("✅ Interface créée avec succès !")

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
            selected_items = self.students_table.selection()
            if selected_items:
                selected_item = selected_items[0]
                values = self.students_table.item(selected_item)['values']
                
                if values and len(values) >= 6:
                    # Trouver l'index de la ligne sélectionnée
                    all_items = self.students_table.get_children()
                    row_index = all_items.index(selected_item)
                    
                    # Récupérer les données de l'élève depuis self.eleves_data
                    if hasattr(self, 'eleves_data') and row_index < len(self.eleves_data):
                        eleve_data = self.eleves_data[row_index]
                        _id, nom, prenom, genre, naissance, classe_id, classe_nom = eleve_data
                        
                        self.update_last_action("Modification", f"Modification de {nom} {prenom}")
                self.formulaire_eleve(mode="Modifier", eleves={
                            'id': _id,
                            'nom': nom,
                            'prenom': prenom,
                            'genre': genre,
                            'date_naissance': naissance,
                            'classe': classe_nom,
                            'statut': 'Actif'
                        })
            else:
                messagebox.showwarning("Aucune sélection", "Veuillez sélectionner un élève dans le tableau pour le modifier.")
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de la modification : {str(e)}")

    def supprimer_eleve(self):
        """Supprime l'élève sélectionné dans le tableau"""
        try:
            # Obtenir l'élève sélectionné depuis le tableau
            selected_items = self.students_table.selection()
            if selected_items:
                selected_item = selected_items[0]
                values = self.students_table.item(selected_item)['values']
                
                if values and len(values) >= 6:
                    # Trouver l'index de la ligne sélectionnée
                    all_items = self.students_table.get_children()
                    row_index = all_items.index(selected_item)
                    
                    # Récupérer les données de l'élève depuis self.eleves_data
                    if hasattr(self, 'eleves_data') and row_index < len(self.eleves_data):
                        eleve_data = self.eleves_data[row_index]
                        _id, nom, prenom, genre, naissance, classe_id, classe_nom = eleve_data
                
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
                    conn = get_db_connection()
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

    def supprimer_eleve_specific(self, eleves):
        """Supprime un élève spécifique"""
        _id, nom, prenom, genre, naissance, statut, cid = eleves
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

    def exporter_eleves(self):
        """Exporte la liste des élèves vers un fichier CSV"""
        try:
            from tkinter import filedialog
            import csv
            
            # Demander où sauvegarder le fichier
            filename = filedialog.asksaveasfilename(
                defaultextension=".csv",
                filetypes=[("Fichiers CSV", "*.csv"), ("Tous les fichiers", "*.*")],
                title="Exporter les élèves"
            )
            
            if not filename:
                return
            
            # Récupérer les données des élèves
            eleves_data = get_eleves_list(self.selected_classe_id)
            
            if not eleves_data:
                messagebox.showwarning("Attention", "Aucun élève à exporter.")
                return
            
            # Écrire le fichier CSV
            with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
                fieldnames = ['Nom', 'Prénom', 'Genre', 'Date de naissance', 'Âge', 'Statut', 'Classe']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                
                writer.writeheader()
                for eleve in eleves_data:
                    writer.writerow({
                        'Nom': eleve[1],  # nom
                        'Prénom': eleve[2],  # prenom
                        'Genre': eleve[3],  # genre
                        'Date de naissance': eleve[4],  # date_naissance
                        'Âge': eleve[5],  # age
                        'Statut': eleve[6],  # statut
                        'Classe': self.selected_classe
                    })
            
            messagebox.showinfo("Succès", f"Les élèves ont été exportés vers {filename}")
            
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de l'exportation : {e}")

    def transferer_eleve(self):
        """Transfert l'élève sélectionné vers une autre classes"""
        self.update_last_action("Transfert", "Ouverture du formulaire de transfert")
        messagebox.showinfo("Transfert", "Fonctionnalité de transfert d'élève - À implémenter")

    def details_eleve(self):
        """Affiche les détails de l'élève sélectionné"""
        messagebox.showinfo("Détails", "Fonctionnalité de détails d'élève - À implémenter")

    def afficher_details_eleve(self):
        """Affiche les détails complets d'un élève sélectionné dans le tableau"""
        try:
            # Obtenir l'élève sélectionné depuis le tableau
            selected_items = self.students_table.selection()
            if selected_items:
                selected_item = selected_items[0]
                values = self.students_table.item(selected_item)['values']
                
                if values and len(values) >= 6:
                    # Trouver l'index de la ligne sélectionnée
                    all_items = self.students_table.get_children()
                    row_index = all_items.index(selected_item)
                    
                    # Récupérer les données de l'élève depuis self.eleves_data
                    if hasattr(self, 'eleves_data') and row_index < len(self.eleves_data):
                        eleve_data = self.eleves_data[row_index]
                        _id, nom, prenom, genre, naissance, classe_id, classe_nom = eleve_data
                        
                        # Ouvrir la fenêtre de détails
                        self.show_student_details_from_table({
                            'id': _id,
                            'nom': nom,
                            'prenom': prenom,
                            'genre': genre,
                            'naissance': naissance,
                            'classe': classe_nom,
                            'statut': 'Actif'
                        })
                    else:
                        messagebox.showwarning("Aucune sélection", "Veuillez sélectionner un élève dans le tableau pour voir ses détails.")
                else:
                    messagebox.showwarning("Aucune sélection", "Veuillez sélectionner un élève dans le tableau pour voir ses détails.")
            else:
                messagebox.showwarning("Aucune sélection", "Veuillez sélectionner un élève dans le tableau pour voir ses détails.")
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de l'affichage des détails : {str(e)}")

    def show_student_details_from_table(self, eleve_data):
        """Affiche les détails d'un élève dans le panneau de droite"""
        # Effacer le contenu du panneau de détails
        for w in self.student_details_panel.winfo_children():
            w.destroy()
        
        # Conteneur principal
        details_frame = ctk.CTkFrame(self.student_details_panel, fg_color="transparent")
        details_frame.pack(fill="both", expand=True, padx=8, pady=8)
        
        # En-tête avec avatar et informations principales
        header_frame = ctk.CTkFrame(details_frame, fg_color=BG_SIDEBAR, corner_radius=12)
        header_frame.pack(fill="x", pady=(0, 8))
        
        header_content = ctk.CTkFrame(header_frame, fg_color="transparent")
        header_content.pack(fill="x", padx=15, pady=15)
        
        # Avatar
        avatar_frame = ctk.CTkFrame(header_content, fg_color=BG_CARD, corner_radius=25, width=50, height=50)
        avatar_frame.pack(side="left")
        avatar_frame.pack_propagate(False)
        
        # Icône de personne dans l'avatar
        person_icon = get_icon("person", (20, 20))
        if person_icon:
            avatar_label = ctk.CTkLabel(avatar_frame, text="", image=person_icon, text_color=TEXT_ACCENT)
            avatar_label._imgref = person_icon
            avatar_label.pack(expand=True)
        else:
            # Fallback avec initiales
            initiales = f"{eleve_data['prenom'][0]}{eleve_data['nom'][0]}".upper()
            avatar_label = ctk.CTkLabel(avatar_frame, text=initiales, font=("Segoe UI", 14, "bold"), text_color=TEXT_ACCENT)
            avatar_label.pack(expand=True)
        
        # Informations principales
        info_frame = ctk.CTkFrame(header_content, fg_color="transparent")
        info_frame.pack(side="left", fill="x", expand=True, padx=(15, 0))
        
        # Nom complet
        nom_complet = f"{eleve_data['prenom']} {eleve_data['nom']}"
        nom_label = ctk.CTkLabel(info_frame, text=nom_complet, font=("Segoe UI", 18, "bold"), text_color=TEXT_PRIMARY)
        nom_label.pack(anchor="w")
        
        # Classe et âge
        age = calculate_age(eleve_data['naissance']) if eleve_data['naissance'] else "N/A"
        classe_age = f"{eleve_data['classe']} • {age} ans"
        classe_label = ctk.CTkLabel(info_frame, text=classe_age, font=("Segoe UI", 14), text_color=TEXT_SECONDARY)
        classe_label.pack(anchor="w", pady=(2, 0))
        
        # Boutons d'action
        actions_frame = ctk.CTkFrame(header_content, fg_color="transparent")
        actions_frame.pack(side="right")
        
        # Bouton Modifier
        edit_icon = get_icon("edit", (16, 16))
        btn_edit = ctk.CTkButton(
            actions_frame,
            text="Modifier",
            image=edit_icon,
            width=100,
            height=30,
            font=("Segoe UI", 12, "bold"),
            fg_color="transparent",
            hover_color=BG_CARD,
            text_color=TEXT_PRIMARY,
            corner_radius=8,
            border_width=1,
            border_color=BORDER_COLOR
        )
        btn_edit.pack(side="right", padx=(5, 0))
        
        # Bouton Supprimer
        delete_icon = get_icon("delete", (16, 16))
        btn_delete = ctk.CTkButton(
            actions_frame,
            text="Supprimer",
            image=delete_icon,
            width=100,
            height=30,
            font=("Segoe UI", 12, "bold"),
            fg_color="transparent",
            hover_color=ERROR_RED,
            text_color=TEXT_PRIMARY,
            corner_radius=8,
            border_width=1,
            border_color=BORDER_COLOR
        )
        btn_delete.pack(side="right")
        
        # Contenu scrollable pour les détails
        content_frame = ctk.CTkScrollableFrame(details_frame, fg_color="transparent")
        content_frame.pack(fill="both", expand=True)
        
        # Section informations personnelles
        self.create_info_section(content_frame, "Informations Personnelles", [
            ("ID", str(eleve_data['id'])),
            ("Nom", eleve_data['nom']),
            ("Prénom", eleve_data['prenom']),
            ("Genre", eleve_data['genre']),
            ("Date de naissance", eleve_data['naissance']),
            ("Âge", f"{age} ans")
        ])
        
        # Section informations académiques
        self.create_info_section(content_frame, "Informations Académiques", [
            ("Classe", eleve_data['classe']),
            ("Statut", "Actif"),
            ("Année scolaire", "2024-2025")
        ])
        
        # Section statistiques
        self.create_info_section(content_frame, "Statistiques", [
            ("Moyenne générale", "15.5/20"),
            ("Rang", "5ème"),
            ("Absences", "3 jours"),
            ("Retards", "2 fois")
        ])
    
    def create_info_section(self, parent, title, items):
        """Crée une section d'informations avec titre et éléments"""
        section_frame = ctk.CTkFrame(parent, fg_color=BG_CARD, corner_radius=12, border_width=1, border_color=BORDER_COLOR)
        section_frame.pack(fill="x", pady=(0, 8))
        
        # Titre de section
        title_frame = ctk.CTkFrame(section_frame, fg_color=BG_SIDEBAR, corner_radius=12)
        title_frame.pack(fill="x", padx=2, pady=2)
        
        title_label = ctk.CTkLabel(
            title_frame,
            text=title,
            font=("Segoe UI", 16, "bold"),
            text_color=TEXT_PRIMARY
        )
        title_label.pack(padx=15, pady=10)
        
        # Contenu de la section
        content_frame = ctk.CTkFrame(section_frame, fg_color="transparent")
        content_frame.pack(fill="x", padx=15, pady=(0, 15))
        
        for label, value in items:
            item_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
            item_frame.pack(fill="x", pady=2)
            
            label_widget = ctk.CTkLabel(
                item_frame,
                text=f"{label}:",
                font=("Segoe UI", 12, "bold"),
                text_color=TEXT_SECONDARY,
                width=120,
                anchor="w"
            )
            label_widget.pack(side="left")
            
            value_widget = ctk.CTkLabel(
                item_frame,
                text=str(value),
                font=("Segoe UI", 12),
                text_color=TEXT_PRIMARY,
                anchor="w"
            )
            value_widget.pack(side="left", padx=(10, 0))

    def get_classe_id_by_name(self, classe_name):
        """Récupère l'ID de la classe à partir de son nom"""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT id_classe FROM classes WHERE nom_classe = ?", (classe_name,))
            result = cursor.fetchone()
            return result[0] if result and len(result) > 0 else None
        except Exception as e:
            print(f"Erreur lors de la récupération de l'ID de la classe: {e}")
            return None
        finally:
            try:
                conn.close()
            except:
                pass

    def get_classes_list(self):
        """Récupère la liste des classes disponibles depuis la base de données"""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT nom_classe FROM classes ORDER BY nom_classe")
            classes = cursor.fetchall()
            conn.close()
            return [classe[0] for classe in classes] if classes else ["Aucune classe"]
        except Exception as e:
            print(f"Erreur lors de la récupération des classes: {e}")
            return ["Aucune classe"]

    def formulaire_eleve(self, mode="Ajouter", eleves=None):
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
        main_container.pack(fill="both", expand=True, padx=4, pady=4)
        
        # En-tête du formulaire
        header = ctk.CTkFrame(main_container, fg_color=BG_CARD, corner_radius=12)
        header.pack(fill="x", pady=(0, 4))
        
        title_text = "Nouveau Profil Élève" if mode == "Ajouter" else f"Modification de {eleves.get('nom','')} {eleves.get('prenom','')}"
        ctk.CTkLabel(
            header, 
            text=title_text, text_color=ACCENT_BLUE
        ).pack(pady=20)

        # Corps du formulaire
        body = ctk.CTkScrollableFrame(main_container, fg_color=BG_CARD, corner_radius=12)
        body.pack(fill="both", expand=True, pady=(0, 4))
        
        # Champs du formulaire
        fields = [
            ("Matricule", "matricule"),
            ("Nom *", "nom"),
            ("Prénom *", "prenom"),
            ("Date de naissance", "date_naissance"),
            ("Genre", "genre"),
            ("Classe *", "classe"),
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
                text=label, text_color=TEXT_PRIMARY
            ).grid(row=row*2, column=col, sticky="w", padx=10, pady=(10, 5))
            
            # Champ de saisie
            if key in ["genre", "statut"]:
                widget = ctk.CTkOptionMenu(
                    body,
                    values=["Masculin", "Féminin"] if key == "genre" else ["Actif", "Inactif"], fg_color=BG_CARD_HOVER,
                    button_color=ACCENT_BLUE,
                    button_hover_color=BORDER_ACCENT,
                    height=35
                )
            elif key == "classe":
                # Récupérer les classes disponibles depuis la base de données
                classes_values = self.get_classes_list()
                widget = ctk.CTkOptionMenu(
                    body,
                    values=classes_values, fg_color=BG_CARD_HOVER,
                    button_color=ACCENT_BLUE,
                    button_hover_color=BORDER_ACCENT,
                    height=35
                )
            else:
                widget = ctk.CTkEntry(
                    body, fg_color=BG_CARD_HOVER, border_color=BORDER_COLOR,
                    height=35
                )
            
            widget.grid(row=row*2+1, column=col, sticky="ew", padx=10, pady=(0, 4))
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
                command=lambda: self.save_eleve(popup, mode), fg_color=SUCCESS_GREEN, hover_color="#059669",
                height=40,
            ).pack(side="left", padx=(0, 4), pady=15)
        elif mode == "Modifier":
            ctk.CTkButton(
                footer, 
                text="Mettre à jour",
                command=lambda: self.save_eleve(popup, mode, eleves.get('id_eleve')), fg_color=WARNING_ORANGE, hover_color="#d97706",
                height=40,
            ).pack(side="left", padx=(0, 4), pady=15)

        ctk.CTkButton(
            footer, 
            text="Fermer", 
            command=popup.destroy, fg_color=ERROR_RED, hover_color="#dc2626",
            height=40,
        ).pack(side="right", pady=15)

        # Pré-remplissage si modification
        if isinstance(eleves, dict):
            self.fill_form(eleves)

    def fill_form(self, eleves: dict):
        """Pré-remplit le formulaire avec les données de l'élève"""
        data_map = {
            "matricule": eleves.get("matricule"),
            "nom": eleves.get("nom"),
            "prenom": eleves.get("prenom"),
            "genre": eleves.get("genre"),
            "date_naissance": eleves.get("date_naissance"),
            "classe": eleves.get("classe"),
            "statut": eleves.get("statut"),
            "telephone": eleves.get("telephone"),
            "email": eleves.get("email"),
            "adresse": eleves.get("adresse"),
            "parent_nom": eleves.get("parent_nom"),
            "parent_prenom": eleves.get("parent_prenom"),
            "parent_telephone": eleves.get("parent_telephone"),
            "parent_email": eleves.get("parent_email"),
            "parent_adresse": eleves.get("parent_adresse"),
            "parent_profession": eleves.get("parent_profession"),
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
            "classe": _get("classe"),
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
        if not all([data.get("nom"), data.get("prenom"), data.get("classe")]):
            messagebox.showerror("Erreur", "Nom, Prénom et Classe sont obligatoires.")
            return

        # Récupérer l'ID de la classe
        classe_id = self.get_classe_id_by_name(data.get("classe"))
        if not classe_id:
            messagebox.showerror("Erreur", "Classe sélectionnée introuvable.")
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
                    data["statut"], data["telephone"], data["email"], data["adresse"], classe_id,
                    data["parent_nom"], data["parent_prenom"], data["parent_telephone"],
                    data["parent_email"], data["parent_adresse"], data["parent_profession"]
                ))
                messagebox.showinfo("Succès", "Élève ajouté avec succès.")
            elif mode == "Modifier" and eleve_id:
                cur.execute("""
                    UPDATE eleves SET 
                        matricule=?, nom=?, prenom=?, genre=?, date_naissance=?, statut=?, 
                        telephone=?, email=?, adresse=?, id_classe=?, parent_nom=?, parent_prenom=?, 
                        parent_telephone=?, parent_email=?, parent_adresse=?, parent_profession=?
                    WHERE id_eleve=?
                """, (
                    data["matricule"], data["nom"], data["prenom"], data["genre"], data["date_naissance"],
                    data["statut"], data["telephone"], data["email"], data["adresse"], classe_id,
                    data["parent_nom"], data["parent_prenom"], data["parent_telephone"],
                    data["parent_email"], data["parent_adresse"], data["parent_profession"], eleve_id
                ))
                messagebox.showinfo("Succès", "Élève mis à jour avec succès.")

            conn.commit()
            self.refresh_dashboard()
            popup.destroy()
        except Exception as e:
            messagebox.showerror("Erreur de base de données", f"Une erreur est survenue : {e}")
        finally:
            conn.close()

    def _open_eleve_details_card(self, eleves):
        """Ouvre la carte de détails de l'élève"""
        popup = ctk.CTkToplevel(self)
        popup.title(f"Détails - {eleves.get('nom', '')} {eleves.get('prenom', '')}")
        popup.geometry("700x500")
        popup.transient(self.winfo_toplevel())
        popup.grab_set()
        popup.configure(fg_color=BG_MAIN)
        
        # Contenu principal
        main_container = ctk.CTkFrame(popup, fg_color="transparent")
        main_container.pack(fill="both", expand=True, padx=4, pady=4)
        
        # En-tête avec design moderne
        header = ctk.CTkFrame(main_container, fg_color=ACCENT_BLUE, corner_radius=15)
        header.pack(fill="x", pady=(0, 4))
        
        # Contenu de l'en-tête avec icône
        header_content = ctk.CTkFrame(header, fg_color="transparent")
        header_content.pack(fill="x", padx=20, pady=15)
        
        # Icône élève
        eleve_icon = get_icon("eleve", (40, 40))
        if eleve_icon:
            icon_label = ctk.CTkLabel(header_content, text="", image=eleve_icon, text_color=WHITE)
            icon_label._imgref = eleve_icon
            icon_label.pack(side="left", padx=(0, 4))
        
        # Titre principal
        title_label = ctk.CTkLabel(
            header_content, 
            text=f"Détails de {eleves.get('nom', '')} {eleves.get('prenom', '')}", text_color=WHITE
        )
        title_label.pack(side="left")
        
        # Badge du statut à droite
        statut = eleves.get('statut', 'Inconnu')
        statut_color = SUCCESS_GREEN if statut.lower() == 'actif' else ERROR_RED
        statut_badge = ctk.CTkFrame(header_content, fg_color=statut_color, corner_radius=20)
        statut_badge.pack(side="right", padx=(4, 0))
        
        statut_label = ctk.CTkLabel(
            statut_badge,
            text=f"Statut: {statut}", text_color=WHITE
        )
        statut_label.pack(padx=15, pady=8)

        # Corps des détails
        body = ctk.CTkScrollableFrame(main_container, fg_color=BG_CARD, corner_radius=12)
        body.pack(fill="both", expand=True, pady=(0, 4))
        
        # Affichage des informations
        details = [
            ("Matricule", eleves.get("matricule", "—")),
            ("Nom", eleves.get("nom", "—")),
            ("Prénom", eleves.get("prenom", "—")),
            ("Date de naissance", eleves.get("date_naissance", "—")),
            ("Genre", eleves.get("genre", "—")),
            ("Statut", eleves.get("statut", "—")),
            ("Téléphone", eleves.get("telephone", "—")),
            ("Email", eleves.get("email", "—")),
            ("Adresse", eleves.get("adresse", "—")),
            ("Classe", get_classe_name(eleves.get("id_classe")) or "—"),
            ("Date d'inscription", eleves.get("date_inscription", "—")),
            ("Nom Parent", eleves.get("parent_nom", "—")),
            ("Prénom Parent", eleves.get("parent_prenom", "—")),
            ("Téléphone Parent", eleves.get("parent_telephone", "—")),
            ("Email Parent", eleves.get("parent_email", "—")),
            ("Adresse Parent", eleves.get("parent_adresse", "—")),
            ("Profession Parent", eleves.get("parent_profession", "—")),
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
                text=f"{label}:", text_color=WHITE
            ).pack(padx=10, pady=5)
            
            # Valeur dans un cadre stylé
            value_frame = ctk.CTkFrame(field_container, fg_color=BG_CARD_HOVER, corner_radius=8)
            value_frame.pack(fill="x")
            
            ctk.CTkLabel(
                value_frame, 
                text=str(value), text_color=TEXT_PRIMARY
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
            image=edit_icon, fg_color=ACCENT_BLUE, text_color=WHITE, hover_color=HOVER_PRIMARY,
            command=lambda: self.formulaire_eleve("Modifier", eleves),
            corner_radius=10,
            height=40,
            width=120, border_width=1, border_color=ACCENT_BLUE
        )
        if edit_icon:
            btn_edit._imgref = edit_icon
        btn_edit.pack(side="left", padx=(0, 4))
        
        # Bouton Supprimer
        delete_icon = get_icon("delete", (20, 20))
        btn_delete = ctk.CTkButton(
            buttons_container,
            text="Supprimer",
            image=delete_icon, fg_color=WARNING_ORANGE, text_color=WHITE, hover_color=HOVER_WARNING,
            command=self.supprimer_eleve,
            corner_radius=10,
            height=40,
            width=120, border_width=1, border_color=WARNING_ORANGE
        )
        if delete_icon:
            btn_delete._imgref = delete_icon
        btn_delete.pack(side="left", padx=(0, 4))
        
        # Bouton Fermer
        btn_close = ctk.CTkButton(
            buttons_container,
            text="Fermer",
            command=popup.destroy, fg_color=SUCCESS_GREEN, text_color=WHITE, hover_color=HOVER_SUCCESS,
            corner_radius=10,
            height=40,
            width=120, border_width=1, border_color=SUCCESS_GREEN
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


class StudentListItem(ctk.CTkFrame):
    """Un élément de liste cliquable pour un élève avec design moderne comme les salles"""
    def __init__(self, parent, student_data, command):
        super().__init__(parent, fg_color=BG_CARD, height=60, corner_radius=12, 
                         border_color=BORDER_COLOR, border_width=1)
        self.student_data = student_data
        self.command = command
        self.is_selected = False

        # Container principal
        main_frame = ctk.CTkFrame(self, fg_color="transparent")
        main_frame.pack(fill="both", expand=True, padx=12, pady=12)

        # Icône selon le genre
        try:
            if student_data['genre'] == "M":
                icon_name = "person.png"
            else:
                icon_name = "person.png"  # Même icône pour les deux genres
            
            icon_path = os.path.join(os.path.dirname(__file__), '..', '..', '..', '..', '..', 'resources', 'icons', icon_name)
            student_icon = ctk.CTkImage(Image.open(icon_path), size=(24, 24))
            icon_label = ctk.CTkLabel(main_frame, text="", image=student_icon)
            icon_label.pack(side="left", padx=(0, 8))
        except FileNotFoundError:
            print(f"Icône '{icon_name}' non trouvée.")

        # Informations de l'élève
        info_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        info_frame.pack(side="left", fill="both", expand=True)

        # Nom complet de l'élève
        full_name = f"{student_data['prenom']} {student_data['nom']}"
        self.name_label = ctk.CTkLabel(info_frame, text=full_name, 
                                      font=("Segoe UI", 14, "bold"), 
                                      text_color=TEXT_PRIMARY, anchor="w")
        self.name_label.pack(side="left", fill="x", expand=True)

        # Âge à droite
        age_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        age_frame.pack(side="right", padx=(8, 0))

        self.age_label = ctk.CTkLabel(age_frame, text=f"{student_data['age']} ans", 
                                     font=("Segoe UI", 12), text_color=TEXT_SECONDARY)
        self.age_label.pack(side="left")

        # Bindings pour l'interactivité
        self.bind("<Button-1>", self.on_click)
        main_frame.bind("<Button-1>", self.on_click)
        self.name_label.bind("<Button-1>", self.on_click)
        self.age_label.bind("<Button-1>", self.on_click)
        
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)
        main_frame.bind("<Enter>", self.on_enter)
        main_frame.bind("<Leave>", self.on_leave)
        self.name_label.bind("<Enter>", self.on_enter)
        self.name_label.bind("<Leave>", self.on_leave)
        self.age_label.bind("<Enter>", self.on_enter)
        self.age_label.bind("<Leave>", self.on_leave)

    def on_click(self, event=None):
        self.command(self.student_data, self)

    def on_enter(self, event=None):
        if not self.is_selected:
            self.configure(fg_color=BG_CARD_HOVER, border_color=ACCENT_BLUE)

    def on_leave(self, event=None):
        if not self.is_selected:
            self.configure(fg_color=BG_CARD, border_color=BORDER_COLOR)

    def select(self):
        self.is_selected = True
        self.configure(fg_color=ACCENT_BLUE, border_color=ACCENT_BLUE, border_width=2)

    def deselect(self):
        self.is_selected = False
        self.configure(fg_color=BG_CARD, border_color=BORDER_COLOR, border_width=1)
