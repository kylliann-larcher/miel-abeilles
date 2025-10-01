from dataclasses import dataclass, field
import csv
import random
from math import hypot
from typing import Dict, List, Tuple, Optional
from config import RUCHE_POS, POP_SIZE, ELITE_N, P_MUT, TOURNOI_K


# ---------- Entités ----------

@dataclass(frozen=True)
class Fleur:
    id: int
    x: float
    y: float

    def position(self) -> tuple[float, float]:
        return (self.x, self.y)


@dataclass(frozen=True)
class Ruche:
    """Ruche immuable avec position par défaut (500, 500)."""
    x: float = RUCHE_POS[0]
    y: float = RUCHE_POS[1]

    def position(self) -> tuple[float, float]:
        return (self.x, self.y)


@dataclass
class Abeille:
    """Une abeille = un chemin (permutation des IDs de fleurs)."""
    chemin: List[int]
    fitness: Optional[float] = field(default=None)
    parents: Optional[Tuple[int, int]] = field(default=None)  # pour généalogie future

    def compute_fitness(self, fleurs_idx: Dict[int, Fleur], ruche: Ruche) -> float:
        """Calcule et stocke la distance totale du chemin."""
        dist = 0.0
        cur = ruche.position()

        # ruche -> première fleur
        first = fleurs_idx[self.chemin[0]].position()
        dist += distance_xy(cur, first)
        cur = first

        # fleurs successives
        for fid in self.chemin[1:]:
            nxt = fleurs_idx[fid].position()
            dist += distance_xy(cur, nxt)
            cur = nxt

        # retour à la ruche
        dist += distance_xy(cur, ruche.position())

        self.fitness = dist
        return dist

    def evaluer_fitness(self, fleurs_idx: Dict[int, Fleur], ruche: Ruche) -> float:
        """Alias en français pour compute_fitness (DoD)."""
        return self.compute_fitness(fleurs_idx, ruche)


# ---------- Utilitaires ----------

def distance_xy(a: Tuple[float, float], b: Tuple[float, float]) -> float:
    """Distance euclidienne entre deux points (x, y)."""
    return hypot(a[0] - b[0], a[1] - b[1])


def make_fleurs_index(fleurs: List[Fleur]) -> Dict[int, Fleur]:
    """Crée un index {id -> Fleur} pour lookup rapide."""
    return {f.id: f for f in fleurs}


# ---------- Fleurs: génération / IO CSV ----------

def generate_fleurs(n: int, max_coord: int) -> List[Fleur]:
    """Génère n fleurs aléatoires dans [0, max_coord]."""
    return [Fleur(i, random.randint(0, max_coord), random.randint(0, max_coord))
            for i in range(1, n + 1)]


def save_fleurs(filepath, fleurs: List[Fleur]) -> None:
    with open(filepath, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["id", "x", "y"])
        for fl in fleurs:
            writer.writerow([fl.id, fl.x, fl.y])


def load_fleurs(filepath) -> List[Fleur]:
    fleurs = []
    with open(filepath, "r", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            fleurs.append(Fleur(int(row["id"]), float(row["x"]), float(row["y"])))
    return fleurs


# ---------- Initialisation population ----------

def init_population(fleurs: List[Fleur], pop_size: int = POP_SIZE,
                    seed: Optional[int] = None) -> List[Abeille]:
    """Crée une population d'abeilles avec chemins aléatoires, fitness évaluée."""
    if seed is not None:
        random.seed(seed)

    fleurs_ids = [f.id for f in fleurs]
    fleurs_idx = make_fleurs_index(fleurs)
    ruche = Ruche()

    population: List[Abeille] = []
    for _ in range(pop_size):
        chemin = fleurs_ids[:]
        random.shuffle(chemin)
        ab = Abeille(chemin=chemin)
        ab.compute_fitness(fleurs_idx, ruche)
        population.append(ab)

    return population


# ---------- Algorithme Génétique ----------

def selection_tournoi(population: List[Abeille], k=3, n_parents=2) -> List[Abeille]:
    """Sélection par tournoi : on choisit le meilleur parmi k aléatoires."""
    parents = []
    for _ in range(n_parents):
        cand = random.sample(population, k)
        parents.append(min(cand, key=lambda a: a.fitness))
    return parents


def crossover_ox(p1_chemin: List[int], p2_chemin: List[int]) -> List[int]:
    """Crossover OX (Order Crossover) pour permutations."""
    n = len(p1_chemin)
    a, b = sorted(random.sample(range(n), 2))
    enfant = [None] * n
    # copie segment parent1
    enfant[a:b+1] = p1_chemin[a:b+1]
    # complète avec ordre parent2
    p2_seq = [x for x in p2_chemin if x not in enfant]
    j = 0
    for i in range(n):
        if enfant[i] is None:
            enfant[i] = p2_seq[j]
            j += 1
    return enfant


def mutation_swap(chemin: List[int], p_mut=0.05) -> None:
    """Mutation : échange deux positions aléatoires."""
    if random.random() < p_mut:
        i, j = random.sample(range(len(chemin)), 2)
        chemin[i], chemin[j] = chemin[j], chemin[i]


def boost_population(population: List[Abeille], fleurs: List[Fleur],
                     boost_rate=0.1, immigrants=0, seed=None) -> List[Abeille]:
    """
    Booster une population :
      - dupliquer le top X%
      - ajouter des immigrants aléatoires
    """
    if seed is not None:
        random.seed(seed)
    if not population:
        return population

    n = len(population)
    k = max(1, int(n * boost_rate))
    top = sorted(population, key=lambda a: a.fitness)[:k]

    # clones
    clones = [Abeille(chemin=list(ab.chemin), fitness=ab.fitness) for ab in top]

    # immigrants
    fleurs_ids = [f.id for f in fleurs]
    fleurs_idx = make_fleurs_index(fleurs)
    ruche = Ruche()
    imms = []
    for _ in range(immigrants):
        ch = fleurs_ids[:]
        random.shuffle(ch)
        ab = Abeille(ch)
        ab.compute_fitness(fleurs_idx, ruche)
        imms.append(ab)

    return population + clones + imms


def next_generation(population: List[Abeille], fleurs_idx: Dict[int, Fleur], ruche: Ruche,
                    elite_n=ELITE_N, p_mut=P_MUT, tournoi_k=TOURNOI_K, pop_size=None) -> List[Abeille]:
    """Produit une nouvelle génération (sélection + croisement + mutation + élitisme)."""
    pop_size = pop_size or len(population)
    population_sorted = sorted(population, key=lambda a: a.fitness)

    # élitisme
    next_pop = [population_sorted[i] for i in range(min(elite_n, len(population_sorted)))]

    # reproduction
    while len(next_pop) < pop_size:
        p1, p2 = selection_tournoi(population_sorted, k=tournoi_k, n_parents=2)
        child_path = crossover_ox(p1.chemin, p2.chemin)
        mutation_swap(child_path, p_mut=p_mut)
        child = Abeille(child_path)
        child.compute_fitness(fleurs_idx, ruche)
        next_pop.append(child)

    return next_pop


def evolve(fleurs: List[Fleur], generations=50, pop_size=POP_SIZE,
           p_mut=P_MUT, elite_n=ELITE_N, tournoi_k=TOURNOI_K,
           boost_every=None, boost_rate=0.1, immigrants=0, seed=None) -> dict:
    """
    Boucle d'évolution complète.
    boost_every: si int, applique boost_population toutes les 'boost_every' générations
    """
    if seed is not None:
        random.seed(seed)

    fleurs_idx = make_fleurs_index(fleurs)
    ruche = Ruche()
    population = init_population(fleurs, pop_size=pop_size)

    best_hist, avg_hist = [], []

    for gen in range(generations):
        best = min(a.fitness for a in population)
        avg = sum(a.fitness for a in population) / len(population)
        best_hist.append(best)
        avg_hist.append(avg)

        if boost_every and (gen > 0) and (gen % boost_every == 0):
            population = boost_population(population, fleurs,
                                          boost_rate=boost_rate,
                                          immigrants=immigrants,
                                          seed=seed)

        population = next_generation(population, fleurs_idx, ruche,
                                     elite_n=elite_n, p_mut=p_mut,
                                     tournoi_k=tournoi_k, pop_size=pop_size)

    best_ind = min(population, key=lambda a: a.fitness)
    return {
        "best": best_ind,
        "history_best": best_hist,
        "history_avg": avg_hist,
        "fleurs_idx": fleurs_idx,
        "ruche": ruche,
    }

# --- Chemins de référence & comparaison ---

def nearest_neighbor_path(fleurs_idx: Dict[int, Fleur], ruche: Ruche) -> Tuple[List[int], float]:
    """Construit un chemin glouton (plus proche voisin) et renvoie (chemin, distance)."""
    import math

    remaining = set(fleurs_idx.keys())
    chemin: List[int] = []
    cur = ruche.position()

    while remaining:
        # trouve la fleur la plus proche du point courant
        best_id = None
        best_d = math.inf
        for fid in remaining:
            d = distance_xy(cur, fleurs_idx[fid].position())
            if d < best_d:
                best_d = d
                best_id = fid
        chemin.append(best_id)
        cur = fleurs_idx[best_id].position()
        remaining.remove(best_id)

    # calcule la distance totale ruche -> fleurs -> ruche
    d_total = chemin_distance(chemin, fleurs_idx, ruche)
    return chemin, d_total


def brute_force_optimal_distance(fleurs_idx: Dict[int, Fleur], ruche: Ruche, limit_n: int = 10) -> Tuple[Optional[List[int]], Optional[float]]:
    """
    Si le nombre de fleurs <= limit_n, calcule l'optimal exact par brute-force (permutations).
    Sinon renvoie (None, None).
    """
    from itertools import permutations
    ids = list(fleurs_idx.keys())
    n = len(ids)
    if n > limit_n:
        return None, None

    best_path = None
    best_dist = float("inf")

    for perm in permutations(ids):
        d = chemin_distance(list(perm), fleurs_idx, ruche)
        if d < best_dist:
            best_dist = d
            best_path = list(perm)

    return best_path, best_dist


def chemin_distance(chemin: List[int], fleurs_idx: Dict[int, Fleur], ruche: Ruche) -> float:
    """Distance totale pour un chemin (helper fonctionnel)."""
    ab = Abeille(chemin=list(chemin))
    return ab.compute_fitness(fleurs_idx, ruche)
