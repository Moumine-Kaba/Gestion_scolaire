import sys
import os
sys.path.append('src')

from database.connection import get_db_connection
from datetime import datetime, timedelta
import random

def add_20_guinean_professors():
    """Ajoute 20 professeurs avec des noms guinéens"""
    
    # Noms guinéens authentiques
    noms_guineens = [
        "Diallo", "Bah", "Camara", "Keita", "Sow", "Barry", "Traore", "Cisse", 
        "Conde", "Toure", "Kone", "Sangare", "Fofana", "Sylla", "Diawara",
        "Kourouma", "Doumbouya", "Kante", "Coulibaly", "Diakite", "Sidibe",
        "Ouattara", "Sanogo", "Diarra", "Kouyate", "Sissoko", "Bamba",
        "Dramé", "Fall", "Ndiaye", "Gueye", "Mbaye", "Diop", "Thiam"
    ]
    
    prenoms_guineens = [
        "Mamadou", "Fatou", "Ibrahima", "Aminata", "Ousmane", "Mariama", 
        "Alpha", "Aissatou", "Mohamed", "Kadiatou", "Sekou", "Fanta",
        "Boubacar", "Hawa", "Lamine", "Aicha", "Moussa", "Ramatou",
        "Cheick", "Fatoumata", "Amadou", "Kadija", "Saliou", "Aminata",
        "Bakary", "Maimouna", "Saidou", "Nafissatou", "Djibril", "Marietou",
        "Abdoulaye", "Aissata", "Mamady", "Kadiatou", "Souleymane", "Fatouma",
        "Ibrahima", "Aminata", "Oumar", "Mariama", "Cheikh", "Aissatou"
    ]
    
    specialites = [
        "Mathématiques", "Français", "Histoire-Géographie", "Sciences Physiques",
        "Sciences Naturelles", "Anglais", "Éducation Physique", "Arts Plastiques",
        "Musique", "Informatique", "Économie", "Philosophie", "Espagnol",
        "Arabe", "Allemand", "Chimie", "Biologie", "Physique", "Géographie",
        "Littérature", "Grammaire", "Comptabilité", "Droit", "Sociologie"
    ]
    
    statuts = ["Actif", "Actif", "Actif", "Actif", "Inactif"]  # Plus d'actifs
    
    conn = get_db_connection()
    if not conn:
        print("❌ Impossible de se connecter à la base de données")
        return False
    
    try:
        cursor = conn.cursor()
        
        print("🚀 Ajout de 20 professeurs guinéens...")
        
        for i in range(20):
            # Génération des données
            nom = random.choice(noms_guineens)
            prenom = random.choice(prenoms_guineens)
            email = f"{prenom.lower()}.{nom.lower()}@ecole-guinee.gn"
            telephone = f"6{random.randint(10, 99)}{random.randint(100000, 999999)}"
            specialite = random.choice(specialites)
            statut = random.choice(statuts)
            
            # Configuration salariale réaliste pour la Guinée
            taux_horaire = random.randint(15000, 35000)  # 15k-35k GNF/heure
            heures_par_session = 2.0
            sessions_semaine = random.randint(8, 15)  # 8-15 sessions/semaine
            
            # Calculs automatiques
            heures_semaine = sessions_semaine * heures_par_session
            heures_mois = heures_semaine * 4.33
            heures_annee_scolaire = heures_mois * 9
            
            salaire_semaine = heures_semaine * taux_horaire
            salaire_mois = heures_mois * taux_horaire
            salaire_annee = heures_annee_scolaire * taux_horaire
            
            # Date d'embauche aléatoire dans les 3 dernières années
            date_embauche = datetime.now() - timedelta(days=random.randint(30, 1095))
            
            # Insertion en base
            cursor.execute("""
                INSERT INTO professeurs (
                    nom, prenom, email, telephone, specialite, statut, date_embauche,
                    heures_par_session, sessions_semaine, salaire_horaire, heures_mensuelles,
                    salaire_base, salaire_net, date_creation, date_modification
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                nom, prenom, email, telephone, specialite, statut, 
                date_embauche.strftime("%Y-%m-%d"),
                heures_par_session, sessions_semaine, taux_horaire, heures_mois,
                salaire_mois, salaire_mois,  # salaire_base = salaire_net = salaire_mois
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            ))
            
            print(f"✅ {i+1:2d}. {prenom} {nom} - {specialite} - {salaire_mois:,.0f} GNF/mois")
        
        conn.commit()
        print(f"\n🎉 {20} professeurs guinéens ajoutés avec succès !")
        print("💰 Calculs automatiques appliqués pour tous les salaires")
        print("📊 Prêts à être utilisés dans l'interface")
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors de l'ajout: {e}")
        return False
    finally:
        conn.close()

if __name__ == "__main__":
    add_20_guinean_professors()
