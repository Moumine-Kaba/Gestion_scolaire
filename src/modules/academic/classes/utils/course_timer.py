import customtkinter as ctk
from datetime import datetime, timedelta
import threading
import time
from tkinter import messagebox
import os
import sys
from PIL import Image

# Import du thème global
try:
    # Ajouter le chemin racine au sys.path
    root_path = os.path.join(os.path.dirname(__file__), '../../../../..')
    sys.path.insert(0, root_path)
    
    from resources.themes.theme import *
    print("✅ Thème global importé pour les notifications")
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

class CourseHistoryManager:
    """Gestionnaire de l'historique des cours terminés"""
    
    def __init__(self):
        self.completed_courses = []
    
    def add_completed_course(self, course_data):
        """Ajoute un cours terminé à l'historique"""
        course_info = {
            'id': course_data.get('id'),
            'professeur_nom': course_data.get('professeur_nom', 'Inconnu'),
            'classe_nom': course_data.get('classe_nom', 'Inconnue'),
            'matiere_nom': course_data.get('matiere_nom', 'Inconnue'),
            'salle_nom': course_data.get('salle_nom', 'Non spécifiée'),
            'heure': course_data.get('heure', 'Non spécifiée'),
            'duree': course_data.get('duree', 60),
            'jour': course_data.get('jour', 'Non spécifié'),
            'completed_at': datetime.now().strftime('%H:%M:%S'),
            'completed_date': datetime.now().strftime('%d/%m/%Y')
        }
        self.completed_courses.append(course_info)
        # Log supprimé - maintenant géré visuellement
    
    def get_completed_courses(self):
        """Retourne la liste des cours terminés"""
        return self.completed_courses
    
    def clear_history(self):
        """Vide l'historique des cours terminés"""
        self.completed_courses.clear()
    
    def get_recent_courses(self, limit=10):
        """Retourne les cours récents terminés"""
        return self.completed_courses[-limit:] if self.completed_courses else []

class NotificationManager:
    """Gestionnaire de notifications pour les cours"""
    
    def __init__(self, parent_widget):
        self.parent = parent_widget
        self.notifications = []
        self.notification_frame = None
        self.icons = self._load_notification_icons()
        self.setup_notification_area()
    
    def setup_notification_area(self):
        """Configure la zone de notifications"""
        # Frame pour les notifications (en haut à droite)
        self.notification_frame = ctk.CTkFrame(
            self.parent,
            fg_color="transparent",
            width=350,
            height=100
        )
        self.notification_frame.place(relx=1.0, rely=0.0, anchor="ne", x=-20, y=20)
        self.notification_frame.pack_propagate(False)
    
    def _load_notification_icons(self):
        """Charge les icônes pour les notifications"""
        icons = {}
        try:
            # Chemin vers les icônes
            icons_path = os.path.join(os.path.dirname(__file__), '../../../../../../resources/icons')
            
            # Icônes pour les notifications
            icon_files = {
                'bell': 'bell.png',
                'check_circle': 'check_circle.png',
                'clock': 'clock_icon.png',
                'book': 'book.png',
                'person': 'person.png',
                'classroom': 'classroom.png',
                'close': 'close.png',
                'view': 'view.png'
            }
            
            for key, filename in icon_files.items():
                icon_path = os.path.join(icons_path, filename)
                if os.path.exists(icon_path):
                    try:
                        image = Image.open(icon_path)
                        icons[key] = ctk.CTkImage(light_image=image, dark_image=image, size=(20, 20))
                    except Exception as e:
                        print(f"⚠️ Erreur chargement icône {filename}: {e}")
                        icons[key] = None
                else:
                    icons[key] = None
                    
        except Exception as e:
            print(f"⚠️ Erreur chargement icônes notifications: {e}")
            
        return icons
    
    def add_notification(self, course_data, notification_type="course_end"):
        """Ajoute une nouvelle notifications"""
        notification_id = len(self.notifications)
        
        # Créer la notifications
        notifications = self.create_notification_widget(course_data, notification_type, notification_id)
        self.notifications.append(notifications)
        
        # Animer l'apparition
        self.animate_notification_in(notifications)
        
        # Auto-suppression après 10 secondes
        self.parent.after(10000, lambda: self.remove_notification(notification_id))
    
    def create_notification_widget(self, course_data, notification_type, notification_id):
        """Crée le widget de notifications avec thème EduManager+"""
        # Couleurs selon le type (thème EduManager+)
        if notification_type == "course_end":
            bg_color = ERROR_RED  # Rouge pour fin de cours
            icon = self.icons.get('check_circle')
            title_text = "COURS TERMINÉ"
        elif notification_type == "course_start":
            bg_color = SUCCESS_GREEN  # Vert pour début de cours
            icon = self.icons.get('clock')
            title_text = "COURS DÉMARRÉ"
        else:
            bg_color = ACCENT  # Cyan par défaut
            icon = self.icons.get('bell')
            title_text = "NOTIFICATION"
        
        # Frame principal de la notifications (thème EduManager+)
        notification_widget = ctk.CTkFrame(
            self.notification_frame,
            fg_color=CARD_BG,
            border_color=bg_color,
            border_width=2,
            corner_radius=15,
            height=90
        )
        
        # Header avec icône et titre
        header_frame = ctk.CTkFrame(notification_widget, fg_color="transparent")
        header_frame.pack(fill="x", padx=10, pady=(8, 4))
        
        # Icône (si disponible) et titre
        if icon:
            icon_label = ctk.CTkLabel(
                header_frame,
                image=icon,
                text=""
            )
            icon_label.pack(side="left")
        else:
            # Fallback avec emoji
            icon_label = ctk.CTkLabel(
                header_frame,
                text="🎓" if notification_type == "course_end" else "🚀" if notification_type == "course_start" else "📢",
                font=("Segoe UI", 16),
                text_color=bg_color
            )
            icon_label.pack(side="left")
        
        title_label = ctk.CTkLabel(
            header_frame,
            text=title_text,
            font=("Segoe UI", 12, "bold"),
            text_color=TEXT,
            fg_color="transparent"
        )
        title_label.pack(side="left", padx=(8, 0))
        
        # Bouton fermer avec icône
        close_icon = self.icons.get('close')
        if close_icon:
            close_btn = ctk.CTkButton(
                header_frame,
                image=close_icon,
                text="",
                width=25,
                height=25,
                fg_color="transparent",
                hover_color=MUTED,
                command=lambda: self.remove_notification(notification_id)
            )
        else:
            close_btn = ctk.CTkButton(
                header_frame,
                text="✕",
                font=("Segoe UI", 10, "bold"),
                fg_color="transparent",
                text_color=TEXT,
                hover_color=MUTED,
                command=lambda: self.remove_notification(notification_id),
                width=20,
                height=20,
                corner_radius=10
            )
        close_btn.pack(side="right")
        
        # Contenu de la notifications
        content_frame = ctk.CTkFrame(notification_widget, fg_color="transparent")
        content_frame.pack(fill="x", padx=10, pady=(0, 8))
        
        # Informations du cours avec icônes
        course_info_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        course_info_frame.pack(fill="x")
        
        # Matière avec icône livre
        book_icon = self.icons.get('book')
        if book_icon:
            book_label = ctk.CTkLabel(course_info_frame, image=book_icon, text="")
            book_label.pack(side="left")
        
        course_info = f"{course_data.get('matiere_nom', 'Matière')} - {course_data.get('professeur_nom', 'Professeur')}"
        course_label = ctk.CTkLabel(
            course_info_frame,
            text=course_info,
            font=("Segoe UI", 11, "bold"),
            text_color=TEXT
        )
        course_label.pack(side="left", padx=(5, 0))
        
        # Informations supplémentaires avec icônes
        extra_info_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        extra_info_frame.pack(fill="x", pady=(2, 0))
        
        # Salle avec icône
        classroom_icon = self.icons.get('classroom')
        if classroom_icon:
            classroom_label = ctk.CTkLabel(extra_info_frame, image=classroom_icon, text="")
            classroom_label.pack(side="left")
        
        extra_info = f"Salle: {course_data.get('salle_nom', 'Non spécifiée')} | Classe: {course_data.get('classe_nom', 'Inconnue')}"
        extra_label = ctk.CTkLabel(
            extra_info_frame,
            text=extra_info,
            font=("Segoe UI", 10),
            text_color=MUTED
        )
        extra_label.pack(side="left", padx=(5, 0))
        
        # Bouton d'action avec icône
        view_icon = self.icons.get('view')
        if view_icon:
            action_btn = ctk.CTkButton(
                notification_widget,
                image=view_icon,
                text="Voir détails",
                font=("Segoe UI", 10, "bold"),
                fg_color=bg_color,
                text_color=TEXT,
                hover_color=ACCENT,
                command=lambda: self.show_course_details(course_data),
                height=25,
                corner_radius=8
            )
        else:
            action_btn = ctk.CTkButton(
                notification_widget,
                text="Voir détails",
                font=("Segoe UI", 10, "bold"),
                fg_color=bg_color,
                text_color=TEXT,
                hover_color=ACCENT,
                command=lambda: self.show_course_details(course_data),
                height=25,
                corner_radius=8
            )
        action_btn.pack(fill="x", padx=10, pady=(0, 8))
        
        return {
            'id': notification_id,
            'widget': notification_widget,
            'course_data': course_data,
            'type': notification_type
        }
    
    def animate_notification_in(self, notifications):
        """Anime l'apparition de la notifications"""
        widget = notifications['widget']
        
        # Position initiale (hors écran)
        widget.pack(fill="x", padx=5, pady=2)
        
        # Animation de glissement depuis la droite
        def slide_in():
            # L'animation sera gérée par le pack()
            pass
        
        self.parent.after(100, slide_in)
    
    def remove_notification(self, notification_id):
        """Supprime une notifications"""
        for i, notifications in enumerate(self.notifications):
            if notifications['id'] == notification_id:
                # Animation de sortie
                widget = notifications['widget']
                widget.pack_forget()
                widget.destroy()
                self.notifications.pop(i)
                break
    
    def show_course_details(self, course_data):
        """Affiche les détails du cours dans une fenêtre"""
        details_window = ctk.CTkToplevel(self.parent)
        details_window.title("Détails du Cours")
        details_window.geometry("400x300")
        details_window.transient(self.parent)
        details_window.grab_set()
        
        # Contenu des détails
        content_frame = ctk.CTkFrame(details_window, fg_color="transparent")
        content_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Titre
        title_label = ctk.CTkLabel(
            content_frame,
            text="📚 Détails du Cours",
            font=("Segoe UI", 18, "bold"),
            text_color="#00D4FF"
        )
        title_label.pack(pady=(0, 20))
        
        # Informations détaillées
        details_text = f"""
📚 Matière: {course_data.get('matiere_nom', 'Inconnue')}
👨‍🏫 Professeur: {course_data.get('professeur_nom', 'Inconnu')}
🏫 Classe: {course_data.get('classe_nom', 'Inconnue')}
🚪 Salle: {course_data.get('salle_nom', 'Non spécifiée')}
📅 Jour: {course_data.get('jour', 'Non spécifié')}
🕐 Heure: {course_data.get('heure', 'Non spécifiée')}
⏰ Durée: {course_data.get('duree', 60)} minutes
📊 Statut: {course_data.get('statut', 'Actif')}
        """
        
        details_label = ctk.CTkLabel(
            content_frame,
            text=details_text,
            font=("Segoe UI", 12),
            text_color="#FFFFFF",
            fg_color="transparent",
            anchor="w",
            justify="left"
        )
        details_label.pack(fill="x", pady=(0, 20))
        
        # Bouton fermer
        close_btn = ctk.CTkButton(
            content_frame,
            text="Fermer",
            font=("Segoe UI", 12, "bold"),
            fg_color="#00D4FF",
            text_color="#FFFFFF",
            hover_color="#0099CC",
            command=details_window.destroy,
            height=40
        )
        close_btn.pack()
    
    def clear_all_notifications(self):
        """Supprime toutes les notifications"""
        for notifications in self.notifications:
            notifications['widget'].destroy()
        self.notifications.clear()

class CourseHistoryWindow:
    """Fenêtre pour afficher l'historique des cours terminés"""
    
    def __init__(self, parent, history_manager):
        self.parent = parent
        self.history_manager = history_manager
        self.window = None
    
    def show_history(self):
        """Affiche la fenêtre d'historique"""
        if self.window and self.window.winfo_exists():
            self.window.lift()
            return
        
        self.window = ctk.CTkToplevel(self.parent)
        self.window.title("📚 Historique des Cours Terminés")
        self.window.geometry("840x640")
        self.window.transient(self.parent)
        self.window.grab_set()
        self.window.configure(fg_color=BG_MAIN)
        
        # Titre
        title_frame = ctk.CTkFrame(self.window, fg_color="transparent")
        title_frame.pack(fill="x", padx=20, pady=20)
        
        title_label = ctk.CTkLabel(
            title_frame,
            text="📚 Historique des Cours Terminés",
            font=("Segoe UI", 22, "bold"),
            text_color=TEXT_ACCENT
        )
        title_label.pack(side="left")
        
        # Bouton fermer (avec icône)
        close_btn = ctk.CTkButton(
            title_frame,
            text="Fermer",
            image=self._load_icon("close.png", 18),
            fg_color="transparent",
            hover_color=BG_CARD_HOVER,
            command=self.window.destroy,
            width=36,
            height=36,
            corner_radius=10,
            border_width=1,
            border_color=BORDER_COLOR
        )
        close_btn.pack(side="right")
        
        # Bouton nettoyer (avec icône)
        clear_btn = ctk.CTkButton(
            title_frame,
            text="Nettoyer",
            font=("Segoe UI", 12, "bold"),
            fg_color=BG_CARD,
            text_color=TEXT_PRIMARY,
            hover_color=BG_CARD_HOVER,
            command=self.clear_history,
            width=110,
            height=36,
            corner_radius=12,
            border_width=1,
            border_color=BORDER_COLOR,
            image=self._load_icon("broom.png", 18) or self._load_icon("clean.png", 18)
        )
        clear_btn.pack(side="right", padx=(0, 10))
        
        # Frame pour la liste (grille 2 colonnes)
        list_frame = ctk.CTkScrollableFrame(self.window, fg_color=BG_CARD, corner_radius=16, border_width=1, border_color=BORDER_COLOR)
        list_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        list_frame.grid_columnconfigure((0, 1), weight=1, uniform="cols")
        
        # Charger et afficher les cours terminés
        self.load_completed_courses(list_frame)
    
    def load_completed_courses(self, parent_frame):
        """Charge et affiche les cours terminés"""
        completed_courses = self.history_manager.get_completed_courses()
        
        if not completed_courses:
            # Message si aucun cours terminé
            no_courses_label = ctk.CTkLabel(
                parent_frame,
                text="📭 Aucun cours terminé pour le moment",
                font=("Segoe UI", 16),
                text_color="#8B949E"
            )
            no_courses_label.pack(pady=50)
            return
        
        # Afficher les cours terminés (du plus récent au plus ancien) en 2 colonnes
        for idx, course in enumerate(reversed(completed_courses)):
            row = idx // 2
            col = idx % 2
            self.create_course_item(parent_frame, course, grid_position=(row, col))
    
    def create_course_item(self, parent_frame, course, grid_position=None):
        """Crée un élément de cours terminé"""
        # Frame principal
        course_frame = ctk.CTkFrame(
            parent_frame,
            fg_color=BG_CARD,
            corner_radius=12,
            border_width=1,
            border_color=BORDER_COLOR,
            height=110
        )
        if grid_position is None:
            course_frame.pack(fill="x", padx=5, pady=5)
        else:
            r, c = grid_position
            course_frame.grid(row=r, column=c, padx=8, pady=8, sticky="nsew")
        course_frame.pack_propagate(False)
        
        # Header avec icône et titre
        header_frame = ctk.CTkFrame(course_frame, fg_color="transparent")
        header_frame.pack(fill="x", padx=15, pady=(10, 5))
        
        # Icône
        icon_img = self._load_icon("check_circle.png", 20)
        if icon_img:
            icon_label = ctk.CTkLabel(header_frame, text="", image=icon_img, fg_color="transparent")
        else:
            icon_label = ctk.CTkLabel(header_frame, text="✅", font=("Segoe UI", 18), text_color=TEXT_ACCENT, fg_color="transparent")
        icon_label.pack(side="left")
        
        # Titre
        title_label = ctk.CTkLabel(
            header_frame,
            text=f"{course['matiere_nom']} - {course['professeur_nom']}",
            font=("Segoe UI", 14, "bold"),
            text_color=TEXT_PRIMARY,
            fg_color="transparent"
        )
        title_label.pack(side="left", padx=(10, 0))
        
        # Heure de fin
        time_label = ctk.CTkLabel(
            header_frame,
            text=f"Terminé à {course['completed_at']}",
            font=("Segoe UI", 12),
            text_color=TEXT_SECONDARY,
            fg_color="transparent"
        )
        time_label.pack(side="right")
        
        # Détails
        details_frame = ctk.CTkFrame(course_frame, fg_color="transparent")
        details_frame.pack(fill="x", padx=15, pady=(0, 10))
        
        details_text = f"{course['classe_nom']} • {course['salle_nom']} • {course['duree']} min • {course['jour']} {course['heure']}"
        details_label = ctk.CTkLabel(
            details_frame,
            text=details_text,
            font=("Segoe UI", 11),
            text_color=TEXT_SECONDARY,
            fg_color="transparent"
        )
        details_label.pack(anchor="w")

    def _load_icon(self, filename, size):
        try:
            icons_path = os.path.join(os.path.dirname(__file__), '../../../../../../resources/icons')
            path = os.path.join(icons_path, filename)
            if os.path.exists(path):
                img = Image.open(path)
                return ctk.CTkImage(light_image=img, dark_image=img, size=(size, size))
        except Exception as e:
            print(f"⚠️ Erreur chargement icône historique: {e}")
        return None
    
    def clear_history(self):
        """Nettoie l'historique"""
        self.history_manager.clear_history()
        # Fermer et rouvrir la fenêtre pour actualiser
        self.window.destroy()
        self.show_history()

class CourseTimer:
    """Gestionnaire de minuteur pour les cours"""
    
    def __init__(self, parent_widget, course_data, notification_manager=None, history_manager=None, on_timer_update=None, on_course_end=None):
        self.parent = parent_widget
        self.course_data = course_data
        self.notification_manager = notification_manager
        self.history_manager = history_manager
        self.on_timer_update = on_timer_update
        self.on_course_end = on_course_end
        
        # Données du cours
        self.professeur_nom = course_data.get("professeur_nom", "Inconnu")
        self.classe_nom = course_data.get("classe_nom", "Inconnue")
        self.matiere_nom = course_data.get("matiere_nom", "Inconnue")
        self.salle_nom = course_data.get("salle_nom", "Non spécifiée")
        self.heure_debut = course_data.get("heure", "08:00")
        self.duree = course_data.get("duree", 60)  # en minutes
        
        # Calcul des heures
        self.start_time = self._parse_time(self.heure_debut)
        self.end_time = self.start_time + timedelta(minutes=self.duree)
        
        # État du minuteur
        self.is_running = False
        self.timer_thread = None
        self.current_time = datetime.now()
        self._has_announced_end = False  # éviter les notifications en boucle
        
        # Widgets du minuteur
        self.timer_frame = None
        self.timer_label = None
        self.status_label = None
        
        self.create_timer_widgets()
        self.start_timer()
    
    def _parse_time(self, time_str):
        """Parse une heure au format HH:MM"""
        try:
            hour, minute = map(int, time_str.split(':'))
            today = datetime.now().date()
            return datetime.combine(today, datetime.min.time().replace(hour=hour, minute=minute))
        except:
            return datetime.now().replace(hour=8, minute=0, second=0, microsecond=0)
    
    def create_timer_widgets(self):
        """Crée les widgets du minuteur"""
        # Frame principal du minuteur
        self.timer_frame = ctk.CTkFrame(self.parent, fg_color="transparent")
        
        # Label de l'heure actuelle (gros et visible)
        self.current_time_label = ctk.CTkLabel(
            self.timer_frame,
            text="00:00:00",
            font=("Segoe UI", 20, "bold"),
            text_color="#00D4FF",  # Couleur bleue vive comme 1xBet
            fg_color="transparent"
        )
        self.current_time_label.pack(pady=(5, 2))
        
        # Label du minuteur principal (compte à rebours ou chronomètre)
        self.timer_label = ctk.CTkLabel(
            self.timer_frame,
            text="00:00:00",
            font=("Segoe UI", 16, "bold"),
            text_color="#3FB950",  # Couleur verte par défaut
            fg_color="transparent"
        )
        self.timer_label.pack(pady=(2, 2))
        
        # Label de statut
        self.status_label = ctk.CTkLabel(
            self.timer_frame,
            text="En attente...",
            font=("Segoe UI", 10, "bold"),
            text_color="#8B949E",
            fg_color="transparent"
        )
        self.status_label.pack()
    
    def start_timer(self):
        """Démarre le minuteur"""
        if not self.is_running:
            self.is_running = True
            self.timer_thread = threading.Thread(target=self._timer_loop, daemon=True)
            self.timer_thread.start()
    
    def stop_timer(self):
        """Arrête le minuteur"""
        self.is_running = False
    
    def _timer_loop(self):
        """Boucle principale du minuteur"""
        while self.is_running:
            try:
                # Si le parent ou les widgets n'existent plus, arrêter proprement
                if not self._widget_exists(self.parent) or (self.timer_frame and not self._widget_exists(self.timer_frame)):
                    self.stop_timer()
                    break
                self.current_time = datetime.now()
                self._update_timer()
                time.sleep(1)  # Mise à jour chaque seconde
            except Exception as e:
                print(f"Erreur minuteur: {e}")
                break
    
    def _update_timer(self):
        """Met à jour l'affichage du minuteur"""
        try:
            # Heure actuelle (toujours affichée)
            current_time_text = self.current_time.strftime('%H:%M:%S')
            
            if self.current_time < self.start_time:
                # Compte à rebours avant le début
                time_diff = self.start_time - self.current_time
                hours, remainder = divmod(time_diff.total_seconds(), 3600)
                minutes, seconds = divmod(remainder, 60)
                
                timer_text = f"Démarre dans {int(hours):02d}:{int(minutes):02d}:{int(seconds):02d}"
                status_text = f"Début prévu à {self.start_time.strftime('%H:%M')}"
                
                # Couleur verte pour le compte à rebours
                timer_color = "#3FB950"
                
            elif self.current_time < self.end_time:
                # Chronomètre pendant le cours
                time_diff = self.current_time - self.start_time
                hours, remainder = divmod(time_diff.total_seconds(), 3600)
                minutes, seconds = divmod(remainder, 60)
                
                timer_text = f"En cours depuis {int(hours):02d}:{int(minutes):02d}:{int(seconds):02d}"
                status_text = f"Fin prévue à {self.end_time.strftime('%H:%M')}"
                
                # Couleur bleue pour le chronomètre
                timer_color = "#00D4FF"
                
            else:
                # Cours terminé
                time_diff = self.end_time - self.start_time
                hours, remainder = divmod(time_diff.total_seconds(), 3600)
                minutes, seconds = divmod(remainder, 60)
                
                timer_text = f"Terminé - Durée: {int(hours):02d}:{int(minutes):02d}:{int(seconds):02d}"
                status_text = f"Terminé à {self.end_time.strftime('%H:%M')}"
                
                # Couleur rouge pour terminé
                timer_color = "#F85149"
                
                # Déclencher l'alerte de fin de cours (une seule fois)
                if not self._has_announced_end:
                    self._has_announced_end = True
                    self._trigger_course_end_alert()
                    # Arrêter le minuteur pour éviter les callbacks récurrents
                    self.stop_timer()
            
            # Mise à jour des widgets (thread-safe) si parent existe
            if self._widget_exists(self.parent):
                self.parent.after(0, self._update_widgets, current_time_text, timer_text, status_text, timer_color)
            
        except Exception as e:
            print(f"Erreur mise à jour minuteur: {e}")
    
    def _update_widgets(self, current_time_text, timer_text, status_text, timer_color):
        """Met à jour les widgets de manière thread-safe"""
        try:
            if self.current_time_label and self._widget_exists(self.current_time_label):
                self.current_time_label.configure(text=current_time_text)
            if self.timer_label and self.status_label and self._widget_exists(self.timer_label) and self._widget_exists(self.status_label):
                self.timer_label.configure(text=timer_text, text_color=timer_color)
                self.status_label.configure(text=status_text)
        except Exception as e:
            print(f"Erreur mise à jour widgets: {e}")
    
    def _trigger_course_end_alert(self):
        """Déclenche l'alerte de fin de cours via notifications"""
        try:
            # Ajouter à l'historique des cours terminés
            if self.history_manager:
                try:
                    # éviter les doublons simples consécutifs
                    existing = self.history_manager.get_recent_courses(limit=1)
                    if not existing or existing[-1].get('id') != self.course_data.get('id'):
                        self.history_manager.add_completed_course(self.course_data)
                except Exception:
                    self.history_manager.add_completed_course(self.course_data)
            
            # Utiliser le système de notifications si disponible
            if self.notification_manager:
                self.parent.after(0, lambda: self.notification_manager.add_notification(
                    self.course_data, 
                    "course_end"
                ))
            else:
                # Fallback vers messagebox si pas de notifications manager
                alert_message = f"""🎓 COURS TERMINÉ ! 🎓

📚 Matière: {self.matiere_nom}
👨‍🏫 Professeur: {self.professeur_nom}
🏫 Classe: {self.classe_nom}
🚪 Salle: {self.salle_nom}
⏰ Durée: {self.duree} minutes
🕐 Heure de fin: {self.end_time.strftime('%H:%M')}

Le cours est maintenant terminé."""
                
                self.parent.after(0, lambda: messagebox.showinfo("Cours Terminé", alert_message))
            
            # Callback personnalisé si fourni
            if self.on_course_end and self._widget_exists(self.parent):
                self.parent.after(0, lambda: self.on_course_end(self.course_data))
                
        except Exception as e:
            print(f"Erreur alerte fin de cours: {e}")
    
    def get_timer_info(self):
        """Retourne les informations du minuteur"""
        return {
            "professeurs": self.professeur_nom,
            "classes": self.classe_nom,
            "matieres": self.matiere_nom,
            "salles": self.salle_nom,
            "heure_debut": self.heure_debut,
            "duree": self.duree,
            "heure_fin": self.end_time.strftime('%H:%M'),
            "statut": self._get_current_status()
        }
    
    def _get_current_status(self):
        """Retourne le statut actuel du cours"""
        if self.current_time < self.start_time:
            return "En attente"
        elif self.current_time < self.end_time:
            return "En cours"
        else:
            return "Terminé"
    
    def destroy(self):
        """Nettoie le minuteur"""
        self.stop_timer()
        # Attendre brièvement que le thread s'arrête pour éviter des callbacks tardifs
        try:
            if self.timer_thread and self.timer_thread.is_alive():
                self.timer_thread.join(timeout=0.2)
        except Exception:
            pass
        if self.timer_frame and self._widget_exists(self.timer_frame):
            try:
                self.timer_frame.destroy()
            except Exception:
                pass
        # Libérer les références pour éviter des updates
        self.current_time_label = None
        self.timer_label = None
        self.status_label = None

    def _widget_exists(self, widget):
        try:
            return bool(widget) and widget.winfo_exists()
        except Exception:
            return False

class CourseTimerManager:
    """Gestionnaire global des minuteurs de cours"""
    
    def __init__(self, parent_widget=None):
        self.active_timers = {}
        self.notification_manager = None
        self.history_manager = CourseHistoryManager()
        self._listeners = []  # callbacks on course end
        
        # Créer le gestionnaire de notifications si un parent est fourni
        if parent_widget:
            self.notification_manager = NotificationManager(parent_widget)
    
    def add_timer(self, course_id, parent_widget, course_data):
        """Ajoute un nouveau minuteur"""
        if course_id in self.active_timers:
            self.remove_timer(course_id)
        
        timer = CourseTimer(
            parent_widget, 
            course_data,
            notification_manager=self.notification_manager,
            history_manager=self.history_manager,
            on_course_end=self._on_course_end
        )
        self.active_timers[course_id] = timer
        return timer
    
    def remove_timer(self, course_id):
        """Supprime un minuteur"""
        if course_id in self.active_timers:
            self.active_timers[course_id].destroy()
            del self.active_timers[course_id]
    
    def _on_course_end(self, course_data):
        """Callback appelé à la fin d'un cours"""
        # Notifier les auditeurs inscrits
        try:
            for listener in list(self._listeners):
                try:
                    listener(course_data)
                except Exception as e:
                    print(f"Erreur listener fin de cours: {e}")
        except Exception as e:
            print(f"Erreur notifications des listeners: {e}")

    def add_listener(self, callback):
        """Ajoute un callback appelé quand un cours se termine."""
        if callable(callback) and callback not in self._listeners:
            self._listeners.append(callback)

    def remove_listener(self, callback):
        """Retire un callback inscrit."""
        if callback in self._listeners:
            self._listeners.remove(callback)
    
    def cleanup_all(self):
        """Nettoie tous les minuteurs"""
        for timer in self.active_timers.values():
            timer.destroy()
        self.active_timers.clear()

# Instance globale du gestionnaire
timer_manager = CourseTimerManager()
