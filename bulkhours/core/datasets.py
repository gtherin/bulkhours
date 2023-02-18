import numpy as np
import scipy as sp


def get_scipy_distributions_list():
    return [d for d in dir(sp.stats._continuous_distns) if not d in ["levy_stable", "studentized_range"]]


def clean_life_expectancy_vs_gdp_2018(df):
    df = df.dropna().query("Year == 2018 and Population > 1e7")
    df["GDP per capita ($, log)"] = np.log(df["GDP per capita ($)"])
    return df


datasets = {
    "vaccinations": dict(
        httplink="https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/vaccinations/vaccinations.csv",
        source="https://ourworldindata.org/coronavirus",
    ),
    "covid": dict(
        httplink="https://covid.ourworldindata.org/data/owid-covid-data.csv",
        source="https://ourworldindata.org/coronavirus",
    ),
    "poverty": dict(
        httplink="https://nyc3.digitaloceanspaces.com/owid-public/data/poverty/pip_dataset.csv",
        source="""World Bank Poverty and Inequality Platform
- Direct source: https://ourworldindata.org/poverty
- Info on the columns: https://github.com/owid/poverty-data/blob/main/datasets/pip_codebook.csv
- Data source: https://pip.worldbank.org/
        """,
    ),
    "supercomputers": dict(
        httplink="https://raw.githubusercontent.com/owid/owid-datasets/dd7a4ecbb249f98028e25c304ef7d68de8979ea9/datasets/Supercomputer%20power%20(FLOPS)%20%E2%80%93%20TOP500%20Database/Supercomputer%20power%20(FLOPS)%20%E2%80%93%20TOP500%20Database.csv",
        source="https://ourworldindata.org/grapher/supercomputer-power-flops",
    ),
    "scipy_distributions_list": dict(drop=get_scipy_distributions_list),
    "macro": dict(
        files_list=[
            "corruption.csv",
            "cost_of_living.csv",
            "richest_countries.csv",
            "unemployment.csv",
            "tourism.csv",
            "continent.tsv",
        ],
        drop=["monthly_income", "continent"],
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
