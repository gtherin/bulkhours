import os
import ipywidgets
from .tools import md


class WidgetBase:
    widget_id = "base"
    default_wopts = "lwsc"

    def __init__(self, cinfo, cell, in_french, shell):
        self.cinfo = cinfo
        self.cell = cell
        self.in_french = in_french
        self.shell = shell
        self.widget = self.init_widget()

    def init_widget(self):
        return None

    def get_layout(self):
        return ipywidgets.Layout(overflow="scroll hidden", width="auto", flex_flow="row", display="flex")

    def get_params(self):
        return dict(answer=self.get_answer(), atype=self.cinfo.type)

    def get_label_widget(self):
        label = f"<b><font face='FiraCode Nerd Font' size=4 color='black'>{self.cinfo.label}<font></b>"
        return ipywidgets.HTML(value=label, layout=ipywidgets.Layout(height="auto", width="auto"))

    def get_answer(self):
        return self.widget.value

    def display_ecorrection(self, output):
        from .. import firebase

        data = firebase.get_solution_from_corrector(self.cinfo.id, corrector="solution")
        if data is None:
            with output:
                md(
                    mdbody=f"*La solution n'est pas disponible (pour le moment 😕)*"
                    if self.in_french
                    else f"*Solution is not available (yet 😕)*"
                )
                return

        self.display_correction(data, output=output)

        if "hidecode" in data:
            if self.get_answer() is not None:
                hide_code = data["hidecode"].replace("ANSWER", str(self.get_answer()))
            elif "answer" in data:
                hide_code = data["hidecode"].replace("ANSWER", str(data["answer"]))
            self.shell.run_cell(hide_code)

    def submit(self, output):
        from .. import firebase

        answer = self.get_answer()
        if answer == "":
            with output:
                output.clear_output()
                md(mdbody=f"Nothing to send 🙈🙉🙊")
            return

        return firebase.send_answer_to_corrector(self.cinfo, **self.get_params())

    def send_message(self, output):
        from .. import firebase
        from .colors import md

        data = firebase.get_solution_from_corrector(self.cell_id, corrector="solution")
        if (user := os.environ["STUDENT"]) in data or (user := "all") in data:
            md(
                header=f"Message ({self.cinfo.id}, {user}) du correcteur"
                if self.in_french
                else f"Message ({self.cinfo.id}, {user}) from corrector",
                rawbody=data[user],
            )

    def execute_raw_cell(self, bbox, output):
        import IPython

        bbox = bbox[0] if len(bbox) == 1 else ipywidgets.VBox(bbox)
        IPython.display.display(bbox, output)

    def display_correction(self, data, output=None):
        md(header=f"Correction ({self.cinfo.id})", mdbody=data["answer"])
