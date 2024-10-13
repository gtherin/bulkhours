import IPython
import ipywidgets
import numpy as np
import pandas as pd
import sys

from .grade import Grade
from . import tools
from .cell_parser import CellParser
from .line_parser import LineParser
from . import buttons
from . import equals
from . import contexts


class WidgetBase:
    widget_id = "base"
    widget_comp = "lwsc"

    def __init__(self, line, cell_source):
        self.cinfo = LineParser(line, cell_source)
        self.user = self.cinfo.user
        self.widget, self.cell_source = None, cell_source
        self.widget = self.init_widget()

    def init_widget(self):
        return None

    def get_layout(self):
        return ipywidgets.Layout(
            overflow="scroll hidden", width="auto", flex_flow="row", display="flex"
        )

    def get_answer(self):
        if self.widget is not None:
            return self.widget.value
        return "Nope"

    def display_ecorrection(self, output):
        teacher_data = CellParser.crunch_data(cinfo=self.cinfo, user=tools.REF_USER)
        student_data = CellParser.crunch_data(
            cinfo=self.cinfo, user=self.cinfo.user, data=self.cell_source
        )

        if teacher_data.is_hint_available():
            equals.hint_student(student_data, teacher_data, raw=False, tmode="hint")

        if teacher_data.is_explanation_available():
            print("")
            equals.execute_teacher_code(
                student_data, teacher_data, raw=False, tmode="explanation"
            )
            if not teacher_data.is_evaluation_visible():
                return

        if not teacher_data.is_evaluation_visible():
            with output:
                tools.html(
                    f"La solution n'est pas disponible (pour le moment 😕)"
                    if self.cinfo.language == "fr"
                    else f"Solution is not available (yet 😕)",
                    display=True,
                    style="body",
                )
                return

        self.display_correction(student_data, teacher_data, output=output)

    def autocorrect(self, output):
        if 0:
            teacher_is_local, sort_by, verbose, duser = True, None, True, "Guillaume.T"
        else:
            teacher_is_local, sort_by, verbose, duser = True, None, False, None

        if teacher_is_local:
            teacher_data = CellParser.crunch_data(
                cinfo=self.cinfo, user=self.cinfo.user, data=self.cell_source
            )  # Get data from cell

        from .. import admin

        return admin.evaluate(
            self.cinfo.cell_id,
            user="ALL",
            style=None,
            execute=True,
            level=None,
            teacher_data=teacher_data,
            verbose=verbose,
            duser=duser,
        )

    def submit(self, output, user=None):
        from . import firebase

        answer = self.get_answer()
        if answer == "":
            with output:
                output.clear_output()
                tools.html(f"Nothing to send 🙈🙉🙊", display=True, style="body")
            return

        local_data = CellParser.crunch_data(
            cinfo=self.cinfo, user=user, data=self.cell_source, output=output
        )
        return firebase.send_answer_to_corrector(
            local_data.cinfo, **local_data.get_dbcell_decomposition()
        )

    def osubmit(self, output):
        return self.submit(output, user=tools.REF_USER)

    def send_message(self, output):
        from . import firebase

        data = firebase.get_solution_from_corrector(
            self.cinfo.cell_id, corrector=tools.REF_USER
        )
        if (user := self.cinfo.user) in data or (user := "all") in data:
            tools.html(
                f"Message ({self.cinfo.cell_id}, {user}) du correcteur"
                if self.cinfo.language == "fr"
                else f"Message ({self.cinfo.cell_id}, {user}) from corrector",
                display=True,
                style="rheader",
            )
            tools.html(data[user], display=True, style="raw")

    def execute_raw_cell(self, bbox, output):
        bbox = bbox[0] if len(bbox) == 1 else ipywidgets.VBox(bbox)

        configs = vars(self.cinfo)

        contexts.add_variables_in_contexts(self.cinfo.cell_id, configs)

        IPython.display.display(bbox, output)

    def display_correction(self, student_data, teacher_data, output=None):
        comment = (
            ""
            if self.cinfo.type in ["bkcode", "bkscript"]
            else f": {teacher_data['answer']} VS {self.get_answer()}"
        )

        with output:
            output.clear_output()
            tools.html(
                f"Correction ({self.cinfo.cell_id}) {comment}",
                style="title",
                display=True,
            )

            tools.code(scode := teacher_data.get_solution(), display=True)

            if (
                self.cinfo.type in ["bkcode", "bkscript"]
                and teacher_data is not None
                and "main_execution" in teacher_data.minfo
            ):
                tools.html(
                    f"""Execution du code ({self.cinfo.cell_id}) 💻"""
                    if self.cinfo.language == "fr"
                    else f"""Let's execute the code ({self.cinfo.cell_id}) 💻""",
                    style="title",
                    display=True,
                )

                IPython.get_ipython().run_cell(scode)

    def ask_gpt(self, output):
        from .gpt import ask_gpt

        return ask_gpt(prompt=self.gtext.value, is_code=True)

    def evaluate_cell(self):
        bbox = self.init_widgets()

        if self.cinfo.autorun == "publish":
            from . import firebase
            output = ipywidgets.Output()
            local_data = CellParser.crunch_data(
                cinfo=self.cinfo, user=self.user, data=self.cell_source, output=output
            )
            print(self.cinfo)
            #virtual_rooms = [self.cinfo.virtual_room] if virtual_rooms == "" else self.cinfo.virtual_rooms.split(",")

            print(virtual_rooms)
            print(self.cinfo.virtual_rooms)
            virtual_rooms = ["toy", "TISA"]

            for virtual_room in ["toy", "TISA"]:
                #cinfo = local_data.cinfo.virtual_room = virtual_room
                return firebase.send_answer_to_corrector(
                    local_data.cinfo, virtual_room=virtual_room, **local_data.get_dbcell_decomposition()
                )

        self.display_widgets(bbox, self.abuttons)

    def init_widgets(self):
        bbox = []
        ws = []

        self.abuttons = buttons.get_buttons_list(
            self.cinfo.label, language=self.cinfo.language, user=self.cinfo.user
        )
        self.gtext = ipywidgets.Text(self.cinfo.label)

        for w in self.cinfo.widgets:
            if w == "|":
                bbox.append(ipywidgets.HBox(ws))
                ws = []
            elif w == "w":
                ws += [self.widget]
            elif w == "g":
                ws += [self.gtext, self.abuttons[w].b]
            elif self.abuttons[w]:
                ws.append(self.abuttons[w].b)
        if len(ws) > 0:
            bbox.append(ipywidgets.HBox(ws))
        return bbox

    def display_widgets(self, bbox, abuttons):
        output = ipywidgets.Output()

        def func_m(b):
            return buttons.update_button(b, abuttons["m"], output, self, "send_message")

        def func_t(b):
            return buttons.update_button(
                b, abuttons["t"], output, self, "write_exec_process"
            )

        def func_c(b):
            return buttons.update_button(
                b, abuttons["c"], output, self, "display_ecorrection"
            )

        def func_s(b):
            return buttons.update_button(b, abuttons["s"], output, self, "submit")

        def func_o(b):
            return buttons.update_button(b, abuttons["o"], output, self, "osubmit")

        if "student_evaluation_function" in self.cell_source:
            abuttons["a"].b.description = "🧮Correct students"
        else:
            abuttons["a"].b.description = "🤖Correct students"

        def func_a(b):
            return buttons.update_button(b, abuttons["a"], output, self, "autocorrect")

        def func_g(b):
            return buttons.update_button(b, abuttons["g"], output, self, "ask_gpt")

        for w in self.cinfo.widgets:
            if w not in "l|w":
                exec("""self.abuttons["{w}"].b.on_click(func_{w})""".format(w=w))

        self.execute_raw_cell(bbox, output)
