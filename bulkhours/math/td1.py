import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from fractions import Fraction
from .. import core
from matplotlib.lines import Line2D


colors = {
    "is_in": core.c.caliases["blue"],
    "is_out": core.c.caliases["red"],
    "is_neutral": core.c.caliases["purple"],
    "secondary": core.c.caliases["orange"],
}


def get_solution2(self, x2=None, y2=None):
    ax = self.get_graph(show_solutions=False)
    minx, maxx = self.get_xrange()
    x = np.linspace(minx, maxx, 100)
    df = pd.DataFrame([np.linspace(minx, maxx, 100)], index=["x"]).T
    df["y"] = self.f(x)
    ymin, ymax = ax.get_ylim()

    # By default, no solution on the axis
    tail_color, middle_color = colors["is_out"], colors["is_out"]

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
            if self.sx1 == self.sx2:
                gleg, lleg = Line2D([], [], color=colors["is_in"]), "$x \in \{%s\}$" % (self.sx1)
            else:
                gleg, lleg = Line2D([], [], color=colors["is_in"]), "$x \in \{%s, %s\}$" % (self.sx1, self.sx2)
        else:
            gleg, lleg = Line2D([0], [0], color=colors["is_in"], marker="o", markersize=20), lleg.replace(
                "<", " <= "
            ).replace(">", " >= ")
    else:
        ax.plot([self.x1], [0], "X", markersize=15, color=colors["is_out"])
        ax.plot([self.x2], [0], "X", markersize=15, color=colors["is_out"])

    if self.delta < 0:
      if (">" in self.constraint and self.a < 0) or  ("<" in self.constraint and self.a > 0):
          gleg, lleg = Line2D([0], [0], color=colors["is_out"]), "Aucune solution"
          ax.plot(df["x"], df["y"] * 0, color=colors["is_out"])

    ax.set_ylim(ymin, ymax)
    ax.set_xlim(minx, maxx)
    # self.get_sign_table()
    if gleg is not None:
        ax.legend([gleg], [lleg], loc="upper left")

    if y2 is not None:
        ax.plot(x2, y2, color=colors["secondary"])
