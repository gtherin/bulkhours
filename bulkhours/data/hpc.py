import pandas as pd

from ..hpc import flops
from .data_parser import DataParser


@DataParser.register_dataset(
    label="hpc.transistor_count",
    summary="transistor_count",
    category="Computing",
    ref_site="https://en.wikipedia.org/wiki/Transistor_count",
)
def get_dfistor_count(self):
    columns = ["processor", "count", "date", "designer", "manufacturer", "engraving_scale", "area", "density", "ref"]
    df = flops.get_table_from_wiki(wpage="Transistor_count", in_table="Voodoo Graphics", columns=columns)
    return df.iloc[:-1]


@DataParser.register_dataset(
    label="hpc.engraving_scale",
    summary="Semiconductor device fabrication: MOSFET scaling",
    category="Computing",
    ref_site="https://en.wikipedia.org/wiki/Transistor_count",
)
def get_engraving_scale(self):
    return flops.get_engraving_scale(verbose=True)


@DataParser.register_dataset(
    label="hpc.FLOPS_units",
    summary="FLOPS sub-units",
    category="Computing",
    ref_site="https://en.wikipedia.org/wiki/FLOPS",
)
def get_FLOPS(self):
    return flops.get_table_from_wiki("FLOPS", "Computer performance")


@DataParser.register_dataset(
    label="hpc.FLOPS_gpus",
    summary="FLOPS for gpus",
    category="Computing",
    ref_site="https://en.wikipedia.org/wiki/FLOPS",
)
def get_gpus(self):
    return flops.get_table_from_wiki("FLOPS", "NVIDIA", columns=["date", "un_costs", "costs", "platform", "comments"])

@DataParser.register_dataset(
    label="hpc.FLOPS_cpus",
    summary="FLOPS for cpus",
    category="Computing",
    ref_site="https://en.wikipedia.org/wiki/FLOPS",
)
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

@DataParser.register_dataset(
    label="hpc.FLOPS_costs",
    summary="Costs of FLOPS",
    category="Computing",
    ref_site="https://en.wikipedia.org/wiki/FLOPS",
)
def get_costs(self):
    return flops.get_table_from_wiki("FLOPS", "Approximate USD per GFLOPS")#, columns=["date", "un_costs", "costs", "platform", "comments"])

DataParser.register_dataset(
    label="hpc.green500",
    summary="Energy Efficiency (GFlops/watts)",
    category="Computing",
    ref_site="https://www.top500.org/lists/green500/2023/06/",
    raw_data="https://huggingface.co/datasets/guydegnol/bulkhours/raw/main/green500_top_202306.xlsx",
)

DataParser.register_dataset(
    label="hpc.top500",
    summary="Energy Efficiency (GFlops/watts)",
    category="Computing",
    ref_site="https://www.top500.org/lists/top500/2023/06/",
    raw_data="https://huggingface.co/datasets/guydegnol/bulkhours/raw/main/TOP500_202306.xlsx",
)
