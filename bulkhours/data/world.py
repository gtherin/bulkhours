import numpy as np

from .data_parser import DataParser, register_dataset


def get_mapgeneric(df):
    import geopandas as gpd

    if "continent" in df.columns:
        del df["continent"]

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


@register_dataset("world.poverty")
def get_poverty(self, timeopt=None):
    timeopt = self.data_info["timeopt"] if "timeopt" in self.data_info else None
    df = self.read_raw_data(self.raw_data)
    return geo_format(df, timeopt)


@register_dataset("world.mappoverty")
def get_mappoverty(self, **kwargs):
    return get_mapgeneric(get_poverty(self, **kwargs))


@register_dataset("world.gdp")
def get_gdp(self, timeopt=None, **data_info):
    timeopt = self.data_info["timeopt"] if "timeopt" in self.data_info else None
    df = self.read_raw_data(self.raw_data)
    df = df.set_index("country").stack().to_frame().reset_index()
    df.columns = ["country", "year", "gdp"]

    return geo_format(df, timeopt)


@register_dataset("world.mapgdp")
def get_mapgdp(self, **kwargs):
    return get_mapgeneric(get_gdp(self, **kwargs))


@register_dataset("world.macro")
def get_macro(self, **data_info):
    df = self.read_raw_data(self.raw_data)
    return geo_format(df, None)


@register_dataset("world.mapmacro")
def get_mapmacro(self, **kwargs):
    return get_mapgeneric(get_macro(self, **kwargs))


@register_dataset("world.corruption")
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


@register_dataset("world.life_expectancy_vs_gdp_2018")
def get_life_expectancy_vs_gdp_2018(self, **data_info):
    return self.read_raw_data(self.raw_data).dropna()


@register_dataset("co2.concentrations")
def get_concentrations(self, zone="World", **data_info):
    df = self.read_raw_data(self.raw_data)

    df = df.rename(columns={"Entity": "country", "Year": "year"})

    if zone is not None:
        df = df.query(f"country == '{zone}'")
    return df


@register_dataset("co2.mapconcentrations")
def get_mapconcentrations(self, **kwargs):
    return get_mapgeneric(get_concentrations(self, **kwargs))
