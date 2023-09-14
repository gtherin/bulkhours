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
