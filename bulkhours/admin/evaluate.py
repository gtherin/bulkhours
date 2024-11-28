import IPython
import ipywidgets
import numpy as np
import pandas as pd
import re

from .. import core
from . import answers
from . import tools


def get_alias_name(cuser):
    if "@" in cuser:
        auser = cuser.split("@")[0].split(".")
        return auser[0].capitalize() + "." + auser[1][0]
    return cuser


def show_answer(out, cuser, answer, style=None, execute=True, black_format=False):
    color = "green" if cuser == core.tools.REF_USER else "red"
    cuser = get_alias_name(cuser)
    show_raw_code = (
        style == "dark"
    )  # not ("google.colab" in sys.modules and style != "dark")

    if black_format:
        answer = core.tools.black_format_str(answer)

    with out:
        # Show code
        core.tools.html(
            f"Code ({cuser})", size="4", color=color, use_ipywidgets=True, display=True
        )
        core.tools.code(answer, display=True, style=style)  # , raw=show_raw_code

        # Execute code
        core.tools.html(
            f"Execution ({cuser})💻",
            size="4",
            color=color,
            use_ipywidgets=True,
            display=True,
        )
        if execute:
            core.tools.eval_code(answer)


def create_evaluation_buttonanswer(cell_id, cuser, cfg, student_data, teacher_data):
    language = cfg.g["language"]
    label = core.tools.html(
        get_alias_name(cuser), size="6", color="#4F4F4F", use_ipywidgets=True
    )
    abuttons = core.buttons.get_buttons_list(
        label="", language=language, user=core.tools.REF_USER
    )
    output = ipywidgets.Output()

    grade = core.Grade.create_from_info(student_data)
    max_score = 10

    widget = ipywidgets.FloatSlider(
        min=0,
        max=max_score,
        value=grade.score,
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
            print("")
            answers.update_grade(cell_id, cuser, widget.value, grade_name="grade_man")

    if (
        "main_execution" in student_data.minfo
        and "main_execution" in teacher_data.minfo
        and core.gpt.evaluation_instructions is not None
    ):
        abuttons["a"].b.description = "🤖Correct student"

    def autocorrect(data, output):
        if (
            "main_execution" in student_data.minfo
            and "main_execution" in teacher_data.minfo
            and core.gpt.evaluation_instructions is not None
        ):
            print("")
            grade = core.gpt.get_grade(student_data, teacher_data, max_score)
            if grade != grade:
                answers.update_grade(
                    cell_id,
                    cuser,
                    grade.score,
                    grade_name="grade_bot",
                    comment=grade.comment,
                )
            return

        print("🚧Need to implement autocorrect here")

    def sevaluate2(b):
        return core.buttons.update_button(b, abuttons["e"], output, None, sevaluate)

    def sautocorrect(b):
        return core.buttons.update_button(b, abuttons["a"], output, None, autocorrect)

    abuttons["e"].b.on_click(sevaluate2)
    abuttons["a"].b.on_click(sautocorrect)

    IPython.display.display(
        ipywidgets.HBox([label, widget, abuttons["e"].b, abuttons["a"].b]), output
    )


def clean_grades(cell_id, **kwargs):
    cell_answers = answers.get_answers(cell_id, **kwargs)
    cfg = core.tools.get_config(is_new_format=True)
    for cuser, answer in cell_answers.items():
        if core.firebase.DbDocument.data_base_cache is None:
            from google.cloud import firestore

            dcols = {
                k: firestore.DELETE_FIELD
                for k in answer.keys()
                if k in ["note", "note_upd", "note_src", "grade_bot", "grade_bot_upd"]
            }
            core.firebase.get_document(question=cell_id, user=cuser, cinfo=cfg).update(
                dcols
            )
        else:
            dcols = {
                k: None
                for k in answer.items()
                if k in ["note", "note_upd", "note_src", "grade_bot", "grade_bot_upd"]
            }
            core.firebase.get_document(
                question=cell_id, user=cuser, cinfo=cfg
            ).delete_fields(
                answer, ["note", "note_upd", "note_src", "grade_bot", "grade_bot_upd"]
            )


def evaluate_student(
    cell_id,
    cfg,
    cuser,
    student_data,
    teacher_data,
    show_correction=True,
    style=None,
    execute=True,
    black_format=False,
):
    if show_correction and teacher_data.has_answer():
        out1 = ipywidgets.Output(layout={"width": "50%"})
        out2 = ipywidgets.Output(layout={"width": "50%"})
        tabs = ipywidgets.HBox([out1, out2])

        show_answer(
            out1,
            cuser,
            student_data.get_solution(),
            style=style,
            execute=execute,
            black_format=black_format,
        )
        # bulkhours.c.set_style(out2, "sol_background")
        show_answer(
            out2,
            core.tools.REF_USER,
            teacher_data.get_solution(),
            style=style,
            execute=execute,
            black_format=black_format,
        )

    else:
        tabs = ipywidgets.Output(layout={"width": "100%"})
        show_answer(
            tabs,
            cuser,
            student_data.get_solution(),
            style=style,
            execute=execute,
            black_format=black_format,
        )

    out = ipywidgets.Output(layout={"border": "1px solid #CFCFCF", "width": "100%"})
    # bulkhours.c.set_style(out, "cell_background")

    with out:
        create_evaluation_buttonanswer(cell_id, cuser, cfg, student_data, teacher_data)

    IPython.display.display(ipywidgets.VBox([tabs, out]))


def evaluate(
    cell_id,
    user="NEXT",
    show_correction=True,
    style=None,
    execute=True,
    virtual_room=None,
    level=None,
    teacher_data=None,
    duser=None,
    verbose=False,
    force_grades=False,
    normalize_score=True,
    black_format=False,
    delete_solution=False,
    **kwargs,
):
    if virtual_room is not None:
        cfg = tools.switch_classroom(virtual_room)
    else:
        cfg = core.tools.get_config(is_new_format=True)

    if user == "ALL":
        return evaluate_all(
            cell_id,
            user=user,
            show_correction=show_correction,
            style=style,
            execute=execute,
            virtual_room=virtual_room,
            level=level,
            teacher_data=teacher_data,
            duser=duser,
            verbose=verbose,
            force_grades=force_grades,
            normalize_score=normalize_score,
            delete_solution=delete_solution,
        )

    if cell_id == "NEXT":
        exos = cfg.n["exercices"].split(";")
        print(exos)
        return

    aliases = (
        core.firebase.get_document(question="info", user="aliases", cinfo=cfg)
        .get()
        .to_dict()
    )

    cell_answers = answers.get_answers(cell_id, aliases=aliases, **kwargs)
    cinfo = core.LineParser.from_cell_id_user(cell_id, core.tools.REF_USER)
    teacher_data = core.CellParser.crunch_data(
        cinfo=cinfo,
        data=cell_answers[core.tools.REF_USER]
        if core.tools.REF_USER in cell_answers
        else "",
        user=core.tools.REF_USER,
    )

    users = tools.get_users_list(no_admin=False, euser=user)
    uidx = (
        int(uidx)
        if user[:4] == "NEXT" and len(uidx := user.replace("NEXT", "")) > 0
        else 0
    )

    for e, u in enumerate(users.index):
        mail, auser = users["mail"][u], users["auser"][u]
        cinfo = core.LineParser.from_cell_id_user(cell_id, mail)
        student_data = core.CellParser.crunch_data(
            cinfo=cinfo,
            data=cell_answers[mail] if mail in cell_answers else "",
            user=mail,
        )

        if (
            user[:4] == "NEXT"
            and student_data.has_answer()
            and core.Grade.ANSWER_FOUND == int(student_data.get_grade(level).score)
        ):
            if uidx > 0:
                uidx -= 1
                continue
            print(f"{e}/{len(users)}")
            return evaluate_student(
                cell_id,
                cfg,
                mail,
                student_data,
                teacher_data,
                show_correction=show_correction,
                style=style,
                execute=execute,
                black_format=black_format,
            )
        if user == mail or user == auser:
            return evaluate_student(
                cell_id,
                cfg,
                mail,
                student_data,
                teacher_data,
                show_correction=show_correction,
                style=style,
                execute=execute,
                black_format=black_format,
            )

    core.tools.html(
        f"Pas de traitement possible pour {user}"
        if cfg.language == "fr"
        else f"No possible treatment for {user}",
        use_ipywidgets=True,
    )


def is_automatic_evaluation(evaluation_code=""):
    return "def student_evaluation_function" not in evaluation_code or "admin.gpt_eval" in evaluation_code or "gpt_evaluation" in evaluation_code


def evaluate_all(
    cell_id,
    user="ALL",
    show_correction=True,
    style=None,
    execute=True,
    virtual_room=None,
    level=None,
    teacher_data=None,
    duser=None,
    verbose=False,
    force_grades=False,
    normalize_score=True,
    delete_solution=False,
):
    grades = tools.get_users_list(no_admin=False)

    cinfo = core.LineParser.from_cell_id_user(cell_id, core.tools.REF_USER)

    grades[cell_id + ".n"] = np.nan
    grades = grades[["auser", "mail", cinfo.cell_id + ".n"]]

    print(f"\x1b[35m\x1b[1mNotes for {cinfo.cell_id}: \x1b[m", end="")

    if teacher_data is None:
        teacher_data = core.CellParser.crunch_data(
            cinfo=cinfo, user=core.tools.REF_USER, data=None
        )

    # Get basic evaluation code
    evaluation_code = teacher_data.get_code("evaluation")


    # Get parameters of evaluation_code
    matches = re.findall(r"(\w+)\s*=\s*([^\),\s]+)", evaluation_code)
    evaluation_params = {name: value for name, value in matches}

    if verbose:
        print(evaluation_code)
        print(evaluation_params)

    # Get default max_score
    max_score = float(evaluation_params["max_score"]) if "max_score" in evaluation_params else 10.

    # Get answers
    cell_answers = answers.get_answers(cinfo.cell_id, verbose=False)

    is_gpt = is_automatic_evaluation(evaluation_code)
    if is_gpt:
        if verbose:
            print(core.gpt.evaluation_instructions.replace("MAX_SCORE", str(max_score)))
        messages=[
            {"role": "system", "content": core.gpt.evaluation_instructions.replace("MAX_SCORE", str(max_score))},
            {"role": "user", "content": "Here is the expected solution:\n%s" % teacher_data.get_solution()},
        ]
        for stu in cell_answers:
            student_data = core.CellParser.crunch_data(cinfo=cinfo, data=cell_answers[stu], user=stu)
            messages.append({"role": "user", "content": "Here is the answer of student '%s':\n%s" % (stu, student_data.get_solution())})

        grades_gpt = core.gpt.evaluate_with_gpt(messages)

    for u in grades.index:
        email, auser = grades["mail"][u], grades["auser"][u]
        if type(email) == pd.Series:
            email, auser = email.iloc[0], auser.iloc[0]

        if duser is not None and auser != duser:
            continue

        # print(f"\x1b[35m\x1b[1m{auser}, \x1b[m", end="")
        if email not in cell_answers:
            print(f"\x1b[35m\x1b[1m(nan), \x1b[m", end="")
            continue

        # Get student data
        student_data = core.CellParser.crunch_data(
            cinfo=cinfo, data=cell_answers[email], user=email
        )

        # Don't manual data is available
        comment = ""
        if is_gpt:
            if email in grades_gpt:
                grade = grades_gpt[email]
            else:
                continue
        elif student_data.is_manual_note() and email != core.tools.REF_USER:
            comment = student_data.minfo["grade_man_comment"] if "grade_man_comment" in student_data.minfo else "To be discussed with evaluator"
            grade = core.Grade(score=student_data.minfo["grade_man"], src="man", comment=comment)
            comment = " [MAN]"
        else:
            grade = core.equals.student_evaluation_function(
                student_data,
                teacher_data,
                user=auser,
                verbose=verbose,
                execute=execute,
                normalize_score=normalize_score,
            )


        print(f"\x1b[35m\x1b[1m({grade.score}{comment}), \x1b[m", end="")
        grades.loc[u, cinfo.cell_id + ".n"] = grade.score
        grades.loc[u, cinfo.cell_id + ".c"] = grade.comment

        if email == core.tools.REF_USER:
            max_score = grade.score

    answers.update_grades(cinfo.cell_id, grades, "grade_bot" if is_gpt else "grade_ana")

    del grades[cinfo.cell_id + ".c"]
    grades = grades.drop(columns=["mail"]).set_index("auser").T

    core.Grade.set_static_style_info(minvalue=0.0, cmap=(cmap := "RdBu"))
    fstyles = lambda v: core.Grade.apply_style(v, False)
    grades = (
        grades.style.format(precision=1)
        .map(fstyles)
        .background_gradient(cmap=cmap, vmin=0, vmax=max_score)
    )
    IPython.display.display(grades)
    if delete_solution:
        core.firebase.delete_documents(cinfo, cinfo.cell_id, verbose=True)

