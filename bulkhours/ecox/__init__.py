from .brownian import plot_brownian_sample  # noqa
from .gallery import *  # noqa
from . import regression  # noqa
from . import gradient  # noqa
from . import trading  # noqa

from .block import Block, BlockCoin, BlockMsg  # noqa
from .blockchain import BlockChain  # noqa
from .weather_data import get_wheather_data  # noqa

from .lob import OrderBook  # noqa
from .market import Market  # noqa
from . import agents  # noqa
from .agents import generate_random_walks  # noqa

def random(samples_number, sample_size, mu=4, distrib="bimodal", seed=42):
    """return a dataframe of exp(-X/scale)/scale for random X"""
    np.random.seed(seed)
    if distrib == "exp":
        return pd.DataFrame(np.random.exponential(scale=mu, size=(sample_size, samples_number)))
    u = np.random.choice([0, 1], size=(sample_size, samples_number))
    d1 = sp.stats.skewnorm.rvs(loc=mu - 3.6, a=7, size=(sample_size, samples_number))
    d2 = sp.stats.skewnorm.rvs(loc=mu, a=7, size=(sample_size, samples_number))
    return pd.DataFrame(u * d1 + 0.5 * (1 - u) * d2)


def sampler(samples_number, sample_size, **kwargs):
    return random(samples_number, sample_size, **kwargs)


def plot_ob_bars(ax, df, title=None, sleep=None, xlim=None, ylim=None, cumsum=False):
    """
    Plots order book bars on the given axis.

    Parameters:
    ax (matplotlib.axes.Axes): The axis on which to plot the bars.
    df (pandas.DataFrame): The data frame containing the order book data.
    title (str, optional): The title of the plot. If 'NOW' is included in the title, it will be replaced with the current time.
    sleep (int or float, optional): Time in seconds to sleep after plotting.
    xlim (tuple, optional): The x-axis limits for the plot.
    ylim (tuple, optional): The y-axis limits for the plot.
    cumsum (bool, optional): If True, use cumulative volume for the bars. Defaults to False.

    Returns:
    None
    """
    import time
    import datetime

    # Clear the axis
    ax.cla()
    column = "volume_cum" if cumsum else "volume"

    xaxis = "layer"
    if xlim is not None:
        xaxis = "price"

    dfb = df[df["layer"]<0]
    if not dfb.empty:
        ax.bar(dfb[xaxis], dfb[column], color="#52DE97", width=1)
        
    dfa = df[df["layer"]>0]
    if not dfa.empty:
        ax.bar(dfa[xaxis], dfa[column], color="#C70039", width=1)

    if title is not None:
        now = (datetime.datetime.now()+datetime.timedelta(hours=2)).strftime('%H:%M:%S')
        ax.set_title(title.replace("NOW", now))

    if xlim is not None:
        ax.set_xlim(xlim)
    else:
        # Use slicing to select equidistant rows
        n = 5
        step = len(df) // (n - 1)
        if step > 0:
            df_equidistant = df.iloc[::step][:n]
            ax.set_xticks(df_equidistant[xaxis])
            ax.set_xticklabels(df_equidistant["price"].round(2))
            ax.tick_params(axis='x', labelrotation=15)

    if ylim is not None:
        ax.set_ylim(ylim)

    if sleep is not None:
        time.sleep(sleep)
