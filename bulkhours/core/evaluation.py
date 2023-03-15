import argparse
import datetime
import os

from IPython.core.magic import Magics, cell_magic, magics_class, line_cell_magic, needs_local_scope
import IPython
import ipywidgets

from .textstyles import *
from .logins import *
from . import firebase


@magics_class
class Evaluation(Magics):
    def __init__(self, shell):
        super(Evaluation, self).__init__(shell)

        self.argparser = argparse.ArgumentParser(description="Evaluation params")
        self.argparser.add_argument("-i", "--id", default=None)
        self.argparser.add_argument("-u", "--user", default=os.environ["STUDENT"])
        self.argparser.add_argument("-o", "--options", default=None)
        self.show_answer = False

    def show_cell(self, cell_id, cell_type, corrector="solution", private_msg=False, answer=None):
        data = firebase.get_solution_from_corrector(cell_id, corrector=corrector)

        if data is None and private_msg:
            pass
        elif data is None:
            md(mdbody=f"*Solution is not available (yet 😕)*")
        elif private_msg:
            if (user := os.environ["STUDENT"]) in data or (user := "all") in data:
                md(header=f"Message ({cell_id}, {user}) from corrector", rawbody=data[user])
        elif cell_type == "code":
            md(header=f"Correction ({cell_id})", rawbody=data["answer"])
            md(
                f"""---
**Let's execute the code (for {cell_id})** 💻
    ---"""
            )
            self.shell.run_cell(data["answer"])
        elif cell_type in ["markdown", "textarea"]:
            md(header=f"Correction ({cell_id})", mdbody=data["answer"])
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
        cell_info = line.split()
        cell_id, cell_user = cell_info[0], cell_info[1] if len(cell_info) > 1 else "all"
        firebase.send_answer_to_corrector(cell_id, **{cell_user: cell})

    @line_cell_magic
    @needs_local_scope
    def update_cell_id(self, line, cell="", local_ns=None):
        try:
            args = self.argparser.parse_args(line.split())
        except SystemExit as e:
            self.argparser.print_help()
            return

        opts = {
            a.split(":")[0]: cell if a.split(":")[1] == "CELL" else a.split(":")[1] for a in args.options.split(";")
        }
        firebase.send_answer_to_corrector(args.id, user=args.user, **opts)

    @line_cell_magic
    @needs_local_scope
    def evaluation_cell_id(self, line, cell="", local_ns=None):
        cell_info = line.split()
        cell_id, cell_type = cell_info[0], cell_info[1] if len(cell_info) > 1 else "code"

        buttons = [s.b for s in sbuttons]

        output = ipywidgets.Output()

        if cell_type == "code":
            self.shell.run_cell(cell)
        elif cell_type == "markdown":
            IPython.display.display(IPython.display.Markdown(cell))

        def func(b, i, func, args, kwargs):
            with output:
                output.clear_output()
                self.show_answer = not self.show_answer
                sbuttons[i].update_style(b, on=self.show_answer)
                if self.show_answer:
                    func(*args, **kwargs)

        cell_label = " ".join(cell_info[2:-1]) if ";" in cell_info[-1] else " ".join(cell_info[2:])
        cell_checks = cell_info[-1].split(";")

        if cell_type in ["code", "markdown"]:
            label = []
        else:
            label = (
                f"<b><font face='FiraCode Nerd Font' size=4 color='red'>{cell_label}<font></b>"
                if cell_type == "floatslider"
                else f"<font face='FiraCode Nerd Font' size=4 color='black'>{cell_label}<font>"
            )
            label = [ipywidgets.HTML(value=label, layout=ipywidgets.Layout(height="auto", width="auto"))]

        if cell_type == "checkboxes":
            widgets = [ipywidgets.Checkbox(value=False, description=i, indent=False) for i in cell_checks]
        elif cell_type in ["intslider"]:
            widgets = [
                ipywidgets.IntSlider(
                    min=int(cell_checks[0]),
                    max=int(cell_checks[1]),
                    step=1,
                    continuous_update=True,
                    orientation="horizontal",
                    readout=True,
                    readout_format="d",
                )
            ]
        elif cell_type in ["floatslider"]:
            widgets = [
                ipywidgets.FloatSlider(
                    min=float(cell_checks[0]),
                    max=float(cell_checks[1]),
                    value=float(cell_checks[2]),
                    step=0.5,
                    continuous_update=True,
                    orientation="horizontal",
                    readout=True,
                    readout_format=".1f",
                )
            ]

        elif cell_type == "textarea":
            widgets = [ipywidgets.Textarea(placeholder="I don't know", disabled=False)]
        elif cell_type == "radios":
            widgets = [ipywidgets.RadioButtons(options=cell_checks, layout={"width": "max-content"})]
        elif cell_type == "codetext":
            widgets = [ipywidgets.Text()]
        else:
            widgets = []

        def get_answer(widgets, cell_type):
            if cell_type in ["codetext"]:
                return eval(widgets[0].value)
            elif cell_type in ["code", "markdown"]:
                return cell
            elif cell_type in ["checkboxes", "radios"]:
                return ";".join([cell_checks[k] for k, i in enumerate(widgets) if i.value])
            else:
                return widgets[0].value

        def submit(b):
            answer = get_answer(widgets, cell_type)
            if answer == "":
                with output:
                    output.clear_output()
                    md(mdbody=f"Nothing to send 🙈🙉🙊")
                return

            pams = dict(answer=answer, atype=cell_type)

            if cell_type in ["codetext"]:
                pams.update(dict(code=widgets[0].value, comment=f"'{widgets[0].value}'"))
            if cell_type in ["textarea", "intslider", "floatslider"]:
                pams.update(dict(comment=f"'{widgets[0].value}'"))
            return func(b, 0, firebase.send_answer_to_corrector, [cell_id], pams)

        buttons[0].on_click(submit)

        def fun1(b):
            return func(b, 1, self.show_cell, [cell_id, cell_type], dict(answer=get_answer(widgets, cell_type)))

        buttons[1].on_click(fun1)

        def fun2(b):
            return func(b, 2, self.show_cell, [cell_id, cell_type], dict(private_msg=True))

        buttons[2].on_click(fun2)

        layout = (
            ipywidgets.Layout(overflow="scroll hidden", width="auto", flex_flow="row", display="flex")
            if cell_type == "checkboxes"
            else ipywidgets.Layout()
        )

        if cell_type == "floatslider":
            IPython.display.display(ipywidgets.HBox(label + widgets + buttons[3:], layout=layout), output)
        else:
            IPython.display.display(ipywidgets.HBox(label + widgets + buttons[:2], layout=layout), output)
