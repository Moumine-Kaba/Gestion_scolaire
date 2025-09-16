# 🔧 Guide de Résolution des Problèmes - EduManager+

## 🚨 **Problèmes Courants et Solutions**

### **1. Erreur "database is locked"**
**Symptôme :** Messages d'erreur "database is locked" dans la console
**Cause :** Conflit d'accès à la base de données
**Solution :**
```bash
# Fermer toutes les instances de l'application
# Puis relancer
python main.py
```

### **2. Erreur "no such table: [nom_table]"**
**Symptôme :** Erreur lors de l'accès à une section
**Cause :** Table manquante dans la base de données
**Solution :**
```bash
# Initialiser les tables manquantes
python init_tables.py

# Ajouter des données de test
python init_test_data.py
```

### **3. Erreur de signature de constructeur**
**Symptôme :** `TypeError: [Classe].__init__() takes X positional arguments but Y were given`
**Cause :** Incompatibilité entre les vues et le système de permissions
**Solution :**
```bash
# Vérifier que toutes les tables sont créées
python init_tables.py

# Vérifier le système de permissions
python test_permissions.py
```

### **4. Problème de chemin de base de données**
**Symptôme :** Erreur "Fichier DB utilisé : [chemin_incorrect]"
**Cause :** Chemin absolu incorrect dans le code
**Solution :**
- Vérifier que le fichier `views/dashboard_view.py` utilise le chemin relatif `"database/edumanager.db"`
- S'assurer que le dossier `database/` existe à la racine du projet

### **5. Erreur d'import de modules**
**Symptôme :** `ImportError: No module named [nom_module]`
**Cause :** Module manquant ou problème de chemin
**Solution :**
```bash
# Installer les dépendances
pip install customtkinter Pillow matplotlib

# Vérifier la structure des dossiers
ls -la models/ views/
```

## 🛠️ **Scripts de Diagnostic et Réparation**

### **Script de Vérification Complète**
```bash
# Vérifier l'état du système
python test_system.py

# Vérifier les permissions
python test_permissions.py

# Vérifier la structure de la base
python -c "import sqlite3; conn = sqlite3.connect('database/edumanager.db'); cursor = conn.cursor(); cursor.execute('SELECT name FROM sqlite_master WHERE type=\"table\"'); print('Tables:', [row[0] for row in cursor.fetchall()]); conn.close()"
```

### **Script de Réparation Automatique**
```bash
# 1. Initialiser les tables
python init_tables.py

# 2. Ajouter des données de test
python init_test_data.py

# 3. Assigner les rôles
python assign_roles.py

# 4. Tester le système
python test_permissions.py
```

## 📊 **Structure de Base de Données Attendue**

### **Tables Principales**
- ✅ `utilisateurs` - Comptes utilisateurs
- ✅ `roles` - Définition des rôles
- ✅ `user_roles` - Attribution des rôles
- ✅ `role_view_permissions` - Permissions par vue
- ✅ `bulletins` - Bulletins scolaires
- ✅ `notes` - Notes des élèves
- ✅ `presences` - Présences et absences
- ✅ `eleves` - Dossiers des élèves
- ✅ `professeurs` - Dossiers des professeurs
- ✅ `classes` - Classes et niveaux
- ✅ `matieres` - Matières enseignées
- ✅ `parents` - Informations des parents
- ✅ `salles` - Salles de classe
- ✅ `enseignements` - Attribution prof-matière-classe
- ✅ `emplois_temps` - Planning des cours
- ✅ `paiements` - Gestion financière

### **Tables de Système**
- ✅ `sessions` - Gestion des sessions
- ✅ `login_attempts` - Log des tentatives de connexion

## 🔍 **Diagnostic Pas à Pas**

### **Étape 1 : Vérifier l'Environnement**
```bash
# Vérifier Python
python --version

# Vérifier les packages
pip list | grep -E "(customtkinter|Pillow|matplotlib)"

# Vérifier la structure
ls -la
ls -la models/ views/ database/
```

### **Étape 2 : Vérifier la Base de Données**
```bash
# Vérifier l'existence
ls -la database/edumanager.db

# Vérifier l'intégrité
python -c "import sqlite3; conn = sqlite3.connect('database/edumanager.db'); print('✅ Base de données accessible'); conn.close()"
```

### **Étape 3 : Vérifier les Permissions**
```bash
# Tester le système de permissions
python test_permissions.py

# Vérifier les rôles assignés
python -c "import sqlite3; conn = sqlite3.connect('database/edumanager.db'); cursor = conn.cursor(); cursor.execute('SELECT u.username, r.nom FROM user_roles ur JOIN utilisateurs u ON ur.user_id = u.id_utilisateur JOIN roles r ON ur.role_id = r.id_role'); print('Rôles assignés:'); [print(f'  {row[0]} -> {row[1]}') for row in cursor.fetchall()]; conn.close()"
```

### **Étape 4 : Vérifier les Vues**
```bash
# Tester le gestionnaire de vues
python -c "from src.modules.view_manager import ViewManager; print('✅ ViewManager accessible')"
```

## 🚀 **Solutions Rapides par Problème**

### **Problème : L'application ne démarre pas**
```bash
# Solution rapide
python init_tables.py
python init_test_data.py
python assign_roles.py
python main.py
```

### **Problème : Erreur lors de la navigation**
```bash
# Vérifier les permissions
python test_permissions.py

# Si erreur, réinitialiser
python init_tables.py
python assign_roles.py
```

### **Problème : Tables manquantes**
```bash
# Créer toutes les tables
python init_tables.py

# Ajouter des données
python init_test_data.py
```

### **Problème : Utilisateurs sans permissions**
```bash
# Réassigner les rôles
python assign_roles.py

# Vérifier
python test_permissions.py
```

## 📞 **Support et Dépannage**

### **Logs à Vérifier**
- Console de l'application
- Messages d'erreur Python
- Fichiers de base de données

### **Informations à Fournir**
- Message d'erreur exact
- Version de Python
- Système d'exploitation
- Actions effectuées avant l'erreur

### **Commandes de Diagnostic**
```bash
# Diagnostic complet
python test_system.py && python test_permissions.py

# Vérification de la base
python -c "import sqlite3; conn = sqlite3.connect('database/edumanager.db'); cursor = conn.cursor(); cursor.execute('PRAGMA integrity_check'); print('Intégrité:', cursor.fetchone()[0]); conn.close()"
```

## 🎯 **Prévention des Problèmes**

### **Bonnes Pratiques**
1. **Toujours fermer** l'application avant de la relancer
2. **Vérifier** que le dossier `database/` existe
3. **Exécuter** les scripts d'initialisation après clonage
4. **Tester** le système après modifications

### **Maintenance Régulière**
```bash
# Vérification mensuelle
python test_system.py
python test_permissions.py

# Sauvegarde de la base
cp database/edumanager.db database/edumanager_backup_$(date +%Y%m%d).db
```

---

**💡 Conseil :** En cas de problème persistant, exécutez toujours la séquence complète de réparation :
```bash
python init_tables.py && python init_test_data.py && python assign_roles.py && python test_permissions.py
```
