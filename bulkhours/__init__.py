import IPython

from . import core  # noqa
from .core.tools import get_config, get_value  # noqa
from .core.timeit import timeit  # noqa
from .core import tools  # noqa
from .core.tools import html2 as html  # noqa

# from . import data  # noqa
from .data import get_data, get_image, geo_plot  # noqa

from .core.gpt import ask_chat_gpt, ask_dall_e  # noqa
from .core.equals import is_equal  # noqa

from .core import colors as c  # noqa

from .core import installer  # noqa
from . import admin  # noqa
from . import rl  # noqa
from . import hpc  # noqa
from . import ecox  # noqa
from . import beaut  # noqa
from . import boids  # noqa
from . import phyu  # noqa
from .phyu.constants import constants  # noqa
from .phyu.formulas import formulas  # noqa

from .ecox.trading import *  # noqa

from .core.logins import init_env  # noqa

if ipp := IPython.get_ipython():
    from .core.evaluation import Evaluation
    from .hpc.compiler import CCPPlugin

    ipp.register_magics(CCPPlugin(ipp))
    ipp.register_magics(Evaluation(ipp))


def generate_header_links(filename):
    import IPython

    IPython.display.display(
        IPython.display.Markdown(
            f"""[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/guydegnol/bulkhours/blob/main/{filename}) [![Open In Kaggle](https://kaggle.com/static/images/open-in-kaggle.svg)](https://kaggle.com/kernels/welcome?src=https://github.com/guydegnol/bulkhours/blob/main/{filename}) [![GitHub](https://badgen.net/badge/icon/Open%20in%20Github?icon=github&label)](https://github.com/guydegnol/bulkhours/blob/main/{filename}) [![Open in Visual Studio Code](https://img.shields.io/static/v1?logo=visualstudiocode&label=&message=Open%20in%20Visual%20Studio&labelColor=2c2c32&color=007acc&logoColor=007acc)](https://vscode.dev/github/guydegnol/bulkhours/blob/main/{filename}) [![CC-0 license](https://img.shields.io/badge/License-CC--0-blue.svg)](https://creativecommons.org/licenses/by-nd/4.0)"""
        )
    )
