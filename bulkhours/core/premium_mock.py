import IPython
from IPython.core.magic import Magics, magics_class, line_cell_magic, needs_local_scope
import ipywidgets
from .tools import is_premium, get_value


def mock_message(language):
    return (
        "Les fonctionnalités 'premium' ne sont pas disponibles avec votre token😕. Contacter bulkhours@guydegnol.net pour avoir un new token🚀"
        if language == "fr"
        else "The 'premium' functionalities are not available with your token😕. Contact bulkhours@guydegnol.net to have a new token🚀"
    )


def generic_func(func, *kargs, **kwargs):
    language = get_value("language")
    if not is_premium():
        IPython.display.display(mock_message(language))
        return

    try:
        module = __import__("bulkhours_premium", fromlist=[func])
        return getattr(module, func)(*kargs, **kwargs)

    except ImportError:
        IPython.display.display(mock_message(language))


@magics_class
class MockEvaluation(Magics):
    @line_cell_magic
    @needs_local_scope
    def evaluation_cell_id(self, line, cell="", local_ns=None):
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


def is_documented_by(func):
    def wrapper(target):
        try:
            module = __import__("bulkhours_premium", fromlist=[func])
            original = getattr(module, func)

            target.__doc__ = original.__doc__
            return target
        except ImportError:
            return func

    return wrapper


class PremiumMove:
    @staticmethod
    @is_documented_by("ask_chat_gpt")
    def ask_chat_gpt(*kargs, **kwargs):
        return generic_func("ask_chat_gpt", *kargs, **kwargs)

    @staticmethod
    @is_documented_by("ask_dall_e")
    def ask_dall_e(*kargs, **kwargs):
        return generic_func("ask_dall_e", *kargs, **kwargs)

    @staticmethod
    @is_documented_by("is_equal")
    def is_equal(*kargs, **kwargs):
        return generic_func("is_equal", *kargs, **kwargs)
