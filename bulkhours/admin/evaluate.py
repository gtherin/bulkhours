import IPython
import ipywidgets

from .. import core
from . import answers
from . import tools


def get_alias_name(cuser):
    if "@" in cuser:
        auser = cuser.split("@")[0].split(".")
        return auser[0].capitalize() + "." + auser[1][0]
    return cuser


def show_answer(out, cuser, answer, style=None):
    color = "green" if cuser == core.tools.REF_USER else "red"
    cuser = get_alias_name(cuser)
    show_raw_code = style == "dark"  # not ("google.colab" in sys.modules and style != "dark")

    with out:
        # Show code
        core.tools.html(f"Code ({cuser})", size="4", color=color, use_ipywidgets=True, display=True)
        core.tools.code(answer, display=True, style=style)  # , raw=show_raw_code

        # Execute code
        core.tools.html(f"Execution ({cuser})💻", size="4", color=color, use_ipywidgets=True, display=True)
        core.tools.eval_code(answer)


def create_evaluation_buttonanswer(cell_id, cuser, cfg, student_data, teacher_data):

    language = cfg.g["language"]
    label = core.tools.html(get_alias_name(cuser), size="6", color="#4F4F4F", use_ipywidgets=True)
    abuttons = core.buttons.get_buttons_list(label="", language=language, user=core.tools.REF_USER)
    output = ipywidgets.Output()

    grade = core.Grade.get(student_data)

    widget = ipywidgets.FloatSlider(
        min=0,
        max=10,
        value=grade,
        step=0.5,
        continuous_update=True,
        orientation="horizontal",
        readout=True,
        readout_format=".1f",
    )
    widget.style.handle_color = "lightblue"

    def sevaluate(data, output):
        with output:
            output.clear_output()
            answers.update_grade(cell_id, cuser, widget.value, name="grade_man")

    if "main_execution" in student_data.minfo and "main_execution" in teacher_data.minfo and core.gpt.evaluation_instructions is not None:
        abuttons["a"].b.description = "🤖Correct student"

    def autocorrect(data, output):

        if "main_execution" in student_data.minfo and "main_execution" in teacher_data.minfo and core.gpt.evaluation_instructions is not None:
            print("")
            grade, response = core.gpt.get_grade(student_data, teacher_data)
            if grade != grade:
                answers.update_grade(cell_id, cuser, grade, grade_name="grade_bot", comment=response)
            return

        print("🚧Need to implement autocorrect here")

    def sevaluate2(b):
        return core.buttons.update_button(b, abuttons["e"], output, None, sevaluate)

    def sautocorrect(b):
        return core.buttons.update_button(b, abuttons["a"], output, None, autocorrect)

    abuttons["e"].b.on_click(sevaluate2)
    abuttons["a"].b.on_click(sautocorrect)

    IPython.display.display(ipywidgets.HBox([label, widget, abuttons["e"].b, abuttons["a"].b]), output)


def evaluate(cell_id, user="NEXT", show_correction=False, style=None, **kwargs):
    cell_answers = answers.get_answers(cell_id, **kwargs)
    cfg = core.tools.get_config(is_new_format=True)

    users = tools.get_users_list(no_admin=False)
    ausers = users.set_index("auser")["mail"].to_dict()

    if core.tools.REF_USER in cell_answers:
        cinfo = core.LineParser.from_cell_id_user(cell_id, core.tools.REF_USER)
        teacher_data = core.CellParser.crunch_data(cinfo=cinfo, data=cell_answers[core.tools.REF_USER], user=core.tools.REF_USER)

    nuser, did_find_answer = user, False
    for cuser, answer in cell_answers.items():

        if (user == "NEXT" and core.Grade.DEFAULT_GRADE == core.Grade.get(answer)) or user == cuser or (user in ausers and ausers[user] == cuser):
            nuser, did_find_answer = cuser, True

            cinfo = core.LineParser.from_cell_id_user(cell_id, cuser)
            student_data = core.CellParser.crunch_data(cinfo=cinfo, data=answer, user=cuser)
            if show_correction and core.tools.REF_USER in cell_answers:
                out1 = ipywidgets.Output(layout={"width": "50%"})
                out2 = ipywidgets.Output(layout={"width": "50%"})
                tabs = ipywidgets.HBox([out1, out2])

                show_answer(out1, cuser, student_data.get_solution(), style=style)
                # bulkhours.c.set_style(out2, "sol_background")
                show_answer(out2, core.tools.REF_USER, teacher_data.get_solution(), style=style)

            else:
                tabs = ipywidgets.Output(layout={"width": "100%"})
                show_answer(tabs, cuser, student_data.get_solution(), style=style)

            out = ipywidgets.Output(layout={"border": "1px solid #CFCFCF", "width": "100%"})
            # bulkhours.c.set_style(out, "cell_background")

            if core.tools.REF_USER in cell_answers:
                with out:
                    create_evaluation_buttonanswer(cell_id, cuser, cfg, student_data, teacher_data)

            IPython.display.display(ipywidgets.VBox([tabs, out]))
            return

    if not did_find_answer:
        core.tools.html(
            f"Pas de réponse disponible pour {nuser}"
            if cfg.language == "fr"
            else f"{nuser} answer is not available",
            use_ipywidgets=True,
        )
