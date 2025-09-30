# visualisation.py
import matplotlib.pyplot as plt

def plot_fleurs(fleurs, ruche=None, title="Champ de fleurs", savepath=None):
    xs = [f.x for f in fleurs]; ys = [f.y for f in fleurs]
    plt.figure()
    plt.scatter(xs, ys, s=30, label="Fleurs")
    if ruche is not None:
        rx, ry = ruche.position()
        plt.scatter([rx], [ry], marker="*", s=180, label="Ruche")
    plt.title(title); plt.xlabel("x"); plt.ylabel("y"); plt.axis("equal"); plt.legend()
    if savepath: plt.savefig(savepath, bbox_inches="tight")
    plt.show()

def plot_best_path(fleurs_idx, ruche, chemin, title="Meilleur chemin", savepath=None):
    pts = [ruche.position()] + [fleurs_idx[i].position() for i in chemin] + [ruche.position()]
    xs = [p[0] for p in pts]; ys = [p[1] for p in pts]
    plt.figure()
    # points fleurs
    plt.scatter([p[0] for p in pts[1:-1]], [p[1] for p in pts[1:-1]], s=30, label="Fleurs")
    # ruche
    rx, ry = ruche.position()
    plt.scatter([rx], [ry], marker="*", s=180, label="Ruche")
    # chemin
    plt.plot(xs, ys, marker="o", linewidth=1, label="Chemin")
    plt.title(title); plt.xlabel("x"); plt.ylabel("y"); plt.axis("equal"); plt.legend()
    if savepath: plt.savefig(savepath, bbox_inches="tight")
    plt.show()

def plot_fitness_history(best_list, avg_list, title="Évolution de la fitness", savepath=None):
    plt.figure()
    plt.plot(best_list, label="Best")
    plt.plot(avg_list, label="Moyenne")
    plt.title(title); plt.xlabel("Génération"); plt.ylabel("Distance (plus bas = mieux)"); plt.legend()
    if savepath: plt.savefig(savepath, bbox_inches="tight")
    plt.show()
