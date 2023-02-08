import glob
import pandas as pd


core_datasets = {
    "vaccinations": dict(
        httplink="https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/vaccinations/vaccinations.csv",
        source="https://ourworldindata.org/coronavirus",
    ),
    "covid": dict(
        httplink="https://covid.ourworldindata.org/data/owid-covid-data.csv",
        source="https://ourworldindata.org/coronavirus",
    ),
    "poverty": dict(
        httplink="https://nyc3.digitaloceanspaces.com/owid-public/data/poverty/pip_dataset.csv",
        source="World Bank Poverty and Inequality Platform\nhttps://ourworldindata.org/poverty\nhttps://pip.worldbank.org/",
    ),
    "supercomputers": dict(
        httplink="https://raw.githubusercontent.com/owid/owid-datasets/dd7a4ecbb249f98028e25c304ef7d68de8979ea9/datasets/Supercomputer%20power%20(FLOPS)%20%E2%80%93%20TOP500%20Database/Supercomputer%20power%20(FLOPS)%20%E2%80%93%20TOP500%20Database.csv",
        source="https://ourworldindata.org/grapher/supercomputer-power-flops",
    ),
}


def clean_columns(df, data_info):
    if "rename" in data_info:
        df.columns = data_info["rename"]
    if "drop" in data_info:
        for c in data_info["drop"]:
            del df[c]

    return df


def get_data_from_file(label, **kwargs):
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
    if ext in ["png", "jpg", "gif", "xlsx"]:
        return filename
    elif ext == "xlsx":
        return pd.read_excel(filename, **kwargs)
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


def get_core_data(label, datasets={}, modules={}, credit=False, query=None, index=None, **kwargs):
    datasets.update(core_datasets)
    data_info = (
        datasets[label] if label in datasets else ({"httplink": label} if "http" in label else {"files_list": label})
    )
    if credit and "source" in data_info:
        print(data_info["source"])

    if (di := label.split(".")[0]) in modules:
        func = label.replace(di + ".", "get_")
        df = getattr(modules[di], func)(credit=credit, **kwargs)
    elif "httplink" in data_info:
        df = pd.read_csv(data_info["httplink"])
    else:
        df = get_data_from_file(data_info["files_list"], **kwargs)
    df = clean_columns(df, data_info)

    if "filter" in data_info:
        df = data_info["filter"](df)

    return clean_data(df, query=query, index=index)


def get_image(label, ax=None):
    from PIL import Image

    filename = get_data_from_file(label)
    img = Image.open(filename)
    if not ax:
        return img
    ax.imshow(img)
    ax.set_axis_off()
