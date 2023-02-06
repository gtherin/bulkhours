from .statsdata import *  # noqa
from .brownian import plot_brownian_sample  # noqa
from .gallery import *  # noqa
from . import regression  # noqa
from . import gradient  # noqa
from . import france  # noqa
from . import fhgdpq  # noqa
from . import statsdata  # noqa
from . import mincer  # noqa

modules = {"france": france, "mincer": mincer, "statsdata": statsdata, "fhgdpq": fhgdpq}


def get_list_of_distribs():
    import scipy as sp

    return [d for d in sp.stats._continuous_distns if not d in ["levy_stable", "studentized_range"]]


def clean_life_expectancy_vs_gdp_2018(df):
    df = df.dropna().query("Year == 2018 and Population > 1e7")
    df["GDP per capita ($, log)"] = np.log(df["GDP per capita ($)"])
    return df


datasets = {
    "countries": dict(
        files_list=["corruption.csv", "cost_of_living.csv", "richest_countries.csv", "unemployment.csv"],
        drop=["monthly_income"],
    ),
    "tourism": dict(
        files_list=["corruption.csv", "cost_of_living.csv", "richest_countries.csv", "unemployment.csv", "tourism"],
        drop=["monthly_income"],
    ),
    "life_expectancy_vs_gdp_2018": dict(
        files_list=["life-expectancy-vs-gdp-per-capita.csv"],
        info="GDP per capita is measured in 2011 international dollars, which corrects for inflation and cross-country price differences.",
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
