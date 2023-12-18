import IPython
from IPython.core.magic import (
    Magics,
    magics_class,
    line_cell_magic,
    needs_local_scope,
)

from . import tools


def format_with_black(cell, line_length=88):
    import black
    import ipywidgets

    tabs = ipywidgets.HBox(
        [
            out_left := ipywidgets.Output(layout={"width": "50%"}),
            out_right := ipywidgets.Output(layout={"width": "50%"}),
        ]
    )

    with out_left:
        tools.html(f"Code (Raw)", color="red", use_ipywidgets=True, display=True)
        tools.code(cell, display=True)

    with out_right:
        tools.html(f"Code (PEP8)", color="green", use_ipywidgets=True, display=True)
        # tools.code(black.format_str(cell, mode=black.FileMode()), display=True)
        tools.code(
            black.format_str(
                cell,
                mode=black.Mode(line_length=line_length),
            ),
            display=True,
        )

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
