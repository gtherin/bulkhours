import os
import IPython
import ipywidgets
import subprocess

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


def evaluate_core_cpp_project(cinfo, show_solution=False, verbose=False):
    height = "550px"
    # 20 px par ligne
    for o in cinfo.puppet.split(","):
        if "height=" in o:
            height = o.split("=")[1]

    filenames = cinfo.options.split(",")
    os.system("mkdir -p cache")

    if show_solution:
        solution = firebase.get_solution_from_corrector(cinfo.id, corrector="solution")

    files = []
    for t, f in enumerate(filenames):
        ff = f.split(":")
        if not os.path.exists(cfilename := f"cache/{cinfo.id}_{ff[0]}"):
            rfilename = get_data_from_file(f"{cinfo.id}_{ff[0]}", subdir="bulkhours/hpc")
            if verbose:
                print(f"Generate {cfilename} from {rfilename}")

            # Store in files to be compiled
            data = open(rfilename).read()
            with open(cfilename, "w") as f:
                f.write(data)

        if show_solution:
            data1 = ipywidgets.Textarea(
                open(cfilename, "r").read(), layout=ipywidgets.Layout(height=height, width="49%")
            )

            data2 = ipywidgets.Textarea(solution[f], layout=ipywidgets.Layout(height=height, width="49%"))
            # data2 = ipywidgets.Output(layout={"height": height, "width": "49%"})
            # with data2:
            #    IPython.display.display(IPython.display.Code(solution[f]))
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
        self.widget, self.files = evaluate_core_cpp_project(self.cinfo, show_solution=False)
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
            with open(f"cache/{fn}", "w") as f:
                f.write(files[t].value)

        if exec_process:
            print(f"Save files cache/{filenames}, compile and execute program")
            os.system('echo "cd cache && make all && ./main" > cache/main.sh && chmod 777 cache/main.sh')
            print(
                subprocess.run(
                    "bash cache/main.sh".split(), stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True
                ).stdout
            )

        else:
            print(f"Save files cache/{filenames}")

    def basic_execution(self, buttons, bwidget, output):
        htabs = ipywidgets.VBox(children=[bwidget.widget.widget])
        IPython.display.display(htabs)
        IPython.display.display(buttons, output)

    @staticmethod
    def get_core_correction(self, buttons, bwidget, output):
        files = bwidget.widget.files
        filenames = self.cinfo.options.split(",")

        WidgetCodeProject.write_exec_process(self, files, filenames, exec_process=False)

        with output:
            output.clear_output()
            tab2, _ = evaluate_core_cpp_project(self.cinfo, show_solution=True)
            htabs = ipywidgets.HBox([tab2])  # , layout=bwidget.get_layout())
            IPython.display.display(htabs)
        # IPython.display.display(buttons, output)

    @staticmethod
    def submit(self, bwidget, widgets, output):
        files = bwidget.widget.files
        filenames = self.cinfo.options.split(",")

        WidgetCodeProject.write_exec_process(self, files, filenames, exec_process=False)
        pams = {fn: files[t].value for t, fn in enumerate(filenames)}
        pams.update(dict(atype=self.cinfo.type))

        return firebase.send_answer_to_corrector(self.cinfo, **pams)
