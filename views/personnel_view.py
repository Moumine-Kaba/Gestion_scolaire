import tkinter as tk
from controllers.personnel_controller import get_all_personnel, add_personnel, update_personnel, delete_personnel

class PersonnelView(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="#111827")
        tk.Label(self, text="Gestion du Personnel", font=("Segoe UI", 22, "bold"),
                 fg="white", bg="#111827").pack(pady=18)
        # À compléter : CRUD + tableau
