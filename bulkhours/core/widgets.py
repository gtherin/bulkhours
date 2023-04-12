import os

from IPython.core.magic import Magics, cell_magic, magics_class, line_cell_magic, needs_local_scope
import IPython
import ipywidgets

from .textstyles import *
from .logins import *
from . import firebase
from . import install
from .widget_table import WidgetTable


class BulkWidget:
    def __init__(self, cinfo, cell, in_french) -> None:
        self.cinfo = cinfo
        self.cell = cell
        if cinfo.type in ["table"]:
            self.widget = WidgetTable(cinfo, cell, in_french)
        else:
            self.widget = None

    def get_label(self):
        if self.cinfo.type in ["code", "markdown"]:
            return None
        label = (
            f"<b><font face='FiraCode Nerd Font' size=4 color='red'>{self.cinfo.label}<font></b>"
            if self.cinfo.type == "floatslider"
            else f"<font face='FiraCode Nerd Font' size=4 color='black'>{self.cinfo.label}<font>"
        )
        return ipywidgets.HTML(value=label, layout=ipywidgets.Layout(height="auto", width="auto"))

    def get_widgets(self):
        cell_checks = self.cinfo.options.split(";")
        if self.widget:
            widgets = [self.widget.get_widget()]
        elif self.cinfo.type == "checkboxes":
            widgets = [ipywidgets.Checkbox(value=False, description=i, indent=False) for i in cell_checks]
        elif self.cinfo.type in ["intslider"]:
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
        elif self.cinfo.type in ["floatslider"]:
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

        elif self.cinfo.type == "textarea":
            widgets = [ipywidgets.Textarea(placeholder="Je ne sais pas", disabled=False)]
            # widgets = [ipywidgets.Textarea(placeholder="I don't know", disabled=False)]
        elif self.cinfo.type == "radios":
            widgets = [ipywidgets.RadioButtons(options=cell_checks, layout={"width": "max-content"})]
        elif self.cinfo.type in ["codetext"]:
            widgets = [ipywidgets.Text(value=self.cinfo.default)]
        else:
            widgets = []

        return widgets

    def get_layout(self):
        if self.widget:
            return self.widget.get_layout()

        return (
            ipywidgets.Layout(overflow="scroll hidden", width="auto", flex_flow="row", display="flex")
            if self.cinfo.type == "checkboxes"
            else ipywidgets.Layout()
        )

    def get_answer(self, widgets, cinfo_type):
        if self.widget:
            return self.widget.get_answer()
        elif cinfo_type in ["codetext"]:
            return eval(widgets[0].value)
        elif cinfo_type in ["formula"]:
            return self.cell
        elif cinfo_type in ["code", "markdown"]:
            return self.cell
        elif cinfo_type in ["checkboxes", "radios"]:
            cell_checks = self.cinfo.options.split(";")
            return ";".join([cell_checks[k] for k, i in enumerate(widgets) if i.value])
        else:
            return widgets[0].value

    def get_submit_params(self, widgets, answer):
        if self.widget:
            return self.widget.get_params(answer)
        pams = dict(answer=answer, atype=self.cinfo.type)
        if self.cinfo.type in ["codetext"]:
            pams.update(dict(code=widgets[0].value, comment=f"'{widgets[0].value}'"))
        if self.cinfo.type in ["textarea", "intslider", "floatslider"]:
            pams.update(dict(comment=f"'{widgets[0].value}'"))
        return pams

    @staticmethod
    def submit(self, bwidget, widgets, output):
        answer = bwidget.get_answer(widgets, self.cinfo.type)
        if answer == "":
            with output:
                output.clear_output()
                md(mdbody=f"Nothing to send 🙈🙉🙊")
            return

        return firebase.send_answer_to_corrector(self.cinfo, **bwidget.get_submit_params(widgets, answer))

    @staticmethod
    def get_core_correction(self, bwidget, widgets):
        data = firebase.get_solution_from_corrector(self.cinfo.id, corrector="solution")
        print(data)
        print(bwidget)
        return BulkWidget.show_cell(self, self.cinfo, data, answer=bwidget.get_answer(widgets, self.cinfo.type))

    @staticmethod
    def send_message(self):
        data = firebase.get_solution_from_corrector(self.cell_id, corrector="solution")
        return BulkWidget.show_cell(self, self.cinfo, data, private_msg=True)

    @staticmethod
    def show_cell(self, cinfo, data, private_msg=False, answer=None):
        cell_id = cinfo.id
        in_french = self.in_french
        cell_type = cinfo.type
        if data is None and private_msg:
            pass
        elif data is None:
            md(
                mdbody=f"*La solution n'est pas disponible (pour le moment 😕)*"
                if in_french
                else f"*Solution is not available (yet 😕)*"
            )
        elif private_msg:
            if (user := os.environ["STUDENT"]) in data or (user := "all") in data:
                md(
                    header=f"Message ({cell_id}, {user}) du correcteur"
                    if in_french
                    else f"Message ({cell_id}, {user}) from corrector",
                    rawbody=data[user],
                )
        elif cell_type == "code":
            md(header=f"Correction ({cell_id})", rawbody=data["answer"])
            md(
                f"""**Execution du code ({cell_id})** 💻"""
                if in_french
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
