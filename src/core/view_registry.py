# -*- coding: utf-8 -*-
"""
Registre centralisé des vues pour EduManager+
- Découverte automatique des vues
- Import centralisé
- Gestion des erreurs
"""

import os
import sys
import importlib
from typing import Dict, Any, Optional, List
from .paths import PROJECT_ROOT, setup_theme_import

class ViewRegistry:
    """Registre centralisé pour la gestion des vues"""
    
    def __init__(self):
        self.views = {}
        self.view_errors = {}
        self.setup_paths()
    
    def setup_paths(self):
        """Configure les chemins pour l'import des vues"""
        if PROJECT_ROOT not in sys.path:
            sys.path.insert(0, PROJECT_ROOT)
        
        # Import du thème global
        setup_theme_import()
    
    def discover_views(self) -> Dict[str, str]:
        """Découvre automatiquement toutes les vues dans src/modules"""
        views_map = {}
        modules_path = os.path.join(PROJECT_ROOT, "src", "modules")
        
        if not os.path.exists(modules_path):
            print(f"⚠️ Dossier modules introuvable: {modules_path}")
            return views_map
        
        # Parcourir tous les dossiers de modules
        for root, dirs, files in os.walk(modules_path):
            if "views" in dirs:
                views_dir = os.path.join(root, "views")
                for file in os.listdir(views_dir):
                    if file.endswith("_view.py") or file.endswith("_dashboard.py"):
                        view_name = file.replace("_view.py", "").replace("_dashboard.py", "")
                        view_path = os.path.join(views_dir, file)
                        views_map[view_name] = view_path
        
        return views_map
    
    def import_view_class(self, view_name: str, view_path: str) -> Optional[Any]:
        """Importe une classes de vue spécifique"""
        try:
            # Convertir le chemin en module Python
            relative_path = os.path.relpath(view_path, PROJECT_ROOT)
            module_path = relative_path.replace(os.sep, ".").replace(".py", "")
            
            # Import du module
            module = importlib.import_module(module_path)
            
            # Rechercher la classes principale de la vue
            view_class = None
            # Priorité aux classes principales
            priority_classes = []
            other_classes = []
            
            for attr_name in dir(module):
                attr = getattr(module, attr_name)
                if (isinstance(attr, type) and 
                    hasattr(attr, '__module__') and 
                    attr.__module__ == module_path and
                    (attr_name.endswith('View') or 
                     attr_name.endswith('Dashboard') or
                     attr_name.endswith('Manager') or
                     attr_name.startswith('Dashboard') or
                     attr_name.startswith('View'))):
                    
                    # Donner la priorité aux classes principales
                    if (attr_name == 'ProfessorsDashboard' or 
                        attr_name == 'ProfessorsView' or 
                        attr_name == 'DashboardEleves' or
                        attr_name == 'ClassesCardView' or
                        (attr_name.endswith('Dashboard') and not 'Details' in attr_name) or
                        (attr_name.endswith('View') and not 'Details' in attr_name and not 'Form' in attr_name)):
                        priority_classes.append((attr_name, attr))
                    elif not ('Details' in attr_name or 'Form' in attr_name or 'Modal' in attr_name):
                        other_classes.append((attr_name, attr))
            
            # Prendre d'abord les classes prioritaires, puis les autres
            all_classes = priority_classes + other_classes
            if all_classes:
                view_class = all_classes[0][1]
            
            if view_class:
                print(f"✅ Vue '{view_name}' importée: {view_class.__name__}")
                return view_class
            else:
                print(f"⚠️ Aucune classes de vue trouvée dans {view_name}")
                return None
                
        except Exception as e:
            error_msg = f"Erreur import {view_name}: {e}"
            print(f"⚠️ {error_msg}")
            self.view_errors[view_name] = error_msg
            return None
    
    def register_all_views(self):
        """Enregistre toutes les vues découvertes"""
        print("🔍 Découverte des vues...")
        views_map = self.discover_views()
        
        print(f"📋 {len(views_map)} vues trouvées:")
        for view_name, view_path in views_map.items():
            print(f"  - {view_name}: {view_path}")
        
        print("\n📦 Import des vues...")
        for view_name, view_path in views_map.items():
            view_class = self.import_view_class(view_name, view_path)
            if view_class:
                self.views[view_name] = view_class
        
        print(f"\n✅ {len(self.views)} vues importées avec succès")
        if self.view_errors:
            print(f"⚠️ {len(self.view_errors)} erreurs d'import:")
            for view_name, error in self.view_errors.items():
                print(f"  - {view_name}: {error}")
    
    def get_view(self, view_name: str) -> Optional[Any]:
        """Récupère une vue par son nom"""
        return self.views.get(view_name)
    
    def get_all_views(self) -> Dict[str, Any]:
        """Retourne toutes les vues enregistrées"""
        return self.views.copy()
    
    def get_view_names(self) -> List[str]:
        """Retourne la liste des noms de vues"""
        return list(self.views.keys())
    
    def create_placeholder_view(self, view_name: str):
        """Crée une vue placeholder pour les vues manquantes"""
        import customtkinter as ctk
        
        class PlaceholderView(ctk.CTkFrame):
            def __init__(self, parent, title=None):
                super().__init__(parent, fg_color="transparent")
                title = title or view_name.replace("_", " ").title()
                
                # Titre
                ctk.CTkLabel(
                    self, 
                    text=title, 
                    font=("Segoe UI", 24, "bold"), 
                    text_color="#64FFDA"
                ).pack(pady=20)
                
                # Message
                ctk.CTkLabel(
                    self, 
                    text="Vue en cours de développement...", 
                    font=("Segoe UI", 14), 
                    text_color="#8892B0"
                ).pack(pady=10)
                
                # Icône
                ctk.CTkLabel(
                    self, 
                    text="🚧", 
                    font=("Segoe UI", 48)
                ).pack(pady=20)
        
        return PlaceholderView

# Instance globale du registre
view_registry = ViewRegistry()

def get_view_registry() -> ViewRegistry:
    """Retourne l'instance globale du registre de vues"""
    return view_registry

def register_all_views():
    """Fonction utilitaire pour enregistrer toutes les vues"""
    view_registry.register_all_views()

def get_view(view_name: str):
    """Fonction utilitaire pour récupérer une vue"""
    return view_registry.get_view(view_name)

if __name__ == "__main__":
    # Test du registre
    registry = ViewRegistry()
    registry.register_all_views()
    
    print("\n=== VUES DISPONIBLES ===")
    for name, view_class in registry.get_all_views().items():
        print(f"✅ {name}: {view_class.__name__}")
