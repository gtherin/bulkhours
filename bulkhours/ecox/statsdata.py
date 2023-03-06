import numpy as np
import pandas as pd


def get_oil(credit=True, **kwargs):
    if credit:
        print("https://www.statsmodels.org/stable/index.html")
    data = [
        446.6565,
        454.4733,
        455.663,
        423.6322,
        456.2713,
        440.5881,
        425.3325,
        485.1494,
        506.0482,
        526.792,
        514.2689,
        494.211,
    ]
    if credit:
        print("Oil production in Saudi Arabia from 1996 to 2007")
    return pd.Series(data, pd.date_range(start="1996", end="2008", freq="A")).to_frame("oil")


def get_air(credit=True, **kwargs):
    if credit:
        print("https://www.statsmodels.org/stable/index.html")
    data = [
        17.5534,
        21.86,
        23.8866,
        26.9293,
        26.8885,
        28.8314,
        30.0751,
        30.9535,
        30.1857,
        31.5797,
        32.5776,
        33.4774,
        39.0216,
        41.3864,
        41.5966,
    ]
    air = pd.Series(data, pd.date_range(start="1990", end="2005", freq="A"))
    return air.to_frame("air")


def get_livestock2(credit=True, **kwargs):
    if credit:
        print("https://www.statsmodels.org/stable/index.html")
    # Forecasting livestock, sheep in Asia: comparing forecasting performance of non-seasonal methods.
    data = [
        263.9177,
        268.3072,
        260.6626,
        266.6394,
        277.5158,
        283.834,
        290.309,
        292.4742,
        300.8307,
        309.2867,
        318.3311,
        329.3724,
        338.884,
        339.2441,
        328.6006,
        314.2554,
        314.4597,
        321.4138,
        329.7893,
        346.3852,
        352.2979,
        348.3705,
        417.5629,
        417.1236,
        417.7495,
        412.2339,
        411.9468,
        394.6971,
        401.4993,
        408.2705,
        414.2428,
    ]
    index = pd.date_range(start="1970", end="2001", freq="A")
    return pd.Series(data, index).to_frame("livestock2")


def get_livestock3(credit=True, **kwargs):
    if credit:
        print("https://www.statsmodels.org/stable/index.html")
    data = [407.9979, 403.4608, 413.8249, 428.105, 445.3387, 452.9942, 455.7402]
    return pd.Series(data, pd.date_range(start="2001", end="2008", freq="A")).to_frame("livestock3")


def get_aust(credit=True, **kwargs):
    if credit:
        print("https://www.statsmodels.org/stable/index.html")
    data = [
        41.7275,
        24.0418,
        32.3281,
        37.3287,
        46.2132,
        29.3463,
        36.4829,
        42.9777,
        48.9015,
        31.1802,
        37.7179,
        40.4202,
        51.2069,
        31.8872,
        40.9783,
        43.7725,
        55.5586,
        33.8509,
        42.0764,
        45.6423,
        59.7668,
        35.1919,
        44.3197,
        47.9137,
    ]
    return pd.Series(data, pd.date_range(start="2005", end="2010-Q4", freq="QS-OCT")).to_frame("aust")


def get_air_passengers(credit=True, **kwargs):
    from ..core import data

    df = data.get_core_data("AirPassengers.csv", index="Month")
    df.index = pd.to_datetime(df.index)
    df.index.freq = "MS"
    df["is_test"] = df.index >= df.index[120]

    return df
