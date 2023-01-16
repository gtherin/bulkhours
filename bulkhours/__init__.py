__version__ = "2.0.0"

from .block import Block, BlockCoin, BlockMsg  # noqa
from .blockchain import BlockChain  # noqa
from .evaluation import Evaluation, set_up_student  # noqa
from .flops import *  # noqa
from .languages import get_languages_perf  # noqa
from .pycker import *  # noqa
from .git_graph import *  # noqa
from .git_graphviz import *  # noqa
from .timeit import timeit  # noqa
from .ffiles import *  # noqa
from . import rl  # noqa
from . import econometry  # noqa


def load_extra_magics(ip, verbose=True):
    from .compiler import CCPPlugin

    ipp = ip.get_ipython()

    ipp.register_magics(CCPPlugin(ipp))
    ipp.register_magics(Evaluation(ipp))

    if verbose:
        print(f"Load bulkhours (version={__version__})")


def init_env(login=None, ip=None, pass_code=None, env=None):
    import importlib

    student_login = set_up_student(login, pass_code=pass_code)
    if ip is None:
        set_up_student(None)

    if ip is not None:
        load_extra_magics(ip, verbose=False)

    env_info = ""
    if env in ["rl", "reinforcement learning"]:
        rl.init_env(ip)
        env_info = f", in env=rl"
    elif env in ["econometry"]:
        rl.runrealcmd("pip install yfinance", verbose=True)
        env_info = f", in env=econometry"
    elif env is not None:
        print(f"Unknown env={env}")

    set_style()
    print(f'Load BULK Helper cOURSe (version={__version__}, connected as "{student_login}{env_info}")')


def get_data(label):

    import glob

    filename = None
    for directory in [f"bulkhours/data", f"./data", f"../data"]:
        if len((files := glob.glob(f"{directory}/{label}*"))):
            filename = files[0]
    if not filename:
        print(f"No data available for {label}")
        return None

    ext = filename.split(".")[-1]
    if ext == "tsv":
        df = pd.read_csv(filename, sep="\t")
    else:
        df = pd.read_csv(filename)
    df = df.set_index(df.columns[0])

    return df


def get_color(discipline):
    colors = {
        "swimming": "#581845",
        "cycling": "#C70039",
        "running": "#FF5733",
        "axis": "#4F77AA",
    }
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
    # mpl.rcParams['axes.prop_cycle'] = cycler(color='bgrcmyk')
    plt.rcParams["axes.prop_cycle"] = cycler(
        color=[get_color(c) for c in ["swimming", "cycling", "running", "The end"]]
    )
