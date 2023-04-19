import sys
from .buttons import *
from .base import WidgetBase


class WidgetCode(WidgetBase):
    widget_id = "code"

    def init_widget(self):
        return None

    def get_answer(self):
        return self.cell

    def display_correction(self, data, output=None):
        codebody = "google.colab" in sys.modules and self.user != "solution"
        md(header=f"Correction ({self.cinfo.id})", **{"codebody" if codebody else "rawbody": data["answer"]})
        md(
            f"""**Execution du code ({self.cinfo.id})** 💻"""
            if self.in_french
            else f"""**Let's execute the code ({self.cinfo.id})** 💻"""
        )
        if self.cinfo.type == "code" and data is not None and "answer" in data:
            self.shell.run_cell(data["answer"])


class WidgetMarkdown(WidgetCode):
    widget_id = "markdown"

    def display_correction(self, data, output=None):
        md(header=f"Correction ({self.cinfo.id})", mdbody=data["answer"])


class WidgetFormula(WidgetCode):
    widget_id = "formula"

    def display_correction(self, data, output=None):
        md(header=f"Correction ({self.cinfo.id})")
        IPython.display.display(IPython.display.Markdown("$" + data["answer"] + "$"))
