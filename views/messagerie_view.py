import tkinter as tk
from controllers.messagerie_controller import get_all_messages, add_message, update_message, delete_message

class MessagerieView(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="#111827")
        tk.Label(self, text="Messagerie interne", font=("Segoe UI", 22, "bold"),
                 fg="white", bg="#111827").pack(pady=18)
        # À compléter : CRUD + tableau/messages
