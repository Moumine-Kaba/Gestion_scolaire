import customtkinter as ctk
from tkinter import messagebox
from datetime import datetime
import sqlite3

# Le chemin de la base de données est géré par la configuration utilisateur
DB_PATH = r"C:\Users\Lenovo\Desktop\EduManager+\database\edumanager.db"

# --- CONTROLLERS (fonctions pour la base de données) ---

def _connect():
    """Crée et retourne une connexion à la base de données."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def get_all_classes():
    """Récupère toutes les classes."""
    with _connect() as conn:
        cur = conn.cursor()
        cur.execute("SELECT id, nom FROM classe ORDER BY nom")
        rows = cur.fetchall()
        return [dict(row) for row in rows]

def get_all_eleves(classe_id):
    """Récupère tous les élèves d'une classe spécifique."""
    with _connect() as conn:
        cur = conn.cursor()
        cur.execute("SELECT id, nom, prenom FROM eleves WHERE classe_id=? ORDER BY nom", (classe_id,))
        rows = cur.fetchall()
        return [dict(row) for row in rows]

def get_presence_for_date_and_class(classe_id, date):
    """Récupère les présences existantes pour une classe et une date données."""
    with _connect() as conn:
        cur = conn.cursor()
        cur.execute("""
            SELECT eleve_id, statut, commentaire FROM presence
            WHERE classe_id=? AND date=?
        """, (classe_id, date))
        return {row['eleve_id']: dict(row) for row in cur.fetchall()}

# Fonction corrigée pour ne plus accepter l'ID du professeur
def add_presence(eleve_id, classe_id, date, statut, commentaire):
    """Ajoute une nouvelle entrée de présence."""
    with _connect() as conn:
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO presence (eleve_id, classe_id, date, statut, commentaire)
            VALUES (?, ?, ?, ?, ?)
        """, (eleve_id, classe_id, date, statut, commentaire))
        conn.commit()

def update_presence(eleve_id, classe_id, date, statut, commentaire):
    """Met à jour une entrée de présence existante."""
    with _connect() as conn:
        cur = conn.cursor()
        cur.execute("""
            UPDATE presence
            SET statut=?, commentaire=?
            WHERE eleve_id=? AND classe_id=? AND date=?
        """, (statut, commentaire, eleve_id, classe_id, date))
        conn.commit()

# --- VUE DE PRÉSENCE RAPIDE ---

# Thème et polices
THEME = {
    "bg_main": "#0A192F", "header_bg": "#172A45", "card_bg": "#0B2039",
    "border_color": "#334155", "accent_blue": "#64FFDA", "primary_text": "#CCD6F6",
    "secondary_text": "#8892B0", "error_red": "#FF6363", "success_green": "#22c55e",
    "warning_yellow": "#FFD700", "info_orange": "#F97316"
}
FONT_FAMILY = "Fira Sans"
FONT_TITLE = (FONT_FAMILY, 20, "bold")
FONT_HEADING = (FONT_FAMILY, 14, "bold")
FONT_TEXT = (FONT_FAMILY, 12)

STATUTS = ["Présent", "Absent", "Retard", "Justifié"]

# La classe est renommée 'PresenceView'
class PresenceView(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Gestion de Présence Rapide")
        self.geometry("750x650")
        self.configure(fg_color=THEME["bg_main"])
        self.grab_set()
        
        # État de l'application
        self._classes = get_all_classes()
        self._classe_names = [c['nom'] for c in self._classes]
        self._classe_name_to_id = {c['nom']: c['id'] for c in self._classes}
        
        self.selected_classe_id = None
        self.eleves = []
        self.presence_vars = {}

        # UI
        self._build_ui()

    def _build_ui(self):
        # Section de sélection de la classe et de la date
        top_frame = ctk.CTkFrame(self, fg_color=THEME["card_bg"])
        top_frame.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkLabel(top_frame, text="Classe :", text_color=THEME["primary_text"]).pack(side="left", padx=10, pady=10)
        self.classe_cb = ctk.CTkComboBox(
            top_frame, values=self._classe_names, command=self.charger_eleves,
            fg_color=THEME["header_bg"], text_color=THEME["primary_text"], font=FONT_TEXT
        )
        self.classe_cb.set("Sélectionnez une classe")
        self.classe_cb.pack(side="left", padx=10, pady=10)

        ctk.CTkLabel(top_frame, text="Date :", text_color=THEME["primary_text"]).pack(side="left", padx=10, pady=10)
        self.date_entry = ctk.CTkEntry(
            top_frame, placeholder_text="AAAA-MM-JJ", fg_color=THEME["header_bg"],
            text_color=THEME["primary_text"], font=FONT_TEXT, width=120
        )
        self.date_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))
        self.date_entry.pack(side="left", padx=10, pady=10)

        # Bouton pour charger les élèves
        ctk.CTkButton(top_frame, text="Charger", command=self.charger_eleves,
                      fg_color=THEME["accent_blue"], text_color=THEME["bg_main"], hover_color="#45b69c").pack(side="left", padx=10)

        # Section de la liste des élèves
        self.scrollable_frame = ctk.CTkScrollableFrame(self, fg_color=THEME["bg_main"])
        self.scrollable_frame.pack(fill="both", expand=True, padx=20, pady=10)

        # Section des boutons d'action
        bottom_frame = ctk.CTkFrame(self, fg_color="transparent")
        bottom_frame.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkButton(bottom_frame, text="Enregistrer les présences", command=self.enregistrer_presences,
                      fg_color=THEME["success_green"], text_color=THEME["bg_main"], hover_color="#16a34a").pack(side="left", padx=10)
        
        ctk.CTkButton(bottom_frame, text="Annuler", command=self.destroy,
                      fg_color=THEME["error_red"], text_color=THEME["primary_text"], hover_color="#dc2626").pack(side="left", padx=10)

    def charger_eleves(self, *args):
        classe_nom = self.classe_cb.get()
        if classe_nom == "Sélectionnez une classe":
            return
            
        self.selected_classe_id = self._classe_name_to_id.get(classe_nom)
        if not self.selected_classe_id:
            messagebox.showerror("Erreur", "Classe introuvable.")
            return

        # Vider la liste actuelle
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        
        self.eleves = get_all_eleves(self.selected_classe_id)
        self.presence_vars = {}
        
        # Récupérer les présences déjà enregistrées pour cette classe/date
        date_str = self.date_entry.get().strip()
        if date_str:
            presences_existantes = get_presence_for_date_and_class(self.selected_classe_id, date_str)
        else:
            presences_existantes = {}

        # Générer l'interface pour chaque élève
        for eleve in self.eleves:
            eleve_id = eleve['id']
            row_frame = ctk.CTkFrame(self.scrollable_frame, fg_color=THEME["card_bg"])
            row_frame.pack(fill="x", pady=5, padx=5)

            ctk.CTkLabel(row_frame, text=f"{eleve['prenom']} {eleve['nom']}", font=FONT_TEXT, width=200, anchor="w",
                         text_color=THEME["primary_text"]).pack(side="left", padx=(15, 10))
            
            # Variables de statut et commentaire
            statut_var = ctk.StringVar()
            commentaire_var = ctk.StringVar()

            # Initialiser avec la valeur existante ou par défaut
            if eleve_id in presences_existantes:
                statut_var.set(presences_existantes[eleve_id]['statut'])
                commentaire_var.set(presences_existantes[eleve_id]['commentaire'])
            else:
                statut_var.set("Présent")
            
            # Boutons de statut
            for statut in STATUTS:
                radio_button = ctk.CTkRadioButton(
                    row_frame, text=statut, variable=statut_var, value=statut,
                    font=FONT_TEXT, text_color=THEME["primary_text"]
                )
                radio_button.pack(side="left", padx=5)

            # Champ de commentaire
            commentaire_entry = ctk.CTkEntry(
                row_frame, textvariable=commentaire_var, placeholder_text="Commentaire",
                width=200, font=FONT_TEXT, fg_color=THEME["header_bg"], text_color=THEME["primary_text"]
            )
            commentaire_entry.pack(side="left", padx=10)

            self.presence_vars[eleve_id] = {'statut': statut_var, 'commentaire': commentaire_var}

    def enregistrer_presences(self):
        if not self.selected_classe_id or not self.eleves:
            messagebox.showwarning("Avertissement", "Veuillez d'abord sélectionner une classe et charger les élèves.")
            return

        date_str = self.date_entry.get().strip()
        if not date_str:
            messagebox.showerror("Erreur", "Veuillez entrer une date valide.")
            return

        try:
            datetime.strptime(date_str, "%Y-%m-%d")
            
            for eleve in self.eleves:
                eleve_id = eleve['id']
                vars = self.presence_vars.get(eleve_id)
                statut = vars['statut'].get()
                commentaire = vars['commentaire'].get()
                
                presences_existantes = get_presence_for_date_and_class(self.selected_classe_id, date_str)
                
                if eleve_id in presences_existantes:
                    update_presence(eleve_id, self.selected_classe_id, date_str, statut, commentaire)
                else:
                    # La fonction add_presence ne prend plus prof_id
                    add_presence(eleve_id, self.selected_classe_id, date_str, statut, commentaire)
            
            messagebox.showinfo("Succès", "Présences enregistrées avec succès.")
            self.destroy()
            
        except ValueError:
            messagebox.showerror("Erreur", "Format de date invalide (AAAA-MM-JJ).")
        except Exception as e:
            messagebox.showerror("Erreur", f"Une erreur est survenue : {e}")