#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gestionnaire de Vues avec Contrôle d'Accès
EduManager+ - Gestion Scolaire
"""

import customtkinter as ctk
from typing import Dict, Optional, Callable
import os
import sys

# Import local avec fallback
try:
    from src.modules.auth.models.permissions import PermissionManager, ViewType, PermissionLevel
except ImportError as e:
    print(f"❌ Erreur import PermissionManager: {e}")
    PermissionManager = None

class ViewManager:
    """Gestionnaire central des vues avec contrôle d'accès"""
    
    def __init__(self, db_path: str, main_app):
        self.db_path = db_path
        self.main_app = main_app
        self.current_user = None
        self.permission_manager = None
        self.views = {}
        self.current_view = None
        
        # Initialiser le gestionnaire de permissions
        self._init_permission_manager()
        
        # Définir les vues disponibles
        self._define_available_views()
    
    def _init_permission_manager(self):
        """Initialise le gestionnaire de permissions"""
        try:
            if PermissionManager:
                self.permission_manager = PermissionManager(self.db_path)
                print("✅ Gestionnaire de vues initialisé avec permissions")
            else:
                print("⚠️ Gestionnaire de permissions non disponible")
        except Exception as e:
            print(f"❌ Erreur initialisation gestionnaire de vues: {e}")
    
    def _define_available_views(self):
        """Définit toutes les vues disponibles dans l'application"""
        self.views = {
            ViewType.DASHBOARD.value: {
                "title": "Tableau de Bord",
                "icon": "📊",
                "description": "Vue d'ensemble du système",
                "create_func": self._create_dashboard_view,
                "min_permission": PermissionLevel.READ.value
            },
            ViewType.NOTES.value: {
                "title": "Gestion des Notes",
                "icon": "📝",
                "description": "Saisie et consultation des notes",
                "create_func": self._create_notes_view,
                "min_permission": PermissionLevel.READ.value
            },
            ViewType.PRESENCES.value: {
                "title": "Gestion des Présences",
                "icon": "✅",
                "description": "Suivi des présences et absences",
                "create_func": self._create_presences_view,
                "min_permission": PermissionLevel.READ.value
            },
            ViewType.BULLETINS.value: {
                "title": "Bulletins Scolaires",
                "icon": "📋",
                "description": "Génération et consultation des bulletins",
                "create_func": self._create_bulletins_view,
                "min_permission": PermissionLevel.READ.value
            },
            ViewType.ELEVES.value: {
                "title": "Gestion des Élèves",
                "icon": "👨‍🎓",
                "description": "Administration des dossiers élèves",
                "create_func": self._create_eleves_view,
                "min_permission": PermissionLevel.READ.value
            },
            ViewType.PROFESSEURS.value: {
                "title": "Gestion des Professeurs",
                "icon": "👨‍🏫",
                "description": "Administration des dossiers professeurs",
                "create_func": self._create_professeurs_view,
                "min_permission": PermissionLevel.READ.value
            },
            ViewType.CLASSES.value: {
                "title": "Gestion des Classes",
                "icon": "🏫",
                "description": "Organisation des classes et emplois du temps",
                "create_func": self._create_classes_view,
                "min_permission": PermissionLevel.READ.value
            },
            ViewType.MATIERES.value: {
                "title": "Gestion des Matières",
                "icon": "📚",
                "description": "Configuration des matières et programmes",
                "create_func": self._create_matieres_view,
                "min_permission": PermissionLevel.READ.value
            },
            ViewType.UTILISATEURS.value: {
                "title": "Gestion des Utilisateurs",
                "icon": "👥",
                "description": "Administration des comptes utilisateurs",
                "create_func": self._create_utilisateurs_view,
                "min_permission": PermissionLevel.READ.value
            },
            ViewType.ROLES.value: {
                "title": "Gestion des Rôles",
                "icon": "🔐",
                "description": "Configuration des rôles et permissions",
                "create_func": self._create_roles_view,
                "min_permission": PermissionLevel.READ.value
            },
            ViewType.PARAMETRES.value: {
                "title": "Paramètres",
                "icon": "⚙️",
                "description": "Configuration du système",
                "create_func": self._create_parametres_view,
                "min_permission": PermissionLevel.READ.value
            },
            ViewType.RAPPORTS.value: {
                "title": "Rapports et Statistiques",
                "icon": "📈",
                "description": "Génération de rapports et analyses",
                "create_func": self._create_rapports_view,
                "min_permission": PermissionLevel.READ.value
            },
            ViewType.FINANCE.value: {
                "title": "Gestion Financière",
                "icon": "💰",
                "description": "Suivi des finances et facturation",
                "create_func": self._create_finance_view,
                "min_permission": PermissionLevel.READ.value
            },
            ViewType.BIBLIOTHEQUE.value: {
                "title": "Bibliothèque",
                "icon": "📖",
                "description": "Gestion des ressources documentaires",
                "create_func": self._create_bibliotheque_view,
                "min_permission": PermissionLevel.READ.value
            },
            ViewType.CALENDRIER.value: {
                "title": "Calendrier",
                "icon": "📅",
                "description": "Planning et événements",
                "create_func": self._create_calendrier_view,
                "min_permission": PermissionLevel.READ.value
            }
        }
    
    def set_current_user(self, user_info: Dict):
        """Définit l'utilisateurs actuel et ses permissions"""
        self.current_user = user_info
        print(f"👤 Utilisateur connecté: {user_info.get('username', 'Inconnu')}")
        if self.permission_manager:
            accessible_views = self.permission_manager.get_accessible_views_for_user(user_info['id_utilisateur'])
            print(f"🔐 Vues accessibles: {len(accessible_views)} vues")
    
    def can_access_view(self, view_name: str) -> bool:
        """Vérifie si l'utilisateurs actuel peut accéder à une vue"""
        if not self.current_user or not self.permission_manager:
            return False
        
        return self.permission_manager.can_access_view(self.current_user['id_utilisateur'], view_name)
    
    def get_view_permission_level(self, view_name: str) -> str:
        """Récupère le niveau de permissions de l'utilisateurs pour une vue"""
        if not self.current_user or not self.permission_manager:
            return PermissionLevel.NONE.value
        
        return self.permission_manager.get_view_permission_level(self.current_user['id_utilisateur'], view_name)
    
    def get_accessible_views(self) -> Dict[str, Dict]:
        """Récupère les vues accessibles pour l'utilisateurs actuel"""
        if not self.current_user or not self.permission_manager:
            return {}
        
        accessible_views = {}
        for view_name, view_info in self.views.items():
            if self.can_access_view(view_name):
                accessible_views[view_name] = view_info
        
        return accessible_views
    
    def switch_to_view(self, view_name: str) -> bool:
        """Change vers une vue spécifique avec vérification des permissions"""
        if not self.can_access_view(view_name):
            print(f"❌ Accès refusé à la vue: {view_name}")
            return False
        
        try:
            # Nettoyer la vue actuelle
            if self.current_view:
                self.current_view.destroy()
            
            # Créer la nouvelle vue
            view_info = self.views.get(view_name)
            if view_info and view_info.get("create_func"):
                self.current_view = view_info["create_func"]()
                self.current_view.pack(fill="both", expand=True, padx=20, pady=20)
                
                # Mettre à jour le titre de la fenêtre
                if hasattr(self.main_app, 'update_title'):
                    self.main_app.update_title(view_info["title"])
                
                print(f"✅ Vue changée vers: {view_info['title']}")
                return True
            else:
                print(f"❌ Vue non trouvée: {view_name}")
                return False
                
        except Exception as e:
            print(f"❌ Erreur changement de vue: {e}")
            return False
    
    def get_view_info(self, view_name: str) -> Optional[Dict]:
        """Récupère les informations d'une vue"""
        return self.views.get(view_name)
    
    def get_current_view_name(self) -> Optional[str]:
        """Récupère le nom de la vue actuellement affichée"""
        if self.current_view:
            for view_name, view_info in self.views.items():
                if view_info.get("create_func") == self.current_view.__class__:
                    return view_name
        return None
    
    # Méthodes de création des vues (placeholders)
    def _create_dashboard_view(self):
        """Crée la vue du tableau de bord"""
        frame = ctk.CTkFrame(self.main_app.main_content)
        
        # Titre
        title_label = ctk.CTkLabel(
            frame, 
            text="📊 Tableau de Bord", 
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title_label.pack(pady=20)
        
        # Contenu du dashboard
        content_frame = ctk.CTkFrame(frame)
        content_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Statistiques rapides
        stats_frame = ctk.CTkFrame(content_frame)
        stats_frame.pack(fill="x", pady=10)
        
        stats_label = ctk.CTkLabel(
            stats_frame,
            text="Statistiques du système",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        stats_label.pack(pady=10)
        
        return frame
    
    def _create_notes_view(self):
        """Crée la vue de gestion des notes"""
        frame = ctk.CTkFrame(self.main_app.main_content)
        
        title_label = ctk.CTkLabel(
            frame, 
            text="📝 Gestion des Notes", 
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title_label.pack(pady=20)
        
        # Contrôle des permissions
        permission_level = self.get_view_permission_level(ViewType.NOTES.value)
        
        if permission_level == PermissionLevel.ADMIN.value:
            # Interface complète pour l'admin
            self._create_notes_admin_interface(frame)
        elif permission_level == PermissionLevel.WRITE.value:
            # Interface pour les professeurs
            self._create_notes_teacher_interface(frame)
        elif permission_level == PermissionLevel.READ.value:
            # Interface en lecture seule
            self._create_notes_readonly_interface(frame)
        
        return frame
    
    def _create_notes_admin_interface(self, parent):
        """Interface admin pour les notes"""
        content_frame = ctk.CTkFrame(parent)
        content_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        admin_label = ctk.CTkLabel(
            content_frame,
            text="🔐 Interface Administrateur - Tous les droits",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        admin_label.pack(pady=10)
        
        # Boutons d'action admin
        actions_frame = ctk.CTkFrame(content_frame)
        actions_frame.pack(fill="x", pady=10)
        
        ctk.CTkButton(actions_frame, text="➕ Ajouter Note").pack(side="left", padx=5)
        ctk.CTkButton(actions_frame, text="✏️ Modifier Note").pack(side="left", padx=5)
        ctk.CTkButton(actions_frame, text="🗑️ Supprimer Note").pack(side="left", padx=5)
        ctk.CTkButton(actions_frame, text="📊 Statistiques").pack(side="left", padx=5)
    
    def _create_notes_teacher_interface(self, parent):
        """Interface professeurs pour les notes"""
        content_frame = ctk.CTkFrame(parent)
        content_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        teacher_label = ctk.CTkLabel(
            content_frame,
            text="👨‍🏫 Interface Professeur - Lecture + Écriture",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        teacher_label.pack(pady=10)
        
        # Boutons d'action professeurs
        actions_frame = ctk.CTkFrame(content_frame)
        actions_frame.pack(fill="x", pady=10)
        
        ctk.CTkButton(actions_frame, text="➕ Ajouter Note").pack(side="left", padx=5)
        ctk.CTkButton(actions_frame, text="✏️ Modifier Note").pack(side="left", padx=5)
        ctk.CTkButton(actions_frame, text="📊 Mes Classes").pack(side="left", padx=5)
    
    def _create_notes_readonly_interface(self, parent):
        """Interface en lecture seule pour les notes"""
        content_frame = ctk.CTkFrame(parent)
        content_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        readonly_label = ctk.CTkLabel(
            content_frame,
            text="👁️ Interface Lecture Seule",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        readonly_label.pack(pady=10)
        
        # Message d'information
        info_label = ctk.CTkLabel(
            content_frame,
            text="Vous avez accès en lecture seule à cette section",
            font=ctk.CTkFont(size=14)
        )
        info_label.pack(pady=10)
    
    # Placeholders pour les autres vues
    def _create_presences_view(self):
        frame = ctk.CTkFrame(self.main_app.main_content)
        ctk.CTkLabel(frame, text="✅ Gestion des Présences", font=ctk.CTkFont(size=24, weight="bold")).pack(pady=20)
        return frame
    
    def _create_bulletins_view(self):
        frame = ctk.CTkFrame(self.main_app.main_content)
        ctk.CTkLabel(frame, text="📋 Bulletins Scolaires", font=ctk.CTkFont(size=24, weight="bold")).pack(pady=20)
        return frame
    
    def _create_eleves_view(self):
        """Crée la vue de gestion des élèves"""
        try:
            # Import de la vraie vue des élèves
            from src.modules.academic.students.views.eleves_dashboard import DashboardEleves
            
            # Créer le dashboard des élèves
            dashboard = DashboardEleves(self.main_app.main_content)
            return dashboard
            
        except Exception as e:
            print(f"⚠️ Erreur création vue élèves: {e}")
            # Fallback vers placeholder
            frame = ctk.CTkFrame(self.main_app.main_content)
            ctk.CTkLabel(frame, text="👨‍🎓 Gestion des Élèves", font=ctk.CTkFont(size=24, weight="bold")).pack(pady=20)
            ctk.CTkLabel(frame, text=f"Erreur: {e}", font=ctk.CTkFont(size=12)).pack(pady=10)
            return frame
    
    def _create_professeurs_view(self):
        """Crée la vue de gestion des professeurs"""
        try:
            # Import de la vraie vue des professeurs
            from src.modules.academic.teachers.views.professeurs_view import ProfessorsDashboard
            
            # Créer le dashboard des professeurs
            dashboard = ProfessorsDashboard(self.main_app.main_content)
            return dashboard
            
        except Exception as e:
            print(f"⚠️ Erreur création vue professeurs: {e}")
            # Fallback vers placeholder
            frame = ctk.CTkFrame(self.main_app.main_content)
            ctk.CTkLabel(frame, text="👨‍🏫 Gestion des Professeurs", font=ctk.CTkFont(size=24, weight="bold")).pack(pady=20)
            ctk.CTkLabel(frame, text=f"Erreur: {e}", font=ctk.CTkFont(size=12)).pack(pady=10)
            return frame
    
    def _create_classes_view(self):
        frame = ctk.CTkFrame(self.main_app.main_content)
        ctk.CTkLabel(frame, text="🏫 Gestion des Classes", font=ctk.CTkFont(size=24, weight="bold")).pack(pady=20)
        return frame
    
    def _create_matieres_view(self):
        frame = ctk.CTkFrame(self.main_app.main_content)
        ctk.CTkLabel(frame, text="📚 Gestion des Matières", font=ctk.CTkFont(size=24, weight="bold")).pack(pady=20)
        return frame
    
    def _create_utilisateurs_view(self):
        frame = ctk.CTkFrame(self.main_app.main_content)
        ctk.CTkLabel(frame, text="👥 Gestion des Utilisateurs", font=ctk.CTkFont(size=24, weight="bold")).pack(pady=20)
        return frame
    
    def _create_roles_view(self):
        frame = ctk.CTkFrame(self.main_app.main_content)
        ctk.CTkLabel(frame, text="🔐 Gestion des Rôles", font=ctk.CTkFont(size=24, weight="bold")).pack(pady=20)
        return frame
    
    def _create_parametres_view(self):
        frame = ctk.CTkFrame(self.main_app.main_content)
        ctk.CTkLabel(frame, text="⚙️ Paramètres", font=ctk.CTkFont(size=24, weight="bold")).pack(pady=20)
        return frame
    
    def _create_rapports_view(self):
        frame = ctk.CTkFrame(self.main_app.main_content)
        ctk.CTkLabel(frame, text="📈 Rapports et Statistiques", font=ctk.CTkFont(size=24, weight="bold")).pack(pady=20)
        return frame
    
    def _create_finance_view(self):
        frame = ctk.CTkFrame(self.main_app.main_content)
        ctk.CTkLabel(frame, text="💰 Gestion Financière", font=ctk.CTkFont(size=24, weight="bold")).pack(pady=20)
        return frame
    
    def _create_bibliotheque_view(self):
        frame = ctk.CTkFrame(self.main_app.main_content)
        ctk.CTkLabel(frame, text="📖 Bibliothèque", font=ctk.CTkFont(size=24, weight="bold")).pack(pady=20)
        return frame
    
    def _create_calendrier_view(self):
        frame = ctk.CTkFrame(self.main_app.main_content)
        ctk.CTkLabel(frame, text="📅 Calendrier", font=ctk.CTkFont(size=24, weight="bold")).pack(pady=20)
        return frame
