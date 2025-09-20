# -*- coding: utf-8 -*-
"""
EduManager+ - Tableau de bord principal (CustomTkinter, thème sombre)
- Graphique amélioré "Moyenne par matière (Tendance)" avec effets visuels premium
"""

# Import du système centralisé
from database.connection import get_db_connection
import sys
import os

# Ajouter le chemin racine au sys.path
root_path = os.path.join(os.path.dirname(__file__), "..", "..", "..", "..")
if root_path not in sys.path:
    sys.path.insert(0, root_path)

# Import du système centralisé
from src.core.paths import (
    DATABASE_PATH, ICONS_PATH, THEME_PATH, 
    get_icon_path, icon_exists,
    print_paths
)
from src.core.view_registry import get_view_registry, register_all_views

# Import du système d'optimisation
try:
    from src.core.database.optimized_queries import get_optimized_query_manager
    print("✅ Système d'optimisation importé")
except ImportError as e:
    print(f"⚠️ Système d'optimisation non disponible: {e}")

# Fonctions utilitaires pour les chemins (compatibilité)
def get_db_path():
    """Retourne le chemin vers la base de données (compatibilité)"""
    return DATABASE_PATH

def get_icons_dir():
    """Retourne le chemin vers le dossier des icônes (compatibilité)"""
    return ICONS_PATH

import math
import datetime
# Remplacé par SQL Server  # Remplacé par SQL Server
import tkinter as tk
from tkinter import messagebox
import customtkinter as ctk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd
from PIL import Image, ImageDraw
import numpy as np

# =================== CHEMINS CENTRALISÉS =====================
# Affichage des chemins centralisés
print_paths()

# DB - Utilise la base de données centralisée
DB_PATH = DATABASE_PATH
print(">>> Fichier DB utilisé :", DB_PATH)

# ICÔNES - Chemin centralisé
ICONS_DIR = ICONS_PATH
print(">>> Dossier icônes utilisé :", ICONS_DIR)

# =================== SQLITE HELPERS CENTRALISÉS =====================
def get_conn():
    """Utilise la connexion centralisée à la base de données"""
    try:
        from database.connection import get_db_connection
        return get_db_connection()
    except ImportError:
        print("⚠️ Impossible d'importer get_db_connection")
        return None

def table_exists(conn, name):
    try:
        cur = conn.cursor()
        cur.execute(
            "SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = ?",
            (name,),
        )
        return cur.fetchone() is not None
    except Exception:
        return False

def get_stats_count_any(*table_candidates) -> int:
    """Renvoie COUNT(*) pour la première table existante parmi table_candidates."""
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
        return int((r[0] if not isinstance(r, dict) else r[0]) or 0)
    except Exception as e:
        print(f"⚠️ get_stats_count_any: {e}")
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
            SELECT c.nom_classe AS classes, COUNT(e.id_eleve) AS nb
            FROM classes c
            LEFT JOIN eleves e ON e.id_classe = c.id_classe
            GROUP BY c.id_classe, c.nom_classe
            ORDER BY nb DESC, classes ASC
            OFFSET 0 ROWS FETCH NEXT ? ROWS ONLY
        """, (limit,))
        rows = cur.fetchall()
        out = []
        for r in rows:
            if isinstance(r, dict):
                out.append((r["classes"], int(r["nb"] or 0)))
            else:
                out.append((r[0], int(r[1] or 0)))
        return out
    except Exception as e:
        print("⚠️ fetch_effectifs_par_classe:", e)
        return []
    finally:
        try:
            conn.close()
        except:
            pass

# =================== THÈME / COULEURS =====================
# Import du thème global EduManager+
from resources.themes.theme import *

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# Utilisation des couleurs du nouveau thème EduManager+
BG_MAIN     = BG_MAIN      # "#0A192F" - Fond principal
BG_SIDEBAR  = BG_SIDEBAR   # "#0E1C36" - Fond sidebar
HEADER_BG   = CARD_BG      # "#0b1d34" - Fond des cartes
CARD_BG     = CARD_BG      # "#0b1d34" - Fond des cartes
CARD_INNER  = BORDER_COLOR # "#1f3b5a" - Intérieur des cartes
BORDER_COLOR= BORDER_COLOR # "#1f3b5a" - Bordures

ACCENT      = ACCENT       # "#64FFDA" - Accent cyan
OK          = SUCCESS_GREEN # "#22c55e" - Vert succès
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

# =================== ICONES : PIL local + pool CTkImage =====================
_DASHBOARD_PIL_CACHE = {}  # name -> PIL.Image (lié au chemin)
_DASHBOARD_IMG_POOL = set() # références CTkImage à garder vivantes dans CE root

def _load_dashboard_pil_icon(name: str):
    """Charge une icône PIL.Image (RGBA) depuis le système centralisé."""
    # Utiliser le système centralisé
    icon_path = get_icon_path(name)
    
    if not icon_exists(name):
        print(f"⚠️ Icône '{name}' non trouvée: {icon_path}")
        return None
        
    if name in _DASHBOARD_PIL_CACHE:
        return _DASHBOARD_PIL_CACHE[name]
    try:
        im = Image.open(icon_path).convert("RGBA")
        _DASHBOARD_PIL_CACHE[name] = im
        print(f"✅ Icône '{name}' chargée: {icon_path}")
        return im
    except Exception as e:
        print(f"⚠️ Erreur chargement icône {name}: {e}")
        return None

def get_icon(name: str, size=(24, 24)):
    """
    Crée un CTkImage pour le root courant à partir du PIL local.
    Conserve la référence dans _DASHBOARD_IMG_POOL pour éviter le GC.
    Utilise le système centralisé d'icônes.
    """
    pil = _load_dashboard_pil_icon(name)
    if not pil:
        return None
    cimg = ctk.CTkImage(light_image=pil, dark_image=pil, size=size)
    _DASHBOARD_IMG_POOL.add(cimg)
    return cimg

# Permet au Login de purger proprement ces images avant instanciation
# (utilisé par reset_ctk_image_caches_dashboard du login)
# _DASHBOARD_PIL_CACHE.clear() et _DASHBOARD_IMG_POOL.clear() seront appelés côté login.

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
    return text if len(text) <= n else text[:n-1] + "…"

def draw_vertical_gradient_bar(cnv, x, y, w, h, base_color, steps=28, radius=6):
    """Dessine une barre à dégradé vertical (clair->foncé) avec petite coiffe arrondie."""
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
    ("Actualités", "actualites"),
    ("Annonces", "annonces"),
    ("Notifications", "notifications"),
    ("Tâches", "taches"),
    ("Bibliothèque", "biblio"),
    ("Calendriers", "calendriers"),
    ("Carrières", "carrieres"),
    ("Messagerie", "messagerie"),
    ("Paramètres", "settings"),
]

# =================== PLACEHOLDER (si vue manquante) =====================
class PlaceholderView(ctk.CTkFrame):
    def __init__(self, master, title):
        super().__init__(master, fg_color="transparent")
        ctk.CTkLabel(self, text=title, font=(FONT, FS_TITLE, "bold"), text_color=TEXT)\
            .pack(pady=10, padx=10)
        ctk.CTkLabel(self, text="Contenu à venir...", font=(FONT, FS_TEXT), text_color=MUTED)\
            .pack(padx=10, pady=5)

# =================== IMPORT CENTRALISÉ DES VUES =====================
print("🔍 Enregistrement des vues centralisées...")

# Enregistrer toutes les vues automatiquement
register_all_views()

# Récupérer le registre de vues
view_registry = get_view_registry()

# Mapping des vues avec leurs noms dans le système
VIEW_MAPPING = {
    # Vues académiques
    "eleves": "eleves_dashboard",
    "profs": "professeurs", 
    "classes": "classes",
    "cours": "cours",
    "enseignements": "enseignements",  # Compatibilité
    "emplois": "emplois",  # Compatibilité
    "matieres": "matieres",
    "notes": "notes",
    "presences": "presences",
    "bulletins": "bulletins",
    
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

# Fonction pour récupérer une vue avec fallback
def get_view_with_fallback(view_key):
    """Récupère une vue avec fallback vers placeholder"""
    view_name = VIEW_MAPPING.get(view_key, view_key)
    view_class = view_registry.get_view(view_name)
    
    if view_class:
        return view_class
    else:
        print(f"⚠️ Vue '{view_key}' non trouvée, utilisation du placeholder")
        return view_registry.create_placeholder_view(view_key)

# Récupération des vues principales - Utilisation directe du registre
view_registry = get_view_registry()
ElevesView = view_registry.views.get("eleves")
ProfessorsDashboard = view_registry.views.get("professeurs")
# Import direct de la vue des classes
try:
    from src.modules.academic.classes.views.classes_view import ClassesManagerView
    print("✅ Vue 'classes' importée directement: ClassesManagerView")
except ImportError as e:
    print(f"⚠️ Erreur import classes: {e}")
    ClassesManagerView = None
# Import de la nouvelle vue unifiée des cours
from src.modules.academic.classes.views.cours_view import CoursManagerView
EnseignementsView = CoursManagerView  # Alias pour compatibilité
EmploisView = CoursManagerView  # Alias pour compatibilité

SallesView = view_registry.views.get("salles")
UtilisateursView = view_registry.views.get("utilisateurs")
MatieresView = view_registry.views.get("matieres")
NotesView = view_registry.views.get("notes")
# Import de la nouvelle vue avancée des présences
try:
    from src.modules.academic.attendance.views.advanced_attendance_view import AdvancedAttendanceView
    PresenceView = AdvancedAttendanceView
    print("✅ Vue avancée des présences importée")
except ImportError as e:
    print(f"⚠️ Vue avancée des présences non disponible: {e}")
    PresenceView = view_registry.views.get("presences")
PaiementsView = view_registry.views.get("paiements")
BulletinsView = view_registry.views.get("bulletins")

# Vérification et affichage des vues importées
print("🔍 Vérification des vues importées:")
for name, view_class in [
    ("eleves", ElevesView), ("profs", ProfessorsDashboard), ("classes", ClassesManagerView),
    ("enseignements", EnseignementsView), ("emplois", EmploisView), ("salles", SallesView), 
    ("utilisateurs", UtilisateursView), ("matieres", MatieresView), ("notes", NotesView), 
    ("presences", PresenceView), ("paiements", PaiementsView), ("bulletins", BulletinsView)
]:
    if view_class:
        print(f"✅ Vue '{name}' importée: {view_class.__name__}")
    else:
        print(f"⚠️ Vue '{name}' non trouvée, utilisation du placeholder")

# Vues de communication
ActualitesView = view_registry.views.get("actualites")
AnnoncesView = view_registry.views.get("annonces")
NotificationsView = view_registry.views.get("notifications")
BibliothequeView = view_registry.views.get("bibliotheque")

# Vérification des vues de communication
print("🔍 Vérification des vues de communication:")
for name, view_class in [
    ("actualites", ActualitesView), ("annonces", AnnoncesView), 
    ("notifications", NotificationsView), ("bibliotheque", BibliothequeView)
]:
    if view_class:
        print(f"✅ Vue '{name}' importée: {view_class.__name__}")
    else:
        print(f"⚠️ Vue '{name}' non trouvée, utilisation du placeholder")
MessagerieView = view_registry.views.get("messagerie")
TachesView = view_registry.views.get("taches")
CalendriersView = view_registry.views.get("calendriers")
CarrieresView = view_registry.views.get("carrieres")

# Vérification des vues administratives
print("🔍 Vérification des vues administratives:")
for name, view_class in [
    ("messagerie", MessagerieView), ("taches", TachesView), 
    ("calendriers", CalendriersView), ("carrieres", CarrieresView)
]:
    if view_class:
        print(f"✅ Vue '{name}' importée: {view_class.__name__}")
    else:
        print(f"⚠️ Vue '{name}' non trouvée, utilisation du placeholder")

print(f"✅ {len(view_registry.get_all_views())} vues chargées avec succès")

# =================== UI HELPERS (cartes) =====================
def stat_card(parent, title, value, icon_key, color, ratio=0.0):
    """Carte stat compacte (taille réduite pour laisser plus d'espace au graphique)."""
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
    ctk.CTkLabel(wrap, text="Temps réel", font=(FONT, 9), text_color=MUTED)\
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

# =================== GRAPHIQUE ULTRA MODERNE =====================
class UltraModernGraphFrame(ctk.CTkFrame):
    """Frame moderne pour le graphique avec matplotlib comme le dashboard des élèves"""
    
    def __init__(self, parent, width, height, **kwargs):
        super().__init__(parent, **kwargs)
        self.width = width
        self.height = height
        self.configure(fg_color=CARD_BG, corner_radius=20, border_width=2, border_color=BORDER_COLOR)
        
        # Calculer les vraies moyennes depuis la base de données
        self.labels, self.data_points = self.calculate_real_averages()
        
        self.setup_ui()
        self.create_matplotlib_chart()
    
    def setup_ui(self):
        """Configure l'interface utilisateurs"""
        # Titre du graphique avec icône analytics
        title_frame = ctk.CTkFrame(self, fg_color="transparent")
        title_frame.pack(fill="x", padx=20, pady=(15, 5))
        
        # Icône analytics
        try:
            analytics_icon = get_icon("analytics", (24, 24))
            if analytics_icon:
                icon_label = ctk.CTkLabel(title_frame, text="", image=analytics_icon)
                icon_label.pack(side="left", padx=(0, 10))
        except Exception as e:
            print(f"⚠️ Erreur chargement icône analytics: {e}")
        
        # Titre principal
        title_label = ctk.CTkLabel(
            title_frame, 
            text="📊 Taux de Réussite par Classe", 
            font=FONT_TITLE, 
            text_color=TEXT
        )
        title_label.pack(side="left")
        
        # Sous-titre
        subtitle_label = ctk.CTkLabel(
            self, 
            text="Performance académique par classes avec taux de réussite global", 
            font=FONT_SMALL, 
            text_color=MUTED
        )
        subtitle_label.pack(pady=(0, 10))
    
    def create_matplotlib_chart(self):
        """Crée le graphique avec matplotlib et pandas pour une meilleure gestion des données"""
        # Création du DataFrame pandas pour une meilleure gestion des données
        df = pd.DataFrame({
            'Matiere': self.labels,
            'Moyenne': self.data_points
        })
        
        # Ajouter des colonnes calculées avec pandas
        df['Niveau'] = df['Moyenne'].apply(lambda x: 
            'Excellent' if x >= 80 else 
            'Bon' if x >= 70 else 
            'Moyen' if x >= 60 else 'Faible')
        
        df['Couleur'] = df['Moyenne'].apply(lambda x: 
            SUCCESS_GREEN if x >= 80 else 
            WARNING_YELLOW if x >= 70 else 
            "#FF6B35" if x >= 60 else ERROR_RED)
        
        df['Emoji'] = df['Moyenne'].apply(lambda x: 
            "🟢" if x >= 80 else 
            "🟡" if x >= 70 else 
            "🟠" if x >= 60 else "🔴")
        
        # Création du graphique en barres avec matplotlib (taille adaptée pour toutes les classes)
        fig = plt.Figure(figsize=(12, 7), dpi=100)
        ax = fig.add_subplot(111)
        
        # Ajuster les marges pour éviter la coupure (plus d'espace pour toutes les classes)
        fig.subplots_adjust(bottom=0.4, top=0.85, left=0.1, right=0.95)
        
        # Données pour le graphique
        x_pos = range(len(df))
        
        # Mapping des classes avec leurs icônes
        classe_icons = {
            "6°": "graduation",
            "5°": "graduation", 
            "4°": "graduation",
            "3°": "graduation",
            "2°": "graduation",
            "1°": "graduation",
            "TSE": "science",
            "TSM": "science",
            "TSS": "science"
        }
        
        # Graphique en barres avec couleurs du taux de réussite (utilisant pandas)
        bars = ax.bar(x_pos, df['Moyenne'], color=df['Couleur'], alpha=0.8, 
                     edgecolor=TEXT, linewidth=2, width=0.5)
        
        # Ajouter des valeurs sur les barres avec pandas (plus efficace)
        for i, row in df.iterrows():
            if row['Moyenne'] > 0:
                # Valeur avec statut positionnée à gauche de la barre
                ax.annotate(f"{row['Moyenne']:.1f}% {row['Emoji']}", 
                           (i, row['Moyenne']), textcoords="offset points", 
                           xytext=(-15, 10), ha='left', va='bottom', 
                           color=TEXT, fontweight='bold', fontsize=8,
                           bbox=dict(boxstyle="round,pad=0.3", facecolor=CARD_BG, 
                                   edgecolor=row['Couleur'], alpha=0.9))
        
        # Afficher les détails des classes dans la console
        print(f"\n📋 Détail des taux de réussite par classes:")
        print("-" * 50)
        for _, row in df.iterrows():
            print(f"{row['Matiere']:>8}: {row['Moyenne']:>5.1f}% {row['Emoji']} ({row['Niveau']})")
        
        # Configuration des axes avec plus d'espace et icônes (utilisant pandas)
        ax.set_xticks(x_pos)
        
        # Créer les labels avec icônes en utilisant pandas
        df['Icone'] = df['Matiere'].map(classe_icons).fillna('graduation')
        labels_with_icons = df.apply(lambda row: f"🎓 {row['Matiere']}", axis=1).tolist()
        
        ax.set_xticklabels(labels_with_icons, rotation=60, ha='right', color=TEXT, fontsize=9)
        ax.set_ylabel("Taux de Réussite (%)", color=TEXT, fontsize=11, fontweight='bold')
        ax.set_title("Taux de Réussite par Classe", color=TEXT, fontsize=14, fontweight='bold', pad=20)
        
        # Style des axes avec le thème
        ax.tick_params(axis='y', colors=TEXT, labelsize=10)
        ax.tick_params(axis='x', colors=TEXT, labelsize=10, pad=10)  # Plus d'espace pour les labels X
        ax.spines['bottom'].set_color(BORDER_COLOR)
        ax.spines['left'].set_color(BORDER_COLOR)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        
        # Fond du graphique
        ax.set_facecolor(CARD_BG)
        fig.patch.set_facecolor(CARD_BG)
        
        # Calculer le taux de réussite global
        taux_reussite = self.calculate_taux_reussite()
        
        # Ligne de moyenne avec position ajustée
        avg_value = sum(self.data_points) / len(self.data_points)
        ax.axhline(y=avg_value, color=TEXT, linestyle='--', linewidth=2, alpha=0.7)
        
        # Texte du taux de réussite positionné plus haut
        max_val = max(self.data_points)
        ax.text(len(self.labels)-1, max_val * 0.9, f'Taux de Réussite Global: {taux_reussite:.1f}%', 
                color=TEXT, fontweight='bold', fontsize=10, ha='right',
                bbox=dict(boxstyle="round,pad=0.3", facecolor=CARD_BG, 
                         edgecolor=BORDER_COLOR, alpha=0.9))
        
        # Légende des niveaux de réussite
        legend_elements = [
            plt.Rectangle((0,0),1,1, facecolor=SUCCESS_GREEN, alpha=0.8, label='Excellent (≥80%)'),
            plt.Rectangle((0,0),1,1, facecolor=WARNING_YELLOW, alpha=0.8, label='Bon (70-79%)'),
            plt.Rectangle((0,0),1,1, facecolor="#FF6B35", alpha=0.8, label='Moyen (60-69%)'),
            plt.Rectangle((0,0),1,1, facecolor=ERROR_RED, alpha=0.8, label='Faible (<60%)')
        ]
        ax.legend(handles=legend_elements, loc='upper left', 
                 frameon=True, facecolor=CARD_BG, edgecolor=BORDER_COLOR,
                 labelcolor=TEXT, fontsize=9)
        
        # Créer le canvas matplotlib
        canvas = FigureCanvasTkAgg(fig, self)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True, padx=10, pady=10)
        
        # Garder une référence
        self.fig = fig
        self.canvas = canvas
    
    def calculate_taux_reussite(self):
        """Calcule le taux de réussite global basé sur les moyennes avec pandas"""
        if not self.data_points:
            return 0
        
        # Créer un DataFrame temporaire pour le calcul
        df_temp = pd.DataFrame({'Moyenne': self.data_points})
        
        # Compter les matières avec une moyenne >= 70% (seuil de réussite) avec pandas
        matieres_reussies = (df_temp['Moyenne'] >= 70).sum()
        total_matieres = len(df_temp)
        
        # Calculer le pourcentage de réussite
        taux_reussite = (matieres_reussies / total_matieres) * 100
        
        return taux_reussite
    
    def calculate_real_averages(self):
        """Calcule les taux de réussite par classes depuis la base de données avec toutes les classes"""
        # Données par défaut pour toutes les classes avec abréviations (données réalistes)
        default_labels = ["6°", "5°", "4°", "3°", "2°", "1°", "7°", "8°", "9°", "10°", "11° SE", "11° SM", "11° SS", "12° SE", "12° SM", "12° SS", "TSE", "TSM", "TSS"]
        default_points = [78.5, 82.3, 75.8, 85.2, 79.1, 88.7, 76.4, 81.2, 77.9, 83.6, 79.8, 85.1, 72.3, 80.5, 84.7, 75.2, 87.3, 89.1, 76.8]
        
        print(f"🎯 Calcul du taux de réussite pour {len(default_labels)} classes...")
        print(f"📊 Classes: {default_labels}")
        print(f"📈 Taux: {default_points}")
        
        conn = get_conn()
        if not conn:
            print("⚠️ Pas de connexion DB, utilisation des données par défaut pour toutes les classes")
            
            # Calculer les statistiques pour les données par défaut
            excellent_classes = sum(1 for taux in default_points if taux >= 80)
            bon_classes = sum(1 for taux in default_points if 70 <= taux < 80)
            moyen_classes = sum(1 for taux in default_points if 60 <= taux < 70)
            faible_classes = sum(1 for taux in default_points if taux < 60)
            taux_reussite_global = sum(1 for taux in default_points if taux >= 70) / len(default_points) * 100
            
            print(f"📊 Statistiques (données par défaut):")
            print(f"   • Excellent (≥80%): {excellent_classes} classes")
            print(f"   • Bon (70-79%): {bon_classes} classes")
            print(f"   • Moyen (60-69%): {moyen_classes} classes")
            print(f"   • Faible (<60%): {faible_classes} classes")
            print(f"   • Taux de réussite global: {taux_reussite_global:.1f}%")
            
            return default_labels, default_points
        
        try:
            cur = conn.cursor()
            
            # Vérifier si les tables existent
            if not table_exists(conn, "classes") or not table_exists(conn, "eleves") or not table_exists(conn, "notes"):
                print("⚠️ Tables classes/eleves/notes non trouvées, utilisation des données par défaut")
                return default_labels, default_points
            
            # Requête pour calculer le taux de réussite par classes (toutes les classes)
            # Un élève réussit s'il a une moyenne >= 70% sur toutes ses matières
            cur.execute("""
                SELECT 
                    c.nom_classe,
                    COUNT(DISTINCT e.id_eleve) as total_eleves,
                    COUNT(DISTINCT CASE 
                        WHEN eleve_moyenne.moyenne_generale >= 10 THEN e.id_eleve 
                    END) as eleves_reussis,
                    ROUND(
                        (COUNT(DISTINCT CASE 
                            WHEN eleve_moyenne.moyenne_generale >= 10 THEN e.id_eleve 
                        END) * 100.0 / COUNT(DISTINCT e.id_eleve)), 1
                    ) as taux_reussite
                FROM classes c
                LEFT JOIN eleves e ON c.id_classe = e.id_classe
                LEFT JOIN (
                    SELECT 
                        n.id_eleve,
                        AVG(n.note) as moyenne_generale
                    FROM notes n
                    WHERE n.note IS NOT NULL AND n.note > 0
                    GROUP BY n.id_eleve
                ) eleve_moyenne ON e.id_eleve = eleve_moyenne.id_eleve
                WHERE c.statut = 'Active' AND e.statut = 'Actif'
                GROUP BY c.id_classe, c.nom_classe
                HAVING COUNT(DISTINCT e.id_eleve) > 0
                ORDER BY taux_reussite DESC
            """)
            
            results = cur.fetchall()
            
            if not results:
                print("⚠️ Aucune donnée de classes trouvée, utilisation des données par défaut")
                return default_labels, default_points
            
            labels = []
            data_points = []
            
            for row in results:
                if isinstance(row, dict):
                    # Appliquer les abréviations comme dans le dashboard des élèves
                    classe_name = row["nom_classe"]
                    classe_abbrev = self.get_classe_abbreviation(classe_name)
                    labels.append(classe_abbrev)
                    data_points.append(float(row["taux_reussite"]))
                else:
                    classe_name = row[0]
                    classe_abbrev = self.get_classe_abbreviation(classe_name)
                    labels.append(classe_abbrev)
                    data_points.append(float(row[3]))
            
            # S'assurer qu'on a au moins 3 éléments
            if len(labels) < 3:
                print("⚠️ Pas assez de données de classes, utilisation des données par défaut")
                return default_labels, default_points
            
            # Calculer les statistiques détaillées
            excellent_classes = sum(1 for taux in data_points if taux >= 80)
            bon_classes = sum(1 for taux in data_points if 70 <= taux < 80)
            moyen_classes = sum(1 for taux in data_points if 60 <= taux < 70)
            faible_classes = sum(1 for taux in data_points if taux < 60)
            taux_reussite_global = sum(1 for taux in data_points if taux >= 70) / len(data_points) * 100
            
            print(f"✅ Taux de réussite par classes calculés: {len(labels)} classes")
            print(f"📊 Statistiques:")
            print(f"   • Excellent (≥80%): {excellent_classes} classes")
            print(f"   • Bon (70-79%): {bon_classes} classes")
            print(f"   • Moyen (60-69%): {moyen_classes} classes")
            print(f"   • Faible (<60%): {faible_classes} classes")
            print(f"   • Taux de réussite global: {taux_reussite_global:.1f}%")
            
            return labels, data_points
            
        except Exception as e:
            print(f"❌ Erreur lors du calcul des taux de réussite par classes: {e}")
            return default_labels, default_points
        finally:
            try:
                conn.close()
            except:
                pass
    
    def get_classe_abbreviation(self, classe_name):
        """Convertit le nom complet de la classes en abréviation comme dans le dashboard des élèves"""
        abbreviations = {
            # PRIMAIRE
            "1° Année": "1°",
            "2° Année": "2°", 
            "3° Année": "3°",
            "4° Année": "4°",
            "5° Année": "5°",
            "6° Année": "6°",
            
            # COLLÈGE
            "7° Année": "7°",
            "8° Année": "8°",
            "9° Année": "9°",
            "10° Année (BEPC)": "10°",
            
            # LYCÉE
            "11° Sciences Exactes": "11° SE",
            "11° Sciences Mathématiques": "11° SM", 
            "11° Sciences Sociales": "11° SS",
            "12° Sciences Exactes": "12° SE",
            "12° Sciences Mathématiques": "12° SM",
            "12° Sciences Sociales": "12° SS",
            "Terminale Sciences Exactes": "TSE",
            "Terminale Sciences Mathématiques": "TSM",
            "Terminale Sciences Sociales": "TSS"
        }
        
        return abbreviations.get(classe_name, classe_name)

# =================== APPLICATION PRINCIPALE =====================
        # Titre du graphique avec style futuriste
        title_frame = ctk.CTkFrame(self, fg_color="transparent")
        title_frame.pack(fill="x", padx=25, pady=(20, 15))
        
        # Titre principal avec icône analytics et effet de brillance
        try:
            analytics_icon = get_icon("analytics", (28, 28))
            if analytics_icon:
                icon_label = ctk.CTkLabel(
                    title_frame, text="", image=analytics_icon,
                    text_color=self.colors['primary'], fg_color="transparent"
                )
                icon_label._imgref = analytics_icon
                icon_label.pack(side="left", padx=(0, 10))
        except:
            pass
        
        title_label = ctk.CTkLabel(
            title_frame, 
            text="Performance Académique Ultra-Moderne", 
            font=(FONT, 20, "bold"), 
            text_color=self.colors['primary']
        )
        title_label.pack(side="left")
        
        # Indicateur de statut en temps réel avec icône
        status_frame = ctk.CTkFrame(title_frame, fg_color="transparent")
        status_frame.pack(side="right")
        
        # Icône de temps réel
        try:
            clock_icon = get_icon("clock", (16, 16))
            if clock_icon:
                clock_label = ctk.CTkLabel(
                    status_frame, text="", image=clock_icon,
                    text_color=self.colors['primary'], fg_color="transparent"
                )
                clock_label._imgref = clock_icon
                clock_label.pack(side="left", padx=(0, 5))
        except:
            pass
        
        # Point de statut animé
        self.status_dot = ctk.CTkFrame(
            status_frame,
            fg_color=self.colors['primary'],
            corner_radius=5,
            width=10,
            height=10
        )
        self.status_dot.pack(side="left", padx=(0, 8))
        self.status_dot.pack_propagate(False)
        
        # Texte de statut
        status_text = ctk.CTkLabel(
            status_frame,
            text="Temps Réel",
            font=(FONT, 11, "bold"),
            text_color=self.colors['primary']
        )
        status_text.pack(side="left")
        
        # Canvas pour le graphique avec fond du thème EduManager+ et hauteur augmentée
        self.canvas = tk.Canvas(
            self, 
            width=self.width-30, 
            height=self.height-50, 
            bg=CARD_BG, 
            highlightthickness=0,
            relief="flat"
        )
        self.canvas.pack(padx=25, pady=(0, 15))
        
        # Tooltip avec couleurs du thème EduManager+
        self.tooltip = ctk.CTkLabel(
            self, 
            text="", 
            font=(FONT, 11, "bold"), 
            fg_color=BORDER_COLOR, 
            text_color=TEXT,
            corner_radius=12, 
            padx=15, 
            pady=8
        )
        
        # Bind events pour interactions avancées
        self.canvas.bind("<Motion>", self.on_motion)
        self.canvas.bind("<Leave>", self.on_leave)
        self.canvas.bind("<Button-1>", self.on_click)
        
        # Animation du point de statut
        self.animate_status_dot()
    
    def animate_status_dot(self):
        """Animation désactivée - ne fait rien"""
        pass
    
    def draw_graph(self):
        """Dessine le graphique ultra moderne avec effets 3D et animations"""
        self.canvas.delete("all")
        
        # Dimensions du canvas
        canvas_width = self.canvas.winfo_reqwidth()
        canvas_height = self.canvas.winfo_reqheight()
        
        # Marges optimisées avec plus d'espace pour les labels
        margin_x = 60
        margin_y = 20  # Espace en haut réduit
        margin_bottom = 280  # Plus d'espace en bas pour les labels
        graph_width = canvas_width - 2 * margin_x
        graph_height = canvas_height - margin_y - margin_bottom
        
        # Calcul des points avec animation
        self.points = []
        
        # Vérifier que nous avons des données
        if not self.data_points or len(self.data_points) == 0:
            self.data_points = [78.5, 82.3, 71.2, 85.7, 79.1, 88.9]
            self.labels = ["Mathématiques", "Français", "Anglais", "Histoire-Géo", "Sciences", "Sport"]
        
        max_val = max(self.data_points)
        min_val = min(self.data_points)
        val_range = max_val - min_val if max_val != min_val else 1
        
        # Animation des points avec effet de vague
        for i, value in enumerate(self.data_points):
            # Effet de vague pour l'animation
            wave_offset = math.sin(self.animation_step + i * 0.5) * 5
            animated_value = value + wave_offset
            
            x = margin_x + (i * graph_width) / (len(self.data_points) - 1)
            y = margin_y + graph_height - ((animated_value - min_val) / val_range) * graph_height
            self.points.append((x, y))
        
        # Dessiner le fond avec gradient ultra moderne
        self.draw_ultra_modern_background()
        
        # Dessiner la grille futuriste
        self.draw_futuristic_grid(margin_x, margin_y, graph_width, graph_height, min_val, max_val)
        
        # Dessiner la ligne principale avec effet néon 3D
        self.draw_3d_neon_line()
        
        # Dessiner les points avec effets 3D et brillance
        self.draw_3d_neon_points()
        
        # Dessiner les labels avec style futuriste et position optimisée pour l'espace augmenté
        self.draw_futuristic_labels(margin_x, margin_y + graph_height + 35)
        
        # Ajouter des effets de particules avancés
        self.draw_advanced_particle_effects()
        
        # Ajouter des effets de connexion entre points
        self.draw_connection_effects()
    
    def draw_ultra_modern_background(self):
        """Dessine un gradient avec les couleurs du thème EduManager+"""
        canvas_width = self.canvas.winfo_reqwidth()
        canvas_height = self.canvas.winfo_reqheight()
        
        # Gradient radial avec les couleurs du thème
        center_x, center_y = canvas_width // 2, canvas_height // 2
        max_radius = max(canvas_width, canvas_height) // 2
        
        for radius in range(0, max_radius, 5):
            ratio = radius / max_radius
            
            # Gradient du centre vers l'extérieur avec les couleurs du thème
            # Du fond principal vers le fond sidebar
            r = int(10 + (14 - 10) * ratio)  # BG_MAIN vers BG_SIDEBAR
            g = int(25 + (28 - 25) * ratio)
            b = int(47 + (54 - 47) * ratio)
            
            color = f"#{r:02x}{g:02x}{b:02x}"
            
            # Dessiner des cercles concentriques pour l'effet radial
            self.canvas.create_oval(
                center_x - radius, center_y - radius,
                center_x + radius, center_y + radius,
                fill=color, outline="", width=0
            )
    
    def draw_futuristic_grid(self, x1, y1, width, height, min_val, max_val):
        """Dessine une grille avec le thème EduManager+"""
        # Fond avec couleur du thème
        self.canvas.create_rectangle(x1, y1, x1 + width, y1 + height,
                                   fill=CARD_BG, outline="", width=0)
        
        # Lignes horizontales avec style du thème
        for i in range(8):
            y = y1 + (i * height) / 7
            
            # Ligne principale plus visible pour les valeurs importantes
            if i % 2 == 0:  # Lignes principales
                self.canvas.create_line(x1, y, x1 + width, y,
                                      fill=BORDER_COLOR, width=1.5)
            else:  # Lignes secondaires
                self.canvas.create_line(x1, y, x1 + width, y,
                                      fill=BG_SIDEBAR, width=1)

            # Valeurs sur l'axe Y avec style du thème
            val = min_val + (max_val - min_val) * (7 - i) / 7
            if i % 2 == 0:  # Seulement pour les lignes principales
                self.canvas.create_text(x1 - 20, y, text=f"{val:.0f}%",
                                      fill=TEXT, font=FONT_SMALL, anchor="e")

        # Lignes verticales avec couleur du thème
        for i in range(len(self.points)):
            x = self.points[i][0] if i < len(self.points) else x1 + (i * width) / (len(self.data_points) - 1)
            self.canvas.create_line(x, y1, x, y1 + height,
                                  fill=BORDER_COLOR, width=1)
    
    def draw_3d_neon_line(self):
        """Dessine les barres avec le thème EduManager+"""
        if len(self.points) < 1:
            return
            
        # Couleur principale pour les barres (accent cyan du thème)
        bar_color = ACCENT  # "#64FFDA"
        
        # Calculer la largeur des barres (plus compact)
        bar_width = 25
        
        # Dessiner les barres avec style du thème
        for i, (x, y) in enumerate(self.points):
            # Calculer les dimensions de la barre
            bar_height = y - self.graph_y1
            bar_x1 = x - bar_width // 2
            bar_y1 = y
            bar_x2 = x + bar_width // 2
            bar_y2 = self.graph_y1
            
            # Ombre de la barre pour la profondeur (couleur du thème)
            self.canvas.create_rectangle(bar_x1 + 2, bar_y1 + 2, bar_x2 + 2, bar_y2 + 2,
                                       fill=BG_MAIN, outline="", width=0)
            
            # Barre principale avec couleur du thème
            self.canvas.create_rectangle(bar_x1, bar_y1, bar_x2, bar_y2,
                                       fill=bar_color, outline="", width=0)
            
            # Effet de dégradé (ligne plus claire en haut)
            self.canvas.create_rectangle(bar_x1, bar_y1, bar_x2, bar_y1 + 4,
                                       fill=TEXT, outline="", width=0)
            
            # Bordure élégante (couleur du thème)
            self.canvas.create_rectangle(bar_x1, bar_y1, bar_x2, bar_y2,
                                       fill="", outline=TEXT, width=1)
    
    def draw_3d_neon_points(self):
        """Dessine les valeurs sur les barres avec le thème EduManager+"""
        # Couleur pour les valeurs (texte du thème)
        value_color = TEXT  # "#E2E8F0"
        
        for i, (x, y) in enumerate(self.points):
            # Calculer la valeur à afficher
            value = self.data_points[i] if i < len(self.data_points) else 0
            
            # Position du texte au-dessus de la barre (plus proche)
            text_x = x
            text_y = y - 8
            
            # Fond pour le texte (couleur du thème)
            self.canvas.create_rectangle(text_x - 12, text_y - 6, text_x + 12, text_y + 6,
                                       fill=CARD_BG, outline="", width=0)
            
            # Texte de la valeur (police du thème)
            self.canvas.create_text(text_x, text_y, text=f"{value:.0f}",
                                  fill=value_color, font=FONT_SMALL, anchor="s")
    
    def draw_futuristic_labels(self, x1, y1):
        """Dessine les labels des classes avec le thème EduManager+"""
        for i, (x, y) in enumerate(self.points):
            # Texte des classes avec style du thème (plus proche)
            self.canvas.create_text(x, y1 + 25, text=self.labels[i],
                                   fill=TEXT, font=FONT_SMALL, anchor="n")
    
    def draw_advanced_particle_effects(self):
        """Dessine la ligne de moyenne avec le thème EduManager+"""
        if len(self.data_points) == 0:
            return
            
        # Calculer la moyenne
        average_value = sum(self.data_points) / len(self.data_points)
        
        # Calculer la position Y de la ligne de moyenne
        min_val = min(self.data_points)
        max_val = max(self.data_points)
        range_val = max_val - min_val if max_val != min_val else 1
        
        # Position Y de la ligne de moyenne
        avg_y = self.graph_y1 + (self.graph_height * (max_val - average_value) / range_val)
        
        # Dessiner la ligne de moyenne en pointillés (couleur du thème)
        self.canvas.create_line(self.graph_x1, avg_y, self.graph_x1 + self.graph_width, avg_y,
                              fill=TEXT, width=2, dash=(5, 5))
        
        # Texte de la moyenne (police du thème)
        self.canvas.create_text(self.graph_x1 + self.graph_width - 40, avg_y - 8,
                              text=f"Moyenne: {average_value:.1f}",
                              fill=TEXT, font=FONT_SMALL, anchor="e")
    
    def draw_connection_effects(self):
        """Effets de connexion désactivés - ne fait rien"""
        pass
    
    def on_click(self, e):
        """Gère les clics sur le graphique avec les couleurs du thème EduManager+"""
        mx, my = e.x, e.y
        
        for i, (x, y) in enumerate(self.points):
            if abs(mx - x) < 20 and abs(my - y) < 20:
                # Effet de clic statique utilisant l'accent du thème
                self.canvas.create_oval(x - 25, y - 25, x + 25, y + 25, 
                                      fill="", outline=self.colors['primary'], width=3)
                break
    
    def on_motion(self, e):
        """Gère le survol de la souris avec les couleurs du thème EduManager+"""
        mx, my = e.x, e.y
        hovered = None
        
        for i, (x, y) in enumerate(self.points):
            if abs(mx - x) < 25 and abs(my - y) < 25:
                hovered = (i, x, y, self.labels[i], self.data_points[i])
                break

        if hovered:
            i, x, y, label, value = hovered
            # Tooltip avec informations enrichies utilisant les couleurs du thème
            trend = "📈" if value > 75 else "📊" if value > 65 else "📉"
            performance = "Excellent" if value > 85 else "Bon" if value > 75 else "Moyen" if value > 65 else "À améliorer"
            
            tooltip_text = f"🎯 {label}\n📊 Moyenne: {value}%\n{trend} Performance: {performance}"
            self.tooltip.configure(text=tooltip_text)
            
            # Positionnement intelligent du tooltip
            tx = min(mx + 25, self.width - 150)
            ty = max(my - 80, 30)
            self.tooltip.place(x=tx, y=ty)
            
            # Effet de survol sur le point avec accent du thème
            self.canvas.create_oval(x - 15, y - 15, x + 15, y + 15, 
                                  fill="", outline=self.colors['primary'], width=2)
        else:
            self.tooltip.place_forget()
    
    def on_leave(self, _):
        """Masque le tooltip quand la souris quitte le canvas"""
        self.tooltip.place_forget()

# =================== APPLICATION =====================
class MainApp(ctk.CTk):
    def __init__(self, utilisateurs):
        super().__init__()
        self.title("EduManager+ | Application de gestion")
        self.minsize(1100, 720)
        self.configure(fg_color=BG_MAIN)
        self.after(80, self._maximize_on_start)

        # Plein écran
        self.bind("<F11>", self._toggle_fullscreen)
        self.bind("<Escape>", self._exit_fullscreen)

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self.utilisateurs = utilisateurs or {"username": "Invité", "roles": "Utilisateur"}

        print("🚀 Initialisation du système d'optimisation...")
        
        # Initialiser le système d'optimisation
        self._init_optimization_system()

        # Layout
        self.sidebar_frame = ctk.CTkFrame(self, fg_color=BG_SIDEBAR, width=230, corner_radius=12, border_width=1, border_color=BORDER_COLOR)
        self.sidebar_frame.grid(row=0, column=0, sticky="ns", padx=10, pady=10)
        self.sidebar_frame.grid_propagate(False)
        self.sidebar_frame.grid_rowconfigure(2, weight=1)
        self.sidebar_frame.grid_rowconfigure(99, weight=0)

        self.nav_scroll = ctk.CTkScrollableFrame(self.sidebar_frame, fg_color="transparent")

        self.main_content = ctk.CTkFrame(self, fg_color=BG_MAIN, corner_radius=12, border_width=1, border_color=BORDER_COLOR)
        self.main_content.grid(row=0, column=1, sticky="nsew", padx=(0, 10), pady=10)

        # State
        self.views = {}
        self.sidebar_btns = []
        self.sidebar_inds = []
        self.key_to_index = {}

        # Dashboard container
        self.frame_dashboard_content = ctk.CTkFrame(self.main_content, fg_color="transparent")
        self.frame_dashboard_content.grid_columnconfigure(0, weight=1)

        # Build UI
        self.create_sidebar()
        self.create_dashboard()

        # Vue par défaut selon rôle
        default_key = self._default_view_for_role(self._get_user_role())
        idx = self.key_to_index.get(default_key, 0)
        self.set_active(idx)
        self.show_vue_action(default_key)

    def _init_optimization_system(self):
        """Initialise le système d'optimisation complet"""
        try:
            print("🚀 Initialisation du système d'optimisation complet...")
            
            # Initialiser le système d'optimisation complet
            from src.core.optimization.edu_manager_optimizer import initialize_optimization_system
            initialize_optimization_system()
            
            print("✅ Système d'optimisation complet initialisé")
            
        except Exception as e:
            print(f"⚠️ Erreur initialisation système d'optimisation: {e}")
    
    def _register_view_factories(self, view_preloader):
        """Enregistre les factories de vues pour le préchargement"""
        try:
            # Factory pour ClassesManagerView
            def create_classes_view(parent, icons=None):
                from src.modules.academic.classes.views.classes_view import ClassesManagerView
                return ClassesManagerView(parent, icons or self._default_class_icons())
            
            # Factory pour CoursManagerView
            def create_cours_view(parent, icons=None):
                from src.modules.academic.classes.views.cours_view import CoursManagerView
                return CoursManagerView(parent, icons or self._default_class_icons())
            
            # Factory pour NotesView
            def create_notes_view(parent, icons=None):
                from src.modules.academic.grades.views.notes_view import NotesView
                return NotesView(parent, icons or self._default_class_icons())
            
            # Factory pour ElevesView
            def create_eleves_view(parent, icons=None):
                from src.modules.academic.students.views.eleves_dashboard import DashboardEleves
                return DashboardEleves(parent)
            
            # Enregistrer les factories avec arguments par défaut
            view_preloader.register_view_factory("classes", lambda parent=None: create_classes_view(parent or self, self._default_class_icons()))
            view_preloader.register_view_factory("cours", lambda parent=None: create_cours_view(parent or self, self._default_class_icons()))
            view_preloader.register_view_factory("notes", lambda parent=None: create_notes_view(parent or self, self._default_class_icons()))
            view_preloader.register_view_factory("eleves", lambda parent=None: create_eleves_view(parent or self))
            
            print("✅ Factories de vues enregistrées")
            
        except Exception as e:
            print(f"⚠️ Erreur enregistrement factories: {e}")
    
    def _create_view_instance(self, key, cls):
        """Crée une instance de vue avec gestion d'erreurs"""
        try:
            if key == "classes" and cls:
                # ClassesManagerView nécessite: parent, icons
                self.views[key] = cls(
                    self.main_content,
                    icons=self._default_class_icons()
                )
            elif key == "profs" and cls and cls.__name__ == "ProfessorsView":
                # ProfessorsView nécessite: parent, icons
                self.views[key] = cls(
                    self.main_content,
                    icons=self._default_class_icons()
                )
            elif key in ["cours", "enseignements", "emplois"] and cls:
                # CoursManagerView nécessite: parent, icons
                self.views[key] = cls(
                    self.main_content,
                    icons=self._default_class_icons()
                )
            elif key == "notes" and cls:
                # NotesView nécessite: parent, icons
                self.views[key] = cls(
                    self.main_content,
                    icons=self._default_class_icons()
                )
            else:
                # Vues standard
                self.views[key] = cls(self.main_content)
        except TypeError as e:
            if "icons" in str(e).lower():
                try:
                    self.views[key] = cls(self.main_content, self._default_class_icons())
                except Exception as e2:
                    print(f"⚠️ Échec instanciation {key} avec icons: {e2}")
                    self.views[key] = PlaceholderView(self.main_content, f"Gestion des {key}")
            else:
                print(f"⚠️ Échec instanciation {key}: {e}")
                self.views[key] = PlaceholderView(self.main_content, f"Gestion des {key}")
        except Exception as e:
            print(f"⚠️ Échec instanciation {key}: {e}")
            self.views[key] = PlaceholderView(self.main_content, key.capitalize())
    
    def _create_placeholder_view(self, key):
        """Crée une vue placeholder pour les vues manquantes"""
        import customtkinter as ctk
        
        placeholder = ctk.CTkFrame(self.main_content)
        
        # Titre
        title = ctk.CTkLabel(
            placeholder,
            text=f"Vue {key.upper()}",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color="#FFFFFF"
        )
        title.pack(pady=50)
        
        # Message
        message = ctk.CTkLabel(
            placeholder,
            text=f"Cette vue n'est pas encore disponible.\nLe module {key} sera bientôt implémenté.",
            font=ctk.CTkFont(size=16),
            text_color="#CCCCCC",
            justify="center"
        )
        message.pack(pady=20)
        
        # Icône placeholder
        icon_label = ctk.CTkLabel(
            placeholder,
            text="🚧",
            font=ctk.CTkFont(size=48),
            text_color="#FFA500"
        )
        icon_label.pack(pady=20)
        
        return placeholder

    # ----- Fenêtre / Fullscreen
    def _maximize_on_start(self):
        self.update_idletasks()
        try: self.state('zoomed')
        except Exception: pass

    def _toggle_fullscreen(self, _evt=None):
        self.attributes('-fullscreen', not bool(self.attributes('-fullscreen')))

    def _exit_fullscreen(self, _evt=None):
        if bool(self.attributes('-fullscreen')):
            self.attributes('-fullscreen', False)

    # ----- Permissions / Rôle
    def _get_user_role(self):
        try:
            return self.utilisateurs.get("roles", "Utilisateur")
        except Exception:
            return "Utilisateur"

    def _default_view_for_role(self, roles: str) -> str:
        roles = (roles or "").lower()
        if "prof" in roles:
            return "notes"
        if "secr" in roles:
            return "eleves"
        if "élève" in roles or "eleves" in roles or "student" in roles:
            return "notes"
        if "parent" in roles:
            return "notes"
        # admin / directeur / autres -> dashboard
        return "dashboard"

    def _can_access_view(self, view_key: str) -> bool:
        """Vérifie si l'utilisateurs peut accéder à une vue selon les contraintes RBAC"""
        roles = (self._get_user_role() or "").lower()
        
        # Définir les permissions par rôle selon RBAC_SUMMARY.md
        role_permissions = {
            "administrateur": {
                # Accès complet à toutes les vues
                "dashboard": True, "eleves": True, "profs": True, "classes": True,
                "salles": True, "cours": True, "enseignements": True, "emplois": True,
                "matieres": True, "notes": True, "presences": True, "paiements": True, 
                "bulletins": True, "utilisateurs": True, "bibliotheque": True, "messagerie": True,
                "actualites": True, "annonces": True, "notifications": True,
                "taches": True, "biblio": True, "calendriers": True, "carrieres": True
            },
            "comptable": {
                # 13 vues accessibles selon RBAC
                "dashboard": True, "eleves": True, "classes": True, "cours": True,
                "enseignements": True, "emplois": True, "notes": True, "bulletins": True, 
                "paiements": True, "bibliotheque": True, "messagerie": True,
                "actualites": True, "annonces": True, "notifications": True,
                "taches": True, "calendriers": True,
                # Accès refusé
                "profs": False, "salles": False, "matieres": False,
                "presences": False, "utilisateurs": False,
                "biblio": False, "carrieres": False
            },
            "secretaire": {
                # 14 vues accessibles selon RBAC
                "dashboard": True, "eleves": True, "classes": True, "cours": True,
                "enseignements": True, "emplois": True, "presences": True, "notes": True, 
                "bulletins": True, "profs": True, "bibliotheque": True, "messagerie": True,
                "actualites": True, "annonces": True, "notifications": True,
                "taches": True, "calendriers": True,
                # Accès refusé
                "salles": False, "matieres": False, "paiements": False, "utilisateurs": False,
                "biblio": False, "carrieres": False
            },
            "surveillant": {
                # 10 vues accessibles selon RBAC
                "dashboard": True, "presences": True, "cours": True, "emplois": True, "enseignements": True, "eleves": True,
                "classes": True, "bibliotheque": True, "messagerie": True,
                "actualites": True, "annonces": True, "notifications": True,
                # Accès refusé
                "profs": False, "salles": False, "enseignements": False, "matieres": False,
                "notes": False, "bulletins": False, "paiements": False, "utilisateurs": False,
                "taches": False, "biblio": False, "calendriers": False, "carrieres": False
            }
        }
        
        # Vérifier les permissions selon le rôle
        if roles in role_permissions:
            return role_permissions[roles].get(view_key, False)
        
        # Par défaut, refuser l'accès si le rôle n'est pas reconnu
        return False

    # ----- Sidebar
    def _separator(self, parent, pad=(8, 6)):
        sep = ctk.CTkFrame(parent, height=1, fg_color=BORDER_COLOR)
        sep.pack(fill="x", padx=pad[0], pady=(pad[1], pad[1]))
        return sep

    def _add_nav_button(self, parent, text, key, index):
        row = ctk.CTkFrame(parent, fg_color="transparent")
        row.pack(fill="x", padx=6, pady=2)
        row.grid_columnconfigure(1, weight=1)

        indicator = ctk.CTkFrame(row, width=4, height=36, fg_color="transparent", corner_radius=3)
        indicator.grid(row=0, column=0, sticky="nsw", padx=(0, 6))
        indicator.grid_propagate(False)

        btn = ctk.CTkButton(
            row, text=f"  {text}", anchor="w",
            command=lambda k=key, i=index: self.navigate(k, i),
            font=(FONT, 12, "bold"), fg_color="transparent",
            hover_color=HOVER, height=36, corner_radius=8
        )

        # Icône (créée dans ce root) + ref attachée au widget
        icon_file = ICON_MAP.get(key, "home")
        try:
            icon_image = get_icon(icon_file, (20, 20))
            if icon_image:
                btn.configure(image=icon_image)
                btn._imgref = icon_image
        except Exception as e:
            print(f"⚠️ Erreur chargement icône {icon_file}: {e}")

        btn.grid(row=0, column=1, sticky="ew")
        self.sidebar_inds.append(indicator)
        self.sidebar_btns.append(btn)
        self.key_to_index[key] = index

    def create_sidebar(self):
        # Carte utilisateurs ultra-élégante avec design premium
        user_frame = ctk.CTkFrame(
            self.sidebar_frame, 
            fg_color=CARD_BG, 
            corner_radius=16, 
            border_width=2, 
            border_color=BORDER_COLOR,
            height=140
        )
        user_frame.grid(row=1, column=0, sticky="ew", padx=12, pady=(10, 8))
        user_frame.grid_propagate(False)
        
        # Conteneur principal avec effet de profondeur subtil
        profile_container = ctk.CTkFrame(
            user_frame, 
            fg_color="transparent",
            corner_radius=12
        )
        profile_container.pack(fill="both", expand=True, padx=16, pady=16)
        
        # Header avec avatar et informations principales
        header_frame = ctk.CTkFrame(profile_container, fg_color="transparent")
        header_frame.pack(fill="x", pady=(0, 10))
        
        # Avatar avec design premium
        avatar_container = ctk.CTkFrame(header_frame, fg_color="transparent")
        avatar_container.pack(side="left", padx=(0, 12))
        
        # Avatar avec double bordure élégante
        avatar_frame = ctk.CTkFrame(
            avatar_container, 
            fg_color="transparent", 
            corner_radius=30,
            width=60, 
            height=60,
            border_width=2,
            border_color=BORDER_COLOR
        )
        avatar_frame.pack()
        avatar_frame.pack_propagate(False)
        
        # Cercle intérieur avec effet de profondeur
        inner_avatar = ctk.CTkFrame(
            avatar_frame,
            fg_color=BG_MAIN,
            corner_radius=26,
            width=52,
            height=52
        )
        inner_avatar.pack(expand=True, padx=2, pady=2)
        inner_avatar.pack_propagate(False)
        
        # Icône utilisateurs avec effet premium
        user_icon = get_icon("person", (28, 28))
        if user_icon:
            avatar_label = ctk.CTkLabel(inner_avatar, text="", image=user_icon, text_color=ACCENT)
            avatar_label._imgref = user_icon
            avatar_label.pack(expand=True)
        else:
            avatar_label = ctk.CTkLabel(
                inner_avatar, 
                text="👤", 
                font=ctk.CTkFont(size=24, weight="bold"),
                text_color=ACCENT
            )
            avatar_label.pack(expand=True)

        # Informations utilisateurs avec layout horizontal moderne
        info_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        info_frame.pack(side="left", fill="both", expand=True)
        
        # Nom utilisateurs avec typographie moderne
        username_text = self.utilisateurs.get("username", "User").upper()
        username_label = ctk.CTkLabel(
            info_frame, 
            text=username_text, 
            font=ctk.CTkFont(size=15, weight="bold"), 
            text_color=TEXT
        )
        username_label.pack(anchor="w", pady=(0, 8))
        
        # Badge de rôle avec design premium et couleurs dynamiques
        user_role = self._get_user_role()
        role_colors = {
            'administrateur': ('#FF6B6B', '#FF4444'),
            'directeur': ('#4ECDC4', '#2ECFC0'), 
            'secretaire': ('#45B7D1', '#2A9FD1'),
            'comptable': ('#96CEB4', '#7BC4A4'),
            'surveillant': ('#FFEAA7', '#FFD93D'),
            'professeurs': ('#DDA0DD', '#C77DFF')
        }
        
        role_color, role_border = role_colors.get(user_role.lower(), (ACCENT, ACCENT))
        role_text = user_role if len(user_role) <= 12 else user_role[:9] + "..."
        
        # Badge avec effet de gradient et bordure premium
        role_badge = ctk.CTkFrame(
            info_frame,
            fg_color=role_color,
            corner_radius=12,
            height=24,
            width=100,
            border_width=1,
            border_color=role_border
        )
        role_badge.pack(anchor="w", pady=(0, 8))
        role_badge.pack_propagate(False)
        
        # Texte du rôle avec effet premium
        role_label = ctk.CTkLabel(
            role_badge,
            text=f" {role_text} ",
            font=ctk.CTkFont(size=10, weight="bold"),
            text_color=BG_MAIN
        )
        role_label.pack(expand=True)
        
        # Footer avec statut et informations supplémentaires
        footer_frame = ctk.CTkFrame(profile_container, fg_color="transparent")
        footer_frame.pack(fill="x")
        
        # Indicateur de statut avec design moderne
        status_container = ctk.CTkFrame(footer_frame, fg_color="transparent")
        status_container.pack(side="left")
        
        # Point de statut avec effet de brillance
        status_dot = ctk.CTkFrame(
            status_container,
            fg_color=SUCCESS_GREEN,
            corner_radius=4,
            width=10,
            height=10
        )
        status_dot.pack(side="left", padx=(0, 8))
        status_dot.pack_propagate(False)
        
        # Texte de statut avec style moderne
        status_label = ctk.CTkLabel(
            status_container,
            text="En ligne",
            font=ctk.CTkFont(size=10, weight="bold"),
            text_color=SUCCESS_GREEN
        )
        status_label.pack(side="left")
        
        # Informations supplémentaires (heure de connexion)
        extra_info_frame = ctk.CTkFrame(footer_frame, fg_color="transparent")
        extra_info_frame.pack(side="right")
        
        # Heure de connexion avec icône
        time_container = ctk.CTkFrame(extra_info_frame, fg_color="transparent")
        time_container.pack(anchor="e")
        
        # Icône d'horloge
        clock_icon = get_icon("clock", (12, 12))
        if clock_icon:
            clock_label = ctk.CTkLabel(time_container, text="", image=clock_icon, text_color=MUTED)
            clock_label._imgref = clock_icon
            clock_label.pack(side="left", padx=(0, 4))
        
        # Heure de connexion
        login_time = ctk.CTkLabel(
            time_container,
            text="13:04",
            font=ctk.CTkFont(size=9, weight="bold"),
            text_color=MUTED
        )
        login_time.pack(side="left")

        self.nav_scroll.grid(row=2, column=0, sticky="nsew", padx=6, pady=(6, 6))

        nav_sections = {
            "SCOLARITÉ": [
                ("Tableau de bord", "dashboard"),
                ("Élèves", "eleves"),
                ("Professeurs", "profs"),
                ("Classes", "classes"),
                ("Salles", "salles"),
            ],
            "PÉDAGOGIE": [
                ("Cours", "cours"),
                ("Matières", "matieres"),
                ("Notes", "notes"),
                ("Présences", "presences"),
                ("Bulletins", "bulletins"),
            ],
            "FINANCES": [("Paiements", "paiements")],
            "COMMUNICATION": [
                ("Bibliothèque", "bibliotheque"),
                ("Messagerie", "messagerie"),
            ],
            "ADMINISTRATION": [("Utilisateurs", "utilisateurs")],
        }

        self.sidebar_btns.clear()
        self.sidebar_inds.clear()
        self.key_to_index.clear()

        idx = 0
        for section_title, buttons in nav_sections.items():
            sec = ctk.CTkFrame(self.nav_scroll, fg_color="transparent")
            sec.pack(fill="x", pady=(6, 2))
            ctk.CTkLabel(sec, text=section_title, font=(FONT, 10, "bold"), text_color=MUTED)\
                .pack(anchor="w", padx=8, pady=(2, 4))
            for text, key in buttons:
                self._add_nav_button(sec, text, key, idx); idx += 1
            self._separator(self.nav_scroll)

        # Déconnexion
        logout_icon = get_icon("logout", (20, 20))
        btn_logout = ctk.CTkButton(self.sidebar_frame, text=" Déconnexion", image=logout_icon,
                                   font=(FONT, 12, "bold"),
                                   fg_color=DANGER, hover_color="#A34646",
                                   corner_radius=8, height=35, command=self._secure_logout)
        if logout_icon:
            btn_logout._imgref = logout_icon
        btn_logout.grid(row=100, column=0, sticky="sew", pady=(6, 10), padx=10)

    def _secure_logout(self):
        """Déconnexion sécurisée qui retourne au LoginView"""
        import gc
        from tkinter import messagebox
        
        # Confirmation de déconnexion
        if messagebox.askyesno("Déconnexion", "Êtes-vous sûr de vouloir vous déconnecter ?"):
            try:
                # 1. Nettoyer la mémoire
                self._cleanup_session()
                
                # 2. Fermer la fenêtre dashboard
                self.destroy()
                
                # 3. Nettoyer la mémoire
                gc.collect()
                
                # 4. Retourner au LoginView
                self._return_to_login()
                
            except Exception as e:
                print(f"❌ Erreur lors de la déconnexion: {e}")
                messagebox.showerror("Erreur", "Erreur lors de la déconnexion")
    
    def _cleanup_session(self):
        """Nettoie la session et la mémoire"""
        try:
            # Nettoyer les images
            if hasattr(self, '_DASHBOARD_PIL_CACHE'):
                self._DASHBOARD_PIL_CACHE.clear()
            if hasattr(self, '_DASHBOARD_IMG_POOL'):
                self._DASHBOARD_IMG_POOL.clear()
            
            # Nettoyer les vues
            for view in self.views.values():
                try:
                    if hasattr(view, 'destroy'):
                        view.destroy()
                except Exception:
                    pass
            
            # Vider les dictionnaires
            self.views.clear()
            self.sidebar_btns.clear()
            self.sidebar_inds.clear()
            self.key_to_index.clear()
            
            print("✅ Session nettoyée avec succès")
            
        except Exception as e:
            print(f"⚠️ Erreur lors du nettoyage de la session: {e}")
    
    def _return_to_login(self):
        """Retourne au LoginView avec le même design"""
        try:
            from src.modules.auth.views.login_view import LoginView
            
            # Créer une nouvelle instance du LoginView
            login_app = LoginView()
            login_app.mainloop()
            
        except Exception as e:
            print(f"❌ Erreur lors du retour au login: {e}")
            import traceback
            traceback.print_exc()

    # Méthodes de recherche supprimées pour éviter les erreurs de base de données
    
    def _has_permission(self, resource, action):
        """Vérifie si l'utilisateurs a la permissions pour une ressource et action selon RBAC"""
        try:
            from src.core.permissions import check_permission
            return check_permission(self.utilisateurs.get('roles', ''), resource, action)
        except Exception:
            # Fallback: permissions détaillées selon RBAC_SUMMARY.md
            user_role = self._get_user_role().lower()
            
            # Permissions par rôle et ressource
            role_permissions = {
                "administrateur": {
                    # Accès complet à toutes les ressources
                    "eleves": ["read", "create", "update", "delete"],
                    "profs": ["read", "create", "update", "delete"],
                    "classes": ["read", "create", "update", "delete"],
                    "salles": ["read", "create", "update", "delete"],
                    "cours": ["read", "create", "update", "delete"],
                    "enseignements": ["read", "create", "update", "delete"],
                    "emplois": ["read", "create", "update", "delete"],
                    "matieres": ["read", "create", "update", "delete"],
                    "notes": ["read", "create", "update", "delete"],
                    "presences": ["read", "create", "update", "delete"],
                    "paiements": ["read", "create", "update", "delete"],
                    "bulletins": ["read", "create", "update", "delete"],
                    "emplois": ["read", "create", "update", "delete"],
                    "utilisateurs": ["read", "create", "update", "delete"]
                },
                "comptable": {
                    # ADMIN sur Paiements, READ sur données scolaires
                    "paiements": ["read", "create", "update", "delete"],
                    "eleves": ["read"],
                    "classes": ["read"],
                    "notes": ["read"],
                    "bulletins": ["read"]
                },
                "secretaire": {
                    # ADMIN sur Élèves, Classes, Présences, READ sur Notes, Bulletins
                    "eleves": ["read", "create", "update", "delete"],
                    "classes": ["read", "create", "update", "delete"],
                    "presences": ["read", "create", "update", "delete"],
                    "profs": ["read", "create", "update", "delete"],
                    "notes": ["read"],
                    "bulletins": ["read"]
                },
                "surveillant": {
                    # ADMIN sur Présences, Emplois du temps, READ sur Élèves, Classes
                    "presences": ["read", "create", "update", "delete"],
                    "emplois": ["read", "create", "update", "delete"],
                    "eleves": ["read"],
                    "classes": ["read"]
                }
            }
            
            # Vérifier les permissions
            if user_role in role_permissions:
                resource_perms = role_permissions[user_role].get(resource, [])
                return action in resource_perms
            
            return False

    def navigate(self, key, idx):
        self.set_active(idx)
        self.show_vue_action(key)

    def set_active(self, idx_active):
        for i, btn in enumerate(self.sidebar_btns):
            ind = self.sidebar_inds[i]
            if i == idx_active:
                ind.configure(fg_color=ACCENT)
                btn.configure(fg_color=ACTIVE, text_color=TEXT, hover_color=ACTIVE)
            else:
                ind.configure(fg_color="transparent")
                btn.configure(fg_color="transparent", text_color=TEXT, hover_color=HOVER)

    # ----- Helpers pour les vues
    def _create_notif_bar(self):
        """Crée une barre de notifications simple"""
        class SimpleNotifBar:
            def __init__(self, parent):
                self.parent = parent
                self.frame = ctk.CTkFrame(parent, fg_color="transparent", height=30)
                self.label = ctk.CTkLabel(self.frame, text="", font=("Segoe UI", 10))
                self.label.pack()
            
            def show(self, message, color=None):
                self.label.configure(text=message, text_color=color or "#00D4FF")
                self.frame.after(3000, lambda: self.label.configure(text=""))
        
        return SimpleNotifBar(self.main_content)

    def _default_class_icons(self):
        def p(name): return os.path.join(ICONS_DIR, f"{name}.png")
        return {
            "add": p("add"),
            "edit": p("edit"),
            "delete": p("delete"),
            "search": p("search"),
            "export": p("csv"),
            "import": p("upload"),
            "pdf": p("csv"),
            "reload": p("refresh"),
            "view": p("view"),
        }

    # ----- Navigation principale
    def show_vue_action(self, key):
        if not self._can_access_view(key):
            messagebox.showerror("Accès Refusé", "Vous n'avez pas les permissions nécessaires pour accéder à cette vue.")
            return

        for w in self.main_content.winfo_children():
            try:
                w.pack_forget()
            except AttributeError:
                # Certains widgets n'ont pas pack_forget, on les supprime directement
                try:
                    w.destroy()
                except:
                    pass

        if key == "dashboard":
            self.frame_dashboard_content.pack(fill="both", expand=True, padx=10, pady=10)
            self.refresh_dashboard()
            return

        VIEW_MAP = {
            "eleves": ElevesView,
            "utilisateurs": UtilisateursView,
            "classes": ClassesManagerView,
            "profs": ProfessorsDashboard,
            "salles": SallesView,
            "cours": CoursManagerView,
            "enseignements": CoursManagerView,  # Compatibilité
            "emplois": CoursManagerView,  # Compatibilité
            "matieres": MatieresView if 'MatieresView' in globals() else None,
            "notes": NotesView,
            "presences": PresenceView,
            "paiements": PaiementsView,
            "bulletins": BulletinsView,
            # Nouvelles vues d'action
            "actualites": ActualitesView,
            "annonces": AnnoncesView,
            "notifications": NotificationsView,
            "bibliotheque": BibliothequeView,
            "messagerie": MessagerieView,
            "taches": TachesView,
            "biblio": BibliothequeView,
            "calendriers": CalendriersView,
            "carrieres": CarrieresView,
            "messagerie": MessagerieView,
        }

        if key in VIEW_MAP:
            if key not in self.views:
                cls = VIEW_MAP[key]
                print(f"🚀 Chargement de la vue {key}...")
                
                # Vérifier si la classes existe
                if cls is None:
                    print(f"⚠️ Vue non trouvée: {key}")
                    # Créer une vue placeholder
                    self.views[key] = self._create_placeholder_view(key)
                    print(f"✅ Vue {key} chargée avec succès")
                    return
                
                # Essayer d'utiliser le système de préchargement
                try:
                    from src.core.views.view_preloader import get_preloaded_view
                    preloaded_view = get_preloaded_view(key, self.main_content)
                    if preloaded_view:
                        self.views[key] = preloaded_view
                        print(f"✅ Vue {key} récupérée du pool de préchargement")
                    else:
                        # Créer la vue normalement si pas en pool
                        self._create_view_instance(key, cls)
                except Exception as e:
                    print(f"⚠️ Erreur préchargement {key}: {e}")
                    # Fallback vers la création normale
                    self._create_view_instance(key, cls)
                
                print(f"✅ Vue {key} chargée avec succès")
            
            # Vérifier que la vue existe avant de l'afficher
            if hasattr(self.views[key], 'pack'):
                self.views[key].pack(fill="both", expand=True, padx=10, pady=10)
            elif hasattr(self.views[key], 'geometry'):
                # C'est une fenêtre (CTkToplevel), on l'affiche directement
                print(f"✅ Affichage de la fenêtre {key}")
                # La fenêtre s'affiche automatiquement
            else:
                print(f"⚠️ Vue {key} n'a pas de méthode pack ni geometry")
                PlaceholderView(self.main_content, key.capitalize()).pack(fill="both", expand=True, padx=10, pady=10)
        elif key == "settings":
            PlaceholderView(self.main_content, "Paramètres").pack(fill="both", expand=True, padx=10, pady=10)
        else:
            PlaceholderView(self.main_content, key.capitalize()).pack(fill="both", expand=True, padx=10, pady=10)

    # ----- Tableau de bord
    def refresh_dashboard(self, _=None):
        self.refresh_stats()
        self.update_graph()
        self.update_time()

    def create_dashboard(self):
        # En-tête
        header_frame = ctk.CTkFrame(self.frame_dashboard_content, fg_color="transparent")
        header_frame.pack(fill="x", pady=(0, 10))
        header_frame.grid_columnconfigure(0, weight=1)
        header_frame.grid_columnconfigure(1, weight=1)

        greetings_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        greetings_frame.grid(row=0, column=0, sticky="w")

        greeting_content = ctk.CTkFrame(greetings_frame, fg_color="transparent")
        greeting_content.pack(anchor="w", pady=(2, 0))

        greeting_icon = get_icon("home", (28, 28))
        if greeting_icon:
            glb = ctk.CTkLabel(greeting_content, text="", image=greeting_icon, text_color=ACCENT)
            glb._imgref = greeting_icon
            glb.pack(side="left", padx=(0, 8))

        ctk.CTkLabel(greeting_content, text=f"Bonjour, {self.utilisateurs.get('username','')}",
                     font=(FONT, FS_TITLE, "bold"), text_color=ACCENT).pack(side="left")

        ctk.CTkLabel(greetings_frame, text="Aperçu temps réel de votre établissement.",
                     font=(FONT, FS_SUBHDR-2), text_color=MUTED).pack(anchor="w", pady=(0, 2))

        search_refresh_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        search_refresh_frame.grid(row=0, column=1, sticky="e")

        # Barre de recherche simplifiée (désactivée temporairement)
        search_entry = ctk.CTkEntry(search_refresh_frame, placeholder_text="Rechercher...", width=200,
                     fg_color=CARD_BG, text_color=TEXT, border_color=BORDER_COLOR,
                     corner_radius=8, font=(FONT, FS_TEXT-1))
        search_entry.pack(side="left", padx=(0, 5))
        # Désactiver temporairement pour éviter les erreurs
        search_entry.configure(state="disabled")

        refresh_icon = get_icon("refresh", (20, 20))
        btn_refresh = ctk.CTkButton(search_refresh_frame, text="", image=refresh_icon, width=35,
                                    fg_color=CARD_BG, hover_color=HOVER, corner_radius=8,
                                    command=self.refresh_dashboard)
        if refresh_icon:
            btn_refresh._imgref = refresh_icon
        btn_refresh.pack(side="left")

        # Cartes stats
        self.create_stats_cards()

        # Zone principale (graph + accès rapide + vue rapide)
        self.create_main_content_area()
        
        # Dashboard analytique
        self.create_analytics_dashboard()
        
        # Assistant IA supprimé

        # Heure en direct
        self.update_time()

    def create_stats_cards(self):
        self.stats_frame = ctk.CTkFrame(self.frame_dashboard_content, fg_color="transparent")
        self.stats_frame.pack(fill="x", pady=(5, 5))
        self.refresh_stats()

    def refresh_stats(self):
        eleves   = get_stats_count_any("eleves")
        classes  = get_stats_count_any("classes", "classes")
        profs    = get_stats_count_any("professeurs", "professeurs")
        salles   = get_stats_count_any("salles", "salles")
        maxv = max(1, eleves, classes, profs, salles)

        data = [
            ("Total Élèves", eleves,  "eleves", OK,     eleves/maxv),
            ("Classes",      classes, "classes", ACCENT, classes/maxv),
            ("Professeurs",  profs,   "profs",   WARN,   profs/maxv),
            ("Salles",       salles,  "salles",  DANGER, salles/maxv),
        ]

        for w in self.stats_frame.winfo_children():
            w.destroy()

        for i, (t, v, ic, col, ratio) in enumerate(data):
            c = stat_card(self.stats_frame, t, v, ic, col, ratio)
            c.grid(row=0, column=i, padx=3, sticky="nsew")
            self.stats_frame.grid_columnconfigure(i, weight=1)

    def create_main_content_area(self):
        content = ctk.CTkFrame(self.frame_dashboard_content, fg_color="transparent")
        content.pack(fill="both", expand=True)
        content.grid_columnconfigure(0, weight=3)
        content.grid_columnconfigure(1, weight=1)
        content.grid_rowconfigure(0, weight=1)

        left = ctk.CTkFrame(content, fg_color="transparent")
        left.grid(row=0, column=0, sticky="nsew", padx=(0, 5))
        left.grid_rowconfigure(0, weight=3)  # Plus d'espace pour le graphique
        left.grid_rowconfigure(1, weight=1)   # Moins d'espace pour les boutons
        left.grid_columnconfigure(0, weight=1)
        left.grid_columnconfigure(1, weight=1)

        self.create_graph_box(left)
        self.create_all_actions_cards(left)

        right = ctk.CTkFrame(content, fg_color=CARD_BG, corner_radius=10, border_width=1, border_color=BORDER_COLOR)
        right.grid(row=0, column=1, sticky="nsew")
        self.create_tasks_and_events(right)

    def create_graph_box(self, parent):
        # Utilisation du nouveau graphique ultra moderne avec position ajustée
        self.graph_box = UltraModernGraphFrame(parent, width=1100, height=550)
        self.graph_box.grid(row=0, column=0, columnspan=2, sticky="nsew", padx=(0, 5), pady=(0, 10))

    def create_all_actions_cards(self, parent):
        wrap = ctk.CTkFrame(parent, fg_color=CARD_BG, corner_radius=10, border_width=1, border_color=BORDER_COLOR)
        wrap.grid(row=1, column=0, columnspan=2, sticky="nsew", pady=(10, 0))
        ctk.CTkLabel(wrap, text="Accès Rapide", font=(FONT, FS_HEADER, "bold"), text_color=TEXT).pack(padx=10, pady=(8, 5), anchor="w")
        scroll = ctk.CTkScrollableFrame(wrap, fg_color="transparent")
        scroll.pack(fill="both", expand=True, padx=8, pady=8)

        for i, (label, key) in enumerate(ACTIONS):
            r, c = divmod(i, 4)
            action_card(scroll, label, key, key, command=self.show_vue_action).grid(row=r, column=c, padx=6, pady=6, sticky="nsew")
        for col in range(4):
            scroll.grid_columnconfigure(col, weight=1)

    def create_tasks_and_events(self, parent):
        ctk.CTkLabel(parent, text="Vue Rapide", font=(FONT, FS_HEADER, "bold"), text_color=TEXT).pack(padx=10, pady=(10, 5), anchor="w")

        # Date/heure
        datetime_frame = ctk.CTkFrame(parent, fg_color=HEADER_BG, corner_radius=8)
        datetime_frame.pack(fill="x", padx=10, pady=(0, 10))

        time_frame = ctk.CTkFrame(datetime_frame, fg_color="transparent")
        time_frame.pack(fill="x", padx=8, pady=(8, 0))

        clock_icon = get_icon("clock", (24, 24))
        if clock_icon:
            clb = ctk.CTkLabel(time_frame, text="", image=clock_icon, text_color=OK)
            clb._imgref = clock_icon
            clb.pack(side="left")
        self.time_label = ctk.CTkLabel(time_frame, text="", font=(FONT, 26, "bold"), text_color=OK)
        self.time_label.pack(side="left", padx=(6, 0))

        date_frame = ctk.CTkFrame(datetime_frame, fg_color="transparent")
        date_frame.pack(fill="x", padx=8, pady=(0, 8))
        self.day_label = ctk.CTkLabel(date_frame, text="", font=(FONT, 16, "bold"), text_color=TEXT); self.day_label.pack(side="left", padx=(5, 0))
        self.date_label = ctk.CTkLabel(date_frame, text="", font=(FONT, 12), text_color=MUTED); self.date_label.pack(side="left", padx=(5, 0))

        # Événements (exemple)
        ctk.CTkLabel(parent, text="Événements à venir", font=(FONT, FS_SUBHDR, "bold"), text_color=TEXT).pack(padx=10, pady=(10, 5), anchor="w")
        events_scroll = ctk.CTkScrollableFrame(parent, fg_color="transparent"); events_scroll.pack(fill="both", expand=True, padx=8, pady=4)
        events_data = [
            ("Réunion des parents", "15h00 - Salle A2", "calendar"),
            ("Examen de Maths", "10h00 - Salle B1", "grade"),
            ("Sortie scolaire", "Toute la journée - Muséum", "bus"),
            ("Conseil de classes", "14h00 - Salle des profs", "group"),
            ("Cours de sport", "16h00 - Gymnase", "sport"),
        ]
        for title, subtitle, icon_name in events_data:
            card = ctk.CTkFrame(events_scroll, fg_color=HEADER_BG, corner_radius=8, border_width=1, border_color=BORDER_COLOR)
            card.pack(fill="x", pady=4)
            title_row = ctk.CTkFrame(card, fg_color="transparent"); title_row.pack(fill="x", padx=8, pady=4)
            ev_ico = get_icon(icon_name, (16, 16))
            if ev_ico:
                eimg = ctk.CTkLabel(title_row, text="", image=ev_ico, text_color=ACCENT)
                eimg._imgref = ev_ico
                eimg.pack(side="left", padx=(0, 8))
            ctk.CTkLabel(title_row, text=title, font=(FONT, FS_TEXT, "bold"), text_color=TEXT).pack(side="left")
            ctk.CTkLabel(card, text=subtitle, font=(FONT, FS_TEXT-2), text_color=MUTED).pack(padx=8, pady=(0, 8), anchor="w")

    def create_analytics_dashboard(self):
        """Crée un dashboard analytique avec des graphiques avancés"""
        # Titre de la section analytique
        analytics_title = ctk.CTkLabel(
            self.frame_dashboard_content,
            text="📊 Dashboard Analytique",
            font=(FONT, FS_HEADER, "bold"),
            text_color=ACCENT
        )
        analytics_title.pack(anchor="w", pady=(20, 10))
        
        # Conteneur principal pour les analyses
        analytics_container = ctk.CTkFrame(
            self.frame_dashboard_content,
            fg_color="transparent"
        )
        analytics_container.pack(fill="both", expand=True, pady=(0, 20))
        analytics_container.grid_columnconfigure(0, weight=1)
        analytics_container.grid_columnconfigure(1, weight=1)
        
        # Graphique 1: Statistiques générales
        self.create_simple_stats_chart(analytics_container, 0, 0)
        
        # Graphique 2: Performance des classes
        self.create_simple_classes_chart(analytics_container, 0, 1)
        
        # Graphique 3: Évolution des notes
        self.create_simple_grades_chart(analytics_container, 1, 0)
        
        # Graphique 4: Indicateurs clés
        self.create_simple_indicators_chart(analytics_container, 1, 1)
    
    def create_simple_stats_chart(self, parent, row, col):
        """Crée un graphique simple de statistiques générales"""
        # Carte simple
        chart_frame = ctk.CTkFrame(
            parent,
            fg_color=CARD_BG,
            corner_radius=12,
            border_width=1,
            border_color=BORDER_COLOR,
            height=200
        )
        chart_frame.grid(row=row, column=col, sticky="nsew", padx=5, pady=5)
        chart_frame.grid_propagate(False)
        
        # Titre
        title_label = ctk.CTkLabel(
            chart_frame,
            text="📊 Statistiques Générales",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color=TEXT
        )
        title_label.pack(pady=(15, 10))
        
        # Contenu avec statistiques
        content_frame = ctk.CTkFrame(chart_frame, fg_color="transparent")
        content_frame.pack(fill="both", expand=True, padx=15, pady=(0, 15))
        
        # Statistiques
        stats = [
            ("👥 Total Élèves", "502", "#4ECDC4"),
            ("👨‍🏫 Professeurs", "28", "#45B7D1"),
            ("🏫 Classes", "12", "#96CEB4"),
            ("📚 Matières", "8", "#FFEAA7")
        ]
        
        for i, (label, value, color) in enumerate(stats):
            stat_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
            stat_frame.pack(fill="x", pady=3)
            
            # Indicateur coloré
            indicator = ctk.CTkFrame(
                stat_frame,
                fg_color=color,
                width=15,
                height=15,
                corner_radius=8
            )
            indicator.pack(side="left", padx=(0, 10))
            indicator.pack_propagate(False)
            
            # Label
            label_widget = ctk.CTkLabel(
                stat_frame,
                text=label,
                font=ctk.CTkFont(size=11),
                text_color=TEXT
            )
            label_widget.pack(side="left", padx=(0, 10))
            
            # Valeur
            value_widget = ctk.CTkLabel(
                stat_frame,
                text=value,
                font=ctk.CTkFont(size=12, weight="bold"),
                text_color=color
            )
            value_widget.pack(side="right")
    
    def _get_success_color(self, rate):
        """Retourne la couleur appropriée selon le taux de réussite"""
        if rate >= 80:
            return "#00FF88"  # Vert vif
        elif rate >= 70:
            return "#64FFDA"  # Cyan
        elif rate >= 60:
            return "#FFD700"  # Or
        elif rate >= 50:
            return "#FF8C00"  # Orange
        else:
            return "#FF6B6B"  # Rouge
    
    def _get_success_rate_chart_data(self):
        """Données améliorées pour le graphique de réussite"""
        return {
            "6ème A": 85,
            "5ème B": 78,
            "4ème C": 72,
            "3ème A": 88,
            "2nde B": 75,
            "1ère C": 82
        }
    
    def create_simple_classes_chart(self, parent, row, col):
        """Crée un graphique simple de performance des classes"""
        # Carte simple
        chart_frame = ctk.CTkFrame(
            parent,
            fg_color=CARD_BG,
            corner_radius=12,
            border_width=1,
            border_color=BORDER_COLOR,
            height=200
        )
        chart_frame.grid(row=row, column=col, sticky="nsew", padx=5, pady=5)
        chart_frame.grid_propagate(False)
        
        # Titre
        title_label = ctk.CTkLabel(
            chart_frame,
            text="🏫 Performance des Classes",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color=TEXT
        )
        title_label.pack(pady=(15, 10))
        
        # Contenu avec performance des classes
        content_frame = ctk.CTkFrame(chart_frame, fg_color="transparent")
        content_frame.pack(fill="both", expand=True, padx=15, pady=(0, 15))
        
        # Données de performance
        classes_data = [
            ("6ème A", "85%", "#4ECDC4"),
            ("5ème B", "78%", "#45B7D1"),
            ("4ème C", "72%", "#96CEB4"),
            ("3ème A", "88%", "#FFEAA7")
        ]
        
        for classes, performance, color in classes_data:
            class_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
            class_frame.pack(fill="x", pady=3)
            
            # Indicateur coloré
            indicator = ctk.CTkFrame(
                class_frame,
                fg_color=color,
                width=15,
                height=15,
                corner_radius=8
            )
            indicator.pack(side="left", padx=(0, 10))
            indicator.pack_propagate(False)
            
            # Label de classes
            label_widget = ctk.CTkLabel(
                class_frame,
                text=classes,
                font=ctk.CTkFont(size=11),
                text_color=TEXT
            )
            label_widget.pack(side="left", padx=(0, 10))
            
            # Performance
            perf_widget = ctk.CTkLabel(
                class_frame,
                text=performance,
                font=ctk.CTkFont(size=12, weight="bold"),
                text_color=color
            )
            perf_widget.pack(side="right")
    
    def _get_absence_chart_data(self):
        """Données améliorées pour le graphique des absences"""
        return {
            "Maladie": 45,
            "Retard": 23,
            "Absence": 18,
            "Sortie": 12,
            "Autre": 8
        }
    
    def create_simple_grades_chart(self, parent, row, col):
        """Crée un graphique simple d'évolution des notes"""
        # Carte simple
        chart_frame = ctk.CTkFrame(
            parent,
            fg_color=CARD_BG,
            corner_radius=12,
            border_width=1,
            border_color=BORDER_COLOR,
            height=200
        )
        chart_frame.grid(row=row, column=col, sticky="nsew", padx=5, pady=5)
        chart_frame.grid_propagate(False)
        
        # Titre
        title_label = ctk.CTkLabel(
            chart_frame,
            text="📈 Évolution des Notes",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color=TEXT
        )
        title_label.pack(pady=(15, 10))
        
        # Contenu avec évolution des notes
        content_frame = ctk.CTkFrame(chart_frame, fg_color="transparent")
        content_frame.pack(fill="both", expand=True, padx=15, pady=(0, 15))
        
        # Données d'évolution
        evolution_data = [
            ("Mathématiques", "14.2", "#FF6B6B"),
            ("Français", "12.8", "#4ECDC4"),
            ("Histoire", "13.5", "#45B7D1"),
            ("Sciences", "15.1", "#96CEB4")
        ]
        
        for matieres, notes, color in evolution_data:
            matiere_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
            matiere_frame.pack(fill="x", pady=3)
            
            # Indicateur coloré
            indicator = ctk.CTkFrame(
                matiere_frame,
                fg_color=color,
                width=15,
                height=15,
                corner_radius=8
            )
            indicator.pack(side="left", padx=(0, 10))
            indicator.pack_propagate(False)
            
            # Label de matière
            label_widget = ctk.CTkLabel(
                matiere_frame,
                text=matieres,
                font=ctk.CTkFont(size=11),
                text_color=TEXT
            )
            label_widget.pack(side="left", padx=(0, 10))
            
            # Note
            note_widget = ctk.CTkLabel(
                matiere_frame,
                text=notes,
                font=ctk.CTkFont(size=12, weight="bold"),
                text_color=color
            )
            note_widget.pack(side="right")

    def create_simple_indicators_chart(self, parent, row, col):
        """Crée un graphique simple d'indicateurs clés"""
        # Carte simple
        chart_frame = ctk.CTkFrame(
            parent,
            fg_color=CARD_BG,
            corner_radius=12,
            border_width=1,
            border_color=BORDER_COLOR,
            height=200
        )
        chart_frame.grid(row=row, column=col, sticky="nsew", padx=5, pady=5)
        chart_frame.grid_propagate(False)
        
        # Titre
        title_label = ctk.CTkLabel(
            chart_frame,
            text="🎯 Indicateurs Clés",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color=TEXT
        )
        title_label.pack(pady=(15, 10))
        
        # Contenu avec indicateurs
        content_frame = ctk.CTkFrame(chart_frame, fg_color="transparent")
        content_frame.pack(fill="both", expand=True, padx=15, pady=(0, 15))
        
        # Données d'indicateurs
        indicators_data = [
            ("Taux de Réussite", "82%", "#00FF88"),
            ("Assiduité", "94%", "#64FFDA"),
            ("Satisfaction", "88%", "#FFD700"),
            ("Progression", "+12%", "#FF8C00")
        ]
        
        for indicator, value, color in indicators_data:
            indicator_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
            indicator_frame.pack(fill="x", pady=3)
            
            # Indicateur coloré
            color_indicator = ctk.CTkFrame(
                indicator_frame,
                fg_color=color,
                width=15,
                height=15,
                corner_radius=8
            )
            color_indicator.pack(side="left", padx=(0, 10))
            color_indicator.pack_propagate(False)
            
            # Label d'indicateur
            label_widget = ctk.CTkLabel(
                indicator_frame,
                text=indicator,
                font=ctk.CTkFont(size=11),
                text_color=TEXT
            )
            label_widget.pack(side="left", padx=(0, 10))
            
            # Valeur
            value_widget = ctk.CTkLabel(
                indicator_frame,
                text=value,
                font=ctk.CTkFont(size=12, weight="bold"),
                text_color=color
            )
            value_widget.pack(side="right")

    # ----- Horloge
    def update_time(self):
        """Met à jour l'affichage de l'heure en temps réel"""
        try:
            now = datetime.datetime.now()
            if hasattr(self, 'day_label'):
                self.day_label.configure(text=now.strftime("%A"))
            if hasattr(self, 'date_label'):
                self.date_label.configure(text=now.strftime("%d %B %Y"))
            if hasattr(self, 'time_label'):
                self.time_label.configure(text=now.strftime("%H:%M:%S"))
            # Programmer la prochaine mise à jour
            self.after(1000, self.update_time)
        except Exception as e:
            print(f"⚠️ Erreur mise à jour heure: {e}")

    # ----- Graphe : Moyenne par matière (Tendance)
    def update_graph(self):
        # Cette méthode est maintenant gérée par la classes PremiumGraphFrame
        pass

# =================== CLASSE DASHBOARDVIEW (pour compatibilité) =====================
class DashboardView(MainApp):
    """Alias pour MainApp pour maintenir la compatibilité avec les imports existants."""
    def __init__(self, utilisateurs):
        super().__init__(utilisateurs)

# =================== ENTRÉE DIRECTE (test rapide) =====================
if __name__ == "__main__":
    utilisateurs = {"username": "admin", "id": 1, "roles": "Administrateur"}
    app = MainApp(utilisateurs)
    app.mainloop()
