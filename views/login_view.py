import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from controllers.user_controller import get_all_users
import hashlib

def check_login(username, password):
    hash_pwd = hashlib.sha256(password.encode()).hexdigest()
    for u in get_all_users():
        # u[1] = username, u[6] = password hash, u[7] = role
        if u[1] == username and u[6] == hash_pwd:
            return {
                "id": u[0],
                "username": u[1],
                "prenom": u[2],
                "nom": u[3],
                "email": u[4],
                "telephone": u[5],
                "role": u[7] if len(u) > 7 else "admin"
            }
    return None

def afficher_login():
    root = tk.Tk()
    root.title("Connexion EduManager+")
    root.geometry("440x520")
    root.configure(bg="#0f172a")
    root.resizable(False, False)

    try:
        logo = Image.open("assets/logo.png").resize((85, 85))
        logo_tk = ImageTk.PhotoImage(logo)
        tk.Label(root, image=logo_tk, bg="#0f172a").pack(pady=20)
    except:
        tk.Label(root, text="EduManager+", font=("Segoe UI Black", 28), fg="#38bdf8", bg="#0f172a").pack(pady=20)

    cadre = tk.Frame(root, bg="#1f2937", bd=0, relief="flat")
    cadre.place(relx=0.5, rely=0.53, anchor="center", width=350, height=270)

    tk.Label(cadre, text="Connexion", font=("Segoe UI", 20, "bold"), fg="#38bdf8", bg="#1f2937").pack(pady=(14, 16))

    entry_user = tk.Entry(cadre, font=("Segoe UI", 12), fg="#0ea5e9", bg="#111827", insertbackground="#38bdf8", relief="flat")
    entry_user.pack(fill="x", padx=28, pady=(0, 13))
    entry_user.insert(0, "Nom d'utilisateur")
    entry_user.bind("<FocusIn>", lambda e: entry_user.delete(0, tk.END) if entry_user.get() == "Nom d'utilisateur" else None)

    entry_pass = tk.Entry(cadre, font=("Segoe UI", 12), fg="#0ea5e9", bg="#111827", show="*", insertbackground="#38bdf8", relief="flat")
    entry_pass.pack(fill="x", padx=28, pady=(0, 16))
    entry_pass.insert(0, "Mot de passe")
    def on_focus_pass(e):
        if entry_pass.get() == "Mot de passe":
            entry_pass.delete(0, tk.END)
            entry_pass.config(show="*")
    entry_pass.bind("<FocusIn>", on_focus_pass)

    def on_login():
        user = entry_user.get().strip()
        pwd = entry_pass.get().strip()
        if not user or user == "Nom d'utilisateur" or not pwd or pwd == "Mot de passe":
            messagebox.showerror("Erreur", "Veuillez remplir tous les champs.")
            return
        utilisateur = check_login(user, pwd)
        if utilisateur:
            root.destroy()
            from views.dashboard_view import afficher_dashboard
            afficher_dashboard(utilisateur)
        else:
            messagebox.showerror("Connexion échouée", "Nom d'utilisateur ou mot de passe incorrect.")

    btn = tk.Button(cadre, text="Se connecter", font=("Segoe UI", 13, "bold"),
                    fg="white", bg="#38bdf8", relief="flat", command=on_login)
    btn.pack(fill="x", padx=28, pady=(0, 8), ipady=5)

    root.mainloop()
