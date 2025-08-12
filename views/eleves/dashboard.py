import customtkinter as ctk
from tkinter import ttk, messagebox, filedialog
from PIL import Image
import os, datetime, re, sqlite3
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# ============ Thème et Constantes ============
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

# --- Chemin DB et icônes ---
DB_PATH = r"C:\Users\Lenovo\Desktop\EduManager+\database\edumanager.db"
ICON_PATH_BASE = r"C:\Users\Lenovo\Desktop\EduManager+\assets\icons"

ICON_MAP = {
    "eleves": "book.png",
    "filles": "eleve.png",
    "garcons": "person.png",
    "classes": "cover.png",
    "ajouter": "add.png",
    "edit": "edit.png",
    "delete": "delete.png",
    "detail": "detail.png",
    "transferer": "transfer.png",
    "refresh": "refresh.png",
    "search": "search.png",
    "close": "close.png",
}

def _icon_candidates(name: str):
    yield name
    if name in ICON_MAP:
        yield ICON_MAP.get(name).replace(".png", "")

# --- Regex de validation ---
EMAIL_RE = re.compile(r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$")
PHONE_RE = re.compile(r"^\+?\d{7,15}$")
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
NAME_RE = re.compile(r"^[A-Za-zÀ-ÖØ-öø-ÿ' -]{2,}$")
def is_email(val): return bool(EMAIL_RE.match(val)) if val else True
def is_phone(val): return bool(PHONE_RE.match(val)) if val else True
def is_date(val):
    if not val: return True
    if not DATE_RE.match(val): return False
    try:
        datetime.datetime.strptime(val, "%Y-%m-%d"); return True
    except Exception:
        return False
def is_name(val): return bool(NAME_RE.match(val)) if val else False

# --- Utils ---
def compute_age(date_str: str):
    if not date_str or not is_date(date_str): return "—"
    y, m, d = (int(x) for x in date_str.split("-"))
    today = datetime.date.today()
    age = today.year - y - ((today.month, today.day) < (m, d))
    return str(age)

def square_photo(path, size=(160, 160)):
    try:
        if path and os.path.exists(path):
            img = Image.open(path).resize(size, RESAMPLE_LANCZOS)
        else:
            img = Image.new("RGB", size, THEME["header_bg"])
    except Exception:
        img = Image.new("RGB", size, THEME["header_bg"])
    return ctk.CTkImage(light_image=img, dark_image=img, size=size)

# ============ DB helpers ============
def get_db_connection():
    try:
        return sqlite3.connect(DB_PATH)
    except sqlite3.Error as e:
        messagebox.showerror("Erreur DB", f"Connexion impossible : {e}")
        return None

def get_all_classes():
    conn = get_db_connection()
    if not conn: return []
    cur = conn.cursor()
    cur.execute("SELECT id, nom FROM classe ORDER BY nom")
    rows = cur.fetchall()
    conn.close()
    return rows

def get_stats_eleves(classe_id=None):
    conn = get_db_connection()
    if not conn: return {"total":0, "filles":0, "garcons":0, "classes":0, "profs":0}
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

def get_eleves_by_classe(classe_id=None):
    conn = get_db_connection()
    if not conn: return []
    cur = conn.cursor()
    if classe_id is None:
        cur.execute("""
            SELECT c.nom, COUNT(e.id)
            FROM classe c LEFT JOIN eleves e ON e.classe_id = c.id
            GROUP BY c.nom ORDER BY c.nom
        """)
    else:
        cur.execute("""
            SELECT c.nom, COUNT(e.id)
            FROM classe c LEFT JOIN eleves e ON e.classe_id = c.id
            WHERE c.id=? GROUP BY c.nom
        """, (classe_id,))
    rows = cur.fetchall()
    conn.close()
    return rows

def get_eleves_list(classe_id=None):
    """Retourne (id, nom, prenom, sexe, date_naissance, statut, classe_id)"""
    conn = get_db_connection()
    if not conn: return []
    cur = conn.cursor()
    if classe_id is None:
        cur.execute("SELECT id, nom, prenom, sexe, date_naissance, statut, classe_id FROM eleves ORDER BY nom, prenom")
    else:
        cur.execute("SELECT id, nom, prenom, sexe, date_naissance, statut, classe_id FROM eleves WHERE classe_id=? ORDER BY nom, prenom", (classe_id,))
    rows = cur.fetchall()
    conn.close()
    return rows

def get_eleve_complet(eleve_id):
    """Dict complet aligné sur ta table (avec lieu_naissance + date_inscription)."""
    conn = get_db_connection()
    if not conn: return None
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute("""
        SELECT
            id, nom, prenom, sexe, date_naissance, lieu_naissance, statut,
            telephone, email,
            nom_pere, telephone_pere, nom_mere, telephone_mere,
            adresse, photo_path, classe_id, date_inscription,
            telephone_parent, email_parent
        FROM eleves
        WHERE id=?
    """, (eleve_id,))
    row = cur.fetchone()
    conn.close()
    return dict(row) if row else None

def get_classe_name(classe_id):
    if classe_id is None: return None
    conn = get_db_connection()
    if not conn: return None
    cur = conn.cursor()
    cur.execute("SELECT nom FROM classe WHERE id=?", (classe_id,))
    row = cur.fetchone()
    conn.close()
    return row[0] if row else None

# ============ Classe principale UI ============
class DashboardEleves(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color=THEME["bg_main"])
        self.selected_classe = None
        self.selected_eleve = None
        self._selected_photo_path = None
        self.classes_map = {}
        self._sort_state = {}

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
        self.update_classes_sidebar()
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
        self.clear_btn.grid() if self.search_var.get() else self.clear_btn.grid_remove()

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

            icon = self._load_icon(icon_name, 28, 28)
            row = ctk.CTkFrame(card, fg_color="transparent")
            row.pack(fill="x", padx=10, pady=(10, 5))
            ctk.CTkLabel(row, image=icon, text="", width=30).pack(side="left")
            ctk.CTkLabel(row, text=title, font=ctk.CTkFont(FONT_FAMILY, 13, "bold"),
                         text_color=THEME["secondary_text"]).pack(side="left", padx=(5, 0))
            lbl = ctk.CTkLabel(card, text=value, font=ctk.CTkFont(FONT_FAMILY, 34, "bold"), text_color=accent_color)
            lbl.pack(pady=(0, 10), anchor="w", padx=15)
            self.stats_labels.append(lbl)

    # ---------- Graph
    def _create_graph_section(self, parent_frame):
        self.graph_box = ctk.CTkFrame(parent_frame, fg_color=THEME["card_bg"], corner_radius=16,
                                      border_width=1, border_color=THEME["border_color"])
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
            ctk.CTkLabel(self.graph_box, text="📊\n\nAucune donnée à afficher",
                         font=ctk.CTkFont(FONT_FAMILY, 16, "bold"),
                         text_color=THEME["secondary_text"]).pack(pady=40)
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
            if v > 0: ax.text(i, v + 0.5, str(v), color=THEME["primary_text"], fontsize=10, ha='center', fontweight='bold')
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
        self._btn_crud(actions_bar, "Ajouter", THEME["success_green"], self.ajouter_eleve, "ajouter").pack(side="left", padx=(0, 5), expand=True, fill="x")
        self._btn_crud(actions_bar, "Modifier", THEME["info_orange"], self.modifier_eleve, "edit").pack(side="left", padx=5, expand=True, fill="x")
        self._btn_crud(actions_bar, "Supprimer", THEME["error_red"], self.supprimer_eleve, "delete").pack(side="left", padx=5, expand=True, fill="x")
        self._btn_crud(actions_bar, "Détails", THEME["accent_blue"], self.details_eleve, "detail").pack(side="left", padx=5, expand=True, fill="x")
        self._btn_crud(actions_bar, "Transférer", THEME["warning_yellow"], self.ouvrir_transfert, "transferer").pack(side="left", padx=5, expand=True, fill="x")

    # ---------- Table (design + tri + Âge/Classe)
    def _create_table_section(self, parent_frame):
        table_container = ctk.CTkFrame(parent_frame, fg_color=THEME["card_bg"], corner_radius=16)
        table_container.grid(row=4, column=0, sticky="nsew")
        table_container.grid_rowconfigure(0, weight=1)
        table_container.grid_columnconfigure(0, weight=1)

        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview",
                        background=THEME["card_bg"], fieldbackground=THEME["card_bg"], foreground=THEME["primary_text"],
                        rowheight=50, font=(FONT_FAMILY, 12), borderwidth=0, relief="flat")
        style.configure("Treeview.Heading",
                        background=THEME["header_bg"], foreground=THEME["accent_blue"],
                        font=(FONT_FAMILY, 13, "bold"), relief="flat", borderwidth=0, padding=6)
        style.map("Treeview",
                  background=[('selected', THEME["select_highlight"])],
                  foreground=[('selected', THEME["primary_text"])])

        self.table_columns = ("id", "nom", "prenom", "sexe", "date_naissance", "age", "classe", "statut")
        self.table = ttk.Treeview(table_container, columns=self.table_columns, show="headings", selectmode="browse")

        headings = [
            ("id", "ID"), ("nom", "Nom"), ("prenom", "Prénom"), ("sexe", "Sexe"),
            ("date_naissance", "Naissance"), ("age", "Âge"), ("classe", "Classe"), ("statut", "Statut")
        ]
        for col, label in headings:
            self.table.heading(col, text=label, command=lambda c=col: self._sort_by_column(c))
            width = 80 if col in ("id", "age", "sexe") else 130
            if col in ("nom", "prenom", "classe"): width = 160
            self.table.column(col, anchor="center", minwidth=70, width=width)

        table_scroll = ctk.CTkScrollbar(
            table_container, orientation="vertical", command=self.table.yview,
            fg_color=THEME["header_bg"], button_color=THEME["accent_blue"], button_hover_color=THEME["accent_blue"]
        )
        table_scroll.grid(row=0, column=1, sticky="ns", padx=(0, 2), pady=(10, 10))
        self.table.configure(yscrollcommand=table_scroll.set)
        self.table.grid(row=0, column=0, sticky="nsew", pady=10, padx=(10, 0))

        self.table.tag_configure('oddrow', background=THEME["card_bg"])
        self.table.tag_configure('evenrow', background=THEME["header_bg"])
        self.table.tag_configure('status_actif', foreground=THEME["success_green"])
        self.table.tag_configure('status_inactif', foreground=THEME["error_red"])

        self.table.bind("<<TreeviewSelect>>", self.on_select_eleve)
        self.table_data = []  # tuples DB

    def _sort_by_column(self, col):
        reverse = self._sort_state.get(col, False)
        items = [(iid, self.table.item(iid, "values")) for iid in self.table.get_children()]
        idx = self.table_columns.index(col)
        try:
            items.sort(key=lambda it: (int(it[1][idx]) if str(it[1][idx]).isdigit() else str(it[1][idx]).lower()), reverse=reverse)
        except Exception:
            items.sort(key=lambda it: str(it[1][idx]).lower(), reverse=reverse)
        for i, (iid, _) in enumerate(items):
            self.table.move(iid, "", i)
        self._sort_state[col] = not reverse

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
        # map id -> nom
        classes = get_all_classes()
        self.classes_map = {cid: nom for cid, nom in classes}

        for w in self.classe_btns_frame.winfo_children(): w.destroy()
        self.classe_btns = []

        btn_tous = ctk.CTkButton(
            self.classe_btns_frame, text="Tous les élèves", font=ctk.CTkFont(FONT_FAMILY, 14, "bold"),
            fg_color=THEME["warning_yellow"], text_color=THEME["bg_main"],
            hover_color=THEME["hover_light"],
            command=lambda: self.update_dashboard_for_classe(None)
        )
        btn_tous.pack(fill="x", pady=(5, 2))
        self.classe_btns.append((btn_tous, None))

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
            _id, nom, prenom, sexe, naissance, statut, cid = e
            age = compute_age(naissance)
            cls = self.classes_map.get(cid, "—")
            values = (_id, nom, prenom, sexe or "—", naissance or "—", age, cls, statut or "—")
            tag_zebra = 'evenrow' if i % 2 == 0 else 'oddrow'
            tag_status = 'status_actif' if (statut or "").lower().startswith("act") else 'status_inactif'
            self.table.insert("", "end", values=values, tags=(tag_zebra, tag_status))

    def refresh(self):
        self.update_dashboard_for_classe(self.selected_classe)
        self.clear_search()
        self.selected_eleve = None

    def on_select_eleve(self, event):
        selected = self.table.selection()
        self.selected_eleve = self.table.item(selected[0])["values"][0] if selected else None

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
        self._open_eleve_details_card(eleve)

    def apply_search_filter(self):
        term = self.search_var.get().strip().lower()
        if not term:
            self.update_table(self.table_data); return
        filtered = [r for r in self.table_data if any(term in str(r[i]).lower() for i in [0,1,2,3,5])]
        self.update_table(filtered)

    # ---------- Détails (Carte premium)
    def _open_eleve_details_card(self, e: dict):
        import datetime
        import customtkinter as ctk

        # ---------------- Helpers ----------------
        def _age(d):
            try:
                if not d: return "—"
                y, m, d2 = map(int, str(d).split("-"))
                t = datetime.date.today()
                return str(t.year - y - ((t.month, t.day) < (m, d2)))
            except Exception:
                return "—"

        def _kv_row(parent, r, label, value, span=1):
            """Ligne clé/valeur (full grid, pas de pack)."""
            lbl = ctk.CTkLabel(parent, text=label, text_color=THEME["secondary_text"],
                            font=ctk.CTkFont(FONT_FAMILY, 13, "bold"), anchor="w")
            val = ctk.CTkLabel(parent, text=value or "—", text_color=THEME["primary_text"],
                            font=ctk.CTkFont(FONT_FAMILY, 14), anchor="w", justify="left")
            lbl.grid(row=r, column=0, sticky="w", padx=(16, 10), pady=(6, 0))
            val.grid(row=r, column=1, columnspan=span, sticky="w", padx=(0, 16), pady=(6, 0))

        def _section(parent, title, c=0, r=0, colspan=1):
            """Carte section, full grid."""
            card = ctk.CTkFrame(parent, fg_color=THEME["card_bg"],
                                border_width=1, border_color=THEME["border_color"])
            card.grid(row=r, column=c, columnspan=colspan, sticky="nsew", padx=8, pady=8)
            card.grid_columnconfigure(0, weight=0)
            card.grid_columnconfigure(1, weight=1)

            header = ctk.CTkLabel(card, text=title, text_color=THEME["accent_blue"],
                                font=ctk.CTkFont(FONT_FAMILY, 16, "bold"), anchor="w")
            header.grid(row=0, column=0, columnspan=2, sticky="ew", padx=16, pady=(14, 8))
            ctk.CTkFrame(card, height=1, fg_color=THEME["border_color"]).grid(
                row=1, column=0, columnspan=2, sticky="ew", padx=16, pady=(0, 6)
            )
            return card

        # ---------------- Window ----------------
        top = ctk.CTkToplevel(self)
        top.title(f"Détails — {e.get('nom','')} {e.get('prenom','')}")
        top.geometry("980x720"); top.minsize(940, 700)
        top.transient(self.winfo_toplevel()); top.grab_set()
        top.configure(fg_color=THEME["bg_main"])
        top.bind("<Escape>", lambda _=None: top.destroy())

        # Root (grid only)
        root = ctk.CTkFrame(top, fg_color="transparent")
        root.grid(row=0, column=0, sticky="nsew", padx=16, pady=16)
        top.grid_rowconfigure(0, weight=1)
        top.grid_columnconfigure(0, weight=1)
        root.grid_columnconfigure(0, weight=1)
        root.grid_rowconfigure(1, weight=1)

        # ---------------- Header (full grid) ----------------
        header = ctk.CTkFrame(root, fg_color=THEME["card_bg"],
                            border_width=1, border_color=THEME["border_color"])
        header.grid(row=0, column=0, sticky="ew")
        header.grid_columnconfigure(0, weight=0)
        header.grid_columnconfigure(1, weight=1)
        header.grid_columnconfigure(2, weight=0)

        # Photo carrée (pas d’arrondis)
        photo_wrap = ctk.CTkFrame(header, fg_color=THEME["bg_main"])
        photo_wrap.grid(row=0, column=0, padx=16, pady=16, sticky="w")
        photo_wrap.configure(width=160, height=160); photo_wrap.grid_propagate(False)
        photo = square_photo(e.get("photo_path"), size=(160, 160))
        ctk.CTkLabel(photo_wrap, image=photo, text="").grid(row=0, column=0, sticky="nsew")

        # Bloc identité
        ident = ctk.CTkFrame(header, fg_color="transparent")
        ident.grid(row=0, column=1, sticky="nsew", pady=16)
        ident.grid_columnconfigure(0, weight=1)

        fullname = f"{(e.get('nom') or '').upper()} {e.get('prenom') or ''}".strip()
        ctk.CTkLabel(ident, text=fullname, text_color=THEME["accent_blue"],
                    font=ctk.CTkFont(FONT_FAMILY, 26, "bold"), anchor="w").grid(
            row=0, column=0, sticky="w", padx=(4, 4), pady=(4, 6)
        )

        cls_name = get_classe_name(e.get("classe_id"))
        sub = f"{cls_name or 'Classe —'}   |   {_age(e.get('date_naissance'))} ans"
        ctk.CTkLabel(ident, text=sub, text_color=THEME["secondary_text"],
                    font=ctk.CTkFont(FONT_FAMILY, 14), anchor="w").grid(
            row=1, column=0, sticky="w", padx=(4, 4), pady=(0, 10)
        )

        # Badges plats
        badges = ctk.CTkFrame(ident, fg_color="transparent")
        badges.grid(row=2, column=0, sticky="w", padx=(0, 0))
        for txt, bg in [
            (e.get("statut") or "—", THEME["info_orange"]),
            (e.get("sexe") or "—", THEME["hover_light"]),
        ]:
            ctk.CTkLabel(badges, text=txt, fg_color=bg, text_color=THEME["primary_text"],
                        font=ctk.CTkFont(FONT_FAMILY, 12, "bold"), corner_radius=4, padx=10, pady=4)\
                .grid(row=0, column=badges.grid_size()[0], padx=(0, 6))

        # Actions
        actions = ctk.CTkFrame(header, fg_color="transparent")
        actions.grid(row=0, column=2, padx=16, pady=16, sticky="e")
        ctk.CTkButton(actions, text="Modifier", height=38,
                    fg_color=THEME["info_orange"], hover_color=THEME["hover_light"],
                    command=lambda: (top.destroy(), self.formulaire_eleve("Modifier", e))).grid(row=0, column=0, padx=(0, 8))
        ctk.CTkButton(actions, text="Fermer", height=38,
                    fg_color=THEME["error_red"], hover_color=THEME["hover_light"],
                    command=top.destroy).grid(row=0, column=1)

        # ---------------- Body (scrollable, grid-only) ----------------
        body = ctk.CTkScrollableFrame(root, fg_color="transparent")
        body.grid(row=1, column=0, sticky="nsew", pady=(10, 0))
        body.grid_columnconfigure(0, weight=1, uniform="cols")
        body.grid_columnconfigure(1, weight=1, uniform="cols")

        # Sections
        # Colonne gauche
        perso = _section(body, "Informations personnelles", c=0, r=0)
        _kv_row(perso, 2, "Nom", e.get("nom"))
        _kv_row(perso, 3, "Prénom", e.get("prenom"))
        _kv_row(perso, 4, "Date de naissance", e.get("date_naissance"))
        _kv_row(perso, 5, "Lieu de naissance", e.get("lieu_naissance"))

        contact = _section(body, "Contact", c=0, r=1)
        _kv_row(contact, 2, "Téléphone", e.get("telephone"))
        _kv_row(contact, 3, "Email", e.get("email"))
        _kv_row(contact, 4, "Adresse", e.get("adresse"), span=1)

        # Colonne droite
        parents = _section(body, "Parents / Tuteurs", c=1, r=0)
        _kv_row(parents, 2, "Nom du père", e.get("nom_pere"))
        _kv_row(parents, 3, "Téléphone du père", e.get("telephone_pere"))
        _kv_row(parents, 4, "Nom de la mère", e.get("nom_mere"))
        _kv_row(parents, 5, "Téléphone de la mère", e.get("telephone_mere"))
        _kv_row(parents, 6, "Téléphone parent (général)", e.get("telephone_parent"))
        _kv_row(parents, 7, "Email parent (général)", e.get("email_parent"))

        meta = _section(body, "Scolarité & métadonnées", c=1, r=1)
        _kv_row(meta, 2, "Classe", cls_name)
        _kv_row(meta, 3, "Date d'inscription", e.get("date_inscription"))
        _kv_row(meta, 4, "Âge", f"{_age(e.get('date_naissance'))} ans" if _age(e.get('date_naissance')) != "—" else "—")
        # Si tu stockes created_at / updated_at :
        if e.get("created_at") is not None or e.get("updated_at") is not None:
            _kv_row(meta, 5, "Créé le", e.get("created_at"))
            _kv_row(meta, 6, "Modifié le", e.get("updated_at"))

        # Assure une bonne répartition verticale si peu de contenu
        for r in range(2):
            body.grid_rowconfigure(r, weight=1)


    # ---------- Formulaire (Wizard 3 étapes)
    def formulaire_eleve(self, mode="Ajouter", eleve=None):
        popup = ctk.CTkToplevel(self)
        popup.title(f"{mode} Élève")
        popup.geometry("1000x720")
        popup.minsize(980, 680)
        popup.transient(self.winfo_toplevel())
        popup.grab_set()
        popup.configure(fg_color=THEME["bg_main"])

        root = ctk.CTkFrame(popup, fg_color="transparent")
        root.pack(fill="both", expand=True)
        root.grid_columnconfigure(0, weight=1)
        root.grid_rowconfigure(2, weight=1)

        header = ctk.CTkFrame(root, fg_color=THEME["card_bg"], corner_radius=18)
        header.grid(row=0, column=0, sticky="ew", padx=20, pady=(20, 12))
        header.grid_columnconfigure(0, weight=1)
        title_text = "Nouveau Profil Élève" if mode == "Ajouter" else f"{'Détails' if mode=='Détails' else 'Modification'} de {(eleve or {}).get('nom','')} {(eleve or {}).get('prenom','')}"
        ctk.CTkLabel(header, text=title_text, font=ctk.CTkFont(FONT_FAMILY, 28, "bold"),
                     text_color=THEME["accent_blue"]).grid(row=0, column=0, sticky="w", padx=18, pady=(18, 12))

        steps_bar = ctk.CTkFrame(root, fg_color="transparent")
        steps_bar.grid(row=1, column=0, sticky="ew", padx=20, pady=(0, 8))
        steps_bar.grid_columnconfigure(0, weight=1)

        step_wrap = ctk.CTkFrame(steps_bar, fg_color=THEME["card_bg"], corner_radius=12,
                                 border_width=1, border_color=THEME["border_color"])
        step_wrap.grid(row=0, column=0, sticky="ew")

        self._eleve_step_var = ctk.StringVar(value="Profil")
        stepper = ctk.CTkSegmentedButton(
            step_wrap,
            variable=self._eleve_step_var,
            values=["Profil", "Parents", "Adresse"],
            fg_color=THEME["card_bg"],
            selected_color=THEME["accent_blue"],
            unselected_color=THEME["bg_main"]
        )
        stepper.grid(row=0, column=0, sticky="ew", padx=2, pady=2)

        body = ctk.CTkFrame(root, fg_color="transparent")
        body.grid(row=2, column=0, sticky="nsew", padx=20, pady=(8, 12))
        body.grid_columnconfigure(0, weight=1)
        body.grid_rowconfigure(0, weight=1)

        card_profil = ctk.CTkScrollableFrame(body, fg_color=THEME["card_bg"], corner_radius=18,
                                             border_width=1, border_color=THEME["border_color"])
        card_parents = ctk.CTkScrollableFrame(body, fg_color=THEME["card_bg"], corner_radius=18,
                                              border_width=1, border_color=THEME["border_color"])
        card_adresse = ctk.CTkScrollableFrame(body, fg_color=THEME["card_bg"], corner_radius=18,
                                              border_width=1, border_color=THEME["border_color"])
        for card in (card_profil, card_parents, card_adresse):
            card.grid_columnconfigure(0, weight=1)

        def section_title(parent, text):
            wrap = ctk.CTkFrame(parent, fg_color="transparent")
            wrap.grid_columnconfigure(0, weight=0)
            wrap.grid_columnconfigure(1, weight=1)
            ctk.CTkLabel(wrap, text=text,
                         font=ctk.CTkFont(FONT_FAMILY, FONT_SIZE_HEADER, "bold"),
                         text_color=THEME["accent_blue"]).grid(row=0, column=0, sticky="w",
                                                               padx=(18, 12), pady=(18, 6))
            ctk.CTkFrame(wrap, height=2, fg_color=THEME["border_color"]).grid(
                row=0, column=1, sticky="ew", padx=(0, 18), pady=(28, 0)
            )
            return wrap

        def make_label(parent, text):
            return ctk.CTkLabel(parent, text=text,
                                font=ctk.CTkFont(FONT_FAMILY, 15, "bold"),
                                text_color=THEME["primary_text"])

        def make_entry(parent, placeholder=""):
            return ctk.CTkEntry(parent, font=ctk.CTkFont(FONT_FAMILY, 14),
                                fg_color=THEME["bg_main"], border_color=THEME["border_color"],
                                placeholder_text=placeholder, height=52)

        def make_select(parent, values):
            return ctk.CTkOptionMenu(parent, values=values,
                                     fg_color=THEME["bg_main"], button_color=THEME["accent_blue"],
                                     button_hover_color=THEME["hover_light"], height=52)

        self.form_entries = {}

        # -------- Étape 1 : Profil
        section_title(card_profil, "Profil de l’élève").grid(row=0, column=0, sticky="ew")
        photo_block = ctk.CTkFrame(card_profil, fg_color="transparent")
        photo_block.grid(row=1, column=0, sticky="w", padx=18, pady=(6, 8))
        photo_frame = ctk.CTkFrame(photo_block, fg_color=THEME["bg_main"], corner_radius=16)
        photo_frame.grid(row=0, column=0, sticky="w")
        photo_frame.configure(width=220, height=220)
        photo_frame.grid_propagate(False)
        self.photo_label = ctk.CTkLabel(photo_frame, text="", image=square_photo(None))
        self.photo_label.pack(expand=True, fill="both", padx=12, pady=12)
        def _choose_photo():
            path = filedialog.askopenfilename(title="Choisir une photo", filetypes=[("Images", "*.png;*.jpg;*.jpeg;*.webp")])
            if path:
                try:
                    self.photo_label.configure(image=square_photo(path))
                    self._selected_photo_path = path
                except Exception:
                    pass
        ctk.CTkButton(photo_block, text="Importer", command=_choose_photo,
                      fg_color=THEME["accent_blue"], hover_color=THEME["hover_light"], height=40)\
            .grid(row=0, column=1, sticky="w", padx=(12, 0))
        ctk.CTkButton(photo_block, text="Supprimer",
                      command=lambda: (self.photo_label.configure(image=square_photo(None)), setattr(self, "_selected_photo_path", None)),
                      fg_color=THEME["error_red"], hover_color=THEME["hover_light"], height=40)\
            .grid(row=0, column=2, sticky="w", padx=(8, 0))

        profil_fields = [
            ("Nom *", "nom", "Entry", ""),
            ("Prénom *", "prenom", "Entry", ""),
            ("Date de naissance", "date_naissance", "Entry", "AAAA-MM-JJ"),
            ("Lieu de naissance", "lieu_naissance", "Entry", ""),
            ("Sexe", "sexe", "OptionMenu", ["Masculin", "Féminin"]),
            ("Statut", "statut", "OptionMenu", ["Actif", "Inactif"]),
            ("N° Téléphone", "telephone", "Entry", ""),
            ("Email", "email", "Entry", ""),
        ]
        r = 2
        for label_text, key, wtype, arg in profil_fields:
            make_label(card_profil, label_text).grid(row=r, column=0, sticky="w", padx=18, pady=(12, 4))
            widget = make_entry(card_profil, arg) if wtype == "Entry" else make_select(card_profil, arg)
            widget.grid(row=r+1, column=0, sticky="ew", padx=18, pady=(0, 6))
            self.form_entries[key] = widget
            r += 2

        # -------- Étape 2 : Parents
        section_title(card_parents, "Informations des parents / tuteurs").grid(row=0, column=0, sticky="ew")
        parents_fields = [
            ("Nom du père", "nom_pere", "Entry", ""),
            ("N° Tél du père", "telephone_pere", "Entry", ""),
            ("Nom de la mère", "nom_mere", "Entry", ""),
            ("N° Tél de la mère", "telephone_mere", "Entry", ""),
            ("Téléphone parent (général)", "telephone_parent", "Entry", ""),
            ("Email parent (général)", "email_parent", "Entry", ""),
        ]
        r = 1
        for label_text, key, wtype, arg in parents_fields:
            make_label(card_parents, label_text).grid(row=r, column=0, sticky="w", padx=18, pady=(12, 4))
            widget = make_entry(card_parents, arg)
            widget.grid(row=r+1, column=0, sticky="ew", padx=18, pady=(0, 6))
            self.form_entries[key] = widget
            r += 2

        # -------- Étape 3 : Adresse
        section_title(card_adresse, "Adresse et localisation").grid(row=0, column=0, sticky="ew")
        make_label(card_adresse, "Adresse").grid(row=1, column=0, sticky="w", padx=18, pady=(12, 4))
        self.form_entries["adresse"] = make_entry(card_adresse, "")
        self.form_entries["adresse"].grid(row=2, column=0, sticky="ew", padx=18, pady=(0, 6))

        def _show_card(name):
            for c in (card_profil, card_parents, card_adresse):
                c.grid_forget()
            (card_profil if name == "Profil" else card_parents if name == "Parents" else card_adresse)\
                .grid(row=0, column=0, sticky="nsew")

        stepper.configure(command=_show_card)
        _show_card(self._eleve_step_var.get())

        footer = ctk.CTkFrame(root, fg_color=THEME["card_bg"], corner_radius=14)
        footer.grid(row=3, column=0, sticky="ew", padx=20, pady=(0, 20))
        for i in range(5): footer.grid_columnconfigure(i, weight=1)

        def _go_prev():
            order = ["Profil", "Parents", "Adresse"]
            i = max(0, order.index(self._eleve_step_var.get()) - 1)
            self._eleve_step_var.set(order[i]); _show_card(order[i])

        def _go_next():
            order = ["Profil", "Parents", "Adresse"]
            i = min(len(order)-1, order.index(self._eleve_step_var.get()) + 1)
            self._eleve_step_var.set(order[i]); _show_card(order[i])

        ctk.CTkButton(footer, text="◀ Précédent", command=_go_prev,
                      fg_color=THEME["bg_main"], hover_color=THEME["hover_light"], height=44)\
            .grid(row=0, column=0, sticky="w", padx=10, pady=10)
        ctk.CTkButton(footer, text="Suivant ▶", command=_go_next,
                      fg_color=THEME["accent_blue"], hover_color=THEME["hover_light"], height=44)\
            .grid(row=0, column=1, sticky="w", padx=(0, 10), pady=10)

        if mode == "Ajouter":
            ctk.CTkButton(footer, text="Enregistrer",
                          command=lambda: self.save_eleve(popup, mode, None, eleve_dict=None),
                          fg_color=THEME["success_green"], hover_color=THEME["hover_light"], height=44)\
                .grid(row=0, column=3, sticky="e", padx=(10, 8), pady=10)
        elif mode == "Modifier":
            ctk.CTkButton(footer, text="Mettre à jour",
                          command=lambda: self.save_eleve(popup, mode, (eleve or {}).get('id')),
                          fg_color=THEME["info_orange"], hover_color=THEME["hover_light"], height=44)\
                .grid(row=0, column=3, sticky="e", padx=(10, 8), pady=10)

        ctk.CTkButton(footer, text="Fermer", command=popup.destroy,
                      fg_color=THEME["error_red"], hover_color=THEME["hover_light"], height=44)\
            .grid(row=0, column=4, sticky="e", padx=(0, 10), pady=10)

        # Pré-remplissage
        if isinstance(eleve, dict):
            try: self.photo_label.configure(image=square_photo(eleve.get("photo_path")))
            except Exception: pass
            self.fill_form(eleve)

        if mode == "Détails":
            for w in self.form_entries.values():
                try: w.configure(state="disabled")
                except Exception: pass
            for child in footer.grid_slaves():
                if isinstance(child, ctk.CTkButton) and child.cget("text") in ("Enregistrer", "Mettre à jour"):
                    child.grid_forget()
            for child in footer.grid_slaves():
                if isinstance(child, ctk.CTkButton) and child.cget("text") == "Fermer":
                    child.configure(fg_color=THEME["accent_blue"])

    def fill_form(self, eleve: dict):
        data_map = {
            "nom": eleve.get("nom"),
            "prenom": eleve.get("prenom"),
            "sexe": eleve.get("sexe"),
            "date_naissance": eleve.get("date_naissance"),
            "lieu_naissance": eleve.get("lieu_naissance"),
            "statut": eleve.get("statut"),
            "telephone": eleve.get("telephone"),
            "email": eleve.get("email"),
            "adresse": eleve.get("adresse"),
            "nom_pere": eleve.get("nom_pere"),
            "telephone_pere": eleve.get("telephone_pere"),
            "nom_mere": eleve.get("nom_mere"),
            "telephone_mere": eleve.get("telephone_mere"),
            "telephone_parent": eleve.get("telephone_parent"),
            "email_parent": eleve.get("email_parent"),
        }
        for key, value in data_map.items():
            w = self.form_entries.get(key)
            if not w or value is None: 
                continue
            try:
                if isinstance(w, ctk.CTkOptionMenu):
                    w.set(value)
                else:
                    w.delete(0, "end"); w.insert(0, value)
            except Exception:
                pass

    def save_eleve(self, popup, mode, eleve_id=None, eleve_dict=None):
        def _get(key):
            w = self.form_entries.get(key)
            return w.get().strip() if w and hasattr(w, "get") else None

        data = {
            "nom": _get("nom"),
            "prenom": _get("prenom"),
            "sexe": _get("sexe"),
            "date_naissance": _get("date_naissance"),
            "lieu_naissance": _get("lieu_naissance"),
            "statut": _get("statut"),
            "telephone": _get("telephone"),
            "email": _get("email"),
            "adresse": _get("adresse"),
            "nom_pere": _get("nom_pere"),
            "nom_mere": _get("nom_mere"),
            "telephone_pere": _get("telephone_pere"),
            "telephone_mere": _get("telephone_mere"),
            "telephone_parent": _get("telephone_parent"),
            "email_parent": _get("email_parent"),
            "photo_path": self._selected_photo_path
        }

        # validations minimales
        if not all([data.get("nom"), data.get("prenom")]):
            messagebox.showerror("Erreur", "Nom et Prénom sont obligatoires.")
            return
        if not is_name(data["nom"]) or not is_name(data["prenom"]):
            messagebox.showerror("Erreur", "Nom/Prénom : lettres, espaces, tirets et apostrophes uniquement.")
            return
        if data.get("date_naissance") and not is_date(data["date_naissance"]):
            messagebox.showerror("Erreur", "Format de la date de naissance : AAAA-MM-JJ.")
            return
        for k in ("telephone", "telephone_pere", "telephone_mere", "telephone_parent"):
            if data.get(k) and not is_phone(data[k]):
                messagebox.showerror("Erreur", f"Numéro invalide pour « {k.replace('_',' ')} ».")
                return
        for k in ("email", "email_parent"):
            if data.get(k) and not is_email(data[k]):
                messagebox.showerror("Erreur", f"Email invalide pour « {k.replace('_',' ')} ».")
                return

        conn = get_db_connection()
        if not conn: return
        try:
            cur = conn.cursor()
            if mode == "Ajouter":
                cur.execute("""
                    INSERT INTO eleves
                    (nom, prenom, sexe, date_naissance, lieu_naissance, statut,
                     telephone, email, adresse, nom_pere, nom_mere, photo_path,
                     telephone_pere, telephone_mere, classe_id, date_inscription,
                     telephone_parent, email_parent)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, date('now'), ?, ?)
                """, (
                    data["nom"], data["prenom"], data["sexe"], data["date_naissance"], data["lieu_naissance"],
                    data["statut"], data["telephone"], data["email"], data["adresse"], data["nom_pere"],
                    data["nom_mere"], data["photo_path"], data["telephone_pere"], data["telephone_mere"],
                    self.selected_classe, data["telephone_parent"], data["email_parent"]
                ))
                messagebox.showinfo("Succès", "Élève ajouté avec succès.")
            elif mode == "Modifier" and eleve_id:
                cur.execute("""
                    UPDATE eleves SET
                        nom=?, prenom=?, sexe=?, date_naissance=?, lieu_naissance=?, statut=?,
                        telephone=?, email=?, adresse=?, nom_pere=?, nom_mere=?, photo_path=?,
                        telephone_pere=?, telephone_mere=?, telephone_parent=?, email_parent=?
                    WHERE id=?
                """, (
                    data["nom"], data["prenom"], data["sexe"], data["date_naissance"], data["lieu_naissance"],
                    data["statut"], data["telephone"], data["email"], data["adresse"], data["nom_pere"],
                    data["nom_mere"], data["photo_path"], data["telephone_pere"], data["telephone_mere"],
                    data["telephone_parent"], data["email_parent"], eleve_id
                ))
                messagebox.showinfo("Succès", "Élève mis à jour avec succès.")

            conn.commit()
            self.refresh()
            popup.destroy()
        except sqlite3.Error as e:
            messagebox.showerror("Erreur de base de données", f"Une erreur est survenue : {e}")
        finally:
            conn.close()

# ============ Exécution directe (pour test) ============
if __name__ == "__main__":
    app = ctk.CTk()
    app.title("Dashboard des Élèves")
    app.geometry("1200x800")
    app.grid_rowconfigure(0, weight=1)
    app.grid_columnconfigure(0, weight=1)

    dashboard_eleves = DashboardEleves(app)
    dashboard_eleves.pack(fill="both", expand=True)

    app.mainloop()
