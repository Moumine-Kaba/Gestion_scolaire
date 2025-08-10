import tkinter as tk
from controllers.competence_controller import get_all_competences, add_competence, update_competence, delete_competence

class CompetencesView(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="#111827")
        tk.Label(self, text="Gestion des Compétences", font=("Segoe UI", 22, "bold"),
                 fg="white", bg="#111827").pack(pady=18)
        # À compléter : CRUD + tableau
