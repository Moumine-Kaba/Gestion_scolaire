"""
Vue de la Bibliothèque Numérique
Gestion des documents, supports de cours et partage de fichiers
"""

from database.connection import get_db_connection
from database.connection import get_db_connection
from database.connection import get_db_connection
import customtkinter as ctk
import os
# Remplacé par SQL Server  # Remplacé par SQL Server
from pathlib import Path
from tkinter import filedialog, messagebox
import shutil
from datetime import datetime

# Import du thème global
from resources.themes.theme import *

class BibliothequeView(ctk.CTkFrame):
    def __init__(self, parent, utilisateurs):
        super().__init__(parent, fg_color="transparent")
        self.utilisateurs = utilisateurs
        self.documents_dir = Path("resources/documents")
        self.documents_dir.mkdir(exist_ok=True)
        
        # Créer la table des documents si elle n'existe pas
        self._init_database()
        
        self.create_interface()
        self.load_documents()
    
    def _init_database(self):
        """Initialise la base de données pour les documents"""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS documents (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nom TEXT NOT NULL,
                    description TEXT,
                    chemin TEXT NOT NULL,
                    type_document TEXT,
                    taille INTEGER,
                    date_upload DATETIME DEFAULT CURRENT_TIMESTAMP,
                    uploader_id INTEGER,
                    categorie TEXT,
                    tags TEXT,
                    is_public BOOLEAN DEFAULT 1
                )
            """)
            conn.commit()
            conn.close()
        except Exception as e:
            print(f"⚠️ Erreur initialisation DB bibliothèque: {e}")
    
    def create_interface(self):
        """Crée l'interface de la bibliothèque"""
        # En-tête
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.pack(fill="x", pady=(0, 20))
        
        # Titre
        title_label = ctk.CTkLabel(
            header_frame,
            text="📚 Bibliothèque Numérique",
            font=(FONT, FS_HEADER, "bold"),
            text_color=ACCENT
        )
        title_label.pack(side="left")
        
        # Boutons d'action
        actions_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        actions_frame.pack(side="right")
        
        # Bouton upload
        upload_btn = ctk.CTkButton(
            actions_frame,
            text="📤 Uploader",
            font=(FONT, FS_TEXT, "bold"),
            fg_color=ACCENT,
            hover_color=HOVER_PRIMARY,
            corner_radius=8,
            height=35,
            command=self.upload_document
        )
        upload_btn.pack(side="left", padx=(0, 10))
        
        # Bouton créer dossier
        folder_btn = ctk.CTkButton(
            actions_frame,
            text="📁 Nouveau Dossier",
            font=(FONT, FS_TEXT, "bold"),
            fg_color=CARD_BG,
            hover_color=HOVER,
            corner_radius=8,
            height=35,
            command=self.create_folder
        )
        folder_btn.pack(side="left", padx=(0, 10))
        
        # Barre de recherche
        search_frame = ctk.CTkFrame(self, fg_color="transparent")
        search_frame.pack(fill="x", pady=(0, 15))
        
        search_icon = ctk.CTkLabel(
            search_frame,
            text="🔍",
            font=(FONT, FS_TEXT)
        )
        search_icon.pack(side="left", padx=(0, 10))
        
        self.search_entry = ctk.CTkEntry(
            search_frame,
            placeholder_text="Rechercher dans la bibliothèque...",
            font=(FONT, FS_TEXT),
            height=35,
            corner_radius=8,
            fg_color=CARD_BG,
            text_color=TEXT,
            placeholder_text_color=MUTED,
            border_width=1,
            border_color=BORDER_COLOR
        )
        self.search_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))
        self.search_entry.bind("<KeyRelease>", self.search_documents)
        
        # Filtres
        filter_frame = ctk.CTkFrame(search_frame, fg_color="transparent")
        filter_frame.pack(side="right")
        
        self.category_filter = ctk.CTkComboBox(
            filter_frame,
            values=["Toutes", "Cours", "Exercices", "Examens", "Ressources", "Autres"],
            font=(FONT, FS_TEXT-1),
            height=35,
            corner_radius=8,
            fg_color=CARD_BG,
            text_color=TEXT,
            border_color=BORDER_COLOR,
            command=self.filter_documents
        )
        self.category_filter.set("Toutes")
        self.category_filter.pack(side="left", padx=(0, 10))
        
        # Zone principale
        main_frame = ctk.CTkFrame(self, fg_color="transparent")
        main_frame.pack(fill="both", expand=True)
        main_frame.grid_columnconfigure(0, weight=1)
        main_frame.grid_rowconfigure(0, weight=1)
        
        # Liste des documents
        self.documents_frame = ctk.CTkScrollableFrame(
            main_frame,
            fg_color=CARD_BG,
            corner_radius=12,
            border_width=1,
            border_color=BORDER_COLOR
        )
        self.documents_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        
        # Panneau de détails
        self.details_frame = ctk.CTkFrame(
            main_frame,
            fg_color=CARD_BG,
            corner_radius=12,
            border_width=1,
            border_color=BORDER_COLOR,
            width=300
        )
        self.details_frame.grid(row=0, column=1, sticky="nsew")
        self.details_frame.grid_propagate(False)
        
        # Titre du panneau de détails
        details_title = ctk.CTkLabel(
            self.details_frame,
            text="📋 Détails du Document",
            font=(FONT, FS_SUBHDR, "bold"),
            text_color=TEXT
        )
        details_title.pack(pady=(15, 10))
        
        # Contenu des détails
        self.details_content = ctk.CTkFrame(
            self.details_frame,
            fg_color="transparent"
        )
        self.details_content.pack(fill="both", expand=True, padx=15, pady=(0, 15))
    
    def upload_document(self):
        """Upload un nouveau document"""
        file_path = filedialog.askopenfilename(
            title="Sélectionner un document",
            filetypes=[
                ("Tous les fichiers", "*.*"),
                ("Documents PDF", "*.pdf"),
                ("Documents Word", "*.docx;*.doc"),
                ("Présentations", "*.pptx;*.ppt"),
                ("Images", "*.png;*.jpg;*.jpeg"),
                ("Vidéos", "*.mp4;*.avi;*.mov"),
                ("Audios", "*.mp3;*.wav;*.m4a")
            ]
        )
        
        if file_path:
            self._process_upload(file_path)
    
    def _process_upload(self, file_path):
        """Traite l'upload d'un fichier"""
        try:
            # Fenêtre de configuration du document
            config_window = ctk.CTkToplevel(self)
            config_window.title("Configuration du Document")
            config_window.geometry("500x400")
            config_window.configure(fg_color=BG_MAIN)
            config_window.transient(self)
            config_window.grab_set()
            
            # Centrer la fenêtre
            config_window.update_idletasks()
            x = (config_window.winfo_screenwidth() // 2) - (500 // 2)
            y = (config_window.winfo_screenheight() // 2) - (400 // 2)
            config_window.geometry(f"500x400+{x}+{y}")
            
            # Contenu de la fenêtre
            content_frame = ctk.CTkFrame(config_window, fg_color=CARD_BG, corner_radius=12)
            content_frame.pack(fill="both", expand=True, padx=20, pady=20)
            
            # Titre
            title_label = ctk.CTkLabel(
                content_frame,
                text="📤 Configuration du Document",
                font=(FONT, FS_HEADER, "bold"),
                text_color=ACCENT
            )
            title_label.pack(pady=(20, 20))
            
            # Nom du fichier
            filename = os.path.basename(file_path)
            filename_label = ctk.CTkLabel(
                content_frame,
                text=f"Fichier: {filename}",
                font=(FONT, FS_TEXT),
                text_color=TEXT
            )
            filename_label.pack(pady=(0, 15))
            
            # Nom personnalisé
            ctk.CTkLabel(
                content_frame,
                text="Nom du document:",
                font=(FONT, FS_TEXT, "bold"),
                text_color=TEXT
            ).pack(anchor="w", padx=20)
            
            name_entry = ctk.CTkEntry(
                content_frame,
                placeholder_text="Nom du document...",
                font=(FONT, FS_TEXT),
                height=35,
                corner_radius=8,
                fg_color=CARD_INNER,
                text_color=TEXT,
                placeholder_text_color=MUTED
            )
            name_entry.pack(fill="x", padx=20, pady=(5, 15))
            name_entry.insert(0, os.path.splitext(filename)[0])
            
            # Description
            ctk.CTkLabel(
                content_frame,
                text="Description:",
                font=(FONT, FS_TEXT, "bold"),
                text_color=TEXT
            ).pack(anchor="w", padx=20)
            
            desc_text = ctk.CTkTextbox(
                content_frame,
                height=80,
                corner_radius=8,
                fg_color=CARD_INNER,
                text_color=TEXT,
                font=(FONT, FS_TEXT-1)
            )
            desc_text.pack(fill="x", padx=20, pady=(5, 15))
            
            # Catégorie
            ctk.CTkLabel(
                content_frame,
                text="Catégorie:",
                font=(FONT, FS_TEXT, "bold"),
                text_color=TEXT
            ).pack(anchor="w", padx=20)
            
            category_combo = ctk.CTkComboBox(
                content_frame,
                values=["Cours", "Exercices", "Examens", "Ressources", "Autres"],
                font=(FONT, FS_TEXT),
                height=35,
                corner_radius=8,
                fg_color=CARD_INNER,
                text_color=TEXT
            )
            category_combo.pack(fill="x", padx=20, pady=(5, 15))
            category_combo.set("Cours")
            
            # Tags
            ctk.CTkLabel(
                content_frame,
                text="Tags (séparés par des virgules):",
                font=(FONT, FS_TEXT, "bold"),
                text_color=TEXT
            ).pack(anchor="w", padx=20)
            
            tags_entry = ctk.CTkEntry(
                content_frame,
                placeholder_text="mathématiques, algèbre, exercices...",
                font=(FONT, FS_TEXT),
                height=35,
                corner_radius=8,
                fg_color=CARD_INNER,
                text_color=TEXT,
                placeholder_text_color=MUTED
            )
            tags_entry.pack(fill="x", padx=20, pady=(5, 20))
            
            # Boutons
            buttons_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
            buttons_frame.pack(fill="x", padx=20, pady=(0, 20))
            
            def save_document():
                self._save_document_to_db(
                    file_path,
                    name_entry.get() or filename,
                    desc_text.get("1.0", "end-1c"),
                    category_combo.get(),
                    tags_entry.get(),
                    config_window
                )
            
            save_btn = ctk.CTkButton(
                buttons_frame,
                text="💾 Sauvegarder",
                font=(FONT, FS_TEXT, "bold"),
                fg_color=ACCENT,
                hover_color=HOVER_PRIMARY,
                corner_radius=8,
                height=35,
                command=save_document
            )
            save_btn.pack(side="left", padx=(0, 10))
            
            cancel_btn = ctk.CTkButton(
                buttons_frame,
                text="❌ Annuler",
                font=(FONT, FS_TEXT, "bold"),
                fg_color=CARD_BG,
                hover_color=HOVER,
                corner_radius=8,
                height=35,
                command=config_window.destroy
            )
            cancel_btn.pack(side="left")
            
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de l'upload: {e}")
    
    def _save_document_to_db(self, file_path, name, description, category, tags, window):
        """Sauvegarde le document dans la base de données"""
        try:
            # Copier le fichier vers le dossier documents
            filename = os.path.basename(file_path)
            file_extension = os.path.splitext(filename)[1]
            safe_filename = f"{name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}{file_extension}"
            dest_path = self.documents_dir / safe_filename
            
            shutil.copy2(file_path, dest_path)
            
            # Obtenir la taille du fichier
            file_size = os.path.getsize(dest_path)
            
            # Sauvegarder dans la base de données
            conn = get_db_connection()
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT INTO documents (nom, description, chemin, type_document, taille, 
                                     uploader_id, categorie, tags, is_public)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                name,
                description,
                str(dest_path),
                file_extension,
                file_size,
                self.utilisateurs.get('id', 1),
                category,
                tags,
                1
            ))
            
            conn.commit()
            conn.close()
            
            window.destroy()
            messagebox.showinfo("Succès", f"Document '{name}' uploadé avec succès!")
            self.load_documents()
            
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de la sauvegarde: {e}")
    
    def create_folder(self):
        """Crée un nouveau dossier"""
        folder_name = ctk.CTkInputDialog(
            text="Nom du dossier:",
            title="Nouveau Dossier"
        ).get_input()
        
        if folder_name:
            try:
                folder_path = self.documents_dir / folder_name
                folder_path.mkdir(exist_ok=True)
                messagebox.showinfo("Succès", f"Dossier '{folder_name}' créé avec succès!")
                self.load_documents()
            except Exception as e:
                messagebox.showerror("Erreur", f"Erreur lors de la création du dossier: {e}")
    
    def load_documents(self):
        """Charge et affiche les documents"""
        # Nettoyer la liste actuelle
        for widget in self.documents_frame.winfo_children():
            widget.destroy()
        
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id, nom, description, type_document, taille, date_upload, 
                       categorie, tags, uploader_id
                FROM documents 
                ORDER BY date_upload DESC
            """)
            
            documents = cursor.fetchall()
            conn.close()
            
            if not documents:
                # Message si aucun document
                no_docs_label = ctk.CTkLabel(
                    self.documents_frame,
                    text="📭 Aucun document dans la bibliothèque",
                    font=(FONT, FS_TEXT),
                    text_color=MUTED
                )
                no_docs_label.pack(pady=50)
                return
            
            # Afficher les documents
            for doc in documents:
                self._create_document_card(doc)
                
        except Exception as e:
            print(f"⚠️ Erreur chargement documents: {e}")
    
    def _create_document_card(self, doc):
        """Crée une carte pour un document"""
        doc_id, nom, description, type_doc, taille, date_upload, categorie, tags, uploader_id = doc
        
        # Carte du document
        card = ctk.CTkFrame(
            self.documents_frame,
            fg_color=CARD_INNER,
            corner_radius=10,
            border_width=1,
            border_color=BORDER_COLOR
        )
        card.pack(fill="x", pady=5, padx=10)
        
        # Contenu de la carte
        content_frame = ctk.CTkFrame(card, fg_color="transparent")
        content_frame.pack(fill="x", padx=15, pady=10)
        
        # En-tête de la carte
        header_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        header_frame.pack(fill="x", pady=(0, 8))
        
        # Icône du type de document
        type_icon = self._get_document_icon(type_doc)
        icon_label = ctk.CTkLabel(
            header_frame,
            text=type_icon,
            font=(FONT, 20)
        )
        icon_label.pack(side="left", padx=(0, 10))
        
        # Nom et catégorie
        info_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        info_frame.pack(side="left", fill="x", expand=True)
        
        name_label = ctk.CTkLabel(
            info_frame,
            text=nom,
            font=(FONT, FS_TEXT, "bold"),
            text_color=TEXT
        )
        name_label.pack(anchor="w")
        
        category_label = ctk.CTkLabel(
            info_frame,
            text=f"📁 {categorie}",
            font=(FONT, FS_TEXT-2),
            text_color=MUTED
        )
        category_label.pack(anchor="w")
        
        # Boutons d'action
        actions_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        actions_frame.pack(side="right")
        
        # Bouton télécharger
        download_btn = ctk.CTkButton(
            actions_frame,
            text="⬇️",
            width=30,
            height=30,
            corner_radius=6,
            fg_color=ACCENT,
            hover_color=HOVER_PRIMARY,
            command=lambda: self.download_document(doc_id)
        )
        download_btn.pack(side="left", padx=(0, 5))
        
        # Bouton supprimer (si admin ou propriétaire)
        if self._can_delete_document(uploader_id):
            delete_btn = ctk.CTkButton(
                actions_frame,
                text="🗑️",
                width=30,
                height=30,
                corner_radius=6,
                fg_color=DANGER,
                hover_color="#A34646",
                command=lambda: self.delete_document(doc_id)
            )
            delete_btn.pack(side="left")
        
        # Description
        if description:
            desc_label = ctk.CTkLabel(
                content_frame,
                text=description[:100] + "..." if len(description) > 100 else description,
                font=(FONT, FS_TEXT-1),
                text_color=MUTED,
                wraplength=400
            )
            desc_label.pack(anchor="w", pady=(0, 5))
        
        # Tags
        if tags:
            tags_label = ctk.CTkLabel(
                content_frame,
                text=f"🏷️ {tags}",
                font=(FONT, FS_TEXT-2),
                text_color=MUTED
            )
            tags_label.pack(anchor="w", pady=(0, 5))
        
        # Informations du fichier
        file_info = ctk.CTkLabel(
            content_frame,
            text=f"📊 {self._format_file_size(taille)} • 📅 {date_upload[:10]}",
            font=(FONT, FS_TEXT-2),
            text_color=MUTED
        )
        file_info.pack(anchor="w")
        
        # Bind pour afficher les détails
        card.bind("<Button-1>", lambda e, doc_id=doc_id: self.show_document_details(doc_id))
        for child in card.winfo_children():
            child.bind("<Button-1>", lambda e, doc_id=doc_id: self.show_document_details(doc_id))
    
    def _get_document_icon(self, file_type):
        """Retourne l'icône appropriée selon le type de fichier"""
        icons = {
            '.pdf': '📄',
            '.doc': '📝',
            '.docx': '📝',
            '.ppt': '📊',
            '.pptx': '📊',
            '.png': '🖼️',
            '.jpg': '🖼️',
            '.jpeg': '🖼️',
            '.mp4': '🎥',
            '.avi': '🎥',
            '.mov': '🎥',
            '.mp3': '🎵',
            '.wav': '🎵',
            '.m4a': '🎵',
            '.txt': '📄',
            '.zip': '📦',
            '.rar': '📦'
        }
        return icons.get(file_type.lower(), '📄')
    
    def _format_file_size(self, size_bytes):
        """Formate la taille du fichier"""
        if size_bytes < 1024:
            return f"{size_bytes} B"
        elif size_bytes < 1024 * 1024:
            return f"{size_bytes / 1024:.1f} KB"
        elif size_bytes < 1024 * 1024 * 1024:
            return f"{size_bytes / (1024 * 1024):.1f} MB"
        else:
            return f"{size_bytes / (1024 * 1024 * 1024):.1f} GB"
    
    def _can_delete_document(self, uploader_id):
        """Vérifie si l'utilisateurs peut supprimer le document"""
        user_role = self.utilisateurs.get('roles', '').lower()
        user_id = self.utilisateurs.get('id', 0)
        return user_role == 'administrateur' or user_id == uploader_id
    
    def download_document(self, doc_id):
        """Télécharge un document"""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT nom, chemin FROM documents WHERE id = ?", (doc_id,))
            result = cursor.fetchone()
            conn.close()
            
            if result:
                nom, chemin = result
                # Ouvrir le fichier avec l'application par défaut
                os.startfile(chemin)
            else:
                messagebox.showerror("Erreur", "Document introuvable")
                
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors du téléchargement: {e}")
    
    def delete_document(self, doc_id):
        """Supprime un document"""
        if messagebox.askyesno("Confirmation", "Êtes-vous sûr de vouloir supprimer ce document ?"):
            try:
                conn = get_db_connection()
                cursor = conn.cursor()
                cursor.execute("SELECT chemin FROM documents WHERE id = ?", (doc_id,))
                result = cursor.fetchone()
                
                if result:
                    # Supprimer le fichier
                    file_path = result[0]
                    if os.path.exists(file_path):
                        os.remove(file_path)
                    
                    # Supprimer de la base de données
                    cursor.execute("DELETE FROM documents WHERE id = ?", (doc_id,))
                    conn.commit()
                    
                    messagebox.showinfo("Succès", "Document supprimé avec succès!")
                    self.load_documents()
                
                conn.close()
                
            except Exception as e:
                messagebox.showerror("Erreur", f"Erreur lors de la suppression: {e}")
    
    def show_document_details(self, doc_id):
        """Affiche les détails d'un document"""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT nom, description, type_document, taille, date_upload, 
                       categorie, tags, uploader_id
                FROM documents WHERE id = ?
            """, (doc_id,))
            result = cursor.fetchone()
            conn.close()
            
            if result:
                # Nettoyer le panneau de détails
                for widget in self.details_content.winfo_children():
                    widget.destroy()
                
                nom, description, type_doc, taille, date_upload, categorie, tags, uploader_id = result
                
                # Afficher les détails
                details = [
                    ("📄 Nom", nom),
                    ("📁 Catégorie", categorie),
                    ("📊 Taille", self._format_file_size(taille)),
                    ("📅 Date d'upload", date_upload[:16]),
                    ("👤 Uploadé par", f"Utilisateur {uploader_id}"),
                ]
                
                if description:
                    details.append(("📝 Description", description))
                
                if tags:
                    details.append(("🏷️ Tags", tags))
                
                for label, value in details:
                    detail_frame = ctk.CTkFrame(self.details_content, fg_color="transparent")
                    detail_frame.pack(fill="x", pady=5)
                    
                    label_widget = ctk.CTkLabel(
                        detail_frame,
                        text=label,
                        font=(FONT, FS_TEXT-1, "bold"),
                        text_color=ACCENT
                    )
                    label_widget.pack(anchor="w")
                    
                    value_widget = ctk.CTkLabel(
                        detail_frame,
                        text=str(value),
                        font=(FONT, FS_TEXT-1),
                        text_color=TEXT,
                        wraplength=250
                    )
                    value_widget.pack(anchor="w", padx=(10, 0))
                
        except Exception as e:
            print(f"⚠️ Erreur affichage détails: {e}")
    
    def search_documents(self, event=None):
        """Recherche dans les documents"""
        query = self.search_entry.get().strip().lower()
        # Implémentation de la recherche (à compléter)
        pass
    
    def filter_documents(self, category):
        """Filtre les documents par catégorie"""
        # Implémentation du filtrage (à compléter)
        pass

