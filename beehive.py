from dataclasses import dataclass
import csv
import random
from math import hypot
from typing import List, Tuple
from config import RUCHE_POS


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


# ---------- Utilitaires communs ----------

def distance_xy(a: Tuple[float, float], b: Tuple[float, float]) -> float:
    """Distance euclidienne entre deux points (x, y)."""
    return hypot(a[0] - b[0], a[1] - b[1])


# ---------- Fleurs: génération / IO CSV ----------

def generate_fleurs(n: int, max_coord: int) -> List[Fleur]:
    """Génère n fleurs aléatoires dans un carré [0, max_coord]."""
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
