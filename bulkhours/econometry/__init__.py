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

    if label in ["countries", "tourism"]:
        files_list = ["corruption.csv", "cost_of_living.csv", "richest_countries.csv", "unemployment.csv"]
        if label == "tourism":
            files_list += ["tourism.csv"]
    else:
        files_list = [label]

    df = pd.concat([data.get_data(f) for f in files_list], axis=1)
    if "monthly_income" in df.columns:
        del df["monthly_income"]
    return df
