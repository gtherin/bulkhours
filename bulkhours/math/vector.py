import pandas as pd
import IPython
from . import core
import matplotlib.pyplot as plt


class Vector:
    def __init__(self, x_a, y_a, x_b=None, y_b=None):
        self.x_a, self.y_a, self.x_b, self.y_b = x_a, y_a, x_b, y_b
        if x_b is None:
            self.x_b = self.x_a
        if y_b is None:
            self.y_b = self.y_a

        self.dx, self.dy = self.x_b - self.x_a, self.y_b - self.y_a

    def draw(self, ax, xoffset=0, yoffset=0, text=None, vname=None, color="blue"):
        self.color = core.c.get(color)
        if vname is not None:
            self.text = r"$\overrightarrow{%s}$" % vname
        elif text is not None:
            self.text=text
        ax.arrow(self.x_a, self.y_a, self.dx, self.dy, fc=self.color, ec=self.color, head_width=0.2, head_length=0.2, 
                 width=0.1, length_includes_head=True)
        ax.text(self.x_a+0.5*self.dx+xoffset, self.y_a+0.5*self.dy+yoffset, self.text, size=16, ha='center', va='center', color=self.color)

    def __add__(a, b):
      return Vector(a.x_a, a.y_a, a.x_b+b.dx, a.y_b+b.dy)

    def __sub__(a, b):
      return Vector(a.x_a, a.y_a, a.x_b-b.dx, a.y_b-b.dy)

    def __mul__(a1, a2):
      if type(a1) in [int, float]:
          cst, a = a1, a2
      else:
          a, cst = a1, a2
      return Vector(a.x_a, a.y_a, a.x_a+cst*a.dx, a.y_a+cst*a.dy)


class VectorGrid:
    def __init__(self, x_min, y_min, x_max, y_max):
        self.fig, self.ax = plt.subplots(figsize=(10, 5))
        self.x_min, self.x_max, self.y_min, self.y_max = x_min, y_min, x_max, y_max
        self.ax.set_xlim(self.x_min, self.x_max)
        self.ax.set_ylim(self.y_min, self.y_max)

        self.ax.set_xticks(np.arange(self.x_min, self.x_max))
        self.ax.set_yticks(np.arange(self.y_min, self.y_max))
        self.ax.set_aspect('equal', adjustable='box')
        self.ax.axhline(y=0, color="grey", alpha=0.4)
        self.ax.axvline(x=0, color="grey", alpha=0.4)

        self.ax.grid(which="both", color="grey", linestyle=":", linewidth=1, alpha=0.4)
        self.ax.grid(which="major", color="grey", linestyle=":", linewidth=1, alpha=0.4)

    def draw_point(self, x, y, xoffset=0, yoffset=0, text=None, vname=None, color="blue"):
        color = core.c.get(color)
        self.ax.scatter([x], [y], color=color)
        self.ax.text(x+xoffset, y+yoffset, text, size=16, ha='center', va='center', color=color)

    def draw_vector(self, vector, **kwargs):
        vector.draw(self.ax, **kwargs)
