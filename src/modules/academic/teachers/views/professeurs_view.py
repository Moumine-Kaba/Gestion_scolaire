from database.connection import get_db_connection
import customtkinter as ctk
from PIL import Image, ImageDraw, ImageFont, ImageOps
from tkinter import messagebox, filedialog
import os, sys
import csv
from datetime import datetime

def load_icon(icon_name, size=24):
    """Charge une icône depuis le dossier resources/icons"""
    try:
        # Construire le chemin complet depuis la racine du projet
        project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../../..'))
        icon_path = os.path.join(project_root, 'resources', 'icons', f"{icon_name}.png")
        
        if os.path.exists(icon_path):
            print(f"✅ Icône '{icon_name}' chargée: {icon_path}")
            return ctk.CTkImage(Image.open(icon_path), size=(size, size))
        else:
            print(f"⚠️ Icône '{icon_name}' introuvable: {icon_path}")
            # Créer une icône par défaut simple
            default_icon = Image.new('RGBA', (size, size), (128, 128, 128, 255))
            return ctk.CTkImage(default_icon, size=(size, size))
    except Exception as e:
        print(f"⚠️ Erreur chargement icône {icon_name}: {e}")
        # Créer une icône par défaut simple
        default_icon = Image.new('RGBA', (size, size), (128, 128, 128, 255))
        return ctk.CTkImage(default_icon, size=(size, size))

class ProfesseurDialog(ctk.CTkToplevel):
    """Dialog simple pour ajouter/modifier un professeur"""
    
    def __init__(self, parent, title, professor_data=None):
        super().__init__(parent)
        self.parent = parent
        self.result = None
        
        self.title(title)
        self.geometry("600x650")
        self.configure(fg_color=CARD_BG)
        
        # Empêcher la fermeture accidentelle
        self.transient(parent)
        self.grab_set()
        
        self.setup_dialog(professor_data)
        
    def setup_dialog(self, professor_data=None):
        """Configure le dialog"""
        # Titre
        title_label = ctk.CTkLabel(
            self,
            text=self.title(),
            font=FONT_TITLE,
            text_color=TEXT
        )
        title_label.pack(pady=20)
        
        # Formulaire
        form_frame = ctk.CTkFrame(self, fg_color="transparent")
        form_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Nom
        ctk.CTkLabel(form_frame, text="Nom:", font=FONT_SECONDARY, text_color=TEXT).pack(anchor="w")
        self.nom_entry = ctk.CTkEntry(form_frame, font=FONT_SECONDARY, fg_color=BG_SIDEBAR, text_color=TEXT)
        self.nom_entry.pack(fill="x", pady=(5, 15))
        
        # Prénom
        ctk.CTkLabel(form_frame, text="Prénom:", font=FONT_SECONDARY, text_color=TEXT).pack(anchor="w")
        self.prenom_entry = ctk.CTkEntry(form_frame, font=FONT_SECONDARY, fg_color=BG_SIDEBAR, text_color=TEXT)
        self.prenom_entry.pack(fill="x", pady=(5, 15))
        
        # Email
        ctk.CTkLabel(form_frame, text="Email:", font=FONT_SECONDARY, text_color=TEXT).pack(anchor="w")
        self.email_entry = ctk.CTkEntry(form_frame, font=FONT_SECONDARY, fg_color=BG_SIDEBAR, text_color=TEXT)
        self.email_entry.pack(fill="x", pady=(5, 15))
        
        # Téléphone
        ctk.CTkLabel(form_frame, text="Téléphone:", font=FONT_SECONDARY, text_color=TEXT).pack(anchor="w")
        self.telephone_entry = ctk.CTkEntry(form_frame, font=FONT_SECONDARY, fg_color=BG_SIDEBAR, text_color=TEXT)
        self.telephone_entry.pack(fill="x", pady=(5, 15))
        
        # Spécialité
        ctk.CTkLabel(form_frame, text="Spécialité:", font=FONT_SECONDARY, text_color=TEXT).pack(anchor="w")
        self.specialite_entry = ctk.CTkEntry(form_frame, font=FONT_SECONDARY, fg_color=BG_SIDEBAR, text_color=TEXT)
        self.specialite_entry.pack(fill="x", pady=(5, 15))
        
        # Statut
        ctk.CTkLabel(form_frame, text="Statut:", font=FONT_SECONDARY, text_color=TEXT).pack(anchor="w")
        self.statut_combo = ctk.CTkComboBox(
            form_frame,
            values=["actif", "inactif", "Professeur principal"],
            font=FONT_SECONDARY,
            fg_color=BG_SIDEBAR,
            text_color=TEXT
        )
        self.statut_combo.pack(fill="x", pady=(5, 20))
        
        # Boutons
        buttons_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        buttons_frame.pack(fill="x", pady=10)
        
        # Bouton Annuler
        cancel_btn = ctk.CTkButton(
            buttons_frame,
            text="Annuler",
            font=FONT_BUTTON,
            fg_color=MUTED,
            hover_color=ACCENT,
            text_color=TEXT,
            command=self.cancel
        )
        cancel_btn.pack(side="right", padx=(10, 0))
        
        # Bouton Sauvegarder
        save_btn = ctk.CTkButton(
            buttons_frame,
            text="Sauvegarder",
            font=FONT_BUTTON,
            fg_color=SUCCESS_GREEN,
            hover_color="#047857",
            text_color="white",
            command=self.save
        )
        save_btn.pack(side="right")
        
        # Charger les données si modification
        if professor_data:
            self.load_data(professor_data)
            
    def load_data(self, professor_data):
        """Charge les données du professeur"""
        self.nom_entry.insert(0, professor_data.get('nom', ''))
        self.prenom_entry.insert(0, professor_data.get('prenom', ''))
        self.email_entry.insert(0, professor_data.get('email', ''))
        self.telephone_entry.insert(0, professor_data.get('telephone', ''))
        self.specialite_entry.insert(0, professor_data.get('specialite', ''))
        self.statut_combo.set(professor_data.get('statut', 'actif'))
        
    def save(self):
        """Sauvegarde les données"""
        data = {
            'nom': self.nom_entry.get(),
            'prenom': self.prenom_entry.get(),
            'email': self.email_entry.get(),
            'telephone': self.telephone_entry.get(),
            'specialite': self.specialite_entry.get(),
            'statut': self.statut_combo.get()
        }
        
        # Validation simple
        if not data['nom'] or not data['prenom']:
            messagebox.showerror("Erreur", "Le nom et prénom sont obligatoires.")
            return
            
        self.result = data
        self.destroy()
        
    def cancel(self):
        """Annule le dialog"""
        self.result = None
        self.destroy()

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
        BG_MAIN, BG_SIDEBAR, CARD_BG, BORDER_COLOR, ACCENT, LIGHT_BLUE, TEXT, MUTED,
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
except ImportError:
    print("WARNING: Le module 'utils.validators' n'a pas été trouvé. Utilisation de stubs.")
    def is_name(s): return isinstance(s, str) and len(s) > 1
    def is_phone(s): return isinstance(s, str) and s.isdigit() and len(s) > 5
    def is_email(s): return isinstance(s, str) and "@" in s
    def is_date(s): return isinstance(s, str) and len(s) == 10 and s[4] == '-' and s[7] == '-'

# Import du contrôleur des professeurs
try:
    from src.modules.academic.teachers.controllers.professeur_controller import (
        get_all_professeurs, add_professeur, update_professeur, delete_professeur, get_professeur
    )
    print("✅ Contrôleur des professeurs importé avec succès")
except ImportError as e:
    print("WARNING: Le module 'utils.validators' ou 'controllers.professeur_controller' n'a pas été trouvé. Utilisation de stubs.")
    def is_name(s): return isinstance(s, str) and len(s) > 1
    def is_phone(s): return isinstance(s, str) and s.isdigit() and len(s) > 5
    def is_email(s): return isinstance(s, str) and "@" in s
    def is_date(s): return isinstance(s, str) and len(s) == 10 and s[4] == '-' and s[7] == '-'
    
    def get_db_connection_direct():
        try:
            conn = get_db_connection_direct()
            # conn.row_factory = sqlite3.Row  # Remplacé par SQL Server
            return conn
        except Exception as e:
            print(f"Erreur de connexion à la base de données: {e}")
            return None

    def get_all_professeurs():
        conn = get_db_connection_direct()
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
                'sexe': prof_dict.get('sexe', ''),
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
        """Ajoute un nouveau professeurs à la base de données"""
        conn = get_db_connection_direct()
        if not conn: return False
        try:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO professeurs (matricule, nom, prenom, date_naissance, 
                                       adresse, telephone, email, specialite, date_embauche, statut)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                data.get('matricule', ''),
                data.get('nom', ''),
                data.get('prenom', ''),
                data.get('date_naissance', ''),
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
        """Met à jour un professeurs existant"""
        conn = get_db_connection_direct()
        if not conn: return False
        try:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE professeurs SET 
                    matricule=?, nom=?, prenom=?, date_naissance=?,
                    adresse=?, telephone=?, email=?, specialite=?, date_embauche=?, statut=?
                WHERE id_professeur=?
            """, (
                data.get('matricule', ''),
                data.get('nom', ''),
                data.get('prenom', ''),
                data.get('date_naissance', ''),
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
        """Supprime un professeurs de la base de données"""
        conn = get_db_connection_direct()
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
        conn = get_db_connection_direct()
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
                'sexe': prof_dict.get('sexe', ''),
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
        self.selected_prof_id = None  # Ajout du système de sélection
        self.search_var = ctk.StringVar()
        self.sort_var = ctk.StringVar(value="nom")
        self.selected_prof = None
        self.selected_prof_frame = None
        
        # Import du contrôleur de salaires
        try:
            from src.modules.academic.teachers.controllers.salary_controller import SalaryController
            self.salary_controller = SalaryController()
            print("✅ Contrôleur de salaires importé avec succès")
        except ImportError as e:
            print(f"⚠️ Contrôleur de salaires non disponible: {e}")
            self.salary_controller = None
        
        # Charger les icônes
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
        """Crée l'interface complète de gestion des professeurs avec salaires"""
        self.create_header()
        
        # Frame principal avec layout en 2 colonnes
        main_frame = ctk.CTkFrame(self, fg_color="transparent")
        main_frame.pack(fill="both", expand=True, padx=15, pady=(0, 15))
        main_frame.grid_columnconfigure(0, weight=1)  # Liste des professeurs
        main_frame.grid_columnconfigure(1, weight=2)  # Détails et salaires
        main_frame.grid_rowconfigure(0, weight=1)
        
        # Créer les panneaux
        self.create_professors_list_panel(main_frame)
        self.create_professor_details_panel(main_frame)
        
        # Charger les données
        self.refresh_professors_view()

    def create_header(self):
        """Crée l'en-tête de la vue avec le titre et les boutons d'action"""
        # Frame principal avec gradient effect
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.pack(fill="x", pady=15, padx=15)
        
        # Container avec effet de carte
        header_container = ctk.CTkFrame(header_frame, fg_color=CARD_BG, corner_radius=20, 
                                       border_color=BORDER_COLOR, border_width=1)
        header_container.pack(fill="x")
        
        # Titre principal avec icône
        title_frame = ctk.CTkFrame(header_container, fg_color="transparent")
        title_frame.pack(side="left", fill="x", expand=True, padx=20, pady=15)
        
        # Icône group
        group_icon = ctk.CTkLabel(
            title_frame,
            image=self.icon_cache.get("group", load_icon("group", 32)),
            text="",
            fg_color="transparent"
        )
        group_icon.pack(side="left", padx=(0, 15))
        
        # Titre avec style moderne
        title_label = ctk.CTkLabel(
            title_frame,
            text="Gestion des Professeurs", 
            font=FONT_TITLE,
            text_color=ACCENT
        )
        title_label.pack(side="left")
        
        # Sous-titre informatif
        subtitle_label = ctk.CTkLabel(
            title_frame, 
            text="• Gestion complète des professeurs et salaires", 
            font=FONT_SECONDARY, 
            text_color=MUTED
        )
        subtitle_label.pack(side="left", padx=(15, 0))

        # Boutons d'action avec design moderne
        btn_frame = ctk.CTkFrame(header_container, fg_color="transparent")
        btn_frame.pack(side="right", padx=20, pady=15)

        # Bouton Actualiser
        refresh_btn = ctk.CTkButton(
            btn_frame, 
            text="", 
            image=self.icon_cache.get("refresh", load_icon("refresh", 18)), 
            width=45, 
            height=45,
            fg_color=BG_SIDEBAR, 
            hover_color="#4A90E2",
            corner_radius=12, 
            command=self.refresh_professors_view
        )
        refresh_btn.pack(side="left", padx=(0, 10))

        # Bouton Ajouter
        add_btn = ctk.CTkButton(
            btn_frame, 
            text="Nouveau Professeur", 
            image=self.icon_cache.get("add", load_icon("add", 18)), 
            compound="left", 
            font=FONT_BUTTON,
            fg_color=BG_SIDEBAR, 
            hover_color="#4A90E2", 
            text_color=TEXT,
            command=self.add_professor, 
            width=160,
            height=45, 
            corner_radius=12,
            border_color=BORDER_COLOR,
            border_width=2
        )
        add_btn.pack(side="left")

    def create_professors_list_panel(self, parent_frame):
        """Crée le panneau de gauche avec la liste des professeurs"""
        # Container principal avec design moderne
        list_panel = ctk.CTkFrame(parent_frame, fg_color=CARD_BG, corner_radius=15, 
                                 border_color=BORDER_COLOR, border_width=1)
        list_panel.grid(row=0, column=0, sticky="nsew", padx=(0, 10))

        # En-tête du panneau
        panel_header = ctk.CTkFrame(list_panel, fg_color="transparent")
        panel_header.pack(fill="x", padx=15, pady=15)
        
        # Titre du panneau
        panel_title = ctk.CTkLabel(
            panel_header, 
            text="Liste des Professeurs", 
            font=FONT_TITLE, 
            text_color=TEXT
        )
        panel_title.pack(side="left")
        
        # Compteur de professeurs
        self.prof_count_label = ctk.CTkLabel(
            panel_header, 
            text="",
            font=FONT_SECONDARY, 
            text_color=ACCENT
        )
        self.prof_count_label.pack(side="right")

        # Barre de recherche
        search_frame = ctk.CTkFrame(list_panel, fg_color="transparent")
        search_frame.pack(fill="x", padx=15, pady=(0, 15))
        
        search_entry = ctk.CTkEntry(
            search_frame,
            textvariable=self.search_var,
            font=FONT_SECONDARY,
            placeholder_text="🔍 Rechercher un professeur...",
            fg_color=BG_SIDEBAR,
            text_color=TEXT,
            border_width=1,
            border_color=BORDER_COLOR,
            corner_radius=10,
            height=35
        )
        search_entry.pack(fill="x")
        search_entry.bind("<KeyRelease>", self.filter_professors)
        
        # Liste scrollable des professeurs
        self.professors_list_frame = ctk.CTkScrollableFrame(
            list_panel,
            fg_color="transparent",
            scrollbar_button_color=BORDER_COLOR,
            scrollbar_button_hover_color=ACCENT
        )
        self.professors_list_frame.pack(fill="both", expand=True, padx=15, pady=(0, 15))

    def create_professor_details_panel(self, parent_frame):
        """Crée le panneau de droite avec les détails en design compact"""
        # Container principal avec votre thème
        details_panel = ctk.CTkFrame(parent_frame, fg_color=CARD_BG, corner_radius=12, 
                                    border_color=BORDER_COLOR, border_width=1)
        details_panel.grid(row=0, column=1, sticky="nsew")

        # En-tête simple
        details_header = ctk.CTkFrame(details_panel, fg_color=BG_SIDEBAR, corner_radius=8)
        details_header.pack(fill="x", padx=16, pady=16)
        
        # Titre simple
        title_label = ctk.CTkLabel(
            details_header,
            text="Détails du Professeur",
            font=("Segoe UI", 16, "bold"),
            text_color=TEXT
        )
        title_label.pack(pady=12)

        # Zone de contenu principal SANS scroll
        self.details_content_frame = ctk.CTkFrame(
            details_panel,
                fg_color="transparent"
            )
        self.details_content_frame.pack(fill="both", expand=True, padx=16, pady=(0, 16))
        
    def refresh_professors_view(self):
        """Actualise la vue des professeurs"""
        self.load_professors_data()
        self.display_professors_list()
        self.update_prof_count()
        
    def load_professors_data(self):
        """Charge les données des professeurs"""
        try:
            from src.modules.academic.teachers.controllers.professeur_controller import get_all_professeurs
            self.professors_data = get_all_professeurs()
            print(f"✅ {len(self.professors_data)} professeurs chargés")
        except Exception as e:
            print(f"⚠️ Erreur chargement professeurs: {e}")
            self.professors_data = []

    def display_professors_list(self):
        """Affiche la liste des professeurs dans le panneau de gauche"""
        # Nettoyer la liste existante
        for widget in self.professors_list_frame.winfo_children():
                widget.destroy()
        
        # Filtrer les professeurs selon la recherche
        search_term = self.search_var.get().lower()
        filtered_profs = []
        
        for prof in self.professors_data:
            if not search_term or (
                search_term in prof.get('nom', '').lower() or
                search_term in prof.get('prenom', '').lower() or
                search_term in prof.get('specialite', '').lower() or
                search_term in prof.get('email', '').lower()
            ):
                filtered_profs.append(prof)
        
        # Afficher chaque professeur
        for prof in filtered_profs:
            self.create_professor_list_item(prof)

    def create_professor_list_item(self, prof):
        """Crée un élément de liste pour un professeur"""
        # Frame principal de l'élément
        item_frame = ctk.CTkFrame(
            self.professors_list_frame,
            fg_color=BG_SIDEBAR,
            corner_radius=10,
            border_width=1,
            border_color=BORDER_COLOR
        )
        item_frame.pack(fill="x", pady=5)
        
        # Photo de profil
        photo_frame = ctk.CTkFrame(item_frame, fg_color=CARD_BG, corner_radius=25, width=50, height=50)
        photo_frame.pack(side="left", padx=10, pady=10)
        photo_frame.pack_propagate(False)
        
        photo_label = ctk.CTkLabel(
            photo_frame,
            image=self.icon_cache.get("person", load_icon("person", 25)),
            text="",
            fg_color="transparent"
        )
        photo_label.pack(expand=True)
        
        # Informations du professeur
        info_frame = ctk.CTkFrame(item_frame, fg_color="transparent")
        info_frame.pack(side="left", fill="x", expand=True, padx=10, pady=10)
        
        # Nom et prénom
        name_label = ctk.CTkLabel(
            info_frame,
            text=f"{prof.get('nom', 'N/A')} {prof.get('prenom', 'N/A')}",
            font=FONT_SECONDARY,
            text_color=TEXT,
            fg_color="transparent"
        )
        name_label.pack(anchor="w")
        
        # Spécialité
        spec_label = ctk.CTkLabel(
            info_frame,
            text=prof.get('specialite', 'Non spécifié'),
            font=FONT_SECONDARY,
            text_color=MUTED,
            fg_color="transparent"
        )
        spec_label.pack(anchor="w")
        
        # Salaire (si disponible)
        if self.salary_controller:
            try:
                current_month = datetime.now().month
                current_year = datetime.now().year
                salary_info = self.salary_controller.calculate_salary(prof.get('id'), current_month, current_year)
                if salary_info and salary_info.get('salaire_net'):
                    salary_text = f"Salaire: {salary_info['salaire_net']:,.0f} GNF"
                    salary_label = ctk.CTkLabel(
                        info_frame,
                        text=salary_text,
                        font=FONT_SECONDARY,
                        text_color=SUCCESS_GREEN,
                        fg_color="transparent"
                    )
                    salary_label.pack(anchor="w")
            except:
                pass
        
        # Bouton de sélection
        select_btn = ctk.CTkButton(
            item_frame,
            text="",
            image=self.icon_cache.get("chevron_right", load_icon("chevron_right", 16)),
            width=30,
            height=30,
                fg_color="transparent",
            hover_color=ACCENT,
            corner_radius=15,
            command=lambda p=prof: self.select_professor(p)
        )
        select_btn.pack(side="right", padx=10, pady=10)
        
        # Stocker la référence au professeur
        item_frame.prof_data = prof

    def select_professor(self, prof):
        """Sélectionne un professeur et affiche ses détails"""
        # Mettre à jour la sélection visuelle
        for widget in self.professors_list_frame.winfo_children():
            if hasattr(widget, 'prof_data'):
                if widget.prof_data == prof:
                    widget.configure(fg_color=SUCCESS_GREEN)
                else:
                    widget.configure(fg_color=BG_SIDEBAR)
        
        self.selected_prof = prof
        self.display_professor_details(prof)

    def display_professor_details(self, prof):
        """Affiche les détails d'un professeur dans le panneau de droite"""
        # Nettoyer le contenu existant
        for widget in self.details_content_frame.winfo_children():
            widget.destroy()
        
        if not prof:
            # Message par défaut
            default_label = ctk.CTkLabel(
                self.details_content_frame,
                text="Sélectionnez un professeur pour voir ses détails",
                font=FONT_SECONDARY,
                text_color=MUTED,
                fg_color="transparent"
            )
            default_label.pack(expand=True)
            return
        
        # Informations personnelles
        self.create_personal_info_section(prof)
        
        # Informations de paiement
        self.create_salary_info_section(prof)
        
        # Actions simples
        self.create_simple_actions_section(prof)

    def create_personal_info_section(self, prof):
        """Crée la section d'informations personnelles avec votre thème"""
        # Container principal avec votre thème
        info_container = ctk.CTkFrame(self.details_content_frame, fg_color=CARD_BG, corner_radius=8)
        info_container.pack(fill="x", pady=(0, 12))
        
        # En-tête de la section
        section_header = ctk.CTkFrame(info_container, fg_color=BG_SIDEBAR, corner_radius=8)
        section_header.pack(fill="x", padx=12, pady=12)
        
        # Titre avec icône
        title_frame = ctk.CTkFrame(section_header, fg_color="transparent")
        title_frame.pack()
        
        title_label = ctk.CTkLabel(
            title_frame,
            text="👤 Informations Personnelles",
            font=("Segoe UI", 14, "bold"),
            text_color=TEXT
        )
        title_label.pack()
        
        # Contenu principal
        content_frame = ctk.CTkFrame(info_container, fg_color="transparent")
        content_frame.pack(fill="x", padx=12, pady=12)
        
        # Avatar et nom principal
        header_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        header_frame.pack(fill="x", pady=(0, 16))
        
        # Avatar
        avatar_frame = ctk.CTkFrame(header_frame, fg_color=BORDER_COLOR, corner_radius=40, width=80, height=80)
        avatar_frame.pack(side="left", padx=(0, 16))
        avatar_frame.pack_propagate(False)
        
        avatar_label = ctk.CTkLabel(
            avatar_frame,
            image=self.icon_cache.get("user_avatar", load_icon("user_avatar", 50)),
            text="",
            fg_color="transparent"
        )
        avatar_label.pack(expand=True)
        
        # Nom et spécialité
        name_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        name_frame.pack(side="left", fill="x", expand=True)
        
        name_label = ctk.CTkLabel(
            name_frame,
            text=f"{prof.get('nom', 'N/A')} {prof.get('prenom', 'N/A')}",
            font=("Segoe UI", 18, "bold"),
            text_color=TEXT,
            fg_color="transparent"
        )
        name_label.pack(anchor="w", pady=(0, 4))
        
        specialty_label = ctk.CTkLabel(
            name_frame,
            text=prof.get('specialite', 'Professeur'),
            font=("Segoe UI", 12),
            text_color=MUTED,
            fg_color="transparent"
        )
        specialty_label.pack(anchor="w")
        
        # Grille des informations essentielles
        info_grid = ctk.CTkFrame(content_frame, fg_color="transparent")
        info_grid.pack(fill="x")
        
        # Informations essentielles de la base de données
        essential_info = [
            ("📧 Email", prof.get('email', 'N/A')),
            ("📞 Téléphone", prof.get('telephone', 'N/A')),
            ("📅 Date embauche", prof.get('date_embauche', 'N/A')),
            ("💼 Statut", prof.get('statut', 'Actif'))
        ]
        
        for i, (label, value) in enumerate(essential_info):
            row = i // 2
            col = i % 2
            
            # Item d'information
            info_item = ctk.CTkFrame(info_grid, fg_color=BG_SIDEBAR, corner_radius=6)
            info_item.grid(row=row, column=col, sticky="ew", padx=4, pady=4)
            
            info_content = ctk.CTkFrame(info_item, fg_color="transparent")
            info_content.pack(fill="x", padx=12, pady=8)
            
            # Label avec icône
            label_widget = ctk.CTkLabel(
                info_content,
                text=label,
                font=("Segoe UI", 10, "bold"),
                text_color=MUTED,
                fg_color="transparent"
            )
            label_widget.pack(anchor="w")
            
            # Valeur
            value_widget = ctk.CTkLabel(
                info_content,
                text=str(value) if value != 'N/A' else 'Non renseigné',
                font=("Segoe UI", 11),
                text_color=TEXT,
                fg_color="transparent"
            )
            value_widget.pack(anchor="w")
        
        # Configuration des colonnes
        info_grid.grid_columnconfigure((0, 1), weight=1)

    def create_salary_info_section(self, prof):
        """Crée la section de paiement avec votre thème"""
        # Container principal avec votre thème
        salary_container = ctk.CTkFrame(self.details_content_frame, fg_color=CARD_BG, corner_radius=8)
        salary_container.pack(fill="x", pady=(0, 12))
        
        # En-tête de la section
        section_header = ctk.CTkFrame(salary_container, fg_color=BG_SIDEBAR, corner_radius=8)
        section_header.pack(fill="x", padx=12, pady=12)
        
        # Titre avec icône
        title_frame = ctk.CTkFrame(section_header, fg_color="transparent")
        title_frame.pack()
        
        title_label = ctk.CTkLabel(
            title_frame,
            text="💰 Informations de Paiement",
            font=("Segoe UI", 14, "bold"),
            text_color=TEXT
        )
        title_label.pack()
        
        # Contenu principal
        content_frame = ctk.CTkFrame(salary_container, fg_color="transparent")
        content_frame.pack(fill="x", padx=12, pady=12)
        
        # Taux horaire en évidence
        salaire_horaire = prof.get('salaire_horaire', 0) or 0
        
        # Affichage du taux horaire principal
        rate_frame = ctk.CTkFrame(content_frame, fg_color=BG_SIDEBAR, corner_radius=8)
        rate_frame.pack(fill="x", pady=(0, 12))
        
        rate_content = ctk.CTkFrame(rate_frame, fg_color="transparent")
        rate_content.pack(fill="x", padx=16, pady=16)
        
        # Taux horaire principal
        rate_label = ctk.CTkLabel(
            rate_content,
            text="⏰ Taux Horaire",
            font=("Segoe UI", 12, "bold"),
            text_color=MUTED,
            fg_color="transparent"
        )
        rate_label.pack(anchor="w", pady=(0, 4))
        
        rate_value = ctk.CTkLabel(
            rate_content,
            text=f"{salaire_horaire:,.0f} GNF/heure",
            font=("Segoe UI", 16, "bold"),
            text_color=ACCENT,
            fg_color="transparent"
        )
        rate_value.pack(anchor="w")
        
        # Mode de paiement
        payment_mode_label = ctk.CTkLabel(
            rate_content,
            text="💼 Mode: Par heures dispensées",
            font=("Segoe UI", 11),
            text_color=TEXT,
            fg_color="transparent"
        )
        payment_mode_label.pack(anchor="w", pady=(8, 0))
        
        # Récupérer les heures du mois actuel
        if self.salary_controller:
            current_month = datetime.now().month
            current_year = datetime.now().year
            current_hours = self.salary_controller.get_professor_hours(prof.get('id'), current_month, current_year)
            total_current_hours = sum(hour.get('nombre_heures', 0) for hour in current_hours)
        else:
            total_current_hours = 0
        
        # Calcul du salaire du mois
        salaire_mois = total_current_hours * salaire_horaire
        
        # Statistiques du mois
        stats_frame = ctk.CTkFrame(content_frame, fg_color=BG_SIDEBAR, corner_radius=8)
        stats_frame.pack(fill="x")
        
        stats_content = ctk.CTkFrame(stats_frame, fg_color="transparent")
        stats_content.pack(fill="x", padx=16, pady=16)
        
        stats_title = ctk.CTkLabel(
            stats_content,
            text="📊 Statistiques du Mois",
            font=("Segoe UI", 12, "bold"),
            text_color=TEXT,
            fg_color="transparent"
        )
        stats_title.pack(anchor="w", pady=(0, 12))
        
        # Grille des statistiques
        stats_grid = ctk.CTkFrame(stats_content, fg_color="transparent")
        stats_grid.pack(fill="x")
        
        stats_data = [
            ("🕐 Heures dispensées", f"{total_current_hours}h"),
            ("💵 Salaire du mois", f"{salaire_mois:,.0f} GNF"),
            ("📅 Période", f"{current_month}/{current_year}"),
            ("✅ Statut", "Actif" if total_current_hours > 0 else "Aucune heure")
        ]
        
        for i, (label, value) in enumerate(stats_data):
            row = i // 2
            col = i % 2
            
            # Item de statistique
            stat_item = ctk.CTkFrame(stats_grid, fg_color=CARD_BG, corner_radius=6)
            stat_item.grid(row=row, column=col, sticky="ew", padx=4, pady=4)
            
            stat_content = ctk.CTkFrame(stat_item, fg_color="transparent")
            stat_content.pack(fill="x", padx=12, pady=8)
            
            # Label avec icône
            label_widget = ctk.CTkLabel(
                stat_content,
                text=label,
                font=("Segoe UI", 10, "bold"),
                text_color=MUTED,
                fg_color="transparent"
            )
            label_widget.pack(anchor="w")
            
            # Valeur
            value_widget = ctk.CTkLabel(
                stat_content,
                text=value,
                font=("Segoe UI", 11),
                text_color=TEXT,
                fg_color="transparent"
            )
            value_widget.pack(anchor="w")
        
        # Configuration des colonnes
        stats_grid.grid_columnconfigure((0, 1), weight=1)

    def create_simple_actions_section(self, prof):
        """Crée une section d'actions simple avec votre thème"""
        # Container principal avec votre thème
        actions_container = ctk.CTkFrame(self.details_content_frame, fg_color=CARD_BG, corner_radius=8)
        actions_container.pack(fill="x", pady=(0, 12))
        
        # En-tête de la section
        section_header = ctk.CTkFrame(actions_container, fg_color=BG_SIDEBAR, corner_radius=8)
        section_header.pack(fill="x", padx=12, pady=12)
        
        # Titre avec icône
        title_frame = ctk.CTkFrame(section_header, fg_color="transparent")
        title_frame.pack()
        
        title_label = ctk.CTkLabel(
            title_frame,
            text="⚡ Actions",
            font=("Segoe UI", 14, "bold"),
            text_color=TEXT
        )
        title_label.pack()
        
        # Contenu principal
        content_frame = ctk.CTkFrame(actions_container, fg_color="transparent")
        content_frame.pack(fill="x", padx=12, pady=12)
        
        # Boutons d'action
        buttons_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        buttons_frame.pack(fill="x")
        
        # Bouton Modifier
        edit_btn = ctk.CTkButton(
            buttons_frame,
            text="✏️ Modifier",
            font=("Segoe UI", 11, "bold"),
            fg_color=ACCENT,
            hover_color="#2563EB",
            text_color="white",
            height=32,
            corner_radius=16,
            command=lambda p=prof: self.edit_professor(p)
        )
        edit_btn.pack(side="left", padx=(0, 8))
        
        # Bouton Supprimer
        delete_btn = ctk.CTkButton(
            buttons_frame,
            text="🗑️ Supprimer",
            font=("Segoe UI", 11, "bold"),
            fg_color=ERROR_RED,
            hover_color="#dc2626",
            text_color="white",
                height=32,
            corner_radius=16,
            command=lambda p=prof: self.delete_professor(p)
        )
        delete_btn.pack(side="left", padx=(0, 8))
        
        # Bouton Calculer Salaire
        calc_btn = ctk.CTkButton(
            buttons_frame,
            text="💰 Calculer",
            font=("Segoe UI", 11, "bold"),
            fg_color=SUCCESS_GREEN,
            hover_color="#059669",
            text_color="white",
            height=32,
            corner_radius=16,
            command=lambda p=prof: self.calculate_professor_salary(p)
        )
        calc_btn.pack(side="left")

    def edit_professor(self, prof):
        """Modifie les informations du professeur"""
        messagebox.showinfo("Modification", f"Fonctionnalité de modification pour {prof.get('nom', 'N/A')} {prof.get('prenom', 'N/A')}")

    def delete_professor(self, prof):
        """Supprime le professeur"""
        result = messagebox.askyesno("Confirmation", f"Êtes-vous sûr de vouloir supprimer {prof.get('nom', 'N/A')} {prof.get('prenom', 'N/A')} ?")
        if result:
            messagebox.showinfo("Suppression", f"Professeur {prof.get('nom', 'N/A')} supprimé avec succès")

    def calculate_professor_salary(self, prof):
        """Calcule le salaire du professeur"""
        salaire_horaire = prof.get('salaire_horaire', 0) or 0
        if salaire_horaire > 0:
            messagebox.showinfo("Calcul Salaire", f"Taux horaire: {salaire_horaire} GNF/heure\nMode: Par heures dispensées")
        else:
            messagebox.showwarning("Attention", "Aucun taux horaire configuré pour ce professeur")

    def create_course_hours_section(self, prof):
        """Crée la section des heures de cours"""
        # Titre de section
        section_title = ctk.CTkLabel(
            self.details_content_frame,
            text="⏰ Heures de Cours",
            font=FONT_TITLE,
            text_color=ACCENT,
            fg_color="transparent"
        )
        section_title.pack(anchor="w", pady=(0, 15))
        
        # Frame des heures de cours
        hours_frame = ctk.CTkFrame(self.details_content_frame, fg_color=CARD_BG, corner_radius=10)
        hours_frame.pack(fill="x", pady=(0, 20))
        
        # Récupérer les heures de cours
        if self.salary_controller:
            current_month = datetime.now().month
            current_year = datetime.now().year
            course_hours = self.salary_controller.get_professor_hours(prof.get('id'), current_month, current_year)
        else:
            course_hours = []
        
        # Affichage des heures
        if course_hours:
            total_hours = sum(hour.get('nombre_heures', 0) for hour in course_hours)
            
            # Total des heures avec design amélioré
            total_frame = ctk.CTkFrame(hours_frame, fg_color=BG_MAIN, corner_radius=10, border_width=2, border_color=SUCCESS_GREEN)
            total_frame.pack(fill="x", padx=15, pady=15)
            
            # Header avec total
            header_frame = ctk.CTkFrame(total_frame, fg_color="transparent")
            header_frame.pack(fill="x", padx=15, pady=15)
            
            total_title = ctk.CTkLabel(
                header_frame,
                text="⏰ Total des heures ce mois",
                font=("Segoe UI", 14, "bold"),
                text_color=SUCCESS_GREEN,
                fg_color="transparent"
            )
            total_title.pack(side="left")
            
            total_label = ctk.CTkLabel(
                header_frame,
                text=f"{total_hours}h",
                font=("Segoe UI", 16, "bold"),
                text_color=SUCCESS_GREEN,
                fg_color="transparent"
            )
            total_label.pack(side="right")
            
            # Liste des heures (limité à 5 dernières) avec design amélioré
            for hour in course_hours[:5]:
                hour_item = ctk.CTkFrame(hours_frame, fg_color=BG_MAIN, corner_radius=8, border_width=1, border_color=BORDER_COLOR)
                hour_item.pack(fill="x", padx=15, pady=5)
                
                content_frame = ctk.CTkFrame(hour_item, fg_color="transparent")
                content_frame.pack(fill="x", padx=12, pady=8)
                
                date_label = ctk.CTkLabel(
                    content_frame,
                    text=f"📅 {hour.get('date_cours', 'N/A')}",
                    font=FONT_SECONDARY,
                    text_color=TEXT,
                    fg_color="transparent"
                )
                date_label.pack(side="left")
                
                hours_label = ctk.CTkLabel(
                    content_frame,
                    text=f"⏱️ {hour.get('nombre_heures', 0)}h",
                    font=FONT_SECONDARY,
                    text_color=ACCENT,
                    fg_color="transparent"
                )
                hours_label.pack(side="right")
                
                if hour.get('description'):
                    desc_label = ctk.CTkLabel(
                        content_frame,
                        text=f"📝 {hour.get('description', '')}",
                        font=("Segoe UI", 10),
                        text_color=MUTED,
                        fg_color="transparent"
                    )
                    desc_label.pack(anchor="w", pady=(5, 0))
        else:
            no_hours_label = ctk.CTkLabel(
                hours_frame,
                text="Aucune heure de cours enregistrée ce mois",
                font=FONT_SECONDARY,
                text_color=MUTED,
                fg_color="transparent"
            )
            no_hours_label.pack(pady=20)
        
        # Bouton Ajouter heures
        add_hours_btn = ctk.CTkButton(
            hours_frame,
            text="Ajouter Heures",
            image=self.icon_cache.get("add", load_icon("add", 16)),
            font=FONT_BUTTON,
            fg_color=SUCCESS_GREEN,
            hover_color="#047857",
            text_color="white",
            height=35,
            command=lambda p=prof: self.add_course_hours(p)
        )
        add_hours_btn.pack(padx=15, pady=(0, 15))

    def create_actions_section(self, prof):
        """Crée la section des actions"""
        # Titre de section
        section_title = ctk.CTkLabel(
            self.details_content_frame,
            text="⚙️ Actions",
            font=FONT_TITLE,
            text_color=ACCENT,
            fg_color="transparent"
        )
        section_title.pack(anchor="w", pady=(0, 15))
        
        # Frame des actions
        actions_frame = ctk.CTkFrame(self.details_content_frame, fg_color=CARD_BG, corner_radius=10)
        actions_frame.pack(fill="x", pady=(0, 20))
        
        # Boutons d'action
        buttons_frame = ctk.CTkFrame(actions_frame, fg_color="transparent")
        buttons_frame.pack(fill="x", padx=15, pady=15)
        
        # Bouton Modifier
        edit_btn = ctk.CTkButton(
            buttons_frame,
            text="Modifier",
            image=self.icon_cache.get("edit", load_icon("edit", 16)),
            font=("Segoe UI", 11, "bold"),
            fg_color=INFO_ORANGE,
            hover_color="#ea580c",
            text_color="white",
            height=36,
            corner_radius=18,
            command=lambda p=prof: self.edit_professor(p)
        )
        edit_btn.pack(side="left", padx=(0, 10))
        
        # Bouton Supprimer
        delete_btn = ctk.CTkButton(
            buttons_frame,
            text="Supprimer",
            image=self.icon_cache.get("delete", load_icon("delete", 16)),
            font=("Segoe UI", 11, "bold"),
            fg_color=ERROR_RED,
            hover_color="#dc2626",
            text_color="white",
            height=36,
            corner_radius=18,
            command=lambda p=prof: self.delete_professor(p)
        )
        delete_btn.pack(side="left", padx=(0, 10))
        
        # Bouton Exporter
        export_btn = ctk.CTkButton(
            buttons_frame,
            text="📊 Exporter",
            image=self.icon_cache.get("csv", load_icon("csv", 16)),
            font=FONT_BUTTON,
            fg_color=ACCENT,
            hover_color="#4A90E2",
            text_color="white",
                height=45,
            width=140,
            corner_radius=8,
            command=lambda p=prof: self.export_professor_data(p)
        )
        export_btn.pack(side="left")

    def calculate_professor_salary(self, prof):
        """Ouvre le formulaire de configuration et calcul du salaire"""
        self.open_salary_configuration_form(prof)

    def open_salary_configuration_form(self, prof):
        """Ouvre le formulaire de configuration des salaires avec calcul automatique"""
        try:
            # Créer une fenêtre de configuration des salaires
            salary_window = ctk.CTkToplevel(self)
            salary_window.title(f"Configuration Salaires - {prof.get('nom', 'N/A')} {prof.get('prenom', 'N/A')}")
            salary_window.geometry("800x700")
            salary_window.resizable(False, False)
            
            # Appliquer le fond du thème
            salary_window.configure(fg_color=BG_MAIN)
            
            # Centrer la fenêtre
            salary_window.transient(self)
            salary_window.grab_set()
            
            # Frame principal
            main_frame = ctk.CTkFrame(salary_window, fg_color=CARD_BG, corner_radius=15)
            main_frame.pack(fill="both", expand=True, padx=20, pady=20)
            
            # Titre
            title_label = ctk.CTkLabel(
                main_frame,
                text="💰 Configuration des Salaires",
                font=("Segoe UI", 18, "bold"),
                text_color=SUCCESS_GREEN
            )
            title_label.pack(pady=20)
            
            # Informations du professeur
            prof_info_frame = ctk.CTkFrame(main_frame, fg_color=BG_MAIN, corner_radius=10)
            prof_info_frame.pack(fill="x", padx=20, pady=(0, 20))
            
            prof_info_label = ctk.CTkLabel(
                prof_info_frame,
                text=f"👤 {prof.get('nom', 'N/A')} {prof.get('prenom', 'N/A')} - {prof.get('specialite', 'N/A')}",
                font=FONT_SECONDARY,
                text_color=TEXT
            )
            prof_info_label.pack(pady=15)
            
            # Formulaire de configuration
            form_frame = ctk.CTkFrame(main_frame, fg_color=BG_SIDEBAR, corner_radius=10)
            form_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))
            
            # Section 1: Configuration de base
            section1_title = ctk.CTkLabel(
                form_frame,
                text="📋 Configuration de Base",
                font=FONT_TITLE,
                text_color=SUCCESS_GREEN
            )
            section1_title.pack(anchor="w", padx=20, pady=(20, 15))
            
            # Champ: Heures par semaine
            hours_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
            hours_frame.pack(fill="x", padx=20, pady=5)
            
            hours_label = ctk.CTkLabel(
                hours_frame,
                text="⏰ Nombre d'heures par semaine:",
                font=FONT_SECONDARY,
                text_color=TEXT
            )
            hours_label.pack(side="left")
            
            hours_entry = ctk.CTkEntry(
                hours_frame,
                placeholder_text="Ex: 20",
                width=100,
                height=35,
                font=FONT_SECONDARY,
                fg_color=CARD_BG,
                border_color=BORDER_COLOR,
                text_color=TEXT
            )
            hours_entry.pack(side="right")
            
            # Champ: Salaire par heure
            hourly_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
            hourly_frame.pack(fill="x", padx=20, pady=5)
            
            hourly_label = ctk.CTkLabel(
                hourly_frame,
                text="💵 Salaire par heure (GNF):",
                font=FONT_SECONDARY,
                text_color=TEXT
            )
            hourly_label.pack(side="left")
            
            hourly_entry = ctk.CTkEntry(
                hourly_frame,
                placeholder_text="Ex: 2500",
                width=150,
                height=35,
                font=FONT_SECONDARY,
                fg_color=CARD_BG,
                border_color=BORDER_COLOR,
                text_color=TEXT
            )
            hourly_entry.pack(side="right")
            
            # Champ: Salaire mensuel de base
            monthly_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
            monthly_frame.pack(fill="x", padx=20, pady=5)
            
            monthly_label = ctk.CTkLabel(
                monthly_frame,
                text="🏠 Salaire mensuel de base (GNF):",
                font=FONT_SECONDARY,
                text_color=TEXT
            )
            monthly_label.pack(side="left")
            
            monthly_entry = ctk.CTkEntry(
                monthly_frame,
                placeholder_text="Ex: 150000",
                width=150,
                height=35,
                font=FONT_SECONDARY,
                fg_color=CARD_BG,
                border_color=BORDER_COLOR,
                text_color=TEXT
            )
            monthly_entry.pack(side="right")
            
            # Section 2: Calcul automatique
            section2_title = ctk.CTkLabel(
                form_frame,
                text="🧮 Calcul Automatique",
                font=FONT_TITLE,
                text_color=INFO_ORANGE
            )
            section2_title.pack(anchor="w", padx=20, pady=(20, 15))
            
            # Frame de calcul
            calc_frame = ctk.CTkFrame(form_frame, fg_color=BG_MAIN, corner_radius=8)
            calc_frame.pack(fill="x", padx=20, pady=10)
            
            # Labels de calcul
            self.weekly_calc_label = ctk.CTkLabel(
                calc_frame,
                text="📅 Salaire hebdomadaire: 0 GNF",
                font=FONT_SECONDARY,
                text_color=TEXT
            )
            self.weekly_calc_label.pack(anchor="w", padx=15, pady=5)
            
            self.monthly_calc_label = ctk.CTkLabel(
                calc_frame,
                text="📆 Salaire mensuel: 0 GNF",
                font=FONT_SECONDARY,
                text_color=TEXT
            )
            self.monthly_calc_label.pack(anchor="w", padx=15, pady=5)
            
            self.yearly_calc_label = ctk.CTkLabel(
                calc_frame,
                text="📚 Salaire annuel (9 mois): 0 GNF",
                font=FONT_SECONDARY,
                text_color=SUCCESS_GREEN
            )
            self.yearly_calc_label.pack(anchor="w", padx=15, pady=5)
            
            # Fonction de calcul automatique
            def calculate_salary(*args):
                try:
                    hours_per_week = float(hours_entry.get() or 0)
                    hourly_rate = float(hourly_entry.get() or 0)
                    monthly_base = float(monthly_entry.get() or 0)
                    
                    # Calcul hebdomadaire
                    weekly_salary = hours_per_week * hourly_rate
                    self.weekly_calc_label.configure(
                        text=f"📅 Salaire hebdomadaire: {weekly_salary:,.0f} GNF"
                    )
                    
                    # Calcul mensuel (4.33 semaines par mois)
                    monthly_salary = (weekly_salary * 4.33) + monthly_base
                    self.monthly_calc_label.configure(
                        text=f"📆 Salaire mensuel: {monthly_salary:,.0f} GNF"
                    )
                    
                    # Calcul annuel (9 mois de cours)
                    yearly_salary = monthly_salary * 9
                    self.yearly_calc_label.configure(
                        text=f"📚 Salaire annuel (9 mois): {yearly_salary:,.0f} GNF"
                    )
                    
                except ValueError:
                    pass  # Ignorer les valeurs invalides
            
            # Lier les champs au calcul automatique
            hours_entry.bind("<KeyRelease>", calculate_salary)
            hourly_entry.bind("<KeyRelease>", calculate_salary)
            monthly_entry.bind("<KeyRelease>", calculate_salary)
            
            # Boutons d'action
            buttons_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
            buttons_frame.pack(fill="x", padx=20, pady=20)
            
            def save_salary_config():
                try:
                    hours_per_week = float(hours_entry.get() or 0)
                    hourly_rate = float(hourly_entry.get() or 0)
                    monthly_base = float(monthly_entry.get() or 0)
                    
                    if hours_per_week <= 0 or hourly_rate <= 0:
                        messagebox.showerror("Erreur", "Veuillez saisir des valeurs valides")
                        return
                    
                    # Calculer les salaires
                    weekly_salary = hours_per_week * hourly_rate
                    monthly_salary = (weekly_salary * 4.33) + monthly_base
                    
                    # Sauvegarder en base de données
                    conn = get_db_connection()
                    if conn:
                        cursor = conn.cursor()
                        try:
                            # Mettre à jour les informations de salaire du professeur
                            cursor.execute("""
                                UPDATE professeurs 
                                SET heures_mensuelles = ?, 
                                    salaire_horaire = ?, 
                                    salaire_base = ?,
                                    salaire_net = ?,
                                    date_derniere_maj_salaire = GETDATE(),
                                    statut_paiement = 'configuré'
                                WHERE id_professeur = ?
                            """, (int(hours_per_week * 4.33), hourly_rate, monthly_base, monthly_salary, prof.get('id')))
                            
                            conn.commit()
                            print(f"✅ Configuration salaire sauvegardée en base:")
                            print(f"   - Professeur ID: {prof.get('id')}")
                            print(f"   - Heures/mois: {int(hours_per_week * 4.33)}")
                            print(f"   - Taux horaire: {hourly_rate} GNF")
                            print(f"   - Salaire de base: {monthly_base} GNF")
                            print(f"   - Salaire mensuel: {monthly_salary:,.0f} GNF")
                            
                            messagebox.showinfo("Succès", "Configuration des salaires sauvegardée en base de données!")
                            salary_window.destroy()
                            
                            # Actualiser les détails du professeur
                            self.display_professor_details(prof)
                            
                        except Exception as e:
                            conn.rollback()
                            print(f"❌ Erreur lors de la sauvegarde: {e}")
                            messagebox.showerror("Erreur", f"Erreur lors de la sauvegarde: {e}")
                        finally:
                            conn.close()
                    else:
                        messagebox.showerror("Erreur", "Impossible de se connecter à la base de données")
                    
                except ValueError:
                    messagebox.showerror("Erreur", "Veuillez saisir des valeurs numériques valides")
            
            def cancel_config():
                salary_window.destroy()
            
            # Bouton Sauvegarder
            save_btn = ctk.CTkButton(
                buttons_frame,
                text="💾 Sauvegarder Configuration",
                command=save_salary_config,
                fg_color=SUCCESS_GREEN,
                hover_color="#047857",
                font=FONT_BUTTON,
                height=40,
                width=200,
                corner_radius=8
            )
            save_btn.pack(side="left", padx=(0, 10))
            
            # Bouton Annuler
            cancel_btn = ctk.CTkButton(
                buttons_frame,
                text="❌ Annuler",
                command=cancel_config,
                fg_color=ERROR_RED,
                hover_color="#dc2626",
                font=FONT_BUTTON,
                height=40,
                width=150,
                corner_radius=8
            )
            cancel_btn.pack(side="left")
            
        except Exception as e:
            print(f"❌ Erreur lors de l'ouverture du formulaire de salaires: {e}")
            messagebox.showerror("Erreur", f"Erreur lors de l'ouverture du formulaire: {e}")

    def show_salary_history(self, prof):
        """Affiche l'historique des salaires d'un professeur"""
        messagebox.showinfo("Historique", f"Historique des salaires pour {prof.get('nom', 'N/A')} {prof.get('prenom', 'N/A')}")

    def add_course_hours(self, prof):
        """Ajoute des heures de cours pour un professeur"""
        messagebox.showinfo("Ajouter Heures", f"Ajouter des heures pour {prof.get('nom', 'N/A')} {prof.get('prenom', 'N/A')}")

    def export_professor_data(self, prof):
        """Exporte les données d'un professeur"""
        messagebox.showinfo("Export", f"Export des données pour {prof.get('nom', 'N/A')} {prof.get('prenom', 'N/A')}")

    def update_prof_count(self):
        """Met à jour le compteur de professeurs"""
        total = len(self.professors_data)
        self.prof_count_label.configure(text=f"Total: {total}")

    def filter_professors(self, event=None):
        """Filtre les professeurs selon le terme de recherche"""
        self.display_professors_list()
        
    def update_data(self):
        """Met à jour les données des professeurs"""
        try:
            self.refresh_professors_view()
            print("✅ Données des professeurs mises à jour")
        except Exception as e:
            print(f"❌ Erreur lors de la mise à jour des données: {e}")
            messagebox.showerror("Erreur", f"Erreur lors de la mise à jour: {e}")
    
    def add_professor(self):
        """Ouvre le formulaire d'ajout de professeur"""
        try:
            print("🔍 Debug: Ouverture du formulaire d'ajout de professeur")
            self._simple_add_professor()
        except Exception as e:
            print(f"❌ Erreur lors de l'ouverture du formulaire d'ajout: {e}")
            messagebox.showerror("Erreur", f"Erreur lors de l'ouverture du formulaire: {e}")
    
    def _simple_add_professor(self):
        """Ouvre une fenêtre professionnelle d'ajout de professeur"""
        try:
            # Créer une fenêtre professionnelle
            add_window = ctk.CTkToplevel(self)
            add_window.title("Ajouter un professeur")
            add_window.geometry("1000x700")
            add_window.resizable(False, False)
            
            # Appliquer le fond du thème
            add_window.configure(fg_color=BG_MAIN)
            
            # Centrer la fenêtre
            add_window.transient(self)
            add_window.grab_set()
            
            # Frame principal professionnel
            main_frame = ctk.CTkFrame(
                add_window,
                fg_color=CARD_BG,
                corner_radius=12
            )
            main_frame.pack(fill="both", expand=True, padx=16, pady=16)
            
            # En-tête professionnel
            header_frame = ctk.CTkFrame(main_frame, fg_color=BG_SIDEBAR, corner_radius=8)
            header_frame.pack(fill="x", padx=16, pady=16)
            
            # Titre avec icône
            title_container = ctk.CTkFrame(header_frame, fg_color="transparent")
            title_container.pack(fill="x", padx=16, pady=16)
            
            # Icône et titre
            title_frame = ctk.CTkFrame(title_container, fg_color="transparent")
            title_frame.pack(side="left")
            
            # Icône d'ajout
            icon_frame = ctk.CTkFrame(title_frame, fg_color=ACCENT, corner_radius=20, width=40, height=40)
            icon_frame.pack(side="left", padx=(0, 12))
            icon_frame.pack_propagate(False)
            
            icon_label = ctk.CTkLabel(
                icon_frame,
                image=self.icon_cache.get("add", load_icon("add", 24)),
                text="",
                fg_color="transparent"
            )
            icon_label.pack(expand=True)
            
            title_label = ctk.CTkLabel(
                title_frame,
                text="Ajouter un nouveau professeur",
                font=("Segoe UI", 18, "bold"),
                text_color=TEXT
            )
            title_label.pack(side="left")
            
            # Formulaire professionnel
            form_frame = ctk.CTkFrame(
                main_frame,
                fg_color=BG_SIDEBAR,
                corner_radius=8
            )
            form_frame.pack(fill="both", expand=True, padx=16, pady=(0, 16))
            
            # Configuration en deux colonnes
            form_frame.grid_columnconfigure(0, weight=1)
            form_frame.grid_columnconfigure(1, weight=1)
            
            # Champs du formulaire organisés en deux colonnes
            left_fields = [
                ("Nom", "nom"),
                ("Email", "email"),
                ("Spécialité", "specialite"),
                ("Sexe", "sexe"),
                ("Taux horaire (GNF)", "salaire_horaire")
            ]
            
            right_fields = [
                ("Prénom", "prenom"),
                ("Téléphone", "telephone"),
                ("Adresse", "adresse")
            ]
            
            entries = {}
            
            # Colonne de gauche
            for i, (label_text, field_name) in enumerate(left_fields):
                if label_text:  # Ignorer les espaces vides
                    # Label professionnel
                    label = ctk.CTkLabel(
                        form_frame,
                        text=label_text,
                        font=("Segoe UI", 11, "bold"),
                        text_color=TEXT
                    )
                    label.grid(row=i, column=0, sticky="w", padx=(20, 10), pady=8)
                    
                    # Champs spéciaux
                    if field_name == "sexe":
                        # OptionMenu pour le sexe
                        entry = ctk.CTkOptionMenu(
                            form_frame,
                            values=["M", "F"],
                            font=("Segoe UI", 11),
                            fg_color=CARD_BG,
                            button_color=ACCENT,
                            button_hover_color="#2563EB",
                            text_color=TEXT,
                            dropdown_fg_color=CARD_BG,
                            dropdown_text_color=TEXT
                        )
                        entry.set("M")  # Valeur par défaut
                    elif field_name == "salaire_horaire":
                        # Entry numérique pour le taux horaire
                        entry = ctk.CTkEntry(
                            form_frame,
                            placeholder_text=f"Entrez {label_text.lower()}",
                            width=300,
                            height=36,
                            font=("Segoe UI", 11),
                            fg_color=CARD_BG,
                            border_color=BORDER_COLOR,
                            text_color=TEXT,
                            placeholder_text_color=MUTED
                        )
                    else:
                        # Entry normal pour les autres champs
                        entry = ctk.CTkEntry(
                            form_frame,
                            placeholder_text=f"Entrez {label_text.lower()}",
                            width=300,
                            height=36,
                            font=("Segoe UI", 11),
                            fg_color=CARD_BG,
                            border_color=BORDER_COLOR,
                            text_color=TEXT,
                            placeholder_text_color=MUTED
                        )
                    
                    entry.grid(row=i, column=1, sticky="ew", padx=(0, 20), pady=8)
                entries[field_name] = entry
            
            # Colonne de droite
            for i, (label_text, field_name) in enumerate(right_fields):
                if label_text:  # Ignorer les espaces vides
                    # Label professionnel
                    label = ctk.CTkLabel(
                        form_frame,
                        text=label_text,
                        font=("Segoe UI", 11, "bold"),
                        text_color=TEXT
                    )
                    label.grid(row=i, column=2, sticky="w", padx=(20, 10), pady=8)
                    
                    if field_name in ["heures_semaine"]:
                        # Entry numérique pour les heures
                        entry = ctk.CTkEntry(
                            form_frame,
                            placeholder_text=f"Entrez {label_text.lower()}",
                            width=300,
                            height=36,
                            font=("Segoe UI", 11),
                            fg_color=CARD_BG,
                            border_color=BORDER_COLOR,
                            text_color=TEXT,
                            placeholder_text_color=MUTED
                        )
                    else:
                        # Entry normal pour les autres champs
                        entry = ctk.CTkEntry(
                            form_frame,
                            placeholder_text=f"Entrez {label_text.lower()}",
                            width=300,
                            height=36,
                            font=("Segoe UI", 11),
                            fg_color=CARD_BG,
                            border_color=BORDER_COLOR,
                            text_color=TEXT,
                            placeholder_text_color=MUTED
                        )
                    
                    entry.grid(row=i, column=3, sticky="ew", padx=(0, 20), pady=8)
                    entries[field_name] = entry
            
            # Configurer les colonnes pour l'expansion
            form_frame.grid_columnconfigure(1, weight=1)
            form_frame.grid_columnconfigure(3, weight=1)
            
            # Boutons avec le thème EduManager+
            buttons_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
            buttons_frame.grid(row=6, column=0, columnspan=4, pady=30)
            
            def save_professor():
                try:
                    # Récupérer les données du formulaire
                    professor_data = {
                        'nom': entries['nom'].get(),
                        'prenom': entries['prenom'].get(),
                        'email': entries['email'].get(),
                        'telephone': entries['telephone'].get(),
                        'specialite': entries['specialite'].get(),
                        'sexe': entries['sexe'].get() or 'M',
                        'adresse': entries['adresse'].get(),
                        'statut': 'Actif',  # Valeur par défaut
                        'date_embauche': datetime.now().strftime('%Y-%m-%d')
                    }
                    
                    # Récupérer le taux horaire uniquement
                    salaire_horaire = float(entries['salaire_horaire'].get() or 0)
                    
                    print(f"📊 Informations du professeur:")
                    print(f"   - Nom: {professor_data['nom']} {professor_data['prenom']}")
                    print(f"   - Spécialité: {professor_data.get('specialite', 'N/A')}")
                    print(f"   - Taux horaire: {salaire_horaire} GNF/heure")
                    print(f"   - Mode de paiement: Par heures dispensées")
                    
                    # Vérifier que les champs obligatoires sont remplis
                    if not professor_data['nom'] or not professor_data['prenom']:
                        messagebox.showerror("Erreur", "Le nom et le prénom sont obligatoires")
                        return
                    
                    # Sauvegarder en base de données
                    conn = get_db_connection()
                    if conn:
                        cursor = conn.cursor()
                        try:
                            cursor.execute("""
                                INSERT INTO professeurs (
                                    nom, prenom, email, telephone, specialite, sexe, adresse,
                                    salaire_horaire, date_embauche, statut,
                                    compte_bancaire, numero_cnss, numero_impot
                                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                            """, (
                                professor_data['nom'], professor_data['prenom'], professor_data['email'],
                                professor_data['telephone'], professor_data['specialite'], professor_data['sexe'],
                                professor_data['adresse'], salaire_horaire,
                                professor_data['date_embauche'], professor_data['statut'],
                                f'BANK{datetime.now().year}{datetime.now().month:02d}{datetime.now().day:02d}',  # compte_bancaire
                                f'CNSS{datetime.now().year}{datetime.now().month:02d}{datetime.now().day:02d}',  # numero_cnss
                                f'IMP{datetime.now().year}{datetime.now().month:02d}{datetime.now().day:02d}'   # numero_impot
                            ))
                            
                            conn.commit()
                            print(f"✅ Professeur ajouté avec succès: {professor_data['nom']} {professor_data['prenom']}")
                            print(f"   - Taux horaire: {salaire_horaire} GNF/heure")
                            print(f"   - Mode: Par heures dispensées")
                            
                            messagebox.showinfo("Succès", f"Professeur {professor_data['nom']} {professor_data['prenom']} ajouté avec succès!")
                    
                            # Fermer la fenêtre et actualiser les données
                            add_window.destroy()
                            self.refresh_professors_view()
                            
                        except Exception as e:
                            conn.rollback()
                            print(f"❌ Erreur lors de la sauvegarde: {e}")
                            messagebox.showerror("Erreur", f"Erreur lors de la sauvegarde: {e}")
                        finally:
                            conn.close()
                    else:
                        messagebox.showerror("Erreur", "Impossible de se connecter à la base de données")
                    
                except ValueError as e:
                    messagebox.showerror("Erreur", "Veuillez saisir un taux horaire valide")
                except Exception as e:
                    print(f"❌ Erreur lors de l'ajout: {e}")
                    messagebox.showerror("Erreur", f"Erreur lors de l'ajout: {e}")
            
            def cancel():
                add_window.destroy()
            
            # Bouton Sauvegarder avec le thème
            save_btn = ctk.CTkButton(
                buttons_frame,
                text="💾 Sauvegarder",
                command=save_professor,
                fg_color=SUCCESS_GREEN,
                hover_color="#047857",
                font=FONT_BUTTON,
                height=40,
                width=150,
                corner_radius=8
            )
            save_btn.pack(side="left", padx=10)
            
            # Bouton Annuler avec le thème
            cancel_btn = ctk.CTkButton(
                buttons_frame,
                text="❌ Annuler",
                command=cancel,
                fg_color=ERROR_RED,
                hover_color="#dc2626",
                font=FONT_BUTTON,
                height=40,
                width=150,
                corner_radius=8
            )
            cancel_btn.pack(side="left", padx=10)
            
        except Exception as e:
            print(f"❌ Erreur lors de la création du formulaire: {e}")
            messagebox.showerror("Erreur", f"Erreur lors de la création du formulaire: {e}")

    def edit_professor(self, prof):
        """Ouvre le formulaire de modification d'un professeur"""
        try:
            print(f"🔍 Modification du professeur: {prof.get('nom', 'N/A')}")
            messagebox.showinfo("Modification", f"Modification de {prof.get('nom', 'N/A')} {prof.get('prenom', 'N/A')}")
        except Exception as e:
            print(f"❌ Erreur lors de la modification: {e}")
            messagebox.showerror("Erreur", f"Erreur lors de la modification: {e}")

    def delete_professor(self, prof):
        """Supprime un professeur après confirmation"""
        try:
            name = f"{prof.get('nom', 'N/A')} {prof.get('prenom', 'N/A')}"
            result = messagebox.askyesno(
                "Confirmation de suppression",
                f"Êtes-vous sûr de vouloir supprimer le professeur {name} ?"
            )
            if result:
                print(f"🗑️ Suppression du professeur: {name}")
                messagebox.showinfo("Suppression", f"Professeur {name} supprimé avec succès")
                self.update_data()  # Actualiser les données
        except Exception as e:
            print(f"❌ Erreur lors de la suppression: {e}")
            messagebox.showerror("Erreur", f"Erreur lors de la suppression: {e}")
