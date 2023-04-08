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
from .widget_code_project import evaluate_core_cpp_project
from .widget_table import get_table_widgets


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
        cell_id, cell_user = self.cell_id, self.cinfo.user
        firebase.send_answer_to_corrector(cell_id, **{cell_user: cell})

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
        firebase.send_answer_to_corrector(self.cell_id, user=self.cinfo.user, **opts)

    @line_cell_magic
    @needs_local_scope
    def evaluation_cell_id(self, line, cell="", local_ns=None):
        self.cinfo = install.get_argparser(line, cell)
        if not self.cinfo:
            return

        style = """
            <style>
                .sol_background {background-color:#f7d1d1}
                .cell_background {background-color:#F7F7F7}
                .cell_border {background-color:#CFCFCF}
            </style>
        """
        IPython.display.display(ipywidgets.HTML(style))

        output = ipywidgets.Output()
        if self.cinfo.user == "solution":
            output.add_class("sol_background")

        bwidget = BulkWidget(self.cinfo, cell)

        owidgets = {
            "l": bwidget.get_label(),
            "s": sbuttons[0].g(self.in_french),
            "c": sbuttons[1].g(self.in_french),
            "m": sbuttons[2].g(self.in_french),
            "t": sbuttons[3].g(self.in_french),
            "o": sbuttons[4].g(self.in_french),
        }
        widgets = bwidget.get_widgets()

        def func(b, i, func, args, kwargs):
            with output:
                output.clear_output()
                IPython.display.display(ipywidgets.HTML(style))
                output.add_class("sol_background")
                self.show_answer = not self.show_answer
                sbuttons[i].update_style(b, on=self.show_answer)
                if not self.show_answer:
                    func(*args, **kwargs)

        def submit(b):
            answer = bwidget.get_answer(widgets, self.cinfo.type)
            if answer == "":
                with output:
                    output.clear_output()
                    md(mdbody=f"Nothing to send 🙈🙉🙊")
                return

            return func(
                b, 0, firebase.send_answer_to_corrector, [self.cell_id], bwidget.get_submit_params(widgets, answer)
            )

        owidgets["s"].on_click(submit)

        def get_correction(b):
            data = firebase.get_solution_from_corrector(self.cell_id, corrector="solution")

            return func(
                b,
                1,
                BulkWidget.show_cell,
                [self, self.cell_id, self.cinfo.type, data],
                dict(answer=bwidget.get_answer(widgets, self.cinfo.type)),
            )

        owidgets["c"].on_click(get_correction)

        def send_message(b):
            data = firebase.get_solution_from_corrector(self.cell_id, corrector="solution")
            return func(
                b, 2, BulkWidget.show_cell, [self, self.cell_id, self.cinfo.type, data], dict(private_msg=True)
            )

        owidgets["m"].on_click(send_message)

        def write_exec_process(b):
            for t, fn in enumerate(filenames):
                with open(f"cache/{self.cinfo.id}_{fn}", "w") as f:
                    f.write(files[t].value)
                print(f"Generate cache/{fn}")
                with open(f"cache/{fn}", "w") as f:
                    f.write(files[t].value)

            os.system(f"cd cache && make all && ./main")

        owidgets["o"].on_click(write_exec_process)

        ws = []
        for w in self.cinfo.widgets:
            if w == "w":
                ws += widgets
            elif owidgets[w]:
                ws.append(owidgets[w])

        if self.cinfo.type == "code_project":
            tab, files = evaluate_core_cpp_project(self.cinfo, cell)
            filenames = self.cinfo.options.split(",")

            hbox = ipywidgets.HBox([owidgets["o"]] + ws, layout=bwidget.get_layout())

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
                IPython.display.display(ipywidgets.HTML(style))
                if self.cinfo.user == "solution":
                    output.add_class("sol_background")
                self.shell.run_cell(cell)
        elif self.cinfo.type == "markdown":
            IPython.display.display(IPython.display.Markdown(cell))
        elif self.cinfo.type == "formula":
            IPython.display.display(IPython.display.Markdown("$" + cell + "$"))
            print("$" + cell + "$")
        elif self.cinfo.type == "table":
            IPython.display.display(get_table_widgets(self.cinfo))

        IPython.display.display(ipywidgets.HBox(ws, layout=bwidget.get_layout()), output)
