import argparse
import sys
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
    if student_name is None or pass_code is None or pass_code == "PASS_COURSE":
        raise Exception.DefaultCredentialsError(
            f"""# Register yourself (Password "PASS" should be given in class). Example for John Doe, type:
bulkhours.set_up_student("jdoe", pass_code="PASS")
"""
        )

    os.environ["STUDENT"] = student_name
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = get_cred(d=directory, pass_code=pass_code)
    return student_name


def get_document(sid, user):
    if "STUDENT" not in os.environ:
        set_up_student(None)

    from google.cloud import firestore

    return firestore.Client().collection(sid).document(user)


def send_answer_to_corrector(question, answer, atype="code"):
    get_document(question, os.environ["STUDENT"]).set(
        {"answer": answer, "update_time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "atype": atype}
    )
    print(f'Answer has been submited for: {question}/{os.environ["STUDENT"]}. You can resubmit it several times')


def get_solution_from_corrector(question, corrector="solution"):
    return get_document(question, corrector).get().to_dict()


@magics_class
class Evaluation(Magics):
    def __init__(self, shell):
        super(Evaluation, self).__init__(shell)

        self.argparser = argparse.ArgumentParser(description="Evaluation params")
        self.argparser.add_argument(
            "-t", "--timeit", action="store_true", help="flag to return timeit result instead of stdout"
        )
        self.show_answer = False

    @line_cell_magic
    @needs_local_scope
    def evaluation_cell_id(self, line, cell, local_ns=None):
        cell_info = line.split()
        cell_id, cell_type = cell_info[0], cell_info[1] if len(cell_info) > 1 else "code"
        if cell_type == "code":
            self.shell.run_cell(cell)
        elif cell_type == "markdown":
            IPython.display.display(IPython.display.Markdown(cell))

        button = ipywidgets.Button(description="Send answer", button_style="primary")
        buttonc = ipywidgets.Button(description="Get correction", button_style="primary")
        output = ipywidgets.Output()

        def on_button_clicked(b):
            with output:
                output.clear_output()
                self.show_answer = not self.show_answer
                if self.show_answer:
                    b.button_style, b.description = "danger", f"Answer sent"
                    send_answer_to_corrector(cell_id, cell, atype=cell_type)
                else:
                    b.button_style, b.description = "primary", f"Send answer"

        def on_buttonc_clicked(b):
            with output:
                output.clear_output()
                self.show_answer = not self.show_answer
                if self.show_answer:
                    b.button_style, b.description = "danger", f"Hide correction"
                    text = get_solution_from_corrector(cell_id, corrector="solution")

                    if text is None:
                        IPython.display.display(
                            IPython.display.Markdown(
                                f"""---
**Solution ('{cell_id}') is not available (yet)** 😕
---"""
                            )
                        )
                    else:
                        IPython.display.display(
                            IPython.display.Markdown(
                                f"""---
**Correction ({cell_id})** 🤓
---"""
                            )
                        )

                        if cell_type == "code":
                            IPython.display.display(IPython.display.Code(text["answer"]))
                            IPython.display.display(
                                IPython.display.Markdown(
                                    f"""---
**Let's execute the code (for {cell_id})** 💻
---"""
                                )
                            )
                            self.shell.run_cell(text["answer"])
                        elif cell_type == "markdown":
                            IPython.display.display(IPython.display.Markdown(text["answer"]))
                else:
                    b.button_style, b.description = "primary", "Get correction"

        button.on_click(on_button_clicked)
        buttonc.on_click(on_buttonc_clicked)

        IPython.display.display(ipywidgets.HBox([button, buttonc]), output)


def get_arg_parser(argv):
    import argcomplete

    parser = argparse.ArgumentParser(
        description="Students evaluation",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("-e", "--evaluation-id", help=f"Select which correction to apply")
    parser.add_argument("-s", "--show-solution", help="Show the solution", action="store_true")
    parser.add_argument("-d", "--delete-solution", help="Delete the solution", action="store_true")
    parser.add_argument("-p", "--pass-code", help="Pass code")

    argcomplete.autocomplete(parser)
    return parser.parse_args(argv)


def dump_corrections(argv=sys.argv, promo="2023"):
    args = get_arg_parser(argv[1:])

    from google.cloud import firestore

    set_up_student("correction", pass_code=args.pass_code)

    if args.delete_solution:
        docs = firestore.Client().collection(args.evaluation_id).document("solution").delete()

    docs = firestore.Client().collection(args.evaluation_id).stream()

    directory = os.path.realpath(f"../bulkhours_admin/data/{promo}/")

    with open(f"{directory}/{args.evaluation_id}.txt", "w") as f:
        for answer in docs:
            student_name, student = answer.id, answer.to_dict()
            if answer.id == "solution" and not args.show_solution:
                continue
            student_ts = student["update_time"]
            student_answer = student["answer"]

            title = f"Answer from {student_name} at {student_ts}"
            sep = "#################################################"
            f.write(f"{sep}\n{title}\n{sep}\n{student_answer}")

    print(f"Data was dump here {directory}/{args.evaluation_id}.txt")
