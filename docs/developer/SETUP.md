# 🚀 Guide de Configuration Rapide - EduManager+

## ✅ **Système Prêt à l'Emploi !**

Votre système de gestion scolaire avec authentification et rôles est maintenant **100% fonctionnel** !

## 🔧 **Installation et Configuration**

### **1. Vérifier les Dépendances**
```bash
pip install customtkinter Pillow matplotlib
```

### **2. Tester le Système**
```bash
python test_system.py
```
*Tous les tests doivent passer avec succès ✅*

### **3. Créer les Utilisateurs de Test**
```bash
python init_users.py
```

### **4. Lancer l'Application**
```bash
python main.py
```

## 🔑 **Comptes de Connexion Disponibles**

| Username | Password | Rôle | Permissions |
|----------|----------|------|-------------|
| `admin` | `admin123` | **Super Administrateur** | Toutes les permissions |
| `directeur` | `directeur123` | **Directeur** | Lecture + Écriture |
| `professeur1` | `prof123` | **Professeur** | Notes, Présences, Bulletins |
| `professeur2` | `prof123` | **Professeur** | Notes, Présences, Bulletins |
| `secretaire` | `sec123` | **Secrétaire** | Gestion administrative |
| `eleve1` | `eleve123` | **Élève** | Lecture uniquement |
| `parent1` | `parent123` | **Parent** | Lecture des infos élève |

## 🎯 **Fonctionnalités Implémentées**

### **🔐 Authentification Sécurisée**
- ✅ Hachage SHA-256 des mots de passe
- ✅ Gestion des sessions avec tokens
- ✅ Log des tentatives de connexion
- ✅ Protection contre les attaques

### **👥 Système de Rôles Complet**
- ✅ 7 rôles prédéfinis avec permissions granulaires
- ✅ Gestion dynamique des accès
- ✅ Attribution automatique des rôles

### **🎨 Interface Moderne**
- ✅ Design exceptionnel avec CustomTkinter
- ✅ Sidebar ultra-moderne sans scrollbar
- ✅ Animations fluides et effets visuels
- ✅ Thème sombre professionnel

### **🗄️ Base de Données Robuste**
- ✅ Création automatique des tables
- ✅ Structure optimisée pour la performance
- ✅ Gestion des relations et contraintes

## 🚀 **Utilisation Rapide**

### **Première Connexion**
1. Lancer `python main.py`
2. Se connecter avec `admin` / `admin123`
3. Explorer les fonctionnalités disponibles

### **Gestion des Utilisateurs**
- L'utilisateur `admin` a tous les droits
- Créez de nouveaux comptes selon vos besoins
- Attribuez les rôles appropriés

### **Personnalisation**
- Modifiez les permissions des rôles dans `models/role.py`
- Ajoutez de nouveaux modules selon vos besoins
- Personnalisez l'interface dans `views/`

## 🛠️ **Dépannage**

### **Problème de Dépendances**
```bash
pip install --upgrade customtkinter Pillow matplotlib
```

### **Erreur de Base de Données**
```bash
# Supprimer et recréer la base
rm database/edumanager.db
python test_system.py
```

### **Problème d'Import**
```bash
# Vérifier la structure des dossiers
ls -la models/ views/
```

## 📊 **Structure du Projet**

```
Gestion_scolaire/
├── main.py                 # 🚀 Point d'entrée principal
├── test_system.py         # 🧪 Tests du système
├── init_users.py          # 👥 Création des utilisateurs
├── models/
│   ├── auth.py            # 🔐 Gestionnaire d'authentification
│   └── role.py            # 👑 Gestionnaire des rôles
├── views/
│   ├── login_view.py      # 🎨 Interface de connexion
│   └── dashboard_view.py  # 📊 Dashboard principal
├── database/              # 🗄️ Base de données SQLite
└── assets/                # 🎨 Images et ressources
```

## 🎉 **Félicitations !**

Votre système EduManager+ est maintenant **opérationnel** avec :

- ✅ **Authentification sécurisée** et robuste
- ✅ **Gestion complète des rôles** et permissions
- ✅ **Interface moderne** et professionnelle
- ✅ **Base de données** optimisée et sécurisée
- ✅ **Système de tests** complet et fiable

## 🚀 **Prochaines Étapes**

1. **Testez tous les comptes** de démonstration
2. **Personnalisez** les rôles selon vos besoins
3. **Ajoutez** de nouveaux modules si nécessaire
4. **Formez** vos utilisateurs sur le système
5. **Sauvegardez** régulièrement la base de données

**Bonne utilisation d'EduManager+ ! 🎓✨**
