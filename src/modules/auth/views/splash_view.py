#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
EduManager+ - Splash Screen Révolutionnaire
Design futuriste avec effets de matrice, particules quantiques et animations spectaculaires
- Effet de matrice digitale avec code qui tombe
- Logo holographique avec rotation 3D
- Barre de progression avec effet de vague quantique
- Animations fluides et transitions spectaculaires
- Design cyberpunk avec néons et effets de lueur
"""

import os
import gc
import time
import math
import random
import customtkinter as ctk
from PIL import Image, ImageTk
import tkinter as tk

# ====================== IMPORT THÈME GLOBAL ======================
from resources.themes.theme import *
print("✅ Thème global sombre parfait chargé dans splash")

# ====================== CONFIGURATION CUSTOMTKINTER ======================
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# ====================== COULEURS SPLASH EDU MANAGER+ ======================
# Palette moderne avec le nouveau thème EduManager+
BG              = BG_MAIN         # fond principal (#0A192F)
MATRIX_BG       = BG_SIDEBAR      # fond de la matrice (#0E1C36)
CARD_BG         = CARD_BG         # carte interne (#0b1d34)
BORDER_OUTER    = BORDER_COLOR    # bordure principale (#1f3b5a)
BORDER_INNER    = ACCENT          # bordure accent (#64FFDA)
ACCENT          = ACCENT          # accent principal (#64FFDA)
TEXT_SOFT       = TEXT            # texte principal (#E2E8F0)
TEXT_PERCENT    = MUTED           # texte secondaire (#8aa0b8)
MATRIX_COLOR    = ACCENT          # couleur de la matrice (cyan)
QUANTUM_COLOR   = ACCENT          # couleur quantique (cyan)

WIN_W, WIN_H    = 1000, 700    # Fenêtre plus grande pour plus d'impact
DURATION_MS     = 4000        # Durée plus longue pour apprécier les effets
SHIFT_LEFT_PX   = 50         # Centrage optimal

# ========================== Icônes (logo) ==========================
ICONS_PATH_ABS = r"C:\Users\Lenovo\Desktop\Clonage_git\Gestion_scolaire\Gestion_scolaire\resources\icons"
ICONS_PATH_REL = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", "..", "..", "..", "resources", "icons"))
ICONS_PATH     = ICONS_PATH_ABS if os.path.isdir(ICONS_PATH_ABS) else ICONS_PATH_REL

_ICON, _PIL = {}, {}

def _load_pil(name: str):
    if name in _PIL: return _PIL[name]
    p = os.path.join(ICONS_PATH, f"{name}.png")
    if not os.path.exists(p):
        print(f"⚠️ Icône introuvable: {p}"); return None
    try:
        im = Image.open(p).convert("RGBA")
        _PIL[name] = im
        return im
    except Exception as e:
        print(f"⚠️ Erreur chargement '{name}': {e}")
        return None

def get_icon(name: str, size=(188, 188)):
    key = f"{name}_{size[0]}x{size[1]}"
    if key in _ICON: return _ICON[key]
    im = _load_pil(name)
    if im is None: return None
    cimg = ctk.CTkImage(light_image=im, dark_image=im, size=size)
    _ICON[key] = cimg
    return cimg

# ============================ SplashView Révolutionnaire ============================
class SplashView(ctk.CTkToplevel):
    def __init__(self, master=None, duration_ms: int = DURATION_MS):
        self._own_root = None
        if master is None:
            self._own_root = ctk.CTk(); self._own_root.withdraw(); master = self._own_root
        super().__init__(master)

        # Fenêtre (fond fixe, centrée)
        self.title("EduManager+ - Initialisation")
        self.geometry(f"{WIN_W}x{WIN_H}")
        self.configure(fg_color=BG)
        self.resizable(False, False)
        self.overrideredirect(True)
        self.attributes("-alpha", 0.0)
        self.attributes("-topmost", True)

        # État
        self._alive   = True
        self._afters  = set()
        self._dur     = duration_ms
        self._t0      = None

        # Effets visuels révolutionnaires
        self._create_matrix_background()
        self._create_quantum_particles()
        
        # UI – Design futuriste
        self._center()
        self._build_main_container()
        self._build_holographic_logo()
        self._build_quantum_progress()
        self._build_cyberpunk_footer()

        # Descriptions modernes EduManager+
        self._descriptions = [
            "🚀 Initialisation d'EduManager+…",
            "💾 Chargement de la base de données…",
            "🎨 Préparation de l'interface moderne…",
            "🔐 Connexion au système RBAC…",
            "⚡ Optimisation des performances…",
            "🌟 Finalisation & ouverture…"
        ]
        self._desc_index = 0

        # Interactions (skip)
        self.bind("<Button-1>", lambda e: self._transition())
        self.bind("<Return>",    lambda e: self._transition())
        self.bind("<Escape>",    lambda e: self._transition())

        # Animations révolutionnaires
        self._schedule(60, self._kickoff)
        self._schedule(200, self._anim_matrix_rain)      # Pluie de matrice
        self._schedule(300, self._anim_quantum_particles) # Particules quantiques
        self._schedule(400, self._anim_holographic_logo)   # Logo holographique
        self._schedule(500, self._anim_quantum_progress)   # Progression quantique
        self.protocol("WM_DELETE_WINDOW", self._on_close)

    # ------------------------ after() sûrs -------------------------
    def _schedule(self, ms, fn):
        if not self._alive: return None
        aid = self.after(ms, fn); self._afters.add(aid); return aid
    def _cancel_all(self):
        for aid in tuple(self._afters):
            try: self.after_cancel(aid)
            except Exception: pass
            finally: self._afters.discard(aid)

    # --------------------- Effets Visuels Révolutionnaires --------------------
    def _create_matrix_background(self):
        """Crée un effet de matrice digitale avec code qui tombe"""
        self.matrix_chars = []
        self.matrix_speeds = []
        
        # Créer des colonnes de caractères qui tombent
        for i in range(20):  # 20 colonnes
            chars = []
            speeds = []
            for j in range(15):  # 15 caractères par colonne
                char = random.choice("01ABCDEFGHIJKLMNOPQRSTUVWXYZ")
                speed = random.uniform(0.5, 2.0)
                chars.append(char)
                speeds.append(speed)
            self.matrix_chars.append(chars)
            self.matrix_speeds.append(speeds)
    
    def _create_quantum_particles(self):
        """Crée des particules quantiques flottantes"""
        self.quantum_particles = []
        for i in range(25):  # 25 particules quantiques
            particle = {
                'x': random.randint(0, WIN_W),
                'y': random.randint(0, WIN_H),
                'vx': random.uniform(-2, 2),
                'vy': random.uniform(-2, 2),
                'size': random.randint(2, 6),
                'color': random.choice([DARK_ACCENT, SUCCESS_GREEN, WARNING_YELLOW]),
                'alpha': random.uniform(0.3, 1.0)
            }
            self.quantum_particles.append(particle)

    # --------------------- Construction de l'UI --------------------
    def _build_main_container(self):
        # Conteneur principal avec effet de glassmorphism
        self.main_container = ctk.CTkFrame(
            self, fg_color="transparent", corner_radius=0
        )
        self.main_container.place(relx=0.5, rely=1.2, anchor="center", relwidth=1.0, relheight=1.0)

        # Carte centrale avec effet holographique
        self.holographic_card = ctk.CTkFrame(
            self.main_container, fg_color=CARD_BG, corner_radius=30,
            border_width=4, border_color=BORDER_OUTER
        )
        self.holographic_card.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.85, relheight=0.8)

        # Effet de lueur interne
        self.glow_frame = ctk.CTkFrame(
            self.holographic_card, fg_color="transparent", corner_radius=25,
            border_width=2, border_color=BORDER_INNER
        )
        self.glow_frame.pack(fill="both", expand=True, padx=8, pady=8)

    def _build_holographic_logo(self):
        # Zone du logo holographique
        self.logo_zone = ctk.CTkFrame(
            self.glow_frame, fg_color="transparent", height=200
        )
        self.logo_zone.pack(fill="x", padx=40, pady=(40, 20))
        
        # Titre principal avec effet de glitch (supprimé)
        # self.title_label = ctk.CTkLabel(
        #     self.logo_zone, 
        #     text="EduManager+", 
        #     font=FONT_HERO,
        #     text_color=ACCENT_BLUE
        # )
        # self.title_label.pack(pady=(0, 10))
        
        # Sous-titre cyberpunk
        self.subtitle_label = ctk.CTkLabel(
            self.logo_zone,
            text="Système de Gestion Scolaire Quantique",
            font=FONT_SUBTITLE,
            text_color=TEXT_SECONDARY
        )
        self.subtitle_label.pack()

        # Logo avec effet de rotation 3D (agrandi)
        self.logo_container = ctk.CTkFrame(
            self.glow_frame, fg_color="transparent", height=200
        )
        self.logo_container.pack(fill="x", padx=40, pady=20)
        
        # Cercle holographique (agrandi)
        self.holographic_circle = ctk.CTkFrame(
            self.logo_container, fg_color="transparent", 
            corner_radius=999, width=160, height=160,
            border_width=4, border_color=DARK_ACCENT
        )
        self.holographic_circle.place(relx=0.5, rely=0.5, anchor="center")
        
        # Logo ou texte alternatif (agrandi)
        logo = get_icon("logo", (120, 120))
        if logo:
            self.logo_label = ctk.CTkLabel(
                self.holographic_circle, text="", image=logo,
                fg_color="transparent"
            )
            self.logo_label.place(relx=0.5, rely=0.5, anchor="center")
            self.logo_label.image = logo
        else:
            self.logo_label = ctk.CTkLabel(
                self.holographic_circle,
                text="EM+",
                font=FONT_HERO,
                text_color=DARK_ACCENT,
                fg_color="transparent"
            )
            self.logo_label.place(relx=0.5, rely=0.5, anchor="center")

    def _build_quantum_progress(self):
        # Zone de progression quantique
        self.progress_zone = ctk.CTkFrame(
            self.glow_frame, fg_color="transparent", height=120
        )
        self.progress_zone.pack(fill="x", padx=40, pady=20)
        
        # Titre de progression
        self.progress_title = ctk.CTkLabel(
            self.progress_zone, text="⚡ Initialisation Quantique...",
            text_color=TEXT_PRIMARY, font=FONT_SUBTITLE
        )
        self.progress_title.pack(pady=(0, 15))

        # Barre de progression avec effet de vague quantique
        self.quantum_progress = ctk.CTkProgressBar(
            self.progress_zone, height=20, corner_radius=15,
            progress_color=DARK_ACCENT, fg_color=DARK_BLUE,
            border_color=DARK_ACCENT, border_width=2, mode="determinate"
        )
        self.quantum_progress.pack(fill="x", padx=20, pady=(0, 15))
        self.quantum_progress.set(0.0)

        # Conteneur pour description et pourcentage
        info_container = ctk.CTkFrame(self.progress_zone, fg_color="transparent")
        info_container.pack(fill="x", padx=20, pady=(0, 20))

        # Description avec effet de typewriter
        self.desc_label = ctk.CTkLabel(
            info_container, text="Démarrage quantique…", 
            text_color=TEXT_SOFT, anchor="w",
            font=FONT_PRIMARY
        )
        self.desc_label.pack(side="left")

        # Pourcentage avec effet de compteur
        self.percent_label = ctk.CTkLabel(
            info_container, text="0%", 
            text_color=DARK_ACCENT, 
            font=FONT_TITLE
        )
        self.percent_label.pack(side="right")

    def _build_cyberpunk_footer(self):
        # Footer cyberpunk
        self.footer_zone = ctk.CTkFrame(
            self.glow_frame, fg_color="transparent", height=60
        )
        self.footer_zone.pack(side="bottom", fill="x", padx=40, pady=(0, 30))
        
        # Version avec effet de glitch
        self.version_label = ctk.CTkLabel(
            self.footer_zone,
            text="Version 2.0 • © 2024 EduManager+",
            text_color=TEXT_MUTED,
            font=FONT_SMALL
        )
        self.version_label.pack(side="left")
        
        # Indicateur quantique
        self.quantum_indicator = ctk.CTkLabel(
            self.footer_zone,
            text="◉◉◉",
            text_color=DARK_ACCENT,
            font=FONT_SMALL
        )
        self.quantum_indicator.pack(side="right")

    # -------------------------- Animations Révolutionnaires --------------------------
    def _kickoff(self):
        self._t0 = time.time()
        self._anim_window_fade(0.0, True)
        self._anim_container_entry(1.2)
        self._anim_quantum_progress()
        self._anim_cycle_desc()
        self._schedule(self._dur, self._transition)

    def _anim_window_fade(self, a, fade_in=True):
        if not self._alive or not self.winfo_exists(): return
        if fade_in:
            a = min(1.0, a); self.attributes("-alpha", a)
            if a < 1.0: self._schedule(12, lambda: self._anim_window_fade(a+0.08, True))
            else: self.attributes("-topmost", False)
        else:
            a = max(0.0, a); self.attributes("-alpha", a)
            if a > 0.0: self._schedule(12, lambda: self._anim_window_fade(a-0.12, False))

    def _anim_container_entry(self, rely):
        if not self._alive or not self.winfo_exists(): return
        if rely > 0.5:
            nr = rely - (rely-0.5)*0.15  # Animation ultra-fluide
            self.main_container.place(relx=0.5, rely=nr, anchor="center", relwidth=1.0, relheight=1.0)
            self._schedule(6, lambda: self._anim_container_entry(nr))
        else:
            self.main_container.place(relx=0.5, rely=0.5, anchor="center", relwidth=1.0, relheight=1.0)

    def _anim_matrix_rain(self):
        """Animation de pluie de matrice"""
        if not self._alive or not self.winfo_exists(): return
        try:
            # Simuler la pluie de matrice (effet visuel)
            for i in range(len(self.matrix_chars)):
                for j in range(len(self.matrix_chars[i])):
                    # Changer les caractères aléatoirement
                    if random.random() < 0.1:  # 10% de chance de changement
                        self.matrix_chars[i][j] = random.choice("01ABCDEFGHIJKLMNOPQRSTUVWXYZ")
            self._schedule(100, self._anim_matrix_rain)
        except Exception: pass

    def _anim_quantum_particles(self):
        """Animation des particules quantiques"""
        if not self._alive or not self.winfo_exists(): return
        try:
            for particle in self.quantum_particles:
                # Mouvement quantique
                particle['x'] += particle['vx']
                particle['y'] += particle['vy']
                
                # Rebond sur les bords
                if particle['x'] < 0 or particle['x'] > WIN_W:
                    particle['vx'] *= -1
                if particle['y'] < 0 or particle['y'] > WIN_H:
                    particle['vy'] *= -1
                
                # Garder dans les limites
                particle['x'] = max(0, min(WIN_W, particle['x']))
                particle['y'] = max(0, min(WIN_H, particle['y']))
                
                # Variation d'alpha
                particle['alpha'] = 0.3 + 0.7 * abs(math.sin(time.time() * 2 + particle['x'] * 0.01))
            
            self._schedule(50, self._anim_quantum_particles)
        except Exception: pass

    def _anim_holographic_logo(self):
        """Animation du logo holographique"""
        if not self._alive or not self.winfo_exists(): return
        try:
            # Effet de pulsation sur le cercle holographique
            pulse = (time.time() * 2) % (2 * math.pi)
            intensity = (math.sin(pulse) + 1) / 2
            
            if intensity > 0.7:
                self.holographic_circle.configure(border_color=DARK_ACCENT)
            elif intensity > 0.4:
                self.holographic_circle.configure(border_color="#333333")
            else:
                self.holographic_circle.configure(border_color="#666666")
            
            # Effet de glitch sur le titre (supprimé)
            # if intensity > 0.8:
            #     self.title_label.configure(text_color=ACCENT_BLUE)
            # elif intensity > 0.6:
            #     self.title_label.configure(text_color=LIGHT_BLUE)
            # else:
            #     self.title_label.configure(text_color=TEXT_SECONDARY)
                
            self._schedule(80, self._anim_holographic_logo)
        except Exception: pass

    def _anim_quantum_progress(self):
        """Animation de la progression quantique"""
        if not self._alive or not self.winfo_exists(): return
        if self._t0 is None: self._t0 = time.time()
        elapsed = (time.time() - self._t0) * 1000.0
        prog = max(0.0, min(1.0, elapsed / self._dur))
        try:
            self.quantum_progress.set(prog)
            self.percent_label.configure(text=f"{int(prog*100)}%")
        except Exception: pass
        if prog < 1.0:
            self._schedule(20, self._anim_quantum_progress)

    def _anim_cycle_desc(self):
        if not self._alive or not self.winfo_exists(): return
        # Changement toutes ~1200 ms pour plus de fluidité
        self._desc_index = (self._desc_index + 1) % len(self._descriptions)
        try: 
            self.desc_label.configure(text=self._descriptions[self._desc_index])
        except Exception: pass
        self._schedule(1200, self._anim_cycle_desc)

    def _anim_quantum_indicator(self):
        """Animation de l'indicateur quantique"""
        if not self._alive or not self.winfo_exists(): return
        try:
            current_text = self.quantum_indicator.cget("text")
            if current_text == "◉◉◉":
                self.quantum_indicator.configure(text="◉◉○")
            elif current_text == "◉◉○":
                self.quantum_indicator.configure(text="◉○○")
            elif current_text == "◉○○":
                self.quantum_indicator.configure(text="○○○")
            else:
                self.quantum_indicator.configure(text="◉◉◉")
            self._schedule(400, self._anim_quantum_indicator)
        except Exception: pass

    # --------------------------- Transition -------------------------
    def _transition(self):
        if not self._alive or not self.winfo_exists(): return
        self._cancel_all()
        
        # Animation de sortie spectaculaire
        def slide(rely):
            if not self._alive or not self.winfo_exists(): return
            if rely < 1.2:
                nr = rely + (1.2 - rely) * 0.20  # Animation plus douce
                self.main_container.place(relx=0.5, rely=nr, anchor="center", relwidth=1.0, relheight=1.0)
                self._schedule(8, lambda: slide(nr))
        
        slide(0.5)
        self._anim_window_fade(1.0, False)
        self._schedule(400, self._go_login)

    def _go_login(self):
        self._cancel_all()
        self._alive = False
        try: _ICON.clear(); _PIL.clear()
        except Exception: pass
        try: self.destroy()
        except Exception: pass
        if self._own_root:
            try: self._own_root.destroy()
            except Exception: pass
        gc.collect()
        try:
            from src.modules.auth.views.login_view import LoginViewModern as _LV
            _LV().mainloop()
        except Exception as e:
            print(f"❌ Impossible d'ouvrir l'écran de connexion: {e}")

    # ----------------------------- Divers ---------------------------
    def _center(self):
        self.update_idletasks()
        sw, sh = self.winfo_screenwidth(), self.winfo_screenheight()
        x = (sw - WIN_W)//2 + SHIFT_LEFT_PX
        y = (sh - WIN_H)//2
        self.geometry(f"{WIN_W}x{WIN_H}+{x}+{y}")

    def _on_close(self):
        self._cancel_all(); self._alive = False
        if self._own_root:
            try: self._own_root.quit()
            except Exception: pass
        else:
            try: self.master.quit()
            except Exception: pass

# ====================== Lancement direct ======================
if __name__ == "__main__":
    SplashView(duration_ms=DURATION_MS).mainloop()