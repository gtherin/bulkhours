import pandas as pd

from ..hpc import flops
from .data_parser import register_dataset


@register_dataset("hpc.transistor_count")
def get_dfistor_count(self):
    columns = ["processor", "count", "date", "designer", "manufacturer", "engraving_scale", "area", "density", "ref"]
    df = flops.get_table_from_wiki(wpage="Transistor_count", in_table="Voodoo Graphics", columns=columns)
    return df.iloc[:-1]


@register_dataset("hpc.engraving_scale")
def get_engraving_scale(self):
    return flops.get_engraving_scale(verbose=True)


@register_dataset("hpc.FLOPS_units")
def get_FLOPS(self):
    return flops.get_table_from_wiki("FLOPS", "Computer performance")


@register_dataset("hpc.FLOPS_gpus")
def get_FLOPS(self):
    return flops.get_table_from_wiki("FLOPS", "NVIDIA", columns=["date", "un_costs", "costs", "platform", "comments"])


@register_dataset("hpc.FLOPS_cpus")
def get_cpus(self):
    columns = ["processor", "count", "date", "designer", "engraving_scale", "area", "density"]
    df = flops.get_table_from_wiki(
        wpage="Transistor_count", in_table="20-bit, 6-chip, 28 chips total", columns=columns
    )
    df = df.iloc[:-1]
    df["date"] = df["date"].str.replace("March ", "").str.replace("November ", "")
    df["date"] = df["date"].str.replace("March ", "").str.replace("November ", "")
    df["date"] = df["date"].str.split("[").str[0].astype(int)

    df["count"] = df["count"].str.replace(",", "")
    df["count"] = df["count"].str.split("[").str[0]
    df["count"] = df["count"].str.split("+").str[0]
    df["count"] = df["count"].str.split(" ").str[0]
    df["count"] = pd.to_numeric(df["count"], errors="coerce")

    df["engraving_scale"] = df["engraving_scale"].str.split("[").str[0]
    df["engraving_scale"] = df["engraving_scale"].str.replace(",", "")
    df["engraving_scale"] = df["engraving_scale"].str.split("(").str[0]
    df["engraving_scale"] = df["engraving_scale"].str.replace("\xa0nm", "")
    df["engraving_scale"] = df["engraving_scale"].str.replace("nm", "")
    df["engraving_scale"] = pd.to_numeric(df["engraving_scale"], errors="coerce")

    l = [3, 4, 6, 8, 15, 23, 50, 80, 150, 300, 500, 800, 1000, 3000, 5000, 10000]
    df["engraving_scale2"] = pd.cut(df["engraving_scale"], bins=l, include_lowest=True)
    df["engraving_scale3"] = df["engraving_scale2"].map(
        dict(zip(df["engraving_scale2"].unique(), range(len(df["engraving_scale2"].unique()))))
    )
    df["engraving_scale3"] = df["engraving_scale3"].fillna(1).astype(float)

    return df
