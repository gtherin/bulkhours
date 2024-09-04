import os
import pandas as pd
import datetime

from .data_parser import DataParser
from .world import get_mapgeneric, geo_format


DataParser.register_dataset(
    label="vegetables",
    summary="Vegetables images for classification",
    category="Machine_learning",
    raw_data="https://www.kaggle.com/datasets/misrakahmed/vegetable-image-dataset",
    enrich_data="https://github.com/gtherin/bulkhours/blob/main/bulkhours/data/vegetables.py",
)


def plot_images(sample):

    import tensorflow as tf

    image_categories = os.listdir('/root/bulkhours/data/vegetables/train')

    # Create a figure
    plt.figure(figsize=(12, 12))
    for i, cat in enumerate(image_categories):

        # Load images for the ith category
        image_path = f"/root/bulkhours/data/vegetables/{sample}" + '/' + cat
        images_in_folder = os.listdir(image_path)
        first_image_of_folder = images_in_folder[0]
        first_image_path = image_path + '/' + first_image_of_folder
        img = tf.keras.preprocessing.image.load_img(first_image_path)
        img_arr = tf.keras.preprocessing.image.img_to_array(img) / 255.0

        # Create Subplot and plot the images
        plt.subplot(4, 4, i+1)
        plt.imshow(img_arr)
        plt.title(cat)
        plt.axis('off')

    plt.show()


def download_kaggle_data(filename, chunck_size=40960):

    from tempfile import NamedTemporaryFile
    from urllib.request import urlopen
    from urllib.parse import unquote, urlparse
    from zipfile import ZipFile
    import tarfile

    bfilename = os.path.basename("vegetables.py")
    print(bfilename)

    destination_path = '/root/bulkhours/data/'

    download_url = "https://storage.googleapis.com/kaggle-data-sets/1817999/2965251/bundle/archive.zip?X-Goog-Algorithm=GOOG4-RSA-SHA256&X-Goog-Credential=gcp-kaggle-com%40kaggle-161607.iam.gserviceaccount.com%2F20240903%2Fauto%2Fstorage%2Fgoog4_request&X-Goog-Date=20240903T114415Z&X-Goog-Expires=259200&X-Goog-SignedHeaders=host&X-Goog-Signature=54863d9aab9113332f639e5f141b72361f8d184e885a1a77ad65d035fde5f9e5e2759b2cab289f8c22ed3befe0b3b28f88d1bf957f6d9d3dbd707101984359b488848d0fb3b896694a72a67b4a872d895288e0ea08d413754c1e6db69a64ad3a7d3c22e8a2d06a05515dcd107af66eee290ad42e485d345e18490c55836c0ff520eb460503aa666e2a12b00919f32baf72e2d14450d506a28c606b05711a8b8437aa1ddcacaf97059273b14c7a0c938049e0525508ff1d27bd53726217632cce253134558805700c5e8a83e359621960b73b6fc48f9e43fd834728c9510459514e9bb01b60ba659d34e75d6f3117e65a7e7e8570fba95b5efafc56f89b7fff15"
    filename = urlparse(download_url).path
    with urlopen(download_url) as fileres, NamedTemporaryFile() as tfile:
        total_length = fileres.headers['content-length']
        print(f'\033[36mDownloading {total_length} bytes compressed\033[39m')
        dl = 0
        data = fileres.read(chunck_size)
        while len(data) > 0:
            dl += len(data)
            tfile.write(data)
            done = int(50 * dl / int(total_length))
            sys.stdout.write(f"\033[36m\r[{'=' * done}{' ' * (50-done)}] {dl} bytes downloaded\033[39m")
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

