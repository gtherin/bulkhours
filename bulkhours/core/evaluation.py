import os
import subprocess
import time
import multiprocessing
import numpy as np

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

                            time.sleep(sleep * np.abs((np.random.normal() + 1)))
                            ii += 1

                        abuttons[idx].is_on = abuttons[idx].wait(abuttons[idx].is_on, b)

                    except Exception as e:
                        abuttons[idx].update_style(b, style="danger")
                        IPython.display.display(e)
                        time.sleep(2)
                        abuttons[idx].is_on = True

                abuttons[idx].update_style(b, style="on" if abuttons[idx].is_on else "off")

        widgets = bwidget.get_widgets()

        if self.cinfo.type == "code_project":

            def submit(b):
                return update_button(b, "s", WidgetCodeProject.submit, [self, bwidget, widgets, output], dict())

            def get_correction(b):
                return update_button(b, "c", WidgetCodeProject.get_core_correction, [self, bwidget, widgets], dict())

        else:

            def submit(b):
                return update_button(b, "s", BulkWidget.submit, [self, bwidget, widgets, output], dict())

            def get_correction(b):
                return update_button(b, "c", BulkWidget.get_core_correction, [self, bwidget, widgets], dict())

        abuttons["s"].b.on_click(submit)

        abuttons["c"].b.on_click(get_correction)

        def send_message(b):
            return update_button(b, "m", BulkWidget.send_message, [self], dict())

        abuttons["m"].b.on_click(send_message)

        def write_exec_process(b):
            files = bwidget.widget.files
            filenames = self.cinfo.options.split(",")
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
            elif w == "l" and abuttons[w] is not None:
                ws.append(abuttons[w])
            elif abuttons[w]:
                ws.append(abuttons[w].b)
        if len(ws) > 0:
            bbox.append(ipywidgets.HBox(ws))

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
        elif self.cinfo.type == "code_project":
            if 0:
                tab2, _ = evaluate_core_cpp_project(self.cinfo, cell, show_solution=True)
                htabs = ipywidgets.HBox([tab2])  # , layout=bwidget.get_layout())
                IPython.display.display(htabs)
                IPython.display.display(bbox[1], output)
                # ws = ipywidgets.VBox(children=[htabs, hbox])
            else:
                bwidget.widget.basic_execution(bbox[1], bwidget, output)
            return

        bbox = bbox[0] if len(bbox) == 1 else ipywidgets.VBox(bbox)
        IPython.display.display(bbox, output)
