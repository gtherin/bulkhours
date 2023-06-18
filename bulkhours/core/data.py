import os
import glob
import numpy as np
import pandas as pd
from .datasets import ddatasets


def clean_columns(df, data_info):
    if "drop" in data_info:
        for c in data_info["drop"]:
            del df[c]

    if "rename" in data_info:
        if len(df.columns) != len(data_info["rename"]):
            print("Problem with data columns")
        df.columns = data_info["rename"]

    if "is_test" in data_info:
        df["is_test"] = df.index >= df.index[data_info["is_test"]]

    return df


def get_data_from_file(raw_data, on=None, subdir="data", **kwargs):
    if type(raw_data) == list:
        if on:
            return pd.concat([get_data_from_file(f).set_index(on) for f in raw_data], axis=1)
        else:
            return pd.concat([get_data_from_file(f) for f in raw_data], axis=1)

    if "http" in raw_data:
        filename = raw_data
    else:
        filename = None
        for directory in [
            "bulkhours",
            ".",
            "..",
            "../../bulkhours",
            "../../../bulkhours",
            os.environ["HOME"] + "/projects/bulkhours",
        ]:
            if len((files := glob.glob(f"{directory}/{subdir}/{raw_data}*"))):
                filename = files[0]
        if not filename:
            print(f"No data available for {raw_data}")
            return None

    import h5py

    ext = filename.split(".")[-1]
    if ext == "xlsx":
        return pd.read_excel(filename, **kwargs)
    elif ext == "tsv":
        return pd.read_csv(filename, sep="\t")
    elif ext in ["csv"]:
        return pd.read_csv(filename)
    elif ext in ["h5"]:
        if "key" in kwargs:
            return np.array(h5py.File(filename, "r")[kwargs["key"]][:])
        elif "format" in kwargs and kwargs["format"] == "filename":
            return filename
        else:
            return h5py.File(filename, "r")
    else:
        return filename


def clean_data(df, query=None, index=None, test_data=None):
    if type(df).__module__ == "numpy" or type(df) in [list, dict]:
        return df

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


def get_core_data(label, modules={}, credit=True, query=None, index=None, test_data=None, **kwargs):
    data_info = ddatasets[label] if label in ddatasets else {"raw_data": label}
    data_info.update(kwargs)
    if credit:
        if "source" in data_info:
            print(data_info["source"])
        else:
            print(f"Data {label} is not referenced")

    if (di := label.split(".")[0]) in modules:
        func = label.replace(di + ".", "get_")
        print(func, getattr(modules[di], func))
        df = getattr(modules[di], func)(**data_info)
    else:
        data_info2 = {k: v for k, v in data_info.items() if k != "raw_data"}
        df = get_data_from_file(data_info["raw_data"], **data_info2)

    if type(df) == str:
        return df

    df = clean_columns(df, data_info)

    if "filter" in data_info:
        df = data_info["filter"](df)

    return clean_data(df, query=query, index=index, test_data=test_data)


class DataDocInterpreter:
    def __init__(self, func):
        self.func = func
        self.docstring = func.__doc__

    @property
    def doc(self):
        return self.docstring

    @property
    def data(self):
        df = {}

        directory = os.path.abspath(os.path.dirname(__file__) + f"/../../data/")

        for e, l in enumerate(self.docstring.splitlines()):
            if e == 0:
                df["description"] = l
            elif ":" in l:
                key, value = l[: l.find(":")], l[l.find(":") + 1 :]
                key = key.replace(" ", "").replace("-", "").lower()
                if key == "datafile":
                    value = value.replace(" ", "").replace("bulkhours:/", directory)

                    df[key] = value

        return df

    def generate_readme(self):
        df = self.func(credit=True)
        return self.docstring


def get_image(label, ax=None):
    from PIL import Image

    filename = get_data_from_file(label)
    img = Image.open(filename)
    if not ax:
        return img
    ax.imshow(img)
    ax.set_axis_off()
