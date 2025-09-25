# 💰 SYSTÈME DE PAIEMENT PAR HEURE DE COURS - GUIDE COMPLET

## 🎯 **Principe de Fonctionnement**

Les professeurs sont payés **par heure de cours dispensée** avec un système de calcul automatique basé sur :
- **Taux horaire** : Prix par heure de cours (ex: 50,000 GNF/heure)
- **Heures par session** : Durée d'un cours (généralement 2h)
- **Sessions par semaine** : Nombre de cours par semaine (ex: 10 sessions)

## 🧮 **Calculs Automatiques**

### **Exemple Concret :**
- **Taux horaire** : 50,000 GNF/heure
- **Heures par session** : 2h
- **Sessions par semaine** : 10

### **Calculs :**
```
Heures par semaine = 10 sessions × 2h = 20h
Heures par mois = 20h × 4.33 = 86.6h
Heures par année (9 mois) = 86.6h × 9 = 779.4h

Salaires :
- Semaine = 20h × 50,000 = 1,000,000 GNF
- Mois = 86.6h × 50,000 = 4,330,000 GNF
- Année = 779.4h × 50,000 = 38,970,000 GNF
```

## 📋 **Formulaire de Configuration**

### **Champs de Saisie :**
1. **Taux horaire (GNF/heure de cours)** : Prix par heure
2. **Heures par session de cours** : Durée d'un cours (défaut: 2h)
3. **Sessions par semaine** : Nombre de cours par semaine

### **Calculs Automatiques :**
- Les salaires sont calculés automatiquement
- Affichage en temps réel des montants
- Validation des champs obligatoires

## 📊 **Affichage dans la Vue**

### **Section "Salaires Calculés" :**
- **Taux/H** : 50,000 GNF (vert)
- **Semaine** : 1,000,000 GNF (bleu)
- **Mois** : 4,330,000 GNF (bleu)
- **Année (9m)** : 38,970,000 GNF (vert)

## 🔄 **Flux de Données**

### **1. Saisie dans le Formulaire :**
```
Utilisateur saisit :
- Taux horaire: 50000
- Heures/session: 2
- Sessions/semaine: 10
```

### **2. Calculs Automatiques :**
```python
heures_semaine = 10 × 2 = 20h
heures_mois = 20 × 4.33 = 86.6h
heures_annee = 86.6 × 9 = 779.4h

salaire_semaine = 20 × 50000 = 1,000,000 GNF
salaire_mois = 86.6 × 50000 = 4,330,000 GNF
salaire_annee = 779.4 × 50000 = 38,970,000 GNF
```

### **3. Sauvegarde en Base :**
```sql
INSERT INTO professeurs (
    taux_horaire, heures_par_session, sessions_semaine,
    salaire_base, salaire_net, salaire_horaire
) VALUES (
    50000, 2, 10,
    4330000, 4330000, 50000
)
```

### **4. Affichage dans la Vue :**
- Récupération des données de configuration
- Calculs automatiques des salaires
- Affichage dans la grille 2x2

## 🎨 **Interface Utilisateur**

### **Formulaire ProfesseurDialog :**
```
┌─────────────────────────────────────────────────┐
│           CONFIGURATION SALARIALE              │
├─────────────────────────────────────────────────┤
│ Taux horaire (GNF/heure de cours): [50000]    │
│ Heures par session de cours: [2]               │
│ Sessions par semaine: [10]                     │
│                                                 │
│ ┌─────────────────────────────────────────────┐ │
│ │ Calculs automatiques:                       │ │
│ │ Les salaires seront calculés automatiquement│ │
│ │ selon les heures de cours dispensées        │ │
│ └─────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────┘
```

### **Vue des Détails :**
```
┌─────────────────────────────────────────────────┐
│           SALAIRES CALCULÉS                     │
├─────────────────────────────────────────────────┤
│ ┌─────────────┐  ┌─────────────────────────────┐ │
│ │ Taux/H      │  │ Semaine                     │ │
│ │ 50,000 GNF  │  │ 1,000,000 GNF               │ │
│ └─────────────┘  └─────────────────────────────┘ │
│ ┌─────────────┐  ┌─────────────────────────────┐ │
│ │ Mois         │  │ Année (9m)                  │ │
│ │ 4,330,000 GNF│  │ 38,970,000 GNF              │ │
│ └─────────────┘  └─────────────────────────────┘ │
└─────────────────────────────────────────────────┘
```

## 🔧 **Avantages du Système**

### **1. Simplicité :**
- Un seul taux horaire à configurer
- Calculs automatiques
- Pas de saisie manuelle des salaires

### **2. Flexibilité :**
- Adaptation à différentes écoles
- Modification facile des paramètres
- Calculs en temps réel

### **3. Transparence :**
- Affichage clair des calculs
- Visibilité des montants par période
- Compréhension facile du système

### **4. Cohérence :**
- Calculs uniformes
- Pas d'erreurs de saisie
- Mise à jour automatique

## 📈 **Exemples de Configuration**

### **École Primaire :**
- Taux horaire : 25,000 GNF
- Heures/session : 1h
- Sessions/semaine : 20
- **Résultat** : 500,000 GNF/semaine

### **Collège :**
- Taux horaire : 40,000 GNF
- Heures/session : 2h
- Sessions/semaine : 15
- **Résultat** : 1,200,000 GNF/semaine

### **Lycée :**
- Taux horaire : 60,000 GNF
- Heures/session : 2h
- Sessions/semaine : 12
- **Résultat** : 1,440,000 GNF/semaine

## 🚀 **Utilisation**

1. **Ajouter un professeur** : Saisir les informations + configuration salariale
2. **Modifier un professeur** : Ajuster le taux horaire ou les sessions
3. **Consulter les salaires** : Voir les calculs automatiques dans la vue
4. **Exporter les données** : Utiliser les montants calculés pour la paie

Le système est maintenant **complètement fonctionnel** et adapté au paiement par heure de cours ! 🎯✨
