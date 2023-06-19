from collections import OrderedDict
import os
import glob
import numpy as np
import pandas as pd


def clean_columns(df, drop=None, rename=None, is_test=None):
    if drop is not None:
        for c in drop:
            del df[c]

    if rename is not None:
        if len(df.columns) != len(rename):
            print("Problem with data columns")
        df.columns = rename

    if is_test is not None:
        df["is_test"] = df.index >= df.index[is_test]

    return df


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


def get_data_from_file(raw_data, **kwargs):
    if "http" in raw_data:
        filename = raw_data
    else:
        filename = None
        directory = os.path.abspath(os.path.dirname(__file__) + "../../../data")
        if len((files := glob.glob(gfile := f"{directory}/{raw_data}*"))):
            filename = files[0]
        else:
            print(f"No data available for {raw_data} ({gfile})")
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
        print(filename, kwargs)
        if "key" in kwargs:
            return np.array(h5py.File(filename, "r")[kwargs["key"]][:])
        elif "format" in kwargs and kwargs["format"] == "filename":
            return filename
        else:
            return h5py.File(filename, "r")
    else:
        return filename


class DataParser:
    datasets = {}
    MODELS_LIST = OrderedDict()

    def __init__(
        self,
        label=None,
        raw_data=None,
        credit=False,
        source=None,
        filter=None,
        query=None,
        index=None,
        test_data=None,
        drop=None,
        rename=None,
        on=None,
        is_test=None,
        **data_info,
    ) -> None:
        self.label, self.raw_data, self.credit = label, raw_data, credit
        self.source, self.filter, self.query, self.index, self.test_data = source, filter, query, index, test_data
        self.data_info = data_info
        self.on = on
        self.drop = drop
        self.rename = rename
        self.is_test = is_test

    def read_raw_data(self, raw_data):
        if type(raw_data) == list:
            if self.on:
                return pd.concat(
                    [get_data_from_file(f, **self.data_info).set_index(self.on) for f in raw_data], axis=1
                )
            else:
                return pd.concat([get_data_from_file(f, **self.data_info) for f in raw_data], axis=1)

        return get_data_from_file(raw_data, **self.data_info)

    def get_data(self):
        if self.credit:
            if self.source is not None:
                print(self.source)
            else:
                print(f"Data {self.label} is not referenced")

        if self.label in DataParser.MODELS_LIST:
            df = DataParser.MODELS_LIST[self.label](self)
        else:
            df = self.read_raw_data(self.raw_data)

        if type(df) == str:
            return df

        df = clean_columns(df, drop=self.drop, rename=self.rename, is_test=self.is_test)

        if self.filter is not None:
            if type(self.filter) == str:
                df = df.query(self.filter)
            else:
                df = self.filter(df)

        return clean_data(df, query=self.query, index=self.index, test_data=self.test_data)

    def get_image(self, ax=None):
        from PIL import Image

        filename = self.read_raw_data(self.label)
        img = Image.open(filename)
        if not ax:
            return img
        ax.imshow(img)
        ax.set_axis_off()


def register(name):
    def wrap(f):
        if name not in DataParser.MODELS_LIST:
            DataParser.MODELS_LIST[name] = f
        else:
            print(f"function for {name} ({f}) already defined")
        return f

    return wrap
