from database.connection import get_db_connection
from database.connection import get_db_connection
from database.connection import get_db_connection
import os
# Remplacé par SQL Server  # Remplacé par SQL Server
from datetime import datetime
import customtkinter as ctk
from tkinter import messagebox, filedialog
from tkcalendar import Calendar
from fpdf import FPDF
from PIL import Image
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

DB_PATH = r"database/edumanager.db"
ICON_DIR = r"C:\Users\Lenovo\Desktop\EduManager+\assets\icons"

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
    "transfert": "upload.png"
}

# Import du thème global EduManager+
try:
    import sys
    import os
    root_path = os.path.join(os.path.dirname(__file__), '../../../../..')
    sys.path.insert(0, root_path)
    from resources.themes.theme import *
    print("✅ Thème global EduManager+ importé pour les présences")
except ImportError as e:
    print(f"⚠️ Erreur import thème: {e}")
    # Fallback avec constantes locales
    BG_MAIN = "#0A192F"
    BG_SIDEBAR = "#172A45"
    BG_CARD = "#0B2039"
    BORDER_COLOR = "#334155"
    ACCENT_BLUE = "#64FFDA"
    TEXT_PRIMARY = "#CCD6F6"
    TEXT_SECONDARY = "#8892B0"
    ERROR_RED = "#FF6363"
    SUCCESS_GREEN = "#A0E7E5"
    WARNING_YELLOW = "#FFD700"
    INFO_ORANGE = "#F97316"
    HOVER_SUCCESS = "#8cd5d3"
    HOVER_ERROR = "#e55252"
    HOVER_PRIMARY = "#2A456C"

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green") # Use the default theme, but we'll override colors manually

FONT = "Segoe UI"
F_TITLE = (FONT, 20, "bold")
F_SUB = (FONT, 14, "bold")
F_TXT = (FONT, 12)
F_SMALL = (FONT, 10)
F_BOLD = (FONT, 12, "bold")

STATUTS = ["Présent", "Absent", "Retard", "Justifié"]

# Database and utility functions (unchanged)
def _connect():
    conn = get_db_connection()
    # conn.row_factory = sqlite3.Row  # Remplacé par SQL Server
    return conn

def get_all_classes():
    with _connect() as c:
        r = c.execute("SELECT id_classe, nom_classe FROM classes ORDER BY nom_classe").fetchall()
        return [{"id_classe": x[0], "nom_classe": x[1]} for x in r]

def get_all_eleves(classe_id, search_term="", statut_filter=None, date=None):
    with _connect() as c:
        q = "SELECT e.id_eleve, e.nom, e.prenom, e.email FROM eleves e WHERE e.id_classe=?"
        p = [classe_id]
        if search_term:
            pat = f"%{search_term}%"
            q += " AND (e.nom LIKE ? OR e.prenom LIKE ?)"
            p += [pat, pat]
        if statut_filter and statut_filter != "Tous" and date:
            q += " AND e.id_eleve IN (SELECT eleve_id FROM presences WHERE classe_id=? AND statut=? AND date=?)"
            p += [classe_id, statut_filter, date]
        q += " ORDER BY e.nom, e.prenom"
        return [{"id_eleve": r[0], "nom": r[1], "prenom": r[2], "email": r[3]} for r in c.execute(q, p).fetchall()]

def get_presence_for_date_and_class(classe_id, date):
    with _connect() as c:
        r = c.execute("""
            SELECT eleve_id, statut, commentaire
            FROM presences
            WHERE classe_id=? AND date=?
        """, (classe_id, date)).fetchall()
        return {row[0]: {"eleve_id": row[0], "statut": row[1], "commentaire": row[2]} for row in r}

def add_presence(eleve_id, classe_id, date, statut, commentaire, justificatif_path=None):
    with _connect() as c:
        c.execute("""
            INSERT INTO presences (eleve_id, classe_id, date, statut, commentaire)
            VALUES (?,?,?,?,?)
        """, (eleve_id, classe_id, date, statut, commentaire))
        c.commit()

def update_presence(eleve_id, classe_id, date, statut, commentaire, justificatif_path=None):
    with _connect() as c:
        c.execute("""
            UPDATE presences
            SET statut=?, commentaire=?
            WHERE eleve_id=? AND classe_id=? AND date=?
        """, (statut, commentaire, eleve_id, classe_id, date))
        c.commit()

def get_student_history(eleve_id):
    """Récupère l'historique complet des présences d'un élève"""
    with _connect() as c:
        return c.execute("""
            SELECT p.date, p.statut, p.commentaire, e.prenom, e.nom, c.nom_classe
            FROM presences p 
            JOIN eleves e ON p.eleve_id=e.id_eleve
            JOIN classes c ON p.classe_id=c.id_classe
            WHERE p.eleve_id=? 
            ORDER BY p.date DESC
        """, (eleve_id,)).fetchall()

def get_class_attendance_summary(classe_id, start_date=None, end_date=None):
    """Récupère un résumé des présences d'une classe sur une période"""
    with _connect() as c:
        query = """
            SELECT 
                p.date,
                COUNT(*) as total_eleves,
                SUM(CASE WHEN p.statut = 'Présent' THEN 1 ELSE 0 END) as presents,
                SUM(CASE WHEN p.statut = 'Absent' THEN 1 ELSE 0 END) as absents,
                SUM(CASE WHEN p.statut = 'Retard' THEN 1 ELSE 0 END) as retards,
                SUM(CASE WHEN p.statut = 'Justifié' THEN 1 ELSE 0 END) as justifies
            FROM presences p
            WHERE p.classe_id=?
        """
        params = [classe_id]
        
        if start_date:
            query += " AND p.date >= ?"
            params.append(start_date)
        if end_date:
            query += " AND p.date <= ?"
            params.append(end_date)
            
        query += " GROUP BY p.date ORDER BY p.date DESC"
        
        return c.execute(query, params).fetchall()

def get_student_attendance_stats(eleve_id, start_date=None, end_date=None):
    """Récupère les statistiques de présence d'un élève"""
    with _connect() as c:
        query = """
            SELECT 
                COUNT(*) as total_jours,
                SUM(CASE WHEN statut = 'Présent' THEN 1 ELSE 0 END) as presents,
                SUM(CASE WHEN statut = 'Absent' THEN 1 ELSE 0 END) as absents,
                SUM(CASE WHEN statut = 'Retard' THEN 1 ELSE 0 END) as retards,
                SUM(CASE WHEN statut = 'Justifié' THEN 1 ELSE 0 END) as justifies
            FROM presences
            WHERE eleve_id=?
        """
        params = [eleve_id]
        
        if start_date:
            query += " AND date >= ?"
            params.append(start_date)
        if end_date:
            query += " AND date <= ?"
            params.append(end_date)
            
        return c.execute(query, params).fetchone()

def get_monthly_attendance_data(classe_id, year, month):
    with _connect() as c:
        return c.execute("""
            SELECT e.prenom, e.nom, p.statut, p.date, p.commentaire
            FROM presences p JOIN eleves e ON p.eleve_id=e.id_eleve
            WHERE p.classe_id=? AND YEAR(p.date)=? AND MONTH(p.date)=?
            ORDER BY e.nom, e.prenom, p.date
        """, (classe_id, year, month)).fetchall()

def get_monthly_status_counts(classe_id, year, month):
    with _connect() as c:
        rows = c.execute("""
            SELECT statut, COUNT(*) c
            FROM presences
            WHERE classe_id=? AND YEAR(date)=? AND MONTH(date)=?
            GROUP BY statut
        """, (classe_id, year, month)).fetchall()
        return {r["statut"]: r["c"] for r in rows}

def get_absence_threshold():
    """Retourne le seuil d'absence injustifiée (valeur par défaut pour SQL Server)"""
    return 3  # Valeur par défaut

def get_unjustified_absences_count(eleve_id):
    with _connect() as c:
        r = c.execute("""
            SELECT COUNT(*) c
            FROM presences
            WHERE eleve_id=? AND statut='Absent' AND commentaire IS NULL
        """, (eleve_id,)).fetchone()
        return r[0]

def send_absent_notification(parent_email, student_name, classe_name, date_str):
    print(f"[EMAIL] Notification d'absence envoyée à {parent_email} pour {student_name} en {classe_name} le {date_str}.")

def validate_all_presences(classe_id, date_str, statut="Présent", commentaire=""):
    """Valide toutes les présences d'une classe pour une date donnée"""
    try:
        conn = _connect()
        if not conn:
            return False
        
        cursor = conn.cursor()
        
        # Récupérer tous les élèves de la classe
        eleves = get_all_eleves(classe_id)
        
        # Valider chaque élève
        for eleve in eleves:
            eleve_id = eleve["id_eleve"]
            
            # Vérifier si la présence existe déjà
            cursor.execute("""
                SELECT COUNT(*) FROM presences 
                WHERE eleve_id=? AND classe_id=? AND date=?
            """, (eleve_id, classe_id, date_str))
            
            exists = cursor.fetchone()[0] > 0
            
            if exists:
                # Mettre à jour
                cursor.execute("""
                    UPDATE presences 
                    SET statut=?, commentaire=?
                    WHERE eleve_id=? AND classe_id=? AND date=?
                """, (statut, commentaire, eleve_id, classe_id, date_str))
            else:
                # Insérer
                cursor.execute("""
                    INSERT INTO presences (eleve_id, classe_id, date, statut, commentaire)
                    VALUES (?,?,?,?,?)
                """, (eleve_id, classe_id, date_str, statut, commentaire))
        
        conn.commit()
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Erreur validation en masse: {e}")
        return False

# Main Application Class
class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("EduManager+ — Dashboard")
        self.geometry("1280x820")
        self.configure(fg_color=BG_MAIN)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.icons = {}
        self._load_icons()
        self._build_sidebar()
        self.main_content = ctk.CTkFrame(self, fg_color=BG_MAIN)
        self.main_content.grid(row=0, column=1, sticky="nsew", padx=16, pady=16)
        self.presence_view = PresenceView(self.main_content, self.icons)
        self.presence_view.pack(fill="both", expand=True)

    def _load_icons(self):
        for key, fname in ICON_MAP.items():
            path = os.path.join(ICON_DIR, fname)
            try:
                if os.path.exists(path):
                    im = Image.open(path)
                    self.icons[key] = ctk.CTkImage(im, im, size=(20, 20))
                else:
                    self.icons[key] = None
            except Exception:
                self.icons[key] = None

    def _build_sidebar(self):
        sidebar = ctk.CTkFrame(self, fg_color=BG_SIDEBAR, corner_radius=0)
        sidebar.grid(row=0, column=0, sticky="nsew")
        sidebar.grid_rowconfigure(6, weight=1)
        
        logo_frame = ctk.CTkFrame(sidebar, fg_color="transparent")
        logo_frame.grid(row=0, column=0, sticky="ew", padx=20, pady=(20, 10))
        ctk.CTkLabel(logo_frame, text="EduManager+", font=F_TITLE, text_color=ACCENT_BLUE).pack(side="left")
        
        def add_button(text, icon_key, row, command=None, is_active=False):
            btn = ctk.CTkButton(sidebar, text=text, image=self.icons.get(icon_key), compound="left",
                                 font=F_SUB,
                                 fg_color=HOVER_PRIMARY if is_active else "transparent",
                                 hover_color=HOVER_PRIMARY,
                                 text_color=TEXT_PRIMARY if is_active else TEXT_SECONDARY,
                                 corner_radius=8,
                                 anchor="w", command=command)
            btn.grid(row=row, column=0, sticky="ew", padx=10, pady=5)
            return btn
        
        add_button("Tableau de bord", "dashboard", 1)
        add_button("Présences", "presences", 2, is_active=True)
        add_button("Notes", "notes", 3)
        add_button("Bulletins", "bulletins", 4)
        add_button("Paiements", "paiements", 5)
        
        # Spacer
        spacer = ctk.CTkFrame(sidebar, fg_color="transparent")
        spacer.grid(row=6, column=0, sticky="nsew")

        add_button("Déconnexion", "logout", 7, command=lambda: self.destroy())

# Presence Management View
class PresenceView(ctk.CTkFrame):
    def __init__(self, parent, icons):
        super().__init__(parent, fg_color=BG_MAIN)
        self.icons = icons
        self.ic = lambda k: self.icons.get(k)
        self._classes = get_all_classes()
        self._classe_name_to_id = {c["nom_classe"]: c["id_classe"] for c in self._classes}
        self.selected_classe_id = None
        self.pres_map = {}
        self.eleves = []
        self.search_var = ctk.StringVar()
        self.filter_var = ctk.StringVar(value="Tous")
        self.current_student_id = None
        
        self.grid_columnconfigure(0, weight=1, uniform="group1")
        self.grid_columnconfigure(1, weight=2, uniform="group1")
        self.grid_rowconfigure(0, weight=1)

        self._build_main_layout()

        if self._classes:
            self.cb_class.set(self._classes[0]["nom_classe"])
        self.ent_date.insert(0, datetime.now().strftime("%Y-%m-%d"))
        self._reload()

    def _build_main_layout(self):
        # Left Panel (Master)
        master_panel = ctk.CTkFrame(self, fg_color=BG_CARD, corner_radius=12)
        master_panel.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        master_panel.grid_rowconfigure(3, weight=1)
        
        # Header for the master panel
        header_frame = ctk.CTkFrame(master_panel, fg_color="transparent")
        header_frame.pack(fill="x", padx=20, pady=(20, 10))
        ctk.CTkLabel(header_frame, text="Sélectionner une classes et une date", font=F_SUB, text_color=TEXT_PRIMARY).pack(anchor="w")

        # Controls
        controls_frame = ctk.CTkFrame(master_panel, fg_color="transparent")
        controls_frame.pack(fill="x", padx=20, pady=(0, 10))
        controls_frame.grid_columnconfigure(0, weight=1)
        controls_frame.grid_columnconfigure(1, weight=1)

        self.cb_class = ctk.CTkComboBox(controls_frame, values=[c["nom_classe"] for c in self._classes], command=lambda *_: self._reload(),
                                             fg_color=BG_SIDEBAR, border_color=BORDER_COLOR, text_color=TEXT_PRIMARY)
        self.cb_class.grid(row=0, column=0, sticky="ew", padx=(0, 5))
        
        date_frame = ctk.CTkFrame(controls_frame, fg_color=BG_SIDEBAR, border_color=BORDER_COLOR, border_width=1)
        date_frame.grid(row=0, column=1, sticky="ew", padx=(5, 0))
        date_frame.grid_columnconfigure(0, weight=1)
        self.ent_date = ctk.CTkEntry(date_frame, placeholder_text="AAAA-MM-JJ", border_width=0, fg_color="transparent", font=F_TXT)
        self.ent_date.grid(row=0, column=0, sticky="ew", padx=(8, 0))
        ctk.CTkButton(date_frame, text="", image=self.ic("calendriers"), width=30, fg_color="transparent",
                      hover_color=BG_CARD, command=self._pick_date).grid(row=0, column=1, padx=4, pady=4)

        # Search and Filter
        search_filter_frame = ctk.CTkFrame(master_panel, fg_color="transparent")
        search_filter_frame.pack(fill="x", padx=20, pady=(0, 10))
        search_filter_frame.grid_columnconfigure(0, weight=1)
        search_box = ctk.CTkEntry(search_filter_frame, textvariable=self.search_var, placeholder_text="Rechercher un élève...",
                                     fg_color=BG_SIDEBAR, border_color=BORDER_COLOR)
        search_box.grid(row=0, column=0, sticky="ew", padx=(0, 5))
        search_box.bind("<Return>", lambda _e: self._reload())
        
        self.filter_cb = ctk.CTkComboBox(search_filter_frame, values=["Tous"]+STATUTS, variable=self.filter_var,
                                             fg_color=BG_SIDEBAR, border_color=BORDER_COLOR,
                                             command=lambda *_: self._reload())
        self.filter_cb.grid(row=0, column=1, sticky="ew", padx=(5, 0))
        
        # Actions en masse
        bulk_actions_frame = ctk.CTkFrame(master_panel, fg_color="transparent")
        bulk_actions_frame.pack(fill="x", padx=20, pady=(0, 10))
        
        # Titre des actions
        ctk.CTkLabel(bulk_actions_frame, text="Actions en masse", font=F_SUB, text_color=TEXT_PRIMARY).pack(anchor="w", pady=(0, 8))
        
        # Boutons d'action
        buttons_frame = ctk.CTkFrame(bulk_actions_frame, fg_color="transparent")
        buttons_frame.pack(fill="x")
        buttons_frame.grid_columnconfigure((0, 1, 2), weight=1)
        
        # Bouton Valider tout comme Présent
        validate_all_btn = ctk.CTkButton(buttons_frame, text="✅ Valider tout Présent", 
                                        fg_color=SUCCESS_GREEN, text_color=BG_MAIN, hover_color=HOVER_SUCCESS,
                                        font=F_BOLD, command=self._validate_all_present)
        validate_all_btn.grid(row=0, column=0, sticky="ew", padx=(0, 5))
        
        # Bouton Marquer tout Absent
        mark_absent_btn = ctk.CTkButton(buttons_frame, text="❌ Marquer tout Absent", 
                                      fg_color=ERROR_RED, text_color="white", hover_color=HOVER_ERROR,
                                      font=F_BOLD, command=self._mark_all_absent)
        mark_absent_btn.grid(row=0, column=1, sticky="ew", padx=5)
        
        # Bouton Réinitialiser
        reset_btn = ctk.CTkButton(buttons_frame, text="🔄 Réinitialiser", 
                                 fg_color=WARNING_YELLOW, text_color=BG_MAIN, hover_color="#FFA500",
                                 font=F_BOLD, command=self._reset_all)
        reset_btn.grid(row=0, column=2, sticky="ew", padx=(5, 0))
        
        self.list_wrap = ctk.CTkScrollableFrame(master_panel, fg_color=BG_MAIN, corner_radius=0)
        self.list_wrap.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        # Right Panel (Detail)
        self.detail_panel = ctk.CTkFrame(self, fg_color=BG_CARD, corner_radius=12)
        self.detail_panel.grid(row=0, column=1, sticky="nsew")
        self._build_detail_panel()
        
    def _build_detail_panel(self):
        for w in self.detail_panel.winfo_children():
            w.destroy()
        
        self.detail_panel.grid_columnconfigure(0, weight=1)
        ctk.CTkLabel(self.detail_panel, text="Sélectionnez un élève pour voir les détails",
                      font=F_SUB, text_color=TEXT_SECONDARY).pack(pady=40, padx=20)
        
    def _render_detail_for(self, eleve_id):
        for w in self.detail_panel.winfo_children():
            w.destroy()
            
        self.detail_panel.grid_columnconfigure(0, weight=1)
        self.detail_panel.grid_rowconfigure(2, weight=1)
        
        e = next((x for x in self.eleves if x["id_eleve"] == eleve_id), None)
        if not e:
            self._build_detail_panel()
            return
        
        self.current_student_id = eleve_id
        p = self.pres_map.get(eleve_id, {})
        statut = p.get("statut") or "Présent"
        commentaire = p.get("commentaire", "")
        justificatif = p.get("commentaire", "")
        
        header_frame = ctk.CTkFrame(self.detail_panel, fg_color="transparent")
        header_frame.pack(fill="x", padx=20, pady=(20, 10))
        
        ctk.CTkLabel(header_frame, text=f"{e['prenom']} {e['nom']}", font=F_TITLE, text_color=TEXT_PRIMARY).pack(side="left")
        ctk.CTkButton(header_frame, text="Historique", image=self.ic("documents"),
                      fg_color=ACCENT_BLUE, text_color=BG_MAIN, hover_color=ACCENT_BLUE,
                      command=lambda: self._history(eleve_id)).pack(side="right")
        
        content_frame = ctk.CTkFrame(self.detail_panel, fg_color="transparent")
        content_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        ctk.CTkLabel(content_frame, text="Statut du jour", font=F_TXT, text_color=TEXT_SECONDARY).pack(anchor="w", pady=(0, 5))
        v_statut = ctk.StringVar(value=statut)
        seg = ctk.CTkSegmentedButton(content_frame, values=STATUTS, variable=v_statut,
                                         selected_color=ACCENT_BLUE, selected_hover_color=ACCENT_BLUE,
                                         unselected_color=BG_SIDEBAR, unselected_hover_color=BG_CARD,
                                         font=F_TXT,
                                         text_color=BG_MAIN, text_color_disabled=TEXT_SECONDARY)
        seg.pack(fill="x", pady=(0, 15))
        
        ctk.CTkLabel(content_frame, text="Commentaire", font=F_TXT, text_color=TEXT_SECONDARY).pack(anchor="w", pady=(0, 5))
        txt = ctk.CTkTextbox(content_frame, height=120, fg_color=BG_SIDEBAR, border_color=BORDER_COLOR, font=F_TXT, text_color=TEXT_PRIMARY)
        txt.pack(fill="x", pady=(0, 15))
        if commentaire:
            txt.insert("1.0", commentaire)
            
        ctk.CTkLabel(content_frame, text="Justificatif", font=F_TXT, text_color=TEXT_SECONDARY).pack(anchor="w", pady=(0, 5))
        wrap = ctk.CTkFrame(content_frame, fg_color=BG_SIDEBAR, border_color=BORDER_COLOR, border_width=1, corner_radius=6)
        wrap.pack(fill="x", pady=(0, 20))
        
        path_v = ctk.StringVar(value=justificatif)
        ent = ctk.CTkEntry(wrap, textvariable=path_v, placeholder_text="Chemin vers le fichier (PDF/JPG/PNG)…",
                             border_width=0, fg_color="transparent", font=F_TXT, text_color=TEXT_PRIMARY)
        ent.pack(side="left", fill="x", expand=True, padx=8)
        
        ctk.CTkButton(wrap, text="", image=self.ic("documents"), width=40,
                      fg_color=BG_CARD, hover_color=BG_MAIN,
                      command=lambda: self._pick_file(path_v)).pack(side="left", padx=4, pady=4)
        
        btns_frame = ctk.CTkFrame(self.detail_panel, fg_color="transparent")
        btns_frame.pack(pady=(0, 20))
        
        def apply_one():
            self._apply_one(eleve_id, v_statut.get(), txt.get("1.0", "end-1c").strip(), path_v.get().strip())
        
        ctk.CTkButton(btns_frame, text="Appliquer", image=self.ic("taches"), font=F_BOLD,
                      fg_color=SUCCESS_GREEN, text_color=BG_MAIN, hover_color="#8cd5d3", command=apply_one).pack(side="left", padx=5)
        
        ctk.CTkButton(btns_frame, text="Annuler", image=self.ic("logout"), font=F_BOLD,
                      fg_color=ERROR_RED, text_color=BG_MAIN, hover_color="#e55252", command=lambda: self._render_detail_for(eleve_id)).pack(side="left", padx=5)

    def _reload(self):
        classes = self.cb_class.get()
        if not classes:
            return
            
        self.selected_classe_id = self._classe_name_to_id.get(classes)
        date_str = self.ent_date.get().strip()
        self.pres_map = get_presence_for_date_and_class(self.selected_classe_id, date_str) if date_str else {}
        self.eleves = get_all_eleves(self.selected_classe_id,
                                         self.search_var.get().strip(),
                                         self.filter_var.get(), date_str)
        
        for w in self.list_wrap.winfo_children():
            w.destroy()
            
        counts = {"Présent": 0, "Absent": 0, "Retard": 0, "Justifié": 0}
        seuil = get_absence_threshold()
        
        for e in self.eleves:
            eid = e["id_eleve"]
            p = self.pres_map.get(eid, {})
            # Par défaut, tous les élèves sont présents
            statut = p.get("statut") if p.get("statut") else "Présent"
            counts[statut] = counts.get(statut, 0) + 1
            
            item_bg = HOVER_PRIMARY if eid == self.current_student_id else BG_CARD
            item_hover = HOVER_PRIMARY
            
            item = ctk.CTkFrame(self.list_wrap, fg_color=item_bg, corner_radius=8, cursor="hand2")
            item.pack(fill="x", padx=5, pady=4)
            item.bind("<Button-1>", lambda event, sid=eid: self._render_detail_for(sid))
            
            ctk.CTkLabel(item, text="", image=self.ic("person")).pack(side="left", padx=(10, 5), pady=8)
            
            name = ctk.CTkLabel(item, text=f"{e['prenom']} {e['nom']}", font=F_TXT, text_color=TEXT_PRIMARY)
            name.pack(side="left", padx=(0, 10))
            
            color_map = {
                "Présent": SUCCESS_GREEN,
                "Absent": ERROR_RED,
                "Retard": WARNING_YELLOW,
                "Justifié": INFO_ORANGE
            }
            color = color_map.get(statut, TEXT_SECONDARY)
            
            tag = ctk.CTkLabel(item, text=statut, text_color=BG_MAIN, fg_color=color, corner_radius=999, width=70, font=F_SMALL)
            tag.pack(side="right", padx=10)
            
            abs_c = get_unjustified_absences_count(eid)
            if abs_c >= seuil:
                ctk.CTkLabel(item, text=f"({abs_c} abs. injustifiées)", text_color=ERROR_RED, font=F_SMALL).pack(side="right", padx=5)

        # Statistiques améliorées
        self.master_stats = ctk.CTkFrame(self.list_wrap, fg_color=BG_CARD, corner_radius=12, border_width=1, border_color=BORDER_COLOR)
        self.master_stats.pack(fill="x", pady=10)
        
        # Header des statistiques
        stats_header = ctk.CTkFrame(self.master_stats, fg_color="transparent")
        stats_header.pack(fill="x", padx=15, pady=(12, 8))
        
        classe_name = self.cb_class.get() or "Aucune classe"
        date_str = self.ent_date.get() or "Aucune date"
        total_eleves = len(self.eleves)
        
        ctk.CTkLabel(stats_header, text=f"📊 Statistiques - {classe_name} ({date_str})", 
                     font=F_SUB, text_color=TEXT_PRIMARY).pack(side="left")
        ctk.CTkLabel(stats_header, text=f"Total: {total_eleves} élèves", 
                     font=F_SMALL, text_color=TEXT_SECONDARY).pack(side="right")
        
        # Chips des statistiques
        chips_frame = ctk.CTkFrame(self.master_stats, fg_color="transparent")
        chips_frame.pack(fill="x", padx=15, pady=(0, 12))
        chips_frame.grid_columnconfigure((0, 1, 2, 3), weight=1)

        def add_chip(label, count, color, col, icon=""):
            chip_frame = ctk.CTkFrame(chips_frame, fg_color=BG_SIDEBAR, corner_radius=8, border_width=1, border_color=color)
            chip_frame.grid(row=0, column=col, sticky="ew", padx=5)
            
            # Header du chip
            chip_header = ctk.CTkFrame(chip_frame, fg_color="transparent")
            chip_header.pack(fill="x", padx=8, pady=(6, 2))
            
            ctk.CTkLabel(chip_header, text=f"{icon} {label}", font=F_SMALL, text_color=color).pack(side="left")
            
            # Valeur
            ctk.CTkLabel(chip_frame, text=str(count), font=("Segoe UI", 16, "bold"), text_color=TEXT_PRIMARY).pack(pady=(0, 6))
            
            # Pourcentage si applicable
            if total_eleves > 0:
                percentage = (count / total_eleves) * 100
                ctk.CTkLabel(chip_frame, text=f"{percentage:.1f}%", font=F_SMALL, text_color=TEXT_SECONDARY).pack(pady=(0, 4))
        
        add_chip("Présents", counts.get("Présent", 0), SUCCESS_GREEN, 0, "✅")
        add_chip("Absents", counts.get("Absent", 0), ERROR_RED, 1, "❌")
        add_chip("Retards", counts.get("Retard", 0), WARNING_YELLOW, 2, "⏰")
        add_chip("Justifiés", counts.get("Justifié", 0), INFO_ORANGE, 3, "📝")
        
        if self.current_student_id not in [e["id_eleve"] for e in self.eleves]:
            self._build_detail_panel()
            self.current_student_id = None

    def _pick_date(self):
        top = ctk.CTkToplevel(self)
        top.title("Choisir une date")
        top.configure(fg_color=BG_MAIN)
        top.grab_set()
        
        cal = Calendar(top, selectmode="day",
                       background=BG_CARD,
                       foreground=TEXT_PRIMARY,
                       selectbackground=ACCENT_BLUE,
                       headersbackground=BG_SIDEBAR,
                       normalbackground=BG_MAIN,
                       weekendbackground=BG_MAIN,
                       bordercolor=BORDER_COLOR)
        cal.pack(padx=10, pady=10)
        
        def ok():
            self.ent_date.delete(0, "end")
            self.ent_date.insert(0, cal.selection_get().strftime("%Y-%m-%d"))
            top.destroy()
            self._reload()
            
        ctk.CTkButton(top, text="OK", fg_color=ACCENT_BLUE, text_color=BG_MAIN, hover_color=ACCENT_BLUE, command=ok).pack(pady=8)

    def _pick_file(self, var):
        p = filedialog.askopenfilename(title="Sélectionner un justificatif",
                                             filetypes=[("PDF", "*.pdf"), ("Images", "*.jpg;*.jpeg;*.png"), ("Tous", "*.*")])
        if p:
            var.set(p)

    def _apply_one(self, eleve_id, statut, commentaire, path):
        if not self.selected_classe_id:
            messagebox.showwarning("Attention", "Sélectionnez une classes.")
            return
        
        date_str = self.ent_date.get().strip()
        if not date_str:
            messagebox.showwarning("Attention", "Indique la date.")
            return
            
        try:
            datetime.strptime(date_str, "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Erreur", "Format date invalide (AAAA-MM-JJ).")
            return
        
        if eleve_id in self.pres_map:
            update_presence(eleve_id, self.selected_classe_id, date_str, statut, commentaire, path)
        else:
            add_presence(eleve_id, self.selected_classe_id, date_str, statut, commentaire, path)
            
        messagebox.showinfo("OK", "Présence mise à jour pour l’élève.")
        self._reload()
        self._render_detail_for(eleve_id)

    def _report_pdf(self):
        if not self.selected_classe_id:
            messagebox.showwarning("Attention", "Sélectionnez une classes.")
            return
            
        classes = self.cb_class.get()
        y = datetime.now().strftime("%Y")
        m = datetime.now().strftime("%m")
        month_name = datetime.now().strftime("%B")
        
        data = get_monthly_attendance_data(self.selected_classe_id, y, m)
        if not data:
            messagebox.showinfo("Rapport", "Aucune donnée ce mois.")
            return
            
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", 'B', 16)
        pdf.cell(200, 10, txt=f"Rapport de présence - {classes} ({month_name} {y})", ln=True, align='C')
        pdf.ln(6)
        
        pdf.set_font("Arial", 'B', 11)
        pdf.cell(55, 8, "Nom & Prénom", 1)
        pdf.cell(28, 8, "Date", 1)
        pdf.cell(25, 8, "Statut", 1)
        pdf.cell(0, 8, "Commentaire", 1, ln=True)
        pdf.set_font("Arial", '', 10)
        
        for r in data:
            pdf.cell(55, 8, f"{r['prenom']} {r['nom']}", 1)
            pdf.cell(28, 8, r['date'], 1)
            pdf.cell(25, 8, r['statut'], 1)
            pdf.cell(0, 8, (r['commentaire'] or "")[:80], 1, ln=True)
            
        path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF", "*.pdf")],
                                             initialfile=f"Rapport_Presences_{classes}_{y}_{m}.pdf")
        if path:
            pdf.output(path)
            messagebox.showinfo("PDF", f"Rapport sauvegardé : {path}")

    def _history(self, eid):
        """Affiche l'historique complet des présences d'un élève"""
        rows = get_student_history(eid)
        if not rows:
            messagebox.showinfo("Historique", "Aucun historique pour cet élève.")
            return
        
        # Récupérer les statistiques de l'élève
        stats = get_student_attendance_stats(eid)
        
        nom = f"{rows[0]['prenom']} {rows[0]['nom']}"
        win = ctk.CTkToplevel(self)
        win.title(f"Historique des présences - {nom}")
        win.geometry("900x700")
        win.configure(fg_color=BG_MAIN)
        win.grab_set()
        
        # Header avec informations de l'élève
        header_frame = ctk.CTkFrame(win, fg_color=BG_CARD, corner_radius=12)
        header_frame.pack(fill="x", padx=15, pady=15)
        
        # Nom de l'élève
        title_label = ctk.CTkLabel(header_frame, text=f"📋 Historique de {nom}", 
                                  font=("Segoe UI", 18, "bold"), text_color=TEXT_PRIMARY)
        title_label.pack(pady=(15, 10))
        
        # Statistiques globales
        if stats:
            stats_frame = ctk.CTkFrame(header_frame, fg_color=BG_SIDEBAR, corner_radius=8)
            stats_frame.pack(fill="x", padx=15, pady=(0, 15))
            
            stats_inner = ctk.CTkFrame(stats_frame, fg_color="transparent")
            stats_inner.pack(fill="x", padx=10, pady=10)
            stats_inner.grid_columnconfigure((0, 1, 2, 3, 4), weight=1)
            
            total_jours = stats[0] or 0
            presents = stats[1] or 0
            absents = stats[2] or 0
            retards = stats[3] or 0
            justifies = stats[4] or 0
            
            def create_stat_item(text, value, color, col):
                item_frame = ctk.CTkFrame(stats_inner, fg_color="transparent")
                item_frame.grid(row=0, column=col, sticky="ew", padx=2)
                ctk.CTkLabel(item_frame, text=text, font=F_SMALL, text_color=TEXT_SECONDARY).pack()
                ctk.CTkLabel(item_frame, text=str(value), font=F_BOLD, text_color=color).pack()
            
            create_stat_item("Total", total_jours, TEXT_PRIMARY, 0)
            create_stat_item("Présents", presents, SUCCESS_GREEN, 1)
            create_stat_item("Absents", absents, ERROR_RED, 2)
            create_stat_item("Retards", retards, WARNING_YELLOW, 3)
            create_stat_item("Justifiés", justifies, INFO_ORANGE, 4)
            
            # Taux de présence
            if total_jours > 0:
                taux_presence = (presents / total_jours) * 100
                taux_label = ctk.CTkLabel(stats_frame, 
                                        text=f"📊 Taux de présence: {taux_presence:.1f}%", 
                                        font=F_SUB, text_color=ACCENT_BLUE)
                taux_label.pack(pady=(0, 10))
        
        # Liste des présences avec filtres
        controls_frame = ctk.CTkFrame(win, fg_color="transparent")
        controls_frame.pack(fill="x", padx=15, pady=(0, 10))
        
        # Filtres
        filter_frame = ctk.CTkFrame(controls_frame, fg_color=BG_CARD, corner_radius=8)
        filter_frame.pack(fill="x", padx=5)
        
        filter_inner = ctk.CTkFrame(filter_frame, fg_color="transparent")
        filter_inner.pack(fill="x", padx=10, pady=8)
        
        ctk.CTkLabel(filter_inner, text="Filtrer par statut:", font=F_TXT, text_color=TEXT_PRIMARY).pack(side="left", padx=(0, 10))
        
        filter_var = ctk.StringVar(value="Tous")
        filter_combo = ctk.CTkComboBox(filter_inner, values=["Tous"] + STATUTS, variable=filter_var,
                                      fg_color=BG_SIDEBAR, border_color=BORDER_COLOR, width=120)
        filter_combo.pack(side="left", padx=(0, 10))
        
        # Zone de recherche
        search_var = ctk.StringVar()
        search_entry = ctk.CTkEntry(filter_inner, textvariable=search_var, placeholder_text="Rechercher par date...",
                                   fg_color=BG_SIDEBAR, border_color=BORDER_COLOR, width=200)
        search_entry.pack(side="left", padx=(0, 10))
        
        # Liste scrollable des présences
        list_frame = ctk.CTkScrollableFrame(win, fg_color=BG_CARD, corner_radius=12)
        list_frame.pack(fill="both", expand=True, padx=15, pady=(0, 15))
        
        def update_history_display():
            """Met à jour l'affichage de l'historique selon les filtres"""
            # Nettoyer la liste
            for widget in list_frame.winfo_children():
                widget.destroy()
            
            # Filtrer les données
            filtered_rows = rows
            statut_filter = filter_var.get()
            search_term = search_var.get().lower()
            
            if statut_filter != "Tous":
                filtered_rows = [r for r in filtered_rows if r["statut"] == statut_filter]
            
            if search_term:
                filtered_rows = [r for r in filtered_rows if search_term in str(r["date"]).lower()]
            
            # Afficher les résultats
            if not filtered_rows:
                no_data_frame = ctk.CTkFrame(list_frame, fg_color="transparent")
                no_data_frame.pack(fill="x", padx=20, pady=20)
                ctk.CTkLabel(no_data_frame, text="Aucun résultat trouvé", 
                            font=F_TXT, text_color=TEXT_SECONDARY).pack()
                return
            
            # Header de la liste
            header_list = ctk.CTkFrame(list_frame, fg_color=BG_SIDEBAR, corner_radius=8)
            header_list.pack(fill="x", padx=5, pady=(5, 10))
            
            header_inner = ctk.CTkFrame(header_list, fg_color="transparent")
            header_inner.pack(fill="x", padx=10, pady=8)
            
            ctk.CTkLabel(header_inner, text="Date", font=F_BOLD, text_color=TEXT_PRIMARY, width=120).pack(side="left")
            ctk.CTkLabel(header_inner, text="Statut", font=F_BOLD, text_color=TEXT_PRIMARY, width=100).pack(side="left", padx=10)
            ctk.CTkLabel(header_inner, text="Classe", font=F_BOLD, text_color=TEXT_PRIMARY, width=120).pack(side="left", padx=10)
            ctk.CTkLabel(header_inner, text="Commentaire", font=F_BOLD, text_color=TEXT_PRIMARY).pack(side="left", padx=10)
            
            # Lignes de données
            for r in filtered_rows:
                line = ctk.CTkFrame(list_frame, fg_color=BG_SIDEBAR, corner_radius=8)
                line.pack(fill="x", padx=5, pady=2)
                
                line_inner = ctk.CTkFrame(line, fg_color="transparent")
                line_inner.pack(fill="x", padx=10, pady=6)
                
                # Date
                date_str = r["date"].strftime("%d/%m/%Y") if hasattr(r["date"], 'strftime') else str(r["date"])
                ctk.CTkLabel(line_inner, text=date_str, font=F_TXT, text_color=TEXT_PRIMARY, width=120).pack(side="left")
                
                # Statut avec couleur
                statut_color = {
                    "Présent": SUCCESS_GREEN,
                    "Absent": ERROR_RED,
                    "Retard": WARNING_YELLOW,
                    "Justifié": INFO_ORANGE
                }.get(r["statut"], TEXT_SECONDARY)
                
                statut_label = ctk.CTkLabel(line_inner, text=r["statut"], font=F_TXT, 
                                           text_color="white", fg_color=statut_color, 
                                           corner_radius=12, width=100)
                statut_label.pack(side="left", padx=10)
                
                # Classe
                classe_name = r.get("nom_classe", "N/A")
                ctk.CTkLabel(line_inner, text=classe_name, font=F_TXT, text_color=TEXT_SECONDARY, width=120).pack(side="left", padx=10)
                
                # Commentaire
                commentaire = r["commentaire"] or "-"
                ctk.CTkLabel(line_inner, text=commentaire[:50] + "..." if len(commentaire) > 50 else commentaire, 
                            font=F_TXT, text_color=TEXT_PRIMARY).pack(side="left", padx=10)
        
        # Bindings pour les filtres
        filter_combo.configure(command=lambda *_: update_history_display())
        search_entry.bind("<KeyRelease>", lambda *_: update_history_display())
        
        # Affichage initial
        update_history_display()
        
        # Boutons d'action
        actions_frame = ctk.CTkFrame(win, fg_color="transparent")
        actions_frame.pack(fill="x", padx=15, pady=(0, 15))
        
        export_btn = ctk.CTkButton(actions_frame, text="📄 Exporter PDF", 
                                   fg_color=ACCENT_BLUE, text_color="white", hover_color="#4ECDC4",
                                   font=F_BOLD, command=lambda: self._export_student_history(eid, nom))
        export_btn.pack(side="left", padx=(0, 10))
        
        close_btn = ctk.CTkButton(actions_frame, text="❌ Fermer", 
                                 fg_color=ERROR_RED, text_color="white", hover_color=HOVER_ERROR,
                                 font=F_BOLD, command=win.destroy)
        close_btn.pack(side="right")

    def _export_student_history(self, eleve_id, nom_eleve):
        """Exporte l'historique d'un élève en PDF"""
        try:
            rows = get_student_history(eleve_id)
            stats = get_student_attendance_stats(eleve_id)
            
            if not rows:
                messagebox.showwarning("Export", "Aucun historique à exporter.")
                return
            
            pdf = FPDF()
            pdf.add_page()
            
            # En-tête
            pdf.set_font("Arial", 'B', 16)
            pdf.cell(200, 10, txt=f"Historique des présences - {nom_eleve}", ln=True, align='C')
            pdf.ln(6)
            
            # Statistiques
            if stats:
                pdf.set_font("Arial", 'B', 12)
                pdf.cell(200, 8, txt="Statistiques globales", ln=True)
                pdf.set_font("Arial", '', 10)
                
                total_jours = stats[0] or 0
                presents = stats[1] or 0
                absents = stats[2] or 0
                retards = stats[3] or 0
                justifies = stats[4] or 0
                
                pdf.cell(100, 6, f"Total des jours: {total_jours}", ln=True)
                pdf.cell(100, 6, f"Présents: {presents}", ln=True)
                pdf.cell(100, 6, f"Absents: {absents}", ln=True)
                pdf.cell(100, 6, f"Retards: {retards}", ln=True)
                pdf.cell(100, 6, f"Justifiés: {justifies}", ln=True)
                
                if total_jours > 0:
                    taux_presence = (presents / total_jours) * 100
                    pdf.cell(100, 6, f"Taux de présence: {taux_presence:.1f}%", ln=True)
                
                pdf.ln(6)
            
            # Tableau des présences
            pdf.set_font("Arial", 'B', 11)
            pdf.cell(40, 8, "Date", 1)
            pdf.cell(30, 8, "Statut", 1)
            pdf.cell(50, 8, "Classe", 1)
            pdf.cell(0, 8, "Commentaire", 1, ln=True)
            
            pdf.set_font("Arial", '', 9)
            for r in rows:
                date_str = r["date"].strftime("%d/%m/%Y") if hasattr(r["date"], 'strftime') else str(r["date"])
                pdf.cell(40, 6, date_str, 1)
                pdf.cell(30, 6, r["statut"], 1)
                pdf.cell(50, 6, r.get("nom_classe", "N/A"), 1)
                commentaire = (r["commentaire"] or "")[:60]
                pdf.cell(0, 6, commentaire, 1, ln=True)
            
            # Sauvegarde
            path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF", "*.pdf")],
                                               initialfile=f"Historique_{nom_eleve.replace(' ', '_')}.pdf")
            if path:
                pdf.output(path)
                messagebox.showinfo("Export PDF", f"Historique exporté: {path}")
                
        except Exception as e:
            messagebox.showerror("Erreur Export", f"Erreur lors de l'export: {e}")

    def _validate_all_present(self):
        """Valide toutes les présences comme Présent"""
        if not self.selected_classe_id:
            messagebox.showwarning("Attention", "Sélectionnez une classe.")
            return
        
        date_str = self.ent_date.get().strip()
        if not date_str:
            messagebox.showwarning("Attention", "Indiquez la date.")
            return
        
        try:
            datetime.strptime(date_str, "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Erreur", "Format date invalide (AAAA-MM-JJ).")
            return
        
        # Confirmation
        classe_name = self.cb_class.get()
        if messagebox.askyesno("Confirmation", 
                              f"Valider toutes les présences comme 'Présent' pour la classe {classe_name} le {date_str} ?"):
            
            success = validate_all_presences(self.selected_classe_id, date_str, "Présent", "Validation en masse")
            
            if success:
                messagebox.showinfo("Succès", f"Toutes les présences ont été validées comme 'Présent' pour {len(self.eleves)} élèves.")
                self._reload()
            else:
                messagebox.showerror("Erreur", "Erreur lors de la validation en masse.")

    def _mark_all_absent(self):
        """Marque toutes les présences comme Absent"""
        if not self.selected_classe_id:
            messagebox.showwarning("Attention", "Sélectionnez une classe.")
            return
        
        date_str = self.ent_date.get().strip()
        if not date_str:
            messagebox.showwarning("Attention", "Indiquez la date.")
            return
        
        try:
            datetime.strptime(date_str, "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Erreur", "Format date invalide (AAAA-MM-JJ).")
            return
        
        # Confirmation
        classe_name = self.cb_class.get()
        if messagebox.askyesno("Confirmation", 
                              f"Marquer toutes les présences comme 'Absent' pour la classe {classe_name} le {date_str} ?"):
            
            success = validate_all_presences(self.selected_classe_id, date_str, "Absent", "Marquage en masse")
            
            if success:
                messagebox.showinfo("Succès", f"Toutes les présences ont été marquées comme 'Absent' pour {len(self.eleves)} élèves.")
                self._reload()
            else:
                messagebox.showerror("Erreur", "Erreur lors du marquage en masse.")

    def _reset_all(self):
        """Réinitialise toutes les présences (supprime les enregistrements)"""
        if not self.selected_classe_id:
            messagebox.showwarning("Attention", "Sélectionnez une classe.")
            return
        
        date_str = self.ent_date.get().strip()
        if not date_str:
            messagebox.showwarning("Attention", "Indiquez la date.")
            return
        
        try:
            datetime.strptime(date_str, "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Erreur", "Format date invalide (AAAA-MM-JJ).")
            return
        
        # Confirmation
        classe_name = self.cb_class.get()
        if messagebox.askyesno("Confirmation", 
                              f"Réinitialiser toutes les présences pour la classe {classe_name} le {date_str} ?\n\nCela supprimera tous les enregistrements de présence pour cette date."):
            
            try:
                conn = _connect()
                if not conn:
                    messagebox.showerror("Erreur", "Impossible de se connecter à la base de données.")
                    return
                
                cursor = conn.cursor()
                cursor.execute("""
                    DELETE FROM presences 
                    WHERE classe_id=? AND date=?
                """, (self.selected_classe_id, date_str))
                
                conn.commit()
                conn.close()
                
                messagebox.showinfo("Succès", f"Toutes les présences ont été réinitialisées pour {len(self.eleves)} élèves.")
                self._reload()
                
            except Exception as e:
                messagebox.showerror("Erreur", f"Erreur lors de la réinitialisation: {e}")

if __name__ == "__main__":
    app = App()
    app.mainloop()