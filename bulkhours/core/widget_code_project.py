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
    for directory in ["bulkhours", ".", "..", "../../bulkhours", "../../../bulkhours"]:
        if len((files := glob.glob(f"{directory}/{subdir}/{label}*"))):
            filename = files[0]
    if not filename:
        print(f"No data available for {label}")
        return None
    return filename


def evaluate_cpp_project(cinfo, cell):
    layout = ipywidgets.Layout(height="500px", width="500px")

    filenames = cinfo.options.split(",")
    os.system("mkdir -p cache")

    files = []
    for f in filenames:
        cfilename = f"cache/{cinfo.id}_{f}"
        if not os.path.exists(cfilename):
            print(f"Generate {cfilename}")
            rfilename = get_data_from_file(f"{cinfo.id}_{f}", subdir="bulkhours/hpc")

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
        for t, f in enumerate(filenames):
            cfilename = f"cache/{eid}_{f}"
            with open(cfilename, "w") as f:
                f.write(files[t].value)

        cmd = f"/usr/bin/gcc main.cpp -o main.out"
        subprocess.check_output(cmd.split(), stderr=subprocess.STDOUT)
        subprocess.check_output("main.out")

    button.on_click(write_exec_process)
    return ipywidgets.VBox(children=[tab, button])
