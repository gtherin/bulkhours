import os
import subprocess
import time

from IPython.core.magic import Magics, cell_magic, magics_class, line_cell_magic, needs_local_scope
import IPython
import ipywidgets

from .widgets.buttons import *
from .logins import *
from . import firebase
from . import install
from .widgets.bulk_widget import BulkWidget
from .widgets.code_project import evaluate_core_cpp_project
from . import colors


@magics_class
class Evaluation(Magics):
    def __init__(self, shell, nid, in_french):
        super(Evaluation, self).__init__(shell)
        self.show_answer = True
        self.nid = nid
        self.in_french = in_french
        self.cinfo = None

    @property
    def cell_id(self):
        if self.cinfo.id[0] == "I":
            return self.nid + "_" + self.cinfo.id[1:]
        else:
            return self.cinfo.id

    @line_cell_magic
    @needs_local_scope
    def message_cell_id(self, line, cell="", local_ns=None):
        self.cinfo = install.get_argparser(line, cell)
        firebase.send_answer_to_corrector(self.cinfo, **{self.cinfo.user: cell})

    @line_cell_magic
    @needs_local_scope
    def update_cell_id(self, line, cell="", local_ns=None):
        self.cinfo = install.get_argparser(line, cell)
        if not self.cinfo:
            return

        opts = {
            a.split(":")[0]: cell if a.split(":")[1] == "CELL" else a.split(":")[1]
            for a in self.cinfo.options.split(";")
        }
        firebase.send_answer_to_corrector(self.cinfo, user=self.cinfo.user, **opts)

    @line_cell_magic
    @needs_local_scope
    def evaluation_cell_id(self, line, cell="", local_ns=None):
        self.cinfo = install.get_argparser(line, cell)
        if not self.cinfo:
            return

        output = ipywidgets.Output()
        if self.cinfo.user == "solution":
            colors.set_style(output, "sol_background")

        bwidget = BulkWidget(self.cinfo, cell, in_french=self.in_french)

        owidgets = {
            "l": bwidget.get_label(),
            "s": sbuttons[0].g(self.in_french),
            "c": sbuttons[1].g(self.in_french),
            "m": sbuttons[2].g(self.in_french),
            "t": sbuttons[3].g(self.in_french),
            "o": sbuttons[4].g(self.in_french),
        }
        widgets = bwidget.get_widgets()
        import multiprocessing

        def update_button(b, i, funct, args, kwargs):
            with output:
                output.clear_output()
                IPython.display.display(
                    IPython.display.HTML(
                        '<link rel="stylesheet" href="//stackpath.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css"/>'
                    )
                )

                colors.set_style(output, "sol_background")
                self.show_answer = not self.show_answer
                sbuttons[i].update_style(b, style="warning")
                if not self.show_answer:
                    try:
                        p1 = multiprocessing.Process(target=funct, args=args, kwargs=kwargs)
                        p1.start()
                        loop = ["plane", "rocket", "space-shuttle"]
                        ii = 0

                        while p1.is_alive():
                            print(p1.is_alive(), loop[ii % len(loop)])
                            sbuttons[i].icon = loop[ii % len(loop)]
                            time.sleep(0.5)
                            ii += 1

                        # funct(*args, **kwargs)
                    except TypeError as e:
                        sbuttons[i].update_style(b, style="danger")
                    except Exception as e:
                        sbuttons[i].update_style(b, style="danger")

                self.show_answer = sbuttons[i].wait(self.show_answer, b)
                sbuttons[i].update_style(b, style="on" if self.show_answer else "off")

        def submit(b):
            return update_button(b, 0, BulkWidget.submit, [self, bwidget, widgets, output], dict())

        owidgets["s"].on_click(submit)

        def get_correction(b):
            return update_button(b, 1, BulkWidget.get_core_correction, [self, bwidget, widgets], dict())

        owidgets["c"].on_click(get_correction)

        def send_message(b):
            return update_button(b, 2, BulkWidget.send_message, [self], dict())

        owidgets["m"].on_click(send_message)

        def write_exec_process1(self, files, filenames):
            for t, fn in enumerate(filenames):
                with open(f"cache/{self.cinfo.id}_{fn}", "w") as f:
                    f.write(files[t].value)
                print(f"Generate cache/{fn}")
                with open(f"cache/{fn}", "w") as f:
                    f.write(files[t].value)

            os.system(f"cd cache && make all && ./main")

        def write_exec_process(b):
            return update_button(b, 4, write_exec_process1, [self, files, filenames], dict())

        owidgets["o"].on_click(write_exec_process)

        bbox = []
        ws = []
        for w in self.cinfo.widgets:
            if w == "|":
                bbox.append(ipywidgets.HBox(ws))
                ws = []
            elif w == "w":
                ws += widgets
            elif owidgets[w]:
                ws.append(owidgets[w])
        if len(ws) > 0:
            bbox.append(ipywidgets.HBox(ws))

        bbox = bbox[0] if len(bbox) == 1 else ipywidgets.VBox(bbox)

        if self.cinfo.type == "code_project":
            tab, files = evaluate_core_cpp_project(self.cinfo, cell)
            filenames = self.cinfo.options.split(",")

            hbox = ipywidgets.HBox(ws, layout=bwidget.get_layout())

            if 0:
                tab2, files = evaluate_core_cpp_project(self.cinfo, cell)
                htabs = ipywidgets.HBox([tab, tab2], layout=bwidget.get_layout())
                ws = ipywidgets.VBox(children=[htabs, hbox])
            else:
                ws = ipywidgets.VBox(children=[tab, hbox])
            IPython.display.display(ws, output)
            return

        if self.cinfo.type == "code" and cell != "":
            with output:
                if self.cinfo.user == "solution":
                    colors.set_style(output, "sol_background")
                self.shell.run_cell(cell)
        elif self.cinfo.type == "markdown":
            IPython.display.display(IPython.display.Markdown(cell))
        elif self.cinfo.type == "formula":
            IPython.display.display(IPython.display.Markdown("$" + cell + "$"))
            print("$" + cell + "$")

        IPython.display.display(bbox, output)
