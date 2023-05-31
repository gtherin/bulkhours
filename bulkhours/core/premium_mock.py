import IPython
from IPython.core.magic import Magics, magics_class, line_cell_magic, needs_local_scope
import ipywidgets


def mock_message(in_french):
    return (
        "Les fonctionnalités 'evaluation_cell_id' ne sont plus disponibles😕. Vous pouvez supprimer son appel de la cellule (pour enlever ce button) ou contacter bulkhours@guydegnol.net pour avoir un nouveau token pour reactiver le service🚀"
        if in_french
        else "The 'evaluation_cell_id' functionalities are no more available😕. You can remove its call line from the cell (to remove that button) or contact bulkhours@guydegnol.net to have a new token to reactivate the service🚀"
    )


def generic_func(func, *kargs, **kwargs):
    try:
        module = __import__("bulkhours_premium", fromlist=[func])
        return getattr(module, func)(*kargs, **kwargs)

    except ImportError:
        from .tools import get_config

        config = get_config()
        IPython.display.display(mock_message(config["in_french"]))


@magics_class
class MockEvaluation(Magics):
    def __init__(self, shell, nid, in_french, openai_token):
        super(MockEvaluation, self).__init__(shell)
        self.in_french = in_french

    @line_cell_magic
    @needs_local_scope
    def evaluation_cell_id(self, line, cell="", local_ns=None):
        IPython.display.display(mock_message(self.in_french))
        IPython.display.display(
            ipywidgets.Button(
                description="Evaluation non disponible😕" if self.in_french else "Evaluation not available😕",
                layout=ipywidgets.Layout(width="max-content"),
                disabled=True,
                tooltip=mock_message(self.in_french),
            )
        )

        self.shell.run_cell(cell)


def ask_chat_gpt(*kargs, **kwargs):
    return generic_func("ask_chat_gpt", *kargs, **kwargs)


def ask_dall_e(*kargs, **kwargs):
    return generic_func("ask_dall_e", *kargs, **kwargs)
