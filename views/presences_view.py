import os
import sqlite3
from datetime import datetime
import customtkinter as ctk
from tkinter import messagebox, filedialog
from tkcalendar import Calendar
from fpdf import FPDF
from PIL import Image
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

DB_PATH = r"C:\Users\Lenovo\Desktop\EduManager+\database\edumanager.db"
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

# New Color Theme
THEME = {
    "bg_main": "#0A192F",
    "header_bg": "#172A45",
    "card_bg": "#0B2039",
    "border_color": "#334155",
    "accent_blue": "#64FFDA",
    "primary_text": "#CCD6F6",
    "secondary_text": "#8892B0",
    "error_red": "#FF6363",
    "success_green": "#A0E7E5",
    "warning_yellow": "#FFD700",
    "info_orange": "#F97316",
    "select_highlight": "#2A456C"
}

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green") # Use the default theme, but we'll override colors manually

FONT = "Poppins"
F_TITLE = (FONT, 24, "bold")
F_SUB = (FONT, 14, "bold")
F_TXT = (FONT, 13)
F_SMALL = (FONT, 11)
F_BOLD = (FONT, 13, "bold")

STATUTS = ["Présent", "Absent", "Retard", "Justifié"]

# Database and utility functions (unchanged)
def _connect():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def get_all_classes():
    with _connect() as c:
        r = c.execute("SELECT id, nom FROM classe ORDER BY nom").fetchall()
        return [dict(x) for x in r]

def get_all_eleves(classe_id, search_term="", statut_filter=None, date=None):
    with _connect() as c:
        q = "SELECT e.id, e.nom, e.prenom, e.email_parent FROM eleves e WHERE e.classe_id=?"
        p = [classe_id]
        if search_term:
            pat = f"%{search_term}%"
            q += " AND (e.nom LIKE ? OR e.prenom LIKE ?)"
            p += [pat, pat]
        if statut_filter and statut_filter != "Tous" and date:
            q += " AND e.id IN (SELECT eleve_id FROM presence WHERE classe_id=? AND statut=? AND date=?)"
            p += [classe_id, statut_filter, date]
        q += " ORDER BY e.nom, e.prenom"
        return [dict(r) for r in c.execute(q, p).fetchall()]

def get_presence_for_date_and_class(classe_id, date):
    with _connect() as c:
        r = c.execute("""
            SELECT eleve_id, statut, commentaire, justificatif_path
            FROM presence
            WHERE classe_id=? AND date=?
        """, (classe_id, date)).fetchall()
        return {row["eleve_id"]: dict(row) for row in r}

def add_presence(eleve_id, classe_id, date, statut, commentaire, justificatif_path=None):
    with _connect() as c:
        c.execute("""
            INSERT INTO presence (eleve_id, classe_id, date, statut, commentaire, justificatif_path)
            VALUES (?,?,?,?,?,?)
        """, (eleve_id, classe_id, date, statut, commentaire, justificatif_path))
        c.commit()

def update_presence(eleve_id, classe_id, date, statut, commentaire, justificatif_path=None):
    with _connect() as c:
        c.execute("""
            UPDATE presence
            SET statut=?, commentaire=?, justificatif_path=?
            WHERE eleve_id=? AND classe_id=? AND date=?
        """, (statut, commentaire, justificatif_path, eleve_id, classe_id, date))
        c.commit()

def get_student_history(eleve_id):
    with _connect() as c:
        return c.execute("""
            SELECT p.date, p.statut, p.commentaire, p.justificatif_path, e.prenom, e.nom
            FROM presence p JOIN eleves e ON p.eleve_id=e.id
            WHERE p.eleve_id=? ORDER BY p.date DESC
        """, (eleve_id,)).fetchall()

def get_monthly_attendance_data(classe_id, year, month):
    with _connect() as c:
        return c.execute("""
            SELECT e.prenom, e.nom, p.statut, p.date, p.commentaire
            FROM presence p JOIN eleves e ON p.eleve_id=e.id
            WHERE p.classe_id=? AND strftime('%Y',p.date)=? AND strftime('%m',p.date)=?
            ORDER BY e.nom, e.prenom, p.date
        """, (classe_id, year, month)).fetchall()

def get_monthly_status_counts(classe_id, year, month):
    with _connect() as c:
        rows = c.execute("""
            SELECT statut, COUNT(*) c
            FROM presence
            WHERE classe_id=? AND strftime('%Y',date)=? AND strftime('%m',date)=?
            GROUP BY statut
        """, (classe_id, year, month)).fetchall()
        return {r["statut"]: r["c"] for r in rows}

def get_absence_threshold():
    with _connect() as c:
        r = c.execute("SELECT valeur FROM configuration WHERE cle='seuil_absence_injustifiee'").fetchone()
        return int(r["valeur"]) if r else 3

def get_unjustified_absences_count(eleve_id):
    with _connect() as c:
        r = c.execute("""
            SELECT COUNT(*) c
            FROM presence
            WHERE eleve_id=? AND statut='Absent' AND (justificatif_path IS NULL OR justificatif_path='')
        """, (eleve_id,)).fetchone()
        return r[0]

def send_absent_notification(parent_email, student_name, classe_name, date_str):
    print(f"[EMAIL] Notification d'absence envoyée à {parent_email} pour {student_name} en {classe_name} le {date_str}.")

# Main Application Class
class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("EduManager+ — Dashboard")
        self.geometry("1280x820")
        self.configure(fg_color=THEME["bg_main"])
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.icons = {}
        self._load_icons()
        self._build_sidebar()
        self.main_content = ctk.CTkFrame(self, fg_color=THEME["bg_main"])
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
        sidebar = ctk.CTkFrame(self, fg_color=THEME["header_bg"], corner_radius=0)
        sidebar.grid(row=0, column=0, sticky="nsew")
        sidebar.grid_rowconfigure(6, weight=1)
        
        logo_frame = ctk.CTkFrame(sidebar, fg_color="transparent")
        logo_frame.grid(row=0, column=0, sticky="ew", padx=20, pady=(20, 10))
        ctk.CTkLabel(logo_frame, text="EduManager+", font=F_TITLE, text_color=THEME["accent_blue"]).pack(side="left")
        
        def add_button(text, icon_key, row, command=None, is_active=False):
            btn = ctk.CTkButton(sidebar, text=text, image=self.icons.get(icon_key), compound="left",
                                 font=F_SUB,
                                 fg_color=THEME["select_highlight"] if is_active else "transparent",
                                 hover_color=THEME["select_highlight"],
                                 text_color=THEME["primary_text"] if is_active else THEME["secondary_text"],
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
        super().__init__(parent, fg_color=THEME["bg_main"])
        self.icons = icons
        self.ic = lambda k: self.icons.get(k)
        self._classes = get_all_classes()
        self._classe_name_to_id = {c["nom"]: c["id"] for c in self._classes}
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
            self.cb_class.set(self._classes[0]["nom"])
        self.ent_date.insert(0, datetime.now().strftime("%Y-%m-%d"))
        self._reload()

    def _build_main_layout(self):
        # Left Panel (Master)
        master_panel = ctk.CTkFrame(self, fg_color=THEME["card_bg"], corner_radius=12)
        master_panel.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        master_panel.grid_rowconfigure(3, weight=1)
        
        # Header for the master panel
        header_frame = ctk.CTkFrame(master_panel, fg_color="transparent")
        header_frame.pack(fill="x", padx=20, pady=(20, 10))
        ctk.CTkLabel(header_frame, text="Sélectionner une classe et une date", font=F_SUB, text_color=THEME["primary_text"]).pack(anchor="w")

        # Controls
        controls_frame = ctk.CTkFrame(master_panel, fg_color="transparent")
        controls_frame.pack(fill="x", padx=20, pady=(0, 10))
        controls_frame.grid_columnconfigure(0, weight=1)
        controls_frame.grid_columnconfigure(1, weight=1)

        self.cb_class = ctk.CTkComboBox(controls_frame, values=[c["nom"] for c in self._classes], command=lambda *_: self._reload(),
                                             fg_color=THEME["header_bg"], border_color=THEME["border_color"], text_color=THEME["primary_text"])
        self.cb_class.grid(row=0, column=0, sticky="ew", padx=(0, 5))
        
        date_frame = ctk.CTkFrame(controls_frame, fg_color=THEME["header_bg"], border_color=THEME["border_color"], border_width=1)
        date_frame.grid(row=0, column=1, sticky="ew", padx=(5, 0))
        date_frame.grid_columnconfigure(0, weight=1)
        self.ent_date = ctk.CTkEntry(date_frame, placeholder_text="AAAA-MM-JJ", border_width=0, fg_color="transparent", font=F_TXT)
        self.ent_date.grid(row=0, column=0, sticky="ew", padx=(8, 0))
        ctk.CTkButton(date_frame, text="", image=self.ic("calendriers"), width=30, fg_color="transparent",
                      hover_color=THEME["card_bg"], command=self._pick_date).grid(row=0, column=1, padx=4, pady=4)

        # Search and Filter
        search_filter_frame = ctk.CTkFrame(master_panel, fg_color="transparent")
        search_filter_frame.pack(fill="x", padx=20, pady=(0, 10))
        search_filter_frame.grid_columnconfigure(0, weight=1)
        search_box = ctk.CTkEntry(search_filter_frame, textvariable=self.search_var, placeholder_text="Rechercher un élève...",
                                     fg_color=THEME["header_bg"], border_color=THEME["border_color"])
        search_box.grid(row=0, column=0, sticky="ew", padx=(0, 5))
        search_box.bind("<Return>", lambda _e: self._reload())
        
        self.filter_cb = ctk.CTkComboBox(search_filter_frame, values=["Tous"]+STATUTS, variable=self.filter_var,
                                             fg_color=THEME["header_bg"], border_color=THEME["border_color"],
                                             command=lambda *_: self._reload())
        self.filter_cb.grid(row=0, column=1, sticky="ew", padx=(5, 0))
        
        self.list_wrap = ctk.CTkScrollableFrame(master_panel, fg_color=THEME["bg_main"], corner_radius=0)
        self.list_wrap.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        # Right Panel (Detail)
        self.detail_panel = ctk.CTkFrame(self, fg_color=THEME["card_bg"], corner_radius=12)
        self.detail_panel.grid(row=0, column=1, sticky="nsew")
        self._build_detail_panel()
        
    def _build_detail_panel(self):
        for w in self.detail_panel.winfo_children():
            w.destroy()
        
        self.detail_panel.grid_columnconfigure(0, weight=1)
        ctk.CTkLabel(self.detail_panel, text="Sélectionnez un élève pour voir les détails",
                      font=F_SUB, text_color=THEME["secondary_text"]).pack(pady=40, padx=20)
        
    def _render_detail_for(self, eleve_id):
        for w in self.detail_panel.winfo_children():
            w.destroy()
            
        self.detail_panel.grid_columnconfigure(0, weight=1)
        self.detail_panel.grid_rowconfigure(2, weight=1)
        
        e = next((x for x in self.eleves if x["id"] == eleve_id), None)
        if not e:
            self._build_detail_panel()
            return
        
        self.current_student_id = eleve_id
        p = self.pres_map.get(eleve_id, {})
        statut = p.get("statut") or "Présent"
        commentaire = p.get("commentaire", "")
        justificatif = p.get("justificatif_path", "")
        
        header_frame = ctk.CTkFrame(self.detail_panel, fg_color="transparent")
        header_frame.pack(fill="x", padx=20, pady=(20, 10))
        
        ctk.CTkLabel(header_frame, text=f"{e['prenom']} {e['nom']}", font=F_TITLE, text_color=THEME["primary_text"]).pack(side="left")
        ctk.CTkButton(header_frame, text="Historique", image=self.ic("documents"),
                      fg_color=THEME["accent_blue"], text_color=THEME["bg_main"], hover_color=THEME["accent_blue"],
                      command=lambda: self._history(eleve_id)).pack(side="right")
        
        content_frame = ctk.CTkFrame(self.detail_panel, fg_color="transparent")
        content_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        ctk.CTkLabel(content_frame, text="Statut du jour", font=F_TXT, text_color=THEME["secondary_text"]).pack(anchor="w", pady=(0, 5))
        v_statut = ctk.StringVar(value=statut)
        seg = ctk.CTkSegmentedButton(content_frame, values=STATUTS, variable=v_statut,
                                         selected_color=THEME["accent_blue"], selected_hover_color=THEME["accent_blue"],
                                         unselected_color=THEME["header_bg"], unselected_hover_color=THEME["card_bg"],
                                         font=F_TXT,
                                         text_color=THEME["bg_main"], text_color_disabled=THEME["secondary_text"])
        seg.pack(fill="x", pady=(0, 15))
        
        ctk.CTkLabel(content_frame, text="Commentaire", font=F_TXT, text_color=THEME["secondary_text"]).pack(anchor="w", pady=(0, 5))
        txt = ctk.CTkTextbox(content_frame, height=120, fg_color=THEME["header_bg"], border_color=THEME["border_color"], font=F_TXT, text_color=THEME["primary_text"])
        txt.pack(fill="x", pady=(0, 15))
        if commentaire:
            txt.insert("1.0", commentaire)
            
        ctk.CTkLabel(content_frame, text="Justificatif", font=F_TXT, text_color=THEME["secondary_text"]).pack(anchor="w", pady=(0, 5))
        wrap = ctk.CTkFrame(content_frame, fg_color=THEME["header_bg"], border_color=THEME["border_color"], border_width=1, corner_radius=6)
        wrap.pack(fill="x", pady=(0, 20))
        
        path_v = ctk.StringVar(value=justificatif)
        ent = ctk.CTkEntry(wrap, textvariable=path_v, placeholder_text="Chemin vers le fichier (PDF/JPG/PNG)…",
                             border_width=0, fg_color="transparent", font=F_TXT, text_color=THEME["primary_text"])
        ent.pack(side="left", fill="x", expand=True, padx=8)
        
        ctk.CTkButton(wrap, text="", image=self.ic("documents"), width=40,
                      fg_color=THEME["card_bg"], hover_color=THEME["bg_main"],
                      command=lambda: self._pick_file(path_v)).pack(side="left", padx=4, pady=4)
        
        btns_frame = ctk.CTkFrame(self.detail_panel, fg_color="transparent")
        btns_frame.pack(pady=(0, 20))
        
        def apply_one():
            self._apply_one(eleve_id, v_statut.get(), txt.get("1.0", "end-1c").strip(), path_v.get().strip())
        
        ctk.CTkButton(btns_frame, text="Appliquer", image=self.ic("taches"), font=F_BOLD,
                      fg_color=THEME["success_green"], text_color=THEME["bg_main"], hover_color="#8cd5d3", command=apply_one).pack(side="left", padx=5)
        
        ctk.CTkButton(btns_frame, text="Annuler", image=self.ic("logout"), font=F_BOLD,
                      fg_color=THEME["error_red"], text_color=THEME["bg_main"], hover_color="#e55252", command=lambda: self._render_detail_for(eleve_id)).pack(side="left", padx=5)

    def _reload(self):
        classe = self.cb_class.get()
        if not classe:
            return
            
        self.selected_classe_id = self._classe_name_to_id.get(classe)
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
            eid = e["id"]
            p = self.pres_map.get(eid, {})
            statut = p.get("statut", "Présent")
            counts[statut] = counts.get(statut, 0) + 1
            
            item_bg = THEME["select_highlight"] if eid == self.current_student_id else THEME["card_bg"]
            item_hover = THEME["select_highlight"]
            
            item = ctk.CTkFrame(self.list_wrap, fg_color=item_bg, corner_radius=8, cursor="hand2")
            item.pack(fill="x", padx=5, pady=4)
            item.bind("<Button-1>", lambda event, sid=eid: self._render_detail_for(sid))
            
            ctk.CTkLabel(item, text="", image=self.ic("person")).pack(side="left", padx=(10, 5), pady=8)
            
            name = ctk.CTkLabel(item, text=f"{e['prenom']} {e['nom']}", font=F_TXT, text_color=THEME["primary_text"])
            name.pack(side="left", padx=(0, 10))
            
            color_map = {
                "Présent": THEME["success_green"],
                "Absent": THEME["error_red"],
                "Retard": THEME["warning_yellow"],
                "Justifié": THEME["info_orange"]
            }
            color = color_map.get(statut, THEME["secondary_text"])
            
            tag = ctk.CTkLabel(item, text=statut, text_color=THEME["bg_main"], fg_color=color, corner_radius=999, width=70, font=F_SMALL)
            tag.pack(side="right", padx=10)
            
            abs_c = get_unjustified_absences_count(eid)
            if abs_c >= seuil:
                ctk.CTkLabel(item, text=f"({abs_c} abs. injustifiées)", text_color=THEME["error_red"], font=F_SMALL).pack(side="right", padx=5)

        self.master_stats = ctk.CTkFrame(self.list_wrap, fg_color="transparent")
        self.master_stats.pack(fill="x", pady=10)
        self.master_stats.grid_columnconfigure((0, 1, 2, 3), weight=1)

        def add_chip(label, count, color, col):
            chip_frame = ctk.CTkFrame(self.master_stats, fg_color=THEME["header_bg"], corner_radius=8)
            chip_frame.grid(row=0, column=col, sticky="ew", padx=5)
            ctk.CTkLabel(chip_frame, text=label, font=F_SMALL, text_color=color).pack(pady=(4, 0))
            ctk.CTkLabel(chip_frame, text=str(count), font=F_BOLD, text_color=THEME["primary_text"]).pack(pady=(0, 4))
        
        add_chip("Présents", counts.get("Présent", 0), THEME["success_green"], 0)
        add_chip("Absents", counts.get("Absent", 0), THEME["error_red"], 1)
        add_chip("Retards", counts.get("Retard", 0), THEME["warning_yellow"], 2)
        add_chip("Justifiés", counts.get("Justifié", 0), THEME["info_orange"], 3)
        
        if self.current_student_id not in [e["id"] for e in self.eleves]:
            self._build_detail_panel()
            self.current_student_id = None

    def _pick_date(self):
        top = ctk.CTkToplevel(self)
        top.title("Choisir une date")
        top.configure(fg_color=THEME["bg_main"])
        top.grab_set()
        
        cal = Calendar(top, selectmode="day",
                       background=THEME["card_bg"],
                       foreground=THEME["primary_text"],
                       selectbackground=THEME["accent_blue"],
                       headersbackground=THEME["header_bg"],
                       normalbackground=THEME["bg_main"],
                       weekendbackground=THEME["bg_main"],
                       bordercolor=THEME["border_color"])
        cal.pack(padx=10, pady=10)
        
        def ok():
            self.ent_date.delete(0, "end")
            self.ent_date.insert(0, cal.selection_get().strftime("%Y-%m-%d"))
            top.destroy()
            self._reload()
            
        ctk.CTkButton(top, text="OK", fg_color=THEME["accent_blue"], text_color=THEME["bg_main"], hover_color=THEME["accent_blue"], command=ok).pack(pady=8)

    def _pick_file(self, var):
        p = filedialog.askopenfilename(title="Sélectionner un justificatif",
                                             filetypes=[("PDF", "*.pdf"), ("Images", "*.jpg;*.jpeg;*.png"), ("Tous", "*.*")])
        if p:
            var.set(p)

    def _apply_one(self, eleve_id, statut, commentaire, path):
        if not self.selected_classe_id:
            messagebox.showwarning("Attention", "Sélectionnez une classe.")
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
            messagebox.showwarning("Attention", "Sélectionnez une classe.")
            return
            
        classe = self.cb_class.get()
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
        pdf.cell(200, 10, txt=f"Rapport de présence - {classe} ({month_name} {y})", ln=True, align='C')
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
                                             initialfile=f"Rapport_Presences_{classe}_{y}_{m}.pdf")
        if path:
            pdf.output(path)
            messagebox.showinfo("PDF", f"Rapport sauvegardé : {path}")

    def _history(self, eid):
        rows = get_student_history(eid)
        if not rows:
            messagebox.showinfo("Historique", "Aucun historique pour cet élève.")
            return
            
        nom = f"{rows[0]['prenom']} {rows[0]['nom']}"
        win = ctk.CTkToplevel(self)
        win.title(f"Historique - {nom}")
        win.geometry("760x560")
        win.configure(fg_color=THEME["bg_main"])
        win.grab_set()
        
        ctk.CTkLabel(win, text=f"Historique de {nom}", font=F_TITLE, text_color=THEME["primary_text"]).pack(pady=10)
        fr = ctk.CTkScrollableFrame(win, fg_color=THEME["card_bg"])
        fr.pack(fill="both", expand=True, padx=12, pady=8)
        
        for r in rows:
            line = ctk.CTkFrame(fr, fg_color=THEME["header_bg"], corner_radius=8)
            line.pack(fill="x", padx=6, pady=4)
            ctk.CTkLabel(line, text=r["date"], width=110, font=F_TXT, text_color=THEME["secondary_text"]).pack(side="left", padx=10)
            ctk.CTkLabel(line, text=r["statut"], width=110, font=F_BOLD, text_color=THEME["accent_blue"]).pack(side="left")
            ctk.CTkLabel(line, text=r["commentaire"] or "-", font=F_TXT, text_color=THEME["primary_text"]).pack(side="left", padx=10)
            
            if r["justificatif_path"]:
                ctk.CTkButton(line, text="Ouvrir", width=70,
                              fg_color=THEME["accent_blue"], text_color=THEME["bg_main"],
                              command=lambda p=r["justificatif_path"]: os.startfile(p)).pack(side="right", padx=8)

if __name__ == "__main__":
    app = App()
    app.mainloop()