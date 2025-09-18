from database.connection import get_db_connection
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

FONT = "Segoe UI"
BG_MAIN = "#0f172a"
FG_MAIN = "#f1f5f9"
NEON_BLUE = "#38bdf8"

class TransfertEleveView(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg=BG_MAIN)
        self.pack(fill="both", expand=True)
        self.init_ui()

    def init_ui(self):
        title = tk.Label(self, text="🔁 Transfert d’un élève", font=(FONT, 20, "bold"), bg=BG_MAIN, fg=FG_MAIN)
        title.pack(pady=20)

        frame = tk.Frame(self, bg=BG_MAIN)
        frame.pack(pady=10)

        # Élève
        tk.Label(frame, text="Élève :", font=(FONT, 12), bg=BG_MAIN, fg=FG_MAIN).grid(row=0, column=0, padx=10, pady=10, sticky="e")
        self.eleves_cb = ttk.Combobox(frame, width=40, state="readonly")
        self.eleves_cb.grid(row=0, column=1, padx=10, pady=10)
        self.eleves_cb.bind("<<ComboboxSelected>>", self.maj_classe_actuelle)

        # Classe actuelle (affichage)
        tk.Label(frame, text="Classe actuelle :", font=(FONT, 12), bg=BG_MAIN, fg=FG_MAIN).grid(row=1, column=0, padx=10, pady=10, sticky="e")
        self.classe_actuelle_lbl = tk.Label(frame, text="—", font=(FONT, 12), bg=BG_MAIN, fg=NEON_BLUE)
        self.classe_actuelle_lbl.grid(row=1, column=1, sticky="w", padx=10)

        # Nouvelle classes
        tk.Label(frame, text="Nouvelle classes :", font=(FONT, 12), bg=BG_MAIN, fg=FG_MAIN).grid(row=2, column=0, padx=10, pady=10, sticky="e")
        self.nouvelle_cb = ttk.Combobox(frame, width=40, state="readonly")
        self.nouvelle_cb.grid(row=2, column=1, padx=10, pady=10)

        # Motif
        tk.Label(frame, text="Motif du transfert :", font=(FONT, 12), bg=BG_MAIN, fg=FG_MAIN).grid(row=3, column=0, padx=10, pady=10, sticky="e")
        self.motif_entry = tk.Entry(frame, width=42)
        self.motif_entry.grid(row=3, column=1, padx=10, pady=10)

        # Bouton
        bouton = tk.Button(self, text="📤 Transférer", font=(FONT, 12, "bold"), bg=NEON_BLUE, fg="black", command=self.transférer)
        bouton.pack(pady=20)

        self.charger_eleves()
        self.charger_classes()

    def charger_eleves(self):
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("""
            SELECT e.id, CONCAT(e.nom, ' ', e.prenom), c.nom
            FROM eleves e
            LEFT JOIN classes c ON e.classe_id = c.id
        """)
        self.eleves = cur.fetchall()
        self.eleves_cb["values"] = [f"{e[1]} (Classe: {e[2]})" for e in self.eleves]
        conn.close()

    def charger_classes(self):
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT id, nom FROM classes")
        self.classes = cur.fetchall()
        self.nouvelle_cb["values"] = [c[1] for c in self.classes]
        conn.close()

    def maj_classe_actuelle(self, event):
        idx = self.eleves_cb.current()
        if idx >= 0:
            classes = self.eleves[idx][2] or "—"
            self.classe_actuelle_lbl.config(text=classes)

    def transférer(self):
        idx_eleve = self.eleves_cb.current()
        idx_nouvelle = self.nouvelle_cb.current()
        motif = self.motif_entry.get()

        if idx_eleve == -1 or idx_nouvelle == -1:
            messagebox.showwarning("Champs manquants", "Veuillez sélectionner l'élève et la nouvelle classes.")
            return

        eleve_id = self.eleves[idx_eleve][0]
        ancienne_classe_id = self.get_classe_id(self.eleves[idx_eleve][2])
        nouvelle_classe_id = self.classes[idx_nouvelle][0]

        if ancienne_classe_id == nouvelle_classe_id:
            messagebox.showinfo("Aucun changement", "L’élève est déjà dans cette classes.")
            return

        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO transferts (eleve_id, ancienne_classe_id, nouvelle_classe_id, date_transfert, motif)
            VALUES (?, ?, ?, ?, ?)
        """, (eleve_id, ancienne_classe_id, nouvelle_classe_id, datetime.now().strftime("%Y-%m-%d"), motif))
        cur.execute("UPDATE eleves SET classe_id = ? WHERE id = ?", (nouvelle_classe_id, eleve_id))
        conn.commit()
        conn.close()

        messagebox.showinfo("Succès", "Transfert effectué avec succès.")
        self.charger_eleves()
        self.eleves_cb.current(-1)
        self.nouvelle_cb.current(-1)
        self.motif_entry.delete(0, "end")
        self.classe_actuelle_lbl.config(text="—")

    def get_classe_id(self, nom_classe):
        for c in self.classes:
            if c[1] == nom_classe:
                return c[0]
        return None
# Alias pour compatibilité
TransfertView = TransfertEleveView

