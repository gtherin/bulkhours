__version__ = "1.8.3"

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
from . import rl


def load_extra_magics(ip, verbose=True):
    from .compiler import CCPPlugin

    ip.register_magics(CCPPlugin(ip))
    ip.register_magics(Evaluation(ip))

    if verbose:
        print(f"Load hpccourse (version={__version__})")


def ipsa_login(student_name=None, ip=None, pass_code=None):

    student_login = set_up_student(student_name, pass_code=pass_code)
    if ip is None:
        set_up_student(None)

    load_extra_magics(ip, verbose=False)
    print(f'Load hpccourse (version={__version__}, connected as "{student_login}")')
