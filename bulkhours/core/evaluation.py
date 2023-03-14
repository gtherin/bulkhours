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


def send_answer_to_corrector(question, update=False, user=None, comment="", **kwargs):
    user = os.environ["STUDENT"] if user is None else user
    kwargs.update({"update_time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")})

    if update and get_document(question, user).get().to_dict():
        get_document(question, user).update(kwargs)
    else:
        get_document(question, user).set(kwargs)
    print(f"Answer {comment} has been submited for: {question}/{user}. You can resubmit it several times")


def get_solution_from_corrector(question, corrector="solution"):
    return get_document(question, corrector).get().to_dict()


def get_description(i, j, update=False, lan="fr"):
    if lan == "fr":
        descriptions = [
            [
                dict(description="Envoyer au correcteur", button_style="primary"),
                dict(description="Correction envoyée", button_style="success"),
            ],
            [
                dict(description="Voir la correction", button_style="primary"),
                dict(description="Cacher la correction", button_style="danger"),
            ],
            [
                dict(description="Message au correcteur", button_style="info"),
                dict(description="Cacher le message du correcteur", button_style="warning"),
            ],
        ]
    else:
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
        dict(flex_flow="column", align_items="stretch", layout=ipywidgets.Layout(width="max-content"))
    )
    if update:
        return descriptions[i][j]["button_style"], descriptions[i][j]["description"]

    return ipywidgets.Button(**descriptions[i][j])


def md(mdbody=None, header=None, rawbody=None, codebody=None):
    if header:
        IPython.display.display(
            IPython.display.Markdown(f"<b><font face='FiraCode Nerd Font' size=4 color='red'>{header} 📚:<font></b>")
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
        self.argparser.add_argument("-i", "--id", default=None)
        self.argparser.add_argument("-u", "--user", default=os.environ["STUDENT"])
        self.argparser.add_argument("-o", "--options", default=None)
        self.show_answer = False

    def show_cell(self, cell_id, cell_type, corrector="solution", private_msg=False, answer=None):
        data = get_solution_from_corrector(cell_id, corrector=corrector)

        if data is None and private_msg:
            pass
        elif data is None:
            md(mdbody=f"""*Solution ({cell_id}, {cell_type}) is not available (yet 😕)*""")
        elif private_msg:
            if (user := os.environ["STUDENT"]) in data or (user := "all") in data:
                md(header=f"Message ({cell_id}, {user}) from corrector", rawbody=data[user])
        elif cell_type == "code":
            md(header=f"Correction ({cell_id}, {cell_type})", rawbody=data["answer"])
            md(
                f"""---
**Let's execute the code (for {cell_id})** 💻
    ---"""
            )
            self.shell.run_cell(data["answer"])
        elif cell_type in ["markdown", "textarea"]:
            md(header=f"Correction ({cell_id})", mdbody=data["answer"])
        elif cell_type == "codetext":
            md(mdbody=f"Correction 🤓: {data['answer']} (code({data['code']})")
        if "hidecode" in data:
            if answer is not None:
                hide_code = data["hidecode"].replace("ANSWER", str(answer))
            elif "answer" in data:
                hide_code = data["hidecode"].replace("ANSWER", str(data["answer"]))
            self.shell.run_cell(hide_code)

    @line_cell_magic
    @needs_local_scope
    def message_cell_id(self, line, cell="", local_ns=None):
        cell_info = line.split()
        cell_id, cell_user = cell_info[0], cell_info[1] if len(cell_info) > 1 else "all"
        send_answer_to_corrector(cell_id, update=True, **{cell_user: cell})

    @line_cell_magic
    @needs_local_scope
    def update_cell_id(self, line, cell="", local_ns=None):
        try:
            args = self.argparser.parse_args(line.split())
        except SystemExit as e:
            self.argparser.print_help()
            return

        opts = {
            a.split(":")[0]: cell if a.split(":")[1] == "CELL" else a.split(":")[1] for a in args.options.split(";")
        }
        send_answer_to_corrector(args.id, update=True, user=args.user, **opts)

    @line_cell_magic
    @needs_local_scope
    def evaluation_cell_id(self, line, cell="", local_ns=None):
        cell_info = line.split()
        cell_id, cell_type = cell_info[0], cell_info[1] if len(cell_info) > 1 else "code"

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

        cell_label = " ".join(cell_info[2:-1]) if ";" in cell_info[-1] else " ".join(cell_info[2:])
        cell_checks = cell_info[-1].split(";")

        if cell_type in ["code", "markdown"]:
            label = []
        else:
            label = [
                ipywidgets.HTML(
                    value=f"<font face='FiraCode Nerd Font' size=4 color='black'>{cell_label}<font>",
                    layout=ipywidgets.Layout(height="auto", width="auto"),
                )
            ]

        if cell_type == "checkboxes":
            widgets = [ipywidgets.Checkbox(value=False, description=i, indent=False) for i in cell_checks]
        elif cell_type == "intslider":
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

        elif cell_type == "textarea":
            widgets = [ipywidgets.Textarea(placeholder="I don't know", disabled=False)]
        elif cell_type == "radios":
            widgets = [ipywidgets.RadioButtons(options=cell_checks, layout={"width": "max-content"})]
        elif cell_type == "codetext":
            widgets = [ipywidgets.Text()]
        else:
            widgets = []

        def get_answer(widgets, cell_type):
            if cell_type in ["codetext"]:
                return eval(widgets[0].value)
            elif cell_type in ["code", "markdown"]:
                return cell
            elif cell_type in ["checkboxes", "radios"]:
                return ";".join([cell_checks[k] for k, i in enumerate(widgets) if i.value])
            else:
                return widgets[0].value

        def submit(b):
            answer = get_answer(widgets, cell_type)
            if answer == "":
                with output:
                    output.clear_output()
                    md(mdbody=f"Nothing to send 🙈🙉🙊")
                return

            pams = dict(answer=answer, atype=cell_type)

            if cell_type in ["codetext"]:
                pams.update(dict(code=widgets[0].value, comment=f"'{widgets[0].value}'"))
            if cell_type in ["textarea", "intslider"]:
                pams.update(dict(comment=f"'{widgets[0].value}'"))
            return func(b, 0, send_answer_to_corrector, [cell_id], pams)

        buttons[0].on_click(submit)

        def fun1(b):
            answer = get_answer(widgets, cell_type)
            return func(b, 1, self.show_cell, [cell_id, cell_type], dict(answer=answer))

        buttons[1].on_click(fun1)

        def fun2(b):
            return func(b, 2, self.show_cell, [cell_id, cell_type], dict(private_msg=True))

        buttons[2].on_click(fun2)

        layout = (
            ipywidgets.Layout(overflow="scroll hidden", width="auto", flex_flow="row", display="flex")
            if cell_type == "checkboxes"
            else ipywidgets.Layout()
        )

        IPython.display.display(ipywidgets.HBox(label + widgets + buttons[:2], layout=layout), output)
