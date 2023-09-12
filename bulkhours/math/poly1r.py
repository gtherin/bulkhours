import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from fractions import Fraction


def md(data, style="raw"):
    import IPython

    if style == "header":
        data = r"<font size='+3'>%s</font>" % (data)

    IPython.display.display(IPython.display.Markdown(r"%s" % data))


class Poly1dr:
    def __init__(self, a, b, numbers="float2", constraint="=0"):
        self.a, self.b, self.numbers, self.constraint = a, b, numbers, constraint

        if a == 0:
            raise ValueError("a cannot be zero, otherwise it is a constant")

    @staticmethod
    def from_points(x1, y1, x2, y2, numbers="float2", constraint="=0"):
        a = (y2 - y1) / (x2 - x1)
        b = y1 - a * x1
        return Poly1dr(a, b, numbers=numbers, constraint=constraint)

    @staticmethod
    def from_tangent(x1, y1, fprime, numbers="float2"):
        a = fprime(x1)
        b = (y1 - a * x1)
        return Poly1dr(a, b, numbers=numbers)

    def f(self, x):
        return self.a * x + self.b

    def get_basic(self):
        return r"""${}x{}$""".format(self.sa, self.sb)

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

    def get_solution2(self):
        ax = self.get_graph(show_solutions=False)
        minx, maxx = self.get_xrange()
        x = np.linspace(minx, maxx, 100)
        df = pd.DataFrame([np.linspace(minx, maxx, 100)], index=["x"]).T
        df["y"] = self.f(x)

        ymin, ymax = ax.get_ylim()
        if self.constraint in ["<0", "<=0"]:
            negc, posc = "green", "red"
            ax.plot(df[df["y"] < 0]["x"], df[df["y"] < 0]["y"] * 0, color=negc)
            ax.plot(df[df["y"] > 0]["x"], df[df["y"] > 0]["y"] * 0, color=posc)
        elif self.constraint in [">=0", ">0"]:
            negc, posc = "green", "red"

            ax.plot(df[df["x"] < self.x1]["x"], df[df["x"] < self.x1]["y"] * 0, color=negc)
            ax.plot(df[df["x"] > self.x2]["x"], df[df["x"] > self.x2]["y"] * 0, color=negc)
            ax.plot(df[df["y"] < 0]["x"], df[df["y"] < 0]["y"] * 0, color=posc)

        if "=0" in self.constraint:
            ax.plot([self.x1], [0], "o", markersize=20, color="green")
            ax.plot([self.x2], [0], "o", markersize=20, color="green")
            print(self.x1, self.x2)
        else:
            ax.plot([self.x1], [0], "x", markersize=20, color="red")
            ax.plot([self.x2], [0], "x", markersize=20, color="red")
        return ax

    def get_graph(self, show_solutions=True):
        minx, maxx = self.get_xrange()

        x = np.linspace(minx, maxx, 100)
        df = pd.DataFrame([np.linspace(minx, maxx, 100)], index=["x"]).T
        df["y"] = self.f(x)

        fig = plt.figure()
        ax = fig.add_subplot(1, 1, 1)

        ax.axhline(y=0, color="k")
        ax.axvline(x=0, color="k")
        ax.set_xticks(np.arange(int(np.min(x)), int(np.max(x))))

        ax.grid(which="both")
        ax.grid(which="major", alpha=0.5)

        if show_solutions:
            if self.delta > 0:
                ax.plot(df["x"], df["y"], color="red")
                ax.plot(df[df["x"] < self.x1]["x"], df[df["x"] < self.x1]["y"], color="green")
                ax.plot(df[df["x"] > self.x2]["x"], df[df["x"] > self.x2]["y"], color="green")
            else:
                ax.plot(df["x"], df["y"], color="green")
        else:
            ax.plot(df["x"], df["y"], color="grey")

        if show_solutions:
            if self.delta > 0:
                ax.plot([self.x1], [0], "o")
                ax.annotate("(x1, 0)", [self.x1, 0])
                ax.plot([self.x2], [0], "o")
                ax.annotate("(x2, 0)", [self.x2, 0])
            ax.plot([self.alpha], [self.f(self.alpha)], "o")
            ax.annotate(r"($\alpha, \beta$)", [self.alpha, self.f(self.alpha)])

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
