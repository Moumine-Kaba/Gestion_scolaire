#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import tkinter as tk
from tkinter import ttk, messagebox
import customtkinter as ctk
from src.modules.academic.classes.controllers.cours_controller import get_all_enseignements

class EnseignementsView(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        
        # Titre
        title = ctk.CTkLabel(self, text="Enseignements", 
                           font=("Segoe UI", 24, "bold"))
        title.pack(pady=20)
        
        # Frame pour le contenu
        content_frame = ctk.CTkFrame(self)
        content_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Label d'information
        info_label = ctk.CTkLabel(content_frame, 
                                 text="Gestion des enseignements",
                                 font=("Segoe UI", 16))
        info_label.pack(pady=50)
        
        # Bouton pour charger les enseignements
        load_btn = ctk.CTkButton(content_frame, 
                                text="Charger les enseignements",
                                command=self.load_enseignements)
        load_btn.pack(pady=20)
    
    def load_enseignements(self):
        """Charge les enseignements"""
        try:
            enseignements = get_all_enseignements()
            messagebox.showinfo("Succès", f"{len(enseignements)} enseignements chargés")
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors du chargement: {e}")
