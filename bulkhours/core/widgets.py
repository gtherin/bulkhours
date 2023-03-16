import os

from IPython.core.magic import Magics, cell_magic, magics_class, line_cell_magic, needs_local_scope
import IPython
import ipywidgets

from .textstyles import *
from .logins import *
from . import firebase
from . import install


class BulkWidget:
    def __init__(self, cinfo, cell) -> None:
        self.cinfo = cinfo
        self.cell = cell

    def get_label(self):
        if self.cinfo.type in ["code", "markdown"]:
            label = []
        else:
            label = (
                f"<b><font face='FiraCode Nerd Font' size=4 color='red'>{self.cinfo.label}<font></b>"
                if self.cinfo.type == "floatslider"
                else f"<font face='FiraCode Nerd Font' size=4 color='black'>{self.cinfo.label}<font>"
            )
            label = [ipywidgets.HTML(value=label, layout=ipywidgets.Layout(height="auto", width="auto"))]

        return label

    def get_widgets(self):
        cell_checks = self.cinfo.options.split(";")
        if self.cinfo.type == "checkboxes":
            widgets = [ipywidgets.Checkbox(value=False, description=i, indent=False) for i in cell_checks]
        elif self.cinfo.type in ["intslider"]:
            widgets = [
                ipywidgets.IntSlider(
                    min=int(cell_checks[0]),
                    max=int(cell_checks[1]),
                    step=1,
                    continuous_update=True,
                    orientation="horizontal",
                    readout=True,
                    readout_format="d",
                )
            ]
        elif self.cinfo.type in ["floatslider"]:
            widgets = [
                ipywidgets.FloatSlider(
                    min=float(cell_checks[0]),
                    max=float(cell_checks[1]),
                    value=float(cell_checks[2]),
                    step=0.5,
                    continuous_update=True,
                    orientation="horizontal",
                    readout=True,
                    readout_format=".1f",
                )
            ]

        elif self.cinfo.type == "textarea":
            widgets = [ipywidgets.Textarea(placeholder="I don't know", disabled=False)]
        elif self.cinfo.type == "radios":
            widgets = [ipywidgets.RadioButtons(options=cell_checks, layout={"width": "max-content"})]
        elif self.cinfo.type == "codetext":
            widgets = [ipywidgets.Text()]
        else:
            widgets = []

        return widgets

    def get_layout(self):
        return (
            ipywidgets.Layout(overflow="scroll hidden", width="auto", flex_flow="row", display="flex")
            if self.cinfo.type == "checkboxes"
            else ipywidgets.Layout()
        )

    def get_answer(self, widgets, cinfo_type):
        cell_checks = self.cinfo.options.split(";")
        if cinfo_type in ["codetext"]:
            return eval(widgets[0].value)
        elif cinfo_type in ["code", "markdown"]:
            return self.cell
        elif cinfo_type in ["checkboxes", "radios"]:
            return ";".join([cell_checks[k] for k, i in enumerate(widgets) if i.value])
        else:
            return widgets[0].value
