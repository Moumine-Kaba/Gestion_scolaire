import customtkinter as ctk
from tkinter import messagebox
import os
import sys
import math

# Importations des contrôleurs
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from controllers.enseignement_controller import get_all_enseignements, add_enseignement, update_enseignement, delete_enseignement
from controllers.professeur_controller import get_all_professeurs
from controllers.classe_controller import get_all_classes
from controllers.matiere_controller import get_all_matieres
from controllers.salle_controller import get_all_salles

# =================== IMPORT THEME ET COULEURS =====================
try:
    from main import THEME, FONT_FAMILY, FONT_SIZE_HEADER, FONT_SIZE_SUBHEADER, FONT_SIZE_TEXT
    from main import load_ctk_icon, ICON_MAP
except ImportError:
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
        "select_highlight": "#2A456C"
    }
    FONT_FAMILY = "Segoe UI"
    FONT_SIZE_HEADER = 20
    FONT_SIZE_SUBHEADER = 16
    FONT_SIZE_TEXT = 14

    def load_ctk_icon(icon_name, size=(22, 22)):
        try:
            from PIL import Image
            ICON_PATH = "assets/icons"
            path = os.path.join(ICON_PATH, icon_name)
            image = Image.open(path).resize(size, Image.Resampling.LANCZOS)
            return ctk.CTkImage(light_image=image, dark_image=image)
        except Exception:
            return None

    ICON_MAP = {
        "add": "add.png", "edit": "edit.png", "delete": "delete.png",
        "refresh": "refresh.png", "search": "search.png", "close": "close.png",
        "professor": "person.png", "class": "stacks.png", "subject": "book.png",
        "room": "door.png", "assignment": "assignment.png", "duplicate": "copy.png",
        "calendar": "calendar.png", "timer": "clock.png", "status": "status.png"
    }


class EnseignementsView(ctk.CTkFrame):
    def __init__(self, parent, icons):
        super().__init__(parent, fg_color=THEME["bg_main"])
        self.icons = icons
        self.grid_columnconfigure(0, weight=1)
        self.selected_item_frame = None
        self.selected_item_data = None
        self.search_term = ctk.StringVar()
        self.filter_var = ctk.StringVar(value="Tous")

        self._build_header()
        self._build_list_container()
        self._build_actions()
        self.rafraichir_liste()

    def _build_header(self):
        header_frame = ctk.CTkFrame(self, fg_color=THEME["header_bg"], corner_radius=10)
        header_frame.pack(fill="x", padx=10, pady=(10, 5))
        header_frame.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            header_frame, text="Gestion des Enseignements",
            font=(FONT_FAMILY, FONT_SIZE_HEADER, "bold"),
            text_color=THEME["accent_blue"]
        ).grid(row=0, column=0, sticky="w", padx=10, pady=(8, 0))
        
        ctk.CTkLabel(
            header_frame, text="Associez professeurs, classes, matières et salles.",
            font=(FONT_FAMILY, max(FONT_SIZE_TEXT-2, 10)),
            text_color=THEME["secondary_text"]
        ).grid(row=1, column=0, sticky="w", padx=10, pady=(0, 8))

        right_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        right_frame.grid(row=0, column=1, rowspan=2, sticky="e", padx=8, pady=8)

        add_icon = load_ctk_icon(ICON_MAP.get("add", "add.png"), size=(18, 18))
        refresh_icon = load_ctk_icon(ICON_MAP.get("refresh", "refresh.png"), size=(18, 18))
        
        search_frame = ctk.CTkFrame(right_frame, fg_color="transparent")
        search_frame.pack(side="left", padx=4)
        
        search_icon = load_ctk_icon(ICON_MAP.get("search"), size=(16, 16))
        search_label = ctk.CTkLabel(search_frame, image=search_icon, text="")
        search_label.pack(side="left", padx=2)

        self.search_entry = ctk.CTkEntry(
            search_frame, placeholder_text="Rechercher...",
            font=(FONT_FAMILY, FONT_SIZE_TEXT),
            textvariable=self.search_term,
            fg_color=THEME["card_bg"],
            border_color=THEME["border_color"],
            height=28
        )
        self.search_entry.pack(side="left", fill="x", expand=True)
        self.search_entry.bind("<KeyRelease>", lambda event: self.rafraichir_liste())
        
        filter_options = ["Tous", "Professeur", "Classe", "Matière", "Salle", "Statut"]
        self.filter_combobox = ctk.CTkComboBox(
            right_frame, values=filter_options,
            command=lambda value: self.rafraichir_liste(),
            variable=self.filter_var,
            font=(FONT_FAMILY, FONT_SIZE_TEXT),
            height=28
        )
        self.filter_combobox.pack(side="left", padx=4)

        ctk.CTkButton(
            right_frame, text=" Ajouter", image=add_icon, compound="left",
            font=(FONT_FAMILY, FONT_SIZE_TEXT, "bold"),
            fg_color=THEME["accent_blue"], text_color=THEME["bg_main"],
            hover_color="#45b69c", command=self.ajouter, height=28
        ).pack(side="left", padx=4)

        ctk.CTkButton(
            right_frame, text=" Actualiser", image=refresh_icon, compound="left",
            font=(FONT_FAMILY, FONT_SIZE_TEXT, "bold"),
            fg_color=THEME["card_bg"], text_color=THEME["primary_text"],
            hover_color=THEME["header_bg"], command=self.rafraichir_liste, height=28
        ).pack(side="left")

    def _build_list_container(self):
        self.list_container = ctk.CTkScrollableFrame(self, fg_color="transparent", corner_radius=10)
        self.list_container.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        self.list_container.grid_columnconfigure((0, 1), weight=1, uniform="card")

    def _build_actions(self):
        actions_frame = ctk.CTkFrame(self, fg_color="transparent")
        actions_frame.pack(fill="x", pady=(0, 10), padx=10)

        edit_icon = load_ctk_icon(ICON_MAP.get("edit", "edit.png"), size=(18, 18))
        delete_icon = load_ctk_icon(ICON_MAP.get("delete", "delete.png"), size=(18, 18))

        ctk.CTkButton(
            actions_frame, text=" Modifier", image=edit_icon, compound="left",
            font=(FONT_FAMILY, FONT_SIZE_TEXT, "bold"),
            fg_color=THEME["info_orange"], text_color=THEME["bg_main"],
            hover_color="#cc9f13", command=self.modifier, height=28
        ).pack(side="left", padx=5)

        ctk.CTkButton(
            actions_frame, text=" Supprimer", image=delete_icon, compound="left",
            font=(FONT_FAMILY, FONT_SIZE_TEXT, "bold"),
            fg_color=THEME["error_red"], text_color=THEME["bg_main"],
            hover_color="#dc2626", command=self.supprimer, height=28
        ).pack(side="left")
    
    def rafraichir_liste(self):
        self.selected_item_frame = None
        self.selected_item_data = None
        
        for widget in self.list_container.winfo_children():
            widget.destroy()

        profs = {p["id"]: f"{p['nom']} {p['prenom']}" for p in get_all_professeurs()}
        classes = {c["id"]: c["nom"] for c in get_all_classes()}
        matieres = {m["id"]: m["nom"] for m in get_all_matieres()}
        salles = {s["id"]: s["nom"] for s in get_all_salles()}

        enseignements = get_all_enseignements()
        
        search_term = self.search_term.get().lower()
        filter_type = self.filter_var.get()

        # Filtrage
        filtered_enseignements = []
        for ens in enseignements:
            prof_name = profs.get(ens["professeur_id"], "Inconnu").lower()
            classe_name = classes.get(ens["classe_id"], "Inconnue").lower()
            matiere_name = matieres.get(ens["matiere_id"], "Inconnue").lower()
            salle_name = salles.get(ens["salle_id"], "Non spécifiée").lower()
            jours_cours_str = ens.get("jours_cours", "Non spécifié")
            statut = str(ens.get("statut", "Non spécifié")).lower()

            match_search = not search_term or (
                search_term in prof_name or 
                search_term in classe_name or 
                search_term in matiere_name or 
                search_term in salle_name or 
                search_term in jours_cours_str.lower() or 
                search_term in statut
            )
            
            match_filter = True
            if filter_type == "Professeur" and search_term and search_term not in prof_name:
                match_filter = False
            elif filter_type == "Classe" and search_term and search_term not in classe_name:
                match_filter = False
            elif filter_type == "Matière" and search_term and search_term not in matiere_name:
                match_filter = False
            elif filter_type == "Salle" and search_term and search_term not in salle_name:
                match_filter = False
            elif filter_type == "Statut" and search_term and search_term not in statut:
                match_filter = False
            
            if match_search and match_filter:
                filtered_enseignements.append(ens)
        
        if not filtered_enseignements:
            ctk.CTkLabel(
                self.list_container, text="Aucun enseignement trouvé.",
                font=(FONT_FAMILY, FONT_SIZE_SUBHEADER, "italic"),
                text_color=THEME["secondary_text"]
            ).grid(row=0, column=0, columnspan=2, pady=20, sticky="nsew")
            return

        for i, row_data in enumerate(filtered_enseignements):
            self.create_enseignement_card(self.list_container, row_data, profs, classes, matieres, salles, i)

    def create_enseignement_card(self, parent_frame, data, profs, classes, matieres, salles, index):
        card_frame = ctk.CTkFrame(parent_frame, fg_color=THEME["card_bg"], corner_radius=10, border_width=1, border_color=THEME["card_bg"])
        card_frame.grid(row=index // 2, column=index % 2, padx=5, pady=5, sticky="nsew")
        card_frame.grid_columnconfigure(0, weight=1)

        # En-tête de la carte avec la matière et le statut
        header_frame = ctk.CTkFrame(card_frame, fg_color="transparent")
        header_frame.pack(fill="x", padx=12, pady=(12, 4))
        header_frame.grid_columnconfigure(0, weight=1)

        matiere_name = matieres.get(data["matiere_id"], "Inconnue")
        ctk.CTkLabel(header_frame, text=matiere_name.upper(), 
                     font=(FONT_FAMILY, FONT_SIZE_SUBHEADER, "bold"), 
                     text_color=THEME["accent_blue"]).grid(row=0, column=0, sticky="w")

        status_text = data.get("statut", "Actif")
        status_color = THEME["success_green"] if status_text and status_text.lower() == "actif" else THEME["error_red"] if status_text and status_text.lower() == "archivé" else THEME["secondary_text"]        
        status_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        status_frame.grid(row=0, column=1, sticky="e")
        
        ctk.CTkLabel(status_frame, text="", width=10, height=10, corner_radius=5, fg_color=status_color).pack(side="left", padx=(0, 5))
        ctk.CTkLabel(status_frame, text=status_text,
                     font=(FONT_FAMILY, FONT_SIZE_TEXT),
                     text_color=THEME["secondary_text"]).pack(side="left")

        # Corps de la carte
        body_frame = ctk.CTkFrame(card_frame, fg_color="transparent")
        body_frame.pack(fill="both", expand=True, padx=12, pady=(4, 8))
        body_frame.grid_columnconfigure((0, 1), weight=1, uniform="info")

        prof_name = profs.get(data["professeur_id"], "Inconnu")
        classe_name = classes.get(data["classe_id"], "Inconnue")
        
        self.create_info_item_v2(body_frame, ICON_MAP.get("professor"), "Professeur", prof_name, 0, 0)
        self.create_info_item_v2(body_frame, ICON_MAP.get("class"), "Classe", classe_name, 0, 1)

        # Séparateur visuel
        separator = ctk.CTkFrame(card_frame, fg_color=THEME["border_color"], height=1)
        separator.pack(fill="x", padx=12, pady=4)
        
        # Pied de page avec les détails additionnels
        footer_frame = ctk.CTkFrame(card_frame, fg_color="transparent")
        footer_frame.pack(fill="both", expand=True, padx=12, pady=(4, 12))
        footer_frame.grid_columnconfigure((0, 1), weight=1)

        salle_name = salles.get(data["salle_id"], "Non spécifiée") if data["salle_id"] else "Non spécifiée"
        jours_cours = data.get("jours_cours", "Non spécifié")
        duree_cours = self._format_duree(data.get("duree_cours", 0))
        
        self.create_info_item_v3(footer_frame, ICON_MAP.get("room"), salle_name, 0, 0)
        self.create_info_item_v3(footer_frame, ICON_MAP.get("calendar"), jours_cours, 0, 1)
        self.create_info_item_v3(footer_frame, ICON_MAP.get("timer"), duree_cours, 1, 0)
        
        duplicate_icon = load_ctk_icon(ICON_MAP.get("duplicate"), size=(14, 14))
        duplicate_button = ctk.CTkButton(
            footer_frame, text="", image=duplicate_icon, width=28, height=28,
            fg_color="transparent", hover_color=THEME["header_bg"],
            command=lambda d=data: self.dupliquer(d)
        )
        duplicate_button.grid(row=1, column=1, sticky="e")

        card_frame.bind("<Button-1>", lambda event, d=data, f=card_frame: self._on_select(event, d, f))
        for child in card_frame.winfo_children():
            child.bind("<Button-1>", lambda event, d=data, f=card_frame: self._on_select(event, d, f))
            for sub_child in child.winfo_children():
                sub_child.bind("<Button-1>", lambda event, d=data, f=card_frame: self._on_select(event, d, f))
                for sub_sub_child in sub_child.winfo_children():
                    sub_sub_child.bind("<Button-1>", lambda event, d=data, f=card_frame: self._on_select(event, d, f))

    def create_info_item_v2(self, parent, icon_name, label_text, value_text, row, column):
        item_frame = ctk.CTkFrame(parent, fg_color="transparent")
        item_frame.grid(row=row, column=column, sticky="nsew", padx=4, pady=2)
        item_frame.grid_columnconfigure(1, weight=1)
        
        icon = load_ctk_icon(icon_name, size=(16, 16))
        ctk.CTkLabel(item_frame, text="", image=icon).grid(row=0, column=0, sticky="nsw", padx=(0, 4))
        
        ctk.CTkLabel(item_frame, text=label_text, 
                     font=(FONT_FAMILY, FONT_SIZE_TEXT-2), 
                     text_color=THEME["secondary_text"],
                     justify="left", anchor="w").grid(row=0, column=1, sticky="w")
        
        ctk.CTkLabel(item_frame, text=value_text, 
                     font=(FONT_FAMILY, FONT_SIZE_TEXT-1, "bold"), 
                     text_color=THEME["primary_text"],
                     justify="left", anchor="w").grid(row=1, column=1, sticky="w")

    def create_info_item_v3(self, parent, icon_name, value_text, row, column):
        item_frame = ctk.CTkFrame(parent, fg_color="transparent")
        item_frame.grid(row=row, column=column, sticky="nsew", padx=2, pady=2)
        
        icon = load_ctk_icon(icon_name, size=(14, 14))
        ctk.CTkLabel(item_frame, text="", image=icon).pack(side="left", padx=(0, 3))
        
        ctk.CTkLabel(item_frame, text=value_text, 
                     font=(FONT_FAMILY, FONT_SIZE_TEXT), 
                     text_color=THEME["secondary_text"],
                     justify="left", anchor="w").pack(side="left", fill="x", expand=True)

    def _on_select(self, event, data, frame):
        if self.selected_item_frame:
            self.selected_item_frame.configure(border_color=THEME["card_bg"])
        
        self.selected_item_frame = frame
        if data:
            self.selected_item_data = data
        self.selected_item_frame.configure(border_color=THEME["accent_blue"])

    def ajouter(self):
        self._ouvrir_formulaire("Ajouter")

    def modifier(self):
        if not self.selected_item_data:
            messagebox.showwarning("Modifier", "Sélectionnez un enseignement.")
            return
        self._ouvrir_formulaire("Modifier", self.selected_item_data)

    def dupliquer(self, data):
        self._ouvrir_formulaire("Dupliquer", data)

    def supprimer(self):
        if not self.selected_item_data:
            messagebox.showwarning("Supprimer", "Sélectionnez un enseignement.")
            return
        enseignement_id = self.selected_item_data.get("id")
        if messagebox.askyesno("Confirmer", f"Supprimer l'enseignement ID #{enseignement_id} ?"):
            if delete_enseignement(enseignement_id):
                messagebox.showinfo("Succès", "Enseignement supprimé.")
                self.rafraichir_liste()
            else:
                messagebox.showerror("Erreur", "Suppression échouée.")

    def _ouvrir_formulaire(self, mode, data=None):
        popup = ctk.CTkToplevel(self)
        popup.title(f"{mode} un Enseignement")
        popup.geometry("400x550")
        popup.configure(fg_color=THEME["card_bg"])
        popup.grab_set()

        popup.grid_columnconfigure(0, weight=1)
        popup.grid_rowconfigure(8, weight=1)

        ctk.CTkLabel(popup, text=f"{mode} un Enseignement",
                     font=(FONT_FAMILY, FONT_SIZE_SUBHEADER, "bold"),
                     text_color=THEME["accent_blue"]).grid(row=0, column=0, pady=10, padx=10)
        
        form_frame = ctk.CTkFrame(popup, fg_color="transparent")
        form_frame.grid(row=1, column=0, sticky="ew", padx=20, pady=5)
        form_frame.grid_columnconfigure(1, weight=1)

        profs = {p["id"]: p for p in get_all_professeurs()}
        classes = {c["id"]: c for c in get_all_classes()}
        matieres = {m["id"]: m for m in get_all_matieres()}
        salles = {s["id"]: s for s in get_all_salles()}

        comboboxes = {}
        fields_data = [
            ("Professeur", get_all_professeurs(), "professeur_id"),
            ("Classe", get_all_classes(), "classe_id"),
            ("Matière", get_all_matieres(), "matiere_id"),
            ("Salle", get_all_salles(), "salle_id"),
        ]
        
        for i, (label_text, items, key) in enumerate(fields_data):
            ctk.CTkLabel(form_frame, text=f"{label_text}:",
                         font=(FONT_FAMILY, FONT_SIZE_TEXT),
                         text_color=THEME["primary_text"]).grid(row=i, column=0, sticky="w", padx=(0, 5), pady=5)
            
            display_values = [f"{item['id']} - {item['nom']}" + (f" {item['prenom']}" if 'prenom' in item else "") for item in items]
            
            combo = ctk.CTkComboBox(form_frame, values=[""] + display_values, state="readonly",
                                     font=(FONT_FAMILY, FONT_SIZE_TEXT-2),
                                     fg_color=THEME["header_bg"],
                                     border_color=THEME["border_color"],
                                     height=28)
            combo.grid(row=i, column=1, sticky="ew")
            comboboxes[key] = combo
            
        ctk.CTkLabel(form_frame, text="Jours de cours:",
                     font=(FONT_FAMILY, FONT_SIZE_TEXT),
                     text_color=THEME["primary_text"]).grid(row=4, column=0, columnspan=2, sticky="w", pady=(5,0))
        
        jours_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        jours_frame.grid(row=5, column=0, columnspan=2, sticky="ew")
        
        jours_disponibles = ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi"]
        self.jours_vars = {}
        for i, jour in enumerate(jours_disponibles):
            self.jours_vars[jour] = ctk.StringVar(value="off")
            check = ctk.CTkCheckBox(jours_frame, text=jour, variable=self.jours_vars[jour], 
                                     onvalue="on", offvalue="off",
                                     font=(FONT_FAMILY, FONT_SIZE_TEXT-2),
                                     hover_color=THEME["accent_blue"])
            check.grid(row=math.floor(i/3), column=i%3, sticky="w", padx=2, pady=2)


        ctk.CTkLabel(form_frame, text="Durée (min):",
                     font=(FONT_FAMILY, FONT_SIZE_TEXT),
                     text_color=THEME["primary_text"]).grid(row=6, column=0, sticky="w", padx=(0, 5), pady=5)
        duree_var = ctk.StringVar(value="")
        self.duree_entry = ctk.CTkEntry(form_frame, textvariable=duree_var, 
                                         font=(FONT_FAMILY, FONT_SIZE_TEXT-2),
                                         fg_color=THEME["header_bg"],
                                         border_color=THEME["border_color"],
                                         height=28)
        self.duree_entry.grid(row=6, column=1, sticky="ew")

        ctk.CTkLabel(form_frame, text="Statut:",
                     font=(FONT_FAMILY, FONT_SIZE_TEXT),
                     text_color=THEME["primary_text"]).grid(row=7, column=0, sticky="w", padx=(0, 5), pady=5)
        statut_var = ctk.StringVar(value="Actif")
        self.statut_combobox = ctk.CTkComboBox(form_frame, values=["Actif", "Archivé"], state="readonly",
                                                variable=statut_var,
                                                font=(FONT_FAMILY, FONT_SIZE_TEXT-2),
                                                fg_color=THEME["header_bg"],
                                                border_color=THEME["border_color"],
                                                height=28)
        self.statut_combobox.grid(row=7, column=1, sticky="ew")

        if mode == "Modifier" or mode == "Dupliquer":
            if data:
                if data.get("professeur_id") is not None and data["professeur_id"] in profs:
                    prof_info = profs[data["professeur_id"]]
                    comboboxes["professeur_id"].set(f"{prof_info['id']} - {prof_info['nom']} {prof_info['prenom']}")
                
                if data.get("classe_id") is not None and data["classe_id"] in classes:
                    classe_info = classes[data["classe_id"]]
                    comboboxes["classe_id"].set(f"{classe_info['id']} - {classe_info['nom']}")
                
                if data.get("matiere_id") is not None and data["matiere_id"] in matieres:
                    matiere_info = matieres[data["matiere_id"]]
                    comboboxes["matiere_id"].set(f"{matiere_info['id']} - {matiere_info['nom']}")
                
                if data.get("salle_id") is not None and data["salle_id"] in salles:
                    salle_info = salles[data["salle_id"]]
                    comboboxes["salle_id"].set(f"{salle_info['id']} - {salle_info['nom']}")

                jours_list = data.get("jours_cours", "").split('-') if data.get("jours_cours") else []
                for jour in jours_list:
                    if jour in self.jours_vars:
                        self.jours_vars[jour].set("on")
                
                duree_var.set(str(data.get("duree_cours", "")))
                statut_var.set(data.get("statut", "Actif"))

        def save():
            try:
                prof_str = comboboxes["professeur_id"].get()
                prof_id = int(prof_str.split(" - ")[0]) if prof_str else None
                classe_str = comboboxes["classe_id"].get()
                classe_id = int(classe_str.split(" - ")[0]) if classe_str else None
                matiere_str = comboboxes["matiere_id"].get()
                matiere_id = int(matiere_str.split(" - ")[0]) if matiere_str else None
                salle_str = comboboxes["salle_id"].get()
                salle_id = int(salle_str.split(" - ")[0]) if salle_str else None
                
                selected_jours = [jour for jour, var in self.jours_vars.items() if var.get() == "on"]
                jours_cours = "-".join(selected_jours)
                
                duree_cours = int(duree_var.get())
                statut = statut_var.get()
                
                if not prof_id or not classe_id or not matiere_id:
                    messagebox.showerror("Erreur", "Professeur, Classe et Matière sont obligatoires.", parent=popup)
                    return

                if mode == "Ajouter" or mode == "Dupliquer":
                    if add_enseignement(prof_id, classe_id, matiere_id, salle_id, jours_cours, duree_cours, statut):
                        messagebox.showinfo("Succès", "Enseignement ajouté avec succès.", parent=popup)
                        self.rafraichir_liste()
                        popup.destroy()
                    else:
                        messagebox.showerror("Erreur", "Échec de l'ajout.", parent=popup)
                else: # Modifier
                    enseignement_id = data["id"]
                    if update_enseignement(enseignement_id, prof_id, classe_id, matiere_id, salle_id, jours_cours, duree_cours, statut):
                        messagebox.showinfo("Succès", "Enseignement mis à jour avec succès.", parent=popup)
                        self.rafraichir_liste()
                        popup.destroy()
                    else:
                        messagebox.showerror("Erreur", "Échec de la mise à jour.", parent=popup)
            except Exception as e:
                messagebox.showerror("Erreur", f"Erreur lors de la sauvegarde : {e}", parent=popup)

        btn_frame = ctk.CTkFrame(popup, fg_color="transparent")
        btn_frame.grid(row=8, column=0, pady=10, sticky="s")
        ctk.CTkButton(btn_frame, text="Annuler", command=popup.destroy,
                     fg_color="gray", hover_color="#6e6e6e",
                     font=(FONT_FAMILY, FONT_SIZE_TEXT, "bold"), height=28).pack(side="left", padx=5)
        ctk.CTkButton(btn_frame, text="Enregistrer", command=save,
                     fg_color=THEME["accent_blue"], text_color=THEME["bg_main"],
                     hover_color="#45b69c",
                     font=(FONT_FAMILY, FONT_SIZE_TEXT, "bold"), height=28).pack(side="left", padx=5)

    @staticmethod
    def _format_duree(minutes):
        if minutes is None:
            return "N/A"
        try:
            minutes = int(minutes)
            if minutes < 60:
                return f"{minutes} min"
            hours = minutes // 60
            mins = minutes % 60
            return f"{hours}h {mins}min" if mins > 0 else f"{hours}h"
        except (ValueError, TypeError):
            return "N/A"

    @staticmethod
    def _mix(hex1, hex2, t=0.5):
        def _h2rgb(h):
            h = h.lstrip("#")
            return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))
        def _rgb2h(r, g, b):
            return f"#{r:02x}{g:02x}{b:02x}"
        r1, g1, b1 = _h2rgb(hex1)
        r2, g2, b2 = _h2rgb(hex2)
        r = int(r1*(1-t) + r2*t)
        g = int(g1*(1-t) + g2*t)
        b = int(b1*(1-t) + b2*t)
        return _rgb2h(r, g, b)