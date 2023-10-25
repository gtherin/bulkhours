from .brownian import plot_brownian_sample  # noqa
from .gallery import *  # noqa
from . import regression  # noqa
from . import gradient  # noqa
from . import trading  # noqa

from .block import Block, BlockCoin, BlockMsg  # noqa
from .blockchain import BlockChain  # noqa
from .weather import get_weather_data  # noqa

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
