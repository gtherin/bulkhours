import IPython
import ipywidgets
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
        run_cell(f"from argparse import Namespace\n{context}.{cell_id} = Namespace(**{configs})")


def generate_context_code(code, context):
    code = CellParser.remove_meta_functions_execution(code)
    def tab(t):
        return "    " * t
    ncode = f"""\n
class C{context}:
{tab(1)}def __init__(self):
{tab(2)}self.stderr, self.stdout = "", ""
{tab(2)}with redirect_stdout(stdout := io.StringIO()):
{tab(3)}try:
\n\n"""
    for l in code.splitlines():
        ncode += f"{tab(4)}{l}\n"
    ncode += f"""
{tab(3)}except Exception as e:
{tab(4)}self.stderr = e
"""

    ncode += f"{tab(3)}for k, v in locals().items(): setattr(self, k, v)\n"
    ncode += f"{tab(3)}self.stdout = stdout.getvalue()\n"
    ncode += f"{context.lower()} = C{context}()\n"
    return ncode


def build_context(data, code_label, context, do_evaluate, do_debug=False, use_context=True, user=""):
    output = ipywidgets.Output()
    if code_label not in data.minfo:
        return output

    code = CellParser.remove_meta_functions_execution(data.get_code(code_label))

    generate_empty_context(context)
    if not (code is None or len(code.replace("\n", "").replace(" ", "")) == 0):
        fcode = code if not use_context or "compile_and_exec" in code else generate_context_code(code, context)

        #print(fcode)
        IPython.get_ipython().run_cell(fcode)
        
    #if data.is_cell_type():
    #    run_cell(f'{context}.answer={data["answer"]}')
