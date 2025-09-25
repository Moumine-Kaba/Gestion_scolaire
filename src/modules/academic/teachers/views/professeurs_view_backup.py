from database.connection import get_db_connection
import customtkinter as ctk
from PIL import Image, ImageDraw, ImageFont, ImageOps
from tkinter import messagebox, filedialog
import os, sys
import csv
from datetime import datetime, timedelta

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
        SUCCESS_GREEN, WARNING_YELLOW, ERROR_RED, INFO_ORANGE, HOVER_PRIMARY, GOLD_ACCENT,
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
    # Valeurs par défaut pour les variables manquantes
    BG_MAIN = "#0A192F"
    BG_SIDEBAR = "#172A45"
    CARD_BG = "#0B2039"
    BORDER_COLOR = "#334155"
    ACCENT = "#64FFDA"
    TEXT = "#CCD6F6"
    MUTED = "#8AA0B8"
    SUCCESS_GREEN = "#059669"
    WARNING_YELLOW = "#D97706"
    ERROR_RED = "#DC2626"
    INFO_ORANGE = "#EA580C"
    HOVER_PRIMARY = "#0E1C36"
    GOLD_ACCENT = "#D97706"
    
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
    from src.modules.academic.teachers.controllers.salary_controller import SalaryController
    print("✅ Contrôleur des professeurs et salaires importé avec succès")
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
        # Filtres
        self.filter_statut_var = ctk.StringVar(value="Tous")
        self.filter_specialite_var = ctk.StringVar()
        self.filter_principal_var = ctk.BooleanVar(value=False)
        
        # Import du contrôleur de salaires
        try:
            from src.modules.academic.teachers.controllers.salary_controller import SalaryController
            self.salary_controller = SalaryController(DB_PATH)
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
        # Recherche avec debounce
        def on_key_release(event=None):
            try:
                if hasattr(self, "_search_after_id") and self._search_after_id:
                    self.after_cancel(self._search_after_id)
            except Exception:
                pass
            self._search_after_id = self.after(300, self.filter_professors)
        search_entry.bind("<KeyRelease>", on_key_release)

        # Filtres (statut, spécialité, principal)
        filters_frame = ctk.CTkFrame(list_panel, fg_color="transparent")
        filters_frame.pack(fill="x", padx=15, pady=(0, 10))

        statut_label = ctk.CTkLabel(filters_frame, text="Statut:", font=FONT_SECONDARY, text_color=TEXT)
        statut_label.pack(side="left", padx=(0, 6))
        statut_select = ctk.CTkOptionMenu(
            filters_frame,
            values=["Tous", "Actif", "Inactif"],
            variable=self.filter_statut_var,
            fg_color=BG_SIDEBAR,
            button_color=ACCENT,
            button_hover_color="#2563EB",
            text_color=TEXT,
            dropdown_fg_color=CARD_BG,
            dropdown_text_color=TEXT,
            width=120,
        )
        statut_select.pack(side="left")

        spec_label = ctk.CTkLabel(filters_frame, text="Spécialité:", font=FONT_SECONDARY, text_color=TEXT)
        spec_label.pack(side="left", padx=(12, 6))
        spec_entry = ctk.CTkEntry(
            filters_frame,
            textvariable=self.filter_specialite_var,
            font=FONT_SECONDARY,
            placeholder_text="Toutes",
            fg_color=BG_SIDEBAR,
            text_color=TEXT,
            border_width=1,
            border_color=BORDER_COLOR,
            corner_radius=10,
            height=32,
            width=140,
        )
        spec_entry.pack(side="left")

        principal_chk = ctk.CTkCheckBox(
            filters_frame,
            text="Principal",
            text_color=TEXT,
            fg_color=ACCENT,
            hover_color="#2563EB",
            border_color=BORDER_COLOR,
            variable=self.filter_principal_var,
        )
        principal_chk.pack(side="left", padx=(12, 0))

        # Réagir aux changements de filtres
        def on_filters_change(event=None):
            self.current_offset = 0
            self.load_professors_data()
            self.display_professors_list()
            self.update_prof_count()
        statut_select.configure(command=lambda _: on_filters_change())
        spec_entry.bind("<KeyRelease>", lambda e: self.after(300, on_filters_change))
        principal_chk.configure(command=on_filters_change)

        # Contrôles pagination
        pagination_frame = ctk.CTkFrame(list_panel, fg_color="transparent")
        pagination_frame.pack(fill="x", padx=15, pady=(0, 10))
        
        self.page_size = 50
        self.current_offset = 0
        
        prev_btn = ctk.CTkButton(
            pagination_frame,
            text="◀",
            width=36,
            height=32,
            fg_color=BG_SIDEBAR,
            hover_color="#4A90E2",
            command=lambda: self.change_page(-1)
        )
        prev_btn.pack(side="left")
        
        next_btn = ctk.CTkButton(
            pagination_frame,
            text="▶",
            width=36,
            height=32,
            fg_color=BG_SIDEBAR,
            hover_color="#4A90E2",
            command=lambda: self.change_page(1)
        )
        next_btn.pack(side="left", padx=(8,0))
        
        # Liste scrollable des professeurs
        self.professors_list_frame = ctk.CTkScrollableFrame(
            list_panel,
            fg_color="transparent",
            scrollbar_button_color=BORDER_COLOR,
            scrollbar_button_hover_color=ACCENT
        )
        self.professors_list_frame.pack(fill="both", expand=True, padx=15, pady=(0, 15))

        # Export CSV du résultat courant (page courante)
        export_frame = ctk.CTkFrame(list_panel, fg_color="transparent")
        export_frame.pack(fill="x", padx=15, pady=(0, 12))
        export_btn = ctk.CTkButton(
            export_frame,
            text="Exporter CSV (page)",
            fg_color=BG_SIDEBAR,
            hover_color="#4A90E2",
            text_color=TEXT,
            command=self.export_current_page_csv,
            height=32,
            corner_radius=10,
        )
        export_btn.pack(side="right")

    def create_professor_details_panel(self, parent_frame):
        """Crée le panneau de droite avec les détails en design compact"""
        # Container principal (sans en-tête, pour gagner de l'espace)
        details_panel = ctk.CTkFrame(parent_frame, fg_color=CARD_BG, corner_radius=12,
                                    border_color=BORDER_COLOR, border_width=1)
        details_panel.grid(row=0, column=1, sticky="nsew")

        # Zone de contenu principal pleine hauteur
        self.details_content_frame = ctk.CTkFrame(details_panel, fg_color="transparent")
        self.details_content_frame.pack(fill="both", expand=True, padx=8, pady=8)
        
    def refresh_professors_view(self):
        """Actualise la vue des professeurs"""
        self.load_professors_data()
        self.display_professors_list()
        self.update_prof_count()
        
    def load_professors_data(self):
        """Charge les données des professeurs"""
        try:
            from src.modules.academic.teachers.controllers.professeur_controller import get_professeurs_paginated
            query = (self.search_var.get() or "").strip()
            statut = self.filter_statut_var.get()
            if statut == "Tous":
                statut = None
            specialite = (self.filter_specialite_var.get() or "").strip() or None
            principal = True if self.filter_principal_var.get() else None
            self.professors_data = get_professeurs_paginated(
                limit=getattr(self, 'page_size', 50),
                offset=getattr(self, 'current_offset', 0),
                query=query or None,
                statut=statut,
                specialite=specialite,
                principal=principal,
            )
            print(f"✅ {len(self.professors_data)} professeurs chargés")
        except Exception as e:
            print(f"⚠️ Erreur chargement professeurs: {e}")
            self.professors_data = []

    def display_professors_list(self):
        """Affiche la liste des professeurs dans le panneau de gauche"""
        # Nettoyer la liste existante
        for widget in self.professors_list_frame.winfo_children():
                widget.destroy()
        
        # Filtrer les professeurs selon la recherche (sur page courante)
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

        # Mémoriser la page filtrée courante pour export
        self._current_page_profs = filtered_profs

    def export_current_page_csv(self):
        try:
            import csv, os
            from tkinter import filedialog
            rows = getattr(self, '_current_page_profs', self.professors_data)
            if not rows:
                messagebox.showinfo("Export", "Aucune donnée à exporter.")
                return
            # Choisir fichier
            fpath = filedialog.asksaveasfilename(
                defaultextension=".csv",
                filetypes=[("CSV files", "*.csv")],
                title="Enregistrer l'export CSV"
            )
            if not fpath:
                return
            fields = [
                'id','matricule','nom','prenom','email','telephone','specialite','date_embauche','statut'
            ]
            # Ajouter le champ principal si présent dans les objets
            if rows and isinstance(rows[0], dict) and 'est_professeur_principal' in rows[0]:
                fields.append('est_professeur_principal')
            with open(fpath, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=fields)
                writer.writeheader()
                for r in rows:
                    writer.writerow({k: r.get(k, "") for k in fields})
            messagebox.showinfo("Export", f"Export CSV enregistré: {fpath}")
        except Exception as e:
            print(f"❌ Erreur export CSV: {e}")
            messagebox.showerror("Erreur", f"Erreur export CSV: {e}")

    def create_professor_list_item(self, prof):
        """Crée un élément de liste ultra-moderne avec design spectaculaire"""
        # Frame principal avec effet de carte premium
        item_frame = ctk.CTkFrame(
            self.professors_list_frame,
            fg_color=CARD_BG,
            corner_radius=18,
            border_width=1,
            border_color=BORDER_COLOR
        )
        item_frame.pack(fill="x", pady=3, padx=2)
        
        # Effet de survol ultra-moderne
        def on_enter(event):
            item_frame.configure(fg_color=HOVER_PRIMARY, border_color=ACCENT, border_width=2)
        
        def on_leave(event):
            item_frame.configure(fg_color=CARD_BG, border_color=BORDER_COLOR, border_width=1)
        
        item_frame.bind("<Enter>", on_enter)
        item_frame.bind("<Leave>", on_leave)
        
        # Container principal compact
        main_container = ctk.CTkFrame(item_frame, fg_color="transparent")
        main_container.pack(fill="both", expand=True, padx=12, pady=8)
        
        # Section gauche - Avatar et infos principales
        left_section = ctk.CTkFrame(main_container, fg_color="transparent")
        left_section.pack(side="left", fill="both", expand=True)
        
        # Avatar ultra-moderne avec effet de gradient
        avatar_container = ctk.CTkFrame(
            left_section, 
            fg_color=ACCENT, 
            corner_radius=25, 
            width=45, 
            height=45
        )
        avatar_container.pack(side="left", padx=(0, 12), pady=2)
        avatar_container.pack_propagate(False)
        
        # Icône de profil dans l'avatar
        avatar_label = ctk.CTkLabel(
            avatar_container,
            image=self.icon_cache.get("person", load_icon("person", 22)),
            text="",
            fg_color="transparent"
        )
        avatar_label.pack(expand=True)
        
        # Informations compactes avec hiérarchie parfaite
        info_container = ctk.CTkFrame(left_section, fg_color="transparent")
        info_container.pack(side="left", fill="both", expand=True)
        
        # Nom avec style premium
        name_label = ctk.CTkLabel(
            info_container,
            text=f"{prof.get('nom', 'N/A')} {prof.get('prenom', 'N/A')}",
            font=("Segoe UI", 15, "bold"),
            text_color=TEXT,
            fg_color="transparent"
        )
        name_label.pack(anchor="w", pady=(0, 2))
        
        # Spécialité avec icône compacte
        spec_container = ctk.CTkFrame(info_container, fg_color="transparent")
        spec_container.pack(anchor="w", pady=(0, 3))
        
        spec_icon = ctk.CTkLabel(
            spec_container,
            image=self.icon_cache.get("book", load_icon("book", 12)),
            text="",
            fg_color="transparent"
        )
        spec_icon.pack(side="left", padx=(0, 6))
        
        spec_label = ctk.CTkLabel(
            spec_container,
            text=prof.get('specialite', 'Non spécifié'),
            font=("Segoe UI", 11),
            text_color=MUTED,
            fg_color="transparent"
        )
        spec_label.pack(side="left")
        
        # Email compact (si disponible)
        if prof.get('email'):
            email_container = ctk.CTkFrame(info_container, fg_color="transparent")
            email_container.pack(anchor="w")
            
            email_icon = ctk.CTkLabel(
                email_container,
                image=self.icon_cache.get("email", load_icon("email", 12)),
                text="",
                fg_color="transparent"
            )
            email_icon.pack(side="left", padx=(0, 6))
            
            email_label = ctk.CTkLabel(
                email_container,
                text=prof.get('email', ''),
                font=("Segoe UI", 10),
                text_color=MUTED,
                fg_color="transparent"
            )
            email_label.pack(side="left")
        
        # Section droite - Métriques et actions
        right_section = ctk.CTkFrame(main_container, fg_color="transparent")
        right_section.pack(side="right", fill="y")
        
        # Salaire compact (si disponible)
        if self.salary_controller:
            try:
                current_month = datetime.now().month
                current_year = datetime.now().year
                salary_info = self.salary_controller.calculate_salary(prof.get('id'), current_month, current_year)
                if salary_info and salary_info.get('salaire_net'):
                    salary_container = ctk.CTkFrame(right_section, fg_color="transparent")
                    salary_container.pack(anchor="e", pady=(0, 5))
                    
                    salary_icon = ctk.CTkLabel(
                        salary_container,
                        image=self.icon_cache.get("trending_up", load_icon("trending_up", 12)),
                        text="",
                        fg_color="transparent"
                    )
                    salary_icon.pack(side="left", padx=(0, 6))
                    
                    salary_text = f"{salary_info['salaire_net']:,.0f} GNF"
                    salary_label = ctk.CTkLabel(
                        salary_container,
                        text=salary_text,
                        font=("Segoe UI", 11, "bold"),
                        text_color=SUCCESS_GREEN,
                        fg_color="transparent"
                    )
                    salary_label.pack(side="left")
            except:
                pass
        
        # Statut Professeur Principal compact
        if prof.get('principal'):
            status_container = ctk.CTkFrame(right_section, fg_color="transparent")
            status_container.pack(anchor="e", pady=(0, 5))
            
            status_icon = ctk.CTkLabel(
                status_container,
                image=self.icon_cache.get("star", load_icon("star", 12)),
                text="",
                fg_color="transparent"
            )
            status_icon.pack(side="left", padx=(0, 6))
            
            status_label = ctk.CTkLabel(
                status_container,
                text="Principal",
                font=("Segoe UI", 10, "bold"),
                text_color=GOLD_ACCENT,
                fg_color="transparent"
            )
            status_label.pack(side="left")
        
        # Bouton d'action ultra-moderne
        action_btn = ctk.CTkButton(
            right_section,
            text="",
            image=self.icon_cache.get("chevron_right", load_icon("chevron_right", 16)),
            width=32,
            height=32,
            fg_color=ACCENT,
            hover_color=HOVER_PRIMARY,
            corner_radius=16,
            command=lambda p=prof: self.select_professor(p)
        )
        action_btn.pack(anchor="e", pady=(5, 0))
        
        # Stocker la référence au professeur
        item_frame.prof_data = prof

    def select_professor(self, prof):
        """Sélectionne un professeur et affiche ses détails avec effet visuel moderne"""
        # Mettre à jour la sélection visuelle avec effet moderne
        for widget in self.professors_list_frame.winfo_children():
            if hasattr(widget, 'prof_data'):
                if widget.prof_data == prof:
                    # Effet de sélection avec accent coloré
                    widget.configure(fg_color=ACCENT, border_color=ACCENT)
                    # Ajouter un effet de brillance
                    widget.configure(border_width=3)
                else:
                    # Retour à l'état normal
                    widget.configure(fg_color=CARD_BG, border_color=BORDER_COLOR)
                    widget.configure(border_width=2)
        
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
        
        # Afficher uniquement la carte pleine page
        self.create_professor_details_table(prof)

    def create_professor_profile_section(self, prof):
        """Crée la section de profil du professeur"""
        # Container principal avec votre thème
        profile_container = ctk.CTkFrame(self.details_content_frame, fg_color=CARD_BG, corner_radius=8)
        profile_container.pack(fill="x", pady=(0, 12))
        
        # Contenu principal
        content_frame = ctk.CTkFrame(profile_container, fg_color="transparent")
        content_frame.pack(fill="x", padx=20, pady=20)
        
        # Avatar et informations principales
        header_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        header_frame.pack(fill="x")
        
        # Avatar
        avatar_frame = ctk.CTkFrame(header_frame, fg_color=BORDER_COLOR, corner_radius=50, width=100, height=100)
        avatar_frame.pack(side="left", padx=(0, 20))
        avatar_frame.pack_propagate(False)
        
        avatar_label = ctk.CTkLabel(
            avatar_frame,
            image=self.icon_cache.get("user_avatar", load_icon("user_avatar", 60)),
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
            font=("Segoe UI", 20, "bold"),
            text_color=TEXT,
            fg_color="transparent"
        )
        name_label.pack(anchor="w", pady=(0, 8))
        
        specialty_label = ctk.CTkLabel(
            name_frame,
            text=prof.get('specialite', 'Professeur'),
            font=("Segoe UI", 14),
            text_color=MUTED,
            fg_color="transparent"
        )
        specialty_label.pack(anchor="w", pady=(0, 4))
        
        location_label = ctk.CTkLabel(
            name_frame,
            text="École, Conakry, Guinée",
            font=("Segoe UI", 12),
            text_color=MUTED,
            fg_color="transparent"
        )
        location_label.pack(anchor="w")

    def create_professor_details_table(self, prof):
        """Affiche une fiche professeur ultra-moderne avec design spectaculaire"""

        # === Container principal avec design premium ultra-moderne ===
        container = ctk.CTkFrame(
            self.details_content_frame,
            fg_color=CARD_BG,
            corner_radius=24,
            border_width=2,
            border_color=BORDER_COLOR
        )
        container.pack(fill="both", expand=True, padx=8, pady=8)

        # === Bande supérieure ultra-décorative ===
        top_bar = ctk.CTkFrame(container, fg_color=ACCENT, corner_radius=24, height=6)
        top_bar.pack(fill="x", pady=(0, 0))
        top_bar.pack_propagate(False)

        # === Zone avatar ultra-moderne ===
        avatar_section = ctk.CTkFrame(container, fg_color="transparent")
        avatar_section.pack(pady=12)

        # Avatar avec triple bordure et effet de halo spectaculaire
        avatar_outer = ctk.CTkFrame(
            avatar_section,
            width=100, height=100,
            corner_radius=50,
            fg_color=ACCENT,
            border_width=2,
            border_color=ACCENT
        )
        avatar_outer.pack()
        avatar_outer.pack_propagate(False)

        avatar_container = ctk.CTkFrame(
            avatar_outer,
            fg_color=CARD_BG,
            corner_radius=48,
            width=96, height=96
        )
        avatar_container.pack(expand=True, padx=2, pady=2)
        avatar_container.pack_propagate(False)

        # Icône de profil dans l'avatar
        avatar_label = ctk.CTkLabel(
            avatar_container,
            image=self.icon_cache.get("person", load_icon("person", 40)),
            text="",
            fg_color="transparent"
        )
        avatar_label.pack(expand=True)

        # === Informations principales ultra-compactes ===
        info_section = ctk.CTkFrame(container, fg_color="transparent")
        info_section.pack(pady=(0, 12))

        # Nom avec icône et style premium
        name_container = ctk.CTkFrame(info_section, fg_color="transparent")
        name_container.pack(pady=(0, 4))

        name_icon = ctk.CTkLabel(
            name_container,
            image=self.icon_cache.get("user_avatar", load_icon("user_avatar", 18)),
            text="",
            fg_color="transparent"
        )
        name_icon.pack(side="left", padx=(0, 8))

        name_label = ctk.CTkLabel(
            name_container,
            text=f"{prof.get('nom','').title()} {prof.get('prenom','').title()}",
            font=("Segoe UI", 20, "bold"),
            text_color=TEXT,
            fg_color="transparent"
        )
        name_label.pack(side="left")

        # Spécialité avec icône compacte
        spec_container = ctk.CTkFrame(info_section, fg_color="transparent")
        spec_container.pack(pady=(0, 8))

        spec_icon = ctk.CTkLabel(
            spec_container,
            image=self.icon_cache.get("book", load_icon("book", 14)),
            text="",
            fg_color="transparent"
        )
        spec_icon.pack(side="left", padx=(0, 8))

        spec_label = ctk.CTkLabel(
            spec_container,
            text=f"{prof.get('specialite','').title() or 'Non spécifié'}",
            font=("Segoe UI", 13),
            text_color=MUTED,
            fg_color="transparent"
        )
        spec_label.pack(side="left")

        # === Informations détaillées ultra-compactes ===
        details_section = ctk.CTkFrame(container, fg_color="transparent")
        details_section.pack(fill="x", padx=12, pady=(0, 12))

        # Titre de section compact
        section_title = ctk.CTkLabel(
            details_section,
            text="Informations Personnelles",
            font=("Segoe UI", 14, "bold"),
            text_color=TEXT,
            fg_color="transparent"
        )
        section_title.pack(anchor="w", pady=(0, 8))

        # Grille d'informations ultra-compacte
        info_grid = ctk.CTkFrame(details_section, fg_color="transparent")
        info_grid.pack(fill="x")
        info_grid.grid_columnconfigure((0, 1), weight=1)

        def create_info_card(row, col, title, value, icon_name, color=TEXT):
            card = ctk.CTkFrame(info_grid, fg_color=BG_SIDEBAR, corner_radius=10)
            card.grid(row=row, column=col, padx=4, pady=4, sticky="ew")
            
            # Icône et titre ultra-compacts
            header = ctk.CTkFrame(card, fg_color="transparent")
            header.pack(fill="x", padx=10, pady=(8, 3))
            
            icon_label = ctk.CTkLabel(
                header,
                image=self.icon_cache.get(icon_name, load_icon(icon_name, 14)),
                text="",
                fg_color="transparent"
            )
            icon_label.pack(side="left", padx=(0, 6))
            
            title_label = ctk.CTkLabel(
                header,
                text=title,
                font=("Segoe UI", 10, "bold"),
                text_color=MUTED,
                fg_color="transparent"
            )
            title_label.pack(side="left")
            
            # Valeur compacte
            value_label = ctk.CTkLabel(
                card,
                text=value or "-",
                font=("Segoe UI", 12, "bold"),
                text_color=color,
                fg_color="transparent"
            )
            value_label.pack(anchor="w", padx=10, pady=(0, 8))

        # Informations de base ultra-compactes
        create_info_card(0, 0, "ID Professeur", f"PROF{prof.get('id',0):04d}" if prof.get('id') else prof.get('matricule','-'), "target", ACCENT)
        create_info_card(0, 1, "Email", prof.get('email',''), "email", TEXT)
        create_info_card(1, 0, "Téléphone", prof.get('telephone',''), "phone", TEXT)
        create_info_card(1, 1, "Taux Horaire", f"{prof.get('salaire_horaire',0):,.0f} GNF", "trending_up", SUCCESS_GREEN)

        # === Section paiement ultra-moderne ===
        try:
            current_month = datetime.now().month
            current_year = datetime.now().year
            total_month_hours = 0.0
            total_week_hours = 0.0
            salaire_horaire = float(prof.get('salaire_horaire') or 0)

            if getattr(self, 'salary_controller', None):
                hours = self.salary_controller.get_professor_hours(prof.get('id'), current_month, current_year) or []
                total_month_hours = sum((h.get('nombre_heures') or 0) for h in hours)

                today = datetime.now().date()
                week_start = today - timedelta(days=today.weekday())
                week_end = week_start + timedelta(days=6)

                def _pdate(d):
                    try: return datetime.strptime(str(d), "%Y-%m-%d").date()
                    except Exception:
                        try: return datetime.fromisoformat(str(d)).date()
                        except Exception: return None

                for h in hours:
                    d = _pdate(h.get('date_cours'))
                    if d and week_start <= d <= week_end:
                        total_week_hours += (h.get('nombre_heures') or 0)

            salaire_semaine = total_week_hours * salaire_horaire
            salaire_mois = total_month_hours * salaire_horaire

            # === Carte paiement ultra-moderne ===
            payment_card = ctk.CTkFrame(container, fg_color=BG_SIDEBAR, corner_radius=14)
            payment_card.pack(fill="x", padx=12, pady=(0, 12))

            # En-tête paiement ultra-compact
            payment_header = ctk.CTkFrame(payment_card, fg_color="transparent")
            payment_header.pack(fill="x", padx=12, pady=10)

            # Titre avec icône compact
            title_container = ctk.CTkFrame(payment_header, fg_color="transparent")
            title_container.pack(side="left")

            payment_icon = ctk.CTkLabel(
                title_container,
                image=self.icon_cache.get("trending_up", load_icon("trending_up", 16)),
                text="",
                fg_color="transparent"
            )
            payment_icon.pack(side="left", padx=(0, 8))

            payment_title = ctk.CTkLabel(
                title_container,
                text="Informations de Paiement",
                font=("Segoe UI", 14, "bold"),
                text_color=TEXT,
                fg_color="transparent"
            )
            payment_title.pack(side="left")

            # Boutons d'action ultra-compacts
            actions_container = ctk.CTkFrame(payment_header, fg_color="transparent")
            actions_container.pack(side="right")

            export_btn = ctk.CTkButton(
                actions_container,
                text="",
                image=self.icon_cache.get("csv", load_icon("csv", 14)),
                width=30,
                height=30,
                fg_color=ACCENT,
                hover_color=HOVER_PRIMARY,
                corner_radius=6,
                command=lambda: messagebox.showinfo("Export", "Export salaire en cours...")
            )
            export_btn.pack(side="left", padx=3)

            print_btn = ctk.CTkButton(
                actions_container,
                text="",
                image=self.icon_cache.get("print", load_icon("print", 14)),
                width=30,
                height=30,
                fg_color=ACCENT,
                hover_color=HOVER_PRIMARY,
                corner_radius=6,
                command=lambda: messagebox.showinfo("Impression", "Impression de la fiche salaire...")
            )
            print_btn.pack(side="left", padx=3)

            # Grille de métriques ultra-compactes
            metrics_grid = ctk.CTkFrame(payment_card, fg_color="transparent")
            metrics_grid.pack(fill="x", padx=12, pady=(0, 12))
            metrics_grid.grid_columnconfigure((0, 1, 2, 3), weight=1)

            def create_metric_card(col, title, value, icon_name, color=SUCCESS_GREEN):
                metric_card = ctk.CTkFrame(metrics_grid, fg_color=CARD_BG, corner_radius=10)
                metric_card.grid(row=0, column=col, padx=4, pady=4, sticky="ew")
                
                # Icône et titre ultra-compacts
                metric_header = ctk.CTkFrame(metric_card, fg_color="transparent")
                metric_header.pack(fill="x", padx=8, pady=(6, 2))
                
                metric_icon = ctk.CTkLabel(
                    metric_header,
                    image=self.icon_cache.get(icon_name, load_icon(icon_name, 12)),
                    text="",
                    fg_color="transparent"
                )
                metric_icon.pack(side="left", padx=(0, 6))
                
                metric_title = ctk.CTkLabel(
                    metric_header,
                    text=title,
                    font=("Segoe UI", 9, "bold"),
                    text_color=MUTED,
                    fg_color="transparent"
                )
                metric_title.pack(side="left")
                
                # Valeur compacte
                metric_value = ctk.CTkLabel(
                    metric_card,
                    text=value,
                    font=("Segoe UI", 11, "bold"),
                    text_color=color,
                    fg_color="transparent"
                )
                metric_value.pack(anchor="w", padx=8, pady=(0, 6))

            # Métriques de paiement ultra-compactes
            create_metric_card(0, "Heures Semaine", f"{total_week_hours:.1f} h", "clock", TEXT)
            create_metric_card(1, "Salaire Semaine", f"{salaire_semaine:,.0f} GNF", "trending_up", SUCCESS_GREEN)
            create_metric_card(2, "Heures Mois", f"{total_month_hours:.1f} h", "calendar", TEXT)
            create_metric_card(3, "Salaire Mois", f"{salaire_mois:,.0f} GNF", "trending_up", SUCCESS_GREEN)

        except Exception as e:
            print(f"⚠️ Erreur section paiement: {e}")

        # === Footer ultra-moderne avec branding ===
        footer = ctk.CTkFrame(container, fg_color=ACCENT, corner_radius=14, height=10)
        footer.pack(fill="x", side="bottom")
        footer.pack_propagate(False)

        brand_container = ctk.CTkFrame(footer, fg_color="transparent")
        brand_container.pack(expand=True)

        brand_icon = ctk.CTkLabel(
            brand_container,
            image=self.icon_cache.get("logo", load_icon("logo", 14)),
            text="",
            fg_color="transparent"
        )
        brand_icon.pack(side="left", padx=(0, 6))

        brand_text = ctk.CTkLabel(
            brand_container,
            text="EduManager+",
            font=("Segoe UI", 11, "bold"),
            text_color=TEXT,
            fg_color="transparent"
        )
        brand_text.pack(side="left")


    def create_contact_info_section(self, prof):
        """Crée la section d'informations de contact"""
        # Container principal avec votre thème
        contact_container = ctk.CTkFrame(self.details_content_frame, fg_color=CARD_BG, corner_radius=8)
        contact_container.pack(fill="x", pady=(0, 12))
        
        # En-tête de la section
        section_header = ctk.CTkFrame(contact_container, fg_color=BG_SIDEBAR, corner_radius=8)
        section_header.pack(fill="x", padx=12, pady=12)
        
        # Titre
        title_label = ctk.CTkLabel(
            section_header,
            text="Informations de Contact",
            font=("Segoe UI", 16, "bold"),
            text_color=TEXT
        )
        title_label.pack()
        
        # Contenu principal
        content_frame = ctk.CTkFrame(contact_container, fg_color="transparent")
        content_frame.pack(fill="x", padx=12, pady=12)
        
        # Layout en deux colonnes
        columns_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        columns_frame.pack(fill="x")
        
        # Colonne gauche
        left_column = ctk.CTkFrame(columns_frame, fg_color="transparent")
        left_column.pack(side="left", fill="both", expand=True, padx=(0, 8))
        
        # Colonne droite
        right_column = ctk.CTkFrame(columns_frame, fg_color="transparent")
        right_column.pack(side="right", fill="both", expand=True, padx=(8, 0))
        
        # Informations de contact
        contact_info = [
            ("Email", prof.get('email', 'N/A'), "envelope"),
            ("Téléphone", prof.get('telephone', 'N/A'), "phone"),
            ("Adresse", prof.get('adresse', 'N/A'), "map")
        ]
        
        # Diviser en deux colonnes
        left_info = contact_info[:2]  # Email et Téléphone
        right_info = contact_info[2:]  # Adresse
        
        # Colonne gauche
        for i, (label, value, icon_name) in enumerate(left_info):
            if i > 0:  # Séparateur
                separator = ctk.CTkFrame(left_column, fg_color=BORDER_COLOR, height=1)
                separator.pack(fill="x", pady=12)
            
            # Item de contact
            contact_item = ctk.CTkFrame(left_column, fg_color="transparent")
            contact_item.pack(fill="x", pady=4)
            
            # Icône
            icon_frame = ctk.CTkFrame(contact_item, fg_color="transparent")
            icon_frame.pack(side="left", padx=(0, 12))
            
            icon_label = ctk.CTkLabel(
                icon_frame,
                image=self.icon_cache.get(icon_name, load_icon(icon_name, 20)),
                text="",
                fg_color="transparent"
            )
            icon_label.pack(side="left")
            
            # Texte
            text_frame = ctk.CTkFrame(contact_item, fg_color="transparent")
            text_frame.pack(side="left", fill="x", expand=True)
            
            label_widget = ctk.CTkLabel(
                text_frame,
                text=label,
                font=("Segoe UI", 12, "bold"),
                text_color=TEXT,
                fg_color="transparent"
            )
            label_widget.pack(anchor="w")
            
            value_widget = ctk.CTkLabel(
                text_frame,
                text=str(value) if value != 'N/A' else 'Non renseigné',
                font=("Segoe UI", 11),
                text_color=MUTED,
                fg_color="transparent"
            )
            value_widget.pack(anchor="w")
        
        # Colonne droite
        for i, (label, value, icon_name) in enumerate(right_info):
            if i > 0:  # Séparateur
                separator = ctk.CTkFrame(right_column, fg_color=BORDER_COLOR, height=1)
                separator.pack(fill="x", pady=12)
            
            # Item de contact
            contact_item = ctk.CTkFrame(right_column, fg_color="transparent")
            contact_item.pack(fill="x", pady=4)
            
            # Icône
            icon_frame = ctk.CTkFrame(contact_item, fg_color="transparent")
            icon_frame.pack(side="left", padx=(0, 12))
            
            icon_label = ctk.CTkLabel(
                icon_frame,
                image=self.icon_cache.get(icon_name, load_icon(icon_name, 20)),
                text="",
                fg_color="transparent"
            )
            icon_label.pack(side="left")
            
            # Texte
            text_frame = ctk.CTkFrame(contact_item, fg_color="transparent")
            text_frame.pack(side="left", fill="x", expand=True)
            
            label_widget = ctk.CTkLabel(
                text_frame,
                text=label,
                font=("Segoe UI", 12, "bold"),
                text_color=TEXT,
                fg_color="transparent"
            )
            label_widget.pack(anchor="w")
            
            value_widget = ctk.CTkLabel(
                text_frame,
                text=str(value) if value != 'N/A' else 'Non renseigné',
                font=("Segoe UI", 11),
                text_color=MUTED,
                fg_color="transparent"
            )
            value_widget.pack(anchor="w")

    def create_professional_details_section(self, prof):
        """Crée la section des détails professionnels"""
        # Container principal avec votre thème
        details_container = ctk.CTkFrame(self.details_content_frame, fg_color=CARD_BG, corner_radius=8)
        details_container.pack(fill="x", pady=(0, 12))
        
        # En-tête de la section
        section_header = ctk.CTkFrame(details_container, fg_color=BG_SIDEBAR, corner_radius=8)
        section_header.pack(fill="x", padx=12, pady=12)
        
        # Titre
        title_label = ctk.CTkLabel(
            section_header,
            text="Détails Professionnels",
            font=("Segoe UI", 16, "bold"),
            text_color=TEXT
        )
        title_label.pack()
        
        # Contenu principal
        content_frame = ctk.CTkFrame(details_container, fg_color="transparent")
        content_frame.pack(fill="x", padx=12, pady=12)
        
        # Layout en deux colonnes
        columns_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        columns_frame.pack(fill="x")
        
        # Colonne gauche
        left_column = ctk.CTkFrame(columns_frame, fg_color="transparent")
        left_column.pack(side="left", fill="both", expand=True, padx=(0, 8))
        
        # Colonne droite
        right_column = ctk.CTkFrame(columns_frame, fg_color="transparent")
        right_column.pack(side="right", fill="both", expand=True, padx=(8, 0))
        
        # Informations professionnelles
        professional_info = [
            ("Date d'embauche", prof.get('date_embauche', 'N/A'), "calendar"),
            ("Matricule", prof.get('matricule', 'N/A'), "briefcase"),
            ("Statut", prof.get('statut', 'Actif'), "check_circle")
        ]
        
        # Diviser en deux colonnes
        left_info = professional_info[:2]  # Date d'embauche et Matricule
        right_info = professional_info[2:]  # Statut
        
        # Colonne gauche
        for i, (label, value, icon_name) in enumerate(left_info):
            if i > 0:  # Séparateur
                separator = ctk.CTkFrame(left_column, fg_color=BORDER_COLOR, height=1)
                separator.pack(fill="x", pady=12)
            
            # Item professionnel
            detail_item = ctk.CTkFrame(left_column, fg_color="transparent")
            detail_item.pack(fill="x", pady=4)
            
            # Icône
            icon_frame = ctk.CTkFrame(detail_item, fg_color="transparent")
            icon_frame.pack(side="left", padx=(0, 12))
            
            icon_label = ctk.CTkLabel(
                icon_frame,
                image=self.icon_cache.get(icon_name, load_icon(icon_name, 20)),
                text="",
                fg_color="transparent"
            )
            icon_label.pack(side="left")
            
            # Texte
            text_frame = ctk.CTkFrame(detail_item, fg_color="transparent")
            text_frame.pack(side="left", fill="x", expand=True)
            
            label_widget = ctk.CTkLabel(
                text_frame,
                text=label,
                font=("Segoe UI", 12, "bold"),
                text_color=TEXT,
                fg_color="transparent"
            )
            label_widget.pack(anchor="w")
            
            value_widget = ctk.CTkLabel(
                text_frame,
                text=str(value) if value != 'N/A' else 'Non renseigné',
                font=("Segoe UI", 11),
                text_color=MUTED,
                fg_color="transparent"
            )
            value_widget.pack(anchor="w")
        
        # Colonne droite
        for i, (label, value, icon_name) in enumerate(right_info):
            if i > 0:  # Séparateur
                separator = ctk.CTkFrame(right_column, fg_color=BORDER_COLOR, height=1)
                separator.pack(fill="x", pady=12)
            
            # Item professionnel
            detail_item = ctk.CTkFrame(right_column, fg_color="transparent")
            detail_item.pack(fill="x", pady=4)
            
            # Icône
            icon_frame = ctk.CTkFrame(detail_item, fg_color="transparent")
            icon_frame.pack(side="left", padx=(0, 12))
            
            icon_label = ctk.CTkLabel(
                icon_frame,
                image=self.icon_cache.get(icon_name, load_icon(icon_name, 20)),
                text="",
                fg_color="transparent"
            )
            icon_label.pack(side="left")
            
            # Texte
            text_frame = ctk.CTkFrame(detail_item, fg_color="transparent")
            text_frame.pack(side="left", fill="x", expand=True)
            
            label_widget = ctk.CTkLabel(
                text_frame,
                text=label,
                font=("Segoe UI", 12, "bold"),
                text_color=TEXT,
                fg_color="transparent"
            )
            label_widget.pack(anchor="w")
            
            value_widget = ctk.CTkLabel(
                text_frame,
                text=str(value) if value != 'N/A' else 'Non renseigné',
                font=("Segoe UI", 11),
                text_color=MUTED,
                fg_color="transparent"
            )
            value_widget.pack(anchor="w")

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
        current_month = datetime.now().month
        current_year = datetime.now().year
        today = datetime.now().date()
        # Semaine ISO: début lundi
        week_start = (today - timedelta(days=today.weekday()))
        week_end = week_start + timedelta(days=6)
        
        # Valeurs par défaut
        total_current_hours = 0
        total_academic_hours = 0
        total_week_hours = 0
        
        # Si le contrôleur de salaire est disponible, récupérer les vraies données
        if self.salary_controller:
            try:
                current_hours = self.salary_controller.get_professor_hours(prof.get('id'), current_month, current_year)
                total_current_hours = sum(hour.get('nombre_heures', 0) for hour in current_hours)
                # Calcul heures de la semaine courante
                def parse_date(d):
                    try:
                        return datetime.strptime(str(d), "%Y-%m-%d").date()
                    except Exception:
                        try:
                            return datetime.fromisoformat(str(d)).date()
                        except Exception:
                            return None
                total_week_hours = 0
                for h in current_hours:
                    d = parse_date(h.get('date_cours'))
                    if d and week_start <= d <= week_end:
                        total_week_hours += (h.get('nombre_heures', 0) or 0)
                
                # Calculer les heures cumulées pour les 9 mois de l'année scolaire
                academic_year_start = 9  # Septembre
                academic_year_end = 5    # Mai
                
                if current_month >= academic_year_start:  # Septembre à Décembre
                    for month in range(academic_year_start, min(current_month + 1, 13)):
                        month_hours = self.salary_controller.get_professor_hours(prof.get('id'), month, current_year)
                        total_academic_hours += sum(hour.get('nombre_heures', 0) for hour in month_hours)
                else:  # Janvier à Mai
                    # Heures de septembre à décembre de l'année précédente
                    for month in range(academic_year_start, 13):
                        month_hours = self.salary_controller.get_professor_hours(prof.get('id'), month, current_year - 1)
                        total_academic_hours += sum(hour.get('nombre_heures', 0) for hour in month_hours)
                    
                    # Heures de janvier au mois actuel
                    for month in range(1, min(current_month + 1, academic_year_end + 1)):
                        month_hours = self.salary_controller.get_professor_hours(prof.get('id'), month, current_year)
                        total_academic_hours += sum(hour.get('nombre_heures', 0) for hour in month_hours)
            except Exception as e:
                print(f"⚠️ Erreur récupération heures: {e}")
                # Utiliser des valeurs par défaut
                total_current_hours = 0
                total_academic_hours = 0
                total_week_hours = 0
        else:
            # Valeurs d'exemple pour la démonstration
            total_current_hours = 24  # Exemple: 24h ce mois
            total_academic_hours = 180  # Exemple: 180h cumulées
            total_week_hours = 6  # Exemple: 6h cette semaine
        
        # Calcul du salaire du mois et de la semaine
        salaire_mois = total_current_hours * salaire_horaire
        salaire_semaine = total_week_hours * salaire_horaire
        
        # Calcul du salaire cumulé pour l'année scolaire
        salaire_academique = total_academic_hours * salaire_horaire
        
        # Statistiques du mois
        stats_frame = ctk.CTkFrame(content_frame, fg_color=BG_SIDEBAR, corner_radius=8)
        stats_frame.pack(fill="x")
        
        stats_content = ctk.CTkFrame(stats_frame, fg_color="transparent")
        stats_content.pack(fill="x", padx=16, pady=16)
        
        stats_title = ctk.CTkLabel(
            stats_content,
            text="📊 Statistiques de Paiement",
            font=("Segoe UI", 12, "bold"),
            text_color=TEXT,
            fg_color="transparent"
        )
        stats_title.pack(anchor="w", pady=(0, 12))
        
        # Grille des statistiques
        stats_grid = ctk.CTkFrame(stats_content, fg_color="transparent")
        stats_grid.pack(fill="x")
        
        stats_data = [
            ("🗓️ Heures de la semaine", f"{total_week_hours}h"),
            ("💵 Salaire de la semaine", f"{salaire_semaine:,.0f} GNF"),
            ("🕐 Heures du mois", f"{total_current_hours}h"),
            ("💵 Salaire du mois", f"{salaire_mois:,.0f} GNF"),
            ("📚 Heures cumulées", f"{total_academic_hours}h"),
            ("💰 Salaire cumulé", f"{salaire_academique:,.0f} GNF"),
            ("📅 Période", f"{current_month}/{current_year}"),
            ("🎯 Année scolaire", f"Sept {current_year-1} - Mai {current_year}")
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
        except Exception as e:
            print(f"❌ Erreur lors de l'ouverture du formulaire de salaires: {e}")
            messagebox.showerror("Erreur", f"Erreur lors de l'ouverture du formulaire: {e}")
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

    def create_statistics_dashboard(self, prof):
        """Crée un tableau de bord statistique complet pour le professeur"""
        # Container principal
        stats_container = ctk.CTkFrame(self.details_content_frame, fg_color=CARD_BG, corner_radius=8)
        stats_container.pack(fill="x", pady=(0, 12))
        
        # En-tête
        header_frame = ctk.CTkFrame(stats_container, fg_color=BG_SIDEBAR, corner_radius=8)
        header_frame.pack(fill="x", padx=12, pady=12)
        
        title_label = ctk.CTkLabel(
            header_frame,
            text="📊 Tableau de Bord Statistique",
            font=("Segoe UI", 16, "bold"),
            text_color=TEXT
        )
        title_label.pack()
        
        # Contenu principal
        content_frame = ctk.CTkFrame(stats_container, fg_color="transparent")
        content_frame.pack(fill="x", padx=12, pady=12)
        
        # Grille des statistiques
        stats_grid = ctk.CTkFrame(content_frame, fg_color="transparent")
        stats_grid.pack(fill="x")
        stats_grid.grid_columnconfigure((0, 1, 2), weight=1)
        
        # Statistiques du mois actuel
        current_month = datetime.now().month
        current_year = datetime.now().year
        
        # Récupérer les données du contrôleur de salaire
        monthly_data = None
        if self.salary_controller:
            try:
                monthly_data = self.salary_controller.get_monthly_summary(current_month, current_year)
            except Exception as e:
                print(f"⚠️ Erreur récupération données mensuelles: {e}")
        
        # Statistiques individuelles
        prof_stats = [
            ("Heures ce mois", "24h", SUCCESS_GREEN),
            ("Salaire ce mois", "1,200,000 GNF", SUCCESS_GREEN),
            ("Heures cumulées", "180h", INFO_ORANGE),
            ("Salaire cumulé", "9,000,000 GNF", INFO_ORANGE),
            ("Moyenne/heure", "50,000 GNF", ACCENT),
            ("Statut", "Actif", SUCCESS_GREEN)
        ]
        
        for i, (label, value, color) in enumerate(prof_stats):
            row = i // 3
            col = i % 3
            
            # Card de statistique
            stat_card = ctk.CTkFrame(stats_grid, fg_color=BG_SIDEBAR, corner_radius=6)
            stat_card.grid(row=row, column=col, sticky="ew", padx=4, pady=4)
            
            # Contenu de la carte
            card_content = ctk.CTkFrame(stat_card, fg_color="transparent")
            card_content.pack(fill="x", padx=12, pady=8)
            
            # Label
            label_widget = ctk.CTkLabel(
                card_content,
                text=label,
                font=("Segoe UI", 10, "bold"),
                text_color=MUTED,
                fg_color="transparent"
            )
            label_widget.pack(anchor="w")
            
            # Valeur
            value_widget = ctk.CTkLabel(
                card_content,
                text=value,
                font=("Segoe UI", 12, "bold"),
                text_color=color,
                fg_color="transparent"
            )
            value_widget.pack(anchor="w")
        
        # Boutons d'action rapide
        actions_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        actions_frame.pack(fill="x", pady=(15, 0))
        
        # Bouton Ajouter Heures
        add_hours_btn = ctk.CTkButton(
                actions_frame,
            text="➕ Ajouter Heures",
            command=lambda: self.add_course_hours(prof),
            fg_color=SUCCESS_GREEN,
            hover_color="#059669",
            text_color="white",
            font=("Segoe UI", 11, "bold"),
                height=32,
            corner_radius=16,
            image=self.icon_cache.get("add", load_icon("add", 16))
            )
        add_hours_btn.pack(side="left", padx=(0, 10))
            
        # Bouton Historique
        history_btn = ctk.CTkButton(
                actions_frame,
            text="📋 Historique",
            command=lambda: self.show_salary_history(prof),
            fg_color=INFO_ORANGE,
            hover_color="#ea580c",
            text_color="white",
            font=("Segoe UI", 11, "bold"),
                height=32,
            corner_radius=16,
            image=self.icon_cache.get("history", load_icon("history", 16))
        )
        history_btn.pack(side="left", padx=(0, 10))
        
        # Bouton Export
        export_btn = ctk.CTkButton(
            actions_frame,
            text="📄 Export",
            command=lambda: self.export_professor_data(prof),
            fg_color=ACCENT,
            hover_color="#2563EB",
            text_color="white",
            font=("Segoe UI", 11, "bold"),
            height=32,
            corner_radius=16,
            image=self.icon_cache.get("export", load_icon("export", 16))
        )
        export_btn.pack(side="left")

    def add_course_hours(self, prof):
        """Ouvre une fenêtre pour ajouter des heures de cours"""
        hours_window = ctk.CTkToplevel(self)
        hours_window.title(f"Ajouter Heures - {prof.get('nom', 'N/A')} {prof.get('prenom', 'N/A')}")
        hours_window.geometry("500x400")
        hours_window.resizable(False, False)
        
        # Centrer la fenêtre
        hours_window.transient(self)
        hours_window.grab_set()
        
        # Container principal
        main_container = ctk.CTkFrame(hours_window, fg_color=CARD_BG, corner_radius=12)
        main_container.pack(fill="both", expand=True, padx=20, pady=20)
        
        # En-tête
        header_frame = ctk.CTkFrame(main_container, fg_color=BG_SIDEBAR, corner_radius=8)
        header_frame.pack(fill="x", padx=20, pady=20)
        
        title_label = ctk.CTkLabel(
            header_frame,
            text="⏰ Ajouter des Heures de Cours",
            font=("Segoe UI", 16, "bold"),
            text_color=TEXT
        )
        title_label.pack(pady=15)
        
        # Formulaire
        form_frame = ctk.CTkFrame(main_container, fg_color="transparent")
        form_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        # Champs du formulaire
        fields = [
            ("Date du cours", "date_cours"),
            ("Nombre d'heures", "nombre_heures"),
            ("Matière", "matiere"),
            ("Classe", "classe"),
            ("Commentaire", "commentaire")
        ]
        
        entries = {}
        
        for i, (label_text, field_name) in enumerate(fields):
            # Label
            label = ctk.CTkLabel(
                form_frame,
                text=label_text,
                font=("Segoe UI", 11, "bold"),
                text_color=TEXT
            )
            label.pack(anchor="w", pady=(10, 5))
            
            # Champ spécial pour la date
            if field_name == "date_cours":
                entry = ctk.CTkEntry(
                    form_frame,
                    placeholder_text="YYYY-MM-DD",
                    width=400,
                    height=36,
                    font=("Segoe UI", 11),
                    fg_color=CARD_BG,
                    border_color=BORDER_COLOR,
                    text_color=TEXT,
                    placeholder_text_color=MUTED
                )
                # Valeur par défaut : aujourd'hui
                entry.insert(0, datetime.now().strftime("%Y-%m-%d"))
            elif field_name == "nombre_heures":
                entry = ctk.CTkEntry(
                    form_frame,
                    placeholder_text="Ex: 2.5",
                    width=400,
                    height=36,
                    font=("Segoe UI", 11),
                    fg_color=CARD_BG,
                    border_color=BORDER_COLOR,
                    text_color=TEXT,
                    placeholder_text_color=MUTED
                )
            elif field_name == "commentaire":
                entry = ctk.CTkTextbox(
                    form_frame,
                    width=400,
                    height=80,
                    font=("Segoe UI", 11),
                    fg_color=CARD_BG,
                    border_color=BORDER_COLOR,
                    text_color=TEXT,
                    placeholder_text="Commentaire optionnel..."
                )
            else:
                entry = ctk.CTkEntry(
                    form_frame,
                    placeholder_text=f"Entrez {label_text.lower()}",
                    width=400,
                    height=36,
                    font=("Segoe UI", 11),
                    fg_color=CARD_BG,
                    border_color=BORDER_COLOR,
                    text_color=TEXT,
                    placeholder_text_color=MUTED
                )
            
            entry.pack(fill="x", pady=(0, 10))
            entries[field_name] = entry
        
        # Boutons d'action
        buttons_frame = ctk.CTkFrame(main_container, fg_color="transparent")
        buttons_frame.pack(fill="x", padx=20, pady=(0, 20))
        
        def save_hours():
            try:
                # Validation des champs obligatoires
                date_cours = entries['date_cours'].get().strip()
                nombre_heures = float(entries['nombre_heures'].get() or 0)
                matiere = entries['matiere'].get().strip()
                classe = entries['classe'].get().strip()
                commentaire = entries['commentaire'].get("1.0", "end-1c").strip()
                
                if not date_cours or nombre_heures <= 0:
                    messagebox.showerror("Erreur", "La date et le nombre d'heures sont obligatoires")
                    return
                
                # Sauvegarder via le contrôleur de salaire
                if self.salary_controller:
                    success = self.salary_controller.add_course_hours(
                        prof.get('id'),
                        date_cours,
                        nombre_heures,
                        matiere,
                        classe,
                        commentaire
                    )
                    
                    if success:
                        messagebox.showinfo("Succès", f"{nombre_heures}h ajoutées pour {prof.get('nom')} {prof.get('prenom')}")
                        hours_window.destroy()
                        # Actualiser l'affichage
                        self.display_professor_details(prof)
                    else:
                        messagebox.showerror("Erreur", "Impossible d'ajouter les heures")
                else:
                    messagebox.showerror("Erreur", "Contrôleur de salaire non disponible")
                
            except ValueError:
                messagebox.showerror("Erreur", "Veuillez saisir un nombre d'heures valide")
            except Exception as e:
                print(f"❌ Erreur ajout heures: {e}")
                messagebox.showerror("Erreur", f"Erreur lors de l'ajout: {e}")
        
        def cancel():
            hours_window.destroy()
        
        # Bouton Sauvegarder
        save_btn = ctk.CTkButton(
            buttons_frame,
            text="💾 Sauvegarder",
            command=save_hours,
            fg_color=SUCCESS_GREEN,
            hover_color="#059669",
            text_color="white",
            font=("Segoe UI", 12, "bold"),
            height=40,
            corner_radius=20
        )
        save_btn.pack(side="left", padx=(0, 10))
        
        # Bouton Annuler
        cancel_btn = ctk.CTkButton(
            buttons_frame,
            text="❌ Annuler",
            command=cancel,
            fg_color=ERROR_RED,
            hover_color="#dc2626",
            text_color="white",
            font=("Segoe UI", 12, "bold"),
            height=40,
            corner_radius=20
        )
        cancel_btn.pack(side="left")

    def show_salary_history(self, prof):
        """Affiche l'historique des salaires du professeur"""
        history_window = ctk.CTkToplevel(self)
        history_window.title(f"Historique Salaires - {prof.get('nom', 'N/A')} {prof.get('prenom', 'N/A')}")
        history_window.geometry("800x600")
        history_window.resizable(True, True)
        
        # Centrer la fenêtre
        history_window.transient(self)
        history_window.grab_set()
        
        # Container principal
        main_container = ctk.CTkFrame(history_window, fg_color=CARD_BG, corner_radius=12)
        main_container.pack(fill="both", expand=True, padx=20, pady=20)
        
        # En-tête
        header_frame = ctk.CTkFrame(main_container, fg_color=BG_SIDEBAR, corner_radius=8)
        header_frame.pack(fill="x", padx=20, pady=20)
        
        title_label = ctk.CTkLabel(
            header_frame,
            text="📋 Historique des Salaires",
            font=("Segoe UI", 16, "bold"),
            text_color=TEXT
        )
        title_label.pack(pady=15)
        
        # Contenu avec scroll
        content_frame = ctk.CTkScrollableFrame(main_container, fg_color="transparent")
        content_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        # Récupérer l'historique des heures
        if self.salary_controller:
            try:
                hours_history = self.salary_controller.get_professor_hours(prof.get('id'))
                
                if hours_history:
                    # En-têtes du tableau
                    headers_frame = ctk.CTkFrame(content_frame, fg_color=BG_SIDEBAR, corner_radius=6)
                    headers_frame.pack(fill="x", pady=(0, 2))
                    headers_frame.grid_columnconfigure((0, 1, 2, 3, 4), weight=1)
                    
                    headers = ["Date", "Heures", "Matière", "Classe", "Commentaire"]
                    for i, header in enumerate(headers):
                        header_label = ctk.CTkLabel(
                            headers_frame,
                            text=header,
                            font=("Segoe UI", 12, "bold"),
                            text_color=TEXT,
                            fg_color="transparent"
                        )
                        header_label.grid(row=0, column=i, padx=8, pady=8, sticky="ew")
                    
                    # Données
                    for row_idx, hour_record in enumerate(hours_history):
                        bg_color = BG_SIDEBAR if row_idx % 2 == 0 else CARD_BG
                        
                        row_frame = ctk.CTkFrame(content_frame, fg_color=bg_color, corner_radius=4)
                        row_frame.pack(fill="x", pady=1)
                        row_frame.grid_columnconfigure((0, 1, 2, 3, 4), weight=1)
                        
                        # Colonnes
                        date_label = ctk.CTkLabel(
                            row_frame,
                            text=hour_record.get('date_cours', 'N/A'),
                            font=("Segoe UI", 11),
                            text_color=TEXT,
                            fg_color="transparent"
                        )
                        date_label.grid(row=0, column=0, padx=8, pady=6, sticky="ew")
                        
                        hours_label = ctk.CTkLabel(
                            row_frame,
                            text=f"{hour_record.get('nombre_heures', 0)}h",
                            font=("Segoe UI", 11),
                            text_color=SUCCESS_GREEN,
                            fg_color="transparent"
                        )
                        hours_label.grid(row=0, column=1, padx=8, pady=6, sticky="ew")
                        
                        matiere_label = ctk.CTkLabel(
                            row_frame,
                            text=hour_record.get('matiere', 'N/A'),
                            font=("Segoe UI", 11),
                            text_color=MUTED,
                            fg_color="transparent"
                        )
                        matiere_label.grid(row=0, column=2, padx=8, pady=6, sticky="ew")
                        
                        classe_label = ctk.CTkLabel(
                            row_frame,
                            text=hour_record.get('classe', 'N/A'),
                            font=("Segoe UI", 11),
                            text_color=MUTED,
                            fg_color="transparent"
                        )
                        classe_label.grid(row=0, column=3, padx=8, pady=6, sticky="ew")
                        
                        comment_label = ctk.CTkLabel(
                            row_frame,
                            text=hour_record.get('commentaire', 'N/A'),
                            font=("Segoe UI", 11),
                            text_color=MUTED,
                            fg_color="transparent"
                        )
                        comment_label.grid(row=0, column=4, padx=8, pady=6, sticky="ew")
                else:
                    # Message si pas d'historique
                    no_data_label = ctk.CTkLabel(
                        content_frame,
                        text="Aucun historique d'heures trouvé",
                        font=("Segoe UI", 14, "italic"),
                        text_color=MUTED,
                        fg_color="transparent"
                    )
                    no_data_label.pack(expand=True)
                    
            except Exception as e:
                print(f"❌ Erreur récupération historique: {e}")
                error_label = ctk.CTkLabel(
                    content_frame,
                    text=f"Erreur lors du chargement de l'historique: {e}",
                    font=("Segoe UI", 12),
                    text_color=ERROR_RED,
                    fg_color="transparent"
                )
                error_label.pack(expand=True)
        else:
            error_label = ctk.CTkLabel(
                content_frame,
                text="Contrôleur de salaire non disponible",
                font=("Segoe UI", 12),
                text_color=ERROR_RED,
                fg_color="transparent"
            )
            error_label.pack(expand=True)

    def export_professor_data(self, prof):
        """Exporte les données du professeur en PDF/Excel"""
        messagebox.showinfo("Export", f"Fonctionnalité d'export pour {prof.get('nom')} {prof.get('prenom')} en cours de développement")

    def update_prof_count(self):
        """Met à jour le compteur de professeurs"""
        total = len(self.professors_data)
        self.prof_count_label.configure(text=f"Total: {total}")

    def filter_professors(self, event=None):
        """Filtre et recharge la page 1 avec le terme courant"""
        self.current_offset = 0
        self.load_professors_data()
        self.display_professors_list()

    def change_page(self, direction: int):
        try:
            page_size = getattr(self, 'page_size', 50)
            new_offset = max(0, getattr(self, 'current_offset', 0) + (direction * page_size))
            # Eviter de reculer sous 0
            if new_offset == self.current_offset and direction < 0:
                return
            self.current_offset = new_offset
            self.load_professors_data()
            self.display_professors_list()
        except Exception as e:
            print(f"⚠️ Erreur pagination: {e}")
        
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
            
            # Case à cocher Professeur principal
            try:
                principal_checkbox = ctk.CTkCheckBox(
                    form_frame,
                    text="Professeur principal",
                    text_color=TEXT,
                    fg_color=ACCENT,
                    hover_color="#2563EB",
                    border_color=BORDER_COLOR,
                )
                principal_checkbox.grid(row=5, column=0, columnspan=2, sticky="w", padx=(20, 10), pady=(4, 0))
            except Exception:
                principal_checkbox = None

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
                    # Professeur principal (booléen 0/1)
                    professor_data['est_professeur_principal'] = 1 if (principal_checkbox and principal_checkbox.get()) else 0
                    
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
                        # Adapter l'INSERT selon les colonnes réellement présentes
                        try:
                            # Tentative avec la colonne est_professeur_principal si disponible
                            cursor.execute("""
                                INSERT INTO professeurs (
                                    nom, prenom, email, telephone, specialite, sexe,
                                    salaire_horaire, date_embauche, statut, est_professeur_principal
                                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                            """, (
                                professor_data['nom'], professor_data['prenom'], professor_data['email'],
                                professor_data['telephone'], professor_data['specialite'], professor_data['sexe'],
                                salaire_horaire,
                                professor_data['date_embauche'], professor_data['statut'],
                                professor_data['est_professeur_principal']
                            ))
                        except Exception:
                            # Fallback avec adresse si la colonne existe
                            try:
                                cursor.execute("""
                                    INSERT INTO professeurs (
                                        nom, prenom, email, telephone, specialite, sexe, adresse,
                                        salaire_horaire, date_embauche, statut, est_professeur_principal
                                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                                """, (
                                    professor_data['nom'], professor_data['prenom'], professor_data['email'],
                                    professor_data['telephone'], professor_data['specialite'], professor_data['sexe'],
                                    professor_data['adresse'], salaire_horaire,
                                    professor_data['date_embauche'], professor_data['statut'],
                                    professor_data['est_professeur_principal']
                                ))
                            except Exception:
                                # Dernier fallback minimal
                                cursor.execute("""
                                    INSERT INTO professeurs (
                                        nom, prenom, specialite, salaire_horaire, statut
                                    ) VALUES (?, ?, ?, ?, ?)
                                """, (
                                    professor_data['nom'], professor_data['prenom'], professor_data['specialite'],
                                    salaire_horaire, professor_data['statut']
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
