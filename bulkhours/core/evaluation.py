import os
import subprocess
import time
import multiprocessing

from IPython.core.magic import Magics, cell_magic, magics_class, line_cell_magic, needs_local_scope
import IPython
import ipywidgets

from .widgets.buttons import get_all_buttons, get_buttons_list
from .logins import *
from . import firebase
from . import install
from .widgets.bulk_widget import BulkWidget
from .widgets.code_project import evaluate_core_cpp_project, WidgetCodeProject
from . import colors


@magics_class
class Evaluation(Magics):
    def __init__(self, shell, nid, in_french):
        super(Evaluation, self).__init__(shell)
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
        abuttons = get_buttons_list(bwidget.get_label_widget(), self.in_french)

        def update_button(b, idx, funct, args, kwargs):
            with output:
                output.clear_output()

                colors.set_style(output, "sol_background")
                abuttons[idx].is_on = not abuttons[idx].is_on

                abuttons[idx].update_style(b, style="warning")
                if not abuttons[idx].is_on:
                    try:
                        p1 = multiprocessing.Process(target=funct, args=args, kwargs=kwargs)
                        p1.start()
                        fun, sleep = ["🙈", "🙉", "🙊"], 0.3
                        fun, sleep = ["🌑", "🌒", "🌓‍", "🌖", "🌗", "🌘"], 0.3
                        fun, sleep = ["🤛‍", "✋", "✌"], 0.3
                        fun, sleep = ["🏊", "🚴", "🏃"], 0.3
                        fun, sleep = ["🙂‍", "😐", "😪", "😴", "😅"], 0.3
                        fun, sleep = ["🟥", "🟧", "🟨‍", "🟩", "🟦", "🟪"], 0.3

                        ii, description = 0, b.description
                        while p1.is_alive():
                            b.description = fun[ii % len(fun)] + description
                            time.sleep(sleep)
                            ii += 1

                        abuttons[idx].is_on = abuttons[idx].wait(abuttons[idx].is_on, b)

                    except:
                        abuttons[idx].update_style(b, style="danger")
                        time.sleep(2)
                        abuttons[idx].is_on = True

                abuttons[idx].update_style(b, style="on" if abuttons[idx].is_on else "off")

        widgets = bwidget.get_widgets()

        def submit(b):
            return update_button(b, "s", BulkWidget.submit, [self, bwidget, widgets, output], dict())

        abuttons["s"].b.on_click(submit)

        def get_correction(b):
            return update_button(b, "c", BulkWidget.get_core_correction, [self, bwidget, widgets], dict())

        abuttons["c"].b.on_click(get_correction)

        def send_message(b):
            return update_button(b, "m", BulkWidget.send_message, [self], dict())

        abuttons["m"].b.on_click(send_message)

        def write_exec_process(b):
            return update_button(b, "o", WidgetCodeProject.write_exec_process, [self, files, filenames], dict())

        abuttons["o"].b.on_click(write_exec_process)

        bbox = []
        ws = []
        for w in self.cinfo.widgets:
            if w == "|":
                bbox.append(ipywidgets.HBox(ws))
                ws = []
            elif w == "w":
                ws += widgets
            elif abuttons[w]:
                ws.append(abuttons[w].b)
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
