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

Affiche les informations sur une compétence ou connaissance spécifique (à implémenter).

**Exemple d'utilisation :**
```
Votre choix : 2
Entrez le nom de la compétence ou connaissance : programmation
```

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

Calcule la similarité entre deux métiers (à implémenter).

**Exemple d'utilisation :**
```
Votre choix : 4
Premier métier : développeur web
Deuxième métier : développeur mobile
```

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

Analyse les possibilités de mobilité professionnelle depuis un métier actuel (à implémenter).

**Exemple d'utilisation :**
```
Votre choix : 6
Métier actuel : développeur web
```

---

## Conseils d'utilisation

### Pour la recherche de métiers (Option 1)
- La recherche est **insensible à la casse**
- Utilisez des **mots partiels** : "développ" trouvera "développeur", "développeuse", etc.
- Exemples de recherches :
  - `tisseur` → trouve tous les métiers de tisseur
  - `ingénieur` → trouve tous les types d'ingénieurs
  - `responsable` → trouve tous les postes de responsables

### Pour la similarité de compétences (Option 3)
- Saisir les compétences **exactement** comme elles apparaissent dans la base
- La comparaison est insensible à la casse
- Exemples :
  - ✅ `programmer des machines`
  - ✅ `utiliser Python`
  - ❌ `programme` (trop vague)

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