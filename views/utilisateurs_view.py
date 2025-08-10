import tkinter as tk
from tkinter import ttk, messagebox
from controllers.user_controller import get_all_users, add_user, update_user, delete_user

BG = "#181f30"
ACCENT = "#38bdf8"
BTN_ADD = "#22c55e"
BTN_EDIT = "#7c3aed"
BTN_DEL = "#ef4444"
BTN_REFRESH = "#f59e42"
BTN_TEXT = "#f1f5f9"
FONT = ("Segoe UI", 11, "bold")

class UtilisateursView(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg=BG)
        tk.Label(self, text="Gestion des Utilisateurs", font=("Segoe UI", 22, "bold"),
                 fg=ACCENT, bg=BG).pack(pady=22)

        colonnes = ("ID", "Username", "Nom", "Prénom", "Email", "Téléphone", "Rôle", "Niveau")
        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview", background=BG, foreground=BTN_TEXT, fieldbackground=BG, font=("Segoe UI", 10), rowheight=29)
        style.configure("Treeview.Heading", background=BG, foreground=ACCENT, font=("Segoe UI", 11, "bold"))
        style.map("Treeview", background=[("selected", "#232f3e")])
        self.tree = ttk.Treeview(self, columns=colonnes, show="headings", selectmode="browse")
        for col in colonnes:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor="center", width=115 if col != "ID" else 52)
        self.tree.pack(fill="both", expand=True, padx=18, pady=(6, 4))

        actions = tk.Frame(self, bg=BG)
        actions.pack(pady=13)
        tk.Button(actions, text="➕  Ajouter", font=FONT, bg=BTN_ADD, fg=BTN_TEXT, relief="flat", cursor="hand2",
                  padx=20, pady=7, command=self.ajouter_user).pack(side="left", padx=7)
        tk.Button(actions, text="✏️  Modifier", font=FONT, bg=BTN_EDIT, fg=BTN_TEXT, relief="flat", cursor="hand2",
                  padx=20, pady=7, command=self.modifier_user).pack(side="left", padx=7)
        tk.Button(actions, text="🗑️  Supprimer", font=FONT, bg=BTN_DEL, fg=BTN_TEXT, relief="flat", cursor="hand2",
                  padx=20, pady=7, command=self.supprimer_user).pack(side="left", padx=7)
        tk.Button(actions, text="🔄 Actualiser", font=FONT, bg=BTN_REFRESH, fg=BTN_TEXT, relief="flat", cursor="hand2",
                  padx=20, pady=7, command=self.charger_users).pack(side="left", padx=7)

        self.charger_users()

    def charger_users(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        for u in get_all_users():
            self.tree.insert("", "end", values=u)

    def ajouter_user(self):
        self._ouvrir_formulaire("Ajouter")

    def modifier_user(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Modification", "Veuillez sélectionner un utilisateur.")
            return
        data = self.tree.item(selected[0])["values"]
        self._ouvrir_formulaire("Modifier", data)

    def supprimer_user(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Suppression", "Veuillez sélectionner un utilisateur.")
            return
        user_id = self.tree.item(selected[0])["values"][0]
        if messagebox.askyesno("Confirmation", "Voulez-vous vraiment supprimer cet utilisateur ?"):
            delete_user(user_id)
            self.charger_users()

    def _ouvrir_formulaire(self, mode, data=None):
        form = tk.Toplevel(self)
        form.title(f"{mode} un Utilisateur")
        form.geometry("540x380")
        form.configure(bg=BG)
        form.grab_set()

        y = 20
        labels = [
            ("Username :", "username"),
            ("Nom :", "nom"),
            ("Prénom :", "prenom"),
            ("Email :", "email"),
            ("Téléphone :", "telephone"),
            ("Mot de passe :", "password"),
            ("Rôle :", "role"),
            ("Niveau :", "niveau"),
        ]
        widgets = {}
        for lbl, key in labels:
            tk.Label(form, text=lbl, bg=BG, fg=ACCENT, font=FONT).place(x=34, y=y)
            if key == "role":
                w = ttk.Combobox(form, values=["admin", "directeur", "professeur", "surveillant", "comptable"], state="readonly", font=("Segoe UI", 10))
                w.place(x=180, y=y, width=290)
            elif key == "password":
                w = tk.Entry(form, show="*", font=("Segoe UI", 11), bg="#232f3e", fg=BTN_TEXT, relief="flat")
                w.place(x=180, y=y, width=290)
            else:
                w = tk.Entry(form, font=("Segoe UI", 11), bg="#232f3e", fg=BTN_TEXT, relief="flat")
                w.place(x=180, y=y, width=290)
            widgets[key] = w
            y += 40

        if mode == "Modifier" and data:
            widgets["username"].insert(0, data[1])
            widgets["nom"].insert(0, data[2])
            widgets["prenom"].insert(0, data[3])
            widgets["email"].insert(0, data[4])
            widgets["telephone"].insert(0, data[5])
            widgets["password"].insert(0, data[6])
            widgets["role"].set(data[7])
            widgets["niveau"].insert(0, data[8])

        def enregistrer():
            vals = {k: w.get().strip() for k, w in widgets.items()}
            if not all(vals.values()):
                messagebox.showerror("Erreur", "Veuillez remplir tous les champs.", parent=form)
                return
            if mode == "Ajouter":
                add_user(vals["username"], vals["prenom"], vals["nom"], vals["email"], vals["telephone"], vals["password"], vals["role"], vals["niveau"])
                messagebox.showinfo("Succès", "Utilisateur ajouté avec succès.", parent=form)
            else:
                update_user(data[0], vals["username"], vals["prenom"], vals["nom"], vals["email"], vals["telephone"], vals["password"], vals["role"], vals["niveau"])
                messagebox.showinfo("Succès", "Utilisateur modifié.", parent=form)
            self.charger_users()
            form.destroy()

        btn_frame = tk.Frame(form, bg=BG)
        btn_frame.place(relx=0.5, y=330, anchor="n")
        tk.Button(btn_frame, text="💾 Enregistrer", font=FONT, bg=ACCENT, fg=BG,
                  relief="flat", cursor="hand2", padx=16, pady=5, command=enregistrer).pack(side="left", padx=9)
        tk.Button(btn_frame, text="❌ Annuler", font=FONT, bg=BTN_DEL, fg=BTN_TEXT,
                  relief="flat", cursor="hand2", padx=16, pady=5, command=form.destroy).pack(side="left", padx=9)
