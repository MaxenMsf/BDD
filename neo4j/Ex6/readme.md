# Système de Gestion des Métiers - Guide d'utilisation

Application de gestion et d'analyse des métiers basée sur Neo4j, permettant d'explorer les compétences, connaissances et relations entre différents métiers.

## Prérequis

- Python 3.x
- Neo4j installé et en cours d'exécution
- Bibliothèques Python :
  ```bash
  pip install py2neo pandas
  ```

## Installation

1. Assurez-vous que Neo4j est en cours d'exécution
2. Importez les données avec le script d'insertion :
   ```bash
   python exo6_insert.py
   ```
3. Lancez l'application :
   ```bash
   python commandes.py
   ```

## Fonctionnalités

### 1. 📋 Fiche métier

Affiche toutes les informations détaillées d'un métier : compétences requises/optionnelles, connaissances requises/optionnelles et appellations alternatives.

**Exemple d'utilisation :**
```
Votre choix : 1
Entrez le nom du métier : tisseur
```

**Résultat :**
```
==============================================================
📋 MÉTIER 1: tisseur/tisseuse
==============================================================
Code: 7318

🔄 Autres appellations:
   • tisseuse
   • tisserande
   • tisseur
   • tisserand

✅ Compétences requises:
   • utiliser des techniques textiles pour des produits confectionnés à la main
   • utiliser les technologies de machines à tisser
   • utiliser une machine à tisser
   ... et 1 autre(s)

⭐ Compétences optionnelles:
   • commander des matières textiles
   • produire des échantillons textiles
   • vérifier la qualité de produits sur une ligne de production textile
   ... et 7 autre(s)

📚 Connaissances requises:
   • techniques textiles
   • industrie textile
   • mesure de textiles
   ... et 2 autre(s)
```

---

### 2. 🔍 Compétence/Connaissance

Affiche les informations détaillées sur une compétence ou connaissance : liste des métiers qui la requièrent, métiers où elle est optionnelle, et statistiques d'utilisation.

**Exemple d'utilisation :**
```
Votre choix : 2
Entrez le nom de la compétence ou connaissance : programmer
```

**Résultat attendu :**
```
======================================================================
🔍 ANALYSE : programmer des machines
======================================================================
Type: Compétence (Skill)

📊 Statistiques d'utilisation:
   • Métiers requérant cette compétence: 23
   • Métiers où elle est optionnelle: 12
   • Total de métiers utilisant cette compétence: 35

✅ Métiers qui requièrent cette compétence (exemples):
   1. Développeur logiciel
   2. Ingénieur en automatisation
   3. Technicien en robotique
   4. Programmeur CNC
   5. Développeur d'applications
   ... et 18 autre(s)

⭐ Métiers où cette compétence est optionnelle (exemples):
   1. Chef de projet IT
   2. Analyste de systèmes
   3. Technicien de maintenance
   ... et 9 autre(s)

🔗 Compétences souvent associées:
   • utiliser des bases de données
   • développer des applications
   • analyser des systèmes
```

**Cas d'usage :**
- Découvrir quels métiers nécessitent une compétence particulière
- Identifier si une compétence est très demandée ou spécialisée
- Trouver des compétences complémentaires à développer

---

### 3. 📊 Similarité entre compétences

Calcule la similarité de Jaccard entre deux compétences basée sur leur co-occurrence dans les métiers.

**Formule :** `J(A,B) = |A ∩ B| / |A ∪ B|`

**Exemple d'utilisation :**
```
Votre choix : 3
Première compétence : programmer
Deuxième compétence : coder
```

**Résultat :**
```
======================================================================
🔍 ANALYSE DE SIMILARITÉ
======================================================================

📊 Compétence 1: programmer des machines
   └─ Nombre de métiers: 45

📊 Compétence 2: coder
   └─ Nombre de métiers: 38

🔗 Métiers en commun (Intersection): 12
🌐 Total métiers distincts (Union): 71

======================================================================
📈 SIMILARITÉ DE JACCARD: 0.1690
   Formule: J(A,B) = |A ∩ B| / |A ∪ B|
   Calcul: 12 / 71 = 0.1690
======================================================================

💡 Interprétation: 🟠 Faiblement similaires - Peu de métiers en commun

📋 Métiers utilisant les deux compétences (12):
   1. Développeur logiciel
   2. Ingénieur informatique
   3. Technicien en automatisation
   ...
```

**Interprétation des scores :**
- 🟢 ≥ 0.7 : Très similaires
- 🟡 ≥ 0.4 : Moyennement similaires
- 🟠 ≥ 0.1 : Faiblement similaires
- 🔴 < 0.1 : Très peu similaires

---

### 4. 🔗 Similarité entre métiers

Calcule la similarité entre deux métiers en se basant sur leurs compétences et connaissances communes. Utilise également la similarité de Jaccard pour mesurer le degré de chevauchement.

**Exemple d'utilisation :**
```
Votre choix : 4
Premier métier : développeur web
Deuxième métier : développeur mobile
```

**Résultat attendu :**
```
======================================================================
🔍 ANALYSE DE SIMILARITÉ ENTRE MÉTIERS
======================================================================

📋 Métier 1: Développeur web / développeuse web
   Code: 2512
   • Compétences requises: 15
   • Compétences optionnelles: 8
   • Connaissances requises: 12

📋 Métier 2: Développeur d'applications mobiles
   Code: 2513
   • Compétences requises: 14
   • Compétences optionnelles: 10
   • Connaissances requises: 11

======================================================================
🎯 COMPÉTENCES
======================================================================

✅ Compétences requises en commun (8):
   • programmer en JavaScript
   • utiliser des bases de données
   • développer des interfaces utilisateur
   • tester des applications
   • déboguer du code
   • utiliser des outils de versioning
   • appliquer des principes de sécurité
   • travailler en équipe agile

📊 Statistiques compétences:
   • Intersection: 8
   • Union: 21
   • Similarité de Jaccard: 0.3810 (38.1%)

======================================================================
📚 CONNAISSANCES
======================================================================

✅ Connaissances requises en commun (7):
   • langages de programmation
   • architecture logicielle
   • bases de données
   • protocoles réseau
   • sécurité informatique
   • méthodologies agiles
   • patterns de conception

📊 Statistiques connaissances:
   • Intersection: 7
   • Union: 16
   • Similarité de Jaccard: 0.4375 (43.8%)

======================================================================
📈 SCORE GLOBAL DE SIMILARITÉ
======================================================================

Score moyen (compétences + connaissances): 0.4092 (40.9%)

💡 Interprétation: 🟡 Moyennement similaires - Parcours de transition envisageable

🎓 Recommandations pour la transition:
   • Compétences à acquérir: 6
      - Développement iOS/Swift
      - Développement Android/Kotlin
      - Design mobile-first
      - Optimisation mobile
      - APIs mobiles natives
      - Tests sur devices

   • Compétences transférables: 8
      Ces compétences facilitent grandement la transition !
```

**Cas d'usage :**
- Évaluer la difficulté d'une reconversion professionnelle
- Identifier les compétences à développer pour changer de métier
- Trouver des métiers similaires pour une évolution de carrière

---

### 5. 🎯 Recommandation métier

Recommande des métiers en fonction des compétences fournies, triés par score de correspondance global.

**Exemple d'utilisation :**
```
Votre choix : 5
Entrez vos compétences (séparées par des virgules) : 
utiliser des techniques textiles pour des produits confectionnés à la main,
utiliser les technologies de machines à tisser,
utiliser une machine à tisser,
découper des textiles
```

**Résultat :**
```
================================================================================
🎯 MÉTIERS RECOMMANDÉS (5 résultat(s))
================================================================================

1. 📋 tisseur/tisseuse
   Code: 7318
   🟢 EXCELLENT - Score global: 100.0%
   ✅ Compétences requises: 4/4 (100.0%)
   ⭐ Compétences optionnelles: 0/10 (0.0%)
   📊 Total: 4/14
   🔹 Compétences requises (exemples): utiliser des techniques textiles, utiliser une machine à tisser, découper des textiles
   ⚪ Compétences optionnelles (exemples): commander des matières textiles, produire des échantillons textiles

2. 📋 opérateur de machines textiles
   Code: 8131
   🟡 TRÈS BON - Score global: 67.5%
   ✅ Compétences requises: 3/5 (60.0%)
   ⭐ Compétences optionnelles: 1/3 (33.3%)
   📊 Total: 4/8
   ...
```

**Badges de correspondance :**
- 🟢 EXCELLENT : ≥ 80%
- 🟡 TRÈS BON : ≥ 60%
- 🟠 BON : ≥ 40%
- 🔵 PARTIEL : < 40%

**Tri des résultats :**
Les métiers sont triés par :
1. Score global décroissant
2. Nombre de compétences requises correspondantes
3. Nombre de compétences optionnelles correspondantes

---

### 6. 🔄 Mobilité professionnelle

Analyse les possibilités de mobilité professionnelle depuis un métier actuel, en identifiant les métiers accessibles avec peu de formation complémentaire.

**Exemple d'utilisation :**
```
Votre choix : 6
Métier actuel : développeur web
```

**Résultat attendu :**
```
======================================================================
🔄 ANALYSE DE MOBILITÉ PROFESSIONNELLE
======================================================================

📋 Métier actuel: Développeur web / développeuse web
   Code: 2512
   • Compétences requises: 15
   • Compétences optionnelles: 8
   • Connaissances requises: 12

======================================================================
🎯 MÉTIERS ACCESSIBLES PAR MOBILITÉ
======================================================================
Métiers triés par facilité de transition (score de similarité décroissant)

1. 🟢 TRANSITION FACILE - Développeur d'applications mobiles
   Code: 2513
   Similarité: 85.2%
   
   ✅ Compétences déjà acquises: 12/14 (85.7%)
   📚 Connaissances déjà acquises: 9/11 (81.8%)
   
   🎓 Formation complémentaire nécessaire:
      Compétences à acquérir (2):
      • Développement iOS/Swift
      • Développement Android/Kotlin
      
      Connaissances à acquérir (2):
      • Frameworks mobiles natifs
      • Guidelines design mobile
   
   ⏱️ Durée estimée de formation: 3-6 mois
   💼 Opportunités d'emploi: Élevées

2. 🟡 TRANSITION MOYENNE - Développeur full-stack
   Code: 2514
   Similarité: 72.5%
   
   ✅ Compétences déjà acquises: 10/16 (62.5%)
   📚 Connaissances déjà acquises: 8/13 (61.5%)
   
   🎓 Formation complémentaire nécessaire:
      Compétences à acquérir (6):
      • DevOps et CI/CD
      • Administration système
      • Containers (Docker, Kubernetes)
      • Cloud computing
      • Monitoring et logging
      • Performance optimization
      
   ⏱️ Durée estimée de formation: 6-12 mois
   💼 Opportunités d'emploi: Très élevées

3. 🟡 TRANSITION MOYENNE - Analyste de systèmes
   Code: 2511
   Similarité: 65.8%
   
   ✅ Compétences déjà acquises: 8/14 (57.1%)
   📚 Connaissances déjà acquises: 7/12 (58.3%)
   
   🎓 Formation complémentaire nécessaire:
      Compétences à acquérir (6):
      • Analyse de besoins
      • Modélisation UML
      • Rédaction de spécifications
      • Analyse de processus métier
      • Gestion de projet
      • Communication stakeholders
   
   ⏱️ Durée estimée de formation: 6-9 mois
   💼 Opportunités d'emploi: Élevées

4. 🟠 TRANSITION ACCESSIBLE - Chef de projet IT
   Code: 1330
   Similarité: 48.3%
   
   ✅ Compétences déjà acquises: 5/15 (33.3%)
   📚 Connaissances déjà acquises: 6/14 (42.9%)
   
   🎓 Formation complémentaire nécessaire:
      Compétences à acquérir (10):
      • Management d'équipe
      • Gestion budgétaire
      • Planification de projet
      • Gestion des risques
      • Communication client
      • Méthodologies agiles (Scrum Master)
      • Reporting et KPIs
      • Négociation
      • Gestion de contrats
      • Leadership
   
   ⏱️ Durée estimée de formation: 12-18 mois
   💼 Opportunités d'emploi: Moyennes

======================================================================
💡 CONSEILS POUR LA MOBILITÉ
======================================================================

📈 Évolutions naturelles (même domaine):
   • Senior Developer → Lead Developer → Architect
   • Spécialisation: Frontend, Backend, DevOps

🔄 Reconversions facilitées:
   1. Développeur mobile (forte similarité technique)
   2. Full-stack developer (élargissement des compétences)
   3. DevOps engineer (orientation infrastructure)

🎯 Secteurs porteurs avec vos compétences:
   • FinTech
   • E-commerce
   • SaaS
   • Agences digitales

🎓 Certifications recommandées:
   • AWS/Azure/GCP (Cloud)
   • React Native / Flutter (Mobile)
   • Scrum Master (Gestion de projet)
```

**Critères d'analyse :**
- 🟢 FACILE : ≥ 80% - Transition rapide (< 6 mois)
- 🟡 MOYENNE : ≥ 60% - Formation modérée (6-12 mois)
- 🟠 ACCESSIBLE : ≥ 40% - Reconversion possible (12-24 mois)
- 🔴 DIFFICILE : < 40% - Reconversion majeure (> 24 mois)

**Cas d'usage :**
- Planifier une évolution de carrière
- Identifier les formations à suivre pour changer de métier
- Évaluer la faisabilité d'une reconversion
- Découvrir des opportunités de mobilité interne

---

## Conseils d'utilisation

### Pour la recherche de métiers (Option 1)
- La recherche est **insensible à la casse**
- Utilisez des **mots partiels** : "développ" trouvera "développeur", "développeuse", etc.
- Exemples de recherches :
  - `tisseur` → trouve tous les métiers de tisseur
  - `ingénieur` → trouve tous les types d'ingénieurs
  - `responsable` → trouve tous les postes de responsables

### Pour les compétences/connaissances (Option 2)
- Recherche partielle acceptée : "programm" trouvera "programmer", "programmation", etc.
- Fonctionne avec les compétences ET les connaissances
- Exemples :
  - `python` → trouve toutes les compétences liées à Python
  - `gestion` → trouve toutes les compétences de gestion
  - `textile` → trouve connaissances et compétences textiles

### Pour la similarité de compétences (Option 3)
- Saisir les compétences comme elles apparaissent dans la base (ou partiellement)
- La comparaison est insensible à la casse
- Exemples :
  - ✅ `programmer des machines` / `coder`
  - ✅ `python` / `java`
  - ✅ `gérer` / `manager`

### Pour la similarité de métiers (Option 4)
- Utiliser le nom du métier (recherche partielle acceptée)
- Compare les compétences ET les connaissances
- Exemples :
  - `développeur web` / `développeur mobile`
  - `ingénieur` / `technicien`
  - `comptable` / `gestionnaire`

### Pour la recommandation de métiers (Option 5)
- **Séparez les compétences par des virgules**
- N'utilisez **PAS** de guillemets
- La recherche est partielle et insensible à la casse
- Plus vous saisissez de compétences, plus les recommandations seront précises

**Exemples :**
```
# ✅ Correct
programmer en Python,utiliser des bases de données,développer des applications web

# ❌ Incorrect (avec guillemets)
"programmer en Python","utiliser des bases de données"

# ✅ Recherche partielle fonctionne
python,base de données,web
```

### Pour la mobilité professionnelle (Option 6)
- Saisir votre métier actuel (recherche partielle)
- Analyse automatique des métiers similaires
- Exemples :
  - `développeur` → trouve tous les métiers de développeur
  - `ingénieur` → métier actuel = ingénieur
  - `responsable commercial`

## Structure de la base de données

```
(Occupation) -[:REQUIRES]-> (Skill)
(Occupation) -[:OPTIONAL_SKILL]-> (Skill)
(Occupation) -[:REQUIRES_KNOWLEDGE]-> (Knowledge)
(Occupation) -[:OPTIONAL_KNOWLEDGE]-> (Knowledge)
```

**Propriétés :**
- **Occupation** : `code`, `occupation`, `alt`, `id`
- **Skill** : `name`
- **Knowledge** : `name`

## Quitter l'application

Choisissez l'option **0** dans le menu principal.

## Support

Pour toute question ou problème :
1. Vérifiez que Neo4j est bien démarré
2. Vérifiez que les données ont été importées avec `exo6_insert.py`
3. Assurez-vous que la connexion à `bolt://localhost:7474` fonctionne

---

**Développé avec Python, Neo4j et py2neo**