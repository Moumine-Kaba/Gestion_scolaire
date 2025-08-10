import customtkinter as ctk
from tkinter import messagebox, filedialog
import os
import sys
import csv
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
from tkinter import Toplevel
from CTkTable import CTkTable

# Assurez-vous que ces chemins sont corrects pour votre structure de projet
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from controllers.notes_controller import get_all_notes, add_note, update_note, delete_note, get_notes_by_eleve
from controllers.eleve_controller import get_all_eleves
from controllers.matiere_controller import get_all_matieres
from controllers.classe_controller import get_all_classes

# =================== IMPORT THEME ET COULEURS NEUMORPHISM =====================
THEME = {
    "bg_main": "#233146",
    "header_bg":"#0A192F",
    "card_bg": "#2b2952",
    "border_color": "#40546c",
    "accent_blue": "#64FFDA",
    "primary_text": "#E0E6F0",
    "secondary_text": "#AAB5C6",
    "error_red": "#FF6363",
    "success_green": "#A0E7E5",
    "warning_yellow": "#FFD700",
    "info_orange": "#F97316",
    "select_highlight": "#30435b",
}
FONT_FAMILY = "Segoe UI"
FONT_SIZE_HEADER = 22
FONT_SIZE_SUBHEADER = 18
FONT_SIZE_TEXT = 14

def load_ctk_icon(icon_name, size=(20, 20)):
    try:
        from PIL import Image
        ICON_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets", "icons")
        path = os.path.join(ICON_PATH, icon_name)
        image = Image.open(path).resize(size, Image.Resampling.LANCZOS)
        return ctk.CTkImage(light_image=image, dark_image=image)
    except Exception:
        return None

ICON_MAP = {
    "add": "add.png", "edit": "edit.png", "delete": "delete.png",
    "refresh": "refresh.png", "search": "search.png", "close": "close.png",
    "student": "person.png", "subject": "book.png", "note": "assignment.png",
    "date": "calendar.png", "export": "csv.png", "stats": "analytics.png",
    "grade": "grade.png", "class": "classroom.png", "sort": "sort.png"
}
    
class NotesView(ctk.CTkFrame):
    def __init__(self, parent, icons):
        super().__init__(parent, fg_color=THEME["bg_main"])
        self.icons = icons
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.selected_item_data = None
        self.selected_eleve_data = None
        self.selected_note_id = None
        
        self.eleves = {e["id"]: e for e in get_all_eleves()}
        self.classes = {c["id"]: c for c in get_all_classes()}
        self.matieres = {m["id"]: m for m in get_all_matieres()}

        self._build_main_ui()

    def _refresh_all(self):
        self.eleves = {e["id"]: e for e in get_all_eleves()}
        self.classes = {c["id"]: c for c in get_all_classes()}
        self.matieres = {m["id"]: m for m in get_all_matieres()}
        
        self.selected_eleve_data = None
        self.selected_note_id = None
        
        self._setup_class_dropdown()
        self._clear_dashboard()
        self._update_eleve_list()
        
    def _build_main_ui(self):
        main_frame = ctk.CTkFrame(self, fg_color="transparent")
        main_frame.pack(fill="both", expand=True, padx=15, pady=15)
        main_frame.grid_columnconfigure(1, weight=3)
        main_frame.grid_columnconfigure(0, weight=1)
        main_frame.grid_rowconfigure(0, weight=1)

        # Panneau de gauche: Sélection des élèves
        left_panel = ctk.CTkFrame(main_frame, fg_color=THEME["header_bg"], corner_radius=12)
        left_panel.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        left_panel.grid_columnconfigure(0, weight=1)
        left_panel.grid_rowconfigure(2, weight=1)
        
        self._build_student_selection_panel(left_panel)
        
        # Panneau de droite: Graphique, stats et tableau des notes
        right_panel = ctk.CTkFrame(main_frame, fg_color="transparent")
        right_panel.grid(row=0, column=1, sticky="nsew", padx=(10, 0))
        right_panel.grid_columnconfigure(0, weight=1)
        right_panel.grid_rowconfigure(0, weight=1)
        right_panel.grid_rowconfigure(1, weight=1)
        
        self._build_notes_dashboard(right_panel)
        
    def _build_student_selection_panel(self, parent_frame):
        header_frame = ctk.CTkFrame(parent_frame, fg_color="transparent")
        header_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=(10, 5))
        header_frame.grid_columnconfigure(0, weight=1)
        
        ctk.CTkLabel(header_frame, text="SÉLECTIONNER UN ÉLÈVE", 
                      font=(FONT_FAMILY, FONT_SIZE_SUBHEADER, "bold"),
                      text_color=THEME["primary_text"]).grid(row=0, column=0, sticky="w")
        
        refresh_icon = load_ctk_icon(ICON_MAP.get("refresh"), size=(20, 20))
        ctk.CTkButton(header_frame, text="", image=refresh_icon, width=35,
                      fg_color="transparent", hover_color=THEME["select_highlight"],
                      command=self._refresh_all).grid(row=0, column=1, sticky="e")
        
        selection_frame = ctk.CTkFrame(parent_frame, fg_color="transparent")
        selection_frame.grid(row=1, column=0, sticky="ew", padx=10, pady=5)
        selection_frame.grid_columnconfigure((0, 1), weight=1, uniform="selection_col")
        
        classe_options = ["Sélectionnez une classe..."] + [c["nom"] for c in self.classes.values()]
        self.classe_dropdown = ctk.CTkComboBox(
            selection_frame, values=classe_options,
            command=self._on_classe_selected,
            font=(FONT_FAMILY, FONT_SIZE_TEXT),
            fg_color=THEME["card_bg"],
            dropdown_fg_color=THEME["card_bg"],
            dropdown_hover_color=THEME["select_highlight"],
            border_color=THEME["border_color"]
        )
        self.classe_dropdown.grid(row=0, column=0, sticky="ew", padx=(0, 5))
        
        self.search_entry = ctk.CTkEntry(
            selection_frame, placeholder_text="Rechercher...",
            font=(FONT_FAMILY, FONT_SIZE_TEXT),
            fg_color=THEME["card_bg"],
            border_color=THEME["border_color"]
        )
        self.search_entry.grid(row=0, column=1, sticky="ew", padx=(5, 0))
        self.search_entry.bind("<KeyRelease>", self._filter_eleves)
        
        self.eleve_list_frame = ctk.CTkScrollableFrame(parent_frame, fg_color="transparent")
        self.eleve_list_frame.grid(row=2, column=0, sticky="nsew", padx=10, pady=(5, 10))
        
        self._setup_class_dropdown()
        self._update_eleve_list()

    def _build_notes_dashboard(self, parent_frame):
        top_dashboard = ctk.CTkFrame(parent_frame, fg_color="transparent")
        top_dashboard.grid(row=0, column=0, sticky="nsew")
        top_dashboard.grid_columnconfigure(0, weight=2)
        top_dashboard.grid_columnconfigure(1, weight=1)
        
        self.chart_frame = ctk.CTkFrame(top_dashboard, fg_color=THEME["header_bg"], corner_radius=12)
        self.chart_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 10), pady=(0, 10))
        self.chart_frame.grid_propagate(False)
        
        self.stats_container = ctk.CTkFrame(top_dashboard, fg_color=THEME["header_bg"], corner_radius=12)
        self.stats_container.grid(row=0, column=1, sticky="nsew", padx=(10, 0), pady=(0, 10))
        self.stats_container.grid_propagate(False)

        self.table_panel = ctk.CTkFrame(parent_frame, fg_color=THEME["header_bg"], corner_radius=12)
        self.table_panel.grid(row=1, column=0, sticky="nsew", pady=(10, 0))
        self.table_panel.grid_columnconfigure(0, weight=1)
        self.table_panel.grid_rowconfigure(1, weight=1)
        
        self._build_table_header(self.table_panel)
        self.table_container = ctk.CTkFrame(self.table_panel, fg_color="transparent")
        self.table_container.grid(row=1, column=0, sticky="nsew", padx=10, pady=(0, 10))
        
        self._clear_dashboard()
    
    def _build_table_header(self, parent_frame):
        header_frame = ctk.CTkFrame(parent_frame, fg_color="transparent")
        header_frame.grid(row=0, column=0, sticky="ew", padx=15, pady=10)
        header_frame.grid_columnconfigure(0, weight=1)
        
        self.notes_title = ctk.CTkLabel(header_frame, text="Détails des notes",
                                        font=(FONT_FAMILY, FONT_SIZE_SUBHEADER, "bold"),
                                        text_color=THEME["primary_text"])
        self.notes_title.grid(row=0, column=0, sticky="w")
        
        actions_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        actions_frame.grid(row=0, column=1, sticky="e")
        
        add_icon = load_ctk_icon(ICON_MAP.get("add"), size=(18, 18))
        edit_icon = load_ctk_icon(ICON_MAP.get("edit"), size=(18, 18))
        delete_icon = load_ctk_icon(ICON_MAP.get("delete"), size=(18, 18))
        export_icon = load_ctk_icon(ICON_MAP.get("export"), size=(18, 18))

        ctk.CTkButton(actions_frame, text=" Ajouter", image=add_icon, compound="left",
                      font=(FONT_FAMILY, FONT_SIZE_TEXT - 2, "bold"),
                      fg_color=THEME["accent_blue"], text_color=THEME["bg_main"],
                      hover_color="#45b69c", command=self.ajouter).pack(side="left", padx=5)
        ctk.CTkButton(actions_frame, text=" Modifier", image=edit_icon, compound="left",
                      font=(FONT_FAMILY, FONT_SIZE_TEXT - 2, "bold"),
                      fg_color=THEME["info_orange"], text_color=THEME["bg_main"],
                      hover_color="#cc9f13", command=self.modifier).pack(side="left", padx=5)
        ctk.CTkButton(actions_frame, text=" Supprimer", image=delete_icon, compound="left",
                      font=(FONT_FAMILY, FONT_SIZE_TEXT - 2, "bold"),
                      fg_color=THEME["error_red"], text_color=THEME["bg_main"],
                      hover_color="#dc2626", command=self.supprimer).pack(side="left", padx=5)
        ctk.CTkButton(actions_frame, text=" Exporter", image=export_icon, compound="left",
                      font=(FONT_FAMILY, FONT_SIZE_TEXT - 2, "bold"),
                      fg_color=THEME["card_bg"], text_color=THEME["primary_text"],
                      hover_color=THEME["select_highlight"], command=self.exporter_notes).pack(side="left", padx=5)
    
    def _setup_class_dropdown(self):
        classe_options = ["Sélectionnez une classe..."] + [c["nom"] for c in self.classes.values()]
        self.classe_dropdown.configure(values=classe_options)
        self.classe_dropdown.set("Sélectionnez une classe...")

    def _on_classe_selected(self, selected_class_name):
        self.selected_eleve_data = None
        self._clear_dashboard()
        self._update_eleve_list()

    def _filter_eleves(self, event=None):
        self._update_eleve_list()

    def _update_eleve_list(self):
        search_query = self.search_entry.get().lower()
        selected_classe_name = self.classe_dropdown.get()
        
        for widget in self.eleve_list_frame.winfo_children():
            widget.destroy()

        filtered_eleves = list(self.eleves.values())
        
        if selected_classe_name != "Sélectionnez une classe...":
            classe_id = next((cid for cid, cdata in self.classes.items() if cdata["nom"] == selected_classe_name), None)
            if classe_id:
                filtered_eleves = [e for e in filtered_eleves if e.get("classe_id") == classe_id]

        if search_query:
            filtered_eleves = [
                e for e in filtered_eleves
                if search_query in f"{e['nom']} {e['prenom']}".lower()
            ]

        if not filtered_eleves:
            ctk.CTkLabel(self.eleve_list_frame, text="Aucun élève trouvé", 
                          text_color=THEME["secondary_text"]).pack(pady=10)
        
        for eleve in filtered_eleves:
            eleve_name = f"{eleve['nom']} {eleve['prenom']}"
            btn = ctk.CTkButton(self.eleve_list_frame, text=eleve_name, 
                                 command=lambda e=eleve: self.display_eleve_notes(e),
                                 font=(FONT_FAMILY, FONT_SIZE_TEXT),
                                 fg_color=THEME["card_bg"],
                                 hover_color=THEME["select_highlight"],
                                 corner_radius=10,
                                 text_color=THEME["primary_text"])
            btn.pack(fill="x", padx=5, pady=4)

    def display_eleve_notes(self, eleve_data):
        self.selected_eleve_data = eleve_data
        self.notes_title.configure(text=f"Notes de : {eleve_data['prenom']} {eleve_data['nom']}")
        self.rafraichir_liste()

    def _clear_dashboard(self):
        for widget in self.stats_container.winfo_children():
            widget.destroy()
        for widget in self.chart_frame.winfo_children():
            widget.destroy()
        for widget in self.table_container.winfo_children():
            widget.destroy()
        
        ctk.CTkLabel(self.chart_frame, text="Sélectionnez un élève pour visualiser ses notes.",
                      font=(FONT_FAMILY, FONT_SIZE_SUBHEADER, "italic"),
                      text_color=THEME["secondary_text"]).pack(expand=True, padx=20, pady=20)
        
        ctk.CTkLabel(self.stats_container, text="Aucune donnée à afficher.",
                      font=(FONT_FAMILY, FONT_SIZE_TEXT, "italic"),
                      text_color=THEME["secondary_text"]).pack(expand=True, padx=10, pady=10)
        
        ctk.CTkLabel(self.table_container, text="Aucune note à afficher.",
                      font=(FONT_FAMILY, FONT_SIZE_SUBHEADER, "italic"),
                      text_color=THEME["secondary_text"]).pack(expand=True, padx=20, pady=20)

    def rafraichir_liste(self):
        self.selected_note_id = None
        self.selected_item_data = None
        
        if self.selected_eleve_data:
            notes = get_notes_by_eleve(self.selected_eleve_data.get("id"))
            self._update_stats_display(notes)
            self._create_grade_evolution_chart(notes)
            self._update_notes_table(notes)
        else:
            self._clear_dashboard()

    def _update_stats_display(self, notes):
        for widget in self.stats_container.winfo_children():
            widget.destroy()

        if not notes:
            ctk.CTkLabel(self.stats_container, text="Aucune statistique à afficher.",
                          font=(FONT_FAMILY, FONT_SIZE_TEXT, "italic"),
                          text_color=THEME["secondary_text"]).pack(expand=True, padx=10, pady=10)
            return

        df = pd.DataFrame(notes)
        df.dropna(subset=['note', 'coefficient'], inplace=True)

        if not df.empty:
            total_points = (df['note'] * df['coefficient']).sum()
            total_coeff = df['coefficient'].sum()
            moyenne_generale = total_points / total_coeff if total_coeff > 0 else 0
            meilleure_note = df['note'].max()
            pire_note = df['note'].min()
            nombre_notes = len(df)
        else:
            moyenne_generale = meilleure_note = pire_note = nombre_notes = 0

        self._create_stats_card(self.stats_container, "Moyenne Générale", f"{moyenne_generale:.2f}", THEME["accent_blue"], ICON_MAP.get("grade"))
        self._create_stats_card(self.stats_container, "Meilleure Note", f"{meilleure_note}", THEME["success_green"], ICON_MAP.get("grade"))
        self._create_stats_card(self.stats_container, "Pire Note", f"{pire_note}", THEME["error_red"], ICON_MAP.get("grade"))
        self._create_stats_card(self.stats_container, "Nombre de notes", f"{nombre_notes}", THEME["info_orange"], ICON_MAP.get("subject"))

    def _create_stats_card(self, parent, title, value, color, icon_name):
        card = ctk.CTkFrame(parent, fg_color=THEME["card_bg"], corner_radius=10, height=60)
        card.pack(fill="x", pady=4, padx=8)
        card.grid_columnconfigure(1, weight=1)
        
        icon = load_ctk_icon(icon_name)
        if icon:
            ctk.CTkLabel(card, text="", image=icon, fg_color="transparent").grid(row=0, column=0, rowspan=2, padx=10, pady=8)
            
        ctk.CTkLabel(card, text=title, font=(FONT_FAMILY, FONT_SIZE_TEXT-2), text_color=THEME["secondary_text"]).grid(row=0, column=1, sticky="w")
        ctk.CTkLabel(card, text=value, font=(FONT_FAMILY, FONT_SIZE_SUBHEADER-2, "bold"), text_color=color).grid(row=1, column=1, sticky="w")

    def _create_grade_evolution_chart(self, notes):
        for widget in self.chart_frame.winfo_children():
            widget.destroy()

        if not notes:
            ctk.CTkLabel(self.chart_frame, text="Aucune donnée à afficher.",
                          font=(FONT_FAMILY, FONT_SIZE_SUBHEADER, "italic"),
                          text_color=THEME["secondary_text"]).pack(expand=True, padx=20, pady=20)
            return

        df = pd.DataFrame(notes)
        df['date'] = pd.to_datetime(df['date'], errors='coerce')
        df.sort_values(by='date', inplace=True)
        df.dropna(subset=['date', 'note', 'coefficient'], inplace=True)
        
        fig, ax = plt.subplots(figsize=(6, 4), facecolor=THEME["header_bg"])
        fig.patch.set_facecolor(THEME["header_bg"])
        
        if not df.empty:
            colors = plt.cm.viridis(np.linspace(0, 1, len(df['matiere_id'].unique())))
            for i, (matiere_id, group) in enumerate(df.groupby('matiere_id')):
                matiere_nom = self.matieres.get(matiere_id, {}).get("nom", "Inconnue")
                ax.plot(group['date'], group['note'], marker='o', linestyle='-', label=matiere_nom, color=colors[i])
            
            # Ajout de la moyenne mobile
            window_size = 3
            df['rolling_avg'] = df['note'].rolling(window=window_size).mean()
            ax.plot(df['date'], df['rolling_avg'], color='red', linestyle='--', label=f'Moyenne mobile ({window_size})', linewidth=2)


        ax.set_title("Évolution des notes", color=THEME["primary_text"], font=FONT_FAMILY, fontsize=FONT_SIZE_SUBHEADER)
        ax.set_xlabel("Date", color=THEME["secondary_text"], font=FONT_FAMILY, fontsize=FONT_SIZE_TEXT-2)
        ax.set_ylabel("Note", color=THEME["secondary_text"], font=FONT_FAMILY, fontsize=FONT_SIZE_TEXT-2)
        
        ax.tick_params(axis='x', colors=THEME["secondary_text"], rotation=45, labelsize=10)
        ax.tick_params(axis='y', colors=THEME["secondary_text"], labelsize=10)
        
        ax.set_facecolor(THEME["card_bg"])
        ax.spines['bottom'].set_color(THEME["border_color"])
        ax.spines['left'].set_color(THEME["border_color"])
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.legend(facecolor=THEME["card_bg"], edgecolor=THEME["border_color"], labelcolor=THEME["secondary_text"], fontsize=10)

        plt.tight_layout()
        
        canvas = FigureCanvasTkAgg(fig, master=self.chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True, padx=10, pady=10)

    def _update_notes_table(self, notes):
        for widget in self.table_container.winfo_children():
            widget.destroy()

        if not notes:
            ctk.CTkLabel(self.table_container, text="Aucune note trouvée pour cet élève.",
                          font=(FONT_FAMILY, FONT_SIZE_SUBHEADER, "italic"),
                          text_color=THEME["secondary_text"]).pack(expand=True, padx=20, pady=20)
            return

        headers = ["Matière", "Note", "Coeff.", "Date", "Commentaire"]
        data = [headers]
        
        for note in notes:
            matiere_nom = self.matieres.get(note.get("matiere_id"), {}).get("nom", "Inconnue")
            data.append([
                matiere_nom,
                note.get("note"),
                note.get("coefficient"),
                note.get("date"),
                note.get("commentaire", "Aucun")
            ])
            
        self.note_table = CTkTable(
            self.table_container, 
            values=data, 
            header_color=THEME["card_bg"],
            fg_color=THEME["header_bg"],
            hover_color=THEME["select_highlight"],
            text_color=THEME["primary_text"],
            font=(FONT_FAMILY, FONT_SIZE_TEXT),
            command=self._on_table_select,
            corner_radius=10,
            wraplength=150
        )
        self.note_table.pack(fill="both", expand=True, padx=5, pady=5)
        
        self.notes_data = notes

    def _on_table_select(self, cell):
        self.selected_note_id = None
        self.selected_item_data = None
        row_index = cell.get("row")
        if row_index > 0:
            self.selected_note_id = self.notes_data[row_index - 1].get("id")
            self.selected_item_data = self.notes_data[row_index - 1]

    def ajouter(self):
        if not self.selected_eleve_data:
            messagebox.showwarning("Ajouter", "Sélectionnez d'abord un élève pour lui ajouter une note.")
            return
        self.open_note_form("Ajouter")

    def modifier(self):
        if not self.selected_note_id:
            messagebox.showwarning("Modifier", "Sélectionnez une note à modifier.")
            return
        self.open_note_form("Modifier", self.selected_item_data)

    def supprimer(self):
        if not self.selected_note_id:
            messagebox.showwarning("Supprimer", "Sélectionnez une note à supprimer.")
            return
        if messagebox.askyesno("Confirmer la suppression", f"Êtes-vous sûr de vouloir supprimer cette note ?"):
            if delete_note(self.selected_note_id):
                messagebox.showinfo("Succès", "Note supprimée avec succès.")
                self.rafraichir_liste()
            else:
                messagebox.showerror("Erreur", "Échec de la suppression.")

    def open_note_form(self, mode, data=None):
        popup = ctk.CTkToplevel(self)
        popup.title(f"{mode} une Note")
        popup.geometry("450x550")
        popup.configure(fg_color=THEME["bg_main"])
        popup.grab_set()

        ctk.CTkLabel(popup, text=f"{mode} une Note",
                      font=(FONT_FAMILY, FONT_SIZE_SUBHEADER, "bold"),
                      text_color=THEME["accent_blue"]).pack(pady=(20, 10))
        
        form_frame = ctk.CTkFrame(popup, fg_color=THEME["header_bg"], corner_radius=12)
        form_frame.pack(fill="both", expand=True, padx=20, pady=(10, 20))
        form_frame.grid_columnconfigure(0, weight=1)

        # Rendre l'intérieur du formulaire plus compact et aligné
        inner_form_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        inner_form_frame.pack(fill="x", padx=30, pady=20)
        inner_form_frame.grid_columnconfigure(1, weight=1)

        def create_form_entry(parent, label_text, widget_type, row, default_value=None, options=None):
            ctk.CTkLabel(parent, text=label_text,
                          font=(FONT_FAMILY, FONT_SIZE_TEXT),
                          text_color=THEME["secondary_text"]).grid(row=row, column=0, sticky="w", pady=5)
            
            if widget_type == "entry":
                widget = ctk.CTkEntry(parent, font=(FONT_FAMILY, FONT_SIZE_TEXT), fg_color=THEME["card_bg"], border_color=THEME["border_color"])
                if default_value is not None:
                    widget.insert(0, default_value)
            elif widget_type == "combo":
                widget = ctk.CTkComboBox(parent, values=options, state="readonly",
                                          font=(FONT_FAMILY, FONT_SIZE_TEXT), fg_color=THEME["card_bg"],
                                          border_color=THEME["border_color"], dropdown_fg_color=THEME["card_bg"],
                                          dropdown_hover_color=THEME["select_highlight"])
                if default_value is not None:
                    widget.set(default_value)
            elif widget_type == "textbox":
                widget = ctk.CTkTextbox(parent, height=80, font=(FONT_FAMILY, FONT_SIZE_TEXT), fg_color=THEME["card_bg"], border_color=THEME["border_color"])
                if default_value is not None:
                    widget.insert("0.0", default_value)
            
            widget.grid(row=row, column=1, sticky="ew", padx=(10, 0), pady=5)
            return widget

        eleve_display_name = f"{self.selected_eleve_data['nom']} {self.selected_eleve_data['prenom']}"
        create_form_entry(inner_form_frame, "Élève:", "entry", 0, default_value=eleve_display_name).configure(state="disabled")

        matiere_options = [""] + [f"{m['id']} - {m['nom']}" for m in self.matieres.values()]
        matiere_combo = create_form_entry(inner_form_frame, "Matière:", "combo", 1, options=matiere_options)
        note_entry = create_form_entry(inner_form_frame, "Note:", "entry", 2)
        coeff_entry = create_form_entry(inner_form_frame, "Coefficient:", "entry", 3)
        date_entry = create_form_entry(inner_form_frame, "Date (AAAA-MM-JJ):", "entry", 4)
        comment_entry = create_form_entry(inner_form_frame, "Commentaire:", "textbox", 5)
        
        if mode == "Modifier" and data:
            if data.get("matiere_id") is not None and data["matiere_id"] in self.matieres:
                matiere_info = self.matieres[data["matiere_id"]]
                matiere_combo.set(f"{matiere_info['id']} - {matiere_info['nom']}")
            note_entry.insert(0, str(data.get("note", "")))
            coeff_entry.insert(0, str(data.get("coefficient", "1")))
            date_entry.insert(0, data.get("date", ""))
            commentaire_text = data.get("commentaire", "")
            if commentaire_text is not None:
                comment_entry.insert("0.0", str(commentaire_text))

        def save():
            try:
                matiere_str = matiere_combo.get()
                matiere_id = int(matiere_str.split(" - ")[0]) if matiere_str and " - " in matiere_str else None
                note_value = float(note_entry.get())
                coefficient = float(coeff_entry.get())
                date_note = date_entry.get()
                commentaire = comment_entry.get("1.0", "end-1c")
                
                if not matiere_id or note_value is None:
                    messagebox.showerror("Erreur", "Les champs Matière et Note sont obligatoires.", parent=popup)
                    return

                note_data = {
                    "eleve_id": self.selected_eleve_data['id'],
                    "matiere_id": matiere_id,
                    "note": note_value,
                    "coefficient": coefficient,
                    "date": date_note,
                    "commentaire": commentaire
                }
                
                if mode == "Ajouter":
                    add_note(note_data)
                    messagebox.showinfo("Succès", "Note ajoutée avec succès.", parent=popup)
                else:
                    note_data["id"] = data.get("id")
                    update_note(note_data)
                    messagebox.showinfo("Succès", "Note mise à jour avec succès.", parent=popup)
                
                self.rafraichir_liste()
                popup.destroy()

            except ValueError:
                messagebox.showerror("Erreur", "La note et le coefficient doivent être des nombres.", parent=popup)
            except Exception as e:
                messagebox.showerror("Erreur", f"Une erreur s'est produite : {e}", parent=popup)

        btn_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        btn_frame.pack(pady=(10, 20))
        ctk.CTkButton(btn_frame, text="Annuler", command=popup.destroy,
                      fg_color="gray", hover_color="#6e6e6e",
                      font=(FONT_FAMILY, FONT_SIZE_TEXT, "bold")).pack(side="left", padx=10)
        ctk.CTkButton(btn_frame, text="Enregistrer", command=save,
                      fg_color=THEME["accent_blue"], text_color=THEME["bg_main"],
                      hover_color="#45b69c",
                      font=(FONT_FAMILY, FONT_SIZE_TEXT, "bold")).pack(side="left", padx=10)

    def exporter_notes(self):
        if not self.selected_eleve_data:
            messagebox.showwarning("Exporter", "Sélectionnez un élève pour exporter ses notes.")
            return

        eleve_id = self.selected_eleve_data.get("id")
        notes = get_notes_by_eleve(eleve_id)
        if not notes:
            messagebox.showwarning("Exporter", "Aucune note à exporter pour cet élève.")
            return

        file_path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("Fichiers CSV", "*.csv")],
            title="Enregistrer les notes de l'élève"
        )
        if not file_path:
            return

        try:
            with open(file_path, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(["ID", "Élève", "Matière", "Note", "Coefficient", "Date", "Commentaire"])
                for note in notes:
                    eleve_name = f"{self.eleves.get(note['eleve_id'], {}).get('nom', 'Inconnu')} {self.eleves.get(note['eleve_id'], {}).get('prenom', '')}"
                    matiere_name = self.matieres.get(note["matiere_id"], {}).get("nom", "Inconnue")
                    writer.writerow([
                        note.get("id"),
                        eleve_name,
                        matiere_name,
                        note.get("note"),
                        note.get("coefficient", 1),
                        note.get("date"),
                        note.get("commentaire")
                    ])
            messagebox.showinfo("Exporter", f"Les notes de l'élève ont été exportées avec succès dans {file_path}")
        except Exception as e:
            messagebox.showerror("Erreur", f"Une erreur s'est produite lors de l'exportation : {e}")