#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Exemple d'utilisation du composant IndividualBulletinWidget
Intégration dans bulletins_view.py
"""

import customtkinter as ctk
import os
import sys
from tkinter import messagebox, filedialog

# Ajouter le chemin racine pour les imports
root_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))
sys.path.insert(0, root_path)

# Import du composant et du gestionnaire
from src.modules.academic.grades.components.individual_bulletin_widget import IndividualBulletinWidget
from src.modules.academic.grades.managers.bulletin_manager import bulletin_manager
from resources.themes.theme import *

class BulletinsViewExample(ctk.CTkFrame):
    """Exemple d'utilisation du composant IndividualBulletinWidget"""
    
    def __init__(self, parent):
        super().__init__(parent, fg_color=BG_MAIN)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        # Variables de données
        self.current_student = None
        self.bulletins_data = []
        
        self._build_main_ui()
    
    def _build_main_ui(self):
        """Construit l'interface principale"""
        main_frame = ctk.CTkFrame(self, fg_color="transparent")
        main_frame.pack(fill="both", expand=True, padx=15, pady=15)
        main_frame.grid_columnconfigure(1, weight=1)
        main_frame.grid_rowconfigure(0, weight=1)

        # Panneau de gauche: Liste des élèves
        left_panel = ctk.CTkFrame(main_frame, fg_color=CARD_BG, corner_radius=20, width=300)
        left_panel.grid(row=0, column=0, sticky="ns", padx=(0, 15))
        left_panel.grid_propagate(False)
        left_panel.grid_columnconfigure(0, weight=1)
        left_panel.grid_rowconfigure(1, weight=1)
        
        self._build_students_list(left_panel)
        
        # Panneau de droite: Bulletin individuel
        right_panel = ctk.CTkFrame(main_frame, fg_color="transparent")
        right_panel.grid(row=0, column=1, sticky="nsew", padx=(10, 0))
        right_panel.grid_columnconfigure(0, weight=1)
        right_panel.grid_rowconfigure(0, weight=1)
        
        # Conteneur pour le bulletin individuel
        self.bulletin_container = ctk.CTkFrame(right_panel, fg_color="transparent")
        self.bulletin_container.grid(row=0, column=0, sticky="nsew")
        self.bulletin_container.grid_columnconfigure(0, weight=1)
        self.bulletin_container.grid_rowconfigure(0, weight=1)
        
        # Message par défaut
        self._show_default_message()
    
    def _build_students_list(self, parent):
        """Construit la liste des élèves"""
        # Titre
        title_label = ctk.CTkLabel(
            parent, 
            text="ÉLÈVES DE LA CLASSE",
            font=F_SUB,
            text_color=TEXT_PRIMARY
        )
        title_label.grid(row=0, column=0, sticky="ew", padx=10, pady=10)
        
        # Liste scrollable
        self.students_scroll_frame = ctk.CTkScrollableFrame(
            parent, 
            fg_color="transparent",
            scrollbar_button_color=ACCENT,
            scrollbar_button_hover_color=HOVER_PRIMARY
        )
        self.students_scroll_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=(0, 10))
        self.students_scroll_frame.grid_columnconfigure(0, weight=1)
        
        # Données d'exemple
        self.students_data = [
            {'id_eleve': 1, 'prenom': 'Ahmed', 'nom': 'Benali', 'classe': '4ème A'},
            {'id_eleve': 2, 'prenom': 'Fatima', 'nom': 'Kadiri', 'classe': '4ème A'},
            {'id_eleve': 3, 'prenom': 'Omar', 'nom': 'Tazi', 'classe': '4ème A'},
            {'id_eleve': 4, 'prenom': 'Aicha', 'nom': 'Alami', 'classe': '4ème A'},
            {'id_eleve': 5, 'prenom': 'Youssef', 'nom': 'Bennani', 'classe': '4ème A'},
        ]
        
        self._update_students_list()
    
    def _update_students_list(self):
        """Met à jour la liste des élèves"""
        # Effacer le contenu actuel
        for widget in self.students_scroll_frame.winfo_children():
            widget.destroy()
        
        # Créer les éléments pour chaque élève
        for student in self.students_data:
            student_name = f"{student.get('prenom', '')} {student.get('nom', '')}"
            
            # Conteneur de l'élève avec contour
            student_container = ctk.CTkFrame(
                self.students_scroll_frame,
                fg_color=CARD_BG,
                border_color=BORDER_COLOR,
                border_width=1,
                corner_radius=12,
                height=60
            )
            student_container.pack(fill="x", padx=8, pady=4)
            student_container.pack_propagate(False)
            student_container.grid_columnconfigure(1, weight=1)
            
            # Icône
            icon_label = ctk.CTkLabel(
                student_container,
                text="👤",
                font=("Segoe UI", 20),
                text_color=TEXT_PRIMARY,
                width=40
            )
            icon_label.grid(row=0, column=0, padx=15, pady=15, sticky="w")
            
            # Nom
            name_label = ctk.CTkLabel(
                student_container,
                text=student_name,
                font=("Segoe UI", 14, "bold"),
                text_color=TEXT_PRIMARY,
                anchor="w"
            )
            name_label.grid(row=0, column=1, padx=10, pady=15, sticky="ew")
            
            # Rang (exemple)
            rang_label = ctk.CTkLabel(
                student_container,
                text=f"{student.get('id_eleve', '')}",
                font=("Segoe UI", 16, "bold"),
                text_color=TEXT_SECONDARY,
                width=40
            )
            rang_label.grid(row=0, column=2, padx=15, pady=15, sticky="e")
            
            # Événement de clic
            def make_click_handler(s):
                def on_click(event):
                    self._on_student_selected(s)
                return on_click
            
            student_container.bind("<Button-1>", make_click_handler(student))
            icon_label.bind("<Button-1>", make_click_handler(student))
            name_label.bind("<Button-1>", make_click_handler(student))
            rang_label.bind("<Button-1>", make_click_handler(student))
            
            # Effet hover
            def on_enter(event):
                student_container.configure(fg_color=HOVER_PRIMARY, border_color=ACCENT)
            
            def on_leave(event):
                student_container.configure(fg_color=CARD_BG, border_color=BORDER_COLOR)
            
            student_container.bind("<Enter>", on_enter)
            student_container.bind("<Leave>", on_leave)
    
    def _on_student_selected(self, student):
        """Gère la sélection d'un élève"""
        print(f"🔄 Sélection de l'élève: {student.get('prenom', '')} {student.get('nom', '')}")
        self.current_student = student
        
        # Effacer le conteneur du bulletin
        for widget in self.bulletin_container.winfo_children():
            widget.destroy()
        
        # Créer les données du bulletin
        bulletin_data = bulletin_manager.create_bulletin_data(student, self.bulletins_data)
        
        # Créer le composant bulletin individuel
        self.bulletin_widget = IndividualBulletinWidget(
            self.bulletin_container,
            student_data=student,
            bulletin_data=bulletin_data,
            design_variant='premium',  # premium, compact, simple
            show_actions=True,
            show_grading_scale=True,
            show_comment=True
        )
        self.bulletin_widget.grid(row=0, column=0, sticky="nsew")
        
        # Définir les callbacks
        self.bulletin_widget.set_callbacks(
            on_print=self._on_print_bulletin,
            on_export=self._on_export_bulletin,
            on_back=self._on_back_to_list
        )
    
    def _show_default_message(self):
        """Affiche le message par défaut"""
        message_label = ctk.CTkLabel(
            self.bulletin_container,
            text="Sélectionnez un élève pour afficher son bulletin",
            font=F_SUB,
            text_color=TEXT_SECONDARY
        )
        message_label.grid(row=0, column=0, sticky="nsew")
    
    def _on_print_bulletin(self, student_data, bulletin_data):
        """Callback pour l'impression"""
        print(f"🖨️ Impression du bulletin de {student_data.get('prenom', '')} {student_data.get('nom', '')}")
        success = bulletin_manager.print_bulletin(student_data, bulletin_data)
        if success:
            messagebox.showinfo("Impression", "Bulletin envoyé à l'imprimante")
        else:
            messagebox.showerror("Erreur", "Erreur lors de l'impression")
    
    def _on_export_bulletin(self, student_data, bulletin_data):
        """Callback pour l'export"""
        print(f"📊 Export du bulletin de {student_data.get('prenom', '')} {student_data.get('nom', '')}")
        
        file_path = filedialog.asksaveasfilename(
            defaultextension=".xlsx",
            filetypes=[
                ("Fichiers Excel", "*.xlsx"),
                ("Fichiers CSV", "*.csv")
            ],
            title=f"Exporter le bulletin de {student_data.get('prenom', '')} {student_data.get('nom', '')}"
        )
        
        if file_path:
            success = bulletin_manager.export_bulletin(student_data, bulletin_data, file_path)
            if success:
                messagebox.showinfo("Export réussi", f"Bulletin exporté vers {file_path}")
            else:
                messagebox.showerror("Erreur", "Erreur lors de l'export")
    
    def _on_back_to_list(self):
        """Callback pour le retour à la liste"""
        print("← Retour à la liste des élèves")
        # Effacer le bulletin et afficher le message par défaut
        for widget in self.bulletin_container.winfo_children():
            widget.destroy()
        self._show_default_message()
        self.current_student = None

# Exemple d'utilisation
if __name__ == "__main__":
    import customtkinter as ctk
    
    app = ctk.CTk()
    app.title("Exemple BulletinsView avec Composant Réutilisable")
    app.geometry("1200x800")
    
    # Appliquer le thème
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")
    
    # Créer la vue
    view = BulletinsViewExample(app)
    view.pack(fill="both", expand=True)
    
    app.mainloop()










