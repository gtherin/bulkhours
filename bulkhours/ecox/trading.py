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


def get_apple(credit=True, **kwargs):
    from ..core import data

    apple = data.get_data_from_file("APPLE_DownloadFPrepStatementQuarter").iloc[-4 * 5 :]

    apple.index = pd.to_datetime(apple.index)
    apple = apple[["date", "revenue", "grossProfit", "ebitda", "netIncome", "eps"]].set_index("date")
    apple["revenue"] = apple["revenue"].astype(float)
    apple.index = pd.date_range("2017-12-30", periods=20, freq="Q")

    return apple


def display_sharpe_ratios(srs):
    import IPython

    IPython.display.display(srs.to_frame("pnl").T)


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
    instr_list = ["ALPHABET", "CRUDE", "NASDAQ", "BRENT", "COPPER", "CORN", "SP500", "WHEAT"]
    for i in range(8):
        pnls[instr_list[i]] = gdf[f"ret_{i}"] * pos[f"pos_{i}"].shift(1)

    # Build the aggregated pnl
    pnls["ALL"] = pnls.mean(axis=1)

    # Sharpe ratio calculation
    display_sharpe_ratios(np.sqrt(252) * pnls.mean() / pnls.std())


def build_pnls(gdf, my_trading_algo, plot_pnl=True):
    # The function you will be build
    pos = my_trading_algo(gdf)

    # Build position
    pnls = pd.DataFrame()
    instr_list = ["ALPHABET", "CRUDE", "NASDAQ", "BRENT", "COPPER", "CORN", "SP500", "WHEAT"]
    for i in range(8):
        # The position has a 1-day lag (24h to go to position)
        pnls[instr_list[i]] = gdf[f"ret_{i}"] * pos[f"pos_{i}"].shift(1)

    # Check risk
    raw_risk = pnls.abs().sum() / pnls.abs().sum().sum()
    if not raw_risk[raw_risk < 0.03].empty:
        print(f"""WARNING: Risk is to small on {raw_risk[raw_risk < 0.03]}. It has to be at least 3% of total risk""")

    # Build the aggregated pnl
    pnls["ALL"] = pnls.mean(axis=1)

    # Sharpe ratio calculation
    display_sharpe_ratios(np.sqrt(252) * pnls.mean() / pnls.std())

    # Plot pnls
    if plot_pnl:
        pnls.cumsum().plot()
    check_outsample(my_trading_algo)
