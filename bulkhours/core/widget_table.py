import ipywidgets
import numpy as np

from .textstyles import *
from .logins import *


def get_table_widgets(cinfo):
    # %evaluation_cell_id -i Itable -t table -o x;y;;1;F;;10;I -p execute_on_start,toggle_on,lock
    # %evaluation_cell_id -i Itable -t table -o ;0.5 kpc;1 kpc;1.5 kpc;2 kpc;;v(km/s);I;I;I;I -p execute_on_start,toggle_on,lock

    data = np.array([r.split(";") for r in cinfo.options.split(";;")])
    grid = ipywidgets.GridspecLayout(*data.shape, layout=ipywidgets.Layout(border="3px solid #eaeaea"))

    for i, _ in enumerate(data):
        for j, col in enumerate(data[i]):
            if col == "F":
                grid[i, j] = ipywidgets.FloatText(
                    layout=ipywidgets.Layout(height="auto", width="auto", border="3px solid #eaeaea")
                )
            elif col == "I":
                grid[i, j] = ipywidgets.IntText(
                    layout=ipywidgets.Layout(height="auto", width="auto", border="3px solid #eaeaea")
                )
            elif col == "T":
                grid[i, j] = ipywidgets.Text(
                    "", layout=ipywidgets.Layout(height="auto", width="auto", border="3px solid #eaeaea")
                )
            else:
                grid[i, j] = ipywidgets.Button(
                    description=col, button_style="warning", layout=ipywidgets.Layout(height="auto", width="auto")
                )
                grid[i, j].style.text_color = "black"
                grid[i, j].style.button_color = "#eaeaea"
    return grid
