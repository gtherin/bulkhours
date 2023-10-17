from .brownian import plot_brownian_sample  # noqa
from .gallery import *  # noqa
from . import regression  # noqa
from . import gradient  # noqa
from . import trading  # noqa

from .block import Block, BlockCoin, BlockMsg  # noqa
from .blockchain import BlockChain  # noqa


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

def plot_prediction(df, models, column, label, ax=None, test_data=-5):

    import sklearn as sk # Data fitting
    from IPython.display import display

    if ax is None:
        fig, ax = plt.subplots(figsize=(12, 4))
    if "is_test" not in df.columns:
        df["is_test"] = df.index > df.index[test_data]

    if not df[~df.is_test].empty:
        df[~df.is_test][column].plot(legend=True, label="Train", ax=ax)
    if not df[df.is_test].empty:
        df[df.is_test][column].plot(legend=True, label="Test", alpha=0.4, lw=6, ax=ax)

    params = ["smoothing_level", "smoothing_trend", 'smoothing_seasonal', "damping_trend", "initial_level", "initial_trend"]
    results = pd.DataFrame(index=["alpha", "beta", "gamma", "phi", "l0", "b0", "SSE", "MeanAvgError"])

    for mlabel, model in models.items():
        if not df[df.is_test].empty:
            y_pred = model.forecast(df.is_test.sum()).dropna()
            y_pred.plot(legend=True, label=mlabel, lw=5, ls=(0, (1, 1)), zorder=100, ax=ax)
            mae = sk.metrics.mean_absolute_error(df[df.is_test][column], y_pred)
        else:
            mae = 0
        results[mlabel] = [model.params[p] for p in params] + [np.round(model.sse), np.round(mae)]
    ax.set_title(label)
    display(results.T)
