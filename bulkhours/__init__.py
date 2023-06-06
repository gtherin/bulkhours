import os
import datetime

from .core.data import get_core_data, get_image  # noqa
from .core.tools import is_premium, is_admin, get_config, get_value  # noqa
from .core.timeit import timeit  # noqa
from .core import geo  # noqa
from .core.geo import geo_plot_country  # noqa
from .core import runrealcmd  # noqa
from .core.premium_mock import PremiumMove as premium  # noqa

ask_chat_gpt = premium.ask_chat_gpt  # noqa
ask_dall_e = premium.ask_dall_e  # noqa
is_equal = premium.is_equal  # noqa

from .core import colors as c  # noqa
from .core.help import data_help  # noqa

from .core.admin_mock import AdminMove as admin  # noqa
from .core import installer  # noqa
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


def init_env(debug=False, **kwargs):
    import IPython

    info = f"Import BULK Helper cOURSe ("

    config = get_config(do_update=True, **kwargs)

    if is_premium(debug=debug):
        from bulkhours_premium import init_prems

        info = init_prems(info)

    stime = (
        datetime.datetime.now() + datetime.timedelta(seconds=3600)
        if os.path.exists("/content")
        else datetime.datetime.now()
    )

    if config.get("notebook_id") is not None:
        info += f"nb_id='{config.get('notebook_id')}', "

    if ipp := IPython.get_ipython():
        from .hpc.compiler import CCPPlugin

        ipp.register_magics(CCPPlugin(ipp))

        if is_premium():
            from bulkhours_premium import Evaluation

            ipp.register_magics(Evaluation(ipp))
        else:
            from .core.premium_mock import MockEvaluation

            ipp.register_magics(MockEvaluation(ipp))

        if is_admin(debug=debug):
            from bulkhours_admin import SudoEvaluation

            ipp.register_magics(SudoEvaluation(ipp))

        else:
            from .core.admin_mock import AdminEvaluation

            ipp.register_magics(AdminEvaluation(ipp))

    if "packages" in config:
        installer.install_dependencies(config["packages"])

    set_style()
    vfile = os.path.abspath(os.path.dirname(__file__)) + "/__version__.py"
    versions = open(vfile).readlines()
    version, aversion, mversion = [versions[i].split('"')[1] for i in range(3)]

    info += f"\x1b[0mversion='{version}'"

    info += ", time='%s'" % stime.strftime("%H:%M:%S")
    if is_admin():
        info = f"\x1b[31m{info},\x1b[0m \x1b[36mpremium='{mversion}'\x1b[0m🚀, \x1b[31madmin='{aversion}'\x1b[0m⚠️\x1b[41m\x1b[37mfor teachers only🎓\x1b[0m)"
    elif is_premium():
        info = f"{info}, \x1b[36mpversion='{mversion}'\x1b[0m🚀)"
    else:
        info = f"{info})\x1b[36m. To activate the 🚀 mode, please contact bulkhours@guydegnol.net\x1b[0m"

    print(f"{info}")
    os.environ["BLK_STATUS"] = f"INITIALIZED"


def get_color(discipline):
    colors = {"swimming": "#581845", "cycling": "#C70039", "running": "#FF5733", "axis": "#4F77AA"}
    return colors[discipline] if discipline in colors else "black"


def set_style():
    import matplotlib.pyplot as plt

    background_color = "#F0FDFA11"  # cdcdcd
    axis_color = "#4F77AA"  # cdcdcd

    def get_color(discipline):
        colors = {"swimming": "#581845", "cycling": "#C70039", "running": "#FF5733", "axis": "#4F77AA"}
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


# init_env()


def html(label, display=True, style="raw"):
    import IPython

    if style == "title":
        data = IPython.display.HTML(f"<b><font face='FiraCode Nerd Font' size=6 color='black'>{label}<font></b>")
    else:
        data = IPython.display.HTML(label)
    if display:
        IPython.display.display(data)
