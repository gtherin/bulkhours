import ipywidgets
import numpy as np

from .textstyles import *
from .logins import *


class WidgetBase:
    def __init__(self, cinfo, cell, in_french):
        self.cinfo = cinfo
        self.cell = cell
        self.in_french = in_french
        self.widget = self.get_widget()

    def get_widget(self):
        return None

    def get_layout(self):
        return ipywidgets.Layout(overflow="scroll hidden", width="auto", flex_flow="row", display="flex")

    def get_params(self, answer):
        return dict(answer=answer, atype=self.cinfo.type)

    def get_label(self):
        label = f"<b><font face='FiraCode Nerd Font' size=4 color='red'>{self.cinfo.label}<font></b>"
        return ipywidgets.HTML(value=label, layout=ipywidgets.Layout(height="auto", width="auto"))


class WidgetTable(WidgetBase):
    def get_widget(self):
        # %evaluation_cell_id -i Itable -t table -o x;y;;1;F;;10;I -p execute_on_start,toggle_on,lock
        # %evaluation_cell_id -i Itable -t table -o ;0.5 kpc;1 kpc;1.5 kpc;2 kpc;;v(km/s);I;I;I;I -p execute_on_start,toggle_on,lock

        data = np.array([r.split(";") for r in self.cinfo.options.split(";;")])
        grid = ipywidgets.GridspecLayout(*data.shape)  # , layout=ipywidgets.Layout(border="1px solid #eaeaea"))
        # colors.set_style(grid, "sol_background")

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
                        description=col,
                        # display="flex",
                        # layout=ipywidgets.Layout(height="auto", width="100%"),
                        # button_style="button3"
                        # style={"description_width": "initial"},
                        layout=ipywidgets.Layout(height="auto", width="auto", border="3px solid #eaeaea"),
                    )
                    # colors.set_style(grid[i, j], "button3")
        return grid

    def get_answer(self):
        print(self.widget)
        return self.widget

    def get_params(self, answer):
        return dict(answer=answer, atype=self.cinfo.type)
