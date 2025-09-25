# 🎓 Système de Gestion des Matières du Système Éducatif Guinéen

## 📋 Vue d'ensemble

Ce système organise et gère les matières scolaires selon la structure du système éducatif guinéen dans l'application EduManager+. Il fournit une base de données complète et structurée des matières pour tous les niveaux d'éducation.

## 🏗️ Structure du Système

### 📚 Niveaux d'Éducation

#### 🎒 **Primaire (CP1 → CM2)**
- **Classes** : CP1, CP2, CE1, CE2, CM1, CM2
- **Matières fondamentales** :
  - Français (Coeff: 4.0)
  - Mathématiques (Coeff: 4.0)
  - Sciences d'observation (Coeff: 2.0)
  - Éducation civique et morale (Coeff: 2.0)
  - Éducation artistique (Coeff: 1.5)
  - Éducation physique (Coeff: 1.5)
- **Matières optionnelles** :
  - Anglais (Coeff: 1.0) - selon l'école

#### 🎓 **Collège (7ème → 10ème année)**
- **Classes** : 7ème, 8ème, 9ème, 10ème
- **Matières fondamentales** :
  - Français (Coeff: 4.0)
  - Mathématiques (Coeff: 4.0)
  - Anglais (Coeff: 3.0)
  - Histoire-Géographie (Coeff: 3.0)
  - Physique-Chimie (Coeff: 3.0)
  - Biologie/SVT (Coeff: 2.5)
  - Éducation civique et morale (Coeff: 2.0)
  - Éducation physique (Coeff: 2.0)
  - Technologie/Arts pratiques (Coeff: 2.0)
- **Matières optionnelles** :
  - Espagnol (Coeff: 2.0)
  - Informatique (Coeff: 2.0)

#### 🎯 **Lycée (11ème → 12ème année)**
- **Séries disponibles** :
  - Sciences Mathématiques
  - Sciences Expérimentales
  - Lettres/Sciences Sociales
  - Technique/Professionnelle

##### **Série Sciences Mathématiques**
- **Matières communes** : Français, Anglais, Éducation civique et morale, EPS
- **Matières spécialisées** :
  - Mathématiques (Coeff: 5.0)
  - Physique (Coeff: 4.0)
  - Chimie (Coeff: 3.5)
- **Matières optionnelles** :
  - Informatique (Coeff: 3.0)
  - Biologie (Coeff: 2.5)

##### **Série Sciences Expérimentales**
- **Matières communes** : Français, Anglais, Éducation civique et morale, EPS
- **Matières spécialisées** :
  - Biologie (Coeff: 5.0)
  - Chimie (Coeff: 4.0)
  - Physique (Coeff: 3.5)
  - Mathématiques (Coeff: 3.0)
- **Matières optionnelles** :
  - Géologie (Coeff: 2.5)

##### **Série Lettres/Sciences Sociales**
- **Matières communes** : Français, Anglais, Éducation civique et morale, EPS
- **Matières spécialisées** :
  - Philosophie (Coeff: 4.0)
  - Histoire-Géographie (Coeff: 4.0)
  - Mathématiques (Coeff: 2.5)
- **Matières optionnelles** :
  - Économie (Coeff: 3.0)
  - Espagnol (Coeff: 3.0)
  - Arts plastiques (Coeff: 2.5)

##### **Série Technique/Professionnelle**
- **Matières communes** : Français, Anglais, Éducation civique et morale, EPS
- **Matières spécialisées** :
  - Technologie (Coeff: 5.0)
  - Mathématiques techniques (Coeff: 3.0)
  - Physique appliquée (Coeff: 3.0)
- **Matières optionnelles** :
  - Informatique appliquée (Coeff: 3.5)
  - Gestion (Coeff: 3.0)

## 🛠️ Architecture Technique

### 📁 Structure des Fichiers

```
src/modules/academic/subjects/
├── models/
│   ├── guinean_subjects_structure.py    # Structure des matières
│   └── guinean_subject_model.py         # Modèle de base de données
├── controllers/
│   └── guinean_subjects_controller.py   # Contrôleur principal
└── views/
    └── guinean_subjects_view.py         # Interface utilisateur
```

### 🗄️ Base de Données

**Table principale** : `guinean_subjects`
- `id` : Identifiant unique
- `code` : Code unique de la matière (ex: "FR_CM1", "MATH_11ème_Sciences_Mathématiques")
- `name` : Nom de la matière
- `description` : Description détaillée
- `coefficient` : Coefficient de pondération
- `education_level` : Niveau d'éducation (primaire, college, lycee)
- `grade` : Classe (ex: "CM1", "9ème", "11ème Sciences Mathématiques")
- `series` : Série pour le lycée
- `is_optional` : Matière optionnelle (booléen)
- `is_core` : Matière fondamentale (booléen)
- `is_active` : Matière active (booléen)
- `date_created` : Date de création
- `date_updated` : Date de mise à jour

## 🚀 Installation et Configuration

### 1. Initialisation du Système

```bash
python initialize_guinean_subjects_system.py
```

### 2. Nettoyage (si nécessaire)

```bash
python clean_guinean_subjects_database.py
```

### 3. Migration de la structure

```bash
python migrate_guinean_subjects_table.py
```

### 4. Test et démonstration

```bash
python demo_guinean_subjects_system.py
```

## 📊 Statistiques Actuelles

- **Total des matières** : 161
- **Nombre de classes** : 18
- **Nombre de niveaux** : 3
- **Coefficient moyen** : 2.76

### Répartition par niveau :
- **Primaire** : 43 matières, 6 classes
- **Collège** : 44 matières, 4 classes
- **Lycée** : 74 matières, 8 classes

## 🔧 Utilisation

### Récupération des matières par classe

```python
from src.modules.academic.subjects.controllers.guinean_subjects_controller import get_guinean_subjects_controller

controller = get_guinean_subjects_controller()

# Toutes les matières d'une classe
subjects = controller.get_subjects_by_grade("CM1")

# Matières fondamentales seulement
core_subjects = controller.get_core_subjects_by_grade("CM1")

# Matières optionnelles seulement
optional_subjects = controller.get_optional_subjects_for_grade("CM1")
```

### Recherche de matières

```python
# Recherche par nom
math_subjects = controller.search_subjects("Math")

# Recherche par niveau
primaire_subjects = controller.search_subjects("", level="primaire")

# Recherche par classe
grade_subjects = controller.search_subjects("", grade="9ème")
```

### Ajout de matières personnalisées

```python
custom_subject = {
    "code": "CUSTOM001",
    "name": "Matière Personnalisée",
    "description": "Description de la matière",
    "coefficient": 2.0,
    "education_level": "college",
    "grade": "10ème",
    "is_optional": True,
    "is_core": False
}

controller.add_custom_subject(custom_subject)
```

## 🔗 Intégration avec EduManager+

### Formulaires de saisie de notes
```python
# Récupérer les matières pour un formulaire
core_subjects, optional_subjects = controller.get_subjects_for_form("9ème")
```

### Génération de bulletins
```python
# Récupérer les matières pour un bulletin
bulletin_subjects = controller.get_subjects_for_bulletin("CM1", include_optional=False)
```

### Gestion des emplois du temps
```python
# Récupérer les matières pour un emploi du temps
timetable_subjects = controller.get_subjects_for_timetable("9ème")
```

## 🎨 Interface Utilisateur

La vue `GuineanSubjectsView` fournit une interface moderne avec :
- Navigation par niveaux d'éducation
- Filtrage par classe
- Recherche en temps réel
- Affichage des statistiques
- Gestion des matières personnalisées

## 📈 Fonctionnalités Avancées

### Export de la structure
```python
structure = controller.export_subjects_structure()
```

### Statistiques détaillées
```python
stats = controller.get_statistics()
```

### Hiérarchie des classes
```python
hierarchy = controller.get_grade_hierarchy()
```

## 🔄 Maintenance

### Réinitialisation complète
```python
controller.reset_to_default_structure()
```

### Import de matières personnalisées
```python
subjects_data = [...]  # Liste de dictionnaires
success_count, error_count = controller.import_custom_subjects(subjects_data)
```

## 📝 Notes Importantes

1. **Codes uniques** : Chaque matière a un code unique incluant la classe (ex: "FR_CM1")
2. **Coefficients** : Les coefficients reflètent l'importance relative des matières
3. **Flexibilité** : Le système permet l'ajout de matières personnalisées
4. **Évolutivité** : La structure peut être étendue pour de nouveaux niveaux ou séries

## 🎯 Prochaines Étapes

1. **Intégration dans l'interface principale** d'EduManager+
2. **Connexion aux formulaires** de saisie de notes
3. **Intégration dans la génération** de bulletins
4. **Ajout aux emplois du temps**
5. **Personnalisation** des séries du lycée

---

*Système développé pour EduManager+ - Gestion Scolaire Moderne* 🚀
