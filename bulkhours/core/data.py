import glob
import pandas as pd
from .datasets import datasets


def clean_columns(df, data_info):
    if "rename" in data_info:
        df.columns = data_info["rename"]
    if "drop" in data_info:
        for c in data_info["drop"]:
            del df[c]

    return df


def get_data_from_file(label, on=None, **kwargs):
    if type(label) == list:
        if on:
            return pd.concat([get_data_from_file(f).set_index(on) for f in label], axis=1)
        else:
            return pd.concat([get_data_from_file(f) for f in label], axis=1)

    filename = None
    for directory in ["bulkhours/data", "./data", "../data", "../../bulkhours/data"]:
        if len((files := glob.glob(f"{directory}/{label}*"))):
            filename = files[0]
    if not filename:
        print(f"No data available for {label}")
        return None

    ext = filename.split(".")[-1]
    if ext in ["png", "jpg", "gif", "xlsx"]:
        return filename
    elif ext == "xlsx":
        return pd.read_excel(filename, **kwargs)
    elif ext == "tsv":
        return pd.read_csv(filename, sep="\t")
    else:
        return pd.read_csv(filename)


def clean_data(df, query=None, index=None, test_data=None):
    if "date" in df.columns:
        df["date"] = pd.to_datetime(df["date"])

    if query:
        df = df.query(query)

    if test_data:
        df["is_test"] = df.index >= df.index[test_data]

    if index:
        if index == 0:
            df = df.set_index(df.columns[0])
        else:
            df = df.set_index(index)
    return df


def get_core_data(label, modules={}, credit=False, query=None, index=None, test_data=None, **kwargs):
    data_info = (
        datasets[label] if label in datasets else ({"httplink": label} if "http" in label else {"files_list": label})
    )
    data_info.update(kwargs)
    if credit and "source" in data_info:
        print(data_info["source"])

    if (di := label.split(".")[0]) in modules:
        func = label.replace(di + ".", "get_")
        df = getattr(modules[di], func)(credit=credit, **data_info)
    elif "httplink" in data_info:
        df = pd.read_csv(data_info["httplink"])
    else:
        df = get_data_from_file(data_info["files_list"], **data_info)
    df = clean_columns(df, data_info)

    if "filter" in data_info:
        df = data_info["filter"](df)

    return clean_data(df, query=query, index=index, test_data=test_data)


def get_image(label, ax=None):
    from PIL import Image

    filename = get_data_from_file(label)
    img = Image.open(filename)
    if not ax:
        return img
    ax.imshow(img)
    ax.set_axis_off()
