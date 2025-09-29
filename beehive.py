from dataclasses import dataclass
import csv
import random
from typing import List

@dataclass(frozen=True)
class Fleur:
    id: int
    x: float
    y: float

    def position(self) -> tuple[float, float]:
        return (self.x, self.y)


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
