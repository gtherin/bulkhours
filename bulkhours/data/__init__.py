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
from . import vegetables


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


def download_data(filename, directory=None):
    if filename == "vegetables":
        return vegetables.download_kaggle_data(filename)

    url = "https://huggingface.co/datasets/guydegnol/"
    bfilename = os.path.basename(filename)
    if "http" in filename:
        cmd = f"curl {filename} --output {bfilename}"
    else:
        dirname = os.path.dirname(filename) if "/" in filename else "model_weights"
        cmd = f"curl {url}{dirname}/raw/main/{bfilename} --output {bfilename}"

    print(cmd)
    os.system(cmd)

    if directory is not None:
        os.system(f"mv {bfilename} {directory}")

    return bfilename


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
