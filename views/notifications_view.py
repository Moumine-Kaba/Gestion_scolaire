import tkinter as tk
from tkinter import ttk, messagebox
from controllers.notification_controller import get_all_notifications, add_notification, update_notification, delete_notification

BG = "#181f30"
ACCENT = "#38bdf8"
BTN_ADD = "#22c55e"
BTN_EDIT = "#7c3aed"
BTN_DEL = "#ef4444"
BTN_REFRESH = "#f59e42"
BTN_TEXT = "#f1f5f9"
FONT = ("Segoe UI", 11, "bold")

class NotificationsView(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg=BG)
        tk.Label(self, text="Gestion des Notifications", font=("Segoe UI", 22, "bold"),
                 fg=ACCENT, bg=BG).pack(pady=22)

        colonnes = ("ID", "Contenu", "Date", "Utilisateur", "Lu")
        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview", background=BG, foreground=BTN_TEXT, fieldbackground=BG, font=("Segoe UI", 10), rowheight=29)
        style.configure("Treeview.Heading", background=BG, foreground=ACCENT, font=("Segoe UI", 11, "bold"))
        self.tree = ttk.Treeview(self, columns=colonnes, show="headings", selectmode="browse")
        for col in colonnes:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor="center", width=120 if col != "ID" else 54)
        self.tree.pack(fill="both", expand=True, padx=18, pady=(6, 4))

        actions = tk.Frame(self, bg=BG)
        actions.pack(pady=13)
        tk.Button(actions, text="➕  Ajouter", font=FONT, bg=BTN_ADD, fg=BTN_TEXT, relief="flat", cursor="hand2",
                  padx=20, pady=7, command=self.ajouter_notification).pack(side="left", padx=7)
        tk.Button(actions, text="✏️  Modifier", font=FONT, bg=BTN_EDIT, fg=BTN_TEXT, relief="flat", cursor="hand2",
                  padx=20, pady=7, command=self.modifier_notification).pack(side="left", padx=7)
        tk.Button(actions, text="🗑️  Supprimer", font=FONT, bg=BTN_DEL, fg=BTN_TEXT, relief="flat", cursor="hand2",
                  padx=20, pady=7, command=self.supprimer_notification).pack(side="left", padx=7)
        tk.Button(actions, text="🔄 Actualiser", font=FONT, bg=BTN_REFRESH, fg=BTN_TEXT, relief="flat", cursor="hand2",
                  padx=20, pady=7, command=self.charger_notifications).pack(side="left", padx=7)

        self.charger_notifications()

    def charger_notifications(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        for n in get_all_notifications():
            self.tree.insert("", "end", values=n)

    def ajouter_notification(self):
        self._ouvrir_formulaire("Ajouter")

    def modifier_notification(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Modification", "Veuillez sélectionner une notification.")
            return
        data = self.tree.item(selected[0])["values"]
        self._ouvrir_formulaire("Modifier", data)

    def supprimer_notification(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Suppression", "Veuillez sélectionner une notification.")
            return
        notif_id = self.tree.item(selected[0])["values"][0]
        if messagebox.askyesno("Confirmation", "Voulez-vous vraiment supprimer cette notification ?"):
            delete_notification(notif_id)
            self.charger_notifications()

    def _ouvrir_formulaire(self, mode, data=None):
        form = tk.Toplevel(self)
        form.title(f"{mode} une Notification")
        form.geometry("510x290")
        form.configure(bg=BG)
        form.grab_set()

        y = 24
        tk.Label(form, text="Contenu :", bg=BG, fg=ACCENT, font=FONT).place(x=34, y=y)
        contenu_entry = tk.Entry(form, font=("Segoe UI", 11), bg="#232f3e", fg=BTN_TEXT, relief="flat")
        contenu_entry.place(x=140, y=y, width=320)
        y += 46

        tk.Label(form, text="Date :", bg=BG, fg=ACCENT, font=FONT).place(x=34, y=y)
        date_entry = tk.Entry(form, font=("Segoe UI", 11), bg="#232f3e", fg=BTN_TEXT, relief="flat")
        date_entry.place(x=140, y=y, width=320)
        y += 46

        tk.Label(form, text="Utilisateur ID :", bg=BG, fg=ACCENT, font=FONT).place(x=34, y=y)
        utilisateur_entry = tk.Entry(form, font=("Segoe UI", 11), bg="#232f3e", fg=BTN_TEXT, relief="flat")
        utilisateur_entry.place(x=140, y=y, width=320)
        y += 46

        tk.Label(form, text="Lu (0 ou 1) :", bg=BG, fg=ACCENT, font=FONT).place(x=34, y=y)
        lu_entry = tk.Entry(form, font=("Segoe UI", 11), bg="#232f3e", fg=BTN_TEXT, relief="flat")
        lu_entry.place(x=140, y=y, width=320)

        if mode == "Modifier" and data:
            contenu_entry.insert(0, data[1])
            date_entry.insert(0, data[2])
            utilisateur_entry.insert(0, data[3])
            lu_entry.insert(0, data[4])

        def enregistrer():
            contenu = contenu_entry.get().strip()
            date = date_entry.get().strip()
            utilisateur = utilisateur_entry.get().strip()
            lu = lu_entry.get().strip()
            if not all([contenu, date, utilisateur, lu]):
                messagebox.showerror("Erreur", "Champs obligatoires manquants.", parent=form)
                return
            if mode == "Ajouter":
                add_notification(contenu, date, utilisateur, lu)
                messagebox.showinfo("Succès", "Notification ajoutée avec succès.", parent=form)
            else:
                update_notification(data[0], contenu, date, utilisateur, lu)
                messagebox.showinfo("Succès", "Notification modifiée.", parent=form)
            self.charger_notifications()
            form.destroy()

        btn_frame = tk.Frame(form, bg=BG)
        btn_frame.place(relx=0.5, y=220, anchor="n")
        tk.Button(btn_frame, text="💾 Enregistrer", font=FONT, bg=ACCENT, fg=BG,
                  relief="flat", cursor="hand2", padx=16, pady=5, command=enregistrer).pack(side="left", padx=9)
        tk.Button(btn_frame, text="❌ Annuler", font=FONT, bg=BTN_DEL, fg=BTN_TEXT,
                  relief="flat", cursor="hand2", padx=16, pady=5, command=form.destroy).pack(side="left", padx=9)
