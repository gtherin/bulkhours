import IPython
from IPython.core.magic import Magics, magics_class, line_cell_magic, needs_local_scope
import ipywidgets
from .tools import is_admin, get_value


def mock_message(language):
    return (
        "🚫Les fonctionnalités 'admin' ne sont pas disponibles avec vos token. Contacter bulkhours@guydegnol.net en cas de problème."
        if language == "fr"
        else "🚫The 'admin' functionalities are not available with your token. Contact bulkhours@guydegnol.net in case of problem."
    )


def generic_func(func, *kargs, **kwargs):
    if is_admin():
        module = __import__("bulkhours_admin", fromlist=[func])
        return getattr(module, func)(*kargs, **kwargs)
    else:
        language = get_value("language")
        IPython.display.display(mock_message(language))


def is_documented_by(func):
    def wrapper(target):
        try:
            module = __import__("bulkhours_admin", fromlist=[func])
            original = getattr(module, func)

            target.__doc__ = original.__doc__
            return target
        except ImportError:
            return target

    return wrapper


@magics_class
class AdminEvaluation(Magics):
    @line_cell_magic
    @needs_local_scope
    def evaluation_cell_id_admin(self, line, cell="", local_ns=None):
        language = get_value("language")
        IPython.display.display(mock_message(language))
        IPython.display.display(
            ipywidgets.Button(
                description="Evaluation non disponible😕" if language == "fr" else "Evaluation not available😕",
                layout=ipywidgets.Layout(width="max-content"),
                disabled=True,
                tooltip=mock_message(language),
            )
        )

        IPython.get_ipython().run_cell(cell)

    @line_cell_magic
    @needs_local_scope
    def update_cell_id_admin(self, *kargs, **kwargs):
        return self.evaluation_cell_id_admin(*kargs, **kwargs)


class AdminMove:
    @staticmethod
    @is_documented_by("summary")
    def summary(*kargs, **kwargs):
        return generic_func("summary", *kargs, **kwargs)

    @staticmethod
    @is_documented_by("get_audio")
    def get_audio(*kargs, **kwargs):
        return generic_func("get_audio", *kargs, **kwargs)

    @is_documented_by("dashboard")
    @staticmethod
    def dashboard(*kargs, **kwargs):
        return generic_func("dashboard", *kargs, **kwargs)

    @staticmethod
    @is_documented_by("evaluate")
    def evaluate(*kargs, **kwargs):
        return generic_func("evaluate", *kargs, **kwargs)
