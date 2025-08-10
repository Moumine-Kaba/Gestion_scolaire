import customtkinter as ctk
from tkinter import messagebox, StringVar
import tkinter.font as tkfont
import textwrap
import os
import sys
from PIL import Image

# Importation des contrôleurs pour les matières
# Le chemin de la base de données est géré par le contrôleur
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from controllers.matiere_controller import get_all_matieres, search_matieres, add_matiere, update_matiere, delete_matiere

# ====== THEME / ICONS (fallback) ======
# Ce bloc est un fallback au cas où l'importation depuis main.py échoue
try:
    from main import THEME, FONT_FAMILY, FONT_SIZE_HEADER, FONT_SIZE_SUBHEADER, FONT_SIZE_TEXT
    from main import load_ctk_icon, ICON_MAP
except ImportError:
    THEME = {
        "bg_main": "#0A192F", "header_bg": "#172A45", "card_bg": "#0B2039",
        "border_color": "#334155", "accent_blue": "#64FFDA",
        "primary_text": "#CCD6F6", "secondary_text": "#8892B0",
        "error_red": "#FF6363", "success_green": "#A0E7E5",
        "warning_yellow": "#FFD700", "info_orange": "#F97316",
        "select_highlight": "#2A456C"
    }
    FONT_FAMILY = "Segoe UI"
    FONT_SIZE_HEADER = 20
    FONT_SIZE_SUBHEADER = 16
    FONT_SIZE_TEXT = 14

    def load_ctk_icon(icon_name, size=(22, 22)):
        try:
            ICON_PATH = "assets/icons"
            p = os.path.join(ICON_PATH, icon_name)
            im = Image.open(p).resize(size, Image.Resampling.LANCZOS)
            return ctk.CTkImage(light_image=im, dark_image=im)
        except Exception:
            return None

    ICON_MAP = {
        "add": "add.png", "edit": "edit.png", "delete": "delete.png",
        "refresh": "refresh.png", "search": "search.png", "close": "close.png", "stacks": "stacks.png"
    }

# ====== VIEW ======
class MatieresView(ctk.CTkFrame):
    DEBOUNCE_MS = 250
    BODY_SIDE_PADDING = 16

    def __init__(self, parent, icons=None):
        super().__init__(parent, fg_color=THEME["bg_main"])
        self.grid_columnconfigure(0, weight=1)

        self.var_search = StringVar()
        self._search_after_id = None
        self._matieres_cache = []

        self._build_header()
        self._build_stats()
        self._build_cards_area()

        self.charger_matieres()

    # ---------- HEADER ----------
    def _build_header(self):
        header = ctk.CTkFrame(self, fg_color=THEME["header_bg"], corner_radius=14)
        header.pack(fill="x", padx=18, pady=(18,10))

        left = ctk.CTkFrame(header, fg_color="transparent")
        left.pack(side="left", padx=14, pady=12)
        ctk.CTkLabel(left, text="Gestion des Matières",
            font=(FONT_FAMILY, FONT_SIZE_HEADER, "bold"),
            text_color=THEME["accent_blue"]).pack(anchor="w")
        ctk.CTkLabel(left, text="Ajoutez, modifiez et recherchez vos matières en un clic.",
            font=(FONT_FAMILY, max(FONT_SIZE_TEXT-2,10)),
            text_color=THEME["secondary_text"]).pack(anchor="w", pady=(2,0))

        right = ctk.CTkFrame(header, fg_color="transparent")
        right.pack(side="right", padx=12, pady=12)

        s_icon = load_ctk_icon(ICON_MAP.get("search","search.png"), (18,18))
        x_icon = load_ctk_icon(ICON_MAP.get("close","close.png"), (16,16))

        wrap = ctk.CTkFrame(right, fg_color=THEME["card_bg"], corner_radius=12,
                            border_width=1, border_color=THEME["border_color"])
        wrap.pack(side="left", padx=(0,8))
        ctk.CTkLabel(wrap, text="", image=s_icon).pack(side="left", padx=(10,6), pady=6)
        self.entry_search = ctk.CTkEntry(
            wrap, width=260, corner_radius=10,
            fg_color=THEME["card_bg"], border_color=THEME["card_bg"],
            text_color=THEME["primary_text"],
            placeholder_text="Rechercher une matière...",
            textvariable=self.var_search, font=(FONT_FAMILY, FONT_SIZE_TEXT)
        )
        self.entry_search.pack(side="left", padx=(0,4), pady=6)
        self.entry_search.bind("<Return>", lambda e: self._apply_search())

        ctk.CTkButton(
            wrap, width=30, text="✕" if x_icon is None else "",
            image=None if x_icon is None else x_icon,
            fg_color=THEME["card_bg"], text_color=THEME["secondary_text"],
            hover_color=THEME["header_bg"], command=self._clear_search
        ).pack(side="left", padx=(2,8), pady=6)

        add_icon = load_ctk_icon(ICON_MAP.get("add","add.png"))
        ref_icon = load_ctk_icon(ICON_MAP.get("refresh","refresh.png"))
        ctk.CTkButton(right, text=" Ajouter", image=add_icon, compound="left",
            font=(FONT_FAMILY, FONT_SIZE_TEXT, "bold"),
            fg_color=THEME["accent_blue"], text_color=THEME["bg_main"],
            hover_color="#45b69c", command=self.ajouter_matiere).pack(side="left", padx=6)
        ctk.CTkButton(right, text=" Actualiser", image=ref_icon, compound="left",
            font=(FONT_FAMILY, FONT_SIZE_TEXT, "bold"),
            fg_color=THEME["card_bg"], text_color=THEME["primary_text"],
            hover_color=THEME["header_bg"], command=self._refresh_all).pack(side="left")

        self.var_search.trace_add("write", self._on_search_change)

    # ---------- STATS ----------
    def _build_stats(self):
        bar = ctk.CTkFrame(self, fg_color="transparent")
        bar.pack(fill="x", padx=20, pady=(6,6))
        self.lbl_count = ctk.CTkLabel(bar, text="", font=(FONT_FAMILY, FONT_SIZE_TEXT), text_color=THEME["secondary_text"])
        self.lbl_count.pack(side="left")

    # ---------- CARDS ----------
    def _build_cards_area(self):
        self.cards_area = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.cards_area.pack(fill="both", expand=True, padx=20, pady=(0,18))
        self.cards_area.grid_columnconfigure((0,1,2), weight=1, uniform="col")

    # ---------- DATA FLOW ----------
    def charger_matieres(self, q=""):
        data = search_matieres(q) if q.strip() else get_all_matieres()
        self._matieres_cache = data
        self._render_cards(data)
        self._update_count(len(data))

    def _refresh_all(self):
        self.var_search.set("")
        self.charger_matieres()
        self.entry_search.focus_set()

    def _update_count(self, n):
        self.lbl_count.configure(text=f"{n} matière(s) affichée(s)")

    def _clear_search(self):
        self.var_search.set("")
        self.charger_matieres()
        self.entry_search.focus_set()

    def _apply_search(self):
        self.charger_matieres(self.var_search.get())

    def _on_search_change(self, *_):
        if hasattr(self, "_search_after_id") and self._search_after_id:
            try: self.after_cancel(self._search_after_id)
            except: pass
        self._search_after_id = self.after(self.DEBOUNCE_MS, self._apply_search)

    # ---------- RENDER ----------
    def _render_cards(self, matieres):
        for w in self.cards_area.winfo_children():
            w.destroy()

        if not matieres:
            ctk.CTkLabel(self.cards_area, text="Aucune matière trouvée.",
                         font=(FONT_FAMILY, FONT_SIZE_SUBHEADER, "italic"),
                         text_color=THEME["secondary_text"])\
                .grid(row=0, column=0, padx=10, pady=40, sticky="nsew", columnspan=3)
            return

        for i, m in enumerate(matieres):
            r, c = divmod(i, 3)
            self._create_matiere_card(m).grid(row=r, column=c, sticky="nsew", padx=10, pady=10)

    def _create_matiere_card(self, matiere: dict):
        card = ctk.CTkFrame(self.cards_area, fg_color=THEME["card_bg"],
                            corner_radius=18, border_width=1, border_color=THEME["border_color"])
        card.grid_columnconfigure(0, weight=0)
        card.grid_columnconfigure(1, weight=1)

        ctk.CTkFrame(card, fg_color=THEME["accent_blue"], width=8, corner_radius=18)\
            .grid(row=0, column=0, rowspan=3, sticky="nsw")

        body = ctk.CTkFrame(card, fg_color="transparent")
        body.grid(row=0, column=1, sticky="nsew",
                  padx=(self.BODY_SIDE_PADDING, self.BODY_SIDE_PADDING), pady=(10,6))
        body.grid_columnconfigure(0, weight=1)

        header = ctk.CTkFrame(body, fg_color="transparent")
        header.grid(row=0, column=0, sticky="ew", pady=(2,6))
        icon = load_ctk_icon(ICON_MAP.get("stacks","stacks.png"), (22,22))
        ctk.CTkLabel(header, text="", image=icon).pack(side="left")
        ctk.CTkLabel(header, text=matiere.get("nom","Sans nom"),
                     font=(FONT_FAMILY, FONT_SIZE_SUBHEADER, "bold"),
                     text_color=THEME["primary_text"]).pack(side="left", padx=(8,6))
        initiale = (matiere.get("nom","M")[:1] or "M").upper()
        ctk.CTkLabel(header, text=initiale, width=26, height=26,
                     font=(FONT_FAMILY, FONT_SIZE_TEXT, "bold"),
                     text_color=THEME["bg_main"], fg_color=THEME["accent_blue"],
                     corner_radius=999).pack(side="right")

        full = (matiere.get("description") or "").strip() or "Aucune description."
        font_desc = tkfont.Font(family=FONT_FAMILY, size=FONT_SIZE_TEXT)
        line_h = font_desc.metrics("linespace")

        desc = ctk.CTkTextbox(
            body, height=1,
            fg_color=THEME["card_bg"], text_color=THEME["secondary_text"],
            border_width=0, corner_radius=0
        )
        try: desc._textbox.configure(wrap="word")
        except Exception: pass
        desc.grid(row=1, column=0, sticky="ew", pady=(0,6))
        desc.insert("1.0", full)
        desc.configure(state="disabled")

        def _resize_desc(_=None):
            usable_w = max(body.winfo_width() - 2*self.BODY_SIDE_PADDING, 220)
            avg_char_w = max(font_desc.measure("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz")/52, 1)
            chars_per_line = max(int(usable_w / avg_char_w), 10)
            wrapped = textwrap.wrap(full, width=chars_per_line)
            lines = max(1, len(wrapped))
            target_h = lines * line_h + 6
            try:
                desc.configure(height=target_h)
            except Exception:
                pass

        card.bind("<Configure>", _resize_desc)

        footer = ctk.CTkFrame(card, fg_color="transparent")
        footer.grid(row=2, column=1, sticky="ew",
                    padx=(self.BODY_SIDE_PADDING, self.BODY_SIDE_PADDING), pady=(0,10))
        e_ic = load_ctk_icon(ICON_MAP.get("edit","edit.png"))
        d_ic = load_ctk_icon(ICON_MAP.get("delete","delete.png"))
        ctk.CTkButton(footer, text="Modifier", image=e_ic, compound="left",
                      font=(FONT_FAMILY, FONT_SIZE_TEXT, "bold"),
                      fg_color=THEME["info_orange"], hover_color="#cc9f13",
                      text_color=THEME["primary_text"],
                      command=lambda m=matiere: self.modifier_matiere(m))\
            .pack(side="left", expand=True, fill="x", padx=1)
        ctk.CTkButton(footer, text="Supprimer", image=d_ic, compound="left",
                      font=(FONT_FAMILY, FONT_SIZE_TEXT, "bold"),
                      fg_color=THEME["error_red"], hover_color="#dc2626",
                      text_color=THEME["primary_text"],
                      command=lambda mid=matiere["id"]: self.supprimer_matiere(mid))\
            .pack(side="left", expand=True, fill="x", padx=1)

        return card

    # ---------- Actions ----------
    def ajouter_matiere(self):
        self._open_form_dialog("Ajouter")
    
    def modifier_matiere(self, m):
        self._open_form_dialog("Modifier", m)

    def supprimer_matiere(self, mid):
        if messagebox.askyesno("Confirmation", f"Voulez-vous vraiment supprimer la matière #{mid} ?"):
            if delete_matiere(mid):
                self.charger_matieres(self.var_search.get())
                messagebox.showinfo("Succès", "Matière supprimée avec succès.")
            else:
                messagebox.showerror("Erreur", "La suppression a échoué.")

    # ---------- Formulaire ----------
    def _open_form_dialog(self, mode, data=None):
        top = ctk.CTkToplevel(self)
        top.title(f"{mode} une Matière")
        top.geometry("520x420")
        top.configure(fg_color=THEME["header_bg"])
        top.grab_set()
        top.update_idletasks()
        W,H = 520,420; x = (top.winfo_screenwidth()//2)-(W//2); y = (top.winfo_screenheight()//2)-(H//2)
        top.geometry(f"{W}x{H}+{x}+{y}")

        wrap = ctk.CTkFrame(top, fg_color=THEME["card_bg"], corner_radius=16,
                            border_width=1, border_color=THEME["border_color"])
        wrap.pack(fill="both", expand=True, padx=14, pady=14)
        wrap.grid_rowconfigure(5, weight=1)
        wrap.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(wrap, text=f"{mode} une Matière",
                     font=(FONT_FAMILY, FONT_SIZE_HEADER, "bold"),
                     text_color=THEME["accent_blue"]).grid(row=0, column=0, sticky="w", padx=16, pady=(12,6))

        ctk.CTkLabel(wrap, text="Nom", font=(FONT_FAMILY, FONT_SIZE_TEXT),
                     text_color=THEME["primary_text"]).grid(row=1, column=0, sticky="w", padx=16, pady=(4,2))
        entry_nom = ctk.CTkEntry(wrap, placeholder_text="Ex: Mathématiques",
                                 font=(FONT_FAMILY, FONT_SIZE_TEXT),
                                 fg_color=THEME["header_bg"], text_color=THEME["primary_text"],
                                 border_color=THEME["border_color"])
        entry_nom.grid(row=2, column=0, sticky="ew", padx=16, pady=(0,8))

        ctk.CTkLabel(wrap, text="Description", font=(FONT_FAMILY, FONT_SIZE_TEXT),
                     text_color=THEME["primary_text"]).grid(row=3, column=0, sticky="w", padx=16, pady=(6,2))
        entry_desc = ctk.CTkTextbox(wrap, height=160,
                                    fg_color=THEME["header_bg"], text_color=THEME["primary_text"],
                                    border_color=THEME["border_color"])
        try: entry_desc._textbox.configure(wrap="word")
        except Exception: pass
        entry_desc.grid(row=4, column=0, sticky="nsew", padx=16, pady=(0,8))

        if mode == "Modifier" and data:
            entry_nom.insert(0, data.get("nom",""))
            entry_desc.insert("1.0", data.get("description",""))

        btns = ctk.CTkFrame(wrap, fg_color="transparent")
        btns.grid(row=6, column=0, pady=(4,10))
        def on_save():
            nom = entry_nom.get().strip()
            desc = entry_desc.get("1.0","end-1c").strip()
            if not nom:
                messagebox.showerror("Erreur","Le nom de la matière est obligatoire.", parent=top)
                return
            if len(nom)>100:
                messagebox.showerror("Erreur","Nom trop long (max 100).", parent=top)
                return
            ok = add_matiere(nom, desc) if mode=="Ajouter" else update_matiere(data["id"], nom, desc)
            if ok:
                messagebox.showinfo("Succès", f"Matière {'ajoutée' if mode=='Ajouter' else 'modifiée'} avec succès.", parent=top)
                self.charger_matieres(self.var_search.get())
                top.destroy()
            else:
                messagebox.showerror("Erreur", f"{mode} impossible. Vérifiez l’unicité du nom.", parent=top)

        ctk.CTkButton(btns, text="💾 Enregistrer", font=(FONT_FAMILY, FONT_SIZE_TEXT, "bold"),
                      fg_color=THEME["accent_blue"], text_color=THEME["bg_main"],
                      hover_color="#45b69c", command=on_save).pack(side="left", padx=6)
        ctk.CTkButton(btns, text="❌ Annuler", font=(FONT_FAMILY, FONT_SIZE_TEXT, "bold"),
                      fg_color=THEME["error_red"], text_color=THEME["primary_text"],
                      hover_color="#dc2626", command=top.destroy).pack(side="left", padx=6)

        top.bind("<Escape>", lambda e: top.destroy())
        top.bind("<Return>", lambda e: on_save())
        top.bind("<Control-s>", lambda e: on_save())
        entry_nom.focus_set()