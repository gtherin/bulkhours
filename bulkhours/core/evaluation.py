import sys, inspect
import json

from IPython.core.magic import (
    Magics,
    cell_magic,
    magics_class,
    line_cell_magic,
    needs_local_scope,
)

from .widget_base import WidgetBase  # noqa
from .widget_table import WidgetTable  # noqa
from .widget_code_project import WidgetCodeProject  # noqa
from .widget_sliders import WidgetFloatSlider, WidgetIntSlider  # noqa
from .widget_texts import WidgetCodeText, WidgetTextArea  # noqa
from .widget_selectors import WidgetCheckboxes, WidgetRadios  # noqa
from .widget_cells import (
    WidgetCode,
    WidgetMarkdown,
    WidgetFormula,
    WidgetScript,
)  # noqa

from .line_parser import LineParser
from . import tools


def enumerate_widgets():
    jsonfile = tools.abspath("bulkhours/core/widgets.json")
    with open(jsonfile, "w", encoding="utf-8") as f:
        json.dump(
            {
                obj.widget_id: obj.widget_comp
                for _, obj in inspect.getmembers(sys.modules[__name__])
                if inspect.isclass(obj) and hasattr(obj, "widget_id")
            },
            f,
            ensure_ascii=False,
            indent=4,
        )


def evaluate_cell(line, cell):
    try:
        linfo = LineParser(line, cell)
    except:
        print("""⚠️\x1b[37mConnection to bulkhours database is not set-up. Service might be limited\x1b[0m⛓️‍💥""")
        return

    print(linfo, linfo.cinfo)


    wclass = WidgetBase
    for _, obj in inspect.getmembers(sys.modules[__name__]):
        if (
            inspect.isclass(obj)
            and hasattr(obj, "widget_id")
            and obj.widget_id == linfo.type
        ):
            wclass = obj

    return wclass(line, cell).evaluate_cell()


enumerate_widgets()


from IPython.core.magic import (
    Magics,
    cell_magic,
    magics_class,
    line_cell_magic,
    needs_local_scope,
)


@magics_class
class Evaluation(Magics):
    def __init__(self, shell):
        super(Evaluation, self).__init__(shell)

    @line_cell_magic
    @needs_local_scope
    def evaluation_cell_id(self, line, cell="", local_ns=None):
        """
        evaluation cell method
        """
        evaluate_cell(line, cell)
