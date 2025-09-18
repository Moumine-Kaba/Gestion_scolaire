#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Vue d'inscription pour EduManager+
"""

import customtkinter as ctk
from tkinter import messagebox
import re

class RegisterView(ctk.CTkToplevel):
    """Fenêtre d'inscription pour créer un nouveau compte"""

    def __init__(self, auth_manager):
        super().__init__()

        self.auth_manager = auth_manager
        
        # Fenêtre
        self.title("EduManager+ | Créer un compte")
        self.geometry("800x700")
        self.resizable(False, False)
        
        # Variables
        self.username_var = ctk.StringVar()
        self.email_var = ctk.StringVar()
        self.password_var = ctk.StringVar()
        self.confirm_password_var = ctk.StringVar()
        self.nom_var = ctk.StringVar()
        self.prenom_var = ctk.StringVar()
        self.telephone_var = ctk.StringVar()
        
        # Interface
        self.create_register_interface()
        
        # Bindings
        self.bind("<Return>", self.register)
        self.bind("<Escape>", self.close_window)
        
        # Focus sur le premier champ
        self.username_entry.focus()

    def create_register_interface(self):
        """Crée l'interface d'inscription"""
        # Container principal
        container = ctk.CTkFrame(self, fg_color="#0A192F")
        container.pack(fill="both", expand=True, padx=40, pady=40)
        
        # Header
        header = ctk.CTkFrame(container, fg_color="transparent")
        header.pack(fill="x", pady=(0, 30))
        
        ctk.CTkLabel(header, text="🎓", font=("Segoe UI", 48), text_color="#64FFDA").pack(anchor="center", pady=(0, 10))
        ctk.CTkLabel(header, text="Créer un compte", font=("Segoe UI", 32, "bold"), text_color="#64FFDA").pack(anchor="center")
        ctk.CTkLabel(header, text="Rejoignez EduManager+", font=("Segoe UI", 16), text_color="#8EA6C1").pack(anchor="center", pady=(5, 0))
        
        # Formulaire
        form = ctk.CTkFrame(container, fg_color="#0E1C36", corner_radius=20)
        form.pack(fill="both", expand=True, padx=20, pady=20)
        
        content = ctk.CTkFrame(form, fg_color="transparent")
        content.pack(fill="both", expand=True, padx=30, pady=30)
        
        # Grille
        content.grid_columnconfigure(0, weight=1)
        content.grid_columnconfigure(1, weight=1)
        
        # Champs
        row = 0
        
        # Username
        self.create_field(content, "Nom d'utilisateurs *", self.username_var, row, 0, "Entrez votre nom d'utilisateurs")
        # Email
        self.create_field(content, "Email *", self.email_var, row, 1, "votre@email.com")
        
        row += 1
        
        # Prénom
        self.create_field(content, "Prénom *", self.prenom_var, row, 0, "Votre prénom")
        # Nom
        self.create_field(content, "Nom *", self.nom_var, row, 1, "Votre nom")
        
        row += 1
        
        # Mot de passe
        self.create_password_field(content, "Mot de passe *", self.password_var, row, 0, "Minimum 8 caractères")
        # Confirmation
        self.create_password_field(content, "Confirmer le mot de passe *", self.confirm_password_var, row, 1, "Répétez votre mot de passe")
        
        row += 1
        
        # Téléphone
        self.create_field(content, "Téléphone", self.telephone_var, row, 0, "Votre numéro de téléphone")
        
        row += 1
        
        # Boutons
        buttons_frame = ctk.CTkFrame(content, fg_color="transparent")
        buttons_frame.grid(row=row, column=0, columnspan=2, sticky="ew", pady=(20, 0))
        
        # Bouton d'inscription
        self.register_button = ctk.CTkButton(
            buttons_frame, text="Créer mon compte", font=("Segoe UI", 16, "bold"),
            height=48, corner_radius=14, fg_color="#10B981", hover_color="#059669",
            text_color="#FFFFFF", command=self.register
        )
        self.register_button.pack(fill="x", pady=(0, 10))
        
        # Bouton retour
        self.back_button = ctk.CTkButton(
            buttons_frame, text="Retour à la connexion", font=("Segoe UI", 14),
            height=40, corner_radius=12, fg_color="transparent", 
            border_width=2, border_color="#3B82F6", text_color="#3B82F6",
            hover_color="#10233C", command=self.close_window
        )
        self.back_button.pack(fill="x")
        
        # Informations
        info_frame = ctk.CTkFrame(content, fg_color="#0E1C36", corner_radius=12, border_width=1, border_color="#1F3556")
        info_frame.grid(row=row+1, column=0, columnspan=2, sticky="ew", pady=(20, 0))
        
        ctk.CTkLabel(info_frame, text="ℹ️ Informations", font=("Segoe UI", 12, "bold"),
                     text_color="#64FFDA").pack(pady=(12, 6))
        ctk.CTkLabel(info_frame, text="• Les champs marqués * sont obligatoires\n• Votre mot de passe doit contenir au moins 8 caractères\n• Un rôle par défaut vous sera assigné",
                     font=("Segoe UI", 11), text_color="#8EA6C1", justify="left").pack(pady=(0, 12))

    def create_field(self, parent, label_text, variable, row, column, placeholder=""):
        """Crée un champ de saisie"""
        # Label
        ctk.CTkLabel(parent, text=label_text, font=("Segoe UI", 12, "bold"), 
                     text_color="#E5F0FF").grid(row=row*2, column=column, sticky="w", pady=(0, 6))
        
        # Champ de saisie
        entry = ctk.CTkEntry(
            parent, textvariable=variable, placeholder_text=placeholder,
            font=("Segoe UI", 14), height=44, corner_radius=10,
            fg_color="#12243F", border_width=1, border_color="#274569", text_color="#E5F0FF"
        )
        entry.grid(row=row*2+1, column=column, sticky="ew", pady=(0, 16))
        
        # Stocker la référence pour le focus
        if label_text == "Nom d'utilisateurs *":
            self.username_entry = entry
        elif label_text == "Email *":
            self.email_entry = entry
        elif label_text == "Prénom *":
            self.prenom_entry = entry
        elif label_text == "Nom *":
            self.nom_entry = entry
        elif label_text == "Téléphone":
            self.telephone_entry = entry

    def create_password_field(self, parent, label_text, variable, row, column, placeholder=""):
        """Crée un champ de mot de passe"""
        # Label
        ctk.CTkLabel(parent, text=label_text, font=("Segoe UI", 12, "bold"), 
                     text_color="#E5F0FF").grid(row=row*2, column=column, sticky="w", pady=(0, 6))
        
        # Container du champ
        field_container = ctk.CTkFrame(parent, fg_color="#12243F", corner_radius=10, 
                                      border_width=1, border_color="#274569")
        field_container.grid(row=row*2+1, column=column, sticky="ew", pady=(0, 16))
        field_container.grid_columnconfigure(1, weight=1)
        
        # Icône de cadenas
        ctk.CTkLabel(field_container, text="🔒", font=("Segoe UI", 18), width=34).grid(row=0, column=0, padx=(10, 0), pady=8, sticky="w")
        
        # Champ de saisie
        entry = ctk.CTkEntry(
            field_container, textvariable=variable, placeholder_text=placeholder,
            font=("Segoe UI", 14), height=44, corner_radius=10,
            fg_color="#12243F", border_width=0, text_color="#E5F0FF", show="●"
        )
        entry.grid(row=0, column=1, pady=6, padx=(6, 0), sticky="ew")
        
        # Bouton afficher/masquer
        eye_button = ctk.CTkButton(
            field_container, text="👁️", width=38, height=30,
            fg_color="transparent", hover_color="#0f2037", 
            command=lambda: self.toggle_password_visibility(entry)
        )
        eye_button.grid(row=0, column=2, padx=6, pady=6)
        
        # Stocker la référence pour le focus
        if label_text == "Mot de passe *":
            self.password_entry = entry
        elif label_text == "Confirmer le mot de passe *":
            self.confirm_password_entry = entry

    def toggle_password_visibility(self, entry):
        """Bascule la visibilité du mot de passe"""
        current_show = entry.cget("show")
        entry.configure(show="" if current_show == "●" else "●")

    def validate_form(self):
        """Valide le formulaire d'inscription"""
        # Vérifier les champs obligatoires
        required_fields = {
            "Nom d'utilisateurs": self.username_var.get().strip(),
            "Email": self.email_var.get().strip(),
            "Prénom": self.prenom_var.get().strip(),
            "Nom": self.nom_var.get().strip(),
            "Mot de passe": self.password_var.get(),
            "Confirmation mot de passe": self.confirm_password_var.get()
        }
        
        for field_name, value in required_fields.items():
            if not value:
                messagebox.showerror("Erreur", f"Le champ '{field_name}' est obligatoire")
                return False
        
        # Vérifier la longueur du mot de passe
        if len(self.password_var.get()) < 8:
            messagebox.showerror("Erreur", "Le mot de passe doit contenir au moins 8 caractères")
            self.password_entry.focus()
            return False
        
        # Vérifier la confirmation du mot de passe
        if self.password_var.get() != self.confirm_password_var.get():
            messagebox.showerror("Erreur", "Les mots de passe ne correspondent pas")
            self.confirm_password_entry.focus()
            return False
        
        # Vérifier le format de l'email
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, self.email_var.get()):
            messagebox.showerror("Erreur", "Format d'email invalide")
            self.email_entry.focus()
            return False
        
        # Vérifier la longueur du nom d'utilisateurs
        if len(self.username_var.get()) < 3:
            messagebox.showerror("Erreur", "Le nom d'utilisateurs doit contenir au moins 3 caractères")
            self.username_entry.focus()
            return False
        
        return True

    def register(self, event=None):
        """Traite l'inscription de l'utilisateurs"""
        if not self.validate_form():
            return
        
        # Désactiver le bouton pendant le traitement
        self.register_button.configure(state="disabled", text="Création en cours...")
        self.update()
        
        try:
            # Créer l'utilisateurs
            success = self.auth_manager.create_user_simple(
                username=self.username_var.get().strip(),
                password=self.password_var.get(),
                email=self.email_var.get().strip(),
                nom=self.nom_var.get().strip(),
                prenom=self.prenom_var.get().strip(),
                telephone=self.telephone_var.get().strip() if self.telephone_var.get().strip() else None
            )
            
            if success:
                messagebox.showinfo("Succès", 
                    f"Compte créé avec succès !\n\n"
                    f"Nom d'utilisateurs: {self.username_var.get().strip()}\n"
                    f"Vous pouvez maintenant vous connecter avec vos identifiants.")
                
                # Fermer la fenêtre d'inscription
                self.close_window()
            else:
                messagebox.showerror("Erreur", "Impossible de créer le compte. Vérifiez que le nom d'utilisateurs et l'email ne sont pas déjà utilisés.")
                
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de la création du compte: {str(e)}")
            print(f"❌ Erreur création compte: {e}")
        finally:
            self.register_button.configure(state="normal", text="Créer mon compte")

    def close_window(self):
        """Ferme la fenêtre d'inscription"""
        self.destroy()

if __name__ == "__main__":
    try:
        # Créer un AuthManager factice pour les tests
        class MockAuthManager:
            def create_user_simple(self, **kwargs):
                print(f"Mock: Création utilisateurs {kwargs}")
                return True
        
        app = RegisterView(MockAuthManager())
        app.mainloop()
    except Exception as e:
        print(f"❌ Erreur lancement RegisterView: {e}")
        messagebox.showerror("Erreur Critique", f"Impossible de lancer l'inscription: {str(e)}")
