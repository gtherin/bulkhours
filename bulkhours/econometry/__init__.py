from .statsdata import *  # noqa
from .brownian import plot_brownian_sample  # noqa
from .gallery import *  # noqa
from .income import get_fr_income  # noqa


def get_list_of_distribs():

    import scipy as sp

    return [d for d in sp.stats._continuous_distns if not d in ["levy_stable", "studentized_range"]]


def clean_columns(df, rename=None, drop=None):
    if rename:
        df.columns = ['Code', 'Year', 'Life expectancy', 'GDP', 'annotations', 'Population', 'Continent']
    if drop:
        for c in drop:
            del df[c]

    return df

def get_data(label):
    """
    countries: World Economic Data from kaggle

    """

    from ..core import data

    if label in ["countries", "tourism"]:
        files_list = ["corruption.csv", "cost_of_living.csv", "richest_countries.csv", "unemployment.csv"]
        if label == "tourism":
            files_list += ["tourism.csv"]
    elif label == "life_expectancy_vs_gdp_2018":
        files_list = ["life-expectancy-vs-gdp-per-capita.csv"]
    else:
        files_list = [label]

    df = pd.concat([data.get_data(f) for f in files_list], axis=1)
    if "monthly_income" in df.columns:
        del df["monthly_income"]

    if label == "life_expectancy_vs_gdp_2018":
        df = clean_columns(df, rename=['Code', 'Year', 'Life expectancy', 'GDP per capita', 'annotations', 'Population', 'Continent'], drop=["annotations", "Continent"])
        df = df.dropna().query("Year == 2018 and Population > 1e7")

    return df
