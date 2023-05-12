from IPython.core.magic import Magics, cell_magic, magics_class, line_cell_magic, needs_local_scope
import ipywidgets


@magics_class
class EmptyEvaluation(Magics):
    def __init__(self, shell, nid, in_french, api_key):
        super(EmptyEvaluation, self).__init__(shell)
        self.nid = nid
        self.in_french = in_french

    @line_cell_magic
    @needs_local_scope
    def evaluation_cell_id(self, line, cell="", local_ns=None):
        import IPython

        tooltip = """
The ```evaluation_cell_id``` functionalities are not available anymore. 
You can remove its call line from the cell (probably the first line) or
contact bulkhours@guydegnol.net to have a new token to reactivate it"""
        IPython.display.display(IPython.display.Markdown(tooltip))
        d = "Evaluation non disponible" if self.in_french else "Evaluation not available"
        IPython.display.display(
            ipywidgets.Button(
                description=d,
                button_style="warning",
                layout=ipywidgets.Layout(width="max-content"),
                disabled=True,
                tooltip=tooltip,
            )
        )

        self.shell.run_cell(cell)
