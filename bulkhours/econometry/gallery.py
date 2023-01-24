import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import scipy as sp
import statsmodels.api as sm
import matplotlib
from .brownian import Brown


def plot1(ax):

    pdf = sp.stats.skewnorm(a := 4, 0, 1.0)
    mean, var, skew, kurt = pdf.stats(moments="mvsk")
    pearson_skew = 3 * (pdf.mean() - pdf.median()) / pdf.std()
    print(mean, pdf.std(), skew, kurt, pdf.median())

    xmin, xmax = pdf.ppf(0.001), pdf.ppf(0.95)
    x = np.linspace(xmin, xmax, 100)
    ax.plot(x, pdf.pdf(x), "k-", lw=2, label="pdf")
    ax.vlines(x=pdf.median(), ymin=0, ymax=pdf.pdf(pdf.median()), color="r")
    ax.vlines(x=pdf.mean(), ymin=0, ymax=pdf.pdf(pdf.mean()), color="b")
    # ax.vlines(x=pearson_skew, ymin=0, ymax=pdf.pdf(pearson_skew), color="g")

    ax.vlines(x=kurt, ymin=0, ymax=pdf.pdf(kurt), color="pink")

    ax.hlines(y=0.4, xmin=pdf.mean(), xmax=pdf.median(), color="g")
    ax.hlines(y=0.2, xmin=xmin, xmax=xmax, color="g")

    if 0:
        cmap = plt.cm.get_cmap("jet")
        ax.annotate(
            "Start",
            (x2[0], y2[0]),
            color=cmap(0.99),
            weight="bold",
            fontsize=20,
            ha="center",
            va="center",
            zorder=2000,
        )

        ax.annotate(
            "End",
            (x2[-1], y2[-1]),
            color=cmap(0.01),
            weight="bold",
            fontsize=20,
            ha="center",
            va="center",
            zorder=2000,
        )

    ax.set_axis_off()
    # ax.set_title("X,Y move histogram\n(Y_pos_diff)")


def plot2(ax, a=4):

    # https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.skewnorm.html
    # mean, var, skew, kurt = sp.stats.skewnorm.stats(a, moments="mvsk")
    # print(mean, var, skew, kurt)

    x = np.linspace(sp.stats.skewnorm.ppf(0.01, a), sp.stats.skewnorm.ppf(0.99, a), 100)
    ax.plot(x, sp.stats.skewnorm.pdf(x, a), "r-", lw=5, alpha=0.6, label="skewnorm pdf")

    rv = sp.stats.skewnorm(a)
    ax.plot(x, rv.pdf(x), "k-", lw=2, label="frozen pdf")

    r = sp.stats.skewnorm.rvs(a, size=1000)
    ax.hist(r, density=True, bins="auto", histtype="stepfilled", alpha=0.2)
    # ax.set_xlim([x[0], x[-1]])
    plt.legend(loc="best", frameon=False)
    ax.set_axis_off()


def plot3(ax):
    # https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.skewnorm.html
    a = 4
    q = 0.00001
    x = np.linspace(sp.stats.skewnorm.ppf(q, a), sp.stats.skewnorm.ppf(1 - q, a), 100)
    ax.plot(x, sp.stats.skewnorm.pdf(x, a), "r", lw=5, alpha=0.6, label="Positive Skewness")

    a = -4
    x = np.linspace(sp.stats.skewnorm.ppf(q, a), sp.stats.skewnorm.ppf(1 - q, a), 100)
    ax.plot(x, sp.stats.skewnorm.pdf(x, a), lw=5, alpha=0.6, label="Negative Skewness")

    a = 0
    x = np.linspace(sp.stats.skewnorm.ppf(q, a), sp.stats.skewnorm.ppf(1 - q, a), 100)
    ax.plot(x, sp.stats.skewnorm.pdf(x, a), lw=5, alpha=0.6, label="Null Skewness")

    ax.legend(loc=2, frameon=False)
    ax.set_axis_off()


def get_x(pdf, q=0.01):
    return np.linspace(pdf.ppf(q), pdf.ppf(1 - q), 100)


def plot_mean_median(ax, pdf, fac=1.2):
    # Accentuate diff between mean and median
    cartoon_median = pdf.median() + fac * (pdf.median() - pdf.mean())
    ax.vlines(x=pdf.mean(), ymin=0, ymax=pdf.pdf(pdf.mean()), color="#C70039", ls="dashed", label=" $\mu$: mean")
    ax.vlines(
        x=cartoon_median, ymin=0, ymax=pdf.pdf(cartoon_median), color="#581845", ls="dotted", label=r"$\nu$: median"
    )


def plot_skew(ax, a, label, legend=True):
    # https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.skewnorm.html

    pdf = sp.stats.skewnorm(a := a)

    ax.plot(get_x(pdf), pdf.pdf(get_x(pdf)), "r", lw=5, alpha=0.6)

    plot_mean_median(ax, pdf, fac=1.2)

    if legend:
        ax.legend()

    set_title(ax, label)


def set_title(ax, label):
    ax.set_axis_off()
    ax.set_title(label)


def plot_sigma(ax, x=0, y=0.09, dx=0.55, width=0.007, head_width=0.03, head_length=0.3):
    opts = dict(color="#FF5733", alpha=0.9, x=x, dy=0, y=y)
    opts.update(dict(shape="full", width=width, head_width=head_width, head_length=head_length))
    ax.arrow(dx=dx, label=r"$\propto \sigma:$ std", **opts)
    ax.arrow(dx=-dx, **opts)


def plot_gallery():

    # "swimming": "#581845",
    # "cycling": "#C70039",
    # "running": "#FF5733",
    # "axis": "#4F77AA",

    fig, axes = plt.subplots(3, 3, figsize=(15, 10))

    ax = axes[0][0]
    plot_skew(ax, 4, "Positive skew\nmean < median", legend=True)
    # pdf1 = sp.stats.skewnorm(a=4)
    # ax.plot(get_x(pdf1), pdf1.pdf(get_x(pdf1)), "r", lw=5, alpha=0.6)
    plot_sigma(ax, dx=0.75, x=0.75, y=0.2, width=0.0147, head_width=0.03, head_length=0.1)
    ax.legend(loc=1)
    set_title(ax, "Unimodal distrib")

    ax = axes[0][1]
    pdf1, pdf2 = sp.stats.norm(0, 0.6), sp.stats.norm(0, 4)
    x = np.linspace(-3, 3, 100)
    data = 0.5 * pdf1.pdf(x) + 0.004 * x + 0.025

    ax.plot(x, data, lw=5, alpha=0.6, c="r")
    ax.plot(x, 0.004 * x + 0.025, "#581845", lw=2, alpha=0.4, ls="dotted", label=r"$\propto \zeta:$ skew")
    ax.plot(x, 0.5 * pdf1.pdf(x), lw=2, alpha=0.6, c="grey", ls="dashed")
    ax.fill_between(x, 0.5 * pdf1.pdf(x), data, label=r"$\propto \kappa:$ kurtosis", alpha=0.4)
    plot_sigma(ax, dx=0.59)

    ax.legend(loc=2)
    set_title(ax, "Skew, Kurtosis")

    ax = axes[0][2]
    pdf1 = sp.stats.skewnorm(a=4)
    pdf2 = sp.stats.norm(2, 0.3)
    ax.plot(get_x(pdf1), 0.5 * pdf1.pdf(get_x(pdf1)) + 0.5 * pdf2.pdf(get_x(pdf1)), "r", lw=5, alpha=0.6)
    ax.plot(get_x(pdf1), 0.5 * pdf1.pdf(get_x(pdf1)), "#581845", lw=2, alpha=0.4, ls="dotted")
    ax.plot(get_x(pdf1), 0.59 * sp.stats.norm(1.97, 0.33).pdf(get_x(pdf1)), "#C70039", lw=2, alpha=0.4, ls="dashed")
    set_title(ax, "Bimodal distrib")

    plot_skew(axes[1][0], -4, "Negative skew\nmean < median")
    plot_skew(axes[1][1], 0, "No skew\nmean = median", legend=False)
    plot_skew(axes[1][2], 4, "Positive skew\nmean > median", legend=False)

    ax, nob = axes[2][0], 100
    x = np.linspace(-0.9, 3.5, nob)
    pdf = sp.stats.skewnorm(a=4)
    ax.plot(x, pdf.pdf(x), "r", lw=5, alpha=0.6)
    plot_mean_median(ax, pdf, fac=0.0)

    x = np.linspace(-0.9, pdf.median(), nob)
    ax.fill_between(x, 0.0 * x, pdf.pdf(x), label="", alpha=0.2)

    x = np.linspace(pdf.median(), 3.5, nob)
    ax.fill_between(x, 0.0 * x, pdf.pdf(x), label="", alpha=0.2, color="r")

    ax.annotate(
        "50%",
        (0.35, 0.2),
        color="#C70039",
        weight="bold",
        fontsize=20,
        ha="center",
        va="center",
        rotation=90,
    )
    ax.annotate(
        "50%",
        (1.08, 0.18),
        color="#581845",
        weight="bold",
        fontsize=20,
        ha="center",
        va="center",
        rotation=-90,
    )

    ax.legend(loc=1)
    set_title(ax, "Vizualizing the median")


def plot_celestine(seed=42, sample=1000):

    fig, axes = plt.subplots(3, 3, figsize=(15, 10))

    def plot6(ax, col, palette="jet"):
        xs = np.random.randn(sample)
        cmap = plt.cm.get_cmap(palette)
        ax.hist(xs, bins=50, color=matplotlib.colors.rgb2hex(cmap(col)))
        ax.set_axis_off()
        ax.set_title("X,Y move histogram\n(Y_pos_diff)")

    brown = Brown(seed=seed, sample=sample)

    brown.get_1d_plot(axes[0][0], cmap="twilight")
    brown.get_1d_plot(axes[0][1], cmap="gnuplot2")
    brown.get_1d_plot(axes[0][2], cmap="cool")

    brown.get_2d_plot(axes[1][0], cmap="prism")
    brown.get_2d_plot(axes[1][1], cmap="jet")

    brown.get_2d_plot(axes[1][2], cmap="magma")

    plot6(axes[2][0], 0.2, palette="cool")
    plot6(axes[2][1], 0.6, palette="cool")
    plot6(axes[2][2], 0.0, palette="cool")


def plot_stationary():

    fig, axes = plt.subplots(1, 3, figsize=(15, 3))

    ax, nob = axes[0], 50

    np.random.seed(42)
    data = pd.Series(np.random.randn(nob), index=np.linspace(0, 1, nob))

    ax.plot(data.index, data, lw=1, alpha=0.9, label=r"$x(t)$")
    ax.plot(data.index, np.zeros(nob), lw=1, alpha=0.9, label=r"$\mu(t)=\mu$")
    ax.fill_between(data.index, -2, 2, alpha=0.2, label=r"$\sigma(t)=\sigma$")

    ax.set_ylim([-5, 15])

    ax.legend()
    set_title(ax, "Stationary mean\nStationary variance")

    ax, nob = axes[1], 50

    np.random.seed(42)
    data = pd.Series(
        np.concatenate([np.ones(int(0.6 * nob)), -0.4 * np.ones(int(0.4 * nob))], axis=0), index=np.linspace(0, 1, nob)
    )
    data = data.cumsum().ewm(3).mean() + 200 * np.cumsum(np.random.randn(nob))

    datas = data.rolling(8).mean().shift(-3).fillna(data.ewm(4).mean())
    datap = datas + 1.9 * data.std() / np.sqrt(nob)
    datam = datas - 1.9 * data.std() / np.sqrt(nob)

    ax.plot(data.index, data, lw=1, alpha=0.9, label=r"$x(t)$")
    ax.plot(data.index, datas, lw=1, alpha=0.9, label=r"$\mu(t)$")
    ax.fill_between(data.index, datam, datap, alpha=0.2, label=r"$\sigma(t)=\sigma$")

    ax.legend()
    set_title(ax, "Non-stationary mean\nStationary variance")
    ax, nob = axes[2], 50

    np.random.seed(42)
    fac = np.linspace(10, 1, nob)
    data = pd.Series(fac * np.random.randn(nob), index=np.linspace(0, 1, nob))

    ax.plot(data.index, data, lw=1, alpha=0.9, label=r"$x(t)$")
    ax.plot(data.index, np.zeros(nob), lw=1, alpha=0.9, label=r"$\mu(t)=\mu$")
    ax.fill_between(data.index, -1.5 * fac, 1.5 * fac, alpha=0.2, label=r"$\sigma(t)$")

    ax.set_ylim([-30, 30])

    ax.legend(ncol=3)
    set_title(ax, "Stationary mean\nNon-stationary variance")
