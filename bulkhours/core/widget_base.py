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


def bot_evaluation(student_data, teacher_data):
    from . import gpt

    if gpt.evaluation_instructions is not None:
        print("")
        grade, _ = gpt.get_grade(student_data, teacher_data)
        return grade

    print("🚧Need to implement evaluation_instructions")
    return np.nan


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
        teacher_data = CellParser.crunch_data(cinfo=self.cinfo, user=tools.REF_USER)
        student_data = CellParser.crunch_data(cinfo=self.cinfo, user=self.cinfo.user, data=self.cell_source)

        if teacher_data.is_evaluation_available():
            score = equals.evaluate_student(student_data, teacher_data, raw=False, user=self.cinfo.user)
        else:
            score = ""

        if teacher_data.is_hint_available():
            equals.hint_student(student_data, teacher_data, raw=False, tmode="hint")

        if teacher_data.is_explanation_available():
            print("")
            equals.execute_teacher_code(student_data, teacher_data, raw=False, tmode="explanation")
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

        self.display_correction(student_data, teacher_data, output=output, score=score)


    def autocorrect(self, output):

        if 0:
            teacher_is_local, sort_by, verbose, duser = True, None, True, "Guillaume.T"
        else:
            teacher_is_local, sort_by, verbose, duser = True, None, False, None

        if teacher_is_local:
            teacher_data = CellParser.crunch_data(cinfo=self.cinfo, user=self.cinfo.user, data=self.cell_source) # Get data from cell
        else:
            teacher_data = CellParser.crunch_data(cinfo=self.cinfo, user=tools.REF_USER, data=None) # Get data from database

        bot_correction = teacher_data.get_code("evaluation") == "" or "automatic_eval" in teacher_data.get_code("evaluation")

        from .. import admin

        grades = admin.tools.get_users_list(no_admin=False, sort_by=sort_by)

        grades[self.cinfo.cell_id + ".n"] = np.nan
        grades = grades[["auser", "mail", self.cinfo.cell_id + ".n"]]

        print(f"\x1b[35m\x1b[1mNotes for {self.cinfo.cell_id}: \x1b[m", end="")

        if bot_correction:
            max_score = 10
        else:
            max_score = equals.get_max_score(teacher_data)

        answers = admin.answers.get_answers(self.cinfo.cell_id, verbose=False)
        for u in grades.index:

            mail, auser = grades["mail"][u], grades["auser"][u]
            if type(mail) == pd.Series:
                mail, auser = mail.iloc[0], auser.iloc[0]

            if duser is not None and auser != duser:
                continue

            if not bot_correction:
                print(f"\x1b[35m\x1b[1m{auser}, \x1b[m", end="")

            if mail not in answers:
                print(f"\x1b[35m\x1b[1m(nan), \x1b[m", end="")
                continue

            # Get student data
            student_data = CellParser.crunch_data(cinfo=self.cinfo, data=answers[mail], user=mail)

            # Don't manual data is available 
            if student_data.is_manual_note():
                print(f"\x1b[35m\x1b[1m({student_data.minfo['grade_man']} [MAN]), \x1b[m", end="")
                continue

            if bot_correction:
                score = bot_evaluation(student_data, teacher_data)
            else:
                score = equals.evaluate_student(student_data, teacher_data, raw=True, user=auser, verbose=verbose)
                print(f"\x1b[35m\x1b[1m({score}), \x1b[m", end="")

            grades.loc[u, self.cinfo.cell_id + ".n"] = score
     
        grad_name = "grade_bot" if bot_correction else "grade_ana"

        admin.answers.update_grades(self.cinfo.cell_id, grades, grad_name)
        grades = grades.drop(columns=["mail"]).set_index("auser").T

        Grade.set_static_style_info(minvalue=0.0, cmap=(cmap:="RdBu"))
        fstyles = lambda v: Grade.apply_style(v, False)
        grades = grades.style.format(precision=1).applymap(fstyles).background_gradient(cmap=cmap, vmin=0, vmax=max_score)
        IPython.display.display(grades)

    def submit(self, output, user=None):
        from . import firebase

        answer = self.get_answer()
        if answer == "":
            with output:
                output.clear_output()
                tools.html(f"Nothing to send 🙈🙉🙊", display=True, style="body")
            return
        local_data = CellParser.crunch_data(cinfo=self.cinfo, user=user, data=self.cell_source)
        return firebase.send_answer_to_corrector(local_data.cinfo, **local_data.get_dbcell_decomposition())

    def osubmit(self, output):
        return self.submit(output, user=tools.REF_USER)

    def send_message(self, output):
        from . import firebase

        data = firebase.get_solution_from_corrector(self.cinfo.cell_id, corrector=tools.REF_USER)
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

    def display_correction(self, student_data, teacher_data, output=None, score=""):
        codebody = "google.colab" in sys.modules and self.cinfo.user != tools.REF_USER
        kwargs = (
            {"codebody" if codebody else "rawbody": teacher_data.get_code("main_execution")}
            if "main_execution" in teacher_data.minfo
            else {}
        )
        color = "black"
        kwargs = {}

        if 0:
            if score == "":
                note_auto = score
            else:
                score, max_score = score.split("/")
                if float(score) > 0.6 * float(max_score):
                    note_auto, color = f", note={score}🥳", "green"
                else:
                    note_auto, color = f", note={score}😔", "red"
        note_auto = ""

        comment = (
            "" if self.cinfo.type in ["bkcode", "bkscript"] else f": {teacher_data['answer']} VS {self.get_answer()}"
        )
        sources = ""  # f", {student_data.minfo['source']} VS {teacher_data.minfo['source']}"

        with output:
            output.clear_output()
            tools.html(
                f"Correction ({self.cinfo.cell_id}{note_auto}) {comment}", style="title", display=True, color=color
            )
            tools.code(teacher_data.get_code("main_execution"), display=True)

            if (
                self.cinfo.type in ["bkcode", "bkscript"]
                and teacher_data is not None
                and "main_execution" in teacher_data.minfo
            ):
                tools.html(
                    f"""Execution du code ({self.cinfo.cell_id}{note_auto}{sources}) 💻"""
                    if self.cinfo.language == "fr"
                    else f"""Let's execute the code ({self.cinfo.cell_id}{note_auto}{sources}) 💻""",
                    style="title",
                    display=True,
                    color=color,
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

        if "student_evaluation_function" in self.cell_source:
            abuttons["a"].b.description = "🧮Correct students"
        else:
            abuttons["a"].b.description = "🤖Correct students"

        def func_a(b):
            return buttons.update_button(b, abuttons["a"], output, self, "autocorrect")

        def func_g(b):
            return buttons.update_button(b, abuttons["g"], output, self, "ask_chat_gpt")

        for w in self.cinfo.widgets:
            if w not in "l|w":
                exec("""self.abuttons["{w}"].b.on_click(func_{w})""".format(w=w))

        self.execute_raw_cell(bbox, output)
