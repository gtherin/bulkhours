import matplotlib.pyplot as plt
import pandas as pd
import numpy as np


def get_potential(exp=True, theo=True, fontname="Comic Sans"):
    with plt.xkcd():
        fig, ax = plt.subplots(figsize=(10, 4))

        if exp:
            r = np.linspace(0.2, 7, 200)
            u = 10 * (1.0 - np.exp(-(r - 1))) ** 2.0
            plt.plot(r, u, color="salmon", linewidth=2, linestyle="-")

        ax.plot((-0.3, 7.56), (10.5, 10.5), color="black", linewidth=2)
        ax.text(7.3, 9.5, "x", fontname=fontname)
        ax.plot([0.02, 0.02], (-0.35, 16), color="black", linewidth=2)
        ax.text(-0.3, 14, "U(x)", fontname=fontname, rotation=90)
        ax.text(-0.08, 10.2, "0", fontname=fontname)
        ax.text(5, 11, "a", fontname=fontname)
        ax.text(-0.3, -0.3, "-U", fontname=fontname)

        if theo:
            ax.plot([0.09, 0.09], (-0.3, 14), color="xkcd:sky blue", linewidth=2)
            ax.plot([0.09, 5], (-0.3, -0.3), color="xkcd:sky blue", linewidth=2)
            ax.plot([5, 5], (-0.3, 10.2), color="xkcd:sky blue", linewidth=2)
            ax.plot([5, 7], (10.2, 10.2), color="xkcd:sky blue", linewidth=2)

        ax.spines["top"].set_visible(False)
        ax.spines["bottom"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.spines["left"].set_visible(False)
        ax.set_xticks([])
        ax.set_yticks([])

        return fig


def get_pdf(modes=[0, 1], fontname="Comic Sans"):
    with plt.xkcd():
        fig, ax = plt.subplots(figsize=(8, 5))

        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.set_xticks([])
        ax.set_yticks([])

        x = np.linspace(0, 1)
        for i in modes:
            ax.plot(x, np.sin(np.pi * x * (i + 1)) ** 2, label=f"n={i+1}")

        ax.text(0.0, -0.08, "0", fontname=fontname)
        ax.text(0.98, -0.08, "a", fontname=fontname)
        ax.set_xlim([-0.0, 1.0])
        ax.set_ylim([-0.0, 1.1])
        ax.set_xlabel("x", fontname=fontname)
        ax.set_ylabel("P(x)", fontname=fontname)
        ax.legend(loc=2)
        return fig


def get_spectrum():
    return pd.DataFrame(
        [
            ["Gamma", "λ < 10pm"],
            ["X", "10pm ≤ λ < 1nm"],
            ["Ultra Violet", "1nm ≤ λ < 350nm"],
            ["Violet (Vis.)", "350nm ≤ λ < 450nm"],
            ["Bleu (Vis.)", "450nm ≤ λ < 500nm"],
            ["Vert (Vis.)", "500nm ≤ λ < 550nm"],
            ["Jaune (Vis.)", "550nm ≤ λ < 600nm"],
            ["Rouge (Vis.)", "600nm ≤ λ < 780nm"],
            ["Infra Rouge", "780nm ≤ λ < 1mm"],
            ["Radio", "1mm ≤ λ"],
        ],
        columns=["Domaine", "Longueur d'onde λ"],
    )
