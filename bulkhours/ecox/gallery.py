import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import scipy as sp
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
        cmap = plt.get_cmap("jet")
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


def get_x(pdf, q=0.01):
    return np.linspace(pdf.ppf(q), pdf.ppf(1 - q), 100)


def plot_mean_median(ax, pdf, fac=1.2, mean=True):
    # Accentuate diff between mean and median
    cartoon_median = pdf.median() + fac * (pdf.median() - pdf.mean())
    if mean:
        ax.vlines(x=pdf.mean(), ymin=0, ymax=pdf.pdf(pdf.mean()), color=r"#C70039", ls=r"dashed", label=r" $\mu$: mean")
    ax.vlines(
        x=cartoon_median, ymin=0, ymax=pdf.pdf(cartoon_median), color="#581845", ls="dotted", label=r"$\nu$: median"
    )


def plot_skew(ax, a, label, legend=True, mean=True):
    # https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.skewnorm.html

    pdf = sp.stats.skewnorm(a := a)
    ax.plot(get_x(pdf), pdf.pdf(get_x(pdf)), "r", lw=5, alpha=0.6)
    plot_mean_median(ax, pdf, fac=1.2, mean=mean)

    if legend:
        ax.legend()

    set_title(ax, label)


def set_title(ax, label, yvisible=False):
    if yvisible:
        ax.get_yaxis().set_visible(False)
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.spines["left"].set_visible(False)
    else:
        ax.set_axis_off()
    ax.set_title(label)


def plot_sigma(ax, x=0, y=0.09, dx=0.55, width=0.007, head_width=0.03, head_length=0.3):
    from matplotlib.lines import Line2D

    opts = dict(color="#FF5733", alpha=0.9, x=x, dy=0, y=y)
    opts.update(dict(shape="full", width=width, head_width=head_width, head_length=head_length))
    ax.arrow(dx=dx, **opts)
    ax.arrow(dx=-dx, **opts)

    h, l = ax.get_legend_handles_labels()
    h.append(Line2D([0], [0], color="#FF5733", lw=4, label="Line"))
    l.append(r"$\approx \sigma:$ std")
    ax.legend(h, l, loc=2)
    return ax


def plot_gallery_r1(axes=None):
    if axes is None:
        fig, axes = plt.subplots(1, 3, figsize=(15, 4))
        fig.subplots_adjust(wspace=0.01, hspace=0.3)

    ax = axes[0]
    pdf = sp.stats.skewnorm(a=1)
    x_c = get_x(pdf, q=0.001)
    x_d = np.linspace(-2, 2, 6)

    y_d = pdf.cdf(x_d)
    y_d = y_d - np.array([0] + list(y_d[:-1]))

    ax.plot(x_c, pdf.pdf(x_c), "r", lw=5, alpha=0.6, label="Continuous pdf")
    ax.bar(x_d, y_d * 1.2, lw=5, alpha=0.6, width=0.1, label="Discrete pdf")
    ax.plot(x_c, pdf.cdf(x_c), "#C70039", lw=5, alpha=0.6, label="Continuous cdf")
    ax.legend(loc=2)
    ax.set_ylim([0.0, 1.0])
    set_title(ax, "Density functions")

    ax = axes[1]
    plot_skew(ax, 4, "Positive skew\nmean < median", legend=False)
    set_title(ax, "Unimodal distrib")

    ax = axes[2]
    pdf1 = sp.stats.skewnorm(a=4)
    pdf2 = sp.stats.norm(2, 0.3)
    ax.plot(get_x(pdf1), 0.5 * pdf1.pdf(get_x(pdf1)) + 0.5 * pdf2.pdf(get_x(pdf1)), "r", lw=5, alpha=0.6)
    ax.plot(get_x(pdf1), 0.5 * pdf1.pdf(get_x(pdf1)), "#581845", lw=2, alpha=0.4, ls="dotted")
    ax.plot(get_x(pdf1), 0.59 * sp.stats.norm(1.97, 0.33).pdf(get_x(pdf1)), "#C70039", lw=2, alpha=0.4, ls="dashed")
    set_title(ax, "Bimodal distrib")


def plot_gallery_skews(axes=None):
    if axes is None:
        fig, axes = plt.subplots(1, 3, figsize=(15, 4))
        fig.subplots_adjust(wspace=0.01, hspace=0.3)

    plot_skew(axes[0], -4, "Negative skew\nmean < median")
    plot_skew(axes[1], 0, "No skew\nmean = median", legend=False)
    plot_skew(axes[2], 4, "Positive skew\nmean > median", legend=False)


def annotate(ax, label, x, y, c="#C70039", r=0):
    opts = dict(weight="bold", fontsize=20, ha="center", va="center")
    ax.annotate(label, (x, y), color=c, rotation=r, **opts)


def plot_ci(ax=None, nob=100):

    if ax is None:
        fig, ax = plt.subplots(1, 3, figsize=(6, 4))
        fig.subplots_adjust(wspace=0.01, hspace=0.3)

    x = np.linspace(-4, 4, nob)
    pdf = sp.stats.norm()
    ax.plot(x, pdf.pdf(x), "r", lw=5, alpha=0.6)

    x = np.linspace(-1, 1, nob)
    ax.fill_between(x, 0.0 * x, pdf.pdf(x), label="", alpha=0.2)

    x = np.linspace(-2, 2, nob)
    ax.fill_between(x, 0.0 * x, pdf.pdf(x), label="", alpha=0.2)

    x = np.linspace(-3, 3, nob)
    ax.fill_between(x, 0.0 * x, pdf.pdf(x), label="", alpha=0.2)

    annotate(ax, r"$1\sigma=68.27\%$", -2.8, 0.40, c=r"#C70039")
    annotate(ax, r"$2\sigma=95.45\%$", -2.8, 0.35, c=r"#581845")
    annotate(ax, r"$3\sigma=99.73\%$", -2.8, 0.3, c=r"#FF5733")

    annotate(ax, r"$1.96\sigma=95\%$", 2.8, 0.35, c=r"#581845")
    annotate(ax, r"$2.58\sigma=99\%$", 2.8, 0.3, c=r"#FF5733")

    set_title(ax, "Norm: Confidence Intervals", yvisible=True)
    ax.set_xticks(
        [-3, -2, -1, 1, 2, 3],
        ["-$3\sigma$", r"$-2\sigma$", r"$-1\sigma$", r"$1\sigma$", r"$2\sigma$", r"$3\sigma$"],
    )

def plot_gallery_r3(axes=None):
    if axes is None:
        fig, axes = plt.subplots(1, 3, figsize=(15, 4))
        fig.subplots_adjust(wspace=0.01, hspace=0.3)

    ax, nob = axes[0], 100
    x = np.linspace(-0.9, 3.5, nob)
    pdf = sp.stats.skewnorm(a=4)
    ax.plot(x, pdf.pdf(x), "r", lw=5, alpha=0.6)
    plot_mean_median(ax, pdf, fac=0.0, mean=False)

    x = np.linspace(-0.9, pdf.median(), nob)
    ax.fill_between(x, 0.0 * x, pdf.pdf(x), label="", alpha=0.2)

    x = np.linspace(pdf.median(), 3.5, nob)
    ax.fill_between(x, 0.0 * x, pdf.pdf(x), label="", alpha=0.2, color="r")

    annotate(ax, "50%", 0.35, 0.2, c="#C70039", r=90)
    annotate(ax, "50%", 1.08, 0.18, c="#581845", r=90)

    ax.legend(loc=1)
    set_title(ax, "Vizualizing the median")

    ax = axes[1]
    pdf1, x = sp.stats.norm(0, 0.6), np.linspace(-3, 3, 100)
    data = 0.5 * pdf1.pdf(x) + 0.004 * x + 0.025

    ax.plot(x, data, lw=5, alpha=0.6, c="r")
    ax.plot(x, 0.004 * x + 0.025, "#581845", lw=2, alpha=0.4, ls="dotted", label=r"$\approx \zeta:$ skew")
    ax.plot(x, 0.5 * pdf1.pdf(x), lw=2, alpha=0.6, c="grey", ls="dashed")
    ax.fill_between(x, 0.5 * pdf1.pdf(x), data, label=r"$\approx \kappa:$ kurtosis", alpha=0.4)
    ax = plot_sigma(ax, dx=0.59)

    set_title(ax, "Skew, Kurtosis")

    # Plot confidence interval
    plot_ci(ax=axes[2])


def plot_celestine(seed=42, sample=1000):
    fig, axes = plt.subplots(3, 3, figsize=(15, 10))
    fig.subplots_adjust(wspace=0.01, hspace=0.3)

    def plot6(ax, col, palette="jet"):
        xs = np.random.randn(sample)
        cmap = plt.get_cmap(palette)
        ax.hist(xs, bins=50, color=matplotlib.colors.rgb2hex(cmap(col)))
        ax.set_axis_off()
        ax.set_title("X,Y move histogram\n(Y_pos_diff)")

    brown = Brown(seed=seed, sample=sample)

    brown.get_1d_plot(axes[0][0], cmap="gnuplot2", factor=60)
    brown.get_1d_plot(axes[0][0], cmap="twilight", factor=90)
    brown.get_1d_plot(axes[0][0], cmap="cool", factor=80)
    brown.get_1d_plot(axes[0][0], cmap="magma", factor=70)

    brown.get_1d_plot(axes[0][1], cmap="gnuplot2")
    brown.get_1d_plot(axes[0][2], cmap="cool")

    brown.get_2d_plot(axes[1][0], cmap="gist_rainbow")
    brown.get_2d_plot(axes[1][1], cmap="plasma")
    brown.get_2d_plot(axes[1][2], cmap="jet")

    plot6(axes[2][0], 0.2, palette="plasma")
    plot6(axes[2][1], 0.6, palette="cool")
    plot6(axes[2][2], 0.0, palette="cool")


def plot_stationary():
    fig, axes = plt.subplots(1, 3, figsize=(15, 3))
    fig.subplots_adjust(wspace=0.01, hspace=0.01)

    ax, nob = axes[0], 50

    np.random.seed(42)
    data = pd.Series(np.random.randn(nob), index=np.linspace(0, 1, nob))

    ax.plot(data.index, data, lw=1, alpha=0.9, label=r"$y(t)$")
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

    ax.plot(data.index, data, lw=1, alpha=0.9, label=r"$y(t)$")
    ax.plot(data.index, datas, lw=1, alpha=0.9, label=r"$\mu(t)$")
    ax.fill_between(data.index, datam, datap, alpha=0.2, label=r"$\sigma(t)=\sigma$")

    ax.legend()
    set_title(ax, "Non-stationary mean\nStationary variance")
    ax, nob = axes[2], 50

    np.random.seed(42)
    fac = np.linspace(10, 1, nob)
    data = pd.Series(fac * np.random.randn(nob), index=np.linspace(0, 1, nob))

    ax.plot(data.index, data, lw=1, alpha=0.9, label=r"$y(t)$")
    ax.plot(data.index, np.zeros(nob), lw=1, alpha=0.9, label=r"$\mu(t)=\mu$")
    ax.fill_between(data.index, -1.5 * fac, 1.5 * fac, alpha=0.2, label=r"$\sigma(t)$")

    ax.set_ylim([-30, 30])

    ax.legend(ncol=3)
    set_title(ax, "Stationary mean\nNon-stationary variance")
