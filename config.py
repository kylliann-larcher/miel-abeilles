from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent
DATA_DIR = ROOT_DIR / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)

FLEURS_CSV = DATA_DIR / "fleurs.csv"

# Position ruche affichée sur les graphes
RUCHE_POS = (500.0, 500.0)

# Defaults AG
DEFAULT_N_FLEURS = 30
MAX_COORD = 1000
POP_SIZE = 80
ELITE_N = 2
P_MUT = 0.05
TOURNOI_K = 3

# Sauvegardes éventuelles
RESULTS_DIR = ROOT_DIR / "results"
RESULTS_DIR.mkdir(exist_ok=True)
