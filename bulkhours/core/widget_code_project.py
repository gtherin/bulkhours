import os
import IPython
import ipywidgets
import subprocess
from argparse import Namespace

from . import widget_base
from . import tools
from . import installer


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
    os.system(f"mkdir -p {cinfo.cell_id}")

    if show_solution:
        solution = firebase.get_solution_from_corrector(
            cinfo.cell_id, corrector=tools.REF_USER, cinfo=cinfo
        )
        solution = {k.replace("_dot_", "."): v for k, v in solution.items()}

    if os.path.exists(
        rfilename := tools.abspath(f"data/exercices/{cinfo.cell_id}.uno")
    ):
        code = installer.unobscure(open(rfilename, "r").read())
    elif os.path.exists(
        rfilename := tools.abspath(f"data/exercices/{cinfo.cell_id}_reset.txt")
    ):
        code = open(rfilename, "r").read()

    files_code = code.replace("BKRESET", "BULKHOURS").split("// BULKHOURS.SPLIT:")[1:]
    rfiles = {f[: f.find("\n")]: f[f.find("\n") + 1 :] for f in files_code}

    files = []
    for t, f in enumerate(filenames):
        ff = f.split(":")
        cfilename = f"{cinfo.cell_id}/{ff[0]}"
        if not os.path.exists(cfilename := f"{cinfo.cell_id}/{ff[0]}"):
            if verbose:
                print(f"Generate {cfilename} from {rfilename}")

            # Store in files to be compiled
            data = rfiles[ff[0]]
            with open(cfilename, "w") as f:
                f.write(data)

        if show_solution:
            if os.path.exists("/content"):
                data1 = ipywidgets.Output(layout={"height": height, "width": midwidth})
                with data1:
                    IPython.display.display(
                        IPython.display.Code(open(cfilename, "r").read())
                    )

                data2 = ipywidgets.Output(layout={"height": height, "width": midwidth})
                with data2:
                    IPython.display.display(IPython.display.Code(solution[f]))
            else:
                data1 = ipywidgets.Textarea(
                    open(cfilename, "r").read(),
                    layout=ipywidgets.Layout(height=height, width=midwidth),
                )
                data2 = ipywidgets.Textarea(
                    solution[f], layout=ipywidgets.Layout(height=height, width=midwidth)
                )

            data = ipywidgets.HBox([data1, data2])

        else:
            data = ipywidgets.Textarea(
                open(cfilename, "r").read(),
                layout=ipywidgets.Layout(height=height, width=width),
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
        self.widget, self.files = evaluate_core_cpp_project(
            self.cinfo, show_solution=False
        )
        return self.widget

    def get_answer(self):
        return self.widget

    def write_exec_process(self, output, exec_process=True):
        files = self.files
        filenames = self.cinfo.options.split(",")

        for t, fn in enumerate(filenames):
            with open(f"{self.cinfo.cell_id}/{fn}", "w") as f:
                f.write(files[t].value)

        if exec_process:
            print(
                f"Save files {self.cinfo.cell_id}/{filenames}, compile and execute program"
            )
            os.system(
                f'echo "cd {self.cinfo.cell_id} && make all && ./main" > {self.cinfo.cell_id}/main.sh && chmod 777 {self.cinfo.cell_id}/main.sh'
            )
            print(
                subprocess.run(
                    f"bash {self.cinfo.cell_id}/main.sh".split(),
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    text=True,
                ).stdout
            )

        else:
            print(f"Save files {self.cinfo.cell_id}/{filenames}")

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
            pams = {
                fn.replace(".", "_dot_"): files[t].value
                for t, fn in enumerate(filenames)
            }
            pams.update(dict(atype=cinfo.type))

            return firebase.send_answer_to_corrector(cinfo, **pams)

    def execute_raw_cell(self, bbox, output):
        htabs = ipywidgets.VBox(children=[self.widget])
        IPython.display.display(htabs)
        IPython.display.display(bbox[1], output)
