import IPython
import ipywidgets
from .tools import md
import numpy as np
import sys
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
        return ipywidgets.Layout(overflow="scroll hidden", width="auto", flex_flow="row", display="flex")

    def get_answer(self):
        if self.widget is not None:
            return self.widget.value
        return "Nope"

    def display_ecorrection(self, output):
        teacher_data = CellParser.crunch_data(self.cinfo, user="solution")
        student_data = CellParser.crunch_data(self.cinfo, user=self.cinfo.user, data=self.cell_source)

        if teacher_data.is_evaluation_available():
            score = equals.evaluate_student(student_data, teacher_data, raw=False)
        else:
            score = ""

        if not teacher_data.is_evaluation_visible():
            with output:
                md(
                    mdbody=f"La solution n'est pas disponible (pour le moment 😕)"
                    if self.cinfo.language == "fr"
                    else f"Solution is not available (yet 😕)"
                )
                return

        self.display_correction(student_data, teacher_data, output=output, score=score)

        if teacher_data.is_explanation_available():
            equals.explain_student(student_data, teacher_data, raw=False)

    def autocorrect(self, output):
        teacher_data = CellParser.crunch_data(self.cinfo, user="solution")

        if teacher_data.get_code("evaluation") == "":
            print("No correction available")
            return

        from .. import admin

        users = admin.tools.get_users_list(no_admin=False)

        users[self.cinfo.cell_id + ".n"] = np.nan
        users = users.set_index("mail")[["nom", "prenom", self.cinfo.cell_id + ".n"]]

        answers = admin.answers.get_answers(self.cinfo.cell_id, verbose=False)
        for user, answer in answers.items():
            student_data = CellParser.crunch_data(self.cinfo, user=user, data=answer)
            score = equals.evaluate_student(student_data, teacher_data, raw=True)

            users.loc[user, self.cinfo.cell_id + ".n"] = score
            admin.answers.update_note(self.cinfo.cell_id, user, score)

        IPython.display.display(admin.tools.styles(users))

    def submit(self, output, user=None):
        from . import firebase

        answer = self.get_answer()
        if answer == "":
            with output:
                output.clear_output()
                md(mdbody=f"Nothing to send 🙈🙉🙊")
            return
        if user is None:
            user = self.cinfo.user
        local_data = CellParser.crunch_data(self.cinfo, user=user, data=self.cell_source)
        return firebase.send_answer_to_corrector(local_data.minfo["cinfo"], **local_data.get_dbcell_decomposition())

    def osubmit(self, output):
        return self.submit(output, user="solution")

    def send_message(self, output):
        from . import firebase
        from .colors import md

        data = firebase.get_solution_from_corrector(self.cinfo.cell_id, corrector="solution")
        if (user := self.cinfo.user) in data or (user := "all") in data:
            md(
                header=f"Message ({self.cinfo.cell_id}, {user}) du correcteur"
                if self.cinfo.language == "fr"
                else f"Message ({self.cinfo.cell_id}, {user}) from corrector",
                rawbody=data[user],
            )

    def execute_raw_cell(self, bbox, output):
        bbox = bbox[0] if len(bbox) == 1 else ipywidgets.VBox(bbox)

        configs = vars(self.cinfo)

        contexts.add_variables_in_contexts(self.cinfo.cell_id, configs)

        IPython.display.display(bbox, output)

    def display_correction(self, student_data, teacher_data, output=None, score=""):
        codebody = "google.colab" in sys.modules and self.cinfo.user != "solution"
        kwargs = (
            {"codebody" if codebody else "rawbody": teacher_data.get_code("main_execution")}
            if "main_execution" in teacher_data.minfo
            else {}
        )

        if score == "":
            note_auto = score
        else:
            score, max_score = score.split("/")
            if float(score) > 0.6 * float(max_score):
                note_auto, kwargs["bc"] = f", note={score}🥳", "green"
            else:
                note_auto, kwargs["bc"] = f", note={score}😔", "red"

        comment = (
            "" if self.cinfo.type in ["bkcode", "bkscript"] else f": {teacher_data['answer']} VS {self.get_answer()}"
        )
        sources = ""  # f", {student_data.minfo['source']} VS {teacher_data.minfo['source']}"
        md(header=f"Correction ({self.cinfo.cell_id}{note_auto}) {comment}", **kwargs)

        if (
            self.cinfo.type in ["bkcode", "bkscript"]
            and teacher_data is not None
            and "main_execution" in teacher_data.minfo
        ):
            with output:
                md(
                    header=f"""Execution du code ({self.cinfo.cell_id}{note_auto}{sources}) 💻"""
                    if self.cinfo.language == "fr"
                    else f"""Let's execute the code ({self.cinfo.cell_id}{note_auto}{sources}) 💻""",
                    bc="black",
                )

                IPython.get_ipython().run_cell(teacher_data.get_code("main_execution"))

    def ask_chat_gpt(self, output):
        from .gpt import ask_chat_gpt

        return ask_chat_gpt(question=self.gtext.value, is_code=True)

    def evaluate_cell(self):
        bbox = self.init_widgets()

        self.display_widgets(bbox, self.abuttons)

    def init_widgets(self):
        bbox = []
        ws = []

        self.abuttons = buttons.get_buttons_list(self.cinfo.label, language=self.cinfo.language, user=self.cinfo.user)
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
            return buttons.update_button(b, abuttons["t"], output, self, "write_exec_process")

        def func_c(b):
            return buttons.update_button(b, abuttons["c"], output, self, "display_ecorrection")

        def func_s(b):
            return buttons.update_button(b, abuttons["s"], output, self, "submit")

        def func_o(b):
            return buttons.update_button(b, abuttons["o"], output, self, "osubmit")

        def func_a(b):
            return buttons.update_button(b, abuttons["a"], output, self, "autocorrect")

        def func_g(b):
            return buttons.update_button(b, abuttons["g"], output, self, "ask_chat_gpt")

        for w in self.cinfo.widgets:
            if w not in "l|w":
                exec("""self.abuttons["{w}"].b.on_click(func_{w})""".format(w=w))

        self.execute_raw_cell(bbox, output)
