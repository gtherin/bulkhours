from . import tools  # noqa

from .statsdata import *  # noqa
from .trading import *  # noqa
from .france import *  # noqa
from .gmacro import *  # noqa
from .mincer import *  # noqa
from .world import *  # noqa

from .help import build_readme, help  # noqa
from .datasets import datasets, ddatasets, datacategories  # noqa


def get_data(label, **kwargs):
    data_info = {**ddatasets[label], **kwargs} if label in ddatasets else {"raw_data": label, **kwargs}
    return tools.DataParser(**data_info).get_data()


def get_image(label, ax=None):
    return tools.DataParser(label=label).get_image(ax=ax)
