from .buttons import *  # noqa


from .base import WidgetBase  # noqa
from .table import WidgetTable  # noqa
from .code_project import WidgetCodeProject  # noqa
from .sliders import WidgetFloatSlider, WidgetIntSlider  # noqa
from .texts import WidgetCodeText, WidgetTextArea  # noqa
from .selectors import WidgetCheckboxes, WidgetRadios  # noqa
from .cells import WidgetCode, WidgetMarkdown, WidgetFormula  # noqa


def get_widget_obj(cinfo):
    import sys, inspect

    for _, obj in inspect.getmembers(sys.modules[__name__]):
        if inspect.isclass(obj) and hasattr(obj, "widget_id") and obj.widget_id == cinfo.type:
            return obj
    return WidgetBase


def create_widget(cinfo, cell, in_french, shell):
    return get_widget_obj(cinfo)(cinfo, cell, in_french, shell)


def check_widget(cinfo):
    cinfo.widgets = get_widget_obj(cinfo).default_wopts
    return cinfo
