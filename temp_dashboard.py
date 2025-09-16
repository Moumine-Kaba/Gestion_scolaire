# -*- coding: utf-8 -*-
"""
EduManager+ - Tableau de bord principal (CustomTkinter, thÃ¨me sombre)
- Graphique amÃ©liorÃ© "Moyenne par matiÃ¨re (Tendance)" avec effets visuels premium
"""

# Import du systÃ¨me centralisÃ©
import sys
import os

# Ajouter le chemin racine au sys.path
root_path = os.path.join(os.path.dirname(__file__), "..", "..", "..", "..")
if root_path not in sys.path:
    sys.path.insert(0, root_path)

# Import du systÃ¨me centralisÃ©
from src.core.paths import (
    DATABASE_PATH, ICONS_PATH, THEME_PATH, 
    get_db_connection, get_icon_path, icon_exists,
    print_paths
)
from src.core.view_registry import get_view_registry, register_all_views

# Fonctions utilitaires pour les chemins (compatibilitÃ©)
def get_db_path():
    """Retourne le chemin vers la base de donnÃ©es (compatibilitÃ©)"""
    return DATABASE_PATH

def get_icons_dir():
    """Retourne le chemin vers le dossier des icÃ´nes (compatibilitÃ©)"""
    return ICONS_PATH


import math
import datetime
import sqlite3
import tkinter as tk
from tkinter import messagebox
import customtkinter as ctk
from PIL import Image, ImageDraw
import numpy as np

# =================== CHEMINS CENTRALISÃ‰S =====================
# Affichage des chemins centralisÃ©s
print_paths()

# DB - Utilise la base de donnÃ©es centralisÃ©e
DB_PATH = DATABASE_PATH
print(">>> Fichier DB utilisÃ© :", DB_PATH)

# ICÃ”NES - Chemin centralisÃ©
ICONS_DIR = ICONS_PATH
print(">>> Dossier icÃ´nes utilisÃ© :", ICONS_DIR)

# =================== SQLITE HELPERS CENTRALISÃ‰S =====================
def get_conn():
    """Utilise la connexion centralisÃ©e Ã  la base de donnÃ©es"""
    return get_db_connection()

def table_exists(conn, name):
    try:
        cur = conn.cursor()
        cur.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND lower(name)=lower(?)",
            (name,),
        )
        return cur.fetchone() is not None
    except Exception:
        return False

def get_stats_count_any(*table_candidates) -> int:
    """Renvoie COUNT(*) pour la premiÃ¨re table existante parmi table_candidates."""
    conn = get_conn()
    if not conn:
        return 0
    try:
        cur = conn.cursor()
        table_name = None
        for t in table_candidates:
            if table_exists(conn, t):
                table_name = t
                break
        if not table_name:
            return 0
        cur.execute(f"SELECT COUNT(*) FROM {table_name}")
        r = cur.fetchone()
        return int((r[0] if not isinstance(r, sqlite3.Row) else r[0]) or 0)
    except Exception as e:
        print(f"âš ï¸ get_stats_count_any: {e}")
        return 0
    finally:
        try:
            conn.close()
        except:
            pass

def fetch_effectifs_par_classe(limit: int = 10):
    """
    Retourne [(nom_classe, effectif)] sur base:
      - classes(id_classe, nom_classe)
      - eleves(id_eleve, id_classe)
    """
    conn = get_conn()
    if not conn:
        return []
    try:
        cur = conn.cursor()
        cur.execute("""
            SELECT c.nom_classe AS classe, COUNT(e.id_eleve) AS nb
            FROM classes c
            LEFT JOIN eleves e ON e.id_classe = c.id_classe
            GROUP BY c.id_classe, c.nom_classe
            ORDER BY nb DESC, classe ASC
            LIMIT ?
        """, (limit,))
        rows = cur.fetchall()
        out = []
        for r in rows:
            if isinstance(r, sqlite3.Row):
                out.append((r["classe"], int(r["nb"] or 0)))
            else:
                out.append((r[0], int(r[1] or 0)))
        return out
    except Exception as e:
        print("âš ï¸ fetch_effectifs_par_classe:", e)
        return []
    finally:
        try:
            conn.close()
        except:
            pass

# =================== THÃˆME / COULEURS =====================
# Import du thÃ¨me global EduManager+
from resources.themes.theme import *

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# Utilisation des couleurs du nouveau thÃ¨me EduManager+
BG_MAIN     = BG_MAIN      # "#0A192F" - Fond principal
BG_SIDEBAR  = BG_SIDEBAR   # "#0E1C36" - Fond sidebar
HEADER_BG   = CARD_BG      # "#0b1d34" - Fond des cartes
CARD_BG     = CARD_BG      # "#0b1d34" - Fond des cartes
CARD_INNER  = BORDER_COLOR # "#1f3b5a" - IntÃ©rieur des cartes
BORDER_COLOR= BORDER_COLOR # "#1f3b5a" - Bordures

ACCENT      = ACCENT       # "#64FFDA" - Accent cyan
OK          = SUCCESS_GREEN # "#22c55e" - Vert succÃ¨s
WARN        = WARNING_YELLOW # "#FFD700" - Jaune avertissement
DANGER      = ERROR_RED     # "#FF6363" - Rouge erreur
TEXT        = TEXT          # "#E2E8F0" - Texte principal
MUTED       = MUTED         # "#8aa0b8" - Texte secondaire

HOVER       = HOVER_PRIMARY # "#16365b" - Couleur de survol
ACTIVE      = HOVER_SECONDARY # "#133052" - Couleur active
GLOW        = ACCENT        # "#1aa3a3" - Effet de lueur

FONT        = FONT_PRIMARY[0]  # "Segoe UI" - Police principale
FS_TITLE    = FONT_TITLE[1]    # 32 - Taille titre
FS_HEADER   = FONT_SUBTITLE[1] # 22 - Taille header
FS_SUBHDR   = FONT_CARD_TITLE[1] # 16 - Taille sous-header
FS_TEXT     = FONT_SECONDARY[1] # 13 - Taille texte
FS_VALUE    = FONT_METRIC[1]    # 30 - Taille valeur

# =================== ICONES : PIL cache local + pool CTkImage =====================
_DASHBOARD_PIL_CACHE = {}   # name -> PIL.Image (liÃ© au chemin)
_DASHBOARD_IMG_POOL = set() # rÃ©fÃ©rences CTkImage Ã  garder vivantes dans CE root

def _load_dashboard_pil_icon(name: str):
    """Charge une icÃ´ne PIL.Image (RGBA) depuis le systÃ¨me centralisÃ©."""
    # Utiliser le systÃ¨me centralisÃ©
    icon_path = get_icon_path(name)
    
    if not icon_exists(name):
        print(f"âš ï¸ IcÃ´ne '{name}' non trouvÃ©e: {icon_path}")
        return None
        
    if name in _DASHBOARD_PIL_CACHE:
        return _DASHBOARD_PIL_CACHE[name]
    try:
        im = Image.open(icon_path).convert("RGBA")
        _DASHBOARD_PIL_CACHE[name] = im
        print(f"âœ… IcÃ´ne '{name}' chargÃ©e: {icon_path}")
        return im
    except Exception as e:
        print(f"âš ï¸ Erreur chargement icÃ´ne {name}: {e}")
        return None

def get_icon(name: str, size=(24, 24)):
    """
    CrÃ©e un CTkImage pour le root courant Ã  partir du cache PIL local.
    Conserve la rÃ©fÃ©rence dans _DASHBOARD_IMG_POOL pour Ã©viter le GC.
    Utilise le systÃ¨me centralisÃ© d'icÃ´nes.
    """
    pil = _load_dashboard_pil_icon(name)
    if not pil:
        return None
    cimg = ctk.CTkImage(light_image=pil, dark_image=pil, size=size)
    _DASHBOARD_IMG_POOL.add(cimg)
    return cimg

# Permet au Login de purger proprement ces caches avant instanciation
# (utilisÃ© par reset_ctk_image_caches_dashboard du login)
# _DASHBOARD_PIL_CACHE.clear() et _DASHBOARD_IMG_POOL.clear() seront appelÃ©s cÃ´tÃ© login.

# =================== HELPERS couleurs/texte/graphe =====================
def _hex_to_rgb(h: str):
    h = h.lstrip("#")
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))

def hex_to_rgb(hex_color):
    """Convertit une couleur hex en RGB."""
    return _hex_to_rgb(hex_color)

def _rgb_to_hex(rgb):
    return "#%02x%02x%02x" % rgb

def lighten(hex_color: str, amt: float = 0.35):
    r, g, b = _hex_to_rgb(hex_color)
    r = int(r + (255 - r) * amt)
    g = int(g + (255 - g) * amt)
    b = int(b + (255 - b) * amt)
    return _rgb_to_hex((min(255, r), min(255, g), min(255, b)))

def darken(hex_color: str, amt: float = 0.25):
    r, g, b = _hex_to_rgb(hex_color)
    r = int(r * (1 - amt))
    g = int(g * (1 - amt))
    b = int(b * (1 - amt))
    return _rgb_to_hex((max(0, r), max(0, g), max(0, b)))

def shorten(text: str, n: int = 12) -> str:
    return text if len(text) <= n else text[:n-1] + "â€¦"

def draw_vertical_gradient_bar(cnv, x, y, w, h, base_color, steps=28, radius=6):
    """Dessine une barre Ã  dÃ©gradÃ© vertical (clair->foncÃ©) avec petite coiffe arrondie."""
    if h <= 0 or w <= 0:
        return []
    items = []
    top = y
    slice_h = max(1, int(h / steps))
    for i in range(steps):
        yy = top + i * slice_h
        t = i / max(1, steps - 1)
        col = darken(lighten(base_color, 0.55), 0.35 * t)
        items.append(cnv.create_rectangle(x, yy, x + w, min(y + h, yy + slice_h),
                                          outline=col, fill=col, width=0))
    cap = lighten(base_color, 0.45)
    items.append(cnv.create_arc(x, y - radius*2, x + 2*radius, y + radius*2,
                                start=90, extent=90, style="pieslice",
                                outline=cap, fill=cap, width=0))
    items.append(cnv.create_arc(x + w - 2*radius, y - radius*2, x + w, y + radius*2,
                                start=0, extent=90, style="pieslice",
                                outline=cap, fill=cap, width=0))
    items.append(cnv.create_rectangle(x + radius, y - radius, x + w - radius, y + radius,
                                      outline=cap, fill=cap, width=0))
    border = darken(base_color, 0.4)
    items.append(cnv.create_rectangle(x, y, x + w, y + h, outline=border, width=1))
    return items

# =================== MAPPING ICONES / ACTIONS =====================
ICON_MAP = {
    "dashboard": "home", "eleves": "eleve", "utilisateurs": "group",
    "person": "person", "classes": "class", "profs": "person",
    "salles": "classroom", "logout": "logout", "presences": "check",
    "notes": "grade", "bulletins": "stats", "paiements": "transfer",
    "refresh": "refresh", "search": "search",
    "enseignements": "book", "matieres": "assignment",
    "emplois": "clock", "calendar": "calendar", "clock": "clock",
    "actualites": "newspaper", "annonces": "megaphone", "notifications": "bell",
    "taches": "check_circle", "biblio": "book", "calendriers": "calendar",
    "carrieres": "briefcase", "messagerie": "email", "settings": "settings",
}

ACTIONS = [
    ("ActualitÃ©s", "actualites"),
    ("Annonces", "annonces"),
    ("Notifications", "notifications"),
    ("TÃ¢ches", "taches"),
    ("BibliothÃ¨que", "biblio"),
    ("Calendriers", "calendriers"),
    ("CarriÃ¨res", "carrieres"),
    ("Messagerie", "messagerie"),
    ("ParamÃ¨tres", "settings"),
]

# =================== PLACEHOLDER (si vue manquante) =====================
class PlaceholderView(ctk.CTkFrame):
    def __init__(self, master, title):
        super().__init__(master, fg_color="transparent")
        ctk.CTkLabel(self, text=title, font=(FONT, FS_TITLE, "bold"), text_color=TEXT)\
            .pack(pady=10, padx=10)
        ctk.CTkLabel(self, text="Contenu Ã  venir...", font=(FONT, FS_TEXT), text_color=MUTED)\
            .pack(padx=10, pady=5)

# =================== IMPORT CENTRALISÃ‰ DES VUES =====================
print("ðŸ” Enregistrement des vues centralisÃ©es...")

# Enregistrer toutes les vues automatiquement
register_all_views()

# RÃ©cupÃ©rer le registre de vues
view_registry = get_view_registry()

# Mapping des vues avec leurs noms dans le systÃ¨me
VIEW_MAPPING = {
    # Vues acadÃ©miques
    "eleves": "eleves_dashboard",
    "profs": "professeurs", 
    "classes": "classes",
    "enseignements": "enseignements",
    "matieres": "matieres",
    "notes": "notes",
    "presences": "presences",
    "bulletins": "bulletins",
    "emplois": "emplois",
    
    # Vues administratives
    "salles": "salles",
    "paiements": "paiements",
    "utilisateurs": "utilisateurs",
    "taches": "taches",
    "carrieres": "carrieres",
    
    # Vues de communication
    "actualites": "actualites",
    "annonces": "annonces",
    "notifications": "notifications",
    "bibliotheque": "bibliotheque",
    "messagerie": "messagerie",
    "calendriers": "calendriers",
}

# Fonction pour rÃ©cupÃ©rer une vue avec fallback
def get_view_with_fallback(view_key):
    """RÃ©cupÃ¨re une vue avec fallback vers placeholder"""
    view_name = VIEW_MAPPING.get(view_key, view_key)
    view_class = view_registry.get_view(view_name)
    
    if view_class:
        return view_class
    else:
        print(f"âš ï¸ Vue '{view_key}' non trouvÃ©e, utilisation du placeholder")
        return view_registry.create_placeholder_view(view_key)

# RÃ©cupÃ©ration des vues principales - Utilisation directe du registre
view_registry = get_view_registry()
ElevesView = view_registry.views.get("eleves")
ProfessorsDashboard = view_registry.views.get("professeurs")
# Import direct de la vue des classes
try:
    from src.modules.academic.classes.views.classes_view import ClassesManagerView
    print("âœ… Vue 'classes' importÃ©e directement: ClassesManagerView")
except ImportError as e:
    print(f"âš ï¸ Erreur import classes: {e}")
    ClassesManagerView = None
EnseignementsView = view_registry.views.get("enseignements")
SallesView = view_registry.views.get("salles")
UtilisateursView = view_registry.views.get("utilisateurs")
MatieresView = view_registry.views.get("matieres")
NotesView = view_registry.views.get("notes")
PresenceView = view_registry.views.get("presences")
PaiementsView = view_registry.views.get("paiements")
BulletinsView = view_registry.views.get("bulletins")
EmploisView = view_registry.views.get("emplois")

# VÃ©rification et affichage des vues importÃ©es
print("ðŸ” VÃ©rification des vues importÃ©es:")
for name, view_class in [
    ("eleves", ElevesView), ("profs", ProfessorsDashboard), ("classes", ClassesManagerView),
    ("enseignements", EnseignementsView), ("salles", SallesView), ("utilisateurs", UtilisateursView),
    ("matieres", MatieresView), ("notes", NotesView), ("presences", PresenceView),
    ("paiements", PaiementsView), ("bulletins", BulletinsView), ("emplois", EmploisView)
]:
    if view_class:
        print(f"âœ… Vue '{name}' importÃ©e: {view_class.__name__}")
    else:
        print(f"âš ï¸ Vue '{name}' non trouvÃ©e, utilisation du placeholder")

# Vues de communication
ActualitesView = view_registry.views.get("actualites")
AnnoncesView = view_registry.views.get("annonces")
NotificationsView = view_registry.views.get("notifications")
BibliothequeView = view_registry.views.get("bibliotheque")

# VÃ©rification des vues de communication
print("ðŸ” VÃ©rification des vues de communication:")
for name, view_class in [
    ("actualites", ActualitesView), ("annonces", AnnoncesView), 
    ("notifications", NotificationsView), ("bibliotheque", BibliothequeView)
]:
    if view_class:
        print(f"âœ… Vue '{name}' importÃ©e: {view_class.__name__}")
    else:
        print(f"âš ï¸ Vue '{name}' non trouvÃ©e, utilisation du placeholder")
MessagerieView = view_registry.views.get("messagerie")
TachesView = view_registry.views.get("taches")
CalendriersView = view_registry.views.get("calendriers")
CarrieresView = view_registry.views.get("carrieres")

# VÃ©rification des vues administratives
print("ðŸ” VÃ©rification des vues administratives:")
for name, view_class in [
    ("messagerie", MessagerieView), ("taches", TachesView), 
    ("calendriers", CalendriersView), ("carrieres", CarrieresView)
]:
    if view_class:
        print(f"âœ… Vue '{name}' importÃ©e: {view_class.__name__}")
    else:
        print(f"âš ï¸ Vue '{name}' non trouvÃ©e, utilisation du placeholder")

print(f"âœ… {len(view_registry.get_all_views())} vues chargÃ©es avec succÃ¨s")

# =================== UI HELPERS (cartes) =====================
def stat_card(parent, title, value, icon_key, color, ratio=0.0):
    """Carte stat compacte (taille rÃ©duite pour laisser plus d'espace au graphique)."""
    CARDBG = CARD_BG
    wrap = ctk.CTkFrame(parent, fg_color=CARDBG, corner_radius=12, border_width=1, border_color=BORDER_COLOR)
    wrap.grid_columnconfigure(0, weight=1)

    header = ctk.CTkFrame(wrap, fg_color="transparent")
    header.pack(fill="x", padx=8, pady=(6, 4))

    badge = ctk.CTkFrame(header, fg_color=CARD_INNER, corner_radius=999, width=32, height=32,
                         border_width=1, border_color=BORDER_COLOR)
    badge.pack_propagate(False); badge.pack(side="left")

    icon_img = get_icon(ICON_MAP.get(icon_key, "home"), (16, 16))
    if icon_img:
        lbl = ctk.CTkLabel(badge, text="", image=icon_img, text_color=color)
        lbl._imgref = icon_img
        lbl.pack(expand=True)

    ctk.CTkLabel(header, text=title, font=(FONT, 10, "bold"), text_color=MUTED)\
        .pack(side="left", padx=8)

    ctk.CTkLabel(wrap, text=str(value), font=(FONT, 18, "bold"), text_color=TEXT)\
        .pack(anchor="w", padx=10)
    ctk.CTkLabel(wrap, text="Temps rÃ©el", font=(FONT, 9), text_color=MUTED)\
        .pack(anchor="w", padx=10, pady=(0, 6))

    pb_bg = ctk.CTkFrame(wrap, fg_color=CARD_INNER, corner_radius=8, height=8, border_width=1, border_color=BORDER_COLOR)
    pb_bg.pack(fill="x", padx=8, pady=(2, 8))
    pb_fg = ctk.CTkFrame(pb_bg, fg_color=color, corner_radius=8, height=6)
    pb_fg.place(relx=0, rely=0.5, anchor="w", relwidth=max(0.05, min(1.0, ratio)), relheight=0.7)

    def _enter(_): wrap.configure(border_color=GLOW)
    def _leave(_): wrap.configure(border_color=BORDER_COLOR)
    wrap.bind("<Enter>", _enter); wrap.bind("<Leave>", _leave)
    for w in wrap.winfo_children():
        w.bind("<Enter>", _enter); w.bind("<Leave>", _leave)
    return wrap

def action_card(parent, label, key, icon_key, command=None):
    card = ctk.CTkFrame(parent, fg_color=CARD_BG, corner_radius=12, border_width=1, border_color=BORDER_COLOR, width=110, height=86)
    card.pack_propagate(False)
    icon = get_icon(ICON_MAP.get(icon_key, "home"), (22, 22))
    if icon:
        ilb = ctk.CTkLabel(card, text="", image=icon, text_color=ACCENT)
        ilb._imgref = icon
        ilb.pack(pady=(8, 2))
    ctk.CTkLabel(card, text=label, font=(FONT, 11, "bold"), text_color=TEXT, wraplength=90, justify="center").pack()
    def e(_): card.configure(border_color=ACCENT, fg_color=HOVER)
    def l(_): card.configure(border_color=BORDER_COLOR, fg_color=CARD_BG)
    if command:
        card.bind("<Button-1>", lambda e: command(key))
        for w in card.winfo_children(): w.bind("<Button-1>", lambda e: command(key))
    card.bind("<Enter>", e); card.bind("<Leave>", l)
    for w in card.winfo_children(): w.bind("<Enter>", e); w.bind("<Leave>", l)
    return card

# =================== IMPORT DU WIDGET DE GRAPHIQUE SIMPLE =====================
from .chart_widget import SimpleChartWidget

# =================== FONCTION POUR CALCULER LES MOYENNES =====================
def calculate_real_averages():
    """Calcule les vraies moyennes par matiÃ¨re depuis la base de donnÃ©es"""
    # DonnÃ©es par dÃ©faut rÃ©alistes
        default_labels = ["MathÃ©matiques", "FranÃ§ais", "Anglais", "Histoire-GÃ©o", "Sciences", "Sport"]
        default_points = [78.5, 82.3, 71.2, 85.7, 79.1, 88.9]
        
        conn = get_conn()
        if not conn:
        print("âš ï¸ Pas de connexion DB, utilisation des donnÃ©es par dÃ©faut")
            return default_labels, default_points
        
        try:
            cur = conn.cursor()
            
            # VÃ©rifier si les tables existent
            if not table_exists(conn, "notes") or not table_exists(conn, "matieres"):
            print("âš ï¸ Tables notes/matieres non trouvÃ©es, utilisation des donnÃ©es par dÃ©faut")
                return default_labels, default_points
            
        # Calculer les moyennes par matiÃ¨re
            cur.execute("""
            SELECT m.nom_matiere, AVG(n.note) as moyenne
                FROM notes n
                JOIN matieres m ON n.id_matiere = m.id_matiere
                WHERE n.note IS NOT NULL AND n.note > 0
                GROUP BY m.id_matiere, m.nom_matiere
                ORDER BY moyenne DESC
                LIMIT 6
            """)
            
            results = cur.fetchall()
            
            if not results:
            print("âš ï¸ Aucune note trouvÃ©e, utilisation des donnÃ©es par dÃ©faut")
                return default_labels, default_points
            
            labels = []
            data_points = []
            
            for row in results:
                if isinstance(row, sqlite3.Row):
                    labels.append(row["nom_matiere"])
                    data_points.append(round(float(row["moyenne"]), 1))
                else:
                    labels.append(row[0])
                    data_points.append(round(float(row[1]), 1))
            
            # S'assurer qu'on a au moins 3 Ã©lÃ©ments
            if len(labels) < 3:
            print("âš ï¸ Pas assez de donnÃ©es, utilisation des donnÃ©es par dÃ©faut")
                return default_labels, default_points
            
            print(f"âœ… Moyennes calculÃ©es: {len(labels)} matiÃ¨res")
            return labels[:6], data_points[:6]
            
        except Exception as e:
            print(f"âš ï¸ Erreur calcul moyennes: {e}")
            return default_labels, default_points
        finally:
            try:
                conn.close()
            except:
                pass
    
