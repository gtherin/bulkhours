from . import tools
from . import hpc


@tools.register("hpc.transistor_count")
def get_transistor_count(self):
    return hpc.get_table_from_wiki(
        wpage="Transistor_count",
        in_table="Voodoo Graphics",
        columns=[
            "processor",
            "count",
            "date",
            "designer",
            "manufacturer",
            "engraving_scale",
            "area",
            "density",
            "ref",
            # "dummy",
        ],
    )


@tools.register("hpc.engraving_scale")
def get_engraving_scale(self):
    return hpc.get_engraving_scale(verbose=True)


@tools.register("hpc.FLOPS_units")
def get_FLOPS(self):
    return hpc.get_table_from_wiki("FLOPS", "Computer performance")


@tools.register("hpc.FLOPS_gpus")
def get_FLOPS(self):
    return hpc.get_table_from_wiki("FLOPS", "NVIDIA", columns=["date", "un_costs", "costs", "platform", "comments"])


@tools.register("hpc.FLOPS_cpus")
def get_cpus(self):
    return hpc.get_table_from_wiki(
        wpage="Transistor_count",
        in_table="20-bit, 6-chip, 28 chips total",
        columns=["processor", "count", "date", "designer", "engraving_scale", "area", "density"],
    )
