import matplotlib.pyplot as plt
import numpy as np


def V(r):  # potentiel de Morse
    return 10 * (1.0 - np.exp(-(r - 1))) ** 2.0


def get_potential(exp=True, theo=True):
    with plt.xkcd():
        fig, ax = plt.subplots(figsize=(10, 4))

        r = np.linspace(0.2, 7, 200)
        u = V(r)
        if exp:
            plt.plot(r, u, color="salmon", linewidth=2, linestyle="-")

        ax.spines["top"].set_visible(False)
        ax.spines["bottom"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.spines["left"].set_visible(False)
        ax.set_xticks([])
        ax.set_yticks([])

        ax.plot((-0.3, 7.56), (10.5, 10.5), color="black", linewidth=2)
        ax.text(7.3, 9.5, "x", fontname="default")
        ax.plot([0.02, 0.02], (-0.35, 16), color="black", linewidth=2)
        ax.text(-0.3, 14, "U(x)", fontname="Comic Sans", rotation=90)
        ax.text(-0.08, 10.2, "0", fontname="Comic Sans")
        ax.text(5, 11, "a", fontname="Comic Sans")
        ax.text(-0.3, -0.3, "-U", fontname="Comic Sans")

        if theo:
            ax.plot([0.09, 0.09], (-0.3, 14), color="xkcd:sky blue", linewidth=1.5)
            ax.plot([0.09, 5], (-0.3, -0.3), color="xkcd:sky blue", linewidth=1.5)
            ax.plot([5, 5], (-0.3, 10.2), color="xkcd:sky blue", linewidth=1.5)
            ax.plot([5, 7], (10.2, 10.2), color="xkcd:sky blue", linewidth=1.5)

        return fig


def get_pdf(modes=[0, 1], fontname="Comic Sans"):
    with plt.xkcd():
        fig, ax = plt.subplots(figsize=(8, 5))

        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.set_xticks([])
        ax.set_yticks([])

        args = [[0.62, 0.9], [0.9, 0.5]]

        colors = plt.rcParams["axes.prop_cycle"].by_key()["color"]
        x = np.linspace(0, 1)

        for i in modes:
            ax.plot(x, np.sin(np.pi * x * (i + 1)) ** 2, c=colors[i], label=f"n={i+1}")

        ax.text(0.0, -0.08, "0", fontname=fontname)
        ax.text(0.98, -0.08, "a", fontname=fontname)

        ax.set_xlim([-0.0, 1.0])
        ax.set_ylim([-0.0, 1.1])
        ax.set_xlabel("x", fontname=fontname)
        ax.set_ylabel("P(x)", fontname=fontname)
        ax.legend(loc=2)
        return fig
