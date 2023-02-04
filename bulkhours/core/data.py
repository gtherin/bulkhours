import glob
import pandas as pd

owid_aliases = {
    "vaccinations": "https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/vaccinations/vaccinations.csv",
    "covid": "https://covid.ourworldindata.org/data/owid-covid-data.csv",
    "poverty": "https://nyc3.digitaloceanspaces.com/owid-public/data/poverty/pip_dataset.csv",
}


def get_owid_data(label, credit=True):
    if credit and label in owid_aliases:
        print("Data come from https://github.com/owid/")

    return pd.read_csv(owid_aliases[label] if label in owid_aliases else label)


def clean_columns(df, rename=None, drop=None):
    if rename:
        df.columns = rename
    if drop:
        for c in drop:
            del df[c]

    return df


def get_data_from_file(label):
    if type(label) == list:
        return pd.concat([get_data_from_file(f) for f in label], axis=1)

    filename = None
    for directory in ["bulkhours/data", "./data", "../data", "../../bulkhours/data"]:
        if len((files := glob.glob(f"{directory}/{label}*"))):
            filename = files[0]
    if not filename:
        print(f"No data available for {label}")
        return None

    ext = filename.split(".")[-1]
    if ext in ["png", "jpg", "gif"]:
        return filename
    elif ext == "tsv":
        return pd.read_csv(filename, sep="\t")
    else:
        return pd.read_csv(filename)


def clean_data(df, query=None, index=None):
    if "date" in df.columns:
        df["date"] = pd.to_datetime(df["date"])

    if query:
        df = df.query(query)
    if index:
        if index == 0:
            df = df.set_index(df.columns[0])
        else:
            df = df.set_index(index)
    return df


def get_data(label, credit=False, query=None, index=None):
    if "http" in label or label in owid_aliases:
        df = get_owid_data(label, credit=credit)
    else:
        df = get_data_from_file(label)

    return clean_data(df, query=query, index=index)


def get_image(label, ax=None):
    from PIL import Image

    filename = get_data(label)
    img = Image.open(filename)
    if not ax:
        return img
    ax.imshow(img)
    ax.set_axis_off()
