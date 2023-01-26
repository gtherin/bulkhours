import glob
import pandas as pd


def get_data(label):

    filename = None
    for directory in ["bulkhours/data", "./data", "../data", "../../bulkhours/data"]:
        if len((files := glob.glob(f"{directory}/{label}*"))):
            filename = files[0]
    if not filename:
        print(f"No data available for {label}")
        return None

    ext = filename.split(".")[-1]
    if ext == "tsv":
        df = pd.read_csv(filename, sep="\t")
    else:
        df = pd.read_csv(filename)
    df = df.set_index(df.columns[0])

    return df
