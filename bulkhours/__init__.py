__version__ = "1.8.4"

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
    elif env is not None:
        rl.runrealcmd("pip install yfinance", verbose=True)
    elif env is not None:
        print(f"Unknown env={env}")

    print(f'Load BULK Helper cOURSe (version={__version__}, connected as "{student_login}{env_info}")')


def student_login(login=None, ip=None, pass_code=None):

    student_login = set_up_student(login, pass_code=pass_code)
    if ip is None:
        set_up_student(None)

    load_extra_magics(ip, verbose=False)
    print(f'Load bulkhours (version={__version__}, connected as "{student_login}")')
