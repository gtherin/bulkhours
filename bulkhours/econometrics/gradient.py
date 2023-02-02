import numpy as np
import pandas as pd
import scipy as sp
import matplotlib.pyplot as plt


# Compute square loss
def Loss(y, ypred):
    l = (y - ypred) ** 2
    return l.sum()


def get_grad():
    np.random.seed(1)
    a0 = 0.8
    mdlf = lambda x, a: -0.02 * x**2 + a * x + 0.04
    xm = np.linspace(0, 20, ne := 15)
    ym = mdlf(xm, a0) + sp.stats.norm().rvs(ne)

    fig, axes = plt.subplots(1, 3, figsize=(15, 4))

    def plot_fit(ax, a, c=None, ls="dotted"):
        ax.scatter(xm, ym, marker="X", s=60, zorder=100)
        ax.plot(np.linspace(0, 20, 100), mdlf(np.linspace(0, 20, 100), a), ls=ls, alpha=0.8, c=c)
        for args in zip(xm, ym, mdlf(xm, a)):
            c = "red" if args[1] < args[2] else "green"
            ax.vlines(*args, color=c, alpha=0.5, zorder=50)

    plot_fit(axes[0], 0.8)

    ax = axes[1]
    ex = np.linspace(0.6, 0.95, 20)
    dex = [np.mean((ym - mdlf(xm, e)) ** 2) for e in ex]

    ax.plot(ex, dex)
    c = np.polynomial.polynomial.polyfit(ex, dex, 2, full=True)[0]

    def gd(x):
        return c[0] + c[1] * x + c[2] * x * x

    def dgd(x):
        return c[1] + c[2] * 2 * x

    ax.plot(ex, gd(ex), alpha=0.5)

    def get_tangent(x0):
        xt = np.linspace(x0 - 0.1, x0 + 0.1, 20)
        dym1 = dgd(x0) * (xt - x0) + gd(x0)
        return xt, dym1

    cmap = plt.cm.get_cmap("jet")

    epochs = 10
    theta_1 = 0.5
    cacheLoss = []
    learnRate = 0.003
    plot_fit(axes[2], 0.8, ls="solid")
    for i in range(epochs):
        predictions = mdlf(xm, theta_1)
        theta_1 = theta_1 - learnRate * (predictions - ym).sum()
        cacheLoss.append(theta_1)
        axes[1].plot(*get_tangent(theta_1), color=cmap(i / 10), ls="dashed", alpha=0.6)
        axes[2].plot(
            np.linspace(0, 20, 100), mdlf(np.linspace(0, 20, 100), theta_1), ls="dashed", alpha=0.6, c=cmap(i / 10)
        )
