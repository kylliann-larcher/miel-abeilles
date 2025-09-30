from config import (
    FLEURS_CSV, RESULTS_DIR,
    DEFAULT_N_FLEURS, MAX_COORD, POP_SIZE, P_MUT
)
from beehive import generate_fleurs, save_fleurs, load_fleurs, evolve, Ruche
from visualisation import plot_fleurs, plot_best_path, plot_fitness_history

def ask_int(prompt, default):
    txt = input(f"{prompt} (défaut {default}): ").strip()
    return int(txt) if txt else default

def ask_float(prompt, default):
    txt = input(f"{prompt} (défaut {default}): ").strip()
    return float(txt) if txt else default

def run_menu():
    while True:
        print("\n=== Menu ===")
        print("[1] Générer fleurs.csv")
        print("[2] Visualiser le nuage de fleurs + ruche")
        print("[3] Lancer une démo AG (simplifiée)")
        print("[0] Quitter")

        c = input("Votre choix: ").strip()

        if c == "1":
            try:
                n = ask_int("Nombre de fleurs", DEFAULT_N_FLEURS)
                maxc = ask_int("Coordonnée max", MAX_COORD)
                fleurs = generate_fleurs(n, maxc)
                save_fleurs(FLEURS_CSV, fleurs)
                print(f"✅ {n} fleurs générées → {FLEURS_CSV}")
            except ValueError:
                print("❌ Entrée invalide.")

        elif c == "2":
            try:
                fleurs = load_fleurs(FLEURS_CSV)
                plot_fleurs(fleurs, ruche=Ruche(), title="Fleurs + Ruche")
            except FileNotFoundError:
                print("❌ Aucun fichier trouvé. Générez d'abord des fleurs.")

        elif c == "3":
            try:
                fleurs = load_fleurs(FLEURS_CSV)

                print("\n=== Démo AG simplifiée ===")
                gens = ask_int("Nombre de générations", 50)
                pop  = ask_int("Taille de la population", POP_SIZE)
                pmut = ask_float("Taux de mutation", P_MUT)

                # AG avec paramètres simplifiés
                res = evolve(
                    fleurs,
                    generations=gens,
                    pop_size=pop,
                    p_mut=pmut,
                    elite_n=2,       # fixé par défaut
                    tournoi_k=3,     # fixé par défaut
                    boost_every=None # désactivé par défaut
                )

                best = res["best"]; ruche = res["ruche"]; idx = res["fleurs_idx"]

                # Affichages
                title = f"Meilleur chemin (distance={best.fitness:.1f})"
                plot_best_path(idx, ruche, best.chemin, title=title)
                plot_fitness_history(res["history_best"], res["history_avg"])

            except FileNotFoundError:
                print("❌ Aucun fichier trouvé. Générez d'abord des fleurs.")
            except ValueError:
                print("❌ Paramètres invalides.")

        elif c == "0":
            print("👋 Au revoir."); break
        else:
            print("⛔ Choix invalide.")
