import IPython
import io
import ipywidgets
from contextlib import redirect_stdout
from .cell_parser import CellParser


def exec_code(code, debug=False):
    if debug:
        print("Run in debug mode")

        IPython.get_ipython().run_cell(code)
        return ["FINAL_SCORE=-9999/10"]
    else:
        with redirect_stdout(f := io.StringIO()):
            IPython.get_ipython().run_cell(code)
            return f.getvalue().split()


def generate_empty_context(context):
    return f"""
class EmptyEnv:

    @property
    def data(self):
        return 3

    @property
    def stdout2(self):
        return True

    #def __getattr__(cls, key, *kargs, **kwargs):
    #    if key == "error":
    #        print("Yes bon del")
    #    return None

{context} = EmptyEnv()
"""


def generate_context_code(code, context):
    code = CellParser.remove_meta_functions_execution(code)
    ncode = f"\n\nclass C{context}:\n"
    for l in code.splitlines():
        ncode += f"    {l}\n"

    ncode += f"{context.lower()} = C{context}\n"
    return ncode


def build_context(data, code_label, context, do_evaluate, do_debug=False, use_context=True):
    output = ipywidgets.Output()
    if code_label not in data.minfo:
        return output

    code = CellParser.remove_meta_functions_execution(data.get_code(code_label))
    IPython.get_ipython().run_cell(generate_empty_context(context))
    if not (code is None or len(code.replace("\n", "").replace(" ", "")) == 0):
        fcode = code if not use_context or "compile_and_exec" in code else generate_context_code(code, context)

        if do_debug:
            print(f"Execute context {context}/{code_label}/{data.minfo['source']}")
            IPython.get_ipython().run_cell(fcode)
        else:
            with output:
                if do_evaluate:
                    with redirect_stdout(f := io.StringIO()):
                        IPython.get_ipython().run_cell(fcode)
                        IPython.get_ipython().run_cell(f'{context}.stdout="""{f.getvalue()}"""')

    if data.is_cell_type():
        IPython.get_ipython().run_cell(f'{context}.answer={data["answer"]}')
    return output
