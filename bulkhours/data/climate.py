from .data_parser import DataParser
from .world import get_mapgeneric


DataParser.register_dataset(
    label="co2.main",
    summary="Data on CO2 and Greenhouse Gas Emissions by Our World in Data",
    category="Climate_Evolution",
    raw_data="https://raw.githubusercontent.com/owid/co2-data/master/owid-co2-data.csv",
    enrich_data="https://github.com/guydegnol/bulkhours/blob/main/bulkhours/data/world.py",
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
    raw_data="carbon-footprint-travel-mode.csv",
)


@DataParser.register_dataset(
    label="co2.concentrations",
    summary="Greenhouse effect gaz concentrations",
    category="Climate_Evolution",
    raw_data="climate-change.csv",
    ref_source="""https://ourworldindata.org/atmospheric-concentrations""",
    kwargs=dict(zone="World"),
    enrich_data="https://github.com/guydegnol/bulkhours/blob/main/bulkhours/data/world.py",
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
