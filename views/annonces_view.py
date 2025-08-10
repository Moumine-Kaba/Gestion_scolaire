import tkinter as tk
from tkinter import ttk, messagebox
from controllers.annonce_controller import get_all_annonces, add_annonce, update_annonce, delete_annonce

BG = "#181f30"
ACCENT = "#38bdf8"
BTN_ADD = "#22c55e"
BTN_EDIT = "#7c3aed"
BTN_DEL = "#ef4444"
BTN_REFRESH = "#f59e42"
BTN_TEXT = "#f1f5f9"
FONT = ("Segoe UI", 11, "bold")

class AnnoncesView(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg=BG)
        tk.Label(self, text="Gestion des Annonces", font=("Segoe UI", 22, "bold"),
                 fg=ACCENT, bg=BG).pack(pady=22)

        colonnes = ("ID", "Titre", "Contenu", "Date", "Auteur")
        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview", background=BG, foreground=BTN_TEXT, fieldbackground=BG, font=("Segoe UI", 10), rowheight=29)
        style.configure("Treeview.Heading", background=BG, foreground=ACCENT, font=("Segoe UI", 11, "bold"))
        self.tree = ttk.Treeview(self, columns=colonnes, show="headings", selectmode="browse")
        for col in colonnes:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor="center", width=135 if col in ("Contenu","Auteur") else 95)
        self.tree.pack(fill="both", expand=True, padx=18, pady=(6, 4))

        actions = tk.Frame(self, bg=BG)
        actions.pack(pady=13)
        tk.Button(actions, text="➕  Ajouter", font=FONT, bg=BTN_ADD, fg=BTN_TEXT, relief="flat", cursor="hand2",
                  padx=20, pady=7, command=self.ajouter_annonce).pack(side="left", padx=7)
        tk.Button(actions, text="✏️  Modifier", font=FONT, bg=BTN_EDIT, fg=BTN_TEXT, relief="flat", cursor="hand2",
                  padx=20, pady=7, command=self.modifier_annonce).pack(side="left", padx=7)
        tk.Button(actions, text="🗑️  Supprimer", font=FONT, bg=BTN_DEL, fg=BTN_TEXT, relief="flat", cursor="hand2",
                  padx=20, pady=7, command=self.supprimer_annonce).pack(side="left", padx=7)
        tk.Button(actions, text="🔄 Actualiser", font=FONT, bg=BTN_REFRESH, fg=BTN_TEXT, relief="flat", cursor="hand2",
                  padx=20, pady=7, command=self.charger_annonces).pack(side="left", padx=7)

        self.charger_annonces()

    def charger_annonces(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        for a in get_all_annonces():
            self.tree.insert("", "end", values=a)

    def ajouter_annonce(self):
        self._ouvrir_formulaire("Ajouter")

    def modifier_annonce(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Modification", "Veuillez sélectionner une annonce.")
            return
        data = self.tree.item(selected[0])["values"]
        self._ouvrir_formulaire("Modifier", data)

    def supprimer_annonce(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Suppression", "Veuillez sélectionner une annonce.")
            return
        ann_id = self.tree.item(selected[0])["values"][0]
        if messagebox.askyesno("Confirmation", "Voulez-vous vraiment supprimer cette annonce ?"):
            delete_annonce(ann_id)
            self.charger_annonces()

    def _ouvrir_formulaire(self, mode, data=None):
        form = tk.Toplevel(self)
        form.title(f"{mode} une Annonce")
        form.geometry("540x350")
        form.configure(bg=BG)
        form.grab_set()

        y = 24
        tk.Label(form, text="Titre :", bg=BG, fg=ACCENT, font=FONT).place(x=34, y=y)
        titre_entry = tk.Entry(form, font=("Segoe UI", 11), bg="#232f3e", fg=BTN_TEXT, relief="flat")
        titre_entry.place(x=160, y=y, width=320)
        y += 46

        tk.Label(form, text="Contenu :", bg=BG, fg=ACCENT, font=FONT).place(x=34, y=y)
        contenu_text = tk.Text(form, font=("Segoe UI", 11), bg="#232f3e", fg=BTN_TEXT, relief="flat", height=3, width=38)
        contenu_text.place(x=160, y=y)
        y += 76

        tk.Label(form, text="Date :", bg=BG, fg=ACCENT, font=FONT).place(x=34, y=y)
        date_entry = tk.Entry(form, font=("Segoe UI", 11), bg="#232f3e", fg=BTN_TEXT, relief="flat")
        date_entry.place(x=160, y=y, width=320)
        y += 42

        tk.Label(form, text="Auteur ID :", bg=BG, fg=ACCENT, font=FONT).place(x=34, y=y)
        auteur_entry = tk.Entry(form, font=("Segoe UI", 11), bg="#232f3e", fg=BTN_TEXT, relief="flat")
        auteur_entry.place(x=160, y=y, width=320)

        if mode == "Modifier" and data:
            titre_entry.insert(0, data[1])
            contenu_text.insert("1.0", data[2])
            date_entry.insert(0, data[3])
            auteur_entry.insert(0, data[4])

        def enregistrer():
            titre = titre_entry.get().strip()
            contenu = contenu_text.get("1.0", tk.END).strip()
            date = date_entry.get().strip()
            auteur = auteur_entry.get().strip()
            if not all([titre, contenu, date, auteur]):
                messagebox.showerror("Erreur", "Champs obligatoires manquants.", parent=form)
                return
            if mode == "Ajouter":
                add_annonce(titre, contenu, date, auteur)
                messagebox.showinfo("Succès", "Annonce ajoutée avec succès.", parent=form)
            else:
                update_annonce(data[0], titre, contenu, date, auteur)
                messagebox.showinfo("Succès", "Annonce modifiée.", parent=form)
            self.charger_annonces()
            form.destroy()

        btn_frame = tk.Frame(form, bg=BG)
        btn_frame.place(relx=0.5, y=270, anchor="n")
        tk.Button(btn_frame, text="💾 Enregistrer", font=FONT, bg=ACCENT, fg=BG,
                  relief="flat", cursor="hand2", padx=16, pady=5, command=enregistrer).pack(side="left", padx=9)
        tk.Button(btn_frame, text="❌ Annuler", font=FONT, bg=BTN_DEL, fg=BTN_TEXT,
                  relief="flat", cursor="hand2", padx=16, pady=5, command=form.destroy).pack(side="left", padx=9)
