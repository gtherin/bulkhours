import os
import sys
import glob

modules = glob.glob(os.path.join(os.path.dirname(__file__), "*.py"))
modules = [
    os.path.basename(f)[:-3]
    for f in modules
    if os.path.isfile(f) and os.path.basename(f)[:-3] not in ["data_parser", "__init__", "help", "datasets"]
]
__all__ = modules
from . import *
from .help import build_readme, help, generate_header_links, get_header_links  # noqa
from .data_parser import DataParser  # noqa
from .statsdata import download_data  # noqa
from .trading import merge_ob_data, get_ob_slice  # noqa
from .text import get_sentiments, en2fr, en2icons  # noqa
from .safe_loader import secure_load, secure_save  # noqa


def get_data(label, **kwargs):
    DataParser.build_clean_datasets()

    data_info = (
        {**DataParser.clean_datasets[label], **kwargs}
        if label in DataParser.clean_datasets
        else {"label": label, "raw_data": label, **kwargs}
    )
    
    return DataParser(**data_info).get_data()


def save_model(model_name, model, history, data_directory):

    import json

    # Create a checkpoint callback that saves the model after every epoch
    model.save_weights(f'{data_directory}/{model_name}.weights.h5')

    with open(f'{data_directory}/{model_name}.hist.json', 'r') as f:
        h = json.load(f)
        fit_history = {k: h[k] + history[k] for k in ["accuracy", "loss", "val_accuracy", "val_loss"]}

    with open(f'{data_directory}/{model_name}.hist.json', 'w') as f:
        json.dump(fit_history, f)


def get_image(label, ax=None):
    return DataParser(label=label).get_image(ax=ax)


def geo_plot(label=None, timeopt="last", data=None, **kwargs):
    """
    data: geopandas dataframe (world.mappoverty)
    timeopt: year the estimation (last by default)
    """

    from ..core import geo  # noqa

    if data is None:
        data = get_data(label, timeopt=timeopt) if type(label) is str else label

    return geo.geo_plot(data=data, timeopt=timeopt, **kwargs)


def download_from_gdrive(*, file_id, destination):
    import requests
    from tqdm import tqdm

    # Make the initial request to get file size
    response = requests.get(f"https://drive.google.com/uc?export=download&id={file_id}", stream=True)
    if response.status_code != 200:
        print(f"Failed to download file. HTTP status code: {response.status_code}")
        return

    # Get total file size from headers
    total_size = int(response.headers.get('content-length', 0))

    # Progress bar setup
    with open(destination, "wb") as file, tqdm(desc=f"Downloading {destination}", total=total_size, unit="B", unit_scale=True, unit_divisor=1024) as progress_bar:
        for chunk in response.iter_content(chunk_size=1024):
            if chunk:  # Filter out keep-alive chunks
                file.write(chunk)
                progress_bar.update(len(chunk))
