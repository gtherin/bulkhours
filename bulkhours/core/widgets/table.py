import ipywidgets
import numpy as np

from .buttons import *
from ..logins import *
from . import base


class WidgetTable(base.WidgetBase):
    widget_id = "table"

    def get_data(self):
        return np.array([r.split(";") for r in self.cinfo.options.split(";;")])

    def init_widget(self, force_correction=None):
        # %evaluation_cell_id -i Itable -t table -o x;y;;1;F;;10;I -p execute_on_start,toggle_on,lock
        # %evaluation_cell_id -i Itable -t table -o ;0.5 kpc;1 kpc;1.5 kpc;2 kpc;;v(km/s);I;I;I;I -p execute_on_start,toggle_on,lock

        data = self.get_data()
        grid = ipywidgets.GridspecLayout(*data.shape)
        # colors.set_style(grid, "sol_background")

        p = 0
        WidgetTable.vdata = np.zeros(data.shape)
        for i, row in enumerate(data):
            for j, col in enumerate(row):
                if col == "F" and force_correction is None:
                    grid[i, j] = ipywidgets.FloatText(
                        layout=ipywidgets.Layout(height="auto", width="auto", border="3px solid #eaeaea")
                    )
                elif col == "I" and force_correction is None:
                    grid[i, j] = ipywidgets.IntText(
                        layout=ipywidgets.Layout(height="auto", width="auto", border="3px solid #eaeaea")
                    )
                    exec(f"def on_value_change_{i}_{j}(change): WidgetTable.vdata[{i}, {j}] = change['new']")
                    exec(f"grid[{i}, {j}].observe(on_value_change_{i}_{j}, 'value')")
                elif col == "T" and force_correction is None:
                    grid[i, j] = ipywidgets.Text(
                        "", layout=ipywidgets.Layout(height="auto", width="auto", border="3px solid #eaeaea")
                    )
                else:
                    if col in ["F", "I", "T"]:
                        grid[i, j] = ipywidgets.Button(
                            description=force_correction[p],
                            layout=ipywidgets.Layout(height="auto", width="auto", border="3px solid #eaeaea"),
                        )
                        p += 1
                    else:
                        grid[i, j] = ipywidgets.Button(
                            description=col,
                            layout=ipywidgets.Layout(height="auto", width="auto", border="3px solid #eaeaea"),
                        )
        return grid

    def get_answer(self):
        data = self.get_data()

        answer = []
        for i, _ in enumerate(data):
            for j, col in enumerate(data[i]):
                if col in ["F", "I", "T"]:
                    answer.append(str(WidgetTable.vdata[i, j]))

        answer = ";".join(answer)
        return answer

    def get_params(self):
        return dict(answer=self.get_answer(), atype=self.cinfo.type)

    def display_correction(self, data, output=None):
        import IPython

        print("")
        md(header=f"Correction ({self.cinfo.id})")
        IPython.display.display(
            ipywidgets.HBox(
                [
                    self.init_widget(force_correction=data["answer"].split(";")),
                ]
            )
        )
