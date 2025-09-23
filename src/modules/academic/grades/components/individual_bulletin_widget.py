#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Composant Réutilisable pour les Bulletins Individuels
Design moderne et cohérent pour toutes les vues
"""

import customtkinter as ctk
import os
from PIL import Image
from resources.themes.theme import *

class IndividualBulletinWidget(ctk.CTkFrame):
    """Composant réutilisable pour afficher les bulletins individuels"""
    
    def __init__(self, parent, student_data=None, bulletin_data=None, **kwargs):
        super().__init__(parent, **kwargs)
        
        # Configuration par défaut
        self.student_data = student_data or {}
        self.bulletin_data = bulletin_data or {}
        self.icons_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))), "resources", "icons")
        
        # Options de design
        self.design_variant = kwargs.get('design_variant', 'premium')  # premium, compact, simple
        self.show_actions = kwargs.get('show_actions', True)
        self.show_grading_scale = kwargs.get('show_grading_scale', True)
        self.show_comment = kwargs.get('show_comment', True)
        
        self._build_bulletin()
    
    def load_icon(self, icon_name, size=(24, 24)):
        """Charge une icône depuis le dossier resources/icons"""
        try:
            icon_path = os.path.join(self.icons_path, icon_name)
            if os.path.exists(icon_path):
                img = Image.open(icon_path)
                img = img.resize(size, Image.Resampling.LANCZOS)
                return ctk.CTkImage(img, size=size)
            else:
                print(f"⚠️ Icône non trouvée: {icon_path}")
                return None
        except Exception as e:
            print(f"❌ Erreur chargement icône {icon_name}: {e}")
            return None
    
    def _build_bulletin(self):
        """Construit le bulletin selon la variante de design"""
        if self.design_variant == 'premium':
            self._build_premium_design()
        elif self.design_variant == 'compact':
            self._build_compact_design()
        elif self.design_variant == 'simple':
            self._build_simple_design()
        else:
            self._build_premium_design()  # Par défaut
    
    def _build_premium_design(self):
        """Design premium avec toutes les fonctionnalités"""
        # Configuration de la grille
        self.grid_columnconfigure(0, weight=1)
        
        # Conteneur principal du bulletin (design premium)
        bulletin_frame = ctk.CTkFrame(self, fg_color="white", corner_radius=20, width=600, height=500)
        bulletin_frame.pack(expand=True, padx=20, pady=20)
        bulletin_frame.pack_propagate(False)
        bulletin_frame.grid_columnconfigure(0, weight=1)
        
        # En-tête premium
        self._build_premium_header(bulletin_frame)
        
        # Informations élève premium
        self._build_premium_student_info(bulletin_frame)
        
        # Tableau des notes premium
        self._build_premium_grades_table(bulletin_frame)
        
        # Mention premium
        self._build_premium_mention(bulletin_frame)
        
        # Section basse premium
        if self.show_grading_scale or self.show_comment:
            self._build_premium_bottom_section(bulletin_frame)
        
        # Boutons d'action premium
        if self.show_actions:
            self._build_premium_actions(bulletin_frame)
    
    def _build_premium_header(self, parent):
        """En-tête premium avec logo"""
        header_frame = ctk.CTkFrame(parent, fg_color="#1E40AF", corner_radius=15)
        header_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=10)
        header_frame.grid_columnconfigure(1, weight=1)
        
        # Logo avec logo.png
        try:
            logo_path = os.path.join(self.icons_path, "logo.png")
            if os.path.exists(logo_path):
                logo_image = ctk.CTkImage(light_image=Image.open(logo_path), size=(60, 60))
                logo_label = ctk.CTkLabel(header_frame, text="", image=logo_image)
                logo_label.grid(row=0, column=0, padx=20, pady=20, sticky="w")
            else:
                bulletin_icon = self.load_icon("newspaper.png", size=(50, 50))
                if bulletin_icon:
                    logo_label = ctk.CTkLabel(header_frame, text="", image=bulletin_icon)
                    logo_label.grid(row=0, column=0, padx=20, pady=20, sticky="w")
                else:
                    logo_label = ctk.CTkLabel(header_frame, text="📊", font=("Segoe UI", 35), text_color="white")
                    logo_label.grid(row=0, column=0, padx=20, pady=20, sticky="w")
        except Exception as e:
            print(f"⚠️ Erreur chargement logo: {e}")
            logo_label = ctk.CTkLabel(header_frame, text="📊", font=("Segoe UI", 35), text_color="white")
            logo_label.grid(row=0, column=0, padx=20, pady=20, sticky="w")
        
        # Titre et établissement
        title_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        title_frame.grid(row=0, column=1, sticky="w", padx=20, pady=20)
        
        title_label = ctk.CTkLabel(
            title_frame,
            text="BULLETIN DE NOTES",
            font=("Segoe UI", 22, "bold"),
            text_color="white"
        )
        title_label.grid(row=0, column=0, sticky="w")
        
        school_label = ctk.CTkLabel(
            title_frame,
            text="Établissement Scolaire Moderne",
            font=("Segoe UI", 12),
            text_color="#E0E7FF"
        )
        school_label.grid(row=1, column=0, sticky="w", pady=(5, 0))
        
        year_label = ctk.CTkLabel(
            title_frame,
            text="Année Scolaire 2024-2025",
            font=("Segoe UI", 10),
            text_color="#C7D2FE"
        )
        year_label.grid(row=2, column=0, sticky="w", pady=(2, 0))
    
    def _build_premium_student_info(self, parent):
        """Informations élève premium"""
        student_info_frame = ctk.CTkFrame(parent, fg_color="#F1F5F9", corner_radius=12)
        student_info_frame.grid(row=1, column=0, sticky="ew", padx=10, pady=8)
        student_info_frame.grid_columnconfigure(1, weight=1)
        student_info_frame.grid_columnconfigure(3, weight=1)
        
        # Informations élève avec icônes
        student_icon = self.load_icon("person.png", size=(16, 16))
        if student_icon:
            ctk.CTkLabel(student_info_frame, text="", image=student_icon).grid(row=0, column=0, sticky="w", padx=(15, 5), pady=8)
        ctk.CTkLabel(student_info_frame, text="Élève :", font=("Segoe UI", 11, "bold"), text_color="#475569").grid(row=0, column=0, sticky="w", padx=(15, 5), pady=8)
        student_name_label = ctk.CTkLabel(student_info_frame, text=f"{self.student_data.get('prenom', '')} {self.student_data.get('nom', '')}", font=("Segoe UI", 11, "bold"), text_color="#1E293B")
        student_name_label.grid(row=0, column=1, sticky="w", padx=(0, 20), pady=8)
        
        class_icon = self.load_icon("classroom.png", size=(16, 16))
        if class_icon:
            ctk.CTkLabel(student_info_frame, text="", image=class_icon).grid(row=0, column=2, sticky="w", padx=(0, 5), pady=8)
        ctk.CTkLabel(student_info_frame, text="Classe :", font=("Segoe UI", 11, "bold"), text_color="#475569").grid(row=0, column=2, sticky="w", padx=(0, 5), pady=8)
        class_label = ctk.CTkLabel(student_info_frame, text=self.bulletin_data.get('classe', 'N/A'), font=("Segoe UI", 11, "bold"), text_color="#1E293B")
        class_label.grid(row=0, column=3, sticky="w", pady=8)
        
        # Moyenne, rang et mention
        if self.bulletin_data:
            moyenne_generale = self.bulletin_data.get('moyenne_generale', 0)
            rang = self.bulletin_data.get('rang', 0)
            mention = self.bulletin_data.get('mention', 'N/A')
            
            # Moyenne
            grade_icon = self.load_icon("grade.png", size=(16, 16))
            if grade_icon:
                ctk.CTkLabel(student_info_frame, text="", image=grade_icon).grid(row=1, column=0, sticky="w", padx=(15, 5), pady=(5, 0))
            ctk.CTkLabel(student_info_frame, text="Moyenne :", font=("Segoe UI", 11, "bold"), text_color="#475569").grid(row=1, column=0, sticky="w", padx=(15, 5), pady=(5, 0))
            moyenne_label = ctk.CTkLabel(student_info_frame, text=f"{moyenne_generale:.2f}/20", font=("Segoe UI", 12, "bold"), text_color="#059669")
            moyenne_label.grid(row=1, column=1, sticky="w", padx=(0, 20), pady=(5, 0))
            
            # Rang
            rank_icon = self.load_icon("award.png", size=(16, 16))
            if rank_icon:
                ctk.CTkLabel(student_info_frame, text="", image=rank_icon).grid(row=1, column=2, sticky="w", padx=(0, 5), pady=(5, 0))
            ctk.CTkLabel(student_info_frame, text="Rang :", font=("Segoe UI", 11, "bold"), text_color="#475569").grid(row=1, column=2, sticky="w", padx=(0, 5), pady=(5, 0))
            rang_label = ctk.CTkLabel(student_info_frame, text=f"{rang}ème", font=("Segoe UI", 12, "bold"), text_color="#DC2626")
            rang_label.grid(row=1, column=3, sticky="w", pady=(5, 0))
            
            # Mention
            mention_icon = self.load_icon("star.png", size=(16, 16))
            if mention_icon:
                ctk.CTkLabel(student_info_frame, text="", image=mention_icon).grid(row=2, column=0, sticky="w", padx=(15, 5), pady=(5, 8))
            ctk.CTkLabel(student_info_frame, text="Mention :", font=("Segoe UI", 11, "bold"), text_color="#475569").grid(row=2, column=0, sticky="w", padx=(15, 5), pady=(5, 8))
            mention_color = "#059669" if moyenne_generale >= 10 else "#DC2626"
            mention_label = ctk.CTkLabel(student_info_frame, text=mention, font=("Segoe UI", 12, "bold"), text_color=mention_color)
            mention_label.grid(row=2, column=1, sticky="w", padx=(0, 20), pady=(5, 8))
    
    def _build_premium_grades_table(self, parent):
        """Tableau des notes premium"""
        grades_frame = ctk.CTkFrame(parent, fg_color="white", corner_radius=12)
        grades_frame.grid(row=2, column=0, sticky="ew", padx=10, pady=8)
        grades_frame.grid_columnconfigure(0, weight=1)
        
        # En-tête du tableau
        table_header_frame = ctk.CTkFrame(grades_frame, fg_color="#1E40AF", corner_radius=8)
        table_header_frame.grid(row=0, column=0, sticky="ew", padx=6, pady=6)
        table_header_frame.grid_columnconfigure(0, weight=3)
        table_header_frame.grid_columnconfigure(1, weight=1)
        table_header_frame.grid_columnconfigure(2, weight=1)
        table_header_frame.grid_columnconfigure(3, weight=1)
        
        # En-têtes avec icônes
        headers_data = [
            ("Matière", "book.png"),
            ("Coef.", "target.png"),
            ("Note", "grade.png"),
            ("Moy.", "trending-up.png")
        ]
        
        for i, (header_text, icon_name) in enumerate(headers_data):
            header_container = ctk.CTkFrame(table_header_frame, fg_color="transparent")
            header_container.grid(row=0, column=i, padx=6, pady=8, sticky="ew")
            
            header_icon = self.load_icon(icon_name, size=(16, 16))
            if header_icon:
                icon_label = ctk.CTkLabel(header_container, text="", image=header_icon)
                icon_label.pack(side="left", padx=(0, 4))
            
            label = ctk.CTkLabel(
                header_container, 
                text=header_text, 
                font=("Segoe UI", 11, "bold"), 
                text_color="white"
            )
            label.pack(side="left")
            
            if i == 0:
                header_container.configure(anchor="w")
            else:
                header_container.configure(anchor="center")
        
        # Récupérer les notes de l'élève
        student_notes = self.bulletin_data.get('notes', [])
        
        # Créer les lignes du tableau
        row_index = 1
        total_points = 0
        total_coefficients = 0
        
        for subject_data in student_notes:
            bg_color = "#F8FAFC" if row_index % 2 == 0 else "#FFFFFF"
            row_frame = ctk.CTkFrame(grades_frame, fg_color=bg_color, corner_radius=6)
            row_frame.grid(row=row_index, column=0, sticky="ew", padx=6, pady=2)
            row_frame.grid_columnconfigure(0, weight=3)
            row_frame.grid_columnconfigure(1, weight=1)
            row_frame.grid_columnconfigure(2, weight=1)
            row_frame.grid_columnconfigure(3, weight=1)
            
            # Matière avec icône
            matiere_container = ctk.CTkFrame(row_frame, fg_color="transparent")
            matiere_container.grid(row=0, column=0, padx=8, pady=8, sticky="ew")
            
            subject_icon = self.load_icon("book.png", size=(14, 14))
            if subject_icon:
                matiere_icon_label = ctk.CTkLabel(matiere_container, text="", image=subject_icon)
                matiere_icon_label.pack(side="left", padx=(0, 6))
            
            matiere_label = ctk.CTkLabel(
                matiere_container, 
                text=subject_data.get('nom_matiere', ''), 
                font=("Segoe UI", 10, "bold"), 
                text_color="#1F2937"
            )
            matiere_label.pack(side="left")
            matiere_container.configure(anchor="w")
            
            # Coefficient avec icône
            coefficient = subject_data.get('coefficient', 1)
            coef_container = ctk.CTkFrame(row_frame, fg_color="transparent")
            coef_container.grid(row=0, column=1, padx=8, pady=8, sticky="ew")
            
            coef_icon = self.load_icon("target.png", size=(14, 14))
            if coef_icon:
                coef_icon_label = ctk.CTkLabel(coef_container, text="", image=coef_icon)
                coef_icon_label.pack(side="left", padx=(0, 4))
            
            coef_label = ctk.CTkLabel(
                coef_container, 
                text=str(coefficient), 
                font=("Segoe UI", 10, "bold"), 
                text_color="#374151"
            )
            coef_label.pack(side="left")
            coef_container.configure(anchor="center")
            
            # Note avec icône
            note = subject_data.get('note', 0)
            note_text = f"{note:.1f}" if note > 0 else "-"
            note_container = ctk.CTkFrame(row_frame, fg_color="transparent")
            note_container.grid(row=0, column=2, padx=8, pady=8, sticky="ew")
            
            note_icon = self.load_icon("grade.png", size=(14, 14))
            if note_icon:
                note_icon_label = ctk.CTkLabel(note_container, text="", image=note_icon)
                note_icon_label.pack(side="left", padx=(0, 4))
            
            note_label = ctk.CTkLabel(
                note_container, 
                text=note_text, 
                font=("Segoe UI", 10, "bold"), 
                text_color="#059669"
            )
            note_label.pack(side="left")
            note_container.configure(anchor="center")
            
            # Moyenne pondérée avec icône
            moyenne_ponderee = note * coefficient if note > 0 else 0
            moyenne_text = f"{moyenne_ponderee:.1f}" if moyenne_ponderee > 0 else "-"
            moy_container = ctk.CTkFrame(row_frame, fg_color="transparent")
            moy_container.grid(row=0, column=3, padx=8, pady=8, sticky="ew")
            
            moy_icon = self.load_icon("trending-up.png", size=(14, 14))
            if moy_icon:
                moy_icon_label = ctk.CTkLabel(moy_container, text="", image=moy_icon)
                moy_icon_label.pack(side="left", padx=(0, 4))
            
            moy_label = ctk.CTkLabel(
                moy_container, 
                text=moyenne_text, 
                font=("Segoe UI", 10, "bold"), 
                text_color="#DC2626"
            )
            moy_label.pack(side="left")
            moy_container.configure(anchor="center")
            
            if note > 0:
                total_points += moyenne_ponderee
                total_coefficients += coefficient
            
            row_index += 1
        
        # Ligne de moyenne générale
        if total_coefficients > 0:
            moyenne_generale = total_points / total_coefficients
            
            moyenne_frame = ctk.CTkFrame(grades_frame, fg_color="#F0F9FF", corner_radius=8)
            moyenne_frame.grid(row=row_index, column=0, sticky="ew", padx=6, pady=4)
            moyenne_frame.grid_columnconfigure(0, weight=3)
            moyenne_frame.grid_columnconfigure(1, weight=1)
            moyenne_frame.grid_columnconfigure(2, weight=1)
            moyenne_frame.grid_columnconfigure(3, weight=1)
            
            # Moyenne générale avec icône
            moy_gen_container = ctk.CTkFrame(moyenne_frame, fg_color="transparent")
            moy_gen_container.grid(row=0, column=0, padx=8, pady=10, sticky="ew")
            
            moy_gen_icon = self.load_icon("analytics.png", size=(16, 16))
            if moy_gen_icon:
                moy_gen_icon_label = ctk.CTkLabel(moy_gen_container, text="", image=moy_gen_icon)
                moy_gen_icon_label.pack(side="left", padx=(0, 6))
            
            moy_gen_label = ctk.CTkLabel(moy_gen_container, text="MOYENNE GÉNÉRALE", font=("Segoe UI", 11, "bold"), text_color="#1E40AF")
            moy_gen_label.pack(side="left")
            moy_gen_container.configure(anchor="w")
            
            # Coefficient total
            coef_total_container = ctk.CTkFrame(moyenne_frame, fg_color="transparent")
            coef_total_container.grid(row=0, column=1, padx=8, pady=10, sticky="ew")
            
            coef_total_icon = self.load_icon("target.png", size=(16, 16))
            if coef_total_icon:
                coef_total_icon_label = ctk.CTkLabel(coef_total_container, text="", image=coef_total_icon)
                coef_total_icon_label.pack(side="left", padx=(0, 4))
            
            coef_total_label = ctk.CTkLabel(coef_total_container, text=f"{total_coefficients}", font=("Segoe UI", 11, "bold"), text_color="#1E40AF")
            coef_total_label.pack(side="left")
            coef_total_container.configure(anchor="center")
            
            # Moyenne générale
            moy_val_container = ctk.CTkFrame(moyenne_frame, fg_color="transparent")
            moy_val_container.grid(row=0, column=2, padx=8, pady=10, sticky="ew")
            
            moy_val_icon = self.load_icon("grade.png", size=(16, 16))
            if moy_val_icon:
                moy_val_icon_label = ctk.CTkLabel(moy_val_container, text="", image=moy_val_icon)
                moy_val_icon_label.pack(side="left", padx=(0, 4))
            
            moy_val_label = ctk.CTkLabel(moy_val_container, text=f"{moyenne_generale:.2f}", font=("Segoe UI", 13, "bold"), text_color="#1E40AF")
            moy_val_label.pack(side="left")
            moy_val_container.configure(anchor="center")
            
            # Points total
            points_total_container = ctk.CTkFrame(moyenne_frame, fg_color="transparent")
            points_total_container.grid(row=0, column=3, padx=8, pady=10, sticky="ew")
            
            points_total_icon = self.load_icon("trending-up.png", size=(16, 16))
            if points_total_icon:
                points_total_icon_label = ctk.CTkLabel(points_total_container, text="", image=points_total_icon)
                points_total_icon_label.pack(side="left", padx=(0, 4))
            
            points_total_label = ctk.CTkLabel(points_total_container, text=f"{total_points:.1f}", font=("Segoe UI", 11, "bold"), text_color="#1E40AF")
            points_total_label.pack(side="left")
            points_total_container.configure(anchor="center")
    
    def _build_premium_mention(self, parent):
        """Section mention premium"""
        mention_frame = ctk.CTkFrame(parent, fg_color="#F0FDF4", corner_radius=12)
        mention_frame.grid(row=3, column=0, sticky="ew", padx=10, pady=8)
        
        mention_container = ctk.CTkFrame(mention_frame, fg_color="transparent")
        mention_container.pack(pady=12)
        
        mention_icon = self.load_icon("star.png", size=(20, 20))
        if mention_icon:
            mention_icon_label = ctk.CTkLabel(mention_container, text="", image=mention_icon)
            mention_icon_label.pack(side="left", padx=(0, 8))
        
        mention = self.bulletin_data.get('mention', 'N/A')
        moyenne_generale = self.bulletin_data.get('moyenne_generale', 0)
        mention_color = "#059669" if moyenne_generale >= 10 else "#DC2626"
        mention_label = ctk.CTkLabel(
            mention_container,
            text=f"MENTION: {mention}",
            font=("Segoe UI", 14, "bold"),
            text_color=mention_color
        )
        mention_label.pack(side="left")
    
    def _build_premium_bottom_section(self, parent):
        """Section basse premium"""
        bottom_frame = ctk.CTkFrame(parent, fg_color="#F8FAFC", corner_radius=12)
        bottom_frame.grid(row=4, column=0, sticky="ew", padx=10, pady=8)
        bottom_frame.grid_columnconfigure(0, weight=1)
        bottom_frame.grid_columnconfigure(1, weight=1)
        
        if self.show_grading_scale:
            # Échelle de notation
            grading_frame = ctk.CTkFrame(bottom_frame, fg_color="#F0F9FF", corner_radius=8)
            grading_frame.grid(row=0, column=0, sticky="ew", padx=(0, 6))
            
            grading_title_container = ctk.CTkFrame(grading_frame, fg_color="transparent")
            grading_title_container.pack(padx=10, pady=(8, 4), anchor="w")
            
            grading_icon = self.load_icon("analytics.png", size=(16, 16))
            if grading_icon:
                grading_icon_label = ctk.CTkLabel(grading_title_container, text="", image=grading_icon)
                grading_icon_label.pack(side="left", padx=(0, 6))
            
            ctk.CTkLabel(
                grading_title_container, 
                text="ÉCHELLE DE NOTATION", 
                font=("Segoe UI", 9, "bold"), 
                text_color="#1E40AF"
            ).pack(side="left")
            
            grading_text = """A = 16 - 20 (Excellent)
B = 14 - 15.9 (Très Bien)
C = 12 - 13.9 (Bien)
D = 10 - 11.9 (Assez Bien)
F = 0 - 9.9 (Insuffisant)"""
            
            ctk.CTkLabel(
                grading_frame, 
                text=grading_text, 
                font=("Segoe UI", 9), 
                text_color="#1E40AF",
                justify="left"
            ).pack(padx=10, pady=(0, 8), anchor="w")
        
        if self.show_comment:
            # Commentaire
            comment_frame = ctk.CTkFrame(bottom_frame, fg_color="#F0FDF4", corner_radius=8)
            comment_frame.grid(row=0, column=1, sticky="ew", padx=(6, 0))
            
            comment_title_container = ctk.CTkFrame(comment_frame, fg_color="transparent")
            comment_title_container.pack(padx=10, pady=(8, 4), anchor="w")
            
            comment_icon = self.load_icon("file.png", size=(16, 16))
            if comment_icon:
                comment_icon_label = ctk.CTkLabel(comment_title_container, text="", image=comment_icon)
                comment_icon_label.pack(side="left", padx=(0, 6))
            
            ctk.CTkLabel(
                comment_title_container, 
                text="Commentaire :", 
                font=("Segoe UI", 9, "bold"), 
                text_color="#059669"
            ).pack(side="left")
            
            comment_text = ctk.CTkTextbox(
                comment_frame,
                height=60,
                font=("Segoe UI", 9),
                fg_color="white",
                text_color="#374151",
                border_color="#D1D5DB",
                corner_radius=6
            )
            comment_text.pack(fill="both", expand=True, padx=10, pady=(0, 8))
            comment_text.insert("1.0", self.bulletin_data.get('appreciation', ''))
            comment_text.configure(state="disabled")
    
    def _build_premium_actions(self, parent):
        """Boutons d'action premium"""
        actions_frame = ctk.CTkFrame(parent, fg_color="white")
        actions_frame.grid(row=5, column=0, sticky="ew", padx=10, pady=8)
        actions_frame.grid_columnconfigure(0, weight=1)
        actions_frame.grid_columnconfigure(1, weight=1)
        actions_frame.grid_columnconfigure(2, weight=1)
        
        # Bouton Imprimer
        print_btn = ctk.CTkButton(
            actions_frame,
            text="🖨️ Imprimer",
            font=("Segoe UI", 10, "bold"),
            fg_color="#3B82F6",
            hover_color="#2563EB",
            height=36,
            corner_radius=8,
            command=self._on_print_clicked
        )
        print_btn.grid(row=0, column=0, padx=6, sticky="ew")
        
        # Bouton Exporter
        export_btn = ctk.CTkButton(
            actions_frame,
            text=f"📊 Exporter le bulletin de {self.student_data.get('prenom', '')}",
            font=("Segoe UI", 10, "bold"),
            fg_color="#10B981",
            hover_color="#059669",
            height=36,
            corner_radius=8,
            command=self._on_export_clicked
        )
        export_btn.grid(row=0, column=1, padx=6, sticky="ew")
        
        # Bouton Retour
        back_btn = ctk.CTkButton(
            actions_frame,
            text="← Retour",
            font=("Segoe UI", 10, "bold"),
            fg_color="#6B7280",
            hover_color="#4B5563",
            height=36,
            corner_radius=8,
            command=self._on_back_clicked
        )
        back_btn.grid(row=0, column=2, padx=6, sticky="ew")
    
    def _build_compact_design(self):
        """Design compact pour les vues avec peu d'espace"""
        # Implémentation du design compact
        pass
    
    def _build_simple_design(self):
        """Design simple pour les vues minimalistes"""
        # Implémentation du design simple
        pass
    
    def _on_print_clicked(self):
        """Callback pour l'impression"""
        if hasattr(self, 'on_print'):
            self.on_print(self.student_data, self.bulletin_data)
    
    def _on_export_clicked(self):
        """Callback pour l'export"""
        if hasattr(self, 'on_export'):
            self.on_export(self.student_data, self.bulletin_data)
    
    def _on_back_clicked(self):
        """Callback pour le retour"""
        if hasattr(self, 'on_back'):
            self.on_back()
    
    def update_data(self, student_data=None, bulletin_data=None):
        """Met à jour les données du bulletin"""
        if student_data:
            self.student_data = student_data
        if bulletin_data:
            self.bulletin_data = bulletin_data
        
        # Reconstruire le bulletin
        for widget in self.winfo_children():
            widget.destroy()
        self._build_bulletin()
    
    def set_callbacks(self, on_print=None, on_export=None, on_back=None):
        """Définit les callbacks pour les actions"""
        self.on_print = on_print
        self.on_export = on_export
        self.on_back = on_back










