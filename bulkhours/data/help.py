import glob
import os

from . import tools
from ..core.tools import abspath
from .datasets import datasets, ddatasets, datacategories  # noqa


def get_readme_filename(filename="README.md"):
    return abspath(f"../bulkhours/data/{filename}")


class Script:
    def __init__(self, text="", fname="script.sh") -> None:
        self.text = text + "\n"
        self.fname = fname

    def add_line(self, l) -> None:
        self.text += l + "\n"

    def execute(self, verbose=False) -> None:
        import subprocess

        if verbose:
            print(self.text)
        with open(self.fname, "w") as f:
            f.write(self.text)

        print(
            subprocess.run(
                f"bash {self.fname}".split(), stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True
            ).stdout
        )

        os.system(f"rm -rf {self.fname}")


def get_header_links(filename):
    return f"""[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/guydegnol/bulkhours/blob/main/{filename}) [![Open In Kaggle](https://kaggle.com/static/images/open-in-kaggle.svg)](https://kaggle.com/kernels/welcome?src=https://github.com/guydegnol/bulkhours/blob/main/{filename}) [![GitHub](https://badgen.net/badge/icon/Open%20in%20Github?icon=github&label)](https://github.com/guydegnol/bulkhours/blob/main/{filename}) [![Open in Visual Studio Code](https://img.shields.io/static/v1?logo=visualstudiocode&label=&message=Open%20in%20Visual%20Studio&labelColor=2c2c32&color=007acc&logoColor=007acc)](https://vscode.dev/github/guydegnol/bulkhours/blob/main/{filename}) [![CC-0 license](https://img.shields.io/badge/License-CC--0-blue.svg)](https://creativecommons.org/licenses/by-nd/4.0)"""


def generate_header_links(filename):
    import IPython

    IPython.display.display(IPython.display.Markdown(get_header_links(filename)))


def build_readme(load_data=True):
    examples = sorted(glob.glob(abspath("examples/*.ipynb")))

    with open(f"/home/guydegnol/projects/bulkhours/examples/README.md", "w") as ff:
        for example in examples:
            example_label = example.split("/")[-1].split(".")[0]
            filename = "examples/" + example.split("/")[-1]
            line = f"- [**`{example_label}`**](https://github.com/guydegnol/bulkhours/blob/main/{filename}) "
            line += get_header_links(filename) + "\n"
            ff.write(line)

    return
    if 0:
        s = Script("cd /home/guydegnol/projects/bulkhours")
        tdir = "../bulkhours.wiki"
        s.add_line(f"/opt/miniconda/condabin/conda activate bulkhours_py3.10")
        s.add_line(f"cp -r README.md {tdir}/Home.md")
        s.add_line(f"cp -r data/README.md {tdir}/Data.md")
        s.add_line(f"cp -r bulkhours/ecox/README.md {tdir}/Econometrics.md")
        s.add_line(f"cp -r bulkhours/hpc/README.md {tdir}/HPC.md")
        s.add_line(f"/opt/miniconda/envs/bulkhours_py3.10/bin/pdoc bulkhours/core/tools.py --force -o {tdir}/docs")
        s.add_line(f"/opt/miniconda/envs/bulkhours_py3.10/bin/pdoc bulkhours/core/equals.py -o {tdir}/docs")
        s.execute(verbose=True)

    import pdoc

    modules = ["bulkhours.core.equals"]
    context = pdoc.Context()  # docformat="numpy")  # markdown restructuredtext google numpy

    modules = [pdoc.Module(mod, context=context) for mod in modules]

    pdoc.link_inheritance(context)

    def recursive_htmls(mod):
        yield mod.name, mod.text()  # text html
        for submod in mod.submodules():
            # print(submod)
            yield from recursive_htmls(submod)

    for mod in modules:
        for module_name, html in recursive_htmls(mod):
            with open(f"/home/guydegnol/projects/bulkhours.wiki/{module_name.replace('.', '_')}.md", "w") as ff:
                ff.write(html)
                # print(html)
            # print(module_name, html)

    from ..phyu.constants import Units

    ffile = open(get_readme_filename(), "w")
    ffile.write("# Data\n\n")

    for c, category in enumerate(datacategories):
        ffile.write(f'- [{c+1}. {category["label"]}](#{category["tag"]}) \n')

    for c, category in enumerate(datacategories):
        # ffile.write(f'\n\n## [{c+1}. {category["label"]}](#{category["tag"]})\n\n')
        # ffile.write(f'\n\n## {c+1}. {category["label"]} <a name="{category["tag"]}"></a> \n\n')
        # ffile.write(f'\n\n## {category["label"]} <a name="# {category["tag"]}"></a> \n\n')
        ffile.write(f'\n\n## {category["tag"]} \n\n')

        if category["label"] == "Physics":
            ffile.write(Units().info(size="+1", code=True))

        for d in datasets:
            if d["category"] == category["tag"]:
                ffile.write(tools.DataParser(**d).get_info(load_columns=load_data))

    raw_files = set()
    for d in datasets:
        if "raw_data" in d and type(d["raw_data"]) == str:
            raw_files.add(d["raw_data"])

    dfiles = [f.split("/")[-1] for f in glob.glob(get_readme_filename("*"))]
    for f in dfiles:
        if f not in raw_files:
            print(f"{f}: data is not referenced")


def help():
    import IPython

    readme = open(get_readme_filename()).readlines()

    IPython.display.display(IPython.display.Markdown("\n".join(readme)))
