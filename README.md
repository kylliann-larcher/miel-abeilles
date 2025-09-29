# Partie Théorique du Projet Le Miel et les Abeilles

## 1. Contexte & Métaphore

Une colonie d’abeilles explore un champ de fleurs.  
Chaque abeille représente une solution possible (un chemin pour butiner toutes les fleurs).  
La reine, soucieuse d’efficacité, applique une sélection naturelle numérique :

- Les meilleures abeilles (celles qui trouvent le chemin le plus court ou le plus rapide) transmettent leur savoir.
- Les moins performantes disparaissent.
- Au fil des générations, la colonie apprend à optimiser ses trajets.

C’est exactement le principe d’un Algorithme Génétique (AG).

---

## 2. Qu’est-ce qu’un Algorithme Génétique ?

Un algorithme génétique est une méthode d’optimisation inspirée de la biologie évolutive.  
Il imite le processus de sélection naturelle (Darwin) :

- **Population initiale** : plusieurs solutions candidates (chemins d’abeilles).
- **Évaluation (fitness)** : mesure de la performance de chaque individu (distance ou temps parcouru).
- **Sélection** : les meilleurs sont choisis comme parents.
- **Reproduction (crossover)** : croisement des chemins pour créer de nouveaux individus.
- **Mutation** : petites variations aléatoires pour maintenir la diversité.
- **Nouvelle génération** : le cycle est répété jusqu’à convergence.

Résultat : la population s’améliore génération après génération.

---

## 3. Les Paramètres Clés à Étudier

Il faut tester et comparer différents réglages :

- Taille de la population (ex. 50, 100, 200 abeilles)
- Taux de reproduction (ex. 40%, 60%, 80%)
- Méthode de sélection (roulette, tournoi)
- Taux de mutation (fixe ou adaptatif)
- Nombre de générations (ex. 100, 200, 500)
- Fonction de fitness (distance totale, temps moyen, énergie dépensée)

L’objectif est de justifier pourquoi tel paramétrage est le plus efficace.

---

## 4. Visualisations Attendues

Le sujet impose trois représentations :

- **Chemin optimal** : un graphe avec les fleurs reliées dans l’ordre du parcours de la meilleure abeille.
- **Évolution des performances** : une courbe montrant la fitness moyenne ou minimale par génération.
- **Arbre généalogique** : représentation des ancêtres de la meilleure abeille finale.

Ces visualisations rendent l’algorithme génétique compréhensible pour un non-spécialiste.

---

## 5. Compétences visées

- Algorithmique : comprendre et coder un algorithme génétique.
- Traitement de données : structurer et exploiter des données (coordonnées des fleurs).
- Analyse : comparer des résultats selon plusieurs paramètres.
- Visualisation : présenter des résultats clairs et accessibles.
- Communication : vulgariser la sélection naturelle numérique.

---

## 6. Livrables obligatoires

Repository GitHub public `miel-abeilles` avec :

- `beehive.py` : classes et logique (programmation orientée objet).
- `main.py` : simulation de l’évolution.
- `README.md` : problématique, explications, résultats, conclusion.
- Présentation (slides) : explication, résultats et veille (autres heuristiques comme ACO, PSO, recuit simulé).