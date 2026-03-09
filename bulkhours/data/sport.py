from io import StringIO
import pandas as pd

from .data_parser import DataParser


DataParser.register_dataset(
    label="sport.stravism",
    summary="Activities",
    category="Sport",
    raw_data="stravism.csv.enc",
)
