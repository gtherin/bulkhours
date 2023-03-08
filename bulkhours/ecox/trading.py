import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import scipy as sp
import statsmodels.api as sm
import matplotlib
from .brownian import Brown
import time


def get_test_data():
    from ..core import data

    return data.get_data_from_file("freefight.csv")


class Sampler:
    outsample_dt = None


Sampler.outsample_dt = time.time() - 300


def check_outsample(my_trading_algo):
    waiting_period = 5 * 60
    if (tdiff := time.time() - Sampler.outsample_dt) < waiting_period:
        print(f"This test can be runned in {waiting_period-tdiff:.0f} seconds.")
        return

    Sampler.outsample_dt = time.time()
    print(f"Do the test {tdiff}")

    from ..core import data

    gdf = data.get_data_from_file("ffcontrol.csv")
    pos = my_trading_algo(gdf)

    pnls = pd.DataFrame()
    for i in range(8):
        pnls[f"pnl_{i}"] = gdf[f"ret_{i}"] * pos[f"pos_{i}"].shift(1)

    pnls["pnl_all"] = pnls.mean(axis=1)
    print(np.sqrt(252) * pnls.mean() / pnls.std())


def get_apple(credit=True, **kwargs):
    from ..core import data

    apple = data.get_data_from_file("APPLE_DownloadFPrepStatementQuarter").iloc[-4 * 5 :]

    apple.index = pd.to_datetime(apple.index)
    apple = apple[["date", "revenue", "grossProfit", "ebitda", "netIncome", "eps"]].set_index("date")
    apple["revenue"] = apple["revenue"].astype(float)
    apple.index = pd.date_range("2017-12-30", periods=20, freq="Q")

    return apple


def build_pnls(gdf, my_trading_algo):
    pos = my_trading_algo(gdf)

    # Build position
    pnls = pd.DataFrame()
    for i in range(8):
        # The position has a 1-day lag (24h to go to position)
        pnls[f"pnl_{i}"] = gdf[f"ret_{i}"] * pos[f"pos_{i}"].shift(1)

    pnls["pnl_all"] = pnls.mean(axis=1)
    # 1. Implement the Sharpe ratio
    sr = np.sqrt(252) * pnls.mean() / pnls.std()
    print(sr)

    pnls.cumsum().plot()
    check_outsample(my_trading_algo)
