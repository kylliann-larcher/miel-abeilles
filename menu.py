from config import FLEURS_CSV, DEFAULT_N_FLEURS, MAX_COORD
from beehive import generate_fleurs, save_fleurs, load_fleurs

def run_menu():
    while True:
        print("\n=== Menu Gestion des Fleurs ===")
        print("[1] Générer un nouveau fichier de fleurs")
        print("[2] Afficher un aperçu du fichier actuel")
        print("[0] Quitter")

        choix = input("Votre choix: ").strip()

        if choix == "1":
            try:
                n_str = input(f"Nombre de fleurs (défaut {DEFAULT_N_FLEURS}): ").strip()
                n = int(n_str) if n_str else DEFAULT_N_FLEURS
                fleurs = generate_fleurs(n, MAX_COORD)
                save_fleurs(FLEURS_CSV, fleurs)
                print(f"✅ {n} fleurs générées et enregistrées dans {FLEURS_CSV}")
            except ValueError:
                print("❌ Entrée invalide.")
        elif choix == "2":
            try:
                fleurs = load_fleurs(FLEURS_CSV)
                print(f"📊 Aperçu des {min(5, len(fleurs))} premières fleurs:")
                for f in fleurs[:5]:
                    print(f" - Fleur(id={f.id}, x={f.x}, y={f.y})")
            except FileNotFoundError:
                print("❌ Aucun fichier trouvé, générez d'abord des fleurs.")
        elif choix == "0":
            print("👋 Au revoir.")
            break
        else:
            print("⛔ Choix invalide.")
