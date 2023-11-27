import IPython
from IPython.core.magic import (
    Magics,
    magics_class,
    line_cell_magic,
    needs_local_scope,
)

from . import tools


def format_with_black(cell):
    import black
    import ipywidgets

    tabs = ipywidgets.HBox(
        [
            out1 := ipywidgets.Output(layout={"width": "50%"}),
            out2 := ipywidgets.Output(layout={"width": "50%"}),
        ]
    )

    with out1:
        tools.html(f"Code (Raw)", color="red", use_ipywidgets=True, display=True)
        tools.code(cell, display=True)

    with out2:
        tools.html(f"Code (PEP8)", color="green", use_ipywidgets=True, display=True)
        tools.code(black.format_str(cell, mode=black.FileMode()), display=True)

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
