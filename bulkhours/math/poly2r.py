import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from fractions import Fraction
from .. import core


def md(data, style="raw"):
    import IPython

    if style == "header":
        data = r"<font size='+2'>%s</font>" % (data)

    IPython.display.display(IPython.display.Markdown(r"%s" % data))


colors = {
    "is_in": core.c.caliases["blue"],
    "is_out": core.c.caliases["red"],
    "is_neutral": core.c.caliases["purple"],
    "secondary": core.c.caliases["orange"],
}


class Poly2dr:
    def __init__(self, a, b, c, numbers="fraction", constraint="=0"):
        self.a, self.b, self.c, self.numbers, self.constraint = a, b, c, numbers, constraint

        if a == 0:
            raise ValueError("a cannot be zero, otherwise it is not a second degree polynomial")

        # Calculate basic quantities
        self.alpha, self.beta, self.delta = -b / 2 / a, self.f(-b / 2 / a), b**2 - 4 * a * c
        self.x1, self.x2 = self.alpha - np.sqrt(np.abs(self.beta / a)), self.alpha + np.sqrt(
            np.abs(self.beta / self.a)
        )

    def f(self, x):
        return self.a * x**2 + self.b * x + self.c

    def get_basic(self):
        return r"""${}x^2{}x{}{}$""".format(self.sa, self.sb, self.sc, self.sconstraint)

    def get_canonical(self):
        if self.delta == 0:
            return r"""${}(x{})^2{}$""".format(self.sa, self.msalpha, self.sconstraint)
        else:
            return r"""${}(x{})^2{}{}$""".format(self.sa, self.msalpha, self.sbeta, self.sconstraint)

    def get_factorized(self):
        if self.delta == 0:
            return r"""$(x{})^2{}$""".format(self.msx1, self.sconstraint)
        else:
            return r"""$(x{})(x{}){}$""".format(self.msx1, self.msx2, self.sconstraint)

    def get_various_forms(self):
        md(f"Forme standardisée: %s" % (self.get_basic()), style="header")
        md(f"Forme canonique: %s" % (self.get_canonical()), style="header")
        if self.delta > 0:
            md(f"Forme factorisée: %s" % self.get_factorized(), style="header")

    def get_sign_table(self):
        s = "+" if self.a > 0 else "-"
        ms = "-" if self.a > 0 else "+"

        text = f"""### Tableau de signes:\n"""

        labels = "|$x$|$-\infty$| |"
        signs = "|$f(x)$| |"

        if self.delta >= 0:
            labels += f"${self.sx1}$| |"
            signs += f"{s}|0|"

        if self.delta > 0:
            labels += f"${self.sx2}$| |"
            signs += f"{ms}|0|"

        labels += "$+\infty$|"
        signs += f"{s}| |"

        separators = "---".join(["|"] * labels.count("|"))

        md(f"{text}\n{labels}\n{separators}\n{signs}\n")

    def get_xrange(self):
        minx, maxx = self.alpha - 2 * np.sqrt(np.abs(self.beta / self.a)), self.alpha + 2 * np.sqrt(
            np.abs(self.beta / self.a)
        )
        if self.delta == 0:
            minx, maxx = self.x1 - 10 * np.abs(self.x1), self.x1 + 10 * np.abs(self.x1)
        return minx, maxx

    def get_solution1(self):
        self.get_various_forms()
        self.get_sign_table()
        self.get_graph()

    def get_solution2(self, x2=None, y2=None):
        ax = self.get_graph(show_solutions=False)
        minx, maxx = self.get_xrange()
        x = np.linspace(minx, maxx, 100)
        df = pd.DataFrame([np.linspace(minx, maxx, 100)], index=["x"]).T
        df["y"] = self.f(x)
        ymin, ymax = ax.get_ylim()

        # By default, no solution on the axis
        tail_color, middle_color = colors["is_out"], colors["is_out"]
        from matplotlib.lines import Line2D

        gleg, lleg = None, None

        # Tails point are solutions
        if (">" in self.constraint and self.a > 0) or ("<" in self.constraint and self.a < 0):
            tail_color, middle_color = colors["is_in"], colors["is_out"]
            gleg, lleg = Line2D([0], [0], color=colors["is_in"]), "$x<%s$ ou $x>%s$" % (self.sx1, self.sx2)

        # Center points are solutions
        if (">" in self.constraint and self.a < 0) or ("<" in self.constraint and self.a > 0):
            tail_color, middle_color = colors["is_out"], colors["is_in"]
            gleg, lleg = Line2D([0], [0], color=colors["is_in"]), "$x \> %s$ et $x < %s$" % (self.sx1, self.sx2)

        ax.plot(df[df["x"] < self.x1]["x"], df[df["x"] < self.x1]["y"] * 0, color=tail_color)
        ax.plot(df[self.a * df["y"] < 0]["x"], df[self.a * df["y"] < 0]["y"] * 0, color=middle_color)
        ax.plot(df[df["x"] > self.x2]["x"], df[df["x"] > self.x2]["y"] * 0, color=tail_color)

        if "=" in self.constraint:
            ax.plot([self.x1], [0], "o", markersize=20, color=colors["is_in"])
            ax.plot([self.x2], [0], "o", markersize=20, color=colors["is_in"])
            if gleg is None:
                gleg, lleg = Line2D([], [], color=colors["is_in"]), "$x=%s$ ou $x=%s$" % (self.sx1, self.sx2)
            else:
                gleg, lleg = Line2D([0], [0], color=colors["is_in"], marker="o", markersize=20), lleg.replace(
                    "<", " <= "
                ).replace(">", " >= ")
        else:
            ax.plot([self.x1], [0], "X", markersize=15, color=colors["is_out"])
            ax.plot([self.x2], [0], "X", markersize=15, color=colors["is_out"])

        ax.set_ylim(ymin, ymax)
        ax.set_xlim(minx, maxx)
        # self.get_sign_table()
        if gleg is not None:
            ax.legend([gleg], [lleg], loc="upper left")

        if y2 is not None:
            ax.plot(x2, y2, color=colors["secondary"])

    def get_graph(self, show_solutions=True):
        minx, maxx = self.get_xrange()

        x = np.linspace(minx, maxx, 100)
        df = pd.DataFrame([np.linspace(minx, maxx, 100)], index=["x"]).T
        df["y"] = self.f(x)

        fig = plt.figure()
        ax = fig.add_subplot(1, 1, 1)

        ax.axhline(y=0, color=colors["secondary"], alpha=0.6)
        ax.axvline(x=0, color=colors["secondary"], alpha=0.6)
        ax.set_xticks(np.arange(int(np.min(x)), int(np.max(x))))

        ax.grid(which="both", color=colors["secondary"], linestyle=":", linewidth=1, alpha=0.5)
        ax.grid(which="major", color=colors["secondary"], linestyle=":", linewidth=1, alpha=0.5)

        if show_solutions:
            if self.delta > 0:
                ax.plot(df["x"], df["y"], color=colors["is_out"])
                ax.plot(df[df["x"] < self.x1]["x"], df[df["x"] < self.x1]["y"], color=colors["is_in"])
                ax.plot(df[df["x"] > self.x2]["x"], df[df["x"] > self.x2]["y"], color=colors["is_in"])
            else:
                ax.plot(df["x"], df["y"], color=colors["is_in"])
        else:
            ax.plot(df["x"], df["y"], color=colors["is_neutral"])

        if show_solutions:
            (pab,) = ax.plot(
                [self.alpha],
                [self.f(self.alpha)],
                "d",
                color=colors["secondary"],
                markersize=15,
                label=r"$(\alpha, \beta)=(%s, %s)$" % (self.salpha, self.sbeta),
            )

            if self.delta > 0:
                (px1,) = ax.plot([self.x1], [0], "s", color=colors["is_out"], markersize=15, label=f"$x1={self.sx1}$")
                (px2,) = ax.plot([self.x2], [0], "s", color=colors["is_in"], markersize=15, label=f"$x2={self.sx2}$")
                ax.legend(handles=[px1, px2, pab], loc="upper left")
            else:
                ax.legend(handles=[pab], loc="upper left")

        ax.set_title(
            r"""${}x²{}x{}{}, \ \ \  \Delta={}$""".format(self.sa, self.sb, self.sc, self.sconstraint, self.sdelta)
        )
        return ax

    def __getattr__(self, name):
        if name == "sconstraint":
            if ">=0" in self.constraint:
                return r"\geq 0"
            elif "<=0" in self.constraint:
                return r"\leq 0"
            else:
                return self.constraint

        if name.startswith("m"):
            s = -1
            name = name[1:]
        else:
            s = 1
        if not name.startswith("s"):
            raise AttributeError
        name = name[1:]
        if not hasattr(self, name):
            raise AttributeError
        x = s * getattr(self, name)

        fraction = Fraction(x).limit_denominator().as_integer_ratio()

        if self.numbers == "int" or fraction[1] == 1:
            if name == "a":
                return f"{x:.0f}"
            return f"{x:+.0f}"
        elif self.numbers == "fraction":
            if fraction[1] == 1:
                return f"{fraction[0]:+.0f}"
            sign = "+" if fraction[0] * fraction[1] > 0 else "-"
            if name == "a":
                sign = ""
            return "%s\\frac{%s}{%s}" % (sign, np.abs(fraction[0]), np.abs(fraction[1]))
        else:
            return f"{x:+.2f}"
