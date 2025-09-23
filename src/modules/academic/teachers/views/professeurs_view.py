from database.connection import get_db_connection
import customtkinter as ctk
from PIL import Image, ImageDraw, ImageFont, ImageOps
from tkinter import messagebox, filedialog
import os, sys
import csv

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
        self.geometry("400x500")
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
        """Crée l'interface CRUD moderne avec le thème personnalisé"""
        # Header principal avec titre et bouton ajouter
        header_frame = ctk.CTkFrame(self, fg_color=CARD_BG, height=80, corner_radius=15)
        header_frame.pack(fill="x", padx=15, pady=15)
        header_frame.pack_propagate(False)
        
        # Titre principal avec icône
        title_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        title_frame.pack(side="left", padx=30, pady=25)
        
        # Icône group
        group_icon = ctk.CTkLabel(
            title_frame,
            image=self.icon_cache.get("group"),
            text="",
            fg_color="transparent"
        )
        group_icon.pack(side="left", padx=(0, 15))
        
        # Titre avec icône
        title_label = ctk.CTkLabel(
            title_frame,
            text="Gestion des Profs",
            font=FONT_TITLE,
            text_color=TEXT,
            fg_color="transparent"
        )
        title_label.pack(side="left")
        
        # Frame pour les boutons d'action
        buttons_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        buttons_frame.pack(side="right", padx=30, pady=20)
        
        # Bouton Voir Détails
        details_button = ctk.CTkButton(
            buttons_frame,
            text="Voir Détails",
            image=self.icon_cache.get("view"),
            font=FONT_BUTTON,
            fg_color="transparent",
            hover_color=ACCENT,
            text_color=TEXT,
            height=40,
            width=140,
            corner_radius=20,
            border_width=2,
            border_color=BORDER_COLOR,
            command=self.show_details
        )
        details_button.pack(side="left", padx=(0, 10))
        
        # Bouton Ajouter avec contour gris
        add_button = ctk.CTkButton(
            buttons_frame,
            text="Ajouter Professeur",
            image=self.icon_cache.get("add"),
            font=FONT_BUTTON,
            fg_color="transparent",
            hover_color=ACCENT,
            text_color=TEXT,
            height=40,
            width=160,
            corner_radius=20,
            border_width=2,
            border_color=BORDER_COLOR,
            command=self.add_professor
        )
        add_button.pack(side="left")
        
        # Container principal pour le tableau
        main_container = ctk.CTkFrame(self, fg_color=CARD_BG, corner_radius=15)
        main_container.pack(fill="both", expand=True, padx=15, pady=(0, 15))
        
        # Barre de recherche et filtres améliorée
        search_frame = ctk.CTkFrame(main_container, fg_color=BG_SIDEBAR, height=70, corner_radius=12)
        search_frame.pack(fill="x", padx=15, pady=15)
        search_frame.pack_propagate(False)
        
        # Frame pour la recherche
        search_input_frame = ctk.CTkFrame(search_frame, fg_color="transparent")
        search_input_frame.pack(side="left", padx=20, pady=15)
        
        # Icône de recherche
        search_icon = ctk.CTkLabel(
            search_input_frame,
            image=self.icon_cache.get("search"),
            text="",
            fg_color="transparent"
        )
        search_icon.pack(side="left", padx=(0, 10))
        
        # Champ de recherche amélioré
        self.search_var = ctk.StringVar()
        search_entry = ctk.CTkEntry(
            search_input_frame,
            textvariable=self.search_var,
            font=("Segoe UI", 14),
            placeholder_text="🔍 Rechercher par nom, prénom, spécialité...",
            fg_color=CARD_BG,
            text_color=TEXT,
            border_width=2,
            border_color=BORDER_COLOR,
            corner_radius=10,
            width=400,
            height=40
        )
        search_entry.pack(side="left")
        search_entry.bind("<KeyRelease>", self.filter_professors)
        
        # Frame pour les statistiques avec badge
        stats_frame = ctk.CTkFrame(search_frame, fg_color="transparent")
        stats_frame.pack(side="right", padx=20, pady=15)
        
        self.stats_label = ctk.CTkLabel(
            stats_frame,
            text="📊 Total: 0 professeurs",
            font=("Segoe UI", 12, "bold"),
            text_color=TEXT,
            fg_color="transparent"
        )
        self.stats_label.pack()
        
        # Tableau principal avec scroll
        table_container = ctk.CTkScrollableFrame(
            main_container,
            fg_color=CARD_BG,
            scrollbar_button_color=BORDER_COLOR,
            scrollbar_button_hover_color=ACCENT
        )
        table_container.pack(fill="both", expand=True, padx=15, pady=(0, 15))
        
        # Créer le tableau
        self.table_container = table_container
        self.professors_data = []
        self.create_professors_table()

    def create_professors_table(self):
        """Crée le tableau des professeurs avec design moderne"""
        # Nettoyer le container
        for widget in self.table_container.winfo_children():
            widget.destroy()
        
        # Configuration des colonnes (ajout de la colonne image)
        self.table_container.grid_columnconfigure((0, 1, 2, 3, 4, 5, 6, 7), weight=1)
        
        # En-têtes du tableau avec colonne image
        headers = ["Image", "Nom", "Prénom", "Téléphone", "Email", "Spécialité", "Statut", "Actions"]
        
        for i, header in enumerate(headers):
            header_frame = ctk.CTkFrame(
                self.table_container,
                fg_color=BORDER_COLOR,
                height=50,
                corner_radius=8
            )
            header_frame.grid(row=0, column=i, padx=2, pady=(0, 5), sticky="ew")
            header_frame.grid_propagate(False)
            
            header_label = ctk.CTkLabel(
                header_frame,
                text=header,
                font=FONT_SUBTITLE,
                text_color=TEXT,
                fg_color="transparent"
            )
            header_label.pack(expand=True)
        
        # Charger et afficher les données
        self.load_professors_data()
        
    def load_professors_data(self):
        """Charge les données des professeurs"""
        try:
            from src.modules.academic.teachers.controllers.professeur_controller import get_all_professeurs
            self.professors_data = get_all_professeurs()
            self.display_professors_data()
            self.update_stats()
        except Exception as e:
            print(f"⚠️ Erreur chargement professeurs: {e}")
            
    def display_professors_data(self):
        """Affiche les données des professeurs dans le tableau"""
        # Nettoyer les données existantes (garder les en-têtes)
        for widget in self.table_container.winfo_children():
            if widget.grid_info().get('row', 0) > 0:
                widget.destroy()
        
        # Afficher chaque professeur
        for idx, prof in enumerate(self.professors_data):
            row = idx + 1
            
            # Créer un frame pour toute la ligne pour la sélection
            row_frame = ctk.CTkFrame(self.table_container, fg_color="transparent", corner_radius=5)
            row_frame.grid(row=row, column=0, columnspan=8, padx=5, pady=2, sticky="ew")
            
            # Fonction pour gérer la sélection
            def select_row(prof_id):
                print(f"🔍 Debug: Sélection du professeur ID {prof_id}")  # Debug
                self.selected_prof_id = prof_id
                # Mettre à jour l'apparence de toutes les lignes
                for widget in self.table_container.winfo_children():
                    if hasattr(widget, 'prof_id'):
                        if widget.prof_id == prof_id:
                            widget.configure(fg_color="#31487b")
                        else:
                            widget.configure(fg_color="transparent")
            
            # Associer l'ID du professeur au frame de ligne
            row_frame.prof_id = prof.get('id')
            row_frame.bind("<Button-1>", lambda e, pid=prof.get('id'): select_row(pid))
            
            # Image/Photo du professeur
            image_frame = ctk.CTkFrame(row_frame, fg_color="transparent")
            image_frame.pack(side="left", padx=5, pady=5)
            
            # Charger l'image du professeur ou utiliser l'icône par défaut
            prof_image = prof.get('image_path') or prof.get('photo')
            if prof_image and os.path.exists(prof_image):
                try:
                    from PIL import Image
                    img = Image.open(prof_image)
                    img = img.resize((40, 40), Image.Resampling.LANCZOS)
                    prof_icon = ctk.CTkImage(img, size=(40, 40))
                except:
                    prof_icon = self.icon_cache.get("person", load_icon("person", 40))
            else:
                prof_icon = self.icon_cache.get("person", load_icon("person", 40))
            
            image_label = ctk.CTkLabel(
                image_frame,
                image=prof_icon,
                text="",
                fg_color="transparent"
            )
            image_label.pack(expand=True)
            
            # Nom
            nom_label = ctk.CTkLabel(
                row_frame,
                text=prof.get('nom', ''),
                font=FONT_SECONDARY,
                text_color=TEXT,
                fg_color="transparent"
            )
            nom_label.pack(side="left", padx=5, pady=5, expand=True, fill="x")
            
            # Prénom
            prenom_label = ctk.CTkLabel(
                row_frame,
                text=prof.get('prenom', ''),
                font=FONT_SECONDARY,
                text_color=TEXT,
                fg_color="transparent"
            )
            prenom_label.pack(side="left", padx=5, pady=5, expand=True, fill="x")
            
            # Téléphone
            tel_label = ctk.CTkLabel(
                row_frame,
                text=prof.get('telephone', 'N/A'),
                font=FONT_SECONDARY,
                text_color=MUTED,
                fg_color="transparent"
            )
            tel_label.pack(side="left", padx=5, pady=5, expand=True, fill="x")
            
            # Email
            email_label = ctk.CTkLabel(
                row_frame,
                text=prof.get('email', 'N/A'),
                font=FONT_SECONDARY,
                text_color=MUTED,
                fg_color="transparent"
            )
            email_label.pack(side="left", padx=5, pady=5, expand=True, fill="x")
            
            # Spécialité
            spec_label = ctk.CTkLabel(
                row_frame,
                text=prof.get('specialite', 'N/A'),
                font=FONT_SECONDARY,
                text_color=MUTED,
                fg_color="transparent"
            )
            spec_label.pack(side="left", padx=5, pady=5, expand=True, fill="x")
            
            # Statut avec couleur du thème
            statut = prof.get('statut', 'actif')
            statut_color = SUCCESS_GREEN if statut == 'actif' else WARNING_YELLOW
            statut_label = ctk.CTkLabel(
                row_frame,
                text=statut.title(),
                font=FONT_SECONDARY,
                text_color=statut_color,
                fg_color="transparent"
            )
            statut_label.pack(side="left", padx=5, pady=5, expand=True, fill="x")
            
            # Actions (boutons CRUD centrés uniquement)
            actions_frame = ctk.CTkFrame(row_frame, fg_color="transparent")
            actions_frame.pack(side="left", padx=5, pady=5)
            
            # Bouton Read (Détails) - style avec bordure, centré
            read_btn = ctk.CTkButton(
                actions_frame,
                text="",
                image=load_icon("view", 12),
                font=FONT_SECONDARY,
                fg_color="transparent",
                hover_color=ACCENT,
                text_color=TEXT,
                width=28,
                height=28,
                corner_radius=8,
                border_width=1,
                border_color=BORDER_COLOR,
                command=lambda p=prof: self.show_professor_details(p)
            )
            read_btn.pack(side="left", padx=2)
            
            # Bouton Update (Modifier) - style avec bordure, centré
            update_btn = ctk.CTkButton(
                actions_frame,
                text="",
                image=load_icon("edit", 12),
                font=FONT_SECONDARY,
                fg_color="transparent",
                hover_color=ACCENT,
                text_color=TEXT,
                width=28,
                height=28,
                corner_radius=8,
                border_width=1,
                border_color=BORDER_COLOR,
                command=lambda p=prof: self.edit_professor(p)
            )
            update_btn.pack(side="left", padx=2)
            
            # Bouton Delete (Supprimer) - style avec bordure, centré
            delete_btn = ctk.CTkButton(
                actions_frame,
                text="",
                image=load_icon("delete", 12),
                font=FONT_SECONDARY,
                fg_color="transparent",
                hover_color=ERROR_RED,
                text_color=ERROR_RED,
                width=28,
                height=28,
                corner_radius=8,
                border_width=1,
                border_color=ERROR_RED,
                command=lambda p=prof: self.delete_professor(p)
            )
            delete_btn.pack(side="left", padx=2)
            
    def update_stats(self):
        """Met à jour les statistiques"""
        total = len(self.professors_data)
        self.stats_label.configure(text=f"Total: {total} professeurs")
        
    def show_professor_details(self, professor):
        """Affiche les détails d'un professeur avec le thème CustomTkinter"""
        print(f"🔍 Debug: Affichage des détails pour {professor}")  # Debug
        
        # Créer la fenêtre de détails
        details_window = ctk.CTkToplevel(self)
        details_window.title(f"Profil - {professor.get('prenom', '')} {professor.get('nom', '')}")
        details_window.geometry("800x500")  # Garder les dimensions
        details_window.configure(fg_color=THEME["bg_main"])  # Utiliser le thème
        
        # Empêcher la fermeture accidentelle
        details_window.transient(self)
        details_window.grab_set()
        
        # Centrer la fenêtre
        details_window.update_idletasks()
        x = (details_window.winfo_screenwidth() // 2) - (800 // 2)
        y = (details_window.winfo_screenheight() // 2) - (500 // 2)
        details_window.geometry(f"800x500+{x}+{y}")
        
        # Conteneur principal avec le thème
        main_container = ctk.CTkFrame(details_window, fg_color=THEME["bg_main"], corner_radius=15)
        main_container.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Titre principal
        title_label = ctk.CTkLabel(
            main_container, 
            text=f"Détails du Professeur",
            font=(FONT, 24, "bold"),
            text_color=THEME["primary_text"]
        )
        title_label.pack(pady=(20, 30))
        
        # Frame scrollable pour les informations
        scroll_frame = ctk.CTkScrollableFrame(main_container, fg_color=THEME["card_bg"], corner_radius=10)
        scroll_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Informations personnelles
        personal_frame = ctk.CTkFrame(scroll_frame, fg_color=THEME["header_bg"], corner_radius=8)
        personal_frame.pack(fill="x", padx=10, pady=10)
        
        personal_title = ctk.CTkLabel(
            personal_frame,
            text="📋 Informations Personnelles",
            font=(FONT, 16, "bold"),
            text_color=THEME["accent_blue"]
        )
        personal_title.pack(pady=15)
        
        # Nom et Prénom
        name_frame = ctk.CTkFrame(personal_frame, fg_color="transparent")
        name_frame.pack(fill="x", padx=20, pady=5)
        
        ctk.CTkLabel(name_frame, text="Nom:", font=(FONT, 12, "bold"), text_color=THEME["secondary_text"]).pack(side="left")
        ctk.CTkLabel(name_frame, text=professor.get('nom', 'N/A'), font=(FONT, 12), text_color=THEME["primary_text"]).pack(side="left", padx=(10, 0))
        
        prenom_frame = ctk.CTkFrame(personal_frame, fg_color="transparent")
        prenom_frame.pack(fill="x", padx=20, pady=5)
        
        ctk.CTkLabel(prenom_frame, text="Prénom:", font=(FONT, 12, "bold"), text_color=THEME["secondary_text"]).pack(side="left")
        ctk.CTkLabel(prenom_frame, text=professor.get('prenom', 'N/A'), font=(FONT, 12), text_color=THEME["primary_text"]).pack(side="left", padx=(10, 0))
        
        # Informations professionnelles
        prof_frame = ctk.CTkFrame(scroll_frame, fg_color=THEME["header_bg"], corner_radius=8)
        prof_frame.pack(fill="x", padx=10, pady=10)
        
        prof_title = ctk.CTkLabel(
            prof_frame,
            text="💼 Informations Professionnelles",
            font=(FONT, 16, "bold"),
            text_color=THEME["accent_blue"]
        )
        prof_title.pack(pady=15)
        
        # Matricule
        matricule_frame = ctk.CTkFrame(prof_frame, fg_color="transparent")
        matricule_frame.pack(fill="x", padx=20, pady=5)
        
        ctk.CTkLabel(matricule_frame, text="Matricule:", font=(FONT, 12, "bold"), text_color=THEME["secondary_text"]).pack(side="left")
        ctk.CTkLabel(matricule_frame, text=professor.get('matricule', 'N/A'), font=(FONT, 12), text_color=THEME["primary_text"]).pack(side="left", padx=(10, 0))
        
        # Spécialité
        spec_frame = ctk.CTkFrame(prof_frame, fg_color="transparent")
        spec_frame.pack(fill="x", padx=20, pady=5)
        
        ctk.CTkLabel(spec_frame, text="Spécialité:", font=(FONT, 12, "bold"), text_color=THEME["secondary_text"]).pack(side="left")
        ctk.CTkLabel(spec_frame, text=professor.get('specialite', 'N/A'), font=(FONT, 12), text_color=THEME["primary_text"]).pack(side="left", padx=(10, 0))
        
        # Statut
        statut_frame = ctk.CTkFrame(prof_frame, fg_color="transparent")
        statut_frame.pack(fill="x", padx=20, pady=5)
        
        ctk.CTkLabel(statut_frame, text="Statut:", font=(FONT, 12, "bold"), text_color=THEME["secondary_text"]).pack(side="left")
        statut_text = professor.get('statut', 'N/A')
        statut_color = THEME["success_green"] if statut_text.lower() == 'actif' else THEME["warning_orange"]
        ctk.CTkLabel(statut_frame, text=statut_text, font=(FONT, 12), text_color=statut_color).pack(side="left", padx=(10, 0))
        
        # Date d'embauche
        embauche_frame = ctk.CTkFrame(prof_frame, fg_color="transparent")
        embauche_frame.pack(fill="x", padx=20, pady=5)
        
        ctk.CTkLabel(embauche_frame, text="Date d'embauche:", font=(FONT, 12, "bold"), text_color=THEME["secondary_text"]).pack(side="left")
        ctk.CTkLabel(embauche_frame, text=professor.get('date_embauche', 'N/A'), font=(FONT, 12), text_color=THEME["primary_text"]).pack(side="left", padx=(10, 0))
        
        # Informations de contact
        contact_frame = ctk.CTkFrame(scroll_frame, fg_color=THEME["header_bg"], corner_radius=8)
        contact_frame.pack(fill="x", padx=10, pady=10)
        
        contact_title = ctk.CTkLabel(
            contact_frame,
            text="📞 Informations de Contact",
            font=(FONT, 16, "bold"),
            text_color=THEME["accent_blue"]
        )
        contact_title.pack(pady=15)
        
        # Email
        email_frame = ctk.CTkFrame(contact_frame, fg_color="transparent")
        email_frame.pack(fill="x", padx=20, pady=5)
        
        ctk.CTkLabel(email_frame, text="Email:", font=(FONT, 12, "bold"), text_color=THEME["secondary_text"]).pack(side="left")
        ctk.CTkLabel(email_frame, text=professor.get('email', 'N/A'), font=(FONT, 12), text_color=THEME["primary_text"]).pack(side="left", padx=(10, 0))
        
        # Téléphone
        phone_frame = ctk.CTkFrame(contact_frame, fg_color="transparent")
        phone_frame.pack(fill="x", padx=20, pady=5)
        
        ctk.CTkLabel(phone_frame, text="Téléphone:", font=(FONT, 12, "bold"), text_color=THEME["secondary_text"]).pack(side="left")
        ctk.CTkLabel(phone_frame, text=professor.get('telephone', 'N/A'), font=(FONT, 12), text_color=THEME["primary_text"]).pack(side="left", padx=(10, 0))
        
        # Adresse
        adresse_frame = ctk.CTkFrame(contact_frame, fg_color="transparent")
        adresse_frame.pack(fill="x", padx=20, pady=5)
        
        ctk.CTkLabel(adresse_frame, text="Adresse:", font=(FONT, 12, "bold"), text_color=THEME["secondary_text"]).pack(side="left")
        ctk.CTkLabel(adresse_frame, text=professor.get('adresse', 'N/A'), font=(FONT, 12), text_color=THEME["primary_text"]).pack(side="left", padx=(10, 0))
        
        # Boutons d'action
        buttons_frame = ctk.CTkFrame(main_container, fg_color="transparent")
        buttons_frame.pack(fill="x", pady=20)
        
        # Bouton Modifier
        edit_btn = ctk.CTkButton(
            buttons_frame,
            text="Modifier",
            font=(FONT, 12, "bold"),
            fg_color=THEME["accent_blue"],
            hover_color=THEME["accent_blue_hover"],
            text_color=THEME["bg_main"],
            height=35,
            width=100,
            corner_radius=8,
            command=lambda: self.edit_professor(professor)
        )
        edit_btn.pack(side="left", padx=(0, 10))
        
        # Bouton Fermer
        close_btn = ctk.CTkButton(
            buttons_frame,
            text="Fermer",
            font=(FONT, 12, "bold"),
            fg_color=THEME["error_red"],
            hover_color=THEME["error_red_hover"],
            text_color=THEME["bg_main"],
            height=35,
            width=100,
            corner_radius=8,
            command=details_window.destroy
        )
        close_btn.pack(side="right")
        
        print(f"✅ Debug: Fenêtre de détails créée avec succès pour {professor.get('prenom', '')} {professor.get('nom', '')}")

    def filter_professors(self, event=None):
        """Filtre les professeurs selon la recherche"""
        search_term = self.search_var.get().lower()
        if not search_term:
            self.display_professors_data()
            return
            
        filtered_data = []
        for prof in self.professors_data:
            if (search_term in prof.get('nom', '').lower() or 
                search_term in prof.get('prenom', '').lower() or
                search_term in prof.get('email', '').lower() or
                search_term in prof.get('specialite', '').lower()):
                filtered_data.append(prof)
        
        # Sauvegarder les données originales
        original_data = self.professors_data.copy()
        self.professors_data = filtered_data
        self.display_professors_data()
        self.professors_data = original_data

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
        """Met à jour les données affichées dans le tableau."""
        self.load_professors_data()


    def add_professor(self):
        """Ouvre le formulaire pour ajouter un nouveau professeur."""
        try:
            from src.modules.academic.teachers.views.professeur_form import ProfesseurForm  # pyright: ignore[reportMissingImports]
            ProfesseurForm(self.parent, self.update_data, mode="Ajouter")
        except ImportError:
            # Fallback simple
            self._simple_add_professor()

    def edit_professor(self, professor=None):
        """Ouvre le formulaire pour modifier un professeur."""
        if not professor:
            messagebox.showinfo("Modifier", "Sélectionnez un professeur à modifier.")
            return
            
        try:
            from src.modules.academic.teachers.views.professeur_form import ProfesseurForm  # pyright: ignore[reportMissingImports]
            ProfesseurForm(self.parent, self.update_data, mode="Modifier", data=professor)
        except ImportError:
            # Fallback simple
            self._simple_edit_professor(professor)

    def delete_professor(self, professor=None):
        """Supprime un professeur avec confirmation."""
        if not professor:
            messagebox.showinfo("Supprimer", "Sélectionnez un professeur à supprimer.")
            return
            
        # Demander confirmation
        result = messagebox.askyesno(
            "Supprimer Professeur", 
            f"Êtes-vous sûr de vouloir supprimer {professor.get('prenom', '')} {professor.get('nom', '')} ?"
        )
        
        if result:
            try:
                from src.modules.academic.teachers.controllers.professeur_controller import delete_professeur
                if delete_professeur(professor.get('id_professeur')):
                    messagebox.showinfo("Succès", "Professeur supprimé avec succès.")
                    self.update_data()
                else:
                    messagebox.showerror("Erreur", "Erreur lors de la suppression.")
            except Exception as e:
                messagebox.showerror("Erreur", f"Erreur lors de la suppression: {e}")
        # (Fixed indentation and removed unreachable/duplicate code)
        dialog = ProfesseurDialog(self, "Modifier un Professeur", professor)
        if dialog.result:
            try:
                from src.modules.academic.teachers.controllers.professeur_controller import update_professeur
                if update_professeur(professor.get('id_professeur'), dialog.result):
                    messagebox.showinfo("Succès", "Professeur modifié avec succès.")
                    self.update_data()
                else:
                    messagebox.showerror("Erreur", "Erreur lors de la modification.")
            except Exception as e:
                messagebox.showerror("Erreur", f"Erreur lors de la modification: {e}")

    def show_details(self):
        """Affiche la carte détaillée du professeur sélectionné."""
        print(f"🔍 Debug: show_details appelé, selected_prof_id = {self.selected_prof_id}")  # Debug
        
        if not self.selected_prof_id:
            messagebox.showinfo("Détails", "Sélectionnez un professeur pour voir les détails.")
            return
            
        print(f"🔍 Debug: Récupération des données du professeur ID {self.selected_prof_id}")  # Debug
        prof_data = get_professeur(self.selected_prof_id)
        print(f"🔍 Debug: Données récupérées: {prof_data}")  # Debug
        
        if prof_data:
            self.show_professor_details(prof_data)
        else:
            messagebox.showerror("Erreur", "Professeur non trouvé.")

    def export_to_csv(self):
        """Exporte les données des professeurs vers un fichier CSV."""
        profs_to_export = get_all_professeurs()
        if not profs_to_export:
            messagebox.showinfo("Export", "Aucune donnée à exporter.")
            return
        path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV", "*.csv")],
            title="Exporter les professeurs"
        )
        if not path:
            return
        import csv
        try:
            with open(path, mode='w', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow([
                    "ID", "Matricule", "Nom", "Prénom", "Date de naissance", "Sexe",
                ])
            for row in profs_to_export:
                writer.writerow([
                    row.get('id', ''), row.get('matricule', ''), row.get('nom', ''), row.get('prenom', ''),
                    row.get('date_naissance', ''), row.get('sexe', ''), row.get('adresse', ''),
                    row.get('telephone', ''), row.get('email', ''), row.get('specialite', ''),
                    row.get('date_embauche', ''), row.get('statut', '')
                ])
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de l'export: {e}")
            return
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
                         text_color="#FFFFFF", fg_color="transparent").pack(expand=True)
        
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
                # Texte blanc pour tous les champs
                text_color = "#FFFFFF"  # Blanc pour tous les champs
                
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
            
            ctk.CTkLabel(no_results_frame, text="Aucun professeurs trouvé", font=(FONT, 16, "bold"), 
                         text_color=THEME["secondary_text"], fg_color="transparent").pack(pady=(0, 5))
            
            ctk.CTkLabel(no_results_frame, text="Essayez de modifier votre recherche", font=(FONT, 12), 
                         text_color=THEME["secondary_text"], fg_color="transparent").pack()

    def get_selected_professor_id(self):
        """Retourne l'ID du professeurs sélectionné."""
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
        self.geometry("600x650")
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
        self.title(f"{mode} un professeurs")
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
        save_btn_text = "Enregistrer les modifications" if self.mode == "Modifier" else "Ajouter le professeurs"
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