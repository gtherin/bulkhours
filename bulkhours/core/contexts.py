import IPython
import io
from contextlib import redirect_stdout
from .cell_parser import CellParser


def run_cell(code, stdout=True):
    if (ipp := IPython.get_ipython()) is None:
        print(f"No IPython instance found:\n{code}")
        return

    if not stdout:
        with redirect_stdout(f := io.StringIO()):
            run_cell(code)
            return f.getvalue().split()

    ipp.run_cell(code)


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


def generate_context_code(code, evaluation_code, context):
    code = CellParser.remove_meta_functions_execution(code)

    def tab(t):
        return "    " * t

    code = code.replace('"""', "'''")
    ncode = f"""\n
class C{context}:
{tab(1)}def __init__(self):
{tab(2)}self.stderr, self.stdout, self.code = "", "", \"""{code}\"""
{tab(2)}with redirect_stdout(stdout := io.StringIO()):
{tab(3)}try:
\n\n"""

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
                    if o != "":
                        objs.add(o)
                    break

        print(objs)
        for o in objs:
            ncode += f"{tab(4)}setattr(self, '{o}', {o})\n"

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
