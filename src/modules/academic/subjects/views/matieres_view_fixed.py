import customtkinter as ctk
from tkinter import messagebox
from database.connection import get_db_connection
from modules.academic.subjects.controllers.matieres_controller import (
    get_all_matieres, add_matiere, update_matiere, delete_matiere,
    get_classes_by_niveau, get_all_professeurs
)

# Couleurs du thème
BG_MAIN = "#0A192F"
BG_SIDEBAR = "#172A45"
BG_CARD = "#0B2039"
BORDER_COLOR = "#334155"
ACCENT = "#64FFDA"
TEXT_PRIMARY = "#CCD6F6"
TEXT_SECONDARY = "#8892B0"
ERROR_RED = "#FF6363"
SUCCESS_GREEN = "#22c55e"
WARNING_YELLOW = "#f59e0b"

class MatieresView(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color=BG_MAIN)
        self.selected_matiere = None
        self.selected_niveau = "Primaire"
        self.professeurs = []
        self.classes_selected = {}
        
        self.setup_ui()
        self.load_data()
        self.refresh_table()
    
    def setup_ui(self):
        # Configuration de la grille
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=0, minsize=300)
        
        # Contenu principal
        self.main_content = ctk.CTkFrame(self, fg_color="transparent")
        self.main_content.grid(row=0, column=0, sticky="nsew", padx=(10, 5), pady=10)
        self.main_content.grid_rowconfigure(1, weight=1)
        self.main_content.grid_columnconfigure(0, weight=1)
        
        # En-tête
        self.create_header()
        
        # Tableau
        self.create_table()
        
        # Sidebar
        self.create_sidebar()
    
    def create_header(self):
        header_frame = ctk.CTkFrame(self.main_content, fg_color="transparent")
        header_frame.grid(row=0, column=0, sticky="ew", pady=(0, 15))
        header_frame.grid_columnconfigure(0, weight=1)
        
        # Titre
        title_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        title_frame.grid(row=0, column=0, sticky="w")
        
        ctk.CTkLabel(
            title_frame, 
            text="Gestion des Matières", 
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color=ACCENT
        ).pack(anchor="w")
        
        ctk.CTkLabel(
            title_frame, 
            text="Gérez les matières et leurs associations avec les classes",
            font=ctk.CTkFont(size=14),
            text_color=TEXT_SECONDARY
        ).pack(anchor="w", pady=(2, 0))
        
        # Boutons d'action
        actions_frame = ctk.CTkFrame(header_frame, fg_color=BG_CARD, corner_radius=10)
        actions_frame.grid(row=0, column=1, sticky="e")
        
        # Bouton Ajouter
        add_btn = ctk.CTkButton(
            actions_frame,
            text="➕ Ajouter",
            command=self.open_add_modal,
            fg_color=SUCCESS_GREEN,
            hover_color="#1ea854",
            font=ctk.CTkFont(size=14, weight="bold"),
            height=40,
            width=120
        )
        add_btn.pack(side="left", padx=(10, 5), pady=10)
        
        # Bouton Modifier
        edit_btn = ctk.CTkButton(
            actions_frame,
            text="✏️ Modifier",
            command=self.open_edit_modal,
            fg_color=WARNING_YELLOW,
            hover_color="#d97706",
            font=ctk.CTkFont(size=14, weight="bold"),
            height=40,
            width=120
        )
        edit_btn.pack(side="left", padx=5, pady=10)
        
        # Bouton Supprimer
        delete_btn = ctk.CTkButton(
            actions_frame,
            text="🗑️ Supprimer",
            command=self.delete_matiere,
            fg_color=ERROR_RED,
            hover_color="#dc2626",
            font=ctk.CTkFont(size=14, weight="bold"),
            height=40,
            width=120
        )
        delete_btn.pack(side="left", padx=5, pady=10)
    
    def create_table(self):
        table_frame = ctk.CTkFrame(self.main_content, fg_color=BG_CARD, corner_radius=16)
        table_frame.grid(row=1, column=0, sticky="nsew")
        table_frame.grid_rowconfigure(0, weight=1)
        table_frame.grid_columnconfigure(0, weight=1)
        
        # En-tête du tableau
        table_header = ctk.CTkFrame(table_frame, fg_color="transparent")
        table_header.pack(fill="x", padx=15, pady=(15, 5))
        
        ctk.CTkLabel(
            table_header,
            text="Liste des Matières",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color=TEXT_PRIMARY
        ).pack(side="left")
        
        # Tableau
        from customtkinter import CTkTable
        
        self.table = CTkTable(
            master=table_frame,
            row=0,
            column=4,
            values=[["ID", "Nom", "Coefficient", "Statut"]],
            header_color=BG_SIDEBAR,
            header_text_color=ACCENT,
            fg_color=BG_CARD,
            text_color=TEXT_PRIMARY,
            font=ctk.CTkFont(size=12),
            corner_radius=8,
            border_width=1,
            border_color=BORDER_COLOR
        )
        self.table.pack(expand=True, fill="both", padx=15, pady=(5, 15))
        
        # Bind click event
        self.table.bind("<Button-1>", self.on_table_click)
    
    def create_sidebar(self):
        sidebar = ctk.CTkFrame(self, fg_color=BG_SIDEBAR, width=300, corner_radius=16)
        sidebar.grid(row=0, column=1, sticky="nsew", padx=(5, 10), pady=10)
        sidebar.grid_propagate(False)
        
        # Titre sidebar
        ctk.CTkLabel(
            sidebar,
            text="Filtres",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color=ACCENT
        ).pack(pady=(15, 10))
        
        # Filtre par niveau
        niveau_frame = ctk.CTkFrame(sidebar, fg_color="transparent")
        niveau_frame.pack(fill="x", padx=15, pady=(0, 15))
        
        ctk.CTkLabel(
            niveau_frame,
            text="Niveau",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=TEXT_PRIMARY
        ).pack(anchor="w")
        
        self.niveau_var = ctk.StringVar(value="Primaire")
        niveau_menu = ctk.CTkOptionMenu(
            niveau_frame,
            variable=self.niveau_var,
            values=["Primaire", "Collège", "Lycée"],
            command=self.on_niveau_change,
            fg_color=BG_CARD,
            button_color=ACCENT,
            button_hover_color="#4A90E2",
            font=ctk.CTkFont(size=12)
        )
        niveau_menu.pack(fill="x", pady=(5, 0))
        
        # Statistiques
        stats_frame = ctk.CTkFrame(sidebar, fg_color=BG_CARD, corner_radius=8)
        stats_frame.pack(fill="x", padx=15, pady=(0, 15))
        
        ctk.CTkLabel(
            stats_frame,
            text="Statistiques",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=ACCENT
        ).pack(pady=(10, 5))
        
        self.stats_label = ctk.CTkLabel(
            stats_frame,
            text="Chargement...",
            font=ctk.CTkFont(size=12),
            text_color=TEXT_SECONDARY
        )
        self.stats_label.pack(pady=(0, 10))
    
    def load_data(self):
        try:
            self.professeurs = get_all_professeurs()
            print(f"✅ {len(self.professeurs)} professeurs chargés")
        except Exception as e:
            print(f"❌ Erreur lors du chargement des professeurs: {e}")
            self.professeurs = []
    
    def refresh_table(self):
        try:
            matieres = get_all_matieres()
            
            # Préparer les données pour le tableau
            table_data = [["ID", "Nom", "Coefficient", "Statut"]]
            
            for matiere in matieres:
                table_data.append([
                    str(matiere['id_matiere']),
                    matiere['nom_matiere'],
                    str(matiere['coefficient']),
                    matiere['statut']
                ])
            
            # Mettre à jour le tableau
            self.table.update_values(table_data)
            
            # Mettre à jour les statistiques
            total = len(matieres)
            actives = len([m for m in matieres if m['statut'] == 'active'])
            self.stats_label.configure(
                text=f"Total: {total}\nActives: {actives}\nInactives: {total - actives}"
            )
            
        except Exception as e:
            print(f"❌ Erreur lors du rafraîchissement: {e}")
            messagebox.showerror("Erreur", f"Erreur lors du chargement des données: {e}")
    
    def on_niveau_change(self, niveau):
        self.selected_niveau = niveau
        print(f"🔍 Niveau sélectionné: {niveau}")
    
    def on_table_click(self, event):
        try:
            # Calculer la ligne cliquée
            row_height = 30
            clicked_row = int(event.y / row_height)
            
            if clicked_row > 0 and clicked_row < len(self.table.values):  # Ignorer l'en-tête
                # Désélectionner toutes les lignes
                for i in range(len(self.table.values)):
                    self.table.deselect(i, 0)
                
                # Sélectionner la ligne cliquée
                self.table.select(clicked_row, 0)
                
                # Récupérer les données de la matière
                matiere_data = self.table.values[clicked_row]
                self.selected_matiere = {
                    'id_matiere': int(matiere_data[0]),
                    'nom_matiere': matiere_data[1],
                    'coefficient': float(matiere_data[2]),
                    'statut': matiere_data[3]
                }
                
                print(f"🔍 Matière sélectionnée - ID: {self.selected_matiere['id_matiere']}, Nom: {self.selected_matiere['nom_matiere']}")
                
        except Exception as e:
            print(f"❌ Erreur lors du clic sur le tableau: {e}")
    
    def open_add_modal(self):
        self.matiere_modal("Ajouter")
    
    def open_edit_modal(self):
        if not self.selected_matiere:
            messagebox.showwarning("Attention", "Veuillez sélectionner une matière à modifier.")
            return
        self.matiere_modal("Modifier", self.selected_matiere)
    
    def matiere_modal(self, mode, matiere_data=None):
        modal = ctk.CTkToplevel(self)
        modal.title(f"{mode} Matière")
        modal.geometry("600x500")
        modal.transient(self)
        modal.grab_set()
        modal.configure(fg_color=BG_MAIN)
        
        # Contenu principal
        content_frame = ctk.CTkFrame(modal, fg_color="transparent")
        content_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # En-tête
        header_frame = ctk.CTkFrame(content_frame, fg_color=BG_CARD, corner_radius=12)
        header_frame.pack(fill="x", pady=(0, 20))
        
        title_text = f"Nouvelle Matière" if mode == "Ajouter" else f"Modifier {matiere_data['nom_matiere']}"
        ctk.CTkLabel(
            header_frame,
            text=title_text,
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color=ACCENT
        ).pack(pady=20)
        
        # Formulaire
        form_frame = ctk.CTkFrame(content_frame, fg_color=BG_CARD, corner_radius=12)
        form_frame.pack(fill="both", expand=True)
        
        # Nom de la matière
        nom_label = ctk.CTkLabel(form_frame, text="Nom de la matière", 
                               font=ctk.CTkFont(size=14, weight="bold"), 
                               text_color=TEXT_PRIMARY)
        nom_label.pack(anchor="w", padx=20, pady=(20, 5))
        
        self.nom_entry = ctk.CTkEntry(form_frame, placeholder_text="Ex: Mathématiques", 
                                    font=ctk.CTkFont(size=14), height=40)
        self.nom_entry.pack(fill="x", padx=20, pady=(0, 15))
        
        # Coefficient
        coef_label = ctk.CTkLabel(form_frame, text="Coefficient", 
                                font=ctk.CTkFont(size=14, weight="bold"), 
                                text_color=TEXT_PRIMARY)
        coef_label.pack(anchor="w", padx=20, pady=(0, 5))
        
        self.coef_entry = ctk.CTkEntry(form_frame, placeholder_text="Ex: 3.0", 
                                     font=ctk.CTkFont(size=14), height=40)
        self.coef_entry.pack(fill="x", padx=20, pady=(0, 15))
        
        # Niveau
        niveau_label = ctk.CTkLabel(form_frame, text="Niveau", 
                                  font=ctk.CTkFont(size=14, weight="bold"), 
                                  text_color=TEXT_PRIMARY)
        niveau_label.pack(anchor="w", padx=20, pady=(0, 5))
        
        self.niveau_var_modal = ctk.StringVar(value=self.selected_niveau)
        niveau_menu = ctk.CTkOptionMenu(
            form_frame,
            variable=self.niveau_var_modal,
            values=["Primaire", "Collège", "Lycée"],
            command=self.on_niveau_change_modal,
            fg_color=BG_MAIN,
            button_color=ACCENT,
            button_hover_color="#4A90E2",
            font=ctk.CTkFont(size=14),
            height=40
        )
        niveau_menu.pack(fill="x", padx=20, pady=(0, 15))
        
        # Classes
        classes_label = ctk.CTkLabel(form_frame, text="Classes", 
                                   font=ctk.CTkFont(size=14, weight="bold"), 
                                   text_color=TEXT_PRIMARY)
        classes_label.pack(anchor="w", padx=20, pady=(0, 5))
        
        classes_frame = ctk.CTkFrame(form_frame, fg_color=BG_SIDEBAR, 
                                   corner_radius=8, height=80)
        classes_frame.pack(fill="x", padx=20, pady=(0, 15))
        
        # Liste des classes avec cases à cocher - HORIZONTAL
        self.classes_selected = {}
        try:
            classes_niveau = get_classes_by_niveau(self.niveau_var_modal.get())
            print(f"🔍 DEBUG: classes_niveau = {classes_niveau}")
            
            if not classes_niveau:
                print("⚠️ Aucune classe trouvée pour ce niveau")
                no_classes_label = ctk.CTkLabel(classes_frame, text="Aucune classe disponible", 
                                               font=ctk.CTkFont(size=12), text_color=TEXT_SECONDARY)
                no_classes_label.pack(anchor="w", pady=5, padx=10)
            else:
                # Créer un frame horizontal pour les checkboxes
                checkboxes_frame = ctk.CTkFrame(classes_frame, fg_color="transparent")
                checkboxes_frame.pack(fill="x", padx=10, pady=10)
                
                for i, (classe_id, classe_data) in enumerate(classes_niveau.items()):
                    # Vérifier le nombre de matières existantes pour cette classe
                    conn = get_db_connection()
                    cursor = conn.cursor()
                    cursor.execute("""
                        SELECT COUNT(*) FROM classe_matieres 
                        WHERE id_classe = ? AND statut = 'active'
                    """, (classe_id,))
                    nb_matieres = cursor.fetchone()[0]
                    conn.close()
                    
                    var = ctk.BooleanVar()
                    # Désactiver la checkbox si la classe a déjà 10 matières
                    is_disabled = nb_matieres >= 10
                    
                    # Texte avec indication du nombre de matières
                    classe_text = f"{classe_data['nom_classe']} ({nb_matieres}/10)"
                    
                    checkbox = ctk.CTkCheckBox(checkboxes_frame, text=classe_text, 
                                      variable=var, font=ctk.CTkFont(size=12),
                                      fg_color=ACCENT, hover_color="#4A90E2",
                                      state="disabled" if is_disabled else "normal")
                    checkbox.pack(side="left", padx=(0, 15), pady=5)
                    self.classes_selected[classe_id] = var
                    
                    # Ajouter un tooltip ou indication visuelle si saturée
                    if is_disabled:
                        checkbox.configure(text_color=TEXT_SECONDARY)
                    
                    print(f"✅ Checkbox créée pour {classe_data['nom_classe']} - {nb_matieres}/10 matières")
        except Exception as e:
            print(f"❌ Erreur lors du chargement des classes: {e}")
            error_label = ctk.CTkLabel(classes_frame, text=f"Erreur: {str(e)}", 
                                      font=ctk.CTkFont(size=12), text_color=ERROR_RED)
            error_label.pack(anchor="w", pady=5, padx=10)
        
        # Professeur
        prof_label = ctk.CTkLabel(form_frame, text="Professeur assigné", 
                                font=ctk.CTkFont(size=14, weight="bold"), 
                                text_color=TEXT_PRIMARY)
        prof_label.pack(anchor="w", padx=20, pady=(0, 5))
        
        # Préparer les options de professeurs
        prof_options = ["Aucun"]
        for prof in self.professeurs:
            if isinstance(prof, dict):
                prof_options.append(f"{prof['nom']} {prof['prenom']}")
            else:
                prof_options.append(f"{prof.nom} {prof.prenom}")
        
        self.professeur_var = ctk.StringVar(value="Aucun")
        prof_menu = ctk.CTkOptionMenu(
            form_frame,
            variable=self.professeur_var,
            values=prof_options,
            fg_color=BG_MAIN,
            button_color=ACCENT,
            button_hover_color="#4A90E2",
            font=ctk.CTkFont(size=14),
            height=40
        )
        prof_menu.pack(fill="x", padx=20, pady=(0, 20))
        
        # Boutons
        buttons_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        buttons_frame.pack(fill="x", padx=20, pady=(0, 20))
        
        # Bouton Valider
        if mode == "Ajouter":
            validate_btn = ctk.CTkButton(
                buttons_frame,
                text="✅ Valider",
                command=lambda: self.save_matiere(modal),
                fg_color=SUCCESS_GREEN,
                hover_color="#1ea854",
                font=ctk.CTkFont(size=14, weight="bold"),
                height=40
            )
        else:
            validate_btn = ctk.CTkButton(
                buttons_frame,
                text="✅ Mettre à jour",
                command=lambda: self.update_matiere(modal),
                fg_color=SUCCESS_GREEN,
                hover_color="#1ea854",
                font=ctk.CTkFont(size=14, weight="bold"),
                height=40
            )
        validate_btn.pack(side="right", padx=(10, 0))
        
        # Bouton Annuler
        cancel_btn = ctk.CTkButton(
            buttons_frame,
            text="❌ Annuler",
            command=modal.destroy,
            fg_color=ERROR_RED,
            hover_color="#dc2626",
            font=ctk.CTkFont(size=14, weight="bold"),
            height=40
        )
        cancel_btn.pack(side="right")
        
        # Pré-remplir les champs si modification
        if matiere_data:
            self.nom_entry.insert(0, matiere_data['nom_matiere'])
            self.coef_entry.insert(0, str(matiere_data['coefficient']))
    
    def on_niveau_change_modal(self, niveau):
        print(f"🔍 Niveau modal changé: {niveau}")
        # Recharger les classes pour le nouveau niveau
        # Cette fonctionnalité pourrait être implémentée si nécessaire
    
    def save_matiere(self, modal):
        try:
            nom = self.nom_entry.get().strip()
            coefficient = float(self.coef_entry.get().strip())
            
            if not nom:
                messagebox.showerror("Erreur", "Le nom de la matière est obligatoire.")
                return
            
            # Vérifier que toutes les classes sélectionnées ont moins de 10 matières
            classes_saturées = []
            for classe_id, var in self.classes_selected.items():
                if var.get():  # Si la classe est sélectionnée
                    conn = get_db_connection()
                    cursor = conn.cursor()
                    cursor.execute("""
                        SELECT COUNT(*) FROM classe_matieres 
                        WHERE id_classe = ? AND statut = 'active'
                    """, (classe_id,))
                    nb_matieres = cursor.fetchone()[0]
                    conn.close()
                    
                    if nb_matieres >= 10:
                        classes_saturées.append(classe_id)
            
            if classes_saturées:
                messagebox.showerror("Erreur", f"Les classes suivantes ont déjà 10 matières: {classes_saturées}")
                return
            
            print("✅ Vérification OK: toutes les classes ont moins de 10 matières")
            
            # Récupérer l'ID du professeur
            professeur_nom = self.professeur_var.get()
            professeur_id = None
            if professeur_nom != "Aucun":
                try:
                    if isinstance(self.professeurs, dict):
                        for prof_id, prof_data in self.professeurs.items():
                            if f"{prof_data['nom']} {prof_data['prenom']}" == professeur_nom:
                                professeur_id = prof_id
                                break
                    else:
                        for prof_data in self.professeurs:
                            if f"{prof_data['nom']} {prof_data['prenom']}" == professeur_nom:
                                professeur_id = prof_data.get('id')
                                break
                except Exception as e:
                    print(f"❌ Erreur lors de la recherche du professeur: {e}")
                    professeur_id = None
            
            # Sauvegarder en base
            conn = get_db_connection()
            cursor = conn.cursor()
            
            # Créer la matière
            cursor.execute("""
                INSERT INTO matieres (nom_matiere, coefficient, description)
                VALUES (?, ?, ?)
            """, (nom, coefficient, f"Matière {nom} - Niveau {self.niveau_var_modal.get()}"))
            
            # Récupérer l'ID de la matière créée
            matiere_id = cursor.lastrowid
            
            # Associer la matière aux classes sélectionnées
            for classe_id, var in self.classes_selected.items():
                if var.get():  # Si la classe est sélectionnée
                    cursor.execute("""
                        INSERT INTO classe_matieres (id_classe, id_matiere, id_professeur, statut)
                        VALUES (?, ?, ?, 'active')
                    """, (classe_id, matiere_id, professeur_id))
            
            conn.commit()
            conn.close()
            
            messagebox.showinfo("Succès", f"Matière '{nom}' créée avec succès!")
            modal.destroy()
            self.refresh_table()
            
        except ValueError:
            messagebox.showerror("Erreur", "Le coefficient doit être un nombre valide.")
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de la création: {e}")
    
    def update_matiere(self, modal):
        try:
            nom = self.nom_entry.get().strip()
            coefficient = float(self.coef_entry.get().strip())
            
            if not nom:
                messagebox.showerror("Erreur", "Le nom de la matière est obligatoire.")
                return
            
            # Récupérer l'ID du professeur
            professeur_nom = self.professeur_var.get()
            professeur_id = None
            if professeur_nom != "Aucun":
                try:
                    if isinstance(self.professeurs, dict):
                        for prof_id, prof_data in self.professeurs.items():
                            prof_full_name = f"{prof_data['nom']} {prof_data['prenom']}"
                            print(f"🔍 DEBUG: Comparaison - '{prof_full_name}' vs '{professeur_nom}'")
                            if prof_full_name == professeur_nom:
                                professeur_id = prof_id
                                print(f"🔍 DEBUG: Professeur trouvé - ID: {professeur_id}")
                                break
                    else:
                        for prof_data in self.professeurs:
                            prof_full_name = f"{prof_data['nom']} {prof_data['prenom']}"
                            print(f"🔍 DEBUG: Comparaison - '{prof_full_name}' vs '{professeur_nom}'")
                            if prof_full_name == professeur_nom:
                                professeur_id = prof_data.get('id')
                                print(f"🔍 DEBUG: Professeur trouvé - ID: {professeur_id}")
                                break
                except Exception as e:
                    print(f"❌ Erreur lors de la recherche du professeur: {e}")
                    professeur_id = None

            print(f"🔍 DEBUG: professeur_id final: {professeur_id}")
            # Mettre à jour en base
            conn = get_db_connection()
            cursor = conn.cursor()
            
            # Mettre à jour la matière
            cursor.execute("""
                UPDATE matieres 
                SET nom_matiere = ?, coefficient = ?
                WHERE id_matiere = ?
            """, (nom, coefficient, self.selected_matiere['id_matiere']))
            
            # Mettre à jour les associations classe-matière
            for classe_id, var in self.classes_selected.items():
                if var.get():  # Si la classe est sélectionnée
                    # Vérifier si l'association existe déjà
                    cursor.execute("""
                        SELECT id FROM classe_matieres 
                        WHERE id_classe = ? AND id_matiere = ?
                    """, (classe_id, self.selected_matiere['id_matiere']))
                    
                    if cursor.fetchone():
                        # Mettre à jour l'association existante
                        cursor.execute("""
                            UPDATE classe_matieres 
                            SET id_professeur = ?, statut = 'active'
                            WHERE id_classe = ? AND id_matiere = ?
                        """, (professeur_id, classe_id, self.selected_matiere['id_matiere']))
                    else:
                        # Créer une nouvelle association
                        cursor.execute("""
                            INSERT INTO classe_matieres (id_classe, id_matiere, id_professeur, statut)
                            VALUES (?, ?, ?, 'active')
                        """, (classe_id, self.selected_matiere['id_matiere'], professeur_id))
            
            conn.commit()
            conn.close()
            
            messagebox.showinfo("Succès", f"Matière '{nom}' mise à jour avec succès!")
            modal.destroy()
            self.refresh_table()
            
        except ValueError:
            messagebox.showerror("Erreur", "Le coefficient doit être un nombre valide.")
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de la mise à jour: {e}")
    
    def delete_matiere(self):
        if not self.selected_matiere:
            messagebox.showwarning("Attention", "Veuillez sélectionner une matière à supprimer.")
            return
        
        # Confirmation
        if messagebox.askyesno("Confirmation", 
                              f"Voulez-vous vraiment supprimer la matière '{self.selected_matiere['nom_matiere']}' ?"):
            try:
                # Supprimer la matière
                delete_matiere(self.selected_matiere['id_matiere'])
                
                messagebox.showinfo("Succès", "Matière supprimée avec succès!")
                self.selected_matiere = None
                self.refresh_table()
                
            except Exception as e:
                messagebox.showerror("Erreur", f"Erreur lors de la suppression: {e}")
