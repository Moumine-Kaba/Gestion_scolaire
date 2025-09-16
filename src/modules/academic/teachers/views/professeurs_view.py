import customtkinter as ctk
from PIL import Image, ImageDraw, ImageFont, ImageOps
from tkinter import messagebox, filedialog
import os, sys
import csv
import sqlite3

# ============== Compat Pillow LANCZOS (Pillow ≥ 10) ==============
try:
    RESAMPLE_LANCZOS = Image.Resampling.LANCZOS
except AttributeError:
    RESAMPLE_LANCZOS = Image.LANCZOS

# ==================================================================== #
#                          IMPORTS THÈME ET ICÔNES                    #
# ==================================================================== #
# Import du thème existant
# Nous sommes dans src/modules/academic/teachers/views/
# Nous devons remonter de 4 niveaux pour atteindre la racine du projet
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..'))
sys.path.append(project_root)

try:
    from resources.themes.theme import (
        BG_MAIN, BG_SIDEBAR, CARD_BG, BORDER_COLOR, ACCENT, TEXT, MUTED,
        SUCCESS_GREEN, WARNING_YELLOW, ERROR_RED, INFO_ORANGE,
        FONT_PRIMARY, FONT_SECONDARY, FONT_TITLE, FONT_SUBTITLE, FONT_SMALL,
        FONT_BUTTON, FONT_CARD_TITLE, FONT_METRIC
    )
    # Mapping du thème pour compatibilité
    THEME = {
        "bg_main": BG_MAIN,
        "header_bg": BG_SIDEBAR,
        "card_bg": CARD_BG,
        "border_color": BORDER_COLOR,
        "accent_blue": ACCENT,
        "primary_text": TEXT,
        "secondary_text": MUTED,
        "error_red": ERROR_RED,
        "success_green": SUCCESS_GREEN,
        "warning_yellow": WARNING_YELLOW,
        "info_orange": INFO_ORANGE
    }
    FONT = FONT_PRIMARY[0]  # Utilise la police du thème
except ImportError:
    print("⚠️ Thème non trouvé, utilisation des valeurs par défaut")
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
        "info_orange": "#F97316"
    }
    FONT = "Segoe UI"

# Chemin de la base de données existante
# Utilisation des chemins absolus pour éviter les problèmes de résolution
DB_PATH = os.path.join(os.getcwd(), "database", "edumanager.db")
ICON_PATH_BASE = os.path.join(os.getcwd(), "resources", "icons")

# Mapping des icônes existantes
ICONS = {
    "add": os.path.join(ICON_PATH_BASE, "add.png"),
    "edit": os.path.join(ICON_PATH_BASE, "edit.png"),
    "delete": os.path.join(ICON_PATH_BASE, "delete.png"),
    "search": os.path.join(ICON_PATH_BASE, "search.png"),
    "export": os.path.join(ICON_PATH_BASE, "csv.png"),
    "professors": os.path.join(ICON_PATH_BASE, "group.png"),
    "person": os.path.join(ICON_PATH_BASE, "person.png"),
    "award": os.path.join(ICON_PATH_BASE, "award.png"),
    "detail": os.path.join(ICON_PATH_BASE, "detail.png"),
    "calendar": os.path.join(ICON_PATH_BASE, "calendar.png"),
    "phone": os.path.join(ICON_PATH_BASE, "phone.png"),
    "email": os.path.join(ICON_PATH_BASE, "email.png"),
}

# ==================================================================== #
#                          IMPORTS CONTROLLERS                         #
# ==================================================================== #

try:
    from utils.validators import is_name, is_phone, is_email, is_date
    from controllers.professeur_controller import (
        get_all_professeurs, add_professeur, update_professeur, delete_professeur, get_professeur
    )
except ImportError:
    print("WARNING: Le module 'utils.validators' ou 'controllers.professeur_controller' n'a pas été trouvé. Utilisation de stubs.")
    def is_name(s): return isinstance(s, str) and len(s) > 1
    def is_phone(s): return isinstance(s, str) and s.isdigit() and len(s) > 5
    def is_email(s): return isinstance(s, str) and "@" in s
    def is_date(s): return isinstance(s, str) and len(s) == 10 and s[4] == '-' and s[7] == '-'
    
    def get_db_connection():
        try:
            conn = sqlite3.connect(DB_PATH)
            conn.row_factory = sqlite3.Row
            return conn
        except sqlite3.Error as e:
            print(f"Erreur de connexion à la base de données: {e}")
            return None

    def get_all_professeurs():
        conn = get_db_connection()
        if not conn: return []
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM professeurs")
        profs = cursor.fetchall()
        conn.close()
        # Convertir les données pour correspondre à la structure attendue
        converted_profs = []
        for prof in profs:
            prof_dict = dict(prof)
            # Mapping des champs de la base vers les champs attendus
            converted_prof = {
                'id': prof_dict.get('id_professeur'),
                'matricule': prof_dict.get('matricule', ''),
                'nom': prof_dict.get('nom', ''),
                'prenom': prof_dict.get('prenom', ''),
                'sexe': prof_dict.get('genre', ''),
                'telephone': prof_dict.get('telephone', ''),
                'email': prof_dict.get('email', ''),
                'specialite': prof_dict.get('specialite', ''),
                'date_embauche': prof_dict.get('date_embauche', ''),
                'adresse': prof_dict.get('adresse', ''),
                'date_naissance': prof_dict.get('date_naissance', ''),
                'statut': prof_dict.get('statut', ''),
                'photo_path': ''  # Pas de photo dans la structure actuelle
            }
            converted_profs.append(converted_prof)
        return converted_profs

    def add_professeur(data):
        """Ajoute un nouveau professeur à la base de données"""
        conn = get_db_connection()
        if not conn: return False
        try:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO professeurs (matricule, nom, prenom, date_naissance, genre, 
                                       adresse, telephone, email, specialite, date_embauche, statut)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                data.get('matricule', ''),
                data.get('nom', ''),
                data.get('prenom', ''),
                data.get('date_naissance', ''),
                data.get('sexe', ''),
                data.get('adresse', ''),
                data.get('telephone', ''),
                data.get('email', ''),
                data.get('specialite', ''),
                data.get('date_embauche', ''),
                data.get('statut', 'Actif')
            ))
            conn.commit()
            return True
        except Exception as e:
            print(f"Erreur lors de l'ajout: {e}")
            return False
        finally:
            conn.close()

    def update_professeur(prof_id, data):
        """Met à jour un professeur existant"""
        conn = get_db_connection()
        if not conn: return False
        try:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE professeurs SET 
                    matricule=?, nom=?, prenom=?, date_naissance=?, genre=?,
                    adresse=?, telephone=?, email=?, specialite=?, date_embauche=?, statut=?
                WHERE id_professeur=?
            """, (
                data.get('matricule', ''),
                data.get('nom', ''),
                data.get('prenom', ''),
                data.get('date_naissance', ''),
                data.get('sexe', ''),
                data.get('adresse', ''),
                data.get('telephone', ''),
                data.get('email', ''),
                data.get('specialite', ''),
                data.get('date_embauche', ''),
                data.get('statut', 'Actif'),
                prof_id
            ))
            conn.commit()
            return True
        except Exception as e:
            print(f"Erreur lors de la mise à jour: {e}")
            return False
        finally:
            conn.close()

    def delete_professeur(prof_id):
        """Supprime un professeur de la base de données"""
        conn = get_db_connection()
        if not conn: return False
        try:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM professeurs WHERE id_professeur=?", (prof_id,))
            conn.commit()
            return True
        except Exception as e:
            print(f"Erreur lors de la suppression: {e}")
            return False
        finally:
            conn.close()

    def get_professeur(prof_id):
        conn = get_db_connection()
        if not conn: return None
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM professeurs WHERE id_professeur=?", (prof_id,))
        prof = cursor.fetchone()
        conn.close()
        if prof:
            prof_dict = dict(prof)
            # Mapping des champs de la base vers les champs attendus
            return {
                'id': prof_dict.get('id_professeur'),
                'matricule': prof_dict.get('matricule', ''),
                'nom': prof_dict.get('nom', ''),
                'prenom': prof_dict.get('prenom', ''),
                'sexe': prof_dict.get('genre', ''),
                'telephone': prof_dict.get('telephone', ''),
                'email': prof_dict.get('email', ''),
                'specialite': prof_dict.get('specialite', ''),
                'date_embauche': prof_dict.get('date_embauche', ''),
                'adresse': prof_dict.get('adresse', ''),
                'date_naissance': prof_dict.get('date_naissance', ''),
                'statut': prof_dict.get('statut', ''),
                'photo_path': ''  # Pas de photo dans la structure actuelle
            }
        return None

# ==================================================================== #
#                          FONCTIONS UTILITAIRES                       #
# ==================================================================== #

def load_ctk_image(path_or_img, size=32, fallback_text=""):
    """
    Charge une image pour customtkinter.
    - Accepte un chemin de fichier OU un CTkImage déjà prêt (dans ce cas, on le retourne tel quel).
    - Génère un fallback lisible en cas d'erreur.
    """
    if isinstance(path_or_img, ctk.CTkImage):
        return path_or_img

    try:
        path = str(path_or_img)
        if not os.path.isfile(path):
            raise FileNotFoundError(f"Fichier d'icône non trouvé : {path}")
        img = Image.open(path).convert("RGBA").resize((size, size), RESAMPLE_LANCZOS)
        return ctk.CTkImage(img, size=(size, size))
    except Exception as e:
        print(f"Erreur de chargement de l'icône {path_or_img}: {e}")
        fallback_img = Image.new("RGBA", (size, size), (60, 60, 60, 0))
        draw = ImageDraw.Draw(fallback_img)
        try:
            font = ImageFont.truetype("arial.ttf", size // 2)
        except:
            font = ImageFont.load_default()
        draw.text((size // 4, size // 4), fallback_text or "?", fill=THEME["primary_text"], font=font)
        return ctk.CTkImage(fallback_img, size=(size, size))

def square_photo(path, size=(130, 130)):
    """Charge et ajuste une photo de profil ou crée une image de remplacement."""
    try:
        if path and os.path.isfile(path):
            img = Image.open(path)
            img = ImageOps.fit(img, size, RESAMPLE_LANCZOS)
        else:
            img = Image.new("RGB", size, THEME["header_bg"])
            draw = ImageDraw.Draw(img)
            try:
                font = ImageFont.truetype("arial.ttf", 22)
            except:
                font = ImageFont.load_default()
            text = "No\nPhoto"
            bbox = draw.textbbox((0, 0), text, font=font)
            tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
            draw.text(((size[0] - tw) // 2, (size[1] - th) // 2), text, fill=THEME["secondary_text"], font=font)
        return ctk.CTkImage(img, size=size)
    except Exception as e:
        print(f"Erreur de chargement de la photo {path}: {e}")
        return ctk.CTkImage(Image.new("RGB", size, THEME["header_bg"]), size=size)


# ==================================================================== #
#                          VUE DASHBOARD PROFESSEURS                   #
# ==================================================================== #

class ProfessorsDashboard(ctk.CTkFrame):
    def __init__(self, parent, icons=None):
        super().__init__(parent, fg_color=THEME["bg_main"], corner_radius=0)
        self.parent = parent
        self.icon_cache = {}
        source_keys = set(ICONS.keys()) | (set(icons.keys()) if isinstance(icons, dict) else set())
        for k in source_keys:
            candidate = None
            if isinstance(icons, dict) and k in icons:
                candidate = icons[k]
            default_path = ICONS.get(k)
            img = None
            if candidate is not None:
                img = load_ctk_image(candidate, 24)
            if img is None and default_path:
                img = load_ctk_image(default_path, 24)
            if img is None:
                img = load_ctk_image("???", 24, fallback_text=k[:1].upper())
            self.icon_cache[k] = img

        self._create_widgets()
        self.update_data()
        
    def _create_widgets(self):
        """Crée l'ensemble des widgets du tableau de bord."""
        header = ctk.CTkFrame(self, fg_color=THEME["header_bg"], height=50, corner_radius=10)
        header.pack(fill="x", padx=10, pady=10)
        header.pack_propagate(False)
        ctk.CTkLabel(header, text="Gestion des Professeurs", font=(FONT, 20, "bold"),
                     text_color=THEME["accent_blue"], fg_color="transparent").pack(side="left", padx=15)
        ctk.CTkButton(header, text="Ajouter", image=self.icon_cache.get("add"), compound="left",
                      font=(FONT, 12, "bold"), fg_color=THEME["accent_blue"], text_color=THEME["bg_main"],
                      hover_color="#9FE8FF", corner_radius=8, height=30,
                      command=self.add_professor).pack(side="right", padx=15)

        stats_frame = ctk.CTkFrame(self, fg_color=THEME["bg_main"])
        stats_frame.pack(fill="x", padx=10, pady=5)
        self.stat_cards = []
        stats_def = [
            ("Total", "professors", THEME["accent_blue"]),
            ("Hommes", "person", "#2563eb"),
            ("Femmes", "person", "#be185d"),
            ("Spécialités", "award", "#20e3b2"),
        ]
        for i, (label, icon, color) in enumerate(stats_def):
            card_frame, value_label = self._stat_card(stats_frame, label, icon, color)
            card_frame.pack(side="left", fill="x", expand=True, padx=(0, 10) if i<3 else 0)
            self.stat_cards.append(value_label)

        action_bar = ctk.CTkFrame(self, fg_color=THEME["header_bg"], corner_radius=10)
        action_bar.pack(fill="x", padx=10, pady=5)

        btns = [
            ("Exporter", "export", "#64748b", self.export_to_csv),
            ("Détails", "detail", THEME["accent_blue"], self.show_details),
            ("Modifier", "edit", "#38bdf8", self.edit_professor),
            ("Supprimer", "delete", THEME["error_red"], self.delete_professor),
        ]
        for txt, icn, color, cmd in reversed(btns):
            ctk.CTkButton(action_bar, text=txt, image=self.icon_cache.get(icn), compound="left",
                          font=(FONT, 10, "bold"), fg_color=color,
                          text_color=THEME["bg_main"] if color == THEME["accent_blue"] else THEME["primary_text"],
                          hover_color="#415A77", corner_radius=8, command=cmd, height=28
            ).pack(side="right", padx=4, pady=8)

        search_frame = ctk.CTkFrame(action_bar, fg_color=THEME["card_bg"], corner_radius=8, 
                                   border_width=2, border_color="#4A5568")
        search_frame.pack(side="left", padx=(10, 0), pady=8, ipadx=2, ipady=2)
        self.search_var = ctk.StringVar()
        search_entry = ctk.CTkEntry(search_frame, textvariable=self.search_var, font=(FONT, 11),
                                    placeholder_text="Rechercher...", fg_color=THEME["card_bg"],
                                    text_color=THEME["primary_text"], border_width=1, 
                                    border_color="#4A5568", corner_radius=6, width=200)
        search_entry.pack(side="left", ipady=4, padx=(0,4))
        search_entry.bind("<KeyRelease>", self.filter_professors)
        ctk.CTkLabel(search_frame, image=self.icon_cache.get("search"), text="", fg_color="transparent").pack(side="left", padx=2)
        
        self.table_view = TeacherTable(self, self.update_data)
        self.table_view.pack(fill="both", expand=True, padx=10, pady=(0, 10))

    def _stat_card(self, parent, label, icon_key, color):
        """Crée une carte de statistique individuelle."""
        card = ctk.CTkFrame(parent, fg_color=THEME["card_bg"], corner_radius=10, border_color=color, border_width=1)
        ic_bg = ctk.CTkFrame(card, fg_color=color, width=40, height=40, corner_radius=8)
        ic_bg.pack(side="left", padx=10, pady=8)
        ic_bg.pack_propagate(False)
        icn = load_ctk_image(ICONS.get(icon_key), 20)
        ctk.CTkLabel(ic_bg, image=icn, text="", fg_color="transparent").pack(expand=True)
        
        text_frame = ctk.CTkFrame(card, fg_color=THEME["card_bg"])
        text_frame.pack(side="left", fill="y", padx=(5, 10))
        ctk.CTkLabel(text_frame, text=label, font=(FONT, 10, "bold"), text_color=THEME["secondary_text"]).pack(anchor="w", pady=(8, 0))
        value_label = ctk.CTkLabel(text_frame, text="0", font=(FONT, 20, "bold"), text_color=color)
        value_label.pack(anchor="w", pady=(0, 8))
        return card, value_label

    def update_data(self):
        """Met à jour les données affichées dans les cartes et le tableau."""
        all_profs = get_all_professeurs()
        total = len(all_profs)
        men = len([p for p in all_profs if str(p.get('sexe', '')).lower().startswith("h")])
        women = len([p for p in all_profs if str(p.get('sexe', '')).lower().startswith("f")])
        specialties = len(set(p.get('specialite', '') for p in all_profs if p.get('specialite', '')))
        stats = [total, men, women, specialties]
        for i, val in enumerate(stats):
            self.stat_cards[i].configure(text=str(val))
        self.table_view.update_table(all_profs)

    def filter_professors(self, event=None):
        """Filtre les professeurs affichés en fonction du terme de recherche."""
        term = self.search_var.get().strip().lower()
        self.table_view.filter_table(term)

    def add_professor(self):
        """Ouvre le formulaire pour ajouter un nouveau professeur."""
        TeacherForm(self.parent, self.update_data, mode="Ajouter")

    def edit_professor(self):
        """Ouvre le formulaire pour modifier le professeur sélectionné."""
        selected_prof_id = self.table_view.get_selected_professor_id()
        if selected_prof_id:
            prof_data = get_professeur(selected_prof_id)
            if prof_data:
                TeacherForm(self.parent, self.update_data, mode="Modifier", data=prof_data)
        else:
            messagebox.showinfo("Modifier", "Sélectionnez un professeur à modifier.")

    def delete_professor(self):
        """Supprime le professeur sélectionné après confirmation."""
        selected_prof_id = self.table_view.get_selected_professor_id()
        if not selected_prof_id:
            messagebox.showinfo("Supprimer", "Sélectionnez un professeur à supprimer.")
            return
        prof_data = get_professeur(selected_prof_id)
        if prof_data:
            confirm = messagebox.askyesno("Suppression", f"Voulez-vous vraiment supprimer {prof_data['prenom']} {prof_data['nom']} ?")
            if confirm:
                delete_professeur(selected_prof_id)
                self.update_data()
                messagebox.showinfo("Succès", "Professeur supprimé avec succès.")
        else:
            messagebox.showerror("Erreur", "Professeur non trouvé.")

    def show_details(self):
        """Affiche la carte détaillée du professeur sélectionné."""
        selected_prof_id = self.table_view.get_selected_professor_id()
        if not selected_prof_id:
            messagebox.showinfo("Détails", "Sélectionnez un professeur pour voir les détails.")
            return
        prof_data = get_professeur(selected_prof_id)
        if prof_data:
            ProfessorDetailsFullImageCardView(self.parent, prof_data)
        else:
            messagebox.showerror("Erreur", "Professeur non trouvé.")

    def export_to_csv(self):
        """Exporte les données des professeurs vers un fichier CSV."""
        profs_to_export = get_all_professeurs()
        if not profs_to_export:
            messagebox.showinfo("Export", "Aucune donnée à exporter.")
            return
        path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV", "*.csv")], title="Exporter les professeurs")
        if not path: return
        headers = ["ID", "Matricule", "Nom", "Prénom", "Date de naissance", "Sexe", "Adresse", 
                  "Téléphone", "Email", "Spécialité", "Date d'embauche", "Statut"]
        with open(path, "w", newline='', encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(headers)
            for row in profs_to_export:
                writer.writerow([
                    row.get('id', ''), row.get('matricule', ''), row.get('nom', ''), row.get('prenom', ''),
                    row.get('date_naissance', ''), row.get('sexe', ''), row.get('adresse', ''),
                    row.get('telephone', ''), row.get('email', ''), row.get('specialite', ''),
                    row.get('date_embauche', ''), row.get('statut', '')
                ])
        messagebox.showinfo("Export", "Export CSV réussi !")

# ==================================================================== #
#                          TABLEAU DES PROFESSEURS                     #
# ==================================================================== #

class TeacherTable(ctk.CTkFrame):
    def __init__(self, parent, data_updater):
        super().__init__(parent, fg_color=THEME["card_bg"], corner_radius=10)
        self.all_profs = []
        self.filtered_profs = []
        self.data_updater = data_updater
        self.selected_row_id = None
        self._create_table_widgets()
        
    def _create_table_widgets(self):
        """Crée un tableau unifié avec en-tête et contenu intégrés."""
        # Conteneur principal avec contours subtils
        main_container = ctk.CTkFrame(self, fg_color="transparent", corner_radius=16, 
                                     border_width=1, border_color="#4A5568")
        main_container.pack(fill="both", expand=True, padx=8, pady=8)
        
        # En-tête des colonnes avec contours subtils
        header_frame = ctk.CTkFrame(main_container, fg_color="transparent", corner_radius=12, 
                                   border_width=1, border_color="#4A5568")
        header_frame.pack(fill="x", padx=20, pady=(20, 15))
        
        columns = [
            ("Matricule", 100), ("Nom", 130), ("Prénom", 130),
            ("Sexe", 90), ("Spécialité", 150), ("Email", 200), ("Téléphone", 130)
        ]
        
        for i, (text, width) in enumerate(columns):
            col_frame = ctk.CTkFrame(header_frame, fg_color="transparent", width=width, height=45)
            col_frame.pack(side="left", padx=2, pady=8)
            col_frame.pack_propagate(False)
            
            ctk.CTkLabel(col_frame, text=text, font=(FONT, 13, "bold"), 
                         text_color="#00FF41", fg_color="transparent").pack(expand=True)
        
        # Corps du tableau transparent
        self.table_body = ctk.CTkScrollableFrame(main_container, fg_color="transparent", corner_radius=0)
        self.table_body.pack(fill="both", expand=True, padx=20, pady=(0, 20))

    def update_table(self, professors):
        """Met à jour les données du tableau et gère la sélection."""
        self.all_profs = professors
        self.filter_table()

    def filter_table(self, search_term=""):
        """Filtre les lignes du tableau en fonction du terme de recherche."""
        for widget in self.table_body.winfo_children():
            widget.destroy()
        
        if not search_term:
            self.filtered_profs = self.all_profs
        else:
            st = search_term.lower()
            self.filtered_profs = [
                p for p in self.all_profs
                if any(st in str(value).lower() for value in p.values() if value is not None)
            ]

        for i, data in enumerate(self.filtered_profs):
            # Lignes avec contours subtils
            row_frame = ctk.CTkFrame(self.table_body, fg_color="transparent", corner_radius=8, 
                                   height=50, border_width=1, border_color="#4A5568")
            row_frame.pack(fill="x", pady=3, padx=0)
            row_frame.pack_propagate(False)
            
            row_values = (
                data.get('matricule', ''), data.get('nom', ''), data.get('prenom', ''),
                data.get('sexe', ''), data.get('specialite', ''), data.get('email', ''),
                data.get('telephone', '')
            )
            widths = [100, 130, 130, 90, 150, 200, 130]

            def on_select(prof_id):
                self.selected_row_id = prof_id
                for widget in self.table_body.winfo_children():
                    if hasattr(widget, 'prof_id'):
                        is_selected = widget.prof_id == prof_id
                        widget.configure(
                            fg_color="#31487b" if is_selected else widget.original_color,
                            border_color=THEME["accent_blue"] if is_selected else widget.original_color,
                            border_width=2 if is_selected else 0
                        )

            row_frame.prof_id = data.get('id', None)
            row_frame.original_color = "transparent"
            row_frame.bind("<Button-1>", lambda e, pid=data.get('id'): on_select(pid))

            for j, val in enumerate(row_values):
                # Couleurs néon et gris pour chaque champ
                text_color = "#FFFFFF"  # Blanc par défaut
                
                # Couleurs néon spéciales pour certains champs
                if j == 0:  # Matricule
                    text_color = "#00FF41"  # Vert néon
                elif j == 1:  # Nom
                    text_color = "#FFFFFF"  # Blanc pur
                elif j == 2:  # Prénom
                    text_color = "#FFFFFF"  # Blanc pur
                elif j == 3:  # Sexe
                    if str(val).lower() == "homme":
                        text_color = "#00BFFF"  # Bleu néon
                    elif str(val).lower() == "femme":
                        text_color = "#FF1493"  # Rose néon
                elif j == 4:  # Spécialité
                    text_color = "#FFD700"  # Jaune néon
                elif j == 5:  # Email
                    text_color = "#FF00FF"  # Magenta néon
                elif j == 6:  # Téléphone
                    text_color = "#00FFFF"  # Cyan néon
                
                # Texte avec style néon
                display_text = str(val)
                
                lbl = ctk.CTkLabel(row_frame, text=display_text, font=(FONT, 12), text_color=text_color,
                                    width=widths[j], fg_color="transparent", anchor="center")
                lbl.pack(side="left", padx=2)
                lbl.bind("<Button-1>", lambda e, pid=data.get('id'): on_select(pid))

            # Effet de survol transparent
            def on_hover_enter(event, frame=row_frame):
                if frame.prof_id != self.selected_row_id:
                    frame.configure(fg_color="#404040")
            
            def on_hover_leave(event, frame=row_frame):
                if frame.prof_id != self.selected_row_id:
                    frame.configure(fg_color="transparent")
            
            row_frame.bind("<Enter>", on_hover_enter)
            row_frame.bind("<Leave>", on_hover_leave)
            
            if self.selected_row_id == data.get('id', None):
                row_frame.configure(fg_color="#555555")
        
        # Message si aucun résultat
        count = len(self.filtered_profs)
        if count == 0:
            no_results_frame = ctk.CTkFrame(self.table_body, fg_color="transparent")
            no_results_frame.pack(expand=True, fill="both", pady=50)
            
            ctk.CTkLabel(no_results_frame, text="🔍", font=(FONT, 48), 
                         text_color=THEME["secondary_text"], fg_color="transparent").pack(pady=(0, 10))
            
            ctk.CTkLabel(no_results_frame, text="Aucun professeur trouvé", font=(FONT, 16, "bold"), 
                         text_color=THEME["secondary_text"], fg_color="transparent").pack(pady=(0, 5))
            
            ctk.CTkLabel(no_results_frame, text="Essayez de modifier votre recherche", font=(FONT, 12), 
                         text_color=THEME["secondary_text"], fg_color="transparent").pack()

    def get_selected_professor_id(self):
        """Retourne l'ID du professeur sélectionné."""
        return self.selected_row_id

# ==================================================================== #
#                          MODALE DETAIL PROFESSEUR                    #
# ==================================================================== #

class ProfessorDetailsFullImageCardView(ctk.CTkToplevel):
    def __init__(self, parent, professor_data):
        super().__init__(parent)
        self.parent = parent
        self.professor_data = professor_data
        self.title(f"Détails - {self.professor_data.get('prenom', '')} {self.professor_data.get('nom', '')}")
        self.geometry("450x650")
        self.minsize(350, 400)
        self.configure(fg_color=THEME["bg_main"])
        self.transient(self.parent)
        self.grab_set()
        self.icon_cache = {k: load_ctk_image(v, 20) for k, v in ICONS.items()}
        self._create_widgets()

    def _create_widgets(self):
        """Crée les widgets de la vue détaillée."""
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        CARD_W = 450
        photo_size = CARD_W
        photo_path = self.professor_data.get('photo_path', '')
        
        try:
            if photo_path and os.path.isfile(photo_path):
                img = Image.open(photo_path)
                img = ImageOps.fit(img, (photo_size, photo_size), RESAMPLE_LANCZOS, centering=(0.5, 0.4))
            else:
                img = Image.new("RGB", (photo_size, photo_size), THEME["header_bg"])
                draw = ImageDraw.Draw(img)
                try:
                    font = ImageFont.truetype("arial.ttf", 25)
                except:
                    font = ImageFont.load_default()
                text = "No Photo"
                bbox = draw.textbbox((0, 0), text, font=font)
                tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
                draw.text(((photo_size - tw) // 2, (photo_size - th) // 2), text, fill=THEME["secondary_text"], font=font)
            photo_image = ctk.CTkImage(img, size=(photo_size, photo_size))
        except Exception:
            photo_image = ctk.CTkImage(Image.new("RGB", (photo_size, photo_size), THEME["header_bg"]), size=(photo_size, photo_size))

        photo_label = ctk.CTkLabel(self, image=photo_image, text="", fg_color="transparent", width=photo_size, height=photo_size)
        photo_label.grid(row=0, column=0, sticky="nsew")

        details_frame = ctk.CTkScrollableFrame(self, fg_color=THEME["bg_main"], corner_radius=0)
        details_frame.grid(row=1, column=0, sticky="nsew")
        details_frame.grid_columnconfigure(0, weight=1)

        nom_prenom = f"{self.professor_data.get('prenom', '').title()} {self.professor_data.get('nom', '').upper()}"
        ctk.CTkLabel(details_frame, text=nom_prenom, font=(FONT, 18, "bold"), text_color=THEME["primary_text"]).pack(pady=(10, 2))
        
        specialite = self.professor_data.get('specialite', 'N/A')
        spec_box = ctk.CTkFrame(details_frame, fg_color=THEME["header_bg"], corner_radius=5)
        spec_box.pack(pady=(0, 8))
        ctk.CTkLabel(spec_box, image=self.icon_cache["award"], text="", fg_color="transparent").pack(side="left", padx=(8,2))
        ctk.CTkLabel(spec_box, text=specialite, font=(FONT, 11, "bold"), text_color=THEME["accent_blue"]).pack(side="left", padx=(2, 8))
        
        ctk.CTkFrame(details_frame, height=1, fg_color=THEME["accent_blue"], corner_radius=1).pack(fill="x", padx=20, pady=(2, 8))
        
        infos = [
            ("ID", self.professor_data.get("id", "N/A"), "person"),
            ("Matricule", self.professor_data.get("matricule", "N/A"), "person"),
            ("Date de naissance", self.professor_data.get("date_naissance", "N/A"), "calendar"),
            ("Sexe", self.professor_data.get("sexe", "N/A"), "person"),
            ("Adresse", self.professor_data.get("adresse", "N/A"), "person"),
            ("Téléphone", self.professor_data.get("telephone", "N/A"), "phone"),
            ("Email", self.professor_data.get("email", "N/A"), "email"),
            ("Date d'embauche", self.professor_data.get("date_embauche", "N/A"), "calendar"),
            ("Statut", self.professor_data.get("statut", "N/A"), "person"),
        ]
        
        for label, value, icon_key in infos:
            line = ctk.CTkFrame(details_frame, fg_color=THEME["header_bg"], corner_radius=5)
            line.pack(fill="x", padx=15, pady=5)
            ctk.CTkLabel(line, image=self.icon_cache[icon_key], text="", fg_color="transparent").pack(side="left", padx=(8,6))
            ctk.CTkLabel(line, text=f"{label} :", font=(FONT, 10, "bold"), text_color=THEME["secondary_text"]).pack(side="left")
            ctk.CTkLabel(line, text=value, font=(FONT, 10), text_color=THEME["primary_text"], wraplength=280,
                         anchor="w", justify="left").pack(side="left", padx=(6, 0), fill="x", expand=True)
                             
        ctk.CTkButton(details_frame, text="IMPRIMER LA CARTE", font=(FONT, 11, "bold"),
                      fg_color=THEME["info_orange"], text_color=THEME["bg_main"], hover_color="#d97706",
                      corner_radius=8, command=lambda: messagebox.showinfo("Action", "Fonction d'impression à venir.")
        ).pack(pady=15, fill="x", padx=25)

# ==================================================================== #
#                          FORMULAIRE PROFESSEUR                       #
# ==================================================================== #

class TeacherForm(ctk.CTkToplevel):
    def __init__(self, parent, data_updater, mode="Ajouter", data=None):
        super().__init__(parent)
        self.parent = parent
        self.data_updater = data_updater
        self.data = data or {}
        self.mode = mode
        self.title(f"{mode} un professeur")
        self.geometry("700x480")
        self.minsize(600, 400)
        self.configure(fg_color=THEME["bg_main"])
        self.grab_set()
        self.photo_path = self.data.get('photo_path', "")

        # Layout principal
        root = ctk.CTkFrame(self, fg_color=THEME["bg_main"])
        root.pack(fill="both", expand=True)
        left = ctk.CTkFrame(root, fg_color=THEME["header_bg"], width=200)
        left.pack(side="left", fill="y")
        left.pack_propagate(False)
        right = ctk.CTkFrame(root, fg_color=THEME["bg_main"])
        right.pack(side="left", fill="both", expand=True)
        
        # Photo & onglets
        ctk.CTkLabel(left, text="Photo", font=(FONT, 10, "bold"), text_color=THEME["secondary_text"]).pack(pady=(20, 0))
        img_frame = ctk.CTkFrame(left, fg_color=THEME["card_bg"], width=100, height=100, corner_radius=8, border_color=THEME["accent_blue"], border_width=1)
        img_frame.pack(pady=5)
        img_frame.pack_propagate(False)
        img = square_photo(self.photo_path, size=(100, 100))
        self.photo_widget = ctk.CTkLabel(img_frame, image=img, text="", fg_color="transparent")
        self.photo_widget.pack(expand=True)
        
        btns = ctk.CTkFrame(left, fg_color="transparent")
        btns.pack(pady=(2, 10))
        ctk.CTkButton(btns, text="Changer", font=(FONT, 9, "bold"), fg_color=THEME["accent_blue"],
                      text_color=THEME["bg_main"], corner_radius=5, command=self.upload_photo, height=20).pack(fill="x", padx=8, pady=(0,2))
        ctk.CTkButton(btns, text="Retirer", font=(FONT, 9), fg_color=THEME["border_color"], text_color=THEME["primary_text"],
                      corner_radius=5, command=self.clear_photo, height=20).pack(fill="x", padx=8)
        
        # Onglets navigation
        nav_items = [("infos", "Informations"), ("contact", "Contact")]
        self.sections = {}
        self.tab_buttons = {}
        self.current_tab = ctk.StringVar(value="infos")
        for key, label in nav_items:
            btn = ctk.CTkButton(left, text=label, fg_color=(THEME["accent_blue"] if key == "infos" else THEME["header_bg"]),
                                 text_color=THEME["bg_main"] if key == "infos" else THEME["primary_text"],
                                 font=(FONT, 11, "bold"), hover_color=THEME["accent_blue"], corner_radius=0,
                                 command=lambda t=key: self.switch_tab(t))
            btn.pack(fill="x", padx=0, pady=(1, 0), ipady=8)
            self.tab_buttons[key] = btn

        self.sections["infos"] = ctk.CTkScrollableFrame(right, fg_color=THEME["bg_main"])
        self.sections["contact"] = ctk.CTkScrollableFrame(right, fg_color=THEME["bg_main"])

        # Champs
        self.fields_config = {
            "infos": [
                ("Matricule", "matricule", "entry", True, None),
                ("Nom", "nom", "entry", True, is_name),
                ("Prénom", "prenom", "entry", True, is_name),
                ("Date de naissance (AAAA-MM-JJ)", "date_naissance", "entry", False, is_date),
                ("Sexe", "sexe", "combo", True, None, ["Homme", "Femme"]),
                ("Spécialité", "specialite", "entry", True, None),
                ("Date d'embauche (AAAA-MM-JJ)", "date_embauche", "entry", True, is_date),
                ("Statut", "statut", "combo", True, None, ["Actif", "Inactif", "Retraité"]),
            ],
            "contact": [
                ("Adresse", "adresse", "entry", False, None),
                ("Téléphone", "telephone", "entry", False, is_phone),
                ("Email", "email", "entry", False, is_email),
            ],
        }
        self.widgets = {}
        self.err_labels = {}

        for section_key in self.fields_config:
            self.build_section(section_key)

        # Bouton d'action
        save_btn_text = "Enregistrer les modifications" if self.mode == "Modifier" else "Ajouter le professeur"
        ctk.CTkButton(right, text=save_btn_text, font=(FONT, 12, "bold"),
                      fg_color=THEME["accent_blue"], text_color=THEME["bg_main"], hover_color="#9FE8FF",
                      corner_radius=8, command=self.save_professor).pack(fill="x", padx=10, pady=(10, 10))
        
        self.switch_tab("infos")

    def build_section(self, section_key):
        """Crée les widgets pour une section (onglet) spécifique."""
        frame = self.sections[section_key]
        for spec in self.fields_config[section_key]:
            label, key, wtype, required, validator, *options = spec
            value = self.data.get(key, '')
            
            row = ctk.CTkFrame(frame, fg_color=THEME["bg_main"])
            row.pack(fill="x", padx=10, pady=2)
            
            ctk.CTkLabel(row, text=f"{label}{' *' if required else ''}", font=(FONT, 11, "bold"), text_color=THEME["secondary_text"]).pack(anchor="w", pady=(0, 1))
            
            if wtype == "combo":
                w = ctk.CTkComboBox(row, values=options[0], state="readonly", font=(FONT, 11),
                                    fg_color=THEME["card_bg"], text_color=THEME["primary_text"],
                                    border_color=THEME["border_color"], button_color=THEME["accent_blue"],
                                    corner_radius=6, border_width=1, height=30)
                if value:
                    w.set(value.capitalize())
                else:
                    w.set("Choisir...")
            else:
                w = ctk.CTkEntry(row, font=(FONT, 11), fg_color=THEME["card_bg"], text_color=THEME["primary_text"],
                                 border_color=THEME["border_color"], corner_radius=6, border_width=1, height=30)
                w.insert(0, value)

            w.pack(fill="x", pady=(0, 1))
            
            error_lbl = ctk.CTkLabel(row, text="", font=(FONT, 9), text_color=THEME["error_red"])
            error_lbl.pack(anchor="w")
            
            self.widgets[key] = w
            self.err_labels[key] = error_lbl

            if validator:
                w.bind("<FocusOut>", lambda event, k=key, v=validator, r=required: self.validate_field(k, v, r))

    def switch_tab(self, tab_key):
        """Change d'onglet dans le formulaire."""
        for key, btn in self.tab_buttons.items():
            is_active = (key == tab_key)
            fg_color = THEME["accent_blue"] if is_active else THEME["header_bg"]
            text_color = THEME["bg_main"] if is_active else THEME["primary_text"]
            btn.configure(fg_color=fg_color, text_color=text_color)
            if key in self.sections:
                self.sections[key].pack_forget()
        
        if tab_key in self.sections:
            self.sections[tab_key].pack(fill="both", expand=True)

    def upload_photo(self):
        """Ouvre une boîte de dialogue pour sélectionner une photo de profil."""
        path = filedialog.askopenfilename(
            title="Sélectionner une photo",
            filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.webp")]
        )
        if path:
            self.photo_path = path
            img = square_photo(self.photo_path, size=(100, 100))
            self.photo_widget.configure(image=img)

    def clear_photo(self):
        """Réinitialise la photo de profil."""
        self.photo_path = ""
        img = square_photo(self.photo_path, size=(100, 100))
        self.photo_widget.configure(image=img)

    def set_error(self, key, message):
        """Affiche un message d'erreur sous un champ donné."""
        if key in self.err_labels:
            self.err_labels[key].configure(text=message)
            if key in self.widgets:
                self.widgets[key].configure(border_color=THEME["error_red"])

    def clear_error(self, key):
        """Efface le message d'erreur d'un champ donné."""
        if key in self.err_labels:
            self.err_labels[key].configure(text="")
            if key in self.widgets:
                self.widgets[key].configure(border_color=THEME["border_color"])

    def validate_field(self, key, validator, required):
        """Valide un champ et affiche les erreurs si nécessaire."""
        value = self.widgets[key].get().strip()
        self.clear_error(key)
        
        if required and not value:
            self.set_error(key, "Champ obligatoire.")
            return False
        
        if validator and value and not validator(value):
            if key == "telephone":
                self.set_error(key, "Numéro de téléphone invalide.")
            elif key == "email":
                self.set_error(key, "Adresse e-mail invalide.")
            elif key == "date_embauche":
                self.set_error(key, "Format de date incorrect (AAAA-MM-JJ).")
            else:
                self.set_error(key, "Champ invalide.")
            return False
        
        return True

    def validate_form(self):
        """Valide l'ensemble du formulaire."""
        all_valid = True
        for section in self.fields_config.values():
            for spec in section:
                key = spec[1]
                required = spec[3]
                validator = spec[4]
                if not self.validate_field(key, validator, required):
                    all_valid = False
        return all_valid

    def save_professor(self):
        """Récupère les données, les valide et les envoie au contrôleur."""
        if not self.validate_form():
            messagebox.showerror("Erreur de validation", "Veuillez corriger les champs invalides.")
            return

        form_data = {}
        for section in self.fields_config.values():
            for spec in section:
                key = spec[1]
                value = self.widgets[key].get().strip()
                form_data[key] = value

        form_data['photo_path'] = self.photo_path

        if self.mode == "Ajouter":
            if add_professeur(form_data):
                messagebox.showinfo("Succès", "Professeur ajouté avec succès.")
                self.data_updater()
                self.destroy()
            else:
                messagebox.showerror("Erreur", "Une erreur est survenue lors de l'ajout.")
        elif self.mode == "Modifier":
            prof_id = self.data.get('id')
            if update_professeur(prof_id, form_data):
                messagebox.showinfo("Succès", "Professeur mis à jour avec succès.")
                self.data_updater()
                self.destroy()
            else:
                messagebox.showerror("Erreur", "Une erreur est survenue lors de la mise à jour.")

# # Pour tester la vue seule
# if __name__ == "__main__":
#     app = ctk.CTk()
#     app.geometry("900x600")
#     app.title("EduManager+ - Gestion des Professeurs")
#     app.configure(fg_color=THEME["bg_main"])
#     
#     def dummy_updater():
#         print("Mise à jour des données...")
#         
#     # Test du dashboard
#     # dash = ProfessorsDashboard(app)
#     # dash.pack(fill="both", expand=True)

#     # Test du formulaire
#     # mock_prof = get_all_professeurs()[0] if get_all_professeurs() else None
#     # form = TeacherForm(app, dummy_updater, mode="Modifier", data=mock_prof)
#     
#     app.mainloop()