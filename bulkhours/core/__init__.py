import os
import sys
import argparse
import subprocess


from .evaluation import Evaluation  # noqa
from . import colors as c  # noqa
from .puppets import *  # noqa
from . import tools  # noqa
from . import firebase  # noqa
from . import buttons  # noqa
from .gpt import *  # noqa
from .equals import is_equal  # noqa
from .cache_manager import CacheManager  # noqa
from .widget_texts import WidgetTextArea  # noqa


def git_push(argv=sys.argv[1:]):
    def get_nversion(version):
        sversion = version.split(".")
        if int(sversion[2]) > 30:
            return f"{sversion[0]}.{int(sversion[1])+1}.0"
        else:
            return f"{sversion[0]}.{sversion[1]}.{int(sversion[2])+1}"

    # Update the data doc
    from bulkhours.data import build_readme

    parser = argparse.ArgumentParser(description="Git helper")
    parser.add_argument("-m", "--message", help="Message", default="Some changes")
    parser.add_argument("-r", "--readme", action="store_true")
    args = parser.parse_args(argv)

    if args.readme:
        build_readme()
    else:
        print("README was not updated")

    root_dir = "/home/guydegnol/projects"
    ovs = open(filename := f"{root_dir}/bulkhours/bulkhours/__version__.py").readline().split('"')[1]
    nvs = get_nversion(ovs)

    with open(filename, "w") as the_file:
        the_file.write(f"""__version__ = "{nvs}"\n""")

    with open("git_push.sh", "w") as f:
        f.write(f"""python {root_dir}/pyservice/pyservice/generate_bulkhours_keys.py\n""")
        for p in [""]:  # , ".wiki"]:
            f.write(
                f"""cd ../bulkhours{p} && git pull && git add . && git commit -m "{args.message}" && git push 2> /dev/null\n"""
            )
        f.write(f"""python {root_dir}/pyservice/pyservice/generate_bulkhours_keys.py\n""")
    print(
        subprocess.run("bash git_push.sh".split(), stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True).stdout
    )

    os.system("rm -rf git_push.sh")

    print(f"BULK Helper cOURSe: \x1b[36mpversion='{ovs}=>{nvs}'\x1b[0m🚀")
