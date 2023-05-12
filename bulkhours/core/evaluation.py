from IPython.core.magic import Magics, cell_magic, magics_class, line_cell_magic, needs_local_scope
import ipywidgets


@magics_class
class Evaluation(Magics):
    def __init__(self, shell, nid, in_french, api_key):
        super(Evaluation, self).__init__(shell)
        self.nid = nid
        self.in_french = in_french

    @line_cell_magic
    @needs_local_scope
    def evaluation_cell_id(self, line, cell="", local_ns=None):
        import IPython

        IPython.display.display(
            IPython.display.Markdown(
                """
The ```evaluation_cell_id``` functionalities are not available anymore. 
You can remove its call line from the cell (probably the first line) or
contact bulkhours@guydegnol.net to have a new token to reactivate it"""
            )
        )
        IPython.display.display(
            ipywidgets.Button(
                description="Evaluation not available",
                button_style="Evaluation not available",
                flex_flow="column",
                align_items="stretch",
                tooltip="Evaluation not available",
                layout=ipywidgets.Layout(width=self.width if self.width is not None else "max-content"),
            )
        )

        self.shell.run_cell(cell)
