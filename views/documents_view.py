import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from controllers.document_controller import get_all_documents, add_document, update_document, delete_document

BG = "#181f30"
ACCENT = "#38bdf8"
BTN_ADD = "#22c55e"
BTN_EDIT = "#7c3aed"
BTN_DEL = "#ef4444"
BTN_REFRESH = "#f59e42"
BTN_TEXT = "#f1f5f9"
FONT = ("Segoe UI", 11, "bold")

class DocumentsView(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg=BG)
        tk.Label(self, text="Gestion des Documents", font=("Segoe UI", 22, "bold"),
                 fg=ACCENT, bg=BG).pack(pady=22)

        colonnes = ("ID", "Nom", "Chemin", "Type", "Date ajout")
        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview", background=BG, foreground=BTN_TEXT, fieldbackground=BG, font=("Segoe UI", 10), rowheight=29)
        style.configure("Treeview.Heading", background=BG, foreground=ACCENT, font=("Segoe UI", 11, "bold"))
        self.tree = ttk.Treeview(self, columns=colonnes, show="headings", selectmode="browse")
        for col in colonnes:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor="center", width=135 if col != "ID" else 54)
        self.tree.pack(fill="both", expand=True, padx=18, pady=(6, 4))

        actions = tk.Frame(self, bg=BG)
        actions.pack(pady=13)
        tk.Button(actions, text="➕  Ajouter", font=FONT, bg=BTN_ADD, fg=BTN_TEXT, relief="flat", cursor="hand2",
                  padx=20, pady=7, command=self.ajouter_document).pack(side="left", padx=7)
        tk.Button(actions, text="✏️  Modifier", font=FONT, bg=BTN_EDIT, fg=BTN_TEXT, relief="flat", cursor="hand2",
                  padx=20, pady=7, command=self.modifier_document).pack(side="left", padx=7)
        tk.Button(actions, text="🗑️  Supprimer", font=FONT, bg=BTN_DEL, fg=BTN_TEXT, relief="flat", cursor="hand2",
                  padx=20, pady=7, command=self.supprimer_document).pack(side="left", padx=7)
        tk.Button(actions, text="🔄 Actualiser", font=FONT, bg=BTN_REFRESH, fg=BTN_TEXT, relief="flat", cursor="hand2",
                  padx=20, pady=7, command=self.charger_documents).pack(side="left", padx=7)

        self.charger_documents()

    def charger_documents(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        for doc in get_all_documents():
            self.tree.insert("", "end", values=doc)

    def ajouter_document(self):
        self._ouvrir_formulaire("Ajouter")

    def modifier_document(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Modification", "Veuillez sélectionner un document.")
            return
        data = self.tree.item(selected[0])["values"]
        self._ouvrir_formulaire("Modifier", data)

    def supprimer_document(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Suppression", "Veuillez sélectionner un document.")
            return
        doc_id = self.tree.item(selected[0])["values"][0]
        if messagebox.askyesno("Confirmation", "Voulez-vous vraiment supprimer ce document ?"):
            delete_document(doc_id)
            self.charger_documents()

    def _ouvrir_formulaire(self, mode, data=None):
        form = tk.Toplevel(self)
        form.title(f"{mode} un Document")
        form.geometry("520x290")
        form.configure(bg=BG)
        form.grab_set()

        y = 24
        tk.Label(form, text="Nom :", bg=BG, fg=ACCENT, font=FONT).place(x=34, y=y)
        nom_entry = tk.Entry(form, font=("Segoe UI", 11), bg="#232f3e", fg=BTN_TEXT, relief="flat")
        nom_entry.place(x=140, y=y, width=320)
        y += 46

        tk.Label(form, text="Type :", bg=BG, fg=ACCENT, font=FONT).place(x=34, y=y)
        type_entry = tk.Entry(form, font=("Segoe UI", 11), bg="#232f3e", fg=BTN_TEXT, relief="flat")
        type_entry.place(x=140, y=y, width=320)
        y += 46

        tk.Label(form, text="Chemin (upload) :", bg=BG, fg=ACCENT, font=FONT).place(x=34, y=y)
        chemin_entry = tk.Entry(form, font=("Segoe UI", 11), bg="#232f3e", fg=BTN_TEXT, relief="flat")
        chemin_entry.place(x=140, y=y, width=240)
        btn_upload = tk.Button(form, text="📁 Parcourir", font=FONT, bg=ACCENT, fg=BG, relief="flat", cursor="hand2",
                               command=lambda: self.upload_file(chemin_entry))
        btn_upload.place(x=392, y=y-2, width=90, height=32)
        y += 46

        tk.Label(form, text="Date ajout :", bg=BG, fg=ACCENT, font=FONT).place(x=34, y=y)
        date_entry = tk.Entry(form, font=("Segoe UI", 11), bg="#232f3e", fg=BTN_TEXT, relief="flat")
        date_entry.place(x=140, y=y, width=320)

        if mode == "Modifier" and data:
            nom_entry.insert(0, data[1])
            type_entry.insert(0, data[3])
            chemin_entry.insert(0, data[2])
            date_entry.insert(0, data[4])

        def enregistrer():
            nom = nom_entry.get().strip()
            chemin = chemin_entry.get().strip()
            type_doc = type_entry.get().strip()
            date = date_entry.get().strip()
            if not all([nom, chemin, type_doc, date]):
                messagebox.showerror("Erreur", "Champs obligatoires manquants.", parent=form)
                return
            if mode == "Ajouter":
                add_document(nom, chemin, type_doc, date)
                messagebox.showinfo("Succès", "Document ajouté avec succès.", parent=form)
            else:
                update_document(data[0], nom, chemin, type_doc, date)
                messagebox.showinfo("Succès", "Document modifié.", parent=form)
            self.charger_documents()
            form.destroy()

        btn_frame = tk.Frame(form, bg=BG)
        btn_frame.place(relx=0.5, y=220, anchor="n")
        tk.Button(btn_frame, text="💾 Enregistrer", font=FONT, bg=ACCENT, fg=BG,
                  relief="flat", cursor="hand2", padx=16, pady=5, command=enregistrer).pack(side="left", padx=9)
        tk.Button(btn_frame, text="❌ Annuler", font=FONT, bg=BTN_DEL, fg=BTN_TEXT,
                  relief="flat", cursor="hand2", padx=16, pady=5, command=form.destroy).pack(side="left", padx=9)

    def upload_file(self, entry):
        path = filedialog.askopenfilename(title="Sélectionner un fichier", filetypes=[("Tous les fichiers", "*.*")])
        if path:
            entry.delete(0, tk.END)
            entry.insert(0, path)
