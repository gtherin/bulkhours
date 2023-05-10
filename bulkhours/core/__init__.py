import os
import sys
import argparse
import subprocess

from .data import *  # noqa
from .evaluation import *  # noqa

from .widgets.tools import md  # noqa

# from .widgets.buttons import *  # noqa
# from .gpt import ask_chat_gpt  # noqa


def runrealcmd(command, verbose=True):
    logfile = open("install.log", "w")
    stdout, stderr = subprocess.PIPE, subprocess.STDOUT
    stdout, stderr = logfile, logfile
    process = subprocess.Popen(command, stdout=stdout, shell=True, stderr=stderr, bufsize=1, close_fds=True)
    print(f"RUN {command}")
    process.wait()


def git_push(argv=sys.argv[1:]):
    parser = argparse.ArgumentParser(description="Git helper")
    parser.add_argument("-m", "--message", help="Message", default="Some changes")
    args = parser.parse_args(argv)

    vfile = os.path.abspath(os.path.dirname(__file__)) + "/../__version__.py"
    version = (oversion := open(vfile).readline().split('"')[1]).split(".")
    nversion = f"{version[0]}.{version[1]}.{int(version[2])+1}"

    avfile = os.path.abspath(os.path.dirname(__file__)) + "/../../../bulkhours_admin/bulkhours_admin/__version__.py"
    aversion = (open(avfile).readline().split('"')[1]).split(".")
    naversion = f"{aversion[0]}.{aversion[1]}.{int(aversion[2])+1}"

    pvfile = (
        os.path.abspath(os.path.dirname(__file__)) + "/../../../bulkhours_premium/bulkhours_premium/__version__.py"
    )
    pversion = (open(pvfile).readline().split('"')[1]).split(".")
    npversion = f"{pversion[0]}.{pversion[1]}.{int(pversion[2])+1}"

    with open(vfile, "w") as the_file:
        the_file.write(f"""__version__ = "{nversion}"\n""")
        the_file.write(f"""__aversion__ = "{naversion}"\n""")
        the_file.write(f"""__pversion__ = "{npversion}"\n""")

    with open(avfile, "w") as the_file:
        the_file.write(f"""__aversion__ = "{naversion}"\n""")

    with open(pvfile, "w") as the_file:
        the_file.write(f"""__pversion__ = "{npversion}"\n""")

    print(f"Update {oversion} => {nversion}")
    with open("git_push.sh", "w") as f:
        f.write(f"""git pull && git add . && git commit -m "{args.message}" && git push""")
    print(
        subprocess.run("bash git_push.sh".split(), stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True).stdout
    )
    os.system("rm -rf git_push.sh")
