import numpy as np
import pandas as pd
import scipy as sp
import matplotlib.pyplot as plt


def p2(x, theta0, theta1, theta2):
    return theta0 + theta1 * x + theta2 * x * x


def dp2(x, theta0, theta1, theta2):
    return theta1 + theta2 * 2 * x


def get_grad(seed=1, epochs=10, learnRate=0.003, theta0=0.04, theta1=0.8, theta2=-0.02, sample_size=15, noise=1.0):
    np.random.seed(seed)
    ym = p2(xm := np.linspace(0, 20, sample_size), theta0, theta1, theta2) + noise * sp.stats.norm().rvs(sample_size)

    fig, axes = plt.subplots(1, 3, figsize=(15, 4))

    def plot_fit(ax, theta0, theta1, theta2, c=None, ls="dotted"):
        ax.scatter(xm, ym, marker="X", s=60, zorder=100)
        ax.plot(np.linspace(0, 20, 100), p2(np.linspace(0, 20, 100), theta0, theta1, theta2), ls=ls, alpha=0.8, c=c)
        for args in zip(xm, ym, p2(xm, theta0, theta1, theta2)):
            c = "red" if args[1] < args[2] else "green"
            ax.vlines(*args, color=c, alpha=0.5, zorder=50)

    plot_fit(axes[0], theta0, theta1, theta2)

    ax = axes[1]
    ex = np.linspace(0.55, 0.95, 20)
    dex = [np.mean((ym - p2(xm, theta0, e, theta2)) ** 2) for e in ex]

    ax.plot(ex, dex)
    cfit = np.polynomial.polynomial.polyfit(ex, dex, 2, full=True)[0]

    ax.plot(ex, p2(ex, *cfit), alpha=0.5)

    def get_tangent(x0):
        xt = np.linspace(x0 - 0.1, x0 + 0.1, 20)
        dym1 = dp2(x0, *cfit) * (xt - x0) + p2(x0, *cfit)
        return xt, dym1

    cmap = plt.get_cmap("jet")

    theta_1 = 0.5
    plot_fit(axes[2], theta0, theta1, theta2, ls="solid")
    theta, r2 = [], []
    for i in range(epochs):
        predictions = p2(xm, theta0, theta_1, theta2)
        theta_1 = theta_1 - learnRate * (predictions - ym).sum()
        axes[1].plot(*get_tangent(theta_1), color=cmap(i / 10), ls="dashed", alpha=0.6)
        xi = np.linspace(0, 20, 100)
        axes[2].plot(xi, p2(xi, theta0, theta_1, theta2), ls="dashed", alpha=0.6, c=cmap(i / 10))

        SS_res = ((ym - p2(xm, theta0, theta_1, theta2)) ** 2).sum()
        SS_tot = ((ym - ym.mean()) ** 2).sum()
        theta.append(theta_1)
        r2.append(1.0 - SS_res / SS_tot)

    if 0:
        ax = axes[1]
        plt.sca(ax)
        right_inset_ax = fig.add_axes([0.48, 0.64, 0.15, 0.2])
        right_inset_ax.plot(theta, r2, "o")
        right_inset_ax.set(title="r^2", xticks=[])  # , yticks=[])
