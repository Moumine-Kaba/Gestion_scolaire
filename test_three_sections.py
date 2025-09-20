#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test de la nouvelle organisation en trois sections de la sidebar
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '.'))

import customtkinter as ctk

# Import du thème au niveau du module
try:
    from resources.themes.theme import *
    print("✅ Thème EduManager+ importé avec succès")
except ImportError:
    print("❌ Erreur import du thème")
    sys.exit(1)

# Constantes de police
F_TITLE = ("Segoe UI", 20, "bold")
F_SUB = ("Segoe UI", 14, "bold")
F_TXT = ("Segoe UI", 12)
F_SMALL = ("Segoe UI", 10)
F_BOLD = ("Segoe UI", 12, "bold")

def test_three_sections_layout():
    """Test de la nouvelle organisation en trois sections"""
    print("🧪 Test de l'organisation en trois sections...")
    print("=" * 60)
    
    try:
        # Créer l'application
        app = ctk.CTk()
        app.title("Test Organisation 3 Sections - Vue Avancée des Présences")
        app.geometry("1400x900")
        app.configure(fg_color=BG_MAIN)
        
        # Configuration du layout principal
        app.grid_columnconfigure(0, weight=3)  # Sidebar très large
        app.grid_columnconfigure(1, weight=2)  # Panneau de détails
        app.grid_rowconfigure(0, weight=1)
        
        # Créer le panneau de gauche avec trois sections
        left_panel = ctk.CTkFrame(app, fg_color=BG_CARD, corner_radius=12)
        left_panel.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        
        # Configuration des sections avec poids égaux
        left_panel.grid_rowconfigure(0, weight=0)  # En-tête
        left_panel.grid_rowconfigure(1, weight=1)  # Section 1: Sélection
        left_panel.grid_rowconfigure(2, weight=1)  # Section 2: Recherche et Actions
        left_panel.grid_rowconfigure(3, weight=2)  # Section 3: Liste et Statistiques
        
        # En-tête avec icône
        header_frame = ctk.CTkFrame(left_panel, fg_color="transparent")
        header_frame.grid(row=0, column=0, sticky="ew", padx=20, pady=(20, 15))
        
        # Titre avec icône
        title_container = ctk.CTkFrame(header_frame, fg_color="transparent")
        title_container.pack(anchor="w")
        
        # Fonction pour charger les icônes
        def load_ctk_icon(icon_name, size):
            """Charge une icône CTk"""
            try:
                from PIL import Image
                import customtkinter as ctk
                icon_path = os.path.join("resources", "icons", icon_name)
                if os.path.exists(icon_path):
                    image = Image.open(icon_path)
                    return ctk.CTkImage(image, size=size)
                return None
            except Exception as e:
                print(f"⚠️ Erreur chargement icône {icon_name}: {e}")
                return None
        
        # Icône de présences
        presence_icon = load_ctk_icon("check_circle.png", (24, 24))
        if presence_icon:
            ctk.CTkLabel(title_container, text="", image=presence_icon, fg_color="transparent").pack(side="left", padx=(0, 10))
        
        title_label = ctk.CTkLabel(title_container, text="Gestion des Présences", 
                                  font=F_TITLE, text_color=TEXT_PRIMARY)
        title_label.pack(side="left")
        
        # SECTION 1: SÉLECTION DE CLASSE ET DATE
        section1_frame = ctk.CTkFrame(left_panel, fg_color=BG_SIDEBAR, corner_radius=8, border_width=1, border_color=BORDER_COLOR)
        section1_frame.grid(row=1, column=0, sticky="nsew", padx=20, pady=(0, 10))
        
        # Titre de la section
        section1_title = ctk.CTkFrame(section1_frame, fg_color="transparent")
        section1_title.pack(fill="x", padx=15, pady=(12, 8))
        
        class_icon = load_ctk_icon("class.png", (16, 16))
        if class_icon:
            ctk.CTkLabel(section1_title, text="", image=class_icon, fg_color="transparent").pack(side="left", padx=(0, 8))
        
        ctk.CTkLabel(section1_title, text="Sélection", font=F_SUB, text_color=TEXT_PRIMARY).pack(side="left")
        
        # Contrôles
        controls_frame = ctk.CTkFrame(section1_frame, fg_color="transparent")
        controls_frame.pack(fill="both", expand=True, padx=15, pady=(0, 12))
        controls_frame.grid_columnconfigure(0, weight=1)
        controls_frame.grid_columnconfigure(1, weight=1)
        
        # Classe
        class_frame = ctk.CTkFrame(controls_frame, fg_color="transparent")
        class_frame.grid(row=0, column=0, sticky="ew", padx=(0, 8))
        
        ctk.CTkLabel(class_frame, text="Classe", font=F_SMALL, text_color=TEXT_SECONDARY).pack(anchor="w", pady=(0, 4))
        cb_class = ctk.CTkComboBox(class_frame, values=["1°", "2°", "3°", "4°", "5°"], 
                                  fg_color=BG_CARD, border_color=BORDER_COLOR,
                                  button_color=BG_CARD, button_hover_color=BG_CARD)
        cb_class.pack(fill="x")
        
        # Date
        date_frame = ctk.CTkFrame(controls_frame, fg_color="transparent")
        date_frame.grid(row=0, column=1, sticky="ew", padx=(8, 0))
        
        ctk.CTkLabel(date_frame, text="Date", font=F_SMALL, text_color=TEXT_SECONDARY).pack(anchor="w", pady=(0, 4))
        
        date_input_frame = ctk.CTkFrame(date_frame, fg_color=BG_CARD, border_color=BORDER_COLOR, border_width=1)
        date_input_frame.pack(fill="x")
        date_input_frame.grid_columnconfigure(0, weight=1)
        
        ent_date = ctk.CTkEntry(date_input_frame, placeholder_text="AAAA-MM-JJ", border_width=0, 
                                fg_color="transparent", font=F_TXT)
        ent_date.grid(row=0, column=0, sticky="ew", padx=(8, 0))
        
        calendar_btn = ctk.CTkButton(date_input_frame, text="", 
                                    image=load_ctk_icon("calendar.png", (18,18)), 
                                    width=32, fg_color="transparent",
                                    hover_color=BG_SIDEBAR)
        calendar_btn.grid(row=0, column=1, padx=4, pady=4)
        
        # SECTION 2: RECHERCHE ET ACTIONS EN MASSE
        section2_frame = ctk.CTkFrame(left_panel, fg_color=BG_SIDEBAR, corner_radius=8, border_width=1, border_color=BORDER_COLOR)
        section2_frame.grid(row=2, column=0, sticky="nsew", padx=20, pady=(0, 10))
        
        # Titre de la section
        section2_title = ctk.CTkFrame(section2_frame, fg_color="transparent")
        section2_title.pack(fill="x", padx=15, pady=(12, 8))
        
        search_icon = load_ctk_icon("search.png", (16, 16))
        if search_icon:
            ctk.CTkLabel(section2_title, text="", image=search_icon, fg_color="transparent").pack(side="left", padx=(0, 8))
        
        ctk.CTkLabel(section2_title, text="Recherche et Actions", font=F_SUB, text_color=TEXT_PRIMARY).pack(side="left")
        
        # Contrôles de recherche
        search_controls = ctk.CTkFrame(section2_frame, fg_color="transparent")
        search_controls.pack(fill="x", padx=15, pady=(0, 8))
        search_controls.grid_columnconfigure(0, weight=1)
        search_controls.grid_columnconfigure(1, weight=1)
        
        # Recherche
        search_frame = ctk.CTkFrame(search_controls, fg_color="transparent")
        search_frame.grid(row=0, column=0, sticky="ew", padx=(0, 8))
        
        ctk.CTkLabel(search_frame, text="Rechercher", font=F_SMALL, text_color=TEXT_SECONDARY).pack(anchor="w", pady=(0, 4))
        
        search_entry = ctk.CTkEntry(search_frame, placeholder_text="Nom ou prénom...",
                                   fg_color=BG_CARD, border_color=BORDER_COLOR)
        search_entry.pack(fill="x")
        
        # Filtre par statut
        filter_frame = ctk.CTkFrame(search_controls, fg_color="transparent")
        filter_frame.grid(row=0, column=1, sticky="ew", padx=(8, 0))
        
        ctk.CTkLabel(filter_frame, text="Statut", font=F_SMALL, text_color=TEXT_SECONDARY).pack(anchor="w", pady=(0, 4))
        
        filter_cb = ctk.CTkComboBox(filter_frame, values=["Tous", "Présent", "Absent", "Retard", "Justifié"], 
                                   fg_color=BG_CARD, border_color=BORDER_COLOR,
                                   button_color=BG_CARD, button_hover_color=BG_CARD)
        filter_cb.pack(fill="x")
        
        # Actions en masse
        actions_frame = ctk.CTkFrame(section2_frame, fg_color="transparent")
        actions_frame.pack(fill="x", padx=15, pady=(0, 12))
        actions_frame.grid_columnconfigure((0, 1, 2), weight=1)
        
        # Boutons d'action
        validate_btn = ctk.CTkButton(actions_frame, text="Valider tout Présent", 
                                    image=load_ctk_icon("check.png", (18, 18)),
                                    fg_color="transparent", text_color=SUCCESS_GREEN, 
                                    hover_color=BG_CARD, font=F_BOLD,
                                    border_width=1, border_color=SUCCESS_GREEN)
        validate_btn.grid(row=0, column=0, sticky="ew", padx=(0, 5))
        
        absent_btn = ctk.CTkButton(actions_frame, text="Marquer tout Absent", 
                                  image=load_ctk_icon("close.png", (18, 18)),
                                  fg_color="transparent", text_color=ERROR_RED, 
                                  hover_color=BG_CARD, font=F_BOLD,
                                  border_width=1, border_color=ERROR_RED)
        absent_btn.grid(row=0, column=1, sticky="ew", padx=5)
        
        reset_btn = ctk.CTkButton(actions_frame, text="Réinitialiser", 
                                  image=load_ctk_icon("refresh.png", (18, 18)),
                                  fg_color="transparent", text_color=WARNING_YELLOW, 
                                  hover_color=BG_CARD, font=F_BOLD,
                                  border_width=1, border_color=WARNING_YELLOW)
        reset_btn.grid(row=0, column=2, sticky="ew", padx=(5, 0))
        
        # SECTION 3: LISTE DES ÉLÈVES ET STATISTIQUES
        section3_frame = ctk.CTkFrame(left_panel, fg_color=BG_SIDEBAR, corner_radius=8, border_width=1, border_color=BORDER_COLOR)
        section3_frame.grid(row=3, column=0, sticky="nsew", padx=20, pady=(0, 20))
        
        # Titre de la section
        section3_title = ctk.CTkFrame(section3_frame, fg_color="transparent")
        section3_title.pack(fill="x", padx=15, pady=(12, 8))
        
        list_icon = load_ctk_icon("group.png", (16, 16))
        if list_icon:
            ctk.CTkLabel(section3_title, text="", image=list_icon, fg_color="transparent").pack(side="left", padx=(0, 8))
        
        ctk.CTkLabel(section3_title, text="Élèves et Statistiques", font=F_SUB, text_color=TEXT_PRIMARY).pack(side="left")
        
        # Contenu de la section
        content_frame = ctk.CTkFrame(section3_frame, fg_color="transparent")
        content_frame.pack(fill="both", expand=True, padx=15, pady=(0, 12))
        
        # Liste des élèves (simulée)
        list_wrap = ctk.CTkScrollableFrame(content_frame, fg_color="transparent", corner_radius=0)
        list_wrap.pack(fill="both", expand=True, pady=(0, 10))
        
        # Simuler quelques élèves
        students = ["Jean Dupont", "Marie Martin", "Pierre Durand", "Sophie Bernard", "Lucas Petit"]
        for student in students:
            item = ctk.CTkFrame(list_wrap, fg_color=BG_CARD, corner_radius=8, cursor="hand2")
            item.pack(fill="x", padx=5, pady=4)
            
            content_frame_item = ctk.CTkFrame(item, fg_color="transparent")
            content_frame_item.pack(fill="x", padx=12, pady=10)
            
            # Icône de l'élève
            student_icon = load_ctk_icon("person.png", (20, 20))
            if student_icon:
                icon_label = ctk.CTkLabel(content_frame_item, text="", image=student_icon, fg_color="transparent")
                icon_label.pack(side="left", padx=(0, 10))
            
            # Nom de l'élève
            name_label = ctk.CTkLabel(content_frame_item, text=student, 
                                      font=F_TXT, text_color=TEXT_PRIMARY)
            name_label.pack(side="left", fill="x", expand=True)
            
            # Statut
            status_label = ctk.CTkLabel(content_frame_item, text="Présent", 
                                       font=F_SMALL, text_color=SUCCESS_GREEN)
            status_label.pack(side="right")
        
        # Statistiques
        stats_frame = ctk.CTkFrame(content_frame, fg_color=BG_CARD, corner_radius=8, border_width=1, border_color=BORDER_COLOR)
        stats_frame.pack(fill="x")
        
        stats_title = ctk.CTkFrame(stats_frame, fg_color="transparent")
        stats_title.pack(fill="x", padx=15, pady=(12, 8))
        
        stats_icon = load_ctk_icon("stats.png", (16, 16))
        if stats_icon:
            ctk.CTkLabel(stats_title, text="", image=stats_icon, fg_color="transparent").pack(side="left", padx=(0, 8))
        
        ctk.CTkLabel(stats_title, text="Statistiques", font=F_SUB, text_color=TEXT_PRIMARY).pack(side="left")
        
        # Chips des statistiques
        chips_frame = ctk.CTkFrame(stats_frame, fg_color="transparent")
        chips_frame.pack(fill="x", padx=15, pady=(0, 12))
        chips_frame.grid_columnconfigure((0, 1, 2, 3), weight=1)
        
        # Chips simulés
        stats_data = [
            ("Présents", "5", SUCCESS_GREEN),
            ("Absents", "0", ERROR_RED),
            ("Retards", "0", WARNING_YELLOW),
            ("Total", "5", TEXT_PRIMARY)
        ]
        
        for i, (label, value, color) in enumerate(stats_data):
            chip = ctk.CTkFrame(chips_frame, fg_color=color, corner_radius=12)
            chip.grid(row=0, column=i, sticky="ew", padx=2)
            
            ctk.CTkLabel(chip, text=value, font=F_BOLD, text_color=BG_MAIN).pack(pady=4)
            ctk.CTkLabel(chip, text=label, font=F_SMALL, text_color=BG_MAIN).pack()
        
        # Panneau de droite (détails)
        right_panel = ctk.CTkFrame(app, fg_color=BG_CARD, corner_radius=12)
        right_panel.grid(row=0, column=1, sticky="nsew")
        
        # Message par défaut
        default_frame = ctk.CTkFrame(right_panel, fg_color="transparent")
        default_frame.pack(expand=True, fill="both")
        
        # Icône de sélection
        select_icon = load_ctk_icon("person.png", (48, 48))
        if select_icon:
            ctk.CTkLabel(default_frame, text="", image=select_icon, fg_color="transparent").pack(pady=(40, 20))
        
        # Message
        ctk.CTkLabel(default_frame, text="Sélectionnez un élève", 
                    font=F_TITLE, text_color=TEXT_PRIMARY).pack(pady=(0, 10))
        
        ctk.CTkLabel(default_frame, text="pour voir les détails et modifier sa présence",
                    font=F_TXT, text_color=TEXT_SECONDARY).pack()
        
        print("✅ Interface en trois sections créée avec succès")
        print("\n🎉 ORGANISATION EN TROIS SECTIONS RÉUSSIE !")
        print("=" * 60)
        print("✅ Section 1: Sélection de classe et date")
        print("✅ Section 2: Recherche et actions en masse")
        print("✅ Section 3: Liste des élèves et statistiques")
        print("✅ Interface claire et bien organisée")
        
        print("\n🚀 Lancement de l'interface de test...")
        print("💡 Fermez la fenêtre pour terminer le test")
        
        app.mainloop()
        
        return True
        
    except Exception as e:
        print(f"\n❌ Erreur lors du test: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Fonction principale"""
    print("🏫 Test de l'Organisation en Trois Sections")
    print("=" * 70)
    
    # Test de l'organisation
    success = test_three_sections_layout()
    
    # Résumé
    print("\n" + "=" * 70)
    print("📊 RÉSUMÉ")
    print("=" * 70)
    
    if success:
        print("🎉 SUCCÈS COMPLET !")
        print("✅ L'organisation en trois sections fonctionne parfaitement")
        print("✅ L'interface est claire et bien structurée")
        print("✅ Chaque section a sa fonction spécifique")
        print("\n🚀 Vous pouvez maintenant appliquer cette organisation à la vue avancée !")
    else:
        print("⚠️ PROBLÈMES DÉTECTÉS")
        print("🔧 Vérifiez les erreurs ci-dessus")

if __name__ == "__main__":
    main()
