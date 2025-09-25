import customtkinter as ctk
from tkinter import messagebox, StringVar
import tkinter.font as tkfont
import textwrap
import os
import sys
from PIL import Image

# Importation des contrôleurs pour les matières
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.modules.academic.subjects.controllers.matiere_controller import get_all_matieres, search_matieres, add_matiere, update_matiere, delete_matiere, preload_matieres_cache

# Import du thème global EduManager+
try:
    root_path = os.path.join(os.path.dirname(__file__), '../../../../..')
    sys.path.insert(0, root_path)
    from resources.themes.theme import *
    print("✅ Thème global EduManager+ importé pour les matières")
except ImportError as e:
    print(f"⚠️ Erreur import thème: {e}")
    # Fallback avec constantes locales
    BG_MAIN = "#0A192F"
    CARD_BG = "#0b1d34"
    ACCENT = "#64FFDA"
    TEXT = "#E2E8F0"
    MUTED = "#8aa0b8"
    SUCCESS_GREEN = "#059669"
    ERROR_RED = "#DC2626"
    WARNING_YELLOW = "#D97706"

def load_ctk_icon(icon_name, size=(22, 22)):
    """Charge une icône depuis le pack utilisateurs"""
    try:
        # Chemin absolu vers les icônes depuis la racine du projet
        current_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.join(current_dir, '../../../../..')
        icons_path = os.path.join(project_root, 'resources', 'icons')
        icon_path = os.path.join(icons_path, icon_name)
        
        if os.path.exists(icon_path):
            image = Image.open(icon_path)
            icon = ctk.CTkImage(light_image=image, dark_image=image, size=size)
            return icon
    except Exception as e:
        print(f"⚠️ Erreur chargement icône {icon_name}: {e}")
        return None

class MatieresView(ctk.CTkFrame):
    """Vue des matières avec design EduManager+ magnifique"""

    def __init__(self, parent, icons=None):
        super().__init__(parent, fg_color=BG_MAIN)
        self.grid_columnconfigure(0, weight=1)

        self.var_search = StringVar()
        self._search_after_id = None
        self._matieres_cache = []

        # Précharger le cache pour de meilleures performances
        try:
            preload_matieres_cache()
        except Exception as e:
            print(f"⚠️ Erreur préchargement cache matières: {e}")

        self._build_header()
        self._build_stats_section()
        self._build_cards_area()

        self.charger_matieres()

        # Bindings
        self.var_search.trace_add("write", self._on_search_change)

    def _build_header(self):
        """Header magnifique avec design EduManager+"""
        # Header principal avec espacement légèrement augmenté
        header_frame = ctk.CTkFrame(self, fg_color=BG_SIDEBAR, corner_radius=20, border_width=1, border_color=BORDER_COLOR)
        header_frame.pack(fill="x", padx=12, pady=(12, 6))
        
        # Contenu du header
        header_content = ctk.CTkFrame(header_frame, fg_color="transparent")
        header_content.pack(fill="x", padx=PADDING_CARD, pady=PADDING_CARD)
        
        # Section gauche - Titre et description
        left_section = ctk.CTkFrame(header_content, fg_color="transparent")
        left_section.pack(side="left", fill="x", expand=True)
        
        # Titre avec icône magnifique
        title_container = ctk.CTkFrame(left_section, fg_color="transparent")
        title_container.pack(anchor="w")
        
        # Icône principale sans fond coloré
        main_icon = load_ctk_icon("book.png", (24, 24)) or load_ctk_icon("stacks.png", (24, 24))
        if main_icon:
            ctk.CTkLabel(title_container, text="", image=main_icon, fg_color="transparent").pack(side="left", padx=(0, MARGIN_MEDIUM))
        else:
            ctk.CTkLabel(title_container, text="📚", font=FONT_TITLE, text_color=TEXT_PRIMARY).pack(side="left", padx=(0, MARGIN_MEDIUM))
        
        # Titre magnifique
        title_text = ctk.CTkLabel(title_container, text="Gestion des Matières",
                                 font=FONT_TITLE, text_color=TEXT_PRIMARY)
        title_text.pack(side="left")
        
        # Description élégante
        desc_text = ctk.CTkLabel(left_section, text="Organisez et gérez vos matières scolaires avec style",
                                 font=FONT_SECONDARY, text_color=TEXT_SECONDARY)
        desc_text.pack(anchor="w", pady=(MARGIN_SMALL, 0))
        
        # Section droite - Actions et recherche
        right_section = ctk.CTkFrame(header_content, fg_color="transparent")
        right_section.pack(side="right", fill="y")
        
        # Barre de recherche moderne et élégante
        search_frame = ctk.CTkFrame(right_section, fg_color=CARD_BG, corner_radius=20,
                                  border_width=2, border_color=BORDER_COLOR, height=55)
        search_frame.pack(side="right", padx=(0, MARGIN_MEDIUM))
        
        search_inner = ctk.CTkFrame(search_frame, fg_color="transparent")
        search_inner.pack(fill="both", expand=True, padx=PADDING_MEDIUM, pady=PADDING_MEDIUM)
        
        # Icône de recherche sans fond coloré
        search_icon = load_ctk_icon("search.png", (20, 20))
        if search_icon:
            ctk.CTkLabel(search_inner, text="", image=search_icon, fg_color="transparent").pack(side="left", padx=(0, MARGIN_MEDIUM))
        
        # Champ de recherche amélioré
        self.entry_search = ctk.CTkEntry(search_inner, placeholder_text="Rechercher une matière...",
                                       textvariable=self.var_search, font=FONT_PRIMARY,
                                       fg_color=BG_MAIN, text_color=TEXT_PRIMARY,
                                       border_color=SUCCESS_GREEN, corner_radius=15,
                                       height=45, width=280, border_width=2)
        self.entry_search.pack(side="left", padx=(0, MARGIN_MEDIUM))
        self.entry_search.bind("<Return>", lambda e: self._apply_search())
        self.entry_search.bind("<FocusIn>", lambda e: self.entry_search.configure(border_color=ACCENT))
        self.entry_search.bind("<FocusOut>", lambda e: self.entry_search.configure(border_color=SUCCESS_GREEN))

        # Bouton clear recherche moderne
        clear_icon = load_ctk_icon("close.png", (18, 18))
        clear_btn = ctk.CTkButton(search_inner, text="", image=clear_icon,
                                fg_color="transparent", text_color=TEXT_SECONDARY,
                                hover_color=HOVER_ERROR, command=self._clear_search,
                                corner_radius=12, height=45, width=45,
                                border_width=2, border_color=BORDER_COLOR)
        clear_btn.pack(side="right")

    def _build_stats_section(self):
        """Section statistiques magnifique avec boutons d'action"""
        stats_container = ctk.CTkFrame(self, fg_color="transparent")
        stats_container.pack(fill="x", padx=12, pady=(0, 6))
        
        # Carte statistiques principale
        stats_card = ctk.CTkFrame(stats_container, fg_color=CARD_BG, corner_radius=16,
                                border_width=1, border_color=BORDER_COLOR)
        stats_card.pack(fill="x")
        
        # Contenu des stats
        stats_content = ctk.CTkFrame(stats_card, fg_color="transparent")
        stats_content.pack(fill="x", padx=PADDING_CARD, pady=PADDING_CARD)
        
        # Section gauche - Stats
        stats_left = ctk.CTkFrame(stats_content, fg_color="transparent")
        stats_left.pack(side="left", fill="x", expand=True)
        
        # Icône statistiques sans fond coloré
        stats_icon = load_ctk_icon("stats.png", (24, 24)) or load_ctk_icon("analytics.png", (24, 24))
        if stats_icon:
            ctk.CTkLabel(stats_left, text="", image=stats_icon, fg_color="transparent").pack(side="left", padx=(0, MARGIN_MEDIUM))
        
        # Compteur principal
        self.lbl_count = ctk.CTkLabel(stats_left, text="0 matières",
                                     font=FONT_METRIC, text_color=TEXT_ACCENT)
        self.lbl_count.pack(side="left", padx=(0, MARGIN_LARGE))
        
        # Stats supplémentaires
        self.lbl_stats = ctk.CTkLabel(stats_left, text="Toutes les matières affichées",
                                      font=FONT_SECONDARY, text_color=TEXT_SECONDARY)
        self.lbl_stats.pack(side="left")
        
        # Section droite - Boutons d'action
        stats_right = ctk.CTkFrame(stats_content, fg_color="transparent")
        stats_right.pack(side="right")
        
        # Bouton ajouter avec icône (style transparent comme cours_view)
        add_icon = load_ctk_icon("add.png", (18, 18))
        add_btn = ctk.CTkButton(stats_right, text="Ajouter", image=add_icon, compound="left",
                               font=FONT_BUTTON, fg_color="transparent", text_color=TEXT_PRIMARY,
                               hover_color=HOVER_SUCCESS, command=self.ajouter_matiere,
                               corner_radius=10, height=40, width=100,
                               border_width=2, border_color=BORDER_COLOR)
        add_btn.pack(side="left", padx=MARGIN_SMALL)
        
        # Bouton actualiser avec icône (style transparent comme cours_view)
        refresh_icon = load_ctk_icon("refresh.png", (18, 18))
        refresh_btn = ctk.CTkButton(stats_right, text="Actualiser", image=refresh_icon, compound="left",
                                   font=FONT_BUTTON, fg_color="transparent", text_color=TEXT_PRIMARY,
                                   hover_color=HOVER_PRIMARY, command=self._refresh_all,
                                   corner_radius=10, height=40, width=100,
                                   border_width=2, border_color=BORDER_COLOR)
        refresh_btn.pack(side="left")
        
        # Effet hover sur la carte stats
        def _enter(_):
            stats_card.configure(border_color=ACCENT)
        def _leave(_):
            stats_card.configure(border_color=BORDER_COLOR)
        
        stats_card.bind("<Enter>", _enter)
        stats_card.bind("<Leave>", _leave)

    def _build_cards_area(self):
        """Zone des cartes avec scroll magnifique"""
        self.cards_area = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.cards_area.pack(fill="both", expand=True, padx=8, pady=(0, 8))
        self.cards_area.grid_columnconfigure((0, 1, 2), weight=1, uniform="col")

    def charger_matieres(self, q=""):
        """Charge les matières avec cache"""
        data = search_matieres(q) if q.strip() else get_all_matieres()
        self._matieres_cache = data
        self._render_cards(data)
        self._update_count(len(data))

    def _refresh_all(self):
        """Actualise toutes les données"""
        self.var_search.set("")
        self.charger_matieres()
        self.entry_search.focus_set()

    def _update_count(self, n):
        """Met à jour les statistiques"""
        self.lbl_count.configure(text=f"{n} matière{'s' if n > 1 else ''}")
        
        total_matieres = len(get_all_matieres())
        if n < total_matieres:
            self.lbl_stats.configure(text=f"({total_matieres - n} masquée{'s' if total_matieres - n > 1 else ''} par le filtre)")
        else:
            self.lbl_stats.configure(text="Toutes les matières affichées")

    def _clear_search(self):
        """Efface la recherche"""
        self.var_search.set("")
        self.charger_matieres()
        self.entry_search.focus_set()

    def _apply_search(self):
        """Applique la recherche"""
        self.charger_matieres(self.var_search.get())

    def _on_search_change(self, *_):
        """Gestion du changement de recherche avec debounce"""
        if hasattr(self, "_search_after_id") and self._search_after_id:
            try:
                self.after_cancel(self._search_after_id)
            except:
                pass
        self._search_after_id = self.after(250, self._apply_search)

    def _render_cards(self, matieres):
        """Rend les cartes des matières"""
        for w in self.cards_area.winfo_children():
            w.destroy()

        if not matieres:
            self._render_empty_state()
            return

        for i, m in enumerate(matieres):
            r, c = divmod(i, 3)
            card = self._create_matiere_card(m)
            card.grid(row=r, column=c, sticky="nsew", padx=4, pady=4)

    def _render_empty_state(self):
        """État vide magnifique"""
        empty_frame = ctk.CTkFrame(self.cards_area, fg_color=CARD_BG, corner_radius=20,
                                 border_width=1, border_color=BORDER_COLOR)
        empty_frame.grid(row=0, column=0, padx=12, pady=12, 
                        sticky="nsew", columnspan=3)
        
        # Icône d'état vide sans fond coloré
        empty_icon = load_ctk_icon("folder.png", (64, 64)) or load_ctk_icon("book.png", (64, 64))
        if empty_icon:
            ctk.CTkLabel(empty_frame, text="", image=empty_icon, fg_color="transparent").pack(pady=(MARGIN_HERO, MARGIN_LARGE))
        
        # Titre
        ctk.CTkLabel(empty_frame, text="Aucune matière trouvée",
                     font=FONT_SUBTITLE, text_color=TEXT_PRIMARY).pack(pady=(0, MARGIN_SMALL))
        
        # Description
        ctk.CTkLabel(empty_frame, text="Essayez de modifier votre recherche ou ajoutez une nouvelle matière",
                     font=FONT_SECONDARY, text_color=TEXT_SECONDARY).pack(pady=(0, MARGIN_LARGE))
        
        # Bouton d'ajout (style transparent comme cours_view)
        add_icon = load_ctk_icon("add.png", (20, 20))
        add_btn = ctk.CTkButton(empty_frame, text="Ajouter une matière", image=add_icon, compound="left",
                               font=FONT_BUTTON, fg_color="transparent", text_color=TEXT_PRIMARY,
                               hover_color=HOVER_SUCCESS, command=self.ajouter_matiere,
                               corner_radius=15, height=50, width=200,
                               border_width=2, border_color=BORDER_COLOR)
        add_btn.pack(pady=(0, MARGIN_HERO))

    def _create_matiere_card(self, matieres):
        """Crée une carte de matière magnifique avec design amélioré"""
        # Carte principale avec design moderne amélioré
        card = ctk.CTkFrame(self.cards_area, fg_color=CARD_BG, corner_radius=24,
                          border_width=2, border_color=BORDER_COLOR, height=220)
        card.pack_propagate(False)
        
        # Barre latérale colorée avec gradient
        sidebar = ctk.CTkFrame(card, fg_color=SUCCESS_GREEN, corner_radius=24, width=8)
        sidebar.pack(side="left", fill="y", padx=(0, 0), pady=0)
        
        # Contenu principal avec padding amélioré
        content_frame = ctk.CTkFrame(card, fg_color="transparent")
        content_frame.pack(fill="both", expand=True, padx=PADDING_LARGE, pady=PADDING_LARGE)
        
        # Header de la carte avec design amélioré
        header_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        header_frame.pack(fill="x", pady=(0, MARGIN_LARGE))
        
        # Icône matière sans fond coloré
        matiere_icon = load_ctk_icon("book.png", (28, 28)) or load_ctk_icon("stacks.png", (28, 28))
        if matiere_icon:
            ctk.CTkLabel(header_frame, text="", image=matiere_icon, fg_color="transparent").pack(side="left", padx=(0, MARGIN_LARGE))
        
        # Nom de la matière avec style amélioré
        nom_matiere = matieres.get("nom_matiere", "Sans nom")
        title_label = ctk.CTkLabel(header_frame, text=nom_matiere,
                                 font=FONT_CARD_TITLE, text_color=TEXT_PRIMARY)
        title_label.pack(side="left", fill="x", expand=True)
        
        # Badge avec initiale (couleur différente)
        initiale = (nom_matiere[:1] or "M").upper()
        badge = ctk.CTkFrame(header_frame, fg_color=ERROR_RED, corner_radius=999, width=32, height=32)
        badge.pack_propagate(False)
        badge.pack(side="right")
        ctk.CTkLabel(badge, text=initiale, font=FONT_BUTTON, text_color=TEXT_PRIMARY,
                    fg_color="transparent").pack(expand=True)
        
        # Code matière avec design amélioré
        code_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        code_frame.pack(fill="x", pady=(0, MARGIN_LARGE))
        
        # Icône pour le code
        code_icon = load_ctk_icon("tag.png", (16, 16)) or load_ctk_icon("edit.png", (16, 16))
        if code_icon:
            ctk.CTkLabel(code_frame, text="", image=code_icon).pack(side="left", padx=(0, MARGIN_SMALL))
        
        code_matiere = matieres.get("code_matiere", "") or "Aucun code"
        code_label = ctk.CTkLabel(code_frame, text=f"Code: {code_matiere}",
                                 font=FONT_SECONDARY, text_color=TEXT_SECONDARY)
        code_label.pack(side="left")
        
        # Boutons d'action avec icônes seulement
        actions_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        actions_frame.pack(fill="x", side="bottom")
        
        # Bouton modifier (icône seulement)
        edit_icon = load_ctk_icon("edit.png", (20, 20))
        edit_btn = ctk.CTkButton(actions_frame, text="", image=edit_icon,
                                fg_color="transparent", text_color=TEXT_PRIMARY,
                                hover_color=HOVER_WARNING, command=lambda m=matieres: self.modifier_matiere(m),
                                corner_radius=12, height=40, width=40,
                                border_width=2, border_color=BORDER_COLOR)
        edit_btn.pack(side="left", padx=(0, MARGIN_MEDIUM))
        
        # Bouton supprimer (icône seulement)
        delete_icon = load_ctk_icon("delete.png", (20, 20))
        delete_btn = ctk.CTkButton(actions_frame, text="", image=delete_icon,
                                  fg_color="transparent", text_color=TEXT_PRIMARY,
                                  hover_color=HOVER_ERROR, command=lambda mid=matieres.get("id_matiere"): self.supprimer_matiere(mid),
                                  corner_radius=12, height=40, width=40,
                                  border_width=2, border_color=BORDER_COLOR)
        delete_btn.pack(side="left")
        
        # Effet hover magnifique avec animation
        def _enter(_):
            card.configure(border_color=SUCCESS_GREEN, fg_color=BG_CARD_HOVER)
            sidebar.configure(fg_color=ACCENT)
        def _leave(_):
            card.configure(border_color=BORDER_COLOR, fg_color=CARD_BG)
            sidebar.configure(fg_color=SUCCESS_GREEN)
        
        card.bind("<Enter>", _enter)
        card.bind("<Leave>", _leave)
        for widget in [content_frame, header_frame, code_frame, actions_frame]:
            widget.bind("<Enter>", _enter)
            widget.bind("<Leave>", _leave)

        return card

    def ajouter_matiere(self):
        """Ouvre le formulaire d'ajout"""
        self._open_form_dialog("Ajouter")
    
    def modifier_matiere(self, m):
        """Ouvre le formulaire de modification"""
        self._open_form_dialog("Modifier", m)

    def supprimer_matiere(self, mid):
        """Supprime une matière avec confirmation"""
        if messagebox.askyesno("Confirmation", f"Voulez-vous vraiment supprimer la matière #{mid} ?"):
            if delete_matiere(mid):
                self.charger_matieres(self.var_search.get())
                messagebox.showinfo("Succès", "Matière supprimée avec succès.")
            else:
                messagebox.showerror("Erreur", "La suppression a échoué.")

    def _open_form_dialog(self, mode, data=None):
        """Ouvre le formulaire magnifique"""
        top = ctk.CTkToplevel(self)
        top.title(f"{mode} une Matière")
        top.geometry("600x500")
        top.configure(fg_color=BG_MAIN)
        top.grab_set()
        
        # Centrer la fenêtre
        top.update_idletasks()
        x = (top.winfo_screenwidth() // 2) - (600 // 2)
        y = (top.winfo_screenheight() // 2) - (500 // 2)
        top.geometry(f"600x500+{x}+{y}")
        
        # Container principal
        main_frame = ctk.CTkFrame(top, fg_color=CARD_BG, corner_radius=20,
                                 border_width=1, border_color=BORDER_COLOR)
        main_frame.pack(fill="both", expand=True, padx=PADDING_CARD, pady=PADDING_CARD)
        
        # Header du formulaire
        header_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        header_frame.pack(fill="x", pady=(0, PADDING_LARGE))
        
        # Icône du formulaire sans fond coloré
        form_icon = load_ctk_icon("book.png", (32, 32))
        if form_icon:
            ctk.CTkLabel(header_frame, text="", image=form_icon, fg_color="transparent").pack(side="left", padx=(0, MARGIN_MEDIUM))
        
        # Titre du formulaire
        title_label = ctk.CTkLabel(header_frame, text=f"{mode} une Matière",
                                  font=FONT_TITLE, text_color=TEXT_ACCENT)
        title_label.pack(side="left")
        
        # Formulaire
        form_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        form_frame.pack(fill="both", expand=True)
        
        # Champ nom
        ctk.CTkLabel(form_frame, text="Nom de la matière", font=FONT_BUTTON, text_color=TEXT_PRIMARY).pack(anchor="w", pady=(0, MARGIN_SMALL))
        entry_nom = ctk.CTkEntry(form_frame, placeholder_text="Ex: Mathématiques",
                               font=FONT_PRIMARY, fg_color=BG_MAIN, text_color=TEXT_PRIMARY,
                               border_color=BORDER_COLOR, corner_radius=12, height=45)
        entry_nom.pack(fill="x", pady=(0, PADDING_MEDIUM))
        
        # Champ code
        ctk.CTkLabel(form_frame, text="Code matière", font=FONT_BUTTON, text_color=TEXT_PRIMARY).pack(anchor="w", pady=(0, MARGIN_SMALL))
        entry_code = ctk.CTkEntry(form_frame, placeholder_text="Ex: MATH001",
                                 font=FONT_PRIMARY, fg_color=BG_MAIN, text_color=TEXT_PRIMARY,
                                 border_color=BORDER_COLOR, corner_radius=12, height=45)
        entry_code.pack(fill="x", pady=(0, PADDING_LARGE))
        
        # Pré-remplir si modification
        if mode == "Modifier" and data:
            entry_nom.insert(0, data.get("nom_matiere", ""))
            entry_code.insert(0, data.get("code_matiere", ""))
        
        # Boutons
        buttons_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        buttons_frame.pack(fill="x", side="bottom")
        
        def on_save():
            nom = entry_nom.get().strip()
            code = entry_code.get().strip()
            if not nom:
                messagebox.showerror("Erreur", "Le nom de la matière est obligatoire.", parent=top)
                return
            if len(nom) > 100:
                messagebox.showerror("Erreur", "Nom trop long (max 100).", parent=top)
                return
            
            ok = add_matiere(nom, code) if mode == "Ajouter" else update_matiere(data["id_matiere"], nom, code)
            if ok:
                messagebox.showinfo("Succès", f"Matière {'ajoutée' if mode == 'Ajouter' else 'modifiée'} avec succès.", parent=top)
                self.charger_matieres(self.var_search.get())
                top.destroy()
            else:
                messagebox.showerror("Erreur", f"{mode} impossible. Vérifiez l'unicité du nom.", parent=top)
        
        # Bouton enregistrer (style transparent comme cours_view)
        save_icon = load_ctk_icon("check.png", (18, 18))
        save_btn = ctk.CTkButton(buttons_frame, text="Enregistrer", image=save_icon, compound="left",
                                font=FONT_BUTTON, fg_color="transparent", text_color=TEXT_PRIMARY,
                                hover_color=HOVER_SUCCESS, command=on_save,
                                corner_radius=12, height=45, border_width=2, border_color=BORDER_COLOR)
        save_btn.pack(side="left", fill="x", expand=True, padx=(0, MARGIN_MEDIUM))
        
        # Bouton annuler (style transparent comme cours_view)
        cancel_icon = load_ctk_icon("close.png", (18, 18))
        cancel_btn = ctk.CTkButton(buttons_frame, text="Annuler", image=cancel_icon, compound="left",
                                  font=FONT_BUTTON, fg_color="transparent", text_color=TEXT_PRIMARY,
                                  hover_color=HOVER_PRIMARY, command=top.destroy,
                                  corner_radius=12, height=45, border_width=2, border_color=BORDER_COLOR)
        cancel_btn.pack(side="left", fill="x", expand=True, padx=(MARGIN_MEDIUM, 0))
        
        # Bindings clavier
        top.bind("<Escape>", lambda e: top.destroy())
        top.bind("<Return>", lambda e: on_save())
        top.bind("<Control-s>", lambda e: on_save())
        entry_nom.focus_set()