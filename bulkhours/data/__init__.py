from .statsdata import *  # noqa
from .trading import *  # noqa
from .france import *  # noqa
from .gmacro import *  # noqa
from .mincer import *  # noqa
from .world import *  # noqa

from .help import build_readme, help  # noqa
from .datasets import datasets, ddatasets, datacategories  # noqa


def get_data(label, **kwargs):
    from .tools import DataParser  # noqa

    data_info = {**ddatasets[label], **kwargs} if label in ddatasets else {"raw_data": label, **kwargs}
    return DataParser(**data_info).get_data()


def get_image(label, ax=None):
    from .tools import DataParser  # noqa

    return DataParser(label=label).get_image(ax=ax)


def geo_plot(label=None, timeopt="last", **kwargs):
    """
    data: geopandas dataframe (world.mappoverty)
    timeopt: year the estimation (last by default)
    """

    from ..core import geo  # noqa

    if type(label) is str:
        df = get_data(label, timeopt=timeopt)
    else:
        df = label
    return geo.geo_plot(data=df, timeopt=timeopt, **kwargs)
