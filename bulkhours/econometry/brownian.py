import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


class Brown:
    def __init__(self, seed=None, sample=5000, k=10, cmap="jet") -> None:
        if seed:
            np.random.seed(seed)

        x = np.cumsum(np.random.randn(sample - 1))
        y = np.cumsum(np.random.randn(sample - 1))
        self.x = np.concatenate((np.array([0]), x), axis=None)
        self.y = np.concatenate((np.array([0]), y), axis=None)
        self.k, self.cmap, self.sample = k, cmap, sample
        self.ylim = None

    def get_int_x(self):
        # We add 10 intermediary points between two successive points. We interpolate x and y.
        return np.interp(np.arange(self.sample * self.k), np.arange(self.sample) * self.k, self.x)

    def get_int_y(self, factor=1.0):
        return np.interp(np.arange(self.sample * self.k), np.arange(self.sample) * self.k, self.y + factor)

    def get_2d_plot(self, ax, csample=30, cmap=None, factor=1.0):
        cmap = plt.cm.get_cmap(cmap if cmap else self.cmap)
        ax.scatter(
            self.get_int_x(),
            self.get_int_y(factor),
            c=range(self.sample * self.k),
            linewidths=0,
            marker="o",
            s=3,
            cmap=cmap,
        )

        if self.sample > 3 * csample:
            # ax.add_patch(plt.Circle((x2[0], y2[0]), 3, color=cmap(0.01), fill=True, alpha=0.5, zorder=100))
            ax.annotate(
                "Start",
                (self.get_int_x()[0], self.get_int_y(factor)[0]),
                color=cmap(0.99),
                weight="bold",
                fontsize=20,
                ha="center",
                va="center",
                zorder=2000,
            )

            # ax.add_patch(plt.Circle((x2[-1], y2[-1]), 3, color=cmap(0.99), fill=True, alpha=0.5, zorder=100))
            ax.annotate(
                "End",
                (self.get_int_x()[-1], self.get_int_y(factor)[-1]),
                color=cmap(0.01),
                weight="bold",
                fontsize=20,
                ha="center",
                va="center",
                zorder=2000,
            )
        self.ylim = ax.get_ylim()

        # ax.axis('equal')
        ax.set_axis_off()
        ax.set_title("Trajectory of the particle\n(X_pos versus Y_pos)")

        return ax

    def get_1d_plot(self, ax, csample=30, cmap=None, factor=1.0):
        cmap = plt.cm.get_cmap(cmap if cmap else self.cmap)
        xs = pd.Series(self.y) + factor
        d = 0
        if self.sample > 10 * csample:
            for i in np.linspace(0, 1, csample):
                u = int(i * self.sample)
                xs[d:u].plot(ax=ax, c=cmap(i))
                d = u
        else:
            xs.plot(ax=ax, c="grey")
        ax.set_axis_off()
        ax.set_title("Y position time-series\n(Y_pos versus time)")
        if self.ylim:
            ax.set_ylim(self.ylim)

    def get_hist(self, ax, cmap=None, cval=0.38):
        import matplotlib

        cmap = plt.cm.get_cmap(cmap if cmap else self.cmap)

        xs = pd.concat([pd.Series(self.y).diff(), pd.Series(self.x).diff()])
        ax.hist(xs, bins=50, color=matplotlib.colors.rgb2hex(cmap(cval)))
        ax.set_axis_off()
        ax.set_title("X,Y move histogram\n(Y_pos_diff)")


def plot_brownian_sample(seed=None, sample=5000, csample=30):

    """
    https://ipython-books.github.io/133-simulating-a-brownian-motion/

    """

    brown = Brown(seed=seed, sample=sample, csample=csample)

    _, axes = plt.subplots(1, 3, figsize=(15, 4))

    brown.get_2d_plot(axes[0], csample=csample)
    brown.get_1d_plot(axes[1], csample=csample)
    brown.get_hist(axes[2])
