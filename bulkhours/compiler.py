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

    @line_cell_magic
    def compile_and_exec(self, line, cell="", local_ns=None):
        try:
            args = self.argparser.parse_args(line.split())
        except SystemExit as e:
            self.argparser.print_help()
            return

        with tempfile.TemporaryDirectory() as tmp_dir:
            try:
                # Write code file in a temp file
                file_path = os.path.join(tmp_dir, str(uuid.uuid4()))
                file_code = file_path + (".c" if args.compiler in ["g++", "gcc"] else ".cu")
                with open(file_code, "w") as f:
                    f.write(cell)

                # Compile file
                if args.compiler in ["g++", "gcc"]:
                    cmd = f"/usr/bin/{args.compiler} {file_code} -o {file_path}.out"
                else:
                    cmd = f"/usr/local/cuda/bin/nvcc {file_code} -o {file_path}.out -Wno-deprecated-gpu-targets"
                subprocess.check_output(cmd.split(), stderr=subprocess.STDOUT)

                # Run executable file
                return self.run(file_path + ".out", timeit=args.timeit)
            except OSError as e:
                print(f"Compiler {args.compiler} is probably not here.")
                self.argparser.print_help()
                for l in e.output.decode("utf8").split("\n"):
                    print(l)
            except subprocess.CalledProcessError as e:
                self.argparser.print_help()
                for l in e.output.decode("utf8").split("\n"):
                    print(l)
