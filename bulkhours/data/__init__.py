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
from .data_parser import DataParser  # noqa


def get_data(label, **kwargs):
    DataParser.build_clean_datasets()

    data_info = (
        {**DataParser.clean_datasets[label], **kwargs}
        if label in DataParser.clean_datasets
        else {"raw_data": label, **kwargs}
    )

    return DataParser(**data_info).get_data()


def get_image(label, ax=None):
    return DataParser(label=label).get_image(ax=ax)


def geo_plot(label=None, timeopt="last", **kwargs):
    """
    data: geopandas dataframe (world.mappoverty)
    timeopt: year the estimation (last by default)
    """

    from ..core import geo  # noqa

    df = get_data(label, timeopt=timeopt) if type(label) is str else label
    return geo.geo_plot(data=df, timeopt=timeopt, **kwargs)
