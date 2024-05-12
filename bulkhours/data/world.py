import pandas as pd
import numpy as np

from .data_parser import DataParser


def get_mapgeneric(df):
    import geopandas as gpd

    if "continent" in df.columns:
        del df["continent"]

    df = df.rename(columns={"Country": "country"})
    df["country"] = df["country"].str.replace("United States", "United States of America")
    df["country"] = df["country"].str.replace("Democratic Republic of Congo", "Dem. Rep. Congo")

    filepath = gpd.datasets.get_path("naturalearth_lowres")
    world = gpd.read_file(filepath)

    # world = gpd.read_file(gpd.datasets.get_path(""))

    world = world[(world.pop_est > 0) & (world.name != "Antarctica")]
    # world[world.continent == 'South America']
    return world.merge(df.set_index("country"), how="left", left_on="name", right_index=True)


def geo_format(df, timeopt):
    cont = DataParser.get_data_from_file("continent.tsv")
    df = df.merge(cont, how="left", on="country")

    df["country"] = df["country"].str.replace("United States", "United States of America")
    df["country"] = df["country"].str.replace("Democratic Republic of Congo", "Dem. Rep. Congo")

    if type(timeopt) == int:
        df = df[df["year"] <= timeopt]
    if timeopt == "first":
        df = df[df.groupby("country")["year"].rank(method="dense", ascending=True) == 1.0]
    if timeopt == "last" or type(timeopt) == int:
        df = df[df.groupby("country")["year"].rank(method="dense", ascending=False) == 1.0]
    if timeopt:
        df = df.groupby(["country", "year"]).mean(numeric_only=True).reset_index()

    return df


@DataParser.register_dataset(
    label="world.poverty",
    summary="World Bank Poverty and Inequality data",
    category="Economics",
    raw_data="https://nyc3.digitaloceanspaces.com/owid-public/data/poverty/pip_dataset.csv",
    ref_source="https://ourworldindata.org/poverty",
    ref_site="""https://pip.worldbank.org/""",
    enrich_data="https://github.com/gtherin/bulkhours/blob/main/bulkhours/data/world.py",
    columns_info="https://github.com/owid/poverty-data/blob/main/datasets/pip_codebook.csv",
)
def get_poverty(self, timeopt=None):
    timeopt = self.data_info["timeopt"] if "timeopt" in self.data_info else None
    df = self.read_raw_data(self.raw_data)
    return geo_format(df, timeopt)


@DataParser.register_dataset(
    label="world.mappoverty",
    summary="World Bank Poverty and Inequality data (with gpx extra info)",
    reference="world.poverty",
)
def get_mappoverty(self, **kwargs):
    return get_mapgeneric(get_poverty(self, **kwargs))


@DataParser.register_dataset(
    label="world.gdp",
    summary="World Bank Gdp data",
    category="Economics",
    raw_data="https://nyc3.digitaloceanspaces.com/owid-public/data/poverty/pip_dataset.csv",
    ref_source="https://ourworldindata.org/poverty",
    ref_site="""https://pip.worldbank.org/""",
    # drop=["Country Code", "Indicator Name", "Indicator Code", "Unnamed: 66"]
    enrich_data="https://github.com/gtherin/bulkhours/blob/main/bulkhours/data/world.py",
    columns_info="https://github.com/owid/poverty-data/blob/main/datasets/pip_codebook.csv",
)
def get_gdp(self, timeopt=None, **data_info):
    timeopt = self.data_info["timeopt"] if "timeopt" in self.data_info else None
    df = self.read_raw_data(self.raw_data)
    df = df.set_index("country").stack().to_frame().reset_index()
    df.columns = ["country", "year", "gdp"]

    return geo_format(df, timeopt)


@DataParser.register_dataset(
    label="world.mapgdp", summary="World Bank Gdp data (with gpx extra info)", reference="world.gdp"
)
def get_mapgdp(self, **kwargs):
    return get_mapgeneric(get_gdp(self, **kwargs))


@DataParser.register_dataset(
    label="world.macro",
    summary="Global economic data",
    category="Economics",
    raw_data=[
        "corruption.csv",
        "cost_of_living.csv",
        "richest_countries.csv",
        "unemployment.csv",
        "tourism.csv",
        "continent.tsv",
    ],
    on="country",
    enrich_data="https://github.com/gtherin/bulkhours/blob/main/bulkhours/data/world.py",
)
def get_macro(self, **data_info):
    df = self.read_raw_data(self.raw_data)
    return geo_format(df, None)


@DataParser.register_dataset(
    label="world.mapmacro", summary="Global economic data (with gpx extra info)", reference="world.macro"
)
def get_mapmacro(self, **kwargs):
    return get_mapgeneric(get_macro(self, **kwargs))


@DataParser.register_dataset(
    label="world.corruption", 
    summary="Corruption index per country", 
    category="Economics", 
    raw_data=[
        "corruption.csv",
        "cost_of_living.csv",
        "richest_countries.csv",
        "unemployment.csv",
        "continent.tsv",
    ],
    on="country",
)
def get_corruption(self, show_truth=False, **data_info):
    show_truth = self.data_info["show_truth"] if "show_truth" in self.data_info else False
    df = self.read_raw_data(self.raw_data)

    if not show_truth:
        df["corruption_index"] = df["corruption_index"].where(
            ~df.index.isin(["Spain", "Japan", "Sweden", "Romania"]), other=np.nan
        )

    df = df[["annual_income", "corruption_index", "gdp_per_capita", "unemployment_rate"]]
    df = df.dropna(subset=["annual_income", "gdp_per_capita", "unemployment_rate"])

    return geo_format(df, None)


@DataParser.register_dataset(
    label="world.life_expectancy_vs_gdp_2018",
    summary="Life expectancy versus GDP/capita per country",
    category="Economics",
    raw_data="https://huggingface.co/datasets/guydegnol/bulkhours/raw/main/life-expectancy-vs-gdp-per-capita.csv",
    info="GDP per capita is measured in 2011 international dollars, which corrects for inflation and cross-country price differences",
    ref_source="https://ourworldindata.org/grapher/life-expectancy-vs-gdp-per-capita",
    ref_site="""Maddison Project Database (2020); UN WPP (2022); Zijdeman et al. (2015)""",
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
    # drop=["annotations", "Continent"],
    enrich_data="https://github.com/gtherin/bulkhours/blob/main/bulkhours/data/world.py",
    query="Year == 2018 and Population > 1e7",
)
def get_life_expectancy_vs_gdp_2018(self, **data_info):
    return self.read_raw_data(self.raw_data)  # .dropna()


@DataParser.register_dataset(
    label="ww2.slbombing",
    summary="South London bombing data during World War II for 576 districts (of equal sizes 0.25km²)",
    columns_description="""| Column   |      Info |
|-----------|:-----------|
| Number_of_bombs   |  Numbers of bombs hit k |         
| Nk                |  Numbers of districts hit by k bombs |""",
)
def get_londonbombing(self, **kwargs):
    return pd.DataFrame({"Number_of_bombs": range(6), "Nk": [229, 211, 93, 35, 7, 1]})

