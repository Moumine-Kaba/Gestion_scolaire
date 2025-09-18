#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from database.connection import get_db_connection
from database.connection import get_db_connection
from database.connection import get_db_connection
from pathlib import Path
from tkinter import messagebox
import tkinter as tk
import customtkinter as ctk
from PIL import Image, ImageEnhance, ImageFilter
import itertools
import re
import os
import sys
# Remplacé par SQL Server  # Remplacé par SQL Server

__all__ = ["LoginViewModern", "LoginView"]

# ================== IMPORT THÈME GLOBAL ==================
from resources.themes.theme import *
print("✅ Thème global sombre parfait chargé dans login")

# ================== CONFIGURATION CUSTOMTKINTER ==================
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# ================== PALETTE COULEURS LOGIN EDU MANAGER+ ==================
# Utilisation directe des couleurs du nouveau thème EduManager+
COL = {
    # Arrière-plan appli principal (cohérent avec le thème)
    "bg": BG_MAIN,                    # "#0A192F" - Fond principal

    # Formulaire = teinte du thème
    "panel":        CARD_BG,          # "#0b1d34" - carte du formulaire
    "panel_deeper": BG_SIDEBAR,       # "#0E1C36" - bordure externe
    "panel_inner":  "#2a3f5f",        # intérieur des champs plus clair

    # Lignes & focus (couleurs du thème)
    "line":        "#3a4f6f",         # bordure principale plus visible
    "line_focus":  "#00D4FF",         # focus accent cyan plus vif

    # Texte
    "text":   TEXT,                   # "#E2E8F0" - texte principal
    "muted":  MUTED,                  # "#8aa0b8" - texte secondaire

    # Accents généraux
    "primary":        "#00D4FF",      # accent principal cyan plus vif
    "primary_hover":  "#00B8E6",      # survol cyan plus foncé
    "accent":         "#00D4FF",      # accent principal cyan
    "accent_neon":    "#00D4FF",      # accent néon cyan vif
    "accent_alt":     TEXT,           # accent alternatif clair
    "danger":         ERROR_RED,      # danger rouge vif

    # CTA (bouton Connexion)
    "cta":        "#00D4FF",          # bouton principal cyan vif
    "cta_hover":  "#00B8E6",          # survol bouton cyan foncé
    "cta_text":   "#0A192F",          # texte bouton sombre pour contraste
}

FNT = {
    "body": FONT_PRIMARY,        # ("Segoe UI", 14) - police principale moderne
    "btn": FONT_BUTTON,          # ("Segoe UI", 13, "bold") - police boutons moderne
    "small": FONT_SMALL,         # ("Segoe UI", 11) - police petite moderne
}

# ================== Chemins projet ==================
try:
    PROJ_ROOT = Path(__file__).resolve().parents[4]
except Exception:
    PROJ_ROOT = Path.cwd()

if str(PROJ_ROOT) not in sys.path:
    sys.path.append(str(PROJ_ROOT))

RESOURCES = PROJ_ROOT / "resources"
ICONS = RESOURCES / "icons"
IMAGES = RESOURCES / "images"

RIGHT_IMAGE_NAME = "journee-internationale-de-l-education-dans-le-style-sombre.jpg"
DB_PATH = PROJ_ROOT / "database" / "edumanager.db"

# ================== Import RBAC System ==================
RBACSystem = None
try:
    from src.modules.auth.models.rbac_system import RBACSystem as _RBAC
    RBACSystem = _RBAC
    print("✅ Système RBAC importé avec succès")
except Exception as e:
    print(f"⚠️ Système RBAC indisponible: {e}")
    RBACSystem = None

# ================== Mini-migration auth (colonne fautive) ==================
def _ensure_login_attempts_schema():
    """Fonction adaptée pour SQL Server - les tables sont déjà créées."""
    try:
        # Pour SQL Server, on vérifie juste que la table existe
        conn = get_db_connection()
        if conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT COUNT(*) FROM INFORMATION_SCHEMA.TABLES 
                WHERE TABLE_NAME = 'login_attempts'
            """)
            if cursor.fetchone()[0] > 0:
                print("✅ Table login_attempts existe dans SQL Server")
            else:
                print("⚠️ Table login_attempts non trouvée dans SQL Server")
            conn.close()
        else:
            print("⚠️ Impossible de se connecter à la base de données")
    except Exception as e:
        print(f"⚠️ Erreur vérification login_attempts: {e}")

_ensure_login_attempts_schema()

# ================== Import EnhancedAuthManager (optionnel) ==================
EnhancedAuthManager = None
try:
    from src.modules.auth.models.auth_enhanced import EnhancedAuthManager as _EAM
    EnhancedAuthManager = _EAM
except Exception as e:
    print(f"ℹ️ EnhancedAuthManager indisponible (mode démo): {e}")
    EnhancedAuthManager = None

# ================== Import robuste du Dashboard MainApp ==================
MainApp = None
_import_errors = []

def _try_import_mainapp():
    """Essaie plusieurs chemins sans casser l'app si le dashboard n'est pas encore présent."""
    global MainApp
    candidates = [
        "src.modules.auth.views.dashboard_view",         # chemin standard
        "src.modules.auth.views",                        # si MainApp est exporté ailleurs
        "src.modules.academic.dashboard.dashboard_view", # variante
        f"{__package__}.dashboard_view" if __package__ else "dashboard_view",
    ]
    for mod in candidates:
        try:
            module = __import__(mod, fromlist=["MainApp"])
            ma = getattr(module, "MainApp", None)
            if ma:
                MainApp = ma
                return True
        except Exception as e:
            _import_errors.append(f"{mod}: {e}")
    return False

_try_import_mainapp()

# ================== Utils images — cache PIL ONLY ==================
# Important : aucun CTkImage persistant au-delà du root courant
_pil_cache: dict[str, Image.Image] = {}

def _load_pil_icon(name: str) -> Image.Image | None:
    if name in _pil_cache:
        return _pil_cache[name]
    p = ICONS / f"{name}.png"
    if not p.exists():
        return None
    pil = Image.open(p).convert("RGBA")
    _pil_cache[name] = pil
    return pil

def get_icon(name: str, size=(24, 24)) -> ctk.CTkImage | None:
    pil = _load_pil_icon(name)
    if not pil:
        return None
    return ctk.CTkImage(light_image=pil, dark_image=pil, size=size)

def load_image(path: Path):
    try:
        if path.exists():
            return Image.open(path).convert("RGB")
    except Exception as e:
        print(f"⚠️ Erreur ouverture image '{path.name}': {e}")
    return None

def reset_ctk_image_caches_dashboard():
    """Nettoie tous les caches d'icônes du dashboard avant instanciation."""
    try:
        from src.modules.auth.views import dashboard_view as dv
        for k in ("_ICON_CACHE", "_icon_cache"):
            if hasattr(dv, k):
                try:
                    getattr(dv, k).clear()
                    print(f"✅ Cache {k} nettoyé")
                except Exception:
                    pass
        if hasattr(dv, '_DASHBOARD_PIL_CACHE'):
            dv._DASHBOARD_PIL_CACHE.clear()
            print("✅ Cache PIL dashboard nettoyé")
        if hasattr(dv, '_DASHBOARD_IMG_POOL'):
            dv._DASHBOARD_IMG_POOL.clear()
            print("✅ Pool images dashboard nettoyé")
    except Exception as e:
        print(f"⚠️ Erreur nettoyage cache dashboard: {e}")

# ================== Effets / composants ==================
class NeonPulseBorderMixin:
    """Pulse néon sûr: annule automatiquement les after lors de la destruction."""
    def enable_neon_pulse(self, colors: list[str], period_ms: int = 160):
        self._np_colors = itertools.cycle(colors)
        self._np_period = period_ms
        self._np_after_id = None
        try:
            self.bind("<Destroy>", self._neon_on_destroy, add="+")
        except Exception:
            pass
        self._neon_pulse_tick()

    def _neon_pulse_tick(self):
        try:
            if not self.winfo_exists():
                return
            col = next(self._np_colors)
            self.configure(border_color=col, border_width=1)
            self._np_after_id = self.after(self._np_period, self._neon_pulse_tick)
        except Exception:
            self._np_after_id = None

    def _neon_on_destroy(self, _evt=None):
        aid = getattr(self, "_np_after_id", None)
        if aid:
            try:
                self.after_cancel(aid)
            except Exception:
                pass
            self._np_after_id = None

class DoubleBorderCard(ctk.CTkFrame):
    """Carte entrée avec double-bordure premium."""
    def __init__(self, master, **kw):
        super().__init__(master, fg_color=COL["panel"], corner_radius=16,
                         border_width=1, border_color=COL["panel_deeper"], **kw)
        self.inner = ctk.CTkFrame(self, fg_color=COL["panel_inner"],
                                  corner_radius=12, border_width=1,
                                  border_color="#1C2A46")
        self.inner.pack(fill="x", padx=8, pady=6)

class FieldStyleButton(ctk.CTkFrame):
    """Bouton ‘Connexion’ dans le style des champs, inversé + CTA élégant."""
    def __init__(self, master, text: str, command):
        super().__init__(master, fg_color="transparent")
        self._text = text
        self._command = command

        # Carte externe (double-bordure)
        self.card = DoubleBorderCard(self)
        self.card.pack(fill="x")

        # Corps du bouton (fond CTA plein)
        self.body = ctk.CTkFrame(
            self.card.inner,
            fg_color=COL["cta"],
            corner_radius=12
        )
        self.body.pack(fill="x", padx=12, pady=(14, 12))

        # Libellé
        self._label = ctk.CTkLabel(
            self.body,
            text=self._text,
            text_color=COL["cta_text"],
            font=FNT["btn"]
        )
        self._label.pack(pady=10)

        # Ligne décorative (fine, en bas) — bg valide (pas de chaîne vide)
        self._line = tk.Canvas(
            self.card.inner,
            height=3,
            bd=0,
            highlightthickness=0,
            relief="flat",
            bg=COL["panel_inner"]
        )
        self._line.pack(fill="x", padx=10, pady=(0, 10))
        self._line.bind("<Configure>", self._draw_line)

        # Interactions (clic & hover)
        for w in (self, self.card, self.card.inner, self.body, self._label, self._line):
            w.bind("<Button-1>", lambda e: self._command())
            w.bind("<Enter>", lambda e: self._hover(True))
            w.bind("<Leave>", lambda e: self._hover(False))

    def _draw_line(self, _evt=None):
        c = self._line
        c.delete("all")
        w = max(1, c.winfo_width())
        h = max(2, c.winfo_height())

        def mix_hex(a: str, b: str, t: float) -> str:
            t = 0.0 if t < 0 else 1.0 if t > 1 else float(t)
            fa = tuple(int(a[i:i+2], 16) for i in (1, 3, 5))
            fb = tuple(int(b[i:i+2], 16) for i in (1, 3, 5))
            rgb = [int(fa[k] + (fb[k] - fa[k]) * t) for k in range(3)]
            return f"#{rgb[0]:02x}{rgb[1]:02x}{rgb[2]:02x}"

        # Dégradé discret du CTA vers un cyan plus doux
        for x in range(w):
            t = x / (w - 1) if w > 1 else 0.0
            c.create_line(x, 0, x, h, fill=mix_hex(COL["cta"], COL["cta_hover"], t))

    def _hover(self, v: bool):
        if v:
            self.body.configure(fg_color=COL["cta_hover"])
            self.card.configure(border_color=COL["cta_hover"])
            self.card.inner.configure(border_color="#2A3E66")
            try: self._line.configure(height=4)
            except Exception: pass
        else:
            self.body.configure(fg_color=COL["cta"])
            self.card.configure(border_color=COL["panel_deeper"])
            self.card.inner.configure(border_color="#1C2A46")
            try: self._line.configure(height=3)
            except Exception: pass

    def set_text(self, t: str):
        self._text = t
        self._label.configure(text=self._text)
        self._label.update_idletasks()

class LineInput(ctk.CTkFrame):
    """Champ material avec double-bordure + ligne focus + icône + erreurs inline."""
    def __init__(self, master, icon: ctk.CTkImage | None, placeholder: str,
                 var: ctk.StringVar, show: str | None = None):
        super().__init__(master, fg_color="transparent")
        self._img_ref = icon
        self.card = DoubleBorderCard(self); self.card.pack(fill="x")
        row = ctk.CTkFrame(self.card.inner, fg_color="transparent"); row.pack(fill="x", padx=12, pady=(10, 6))
        if icon:
            lbl = ctk.CTkLabel(row, text="", image=icon, width=28)
            lbl.pack(side="left", padx=(2, 10))
            lbl.image = icon
        self.entry = ctk.CTkEntry(
            row, textvariable=var, placeholder_text=placeholder,
            height=48, border_width=0, corner_radius=12,
            fg_color=COL["panel_inner"],  # champs sur la teinte EduManager+
            text_color=COL["text"],
            placeholder_text_color=COL["muted"],
            font=FNT["body"], show=show
        ); self.entry.pack(side="left", fill="x", expand=True)
        self._line = ctk.CTkFrame(self.card.inner, fg_color=COL["line"], height=2); self._line.pack(fill="x", padx=10, pady=(0, 6))
        self._error = ctk.CTkLabel(self.card.inner, text="", text_color=COL["danger"], font=FNT["small"])
        self._error.pack(anchor="w", padx=12, pady=(0, 6)); self._error.pack_forget()
        self.entry.bind("<FocusIn>", self._on_focus_in); self.entry.bind("<FocusOut>", self._on_focus_out)
        self._right_btn = None
    def _on_focus_in(self, _=None):
        self._line.configure(fg_color=COL["line_focus"], height=3)
        self.card.configure(border_color=COL["accent_neon"]); self.card.inner.configure(border_color=COL["accent"])
    def _on_focus_out(self, _=None):
        self._line.configure(fg_color=COL["line"], height=2)
        self.card.configure(border_color=COL["panel_deeper"]); self.card.inner.configure(border_color=COL["panel_inner"])
    def set_right_button(self, image: ctk.CTkImage, on_press, on_release):
        self._right_btn = ctk.CTkButton(self.card.inner, text="", image=image, width=40, height=36,
                                        corner_radius=12, fg_color=COL["panel_inner"], hover_color=COL["primary_hover"])
        self._right_btn.place(relx=1.0, rely=0.06, x=-12, y=0, anchor="ne")
        self._right_btn.bind("<ButtonPress-1>", lambda e: on_press())
        self._right_btn.bind("<ButtonRelease-1>", lambda e: on_release())
        self._right_btn.image = image
    def show_error(self, text: str):
        self._error.configure(text=text); self._error.pack(anchor="w", padx=12, pady=(0, 6))
        self.card.configure(border_color=COL["danger"]); self._line.configure(fg_color=COL["danger"])
    def clear_error(self):
        try: self._error.pack_forget()
        except Exception: pass
        self.card.configure(border_color=COL["panel_deeper"]); self._line.configure(fg_color=COL["line"])

class Divider(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color="transparent")
        ctk.CTkFrame(self, fg_color="#20304C", height=1).pack(fill="x", pady=6)

# ================== Formulaire ==================
class LoginForm(NeonPulseBorderMixin, ctk.CTkFrame):
    def __init__(self, master, on_success=None):
        super().__init__(master, fg_color=COL["panel"], corner_radius=24,
                         border_color=COL["accent_neon"], border_width=2)
        self.on_success = on_success
        self._img_refs: list[ctk.CTkImage] = []
        self.username = ctk.StringVar()
        self.password = ctk.StringVar()
        self.remember = ctk.BooleanVar(value=True)
        self._build()
        self.enable_neon_pulse([COL["accent_neon"], COL["primary"], COL["accent_alt"], COL["primary"]], 200)

    def destroy(self):
        # coupe le pulse avant destruction
        try:
            self._neon_on_destroy()
        except Exception:
            pass
        super().destroy()

    def _build(self):
        self.grid_columnconfigure(0, weight=1)
        wrap = ctk.CTkFrame(self, fg_color="transparent")
        wrap.grid(row=0, column=0, padx=18, pady=16, sticky="nsew")

        logo = get_icon("logo", (150, 150))
        if logo:
            self._img_refs.append(logo)
            l = ctk.CTkLabel(wrap, text="", image=logo)
            l.pack(pady=(0, 8)); l.image = logo

        user_ic = get_icon("person", (20, 20))
        if user_ic: self._img_refs.append(user_ic)
        self.user_in = LineInput(wrap, user_ic, "Nom d'utilisateurs", self.username)
        self.user_in.pack(fill="x", pady=(0, 10))
        self.user_in.entry.bind("<KeyRelease>", lambda e: self.user_in.clear_error())

        lock_ic = get_icon("protect", (20, 20))
        if lock_ic: self._img_refs.append(lock_ic)
        self.pass_in = LineInput(wrap, lock_ic, "Mot de passe", self.password, show="●")
        self.pass_in.pack(fill="x", pady=(0, 6))
        eye_off = get_icon("eye-off", (18, 18))
        if eye_off:
            self._img_refs.append(eye_off)
            self.pass_in.set_right_button(
                image=eye_off,
                on_press=lambda: self.pass_in.entry.configure(show=""),
                on_release=lambda: self.pass_in.entry.configure(show="●"),
            )

        meter_row = ctk.CTkFrame(wrap, fg_color="transparent"); meter_row.pack(fill="x", pady=(0, 8))
        ctk.CTkLabel(meter_row, text="Robustesse :", font=FNT["small"], text_color=COL["muted"]).pack(side="left", padx=(2, 8))
        self.pw_meter = ctk.CTkProgressBar(meter_row, height=10, corner_radius=8, mode="determinate")
        self.pw_meter.pack(side="left", fill="x", expand=True); self.pw_meter.set(0.0)
        self.pw_meter.configure(progress_color=COL["cta"])
        self.pw_label = ctk.CTkLabel(meter_row, text="—", font=FNT["small"], text_color=COL["muted"]); self.pw_label.pack(side="left", padx=8)
        self.pass_in.entry.bind("<KeyRelease>", self._on_password_input)
        self.pass_in.entry.bind("<KeyRelease>", lambda e: self.pass_in.clear_error(), add="+")
        self.pass_in.entry.bind("<FocusOut>", lambda e: self._on_password_input(None), add="+")

        opt = ctk.CTkFrame(wrap, fg_color="transparent"); opt.pack(fill="x", pady=(2, 2))
        ctk.CTkSwitch(opt, text="Se souvenir de moi", variable=self.remember,
                      font=FNT["small"], text_color=COL["muted"],
                      progress_color=COL["primary"], button_color=COL["primary_hover"]).pack(side="left")
        ctk.CTkButton(opt, text="Mot de passe oublié ?", width=1, fg_color="transparent",
                      text_color=COL["cta"], hover_color="#0E2A45",
                      command=lambda: messagebox.showinfo("Aide", "Contactez l'administrateur.")).pack(side="right")

        Divider(wrap).pack(fill="x")

        self.cta = FieldStyleButton(wrap, text="Se connecter", command=self._do_login)
        self.cta.pack(fill="x", pady=(10, 2))

    def _on_password_input(self, _evt):
        pwd = self.password.get()
        score, label, color = self._compute_strength(pwd)
        self.pw_meter.set(score); self.pw_meter.configure(progress_color=color if score < 0.67 else COL["cta"]); self.pw_label.configure(text=label)

    def _compute_strength(self, pwd: str):
        if not pwd: return 0.0, "—", "#334155"
        score = 0; length = len(pwd)
        classes = sum(bool(re.search(p, pwd)) for p in [r"[a-z]", r"[A-Z]", r"[0-9]", r"[^A-Za-z0-9]"])
        if length >= 8: score += 1
        if length >= 12: score += 1
        if length >= 16: score += 1
        score += max(0, classes-1)
        if re.search(r"(.)\1\1", pwd): score -= 1
        if re.fullmatch(r"[a-z]+", pwd) or re.fullmatch(r"[A-Z]+", pwd) or re.fullmatch(r"\d+", pwd): score -= 1
        score = max(0, min(6, score)) / 6.0
        if score < 0.34:   return score, "Faible", "#ef4444"
        elif score < 0.67: return score, "Moyen", "#f59e0b"
        elif score < 0.9:  return score, "Fort", "#22c55e"
        else:              return score, "Très fort", "#10b981"

    def _validate(self) -> bool:
        ok = True
        u = (self.username.get() or "").strip()
        p = (self.password.get() or "").strip()
        if len(u) < 3:
            self.user_in.show_error("Nom d'utilisateurs trop court (min. 3)."); ok = False
        if len(p) < 6:
            self.pass_in.show_error("Mot de passe trop court (min. 6)."); ok = False
        self._on_password_input(None)
        return ok

    def _auth_with_rbac(self, u: str, p: str):
        """Authentification avec récupération du rôle RBAC"""
        if not RBACSystem:
            return None
            
        try:
            # Connexion à la base de données
            conn = get_db_connection()
            cursor = conn.cursor()
            
            # Vérifier les identifiants
            cursor.execute('''
                SELECT id_utilisateur, username, nom, prenom, email
                FROM utilisateurs 
                WHERE username = ? AND password = ?
            ''', (u, p))
            
            user_row = cursor.fetchone()
            if not user_row:
                conn.close()
                return None
            
            user_id, username, nom, prenom, email = user_row
            
            # Récupérer le rôle RBAC
            rbac = RBACSystem(None, dev_mode=False)  # Pas de chemin DB pour SQL Server
            user_role = rbac.get_user_role(user_id)
            
            conn.close()
            
            if user_role:
                # Créer un objet rôle si c'est une chaîne
                if isinstance(user_role, str):
                    role_obj = type('Role', (), {'name': user_role})()
                else:
                    role_obj = user_role
                
                return {
                    "id": user_id,
                    "username": username,
                    "full_name": f"{nom} {prenom}" if nom and prenom else username,
                    "roles": role_obj.name,
                    "rbac_role": role_obj,
                    "rbac_system": rbac,
                    "email": email
                }
            else:
                # Utilisateur sans rôle RBAC
                return {
                    "id": user_id,
                    "username": username,
                    "full_name": f"{nom} {prenom}" if nom and prenom else username,
                    "roles": "Utilisateur",
                    "rbac_role": None,
                    "rbac_system": rbac,
                    "email": email
                }
                
        except Exception as e:
            print(f"❌ Erreur authentification RBAC: {e}")
            return None

    def _auth_demo(self, u: str, p: str):
        """Authentification de démonstration (fallback)"""
        demo = {
            "admin": ("admin123", "Administrateur"),
            "directeur": ("directeur123", "Directeur"),
            "professeurs": ("prof123", "Professeur"),
            "secretaire": ("sec123", "Secrétaire"),
            "eleves": ("eleve123", "Élève"),
        }
        if u in demo and p == demo[u][0]:
            return {"id": 1, "username": u, "full_name": u.title(), "roles": demo[u][1]}
        return None

    def _do_login(self, _evt=None):
        if not self._validate():
            return
        u = self.username.get().strip()
        p = self.password.get().strip()
        self.cta.set_text("Vérification…"); self.update_idletasks()

        user_info = None

        # Essayer d'abord l'authentification RBAC
        if RBACSystem:
            user_info = self._auth_with_rbac(u, p)
            if user_info:
                print(f"✅ Authentification RBAC réussie: {user_info['username']} ({user_info['roles']})")

        # Fallback vers EnhancedAuthManager
        if not user_info and EnhancedAuthManager:
            try:
                auth = EnhancedAuthManager(str(DB_PATH))
                user_info = auth.authenticate_user(u, p, "127.0.0.1", "CTk/Win")
                if user_info and "roles" not in user_info:
                    user_info["roles"] = user_info.get("primary_role", "Utilisateur")
            except Exception as e:
                print(f"⚠️ Auth manager erreur: {e}")

        # Fallback vers authentification de démonstration
        if not user_info:
            user_info = self._auth_demo(u, p)

        if user_info:
            if self.on_success: self.on_success(user_info)
        else:
            messagebox.showerror("Échec", "Identifiants incorrects.")
            self.password.set(""); self.pass_in.entry.focus(); self._on_password_input(None)

        self.cta.set_text("Se connecter")

# ================== Fenêtre principale (image GAUCHE / form DROITE) ==================
class LoginViewModern(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("EduManager+ - Connexion")
        self.W, self.H = 1200, 700
        self.geometry(f"{self.W}x{self.H}")
        self.minsize(self.W, self.H)
        self.configure(fg_color=COL["bg"])

        # Gestion des after pour éviter "invalid command name …"
        self._after_ids = []

        self._img_refs: list[ctk.CTkImage] = []
        self._bg_canvas = tk.Canvas(self, highlightthickness=0, bd=0, bg=COL["bg"])
        self._bg_canvas.place(relx=0, rely=0, relwidth=1, relheight=1)

        self.grid_columnconfigure(0, weight=1, uniform="a"); self.grid_columnconfigure(1, weight=1, uniform="a")
        self.grid_rowconfigure(0, weight=1)

        # GAUCHE : image
        self.left = ctk.CTkFrame(self, fg_color="transparent", corner_radius=0)
        self.left.grid(row=0, column=0, sticky="nsew", padx=0, pady=0)
        self.left.grid_columnconfigure(0, weight=1); self.left.grid_rowconfigure(0, weight=1)

        self.left_panel = ctk.CTkFrame(self.left, fg_color=COL["panel"], corner_radius=0)
        self.left_panel.grid(row=0, column=0, sticky="nsew", padx=0, pady=0)
        self.left_panel.grid_columnconfigure(0, weight=1); self.left_panel.grid_rowconfigure(0, weight=1)

        self._left_label = ctk.CTkLabel(self.left_panel, text="")
        self._left_label.grid(row=0, column=0, sticky="nsew", padx=0, pady=0)

        self._left_pil = load_image(IMAGES / RIGHT_IMAGE_NAME)
        if not self._left_pil:
            print(f"⚠️ Illustration non trouvée: {IMAGES / RIGHT_IMAGE_NAME}")

        self.left_panel.bind("<Configure>", self._update_left_image)

        # DROITE : formulaire (teinte splash)
        right_bg = ctk.CTkFrame(self, fg_color="transparent", corner_radius=0)
        right_bg.grid(row=0, column=1, sticky="nsew", padx=0, pady=0)
        right_bg.grid_columnconfigure(0, weight=1); right_bg.grid_rowconfigure(0, weight=1)

        self.form = LoginForm(right_bg, on_success=self._success)
        self.form.grid(row=0, column=0, sticky="nsew", padx=16, pady=16)

        self.safe_after(10, self._center)

    # -------- after helpers --------
    def safe_after(self, ms, func):
        aid = self.after(ms, func)
        self._after_ids.append(aid)
        return aid

    def cancel_afters(self):
        for aid in self._after_ids:
            try: self.after_cancel(aid)
            except Exception: pass
        self._after_ids.clear()

    def destroy(self):
        self.cancel_afters()
        super().destroy()

    # -------- layout helpers --------
    def _center(self):
        self.update_idletasks()
        x = (self.winfo_screenwidth() // 2) - (self.W // 2)
        y = (self.winfo_screenheight() // 2) - (self.H // 2)
        self.geometry(f"{self.W}x{self.H}+{x}+{y}")

    def _update_left_image(self, _evt=None):
        if not self._left_pil or not self.winfo_exists():
            return

        w = max(100, self.left_panel.winfo_width())
        h = max(100, self.left_panel.winfo_height())

        img = self._left_pil

        try:
            # Légère atténuation + contraste
            img = ImageEnhance.Brightness(img).enhance(0.82)
            img = ImageEnhance.Contrast(img).enhance(1.06)
        except Exception:
            pass

        # Resize/crop
        iw, ih = img.size
        scale = max(w / iw, h / ih)
        new_size = (int(iw * scale), int(ih * scale))
        img = img.resize(new_size, Image.LANCZOS)
        x = (img.width - w) // 2
        y = (img.height - h) // 2
        img = img.crop((x, y, x + w, y + h))

        # Teinte bleue premium + adoucissement
        try:
            overlay = Image.new("RGB", img.size, "#0C2040")
            img = Image.blend(img, overlay, 0.10)
            img = img.filter(ImageFilter.GaussianBlur(radius=0.6))
        except Exception:
            pass

        cimg = ctk.CTkImage(light_image=img, dark_image=img, size=(w, h))
        self._img_refs.append(cimg)
        self._left_label.configure(image=cimg)
        self._left_label.image = cimg

    # ===== Transition (destruction AVANT dashboard) =====
    def _success(self, user_info: dict):
        role_name = user_info.get('roles', 'Utilisateur')
        full_name = user_info.get('full_name', user_info.get('username', ''))
        
        # Message de bienvenue avec le rôle RBAC
        if user_info.get('rbac_role'):
            messagebox.showinfo("Succès", f"Bienvenue {full_name}\nRôle: {role_name}")
        else:
            messagebox.showinfo("Succès", f"Bienvenue {full_name}")
            
        # 1) Annuler tous les after
        self.cancel_afters()
        # 2) Purger caches potentiels du dashboard
        reset_ctk_image_caches_dashboard()
        # 3) Détruire complètement le root Login AVANT de créer le dashboard
        self.after(0, lambda: self._handoff_to_dashboard(user_info))

    def _handoff_to_dashboard(self, user_info: dict):
        import gc
        try:
            self.destroy()
        except Exception:
            pass
        gc.collect()

        if not MainApp and not _try_import_mainapp():
            print("❌ Import MainApp échoué. Traces :", *(_import_errors or ["(aucune)"]), sep="\n - ")
            messagebox.showerror("Erreur", "Impossible d'ouvrir le tableau de bord (MainApp introuvable).")
            return

        try:
            # Passer les informations RBAC au dashboard
            app = MainApp(user_info)
        except Exception as e:
            import traceback
            traceback.print_exc()
            messagebox.showerror("Erreur", f"Impossible d'ouvrir le dashboard: {e}")
            return

        app.mainloop()

LoginView = LoginViewModern

if __name__ == "__main__":
    LoginViewModern().mainloop()
