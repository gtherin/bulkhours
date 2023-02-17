from .statsdata import *  # noqa
from .brownian import plot_brownian_sample  # noqa
from .gallery import *  # noqa
from . import regression  # noqa
from . import gradient  # noqa
from . import france  # noqa
from . import fhgdpq  # noqa
from . import statsdata  # noqa
from . import mincer  # noqa
import scipy as sp

from .block import Block, BlockCoin, BlockMsg  # noqa
from .blockchain import BlockChain  # noqa


modules = {"france": france, "mincer": mincer, "statsdata": statsdata, "fhgdpq": fhgdpq}


def get_scipy_distributions_list():
    return [d for d in dir(sp.stats._continuous_distns) if not d in ["levy_stable", "studentized_range"]]


def clean_life_expectancy_vs_gdp_2018(df):
    df = df.dropna().query("Year == 2018 and Population > 1e7")
    df["GDP per capita ($, log)"] = np.log(df["GDP per capita ($)"])
    return df


datasets = {
    "countries": dict(
        files_list=[
            "corruption.csv",
            "cost_of_living.csv",
            "richest_countries.csv",
            "unemployment.csv",
            "continent.tsv",
        ],
        drop=["monthly_income"],
        on="country",
    ),
    "scipy_distributions_list": dict(drop=get_scipy_distributions_list),
    "tourism": dict(
        files_list=[
            "corruption.csv",
            "cost_of_living.csv",
            "richest_countries.csv",
            "unemployment.csv",
            "tourism.csv",
            "continent.tsv",
        ],
        drop=["monthly_income"],
        on="country",
    ),
    "life_expectancy_vs_gdp_2018": dict(
        files_list=["life-expectancy-vs-gdp-per-capita.csv"],
        info="GDP per capita is measured in 2011 international dollars, which corrects for inflation and cross-country price differences",
        filter=clean_life_expectancy_vs_gdp_2018,
        rename=[
            "Country",
            "Code",
            "Year",
            "Life expectancy (years)",
            "GDP per capita ($)",
            "annotations",
            "Population",
            "Continent",
        ],
        drop=["annotations", "Continent"],
    ),
}


def random(samples_number, sample_size, mu=4, distrib="bimodal", seed=42):
    """return a dataframe of exp(-X/scale)/scale for random X"""
    np.random.seed(seed)
    if distrib == "exp":
        return pd.DataFrame(np.random.exponential(scale=mu, size=(sample_size, samples_number)))
    u = np.random.choice([0, 1], size=(sample_size, samples_number))
    d1 = sp.stats.skewnorm.rvs(loc=mu - 3.6, a=7, size=(sample_size, samples_number))
    d2 = sp.stats.skewnorm.rvs(loc=mu, a=7, size=(sample_size, samples_number))
    return pd.DataFrame(u * d1 + 0.5 * (1 - u) * d2)


def sampler(samples_number, sample_size, **kwargs):
    return random(samples_number, sample_size, **kwargs)
