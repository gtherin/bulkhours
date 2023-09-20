import pandas as pd
import IPython
import matplotlib.pyplot as plt
import numpy as np

from .. import core


class Vector2:
    def __init__(self, data, x0=0, y0=0):

        if "Vector" in str(type(data)):
            self.v = data.v
        else:
            self.v = np.array(data, dtype=float)
        self.x0, self.y0 = x0, y0

    @staticmethod
    def from_points(x_a, y_a, x_b, y_b):
        return Vector2([x_b-x_a, y_b-y_a], x0=x_a, y0=y_a)

    def norm(self):
        return np.sqrt(np.dot(self.v, self.v))

    def show(self):
        return f"{self.v}"

    def normalize(self):
        self.v = np.array(self.v, dtype=float) / self.norm()
        return self

    def dot(self, b):
        return np.dot(self.v, b.v)

    def cross(self, b):
        # Vectorial product
        return np.cross(self.v, b.v)

    def draw(self, ax, xoffset=0, yoffset=0, text=None, vname=None, color="blue"):
        self.color = core.c.get(color)
        if vname is not None:
            self.text = r"$\overrightarrow{%s}$" % vname
        elif text is not None:
            self.text=text
        ax.arrow(self.x0, self.y0, self.v[0], self.v[1], fc=self.color, ec=self.color, head_width=0.2, head_length=0.2, width=0.1, length_includes_head=True)
        ax.text(self.x0+0.5*self.v[0]+xoffset, self.y0+0.5*self.v[1]+yoffset, self.text, size=16, ha='center', va='center', color=self.color)

    def __add__(a, b):
        return Vector2(a.v+b.v, x0=a.x0, y0=a.y0)

    def __sub__(a, b):
        return Vector2(a.v-b.v, x0=a.x0, y0=a.y0)

    def __mul__(a1, a2):
      if type(a1) in [int, float]:
          cst, a = a1, a2
      else:
          a, cst = a1, a2
      return Vector2(a.x_a, a.y_a, a.x_a+cst*a.dx, a.y_a+cst*a.dy)

class Vector:
    def __init__(self, x_a, y_a, x_b=None, y_b=None, xoffset=0, yoffset=0):
        self.x_a, self.y_a, self.x_b, self.y_b = x_a, y_a, x_b, y_b
        if x_b is None:
            self.x_b = self.x_a
        if y_b is None:
            self.y_b = self.y_a

        self.add_offset(xoffset=xoffset, yoffset=yoffset)
        self.dx, self.dy = self.x_b - self.x_a, self.y_b - self.y_a
        self.v = np.array([self.dx, self.dy])

    def norm(self):
        return np.sqrt(np.dot(self.v, self.v))

    def normalize(self):
        norm = self.norm()
        self.dx, self.dy = self.dx / norm, self.dy / norm
        self.x_b, self.y_b = self.x_a + self.dx, self.y_a + self.dy

    def dot(self, b):
        return np.dot(self.v, b.v)

    def cross(self, b):
        # Vectorial product
        return np.cross(self.v, b.v)

    def add_offset(self, xoffset=0, yoffset=0):
        self.x_a += xoffset
        self.x_b += xoffset
        self.y_a += yoffset
        self.y_b += yoffset

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


def from_vector(vector, xoffset=0, yoffset=0):
    return vector.add_offset(xoffset=xoffset, yoffset=yoffset)


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
