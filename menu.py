# menu.py
from config import (
    FLEURS_CSV, RESULTS_DIR,
    POP_SIZE, P_MUT, PRESETS
)
from beehive import load_fleurs, evolve, Ruche, nearest_neighbor_path, brute_force_optimal_distance, make_fleurs_index
from visualisation import (
    plot_fleurs, plot_best_path, plot_fitness_history,
    plot_benchmark_histories, plot_compare_paths,
    plot_ref_path, plot_bars_ref_vs_best
)

import csv, time
from datetime import datetime
from matplotlib import pyplot as plt


def ask_int(prompt, default):
    txt = input(f"{prompt} (défaut {default}): ").strip()
    return int(txt) if txt else default


def ask_float(prompt, default):
    txt = input(f"{prompt} (défaut {default}): ").strip()
    return float(txt) if txt else default


def _compute_reference(fleurs_idx, ruche, limit_n_opt=10):
    """Retourne (path_ref, dist_ref, ref_label)"""
    path_opt, dist_opt = brute_force_optimal_distance(fleurs_idx, ruche, limit_n=limit_n_opt)
    if path_opt is None:
        path_ref, dist_ref = nearest_neighbor_path(fleurs_idx, ruche)
        ref_label = "Référence NN (plus proche voisin)"
    else:
        path_ref, dist_ref = path_opt, dist_opt
        ref_label = "Référence OPT (brute force)"
    return path_ref, dist_ref, ref_label


def run_menu():
    while True:
        print("\n=== Menu Principal ===")
        print("[1] Visualiser le nuage de fleurs + ruche")
        print("[2] Démo AG (simplifiée + comparaison)")
        print("[3] Benchmark (petit / moyen / très précis)")
        print("[0] Quitter")

        c = input("Votre choix: ").strip()

        # ------------------------------------------------------------
        # [1] VISUALISATION SIMPLE
        # ------------------------------------------------------------
        if c == "1":
            try:
                plt.close('all')
                fleurs = load_fleurs(FLEURS_CSV)
                plot_fleurs(fleurs, ruche=Ruche(), title="Fleurs (rose) + Ruche")
                plt.show(); plt.close('all')
            except FileNotFoundError:
                print("❌ Aucun fichier trouvé. Placez un fichier fleurs.csv dans /data.")

        # ------------------------------------------------------------
        # [2] DEMO AG SIMPLIFIÉE
        # ------------------------------------------------------------
        elif c == "2":
            try:
                plt.close('all')
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
                    boost_every=None,
                    seed=123
                )

                best = res["best"]; ruche = res["ruche"]; idx = res["fleurs_idx"]

                # --- Référence ---
                path_ref, dist_ref, ref_label = _compute_reference(idx, ruche, limit_n_opt=10)

                dist_ag = best.fitness
                gap = 100.0 * (dist_ag - dist_ref) / dist_ref

                print("\n=== Comparaison ===")
                print(f"- {ref_label}: {dist_ref:.2f}")
                print(f"- Abeilles (AG): {dist_ag:.2f}")
                print(f"→ Écart = {gap:+.2f}%")

                # Graphiques préparés
                plot_ref_path(idx, ruche, path_ref, title=f"Chemin de référence — {ref_label}")
                plot_best_path(idx, ruche, best.chemin,
                               title=f"Meilleur chemin (dist={best.fitness:.1f}) — + Référence",
                               chemin_ref=path_ref)
                plot_compare_paths(idx, ruche, path_ref, best.chemin,
                                   title=f"Référence vs Abeilles — {ref_label}")
                plot_fitness_history(res['history_best'], res['history_avg'])

                plt.show(); plt.close('all')

            except FileNotFoundError:
                print("❌ Aucun fichier trouvé. Placez un fichier fleurs.csv dans /data.")
            except ValueError:
                print("❌ Paramètres invalides.")

        # ------------------------------------------------------------
        # [3] BENCHMARK
        # ------------------------------------------------------------
        elif c == "3":
            try:
                plt.close('all')
                fleurs = load_fleurs(FLEURS_CSV)

                run_dir = RESULTS_DIR / f"benchmark_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
                run_dir.mkdir(parents=True, exist_ok=True)

                labels = ["petit", "moyen", "tres_precis"]
                results, best_histories, final_bests = [], [], []

                # Référence globale (même dataset pour tous)
                fleurs_idx0 = make_fleurs_index(fleurs)
                ruche0 = Ruche()
                path_ref, dist_ref, ref_label = _compute_reference(fleurs_idx0, ruche0, limit_n_opt=10)

                summary_csv = run_dir / "summary.csv"
                with summary_csv.open("w", newline="") as fsum:
                    w = csv.writer(fsum)
                    w.writerow([
                        "preset","generations","pop_size","p_mut",
                        "elite_n","tournoi_k","final_best_distance","gap_vs_ref_pct","runtime_seconds"
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
                            seed=123
                        )
                        dt = time.perf_counter() - t0

                        results.append(res)
                        best_histories.append(res["history_best"])
                        final_best = res["best"].fitness
                        final_bests.append(final_best)

                        gap_pct = 100.0 * (final_best - dist_ref) / dist_ref
                        w.writerow([
                            label, p["generations"], p["pop_size"], p["p_mut"],
                            p["elite_n"], p["tournoi_k"],
                            f"{final_best:.6f}", f"{gap_pct:.2f}", f"{dt:.4f}"
                        ])

                        # Historique CSV
                        hist_csv = run_dir / f"history_{label}.csv"
                        with hist_csv.open("w", newline="") as fh:
                            wh = csv.writer(fh)
                            wh.writerow(["generation","best","avg"])
                            for i, (b, a) in enumerate(zip(res["history_best"], res["history_avg"])):
                                wh.writerow([i, f"{b:.6f}", f"{a:.6f}"])

                # Graphiques comparatifs
                histories_png = run_dir / "histories.png"
                plot_benchmark_histories(best_histories, labels,
                                         title="Comparaison presets (seed fixe)",
                                         savepath=str(histories_png),
                                         ref_value=dist_ref)
                                        

                # Comparaison Référence vs AG
                bars_png = run_dir / "ref_vs_ag_bars.png"
                plot_bars_ref_vs_best(labels, dist_ref, final_bests,
                                      title=f"Référence ({ref_label}) vs AG (final) — seed fixe",
                                      savepath=str(bars_png))

                # Chemin de référence seul
                ref_png = run_dir / "ref_path.png"
                plot_ref_path(fleurs_idx0, ruche0, path_ref,
                              title=f"Chemin de référence — {ref_label}",
                              savepath=str(ref_png))

                # Comparatif du meilleur preset
                idx_best = final_bests.index(min(final_bests))
                res_best = results[idx_best]
                best = res_best["best"]; ruche = res_best["ruche"]; idx = res_best["fleurs_idx"]

                plot_best_path(idx, ruche, best.chemin,
                               title=f"Meilleur chemin [{labels[idx_best]}] (dist={best.fitness:.1f}) — + Référence",
                               savepath=str(run_dir / f"best_path_{labels[idx_best]}_with_ref.png"),
                               chemin_ref=path_ref)
                plot_compare_paths(idx, ruche, path_ref, best.chemin,
                                   title=f"Référence vs Abeilles — {ref_label}",
                                   savepath=str(run_dir / f"compare_best_{labels[idx_best]}.png"))

                plt.show(); plt.close('all')

                print(f"\n💾 Résultats sauvegardés dans: {run_dir}")

            except FileNotFoundError:
                print("❌ Aucun fichier trouvé. Placez un fichier fleurs.csv dans /data.")

        # ------------------------------------------------------------
        # [0] QUITTER
        # ------------------------------------------------------------
        elif c == "0":
            print("👋 Au revoir."); break
        else:
            print("⛔ Choix invalide.")
