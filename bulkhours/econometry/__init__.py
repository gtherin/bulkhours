from .statsdata import *  # noqa
from .brownian import plot_brownian_sample  # noqa
from .gallery import *  # noqa
from .income import get_fr_income  # noqa


def get_list_of_distribs():

    import scipy as sp

    return [d for d in sp.stats._continuous_distns if not d in ["levy_stable", "studentized_range"]]


def get_data(label):
    """
    countries: World Economic Data from kaggle

    """

    from ..core import data

    if label == "countries":
        return pd.concat(
            [data.get_data(f"{f}.csv") for f in ["corruption", "cost_of_living", "richest_countries", "unemployment"]],
            axis=1,
        )
    else:
        return data.get_data(label)
