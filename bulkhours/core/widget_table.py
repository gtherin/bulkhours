import ipywidgets
import numpy as np

from . import widget_base
from .tools import md


class WidgetTable(widget_base.WidgetBase):
    widget_id = "table"
    widget_comp = "lw|sc"

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
                layout = ipywidgets.Layout(height="auto", width="auto", border="3px solid #eaeaea")
                if len(col) > 0 and col == "F" and force_correction is None:
                    default = float(col[2:]) if ":" in col else 0
                    grid[i, j] = ipywidgets.FloatText(value=default, layout=layout)
                    exec(f"def on_value_change_{i}_{j}(change): WidgetTable.vdata[{i}, {j}] = change['new']")
                    exec(f"grid[{i}, {j}].observe(on_value_change_{i}_{j}, 'value')")
                elif len(col) > 0 and col[0] == "I" and force_correction is None:
                    default = int(col[2:]) if ":" in col else 0
                    grid[i, j] = ipywidgets.IntText(value=default, layout=layout)
                    exec(f"def on_value_change_{i}_{j}(change): WidgetTable.vdata[{i}, {j}] = change['new']")
                    exec(f"grid[{i}, {j}].observe(on_value_change_{i}_{j}, 'value')")
                elif len(col) > 0 and col[0] == "S" and force_correction is None:
                    default = str(col[2:]) if ":" in col else 0
                    grid[i, j] = ipywidgets.Text(value=default, layout=layout)
                    exec(f"def on_value_change_{i}_{j}(change): WidgetTable.vdata[{i}, {j}] = change['new']")
                    exec(f"grid[{i}, {j}].observe(on_value_change_{i}_{j}, 'value')")
                else:
                    if len(col) > 0 and col[0] in ["F", "I", "S"]:
                        grid[i, j] = ipywidgets.Button(description=force_correction[p], layout=layout)
                        p += 1
                    else:
                        grid[i, j] = ipywidgets.Button(description=col, layout=layout)
        return grid

    def get_answer(self):
        data = self.get_data()

        answer = []
        for i, _ in enumerate(data):
            for j, col in enumerate(data[i]):
                if col in ["F", "I", "S"]:
                    answer.append(str(WidgetTable.vdata[i, j]))

        answer = ";".join(answer)
        return answer

    def display_correction(self, student_data, teacher_data, output=None):
        import IPython

        print("")
        md(header=f"Correction ({self.cinfo.cell_id})")
        IPython.display.display(
            ipywidgets.HBox(
                [
                    self.init_widget(force_correction=teacher_data["answer"].split(";")),
                ]
            )
        )
