import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt


def create_fold(left, width, label, y=0, color=None):
    colors = {"Train": "#581845", "Validation": "#C70039", "Test": '#FF5733', 'Fold': "#52DE97", 'All data': "#0097B2", 'Empty': "white"}

    if color is None:
        color = colors[label] if label in colors else '#C70039'
    ax.barh(y=y, width=width, left=left, color=color, height=0.9, edgecolor='black' if label == "Empty" else "white")
    ax.text(left + width / 2, y, label, ha='center', va='center', color='white', fontsize=17, fontweight='bold')
    left += width
    return left


def rolling_cross(ax=None):
    # Create graph if needed
    if ax is None:
        fig, ax = plt.subplots(figsize=(10, 5))

    for y, width in enumerate(widths:=[0.3, 0.5, 0.7, 0.9]):
        left, y = 0, len(widths)-y-1
        left = create_fold(left, width, 'Train', y=y)
        left = create_fold(left, 0.3, 'Validation', y=y)
        left = create_fold(left, 0.3, 'Test', y=y)
    left = create_fold(0, left, 'All data', y=len(widths))
    plt.axis('off')
    return ax


def lpo_cross(p=1, ax=None):
    # Create graph if needed
    if ax is None:
        fig, ax = plt.subplots(figsize=(10, 5))

    for y in range(al:=10):
      left = 0
      for k in range(11):
          left = create_fold(left, 0.04, k+1, y=y, color="#C70039" if np.abs(k-y) < p else "#581845")
      left = create_fold(left, 0.3, 'Test', y=y)
    left = create_fold(0, left, 'All data', y=al)
    plt.axis('off')
    return ax
