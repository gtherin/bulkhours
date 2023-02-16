import argparse
import sys
import datetime
import os

from IPython.core.magic import Magics, cell_magic, magics_class, line_cell_magic, needs_local_scope


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


def set_up_student(student_name, d="bulkhours/bulkhours/bunker/", pass_code=None):
    if student_name == "noraise":
        return

    # TODO: Fix that thing in the future
    # Ok till I have less-restrictive rules on the server side
    if student_name is None or pass_code is None or pass_code == "PASS_COURSE":
        raise Exception.DefaultCredentialsError(
            f"""# Register yourself (Password "PASS" should be given in class). Example for John Doe, type:
bulkhours.set_up_student("jdoe", IPython, pass_code="PASS")
"""
        )

    os.environ["STUDENT"] = student_name
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = get_cred(d=d, pass_code=pass_code)
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


def get_solution_from_corrector(question, corrector="solution", raw=False):
    output = get_document(question, corrector).get().to_dict()
    if raw:
        return output

    if output is None or "answer" not in output:
        return f"Solution ('{question}') is not available (yet)"
    return output["answer"]


@magics_class
class Evaluation(Magics):
    def __init__(self, shell):
        super(Evaluation, self).__init__(shell)

        self.argparser = argparse.ArgumentParser(description="Evaluation params")
        self.argparser.add_argument(
            "-t", "--timeit", action="store_true", help="flag to return timeit result instead of stdout"
        )
        self.show_answer = False

    @cell_magic
    @needs_local_scope
    def send_answer_to_corrector(self, line, cell, local_ns=None):
        send_answer_to_corrector(line, cell, atype="code")
        self.get_solution_from_corrector(line)
        self.shell.run_cell(cell)

    @line_cell_magic
    @needs_local_scope
    def get_solution_from_corrector_old(self, line, cell="", local_ns=None):
        output = get_solution_from_corrector(line, corrector="solution", raw=True)

        if output is None:
            print(f"Solution ('{line}') is not available (yet)")
        else:
            print(
                f"""########## Correction (for {line}) is:          ########## 
{output["answer"]}
########## Let's execute the code ('{line}') now: ########## 
    """
            )
            self.shell.run_cell(output["answer"])

    @line_cell_magic
    @needs_local_scope
    def get_solution_from_corrector(self, line, cell="", local_ns=None):
        import IPython
        import ipywidgets

        button = ipywidgets.Button(description="Reveal answer", button_style="primary")
        output = ipywidgets.Output()

        def on_button_clicked(b):
            with output:
                output.clear_output()
                self.show_answer = not self.show_answer
                if self.show_answer:
                    b.button_style, b.description = "danger", f"Hide (.{line[-4:]}) answer"
                    text = get_solution_from_corrector(line, corrector="solution", raw=True)

                    if output is None:
                        print(f"Solution ('{line}') is not available (yet)")
                        # IPython.display.display(
                        #    IPython.display.Markdown(f"Solution ('{line}') is not available (yet)")
                        # )
                    else:
                        print(
                            f"""########## Correction (for {line}) is:          ########## 
{text["answer"]}
########## Let's execute the code ('{line}') now: ########## 
                """
                        )
                        self.shell.run_cell(text["answer"])
                else:
                    b.button_style, b.description = "primary", f"Reveal (.{line[-4:]}) answer"

        button.on_click(on_button_clicked)
        IPython.display.display(button, output)


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

    set_up_student("correction", d="bulkhours/bunker/", pass_code=args.pass_code)

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
