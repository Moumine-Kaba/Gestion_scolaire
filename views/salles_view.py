import tkinter as tk
from tkinter import messagebox
import customtkinter as ctk
import os
import sqlite3
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
from PIL import Image

# --- Paramètres de l'application et du thème ---
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# Le chemin de votre base de données.
DB_PATH = r"C:\Users\Lenovo\Desktop\EduManager+\database\edumanager.db"

# Thème de couleurs
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
    "select_highlight": "#2A456C",
    "hover_light": "#1C3558"
}
FONT = "Segoe UI"

# --- Modèle de données (Data Model) ---
class Salle:
    """Classe représentant une salle avec ses attributs."""
    def __init__(self, id, nom, capacite, type_salle):
        self.id = id
        self.nom = nom
        self.capacite = capacite
        self.type_salle = type_salle

# --- Contrôleur de données (Data Controller) avec base de données ---
class SalleController:
    """Gère les interactions avec la base de données pour les salles."""
    def __init__(self, db_path):
        self.db_path = db_path
        self.conn = None
        self.cursor = None
        self._connect_db()
        self._create_table()

    def _connect_db(self):
        """Établit la connexion à la base de données."""
        try:
            os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
            self.conn = sqlite3.connect(self.db_path)
            self.cursor = self.conn.cursor()
        except sqlite3.Error as e:
            print(f"Erreur de Base de Données: Impossible de se connecter à la base de données : {e}")
            self.conn = None
            self.cursor = None

    def _create_table(self):
        """Crée la table 'salle' si elle n'existe pas et s'assure que la colonne 'type_salle' est présente."""
        if self.conn:
            try:
                self.cursor.execute("""
                    CREATE TABLE IF NOT EXISTS salle (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        nom TEXT NOT NULL UNIQUE,
                        capacite INTEGER NOT NULL,
                        type_salle TEXT NOT NULL
                    )
                """)
                self.conn.commit()

                self.cursor.execute("PRAGMA table_info(salle)")
                columns = [info[1] for info in self.cursor.fetchall()]
                if 'type_salle' not in columns:
                    self.cursor.execute("ALTER TABLE salle ADD COLUMN type_salle TEXT NOT NULL DEFAULT 'Général'")
                    self.conn.commit()

            except sqlite3.Error as e:
                print(f"Erreur de Base de Données: Erreur lors de la création ou de la mise à jour de la table : {e}")

    def get_all_salles(self):
        """Récupère toutes les salles de la base de données."""
        if not self.conn:
            return []
        self.cursor.execute("SELECT id, nom, capacite, type_salle FROM salle ORDER BY nom")
        rows = self.cursor.fetchall()
        return [Salle(row[0], row[1], row[2], row[3]) for row in rows]

    def add_salle(self, nom, capacite, type_salle):
        """Ajoute une nouvelle salle à la base de données."""
        if not self.conn: return
        try:
            self.cursor.execute("INSERT INTO salle (nom, capacite, type_salle) VALUES (?, ?, ?)", (nom, capacite, type_salle))
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            messagebox.showerror("Erreur", f"La salle '{nom}' existe déjà.")
            return False
        except sqlite3.Error as e:
            messagebox.showerror("Erreur de Base de Données", f"Erreur lors de l'ajout de la salle : {e}")
            return False

    def update_salle(self, salle_id, nom, capacite, type_salle):
        """Met à jour une salle dans la base de données."""
        if not self.conn: return False
        try:
            self.cursor.execute("UPDATE salle SET nom=?, capacite=?, type_salle=? WHERE id=?", (nom, capacite, type_salle, salle_id))
            self.conn.commit()
            return True
        except sqlite3.Error as e:
            messagebox.showerror("Erreur de Base de Données", f"Erreur lors de la mise à jour de la salle : {e}")
            return False

    def delete_salle(self, salle_id):
        """Supprime une salle de la base de données."""
        if not self.conn: return
        try:
            self.cursor.execute("DELETE FROM salle WHERE id=?", (salle_id,))
            self.conn.commit()
            return True
        except sqlite3.Error as e:
            messagebox.showerror("Erreur de Base de Données", f"Erreur lors de la suppression de la salle : {e}")
            return False

    def get_salles_stats(self):
        """Récupère des statistiques sur les salles pour le graphique."""
        if not self.conn: return {}, 0
        self.cursor.execute("SELECT type_salle, COUNT(*) FROM salle GROUP BY type_salle")
        type_counts = dict(self.cursor.fetchall())
        self.cursor.execute("SELECT SUM(capacite) FROM salle")
        total_capacite = self.cursor.fetchone()[0] or 0
        return type_counts, total_capacite

# Initialisation du contrôleur avec le chemin de la base de données
salle_controller = SalleController(DB_PATH)

# --- Application principale (Main App) ---
class App(ctk.CTk):
    """Classe principale de l'application."""
    def __init__(self):
        super().__init__()
        self.title("EduManager+")
        self.geometry("1200x700")
        self.configure(fg_color=THEME["bg_main"])

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        # Le 'icons' est une dépendance que l'on doit passer si la classe l'attend
        # Création d'un dictionnaire d'icônes, ici il est vide, mais il pourrait être rempli
        self.icons = {} 

        # Créez la vue principale des salles en passant le parent et les icônes
        self.salles_view = SallesView(self, self.icons) # <-- Correction ici
        self.salles_view.grid(row=0, column=0, sticky="nsew")

# --- Vues de l'application (Main Views) ---
class SallesView(ctk.CTkFrame):
    """Vue principale pour la gestion des salles."""
    # La signature de la méthode __init__ a été corrigée ici
    def __init__(self, parent, icons):
        super().__init__(parent, fg_color=THEME["bg_main"])
        self.parent = parent
        self.icons = icons
        self.salle_controller = salle_controller
        self.search_var = tk.StringVar()
        self.sort_var = tk.StringVar(value="nom")
        self.selected_salle = None
        self.selected_salle_frame = None

        self.create_header()

        main_frame = ctk.CTkFrame(self, fg_color="transparent")
        main_frame.pack(fill="both", expand=True, padx=20, pady=(10, 20))
        main_frame.grid_columnconfigure(0, weight=1)
        main_frame.grid_columnconfigure(1, weight=2)
        main_frame.grid_rowconfigure(0, weight=1)

        self.create_salle_list_panel(main_frame)
        self.create_salle_details_panel(main_frame)

        self.refresh_salles_view()

    def create_header(self):
        """Crée l'en-tête de la vue avec le titre et le bouton d'ajout."""
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.pack(fill="x", pady=(20, 10), padx=20)
        ctk.CTkLabel(header_frame, text="Gestion des Salles", font=(FONT, 28, "bold"), text_color=THEME["primary_text"]).pack(side="left")

        btn_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        btn_frame.pack(side="right")

        try:
            refresh_icon = ctk.CTkImage(Image.open("refresh.png"), size=(20, 20))
            refresh_btn = ctk.CTkButton(btn_frame, text="", image=refresh_icon, width=40,
                                         fg_color=THEME["header_bg"], hover_color=THEME["hover_light"],
                                         command=self.refresh_salles_view)
            refresh_btn.pack(side="left", padx=(0, 10))
        except FileNotFoundError:
            print("Icône 'refresh.png' non trouvée.")

        try:
            add_icon = ctk.CTkImage(Image.open("add.png"), size=(20, 20))
            add_btn = ctk.CTkButton(btn_frame, text="Ajouter", image=add_icon, compound="left", font=(FONT, 14, "bold"),
                                     fg_color=THEME["accent_blue"], hover_color="#56A192", text_color=THEME["bg_main"],
                                     command=self.ajouter_salle, width=120)
            add_btn.pack(side="left")
        except FileNotFoundError:
            add_btn = ctk.CTkButton(btn_frame, text="+ Ajouter", font=(FONT, 14, "bold"),
                                     fg_color=THEME["accent_blue"], hover_color="#56A192", text_color=THEME["bg_main"],
                                     command=self.ajouter_salle, width=120)
            add_btn.pack(side="left")
            print("Icône 'add.png' non trouvée. Utilisation du texte par défaut.")


    def create_salle_list_panel(self, parent_frame):
        """Crée le panneau de gauche avec la liste des salles."""
        list_panel = ctk.CTkFrame(parent_frame, fg_color=THEME["card_bg"], corner_radius=10)
        list_panel.grid(row=0, column=0, sticky="nsew", padx=(0, 10))

        search_frame = ctk.CTkFrame(list_panel, fg_color="transparent")
        search_frame.pack(fill="x", padx=10, pady=(10, 5))

        search_entry = ctk.CTkEntry(search_frame, placeholder_text="Rechercher...",
                                     font=(FONT, 14), height=35,
                                     fg_color=THEME["header_bg"], border_color=THEME["border_color"],
                                     textvariable=self.search_var)
        search_entry.pack(side="left", fill="x", expand=True)
        self.search_var.trace_add("write", self.filter_salles)

        sort_options = ["nom", "capacite", "type"]
        sort_menu = ctk.CTkOptionMenu(search_frame, values=sort_options, variable=self.sort_var,
                                       font=(FONT, 14), command=self.filter_salles, width=100,
                                       button_color=THEME["header_bg"], fg_color=THEME["header_bg"])
        sort_menu.pack(side="right", padx=(10, 0))

        self.salle_list_frame = ctk.CTkScrollableFrame(list_panel, fg_color="transparent")
        self.salle_list_frame.pack(fill="both", expand=True, padx=5, pady=(5, 10))

    def create_salle_details_panel(self, parent_frame):
        """Crée le panneau de droite pour afficher les détails et les stats d'une salle."""
        self.details_panel = ctk.CTkFrame(parent_frame, fg_color=THEME["card_bg"], corner_radius=10)
        self.details_panel.grid(row=0, column=1, sticky="nsew")

        self.clear_details_panel()

    def filter_salles(self, *args):
        """Filtre et trie les salles en fonction de la recherche et du tri."""
        search_term = self.search_var.get().lower()
        sort_by = self.sort_var.get()

        all_salles = self.salle_controller.get_all_salles()

        filtered_salles = [
            salle for salle in all_salles
            if search_term in salle.nom.lower() or
               search_term in str(salle.capacite).lower() or
               search_term in salle.type_salle.lower()
        ]

        if sort_by == "nom":
            filtered_salles.sort(key=lambda s: s.nom)
        elif sort_by == "capacite":
            filtered_salles.sort(key=lambda s: s.capacite)
        elif sort_by == "type":
            filtered_salles.sort(key=lambda s: s.type_salle)

        self.display_salle_list(filtered_salles)

    def display_salle_list(self, salles_to_display):
        """Affiche les salles sous forme de liste cliquable."""
        for w in self.salle_list_frame.winfo_children():
            w.destroy()

        if not salles_to_display:
            ctk.CTkLabel(self.salle_list_frame, text="Aucune salle trouvée.",
                          font=(FONT, 14), text_color=THEME["secondary_text"]).pack(pady=20)
            self.clear_details_panel()
            return

        for salle in salles_to_display:
            salle_item_frame = SalleListItem(self.salle_list_frame, salle, self.show_salle_details)
            salle_item_frame.pack(fill="x", padx=5, pady=2)

    def show_salle_details(self, salle, item_frame):
        """Affiche les détails, les stats et le graphique d'une salle sélectionnée."""
        self.selected_salle = salle

        if self.selected_salle_frame:
            self.selected_salle_frame.deselect()
        self.selected_salle_frame = item_frame
        self.selected_salle_frame.select()

        # Effacez d'abord tout le contenu du panneau de détails existant.
        self.clear_details_panel(keep_placeholder=False)

        details_frame = ctk.CTkFrame(self.details_panel, fg_color="transparent")
        details_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Titre
        ctk.CTkLabel(details_frame, text=salle.nom, font=(FONT, 32, "bold"), text_color=THEME["primary_text"]).pack(pady=(0, 20))

        # Détails de la salle
        details_card = ctk.CTkFrame(details_frame, fg_color=THEME["header_bg"], corner_radius=12)
        details_card.pack(fill="x", pady=(0, 20), padx=10)

        def create_detail_row(parent, label, value):
            frame = ctk.CTkFrame(parent, fg_color="transparent")
            frame.pack(fill="x", pady=5)
            ctk.CTkLabel(frame, text=f"{label} :", font=(FONT, 16), text_color=THEME["secondary_text"], width=150, anchor="w").pack(side="left")
            ctk.CTkLabel(frame, text=value, font=(FONT, 16, "bold"), text_color=THEME["primary_text"], anchor="w").pack(side="left", padx=5)

        create_detail_row(details_card, "Capacité", str(salle.capacite))
        create_detail_row(details_card, "Type de salle", salle.type_salle)

        # Panneau des stats et du graphique
        stats_frame = ctk.CTkFrame(details_frame, fg_color=THEME["header_bg"], corner_radius=12)
        stats_frame.pack(fill="both", expand=True, padx=10)

        self.create_stats_and_chart(stats_frame)

        # Boutons d'action
        btn_frame = ctk.CTkFrame(details_frame, fg_color="transparent")
        btn_frame.pack(pady=20)

        try:
            edit_icon = ctk.CTkImage(Image.open("edit.png"), size=(20, 20))
            edit_btn = ctk.CTkButton(btn_frame, text="Modifier", image=edit_icon, compound="left", font=(FONT, 14, "bold"),
                                      fg_color=THEME["accent_blue"], hover_color="#56A192", text_color=THEME["bg_main"],
                                      command=lambda: self.modifier_salle(salle), height=35)
            edit_btn.pack(side="left", padx=10, fill="x", expand=True)
        except FileNotFoundError:
            edit_btn = ctk.CTkButton(btn_frame, text="Modifier", font=(FONT, 14, "bold"),
                                      fg_color=THEME["accent_blue"], hover_color="#56A192", text_color=THEME["bg_main"],
                                      command=lambda: self.modifier_salle(salle), height=35)
            edit_btn.pack(side="left", padx=10, fill="x", expand=True)
            print("Icône 'edit.png' non trouvée. Utilisation du texte par défaut.")

        try:
            delete_icon = ctk.CTkImage(Image.open("delete.png"), size=(20, 20))
            delete_btn = ctk.CTkButton(btn_frame, text="Supprimer", image=delete_icon, compound="left", font=(FONT, 14, "bold"),
                                        fg_color=THEME["error_red"], hover_color="#D14545", text_color=THEME["bg_main"],
                                        command=lambda: self.supprimer_salle(salle), height=35)
            delete_btn.pack(side="left", padx=10, fill="x", expand=True)
        except FileNotFoundError:
            delete_btn = ctk.CTkButton(btn_frame, text="Supprimer", font=(FONT, 14, "bold"),
                                        fg_color=THEME["error_red"], hover_color="#D14545", text_color=THEME["bg_main"],
                                        command=lambda: self.supprimer_salle(salle), height=35)
            delete_btn.pack(side="left", padx=10, fill="x", expand=True)
            print("Icône 'delete.png' non trouvée. Utilisation du texte par défaut.")

    def create_stats_and_chart(self, parent_frame):
        """Crée le graphique et affiche les statistiques globales."""
        type_counts, total_capacite = self.salle_controller.get_salles_stats()

        stats_header = ctk.CTkLabel(parent_frame, text="Statistiques Globales des Salles", font=(FONT, 18, "bold"), text_color=THEME["primary_text"])
        stats_header.pack(pady=(10, 0))

        if not type_counts:
            ctk.CTkLabel(parent_frame, text="Aucune donnée statistique disponible.", font=(FONT, 14, "italic"), text_color=THEME["secondary_text"]).pack(pady=20)
            return

        fig, ax = plt.subplots(facecolor=THEME["header_bg"], figsize=(5, 4))
        fig.patch.set_facecolor(THEME["header_bg"])
        
        types = list(type_counts.keys())
        counts = list(type_counts.values())
        
        bars = ax.bar(types, counts, color=THEME["accent_blue"])
        
        ax.set_title("Nombre de salles par type", color=THEME["primary_text"], font=FONT)
        ax.set_ylabel("Nombre de salles", color=THEME["secondary_text"])
        ax.set_facecolor(THEME["header_bg"])
        
        # Style des axes et des labels
        ax.tick_params(axis='x', colors=THEME["secondary_text"])
        ax.tick_params(axis='y', colors=THEME["secondary_text"])
        ax.spines['bottom'].set_color(THEME["secondary_text"])
        ax.spines['left'].set_color(THEME["secondary_text"])
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)
        
        # Ajouter des étiquettes de données sur les barres
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width() / 2, height, f'{height}',
                     ha='center', va='bottom', color=THEME["success_green"], fontsize=12)

        plt.tight_layout()

        canvas = FigureCanvasTkAgg(fig, master=parent_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True, pady=(5, 10), padx=10)

        # Afficher la capacité totale
        total_capacite_label = ctk.CTkLabel(parent_frame, text=f"Capacité totale de l'établissement : {total_capacite}",
                                              font=(FONT, 14, "bold"), text_color=THEME["success_green"])
        total_capacite_label.pack(pady=(0, 10))

    def clear_details_panel(self, keep_placeholder=True):
        """Efface le contenu du panneau de détails et affiche un message d'attente."""
        for w in self.details_panel.winfo_children():
            w.destroy()

        if keep_placeholder:
            details_placeholder = ctk.CTkLabel(self.details_panel, text="Sélectionnez une salle pour voir les détails",
                                                font=(FONT, 16), text_color=THEME["secondary_text"])
            details_placeholder.pack(expand=True)
            self.selected_salle = None

        if self.selected_salle_frame:
            self.selected_salle_frame.deselect()
            self.selected_salle_frame = None

    def refresh_salles_view(self):
        """Actualise la vue des salles après une action (ajout, modification, suppression)."""
        self.filter_salles()
        self.clear_details_panel()

    def ajouter_salle(self):
        """Ouvre le formulaire d'ajout de salle."""
        self._ouvrir_formulaire("Ajouter")

    def modifier_salle(self, salle_data):
        """Ouvre le formulaire de modification de salle."""
        self._ouvrir_formulaire("Modifier", salle_data)

    def supprimer_salle(self, salle_data):
        """Supprime une salle après confirmation."""
        if messagebox.askyesno("Confirmation", f"Voulez-vous vraiment supprimer la salle « {salle_data.nom} » ?"):
            if self.salle_controller.delete_salle(salle_data.id):
                messagebox.showinfo("Succès", f"La salle '{salle_data.nom}' a été supprimée.")
                self.refresh_salles_view()

    def _ouvrir_formulaire(self, mode, data=None):
        """Ouvre la fenêtre modale du formulaire."""
        form = SalleForm(self.parent, mode, data)
        form.wait_window()
        self.refresh_salles_view()

# --- Composants réutilisables (Reusable Components) ---
class SalleListItem(ctk.CTkFrame):
    """Un élément de liste cliquable pour une salle."""
    def __init__(self, parent, salle_data, command):
        super().__init__(parent, fg_color=THEME["card_bg"], height=40, corner_radius=8, border_color=THEME["border_color"], border_width=1)
        self.salle_data = salle_data
        self.command = command
        self.is_selected = False

        self.label = ctk.CTkLabel(self, text=salle_data.nom, font=(FONT, 14, "bold"), text_color=THEME["primary_text"], anchor="w", padx=15)
        self.label.pack(side="left", fill="both", expand=True)

        self.cap_label = ctk.CTkLabel(self, text=f"{salle_data.capacite} places", font=(FONT, 12), text_color=THEME["secondary_text"], anchor="e", padx=15)
        self.cap_label.pack(side="right", fill="both")

        self.bind("<Button-1>", self.on_click)
        self.label.bind("<Button-1>", self.on_click)
        self.cap_label.bind("<Button-1>", self.on_click)
        
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)
        self.label.bind("<Enter>", self.on_enter)
        self.label.bind("<Leave>", self.on_leave)
        self.cap_label.bind("<Enter>", self.on_enter)
        self.cap_label.bind("<Leave>", self.on_leave)


    def on_click(self, event=None):
        self.command(self.salle_data, self)

    def on_enter(self, event=None):
        if not self.is_selected:
            self.configure(fg_color=THEME["hover_light"])

    def on_leave(self, event=None):
        if not self.is_selected:
            self.configure(fg_color=THEME["card_bg"])

    def select(self):
        self.is_selected = True
        self.configure(fg_color=THEME["select_highlight"])

    def deselect(self):
        self.is_selected = False
        self.configure(fg_color=THEME["card_bg"])

class SalleForm(ctk.CTkToplevel):
    """Fenêtre modale pour ajouter ou modifier une salle."""
    def __init__(self, parent, mode, data=None):
        super().__init__(parent)
        self.parent = parent
        self.mode = mode
        self.data = data

        self.title(f"{mode} une Salle")
        self.geometry("450x350")
        self.transient(parent)
        self.grab_set()
        self.configure(fg_color=THEME["bg_main"])

        self.update_idletasks()
        x = self.parent.winfo_rootx() + (self.parent.winfo_width() - self.winfo_width()) // 2
        y = self.parent.winfo_rooty() + (self.parent.winfo_height() - self.winfo_height()) // 2
        self.geometry(f"+{x}+{y}")

        self._create_widgets()

    def _create_widgets(self):
        """Crée les widgets du formulaire."""
        form_frame = ctk.CTkFrame(self, fg_color=THEME["card_bg"], corner_radius=10)
        form_frame.pack(fill="both", expand=True, padx=20, pady=20)

        ctk.CTkLabel(form_frame, text=f"{self.mode} une salle", font=(FONT, 20, "bold"), text_color=THEME["accent_blue"]).pack(pady=(10, 20))

        self.nom_entry = ctk.CTkEntry(form_frame, placeholder_text="Nom de la salle", font=(FONT, 14), height=35, fg_color=THEME["header_bg"], border_color=THEME["border_color"])
        self.nom_entry.pack(fill="x", pady=5, padx=20)
        if self.data: self.nom_entry.insert(0, self.data.nom)

        self.capacite_entry = ctk.CTkEntry(form_frame, placeholder_text="Capacité", font=(FONT, 14), height=35, fg_color=THEME["header_bg"], border_color=THEME["border_color"])
        self.capacite_entry.pack(fill="x", pady=5, padx=20)
        if self.data: self.capacite_entry.insert(0, self.data.capacite)

        salle_types = ["Général", "Amphithéâtre", "Laboratoire", "Salle de conférence"]
        self.type_optionmenu = ctk.CTkOptionMenu(form_frame, values=salle_types, font=(FONT, 14), height=35, fg_color=THEME["header_bg"], button_color=THEME["header_bg"], button_hover_color=THEME["accent_blue"])
        self.type_optionmenu.pack(fill="x", pady=5, padx=20)
        if self.data and self.data.type_salle in salle_types:
            self.type_optionmenu.set(self.data.type_salle)
        else:
            self.type_optionmenu.set(salle_types[0])

        btn_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        btn_frame.pack(pady=(20, 10))

        ctk.CTkButton(btn_frame, text="Enregistrer", font=(FONT, 14, "bold"),
                                  command=self._save_data, fg_color=THEME["accent_blue"], hover_color="#56A192", text_color=THEME["bg_main"]).pack(side="left", padx=10)
        ctk.CTkButton(btn_frame, text="Annuler", font=(FONT, 14, "bold"),
                                  command=self.destroy, fg_color=THEME["error_red"], hover_color="#D14545", text_color=THEME["bg_main"]).pack(side="left", padx=10)

    def _save_data(self):
        """Valide et enregistre les données du formulaire."""
        nom = self.nom_entry.get().strip()
        capacite = self.capacite_entry.get().strip()
        type_salle = self.type_optionmenu.get()

        if not nom:
            messagebox.showerror("Erreur de saisie", "Le nom de la salle est obligatoire.")
            return
        if not capacite or not capacite.isdigit() or int(capacite) <= 0:
            messagebox.showerror("Erreur de saisie", "La capacité doit être un nombre entier positif.")
            return

        if self.mode == "Ajouter":
            if salle_controller.add_salle(nom, int(capacite), type_salle):
                messagebox.showinfo("Succès", f"La salle '{nom}' a été ajoutée avec succès.")
        else: # mode == "Modifier"
            if salle_controller.update_salle(self.data.id, nom, int(capacite), type_salle):
                messagebox.showinfo("Succès", f"La salle '{nom}' a été mise à jour avec succès.")

        self.destroy()

if __name__ == "__main__":
    if salle_controller.conn:
        app = App()
        app.mainloop()
    else:
        print("L'application n'a pas pu démarrer en raison d'une erreur de connexion à la base de données.")