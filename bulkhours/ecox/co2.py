import numpy as np
import pandas as pd
from .world import get_mapgeneric


def get_main(credit=True, **kwargs):
    if credit:
        print(
            """Data on CO2 and Greenhouse Gas Emissions by Our World in Data
- Data source: https://raw.githubusercontent.com/owid/co2-data/master/owid-co2-data.csv
- Info columns: https://github.com/owid/co2-data/blob/master/owid-co2-codebook.csv
        """
        )

    df = pd.read_csv("https://raw.githubusercontent.com/owid/co2-data/master/owid-co2-data.csv")

    return df


def get_mapmain(**kwargs):
    return get_mapgeneric(get_main(**kwargs))


def get_concentrations(credit=True, zone="World", **kwargs):
    from ..core import data

    if credit:
        print(
            """Data concentrations
- Data source: https://ourworldindata.org/atmospheric-concentrations
        """
        )

    df = data.get_core_data("climate-change.csv")
    if zone is not None:
        df = df.query(f"Entity == '{zone}'")
    return df


def get_mapconcentrations(**kwargs):
    return get_mapgeneric(get_concentrations(**kwargs))
