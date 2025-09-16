# 🚀 Guide d'Utilisation Rapide - EduManager+

## 🎯 **Démarrage Rapide**

### **1. Première Utilisation**
```bash
# Créer la structure complète du système
python repair_system.py

# Ou utiliser le démarrage automatique
python start_app.py
```

### **2. Démarrage Normal**
```bash
# Lancer directement l'application
python main.py

# Ou utiliser le script de démarrage intelligent
python start_app.py
```

## 🔐 **Connexion au Système**

### **Utilisateurs de Test Disponibles**

| Rôle | Nom d'utilisateur | Mot de passe | Permissions |
|------|-------------------|--------------|-------------|
| **Super Administrateur** | `admin` | `admin123` | Accès complet à tout |
| **Directeur** | `directeur` | `directeur123` | Gestion globale |
| **Professeur** | `prof1` | `prof123` | Gestion des notes et présences |
| **Secrétaire** | `secretaire` | `secretaire123` | Gestion administrative |
| **Élève** | `eleve1` | `eleve123` | Consultation uniquement |
| **Parent** | `parent1` | `parent123` | Consultation des bulletins |

## 🎨 **Interface Utilisateur**

### **Sidebar - Navigation Principale**
- **📊 Tableau de Bord** - Vue d'ensemble et statistiques
- **📝 Notes** - Gestion des notes des élèves
- **✅ Présences** - Suivi des présences et absences
- **📋 Bulletins** - Création et consultation des bulletins
- **👥 Élèves** - Gestion des dossiers élèves
- **👨‍🏫 Professeurs** - Gestion des enseignants
- **🏫 Classes** - Organisation des classes
- **📚 Matières** - Gestion du programme
- **👤 Utilisateurs** - Gestion des comptes (Admin uniquement)
- **🔐 Rôles** - Gestion des permissions (Admin uniquement)

### **Contrôle d'Accès par Rôle**
- **Super Admin** : Accès complet à toutes les fonctionnalités
- **Directeur** : Accès à la gestion pédagogique et administrative
- **Professeur** : Accès aux notes, présences, et informations de ses classes
- **Secrétaire** : Accès aux données administratives et de gestion
- **Élève** : Consultation de ses propres informations
- **Parent** : Consultation des informations de ses enfants

## 🛠️ **Fonctionnalités Principales**

### **📊 Tableau de Bord**
- Statistiques en temps réel
- Indicateurs de performance
- Graphiques et visualisations
- Notifications importantes

### **📝 Gestion des Notes**
- Saisie des notes par matière
- Calcul automatique des moyennes
- Historique des évaluations
- Export des résultats

### **✅ Suivi des Présences**
- Marquage des présences/absences
- Justificatifs et motifs
- Statistiques de fréquentation
- Alertes automatiques

### **📋 Bulletins Scolaires**
- Génération automatique
- Personnalisation des modèles
- Impression et export PDF
- Archivage sécurisé

## 🔧 **Maintenance et Dépannage**

### **Scripts de Maintenance**
```bash
# Diagnostic complet du système
python test_system.py

# Test du système de permissions
python test_permissions.py

# Réparation automatique complète
python repair_system.py

# Vérification de la base de données
python -c "import sqlite3; conn = sqlite3.connect('database/edumanager.db'); cursor = conn.cursor(); cursor.execute('SELECT name FROM sqlite_master WHERE type=\"table\"'); print('Tables:', [row[0] for row in cursor.fetchall()]); conn.close()"
```

### **Problèmes Courants**

#### **❌ "database is locked"**
```bash
# Fermer toutes les instances et relancer
python repair_system.py
```

#### **❌ "no such table"**
```bash
# Recréer les tables manquantes
python init_tables.py
python init_test_data.py
```

#### **❌ Erreur de permissions**
```bash
# Réassigner les rôles
python assign_roles.py
python test_permissions.py
```

## 📁 **Structure des Fichiers**

```
Gestion_scolaire/
├── 📁 models/           # Modèles de données
│   ├── auth.py         # Authentification
│   ├── role.py         # Gestion des rôles
│   └── permissions.py  # Système de permissions
├── 📁 views/            # Interfaces utilisateur
│   ├── login_view.py   # Écran de connexion
│   ├── dashboard_view.py # Tableau de bord principal
│   └── view_manager.py # Gestionnaire de vues
├── 📁 database/         # Base de données SQLite
├── 📁 assets/           # Images et ressources
├── 📁 logs/             # Fichiers de log
├── 📁 reports/          # Rapports générés
├── 📁 backups/          # Sauvegardes
├── 🔧 repair_system.py  # Réparation automatique
├── 🚀 start_app.py      # Démarrage intelligent
├── ⚙️ config.py         # Configuration centralisée
└── 📖 README.md         # Documentation complète
```

## 🎮 **Raccourcis et Astuces**

### **Navigation Rapide**
- **Ctrl+N** : Nouvelle note
- **Ctrl+P** : Nouvelle présence
- **Ctrl+B** : Nouveau bulletin
- **Ctrl+S** : Sauvegarder
- **F5** : Actualiser les données

### **Recherche et Filtres**
- Utilisez la barre de recherche pour trouver rapidement
- Filtrez par classe, matière, ou période
- Triez les colonnes en cliquant sur les en-têtes

### **Export et Impression**
- Exportez les données en CSV, Excel, ou PDF
- Imprimez les rapports directement
- Sauvegardez les graphiques en image

## 🔒 **Sécurité et Sauvegarde**

### **Sauvegarde Automatique**
```bash
# Créer une sauvegarde manuelle
cp database/edumanager.db database/edumanager_backup_$(date +%Y%m%d).db

# Restaurer une sauvegarde
cp database/edumanager_backup_YYYYMMDD.db database/edumanager.db
```

### **Gestion des Sessions**
- Sessions automatiquement fermées après 24h d'inactivité
- Déconnexion forcée en cas de problème de sécurité
- Logs de toutes les actions importantes

## 📞 **Support et Aide**

### **En Cas de Problème**
1. **Consultez** ce guide d'utilisation
2. **Exécutez** `python repair_system.py`
3. **Vérifiez** les logs dans le dossier `logs/`
4. **Consultez** le fichier `TROUBLESHOOTING.md`

### **Informations Système**
```bash
# Vérifier la version
python -c "import config; info = config.get_version_info(); print(f'{info['name']} v{info['version']}')"

# Vérifier l'état
python test_system.py
```

## 🎉 **Félicitations !**

Vous êtes maintenant prêt à utiliser **EduManager+** ! 

**💡 Conseil :** Commencez par explorer le tableau de bord avec le compte `admin` pour découvrir toutes les fonctionnalités disponibles.

**🚀 Bonne utilisation !**
