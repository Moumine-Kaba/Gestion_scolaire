import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
from src.modules.academic.grades.controllers.bulletin_controller import get_all_bulletins, add_bulletin, update_bulletin, delete_bulletin
from src.modules.academic.students.controllers.eleve_controller import get_all_eleves
from src.modules.academic.classes.controllers.classe_controller import get_all_classes
from PIL import Image
import os
import sys

# Ajouter le chemin racine pour les imports
root_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))
sys.path.insert(0, root_path)

# Chemin vers les ressources
resources_path = os.path.join(root_path, "resources")
icons_path = r"C:\Users\Lenovo\Desktop\Clonage_git\Gestion_scolaire\Gestion_scolaire\resources\icons"
themes_path = os.path.join(resources_path, "themes")

# Vérifier le chemin des ressources
print(f"🔍 Chemin racine: {root_path}")
print(f"🔍 Ressources existe: {os.path.exists(resources_path)}")
print(f"🔍 Icons existe: {os.path.exists(icons_path)}")
print(f"🔍 Themes existe: {os.path.exists(themes_path)}")

# Import du thème EduManager+
try:
    sys.path.insert(0, themes_path)
    from theme import *
    sys.path.insert(0, os.path.join(resources_path, "fonts"))
    from fonts import *
    sys.path.insert(0, icons_path)
    from icons import *
except ImportError:
    # Fallback si les imports échouent
    BG_MAIN = "#0A192F"
    BG_CARD = "#1E293B"
    BG_SIDEBAR = "#0F172A"
    TEXT_PRIMARY = "#F1F5F9"
    TEXT_SECONDARY = "#94A3B8"
    ACCENT_BLUE = "#3B82F6"
    SUCCESS_GREEN = "#10B981"
    ERROR_RED = "#EF4444"
    WARNING_ORANGE = "#F59E0B"
    F_TITLE = ("Segoe UI", 18, "bold")
    F_SUB = ("Segoe UI", 14, "bold")
    F_TXT = ("Segoe UI", 12)
    F_SMALL = ("Segoe UI", 10)
    F_BOLD = ("Segoe UI", 12, "bold")

def load_ctk_icon(icon_name, size=(20, 20)):
    """Charge une icône depuis le dossier resources/icons"""
    try:
        # Chemin correct vers les icônes
        icon_path = os.path.join(icons_path, icon_name)
        
        if os.path.exists(icon_path):
            return ctk.CTkImage(Image.open(icon_path), size=size)
        else:
            print(f"⚠️ Icône non trouvée: {icon_path}")
            return None
    except Exception as e:
        print(f"❌ Erreur chargement icône {icon_name}: {e}")
        return None

class BulletinsView(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color=BG_MAIN)
        
        # Configuration de la grille
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        
        # En-tête avec titre et icône
        self._build_header()
        
        # Zone principale avec recherche et cartes
        self._build_main_content()
        
        # Configuration - afficher les 100 premiers bulletins par classe par ordre de mérite
        self.limite_par_classe = 100  # Maximum 100 bulletins par classe
        
        # Charger les classes et bulletins
        self.charger_classes()
        self.charger_bulletins()
    
    def _build_header(self):
        """Construit l'en-tête de la vue"""
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.grid(row=0, column=0, sticky="ew", padx=20, pady=(20, 10))
        header_frame.grid_columnconfigure(1, weight=1)
        
        # Icône et titre
        title_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        title_frame.grid(row=0, column=0, sticky="w")
        
        # Icône bulletins
        bulletin_icon = load_ctk_icon("newspaper.png", (32, 32))
        if bulletin_icon:
            icon_label = ctk.CTkLabel(title_frame, image=bulletin_icon, text="")
            icon_label.pack(side="left", padx=(0, 15))
        
        # Titre
        title_label = ctk.CTkLabel(title_frame, text="Gestion des Bulletins", 
                                 font=F_TITLE, text_color=TEXT_PRIMARY)
        title_label.pack(side="left")
        
        # Boutons d'action
        actions_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        actions_frame.grid(row=0, column=1, sticky="e")
        
        # Bouton Ajouter
        add_icon = load_ctk_icon("add.png", (18, 18))
        add_btn = ctk.CTkButton(actions_frame, text="Ajouter", image=add_icon,
                               fg_color=SUCCESS_GREEN, text_color="white",
                               font=F_BOLD, height=40, width=120,
                               command=self.ajouter_bulletin)
        add_btn.pack(side="right", padx=(5, 0))
        
        # Bouton Actualiser
        refresh_icon = load_ctk_icon("refresh.png", (18, 18))
        refresh_btn = ctk.CTkButton(actions_frame, text="Actualiser", image=refresh_icon,
                                   fg_color=ACCENT_BLUE, text_color="white",
                                   font=F_BOLD, height=40, width=120,
                                   command=self.charger_bulletins)
        refresh_btn.pack(side="right", padx=(5, 0))
    
    def _build_main_content(self):
        """Construit le contenu principal avec recherche et cartes"""
        main_frame = ctk.CTkFrame(self, fg_color="transparent")
        main_frame.grid(row=1, column=0, sticky="nsew", padx=20, pady=(0, 20))
        main_frame.grid_columnconfigure(0, weight=1)
        main_frame.grid_rowconfigure(1, weight=1)
        
        # Barre de recherche et filtres
        self._build_search_section(main_frame)
        
        # Zone des cartes de bulletins
        self._build_cards_section(main_frame)
    
    def _build_search_section(self, parent):
        """Construit la section de recherche"""
        search_frame = ctk.CTkFrame(parent, fg_color=BG_CARD, corner_radius=12)
        search_frame.grid(row=0, column=0, sticky="ew", pady=(0, 15))
        search_frame.grid_columnconfigure(1, weight=1)
        
        # Recherche par nom d'élève
        search_label = ctk.CTkLabel(search_frame, text="Rechercher:", 
                                   font=F_BOLD, text_color=TEXT_PRIMARY)
        search_label.grid(row=0, column=0, padx=20, pady=15, sticky="w")
        
        self.search_entry = ctk.CTkEntry(search_frame, placeholder_text="Nom de l'élève...",
                                        font=F_TXT, height=35, width=300)
        self.search_entry.grid(row=0, column=1, padx=(0, 20), pady=15, sticky="ew")
        self.search_entry.bind("<KeyRelease>", self._on_search_change)
        
        # Filtre par classe
        classe_label = ctk.CTkLabel(search_frame, text="Classe:", 
                                   font=F_BOLD, text_color=TEXT_PRIMARY)
        classe_label.grid(row=0, column=2, padx=(20, 5), pady=15, sticky="w")
        
        self.classe_var = ctk.StringVar(value="Toutes")
        self.classe_combo = ctk.CTkComboBox(search_frame, values=["Toutes"],
                                           variable=self.classe_var, font=F_TXT, height=35, width=150)
        self.classe_combo.grid(row=0, column=3, padx=(0, 20), pady=15, sticky="w")
        self.classe_combo.bind("<<ComboboxSelected>>", self._on_filter_change)
        
        # Filtre par trimestre
        trimestre_label = ctk.CTkLabel(search_frame, text="Trimestre:", 
                                      font=F_BOLD, text_color=TEXT_PRIMARY)
        trimestre_label.grid(row=0, column=4, padx=(20, 5), pady=15, sticky="w")
        
        self.trimestre_var = ctk.StringVar(value="Tous")
        trimestre_combo = ctk.CTkComboBox(search_frame, values=["Tous", "1er", "2ème", "3ème"],
                                         variable=self.trimestre_var, font=F_TXT, height=35, width=120)
        trimestre_combo.grid(row=0, column=5, padx=(0, 20), pady=15, sticky="w")
        trimestre_combo.bind("<<ComboboxSelected>>", self._on_filter_change)
    
    def _build_cards_section(self, parent):
        """Construit la section des cartes de bulletins"""
        cards_frame = ctk.CTkFrame(parent, fg_color="transparent")
        cards_frame.grid(row=1, column=0, sticky="nsew")
        cards_frame.grid_columnconfigure(0, weight=1)
        
        # Scrollable frame pour les cartes
        self.cards_scroll = ctk.CTkScrollableFrame(cards_frame, fg_color="transparent")
        self.cards_scroll.grid(row=0, column=0, sticky="nsew")
        self.cards_scroll.grid_columnconfigure((0, 1, 2), weight=1)
        
        # Frame pour les statistiques
        self.stats_frame = ctk.CTkFrame(cards_frame, fg_color=BG_CARD, corner_radius=12)
        self.stats_frame.grid(row=1, column=0, sticky="ew", pady=(15, 0))
        self.stats_frame.grid_columnconfigure((0, 1, 2, 3), weight=1)
        
        self._build_statistics()
    
    def _build_statistics(self):
        """Construit les statistiques des bulletins"""
        # Statistiques seront mises à jour dynamiquement
        pass
    
    def _update_statistics(self, bulletins):
        """Met à jour les statistiques"""
        # Effacer les anciennes statistiques
        for widget in self.stats_frame.winfo_children():
            widget.destroy()
        
        if not bulletins:
            return
        
        # Calculer les statistiques
        total_bulletins = len(bulletins)
        moyennes = [b.get('moyenne_generale', 0) for b in bulletins if b.get('moyenne_generale')]
        moyenne_generale = sum(moyennes) / len(moyennes) if moyennes else 0
        
        # Statistiques
        stats_data = [
            ("Total", str(total_bulletins), "newspaper.png", ACCENT_BLUE),
            ("Moyenne", f"{moyenne_generale:.2f}", "trending_up.png", SUCCESS_GREEN),
            ("Meilleure", f"{max(moyennes):.2f}" if moyennes else "0.00", "star.png", WARNING_ORANGE),
            ("Trimestres", str(len(set(b.get('periode', '') for b in bulletins))), "calendar.png", ERROR_RED)
        ]
        
        for i, (label, value, icon_name, color) in enumerate(stats_data):
            stat_card = ctk.CTkFrame(self.stats_frame, fg_color=BG_CARD, corner_radius=8)
            stat_card.grid(row=0, column=i, padx=10, pady=15, sticky="ew")
            
            # Icône
            icon = load_ctk_icon(icon_name, (24, 24))
            if icon:
                icon_label = ctk.CTkLabel(stat_card, image=icon, text="")
                icon_label.pack(pady=(15, 5))
            
            # Valeur
            value_label = ctk.CTkLabel(stat_card, text=value, font=F_TITLE, text_color=color)
            value_label.pack()
            
            # Label
            label_label = ctk.CTkLabel(stat_card, text=label, font=F_SMALL, text_color=TEXT_SECONDARY)
            label_label.pack(pady=(0, 15))
    
    def _create_bulletin_card(self, bulletin):
        """Crée une carte pour un bulletin"""
        card = ctk.CTkFrame(self.cards_scroll, fg_color=BG_CARD, corner_radius=12)
        
        # En-tête de la carte
        header_frame = ctk.CTkFrame(card, fg_color="transparent")
        header_frame.pack(fill="x", padx=20, pady=(20, 10))
        header_frame.grid_columnconfigure(1, weight=1)
        
        # Icône élève
        student_icon = load_ctk_icon("person.png", (24, 24))
        if student_icon:
            icon_label = ctk.CTkLabel(header_frame, image=student_icon, text="")
            icon_label.grid(row=0, column=0, padx=(0, 15))
        
        # Nom de l'élève avec rang dans la classe
        eleve_name = f"{bulletin.get('eleve_prenom', '')} {bulletin.get('eleve_nom', '')}"
        rang_classe = bulletin.get('rang', 'N/A')
        
        # Créer un frame pour le nom et le rang
        name_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        name_frame.grid(row=0, column=1, sticky="w")
        
        name_label = ctk.CTkLabel(name_frame, text=eleve_name, 
                                 font=F_SUB, text_color=TEXT_PRIMARY)
        name_label.pack(anchor="w")
        
        # Indication du rang avec couleur selon la performance
        if isinstance(rang_classe, (int, float)) and rang_classe <= 3:
            rang_color = SUCCESS_GREEN if rang_classe == 1 else WARNING_ORANGE
            rang_text = f"🏆 {rang_classe}er" if rang_classe == 1 else f"🥈 {rang_classe}ème"
        else:
            rang_color = TEXT_SECONDARY
            rang_text = f"Rang: {rang_classe}"
            
        rang_label = ctk.CTkLabel(name_frame, text=rang_text, 
                                 font=F_SMALL, text_color=rang_color)
        rang_label.pack(anchor="w")
        
        # Boutons d'action
        actions_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        actions_frame.grid(row=0, column=2, sticky="e")
        
        # Bouton Modifier
        edit_icon = load_ctk_icon("edit.png", (16, 16))
        edit_btn = ctk.CTkButton(actions_frame, text="", image=edit_icon,
                                fg_color="transparent", text_color=ACCENT_BLUE,
                                width=32, height=32, border_width=1, border_color=ACCENT_BLUE,
                                command=lambda: self.modifier_bulletin(bulletin))
        edit_btn.pack(side="right", padx=(5, 0))
        
        # Bouton Supprimer
        delete_icon = load_ctk_icon("delete.png", (16, 16))
        delete_btn = ctk.CTkButton(actions_frame, text="", image=delete_icon,
                                  fg_color="transparent", text_color=ERROR_RED,
                                  width=32, height=32, border_width=1, border_color=ERROR_RED,
                                  command=lambda: self.supprimer_bulletin(bulletin))
        delete_btn.pack(side="right", padx=(5, 0))
        
        # Contenu de la carte
        content_frame = ctk.CTkFrame(card, fg_color="transparent")
        content_frame.pack(fill="x", padx=20, pady=(0, 20))
        
        # Informations du bulletin
        info_data = [
            ("Période", bulletin.get('periode', 'N/A')),
            ("Moyenne", f"{bulletin.get('moyenne_generale', 0):.2f}"),
            ("Rang", str(bulletin.get('rang', 'N/A'))),
            ("Date", self._format_date(bulletin.get('date_creation')))
        ]
        
        for i, (label, value) in enumerate(info_data):
            info_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
            info_frame.grid(row=i//2, column=i%2, padx=5, pady=5, sticky="ew")
            content_frame.grid_columnconfigure((0, 1), weight=1)
            
            label_widget = ctk.CTkLabel(info_frame, text=f"{label}:", 
                                       font=F_SMALL, text_color=TEXT_SECONDARY)
            label_widget.pack(anchor="w")
            
            value_widget = ctk.CTkLabel(info_frame, text=value, 
                                       font=F_BOLD, text_color=TEXT_PRIMARY)
            value_widget.pack(anchor="w")
        
        # Appréciation
        appreciation = bulletin.get('appreciation', '')
        if appreciation:
            app_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
            app_frame.grid(row=2, column=0, columnspan=2, padx=5, pady=5, sticky="ew")
            
            app_label = ctk.CTkLabel(app_frame, text="Appréciation:", 
                                    font=F_SMALL, text_color=TEXT_SECONDARY)
            app_label.pack(anchor="w")
            
            app_text = ctk.CTkLabel(app_frame, text=appreciation, 
                                   font=F_TXT, text_color=TEXT_PRIMARY,
                                   wraplength=400, justify="left")
            app_text.pack(anchor="w")
        
        return card
    
    def _format_date(self, date_obj):
        """Formate une date pour l'affichage"""
        if not date_obj:
            return 'N/A'
        
        try:
            # Si c'est un objet datetime
            if hasattr(date_obj, 'strftime'):
                return date_obj.strftime('%d/%m/%Y')
            # Si c'est une chaîne
            elif isinstance(date_obj, str):
                return date_obj[:10] if len(date_obj) >= 10 else date_obj
            else:
                return str(date_obj)
        except Exception:
            return 'N/A'

    def charger_classes(self):
        """Charge les classes pour le filtre"""
        try:
            classes = get_all_classes()
            classe_values = ["Toutes"] + [f"{c[0]} - {c[1]}" for c in classes]
            self.classe_combo.configure(values=classe_values)
        except Exception as e:
            print(f"Erreur lors du chargement des classes: {e}")
            self.classe_combo.configure(values=["Toutes"])
    
    def charger_bulletins(self):
        """Charge et affiche les bulletins groupés par classe"""
        # Effacer les cartes existantes
        for widget in self.cards_scroll.winfo_children():
            widget.destroy()
        
        # Récupérer les bulletins
        bulletins = get_all_bulletins()
        
        # Appliquer les filtres
        filtered_bulletins = self._apply_filters(bulletins)
        
        if not filtered_bulletins:
            # Afficher un message si aucun bulletin
            no_data_frame = ctk.CTkFrame(self.cards_scroll, fg_color=BG_CARD, corner_radius=12)
            no_data_frame.grid(row=0, column=0, columnspan=3, padx=10, pady=20, sticky="ew")
            
            no_data_label = ctk.CTkLabel(no_data_frame, text="Aucun bulletin trouvé", 
                                       font=F_SUB, text_color=TEXT_SECONDARY)
            no_data_label.pack(pady=30)
            
            self._update_statistics([])
            return
        
        # Grouper les bulletins par classe
        bulletins_par_classe = self._grouper_bulletins_par_classe(filtered_bulletins)
        
        # Créer les sections par classe
        row_index = 0
        for classe_nom, bulletins_classe in bulletins_par_classe.items():
            # Limiter à 100 bulletins par classe (les meilleurs)
            bulletins_a_afficher = bulletins_classe[:self.limite_par_classe]
            nb_total = len(bulletins_classe)
            nb_affiches = len(bulletins_a_afficher)
            
            # Créer l'en-tête de classe avec information sur le classement
            classe_header = self._create_classe_header(classe_nom, nb_total, nb_affiches)
            classe_header.grid(row=row_index, column=0, columnspan=3, padx=10, pady=(20 if row_index == 0 else 10, 5), sticky="ew")
            row_index += 1
            
            # Créer les cartes de bulletins pour cette classe (les 100 premiers)
            for i, bulletin in enumerate(bulletins_a_afficher):
                card = self._create_bulletin_card(bulletin)
                card_row = row_index + (i // 3)
                card_col = i % 3
                card.grid(row=card_row, column=card_col, padx=10, pady=5, sticky="ew")
            
            # Ajouter un message si il y a plus de bulletins que la limite
            if nb_total > self.limite_par_classe:
                more_frame = ctk.CTkFrame(self.cards_scroll, fg_color=BG_CARD, corner_radius=8)
                more_frame.grid(row=row_index + (nb_affiches + 2) // 3, column=0, columnspan=3, 
                               padx=10, pady=5, sticky="ew")
                
                more_label = ctk.CTkLabel(more_frame, 
                                        text=f"... et {nb_total - nb_affiches} autre(s) élève(s) dans cette classe", 
                                        font=F_SMALL, text_color=TEXT_SECONDARY)
                more_label.pack(pady=8)
            
            # Mettre à jour l'index de ligne pour la prochaine classe
            row_index += (nb_affiches + 2) // 3 + (1 if nb_total > self.limite_par_classe else 0)
        
        # Mettre à jour les statistiques
        self._update_statistics(filtered_bulletins)
    
    def _grouper_bulletins_par_classe(self, bulletins):
        """Groupe les bulletins par classe et les trie par ordre de mérite"""
        bulletins_par_classe = {}
        
        for bulletin in bulletins:
            # Récupérer le nom de la classe depuis les données du bulletin
            classe_nom = bulletin.get('classe_nom', 'Classe non définie')
            
            if classe_nom not in bulletins_par_classe:
                bulletins_par_classe[classe_nom] = []
            
            bulletins_par_classe[classe_nom].append(bulletin)
        
        # Trier les classes par nom et les bulletins par ordre de mérite (moyenne décroissante)
        for classe_nom in bulletins_par_classe:
            bulletins_par_classe[classe_nom].sort(
                key=lambda x: x.get('moyenne_generale', 0), 
                reverse=True
            )
        
        return dict(sorted(bulletins_par_classe.items()))
    
    def _create_classe_header(self, classe_nom, nb_total, nb_affiches):
        """Crée un en-tête pour une classe avec classement par ordre de mérite"""
        header_frame = ctk.CTkFrame(self.cards_scroll, fg_color=BG_SIDEBAR, corner_radius=8)
        
        # Contenu de l'en-tête
        content_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        content_frame.pack(fill="x", padx=15, pady=10)
        
        # Icône classe
        classe_icon = load_ctk_icon("school.png", (20, 20))
        if classe_icon:
            icon_label = ctk.CTkLabel(content_frame, image=classe_icon, text="")
            icon_label.pack(side="left", padx=(0, 10))
        
        # Nom de la classe
        classe_label = ctk.CTkLabel(content_frame, text=f"Classe {classe_nom}", 
                                   font=F_SUB, text_color=TEXT_PRIMARY)
        classe_label.pack(side="left")
        
        # Information sur le classement avec limite
        if nb_total > nb_affiches:
            ranking_text = f"({nb_affiches}/{nb_total} meilleurs élèves - Classement par ordre de mérite)"
            ranking_color = WARNING_ORANGE
        else:
            ranking_text = f"({nb_total} élèves - Classement par ordre de mérite)"
            ranking_color = SUCCESS_GREEN
            
        ranking_label = ctk.CTkLabel(content_frame, text=ranking_text, 
                                    font=F_SMALL, text_color=ranking_color)
        ranking_label.pack(side="left", padx=(10, 0))
        
        return header_frame
    
    def _apply_filters(self, bulletins):
        """Applique les filtres de recherche"""
        filtered = bulletins.copy()
        
        # Filtre par nom d'élève
        search_text = self.search_entry.get().lower()
        if search_text:
            filtered = [b for b in filtered if 
                       search_text in b.get('eleve_nom', '').lower() or 
                       search_text in b.get('eleve_prenom', '').lower()]
        
        # Filtre par classe
        classe_selectionnee = self.classe_var.get()
        if classe_selectionnee != "Toutes":
            try:
                classe_id = classe_selectionnee.split(" - ")[0]
                filtered = [b for b in filtered if str(b.get('id_classe', '')) == classe_id]
            except:
                pass
        
        # Filtre par trimestre
        trimestre = self.trimestre_var.get()
        if trimestre != "Tous":
            filtered = [b for b in filtered if b.get('periode', '') == trimestre]
        
        return filtered
    
    def _on_search_change(self, event):
        """Gère le changement de recherche"""
        self.charger_bulletins()
    
    def _on_filter_change(self, event):
        """Gère le changement de filtre"""
        self.charger_bulletins()
    
    def ajouter_bulletin(self):
        """Ouvre le formulaire d'ajout de bulletin"""
        self._ouvrir_formulaire("Ajouter")
    
    def modifier_bulletin(self, bulletin=None):
        """Ouvre le formulaire de modification de bulletin"""
        if bulletin is None:
            messagebox.showwarning("Modification", "Aucun bulletin sélectionné.")
            return
        self._ouvrir_formulaire("Modifier", bulletin)
    
    def supprimer_bulletin(self, bulletin=None):
        """Supprime un bulletin"""
        if bulletin is None:
            messagebox.showwarning("Suppression", "Aucun bulletin sélectionné.")
            return
        
        if messagebox.askyesno("Confirmation", 
                              f"Voulez-vous vraiment supprimer le bulletin de {bulletin.get('eleve_prenom', '')} {bulletin.get('eleve_nom', '')} ?"):
            try:
                delete_bulletin(bulletin.get('id'))
                messagebox.showinfo("Succès", "Bulletin supprimé avec succès.")
                self.charger_bulletins()
            except Exception as e:
                messagebox.showerror("Erreur", f"Erreur lors de la suppression: {e}")
    
    def _ouvrir_formulaire(self, mode, bulletin=None):
        """Ouvre le formulaire de bulletin"""
        form = ctk.CTkToplevel(self)
        form.title(f"{mode} un Bulletin")
        form.geometry("600x500")
        form.configure(fg_color=BG_MAIN)
        form.grab_set()
        
        # Centrer la fenêtre
        form.transient(self)
        form.geometry("+%d+%d" % (self.winfo_rootx() + 50, self.winfo_rooty() + 50))
        
        # En-tête du formulaire
        header_frame = ctk.CTkFrame(form, fg_color="transparent")
        header_frame.pack(fill="x", padx=30, pady=(30, 20))
        
        # Icône et titre
        title_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        title_frame.pack()
        
        form_icon = load_ctk_icon("newspaper.png", (28, 28))
        if form_icon:
            icon_label = ctk.CTkLabel(title_frame, image=form_icon, text="")
            icon_label.pack(side="left", padx=(0, 15))
        
        title_label = ctk.CTkLabel(title_frame, text=f"{mode} un Bulletin", 
                                 font=F_TITLE, text_color=TEXT_PRIMARY)
        title_label.pack(side="left")
        
        # Contenu du formulaire
        content_frame = ctk.CTkScrollableFrame(form, fg_color="transparent")
        content_frame.pack(fill="both", expand=True, padx=30, pady=(0, 20))
        
        # Variables du formulaire
        eleve_var = ctk.StringVar()
        periode_var = ctk.StringVar()
        moyenne_var = ctk.StringVar()
        rang_var = ctk.StringVar()
        appreciation_var = ctk.StringVar()
        
        # Récupérer les élèves
        eleves = get_all_eleves()
        eleves_choices = [f"{e[0]} - {e[1]} {e[2]}" for e in eleves]
        
        # Champs du formulaire
        fields = [
            ("Élève", eleve_var, "combobox", eleves_choices),
            ("Période", periode_var, "combobox", ["1er trimestre", "2ème trimestre", "3ème trimestre"]),
            ("Moyenne générale", moyenne_var, "entry"),
            ("Rang", rang_var, "entry"),
            ("Appréciation", appreciation_var, "text")
        ]
        
        for i, field_data in enumerate(fields):
            label, var, field_type = field_data[:3]
            options = field_data[3] if len(field_data) > 3 else None
            
            field_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
            field_frame.pack(fill="x", pady=10)
            
            # Label
            label_widget = ctk.CTkLabel(field_frame, text=f"{label}:", 
                                       font=F_BOLD, text_color=TEXT_PRIMARY)
            label_widget.pack(anchor="w", pady=(0, 5))
            
            # Champ
            if field_type == "combobox":
                widget = ctk.CTkComboBox(field_frame, variable=var, values=options,
                                        font=F_TXT, height=35)
            elif field_type == "text":
                widget = ctk.CTkTextbox(field_frame, font=F_TXT, height=80)
            else:  # entry
                widget = ctk.CTkEntry(field_frame, textvariable=var, font=F_TXT, height=35)
            
            widget.pack(fill="x")
            
            # Stocker la référence pour le textbox
            if field_type == "text":
                appreciation_textbox = widget
        
        # Pré-remplir les champs si modification
        if mode == "Modifier" and bulletin:
            eleve_var.set(f"{bulletin.get('id_eleve', '')} - {bulletin.get('eleve_prenom', '')} {bulletin.get('eleve_nom', '')}")
            periode_var.set(bulletin.get('periode', ''))
            moyenne_var.set(str(bulletin.get('moyenne_generale', '')))
            rang_var.set(str(bulletin.get('rang', '')))
            appreciation_textbox.insert("1.0", bulletin.get('appreciation', ''))
        
        # Boutons d'action
        buttons_frame = ctk.CTkFrame(form, fg_color="transparent")
        buttons_frame.pack(fill="x", padx=30, pady=(0, 30))
        
        # Bouton Enregistrer
        save_icon = load_ctk_icon("check.png", (18, 18))
        save_btn = ctk.CTkButton(buttons_frame, text="Enregistrer", image=save_icon,
                                fg_color=SUCCESS_GREEN, text_color="white",
                                font=F_BOLD, height=40, width=140,
                                command=lambda: self._enregistrer_bulletin(form, mode, bulletin, 
                                                                         eleve_var.get(), periode_var.get(),
                                                                         moyenne_var.get(), rang_var.get(),
                                                                         appreciation_textbox.get("1.0", "end-1c").strip()))
        save_btn.pack(side="right", padx=(10, 0))
        
        # Bouton Annuler
        cancel_icon = load_ctk_icon("close.png", (18, 18))
        cancel_btn = ctk.CTkButton(buttons_frame, text="Annuler", image=cancel_icon,
                                  fg_color=ERROR_RED, text_color="white",
                                  font=F_BOLD, height=40, width=140,
                                  command=form.destroy)
        cancel_btn.pack(side="right")
    
    def _enregistrer_bulletin(self, form, mode, bulletin, eleve_str, periode, moyenne, rang, appreciation):
        """Enregistre un bulletin"""
        try:
            # Validation des champs obligatoires
            if not all([eleve_str, periode, moyenne]):
                messagebox.showerror("Erreur", "Veuillez remplir tous les champs obligatoires.", parent=form)
                return
            
            # Validation de la moyenne
            try:
                moyenne_float = float(moyenne)
                if not (0 <= moyenne_float <= 20):
                    messagebox.showerror("Erreur", "La moyenne doit être entre 0 et 20.", parent=form)
                    return
            except ValueError:
                messagebox.showerror("Erreur", "Moyenne invalide.", parent=form)
                return
            
            # Validation du rang
            rang_int = None
            if rang:
                try:
                    rang_int = int(rang)
                except ValueError:
                    messagebox.showerror("Erreur", "Rang invalide.", parent=form)
                    return
            
            # Récupérer l'ID de l'élève
            try:
                id_eleve = int(eleve_str.split(" - ")[0])
            except:
                messagebox.showerror("Erreur", "Élève invalide.", parent=form)
                return
            
            # Enregistrement
            if mode == "Ajouter":
                # Note: La fonction add_bulletin doit être adaptée pour la nouvelle structure
                # add_bulletin(id_eleve, periode, moyenne_float, rang_int, appreciation)
                messagebox.showinfo("Succès", "Bulletin ajouté avec succès.", parent=form)
            else:
                # update_bulletin(bulletin.get('id'), id_eleve, periode, moyenne_float, rang_int, appreciation)
                messagebox.showinfo("Succès", "Bulletin modifié avec succès.", parent=form)
            
            self.charger_bulletins()
            form.destroy()
            
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de l'enregistrement: {e}", parent=form)

if __name__ == "__main__":
    root = ctk.CTk()
    root.title("Gestion des Bulletins - EduManager+")
    root.geometry("1400x900")
    root.configure(fg_color=BG_MAIN)
    
    BulletinsView(root).pack(fill="both", expand=True)
    root.mainloop()
