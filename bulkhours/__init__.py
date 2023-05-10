import os

try:
    import bulkhours_premium
except ImportError:
    print("bulkhours_premium not installed")


from .core.data import get_core_data, get_image  # noqa
from .core.evaluation import Evaluation, set_up_student  # noqa
from .core.logins import clean_student_name  # noqa
from .core.timeit import timeit  # noqa
from .core import geo  # noqa
from .core.geo import geo_plot_country  # noqa
from .core import runrealcmd  # noqa
from .core.gpt import ask_chat_gpt, ask_dall_e  # noqa
from .core.widgets import colors as c  # noqa
from .core import widgets  # noqa
from .core.puppets import *  # noqa
from .core.help import data_help  # noqa


from . import rl  # noqa
from . import hpc  # noqa
from . import ecox  # noqa
from . import beaut  # noqa
from . import boids  # noqa
from . import phyu  # noqa
from .phyu.constants import constants  # noqa
from .phyu.formulas import formulas  # noqa

from .ecox.trading import *  # noqa

econometrics = ecox  # noqa
DEFAULT_TOKEN = "NO_TOKEN"


def load_extra_magics(verbose=True, nid=None, in_french=False, api_key=None):
    from .hpc.compiler import CCPPlugin
    import IPython
    from . import __version__

    ipp = IPython.get_ipython()
    if ipp:
        ipp.register_magics(CCPPlugin(ipp))
        ipp.register_magics(Evaluation(ipp, nid, in_french, api_key))

    if verbose:
        print(f"ENV BULK Helper cOURSe (version={__version__.__version__})")


def init_env(
    login=None,
    pass_code=None,
    env=None,
    verbose=False,
    in_french=False,
    nid=None,
    promo=None,
    api_key=DEFAULT_TOKEN,
    atoken=DEFAULT_TOKEN,
    mtoken=DEFAULT_TOKEN,
):
    student_login = set_up_student(login, pass_code=pass_code)

    load_extra_magics(verbose=False, nid=nid, in_french=in_french, api_key=api_key)

    if env in ["rl", "reinforcement learning"]:
        rl.init_env(verbose=verbose)
    set_style()
    vfile = os.path.abspath(os.path.dirname(__file__)) + "/__version__.py"
    versions = open(vfile).readlines()
    version, aversion, mversion = [versions[i].split('"')[1] for i in range(3)]

    info = f"Import BULK Helper cOURSe (user='{student_login}', id='{nid}', \x1b[0mversion='{version}'"
    if env is not None:
        info += f", env='{env}'"

    if atoken != DEFAULT_TOKEN:
        info = f"\x1b[31m{info},\x1b[0m \x1b[36mpversion='{mversion}'\x1b[0m🚀, \x1b[31maversion='{aversion}'\x1b[0m⚠️"
    elif mtoken != DEFAULT_TOKEN:
        info = f"{info}, \x1b[36mpversion='{mversion}'\x1b[0m🚀"
    else:
        info = f"{info}, \x1b[36m. To activate the 🚀 mode, please contact bulkhours@guydegnol.net\x1b[0m"

    print(f"{info})")


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


def get_config(directory=None):
    import json

    directory = os.path.dirname(__file__) + "/../" if directory is None else directory

    jsonfile = directory + "/.safe"
    if os.path.exists(jsonfile):
        with open(jsonfile) as json_file:
            return json.load(json_file)

    return {}


def init(verbose=False):
    kwargs = get_config()
    if len(kwargs) > 1:
        init_env(verbose=verbose, **kwargs)


init()
