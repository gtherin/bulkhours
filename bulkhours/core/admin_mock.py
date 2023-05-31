import IPython
from IPython.core.magic import Magics, magics_class, line_cell_magic, needs_local_scope
import ipywidgets


def mock_message(in_french):
    return (
        "🚫Les fonctionnalités 'admin' ne sont pas disponibles en mode élève🎓.Contacter bulkhours@guydegnol.net en cas de problème"
        if in_french
        else "🚫The 'admin' functionalities are not available in student mode🎓. Contact bulkhours@guydegnol.net in case of problem"
    )


def generic_func(func, *kargs, **kwargs):
    try:
        module = __import__("bulkhours_admin", fromlist=[func])
        return getattr(module, func)(*kargs, **kwargs)

    except ImportError:
        from .tools import get_config

        config = get_config()
        IPython.display.display(mock_message(config["in_french"]))


@magics_class
class AdminEvaluation(Magics):
    def __init__(self, shell, nid, in_french, openai_token):
        super(AdminEvaluation, self).__init__(shell)
        self.in_french = in_french

    @line_cell_magic
    @needs_local_scope
    def evaluation_cell_id_admin(self, line, cell="", local_ns=None):
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

    @line_cell_magic
    @needs_local_scope
    def update_cell_id_admin(self, *kargs, **kwargs):
        return self.evaluation_cell_id_admin(*kargs, **kwargs)


def summary(*kargs, **kwargs):
    return generic_func("summary", *kargs, **kwargs)


def edit_students(*kargs, **kwargs):
    return generic_func("edit_students", *kargs, **kwargs)


def get_audio(*kargs, **kwargs):
    return generic_func("get_audio", *kargs, **kwargs)


def dashboard(*kargs, **kwargs):
    return generic_func("dashboard", *kargs, **kwargs)


def evaluate(*kargs, **kwargs):
    return generic_func("evaluate", *kargs, **kwargs)
