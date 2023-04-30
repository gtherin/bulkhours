import IPython
import sys

from .tools import md
from .base import WidgetBase


class WidgetCode(WidgetBase):
    widget_id = "code"

    def init_widget(self):
        return None

    def get_answer(self):
        return self.cell

    def display_correction(self, data, output=None):
        codebody = "google.colab" in sys.modules and self.cinfo.user != "solution"
        md(header=f"Correction ({self.cinfo.id})", **{"codebody" if codebody else "rawbody": data["answer"]})
        md(
            f"""**Execution du code ({self.cinfo.id})** 💻"""
            if self.in_french
            else f"""**Let's execute the code ({self.cinfo.id})** 💻"""
        )
        if self.cinfo.type == "code" and data is not None and "answer" in data:
            self.shell.run_cell(data["answer"])

    def execute_raw_cell(self, bbox, output):
        from . import colors

        if self.cell != "":
            with output:
                if self.cinfo.user == "solution":
                    colors.set_style(output, "sol_background")
                self.shell.run_cell(self.cell)
        WidgetBase.execute_raw_cell(self, bbox, output)


class WidgetMarkdown(WidgetCode):
    widget_id = "markdown"

    def display_correction(self, data, output=None):
        md(header=f"Correction ({self.cinfo.id})", mdbody=data["answer"])

    def execute_raw_cell(self, bbox, output):
        IPython.display.display(IPython.display.Markdown(self.cell))
        WidgetBase.execute_raw_cell(self, bbox, output)


class WidgetFormula(WidgetCode):
    widget_id = "formula"

    def display_correction(self, data, output=None):
        with output:
            md(header=f"Correction ({self.cinfo.id})")
        IPython.display.display(IPython.display.Markdown("$" + data["answer"] + "$"))

    def execute_raw_cell(self, bbox, output):
        with output:
            IPython.display.display(IPython.display.Markdown("$" + self.cell + "$"))
            print("$" + self.cell[:-1] + "$")
        WidgetBase.execute_raw_cell(self, bbox, output)
