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
    import numpy as np
    import matplotlib.pyplot as plt
    from pathlib import Path
    import tensorflow as tf

    path = Path(os.path.dirname(__file__))
    data_directory = str(path.parent.parent.absolute()) + "/data/vegetables"

    # Print the class encodings done by the generators
    class_map = {k: v.split("/")[-1] for k, v in enumerate(sorted(glob.glob(f'{data_directory}/{directory}/*')))}

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
    import sys
    #import huggingface_hub

    from pathlib import Path

    #path = Path(os.path.dirname(__file__))
    destination_path = "/root/bulkhours/data/"
    os.system("kaggle datasets download -d misrakahmed/vegetable-image-dataset")
    dfilename = "vegetable-image-dataset.zip"
    print(dfilename, destination_path)
    with ZipFile(dfilename) as zfile:
        zfile.extractall(destination_path)
    os.system(f'mv "{destination_path}Vegetable Images" "{destination_path}{filename}"')

    #huggingface_hub.snapshot_download(repo_id="guydegnol/vegetables", repo_type="model",
    #                                  allow_patterns=["*.h5", "*.json"], local_dir=f"{destination_path}{filename}")

    return f'{destination_path}{filename}'

