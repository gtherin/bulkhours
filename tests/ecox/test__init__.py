import bulkhours

import pytest
import pandas as pd
from ecox import plot_ob_bars

import matplotlib.pyplot as plt

@pytest.fixture
def sample_data():
    data = {
        "layer": [-3, -2, -1, 1, 2, 3],
        "volume": [10, 20, 30, 40, 50, 60],
        "volume_cum": [10, 30, 60, 40, 90, 150],
        "price": [100, 101, 102, 103, 104, 105]
    }
    return pd.DataFrame(data)

def test_plot_ob_bars_basic(sample_data):
    fig, ax = plt.subplots()
    plot_ob_bars(ax, sample_data)
    assert len(ax.patches) == 6  # 6 bars should be plotted

def test_plot_ob_bars_with_title(sample_data):
    fig, ax = plt.subplots()
    plot_ob_bars(ax, sample_data, title="Order Book NOW")
    assert "Order Book" in ax.get_title()

def test_plot_ob_bars_with_xlim(sample_data):
    fig, ax = plt.subplots()
    plot_ob_bars(ax, sample_data, xlim=(-5, 5))
    assert ax.get_xlim() == (-5, 5)

def test_plot_ob_bars_with_ylim(sample_data):
    fig, ax = plt.subplots()
    plot_ob_bars(ax, sample_data, ylim=(0, 100))
    assert ax.get_ylim() == (0, 100)

def test_plot_ob_bars_with_cumsum(sample_data):
    fig, ax = plt.subplots()
    plot_ob_bars(ax, sample_data, cumsum=True)
    assert all(p.get_height() in sample_data["volume_cum"].values for p in ax.patches)

def test_plot_ob_bars_with_sleep(sample_data, mocker):
    mock_sleep = mocker.patch("time.sleep")
    fig, ax = plt.subplots()
    plot_ob_bars(ax, sample_data, sleep=1)
    mock_sleep.assert_called_once_with(1)