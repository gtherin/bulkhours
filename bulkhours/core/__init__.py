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

    def get_fversion(v):
        root_dir = "/home/guydegnol/projects"
        return f"{root_dir}/bulkhours{v}/bulkhours{v}/__version__.py"

    # Update the data doc
    from bulkhours.data import build_readme

    root_dir = "/home/guydegnol/projects"

    parser = argparse.ArgumentParser(description="Git helper")
    parser.add_argument("-m", "--message", help="Message", default="Some changes")
    parser.add_argument("-r", "--readme", action="store_true")
    args = parser.parse_args(argv)

    if args.readme:
        build_readme()

    ps = {"": ""}
    ovs = {k: open(get_fversion(v)).readline().split('"')[1] for k, v in ps.items()}
    nvs = {k: get_nversion(v) for k, v in ovs.items()}

    for r, p in ps.items():
        with open(get_fversion(p), "w") as the_file:
            the_file.write(f"""__version__ = "{nvs['']}"\n""")

    with open("git_push.sh", "w") as f:
        f.write(f"""python {root_dir}/pyservice/pyservice/generate_bulkhours_keys.py\n""")
        for r, p in ps.items():
            f.write(
                f"""cd ../bulkhours{p} && git pull && git add . && git commit -m "{args.message}" && git push 2> /dev/null\n"""
            )
        f.write(f"""python {root_dir}/pyservice/pyservice/generate_bulkhours_keys.py\n""")
    print(
        subprocess.run("bash git_push.sh".split(), stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True).stdout
    )

    os.system("rm -rf git_push.sh")

    print(
        f"BULK Helper cOURSe: \x1b[0mversion='{ovs['']}=>{nvs['']}' \x1b[36mpversion='{ovs['m']}=>{nvs['m']}'\x1b[0m🚀, \x1b[31maversion='{ovs['a']}=>{nvs['a']}'\x1b[0m⚠️"
    )
