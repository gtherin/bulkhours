import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def plot_brownian_sample(seed=None, sample=5000, csample=30):

    """
    https://ipython-books.github.io/133-simulating-a-brownian-motion/

    """

    if seed:
        np.random.seed(seed)

    x = np.cumsum(np.random.randn(sample - 1))
    y = np.cumsum(np.random.randn(sample - 1))
    x = np.concatenate((np.array([0]), x), axis=None)
    y = np.concatenate((np.array([0]), y), axis=None)

    # We add 10 intermediary points between two successive points. We interpolate x and y.
    k = 10
    x2 = np.interp(np.arange(sample * k), np.arange(sample) * k, x)
    y2 = np.interp(np.arange(sample * k), np.arange(sample) * k, y)

    _, axes = plt.subplots(1, 2, figsize=(12, 4))

    ax = axes[0]
    cmap = plt.cm.get_cmap("jet")
    ax.scatter(x2, y2, c=range(sample * k), linewidths=0, marker="o", s=3, cmap=cmap)

    ax.add_patch(plt.Circle((x2[0], y2[0]), 3, color=cmap(0.01), fill=True, alpha=0.5, zorder=100))
    ax.annotate(
        "Start", (x2[0], y2[0]), color=cmap(0.99), weight="bold", fontsize=20, ha="center", va="center", zorder=2000
    )

    ax.add_patch(plt.Circle((x2[-1], y2[-1]), 3, color=cmap(0.99), fill=True, alpha=0.5, zorder=100))
    ax.annotate(
        "End", (x2[-1], y2[-1]), color=cmap(0.01), weight="bold", fontsize=20, ha="center", va="center", zorder=2000
    )
    ylim = ax.get_ylim()

    # ax.axis('equal')
    axes[0].set_axis_off()
    axes[0].set_title("Trajectory of the particle (X_pos x Y_pos)")

    xs = pd.Series(y)
    d = 0
    for i in np.linspace(0, 1, csample):
        u = int(i * sample)
        xs[d:u].plot(ax=axes[1], c=cmap(i))
        d = u
    axes[1].set_axis_off()
    axes[1].set_title("Y position time series (Y_pos x time)")
    axes[1].set_ylim(ylim)
