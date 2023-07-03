from os.path import dirname, basename, isfile, join
import glob

modules = glob.glob(join(dirname(__file__), "*.py"))
modules = [
    basename(f)[:-3]
    for f in modules
    if isfile(f) and basename(f)[:-3] not in ["data_parser", "__init__", "help", "datasets"]
]
__all__ = modules
from . import *
from .help import build_readme, help, generate_header_links  # noqa


def get_data(label, **kwargs):
    from .data_parser import DataParser  # noqa

    DataParser.build_clean_datasets()

    data_info = (
        {**DataParser.clean_datasets[label], **kwargs}
        if label in DataParser.clean_datasets
        else {"raw_data": label, **kwargs}
    )

    return DataParser(**data_info).get_data()


def get_image(label, ax=None):
    from .data_parser import DataParser  # noqa

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
