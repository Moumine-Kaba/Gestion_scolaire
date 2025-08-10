import customtkinter as ctk
from tkinter import messagebox
from PIL import Image
import os
import sys
import sqlite3

# =================== CHEMIN DE LA BASE DE DONNÉES =====================
DB_PATH = r"C:\Users\Lenovo\Desktop\EduManager+\database\edumanager.db"

# Assurez-vous que cette ligne correspond à votre structure de dossiers
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# --- Fonctions de contrôleur avec BDD SQLite (inchangées) ---

def get_db_connection():
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        return conn
    except sqlite3.Error as e:
        print(f"Erreur de connexion à la base de données : {e}")
        return None

def get_all_classes():
    conn = get_db_connection()
    if conn is None: return []
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM classe")
        classes = cursor.fetchall()
        return classes
    except sqlite3.Error as e:
        print(f"Erreur lors de la récupération des classes : {e}")
        return []
    finally:
        if conn: conn.close()

def add_class(nom, prof_id, salle_id, niveau, annee):
    conn = get_db_connection()
    if conn is None: return False
    try:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO classe (nom, niveau, annee, prof_id, salle_id) VALUES (?, ?, ?, ?, ?)",
                       (nom, niveau, annee, prof_id, salle_id))
        conn.commit()
        return True
    except sqlite3.Error as e:
        print(f"Erreur lors de l'ajout de la classe : {e}")
        return False
    finally:
        if conn: conn.close()

def update_class_data(classe_id, nom, prof_id, salle_id, niveau, annee):
    conn = get_db_connection()
    if conn is None: return False
    try:
        cursor = conn.cursor()
        cursor.execute("UPDATE classe SET nom = ?, niveau = ?, annee = ?, prof_id = ?, salle_id = ? WHERE id = ?",
                       (nom, niveau, annee, prof_id, salle_id, classe_id))
        conn.commit()
        return True
    except sqlite3.Error as e:
        print(f"Erreur lors de la mise à jour de la classe : {e}")
        return False
    finally:
        if conn: conn.close()

def delete_class(classe_id):
    conn = get_db_connection()
    if conn is None: return False
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM eleves WHERE classe_id = ?", (classe_id,))
        cursor.execute("DELETE FROM classe WHERE id = ?", (classe_id,))
        conn.commit()
        return True
    except sqlite3.Error as e:
        print(f"Erreur lors de la suppression de la classe et des élèves : {e}")
        if conn: conn.rollback()
        return False
    finally:
        if conn: conn.close()

def get_classe_by_id(classe_id):
    conn = get_db_connection()
    if conn is None: return None
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM classe WHERE id = ?", (classe_id,))
        row = cursor.fetchone()
        return row if row else None
    except sqlite3.Error as e:
        print(f"Erreur lors de la récupération de la classe par ID : {e}")
        return None
    finally:
        if conn: conn.close()

def get_all_professeurs():
    conn = get_db_connection()
    if conn is None: return []
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT id, nom, prenom FROM professeurs")
        profs = cursor.fetchall()
        return [dict(p) for p in profs]
    except sqlite3.Error as e:
        print(f"Erreur lors de la récupération des professeurs : {e}")
        return []
    finally:
        if conn: conn.close()

def get_all_salles():
    conn = get_db_connection()
    if conn is None: return []
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT id, nom FROM salle")
        salles = cursor.fetchall()
        return [dict(s) for s in salles]
    except sqlite3.Error as e:
        print(f"Erreur lors de la récupération des salles : {e}")
        return []
    finally:
        if conn: conn.close()
        
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

# --- Configuration de l'interface ---
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

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
    "hover_light": "#1C3558"
}
FONT = "Inter"

# Nouveau chemin de base pour les icônes
ICONS_BASE_PATH = r"C:\Users\Lenovo\Desktop\EduManager+\assets\icons"

ICONS_PATH = {
    "edit": os.path.join(ICONS_BASE_PATH, "edit.png"),
    "delete": os.path.join(ICONS_BASE_PATH, "delete.png"),
    "view": os.path.join(ICONS_BASE_PATH, "view.png"),
    "add": os.path.join(ICONS_BASE_PATH, "add.png"),
    "import": os.path.join(ICONS_BASE_PATH, "upload.png"),
    "export": os.path.join(ICONS_BASE_PATH, "csv.png"),
    "search": os.path.join(ICONS_BASE_PATH, "search.png"),
    "pdf": os.path.join(ICONS_BASE_PATH, "pdf.png"),
    "reload": os.path.join(ICONS_BASE_PATH, "refresh.png"),
}

def load_icon(path_or_img, size=14):
    """Charge une icône à partir d'un chemin ou d'un CTkImage."""
    if isinstance(path_or_img, ctk.CTkImage):
        return path_or_img
    
    # Vérifie si le fichier existe
    if not os.path.exists(path_or_img):
        img = Image.new("RGBA", (size, size), (255, 255, 255, 0))
        return ctk.CTkImage(light_image=img, dark_image=img, size=(size, size))
    try:
        image = Image.open(path_or_img).resize((size, size), Image.Resampling.LANCZOS)
        return ctk.CTkImage(light_image=image, dark_image=image, size=(size, size))
    except Exception:
        img = Image.new("RGBA", (size, size), (255, 255, 255, 0))
        return ctk.CTkImage(light_image=img, dark_image=img, size=(size, size))

class Badge(ctk.CTkLabel):
    def __init__(self, parent, text, color="#ffffff", bg="#2c3140", font_size=9):
        super().__init__(
            parent,
            text=text,
            font=(FONT, font_size, "bold"),
            fg_color=bg,
            text_color=color,
            corner_radius=4,
            padx=4, pady=1
        )

class NotificationBar(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color=THEME["card_bg"], height=28, corner_radius=8)
        self.msg = ctk.CTkLabel(self, text="", font=(FONT, 10), text_color=THEME["accent_blue"], fg_color="transparent")
        self.msg.pack(side="left", padx=8, pady=2)
    
    def show(self, message, color=None):
        self.msg.configure(text=message, text_color=color or THEME["accent_blue"])
        self.after(2500, lambda: self.msg.configure(text=""))

class StatsBar(ctk.CTkFrame):
    def __init__(self, parent, get_classes_func, get_profs_func):
        super().__init__(parent, fg_color="transparent")
        self.get_classes = get_classes_func
        self.get_profs = get_profs_func
        
        self.stat_classes = Badge(self, "", color="#f190d7", bg="#453141", font_size=8)
        self.stat_classes.pack(side="left", padx=(0, 4), ipady=1)
        
        self.stat_profs = Badge(self, "", color="#90d7f1", bg="#314145", font_size=8)
        self.stat_profs.pack(side="left", padx=4, ipady=1)
        
        self.stat_eleves = Badge(self, "", color=THEME["success_green"], bg="#324531", font_size=8)
        self.stat_eleves.pack(side="left", padx=4, ipady=1)
        
        self.refresh()
    
    def refresh(self):
        classes = self.get_classes()
        profs = self.get_profs()
        total_eleves = 0
        conn = get_db_connection()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute("SELECT COUNT(*) FROM eleves")
                total_eleves = cursor.fetchone()[0]
            except sqlite3.Error as e:
                print(f"Erreur lors du calcul du nombre total d'élèves : {e}")
            finally:
                if conn: conn.close()

        self.stat_classes.configure(text=f"{len(classes)} Classes")
        self.stat_profs.configure(text=f"{len(profs)} Profs")
        self.stat_eleves.configure(text=f"{total_eleves} Élèves")

class ClassCard(ctk.CTkFrame):
    def __init__(self, parent, classe_data, prof_name, salle_name, on_edit, on_delete, icons):
        super().__init__(parent, fg_color=THEME["card_bg"], corner_radius=10, 
                         border_color=THEME["border_color"], border_width=1)
        self.classe_id = classe_data['id']
        self.on_edit = on_edit
        self.on_delete = on_delete
        self.icons = icons

        top_frame = ctk.CTkFrame(self, fg_color="transparent")
        top_frame.pack(fill="x", padx=8, pady=(8, 4))
        
        ctk.CTkLabel(top_frame, text=classe_data['nom'], font=(FONT, 14, "bold"), 
                     text_color=THEME["primary_text"]).pack(anchor="w")

        badges_frame = ctk.CTkFrame(top_frame, fg_color="transparent")
        badges_frame.pack(anchor="w", pady=(2, 0))
        Badge(badges_frame, classe_data['niveau'] or "Niveau non spécifié", color=THEME["accent_blue"], bg=THEME["header_bg"]).pack(side="left")
        Badge(badges_frame, classe_data['annee'] or "Année non spécifiée", color=THEME["warning_yellow"], bg=THEME["header_bg"]).pack(side="left", padx=2)

        details_frame = ctk.CTkFrame(self, fg_color="transparent")
        details_frame.pack(fill="x", padx=8, pady=(4, 8))
        
        details_frame.grid_columnconfigure(0, weight=0)
        details_frame.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(details_frame, text="Prof. Principal:", font=(FONT, 9, "bold"), text_color=THEME["secondary_text"]).grid(row=0, column=0, sticky="w", pady=1)
        ctk.CTkLabel(details_frame, text=prof_name, font=(FONT, 10), text_color=THEME["primary_text"]).grid(row=0, column=1, sticky="w", padx=6)
        
        ctk.CTkLabel(details_frame, text="Salle:", font=(FONT, 9, "bold"), text_color=THEME["secondary_text"]).grid(row=1, column=0, sticky="w", pady=1)
        ctk.CTkLabel(details_frame, text=salle_name, font=(FONT, 10), text_color=THEME["primary_text"]).grid(row=1, column=1, sticky="w", padx=6)
        
        actions_frame = ctk.CTkFrame(self, fg_color="transparent")
        actions_frame.pack(fill="x", padx=8, pady=(0, 8))
        
        edit_btn = ctk.CTkButton(actions_frame, image=load_icon(self.icons["edit"], 14), text="Modifier", 
                                 fg_color=THEME["header_bg"], hover_color=THEME["hover_light"], 
                                 text_color=THEME["primary_text"], font=(FONT, 10, "bold"), corner_radius=6, 
                                 compound="left", command=lambda: self.on_edit(self.classe_id), height=24)
        edit_btn.pack(side="left", fill="x", expand=True, padx=(0, 2))
        
        delete_btn = ctk.CTkButton(actions_frame, image=load_icon(self.icons["delete"], 14), text="Supprimer", 
                                 fg_color=THEME["header_bg"], hover_color=THEME["error_red"], 
                                 text_color=THEME["primary_text"], font=(FONT, 10, "bold"), corner_radius=6,
                                 compound="left", command=lambda: self.on_delete(self.classe_id), height=24)
        delete_btn.pack(side="left", fill="x", expand=True, padx=(2, 0))
        
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)
        for child in self.winfo_children():
            child.bind("<Enter>", self.on_enter)
            child.bind("<Leave>", self.on_leave)
            for sub_child in child.winfo_children():
                sub_child.bind("<Enter>", self.on_enter)
                sub_child.bind("<Leave>", self.on_leave)

    def on_enter(self, event):
        self.configure(fg_color=THEME["hover_light"])
        self.configure(border_color=THEME["accent_blue"])

    def on_leave(self, event):
        self.configure(fg_color=THEME["card_bg"])
        self.configure(border_color=THEME["border_color"])

class ClassesCardView(ctk.CTkFrame):
    def __init__(self, parent, on_edit, on_delete, notif_bar, icons):
        super().__init__(parent, fg_color="transparent")
        self.on_edit = on_edit
        self.on_delete = on_delete
        self.notif_bar = notif_bar
        self.icons = icons
        
        # Le conteneur de la barre de recherche et du bouton de filtre
        top_bar = ctk.CTkFrame(self, fg_color="transparent")
        top_bar.pack(fill="x", padx=15, pady=(8, 4))
        
        # Bouton "Ajouter" à gauche
        ctk.CTkButton(top_bar, text="Ajouter", image=load_icon(self.icons["add"], 14), 
                      fg_color=THEME["header_bg"], hover_color=THEME["border_color"], text_color=THEME["accent_blue"], 
                      font=(FONT, 11, "bold"), corner_radius=8, height=28,
                      command=lambda: self.on_edit(None)).pack(side="left", padx=(0, 8))
        
        # NOUVEAU DESIGN : Le frame unifié pour la barre de recherche et les filtres
        search_filter_frame = ctk.CTkFrame(top_bar, fg_color=THEME["header_bg"], height=28, corner_radius=8, border_color=THEME["border_color"], border_width=1)
        search_filter_frame.pack(side="right")
        
        self.search_var = ctk.StringVar()
        self.search_entry = ctk.CTkEntry(search_filter_frame, textvariable=self.search_var, width=220, height=28, 
                                         placeholder_text="Rechercher...", fg_color=THEME["header_bg"], 
                                         border_width=0, text_color=THEME["primary_text"], font=(FONT, 11), 
                                         corner_radius=8)
        self.search_entry.pack(side="left", padx=(6, 0))
        self.search_entry.bind("<KeyRelease>", self.filter_view)

        # Le bouton de filtre est maintenant un bouton avec une icône dans le même frame
        filter_btn = ctk.CTkButton(search_filter_frame, text="", image=load_icon(self.icons["search"], 14), 
                      fg_color="transparent", hover_color=THEME["card_bg"], 
                      text_color=THEME["primary_text"], font=(FONT, 10, "bold"), width=30, 
                      corner_radius=6, height=26, command=self.refresh_view)
        filter_btn.pack(side="right", padx=2)

        self.card_container = ctk.CTkScrollableFrame(self, fg_color="transparent", corner_radius=10)
        self.card_container.pack(fill="both", expand=True, padx=15, pady=(0, 8))
        
        self.refresh_view()

    def refresh_view(self):
        for w in self.card_container.winfo_children(): w.destroy()
        
        search = self.search_var.get().lower().strip()
        all_classes = get_all_classes()
        
        filtered_classes = [c for c in all_classes if search in (c['nom'] or '').lower() or search in (c['niveau'] or '').lower() or search in (c['annee'] or '').lower()]
        
        order_map = {"1ère": 1, "TSM": 2}
        filtered_classes.sort(key=lambda classe: order_map.get(classe['nom'], float('inf')))
        
        profs = {p['id']: f"{p['nom']} {p['prenom']}" for p in get_all_professeurs()}
        salles = {s['id']: s['nom'] for s in get_all_salles()}

        num_columns = 3
        
        for idx, row in enumerate(filtered_classes):
            prof_name = profs.get(row['prof_id'], '—')
            salle_name = salles.get(row['salle_id'], '—')
            
            card = ClassCard(self.card_container, row, prof_name, salle_name, self.on_edit, self.on_delete, self.icons)
            card.grid(row=idx // num_columns, column=idx % num_columns, padx=6, pady=6, sticky="nsew")
        
        for i in range(num_columns):
            self.card_container.grid_columnconfigure(i, weight=1)

    def filter_view(self, event=None):
        self.refresh_view()

class ClassesManagerView(ctk.CTkFrame):
    def __init__(self, parent, icons):
        super().__init__(parent, fg_color=THEME["bg_main"])

        _required_icon_keys = {"add","edit","delete","search","export","import","pdf","reload","view"}
        _default_icons = {k: ICONS_PATH.get(k, "") for k in _required_icon_keys}
        incoming = icons or {}
        self.icons = {**_default_icons, **incoming}
        for k in _required_icon_keys:
            if k not in self.icons or not self.icons[k]:
                self.icons[k] = ""

        main_frame = ctk.CTkFrame(self, fg_color=THEME["card_bg"], corner_radius=12, border_color=THEME["border_color"], border_width=1)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        header = ctk.CTkFrame(main_frame, fg_color=THEME["header_bg"], height=40, corner_radius=10)
        header.pack(fill="x", padx=8, pady=8)
        
        title_frame = ctk.CTkFrame(header, fg_color="transparent")
        title_frame.pack(side="left", padx=(10, 0), pady=4)
        
        ctk.CTkLabel(title_frame, text="EduManager+", font=(FONT, 18, "bold"), 
                     text_color=THEME["primary_text"], fg_color="transparent").pack(anchor="w")
        ctk.CTkLabel(title_frame, text="Gestion des Classes", font=(FONT, 12, "bold"), 
                     text_color=THEME["accent_blue"], fg_color="transparent").pack(anchor="w", pady=(0, 1))
        
        self.statsbar = StatsBar(header, get_all_classes, get_all_professeurs)
        self.statsbar.pack(side="right", padx=(0, 10))
        
        main_content_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        main_content_frame.pack(fill="both", expand=True)

        self.notif_bar = NotificationBar(main_content_frame)
        self.notif_bar.pack(fill="x", padx=15, pady=(0, 4))
        
        self.card_view = ClassesCardView(main_content_frame, self.open_edit_modal, self.delete_classe, self.notif_bar, self.icons)
        self.card_view.pack(fill="both", expand=True)

        footer = ctk.CTkFrame(main_frame, fg_color=THEME["header_bg"], height=25, corner_radius=10)
        footer.pack(fill="x", padx=8, pady=(0, 8))
        ctk.CTkLabel(footer, text="EduManager+ • Gestion des classes sans photo – v4.1", 
                     font=(FONT, 8), text_color=THEME["secondary_text"], fg_color="transparent").pack(side="left", padx=10)

    def open_edit_modal(self, classe_id=None):
        popup = ctk.CTkToplevel(self)
        popup.title("Ajouter une Classe" if classe_id is None else "Modifier la Classe")
        popup.geometry("400x400")
        popup.resizable(False, False)
        popup.grab_set()
        popup.focus_force()
        popup.configure(fg_color=THEME["card_bg"])

        card = ctk.CTkFrame(popup, fg_color=THEME["card_bg"], corner_radius=10)
        card.pack(fill="both", expand=True, padx=12, pady=12)

        ctk.CTkLabel(card, text="Ajouter / Modifier une classe", font=(FONT, 14, "bold"), text_color=THEME["primary_text"], 
                     fg_color="transparent").pack(pady=(8, 4))
        
        form_frame = ctk.CTkFrame(card, fg_color="transparent")
        form_frame.pack(fill="x", padx=10, pady=4)

        fields = [
            ("Nom de la classe", "nom", "text"),
            ("Niveau scolaire", "niveau", "text"),
            ("Année scolaire", "annee", "text"),
            ("Professeur principal", "prof_id", "combo"),
            ("Salle de classe", "salle_id", "combo"),
        ]
        
        profs_list = get_all_professeurs()
        profs_map = {p['id']: f"{p['nom']} {p['prenom']}" for p in profs_list}
        profs_values = [" "] + list(profs_map.values())

        salles_list = get_all_salles()
        salles_map = {s['id']: f"{s['nom']}" for s in salles_list}
        salles_values = [" "] + list(salles_map.values())

        values_dict = {
            "prof_id": profs_values,
            "salle_id": salles_values,
        }
        
        data = {}
        if classe_id:
            row = get_classe_by_id(classe_id)
            if row:
                data = dict(row)

        entries = {}
        error_labels = {}
        
        for i, (label, key, ftype) in enumerate(fields):
            row_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
            row_frame.pack(fill="x", pady=2)
            
            ctk.CTkLabel(row_frame, text=label, font=(FONT, 10, "bold"), text_color=THEME["secondary_text"], 
                         fg_color="transparent", anchor="w", width=120).pack(side="left")
            
            if ftype == "text":
                ent = ctk.CTkEntry(row_frame, font=(FONT, 11), fg_color=THEME["header_bg"], 
                                   border_color=THEME["border_color"], text_color=THEME["primary_text"], 
                                   corner_radius=4, width=200, height=24)
                ent.pack(side="right", fill="x", expand=True)
                ent.insert(0, data.get(key, ""))
                entries[key] = ent
            else:
                combo = ctk.CTkComboBox(row_frame, values=values_dict[key], font=(FONT, 11), 
                                        fg_color=THEME["header_bg"], border_color=THEME["border_color"], 
                                        text_color=THEME["primary_text"], corner_radius=4, width=200, height=24)
                
                selected_value = ""
                if classe_id and data.get(key) is not None:
                    if key == "prof_id":
                        prof_id = data.get(key)
                        selected_value = profs_map.get(prof_id, " ")
                    elif key == "salle_id":
                        salle_id = data.get(key)
                        selected_value = salles_map.get(salle_id, " ")
                
                combo.set(selected_value or " ")
                combo.pack(side="right", fill="x", expand=True)
                entries[key] = combo

            error = ctk.CTkLabel(row_frame, text="", font=(FONT, 8, "italic"), text_color=THEME["error_red"], 
                                 fg_color="transparent", height=10)
            error.pack(side="bottom", anchor="e", fill="x", padx=(0, 4))
            error_labels[key] = error

        footer_frame = ctk.CTkFrame(card, fg_color="transparent")
        footer_frame.pack(fill="x", pady=(12, 4))
        
        def close_popup(): popup.destroy()
        
        cancel_btn = ctk.CTkButton(
            footer_frame, text="Annuler", font=(FONT, 11, "bold"),
            fg_color=THEME["header_bg"], text_color=THEME["primary_text"], hover_color=THEME["border_color"],
            corner_radius=6, command=close_popup, height=26
        )
        cancel_btn.pack(side="right", padx=2)
        
        save_btn = ctk.CTkButton(
            footer_frame, text="Valider", font=(FONT, 11, "bold"),
            fg_color=THEME["accent_blue"], text_color=THEME["bg_main"], hover_color=THEME["success_green"],
            corner_radius=6, height=26
        )
        save_btn.pack(side="right", padx=2)

        def validate_and_save():
            for e in error_labels.values(): e.configure(text="")
            
            nom = entries["nom"].get().strip()
            niveau = entries["niveau"].get().strip()
            annee = entries["annee"].get().strip()
            
            prof_str = entries["prof_id"].get()
            prof_id = next((k for k, v in profs_map.items() if v == prof_str), None)
            
            salle_str = entries["salle_id"].get()
            salle_id = next((k for k, v in salles_map.items() if v == salle_str), None)

            ok = True
            if not nom: error_labels["nom"].configure(text="Nom requis."); ok = False
            if not niveau: error_labels["niveau"].configure(text="Niveau requis."); ok = False
            if not annee: error_labels["annee"].configure(text="Année requise."); ok = False
            if not prof_id: error_labels["prof_id"].configure(text="Professeur requis."); ok = False
            if not salle_id: error_labels["salle_id"].configure(text="Salle requise."); ok = False
            
            if ok:
                if classe_id:
                    success = update_class_data(classe_id, nom, prof_id, salle_id, niveau, annee)
                    message_title = "Succès" if success else "Erreur"
                    message_text = "Classe modifiée." if success else "La modification a échoué."
                    messagebox.showinfo(message_title, message_text, parent=popup)
                else:
                    success = add_class(nom, prof_id, salle_id, niveau, annee)
                    message_title = "Succès" if success else "Erreur"
                    message_text = "Classe ajoutée." if success else "L'ajout a échoué."
                    messagebox.showinfo(message_title, message_text, parent=popup)
                
                if success:
                    popup.destroy()
                    self.card_view.refresh_view()
                    self.statsbar.refresh()

        save_btn.configure(command=validate_and_save)

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
                self.notif_bar.show("Classe et élèves supprimés avec succès.", THEME["success_green"])
                self.card_view.refresh_view()
                self.statsbar.refresh()
            else:
                self.notif_bar.show("Erreur lors de la suppression.", THEME["error_red"])

if __name__ == "__main__":
    setup_database()
    root = ctk.CTk()
    root.title("EduManager+ : Gestion des Classes")
    root.state('zoomed')
    root.minsize(900, 600)

    icons_to_load = {}
    for key, path in ICONS_PATH.items():
        icons_to_load[key] = path
    
    icons_to_load["add"] = r"C:\Users\Lenovo\Desktop\EduManager+\assets\icons\image_998b66.png"

    ClassesManagerView(root, icons_to_load).pack(fill="both", expand=True)
    root.mainloop()