import tkinter as tk
from tkinter import ttk, messagebox
from controllers.tache_controller import get_all_taches, add_tache, update_tache, delete_tache

BG = "#181f30"
ACCENT = "#38bdf8"
BTN_ADD = "#22c55e"
BTN_EDIT = "#7c3aed"
BTN_DEL = "#ef4444"
BTN_REFRESH = "#f59e42"
BTN_TEXT = "#f1f5f9"
FONT = ("Segoe UI", 11, "bold")

class TachesView(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg=BG)
        tk.Label(self, text="Gestion des Tâches", font=("Segoe UI", 22, "bold"),
                 fg=ACCENT, bg=BG).pack(pady=22)

        colonnes = ("ID", "Titre", "Description", "Statut", "Date échéance")
        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview", background=BG, foreground=BTN_TEXT, fieldbackground=BG, font=("Segoe UI", 10), rowheight=29)
        style.configure("Treeview.Heading", background=BG, foreground=ACCENT, font=("Segoe UI", 11, "bold"))
        self.tree = ttk.Treeview(self, columns=colonnes, show="headings", selectmode="browse")
        for col in colonnes:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor="center", width=125 if col != "ID" else 54)
        self.tree.pack(fill="both", expand=True, padx=18, pady=(6, 4))

        actions = tk.Frame(self, bg=BG)
        actions.pack(pady=13)
        tk.Button(actions, text="➕  Ajouter", font=FONT, bg=BTN_ADD, fg=BTN_TEXT, relief="flat", cursor="hand2",
                  padx=20, pady=7, command=self.ajouter_tache).pack(side="left", padx=7)
        tk.Button(actions, text="✏️  Modifier", font=FONT, bg=BTN_EDIT, fg=BTN_TEXT, relief="flat", cursor="hand2",
                  padx=20, pady=7, command=self.modifier_tache).pack(side="left", padx=7)
        tk.Button(actions, text="🗑️  Supprimer", font=FONT, bg=BTN_DEL, fg=BTN_TEXT, relief="flat", cursor="hand2",
                  padx=20, pady=7, command=self.supprimer_tache).pack(side="left", padx=7)
        tk.Button(actions, text="🔄 Actualiser", font=FONT, bg=BTN_REFRESH, fg=BTN_TEXT, relief="flat", cursor="hand2",
                  padx=20, pady=7, command=self.charger_taches).pack(side="left", padx=7)

        self.charger_taches()

    def charger_taches(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        for t in get_all_taches():
            self.tree.insert("", "end", values=t)

    def ajouter_tache(self):
        self._ouvrir_formulaire("Ajouter")

    def modifier_tache(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Modification", "Veuillez sélectionner une tâche.")
            return
        data = self.tree.item(selected[0])["values"]
        self._ouvrir_formulaire("Modifier", data)

    def supprimer_tache(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Suppression", "Veuillez sélectionner une tâche.")
            return
        tache_id = self.tree.item(selected[0])["values"][0]
        if messagebox.askyesno("Confirmation", "Voulez-vous vraiment supprimer cette tâche ?"):
            delete_tache(tache_id)
            self.charger_taches()

    def _ouvrir_formulaire(self, mode, data=None):
        form = tk.Toplevel(self)
        form.title(f"{mode} une Tâche")
        form.geometry("510x320")
        form.configure(bg=BG)
        form.grab_set()

        y = 24
        tk.Label(form, text="Titre :", bg=BG, fg=ACCENT, font=FONT).place(x=34, y=y)
        titre_entry = tk.Entry(form, font=("Segoe UI", 11), bg="#232f3e", fg=BTN_TEXT, relief="flat")
        titre_entry.place(x=140, y=y, width=320)
        y += 46

        tk.Label(form, text="Description :", bg=BG, fg=ACCENT, font=FONT).place(x=34, y=y)
        desc_text = tk.Text(form, font=("Segoe UI", 11), bg="#232f3e", fg=BTN_TEXT, relief="flat", height=3, width=32)
        desc_text.place(x=140, y=y)
        y += 76

        tk.Label(form, text="Statut :", bg=BG, fg=ACCENT, font=FONT).place(x=34, y=y)
        statut_entry = tk.Entry(form, font=("Segoe UI", 11), bg="#232f3e", fg=BTN_TEXT, relief="flat")
        statut_entry.place(x=140, y=y, width=320)
        y += 46

        tk.Label(form, text="Date échéance :", bg=BG, fg=ACCENT, font=FONT).place(x=34, y=y)
        date_entry = tk.Entry(form, font=("Segoe UI", 11), bg="#232f3e", fg=BTN_TEXT, relief="flat")
        date_entry.place(x=140, y=y, width=320)

        if mode == "Modifier" and data:
            titre_entry.insert(0, data[1])
            desc_text.insert("1.0", data[2])
            statut_entry.insert(0, data[3])
            date_entry.insert(0, data[4])

        def enregistrer():
            titre = titre_entry.get().strip()
            description = desc_text.get("1.0", tk.END).strip()
            statut = statut_entry.get().strip()
            date = date_entry.get().strip()
            if not all([titre, description, statut, date]):
                messagebox.showerror("Erreur", "Champs obligatoires manquants.", parent=form)
                return
            if mode == "Ajouter":
                add_tache(titre, description, statut, date)
                messagebox.showinfo("Succès", "Tâche ajoutée avec succès.", parent=form)
            else:
                update_tache(data[0], titre, description, statut, date)
                messagebox.showinfo("Succès", "Tâche modifiée.", parent=form)
            self.charger_taches()
            form.destroy()

        btn_frame = tk.Frame(form, bg=BG)
        btn_frame.place(relx=0.5, y=245, anchor="n")
        tk.Button(btn_frame, text="💾 Enregistrer", font=FONT, bg=ACCENT, fg=BG,
                  relief="flat", cursor="hand2", padx=16, pady=5, command=enregistrer).pack(side="left", padx=9)
        tk.Button(btn_frame, text="❌ Annuler", font=FONT, bg=BTN_DEL, fg=BTN_TEXT,
                  relief="flat", cursor="hand2", padx=16, pady=5, command=form.destroy).pack(side="left", padx=9)
