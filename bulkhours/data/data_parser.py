from collections import OrderedDict
import os
import glob
import numpy as np
import pandas as pd
import IPython
import inspect


def get_rdata(rdata):
    if "http" in rdata:
        label = rdata.split("/")[-1]
        if "raw.githubusercontent.com" in rdata:
            address = rdata.replace("raw.githubusercontent.com", "github.com")
            return f"[{label}]({address})  ([raw]({rdata}))"
        else:
            address = rdata.replace("github.com", "raw.githubusercontent.com").replace("blob/", "")
            return f"[{label}]({rdata})  ([raw]({address}))"
    if type(rdata) in [list]:
        return ", ".join([f"[{f}](https://github.com/guydegnol/bulkhours/blob/main/data/{f})" for f in rdata])
    return f"[{rdata}](https://github.com/guydegnol/bulkhours/blob/main/data/{rdata})"


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
    if type(df) != pd.DataFrame:
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
        kwargs = {k: v for k, v in kwargs.items() if k not in ["summary", "category"]}
        return pd.read_excel(filename)  # , **kwargs)
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


class DataParser:
    datasets = OrderedDict()
    clean_datasets = OrderedDict()

    @staticmethod
    def get_data_from_file(raw_data, **kwargs):
        return get_data_from_file(raw_data, **kwargs)

    def __init__(
        self,
        label=None,
        raw_data=None,
        credit=True,
        source=None,
        query=None,
        index=None,
        test_data=None,
        drop=None,
        rename=None,
        on=None,
        is_test=None,
        func=None,
        **data_info,
    ) -> None:
        self.label, self.raw_data, self.credit = label, raw_data, credit
        self.source, self.query, self.index, self.test_data = source, query, index, test_data
        self.data_info = data_info
        self.on = on
        self.drop = drop
        self.rename = rename
        self.is_test = is_test
        self.func = func

    @staticmethod
    def declare_data(func=None, label=None, **info):
        DataParser.datasets[label] = dict(label=label, func=func, **info)

    @staticmethod
    def register_dataset(**info):
        DataParser.declare_data(**info)

        def wrap(f):
            lines = "\n".join(inspect.getsource(f).splitlines())
            func_code = "def " + lines.split("def ")[1]
            DataParser.declare_data(func=f, func_code=func_code, **info)
            return f

        return wrap

    @staticmethod
    def save_dataset(**info):
        def wrap(f):
            # TODO: finish the saving function
            # Parse the filename file:
            #   - Extract the dict with label and func_names
            # Check if the new function is not in the list
            #   - If no, add it to the list
            #   - If yes, don't add it
            lines = "\n".join(inspect.getsource(f).splitlines()[1:])
            func_name = lines.split("def ")[1].split("(")[0]
            label = lines.split("label=")[1].split(",")[0]
            # print(func_name, label)
            return f

        return wrap

    def get_info(self, load_columns=False, summary=False):
        columns = None
        if load_columns:
            try:
                data = self.get_data(credit=False)
                columns = list(data.columns)
            except:
                pass

        d = self.data_info
        comment = ""
        if "summary" in d:
            comment += f"#### {d['summary']}\n"

        if not summary:
            comment += f'#### `bulkhours.get_data("{self.label}")`\n'
        if self.raw_data is not None:
            comment += f"- Raw data: {get_rdata(self.raw_data)}\n"
        if "enrich_data" in d:
            comment += f"- Enrich data: {get_rdata(d['enrich_data'])}\n"
        if "source" in d:
            comment += d["source"] + "\n"
        if "ref_source" in d:
            comment += f"- Direct source: {d['ref_source']}\n"
        if "ref_site" in d:
            comment += f"- Reference site: {d['ref_site']}\n"

        if 1:
            cols = ""
            if "columns_info" in d:
                cols = f"> {d['columns_info']}\n"

            if "columns_description" in d:
                cols += f"\n{d['columns_description']}\n"
            else:
                if columns is None:
                    try:
                        data = self.get_data(credit=False)
                        columns = list(data.columns)
                    except:
                        pass
                if columns is not None:
                    cols += """\n| Column   |      Info |\n|-----------|:-----------|\n"""
                    for c in columns:
                        cols += f"| {c} |  |\n"

            if cols != "":
                comment += f"""\n<details>\n<summary>Show columns info</summary>\n{cols}\n</details>\n\n"""

        if "func_code" in d:
            comment += (
                f"""\n<details>\n<summary>Show code</summary>\n<code>\n{d["func_code"]}\n</code>\n</details>\n\n"""
            )
        return comment

    def read_raw_data(self, raw_data):
        if type(raw_data) == list:
            if self.on:
                return pd.concat(
                    [get_data_from_file(f, **self.data_info).set_index(self.on) for f in raw_data], axis=1
                )
            else:
                return pd.concat([get_data_from_file(f, **self.data_info) for f in raw_data], axis=1)

        return get_data_from_file(raw_data, **self.data_info)

    def get_data(self, credit=None):
        if self.func is not None:
            df = self.func(self)
        else:
            df = self.read_raw_data(self.raw_data)

        credit = credit if credit is not None else self.credit

        if credit:
            if "summary" in self.data_info:
                comment = self.get_info(load_columns=False, summary=True)

                IPython.display.display(IPython.display.Markdown(f"""{comment}"""))
                print(
                    f"\x1b[31mBulkHours database info:\x1b[0m https://github.com/guydegnol/bulkhours/blob/main/data/README.md"
                )
                print(f'bulkhours.get_data("{self.label}", credit=\033[1mFalse\033[0m)  # To stop showing this text')

            elif not (".gif" in self.label or ".png" in self.label):
                print(f"Data {self.label} is not referenced")

        if type(df) == str:
            return df

        df = clean_columns(df, drop=self.drop, rename=self.rename, is_test=self.is_test)
        return clean_data(df, query=self.query, index=self.index, test_data=self.test_data)

    def get_image(self, ax=None):
        from PIL import Image

        filename = self.read_raw_data(self.label)
        img = Image.open(filename)
        if not ax:
            return img
        ax.imshow(img)
        ax.set_axis_off()

    @staticmethod
    def build_clean_datasets():
        if len(DataParser.clean_datasets) == 0:
            datasets2 = {}
            for k, data_info in DataParser.datasets.items():
                if "reference" in data_info and (lr := data_info["reference"]) in DataParser.datasets:
                    datasets2[k] = {**DataParser.datasets[lr], **data_info}
                else:
                    datasets2[k] = data_info
            DataParser.clean_datasets = datasets2
