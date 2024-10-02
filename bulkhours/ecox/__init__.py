from .brownian import plot_brownian_sample  # noqa
from .gallery import *  # noqa
from . import regression  # noqa
from . import gradient  # noqa
from . import trading  # noqa

from .block import Block, BlockCoin, BlockMsg  # noqa
from .blockchain import BlockChain  # noqa
from .weather_data import get_wheather_data  # noqa

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


def plot_ob_bars(ax, df, title=None, sleep=None, xlim=None, ylim=None):
    import time
    import datetime

    # Clear the axis
    ax.cla()

    ax.bar(df[df["layer"]<0]["layer"], df[df["layer"]<0]["volume"], color="#52DE97", width=1)
    ax.bar(df[df["layer"]>0]["layer"], df[df["layer"]>0]["volume"], color="#C70039", width=1)

    if title is not None:
        now = (datetime.datetime.now()+datetime.timedelta(hours=2)).strftime('%H:%M:%S')
        ax.set_title(title.replace("NOW", now))

    if xlim is not None:
        ax.set_xlim(xlim)
    else:
        # Use slicing to select equidistant rows
        n = 5
        step = len(df) // (n - 1)
        df_equidistant = df.iloc[::step][:n]
        ax.set_xticks(df_equidistant["layer"])
        ax.set_xticklabels(df_equidistant["price"].round(2))
        ax.tick_params(axis='x', labelrotation=15)

    if ylim is not None:
        ax.set_ylim(ylim)

    if sleep is not None:
        time.sleep(sleep)
