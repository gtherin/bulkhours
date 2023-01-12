import matplotlib as mpl
import matplotlib.animation as animation
import matplotlib.pyplot as plt
import numpy as np
import collections
import random
import sys


def plot_environment(env, figsize=(5, 4)):
    plt.figure(figsize=figsize)
    img = env.render()
    if type(img) == list:
        img = img[0]
    plt.imshow(img)
    plt.axis("off")
    plt.show()
    return img
