# miel-abeilles

## 📖 Partie Théorique du Projet Le Miel et les Abeilles

### 1. Contexte & Métaphore

Une colonie d’abeilles explore un champ de fleurs.  
Chaque abeille représente une solution possible (un chemin pour butiner toutes les fleurs).  
La reine, soucieuse d’efficacité, applique une sélection naturelle numérique :

- Les meilleures abeilles (celles qui trouvent le chemin le plus court/rapide) transmettent leur savoir.
- Les moins performantes disparaissent.
- Au fil des générations, la colonie apprend à optimiser ses trajets.

👉 **C’est exactement le principe d’un Algorithme Génétique (AG).**

---

### 2. 🧬 Qu’est-ce qu’un Algorithme Génétique ?

Un algorithme génétique est une méthode d’optimisation inspirée de la biologie évolutive.  
Il imite le processus de sélection naturelle (Darwin) :

- **Population initiale** : plusieurs solutions candidates (chemins d’abeilles).
- **Évaluation (fitness)** : on mesure la performance de chaque individu (distance/temps parcouru).
- **Sélection** : les meilleurs sont choisis comme parents.
- **Reproduction (crossover)** : croisement des chemins pour créer de nouveaux individus.
- **Mutation** : petites variations aléatoires pour maintenir de la diversité.
- **Nouvelle génération** : on répète le cycle jusqu’à convergence.

👉 **Résultat : la population s’améliore génération après génération.**

---

### 3. ⚙️ Les Paramètres Clés à Étudier

Tu dois tester et comparer différents réglages :

- **Taille de la population** (ex. 50, 100, 200 abeilles).
- **Taux de reproduction** (ex. 40%, 60%, 80%).
- **Méthode de sélection** (roulette, tournoi).
- **Taux de mutation** (fixe ou adaptatif).
- **Nombre de générations** (ex. 100, 200, 500).
- **Fonction de fitness** (distance totale, temps moyen, énergie dépensée).

👉 **L’objectif est de justifier pourquoi tel paramétrage est le plus efficace.**

---

### 4. 📊 Visualisations Attendues

Le sujet impose 3 représentations :

- **Chemin optimal** : un graphe avec les fleurs reliées dans l’ordre du parcours de la meilleure abeille.
- **Évolution des performances** : une courbe montrant la fitness moyenne/minimale par génération.
- **Arbre généalogique** : montrer les ancêtres de la meilleure abeille finale.

👉 **Ces visualisations rendent l’AG compréhensible pour un non-spécialiste.**

---

### 5. 🔍 Compétences visées

- **Algorithmique** : comprendre et coder un AG.
- **Traitement de données** : structurer et exploiter des données (coordonnées des fleurs).
- **Analyse** : comparer des résultats selon plusieurs paramètres.
- **Visualisation** : présenter des résultats clairs et accessibles.
- **Communication** : vulgariser la sélection naturelle numérique.

---

### 6. 📂 Livrables obligatoires

Repository GitHub public `miel-abeilles` avec :

- `beehive.py` → classes & logique (POO).
- `main.py` → simulation de l’évolution.
- `README.md` → problématique, explications, résultats, conclusion.
- Présentation (slides) → explication + résultats + veille (autres heuristiques comme ACO, PSO, recuit simulé).

---

Un fichier `Readme.md` expliquant la problématique, les solutions apportées et une conclusion de votre travail.

---

### connaissances

- Darwin and Natural Selection: Crash Course History of Science #22.
- Bibliotech : Les quatre forces évolutives.
- Algorithme Génétique : Wiki algorithmes génétiques.
- Université de Gustave Eiffel : Fonctionnement Algorithme génétique.
