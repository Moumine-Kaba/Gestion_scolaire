import customtkinter as ctk
from tkinter import ttk, messagebox, filedialog
from PIL import Image, ImageTk
import os, datetime, re, sqlite3
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# ============ Thème et Constantes (Amélioré) ============
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

try:
    RESAMPLE_LANCZOS = Image.Resampling.LANCZOS
except AttributeError:
    RESAMPLE_LANCZOS = Image.LANCZOS

THEME = {
    "bg_main": "#0A192F",
    "header_bg": "#172A45",
    "card_bg": "#0B2039",
    "border_color": "#334155",
    "accent_blue": "#64FFDA",
    "primary_text": "#CCD6F6",
    "secondary_text": "#8892B0",
    "error_red": "#FF6363",
    "success_green": "#22c55e",
    "warning_yellow": "#f59e0b",
    "info_orange": "#F97316",
    "select_highlight": "#2A456C",
    "hover_light": "#1C3558"
}

FONT_FAMILY = "Segoe UI"
FONT_SIZE_TITLE = 28
FONT_SIZE_HEADER = 18
FONT_SIZE_TEXT = 14

# --- Chemin DB et icônes ---
DB_PATH = r"C:\Users\Lenovo\Desktop\EduManager+\database\edumanager.db"
ICON_PATH_BASE = r"C:\Users\Lenovo\Desktop\EduManager+\assets\icons"

ICON_MAP = {
    "eleves": "book.png",
    "filles": "eleve.png",
    "garcons": "person.png",
    "classes": "cover.png",
    "profs": "profs.png",
    "ajouter": "add.png",
    "edit": "edit.png",
    "delete": "delete.png",
    "detail": "detail.png",
    "transferer": "transfer.png",
    "refresh": "refresh.png",
    "search": "search.png",
    "chevron_right": "chevron_right.png",
    "home": "home.png",
    "person": "person.png",
    "group": "group.png",
    "door": "door.png",
    "book": "book.png",
    "notes": "notes.png",
    "check": "check.png",
    "file": "file.png",
    "bell": "bell.png",
    "calendar": "calendar.png",
    "money": "money.png",
    "logout": "logout.png",
    "close": "close.png",
    "add": "add.png", # Alias explicite
    "pdf": "file.png", # Alias
    "stats": "notes.png", # Alias
    "transfer": "transfer.png", # Alias
}

def _icon_candidates(name: str):
    yield name
    if name in ICON_MAP:
        yield ICON_MAP.get(name).replace(".png", "") # Pour les doublons éventuels
    for k, lst in {
        "add": ["ajouter", "check", "upload"],
        "pdf": ["file", "notes"],
        "calendar": ["calendar"],
        "stats": ["notes", "book"],
        "transfer": ["transferer"],
    }.items():
        if name == k:
            for alt in lst:
                yield alt

# --- Regex de validation ---
EMAIL_RE = re.compile(r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$")
PHONE_RE = re.compile(r"^\+?\d{7,15}$")
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
NAME_RE = re.compile(r"^[A-Za-zÀ-ÖØ-öø-ÿ' -]{2,}$")

def is_email(val): return bool(EMAIL_RE.match(val))
def is_phone(val): return bool(PHONE_RE.match(val))
def is_date(val):
    if not DATE_RE.match(val): return False
    try:
        datetime.datetime.strptime(val, "%Y-%m-%d"); return True
    except Exception:
        return False
def is_name(val): return bool(NAME_RE.match(val))

# --- DB helpers ---
def get_db_connection():
    try:
        conn = sqlite3.connect(DB_PATH)
        return conn
    except sqlite3.Error as e:
        messagebox.showerror("Erreur de connexion", f"Impossible de se connecter à la base de données: {e}")
        return None

def get_all_classes():
    conn = get_db_connection()
    if conn:
        cur = conn.cursor()
        cur.execute("""
            SELECT id, nom FROM classe ORDER BY
            CASE
                WHEN nom LIKE '1er%' THEN 1
                WHEN nom LIKE '2em%' THEN 2
                WHEN nom LIKE '3em%' THEN 3
                WHEN nom LIKE '4em%' THEN 4
                WHEN nom LIKE '5em%' THEN 5
                WHEN nom LIKE '6em%' THEN 6
                WHEN nom LIKE '7em%' THEN 7
                WHEN nom LIKE '8em%' THEN 8
                WHEN nom LIKE '9em%' THEN 9
                WHEN nom LIKE '10em%' THEN 10
                WHEN nom LIKE '11em%' THEN 11
                WHEN nom LIKE '12em%' THEN 12
                ELSE 99
            END,
            nom
        """)
        rows = cur.fetchall()
        conn.close()
        return rows
    return []

def get_stats_eleves(classe_id=None):
    conn = get_db_connection()
    if conn:
        cur = conn.cursor()
        stats = {}
        if classe_id is None:
            cur.execute("SELECT COUNT(*) FROM eleves"); stats["total"] = cur.fetchone()[0]
            cur.execute("SELECT COUNT(*) FROM eleves WHERE sexe LIKE 'F%'"); stats["filles"] = cur.fetchone()[0]
            cur.execute("SELECT COUNT(*) FROM eleves WHERE sexe LIKE 'M%'"); stats["garcons"] = cur.fetchone()[0]
            cur.execute("SELECT COUNT(*) FROM classe"); stats["classes"] = cur.fetchone()[0]
            cur.execute("SELECT COUNT(DISTINCT professeur_principal_id) FROM classe WHERE professeur_principal_id IS NOT NULL")
            stats["profs"] = cur.fetchone()[0]
        else:
            cur.execute("SELECT COUNT(*) FROM eleves WHERE classe_id=?", (classe_id,)); stats["total"] = cur.fetchone()[0]
            cur.execute("SELECT COUNT(*) FROM eleves WHERE sexe LIKE 'F%' AND classe_id=?", (classe_id,)); stats["filles"] = cur.fetchone()[0]
            cur.execute("SELECT COUNT(*) FROM eleves WHERE sexe LIKE 'M%' AND classe_id=?", (classe_id,)); stats["garcons"] = cur.fetchone()[0]
            stats["classes"] = 1
            cur.execute("SELECT professeur_principal_id FROM classe WHERE id=?", (classe_id,))
            prof = cur.fetchone(); stats["profs"] = 1 if prof and prof[0] else 0
        conn.close()
        return stats
    return {"total": 0, "filles": 0, "garcons": 0, "classes": 0, "profs": 0}

def get_eleves_by_classe(classe_id=None):
    conn = get_db_connection()
    if conn:
        cur = conn.cursor()
        if classe_id is None:
            cur.execute("SELECT c.nom, COUNT(e.id) FROM classe c LEFT JOIN eleves e ON e.classe_id = c.id GROUP BY c.nom ORDER BY c.nom")
        else:
            cur.execute("SELECT c.nom, COUNT(e.id) FROM classe c LEFT JOIN eleves e ON e.classe_id = c.id WHERE c.id=? GROUP BY c.nom", (classe_id,))
        rows = cur.fetchall()
        conn.close()
        return rows
    return []

def get_eleves_list(classe_id=None):
    conn = get_db_connection()
    if conn:
        cur = conn.cursor()
        if classe_id is None:
            cur.execute("SELECT id, nom, prenom, sexe, date_naissance, statut FROM eleves ORDER BY nom")
        else:
            cur.execute("SELECT id, nom, prenom, sexe, date_naissance, statut FROM eleves WHERE classe_id=? ORDER BY nom", (classe_id,))
        rows = cur.fetchall()
        conn.close()
        return rows
    return []

def get_eleve_complet(eleve_id):
    conn = get_db_connection()
    if conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM eleves WHERE id=?", (eleve_id,))
        data = cur.fetchone()
        conn.close()
        return data
    return None

def square_photo(path, size=(160, 160)):
    try:
        if path and os.path.exists(path):
            img = Image.open(path).resize(size, RESAMPLE_LANCZOS)
        else:
            img = Image.new("RGB", size, THEME["header_bg"])
    except Exception:
        img = Image.new("RGB", size, THEME["header_bg"])
    return ctk.CTkImage(light_image=img, dark_image=img, size=size)

# ============ Classe principale UI ============
class DashboardEleves(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color=THEME["bg_main"])
        self.selected_classe = None
        self.selected_eleve = None

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=0, minsize=250)

        main_content_frame = ctk.CTkFrame(self, fg_color="transparent")
        main_content_frame.grid(row=0, column=0, sticky="nsew", padx=(10, 5), pady=10)
        main_content_frame.grid_rowconfigure(4, weight=1)
        main_content_frame.grid_columnconfigure(0, weight=1)

        self._create_header(main_content_frame)
        self._create_stats_cards(main_content_frame)
        self._create_graph_section(main_content_frame)
        self._create_table_actions_bar(main_content_frame)
        self._create_table_section(main_content_frame)
        self._create_classes_sidebar()
        self.update_classes_sidebar() # Initial call
        self.refresh()

    # ---------- Header
    def _create_header(self, parent_frame):
        header_frame = ctk.CTkFrame(parent_frame, fg_color="transparent")
        header_frame.grid(row=0, column=0, sticky="ew", pady=(0, 15))
        header_frame.grid_columnconfigure(0, weight=1)
        header_frame.grid_columnconfigure(1, weight=1)

        title_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        title_frame.grid(row=0, column=0, sticky="w")
        ctk.CTkLabel(
            title_frame, text="Dashboard Élèves", font=ctk.CTkFont(FONT_FAMILY, FONT_SIZE_TITLE, "bold"),
            text_color=THEME["accent_blue"]
        ).pack(anchor="w")
        ctk.CTkLabel(
            title_frame, text="Gérez la liste, les informations et les statistiques de vos élèves.",
            font=ctk.CTkFont(FONT_FAMILY, 14), text_color=THEME["secondary_text"]
        ).pack(anchor="w", pady=(2, 5))

        search_refresh_frame = ctk.CTkFrame(header_frame, fg_color=THEME["card_bg"], height=45, corner_radius=10)
        search_refresh_frame.grid(row=0, column=1, sticky="e")
        search_refresh_frame.pack_propagate(False)
        search_refresh_frame.grid_columnconfigure(1, weight=1)
        
        search_icon = self._load_icon("search", 20, 20)
        ctk.CTkLabel(search_refresh_frame, image=search_icon, text="", width=25).grid(row=0, column=0, padx=(10, 0))

        self.search_var = ctk.StringVar()
        self.search_entry = ctk.CTkEntry(
            search_refresh_frame, textvariable=self.search_var,
            font=ctk.CTkFont(FONT_FAMILY, 14), height=45,
            fg_color=THEME["card_bg"], border_width=0,
            placeholder_text="Rechercher un élève...",
            placeholder_text_color=THEME["secondary_text"],
            text_color=THEME["primary_text"],
            corner_radius=0
        )
        self.search_entry.grid(row=0, column=1, sticky="ew")
        self.search_entry.bind("<KeyRelease>", self.on_search_key_release)

        clear_icon = self._load_icon("close", 20, 20)
        self.clear_btn = ctk.CTkButton(
            search_refresh_frame, text="", image=clear_icon,
            command=self.clear_search, width=45, height=45,
            fg_color=THEME["card_bg"], hover_color=THEME["hover_light"],
            corner_radius=8
        )
        self.clear_btn.grid(row=0, column=2, sticky="e")
        self.clear_btn.grid_remove()

        refresh_icon = self._load_icon("refresh", 20, 20)
        ctk.CTkButton(
            search_refresh_frame, text="", image=refresh_icon,
            command=self.refresh, width=45, height=45,
            fg_color=THEME["card_bg"], hover_color=THEME["hover_light"],
            corner_radius=8
        ).grid(row=0, column=3, sticky="e", padx=(0, 5))

    def on_search_key_release(self, event):
        self.apply_search_filter()
        if self.search_var.get():
            self.clear_btn.grid()
        else:
            self.clear_btn.grid_remove()
    
    def clear_search(self):
        self.search_var.set("")
        self.apply_search_filter()
        self.clear_btn.grid_remove()
        self.search_entry.focus_set()

    # ---------- Stat cards
    def _create_stats_cards(self, parent_frame):
        cards_container = ctk.CTkFrame(parent_frame, fg_color="transparent")
        cards_container.grid(row=1, column=0, sticky="ew", pady=(0, 15))
        cards_container.grid_columnconfigure((0, 1, 2, 3), weight=1, uniform="group1")

        stats_info = [
            ("Total Élèves", 0, "eleves", THEME["accent_blue"]),
            ("Filles", 0, "filles", THEME["success_green"]),
            ("Garçons", 0, "garcons", THEME["warning_yellow"]),
            ("Classes", 0, "classes", THEME["error_red"]),
        ]

        self.stats_labels = []
        for i, (title, value, icon_name, accent_color) in enumerate(stats_info):
            card = ctk.CTkFrame(cards_container, fg_color=THEME["card_bg"], corner_radius=16)
            card.grid(row=0, column=i, padx=(0, 10) if i < len(stats_info) - 1 else 0, sticky="nsew")

            icon_frame = ctk.CTkFrame(card, fg_color="transparent")
            icon_frame.pack(fill="x", padx=10, pady=(10, 5))

            icon = self._load_icon(icon_name, 28, 28)
            ctk.CTkLabel(icon_frame, image=icon, text="", width=30).pack(side="left")

            ctk.CTkLabel(icon_frame, text=title, font=ctk.CTkFont(FONT_FAMILY, 13, "bold"),
                         text_color=THEME["secondary_text"]).pack(side="left", padx=(5, 0))

            lbl = ctk.CTkLabel(card, text=value, font=ctk.CTkFont(FONT_FAMILY, 34, "bold"), text_color=accent_color)
            lbl.pack(pady=(0, 10), anchor="w", padx=15)
            self.stats_labels.append(lbl)

    # ---------- Graph
    def _create_graph_section(self, parent_frame):
        self.graph_box = ctk.CTkFrame(parent_frame, fg_color=THEME["card_bg"], corner_radius=16, border_width=1, border_color=THEME["border_color"])
        self.graph_box.grid(row=2, column=0, sticky="ew", pady=(0, 15))

        graph_header = ctk.CTkFrame(self.graph_box, fg_color="transparent")
        graph_header.pack(fill="x", pady=(10, 5))
        ctk.CTkLabel(graph_header, text="Répartition des élèves par classe",
                     font=ctk.CTkFont(FONT_FAMILY, FONT_SIZE_HEADER, "bold"),
                     text_color=THEME["primary_text"]).pack(side="left", padx=15)

    def update_graph(self, data):
        for widget in self.graph_box.winfo_children()[1:]:
            widget.destroy()

        cls_names = [x[0] for x in data]
        counts = [x[1] for x in data]

        if not cls_names or all(c == 0 for c in counts):
            label = ctk.CTkLabel(self.graph_box, text="📊\n\nAucune donnée à afficher",
                                 font=ctk.CTkFont(FONT_FAMILY, 16, "bold"),
                                 text_color=THEME["secondary_text"])
            label.pack(pady=40)
            return

        fig = plt.Figure(figsize=(6.6, 3.5), dpi=100)
        ax = fig.add_subplot(111)
        x_pos = range(len(cls_names))
        colors = plt.cm.viridis(range(len(cls_names)))
        ax.bar(x_pos, counts, color=colors, width=0.6)

        ax.set_xticks(list(x_pos))
        ax.set_xticklabels(cls_names, fontsize=10, rotation=45, ha='right', color=THEME["primary_text"])
        ax.set_ylabel("Nombre d'élèves", fontsize=12, color=THEME["primary_text"])
        ax.tick_params(axis='x', colors=THEME["primary_text"])
        ax.tick_params(axis='y', colors=THEME["primary_text"])

        for i, v in enumerate(counts):
            if v > 0:
                ax.text(i, v + 0.5, str(v), color=THEME["primary_text"], fontsize=10, ha='center', fontweight='bold')

        fig.tight_layout()
        fig.patch.set_facecolor(THEME["card_bg"])
        ax.set_facecolor(THEME["card_bg"])
        ax.spines['bottom'].set_color(THEME["border_color"])
        ax.spines['left'].set_color(THEME["border_color"])
        ax.spines['right'].set_color(THEME["card_bg"])
        ax.spines['top'].set_color(THEME["card_bg"])

        canvas_fig = FigureCanvasTkAgg(fig, master=self.graph_box)
        canvas_fig.draw()
        canvas_fig.get_tk_widget().pack(fill="x", pady=6)

    # ---------- Actions bar
    def _create_table_actions_bar(self, parent_frame):
        actions_bar = ctk.CTkFrame(parent_frame, fg_color="transparent")
        actions_bar.grid(row=3, column=0, sticky="ew", pady=(0, 5))

        btn_add = self._btn_crud(actions_bar, "Ajouter", THEME["success_green"], self.ajouter_eleve, "ajouter")
        btn_add.pack(side="left", padx=(0, 5), expand=True, fill="x")
        self._btn_crud(actions_bar, "Modifier", THEME["info_orange"], self.modifier_eleve, "edit").pack(side="left", padx=5, expand=True, fill="x")
        self._btn_crud(actions_bar, "Supprimer", THEME["error_red"], self.supprimer_eleve, "delete").pack(side="left", padx=5, expand=True, fill="x")
        self._btn_crud(actions_bar, "Détails", THEME["accent_blue"], self.details_eleve, "detail").pack(side="left", padx=5, expand=True, fill="x")
        self._btn_crud(actions_bar, "Transférer", THEME["warning_yellow"], self.ouvrir_transfert, "transferer").pack(side="left", padx=5, expand=True, fill="x")

    # ---------- Table
    def _create_table_section(self, parent_frame):
        table_container = ctk.CTkFrame(parent_frame, fg_color=THEME["card_bg"], corner_radius=16)
        table_container.grid(row=4, column=0, sticky="nsew")
        table_container.grid_rowconfigure(0, weight=1)
        table_container.grid_columnconfigure(0, weight=1)

        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview",
                        background=THEME["card_bg"], fieldbackground=THEME["card_bg"], foreground=THEME["primary_text"],
                        rowheight=45, font=(FONT_FAMILY, 12), borderwidth=0, relief="flat")
        style.configure("Treeview.Heading",
                        background=THEME["header_bg"], foreground=THEME["accent_blue"],
                        font=(FONT_FAMILY, 14, "bold"), relief="flat", borderwidth=0)
        style.map("Treeview", background=[('selected', THEME["hover_light"])])

        columns = ("id", "nom", "prenom", "sexe", "date_naissance", "statut")
        self.table = ttk.Treeview(table_container, columns=columns, show="headings", selectmode="browse")
        for col, label in [
            ("id", "ID"),
            ("nom", "Nom"),
            ("prenom", "Prénom"),
            ("sexe", "Sexe"),
            ("date_naissance", "Date de naissance"),
            ("statut", "Statut")
        ]:
            self.table.heading(col, text=label)
            self.table.column(col, anchor="center", minwidth=80, width=150 if col in ("nom", "prenom") else 120)

        table_scroll = ctk.CTkScrollbar(
            table_container, orientation="vertical", command=self.table.yview,
            fg_color=THEME["header_bg"], button_color=THEME["accent_blue"], button_hover_color=THEME["accent_blue"]
        )
        table_scroll.grid(row=0, column=1, sticky="ns", padx=(0, 2), pady=(10, 10))
        self.table.configure(yscrollcommand=table_scroll.set)
        self.table.grid(row=0, column=0, sticky="nsew", pady=10, padx=(10, 0))

        self.table.bind("<<TreeviewSelect>>", self.on_select_eleve)
        self.table.tag_configure('oddrow', background=THEME["card_bg"])
        self.table.tag_configure('evenrow', background=THEME["header_bg"])
        self.table_data = [] # pour le filtrage

    # ---------- Sidebar classes
    def _create_classes_sidebar(self):
        sidebar_frame = ctk.CTkFrame(self, fg_color=THEME["header_bg"], width=250, corner_radius=16)
        sidebar_frame.grid(row=0, column=1, sticky="nsew", padx=(5, 10), pady=10)
        sidebar_frame.grid_propagate(False)

        ctk.CTkLabel(sidebar_frame, text="Classes", font=ctk.CTkFont(FONT_FAMILY, 18, "bold"),
                     text_color=THEME["accent_blue"]).pack(pady=(15, 8))

        self.classe_btns_frame = ctk.CTkScrollableFrame(sidebar_frame, fg_color="transparent")
        self.classe_btns_frame.pack(fill="both", expand=True, padx=10)
        self.classe_btns = []

    def update_classes_sidebar(self):
        for w in self.classe_btns_frame.winfo_children():
            w.destroy()
        self.classe_btns = []

        btn_tous = ctk.CTkButton(
            self.classe_btns_frame, text="Tous les élèves", font=ctk.CTkFont(FONT_FAMILY, 14, "bold"),
            fg_color=THEME["warning_yellow"], text_color=THEME["bg_main"],
            hover_color=THEME["hover_light"],
            command=lambda: self.update_dashboard_for_classe(None)
        )
        btn_tous.pack(fill="x", pady=(5, 2))
        self.classe_btns.append((btn_tous, None))

        classes = get_all_classes()
        if not classes:
            ctk.CTkLabel(self.classe_btns_frame, text="Aucune classe trouvée.", text_color=THEME["secondary_text"]).pack(pady=10)
        else:
            for cid, nom in classes:
                btn = ctk.CTkButton(
                    self.classe_btns_frame, text=nom, font=ctk.CTkFont(FONT_FAMILY, 12, "bold"),
                    fg_color=THEME["card_bg"], text_color=THEME["primary_text"], hover_color=THEME["hover_light"],
                    command=lambda c=cid: self.update_dashboard_for_classe(c)
                )
                btn.pack(fill="x", pady=2)
                self.classe_btns.append((btn, cid))
        self.update_btn_states(self.selected_classe)

    def update_btn_states(self, classe_id):
        for btn, cid in self.classe_btns:
            if classe_id == cid:
                btn.configure(fg_color=THEME["accent_blue"], text_color=THEME["bg_main"], hover_color=THEME["accent_blue"])
            elif cid is None and classe_id is None:
                btn.configure(fg_color=THEME["warning_yellow"], text_color=THEME["bg_main"], hover_color=THEME["warning_yellow"])
            else:
                btn.configure(fg_color=THEME["card_bg"], text_color=THEME["primary_text"], hover_color=THEME["hover_light"])

    # ---------- Icônes
    def _load_icon(self, name, w, h):
        for cand in _icon_candidates(name):
            file = ICON_MAP.get(cand)
            if not file: continue
            icon_path = os.path.join(ICON_PATH_BASE, file)
            if os.path.exists(icon_path):
                try:
                    img = Image.open(icon_path).resize((w, h), RESAMPLE_LANCZOS)
                    return ctk.CTkImage(light_image=img, dark_image=img, size=(w, h))
                except Exception as e:
                    print(f"Error opening icon {cand}: {e}")
        img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
        return ctk.CTkImage(light_image=img, dark_image=img, size=(w, h))

    def _btn_crud(self, parent_frame, label, color, cmd, icon_name):
        icon = self._load_icon(icon_name, 20, 20)
        btn = ctk.CTkButton(
            parent_frame, text=f" {label}", font=ctk.CTkFont(FONT_FAMILY, 13, "bold"),
            text_color="white", fg_color=color,
            hover_color=THEME["hover_light"] if color != THEME["accent_blue"] else THEME["accent_blue"],
            image=icon, compound="left", command=cmd,
            corner_radius=10, height=35
        )
        return btn

    # ---------- Actions
    def ouvrir_transfert(self):
        if not self.selected_eleve:
            messagebox.showwarning("Transfert", "Sélectionnez d'abord un élève.")
            return
        messagebox.showinfo("Transfert", "Fonctionnalité de transfert à implémenter.")

    def update_dashboard_for_classe(self, classe_id):
        stats = get_stats_eleves(classe_id)
        data = get_eleves_by_classe(classe_id)
        for i, val in enumerate([stats["total"], stats["filles"], stats["garcons"], stats["classes"]]):
            self.stats_labels[i].configure(text=val)
        self.update_graph(data)
        self.table_data = get_eleves_list(classe_id)
        self.update_table(self.table_data)
        self.selected_classe = classe_id
        self.selected_eleve = None
        self.clear_search()
        self.update_btn_states(classe_id)

    def update_table(self, eleves):
        for row in self.table.get_children():
            self.table.delete(row)
        for i, e in enumerate(eleves):
            tag = 'evenrow' if i % 2 == 0 else 'oddrow'
            self.table.insert("", "end", values=e, tags=(tag,))

    def refresh(self):
        self.update_dashboard_for_classe(self.selected_classe)
        self.clear_search()
        self.selected_eleve = None

    def on_select_eleve(self, event):
        selected = self.table.selection()
        if selected:
            self.selected_eleve = self.table.item(selected[0])["values"][0]
        else:
            self.selected_eleve = None

    def ajouter_eleve(self):
        self.formulaire_eleve(mode="Ajouter")

    def modifier_eleve(self):
        if not self.selected_eleve:
            messagebox.showwarning("Modifier", "Sélectionnez d'abord un élève à modifier.")
            return
        eleve = get_eleve_complet(self.selected_eleve)
        if not eleve:
            messagebox.showerror("Erreur", "Élève introuvable.")
            return
        self.formulaire_eleve(mode="Modifier", eleve=eleve)

    def supprimer_eleve(self):
        if not self.selected_eleve:
            messagebox.showwarning("Supprimer", "Sélectionnez d'abord un élève à supprimer.")
            return
        if messagebox.askyesno("Confirmation", f"Voulez-vous vraiment supprimer l'élève ID {self.selected_eleve} ?"):
            conn = get_db_connection()
            if conn:
                try:
                    cur = conn.cursor()
                    cur.execute("DELETE FROM eleves WHERE id=?", (self.selected_eleve,))
                    conn.commit()
                    messagebox.showinfo("Succès", "Élève supprimé avec succès.")
                    self.refresh()
                except sqlite3.Error as e:
                    messagebox.showerror("Erreur de base de données", f"Une erreur est survenue : {e}")
                finally:
                    conn.close()

    def details_eleve(self):
        if not self.selected_eleve:
            messagebox.showwarning("Détails", "Sélectionnez d'abord un élève à détailler.")
            return
        eleve = get_eleve_complet(self.selected_eleve)
        if not eleve:
            messagebox.showerror("Erreur", "Élève introuvable.")
            return
        self.formulaire_eleve(mode="Détails", eleve=eleve)

    def apply_search_filter(self):
        term = self.search_var.get().strip().lower()
        if not term:
            self.update_table(self.table_data)
            return
        filtered = [r for r in self.table_data if any(term in str(r[i]).lower() for i in [0, 1, 2, 3, 5])]
        self.update_table(filtered)

    # ---------- Formulaire élève
    def formulaire_eleve(self, mode="Ajouter", eleve=None):
        popup = ctk.CTkToplevel(self)
        popup.title(f"{mode} Élève")
        popup.geometry("800x550")
        popup.minsize(800, 550)
        popup.transient(self.winfo_toplevel())
        popup.grab_set()
        popup.configure(fg_color=THEME["bg_main"])
        
        main_frame = ctk.CTkFrame(popup, fg_color="transparent")
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        main_frame.grid_columnconfigure(0, weight=1)
        main_frame.grid_columnconfigure(1, weight=1)
        main_frame.grid_rowconfigure(1, weight=1)

        # Header du formulaire
        title_text = "Nouveau Profil Élève" if mode == "Ajouter" else f"Détails de {eleve[1]} {eleve[2]}" if mode == "Détails" else f"Modification de {eleve[1]} {eleve[2]}"
        ctk.CTkLabel(main_frame, text=title_text, font=ctk.CTkFont(FONT_FAMILY, 24, "bold"), text_color=THEME["accent_blue"]).grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 15))

        # Cadre photo
        photo_frame = ctk.CTkFrame(main_frame, fg_color=THEME["card_bg"], corner_radius=16)
        photo_frame.grid(row=0, column=1, sticky="e", pady=(0, 15), padx=(10, 0))
        photo_frame.grid_propagate(False)
        photo_frame.configure(width=160, height=160)
        self.photo_label = ctk.CTkLabel(photo_frame, text="", image=square_photo(None))
        self.photo_label.pack(fill="both", expand=True, padx=10, pady=10)

        # Cadre pour les champs du formulaire
        form_frame = ctk.CTkScrollableFrame(main_frame, fg_color=THEME["card_bg"], corner_radius=16)
        form_frame.grid(row=1, column=0, columnspan=2, sticky="nsew", pady=(0, 20))
        form_frame.grid_columnconfigure(0, weight=1)
        form_frame.grid_columnconfigure(1, weight=1)

        fields = [
            ("Informations Personnelles", [
                ("Nom", "nom", "Entry"), ("Prénom", "prenom", "Entry"),
                ("Date de naissance", "date_naissance", "Entry", "AAAA-MM-JJ"),
                ("Lieu de naissance", "lieu_naissance", "Entry"),
                ("Sexe", "sexe", "OptionMenu", ["Masculin", "Féminin"]),
                ("Statut", "statut", "OptionMenu", ["Actif", "Inactif"]),
                ("N° Téléphone", "telephone", "Entry"), ("Email", "email", "Entry"),
            ]),
            ("Informations sur les Parents", [
                ("Nom du père", "nom_pere", "Entry"), ("Nom de la mère", "nom_mere", "Entry"),
                ("N° Tél du père", "telephone_pere", "Entry"), ("N° Tél de la mère", "telephone_mere", "Entry"),
            ]),
            ("Adresse", [
                ("Adresse", "adresse", "Entry"),
            ]),
        ]

        self.form_entries = {}
        row_idx = 0
        for section_title, section_fields in fields:
            ctk.CTkLabel(form_frame, text=section_title, font=ctk.CTkFont(FONT_FAMILY, FONT_SIZE_HEADER-2, "bold"), text_color=THEME["accent_blue"])\
                .grid(row=row_idx, column=0, columnspan=2, sticky="w", padx=10, pady=(10, 5))
            row_idx += 1
            
            for i, (label_text, key, widget_type, *args) in enumerate(section_fields):
                current_row, current_col = row_idx + i // 2, (i % 2) * 2
                
                ctk.CTkLabel(form_frame, text=f"{label_text}:", font=ctk.CTkFont(FONT_FAMILY, 14, "bold"),
                             text_color=THEME["primary_text"]).grid(row=current_row, column=current_col, sticky="w", padx=(10, 0), pady=(0,5))
                
                if widget_type == "Entry":
                    widget = ctk.CTkEntry(form_frame, font=ctk.CTkFont(FONT_FAMILY, 14),
                                          fg_color=THEME["bg_main"], border_color=THEME["border_color"],
                                          placeholder_text=args[0] if args else "")
                elif widget_type == "OptionMenu":
                    widget = ctk.CTkOptionMenu(form_frame, values=args[0],
                                               fg_color=THEME["bg_main"], button_color=THEME["accent_blue"],
                                               button_hover_color=THEME["hover_light"])
                
                widget.grid(row=current_row, column=current_col + 1, sticky="ew", padx=(0, 10), pady=(0,5))
                self.form_entries[key] = widget
            row_idx += (len(section_fields) + 1) // 2

        # Boutons d'action
        btn_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        btn_frame.grid(row=2, column=0, columnspan=2, sticky="ew")

        if mode == "Ajouter":
            ctk.CTkButton(btn_frame, text="Enregistrer",
                          command=lambda: self.save_eleve(popup, mode),
                          fg_color=THEME["success_green"], hover_color=THEME["hover_light"]).pack(side="left", expand=True, fill="x", padx=(0, 5))
        elif mode == "Modifier":
            ctk.CTkButton(btn_frame, text="Mettre à jour",
                          command=lambda: self.save_eleve(popup, mode, eleve[0]),
                          fg_color=THEME["info_orange"], hover_color=THEME["hover_light"]).pack(side="left", expand=True, fill="x", padx=(0, 5))

        close_btn = ctk.CTkButton(btn_frame, text="Fermer", command=popup.destroy,
                                  fg_color=THEME["error_red"], hover_color=THEME["hover_light"])
        close_btn.pack(side="left", expand=True, fill="x", padx=(5, 0))

        if eleve:
            self.photo_label.configure(image=square_photo(eleve[12]))
            self.fill_form(eleve)
        if mode == "Détails":
            for entry in self.form_entries.values():
                try: entry.configure(state="disabled")
                except Exception: pass
            close_btn.configure(fg_color=THEME["accent_blue"])
            btn_frame.winfo_children()[0].destroy()
            btn_frame.winfo_children()[0].pack_forget()

    def fill_form(self, eleve):
        data_map = {
            "nom": eleve[1], "prenom": eleve[2], "sexe": eleve[3],
            "date_naissance": eleve[4], "lieu_naissance": eleve[5],
            "statut": eleve[6], "telephone": eleve[7], "email": eleve[8],
            "adresse": eleve[9], "nom_pere": eleve[10], "nom_mere": eleve[11],
            "telephone_pere": eleve[13], "telephone_mere": eleve[14]
        }
        for key, value in data_map.items():
            w = self.form_entries.get(key)
            if not w or value is None: continue
            if isinstance(w, ctk.CTkEntry):
                w.insert(0, value)
            elif isinstance(w, ctk.CTkOptionMenu):
                w.set(value)

    def save_eleve(self, popup, mode, eleve_id=None):
        data = {key: widget.get() for key, widget in self.form_entries.items()}
        data["photo"] = None # Pas de gestion de l'upload de photo dans cet exemple

        if not all([data.get("nom"), data.get("prenom"), data.get("sexe"), data.get("date_naissance"), data.get("statut")]):
            messagebox.showerror("Erreur", "Veuillez remplir les champs obligatoires.")
            return
        if not is_name(data["nom"]) or not is_name(data["prenom"]):
            messagebox.showerror("Erreur", "Le nom et le prénom ne doivent contenir que des lettres et des espaces.")
            return
        if not is_date(data["date_naissance"]):
            messagebox.showerror("Erreur", "Le format de la date de naissance est incorrect (AAAA-MM-JJ).")
            return
        if data.get("telephone") and not is_phone(data["telephone"]):
            messagebox.showerror("Erreur", "Le format du numéro de téléphone est incorrect.")
            return
        if data.get("email") and not is_email(data["email"]):
            messagebox.showerror("Erreur", "Le format de l'email est incorrect.")
            return

        conn = get_db_connection()
        if conn:
            cur = conn.cursor()
            try:
                if mode == "Ajouter":
                    cur.execute("""
                        INSERT INTO eleves (nom, prenom, sexe, date_naissance, lieu_naissance, statut,
                        telephone, email, adresse, nom_pere, nom_mere, photo, telephone_pere, telephone_mere, classe_id)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """, (data["nom"], data["prenom"], data["sexe"], data["date_naissance"], data["lieu_naissance"],
                          data["statut"], data["telephone"], data["email"], data["adresse"], data["nom_pere"],
                          data["nom_mere"], data["photo"], data["telephone_pere"], data["telephone_mere"], self.selected_classe))
                    messagebox.showinfo("Succès", "Élève ajouté avec succès.")
                elif mode == "Modifier":
                    cur.execute("""
                        UPDATE eleves SET nom=?, prenom=?, sexe=?, date_naissance=?, lieu_naissance=?, statut=?,
                        telephone=?, email=?, adresse=?, nom_pere=?, nom_mere=?, photo=?, telephone_pere=?, telephone_mere=?
                        WHERE id=?
                    """, (data["nom"], data["prenom"], data["sexe"], data["date_naissance"], data["lieu_naissance"],
                          data["statut"], data["telephone"], data["email"], data["adresse"], data["nom_pere"],
                          data["nom_mere"], data["photo"], data["telephone_pere"], data["telephone_mere"], eleve_id))
                    messagebox.showinfo("Succès", "Élève mis à jour avec succès.")
                
                conn.commit()
                self.refresh()
                popup.destroy()
            except sqlite3.Error as e:
                messagebox.showerror("Erreur de base de données", f"Une erreur est survenue : {e}")
            finally:
                conn.close()

# ============ Exécution de l'application ============
if __name__ == "__main__":
    app = ctk.CTk()
    app.title("Dashboard des Élèves")
    app.geometry("1200x800")
    app.grid_rowconfigure(0, weight=1)
    app.grid_columnconfigure(0, weight=1)
    
    # Simuler un utilisateur pour l'exemple
    class FakeUser:
        def __init__(self, username):
            self.username = username
    
    dashboard_eleves = DashboardEleves(app)
    dashboard_eleves.pack(fill="both", expand=True)

    app.mainloop()