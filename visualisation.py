# visualisation.py
import matplotlib.pyplot as plt

# Couleurs
ROSE   = "#ff69b4"   # fleurs
OR     = "#ffd700"   # ruche
CHEMIN = "#3a3a3a"   # ligne de chemin

def plot_fleurs(fleurs, ruche=None, title="Champ de fleurs", savepath=None):
    xs = [f.x for f in fleurs]; ys = [f.y for f in fleurs]
    plt.figure()
    plt.scatter(xs, ys, s=36, color=ROSE, edgecolors="none", zorder=3, label="Fleurs")
    if ruche is not None:
        rx, ry = ruche.position()
        plt.scatter([rx], [ry], marker="*", s=200, color=OR, edgecolors="black",
                    linewidths=0.5, zorder=4, label="Ruche")
    plt.title(title); plt.xlabel("x"); plt.ylabel("y"); plt.axis("equal"); plt.legend()
    if savepath: plt.savefig(savepath, bbox_inches="tight")
    plt.show()

def plot_best_path(fleurs_idx, ruche, chemin, title="Meilleur chemin", savepath=None):
    pts = [ruche.position()] + [fleurs_idx[i].position() for i in chemin] + [ruche.position()]
    xs = [p[0] for p in pts]; ys = [p[1] for p in pts]

    plt.figure()
    # fleurs
    plt.scatter([p[0] for p in pts[1:-1]], [p[1] for p in pts[1:-1]],
                s=36, color=ROSE, edgecolors="none", zorder=3, label="Fleurs")
    # ruche
    rx, ry = ruche.position()
    plt.scatter([rx], [ry], marker="*", s=200, color=OR, edgecolors="black",
                linewidths=0.5, zorder=4, label="Ruche")
    # chemin
    plt.plot(xs, ys, marker="o", markersize=3, linewidth=1.2, color=CHEMIN, zorder=2, label="Chemin")

    plt.title(title); plt.xlabel("x"); plt.ylabel("y"); plt.axis("equal"); plt.legend()
    if savepath: plt.savefig(savepath, bbox_inches="tight")
    plt.show()

def plot_fitness_history(best_list, avg_list, title="Évolution de la fitness", savepath=None):
    """Trace best & moyenne par génération (↓ = mieux)."""
    plt.figure()
    plt.plot(best_list, label="Best")
    plt.plot(avg_list,  label="Moyenne")
    plt.title(title); plt.xlabel("Génération"); plt.ylabel("Distance (plus bas = mieux)"); plt.legend()
    if savepath: plt.savefig(savepath, bbox_inches="tight")
    plt.show()

def plot_benchmark_histories(best_histories, labels, title="Comparaison des presets", savepath=None):
    """Plusieurs courbes 'best' (une par preset)."""
    plt.figure()
    for hist, label in zip(best_histories, labels):
        plt.plot(hist, label=label)
    plt.title(title); plt.xlabel("Génération"); plt.ylabel("Meilleure distance (↓ = mieux)"); plt.legend()
    if savepath: plt.savefig(savepath, bbox_inches="tight")
    plt.show()

def plot_benchmark_bars(best_values, labels, title="Distance finale par preset", savepath=None):
    """Barres comparant la meilleure distance finale de chaque preset."""
    plt.figure()
    x = range(len(labels))
    plt.bar(x, best_values)
    plt.xticks(x, labels)
    plt.title(title); plt.ylabel("Distance finale (↓ = mieux)")
    if savepath: plt.savefig(savepath, bbox_inches="tight")
    plt.show()
