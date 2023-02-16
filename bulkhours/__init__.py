import os

from .core.evaluation import Evaluation, set_up_student, send_answer_to_corrector, get_solution_from_corrector  # noqa
from .core.data import get_core_data, get_image  # noqa
from .core.timeit import timeit  # noqa
from .core import runrealcmd  # noqa
from . import rl  # noqa
from . import hpc  # noqa
from . import ecox  # noqa
from . import beaut  # noqa
from . import boids  # noqa
from . import phyu  # noqa

econometrics = ecox  # noqa


def load_extra_magics(verbose=True):
    from .hpc.compiler import CCPPlugin
    import IPython as ip
    from . import __version__

    ipp = ip.get_ipython()

    ipp.register_magics(CCPPlugin(ipp))
    ipp.register_magics(Evaluation(ipp))

    if verbose:
        print(f"ENV BULK Helper cOURSe (version={__version__.__version__})")


def init_env(login=None, pass_code=None, env=None, verbose=False):
    student_login = set_up_student(login, pass_code=pass_code)

    load_extra_magics(verbose=False)

    env_info = ""
    if env in ["rl", "reinforcement learning"]:
        rl.init_env(verbose=verbose)
        env_info = f", env=rl"
    elif env in ["econometrics", "ecox"]:
        runrealcmd("pip install yfinance  # Data loader for finance data", verbose=verbose)
        env_info = f", env=econometrics"
    elif env is not None:
        print(f"env={env} (Unknown)")
    set_style()
    vfile = os.path.abspath(os.path.dirname(__file__)) + "/__version__.py"
    version = open(vfile).readline().split('"')[1]

    print(f"ENV BULK Helper cOURSe (version={version}, user={student_login}{env_info})")


def get_color(discipline):
    colors = {"swimming": "#581845", "cycling": "#C70039", "running": "#FF5733", "axis": "#4F77AA"}
    return colors[discipline] if discipline in colors else "black"


def set_style():
    import matplotlib.pyplot as plt

    background_color = "#F0FDFA11"  # cdcdcd

    def get_color(discipline):
        colors = {
            "swimming": "#581845",
            "cycling": "#C70039",
            "running": "#FF5733",
            "axis": "#4F77AA",
        }
        return colors[discipline] if discipline in colors else "black"

    plt.rcParams["axes.grid"] = True
    plt.rcParams["axes.edgecolor"] = get_color("axis")
    plt.rcParams["axes.labelcolor"] = get_color("axis")
    plt.rcParams["axes.titlecolor"] = get_color("axis")
    plt.rcParams["axes.facecolor"] = background_color
    plt.rcParams["figure.edgecolor"] = get_color("axis")
    plt.rcParams["figure.facecolor"] = background_color
    plt.rcParams["grid.color"] = "white"
    plt.rcParams["legend.facecolor"] = background_color
    plt.rcParams["legend.edgecolor"] = background_color
    plt.rcParams["xtick.color"] = get_color("axis")
    plt.rcParams["ytick.color"] = get_color("axis")

    plt.rcParams["font.size"] = 14
    plt.rcParams["lines.linewidth"] = 4

    # ax.grid(True, axis="y", color="white")

    from cycler import cycler

    # mpl.rcParams['axes.prop_cycle'] = cycler(color='bgrcmyk')
    plt.rcParams["axes.prop_cycle"] = cycler(
        color=[get_color(c) for c in ["swimming", "cycling", "running", "The end"]]
    )


def get_data(label, **kwargs):
    return get_core_data(label, datasets=ecox.datasets, modules=ecox.modules, **kwargs)
