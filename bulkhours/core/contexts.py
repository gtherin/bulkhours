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
                if i.isalnum():
                    o += i
                else:
                    if o != "":
                        objs.add(o)
                    break

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


def build_context(
    execution_code,
    context,
    evaluation_code,
    do_debug=False,
    use_context=True,
    user="",
    execute=True,
):
    output = ipywidgets.Output()
    if execution_code == "":
        return output

    code = CellParser.remove_meta_functions_execution(execution_code)

    if "bulkhours.admin.replace(" in evaluation_code:
        replacements = evaluation_code.split("bulkhours.admin.replace(")
        for r in replacements[1:]:
            cmd = "code.replace(" + r.split("\n")[0]
            code = eval(cmd)

    generate_empty_context(context)
    if not (code is None or len(code.replace("\n", "").replace(" ", "")) == 0):
        fcode = (
            code
            if not use_context or "compile_and_exec" in code
            else generate_context_code(code, evaluation_code, context)
        )

        if do_debug:
            fcode = """
import tensorflow as tf
tf.keras.utils.set_random_seed(42)

print("AAAAAAAAAAAAAAAAAAA 4 ")
model = tf.keras.Sequential([
    tf.keras.layers.Flatten(input_shape=[12288]),
    tf.keras.layers.Dense(1, activation="sigmoid", kernel_initializer="he_normal", name="layer5")])        
print("AAAAAAAAAAAAAAAAAAA 5")
"""
            print("HHHHHHHHHHHHHHHHH")
            print(fcode)
            print("HHHHHHHHHHHHHHHHH")

        print(fcode)
        if execute:
            IPython.get_ipython().run_cell(fcode)
