import IPython

from . import core  # noqa
from .core.tools import get_config, get_value  # noqa
from .core.timeit import timeit  # noqa
from .core import tools  # noqa
from .core.tools import html  # noqa

# from . import data  # noqa
from .data import get_data, get_image, geo_plot, generate_header_links, DataParser  # noqa

from .core.gpt import ask_chat_gpt, ask_dall_e  # noqa
from .core.equals import is_equal  # noqa

from .core import colors as c  # noqa

from .core import installer  # noqa
from . import admin  # noqa
from . import ml  # noqa
from . import hpc  # noqa
from . import ecox  # noqa
from . import bots  # noqa
from .bots import beaut  # noqa
from .bots import boids  # noqa
from . import phyu  # noqa
from .phyu.constants import constants  # noqa
from .phyu.formulas import formulas  # noqa
from . import math  # noqa

from .ecox.trading import *  # noqa

from .core.logins import init_env  # noqa
from .core.tools import dmd  # noqa

if ipp := IPython.get_ipython():
    from .core.evaluation import Evaluation
    from .hpc.compiler import CCPPlugin

    ipp.register_magics(CCPPlugin(ipp))
    ipp.register_magics(Evaluation(ipp))

