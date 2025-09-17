#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Thème Global EduManager+ - Thème Sombre Moderne
Thème sombre avec fond bleu nuit et accents cyan
"""

# ====================== Thème global EduManager+ ======================

# Arrière-plans
BG_MAIN      = "#0A192F"   # Fond principal (dashboard)
BG_SIDEBAR   = "#0E1C36"   # Fond sidebar / wrap

# Cartes et panneaux
CARD_BG      = "#0b1d34"   # Fond cartes / widgets

# Bordures
BORDER_COLOR = "#1f3b5a"   # Bordures sobres

# Accents et highlights
ACCENT       = "#64FFDA"   # Couleur accent / boutons / progress

# Texte
TEXT         = "#E2E8F0"   # Texte principal
MUTED        = "#8aa0b8"   # Texte secondaire / muted

# Couleurs principales (thème EduManager+)
PRIMARY_BLUE = "#0A192F"          # Bleu nuit (accent principal)
DARK_BLUE = "#0A192F"             # Fond principal sombre
DEEPER_BLUE = "#0E1C36"           # Fond sidebar
NAVY_BLUE = "#0b1d34"             # Fond des cartes
DARKER_BLUE = "#1f3b5a"           # Bordures

# Couleurs secondaires (thème EduManager+)
LIGHT_BLUE = "#64FFDA"            # Accent cyan
ACCENT_BLUE = "#64FFDA"           # Accent cyan
SOFT_BLUE = "#E2E8F0"             # Texte principal clair
PALE_BLUE = "#8aa0b8"             # Texte secondaire
MUTED_BLUE = "#8aa0b8"            # Texte atténué

# Couleurs neutres (thème EduManager+)
DARK_GRAY = "#1f3b5a"             # Bordure principale
MEDIUM_GRAY = "#8aa0b8"           # Bordure moyenne
LIGHT_GRAY = "#64FFDA"            # Bordure accent
WHITE = "#E2E8F0"                 # Texte principal
OFF_WHITE = "#8aa0b8"             # Texte secondaire
PURE_WHITE = "#FFFFFF"            # Blanc pur

# Couleurs d'état (thème inversé)
SUCCESS_GREEN = "#059669"         # Vert succès foncé
WARNING_YELLOW = "#D97706"        # Jaune avertissement foncé
WARNING_ORANGE = "#EA580C"        # Orange information foncé
ERROR_RED = "#DC2626"             # Rouge erreur foncé
INFO_ORANGE = "#EA580C"           # Orange info foncé
INFO_CYAN = "#0A192F"             # Bleu nuit info

# Couleurs spéciales (thème EduManager+)
PURPLE_ACCENT = "#64FFDA"         # Violet accent (cyan)
PINK_ACCENT = "#64FFDA"           # Rose accent (cyan)
GOLD_ACCENT = "#D97706"           # Or accent
SILVER_ACCENT = "#8aa0b8"         # Argent accent
EMERALD_ACCENT = "#059669"        # Émeraude accent
CORAL_ACCENT = "#DC2626"         # Corail accent
DARK_ACCENT = "#0b1d34"          # Fond des cartes
DARK_ACCENT_ALT = "#0E1C36"      # Fond sidebar alternatif
DARK_ACCENT_WARM = "#1f3b5a"     # Bordure chaud
DARK_ACCENT_COOL = "#64FFDA"     # Accent froid

# Couleurs de survol (thème EduManager+)
HOVER_PRIMARY = "#0E1C36"         # Survol primaire (sidebar)
HOVER_SECONDARY = "#1f3b5a"      # Survol secondaire (bordure)
HOVER_SUCCESS = "#047857"        # Survol succès
HOVER_WARNING = "#B45309"        # Survol avertissement
HOVER_ERROR = "#B91C1C"          # Survol erreur
HOVER_INFO = "#C2410C"           # Survol info

# Couleurs de focus (thème EduManager+)
FOCUS_PRIMARY = "#64FFDA"         # Focus primaire (accent cyan)
FOCUS_SUCCESS = "#059669"         # Focus succès
FOCUS_WARNING = "#D97706"         # Focus avertissement
FOCUS_ERROR = "#DC2626"          # Focus erreur

# =================== THÈME CUSTOMTKINTER PARFAIT =====================

# Configuration du thème CustomTkinter (thème EduManager+)
CTK_THEME = {
    "name": "edumanager_theme",
    "description": "Thème EduManager+ avec fond sombre et accents cyan",
    
    # Couleurs de base (thème EduManager+)
    "fg_color": [BG_MAIN, BG_MAIN],               # Fond principal
    "top_fg_color": [BG_SIDEBAR, BG_SIDEBAR],     # Header sidebar
    "corner_radius": 20,                         # Rayon des coins très arrondi
    
    # Couleurs des composants (thème EduManager+)
    "button_color": [ACCENT, ACCENT],             # Boutons accent cyan
    "button_hover_color": [HOVER_PRIMARY, HOVER_PRIMARY], # Hover sidebar
    "button_text_color": [TEXT, TEXT],            # Texte principal
    
    # Couleurs des entrées (thème EduManager+)
    "entry_fg_color": [CARD_BG, CARD_BG],         # Fond des entrées (cartes)
    "entry_border_color": [BORDER_COLOR, ACCENT], # Bordure / accent
    "entry_text_color": [TEXT, TEXT],             # Texte principal
    
    # Couleurs des labels (thème EduManager+)
    "text_color": [TEXT, TEXT],                   # Texte principal
    "text_color_disabled": [MUTED, MUTED],        # Texte atténué
    
    # Couleurs des frames (thème EduManager+)
    "frame_color": [CARD_BG, CARD_BG],            # Fond des frames (cartes)
    "frame_border_color": [BORDER_COLOR, BORDER_COLOR], # Bordure
    
    # Couleurs des scrollbars (thème EduManager+)
    "scrollbar_color": [ACCENT, ACCENT],          # Scrollbar accent
    "scrollbar_button_color": [BORDER_COLOR, BORDER_COLOR], # Boutons scrollbar
    "scrollbar_button_hover_color": [ACCENT, ACCENT], # Hover scrollbar accent
}

# =================== COULEURS SPÉCIFIQUES EDU MANAGER =====================

# Couleurs pour le tableau de bord (thème EduManager+)
# BG_MAIN, BG_SIDEBAR, CARD_BG, BORDER_COLOR, ACCENT, TEXT, MUTED déjà définis plus haut
BG_CARD = CARD_BG                          # Cartes (alias)
BG_CARD_HOVER = HOVER_PRIMARY              # Hover sidebar
BG_SECONDARY = BORDER_COLOR                # Fond secondaire (bordure)

# Couleurs de texte (thème EduManager+)
TEXT_PRIMARY = TEXT                         # Texte principal
TEXT_SECONDARY = MUTED                      # Texte secondaire
TEXT_MUTED = MUTED                          # Texte atténué
TEXT_ACCENT = "#10B981"                        # Texte accent vert émeraude moderne

# Couleurs des bordures (thème EduManager+)
# BORDER_COLOR déjà défini plus haut
BORDER_LIGHT = ACCENT                       # Bordure claire accent
BORDER_ACCENT = ACCENT                      # Bordure accent

# Couleurs des boutons (thème EduManager+)
BTN_PRIMARY = ACCENT                        # Bouton principal accent
BTN_SECONDARY = BORDER_COLOR                # Bouton secondaire bordure
BTN_SUCCESS = SUCCESS_GREEN                 # Bouton succès vert
BTN_WARNING = WARNING_YELLOW                # Bouton avertissement jaune
BTN_DANGER = ERROR_RED                      # Bouton danger rouge
BTN_INFO = INFO_ORANGE                      # Bouton info orange
BTN_TRANSFER = ACCENT                       # Bouton transfert accent

# Couleurs des états (parfaites pour le sombre)
STATE_SUCCESS = SUCCESS_GREEN              # État succès
STATE_WARNING = WARNING_YELLOW             # État avertissement
STATE_ERROR = ERROR_RED                    # État erreur
STATE_INFO = INFO_ORANGE                    # État info

# =================== GRADIENTS EDU MANAGER+ =====================

# Gradients pour les effets visuels (thème EduManager+)
GRADIENT_PRIMARY = [BG_MAIN, BG_SIDEBAR]             # Gradient principal vers sidebar
GRADIENT_SECONDARY = [BG_SIDEBAR, CARD_BG]           # Gradient sidebar vers cartes
GRADIENT_ACCENT = [ACCENT, SUCCESS_GREEN]            # Gradient accent vers vert
GRADIENT_CARD = [CARD_BG, BORDER_COLOR]              # Gradient carte vers bordure
GRADIENT_BUTTON = [ACCENT, BORDER_COLOR]             # Gradient bouton accent
GRADIENT_HOVER = [BORDER_COLOR, BG_SIDEBAR]          # Gradient survol
GRADIENT_PREMIUM = [ACCENT, BG_MAIN]                 # Gradient premium accent
GRADIENT_SUCCESS = [SUCCESS_GREEN, "#2EA043"]        # Gradient succès vert
GRADIENT_WARNING = [WARNING_YELLOW, "#BF8700"]       # Gradient avertissement jaune
GRADIENT_ERROR = [ERROR_RED, "#DA3633"]              # Gradient erreur rouge
GRADIENT_DARK = [BG_MAIN, BG_SIDEBAR]                # Gradient sombre pur
GRADIENT_GLOW = [ACCENT, BG_MAIN]                    # Gradient lueur accent

# =================== OMBRES EDU MANAGER+ =====================

# Couleurs d'ombres (thème EduManager+)
SHADOW_COLOR = "rgba(10, 25, 47, 0.6)"             # Ombre principale (BG_MAIN)
SHADOW_LIGHT = "rgba(100, 255, 218, 0.4)"          # Ombre accent cyan
SHADOW_DARK = "rgba(0, 0, 0, 0.8)"                 # Ombre très foncée
SHADOW_CARD = "rgba(11, 29, 52, 0.5)"              # Ombre des cartes
SHADOW_BUTTON = "rgba(100, 255, 218, 0.5)"         # Ombre des boutons accent
SHADOW_HOVER = "rgba(100, 255, 218, 0.3)"          # Ombre au survol accent
SHADOW_PREMIUM = "rgba(100, 255, 218, 0.4)"        # Ombre premium accent
SHADOW_SUCCESS = "rgba(63, 185, 80, 0.4)"          # Ombre succès verte
SHADOW_WARNING = "rgba(210, 153, 34, 0.4)"         # Ombre avertissement jaune
SHADOW_ERROR = "rgba(248, 81, 73, 0.4)"            # Ombre erreur rouge
SHADOW_GLOW = "rgba(100, 255, 218, 0.6)"           # Ombre lueur accent

# =================== POLICES PARFAITES =====================

# Polices (parfaites pour le sombre)
FONT_PRIMARY = ("Segoe UI", 14)                   # Police principale moderne
FONT_SECONDARY = ("Segoe UI", 12)                 # Police secondaire moderne
FONT_TITLE = ("Segoe UI", 24, "bold")             # Police titre grande
FONT_SUBTITLE = ("Segoe UI", 18, "bold")          # Police sous-titre moderne
FONT_SMALL = ("Segoe UI", 11)                     # Police petite moderne
FONT_BUTTON = ("Segoe UI", 13, "bold")            # Police boutons moderne
FONT_CARD_TITLE = ("Segoe UI", 16, "bold")        # Police titre de carte moderne
FONT_METRIC = ("Segoe UI", 20, "bold")            # Police métriques grande
FONT_PREMIUM = ("Segoe UI", 17, "bold")           # Police premium moderne
FONT_ACCENT = ("Segoe UI", 13, "bold")            # Police accent moderne
FONT_HERO = ("Segoe UI", 28, "bold")              # Police héro très grande

# Variables de police simplifiées pour compatibilité
FONT = "Segoe UI"                                 # Nom de police simple
FONT_SIZE_TITLE = 24                              # Taille titre
FONT_SIZE_HEADER = 18                             # Taille header
FONT_SIZE_TEXT = 14                               # Taille texte
FONT_SIZE_SMALL = 12                              # Taille petit texte

# =================== ESPACEMENTS PARFAITS =====================

# Espacements (parfaits pour le sombre)
PADDING_SMALL = 10                                # Petit espacement moderne
PADDING_MEDIUM = 18                               # Espacement moyen moderne
PADDING_LARGE = 28                                # Grand espacement moderne
PADDING_XLARGE = 36                               # Très grand espacement moderne
PADDING_CARD = 24                                 # Espacement des cartes moderne
PADDING_BUTTON = 18                               # Espacement des boutons moderne
PADDING_PREMIUM = 32                              # Espacement premium moderne
PADDING_HERO = 40                                 # Espacement héro très grand

# Marges (parfaites pour le sombre)
MARGIN_SMALL = 8                                  # Petite marge moderne
MARGIN_MEDIUM = 16                                # Marge moyenne moderne
MARGIN_LARGE = 24                                 # Grande marge moderne
MARGIN_CARD = 18                                  # Marge des cartes moderne
MARGIN_SECTION = 24                               # Marge des sections moderne
MARGIN_PREMIUM = 32                               # Marge premium moderne
MARGIN_HERO = 40                                  # Marge héro très grande

# =================== FONCTIONS UTILITAIRES PARFAITES =====================

def get_theme_colors():
    """Retourne toutes les couleurs du thème sombre parfait"""
    return {
        "primary": PRIMARY_BLUE,
        "dark": DARK_BLUE,
        "deeper": DEEPER_BLUE,
        "navy": NAVY_BLUE,
        "darker": DARKER_BLUE,
        "light": LIGHT_BLUE,
        "accent": ACCENT_BLUE,
        "soft": SOFT_BLUE,
        "pale": PALE_BLUE,
        "muted": MUTED_BLUE,
        "dark_gray": DARK_GRAY,
        "medium_gray": MEDIUM_GRAY,
        "light_gray": LIGHT_GRAY,
        "white": WHITE,
        "off_white": OFF_WHITE,
        "pure_white": PURE_WHITE,
        "success": SUCCESS_GREEN,
        "warning": WARNING_YELLOW,
        "error": ERROR_RED,
        "info": INFO_CYAN,
        "purple": PURPLE_ACCENT,
        "pink": PINK_ACCENT,
        "gold": GOLD_ACCENT,
        "silver": SILVER_ACCENT,
        "emerald": EMERALD_ACCENT,
        "coral": CORAL_ACCENT
    }

def get_ctk_theme():
    """Retourne la configuration du thème CustomTkinter parfait"""
    return CTK_THEME

def apply_theme_to_app(app):
    """Applique le thème sombre parfait à une application CustomTkinter"""
    try:
        import customtkinter as ctk
        
        # Définir le mode de couleur sombre
        ctk.set_appearance_mode("dark")
        
        # Définir le thème de couleur sombre
        ctk.set_default_color_theme("blue")
        
        # Appliquer les couleurs personnalisées
        app.configure(fg_color=BG_MAIN)
        
        return True
    except Exception as e:
        print(f"⚠️ Erreur application thème: {e}")
        return False

def get_gradient_colors(gradient_name="primary"):
    """Retourne les couleurs d'un gradient parfait"""
    gradients = {
        "primary": GRADIENT_PRIMARY,
        "secondary": GRADIENT_SECONDARY,
        "accent": GRADIENT_ACCENT,
        "card": GRADIENT_CARD,
        "button": GRADIENT_BUTTON,
        "hover": GRADIENT_HOVER,
        "premium": GRADIENT_PREMIUM,
        "success": GRADIENT_SUCCESS,
        "warning": GRADIENT_WARNING,
        "error": GRADIENT_ERROR,
        "dark": GRADIENT_DARK,
        "glow": GRADIENT_GLOW
    }
    return gradients.get(gradient_name, GRADIENT_PRIMARY)

def get_shadow_color(shadow_type="default"):
    """Retourne la couleur d'ombre parfaite"""
    shadows = {
        "default": SHADOW_COLOR,
        "light": SHADOW_LIGHT,
        "dark": SHADOW_DARK,
        "card": SHADOW_CARD,
        "button": SHADOW_BUTTON,
        "hover": SHADOW_HOVER,
        "premium": SHADOW_PREMIUM,
        "success": SHADOW_SUCCESS,
        "warning": SHADOW_WARNING,
        "error": SHADOW_ERROR,
        "glow": SHADOW_GLOW
    }
    return shadows.get(shadow_type, SHADOW_COLOR)

def get_font_config(font_type="primary"):
    """Retourne la configuration de police parfaite"""
    fonts = {
        "primary": FONT_PRIMARY,
        "secondary": FONT_SECONDARY,
        "title": FONT_TITLE,
        "subtitle": FONT_SUBTITLE,
        "small": FONT_SMALL,
        "button": FONT_BUTTON,
        "card_title": FONT_CARD_TITLE,
        "metric": FONT_METRIC,
        "premium": FONT_PREMIUM,
        "accent": FONT_ACCENT,
        "hero": FONT_HERO
    }
    return fonts.get(font_type, FONT_PRIMARY)

def get_spacing_config(spacing_type="medium"):
    """Retourne la configuration d'espacement parfaite"""
    spacings = {
        "small": PADDING_SMALL,
        "medium": PADDING_MEDIUM,
        "large": PADDING_LARGE,
        "xlarge": PADDING_XLARGE,
        "card": PADDING_CARD,
        "button": PADDING_BUTTON,
        "premium": PADDING_PREMIUM,
        "hero": PADDING_HERO
    }
    return spacings.get(spacing_type, PADDING_MEDIUM)

def get_special_colors():
    """Retourne les couleurs spéciales du thème"""
    return {
        "purple": PURPLE_ACCENT,
        "pink": PINK_ACCENT,
        "gold": GOLD_ACCENT,
        "silver": SILVER_ACCENT,
        "emerald": EMERALD_ACCENT,
        "coral": CORAL_ACCENT
    }

def get_modern_colors():
    """Retourne les couleurs modernes principales"""
    return {
        "primary": PRIMARY_BLUE,
        "accent": ACCENT_BLUE,
        "success": SUCCESS_GREEN,
        "warning": WARNING_YELLOW,
        "error": ERROR_RED,
        "info": INFO_ORANGE
    }

def get_hover_colors():
    """Retourne les couleurs de survol"""
    return {
        "primary": HOVER_PRIMARY,
        "secondary": HOVER_SECONDARY,
        "success": HOVER_SUCCESS,
        "warning": HOVER_WARNING,
        "error": HOVER_ERROR,
        "info": HOVER_INFO
    }

def get_focus_colors():
    """Retourne les couleurs de focus pour l'accessibilité"""
    return {
        "primary": FOCUS_PRIMARY,
        "success": FOCUS_SUCCESS,
        "warning": FOCUS_WARNING,
        "error": FOCUS_ERROR
    }

def get_dark_theme_colors():
    """Retourne toutes les couleurs du thème EduManager+"""
    return {
        "bg_main": BG_MAIN,
        "bg_sidebar": BG_SIDEBAR,
        "bg_card": CARD_BG,
        "bg_hover": HOVER_PRIMARY,
        "bg_secondary": BORDER_COLOR,
        "text_primary": TEXT,
        "text_secondary": MUTED,
        "text_muted": MUTED,
        "text_accent": ACCENT,
        "border": BORDER_COLOR,
        "border_light": ACCENT,
        "border_accent": ACCENT
    }

# =================== EXPORT DES COULEURS PARFAITES =====================

# Export de toutes les couleurs pour faciliter l'import
__all__ = [
    # Couleurs principales parfaites
    "PRIMARY_BLUE", "DARK_BLUE", "DEEPER_BLUE", "NAVY_BLUE", "DARKER_BLUE",
    "LIGHT_BLUE", "ACCENT_BLUE", "SOFT_BLUE", "PALE_BLUE", "MUTED_BLUE",
    
    # Couleurs neutres parfaites
    "DARK_GRAY", "MEDIUM_GRAY", "LIGHT_GRAY", "WHITE", "OFF_WHITE", "PURE_WHITE",
    
    # Couleurs d'état parfaites
    "SUCCESS_GREEN", "WARNING_YELLOW", "WARNING_ORANGE", "ERROR_RED", "INFO_ORANGE", "INFO_CYAN",
    
    # Couleurs spéciales parfaites
    "PURPLE_ACCENT", "PINK_ACCENT", "GOLD_ACCENT", "SILVER_ACCENT", "EMERALD_ACCENT", "CORAL_ACCENT", "DARK_ACCENT",
    
    # Couleurs de survol parfaites
    "HOVER_PRIMARY", "HOVER_SECONDARY", "HOVER_SUCCESS", "HOVER_WARNING", "HOVER_ERROR", "HOVER_INFO",
    
    # Couleurs de focus parfaites
    "FOCUS_PRIMARY", "FOCUS_SUCCESS", "FOCUS_WARNING", "FOCUS_ERROR",
    
    # Couleurs EduManager+ principales
    "BG_MAIN", "BG_SIDEBAR", "CARD_BG", "BORDER_COLOR", "ACCENT", "TEXT", "MUTED",
    "BG_CARD", "BG_CARD_HOVER", "BG_SECONDARY",
    "TEXT_PRIMARY", "TEXT_SECONDARY", "TEXT_MUTED", "TEXT_ACCENT",
    "BORDER_LIGHT", "BORDER_ACCENT",
    "BTN_PRIMARY", "BTN_SECONDARY", "BTN_SUCCESS", "BTN_WARNING", "BTN_DANGER", "BTN_INFO", "BTN_TRANSFER",
    "STATE_SUCCESS", "STATE_WARNING", "STATE_ERROR", "STATE_INFO",
    
    # Polices parfaites
    "FONT_PRIMARY", "FONT_SECONDARY", "FONT_TITLE", "FONT_SUBTITLE", "FONT_SMALL",
    "FONT_BUTTON", "FONT_CARD_TITLE", "FONT_METRIC", "FONT_PREMIUM", "FONT_ACCENT", "FONT_HERO",
    "FONT", "FONT_SIZE_TITLE", "FONT_SIZE_HEADER", "FONT_SIZE_TEXT", "FONT_SIZE_SMALL",
    
    # Espacements parfaits
    "PADDING_SMALL", "PADDING_MEDIUM", "PADDING_LARGE", "PADDING_XLARGE", "PADDING_CARD", "PADDING_BUTTON", "PADDING_PREMIUM", "PADDING_HERO",
    "MARGIN_SMALL", "MARGIN_MEDIUM", "MARGIN_LARGE", "MARGIN_CARD", "MARGIN_SECTION", "MARGIN_PREMIUM", "MARGIN_HERO",
    
    # Gradients parfaits
    "GRADIENT_PRIMARY", "GRADIENT_SECONDARY", "GRADIENT_ACCENT", "GRADIENT_CARD", "GRADIENT_BUTTON", "GRADIENT_HOVER",
    "GRADIENT_PREMIUM", "GRADIENT_SUCCESS", "GRADIENT_WARNING", "GRADIENT_ERROR", "GRADIENT_DARK", "GRADIENT_GLOW",
    
    # Ombres parfaites
    "SHADOW_COLOR", "SHADOW_LIGHT", "SHADOW_DARK", "SHADOW_CARD", "SHADOW_BUTTON", "SHADOW_HOVER",
    "SHADOW_PREMIUM", "SHADOW_SUCCESS", "SHADOW_WARNING", "SHADOW_ERROR", "SHADOW_GLOW",
    
    # Fonctions parfaites
    "get_theme_colors", "get_ctk_theme", "apply_theme_to_app", "get_gradient_colors", 
    "get_shadow_color", "get_font_config", "get_spacing_config", "get_special_colors", 
    "get_modern_colors", "get_hover_colors", "get_focus_colors", "get_dark_theme_colors"
]