import os
import sys, inspect

from .buttons import *
from .. import firebase
from .base import WidgetBase
from .table import WidgetTable
from .code_project import WidgetCodeProject
from .sliders import WidgetFloatSlider, WidgetIntSlider
from .texts import WidgetCodeText, WidgetTextArea
from .selectors import WidgetCheckboxes, WidgetRadios
from .cells import WidgetCode, WidgetMarkdown, WidgetFormula


def create_widget(cinfo, cell, in_french, shell):
    for _, obj in inspect.getmembers(sys.modules[__name__]):
        if inspect.isclass(obj) and hasattr(obj, "widget_id") and obj.widget_id == cinfo.type:
            return obj(cinfo, cell, in_french, shell)


def send_message(bwidget, output):
    data = firebase.get_solution_from_corrector(bwidget.cell_id, corrector="solution")
    if (user := os.environ["STUDENT"]) in data or (user := "all") in data:
        md(
            header=f"Message ({bwidget.cinfo.id}, {user}) du correcteur"
            if bwidget.in_french
            else f"Message ({bwidget.cinfo.id}, {user}) from corrector",
            rawbody=data[user],
        )
