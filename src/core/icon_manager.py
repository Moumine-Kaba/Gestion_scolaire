# -*- coding: utf-8 -*-
"""
Gestionnaire d'icônes pour EduManager+
"""

import os
import tkinter as tk
from pathlib import Path
from PIL import Image, ImageTk
import customtkinter as ctk

class IconManager:
    """Gestionnaire centralisé des icônes"""
    
    def __init__(self):
        self.icons_cache = {}
        self.images_cache = {}
        self.icons_path = Path(__file__).parent.parent.parent / "resources" / "icons"
        self._load_icons()
    
    def _load_icons(self):
        """Charge toutes les icônes disponibles"""
        if not self.icons_path.exists():
            print(f"⚠️ Dossier d'icônes non trouvé: {self.icons_path}")
            return
        
        # Mapping des icônes par fonctionnalité
        self.icon_mapping = {
            # Navigation principale
            "dashboard": "home.png",
            "eleves": "person.png", 
            "profs": "person.png",
            "classes": "class.png",
            "salles": "classroom.png",
            "utilisateurs": "group.png",
            
            # Pédagogie
            "enseignements": "book.png",
            "notes": "grade.png",
            "presences": "check.png",
            "bulletins": "stats.png",
            "emplois": "clock.png",
            "matieres": "assignment.png",
            
            # Administration
            "paiements": "transfer.png",
            "settings": "settings.png",
            "logout": "logout.png",
            
            # Actions
            "refresh": "refresh.png",
            "search": "search.png",
            "add": "add.png",
            "edit": "edit.png",
            "delete": "delete.png",
            "view": "view.png",
            "print": "print.png",
            "upload": "upload.png",
            "download": "upload.png",  # Fallback pour download
            
            # Interface
            "menu": "menu.png",
            "close": "close.png",
            "calendar": "calendar.png",
            "clock_icon": "clock_icon.png",
            "envelope": "envelope.png",
            "phone": "phone.png",
            "email": "email.png",
            "folder": "folder.png",
            "file": "file.png",
            "csv": "csv.png",
            "star": "star.png",
            "award": "award.png",
            "target": "target.png",
            "trending_up": "trending_up.png",
            "analytics": "analytics.png",
            "newspaper": "newspaper.png",
            "megaphone": "megaphone.png",
            "protect": "protect.png",
            "wrench": "wrench.png",
            "stacks": "stacks.png",
            "filter": "filter.png",
            "sort": "sort.png",
            "detail": "detail.png",
            "cover": "cover.png",
            "door": "door.png",
            "chevron_right": "chevron_right.png",
            "check_circle": "check_circle.png",
            "autorenew": "autorenew.png",
            "briefcase": "briefcase.png",
            "user_avatar": "user_avatar.png",
            "logo": "logo.png",
            "bell": "bell.png",
        }
        
        # Charger les icônes disponibles
        for icon_name, filename in self.icon_mapping.items():
            icon_path = self.icons_path / filename
            if icon_path.exists():
                try:
                    self.icons_cache[icon_name] = str(icon_path)
                    print(f"✅ Icône '{icon_name}' chargée: {filename}")
                except Exception as e:
                    print(f"⚠️ Erreur lors du chargement de l'icône '{icon_name}': {e}")
            else:
                print(f"⚠️ Icône non trouvée: {filename}")
    
    def get_icon_path(self, icon_name: str) -> str:
        """Retourne le chemin vers une icône"""
        return self.icons_cache.get(icon_name, "")
    
    def get_icon_image(self, icon_name: str, size: tuple = (20, 20)) -> ctk.CTkImage:
        """Retourne une image CTkImage d'une icône"""
        icon_path = self.get_icon_path(icon_name)
        if not icon_path:
            return None
        
        # Créer une clé de cache unique
        cache_key = f"{icon_name}_{size[0]}x{size[1]}"
        
        # Vérifier le cache
        if cache_key in self.images_cache:
            return self.images_cache[cache_key]
        
        try:
            # Charger l'image avec PIL
            pil_image = Image.open(icon_path)
            pil_image = pil_image.resize(size, Image.Resampling.LANCZOS)
            
            # Créer une CTkImage
            ctk_image = ctk.CTkImage(light_image=pil_image, dark_image=pil_image, size=size)
            
            # Mettre en cache
            self.images_cache[cache_key] = ctk_image
            
            return ctk_image
        except Exception as e:
            print(f"⚠️ Erreur lors du chargement de l'image '{icon_name}': {e}")
            return None
    
    def get_available_icons(self) -> list:
        """Retourne la liste des icônes disponibles"""
        return list(self.icons_cache.keys())
    
    def has_icon(self, icon_name: str) -> bool:
        """Vérifie si une icône existe"""
        return icon_name in self.icons_cache

# Instance globale du gestionnaire d'icônes
icon_manager = IconManager()
