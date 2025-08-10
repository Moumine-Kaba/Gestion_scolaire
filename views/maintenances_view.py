import tkinter as tk
from controllers.maintenance_controller import get_all_maintenances, add_maintenance, update_maintenance, delete_maintenance

class MaintenancesView(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="#111827")
        tk.Label(self, text="Gestion de la Maintenance", font=("Segoe UI", 22, "bold"),
                 fg="white", bg="#111827").pack(pady=18)
        # À compléter : CRUD + tableau
