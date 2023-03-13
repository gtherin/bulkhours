import argparse
import datetime
import os
import json

from IPython.core.magic import Magics, cell_magic, magics_class, line_cell_magic, needs_local_scope
import IPython
import ipywidgets


def get_cred(k="pi.pyc", d=None, pass_code=None):
    os.system(f"rm -rf {d}{k}")
    with open(d + k, "w") as f:
        f.write(
            open(f"{d}/pi.so")
            .read()
            .replace("eagezehrzqHHZHZ", "999d262597343d1840c218c3da3ec9c6f803aaf6")
            .replace("egzezqh234ehzqh22", pass_code)
        )
    return d + k


def clean_student_name(student_name):
    import unicodedata

    student_name = unicodedata.normalize("NFKD", student_name.replace("-", "").replace(" ", "").lower())
    return student_name.encode("ASCII", "ignore").decode("utf-8")


def set_up_student(student_name, pass_code=None):
    directory = os.path.dirname(__file__) + "/../bunker/"

    if pass_code is None:
        jsonfile = os.path.dirname(__file__) + "/../../.safe"
        if os.path.exists(jsonfile):
            with open(jsonfile) as json_file:
                data = json.load(json_file)
                pass_code = data["pass_code"]
    if student_name == "noraise":
        return

    # TODO: Fix that thing in the future
    # Ok till I have less-restrictive rules on the server side
    if student_name is None or student_name in ["None", ""] or pass_code is None or pass_code == "PASS_COURSE":
        raise Exception.DefaultCredentialsError(
            f"""# Register yourself (Password "PASS" should be given in class). Example for "John Doe", type:
bulkhours.set_up_student("john.d", pass_code="PASS")
"""
        )

    os.environ["STUDENT"] = clean_student_name(student_name)
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = get_cred(d=directory, pass_code=pass_code)
    return student_name


def get_document(sid, user):
    if "STUDENT" not in os.environ:
        set_up_student(None)

    from google.cloud import firestore

    return firestore.Client().collection(sid).document(user)


def send_answer_to_corrector(question, update=False, **kwargs):
    kwargs.update({"update_time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")})
    if update:
        get_document(question, os.environ["STUDENT"]).update(kwargs)
    else:
        get_document(question, os.environ["STUDENT"]).set(kwargs)
    print(f'Answer has been submited for: {question}/{os.environ["STUDENT"]}. You can resubmit it several times')


def get_solution_from_corrector(question, corrector="solution"):
    return get_document(question, corrector).get().to_dict()


def get_description(i, j, update=False):
    descriptions = [
        [
            dict(description="Send answer to corrector", button_style="primary"),
            dict(description="Answer sent to corrector", button_style="success"),
        ],
        [
            dict(description="Show correction", button_style="primary"),
            dict(description="Hide correction", button_style="danger"),
        ],
        [
            dict(description="Message from corrector", button_style="info"),
            dict(description="Hide message from corrector", button_style="warning"),
        ],
    ]
    descriptions[i][j].update(
        dict(display="flex", flex_flow="column", align_items="stretch", layout=ipywidgets.Layout(width="auto"))
    )
    if update:
        return descriptions[i][j]["button_style"], descriptions[i][j]["description"]

    return ipywidgets.Button(**descriptions[i][j])


def md(mdbody=None, header=None, rawbody=None, codebody=None):
    if header:
        IPython.display.display(
            IPython.display.Markdown(
                f"""---
    **{header}** 🤓
    ---"""
            )
        )

    if mdbody and len(mdbody) > 1:
        IPython.display.display(IPython.display.Markdown(mdbody))
    if rawbody and len(rawbody) > 1:
        print(rawbody)
    if codebody and len(codebody) > 1:
        IPython.display.display(IPython.display.Code(codebody))


@magics_class
class Evaluation(Magics):
    def __init__(self, shell):
        super(Evaluation, self).__init__(shell)

        self.argparser = argparse.ArgumentParser(description="Evaluation params")
        self.argparser.add_argument(
            "-t", "--timeit", action="store_true", help="flag to return timeit result instead of stdout"
        )
        self.show_answer = False

    def show_cell(self, cell_id, cell_type, corrector="solution", private_msg=False):
        text = get_solution_from_corrector(cell_id, corrector=corrector)

        if text is None and private_msg:
            pass
        elif text is None:
            md(mdbody=f"""*Solution ({cell_id}, {cell_type}) is not available (yet 😕)*""")
        elif private_msg:
            if (user := os.environ["STUDENT"]) in text or (user := "all") in text:
                md(header=f"Message ({cell_id}, {user}) from corrector", rawbody=text[user])
        elif cell_type == "code":
            md(header=f"Correction ({cell_id}, {cell_type})", rawbody=text["answer"])
            md(
                f"""---
    **Let's execute the code (for {cell_id})** 💻
    ---"""
            )
            self.shell.run_cell(text["answer"])
        elif cell_type == "markdown":
            md(header=f"Correction ({cell_id}, {cell_type})", mdbody=text["answer"])
        elif cell_type == "codetext":
            md(mdbody=f"Correction 🤓: {text['answer']} (code({text['code']})")

    @line_cell_magic
    @needs_local_scope
    def message_cell_id(self, line, cell="", local_ns=None):
        cell_info = line.split()
        cell_id, cell_user = cell_info[0], cell_info[1] if len(cell_info) > 1 else "all"
        send_answer_to_corrector(cell_id, update=True, **{cell_user: cell})

    @line_cell_magic
    @needs_local_scope
    def evaluation_cell_id(self, line, cell="", local_ns=None):
        cell_info = line.split()
        cell_id, cell_type = cell_info[0], cell_info[1] if len(cell_info) > 1 else "code"
        cell_label = " ".join(cell_info[2:]) if cell_type == "codetext" else ""

        buttons = [get_description(i, 0) for i in [0, 1, 2]]
        output = ipywidgets.Output()

        if cell_type == "code":
            self.shell.run_cell(cell)
        elif cell_type == "markdown":
            IPython.display.display(IPython.display.Markdown(cell))

        def func(b, i, func, args, kwargs):
            with output:
                output.clear_output()
                self.show_answer = not self.show_answer
                if self.show_answer:
                    b.button_style, b.description = get_description(i, 1, update=True)
                    func(*args, **kwargs)
                else:
                    b.button_style, b.description = get_description(i, 0, update=True)

        kargs = [
            [send_answer_to_corrector, [cell_id], dict(answer=cell, atype=cell_type)],
            [self.show_cell, [cell_id, cell_type], dict()],
            [self.show_cell, [cell_id, cell_type], dict(private_msg=True)],
        ]

        def fun1(b):
            return func(b, 1, *kargs[1])

        buttons[1].on_click(fun1)

        def fun2(b):
            return func(b, 2, *kargs[2])

        buttons[2].on_click(fun2)

        def fun0(b):
            return func(b, 0, *kargs[0])

        if cell_type != "codetext":
            buttons[0].on_click(fun0)
        else:
            label = ipywidgets.Button(description=cell_label, layout=ipywidgets.Layout(height="auto", width="auto"))
            text = ipywidgets.Text()

            def submit(b):
                total = eval(text.value)
                args = [send_answer_to_corrector, [cell_id], dict(answer=total, atype=cell_type, code=text.value)]
                return func(b, 0, *args)

            buttons[0].on_click(submit)

        if cell_type == "codetext":
            IPython.display.display(ipywidgets.HBox([label, text] + buttons[:2]), output)
        else:
            IPython.display.display(ipywidgets.HBox(buttons[:2]), output)
