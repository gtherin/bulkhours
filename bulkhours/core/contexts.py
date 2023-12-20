import IPython
import io
from contextlib import redirect_stdout
from .cell_parser import CellParser
from .line_parser import LineParser
from . import tools


def remove_meta_functions_execution(code):
    ncode = ""
    for l in code.splitlines():
        if l.split("(")[0] not in [
            f"student_{m}_function" for m in CellParser.meta_modes
        ]:
            ncode += l + "\n"
    return ncode


def run_cell(code, stdout=True):
    if (ipp := IPython.get_ipython()) is None:
        print(f"No IPython instance found:\n{code}")
        return

    if not stdout:
        with redirect_stdout(f := io.StringIO()):
            run_cell(code)
            return f.getvalue().split()

    ipp.run_cell(code)


def enrich_evaluation_code(evaluation_code):
    return (
        f""" 
import os
os.environ['FINAL_SCORE'] = "0"
%s
global eresult
eresult = student_evaluation_function()
os.environ['FINAL_SCORE'] = str(eresult)
"""
        % evaluation_code
    )


def get_evaluation_code(teacher_data):
    evaluation_code = teacher_data.get_code("evaluation")
    if "def student_evaluation_function" not in evaluation_code:
        evaluation_code += """\ndef student_evaluation_function():\n    return bulkhours.admin.gpt_eval("syntax", max_score=10)"""

    return evaluation_code




def generate_empty_context(context):
    run_cell(
        f"""
import io
from contextlib import redirect_stdout

class CellContext:
    stdout = io.StringIO()
    stderr = io.StringIO()
                                           
{context} = CellContext()
"""
    )


def add_variables_in_contexts(cell_id, configs):
    for context in ["student", "teacher"]:
        run_cell(
            f"from argparse import Namespace\n{context}.{cell_id} = Namespace(**{configs})"
        )


def generate_context_code(code, evaluation_code, context, execute):
    code = remove_meta_functions_execution(code)

    def tab(t):
        return "    " * t

    code = code.replace('"""', "'''")
    ncode = f"""\n
class C{context}:
{tab(1)}def __init__(self):
{tab(2)}self.stderr, self.stdout, self.code = "", "", \"""{code}\"""\n"""
    if "catch_error=false" in evaluation_code.replace(" ", "").lower():
        ncode += f"""
{tab(2)}if True:
{tab(3)}if True:\n{tab(4)}pass\n\n\n"""
    else:
        ncode += f"""
{tab(2)}with redirect_stdout(stdout := io.StringIO()):
{tab(3)}try:\n{tab(4)}pass\n\n\n"""


    if not "execute=false" in evaluation_code.replace(" ", "").lower() or not execute:
        for l in code.splitlines():
            ncode += f"{tab(4)}{l}\n"

    if "student." in evaluation_code:
        objs = set()
        for c in evaluation_code.split("student."):
            o = ""
            for i in c:
                if i.isalnum() or i in ["_"]:
                    o += i
                else:
                    if o not in ["", "stderr", "stdout", "code"]:
                        objs.add(o)
                    break

        for o in objs:
            ncode += f"{tab(4)}setattr(self, '{o}', {o})\n"

        if "catch_error=false" in evaluation_code.replace(" ", "").lower():
            ncode += f"""
    {tab(2)}self.stderr = ""
    {tab(2)}self.stdout = ""
    """
        else:
            ncode += f"""
    {tab(2)}except Exception as e:
    {tab(3)}self.stderr = e
    {tab(2)}self.stdout = stdout.getvalue()
    """

    else:
        ncode += f"{tab(3)}for k, v in locals().items(): setattr(self, k, v)\n"
        ncode += f"""
    {tab(3)}except Exception as e:
    {tab(4)}self.stderr = e
    {tab(3)}self.stdout = stdout.getvalue()
"""

    ncode += f"\n{context.lower()} = C{context}()\n"
    return ncode

def black_format_str(code, line_length=500):
    black = tools.install_if_needed("black")

    return black.format_str(code, mode=black.Mode(line_length=line_length))


def get_contexts_codes(student_data, teacher_data, execute):
    """
    This function is used to evaluate the student code.

    :returns: student_code, teacher_code, evaluation_code
    """

    # Return default grade if no grade
    if student_data.get_code("main_execution") == "":
        return "", "", ""

    # Get the formatted evaluation code
    evaluation_code = get_evaluation_code(teacher_data)

    # Format with black
    evaluation_code = black_format_str(evaluation_code)

    # Get teacher code
    teacher_code = remove_meta_functions_execution(
        teacher_data.get_code("main_execution")
    )

    # Get student code
    student_code = remove_meta_functions_execution(
        student_data.get_code("main_execution")
    )

    # Re-assign the code
    if "recreate_contexts" in evaluation_code:
        icode, ecode, ecodes = [], [], evaluation_code.split("\n")
        for e in ecodes[1:]:
            if "recreate_contexts" in e:
                ecode.append(ecodes[0])
                if "replace" in (rc:=LineParser.get_func_args(e, "bulkhours.recreate_contexts")):
                    print(rc)
                    rc["replace"] = eval(black_format_str(rc["replace"]))
            elif len(ecode) > 0:
                ecode.append(e)
            else:
                icode.append(e[4:])

        student_code = "\n".join(icode) + "\n" + student_code
        teacher_code = "\n".join(icode) + "\n" + teacher_code
        if "replace" in rc:
            for r in rc["replace"]:
                student_code = student_code.replace(r[0], r[1])
                teacher_code = teacher_code.replace(r[0], r[1])

        evaluation_code = enrich_evaluation_code("\n".join(ecode))
    else:
        evaluation_code = enrich_evaluation_code(evaluation_code)

    student_code = generate_context_code(
        student_code, evaluation_code, "student", execute
    )
    teacher_code = generate_context_code(
        teacher_code, evaluation_code, "teacher", execute
    )


    return student_code, teacher_code, evaluation_code

