import customtkinter as ctk
from PIL import Image
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import sqlite3
import os
import sys
from tkinter import messagebox, ttk
import datetime
import calendar

# ================= Compat Pillow LANCZOS =================
try:
    RESAMPLE_LANCZOS = Image.Resampling.LANCZOS
except AttributeError:
    RESAMPLE_LANCZOS = Image.LANCZOS

# =================== CHEMIN DB FIXE =====================
DB_PATH = r"C:\Users\Lenovo\Desktop\EduManager+\database\edumanager.db"
print(">>> Fichier DB utilisé :", DB_PATH)

# ====================================================================
# Thème et Couleurs Modernes (Amélioré)
# ====================================================================
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

BG_MAIN = "#0A192F"
BG_SIDEBAR = "#0E1C36"
HEADER_BG = "#172A45"
CARD_BG = "#0B2039"
BORDER_COLOR = "#334155"
ACCENT_BLUE = "#64FFDA"
PRIMARY_RED = "#FF6363"
PRIMARY_YELLOW = "#FFD700"
PRIMARY_GREEN = "#A0E7E5"
TEXT_COLOR = "#CCD6F6"
SUBTEXT_COLOR = "#8892B0"

# Couleurs de survol et de l'élément actif ajustées pour plus de cohérence
BTN_HOVER_COLOR = "#1D324E"
ACCENT_HOVER_COLOR = "#4cc1a8"
ACTIVE_BG = "#5E82B6"

FONT_FAMILY = "Segoe UI"
FONT_SIZE_TITLE = 32
FONT_SIZE_HEADER = 22
FONT_SIZE_SUBHEADER = 16
FONT_SIZE_TEXT = 14
FONT_SIZE_CARD_VALUE = 28

THEME = {
    "BG_MAIN": BG_MAIN,
    "BG_SIDEBAR": BG_SIDEBAR,
    "CARD": CARD_BG,
    "BORDER_COLOR": BORDER_COLOR,
    "ACCENT_PRIMARY": ACCENT_BLUE,
    "ACCENT_SECONDARY": PRIMARY_RED,
    "TEXT_COLOR": TEXT_COLOR,
    "SUBTEXT_COLOR": SUBTEXT_COLOR,
    "BTN_HOVER": BTN_HOVER_COLOR,
    "ACCENT_HOVER": ACCENT_HOVER_COLOR,
    "FONT": FONT_FAMILY
}

# ====================================================================
# Imports des vues
# ====================================================================
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if project_root not in sys.path:
    sys.path.append(project_root)

class PlaceholderView(ctk.CTkFrame):
    def __init__(self, master, title):
        super().__init__(master, fg_color="transparent")
        ctk.CTkLabel(self, text=title, font=(THEME["FONT"], FONT_SIZE_TITLE, "bold"), text_color=TEXT_COLOR).pack(pady=10, padx=10)
        ctk.CTkLabel(self, text="Contenu à venir...", font=(THEME["FONT"], FONT_SIZE_TEXT), text_color=SUBTEXT_COLOR).pack(padx=10, pady=5)

try:
    from views.eleves.dashboard import DashboardEleves
    from views.professeurs_view import ProfessorsDashboard
    from views.classes_view import ClassesManagerView
    from views.enseignements_view import EnseignementsView
    from views.salles_view import SallesView
    from views.utilisateurs_view import UtilisateursView
    from views.matieres_view import MatieresView
    from views.notes_view import NotesView
    from views.presences_view import PresenceView
    from views.paiements_view import PaiementsView
    from views.bulletins_view import BulletinsView
    from views.emplois_view import EmploisView
except ImportError as e:
    print(f"Erreur import vues : {e}")
    DashboardEleves = lambda parent, icons: PlaceholderView(parent, "Dashboard Élèves")
    ProfessorsDashboard = lambda parent, icons: PlaceholderView(parent, "Dashboard Professeurs")
    ClassesManagerView = lambda parent, icons: PlaceholderView(parent, "Gestion des classes")
    EnseignementsView = lambda parent, icons: PlaceholderView(parent, "Gestion des Enseignements")
    SallesView = lambda parent, icons: PlaceholderView(parent, "Gestion des Salles")
    UtilisateursView = lambda parent, icons: PlaceholderView(parent, "Gestion des utilisateurs")
    MatieresView = lambda parent, icons: PlaceholderView(parent, "Gestion des Matières")
    NotesView = lambda parent, icons: PlaceholderView(parent, "Gestion des Notes")
    PresenceView = lambda parent, icons: PlaceholderView(parent, "Gestion des Présences")
    PaiementsView = lambda parent, icons: PlaceholderView(parent, "Gestion des Paiements")
    BulletinsView = lambda parent, icons: PlaceholderView(parent, "Gestion des Bulletins")
    EmploisView = lambda parent, icons: PlaceholderView(parent, "Gestion des Emplois du temps")

ICON_PATH = "assets/icons"
LOGO_PATH = "assets/logo.png"

def load_ctk_icon(icon_name, size=(20, 20)):
    try:
        path = os.path.join(ICON_PATH, icon_name)
        img = Image.open(path).resize(size, RESAMPLE_LANCZOS)
        return ctk.CTkImage(light_image=img, dark_image=img, size=size)
    except Exception as e:
        print(f"[Icon] {icon_name} : {e}")
        return None

def load_app_logo(size=(30, 30)):
    try:
        img = Image.open(LOGO_PATH).resize(size, RESAMPLE_LANCZOS)
        return ctk.CTkImage(light_image=img, dark_image=img, size=size)
    except Exception as e:
        print(f"[Logo] {LOGO_PATH} : {e}")
        return None

ICON_MAP = {
    "dashboard": "home.png", "eleves": "stacks.png", "utilisateurs": "user_avatar.png",
    "person": "person.png", "classes": "menu.png", "profs": "award.png",
    "salles": "cover.png", "logout": "logout.png", "presences": "check_circle.png",
    "notes": "edit.png", "bulletins": "csv.png", "paiements": "upload.png",
    "actualites": "bell.png", "annonces": "chevron_right.png", "notifications": "bell.png",
    "taches": "check.png", "biblio": "stacks.png", "refresh": "refresh.png",
    "search": "search.png", "enseignements": "book.png", "calendriers": "calendar.png",
    "carrieres": "briefcase.png", "competences": "star.png", "documents": "file.png",
    "emplois": "clock.png", "maintenances": "settings.png", "matieres": "book.png",
    "messagerie": "email.png", "objectifs": "target.png", "personnel": "group.png",
    "transfert": "upload.png", "settings": "settings.png",
    "calendar_icon": "calendar.png", "clock_icon": "clock.png", "date_icon": "folder.png"
}

VIEW_MAP = {
    "dashboard": DashboardEleves,
    "eleves": DashboardEleves,
    "utilisateurs": UtilisateursView,
    "classes": ClassesManagerView,
    "profs": ProfessorsDashboard,
    "salles": SallesView,
    "enseignements": EnseignementsView,
    "matieres": MatieresView,
    "notes": NotesView,
    "presences": PresenceView,
    "paiements": PaiementsView,
    "bulletins": BulletinsView,
    "emplois": EmploisView
}

# ====================================================================
# DB
# ====================================================================
def get_stats_count(table_name):
    try:
        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()
        cur.execute(f"SELECT COUNT(*) FROM {table_name}")
        v = cur.fetchone()[0]
        conn.close()
        return v
    except Exception as e:
        print(f"Erreur stats {table_name} : {e}")
        return 0

def get_student_counts_by_class():
    try:
        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()
        cur.execute("SELECT c.nom, COUNT(e.id_eleve) FROM classe c JOIN eleves e ON c.id_classe = e.id_classe GROUP BY c.nom")
        data = cur.fetchall()
        conn.close()
        return data
    except Exception as e:
        print(f"Erreur répartition élèves par classe : {e}")
        return []

# ====================================================================
# UI helpers
# ====================================================================
def stat_card(parent, title, value, icon_name, color):
    card = ctk.CTkFrame(parent, fg_color=CARD_BG, corner_radius=10, border_width=1, border_color=BORDER_COLOR)
    card.grid_columnconfigure(0, weight=1)
    card.grid_columnconfigure(1, weight=1)

    icon = load_ctk_icon(icon_name, size=(28, 28))
    ctk.CTkLabel(card, text=title.upper(), font=(THEME["FONT"], 12, "bold"), text_color=color)\
        .grid(row=0, column=0, padx=(10, 5), pady=(8, 0), sticky="nw")
    ctk.CTkLabel(card, text=value, font=(THEME["FONT"], FONT_SIZE_CARD_VALUE, "bold"), text_color=TEXT_COLOR)\
        .grid(row=1, column=0, padx=(10, 5), pady=(0, 8), sticky="nw")
    if icon:
        ctk.CTkLabel(card, image=icon, text="").grid(row=0, column=1, rowspan=2, padx=(0, 10), sticky="e")
    return card

def action_card(parent, label, key, icon_name, command=None):
    card = ctk.CTkFrame(parent, fg_color=CARD_BG, corner_radius=10, border_width=1,
                        border_color=BORDER_COLOR, width=100, height=80)
    card.pack_propagate(False)
    icon = load_ctk_icon(icon_name, size=(24, 24))
    if icon:
        ctk.CTkLabel(card, image=icon, text="").pack(pady=(5, 0))
    ctk.CTkLabel(card, text=label, font=(THEME["FONT"], 11, "bold"),
                  text_color=TEXT_COLOR, wraplength=80, justify="center").pack(pady=(2, 2))
    def on_enter(_): card.configure(fg_color=BTN_HOVER_COLOR, border_color=ACCENT_BLUE)
    def on_leave(_): card.configure(fg_color=CARD_BG, border_color=BORDER_COLOR)
    if command:
        card.bind("<Button-1>", lambda e: command(key))
        card.bind("<Enter>", on_enter); card.bind("<Leave>", on_leave)
        for w in card.winfo_children():
            w.bind("<Button-1>", lambda e: command(key))
            w.bind("<Enter>", on_enter); w.bind("<Leave>", on_leave)
    return card

# ====================================================================
# APPLICATION
# ====================================================================
class MainApp(ctk.CTk):
    def __init__(self, utilisateur):
        super().__init__()
        self.title("EduManager+ | Application de gestion")
        self.withdraw()
        self.minsize(1000, 700)
        self.after(60, self._maximize_on_start)
        self.configure(fg_color=BG_MAIN)
        self.utilisateur = utilisateur
        self.bind("<F11>", self._toggle_fullscreen)
        self.bind("<Escape>", self._exit_fullscreen)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # Nouvelle barre latérale avec un design raffiné
        self.sidebar_frame = ctk.CTkFrame(self, fg_color=BG_SIDEBAR, width=220, corner_radius=12, border_width=1, border_color=BORDER_COLOR)
        self.sidebar_frame.grid(row=0, column=0, sticky="ns", padx=10, pady=10)
        self.sidebar_frame.grid_propagate(False)
        self.sidebar_frame.grid_rowconfigure(99, weight=1)

        self.main_content = ctk.CTkFrame(self, fg_color=BG_MAIN, corner_radius=12, border_width=1, border_color=BORDER_COLOR)
        self.main_content.grid(row=0, column=1, sticky="nsew", padx=(0, 10), pady=10)

        self.icons = {k: load_ctk_icon(v) for k, v in ICON_MAP.items()}
        self.views = {}
        self.sidebar_btns = []

        self.frame_dashboard_content = ctk.CTkFrame(self.main_content, fg_color="transparent")
        self.frame_dashboard_content.grid_columnconfigure(0, weight=1)

        self.create_sidebar()
        self.create_dashboard()

        if self.sidebar_btns:
            self.set_active(0)
            self.show_vue_action("dashboard")

    # --- plein écran / maximisation ---
    def _maximize_on_start(self):
        self.update_idletasks()
        try:
            self.state('zoomed')
        except Exception:
            pass
        self.deiconify()
    def _toggle_fullscreen(self, _evt=None):
        cur = bool(self.attributes('-fullscreen'))
        self.attributes('-fullscreen', not cur)
    def _exit_fullscreen(self, _evt=None):
        if bool(self.attributes('-fullscreen')):
            self.attributes('-fullscreen', False)

    # --- sidebar & vues ---
    def create_sidebar(self):
        logo = load_app_logo(size=(35, 35))
        if logo:
            ctk.CTkLabel(self.sidebar_frame, image=logo, text="").grid(row=0, column=0, sticky="w", padx=15, pady=(20, 5))

        user_frame = ctk.CTkFrame(self.sidebar_frame, fg_color=HEADER_BG, corner_radius=8)
        user_frame.grid(row=1, column=0, sticky="ew", padx=10, pady=(10, 10))
        try:
            avatar_path = "assets/icons/user_avatar.png"
            avatar_image = Image.open(avatar_path).resize((30, 30), RESAMPLE_LANCZOS)
            avatar_ctk = ctk.CTkImage(light_image=avatar_image, dark_image=avatar_image, size=(30, 30))
            ctk.CTkLabel(user_frame, image=avatar_ctk, text="").pack(side="left", padx=(8, 5), pady=8)
        except FileNotFoundError:
            ctk.CTkLabel(user_frame, text="👤", font=(THEME["FONT"], 20, "bold"), text_color=TEXT_COLOR).pack(side="left", padx=(8, 5), pady=8)

        info_frame = ctk.CTkFrame(user_frame, fg_color="transparent")
        info_frame.pack(side="left", fill="y", expand=True)
        ctk.CTkLabel(info_frame, text=self.utilisateur["username"], font=(THEME["FONT"], 12, "bold"), text_color=TEXT_COLOR).pack(anchor="w", pady=(0,0))
        ctk.CTkLabel(info_frame, text="Administrateur", font=(THEME["FONT"], 10), text_color=SUBTEXT_COLOR).pack(anchor="w", pady=(0,0))

        nav_sections = {
            "SCOLARITÉ": [
                ("Tableau de bord", "dashboard"),
                ("Élèves", "eleves"),
                ("Professeurs", "profs"),
                ("Classes", "classes"),
                ("Salles", "salles"),
            ],
            "PÉDAGOGIE": [
                ("Enseignements", "enseignements"),
                ("Notes", "notes"),
                ("Présences", "presences"),
                ("Bulletins", "bulletins"),
                ("Emplois du temps", "emplois"),
            ],
            "FINANCES": [
                ("Paiements", "paiements"),
            ],
            "ADMINISTRATION": [
                ("Utilisateurs", "utilisateurs"),
            ]
        }

        row_idx = 2
        for section_title, buttons in nav_sections.items():
            ctk.CTkLabel(self.sidebar_frame, text=section_title, font=(THEME["FONT"], 10, "bold"),
                         text_color=SUBTEXT_COLOR, justify="left").grid(row=row_idx, column=0, sticky="w", padx=15, pady=(8, 2))
            row_idx += 1
            for text, key in buttons:
                icon_name = ICON_MAP.get(key, ICON_MAP["dashboard"])
                icon = load_ctk_icon(icon_name)
                btn = ctk.CTkButton(
                    self.sidebar_frame, text=text, image=icon, compound="left", anchor="w",
                    command=lambda k=key, i=len(self.sidebar_btns): [self.show_vue_action(k), self.set_active(i)],
                    font=(THEME["FONT"], 12, "bold"), fg_color="transparent",
                    hover_color=BTN_HOVER_COLOR, height=35, corner_radius=8
                )
                self.sidebar_btns.append(btn)
                btn.grid(row=row_idx, column=0, sticky="ew", pady=2, padx=10)
                row_idx += 1

        logout_icon = load_ctk_icon(ICON_MAP["logout"])
        ctk.CTkButton(self.sidebar_frame, text=" Déconnexion", image=logout_icon, compound="left",
                      font=(THEME["FONT"], 12, "bold"),
                      fg_color=PRIMARY_RED,
                      hover_color="#A34646",
                      corner_radius=8, height=35,
                      command=self.destroy).grid(row=99, column=0, sticky="sew", pady=(10, 10), padx=10)

    def show_vue_action(self, key):
        for w in self.main_content.winfo_children(): w.pack_forget()
        if key == "dashboard":
            self.frame_dashboard_content.pack(fill="both", expand=True, padx=10, pady=10)
            self.update_time()
            return
        if key in VIEW_MAP:
            if key not in self.views:
                cls = VIEW_MAP[key]
                try:
                    self.views[key] = cls(self.main_content, self.icons)
                except TypeError:
                    self.views[key] = cls(self.main_content)
            self.views[key].pack(fill="both", expand=True, padx=10, pady=10)
        elif key == "settings":
            PlaceholderView(self.main_content, "Paramètres").pack(fill="both", expand=True, padx=10, pady=10)
        else:
            PlaceholderView(self.main_content, key.capitalize()).pack(fill="both", expand=True, padx=10, pady=10)

    def set_active(self, idx_active):
        for i, b in enumerate(self.sidebar_btns):
            if i == idx_active:
                b.configure(fg_color=ACTIVE_BG, text_color=TEXT_COLOR, hover_color=ACTIVE_BG)
            else:
                b.configure(fg_color="transparent", text_color=TEXT_COLOR, hover_color=BTN_HOVER_COLOR)

    # --- Dashboard ---
    def refresh_dashboard(self, _=None):
        self.refresh_stats()
        self.update_graph()
        self.update_time()

    def create_dashboard(self):
        header_frame = ctk.CTkFrame(self.frame_dashboard_content, fg_color="transparent")
        header_frame.pack(fill="x", pady=(0, 10))
        header_frame.grid_columnconfigure(0, weight=1)
        header_frame.grid_columnconfigure(1, weight=1)

        greetings_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        greetings_frame.grid(row=0, column=0, sticky="w")
        ctk.CTkLabel(greetings_frame, text=f"Bonjour, {self.utilisateur['username']} 👋",
                     font=(THEME["FONT"], FONT_SIZE_TITLE, "bold"),
                     text_color=ACCENT_BLUE).pack(anchor="w", pady=(2, 0))
        ctk.CTkLabel(greetings_frame, text="Aperçu des statistiques de votre établissement.",
                     font=(THEME["FONT"], FONT_SIZE_SUBHEADER-2),
                     text_color=SUBTEXT_COLOR).pack(anchor="w", pady=(0, 2))

        search_refresh_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        search_refresh_frame.grid(row=0, column=1, sticky="e")
        ctk.CTkEntry(search_refresh_frame, placeholder_text="Rechercher...", width=200,
                     fg_color=CARD_BG, text_color=TEXT_COLOR,
                     border_color=BORDER_COLOR, corner_radius=8,
                     font=(THEME["FONT"], FONT_SIZE_TEXT-2)).pack(side="left", padx=(0, 5))
        refresh_icon = load_ctk_icon(ICON_MAP["refresh"], size=(18, 18))
        ctk.CTkButton(search_refresh_frame, text="", image=refresh_icon, width=35,
                      fg_color=CARD_BG, hover_color=BTN_HOVER_COLOR,
                      corner_radius=8, command=self.refresh_dashboard).pack(side="left")

        self.create_stats_cards()
        self.create_main_content_area()
        self.update_time()

    def create_stats_cards(self):
        self.stats_frame = ctk.CTkFrame(self.frame_dashboard_content, fg_color="transparent")
        self.stats_frame.pack(fill="x", pady=(5, 10))
        self.refresh_stats()

    def refresh_stats(self):
        data = [
            ("Total Élèves", get_stats_count("eleves"), ICON_MAP["eleves"], PRIMARY_GREEN),
            ("Classes", get_stats_count("classe"), ICON_MAP["classes"], ACCENT_BLUE),
            ("Professeurs", get_stats_count("professeurs"), ICON_MAP["profs"], PRIMARY_YELLOW),
            ("Salles", get_stats_count("salle"), ICON_MAP["salles"], PRIMARY_RED),
        ]
        for w in self.stats_frame.winfo_children(): w.destroy()
        for i, (t, v, ic, col) in enumerate(data):
            c = stat_card(self.stats_frame, t, v, ic, col)
            c.grid(row=0, column=i, padx=5, sticky="nsew")
            self.stats_frame.grid_columnconfigure(i, weight=1)

    def create_main_content_area(self):
        content = ctk.CTkFrame(self.frame_dashboard_content, fg_color="transparent")
        content.pack(fill="both", expand=True)
        content.grid_columnconfigure(0, weight=3)
        content.grid_columnconfigure(1, weight=1)
        content.grid_rowconfigure(0, weight=1)

        left = ctk.CTkFrame(content, fg_color="transparent")
        left.grid(row=0, column=0, sticky="nsew", padx=(0, 5))
        left.grid_rowconfigure(0, weight=1)
        left.grid_rowconfigure(1, weight=1)
        left.grid_columnconfigure(0, weight=1)
        left.grid_columnconfigure(1, weight=1)

        self.create_graph_box(left)
        self.create_all_actions_cards(left)

        right = ctk.CTkFrame(content, fg_color=CARD_BG, corner_radius=10,
                             border_width=1, border_color=BORDER_COLOR)
        right.grid(row=0, column=1, sticky="nsew")
        self.create_tasks_and_events(right)

    def create_tasks_and_events(self, parent):
        ctk.CTkLabel(parent, text="Vue Rapide",
                     font=(THEME["FONT"], FONT_SIZE_HEADER, "bold"),
                     text_color=TEXT_COLOR).pack(padx=10, pady=(10, 5), anchor="w")

        # Nouveau design pour la date et l'heure
        datetime_frame = ctk.CTkFrame(parent, fg_color=HEADER_BG, corner_radius=8)
        datetime_frame.pack(fill="x", padx=10, pady=(0, 10))

        # Heure avec grande icône et texte coloré
        time_frame = ctk.CTkFrame(datetime_frame, fg_color="transparent")
        time_frame.pack(fill="x", padx=8, pady=(8, 0))
        icon_time = load_ctk_icon("clock_icon.png", size=(24, 24))
        if icon_time:
            ctk.CTkLabel(time_frame, image=icon_time, text="", compound="left").pack(side="left")
        self.time_label = ctk.CTkLabel(time_frame, text="", font=(THEME["FONT"], FONT_SIZE_TITLE, "bold"), text_color=PRIMARY_GREEN)
        self.time_label.pack(side="left", padx=(5, 0))

        # Jour et date sous l'heure
        date_frame = ctk.CTkFrame(datetime_frame, fg_color="transparent")
        date_frame.pack(fill="x", padx=8, pady=(0, 8))
        self.day_label = ctk.CTkLabel(date_frame, text="", font=(THEME["FONT"], 16, "bold"), text_color=TEXT_COLOR)
        self.day_label.pack(side="left", padx=(5, 0))
        self.date_label = ctk.CTkLabel(date_frame, text="", font=(THEME["FONT"], 12), text_color=SUBTEXT_COLOR)
        self.date_label.pack(side="left", padx=(5, 0))

        # Nouvelle section d'événements qui prend tout l'espace restant
        ctk.CTkLabel(parent, text="Événements à venir",
                     font=(THEME["FONT"], FONT_SIZE_SUBHEADER, "bold"),
                     text_color=TEXT_COLOR).pack(padx=10, pady=(10, 5), anchor="w")
        events_scroll_frame = ctk.CTkScrollableFrame(parent, fg_color="transparent")
        events_scroll_frame.pack(fill="both", expand=True, padx=8, pady=3)
        events_data = [
            ("Réunion des parents", "15h00 - Salle A2"),
            ("Examen de Maths", "10h00 - Salle B1"),
            ("Sortie scolaire", "Toute la journée - Muséum"),
            ("Conseil de classe", "14h00 - Salle des profs"),
            ("Cours de sport", "16h00 - Gymnase"),
            ("Test d'Anglais", "09h00 - Salle C3"),
            ("Rendez-vous profs", "11h30 - Bureau principal"),
            ("Réunion équipe admin", "10h00 - Salle de conférence"),
        ]
        for title, subtitle in events_data:
            card = ctk.CTkFrame(events_scroll_frame, fg_color=HEADER_BG, corner_radius=8, border_width=1, border_color=BORDER_COLOR)
            card.pack(fill="x", pady=3)
            ctk.CTkLabel(card, text=title, font=(THEME["FONT"], FONT_SIZE_TEXT-2, "bold"),
                         text_color=TEXT_COLOR).pack(padx=8, pady=3, anchor="w")
            ctk.CTkLabel(card, text=subtitle, font=(THEME["FONT"], FONT_SIZE_TEXT-4),
                         text_color=SUBTEXT_COLOR).pack(padx=8, pady=(0, 3), anchor="w")


    def create_all_actions_cards(self, parent):
        wrap = ctk.CTkFrame(parent, fg_color=CARD_BG, corner_radius=10, border_width=1, border_color=BORDER_COLOR)
        wrap.grid(row=1, column=0, columnspan=2, sticky="nsew", pady=(5, 0))
        ctk.CTkLabel(wrap, text="Accès Rapide", font=(THEME["FONT"], FONT_SIZE_HEADER, "bold"),
                     text_color=TEXT_COLOR).pack(padx=10, pady=(10, 5), anchor="w")
        scroll = ctk.CTkScrollableFrame(wrap, fg_color="transparent"); scroll.pack(fill="both", expand=True, padx=8, pady=8)
        actions = [
            ("Enseignements", "enseignements"), ("Matieres", "matieres"),
            ("Bulletins", "bulletins"), ("Actualités", "actualites"),
            ("Annonces", "annonces"), ("Notifications", "notifications"),
            ("Tâches", "taches"), ("Bibliothèque", "biblio"),
            ("Calendriers", "calendriers"), ("Carrières", "carrieres"),
            ("Messagerie", "messagerie"), ("Paramètres", "settings")
        ]
        per_row = 4
        for i, (label, key) in enumerate(actions):
            r, c = divmod(i, per_row)
            action_card(scroll, label, key, ICON_MAP.get(key), command=self.show_vue_action)\
                .grid(row=r, column=c, padx=5, pady=5, sticky="nsew")
        for col in range(per_row):
            scroll.grid_columnconfigure(col, weight=1)

    def create_graph_box(self, parent):
        self.graph_box = ctk.CTkFrame(parent, fg_color=CARD_BG, corner_radius=10, border_width=1, border_color=BORDER_COLOR)
        self.graph_box.grid(row=0, column=0, columnspan=2, sticky="nsew", padx=(0, 5), pady=(0, 5))
        ctk.CTkLabel(self.graph_box, text="Moyenne par matière (Tendance)",
                     font=(THEME["FONT"], FONT_SIZE_HEADER, "bold"),
                     text_color=TEXT_COLOR).pack(padx=10, pady=(10, 5), anchor="w")
        self.update_graph()

    def update_time(self):
        current_time = datetime.datetime.now()
        day_str = current_time.strftime("%A")
        date_str = current_time.strftime("%d %B %Y")
        time_str = current_time.strftime("%H:%M:%S")

        if self.day_label.winfo_exists():
            self.day_label.configure(text=day_str)
        if self.date_label.winfo_exists():
            self.date_label.configure(text=date_str)
        if self.time_label.winfo_exists():
            self.time_label.configure(text=time_str)

        self.after(1000, self.update_time)

    def update_graph(self):
        for w in self.graph_box.winfo_children()[1:]: w.destroy()
        try:
            matieres = ["Maths", "Physique", "Français", "Anglais", "SVT", "Histoire"]
            moyennes = [15.5, 12.0, 17.0, 14.5, 13.0, 16.0]
            fig = plt.Figure(figsize=(5.5, 4.5), dpi=100)
            ax = fig.add_subplot(111)

            ax.fill_between(matieres, moyennes, color=ACCENT_BLUE, alpha=0.3)
            ax.plot(matieres, moyennes, color=ACCENT_BLUE, linewidth=2, marker='o', markersize=5)

            ax.set_facecolor(CARD_BG); fig.patch.set_facecolor(CARD_BG)
            ax.tick_params(colors=SUBTEXT_COLOR, labelsize=9, axis='x', rotation=45)
            ax.tick_params(colors=SUBTEXT_COLOR, labelsize=9, axis='y')
            ax.spines['bottom'].set_color(BORDER_COLOR); ax.spines['left'].set_color(BORDER_COLOR)
            ax.spines['top'].set_visible(False); ax.spines['right'].set_visible(False)
            ax.set_xlabel("Matières", color=SUBTEXT_COLOR); ax.set_ylabel("Moyenne", color=SUBTEXT_COLOR)

            canvas = FigureCanvasTkAgg(fig, master=self.graph_box); canvas.draw()
            canvas.get_tk_widget().pack(fill="both", expand=True, pady=(0, 10), padx=10)
        except Exception as e:
            print("Erreur du graphique:", e)


# ====================================================================
# Entrée
# ====================================================================
if __name__ == "__main__":
    utilisateur = {"username": "admin", "id": 1}
    app = MainApp(utilisateur)
    app.mainloop()