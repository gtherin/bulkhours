import pandas as pd
import numpy as np
from io import StringIO

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
| k   |  Nombre de bombes tombées dans chaque quartier |         
| Nk                |  Nombre de quartiers touchés par k bombes |""",
)
def get_londonbombing(self, **kwargs):
    return pd.DataFrame({"Number_of_bombs": range(6), "Nk": [229, 211, 93, 35, 7, 1]}).set_index("Number_of_bombs")




@DataParser.register_dataset(
    label="world.hgdp",
    summary="World GDP, 20 Countries and zones, (1990 international m$)",
    ref_site="""Maddison Book""",
    category="Economics",
)
def get_hgdp(self):
    return pd.read_csv(
        StringIO(
            """Country 1 1000 1500 1600 1700 1820 1870 1913 1950 1973 2003
Austria 213 298 1414 2093 2483 4104 8419 23451 25702 85227 173311
Belgium 135 170 1225 1561 2288 4529 13716 32347 47190 118516 219069
Denmark 72 144 443 569 727 1471 3782 11670 29654 70032 124781
Finland 8 16 136 215 255 913 1999 6389 17051 51724 106749
France 2366 2763 10912 15559 19539 35468 72100 144489 220492 683965 1315601
Germany 1225 1435 8256 12656 13650 26819 72149 237332 265354 944755 1577423
Italy 6475 2250 11550 14410 14630 22535 41814 95487 164957 582713 1110691
Netherlands 85 128 723 2072 4047 4288 9952 24955 60642 175791 384464
Norway 40 80 183 266 361 777 2360 5988 17728 44852 118591
Sweden 80 160 382 626 1231 3098 6927 17403 47269 109794 193352
Switzerland 128 123 411 750 1068 2165 5581 16483 42545 117251 164773
United_Kingdom 320 800 2815 6007 10709 36232 100180 224618 347850 675941 1280625
Portugal 180 255 606 814 1638 3043 4219 7467 17615 63397 144694
Spain 1867 1800 4495 7029 7481 12299 19556 41653 61429 266896 684537
Other_Western_Europe 1240 504 632 975 1106 2110 4712 12478 30600 105910 294733
Eastern_Europe 1956 2600 6696 9289 11393 24906 50163 134793 185023 550756 786408
Former_USSR 1560 2840 8458 11426 16196 37678 83646 232351 510243 1513070 1552231
USA 272 520 800 600 527 12548 98374 517383 1455916 3536622 8430762
Other_Western_World 176 228 320 320 306 951 13119 65558 179574 521667 1277267
Mexico 880 1800 3188 1134 2558 5000 6214 25921 67368 279302 740226
Other_Latin_America 1360 2760 4100 2629 3788 9921 21097 94875 347960 1110158 2391919
Japan 1200 3188 7700 9620 15390 20739 25393 71653 160966 1242932 2699261
China 26820 26550 61800 96000 82800 228600 189740 241431 244985 739414 6187984
India 33750 33750 60500 74250 90750 111417 134882 204242 222222 494832 2267136
Other_East_Asia 4845 8968 20822 24582 28440 36451 53155 122874 256938 839258 3926975
West_Asia 10120 12415 10495 12637 12291 15270 22468 40588 106283 548120 1473739
Africa 8030 13835 19383 23473 25776 31266 45234 79486 203131 549993 1322087"""
        ),
        sep=" ",
    ).set_index("Country")


@DataParser.register_dataset(
    label="world.hpop",
    summary="World population in thousands",
    ref_site="""Maddison Book""",
    category="Economics",
)
def get_hpop(self):
    return pd.read_csv(
        StringIO(
            """Country 1 1000 1500 1600 1700 1820 1870 1913 1950 1973 2003
Austria 500 700 2000 2500 2500 3369 4520 6767 6935 7586 8163
Belgium 300 400 1400 1600 2000 3434 5096 7666 8639 9738 10331
Denmark 180 360 600 650 700 1155 1888 2983 4271 5022 5394
Finland 20 40 300 400 400 1169 1754 3027 4009 4666 5204
France 5000 6500 15000 18500 21471 31250 38440 41463 41829 52157 60181
Germany 3000 3500 12000 16000 15000 24905 39231 65058 68735 78950 82938
Italy 8000 5000 10500 13100 13300 20176 27888 37248 47105 54797 57998
Netherlands 200 300 950 1500 1900 2333 3610 6164 10114 13438 16223
Norway 100 200 300 400 500 970 1737 2447 3267 3961 4555
Sweden 200 400 550 760 1260 2585 4169 5621 7014 8137 8970
Switzerland 300 300 650 1000 1200 1986 2655 3864 4694 6441 7408
United_Kingdom 800 2000 3942 6170 8565 21239 31400 45649 50127 56210 60095
Portugal 400 600 1000 1100 2000 3297 4327 5972 8443 8976 10480
Spain 3750 4000 6800 8240 8770 12203 16201 20263 28063 34837 40217
Other_Western_Europe 2300 1260 1340 1858 1894 2969 4590 6783 12058 13909 16987
Eastern_Europe 4750 6500 13500 16950 18800 36457 53557 79530 87637 110418 121434
Former_USSR 3900 7100 16950 20700 26550 54765 88672 156192 179571 249712 287601
USA 680 1300 2000 1500 1000 9981 40241 97606 152271 211909 290343
Other_Western_World 440 570 800 800 750 1250 5847 13795 24186 38932 55890
Mexico 2200 4500 7500 2500 4500 6587 9219 14970 28485 57557 103718
Other_Latin_America 3400 6900 10000 6100 7550 15004 31180 65965 137453 250316 437641
Japan 3000 7500 15400 18500 27000 31000 34437 51672 83805 108707 127214
China 59600 59000 103000 160000 138000 381000 358000 437140 546815 881940 1288400
India 75000 75000 110000 135000 165000 209000 253000 303700 359000 580000 1049700
Other_East_Asia 11400 21100 37600 43600 50700 64228 89506 147893 333310 567057 1018844
West_Asia 19400 20000 17800 21400 20800 25147 30290 38956 59847 112918 249809
Africa 17000 32300 46610 55320 65080 74236 90466 124697 228181 390202 853422"""
        ),
        sep=" ",
    ).set_index("Country")
