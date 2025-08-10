import tkinter as tk
from tkinter import ttk, messagebox
from controllers.objectif_controller import get_all_objectifs, add_objectif, update_objectif, delete_objectif

class ObjectifsView(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="#111827")
        tk.Label(self, text="Gestion des Objectifs", font=("Segoe UI", 22, "bold"),
                 fg="white", bg="#111827").pack(pady=18)
        # (à compléter : CRUD + tableau)
