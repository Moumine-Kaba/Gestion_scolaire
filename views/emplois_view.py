import customtkinter as ctk
from tkinter import ttk, messagebox
# Assurez-vous que le contrôleur a bien été mis à jour avec les fonctions manquantes
from controllers.emplois_controller import get_all_emplois, add_emploi, update_emploi, delete_emploi
from views.dashboard_view import HEADER_BG

# Thème (basé sur la palette de couleurs de votre application principale)
BG = "#121212"
CARD_BG = "#2c2c2c"
ACCENT = "#3498db"
BTN_ADD = "#2ecc71"
BTN_EDIT = "#f1c40f"
BTN_DEL = "#e74c3c"
BTN_REFRESH = "#3498db"
BTN_TEXT = "#f5f5f5"
SUBTEXT_COLOR = "#a0a0a0"
BORDER_COLOR = "#3c3c3c"
FONT_FAMILY = "Segoe UI"
FONT_BOLD_14 = (FONT_FAMILY, 14, "bold")
FONT_11 = (FONT_FAMILY, 11)

class EmploisView(ctk.CTkFrame):
    def __init__(self, parent, icons):
        super().__init__(parent, fg_color=BG, corner_radius=0)
        self.icons = icons
        
        ctk.CTkLabel(self, text="Gestion des Emplois du Temps", font=(FONT_FAMILY, 22, "bold"),
                     fg_color="transparent", text_color=ACCENT).pack(pady=22)

        # Style pour le Treeview (compatible avec CustomTkinter)
        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview", background=CARD_BG, foreground=BTN_TEXT, fieldbackground=CARD_BG, font=FONT_11, rowheight=29)
        style.configure("Treeview.Heading", background=HEADER_BG, foreground=ACCENT, font=FONT_BOLD_14)
        style.map("Treeview", background=[("selected", "#2a597a")])
        
        # Le Treeview doit être créé comme un widget standard de tkinter
        colonnes = ("ID", "Jour", "Heure", "Matière", "Professeur", "Salle")
        self.tree = ttk.Treeview(self, columns=colonnes, show="headings", selectmode="browse")
        for col in colonnes:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor="center", width=120 if col != "ID" else 52)
        self.tree.pack(fill="both", expand=True, padx=18, pady=(6, 4))
        
        actions = ctk.CTkFrame(self, fg_color="transparent")
        actions.pack(pady=13)
        
        # Boutons d'action avec CustomTkinter
        ctk.CTkButton(actions, text="➕ Ajouter", font=FONT_BOLD_14, fg_color=BTN_ADD,
                      hover_color="#21a853", text_color=BTN_TEXT, corner_radius=8,
                      command=self.ajouter_emploi).pack(side="left", padx=7)
        
        ctk.CTkButton(actions, text="✏️ Modifier", font=FONT_BOLD_14, fg_color=BTN_EDIT,
                      hover_color="#d6ac0e", text_color=BTN_TEXT, corner_radius=8,
                      command=self.modifier_emploi).pack(side="left", padx=7)
        
        ctk.CTkButton(actions, text="🗑️ Supprimer", font=FONT_BOLD_14, fg_color=BTN_DEL,
                      hover_color="#c0392b", text_color=BTN_TEXT, corner_radius=8,
                      command=self.supprimer_emploi).pack(side="left", padx=7)
        
        ctk.CTkButton(actions, text="🔄 Actualiser", font=FONT_BOLD_14, fg_color=BTN_REFRESH,
                      hover_color="#2980b9", text_color=BTN_TEXT, corner_radius=8,
                      command=self.charger_emplois).pack(side="left", padx=7)

        self.charger_emplois()

    def charger_emplois(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        emplois = get_all_emplois()
        for emploi in emplois:
            self.tree.insert("", "end", values=emploi)

    def ajouter_emploi(self):
        self._ouvrir_formulaire("Ajouter")

    def modifier_emploi(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Modification", "Veuillez sélectionner un emploi du temps.")
            return
        data = self.tree.item(selected[0])["values"]
        self._ouvrir_formulaire("Modifier", data)

    def supprimer_emploi(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Suppression", "Veuillez sélectionner un emploi du temps.")
            return
        emploi_id = self.tree.item(selected[0])["values"][0]
        if messagebox.askyesno("Confirmation", "Voulez-vous vraiment supprimer cet emploi du temps ?"):
            delete_emploi(emploi_id)
            self.charger_emplois()
            messagebox.showinfo("Succès", "Emploi du temps supprimé.")

    def _ouvrir_formulaire(self, mode, data=None):
        form = ctk.CTkToplevel(self)
        form.title(f"{mode} un Emploi du Temps")
        form.geometry("450x350")
        form.configure(fg_color=BG)
        form.grab_set()

        frame = ctk.CTkFrame(form, fg_color="transparent")
        frame.pack(pady=20, padx=20, fill="both", expand=True)

        labels_data = [
            ("Jour :", "jour_cb", ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi"]),
            ("Heure :", "heure_entry"),
            ("Matière :", "matiere_entry"),
            ("Professeur :", "prof_entry"),
            ("Salle :", "salle_entry")
        ]
        widgets = {}
        for i, (label_text, widget_name, *values) in enumerate(labels_data):
            ctk.CTkLabel(frame, text=label_text, fg_color="transparent", text_color=ACCENT, font=FONT_BOLD_14)\
                .grid(row=i, column=0, padx=(0, 20), pady=8, sticky="w")
            if widget_name.endswith("_cb"):
                widget = ctk.CTkComboBox(frame, values=values[0], state="readonly", font=FONT_11)
            else:
                widget = ctk.CTkEntry(frame, font=FONT_11, fg_color=CARD_BG, text_color=BTN_TEXT, border_color=BORDER_COLOR)
            widget.grid(row=i, column=1, pady=8, sticky="ew")
            widgets[widget_name] = widget
        
        frame.grid_columnconfigure(1, weight=1)

        if mode == "Modifier" and data:
            widgets["jour_cb"].set(data[1])
            widgets["heure_entry"].insert(0, data[2])
            widgets["matiere_entry"].insert(0, data[3])
            widgets["prof_entry"].insert(0, data[4])
            widgets["salle_entry"].insert(0, data[5])
            
        def enregistrer():
            jour = widgets["jour_cb"].get()
            heure = widgets["heure_entry"].get().strip()
            matiere = widgets["matiere_entry"].get().strip()
            prof = widgets["prof_entry"].get().strip()
            salle = widgets["salle_entry"].get().strip()
            
            if not all([jour, heure, matiere, prof, salle]):
                messagebox.showerror("Erreur", "Champs obligatoires manquants.", parent=form)
                return
            
            if mode == "Ajouter":
                add_emploi(jour, heure, matiere, prof, salle)
                messagebox.showinfo("Succès", "Emploi du temps ajouté.", parent=form)
            else:
                update_emploi(data[0], jour, heure, matiere, prof, salle)
                messagebox.showinfo("Succès", "Emploi du temps modifié.", parent=form)
            
            self.charger_emplois()
            form.destroy()

        btn_frame = ctk.CTkFrame(form, fg_color="transparent")
        btn_frame.pack(pady=(0, 20), padx=20, fill="x")
        
        ctk.CTkButton(btn_frame, text="💾 Enregistrer", font=FONT_BOLD_14, fg_color=ACCENT,
                      hover_color="#2980b9", text_color=BG, corner_radius=8,
                      command=enregistrer).pack(side="left", padx=(0, 5), expand=True, fill="x")
        ctk.CTkButton(btn_frame, text="❌ Annuler", font=FONT_BOLD_14, fg_color=BTN_DEL,
                      hover_color="#c0392b", text_color=BTN_TEXT, corner_radius=8,
                      command=form.destroy).pack(side="left", padx=(5, 0), expand=True, fill="x")

# Exécution de la vue pour les tests
if __name__ == "__main__":
    root = ctk.CTk()
    root.title("Gestion des Emplois du Temps")
    root.geometry("900x520")
    root.configure(fg_color=BG)
    
    # Création d'une instance avec un dictionnaire d'icônes fictif
    emplois_view = EmploisView(root, {})
    emplois_view.pack(fill="both", expand=True)
    
    root.mainloop()