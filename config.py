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
    "petit":       {"generations": 60,  "pop_size": 50,  "p_mut": 0.12, "elite_n": 1, "tournoi_k": 2},
    "moyen":       {"generations": 200, "pop_size": 100, "p_mut": 0.08, "elite_n": 2, "tournoi_k": 3},
    "tres_precis": {"generations": 500, "pop_size": 200, "p_mut": 0.05, "elite_n": 3, "tournoi_k": 4},
}


