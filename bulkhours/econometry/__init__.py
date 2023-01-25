from .statsdata import *  # noqa
from .brownian import plot_brownian_sample  # noqa
from .gallery import *  # noqa
from .income import get_fr_income  # noqa


def get_list_of_distribs():

    import scipy as sp

    return [d for d in sp.stats._continuous_distns if not d in ["levy_stable", "studentized_range"]]
