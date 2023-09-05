import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from decimal import *


def md(data, style="header"):
    import IPython

    if style == "header":
        data = r"<font size='+3'>%s</font>" % (data)

    IPython.display.display(IPython.display.Markdown(r"%s" % data))


class Poly2dr:
    def __init__(self, a, b, c, numbers="float2"):
        self.a, self.b, self.c, self.numbers = a, b, c, numbers

        getcontext()
        Context(
            prec=28,
            rounding=ROUND_HALF_EVEN,
            Emin=-999999,
            Emax=999999,
            capitals=1,
            clamp=0,
            flags=[],
            traps=[Overflow, DivisionByZero, InvalidOperation],
        )

        getcontext().prec = 7

        if a == 0:
            raise ValueError("a cannot be zero, otherwise it is not a second degree polynomial")

        # Calculate basic quantities
        self.alpha, self.beta, self.delta = -b / 2 / a, self.f(-b / 2 / a), b**2 - 4 * a * c
        self.x1, self.x2 = self.alpha - np.sqrt(np.abs(self.beta / a)), self.alpha + np.sqrt(
            np.abs(self.beta / self.a)
        )

    def __repr__(self):
        return f"Poly2dr({self.a}, {self.b}, {self.c})"

    def f(self, x):
        return self.a * x**2 + self.b * x + self.c

    def get_basic(self):
        return r"""${}x^2{}x{}$""".format(self.sa, self.sb, self.sc)

    def get_canonical(self):
        if self.delta == 0:
            return r"""${}(x{})^2$""".format(self.sa, self.msalpha)
        else:
            return r"""${}(x{})^2{}$""".format(self.sa, self.msalpha, self.sbeta)

    def get_factorized(self):
        if self.delta == 0:
            return r"""$(x{})^2$""".format(self.msx1)
        else:
            return r"""$(x{})(x{})$""".format(self.msx1, self.msx2)

    def get_various_forms(self):
        md(f"(a) Forme canonique: %s=0, %s=0" % (self.get_basic(), self.get_canonical()), style="header")
        if self.delta < 0:
            md(f"(a) Forme factorisée: %s=0" % self.get_factorized(), style="header")

    def get_sign_table(self):
        s = "+" if self.a > 0 else "-"
        ms = "-" if self.a > 0 else "+"

        text = f"""### (b) Tableau de signes:\n"""

        if self.delta > 0:
            md(
                f"""{text}
|$x$|$-\infty$| |{self.sx1}| |{self.sx2}| |$+\infty$|
|---|---|---|---|---|---|---|---|
|$f(x)$| |{s}|0|{ms}|0|{s}| |
        """
            )
        elif self.delta == 0:
            md(
                f"""{text}
|$x$|$-\infty$| |{self.sx1}| |$+\infty$|
|---|---|---|---|---|---|
|$f(x)$| |{s}|0|{s}| |
        """
            )

        else:
            md(
                f"""{text}
|$x$|$-\infty$| |$+\infty$|
|---|---|---|---|
|$f(x)$| |{s}| |
        """
            )

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

    def get_solution2(self, sign):
        ax = self.get_graph()
        minx, maxx = self.get_xrange()
        x = np.linspace(minx, maxx, 100)
        ymin, ymax = ax.get_ylim()
        if sign > 0:
            ax.fill_between(x, x * 0, x * 0 + ymin, alpha=0.2, color="green")
        elif sign == 0:
            ax.axhline(y=0, color="green")
        else:
            ax.fill_between(x, x * 0, x * 0 + ymax, alpha=0.2, color="green")
        ax.set_ylim(ymin, ymax)
        ax.set_xlim(minx, maxx)

        if self.delta > 0:
            ax.plot([self.x1], [0], "X", markersize=20, color="red")
            ax.annotate("Solution 1", [self.x1, 0], color="red")
            ax.plot([self.x2], [0], "X", markersize=20, color="red")
            ax.annotate("Solution 2", [self.x2, 0], color="red")

    def get_graph(self):
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

        if self.delta > 0:
            ax.plot(df["x"], df["y"], color="red")
            ax.plot(df[df["x"] < self.x1]["x"], df[df["x"] < self.x1]["y"], color="green")
            ax.plot(df[df["x"] > self.x2]["x"], df[df["x"] > self.x2]["y"], color="green")
        else:
            ax.plot(df["x"], df["y"], color="green")

        if self.delta > 0:
            ax.plot([self.x1], [0], "o")
            ax.annotate("(x1, 0)", [self.x1, 0])
            ax.plot([self.x2], [0], "o")
            ax.annotate("(x2, 0)", [self.x2, 0])
        ax.plot([self.alpha], [self.f(self.alpha)], "o")
        ax.annotate(r"($\alpha, \beta$)", [self.alpha, self.f(self.alpha)])

        ax.set_title(r"""${}x²{}x{}, \ \ \  \Delta={}$""".format(self.sa, self.sb, self.sc, self.sdelta))
        return ax

    def __getattr__(self, name):
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

        from fractions import Fraction

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
