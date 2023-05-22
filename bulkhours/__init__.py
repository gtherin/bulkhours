import os
from .core.data import get_core_data, get_image  # noqa
from .core.tools import is_premium, is_admin, get_config, get_value  # noqa
from .core.timeit import timeit  # noqa
from .core import geo  # noqa
from .core.geo import geo_plot_country  # noqa
from .core import runrealcmd  # noqa
from .core.gpt import ask_chat_gpt, ask_dall_e  # noqa
from .core import colors as c  # noqa
from .core.help import data_help  # noqa
from .core import admin_mock as admin  # noqa


from . import rl  # noqa
from . import hpc  # noqa
from . import ecox  # noqa
from . import beaut  # noqa
from . import boids  # noqa
from . import phyu  # noqa
from .phyu.constants import constants  # noqa
from .phyu.formulas import formulas  # noqa

from .ecox.trading import *  # noqa


DEFAULT_TOKEN = "NO_TOKEN"


def load_extra_magics(
    nid=None,
    in_french=False,
    openai_token=DEFAULT_TOKEN,
    premium_token=DEFAULT_TOKEN,
    admin_token=DEFAULT_TOKEN,
):
    from .hpc.compiler import CCPPlugin
    import IPython
    from . import __version__

    ipp = IPython.get_ipython()
    if ipp:
        ipp.register_magics(CCPPlugin(ipp))
        if is_premium(premium_token):
            from bulkhours_premium import Evaluation

            ipp.register_magics(Evaluation(ipp, nid, in_french, openai_token))
        else:
            from .core.premium_mock import MockEvaluation

            ipp.register_magics(MockEvaluation(ipp, nid, in_french, openai_token))

        if is_admin(admin_token):
            from bulkhours_admin import SudoEvaluation

            ipp.register_magics(SudoEvaluation(ipp, nid, in_french, openai_token))


def init_env(
    login=None,
    db_token=None,
    env=None,
    verbose=False,
    in_french=False,
    nid=None,
    promo=None,
    openai_token=DEFAULT_TOKEN,
    admin_token=DEFAULT_TOKEN,
    premium_token=DEFAULT_TOKEN,
):
    info = f"Import BULK Helper cOURSe ("

    if premium_token != DEFAULT_TOKEN and is_premium(premium_token):
        from bulkhours_premium import set_up_student

        student_login = set_up_student(login, db_token=db_token)
        is_known_student = "✅" if 1 else "❌"
        info += f"user='{student_login}'{is_known_student}, "

        if promo is not None:
            info += f"class='{promo}', "

    if nid is not None:
        info += f"id='{nid}', "

    load_extra_magics(
        nid=nid, in_french=in_french, openai_token=openai_token, premium_token=premium_token, admin_token=admin_token
    )

    if env in ["rl", "reinforcement learning"]:
        rl.init_env(verbose=verbose)
    set_style()
    vfile = os.path.abspath(os.path.dirname(__file__)) + "/__version__.py"
    versions = open(vfile).readlines()
    version, aversion, mversion = [versions[i].split('"')[1] for i in range(3)]

    info += f"\x1b[0mversion='{version}'"
    if env is not None:
        info += f", env='{env}'"

    if admin_token != DEFAULT_TOKEN:
        info = f"\x1b[31m{info},\x1b[0m \x1b[36mpremium_ver='{mversion}'\x1b[0m🚀, \x1b[31madmin_ver='{aversion}'\x1b[0m⚠️\x1b[41m\x1b[37mfor teachers only\x1b[0m)"
    elif premium_token != DEFAULT_TOKEN:
        info = f"{info}, \x1b[36mpversion='{mversion}'\x1b[0m🚀)"
    else:
        info = f"{info})\x1b[36m. To activate the 🚀 mode, please contact bulkhours@guydegnol.net\x1b[0m"

    print(f"{info}")


def get_color(discipline):
    colors = {"swimming": "#581845", "cycling": "#C70039", "running": "#FF5733", "axis": "#4F77AA"}
    return colors[discipline] if discipline in colors else "black"


def set_style():
    import matplotlib.pyplot as plt

    background_color = "#F0FDFA11"  # cdcdcd
    axis_color = "#4F77AA"  # cdcdcd

    def get_color(discipline):
        colors = {
            "swimming": "#581845",
            "cycling": "#C70039",
            "running": "#FF5733",
            "axis": "#4F77AA",
        }
        return colors[discipline] if discipline in colors else "black"

    plt.rcParams["axes.grid"] = True
    plt.rcParams["axes.edgecolor"] = axis_color
    plt.rcParams["axes.labelcolor"] = axis_color
    plt.rcParams["axes.titlecolor"] = axis_color
    plt.rcParams["axes.facecolor"] = background_color
    plt.rcParams["figure.edgecolor"] = axis_color
    plt.rcParams["figure.facecolor"] = background_color
    plt.rcParams["grid.color"] = "white"
    plt.rcParams["legend.facecolor"] = background_color
    plt.rcParams["legend.edgecolor"] = background_color
    plt.rcParams["xtick.color"] = axis_color
    plt.rcParams["ytick.color"] = axis_color

    plt.rcParams["font.size"] = 14
    plt.rcParams["lines.linewidth"] = 4

    # ax.grid(True, axis="y", color="white")

    from cycler import cycler

    # mpl.rcParams['axes.prop_cycle'] = cycler(color='bgrcmyk')
    plt.rcParams["axes.prop_cycle"] = cycler(
        color=[get_color(c) for c in ["swimming", "cycling", "running", "The end"]]
    )


def get_data(label, **kwargs):
    return get_core_data(label, modules=ecox.modules, **kwargs)


def geo_plot(data=None, timeopt="last", **kwargs):
    """
    data: geopandas dataframe (world.mappoverty)
    timeopt: year the estimation (last by default)
    """
    if type(data) is str:
        data = get_data(data, timeopt=timeopt)
    return geo.geo_plot(data, timeopt=timeopt, **kwargs)


def init(verbose=False):
    kwargs = get_config()
    if len(kwargs) > 1:
        init_env(verbose=verbose, **kwargs)


init()
