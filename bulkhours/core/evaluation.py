import sys, inspect
import json

from IPython.core.magic import Magics, cell_magic, magics_class, line_cell_magic, needs_local_scope

from .widget_base import WidgetBase  # noqa
from .widget_table import WidgetTable  # noqa
from .widget_code_project import WidgetCodeProject  # noqa
from .widget_sliders import WidgetFloatSlider, WidgetIntSlider  # noqa
from .widget_texts import WidgetCodeText, WidgetTextArea  # noqa
from .widget_selectors import WidgetCheckboxes, WidgetRadios  # noqa
from .widget_cells import WidgetCode, WidgetMarkdown, WidgetFormula, WidgetScript  # noqa

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
    if not (config := tools.get_config()) or config.get("email") == "john.doe@un.known":
        print(
            f"""# To be able to use your the evaluation tools, you need to identify yourself with the following command:
bulkhours.init_env(\033[1memail\033[0m="name@institute.ac")  # To be run in an initisalization cell

# You can also use the following command to get more information:
\033[1mhelp(bulkhours.init_env)\033[0m
    """
        )
        return

    linfo = LineParser(line, cell)

    wclass = WidgetBase
    for _, obj in inspect.getmembers(sys.modules[__name__]):
        if inspect.isclass(obj) and hasattr(obj, "widget_id") and obj.widget_id == linfo.type:
            wclass = obj

    return wclass(line, cell).evaluate_cell()


enumerate_widgets()


@magics_class
class Evaluation(Magics):
    def __init__(self, shell):
        super(Evaluation, self).__init__(shell)

    @line_cell_magic
    @needs_local_scope
    def evaluation_cell_id(self, line, cell="", local_ns=None):
        """
        my doc string
        """
        evaluate_cell(line, cell)
