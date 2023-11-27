import IPython
from IPython.core.magic import (
    Magics,
    cell_magic,
    magics_class,
    line_cell_magic,
    needs_local_scope,
)

from . import tools


def show_answer(out, cuser, code, style=None):
    color = "red" if cuser == "Raw" else "green"
    show_raw_code = (
        style == "dark"
    )  # not ("google.colab" in sys.modules and style != "dark")

    with out:
        # Show code
        tools.html(
            f"Code ({cuser})", size="4", color=color, use_ipywidgets=True, display=True
        )
        tools.code(code, display=True)  # , style=style)  # , raw=show_raw_code


def format_with_black(cell):
    import black
    import ipywidgets

    fcell = black.format_str(cell, mode=black.FileMode())

    out1 = ipywidgets.Output(layout={"width": "50%"})
    out2 = ipywidgets.Output(layout={"width": "50%"})
    tabs = ipywidgets.HBox([out1, out2])

    show_answer(out1, "Raw", cell, style="dark")
    show_answer(out2, "PEP", fcell, style="dark")

    IPython.display.display(tabs)


@magics_class
class Black(Magics):
    def __init__(self, shell):
        super(Black, self).__init__(shell)

    @line_cell_magic
    @needs_local_scope
    def format_with_black(self, line, cell="", local_ns=None):
        """
        my doc string
        """
        format_with_black(cell)
