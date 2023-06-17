import numpy as np
import pandas as pd
from .world import get_mapgeneric


# FILE TO BE DELETED
def get_concentrations(zone="World", **kwargs):
    from ..core import data

    df = data.get_core_data("climate-change.csv")
    if zone is not None:
        df = df.query(f"Entity == '{zone}'")
    return df


def get_mapconcentrations(**kwargs):
    return get_mapgeneric(get_concentrations(**kwargs))
