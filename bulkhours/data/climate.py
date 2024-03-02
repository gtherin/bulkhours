import pandas as pd
import datetime

from .data_parser import DataParser
from .world import get_mapgeneric, geo_format


DataParser.register_dataset(
    label="co2.main",
    summary="Data on CO2 and Greenhouse Gas Emissions by Our World in Data",
    category="Climate_Evolution",
    raw_data="https://raw.githubusercontent.com/owid/co2-data/master/owid-co2-data.csv",
    enrich_data="https://github.com/gtherin/bulkhours/blob/main/bulkhours/data/climate.py",
    columns_info="https://github.com/owid/co2-data/blob/master/owid-co2-codebook.csv",
)
DataParser.register_dataset(
    label="co2.mapmain",
    summary="Data on CO2 and Greenhouse Gas Emissions by Our World in Data (with extra gpx data)",
    reference="co2.main",
)

DataParser.register_dataset(
    label="co2.travel_mode",
    summary="CO2 transportation info",
    category="Climate_Evolution",
    ref_source="""https://ourworldindata.org/grapher/carbon-footprint-travel-mode""",
    raw_data="https://huggingface.co/datasets/guydegnol/bulkhours/raw/main/carbon-footprint-travel-mode.csv",
)


@DataParser.register_dataset(
    label="co2.concentrations",
    summary="Greenhouse effect gaz concentrations",
    category="Climate_Evolution",
    raw_data="climate-change.csv",
    ref_source="""https://ourworldindata.org/atmospheric-concentrations""",
    kwargs=dict(zone="World"),
    enrich_data="https://github.com/gtherin/bulkhours/blob/main/bulkhours/data/world.py",
)
def get_concentrations(self, zone="World", **data_info):
    df = self.read_raw_data(self.raw_data)

    df = df.rename(columns={"Entity": "country", "Year": "year"})

    if zone is not None:
        df = df.query(f"country == '{zone}'")
    return df


@DataParser.register_dataset(label="co2.mapconcentrations", reference="co2.concentrations")
def get_mapconcentrations(self, **kwargs):
    return get_mapgeneric(get_concentrations(self, **kwargs))


DataParser.register_dataset(
    label="climate.pisaniferry",
    summary="Les incidences économique de l'action pour le climat",
    category="Climate_Evolution",
    raw_data="https://www.strategie.gouv.fr/sites/strategie.gouv.fr/files/atoms/files/2023-incidences-economiques-transition-climat-rapport-de-synthese_0.pdf",
)

DataParser.register_dataset(
    label="climate.francecarbone",
    summary="La contribution des émissions importées à l'empreinte carbone de la France",
    category="Climate_Evolution",
    raw_data="https://www.ofce.sciences-po.fr/pdf-articles/actu/Rapport-OFCE-HCC-2020.pdf",
)


DataParser.register_dataset(
    label="climate.europecities",
    summary="Statement of Apple stock (Quarterly)",
    category="Economics",
    raw_data="https://huggingface.co/datasets/guydegnol/bulkhours/raw/main/european_cities.json",
    enrich_data="https://github.com/gtherin/bulkhours/blob/main/bulkhours/data/climate.py",
)

@DataParser.register_dataset(
    label="climate.mapeuropecities", summary="Aggregation of public information", reference="BulkHours",
    raw_data="https://huggingface.co/datasets/guydegnol/bulkhours/raw/main/european_cities.json",
)
def get_mapeuropecities(self, **kwargs):
    cities = DataParser.get_data_from_file(self.raw_data, **kwargs)
    return get_mapgeneric(cities)


@DataParser.register_dataset(
    label="climate.europemonthly",
    summary="Aggregation of public information",
    category="Climate_Evolution",
    reference="BulkHours",
    raw_data="https://huggingface.co/datasets/guydegnol/bulkhours/raw/main/european_cities.json",
    enrich_data="https://github.com/gtherin/bulkhours/blob/main/bulkhours/data/climate.py",
)
def get_europemonthly(self, **kwargs):

    from meteostat import Monthly, Point

    # Get cities
    cities = DataParser.get_data_from_file(self.raw_data, **kwargs)

    # Set time period
    start = datetime.datetime(2018, 1, 1)
    end = datetime.datetime(2023, 12, 31)

    gdata = {}
    for _, city in cities.iterrows():
        # Get Monthly data
        data = Monthly(Point(city.Latitude, city.Longitude), start, end).fetch()
        if not data.empty:
            gdata[city.City] = data.groupby(data.index.month)["tavg"].mean().interpolate()

    return pd.DataFrame(gdata).sort_index(axis=1)


@DataParser.register_dataset(
    label="climate.mapeuropemonthly", summary="Aggregation of public information", 
    raw_data="https://huggingface.co/datasets/guydegnol/bulkhours/raw/main/european_cities.json",
    reference="BulkHours"
)
def get_mapeuropemonthly(self, **kwargs):

    cities = DataParser.get_data_from_file(self.raw_data, **kwargs)
    weather = get_europemonthly(self)

    data = cities.merge(weather.T, how="left", left_on="City", right_index=True)
    data = get_mapgeneric(data)
    return data.clip([-20, 30, 40, 60])
