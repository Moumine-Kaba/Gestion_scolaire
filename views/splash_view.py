import tkinter as tk
from PIL import Image, ImageTk
import time
import os
import sys

# Assurer que la racine du projet est dans sys.path.
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if project_root not in sys.path:
    sys.path.append(project_root)

def afficher_splash_suivi_par_connexion():
    root = tk.Tk()
    root.overrideredirect(True)
    root.configure(bg="#0f172a")
    largeur, hauteur = 500, 350
    x = (root.winfo_screenwidth() // 2) - (largeur // 2)
    y = (root.winfo_screenheight() // 2) - (hauteur // 2)
    root.geometry(f"{largeur}x{hauteur}+{x}+{y}")

    try:
        logo = Image.open("assets/icons/logo.png").resize((140, 140))
        logo_tk = ImageTk.PhotoImage(logo)
        label_logo = tk.Label(root, image=logo_tk, bg="#0f172a")
        label_logo.image = logo_tk
        label_logo.pack(pady=(35, 5))
    except:
        tk.Label(root, text="EduManager+", font=("Segoe UI Black", 32),
                 fg="#38bdf8", bg="#0f172a").pack(pady=35)

    tk.Label(root, text="Chargement...", font=("Segoe UI", 17, "bold"),
             fg="#f1f5f9", bg="#0f172a").pack(pady=(10, 0))
    dots = tk.Label(root, text="", font=("Segoe UI", 28), fg="#38bdf8", bg="#0f172a")
    dots.pack(pady=(10, 0))

    def animate_and_next():
        for i in range(18):
            dots["text"] = "." * (i % 4)
            root.update()
            time.sleep(0.18)
        root.destroy()
        
        # Correction ici : importez la classe MainApp, pas une fonction
        from views.dashboard_view import MainApp
        
        utilisateur = {'username': 'admin'}
        app = MainApp(utilisateur)
        app.mainloop()

    root.after(0, animate_and_next)
    root.mainloop()

if __name__ == '__main__':
    afficher_splash_suivi_par_connexion()