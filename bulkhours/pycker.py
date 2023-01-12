import argparse
import os
import dis, marshal
import py_compile

from IPython.core.magic import Magics, cell_magic, magics_class, line_cell_magic, needs_local_scope


def pyccompile_and_cat(cell):

    cache_file = "abc.py"
    os.system(f"rm -rf {cache_file}*")
    with open(cache_file, "w") as f:
        f.write(cell)

    py_compile.compile(cache_file, cfile=cache_file + "c")

    with open(cache_file + "c", "rb") as f:
        f.read(16)
        code_obj = marshal.load(f)
    dis.dis(code_obj)


@magics_class
class Picker(Magics):
    def __init__(self, shell):
        super(Picker, self).__init__(shell)

        self.argparser = argparse.ArgumentParser(description="Evaluation params")
        self.argparser.add_argument(
            "-t", "--timeit", action="store_true", help="flag to return timeit result instead of stdout"
        )

    @cell_magic
    @needs_local_scope
    def ipsa_pyccompile_and_cat(self, line, cell, local_ns=None):
        pyccompile_and_cat(cell)
        return None
