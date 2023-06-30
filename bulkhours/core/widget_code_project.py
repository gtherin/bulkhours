import os
import IPython
import ipywidgets
import subprocess
import glob
from argparse import Namespace

from . import widget_base
from . import tools


def evaluate_core_cpp_project(cinfo, show_solution=False, verbose=False):
    from . import firebase

    height, width = "550px", "900px"
    # 20 px par ligne
    for o in cinfo.puppet.split(","):
        if "height=" in o:
            height = o.split("=")[1]
        if "width=" in o:
            width = o.split("=")[1]

    midwidth = "%.0fpx" % (int(width[:-2]) / 2)

    filenames = cinfo.options.split(",")
    os.system("mkdir -p cache")

    if show_solution:
        solution = firebase.get_solution_from_corrector(cinfo.cell_id, corrector="solution", cinfo=cinfo)
        solution = {k.replace("_dot_", "."): v for k, v in solution.items()}

    files = []
    for t, f in enumerate(filenames):
        ff = f.split(":")
        if not os.path.exists(cfilename := f"cache/{cinfo.cell_id}_{ff[0]}"):
            rfilename = tools.abspath(f"data/exercices/{cinfo.cell_id}_{ff[0]}")
            if verbose:
                print(f"Generate {cfilename} from {rfilename}")

            # Store in files to be compiled
            data = open(rfilename).read()
            with open(cfilename, "w") as f:
                f.write(data)

        if show_solution:
            if os.path.exists("/content"):
                data1 = ipywidgets.Output(layout={"height": height, "width": midwidth})
                with data1:
                    IPython.display.display(IPython.display.Code(open(cfilename, "r").read()))

                data2 = ipywidgets.Output(layout={"height": height, "width": midwidth})
                with data2:
                    IPython.display.display(IPython.display.Code(solution[f]))
            else:
                data1 = ipywidgets.Textarea(
                    open(cfilename, "r").read(), layout=ipywidgets.Layout(height=height, width=midwidth)
                )
                data2 = ipywidgets.Textarea(solution[f], layout=ipywidgets.Layout(height=height, width=midwidth))

            data = ipywidgets.HBox([data1, data2])

        else:
            data = ipywidgets.Textarea(
                open(cfilename, "r").read(), layout=ipywidgets.Layout(height=height, width=width)
            )

        files.append(data)

    tab = ipywidgets.Tab(children=files)
    for t, f in enumerate(filenames):
        tab.set_title(t, f)
    return tab, files


class WidgetCodeProject(widget_base.WidgetBase):
    widget_id = "code_project"
    widget_comp = "w|tsc"

    def init_widget(self):
        self.widget, self.files = evaluate_core_cpp_project(self.cinfo, show_solution=False)
        return self.widget

    def get_answer(self):
        return self.widget

    def write_exec_process(self, output, exec_process=True):
        files = self.files
        filenames = self.cinfo.options.split(",")

        for t, fn in enumerate(filenames):
            with open(f"cache/{self.cinfo.cell_id}_{fn}", "w") as f:
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

    def display_ecorrection(self, output):
        IPython.display.display(self.cinfo)
        self.write_exec_process(output, exec_process=False)

        with output:
            output.clear_output()
            tab2, _ = evaluate_core_cpp_project(self.cinfo, show_solution=True)
            htabs = ipywidgets.HBox([tab2])  # , layout=self.get_layout())
            IPython.display.display(htabs)
        # IPython.display.display(buttons, output)

    def submit(self, output, user=None):
        from . import firebase

        files = self.files
        filenames = self.cinfo.options.split(",")

        cinfo = Namespace(**vars(self.cinfo))

        if user is not None:
            cinfo.user = user

        with output:
            output.clear_output()

            self.write_exec_process(output, exec_process=False)
            pams = {fn.replace(".", "_dot_"): files[t].value for t, fn in enumerate(filenames)}
            pams.update(dict(atype=cinfo.type))

            return firebase.send_answer_to_corrector(cinfo, **pams)

    def execute_raw_cell(self, bbox, output):
        htabs = ipywidgets.VBox(children=[self.widget])
        IPython.display.display(htabs)
        IPython.display.display(bbox[1], output)
