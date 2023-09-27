import pandas as pd
import numpy as np
import time

from .data_parser import DataParser


def get_test_data():
    return DataParser.get_data_from_file("freefight.csv")


class Sampler:
    outsample_dt = None


Sampler.outsample_dt = time.time() - 300


@DataParser.register_dataset(
    label="trading.apple",
    summary="Statement of Apple stock (Quarterly)",
    category="Economics",
    raw_data="https://huggingface.co/datasets/guydegnol/bulkhours/raw/main/APPLE_DownloadFPrepStatementQuarter.tsv",
    enrich_data="https://github.com/gtherin/bulkhours/blob/main/bulkhours/data/trading.py",
)
def get_apple(self):
    apple = self.read_raw_data(self.raw_data).iloc[-4 * 5 :]

    apple.index = pd.to_datetime(apple.index)
    apple = apple[["date", "revenue", "grossProfit", "ebitda", "netIncome", "eps"]].set_index("date")
    apple["revenue"] = apple["revenue"].astype(float)
    apple.index = pd.date_range("2017-12-30", periods=20, freq="Q")

    return apple


def display_sharpe_ratios(srs):
    import IPython

    IPython.display.display(srs.to_frame("pnl").T)


def get_pnls(gdf, pos):
    pnls = pd.DataFrame()
    instr_list = ["ALPHABET", "CRUDE", "NASDAQ", "BRENT", "COPPER", "CORN", "SP500", "WHEAT"]
    for i in range(8):
        pnls[instr_list[i]] = gdf[f"ret_{i}"] * pos[f"pos_{i}"].shift(1)

    # Build the aggregated pnl
    pnls["ALL"] = pnls.mean(axis=1)
    return pnls


def check_outsample(my_trading_algo):
    import IPython

    waiting_period = 5 * 60
    if (tdiff := time.time() - Sampler.outsample_dt) < waiting_period:
        IPython.display.display(
            IPython.display.Markdown(
                f"Outsample test can be runned in {waiting_period-tdiff:.0f} seconds (possible every {waiting_period:.0f} seconds)."
            )
        )
        return

    Sampler.outsample_dt = time.time()
    IPython.display.display(
        IPython.display.Markdown(
            f"""Outsample test (possible every {waiting_period:.0f} seconds) 🤓:
---"""
        )
    )

    gdf = DataParser.get_data_from_file("ffcontrol.csv")
    pos = my_trading_algo(gdf)
    pnls = get_pnls(gdf, pos)

    # Sharpe ratio calculation
    display_sharpe_ratios(np.sqrt(252) * pnls.mean() / pnls.std())


def build_pnls(gdf, my_trading_algo, plot_pnl=True):
    import IPython

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
        IPython.display.display(
            IPython.display.Markdown(
                f"""⚠️ WARNING: Risk is to small on {raw_risk[raw_risk < 0.03]}. It has to be at least 3% of total risk"""
            )
        )

    # Build the aggregated pnl
    pnls["ALL"] = pnls.mean(axis=1)

    # Sharpe ratio calculation
    display_sharpe_ratios(np.sqrt(252) * pnls.mean() / pnls.std())

    # Plot pnls
    if plot_pnl:
        pnls.cumsum().plot()
    check_outsample(my_trading_algo)
