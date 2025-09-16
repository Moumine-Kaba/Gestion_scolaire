"""
Vue de la Messagerie Interne
Système de communication entre professeurs, élèves et administration
"""

import customtkinter as ctk
import sqlite3
from datetime import datetime
from tkinter import messagebox

# Import du thème global
from resources.themes.theme import *

class MessagerieView(ctk.CTkFrame):
    def __init__(self, parent, utilisateur):
        super().__init__(parent, fg_color="transparent")
        self.utilisateur = utilisateur
        self.current_conversation = None
        
        # Créer la table des messages si elle n'existe pas
        self._init_database()
        
        self.create_interface()
        self.load_conversations()
    
    def _init_database(self):
        """Initialise la base de données pour les messages"""
        try:
            conn = sqlite3.connect("database/edumanager.db")
            cursor = conn.cursor()
            
            # Table des conversations
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS conversations (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    sujet TEXT NOT NULL,
                    type_conversation TEXT DEFAULT 'general',
                    date_creation DATETIME DEFAULT CURRENT_TIMESTAMP,
                    derniere_activite DATETIME DEFAULT CURRENT_TIMESTAMP,
                    is_active BOOLEAN DEFAULT 1
                )
            """)
            
            # Table des participants aux conversations
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS conversation_participants (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    conversation_id INTEGER,
                    user_id INTEGER,
                    role TEXT,
                    date_ajout DATETIME DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (conversation_id) REFERENCES conversations (id)
                )
            """)
            
            # Table des messages
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS messages (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    conversation_id INTEGER,
                    sender_id INTEGER,
                    contenu TEXT NOT NULL,
                    date_envoi DATETIME DEFAULT CURRENT_TIMESTAMP,
                    is_lu BOOLEAN DEFAULT 0,
                    type_message TEXT DEFAULT 'text',
                    FOREIGN KEY (conversation_id) REFERENCES conversations (id)
                )
            """)
            
            conn.commit()
            conn.close()
        except Exception as e:
            print(f"⚠️ Erreur initialisation DB messagerie: {e}")
    
    def create_interface(self):
        """Crée l'interface de la messagerie"""
        # En-tête
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.pack(fill="x", pady=(0, 20))
        
        # Titre
        title_label = ctk.CTkLabel(
            header_frame,
            text="💬 Messagerie Interne",
            font=(FONT, FS_HEADER, "bold"),
            text_color=ACCENT
        )
        title_label.pack(side="left")
        
        # Bouton nouvelle conversation
        new_conv_btn = ctk.CTkButton(
            header_frame,
            text="➕ Nouvelle Conversation",
            font=(FONT, FS_TEXT, "bold"),
            fg_color=ACCENT,
            hover_color=HOVER_PRIMARY,
            corner_radius=8,
            height=35,
            command=self.create_new_conversation
        )
        new_conv_btn.pack(side="right")
        
        # Zone principale
        main_frame = ctk.CTkFrame(self, fg_color="transparent")
        main_frame.pack(fill="both", expand=True)
        main_frame.grid_columnconfigure(0, weight=1)
        main_frame.grid_columnconfigure(1, weight=2)
        main_frame.grid_rowconfigure(0, weight=1)
        
        # Panneau des conversations
        self.conversations_frame = ctk.CTkFrame(
            main_frame,
            fg_color=CARD_BG,
            corner_radius=12,
            border_width=1,
            border_color=BORDER_COLOR,
            width=300
        )
        self.conversations_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        self.conversations_frame.grid_propagate(False)
        
        # Titre du panneau des conversations
        conv_title = ctk.CTkLabel(
            self.conversations_frame,
            text="📋 Conversations",
            font=(FONT, FS_SUBHDR, "bold"),
            text_color=TEXT
        )
        conv_title.pack(pady=(15, 10))
        
        # Liste des conversations
        self.conv_list_frame = ctk.CTkScrollableFrame(
            self.conversations_frame,
            fg_color="transparent"
        )
        self.conv_list_frame.pack(fill="both", expand=True, padx=15, pady=(0, 15))
        
        # Panneau de conversation
        self.chat_frame = ctk.CTkFrame(
            main_frame,
            fg_color=CARD_BG,
            corner_radius=12,
            border_width=1,
            border_color=BORDER_COLOR
        )
        self.chat_frame.grid(row=0, column=1, sticky="nsew")
        
        # En-tête de la conversation
        self.chat_header = ctk.CTkFrame(
            self.chat_frame,
            fg_color="transparent"
        )
        self.chat_header.pack(fill="x", padx=15, pady=(15, 10))
        
        # Zone des messages
        self.messages_frame = ctk.CTkScrollableFrame(
            self.chat_frame,
            fg_color="transparent"
        )
        self.messages_frame.pack(fill="both", expand=True, padx=15, pady=(0, 10))
        
        # Zone de saisie
        self.input_frame = ctk.CTkFrame(
            self.chat_frame,
            fg_color="transparent"
        )
        self.input_frame.pack(fill="x", padx=15, pady=(0, 15))
        
        # Champ de saisie
        self.message_entry = ctk.CTkTextbox(
            self.input_frame,
            height=60,
            corner_radius=8,
            fg_color=CARD_INNER,
            text_color=TEXT,
            font=(FONT, FS_TEXT),
            placeholder_text="Tapez votre message..."
        )
        self.message_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))
        
        # Bouton d'envoi
        send_btn = ctk.CTkButton(
            self.input_frame,
            text="📤",
            width=50,
            height=60,
            corner_radius=8,
            fg_color=ACCENT,
            hover_color=HOVER_PRIMARY,
            command=self.send_message
        )
        send_btn.pack(side="right")
        
        # Message par défaut
        self.show_welcome_message()
    
    def show_welcome_message(self):
        """Affiche le message de bienvenue"""
        welcome_label = ctk.CTkLabel(
            self.messages_frame,
            text="👋 Bienvenue dans la messagerie interne!\n\nSélectionnez une conversation ou créez-en une nouvelle pour commencer.",
            font=(FONT, FS_TEXT),
            text_color=MUTED,
            justify="center"
        )
        welcome_label.pack(expand=True, fill="both")
    
    def load_conversations(self):
        """Charge la liste des conversations"""
        # Nettoyer la liste actuelle
        for widget in self.conv_list_frame.winfo_children():
            widget.destroy()
        
        try:
            conn = sqlite3.connect("database/edumanager.db")
            cursor = conn.cursor()
            
            # Récupérer les conversations où l'utilisateur est participant
            cursor.execute("""
                SELECT DISTINCT c.id, c.sujet, c.derniere_activite, c.type_conversation
                FROM conversations c
                JOIN conversation_participants cp ON c.id = cp.conversation_id
                WHERE cp.user_id = ? AND c.is_active = 1
                ORDER BY c.derniere_activite DESC
            """, (self.utilisateur.get('id', 1),))
            
            conversations = cursor.fetchall()
            conn.close()
            
            if not conversations:
                # Message si aucune conversation
                no_conv_label = ctk.CTkLabel(
                    self.conv_list_frame,
                    text="📭 Aucune conversation",
                    font=(FONT, FS_TEXT),
                    text_color=MUTED
                )
                no_conv_label.pack(pady=20)
                return
            
            # Afficher les conversations
            for conv in conversations:
                self._create_conversation_card(conv)
                
        except Exception as e:
            print(f"⚠️ Erreur chargement conversations: {e}")
    
    def _create_conversation_card(self, conv):
        """Crée une carte pour une conversation"""
        conv_id, sujet, derniere_activite, type_conv = conv
        
        # Carte de conversation
        card = ctk.CTkFrame(
            self.conv_list_frame,
            fg_color=CARD_INNER,
            corner_radius=8,
            border_width=1,
            border_color=BORDER_COLOR
        )
        card.pack(fill="x", pady=3, padx=5)
        
        # Contenu de la carte
        content_frame = ctk.CTkFrame(card, fg_color="transparent")
        content_frame.pack(fill="x", padx=10, pady=8)
        
        # Sujet
        sujet_label = ctk.CTkLabel(
            content_frame,
            text=sujet,
            font=(FONT, FS_TEXT, "bold"),
            text_color=TEXT
        )
        sujet_label.pack(anchor="w")
        
        # Type et date
        info_label = ctk.CTkLabel(
            content_frame,
            text=f"📅 {derniere_activite[:16]}",
            font=(FONT, FS_TEXT-2),
            text_color=MUTED
        )
        info_label.pack(anchor="w")
        
        # Bind pour ouvrir la conversation
        card.bind("<Button-1>", lambda e, conv_id=conv_id: self.open_conversation(conv_id))
        for child in card.winfo_children():
            child.bind("<Button-1>", lambda e, conv_id=conv_id: self.open_conversation(conv_id))
    
    def open_conversation(self, conv_id):
        """Ouvre une conversation"""
        self.current_conversation = conv_id
        self.load_messages(conv_id)
        self.update_conversation_header(conv_id)
    
    def load_messages(self, conv_id):
        """Charge les messages d'une conversation"""
        # Nettoyer la zone des messages
        for widget in self.messages_frame.winfo_children():
            widget.destroy()
        
        try:
            conn = sqlite3.connect("database/edumanager.db")
            cursor = conn.cursor()
            
            # Récupérer les messages
            cursor.execute("""
                SELECT m.id, m.sender_id, m.contenu, m.date_envoi, m.is_lu
                FROM messages m
                WHERE m.conversation_id = ?
                ORDER BY m.date_envoi ASC
            """, (conv_id,))
            
            messages = cursor.fetchall()
            conn.close()
            
            if not messages:
                # Message si aucun message
                no_msg_label = ctk.CTkLabel(
                    self.messages_frame,
                    text="📭 Aucun message dans cette conversation",
                    font=(FONT, FS_TEXT),
                    text_color=MUTED
                )
                no_msg_label.pack(pady=20)
                return
            
            # Afficher les messages
            for msg in messages:
                self._create_message_bubble(msg)
                
        except Exception as e:
            print(f"⚠️ Erreur chargement messages: {e}")
    
    def _create_message_bubble(self, msg):
        """Crée une bulle de message"""
        msg_id, sender_id, contenu, date_envoi, is_lu = msg
        
        # Déterminer si c'est notre message
        is_own_message = sender_id == self.utilisateur.get('id', 1)
        
        # Conteneur du message
        msg_container = ctk.CTkFrame(
            self.messages_frame,
            fg_color="transparent"
        )
        msg_container.pack(fill="x", pady=5)
        
        # Aligner selon l'expéditeur
        if is_own_message:
            msg_container.pack(anchor="e")
            bubble_color = ACCENT
            text_color = BG_MAIN
        else:
            msg_container.pack(anchor="w")
            bubble_color = CARD_INNER
            text_color = TEXT
        
        # Bulle de message
        bubble = ctk.CTkFrame(
            msg_container,
            fg_color=bubble_color,
            corner_radius=12,
            border_width=1,
            border_color=BORDER_COLOR
        )
        bubble.pack(fill="x", padx=10 if is_own_message else 50, pady=2)
        
        # Contenu du message
        content_frame = ctk.CTkFrame(bubble, fg_color="transparent")
        content_frame.pack(fill="x", padx=12, pady=8)
        
        # Texte du message
        message_label = ctk.CTkLabel(
            content_frame,
            text=contenu,
            font=(FONT, FS_TEXT),
            text_color=text_color,
            wraplength=300,
            justify="left"
        )
        message_label.pack(anchor="w")
        
        # Date et statut
        date_label = ctk.CTkLabel(
            content_frame,
            text=f"📅 {date_envoi[:16]}",
            font=(FONT, FS_TEXT-2),
            text_color=text_color
        )
        date_label.pack(anchor="e", pady=(5, 0))
    
    def update_conversation_header(self, conv_id):
        """Met à jour l'en-tête de la conversation"""
        # Nettoyer l'en-tête
        for widget in self.chat_header.winfo_children():
            widget.destroy()
        
        try:
            conn = sqlite3.connect("database/edumanager.db")
            cursor = conn.cursor()
            
            # Récupérer les infos de la conversation
            cursor.execute("""
                SELECT sujet, type_conversation
                FROM conversations
                WHERE id = ?
            """, (conv_id,))
            
            result = cursor.fetchone()
            conn.close()
            
            if result:
                sujet, type_conv = result
                
                # Titre de la conversation
                title_label = ctk.CTkLabel(
                    self.chat_header,
                    text=f"💬 {sujet}",
                    font=(FONT, FS_SUBHDR, "bold"),
                    text_color=TEXT
                )
                title_label.pack(side="left")
                
                # Type de conversation
                type_label = ctk.CTkLabel(
                    self.chat_header,
                    text=f"📋 {type_conv}",
                    font=(FONT, FS_TEXT-1),
                    text_color=MUTED
                )
                type_label.pack(side="right")
                
        except Exception as e:
            print(f"⚠️ Erreur mise à jour en-tête: {e}")
    
    def send_message(self):
        """Envoie un message"""
        if not self.current_conversation:
            messagebox.showwarning("Attention", "Veuillez sélectionner une conversation")
            return
        
        message_text = self.message_entry.get("1.0", "end-1c").strip()
        if not message_text:
            messagebox.showwarning("Attention", "Veuillez saisir un message")
            return
        
        try:
            conn = sqlite3.connect("database/edumanager.db")
            cursor = conn.cursor()
            
            # Insérer le message
            cursor.execute("""
                INSERT INTO messages (conversation_id, sender_id, contenu)
                VALUES (?, ?, ?)
            """, (self.current_conversation, self.utilisateur.get('id', 1), message_text))
            
            # Mettre à jour la dernière activité
            cursor.execute("""
                UPDATE conversations
                SET derniere_activite = CURRENT_TIMESTAMP
                WHERE id = ?
            """, (self.current_conversation,))
            
            conn.commit()
            conn.close()
            
            # Vider le champ de saisie
            self.message_entry.delete("1.0", "end")
            
            # Recharger les messages
            self.load_messages(self.current_conversation)
            self.load_conversations()  # Pour mettre à jour la liste
            
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de l'envoi: {e}")
    
    def create_new_conversation(self):
        """Crée une nouvelle conversation"""
        # Fenêtre de création de conversation
        conv_window = ctk.CTkToplevel(self)
        conv_window.title("Nouvelle Conversation")
        conv_window.geometry("500x300")
        conv_window.configure(fg_color=BG_MAIN)
        conv_window.transient(self)
        conv_window.grab_set()
        
        # Centrer la fenêtre
        conv_window.update_idletasks()
        x = (conv_window.winfo_screenwidth() // 2) - (500 // 2)
        y = (conv_window.winfo_screenheight() // 2) - (300 // 2)
        conv_window.geometry(f"500x300+{x}+{y}")
        
        # Contenu de la fenêtre
        content_frame = ctk.CTkFrame(conv_window, fg_color=CARD_BG, corner_radius=12)
        content_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Titre
        title_label = ctk.CTkLabel(
            content_frame,
            text="💬 Nouvelle Conversation",
            font=(FONT, FS_HEADER, "bold"),
            text_color=ACCENT
        )
        title_label.pack(pady=(20, 20))
        
        # Sujet
        ctk.CTkLabel(
            content_frame,
            text="Sujet de la conversation:",
            font=(FONT, FS_TEXT, "bold"),
            text_color=TEXT
        ).pack(anchor="w", padx=20)
        
        sujet_entry = ctk.CTkEntry(
            content_frame,
            placeholder_text="Sujet de la conversation...",
            font=(FONT, FS_TEXT),
            height=35,
            corner_radius=8,
            fg_color=CARD_INNER,
            text_color=TEXT,
            placeholder_text_color=MUTED
        )
        sujet_entry.pack(fill="x", padx=20, pady=(5, 15))
        
        # Type de conversation
        ctk.CTkLabel(
            content_frame,
            text="Type de conversation:",
            font=(FONT, FS_TEXT, "bold"),
            text_color=TEXT
        ).pack(anchor="w", padx=20)
        
        type_combo = ctk.CTkComboBox(
            content_frame,
            values=["Général", "Pédagogique", "Administratif", "Urgent"],
            font=(FONT, FS_TEXT),
            height=35,
            corner_radius=8,
            fg_color=CARD_INNER,
            text_color=TEXT
        )
        type_combo.pack(fill="x", padx=20, pady=(5, 20))
        type_combo.set("Général")
        
        # Boutons
        buttons_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        buttons_frame.pack(fill="x", padx=20, pady=(0, 20))
        
        def create_conversation():
            sujet = sujet_entry.get().strip()
            if not sujet:
                messagebox.showwarning("Attention", "Veuillez saisir un sujet")
                return
            
            try:
                conn = sqlite3.connect("database/edumanager.db")
                cursor = conn.cursor()
                
                # Créer la conversation
                cursor.execute("""
                    INSERT INTO conversations (sujet, type_conversation)
                    VALUES (?, ?)
                """, (sujet, type_combo.get()))
                
                conv_id = cursor.lastrowid
                
                # Ajouter l'utilisateur comme participant
                cursor.execute("""
                    INSERT INTO conversation_participants (conversation_id, user_id, role)
                    VALUES (?, ?, ?)
                """, (conv_id, self.utilisateur.get('id', 1), self.utilisateur.get('role', 'Utilisateur')))
                
                conn.commit()
                conn.close()
                
                conv_window.destroy()
                messagebox.showinfo("Succès", f"Conversation '{sujet}' créée avec succès!")
                self.load_conversations()
                
            except Exception as e:
                messagebox.showerror("Erreur", f"Erreur lors de la création: {e}")
        
        create_btn = ctk.CTkButton(
            buttons_frame,
            text="💾 Créer",
            font=(FONT, FS_TEXT, "bold"),
            fg_color=ACCENT,
            hover_color=HOVER_PRIMARY,
            corner_radius=8,
            height=35,
            command=create_conversation
        )
        create_btn.pack(side="left", padx=(0, 10))
        
        cancel_btn = ctk.CTkButton(
            buttons_frame,
            text="❌ Annuler",
            font=(FONT, FS_TEXT, "bold"),
            fg_color=CARD_BG,
            hover_color=HOVER,
            corner_radius=8,
            height=35,
            command=conv_window.destroy
        )
        cancel_btn.pack(side="left")

