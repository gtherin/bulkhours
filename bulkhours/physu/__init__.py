import matplotlib.pyplot as plt  # directive d'importation standard de Matplotlib
import numpy as np  # directive d'importation standard de numpy


def V(r):  # potentiel de Morse
    return 10 * (1.0 - np.exp(-(r - 1))) ** 2.0


def get_potential():
    with plt.xkcd():
        fig, ax = plt.subplots(figsize=(10, 4))

        r = np.linspace(0.2, 7, 200)
        u = V(r)
        plt.plot(r, u, color="salmon", linewidth=2, linestyle="-")
        ax.spines["top"].set_visible(False)
        ax.spines["bottom"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.spines["left"].set_visible(False)
        ax.set_xticks([])
        ax.set_yticks([])

        # description du puit de potentiel
        ax.plot((-0.3, 7.56), (10.5, 10.5), color="black", linewidth=2)
        ax.text(7.3, 9.5, "x", fontname="Comic Sans")
        ax.plot([0.02, 0.02], (-0.35, 16), color="black", linewidth=2)
        ax.plot([0.09, 0.09], (-0.3, 14), color="xkcd:sky blue", linewidth=1.5)
        ax.plot([0.09, 5], (-0.3, -0.3), color="xkcd:sky blue", linewidth=1.5)

        ax.text(-0.3, -0.3, "-U", fontname="Comic Sans")
        ax.text(-0.3, 14, "U(x)", fontname="Comic Sans", rotation=90)

        ax.plot([5, 5], (-0.3, 10.2), color="xkcd:sky blue", linewidth=1.5)
        ax.plot([5, 7], (10.2, 10.2), color="xkcd:sky blue", linewidth=1.5)

        ax.text(-0.08, 10.2, "0", fontname="Comic Sans")
        ax.text(5, 11, "a", fontname="Comic Sans")

        plt.show()


def get_potential():
    with plt.xkcd():
        fig, ax = plt.subplots(figsize=(8, 5))

        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.set_xticks([])
        ax.set_yticks([])

        args = [[0.62, 0.9], [0.0, -0.08]]

        colors = ["blue", "red", None]

        x = np.linspace(0, 1)

        for i in [0, 1]:
            ax.plot(x, np.sin(np.pi * x * (i + 1)) ** 2, c="blue")
            ax.text(*args[i], f"n={i+1}", color=colors[i], fontname="Comic Sans")
        # ax.plot(x, np.sin(np.pi*2*x)**2, c="red")
        # ax.text(0.9, 0.5, 'n=2', color="red", fontname="Comic Sans")

        ax.text(0.0, -0.08, "0", fontname="Comic Sans")
        ax.text(0.98, -0.08, "a", fontname="Comic Sans")

        ax.set_xlim([-0.0, 1.0])
        ax.set_ylim([-0.0, 1.1])
        ax.set_xlabel("x", fontname="Comic Sans")
        ax.set_ylabel("P(x)", fontname="Comic Sans")
