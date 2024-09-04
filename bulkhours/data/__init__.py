import os
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


def get_data(label, **kwargs):
    DataParser.build_clean_datasets()

    data_info = (
        {**DataParser.clean_datasets[label], **kwargs}
        if label in DataParser.clean_datasets
        else {"label": label, "raw_data": label, **kwargs}
    )

    return DataParser(**data_info).get_data()


def download_kaggle_data(filename, chunck_size=40960):
    destination_path = '/root/bulkhours/data/'

    download_url = "https://storage.googleapis.com/kaggle-data-sets/1817999/2965251/bundle/archive.zip?X-Goog-Algorithm=GOOG4-RSA-SHA256&X-Goog-Credential=gcp-kaggle-com%40kaggle-161607.iam.gserviceaccount.com%2F20240903%2Fauto%2Fstorage%2Fgoog4_request&X-Goog-Date=20240903T114415Z&X-Goog-Expires=259200&X-Goog-SignedHeaders=host&X-Goog-Signature=54863d9aab9113332f639e5f141b72361f8d184e885a1a77ad65d035fde5f9e5e2759b2cab289f8c22ed3befe0b3b28f88d1bf957f6d9d3dbd707101984359b488848d0fb3b896694a72a67b4a872d895288e0ea08d413754c1e6db69a64ad3a7d3c22e8a2d06a05515dcd107af66eee290ad42e485d345e18490c55836c0ff520eb460503aa666e2a12b00919f32baf72e2d14450d506a28c606b05711a8b8437aa1ddcacaf97059273b14c7a0c938049e0525508ff1d27bd53726217632cce253134558805700c5e8a83e359621960b73b6fc48f9e43fd834728c9510459514e9bb01b60ba659d34e75d6f3117e65a7e7e8570fba95b5efafc56f89b7fff15"
    filename = urlparse(download_url).path
    with urlopen(download_url) as fileres, NamedTemporaryFile() as tfile:
        total_length = fileres.headers['content-length']
        print(f'Downloading {total_length} bytes compressed')
        dl = 0
        data = fileres.read(chunck_size)
        while len(data) > 0:
            dl += len(data)
            tfile.write(data)
            done = int(50 * dl / int(total_length))
            sys.stdout.write(f"\r[{'=' * done}{' ' * (50-done)}] {dl} bytes downloaded")
            sys.stdout.flush()
            data = fileres.read(chunck_size)
        if filename.endswith('.zip'):
        with ZipFile(tfile) as zfile:
            zfile.extractall(destination_path)
        else:
        with tarfile.open(tfile.name) as tarfile:
            tarfile.extractall(destination_path)            
        print(f'\nDownloaded and uncompressed')
        os.system(f"mv {destination_path}Vegetable\ Images {destination_path}vegetables")

        return '/root/bulkhours/data/vegetables'


def download_data(filename):
    if filename == "vegetables":
        return download_kaggle_data(filename)

    url = "https://huggingface.co/datasets/guydegnol/"
    bfilename = os.path.basename(filename)
    if "http" in filename:
        cmd = f"curl {filename} --output {bfilename}"
    else:
        dirname = os.path.dirname(filename) if "/" in filename else "model_weights"
        cmd = f"curl {url}{dirname}/raw/main/{bfilename} --output {bfilename}"

    os.system(cmd)
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
