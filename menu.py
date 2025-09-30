from datetime import datetime
import csv
from pathlib import Path

from config import (
    FLEURS_CSV, RESULTS_DIR,
    POP_SIZE, P_MUT, PRESETS
)
from beehive import load_fleurs, evolve, Ruche
from visualisation import (
    plot_fleurs, plot_best_path, plot_fitness_history,
    plot_benchmark_histories, plot_benchmark_bars
)

def ask_int(prompt, default):
    txt = input(f"{prompt} (défaut {default}): ").strip()
    return int(txt) if txt else default

def ask_float(prompt, default):
    txt = input(f"{prompt} (défaut {default}): ").strip()
    return float(txt) if txt else default

def run_menu():
    while True:
        print("\n=== Menu Principal ===")
        print("[1] Visualiser le nuage de fleurs + ruche")
        print("[2] Démo AG (simplifiée)")
        print("[3] Benchmark (petit / moyen / très précis) → autosave + CSV")
        print("[0] Quitter")

        c = input("Votre choix: ").strip()

        if c == "1":
            try:
                fleurs = load_fleurs(FLEURS_CSV)
                plot_fleurs(fleurs, ruche=Ruche(), title="Fleurs (rose) + Ruche")
            except FileNotFoundError:
                print("❌ Aucun fichier trouvé. Placez un fichier fleurs.csv dans /data.")

        elif c == "2":
            try:
                fleurs = load_fleurs(FLEURS_CSV)
                print("\n=== Démo AG simplifiée ===")
                gens = ask_int("Nombre de générations", 50)
                pop  = ask_int("Taille de la population", POP_SIZE)
                pmut = ask_float("Taux de mutation", P_MUT)

                res = evolve(
                    fleurs,
                    generations=gens,
                    pop_size=pop,
                    p_mut=pmut,
                    elite_n=2,
                    tournoi_k=3,
                    boost_every=None
                )
                best = res["best"]; ruche = res["ruche"]; idx = res["fleurs_idx"]
                plot_best_path(idx, ruche, best.chemin, title=f"Meilleur chemin (distance={best.fitness:.1f})")
                plot_fitness_history(res["history_best"], res["history_avg"])

            except FileNotFoundError:
                print("❌ Aucun fichier trouvé. Placez un fichier fleurs.csv dans /data.")
            except ValueError:
                print("❌ Paramètres invalides.")

        elif c == "3":
            # --- BENCHMARK SIMPLIFIÉ (seed fixe) ---
            try:
                from datetime import datetime
                import csv, time
                from pathlib import Path

                fleurs = load_fleurs(FLEURS_CSV)

                # Dossier du benchmark (horodaté)
                run_dir = RESULTS_DIR / f"benchmark_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
                run_dir.mkdir(parents=True, exist_ok=True)

                labels = ["petit", "moyen", "tres_precis"]
                results = []
                best_histories = []
                final_bests = []

                summary_csv = run_dir / "summary.csv"
                with summary_csv.open("w", newline="") as fsum:
                    w = csv.writer(fsum)
                    w.writerow([
                        "preset","generations","pop_size","p_mut",
                        "elite_n","tournoi_k","final_best_distance","runtime_seconds"
                    ])

                    for label in labels:
                        p = PRESETS[label]
                        print(f"→ Exécution preset: {label}")
                        t0 = time.perf_counter()
                        res = evolve(
                            fleurs,
                            generations=p["generations"],
                            pop_size=p["pop_size"],
                            p_mut=p["p_mut"],
                            elite_n=p["elite_n"],
                            tournoi_k=p["tournoi_k"],
                            boost_every=None,
                            seed=123  # FIXE
                        )
                        dt = time.perf_counter() - t0

                        results.append(res)
                        best_histories.append(res["history_best"])
                        final_best = min(res["history_best"])
                        final_bests.append(final_best)

                        # Résumé CSV
                        w.writerow([
                            label, p["generations"], p["pop_size"], p["p_mut"],
                            p["elite_n"], p["tournoi_k"],
                            f"{final_best:.6f}", f"{dt:.4f}"
                        ])

                        # Historique CSV
                        hist_csv = run_dir / f"history_{label}.csv"
                        with hist_csv.open("w", newline="") as fh:
                            wh = csv.writer(fh)
                            wh.writerow(["generation","best","avg"])
                            for i, (b, a) in enumerate(zip(res["history_best"], res["history_avg"])):
                                wh.writerow([i, f"{b:.6f}", f"{a:.6f}"])

                # Graphiques comparatifs
                from visualisation import (
                    plot_benchmark_histories, plot_benchmark_bars, plot_best_path
                )
                histories_png = run_dir / "histories.png"
                bars_png = run_dir / "final_bars.png"
                plot_benchmark_histories(
                    best_histories, labels,
                    title="Comparaison presets (seed fixe)",
                    savepath=str(histories_png)
                )
                plot_benchmark_bars(
                    final_bests, labels,
                    title="Distance finale par preset (seed fixe)",
                    savepath=str(bars_png)
                )

                # Chemin du meilleur preset
                idx_best = final_bests.index(min(final_bests))
                res_best = results[idx_best]
                best = res_best["best"]; ruche = res_best["ruche"]; idx = res_best["fleurs_idx"]
                best_path_png = run_dir / f"best_path_{labels[idx_best]}.png"
                plot_best_path(
                    idx, ruche, best.chemin,
                    title=f"Meilleur chemin [{labels[idx_best]}] (dist={best.fitness:.1f})",
                    savepath=str(best_path_png)
                )

                # Résumé console
                print("\n=== Résumé Benchmark ===")
                for label, res in zip(labels, results):
                    print(f"- {label:12s} | dist finale={res['best'].fitness:.2f}")
                print(f"\n💾 Résultats sauvegardés dans: {run_dir}")

            except FileNotFoundError:
                print("❌ Aucun fichier trouvé. Placez un fichier fleurs.csv dans /data.")

        elif c == "0":
            print("👋 Au revoir.")
            break
        else:
            print("⛔ Choix invalide.")
