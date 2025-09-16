# theme.py
import os

THEME = {
    "bg_main": "#0A192F",
    "header_bg": "#172A45",
    "card_bg": "#0B2039",
    "border_color": "#334155",
    "accent_blue": "#64FFDA",
    "primary_text": "#CCD6F6",
    "secondary_text": "#8892B0",
    "error_red": "#FF6363",
    "success_green": "#A0E7E5",
    "warning_yellow": "#FFD700",
    "info_orange": "#F97316"
}

FONT_FAMILY = "Segoe UI"
FONT_SIZE_TITLE = 28
FONT_SIZE_HEADER = 18
FONT_SIZE_TEXT = 14

ICON_PATH_BASE = os.path.join(os.path.dirname(__file__), "assets", "icons")

ICON_MAP = {
    "eleves": "book.png",
    "filles": "eleve.png",
    "garcons": "person.png",
    "classes": "cover.png",
    "profs": "profs.png",
    "ajouter": "add.png",
    "edit": "edit.png",
    "delete": "delete.png",
    "detail": "detail.png",
    "transferer": "transfer.png",
    "refresh": "refresh.png",
    "search": "search.png",
    "chevron_right": "chevron_right.png",
    "home": "home.png",
    "person": "person.png",
    "group": "group.png",
    "door": "door.png",
    "book": "book.png",
    "notes": "notes.png",
    "check": "check.png",
    "file": "file.png",
    "bell": "bell.png",
    "calendar": "calendar.png",
    "money": "money.png",
    "logout": "logout.png",
    "close": "close.png"
}
