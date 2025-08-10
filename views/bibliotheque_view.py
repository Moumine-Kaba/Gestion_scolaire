import tkinter as tk
from controllers.bibliotheque_controller import get_all_bibliotheques, add_bibliotheque, update_bibliotheque, delete_bibliotheque

class BibliothequeView(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="#111827")
        tk.Label(self, text="Gestion de la Bibliothèque", font=("Segoe UI", 22, "bold"),
                 fg="white", bg="#111827").pack(pady=18)
        # À compléter : CRUD + tableau
