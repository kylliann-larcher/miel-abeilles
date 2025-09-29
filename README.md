# miel-abeilles

#  Partie Théorique – Le Miel et les Abeilles

##  Contexte et Métaphore
Une colonie de 101 abeilles s’installe dans un pommier au milieu d’un champ de fleurs mellifères.  
Leur objectif : butiner toutes les fleurs le plus efficacement possible pour nourrir la reine Maya et ses larves.  

Mais la reine est exigeante : elle veut que sa colonie s’améliore de génération en génération.  
Seules les abeilles les plus rapides, celles qui trouvent les chemins les plus courts, ont le droit de se reproduire.  
Les plus lentes sont remplacées.  

Ce comportement illustre le **principe de sélection naturelle numérique**, au cœur des **algorithmes génétiques**.  

---

##   Le Problème Caché – Le Voyageur de Commerce (TSP)
Le défi des abeilles correspond à un problème bien connu en informatique : le **problème du voyageur de commerce** (*Traveling Salesperson Problem, TSP*).  

- **Définition** : une abeille part de la ruche, doit visiter chaque fleur **une seule fois**, puis revenir à la ruche.  
- **Nature du problème** : optimisation combinatoire.  
- **Explosion combinatoire** :  
  - Avec 10 fleurs → 181 440 chemins possibles.  
  - Avec 20 fleurs → 1,2 × 10¹⁷ chemins.  
  - Tester toutes les solutions est impossible, même avec les ordinateurs les plus rapides.  

  Plutôt que de chercher **le chemin parfait** (souvent hors de portée), on cherche **un chemin excellent**, obtenu rapidement grâce à des méthodes heuristiques.  

---

## La Solution – Les Algorithmes Génétiques
Les algorithmes génétiques (AG) s’inspirent de la théorie de l’évolution de Darwin.  
L’idée est de simuler une population d’individus qui s’améliorent au fil du temps par **sélection, croisement et mutation**.  

### Dictionnaire Abeille ⇔ Algorithme Génétiques
- **Individu (abeille)** = un chemin possible (chromosome).  
- **Population** = l’ensemble des 100 abeilles de la colonie.  
- **Gène** = une fleur dans le chemin.  
- **Fitness (score de qualité)** = l’efficacité d’une abeille :  

  \[
  \text{Fitness} = \frac{1}{\text{distance totale}}
  \]

- **Sélection** = seules les meilleures abeilles se reproduisent.  
- **Croisement (crossover)** = mélange des chemins de deux parents pour créer un nouvel enfant.  
- **Mutation** = petite variation aléatoire (ex. inversion de deux fleurs).  
- **Génération** = un cycle complet : évaluation → sélection → reproduction → mutation → remplacement.  

---

##  Cycle de Vie d’une Génération
```ascii
Initialisation → Évaluation → Sélection → Croisement/Mutation → Remplacement → Nouvelle Génération
