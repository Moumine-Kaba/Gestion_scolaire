import tkinter as tk
from tkinter import ttk, messagebox
from controllers.paiement_controller import get_all_paiements, add_paiement, update_paiement, delete_paiement
from controllers.eleve_controller import get_all_eleves

BG = "#181f30"
ACCENT = "#38bdf8"
BTN_ADD = "#22c55e"
BTN_EDIT = "#7c3aed"
BTN_DEL = "#ef4444"
BTN_REFRESH = "#f59e42"
BTN_TEXT = "#f1f5f9"
FONT = ("Segoe UI", 11, "bold")

class PaiementsView(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg=BG)
        tk.Label(self, text="Gestion des Paiements", font=("Segoe UI", 22, "bold"),
                 fg=ACCENT, bg=BG).pack(pady=22)

        colonnes = ("ID", "Élève", "Montant", "Date", "Mode de paiement", "Description")
        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview", background=BG, foreground=BTN_TEXT, fieldbackground=BG, font=("Segoe UI", 10), rowheight=29)
        style.configure("Treeview.Heading", background=BG, foreground=ACCENT, font=("Segoe UI", 11, "bold"))
        style.map("Treeview", background=[("selected", "#232f3e")])
        self.tree = ttk.Treeview(self, columns=colonnes, show="headings", selectmode="browse")
        for col in colonnes:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor="center", width=142 if col != "ID" else 52)
        self.tree.pack(fill="both", expand=True, padx=22, pady=(6, 4))

        actions = tk.Frame(self, bg=BG)
        actions.pack(pady=13)
        tk.Button(actions, text="➕  Ajouter", font=FONT, bg=BTN_ADD, fg=BTN_TEXT, relief="flat", cursor="hand2",
                  padx=20, pady=7, command=self.ajouter_paiement).pack(side="left", padx=7)
        tk.Button(actions, text="✏️  Modifier", font=FONT, bg=BTN_EDIT, fg=BTN_TEXT, relief="flat", cursor="hand2",
                  padx=20, pady=7, command=self.modifier_paiement).pack(side="left", padx=7)
        tk.Button(actions, text="🗑️  Supprimer", font=FONT, bg=BTN_DEL, fg=BTN_TEXT, relief="flat", cursor="hand2",
                  padx=20, pady=7, command=self.supprimer_paiement).pack(side="left", padx=7)
        tk.Button(actions, text="🔄 Actualiser", font=FONT, bg=BTN_REFRESH, fg=BTN_TEXT, relief="flat", cursor="hand2",
                  padx=20, pady=7, command=self.charger_paiements).pack(side="left", padx=7)

        self.charger_paiements()

    def charger_paiements(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        for p in get_all_paiements():
            self.tree.insert("", "end", values=p)

    def ajouter_paiement(self):
        self._ouvrir_formulaire("Ajouter")

    def modifier_paiement(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Modification", "Veuillez sélectionner un paiement.")
            return
        data = self.tree.item(selected[0])["values"]
        self._ouvrir_formulaire("Modifier", data)

    def supprimer_paiement(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Suppression", "Veuillez sélectionner un paiement.")
            return
        paiement_id = self.tree.item(selected[0])["values"][0]
        if messagebox.askyesno("Confirmation", "Voulez-vous vraiment supprimer ce paiement ?"):
            delete_paiement(paiement_id)
            self.charger_paiements()

    def _ouvrir_formulaire(self, mode, data=None):
        form = tk.Toplevel(self)
        form.title(f"{mode} un Paiement")
        form.geometry("470x320")
        form.configure(bg=BG)
        form.grab_set()

        eleves = get_all_eleves()
        eleves_choices = [f"{e[0]} - {e[1]} {e[2]}" for e in eleves]

        y = 26
        tk.Label(form, text="Élève :", bg=BG, fg=ACCENT, font=FONT).place(x=38, y=y)
        eleve_cb = ttk.Combobox(form, values=eleves_choices, state="readonly", font=("Segoe UI", 10))
        eleve_cb.place(x=180, y=y, width=220)
        y += 48

        tk.Label(form, text="Montant :", bg=BG, fg=ACCENT, font=FONT).place(x=38, y=y)
        montant_entry = tk.Entry(form, font=("Segoe UI", 11), bg="#232f3e", fg=BTN_TEXT, relief="flat")
        montant_entry.place(x=180, y=y, width=220)
        y += 48

        tk.Label(form, text="Date (YYYY-MM-DD) :", bg=BG, fg=ACCENT, font=FONT).place(x=38, y=y)
        date_entry = tk.Entry(form, font=("Segoe UI", 11), bg="#232f3e", fg=BTN_TEXT, relief="flat")
        date_entry.place(x=180, y=y, width=220)
        y += 48

        tk.Label(form, text="Mode de paiement :", bg=BG, fg=ACCENT, font=FONT).place(x=38, y=y)
        mode_cb = ttk.Combobox(form, values=["Espèces", "Chèque", "Mobile Money", "Carte Bancaire"], state="readonly", font=("Segoe UI", 10))
        mode_cb.place(x=180, y=y, width=220)
        y += 48

        tk.Label(form, text="Description :", bg=BG, fg=ACCENT, font=FONT).place(x=38, y=y)
        desc_entry = tk.Entry(form, font=("Segoe UI", 11), bg="#232f3e", fg=BTN_TEXT, relief="flat")
        desc_entry.place(x=180, y=y, width=220)

        if mode == "Modifier" and data:
            eleve_cb.set(data[1])
            montant_entry.insert(0, data[2])
            date_entry.insert(0, data[3])
            mode_cb.set(data[4])
            desc_entry.insert(0, data[5])

        def enregistrer():
            eleve_str = eleve_cb.get()
            montant = montant_entry.get().strip()
            date = date_entry.get().strip()
            mode_p = mode_cb.get()
            desc = desc_entry.get().strip()
            try:
                eleve_id = int(eleve_str.split(" - ")[0]) if eleve_str else None
            except:
                messagebox.showerror("Erreur", "Élève invalide.", parent=form)
                return
            if not all([eleve_id, montant, date, mode_p]):
                messagebox.showerror("Erreur", "Champs obligatoires manquants.", parent=form)
                return
            if not montant.replace('.', '', 1).isdigit():
                messagebox.showerror("Erreur", "Montant invalide.", parent=form)
                return
            if mode == "Ajouter":
                add_paiement(eleve_id, float(montant), date, mode_p, desc)
                messagebox.showinfo("Succès", "Paiement ajouté avec succès.", parent=form)
            else:
                update_paiement(data[0], eleve_id, float(montant), date, mode_p, desc)
                messagebox.showinfo("Succès", "Paiement modifié.", parent=form)
            self.charger_paiements()
            form.destroy()

        btn_frame = tk.Frame(form, bg=BG)
        btn_frame.place(relx=0.5, y=260, anchor="n")
        tk.Button(btn_frame, text="💾 Enregistrer", font=FONT, bg=ACCENT, fg=BG,
                  relief="flat", cursor="hand2", padx=16, pady=5, command=enregistrer).pack(side="left", padx=9)
        tk.Button(btn_frame, text="❌ Annuler", font=FONT, bg=BTN_DEL, fg=BTN_TEXT,
                  relief="flat", cursor="hand2", padx=16, pady=5, command=form.destroy).pack(side="left", padx=9)

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Gestion des Paiements")
    root.geometry("970x520")
    root.configure(bg=BG)
    PaiementsView(root)
    root.mainloop()
