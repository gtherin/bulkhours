from .data import *  # noqa
from .evaluation import *  # noqa


def runrealcmd(command, verbose=True):
    from subprocess import Popen, PIPE, STDOUT

    logfile = open("install.log", "w")
    stdout, stderr = PIPE, STDOUT
    stdout, stderr = logfile, logfile
    process = Popen(command, stdout=stdout, shell=True, stderr=stderr, bufsize=1, close_fds=True)
    # if verbose:
    #    for line in iter(process.stdout.readline, b""):
    #        print(line.rstrip().decode("utf-8"))
    # else:
    # process.stdout.close()
    print(f"RUN {command}")
    process.wait()
