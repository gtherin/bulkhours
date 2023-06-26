import ipywidgets

from .widget_base import WidgetBase
from .cell_parser import CellParser


class WidgetIntSlider(WidgetBase):
    widget_id = "intslider"
    widget_comp = "lwsc"

    def format(self, v):
        return int(v)

    def get_args(self):
        cell_checks = self.cinfo.options.split(";")

        kwargs = dict(min=self.format(cell_checks[0]), max=self.format(cell_checks[1]))
        if self.cinfo.answer != "":
            kwargs["value"] = self.format(self.cinfo.answer)
        elif self.cinfo.answer != "":
            kwargs["value"] = self.format(self.cinfo.default)
        else:
            kwargs["value"] = kwargs["min"]

        return kwargs

    def init_widget(self):
        kwargs = self.get_args()
        return ipywidgets.IntSlider(
            step=1, continuous_update=True, orientation="horizontal", readout=True, readout_format="d", **kwargs
        )


class WidgetFloatSlider(WidgetIntSlider):
    widget_id = "floatslider"
    widget_comp = "lwsc"

    def format(self, v):
        return float(v)

    def init_widget(self):
        kwargs = self.get_args()
        return ipywidgets.FloatSlider(
            step=0.5, continuous_update=True, orientation="horizontal", readout=True, readout_format=".1f", **kwargs
        )
