#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Démonstration du taux de réussite par classe
Script de test pour le graphique des taux de réussite
"""

import sys
import os
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import customtkinter as ctk

# Ajouter le chemin du projet
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Importer les modules nécessaires
from src.modules.auth.views.dashboard_view import UltraModernGraphFrame
from resources.themes.theme import *

def create_demo_data():
    """Crée des données de démonstration pour les classes"""
    print("🎯 Création des données de démonstration...")
    
    # Données réalistes pour toutes les classes
    classes_data = {
        # PRIMAIRE
        "6°": 78.5,
        "5°": 82.3, 
        "4°": 75.8,
        "3°": 85.2,
        "2°": 79.1,
        "1°": 88.7,
        
        # COLLÈGE
        "7°": 76.4,
        "8°": 81.2,
        "9°": 77.9,
        "10°": 83.6,
        
        # LYCÉE
        "11° SE": 79.8,
        "11° SM": 85.1,
        "11° SS": 72.3,
        "12° SE": 80.5,
        "12° SM": 84.7,
        "12° SS": 75.2,
        "TSE": 87.3,
        "TSM": 89.1,
        "TSS": 76.8
    }
    
    return list(classes_data.keys()), list(classes_data.values())

def demo_taux_reussite():
    """Démonstration du taux de réussite par classe"""
    print("🚀 Démonstration du Taux de Réussite par Classe")
    print("=" * 50)
    
    # Créer les données de démonstration
    labels, data_points = create_demo_data()
    
    print(f"📊 Classes analysées: {len(labels)}")
    print(f"📈 Données: {data_points}")
    
    # Calculer le taux de réussite global
    taux_reussite_global = sum(1 for taux in data_points if taux >= 70) / len(data_points) * 100
    print(f"🎯 Taux de réussite global: {taux_reussite_global:.1f}%")
    
    # Créer le DataFrame pandas
    df = pd.DataFrame({
        'Matiere': labels,
        'Moyenne': data_points
    })
    
    # Ajouter des colonnes calculées
    df['Niveau'] = df['Moyenne'].apply(lambda x: 
        'Excellent' if x >= 80 else 
        'Bon' if x >= 70 else 
        'Moyen' if x >= 60 else 'Faible')
    
    df['Couleur'] = df['Moyenne'].apply(lambda x: 
        SUCCESS_GREEN if x >= 80 else 
        WARNING_YELLOW if x >= 70 else 
        "#FF6B35" if x >= 60 else ERROR_RED)
    
    df['Emoji'] = df['Moyenne'].apply(lambda x: 
        "🟢" if x >= 80 else 
        "🟡" if x >= 70 else 
        "🟠" if x >= 60 else "🔴")
    
    print("\n📋 Résumé par classe:")
    print("-" * 30)
    for _, row in df.iterrows():
        print(f"{row['Matiere']:>8}: {row['Moyenne']:>5.1f}% {row['Emoji']} ({row['Niveau']})")
    
    return df

def create_demo_chart(df):
    """Crée le graphique de démonstration"""
    print("\n🎨 Création du graphique de démonstration...")
    
    # Configuration matplotlib
    plt.style.use('dark_background')
    fig = plt.Figure(figsize=(14, 8), dpi=100)
    ax = fig.add_subplot(111)
    
    # Ajuster les marges
    fig.subplots_adjust(bottom=0.4, top=0.85, left=0.1, right=0.95)
    
    # Données pour le graphique
    x_pos = range(len(df))
    
    # Graphique en barres
    bars = ax.bar(x_pos, df['Moyenne'], color=df['Couleur'], alpha=0.8, 
                 edgecolor=TEXT, linewidth=2, width=0.5)
    
    # Ajouter des valeurs sur les barres
    for i, row in df.iterrows():
        if row['Moyenne'] > 0:
            ax.annotate(f"{row['Moyenne']:.1f}% {row['Emoji']}", 
                       (i, row['Moyenne']), textcoords="offset points", 
                       xytext=(-15, 10), ha='left', va='bottom', 
                       color=TEXT, fontweight='bold', fontsize=8,
                       bbox=dict(boxstyle="round,pad=0.3", facecolor=CARD_BG, 
                               edgecolor=row['Couleur'], alpha=0.9))
    
    # Configuration des axes
    ax.set_xticks(x_pos)
    labels_with_icons = df.apply(lambda row: f"🎓 {row['Matiere']}", axis=1).tolist()
    ax.set_xticklabels(labels_with_icons, rotation=60, ha='right', color=TEXT, fontsize=9)
    
    # Titre et labels
    ax.set_ylabel("Taux de Réussite (%)", color=TEXT, fontsize=12, fontweight='bold')
    ax.set_title("📊 Démonstration - Taux de Réussite par Classe", color=TEXT, fontsize=16, fontweight='bold', pad=20)
    
    # Style des axes
    ax.tick_params(axis='y', colors=TEXT, labelsize=10)
    ax.tick_params(axis='x', colors=TEXT, labelsize=9, pad=10)
    
    # Couleurs des bordures
    ax.spines['bottom'].set_color(BORDER_COLOR)
    ax.spines['left'].set_color(BORDER_COLOR)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    
    # Fond
    ax.set_facecolor(CARD_BG)
    fig.patch.set_facecolor(CARD_BG)
    
    # Ligne de moyenne
    avg_value = df['Moyenne'].mean()
    ax.axhline(y=avg_value, color=TEXT, linestyle='--', linewidth=2, alpha=0.7)
    
    # Texte du taux de réussite global
    taux_reussite_global = sum(1 for taux in df['Moyenne'] if taux >= 70) / len(df['Moyenne']) * 100
    max_val = df['Moyenne'].max()
    ax.text(len(df)-1, max_val * 0.9, f'Taux de Réussite Global: {taux_reussite_global:.1f}%', 
            color=TEXT, fontweight='bold', fontsize=11, ha='right',
            bbox=dict(boxstyle="round,pad=0.3", facecolor=CARD_BG, 
                     edgecolor=BORDER_COLOR, alpha=0.9))
    
    # Légende
    legend_elements = [
        plt.Rectangle((0,0),1,1, facecolor=SUCCESS_GREEN, alpha=0.8, label='Excellent (≥80%)'),
        plt.Rectangle((0,0),1,1, facecolor=WARNING_YELLOW, alpha=0.8, label='Bon (70-79%)'),
        plt.Rectangle((0,0),1,1, facecolor="#FF6B35", alpha=0.8, label='Moyen (60-69%)'),
        plt.Rectangle((0,0),1,1, facecolor=ERROR_RED, alpha=0.8, label='Faible (<60%)')
    ]
    ax.legend(handles=legend_elements, loc='upper right', frameon=True, 
             facecolor=CARD_BG, edgecolor=BORDER_COLOR, fontsize=10)
    
    return fig

def main():
    """Fonction principale de démonstration"""
    print("🎯 DÉMONSTRATION DU TAUX DE RÉUSSITE PAR CLASSE")
    print("=" * 60)
    
    try:
        # Créer les données de démonstration
        df = demo_taux_reussite()
        
        # Créer le graphique
        fig = create_demo_chart(df)
        
        # Créer l'interface CustomTkinter
        root = ctk.CTk()
        root.title("📊 Démonstration - Taux de Réussite par Classe")
        root.geometry("1200x800")
        root.configure(fg_color=BG_MAIN)
        
        # Titre principal
        title_label = ctk.CTkLabel(
            root,
            text="📊 Démonstration du Taux de Réussite par Classe",
            font=("Segoe UI", 24, "bold"),
            text_color=TEXT
        )
        title_label.pack(pady=20)
        
        # Sous-titre
        subtitle_label = ctk.CTkLabel(
            root,
            text="Performance académique par classe avec taux de réussite global",
            font=("Segoe UI", 14),
            text_color=MUTED
        )
        subtitle_label.pack(pady=(0, 20))
        
        # Frame pour le graphique
        chart_frame = ctk.CTkFrame(root, fg_color=CARD_BG)
        chart_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        # Intégrer le graphique matplotlib
        canvas = FigureCanvasTkAgg(fig, chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True, padx=10, pady=10)
        
        # Statistiques
        stats_frame = ctk.CTkFrame(root, fg_color=CARD_BG)
        stats_frame.pack(fill="x", padx=20, pady=(0, 20))
        
        # Calculer les statistiques
        total_classes = len(df)
        excellent_classes = len(df[df['Moyenne'] >= 80])
        bon_classes = len(df[(df['Moyenne'] >= 70) & (df['Moyenne'] < 80)])
        moyen_classes = len(df[(df['Moyenne'] >= 60) & (df['Moyenne'] < 70)])
        faible_classes = len(df[df['Moyenne'] < 60])
        taux_reussite_global = sum(1 for taux in df['Moyenne'] if taux >= 70) / len(df['Moyenne']) * 100
        
        stats_text = f"""
📊 STATISTIQUES:
• Total des classes: {total_classes}
• Excellent (≥80%): {excellent_classes} classes
• Bon (70-79%): {bon_classes} classes  
• Moyen (60-69%): {moyen_classes} classes
• Faible (<60%): {faible_classes} classes
• Taux de réussite global: {taux_reussite_global:.1f}%
        """
        
        stats_label = ctk.CTkLabel(
            stats_frame,
            text=stats_text,
            font=("Segoe UI", 12),
            text_color=TEXT,
            justify="left"
        )
        stats_label.pack(pady=15)
        
        print("\n✅ Démonstration prête ! Interface graphique lancée...")
        print("📊 Graphique affiché avec toutes les classes et leurs taux de réussite")
        
        # Lancer l'interface
        root.mainloop()
        
    except Exception as e:
        print(f"❌ Erreur lors de la démonstration: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
