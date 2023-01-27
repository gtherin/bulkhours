from pyparsing import string
from typing import Iterable

import matplotlib.pyplot as plt
import numpy as np
from matplotlib import animation, path





available_shapes = dict(
)

radians = float


class Shape(path.Path):

    @staticmethod
    def init(label, **kwargs):
        if label == "basic":
            return Shape.from_list([[0, 0], [-100, 100], [200, 0], [-100, -100], [0, 0]])
        elif label == "birds":
            return Shape.from_list([[0, 0], [-100, 60], [100, 0], [-100, -60], [0, 0]])
        elif label == "fish":
            return Shape.from_list([[0, 0], [-60, 75], [20, 50], [100, 50], [150, 0], [100, -50], [20, -50], [-60, -75], [0, 0]])
        elif label == "jfish":
            return Shape.from_list([[0, 0], [-60, 10], [0, 20], [-60, 30], [-60, 75], [20, 50], [100, 50], [150, 0], [100, -50], [20, -50], [-60, -75], [0, 0]])
        elif label == "bull":
            return Shape.from_list([[3, 6], [5, 7], [11, 7], [13, 6], [14, 5], [14, 3], [12, 1], [4, 1], [2, 3], [2, 5], [3, 6], [4, 9],
                      [2, 11], [2, 13], [5, 14], [6, 14], [4, 12], [6, 11], [10, 11], [12, 12], [10, 14], [11, 14],
                      [14, 13], [14, 11], [12, 9], [13, 6]#, [3, 4], [5, 3], [11, 3], [13, 4]
                      ], angle=-np.pi/2)
        elif type(label) == list:
            return Shape.from_list(label, **kwargs)
        else:
            return Shape.from_list([[0, 0], [-100, 100], [200, 0], [-100, -100], [0, 0]])

    @staticmethod
    def from_list(vertices, size=300, angle=0):
        vertices=np.array(vertices)

        # Central distribution
        mean = np.mean(vertices, axis=0).astype(np.int16)
        vertices -= mean

        # Adjust size
        dist = np.max(vertices, axis=0) - np.min(vertices, axis=0)
        factor = np.round(1+size / max(dist))
        vertices = (factor * vertices).astype(np.int16)

        # Adjust rotation
        if angle !=0:
            cos, sin = np.cos(angle), np.sin(angle)
            vertices = vertices @ (np.array([[cos, sin], [-sin, cos]]))

        return Shape(vertices=vertices, codes=np.array([path.Path.MOVETO]+[path.Path.LINETO]*(len(vertices)-2)+[path.Path.CLOSEPOLY], dtype=np.uint8),)


    def rotate_marker(p, angle: radians) -> path.Path:
        cos, sin = np.cos(angle), np.sin(angle)
        newpath = p.vertices @ (np.array([[cos, sin], [-sin, cos]]))
        return path.Path(newpath, p.codes)

