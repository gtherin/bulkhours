import IPython

from . import core  # noqa
from .core.tools import get_config, get_value  # noqa
from .core.timeit import timeit  # noqa
from .core import tools  # noqa
from .core.tools import html  # noqa
from .math import ma325
from . import sport  # noqa

# from . import data  # noqa
from .data import (
    get_data,
    download_data,
    get_image,
    geo_plot,
    generate_header_links,
    DataParser,
)  # noqa

from .core.gpt import ask_gpt  # noqa
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

from .core.logins import init_env, init_from_token  # noqa
from .core.tools import dmd  # noqa
from .core.black import format_with_black  # noqa

if ipp := IPython.get_ipython():
    from .core.evaluation import Evaluation
    from .core.black import Black
    from .hpc.compiler import CCPPlugin

    ipp.register_magics(CCPPlugin(ipp))
    ipp.register_magics(Evaluation(ipp))
    ipp.register_magics(Black(ipp))
