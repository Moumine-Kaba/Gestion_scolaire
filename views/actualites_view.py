import tkinter as tk
from tkinter import ttk, messagebox
from controllers.actualite_controller import get_all_actualites, add_actualite, update_actualite, delete_actualite

BG = "#181f30"
ACCENT = "#38bdf8"
BTN_ADD = "#22c55e"
BTN_EDIT = "#7c3aed"
BTN_DEL = "#ef4444"
BTN_REFRESH = "#f59e42"
BTN_TEXT = "#f1f5f9"
FONT = ("Segoe UI", 11, "bold")

class ActualitesView(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg=BG)
        tk.Label(self, text="Gestion des Actualités", font=("Segoe UI", 22, "bold"),
                 fg=ACCENT, bg=BG).pack(pady=22)

        colonnes = ("ID", "Titre", "Contenu", "Date")
        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview", background=BG, foreground=BTN_TEXT, fieldbackground=BG, font=("Segoe UI", 10), rowheight=29)
        style.configure("Treeview.Heading", background=BG, foreground=ACCENT, font=("Segoe UI", 11, "bold"))
        style.map("Treeview", background=[("selected", "#232f3e")])
        self.tree = ttk.Treeview(self, columns=colonnes, show="headings", selectmode="browse")
        for col in colonnes:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor="center", width=180 if col == "Contenu" else 95)
        self.tree.pack(fill="both", expand=True, padx=18, pady=(6, 4))

        actions = tk.Frame(self, bg=BG)
        actions.pack(pady=13)
        tk.Button(actions, text="➕  Ajouter", font=FONT, bg=BTN_ADD, fg=BTN_TEXT, relief="flat", cursor="hand2",
                  padx=20, pady=7, command=self.ajouter_actu).pack(side="left", padx=7)
        tk.Button(actions, text="✏️  Modifier", font=FONT, bg=BTN_EDIT, fg=BTN_TEXT, relief="flat", cursor="hand2",
                  padx=20, pady=7, command=self.modifier_actu).pack(side="left", padx=7)
        tk.Button(actions, text="🗑️  Supprimer", font=FONT, bg=BTN_DEL, fg=BTN_TEXT, relief="flat", cursor="hand2",
                  padx=20, pady=7, command=self.supprimer_actu).pack(side="left", padx=7)
        tk.Button(actions, text="🔄 Actualiser", font=FONT, bg=BTN_REFRESH, fg=BTN_TEXT, relief="flat", cursor="hand2",
                  padx=20, pady=7, command=self.charger_actus).pack(side="left", padx=7)

        self.charger_actus()

    def charger_actus(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        for a in get_all_actualites():
            self.tree.insert("", "end", values=a)

    def ajouter_actu(self):
        self._ouvrir_formulaire("Ajouter")

    def modifier_actu(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Modification", "Veuillez sélectionner une actualité.")
            return
        data = self.tree.item(selected[0])["values"]
        self._ouvrir_formulaire("Modifier", data)

    def supprimer_actu(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Suppression", "Veuillez sélectionner une actualité.")
            return
        act_id = self.tree.item(selected[0])["values"][0]
        if messagebox.askyesno("Confirmation", "Voulez-vous vraiment supprimer cette actualité ?"):
            delete_actualite(act_id)
            self.charger_actus()

    def _ouvrir_formulaire(self, mode, data=None):
        form = tk.Toplevel(self)
        form.title(f"{mode} une Actualité")
        form.geometry("540x320")
        form.configure(bg=BG)
        form.grab_set()

        y = 24
        tk.Label(form, text="Titre :", bg=BG, fg=ACCENT, font=FONT).place(x=34, y=y)
        titre_entry = tk.Entry(form, font=("Segoe UI", 11), bg="#232f3e", fg=BTN_TEXT, relief="flat")
        titre_entry.place(x=160, y=y, width=320)
        y += 46

        tk.Label(form, text="Contenu :", bg=BG, fg=ACCENT, font=FONT).place(x=34, y=y)
        contenu_text = tk.Text(form, font=("Segoe UI", 11), bg="#232f3e", fg=BTN_TEXT, relief="flat", height=4, width=38)
        contenu_text.place(x=160, y=y)
        y += 92

        tk.Label(form, text="Date :", bg=BG, fg=ACCENT, font=FONT).place(x=34, y=y)
        date_entry = tk.Entry(form, font=("Segoe UI", 11), bg="#232f3e", fg=BTN_TEXT, relief="flat")
        date_entry.place(x=160, y=y, width=320)

        if mode == "Modifier" and data:
            titre_entry.insert(0, data[1])
            contenu_text.insert("1.0", data[2])
            date_entry.insert(0, data[3])

        def enregistrer():
            titre = titre_entry.get().strip()
            contenu = contenu_text.get("1.0", tk.END).strip()
            date = date_entry.get().strip()
            if not all([titre, contenu, date]):
                messagebox.showerror("Erreur", "Champs obligatoires manquants.", parent=form)
                return
            if mode == "Ajouter":
                add_actualite(titre, contenu, date)
                messagebox.showinfo("Succès", "Actualité ajoutée avec succès.", parent=form)
            else:
                update_actualite(data[0], titre, contenu, date)
                messagebox.showinfo("Succès", "Actualité modifiée.", parent=form)
            self.charger_actus()
            form.destroy()

        btn_frame = tk.Frame(form, bg=BG)
        btn_frame.place(relx=0.5, y=235, anchor="n")
        tk.Button(btn_frame, text="💾 Enregistrer", font=FONT, bg=ACCENT, fg=BG,
                  relief="flat", cursor="hand2", padx=16, pady=5, command=enregistrer).pack(side="left", padx=9)
        tk.Button(btn_frame, text="❌ Annuler", font=FONT, bg=BTN_DEL, fg=BTN_TEXT,
                  relief="flat", cursor="hand2", padx=16, pady=5, command=form.destroy).pack(side="left", padx=9)
