from pathlib import Path

# Répertoires
ROOT_DIR = Path(__file__).resolve().parent
DATA_DIR = ROOT_DIR / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)

# Fichiers
FLEURS_CSV = DATA_DIR / "fleurs.csv"

# Paramètres par défaut
DEFAULT_N_FLEURS = 20
MAX_COORD = 1000
