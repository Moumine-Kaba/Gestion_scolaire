import tkinter as tk
from tkinter import ttk, messagebox
from controllers.bulletin_controller import get_all_bulletins, add_bulletin, update_bulletin, delete_bulletin
from controllers.eleve_controller import get_all_eleves

BG = "#181f30"
ACCENT = "#38bdf8"
BTN_ADD = "#22c55e"
BTN_EDIT = "#7c3aed"
BTN_DEL = "#ef4444"
BTN_REFRESH = "#f59e42"
BTN_TEXT = "#f1f5f9"
FONT = ("Segoe UI", 11, "bold")

class BulletinsView(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg=BG)
        tk.Label(self, text="Gestion des Bulletins", font=("Segoe UI", 22, "bold"),
                 fg=ACCENT, bg=BG).pack(pady=22)

        colonnes = ("ID", "Élève", "Année scolaire", "Trimestre", "Moyenne", "Remarque", "Date édition")
        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview", background=BG, foreground=BTN_TEXT, fieldbackground=BG, font=("Segoe UI", 10), rowheight=29)
        style.configure("Treeview.Heading", background=BG, foreground=ACCENT, font=("Segoe UI", 11, "bold"))
        style.map("Treeview", background=[("selected", "#232f3e")])
        self.tree = ttk.Treeview(self, columns=colonnes, show="headings", selectmode="browse")
        for col in colonnes:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor="center", width=120 if col != "ID" else 52)
        self.tree.pack(fill="both", expand=True, padx=18, pady=(6, 4))

        actions = tk.Frame(self, bg=BG)
        actions.pack(pady=13)
        tk.Button(actions, text="➕  Ajouter", font=FONT, bg=BTN_ADD, fg=BTN_TEXT, relief="flat", cursor="hand2",
                  padx=20, pady=7, command=self.ajouter_bulletin).pack(side="left", padx=7)
        tk.Button(actions, text="✏️  Modifier", font=FONT, bg=BTN_EDIT, fg=BTN_TEXT, relief="flat", cursor="hand2",
                  padx=20, pady=7, command=self.modifier_bulletin).pack(side="left", padx=7)
        tk.Button(actions, text="🗑️  Supprimer", font=FONT, bg=BTN_DEL, fg=BTN_TEXT, relief="flat", cursor="hand2",
                  padx=20, pady=7, command=self.supprimer_bulletin).pack(side="left", padx=7)
        tk.Button(actions, text="🔄 Actualiser", font=FONT, bg=BTN_REFRESH, fg=BTN_TEXT, relief="flat", cursor="hand2",
                  padx=20, pady=7, command=self.charger_bulletins).pack(side="left", padx=7)

        self.charger_bulletins()

    def charger_bulletins(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        for b in get_all_bulletins():
            self.tree.insert("", "end", values=b)

    def ajouter_bulletin(self):
        self._ouvrir_formulaire("Ajouter")

    def modifier_bulletin(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Modification", "Veuillez sélectionner un bulletin.")
            return
        data = self.tree.item(selected[0])["values"]
        self._ouvrir_formulaire("Modifier", data)

    def supprimer_bulletin(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Suppression", "Veuillez sélectionner un bulletin.")
            return
        bulletin_id = self.tree.item(selected[0])["values"][0]
        if messagebox.askyesno("Confirmation", "Voulez-vous vraiment supprimer ce bulletin ?"):
            delete_bulletin(bulletin_id)
            self.charger_bulletins()

    def _ouvrir_formulaire(self, mode, data=None):
        form = tk.Toplevel(self)
        form.title(f"{mode} un Bulletin")
        form.geometry("530x350")
        form.configure(bg=BG)
        form.grab_set()

        eleves = get_all_eleves()
        eleves_choices = [f"{e[0]} - {e[1]} {e[2]}" for e in eleves]

        y = 26
        tk.Label(form, text="Élève :", bg=BG, fg=ACCENT, font=FONT).place(x=38, y=y)
        eleve_cb = ttk.Combobox(form, values=eleves_choices, state="readonly", font=("Segoe UI", 10))
        eleve_cb.place(x=200, y=y, width=250)
        y += 48

        tk.Label(form, text="Année scolaire :", bg=BG, fg=ACCENT, font=FONT).place(x=38, y=y)
        annee_entry = tk.Entry(form, font=("Segoe UI", 11), bg="#232f3e", fg=BTN_TEXT, relief="flat")
        annee_entry.place(x=200, y=y, width=250)
        y += 48

        tk.Label(form, text="Trimestre :", bg=BG, fg=ACCENT, font=FONT).place(x=38, y=y)
        trim_cb = ttk.Combobox(form, values=["1er", "2ème", "3ème"], state="readonly", font=("Segoe UI", 10))
        trim_cb.place(x=200, y=y, width=250)
        y += 48

        tk.Label(form, text="Moyenne :", bg=BG, fg=ACCENT, font=FONT).place(x=38, y=y)
        moy_entry = tk.Entry(form, font=("Segoe UI", 11), bg="#232f3e", fg=BTN_TEXT, relief="flat")
        moy_entry.place(x=200, y=y, width=250)
        y += 48

        tk.Label(form, text="Remarque :", bg=BG, fg=ACCENT, font=FONT).place(x=38, y=y)
        rem_entry = tk.Entry(form, font=("Segoe UI", 11), bg="#232f3e", fg=BTN_TEXT, relief="flat")
        rem_entry.place(x=200, y=y, width=250)
        y += 48

        tk.Label(form, text="Date édition :", bg=BG, fg=ACCENT, font=FONT).place(x=38, y=y)
        date_entry = tk.Entry(form, font=("Segoe UI", 11), bg="#232f3e", fg=BTN_TEXT, relief="flat")
        date_entry.place(x=200, y=y, width=250)

        if mode == "Modifier" and data:
            eleve_cb.set(data[1])
            annee_entry.insert(0, data[2])
            trim_cb.set(data[3])
            moy_entry.insert(0, data[4])
            rem_entry.insert(0, data[5])
            date_entry.insert(0, data[6])

        def enregistrer():
            eleve_str = eleve_cb.get()
            annee = annee_entry.get().strip()
            trim = trim_cb.get()
            moy = moy_entry.get().strip()
            rem = rem_entry.get().strip()
            date = date_entry.get().strip()
            try:
                eleve_id = int(eleve_str.split(" - ")[0]) if eleve_str else None
            except:
                messagebox.showerror("Erreur", "Élève invalide.", parent=form)
                return
            if not all([eleve_id, annee, trim, moy, date]):
                messagebox.showerror("Erreur", "Champs obligatoires manquants.", parent=form)
                return
            if not moy.replace('.', '', 1).isdigit():
                messagebox.showerror("Erreur", "Moyenne invalide.", parent=form)
                return
            if mode == "Ajouter":
                add_bulletin(eleve_id, annee, trim, float(moy), rem, date)
                messagebox.showinfo("Succès", "Bulletin ajouté avec succès.", parent=form)
            else:
                update_bulletin(data[0], eleve_id, annee, trim, float(moy), rem, date)
                messagebox.showinfo("Succès", "Bulletin modifié.", parent=form)
            self.charger_bulletins()
            form.destroy()

        btn_frame = tk.Frame(form, bg=BG)
        btn_frame.place(relx=0.5, y=308, anchor="n")
        tk.Button(btn_frame, text="💾 Enregistrer", font=FONT, bg=ACCENT, fg=BG,
                  relief="flat", cursor="hand2", padx=16, pady=5, command=enregistrer).pack(side="left", padx=9)
        tk.Button(btn_frame, text="❌ Annuler", font=FONT, bg=BTN_DEL, fg=BTN_TEXT,
                  relief="flat", cursor="hand2", padx=16, pady=5, command=form.destroy).pack(side="left", padx=9)

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Gestion des Bulletins")
    root.geometry("1050x520")
    root.configure(bg=BG)
    BulletinsView(root)
    root.mainloop()
