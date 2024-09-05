import os
import sys
import pandas as pd
import datetime

from .data_parser import DataParser


DataParser.register_dataset(
    label="vegetables",
    summary="Vegetables images for classification",
    category="Machine_learning",
    raw_data="https://www.kaggle.com/datasets/misrakahmed/vegetable-image-dataset",
    enrich_data="https://github.com/gtherin/bulkhours/blob/main/bulkhours/data/vegetables.py",
)



def draw_images(num_of_pics=25, directory="test", seed=42, model=None, is_fr=True):

    import glob
    import random
    from pathlib import Path

    path = Path(os.path.dirname(__file__))
    data_directory = str(path.parent.parent.absolute()) + "/data/"

    # Print the class encodings done by the generators
    class_map = {k: v.split("/")[-1] for k, v in enumerate(sorted(glob.glob(f'{data_directory}/{directory}/train/*')))}
    print(data_directory)
    print(class_map)

    labels = {0 : 'Haricot', 1 : 'Concombre amère', 2 : "Courgette", 3 : "Aubergine", 4 : "Brocoli", 5 : "Chou", 
              6 : "Poivron", 7 : "Carotte", 8 : "Chou-fleur", 9 : "Concombre", 10 : "Papaye", 11 : "Pomme de terre", 
              12 : "Citrouille", 13 : "Radis", 14 : "Tomate"} if is_fr else class_map

    ncols = int(np.sqrt(num_of_pics)+0.2)

    random.seed(seed)
    fig, ax = plt.subplots(nrows=ncols, ncols=ncols, figsize=(12, 12))
    for col in range(ncols):
        for row in range(ncols):
            ax[col][row].set_axis_off()

    for index in range(num_of_pics):

        # 1. Get graph info
        row, col = index % ncols, index // ncols
        y = index%len(class_map)
        rimages = glob.glob(f'{data_directory}/{directory}/{class_map[y]}/*.jpg')
        image_path = random.choice(rimages)

        # 2. Load and preprocess the image
        test_img = tf.keras.preprocessing.image.load_img(image_path, target_size=(150, 150))
        test_img_arr = tf.keras.preprocessing.image.img_to_array(test_img) / 255.0
        test_img_input = test_img_arr.reshape((1, test_img_arr.shape[0], test_img_arr.shape[1], test_img_arr.shape[2]))

        # 3. Plot the image
        ax[col][row].imshow(test_img_arr)
        ax[col][row].set_axis_off()

        # 4. Make Predictions
        if model is None:
            ax[col][row].set_title(f"y={y}-{labels[y]}", backgroundcolor='white', fontsize=11, x=0.5, y=0.85)
        else:
            yhat = np.argmax(model.predict(test_img_input, verbose=0))
            ax[col][row].set_title(f"y={y}-{labels[y]}\nyhat={yhat}-{labels[yhat]}", backgroundcolor='white', 
                                  color="#52DE97" if yhat == y else "#C70039", fontsize=11, x=0.5, y=0.75)

    plt.subplots_adjust(wspace=0, hspace=0)


def download_kaggle_data(filename, chunck_size=40960):

    from tempfile import NamedTemporaryFile
    from urllib.request import urlopen
    from urllib.parse import unquote, urlparse
    from zipfile import ZipFile
    import tarfile
    import huggingface_hub

    from pathlib import Path

    path = Path(os.path.dirname(__file__))
    destination_path = str(path.parent.parent.absolute()) + "/data/"

    download_url = "https://storage.googleapis.com/kaggle-data-sets/1817999/2965251/bundle/archive.zip?X-Goog-Algorithm=GOOG4-RSA-SHA256&X-Goog-Credential=gcp-kaggle-com%40kaggle-161607.iam.gserviceaccount.com%2F20240903%2Fauto%2Fstorage%2Fgoog4_request&X-Goog-Date=20240903T114415Z&X-Goog-Expires=259200&X-Goog-SignedHeaders=host&X-Goog-Signature=54863d9aab9113332f639e5f141b72361f8d184e885a1a77ad65d035fde5f9e5e2759b2cab289f8c22ed3befe0b3b28f88d1bf957f6d9d3dbd707101984359b488848d0fb3b896694a72a67b4a872d895288e0ea08d413754c1e6db69a64ad3a7d3c22e8a2d06a05515dcd107af66eee290ad42e485d345e18490c55836c0ff520eb460503aa666e2a12b00919f32baf72e2d14450d506a28c606b05711a8b8437aa1ddcacaf97059273b14c7a0c938049e0525508ff1d27bd53726217632cce253134558805700c5e8a83e359621960b73b6fc48f9e43fd834728c9510459514e9bb01b60ba659d34e75d6f3117e65a7e7e8570fba95b5efafc56f89b7fff15"
    dfilename = urlparse(download_url).path
    with urlopen(download_url) as fileres, NamedTemporaryFile() as tfile:
        total_length = fileres.headers['content-length']
        print(f'\033[36mDownloading {destination_path}{filename} data ({float(total_length)*1e-6:.0f} MO compressed)\033[39m')
        dl = 0
        data = fileres.read(chunck_size)
        while len(data) > 0:
            dl += len(data)
            tfile.write(data)
            done = int(50 * dl / int(total_length))
            sys.stdout.write(f"\033[36m\r[{'=' * done}{' ' * (50-done)}] {float(dl)*1e-6:.0f} MO downloaded\033[39m")
            sys.stdout.flush()
            data = fileres.read(chunck_size)
        if dfilename.endswith('.zip'):
            with ZipFile(tfile) as zfile:
                zfile.extractall(destination_path)
        else:
            with tarfile.open(tfile.name) as tarfile:
                tarfile.extractall(destination_path)            
        os.system(f"mv {destination_path}Vegetable\ Images {destination_path}{filename}")

        huggingface_hub.snapshot_download(repo_id="guydegnol/vegetables", repo_type="model", 
                                          allow_patterns=["*.h5", "*.json"], local_dir=f"{destination_path}{filename}")

        return f'{destination_path}{filename}'

