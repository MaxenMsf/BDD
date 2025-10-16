# Système de Gestion des Métiers - Guide d'utilisation
# MIONE Alexandre, PIERREUSE Nathan

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
   • découper des textiles

⭐ Compétences optionnelles:
   • commander des matières textiles
   • produire des échantillons textiles
   • vérifier la qualité de produits sur une ligne de production textile
   ... et 7 autre(s)

📚 Connaissances requises:
   • techniques textiles
   • industrie textile
   • mesure de textiles
   • technologies textiles
   • matières textiles
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
🔍 ANALYSE : programmer des approvisionnements en écloserie
======================================================================
Type: Compétence (Skill)

📊 Statistiques d'utilisation:
   • Métiers requérant cette compétence: 1
   • Métiers où elle est optionnelle: 0
   • Total de métiers utilisant cette compétence: 1

✅ Métiers qui requièrent cette compétence:
   1. responsable d'écloserie

🔗 Compétences souvent associées:
   • traiter les maladies des poissons
   • provoquer la reproduction d'espèces aquacoles en élevage
   • gérer la production de stock de ressources aquatiques
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
Première compétence : gérer le personnel
Deuxième compétence : recruter des employés
```

**Résultat :**
```
======================================================================
🔍 ANALYSE DE SIMILARITÉ
======================================================================

📊 Compétence 1: gérer le personnel
   └─ Nombre de métiers: 45

📊 Compétence 2: recruter des employés
   └─ Nombre de métiers: 38

🔗 Métiers en commun (Intersection): 25
🌐 Total métiers distincts (Union): 58

======================================================================
📈 SIMILARITÉ DE JACCARD: 0.4310
   Formule: J(A,B) = |A ∩ B| / |A ∪ B|
   Calcul: 25 / 58 = 0.4310
======================================================================

💡 Interprétation: 🟡 Moyennement similaires - Il y a une corrélation notable

📋 Métiers utilisant les deux compétences (25):
   1. directeur comptable/directrice comptable
   2. responsable import-export de viandes et de produits à base de viande
   3. chef cuisinier/cheffe cuisinière
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
Premier métier : tisseur
Deuxième métier : opérateur de machines textiles
```

**Résultat attendu :**
```
======================================================================
🔍 ANALYSE DE SIMILARITÉ ENTRE MÉTIERS
======================================================================

📋 Métier 1: tisseur/tisseuse
   Code: 7318
   • Compétences requises: 4
   • Compétences optionnelles: 10
   • Connaissances requises: 5

📋 Métier 2: conducteur de machines de produits non tissés
   Code: 8131
   • Compétences requises: 2
   • Compétences optionnelles: 2
   • Connaissances requises: 2

======================================================================
🎯 COMPÉTENCES
======================================================================

✅ Compétences requises en commun (1):
   • contrôler des procédés de production de textiles

📊 Statistiques compétences:
   • Intersection: 1
   • Union: 15
   • Similarité de Jaccard: 0.0667 (6.7%)

======================================================================
📚 CONNAISSANCES
======================================================================

✅ Connaissances requises en commun (2):
   • industrie textile
   • matières textiles

📊 Statistiques connaissances:
   • Intersection: 2
   • Union: 5
   • Similarité de Jaccard: 0.4000 (40.0%)

======================================================================
📈 SCORE GLOBAL DE SIMILARITÉ
======================================================================

Score moyen (compétences + connaissances): 0.2334 (23.3%)

💡 Interprétation: 🔵 Faiblement similaires - Métiers distincts

🎓 Recommandations pour la transition:
   • Compétences à acquérir: 1 (requises)
      - fabriquer des revêtements de sol en textile
   
   • Compétences optionnelles à développer: 2
      - fabriquer des fibres synthétiques
      - produire des échantillons textiles

   • Compétences transférables: 1
      Ces compétences facilitent la transition !
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

2. 📋 opérateur de sciage bois/opératrice de sciage bois
   Code: 8172
   🔵 PARTIEL - Score global: 7.1%
   ✅ Compétences requises: 1/14 (7.1%)
   ⭐ Compétences optionnelles: 0/16 (0.0%)
   📊 Total: 1/30
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
Métier actuel : chef cuisinier
```

**Résultat attendu :**
```
======================================================================
🔄 ANALYSE DE MOBILITÉ PROFESSIONNELLE
======================================================================

📋 Métier actuel: chef cuisinier/cheffe cuisinière
   Code: 3434
   • Compétences requises: 27
   • Compétences optionnelles: 14
   • Connaissances requises: 2

======================================================================
🎯 MÉTIERS ACCESSIBLES PAR MOBILITÉ
======================================================================
Métiers triés par facilité de transition (score de similarité décroissant)

1. 🟢 TRANSITION FACILE - directeur d'établissement thermal/directrice d'établissement thermal
   Code: 1431
   Similarité: 82.4%
   
   ✅ Compétences déjà acquises: 15/34 (44.1%)
   📚 Connaissances déjà acquises: 2/4 (50.0%)
   
   🎓 Formation complémentaire nécessaire:
      Compétences à acquérir (19):
      • garantir la satisfaction des clients
      • répondre aux demandes des clients
      • garantir l'accessibilité des infrastructures
      ... et 16 autre(s)
      
      Connaissances à acquérir (2):
      • activités récréatives
      • types de spa
   
   ⏱️ Durée estimée de formation: 6-12 mois
   💼 Opportunités d'emploi: Moyennes

2. 🟡 TRANSITION MOYENNE - responsable qualité chaussure et de viandes et de produits à base de viande
   Code: 1324
   Similarité: 65.2%
   
   ✅ Compétences déjà acquises: 8/18 (44.4%)
   📚 Connaissances déjà acquises: 1/4 (25.0%)
   
   🎓 Formation complémentaire nécessaire:
      Compétences à acquérir (10):
      • communiquer avec les expéditeurs
      • avoir des connaissances en informatique
      • gérer le risque financier
      ... et 7 autre(s)
   
   ⏱️ Durée estimée de formation: 12-18 mois
   💼 Opportunités d'emploi: Moyennes

======================================================================
💡 CONSEILS POUR LA MOBILITÉ
======================================================================

📈 Évolutions naturelles (même domaine):
   • Chef de cuisine → Chef exécutif → Directeur de restauration
   • Spécialisation: Pâtisserie, Gastronomie moléculaire

🔄 Reconversions facilitées:
   1. Directeur d'établissement thermal (gestion d'équipes)
   2. Responsable qualité alimentaire (normes HACCP)
   3. Formateur en cuisine (transmission de compétences)

🎯 Secteurs porteurs avec vos compétences:
   • Hôtellerie de luxe
   • Restauration collective
   • Traiteur événementiel
   • Formation culinaire

🎓 Certifications recommandées:
   • Management hôtelier
   • Hygiène alimentaire (HACCP avancé)
   • Gestion de restaurant
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
- Utilisez des **mots partiels** : "cuisi" trouvera "chef cuisinier", "cuisinier", etc.
- Exemples de recherches :
  - `tisseur` → trouve tisseur/tisseuse
  - `ingénieur` → trouve tous les types d'ingénieurs
  - `responsable` → trouve tous les postes de responsables

### Pour les compétences/connaissances (Option 2)
- Recherche partielle acceptée : "programm" trouvera "programmer", "programmation", etc.
- Fonctionne avec les compétences ET les connaissances
- Exemples :
  - `gérer` → trouve "gérer le personnel", "gérer des budgets", etc.
  - `textile` → trouve connaissances et compétences textiles
  - `programmer` → trouve "programmer des approvisionnements", etc.

### Pour la similarité de compétences (Option 3)
- Saisir les compétences comme elles apparaissent dans la base (ou partiellement)
- La comparaison est insensible à la casse
- Exemples :
  - ✅ `gérer le personnel` / `recruter des employés`
  - ✅ `programmer` / `gérer`
  - ✅ `utiliser` / `appliquer`

### Pour la similarité de métiers (Option 4)
- Utiliser le nom du métier (recherche partielle acceptée)
- Compare les compétences ET les connaissances
- Exemples :
  - `tisseur` / `opérateur textile`
  - `ingénieur` / `technicien`
  - `chef cuisinier` / `directeur thermal`

### Pour la recommandation de métiers (Option 5)
- **Séparez les compétences par des virgules**
- N'utilisez **PAS** de guillemets
- La recherche est partielle et insensible à la casse
- Plus vous saisissez de compétences, plus les recommandations seront précises

**Exemples :**
```
# ✅ Correct
gérer le personnel,recruter des employés,former le personnel

# ❌ Incorrect (avec guillemets)
"gérer le personnel","recruter des employés"

# ✅ Recherche partielle fonctionne
gérer,recruter,former
```

### Pour la mobilité professionnelle (Option 6)
- Saisir votre métier actuel (recherche partielle)
- Analyse automatique des métiers similaires
- Exemples :
  - `cuisinier` → trouve chef cuisinier
  - `ingénieur` → métier actuel = ingénieur
  - `responsable` → trouve responsable d'écloserie, etc.

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