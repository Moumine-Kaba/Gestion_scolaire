# -*- coding: utf-8 -*-
"""
Gestionnaire de vues centralisé
"""

import sys
import os
from pathlib import Path
import customtkinter as ctk

# Ajoute le répertoire racine du projet au path
PROJECT_ROOT = Path(__file__).parent.parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.append(str(PROJECT_ROOT))

class PlaceholderView(ctk.CTkFrame):
    """Vue de remplacement quand une vue n'est pas disponible"""
    def __init__(self, master, title, description="Contenu à venir..."):
        super().__init__(master, fg_color="transparent")
        
        # Titre
        ctk.CTkLabel(
            self, 
            text=title, 
            font=("Segoe UI", 24, "bold"),
            text_color="#CCD6F6"
        ).pack(pady=20)
        
        # Description
        ctk.CTkLabel(
            self, 
            text=description,
            font=("Segoe UI", 14),
            text_color="#8892B0"
        ).pack(pady=10)
        
        # Icône d'information
        ctk.CTkLabel(
            self,
            text="ℹ️",
            font=("Segoe UI", 48),
            text_color="#64FFDA"
        ).pack(pady=20)

class ViewManager:
    """Gestionnaire centralisé des vues"""
    
    def __init__(self):
        self.views_cache = {}
        self.view_classes = {}
        self._load_view_classes()
    
    def _load_view_classes(self):
        """Charge les classes de vues disponibles"""
        
        # Mapping des vues avec leurs chemins d'import
        view_mappings = {
            "eleves": "src.modules.academic.students.views.eleves_dashboard.DashboardEleves",
            "professeurs": "src.modules.academic.teachers.views.professeurs_view.ProfessorsDashboard",
            "classes": "src.modules.academic.classes.views.classes_view.ClassesManagerView",
            "enseignements": "src.modules.academic.classes.views.enseignements_view.EnseignementsView",
            "salles": "src.modules.administrative.maintenance.views.salles_view.SallesView",
            "utilisateurs": "src.modules.auth.views.utilisateurs_view.UtilisateursView",
            "matieres": "src.modules.academic.subjects.views.matieres_view.MatieresView",
            "notes": "src.modules.academic.grades.views.notes_view.NotesView",
            "presences": "src.modules.academic.classes.views.presences_view.PresenceView",
            "paiements": "src.modules.administrative.payments.views.paiements_view.PaiementsView",
            "bulletins": "src.modules.academic.grades.views.bulletins_view.BulletinsView",
            "emplois": "src.modules.academic.classes.views.emplois_view.EmploisView",
        }
        
        # Import des vues disponibles
        for view_key, import_path in view_mappings.items():
            try:
                module_path, class_name = import_path.rsplit('.', 1)
                module = __import__(module_path, fromlist=[class_name])
                view_class = getattr(module, class_name)
                self.view_classes[view_key] = view_class
                print(f"✅ Vue '{view_key}' chargée avec succès")
            except Exception as e:
                print(f"⚠️ Vue '{view_key}' non disponible: {e}")
                self.view_classes[view_key] = None
    
    def get_view(self, view_key: str, parent):
        """Retourne une instance de vue"""
        
        # Vérifier le cache
        if view_key in self.views_cache:
            return self.views_cache[view_key]
        
        # Créer une nouvelle instance
        if view_key in self.view_classes and self.view_classes[view_key]:
            try:
                view_instance = self.view_classes[view_key](parent)
                self.views_cache[view_key] = view_instance
                return view_instance
            except Exception as e:
                print(f"⚠️ Erreur lors de la création de la vue '{view_key}': {e}")
        
        # Fallback vers placeholder
        placeholder_titles = {
            "eleves": "Gestion des Élèves",
            "professeurs": "Gestion des Professeurs", 
            "classes": "Gestion des Classes",
            "enseignements": "Gestion des Enseignements",
            "salles": "Gestion des Salles",
            "utilisateurs": "Gestion des Utilisateurs",
            "matieres": "Gestion des Matières",
            "notes": "Gestion des Notes",
            "presences": "Gestion des Présences",
            "paiements": "Gestion des Paiements",
            "bulletins": "Gestion des Bulletins",
            "emplois": "Gestion des Emplois du Temps",
        }
        
        title = placeholder_titles.get(view_key, f"Vue {view_key.capitalize()}")
        placeholder = PlaceholderView(parent, title)
        self.views_cache[view_key] = placeholder
        return placeholder
    
    def clear_cache(self):
        """Vide le cache des vues"""
        self.views_cache.clear()
    
    def get_available_views(self):
        """Retourne la liste des vues disponibles"""
        return [key for key, cls in self.view_classes.items() if cls is not None]
    
    def is_view_available(self, view_key: str):
        """Vérifie si une vue est disponible"""
        return view_key in self.view_classes and self.view_classes[view_key] is not None

# Instance globale du gestionnaire de vues
view_manager = ViewManager()

