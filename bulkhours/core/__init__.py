import os
import sys
import argparse
import subprocess

from .tools import md  # noqa


def runrealcmd(command, verbose=True):
    logfile = open("install.log", "w")
    stdout, stderr = subprocess.PIPE, subprocess.STDOUT
    stdout, stderr = logfile, logfile
    process = subprocess.Popen(command, stdout=stdout, shell=True, stderr=stderr, bufsize=1, close_fds=True)
    if verbose:
        print(f"RUN {command}")
    process.wait()


def get_nversion(version):
    sversion = version.split(".")
    if int(sversion[2]) > 30:
        return f"{sversion[0]}.{int(sversion[1])+1}.0"
    else:
        return f"{sversion[0]}.{sversion[1]}.{int(sversion[2])+1}"


def get_fversion(filename):
    return os.path.abspath(os.path.dirname(__file__)) + filename


def git_push(argv=sys.argv[1:]):
    # Update the data doc
    from bulkhours.data import build_readme

    build_readme()

    parser = argparse.ArgumentParser(description="Git helper")
    parser.add_argument("-m", "--message", help="Message", default="Some changes")
    args = parser.parse_args(argv)

    vfile = get_fversion("/../__version__.py")
    nversion = get_nversion(oversion := open(vfile).readline().split('"')[1])

    avfile = get_fversion("/../../../bulkhours_admin/bulkhours_admin/__version__.py")
    naversion = get_nversion(aversion := open(avfile).readline().split('"')[1])

    pvfile = get_fversion("/../../../bulkhours_premium/bulkhours_premium/__version__.py")
    npversion = get_nversion(pversion := open(pvfile).readline().split('"')[1])

    with open(vfile, "w") as the_file:
        the_file.write(f"""__version__ = "{nversion}"\n""")
        the_file.write(f"""__aversion__ = "{naversion}"\n""")
        the_file.write(f"""__mversion__ = "{npversion}"\n""")

    with open(avfile, "w") as the_file:
        the_file.write(f"""__version__ = "{naversion}"\n""")

    with open(pvfile, "w") as the_file:
        the_file.write(f"""__version__ = "{npversion}"\n""")

    with open("git_push.sh", "w") as f:
        # f.write(f"""python /home/guydegnol/projects/pyservice/pyservice/bulkhours.data.build_readme()\n""")
        f.write(f"""python /home/guydegnol/projects/pyservice/pyservice/generate_bulkhours_keys.py\n""")
        for p in ["", "_premium", "_admin"]:
            f.write(
                f"""cd ../bulkhours{p} && git pull && git add . && git commit -m "{args.message}" && git push 2> /dev/null\n"""
            )
        f.write(f"""python /home/guydegnol/projects/pyservice/pyservice/generate_bulkhours_keys.py\n""")
    print(
        subprocess.run("bash git_push.sh".split(), stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True).stdout
    )
    print(
        f"BULK Helper cOURSe: \x1b[0mversion='{oversion}=>{nversion}' \x1b[36mpversion='{pversion}=>{npversion}'\x1b[0m🚀, \x1b[31maversion='{aversion}=>{naversion}'\x1b[0m⚠️"
    )

    os.system("rm -rf git_push.sh")
