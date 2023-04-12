import ipywidgets
import numpy as np

from .buttons import *
from ..logins import *


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
