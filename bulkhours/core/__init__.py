from .data import *  # noqa
from .evaluation import *  # noqa
from .textstyles import *  # noqa
import sys


def runrealcmd(command, verbose=True):
    from subprocess import Popen, PIPE, STDOUT

    logfile = open("install.log", "w")
    stdout, stderr = PIPE, STDOUT
    stdout, stderr = logfile, logfile
    process = Popen(command, stdout=stdout, shell=True, stderr=stderr, bufsize=1, close_fds=True)
    print(f"RUN {command}")
    process.wait()


def git_push(argv=sys.argv[1:]):
    from subprocess import Popen, PIPE, STDOUT

    parser = argparse.ArgumentParser(description="Git helper")
    parser.add_argument("-m", "--message", help="Message", default="Some changes")
    args = parser.parse_args(argv)

    vfile = os.path.abspath(os.path.dirname(__file__)) + "/../__version__.py"
    version = (oversion := open(vfile).readline().split('"')[1]).split(".")
    nversion = f"{version[0]}.{version[1]}.{int(version[2])+1}"

    with open(vfile, "w") as the_file:
        the_file.write(f"""__version__ = "{nversion}"\n""")

    print(f"Update {oversion} => {nversion}")
    cmd = f"""git add . && git commit -m "{args.message}" && git push"""
    Popen(cmd, stdout=PIPE, shell=True, stderr=STDOUT)
