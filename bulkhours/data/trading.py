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


@DataParser.register_dataset(
    label="binance",
    summary="Get BTC-UUD RT Order Book data",
    category="Economics",
    ref_source="https://api.binance.com/api/v3/depth?symbol=BTCUSDT&limit=100",
    enrich_data="https://github.com/gtherin/bulkhours/blob/main/bulkhours/data/statsdata.py",
)
def get_binance_ob_data(self):

    ticker = self.data_info["ticker"] if "ticker" in self.data_info else "BTCUSDT"

    # Get Level 2 order book data from Binance
    data = requests.get(f'https://api.binance.com/api/v3/depth?symbol={ticker}&limit=100').json()

    # Extract bids and asks
    bids = pd.DataFrame(data['bids'], columns=['price', 'volume']).astype(float)
    asks = pd.DataFrame(data['asks'], columns=['price', 'volume']).astype(float)
    bids["layer"] = -(bids.index + 1)
    asks["layer"] = asks.index + 1

    df = [bids.head(nlayers), asks.head(nlayers)]

    include_mid = self.data_info["include_mid"] if "include_mid" in self.data_info else True

    if include_mid:
        df.append(pd.DataFrame({"price": [0.5*(bids["price"].iloc[0]+asks["price"].iloc[0])], "volume": [0], "layer": [0]}))

    return pd.concat(df).sort_values("price").reset_index(drop=True)


@DataParser.register_dataset(
    label="lobster",
    summary="Get Order Book data from LOBSTER [2012-06-21 1hour]",
    category="Economics",
    ref_source="https://lobsterdata.com/info/DataSamples.php",
    enrich_data="https://github.com/gtherin/bulkhours/blob/main/bulkhours/data/statsdata.py",
)
def get_stocks(self):
    # ticker in GOOG AAPL AMZN INTC MSFT SPY
    # depth 1 5 10 30 50

    import requests
    import zipfile
    import io
    import pandas as pd

    ticker = self.data_info["ticker"] if "ticker" in self.data_info else "GOOG"
    depth = self.data_info["depth"] if "depth" in self.data_info else 1
    date = "2012-06-21"

    # Step 1: Download the zip file from the URL
    url = f"https://lobsterdata.com/info/sample/LOBSTER_SampleFile_{ticker}_{date}_{depth}.zip"
    response = requests.get(url)

    # Step 2: Unzip the downloaded file
    with zipfile.ZipFile(io.BytesIO(response.content)) as z:
        # Extract the list of files in the zip
        z.extractall()

    # The LOBSTER file usually contains multiple files like message files and order book files
    # Assuming we have the message file and order book file (adjust based on actual file names)
    message_file = f'{ticker}_{date}_34200000_57600000_message_{depth}.csv'
    orderbook_file = f'{ticker}_{date}_34200000_57600000_orderbook_{depth}.csv'

    # Load the message file (trades) into a DataFrame
    message_columns = ['time', 'event_type', 'order_id', 'trade_vol', 'trade', 'trade_side']
    df_messages = pd.read_csv(message_file, header=None, names=message_columns)

    # Step 5: Load the order book file
    price_columns = ["trade"]
    # Generate column names for order book levels
    orderbook_columns = []
    for i in range(1, depth + 1):
        price_columns += [f'bid{i}', f'ask{i}']
        orderbook_columns += [f'bid{i}', f'bid{i}_vol', f'ask{i}', f'ask{i}_vol']

    # Load the order book file into a DataFrame
    df_orderbook = pd.read_csv(orderbook_file, header=None, names=orderbook_columns)

    # Merge data
    df = pd.concat([df_messages, df_orderbook], axis=1)

    # Convert prices to $
    df[price_columns] /= 10000

    # Remove unregular trades
    #df.loc[~df["event_type"].isin([4, 5]), ['trade', 'trade_vol', 'trade_side']] = np.nan

    # Convert data and set the right date
    df['time'] = pd.to_datetime(df["time"], unit='s').apply(lambda x: x.replace(year=2012, month=6, day=21))

    # Set index
    df = df.set_index('time').sort_index()

    return df
