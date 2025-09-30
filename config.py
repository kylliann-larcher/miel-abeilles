from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent
DATA_DIR = ROOT_DIR / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)

FLEURS_CSV = DATA_DIR / "fleurs.csv"

# Position de la ruche
RUCHE_POS = (500.0, 500.0)

# Paramètres par défaut
DEFAULT_N_FLEURS = 30
MAX_COORD = 1000
POP_SIZE = 80
ELITE_N = 2
P_MUT = 0.05
TOURNOI_K = 3

# Dossier résultats
RESULTS_DIR = ROOT_DIR / "results"
RESULTS_DIR.mkdir(parents=True, exist_ok=True)

# --- Presets de benchmark ---
PRESETS = {
    "petit": {
        "generations": 40,
        "pop_size": 40,
        "p_mut": 0.08,
        "elite_n": 2,
        "tournoi_k": 3,
    },
    "moyen": {
        "generations": 80,
        "pop_size": 80,
        "p_mut": 0.06,
        "elite_n": 2,
        "tournoi_k": 3,
    },
    "tres_precis": {
        "generations": 150,
        "pop_size": 150,
        "p_mut": 0.04,
        "elite_n": 2,
        "tournoi_k": 3,
    },
}
