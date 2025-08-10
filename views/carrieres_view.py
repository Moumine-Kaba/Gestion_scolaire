import tkinter as tk
from tkinter import ttk, messagebox
from controllers.carriere_controller import get_all_carrieres, add_carriere, update_carriere, delete_carriere

class CarrieresView(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="#111827")
        tk.Label(self, text="Gestion des Carrières", font=("Segoe UI", 22, "bold"),
                 fg="white", bg="#111827").pack(pady=18)
        # (à compléter : CRUD + tableau)
