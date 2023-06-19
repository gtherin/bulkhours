import os
import subprocess
import tempfile
import uuid
import argparse

from IPython.core.magic import Magics, line_cell_magic, magics_class


@magics_class
class CCPPlugin(Magics):
    def __init__(self, shell):
        super(CCPPlugin, self).__init__(shell)
        self.argparser = argparse.ArgumentParser(description="compile_and_exec params")
        self.argparser.add_argument(
            "-t", "--timeit", action="store_true", help="flag to return timeit result instead of stdout"
        )
        self.argparser.add_argument("-c", "--compiler", default="nvcc", choices=["nvcc", "g++", "gcc"])

    def run(self, exec_file, timeit=False):
        if timeit:
            stmt = f"subprocess.check_output(['{exec_file}'], stderr=subprocess.STDOUT)"
            output = self.shell.run_cell_magic(magic_name="timeit", line="-q -o import subprocess", cell=stmt)
        else:
            output = subprocess.check_output([exec_file], stderr=subprocess.STDOUT)
            output = output.decode("utf8")

        for l in output.split("\n"):
            print(l)

    def get_cell_decomposition(self, code=None):
        info = {}
        rawdata = self.cell_source if code is None else code
        if rawdata != "":
            info.update({"main_execution": "", "evaluation": "", "explanation": ""})
            mode = "main_execution"
            for l in rawdata.splitlines():
                for tmode in ["evaluation", "explanation"]:
                    # Switch modes
                    if f"def student_{tmode}_function(" in l or f"float student_{tmode}_function(" in l:
                        mode = tmode
                    # elif mode == tmode and len(l) > 0 and l[0] != " ":
                    #    mode = "main_execution"
                    # Remove endline for c++ function
                    # if l[0] == "}":
                    #    continue
                # print(mode, l, f"float student_{tmode}_function(" in l)
                info[mode] += l + "\n"
        return info

    @line_cell_magic
    def compile_and_exec(self, line, cell="", local_ns=None):
        try:
            self.cinfo = self.argparser.parse_args(line.split())
        except SystemExit as e:
            self.argparser.print_help()
            return

        params = self.get_cell_decomposition(code=cell)
        # print(params["main_execution"])

        with tempfile.TemporaryDirectory() as tmp_dir:
            try:
                # Write code file in a temp file
                file_path = os.path.join(tmp_dir, str(uuid.uuid4()))
                file_code = file_path + (".c" if self.cinfo.compiler in ["g++", "gcc"] else ".cu")
                with open(file_code, "w") as f:
                    f.write(params["main_execution"])

                # Compile file
                if self.cinfo.compiler in ["g++", "gcc"]:
                    cmd = f"/usr/bin/{self.cinfo.compiler} {file_code} -o {file_path}.out"
                else:
                    cmd = f"/usr/local/cuda/bin/nvcc {file_code} -o {file_path}.out -Wno-deprecated-gpu-targets"
                subprocess.check_output(cmd.split(), stderr=subprocess.STDOUT)

                # Run executable file
                return self.run(file_path + ".out", timeit=self.cinfo.timeit)
            except OSError as e:
                print(f"Compiler {self.cinfo.compiler} is probably not here.")
                self.argparser.print_help()
                for l in e.output.decode("utf8").split("\n"):
                    print(l)
            except subprocess.CalledProcessError as e:
                self.argparser.print_help()
                for l in e.output.decode("utf8").split("\n"):
                    print(l)
