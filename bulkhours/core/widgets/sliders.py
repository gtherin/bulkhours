import ipywidgets

from .buttons import *
from .base import WidgetBase


class WidgetIntSlider(WidgetBase):
    widget_id = "intslider"

    def init_widget(self):
        cell_checks = self.cinfo.options.split(";")
        return ipywidgets.IntSlider(
            min=int(cell_checks[0]),
            max=int(cell_checks[1]),
            step=1,
            continuous_update=True,
            orientation="horizontal",
            readout=True,
            readout_format="d",
        )

    def get_params(self):
        return dict(answer=self.get_answer(), atype=self.cinfo.type, comment=str(self.widget.value))

    def display_correction(self, data, output=None):
        md(header=f"Correction ({self.cinfo.id})", mdbody=data["answer"])
        if data["answer"] == self.get_answer():
            md(mdbody=f"🥳Correction: {data['answer']}", bc="green")
        else:
            md(mdbody=f"😔Correction: {data['answer']}", bc="red")

    def get_answer(self):
        return self.widget.value


class WidgetFloatSlider(WidgetIntSlider):
    widget_id = "floatslider"

    def init_widget(self):
        cell_checks = self.cinfo.options.split(";")
        return ipywidgets.FloatSlider(
            min=float(cell_checks[0]),
            max=float(cell_checks[1]),
            value=float(cell_checks[2]),
            step=0.5,
            continuous_update=True,
            orientation="horizontal",
            readout=True,
            readout_format=".1f",
        )
