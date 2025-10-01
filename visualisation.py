# visualisation.py
import matplotlib.pyplot as plt

# Style global lisible
plt.rcParams.update({
    "figure.figsize": (8, 6),
    "axes.grid": True,
    "axes.titlesize": 12,
    "axes.labelsize": 10,
    "legend.fontsize": 9,
})

# Couleurs
ROSE   = "#ff69b4"   # fleurs
OR     = "#ffd700"   # ruche
CHEMIN = "#3a3a3a"   # chemin AG
REF    = "#2e8b57"   # chemin Référence (vert)

def _maybe_save(savepath):
    if savepath:
        plt.savefig(savepath, bbox_inches="tight")

def plot_fleurs(fleurs, ruche=None, title="Champ de fleurs", savepath=None):
    xs = [f.x for f in fleurs]; ys = [f.y for f in fleurs]
    plt.figure()
    plt.scatter(xs, ys, s=36, color=ROSE, edgecolors="none", zorder=3, label="Fleurs")
    if ruche is not None:
        rx, ry = ruche.position()
        plt.scatter([rx], [ry], marker="*", s=200, color=OR, edgecolors="black",
                    linewidths=0.5, zorder=4, label="Ruche")
    plt.title(title); plt.xlabel("x"); plt.ylabel("y"); plt.axis("equal"); plt.legend()
    _maybe_save(savepath)

def plot_best_path(fleurs_idx, ruche, chemin_ag, title="Meilleur chemin", savepath=None,
                   chemin_ref=None):
    """Trace le meilleur chemin AG, et (si fourni) SUPERPOSE le chemin de référence."""
    pts_ag  = [ruche.position()] + [fleurs_idx[i].position() for i in chemin_ag] + [ruche.position()]
    xs_ag   = [p[0] for p in pts_ag]; ys_ag = [p[1] for p in pts_ag]

    plt.figure()
    # fleurs
    plt.scatter([p[0] for p in pts_ag[1:-1]], [p[1] for p in pts_ag[1:-1]],
                s=36, color=ROSE, edgecolors="none", zorder=3, label="Fleurs")
    # ruche
    rx, ry = ruche.position()
    plt.scatter([rx], [ry], marker="*", s=200, color=OR, edgecolors="black",
                linewidths=0.5, zorder=4, label="Ruche")
    # chemin AG
    plt.plot(xs_ag, ys_ag, marker="o", markersize=3, linewidth=1.2,
             color=CHEMIN, zorder=2, label="Chemin abeilles")

    # superposition référence
    if chemin_ref is not None:
        pts_ref = [ruche.position()] + [fleurs_idx[i].position() for i in chemin_ref] + [ruche.position()]
        xs_ref  = [p[0] for p in pts_ref]; ys_ref = [p[1] for p in pts_ref]
        plt.plot(xs_ref, ys_ref, marker="o", markersize=3, linewidth=1.2,
                 color=REF, alpha=0.9, zorder=1, label="Chemin référence")

    plt.title(title); plt.xlabel("x"); plt.ylabel("y"); plt.axis("equal"); plt.legend()
    _maybe_save(savepath)

def plot_compare_paths(fleurs_idx, ruche, chemin_ref, chemin_ag, title="Référence vs Abeilles", savepath=None):
    """Comparatif explicite (référence + AG)."""
    rx, ry = ruche.position()
    pts_ref = [ruche.position()] + [fleurs_idx[i].position() for i in chemin_ref] + [ruche.position()]
    xs_ref = [p[0] for p in pts_ref]; ys_ref = [p[1] for p in pts_ref]
    pts_ag  = [ruche.position()] + [fleurs_idx[i].position() for i in chemin_ag] + [ruche.position()]
    xs_ag = [p[0] for p in pts_ag]; ys_ag = [p[1] for p in pts_ag]

    plt.figure()
    plt.scatter([p[0] for p in pts_ref[1:-1]], [p[1] for p in pts_ref[1:-1]],
                s=36, color=ROSE, edgecolors="none", zorder=3, label="Fleurs")
    plt.scatter([rx], [ry], marker="*", s=200, color=OR, edgecolors="black",
                linewidths=0.5, zorder=4, label="Ruche")
    plt.plot(xs_ref, ys_ref, marker="o", markersize=3, linewidth=1.2,
             color=REF, alpha=0.9, zorder=2, label="Chemin référence")
    plt.plot(xs_ag,  ys_ag,  marker="o", markersize=3, linewidth=1.2,
             color=CHEMIN, alpha=0.8, zorder=1, label="Chemin abeilles")
    plt.title(title); plt.xlabel("x"); plt.ylabel("y"); plt.axis("equal"); plt.legend()
    _maybe_save(savepath)

def plot_ref_path(fleurs_idx, ruche, chemin_ref, title="Chemin de référence", savepath=None):
    """Affiche uniquement le chemin de référence (baseline)."""
    pts = [ruche.position()] + [fleurs_idx[i].position() for i in chemin_ref] + [ruche.position()]
    xs = [p[0] for p in pts]; ys = [p[1] for p in pts]
    plt.figure()
    plt.scatter([p[0] for p in pts[1:-1]], [p[1] for p in pts[1:-1]],
                s=36, color=ROSE, edgecolors="none", zorder=3, label="Fleurs")
    rx, ry = ruche.position()
    plt.scatter([rx], [ry], marker="*", s=200, color=OR, edgecolors="black",
                linewidths=0.5, zorder=4, label="Ruche")
    plt.plot(xs, ys, marker="o", markersize=3, linewidth=1.2,
             color=REF, zorder=2, label="Chemin référence")
    plt.title(title); plt.xlabel("x"); plt.ylabel("y"); plt.axis("equal"); plt.legend()
    _maybe_save(savepath)

def plot_fitness_history(best_list, avg_list, title="Évolution de la fitness", savepath=None):
    plt.figure()
    plt.plot(best_list, label="Best")
    plt.plot(avg_list,  label="Moyenne")
    plt.title(title); plt.xlabel("Génération"); plt.ylabel("Distance (↓ = mieux)"); plt.legend()
    _maybe_save(savepath)

def plot_benchmark_histories(best_histories, labels, title="Comparaison des presets",
                             savepath=None, ref_value=None):
    plt.figure()
    for hist, label in zip(best_histories, labels):
        plt.plot(hist, label=label)
    # --- ligne de référence (OPT/NN) si fournie ---
    if ref_value is not None:
        plt.axhline(ref_value, linestyle="--", linewidth=1.3, color="#2e8b57",
                    label="Référence (OPT/NN)", alpha=0.9)
    plt.title(title)
    plt.xlabel("Génération")
    plt.ylabel("Meilleure distance (↓ = mieux)")
    plt.legend()
    if savepath:
        plt.savefig(savepath, bbox_inches="tight")

    plt.figure()
    for hist, label in zip(best_histories, labels):
        plt.plot(hist, label=label)
    plt.title(title); plt.xlabel("Génération"); plt.ylabel("Meilleure distance (↓ = mieux)"); plt.legend()
    _maybe_save(savepath)

def plot_benchmark_bars(best_values, labels, title="Distance finale par preset", savepath=None):
    plt.figure()
    x = range(len(labels))
    plt.bar(x, best_values)
    plt.xticks(x, labels)
    plt.title(title); plt.ylabel("Distance finale (↓ = mieux)")
    _maybe_save(savepath)

def plot_bars_ref_vs_best(labels, ref_value, best_values, title="Référence vs AG (distance finale)", savepath=None):
    """
    Barres groupées: pour chaque preset -> barre Référence (unique, même dataset) + barre AG.
    ref_value: float (distance ref, OPT si <=10, sinon NN)
    best_values: list[float] (distances finales AG par preset, alignées avec labels)
    """
    import numpy as np
    plt.figure()
    x = np.arange(len(labels))
    w = 0.38

    ref = [ref_value] * len(labels)
    plt.bar(x - w/2, ref, width=w, label="Référence", color="#2e8b57", alpha=0.85)
    plt.bar(x + w/2, best_values, width=w, label="AG (final)", color="#3a3a3a", alpha=0.9)

    # petites annotations au-dessus des barres AG (écart %)
    for i, ag in enumerate(best_values):
        gap = 100.0 * (ag - ref_value) / ref_value
        plt.text(x[i] + w/2, ag, f"{gap:+.1f}%", ha="center", va="bottom", fontsize=9)

    plt.xticks(x, labels)
    plt.ylabel("Distance (↓ = mieux)")
    plt.title(title)
    plt.legend()
    if savepath:
        plt.savefig(savepath, bbox_inches="tight")
