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


def set_up_student(student_name, d="bulkhours/bulkhours/", pass_code=None):
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


@magics_class
class Evaluation(Magics):
    def __init__(self, shell):
        super(Evaluation, self).__init__(shell)

        self.argparser = argparse.ArgumentParser(description="Evaluation params")
        self.argparser.add_argument(
            "-t", "--timeit", action="store_true", help="flag to return timeit result instead of stdout"
        )

    @cell_magic
    @needs_local_scope
    def send_answer_to_corrector(self, line, cell, local_ns=None):

        get_document(line, os.environ["STUDENT"]).set(
            {"answer": cell, "update_time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
        )

        self.shell.run_cell(cell)
        print(f'Answer has been submited for: {line}/{os.environ["STUDENT"]}. You can resubmit it several times')

    @line_cell_magic
    @needs_local_scope
    def get_solution_from_corrector(self, line, cell="", local_ns=None):

        output = get_document(line, "solution").get().to_dict()

        if output is None:
            print(f"Solution (for question {line}) is not available (yet)")
        else:
            print(
                f"""########## Correction (for {line}) is:          ########## 
{output["answer"]}
########## Let's execute the code (for {line}) now: ########## 
    """
            )
            self.shell.run_cell(output["answer"])


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


def dump_corrections(argv=sys.argv):

    args = get_arg_parser(argv[1:])
    promo = "2022"

    from google.cloud import firestore

    set_up_student("correction", d="bulkhours/", pass_code=args.pass_code)

    if args.delete_solution:
        docs = firestore.Client().collection(args.evaluation_id).document("solution").delete()

    docs = firestore.Client().collection(args.evaluation_id).stream()

    directory = os.path.realpath(f"../course_admin/data/{promo}/")

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
