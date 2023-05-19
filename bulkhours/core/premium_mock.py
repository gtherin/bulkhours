from IPython.core.magic import Magics, magics_class, line_cell_magic, needs_local_scope
import ipywidgets


@magics_class
class MockEvaluation(Magics):
    def __init__(self, shell, nid, in_french, openai_token):
        super(MockEvaluation, self).__init__(shell)
        self.nid = nid
        self.in_french = in_french

    @line_cell_magic
    @needs_local_scope
    def evaluation_cell_id(self, line, cell="", local_ns=None):
        import IPython

        tooltip = (
            """
Les fonctionnalités 'evaluation_cell_id' ne sont plus disponibles😕.
Vous pouvez supprimer son appel de la cellule (pour enlever ce button) ou
contacter bulkhours@guydegnol.net pour avoir un nouveau token pour reactiver le service🚀"""
            if self.in_french
            else """
The 'evaluation_cell_id' functionalities are no more available😕. 
You can remove its call line from the cell (to remove that button) or
contact bulkhours@guydegnol.net to have a new token to reactivate the service🚀"""
        )

        d = "Evaluation non disponible😕" if self.in_french else "Evaluation not available😕"
        IPython.display.display(
            ipywidgets.Button(
                description=d,
                # button_style="warning",
                layout=ipywidgets.Layout(width="max-content"),
                disabled=True,
                tooltip=tooltip,
            )
        )

        self.shell.run_cell(cell)
