#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import tkinter as tk
from tkinter import ttk, messagebox
import customtkinter as ctk
from src.modules.academic.classes.controllers.cours_controller import get_all_emplois

class EmploisView(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        
        # Titre
        title = ctk.CTkLabel(self, text="Emplois du Temps", 
                           font=("Segoe UI", 24, "bold"))
        title.pack(pady=20)
        
        # Frame pour le contenu
        content_frame = ctk.CTkFrame(self)
        content_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Label d'information
        info_label = ctk.CTkLabel(content_frame, 
                                 text="Gestion des emplois du temps",
                                 font=("Segoe UI", 16))
        info_label.pack(pady=50)
        
        # Bouton pour charger les emplois
        load_btn = ctk.CTkButton(content_frame, 
                                text="Charger les emplois",
                                command=self.load_emplois)
        load_btn.pack(pady=20)
    
    def load_emplois(self):
        """Charge les emplois du temps"""
        try:
            emplois = get_all_emplois()
            messagebox.showinfo("Succès", f"{len(emplois)} emplois chargés")
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors du chargement: {e}")
