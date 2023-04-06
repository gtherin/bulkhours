import os
import subprocess

from IPython.core.magic import Magics, cell_magic, magics_class, line_cell_magic, needs_local_scope
import IPython
import ipywidgets

from .textstyles import *
from .logins import *
from . import firebase
from . import install
from .widgets import BulkWidget


def get_data_from_file(label, on=None, subdir="data", **kwargs):
    import glob

    filename = None
    for directory in [
        "bulkhours",
        ".",
        "..",
        "../../bulkhours",
        "../../../bulkhours",
        os.environ["HOME"] + "/projects/bulkhours",
    ]:
        if len((files := glob.glob(f"{directory}/{subdir}/{label}*"))):
            filename = files[0]
    if not filename:
        print(f"No data available for {subdir}/{label}")
        return None
    return filename


def evaluate_cpp_project(cinfo, cell):
    height = "550px"
    for o in cinfo.puppet.split(","):
        if "height=" in o:
            height = o.split("=")[1]

    layout = ipywidgets.Layout(height=height, width="99%")

    filenames = cinfo.options.split(",")
    os.system("mkdir -p cache")

    files = []
    for t, f in enumerate(filenames):
        ff = f.split(":")
        if not os.path.exists(cfilename := f"cache/{cinfo.id}_{ff[0]}"):
            rfilename = get_data_from_file(f"{cinfo.id}_{ff[0]}", subdir="bulkhours/hpc")
            print(f"Generate {cfilename} from {rfilename}")

            data = open(rfilename).read()
            with open(cfilename, "w") as f:
                f.write(data)
        data = open(cfilename, "r").read()
        files.append(ipywidgets.Textarea(open(cfilename, "r").read(), layout=layout))

    tab = ipywidgets.Tab(children=files)
    for t, f in enumerate(filenames):
        tab.set_title(t, f)

    button = ipywidgets.Button(description="Compile and Execute")

    def write_exec_process(b):
        for t, fn in enumerate(filenames):
            with open(f"cache/{cinfo.id}_{fn}", "w") as f:
                f.write(files[t].value)
            print(f"Generate cache/{fn}")
            with open(f"cache/{fn}", "w") as f:
                f.write(files[t].value)

        os.system(f"cd cache && make all && ./main")

    button.on_click(write_exec_process)
    return ipywidgets.VBox(children=[tab, button])
