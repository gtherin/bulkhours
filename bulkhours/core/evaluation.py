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
from .widget_code_project import evaluate_cpp_project
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

    def show_cell(self, cell_id, cell_type, corrector="solution", private_msg=False, answer=None):
        data = firebase.get_solution_from_corrector(cell_id, corrector=corrector)

        if data is None and private_msg:
            pass
        elif data is None:
            md(
                mdbody=f"*La solution n'est pas disponible (pour le moment 😕)*"
                if self.in_french
                else f"*Solution is not available (yet 😕)*"
            )
        elif private_msg:
            if (user := os.environ["STUDENT"]) in data or (user := "all") in data:
                md(
                    header=f"Message ({cell_id}, {user}) du correcteur"
                    if self.in_french
                    else f"Message ({cell_id}, {user}) from corrector",
                    rawbody=data[user],
                )
        elif cell_type == "code":
            md(header=f"Correction ({cell_id})", rawbody=data["answer"])
            md(
                f"""**Execution du code ({cell_id})** 💻"""
                if self.in_french
                else f"""**Let's execute the code ({cell_id})** 💻"""
            )
            self.shell.run_cell(data["answer"])
        elif cell_type in ["markdown", "textarea"]:
            md(header=f"Correction ({cell_id})", mdbody=data["answer"])
        elif cell_type in ["formula"]:
            md(header=f"Correction ({cell_id})")
            IPython.display.display(IPython.display.Markdown("$" + data["answer"] + "$"))
        elif cell_type in ["codetext", "intslider", "floatslider"]:
            cc = (
                ""
                if cell_type in ["intslider", "floatslider"] or data["answer"] == data["code"]
                else f" ({data['code']})"
            )
            if data["answer"] == answer:
                md(mdbody=f"🥳Correction: {data['answer']}{cc}", bc="green")
            else:
                md(mdbody=f"😔Correction: {data['answer']}{cc}", bc="red")
        if data is not None and "hidecode" in data:
            if answer is not None:
                hide_code = data["hidecode"].replace("ANSWER", str(answer))
            elif "answer" in data:
                hide_code = data["hidecode"].replace("ANSWER", str(data["answer"]))
            self.shell.run_cell(hide_code)

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

        output = ipywidgets.Output()
        if self.cinfo.type == "code_project":
            return evaluate_cpp_project(self.cinfo, cell)

        if self.cinfo.type == "code" and cell == "":
            return
        elif self.cinfo.type == "code":
            self.shell.run_cell(cell)
        elif self.cinfo.type == "markdown":
            IPython.display.display(IPython.display.Markdown(cell))

        bwidget = BulkWidget(self.cinfo, cell)

        owidgets = {
            "l": bwidget.get_label(),
            "s": sbuttons[0].g(self.in_french),
            "c": sbuttons[1].g(self.in_french),
            "m": sbuttons[2].g(self.in_french),
        }
        widgets = bwidget.get_widgets()

        def func(b, i, func, args, kwargs):
            with output:
                output.clear_output()
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

            pams = dict(answer=answer, atype=self.cinfo.type)

            if self.cinfo.type in ["codetext"]:
                pams.update(dict(code=widgets[0].value, comment=f"'{widgets[0].value}'"))
            if self.cinfo.type in ["textarea", "intslider", "floatslider"]:
                pams.update(dict(comment=f"'{widgets[0].value}'"))
            return func(b, 0, firebase.send_answer_to_corrector, [self.cell_id], pams)

        owidgets["s"].on_click(submit)

        def fun1(b):
            return func(
                b,
                1,
                self.show_cell,
                [self.cell_id, self.cinfo.type],
                dict(answer=bwidget.get_answer(widgets, self.cinfo.type)),
            )

        owidgets["c"].on_click(fun1)

        def fun2(b):
            return func(b, 2, self.show_cell, [self.cell_id, self.cinfo.type], dict(private_msg=True))

        owidgets["m"].on_click(fun2)

        ws = []
        for w in self.cinfo.widgets:
            if w == "w":
                ws += widgets
            elif owidgets[w]:
                ws.append(owidgets[w])

        if self.cinfo.type == "formula":
            IPython.display.display(IPython.display.Markdown("$" + cell + "$"))
            print("$" + cell + "$")
        if self.cinfo.type == "table":
            IPython.display.display(get_table_widgets(self.cinfo))
            IPython.display.display(ipywidgets.HBox(ws, layout=bwidget.get_layout()), output)
        else:
            IPython.display.display(ipywidgets.HBox(ws, layout=bwidget.get_layout()), output)

        # if self.cinfo.puppet != "":
        #    print("PUPPET", self.cinfo.puppet)
        #    puppets.dance_puppets(tag)
