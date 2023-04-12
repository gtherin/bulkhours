import os
import IPython
import ipywidgets

from .buttons import *
from ..logins import *
from .. import firebase
from . import base


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


def evaluate_core_cpp_project(cinfo, cell, show_solution=False):
    height = "550px"
    for o in cinfo.puppet.split(","):
        if "height=" in o:
            height = o.split("=")[1]

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

        if show_solution:
            data1 = ipywidgets.Textarea(
                open(cfilename, "r").read(), layout=ipywidgets.Layout(height=height, width="49%")
            )
            data2 = ipywidgets.Output(layout={"height": height, "width": "49%"})
            with data2:
                IPython.display.display(IPython.display.Code(open(cfilename, "r").read()))
            data = ipywidgets.HBox([data1, data2])
        else:
            data = ipywidgets.Textarea(
                open(cfilename, "r").read(), layout=ipywidgets.Layout(height=height, width="99%")
            )

        files.append(data)

    tab = ipywidgets.Tab(children=files)
    for t, f in enumerate(filenames):
        tab.set_title(t, f)
    return tab, files


class WidgetCodeProject(base.WidgetBase):
    def get_widget(self):
        self.widget, self.files = evaluate_core_cpp_project(self.cinfo, self.cell, show_solution=False)
        return self.widget

    def get_answer(self):
        return self.widget

    def get_params(self, answer):
        return dict(answer=answer, atype=self.cinfo.type)

    @staticmethod
    def write_exec_process(self, files, filenames, exec_process=True):
        for t, fn in enumerate(filenames):
            with open(f"cache/{self.cinfo.id}_{fn}", "w") as f:
                f.write(files[t].value)
            print(f"Generate cache/{fn}")
            with open(f"cache/{fn}", "w") as f:
                f.write(files[t].value)

        if exec_process:
            os.system(f"cd cache && make all && ./main")

    def basic_execution(self, buttons, bwidget, output):
        htabs = ipywidgets.VBox(children=[bwidget.widget.widget])
        IPython.display.display(htabs)
        IPython.display.display(buttons, output)

    @staticmethod
    def get_core_correction(self, buttons, bwidget, output, cell):
        tab2, _ = evaluate_core_cpp_project(self.cinfo, cell, show_solution=True)
        htabs = ipywidgets.HBox([tab2])  # , layout=bwidget.get_layout())
        IPython.display.display(htabs)
        IPython.display.display(buttons, output)

    # @staticmethod
    # def get_core_correction(self, bwidget, widgets):
    #    data = firebase.get_solution_from_corrector(self.cinfo.id, corrector="solution")
    #    return BulkWidget.display_correction(self, bwidget, widgets, data)

    @staticmethod
    def submit(self, bwidget, widgets, output):
        files = bwidget.widget.files
        filenames = self.cinfo.options.split(",")

        WidgetCodeProject.write_exec_process(self, files, filenames, exec_process=False)
        pams = {fn: files[t].value for t, fn in enumerate(filenames)}
        pams.update(dict(atype=self.cinfo.type))

        return firebase.send_answer_to_corrector(self.cinfo, update_time=False, **pams)
