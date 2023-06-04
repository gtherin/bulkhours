import IPython
from IPython.core.magic import Magics, magics_class, line_cell_magic, needs_local_scope
import ipywidgets
from .tools import is_premium


def mock_message(in_french):
    return (
        "Les fonctionnalités 'premium' ne sont pas disponibles avec votre token😕. Contacter bulkhours@guydegnol.net pour avoir un new token🚀"
        if in_french
        else "The 'premium' functionalities are not available with your token😕. Contact bulkhours@guydegnol.net to have a new tokeneee🚀"
    )


def generic_func(func, *kargs, **kwargs):
    from .tools import get_value

    in_french = get_value("in_french")
    print(is_premium())

    if not is_premium():
        IPython.display.display(mock_message(in_french))
        return

    try:
        module = __import__("bulkhours_premium", fromlist=[func])
        return getattr(module, func)(*kargs, **kwargs)

    except ImportError:
        IPython.display.display(mock_message(in_french))


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
