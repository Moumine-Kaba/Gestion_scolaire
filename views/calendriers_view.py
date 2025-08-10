import tkinter as tk
from controllers.calendrier_controller import get_all_calendriers, add_calendrier, update_calendrier, delete_calendrier

class CalendriersView(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="#111827")
        tk.Label(self, text="Gestion du Calendrier", font=("Segoe UI", 22, "bold"),
                 fg="white", bg="#111827").pack(pady=18)
        # À compléter : CRUD + tableau
