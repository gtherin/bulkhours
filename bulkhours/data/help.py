import glob
import os

from . import tools
from .datasets import datasets, ddatasets, datacategories  # noqa


def get_readme_filename(filename="README.md"):
    return os.path.abspath(os.path.dirname(__file__) + f"../../../data/{filename}")


def get_rdata(d, dname):
    if dname not in d:
        return ""
    if "http" in d[dname]:
        label = d[dname].split("/")[-1]
        if "raw.githubusercontent.com" in d[dname]:
            address = d[dname].replace("raw.githubusercontent.com", "github.com")
            return f"[{label}]({address})  ([raw]({d[dname]}))"
        else:
            address = d[dname].replace("github.com", "raw.githubusercontent.com").replace("blob/", "")
            return f"[{label}]({d[dname]})  ([raw]({address}))"
    if type(d[dname]) in [list]:
        return ", ".join([f"[{f}](https://github.com/guydegnol/bulkhours/blob/main/data/{f})" for f in d[dname]])
    return f"[{d[dname]}](https://github.com/guydegnol/bulkhours/blob/main/data/{d[dname]})"


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


def build_readme(load_data=True):
    if 0:
        s = Script("cd /home/guydegnol/projects/bulkhours")
        tdir = "../bulkhours.wiki"
        s.add_line(f"/opt/miniconda/condabin/conda activate bulkhours_py3.10")
        s.add_line(f"cp -r README.md {tdir}/Home.md")
        s.add_line(f"cp -r data/README.md {tdir}/Data.md")
        s.add_line(f"cp -r bulkhours/ecox/README.md {tdir}/Econometrics.md")
        s.add_line(f"cp -r bulkhours/hpc/README.md {tdir}/HPC.md")
        s.add_line(f"/opt/miniconda/envs/bulkhours_py3.10/bin/pdoc bulkhours/core/tools.py --force -o {tdir}/docs")
        s.add_line(
            f"/opt/miniconda/envs/bulkhours_py3.10/bin/pdoc ../bulkhours_premium/bulkhours_premium/equals.py -o {tdir}/docs"
        )
        s.execute(verbose=True)

    import pdoc

    # import markdown2

    modules = ["bulkhours_premium.equals"]
    context = pdoc.Context()  # docformat="numpy")  # markdown restructuredtext google numpy

    modules = [pdoc.Module(mod, context=context) for mod in modules]

    pdoc.link_inheritance(context)

    def recursive_htmls(mod):
        yield mod.name, mod.text()  # text html
        for submod in mod.submodules():
            print(submod)
            yield from recursive_htmls(submod)

    for mod in modules:
        for module_name, html in recursive_htmls(mod):
            with open(f"/home/guydegnol/projects/bulkhours.wiki/{module_name.replace('.', '_')}.md", "w") as ff:
                ff.write(html)
                print(html)
            # print(module_name, html)
    return

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
            if d["category"] != category["tag"]:
                continue

            columns = None
            if load_data:
                try:
                    data = tools.DataParser(**d).get_data()
                    columns = list(data.columns)
                except:
                    pass

            comment = ""
            if "summary" in d:
                comment += f"### {d['summary']}\n"
            comment += f'#### `bulkhours.get_data("{d["label"]}")`\n'
            if "raw_data" in d:
                comment += f"- Raw data: {get_rdata(d, 'raw_data')}\n"
            if "enrich_data" in d:
                comment += f"- Enrich data: {get_rdata(d, 'enrich_data')}\n"
            if "source" in d:
                comment += d["source"] + "\n"
            if "ref_source" in d:
                comment += f"- Direct source: {d['ref_source']}\n"
            if "ref_site" in d:
                comment += f"- Reference site: {d['ref_site']}\n"
            if "columns" in d or columns is not None:
                comment += f"- Columns:\n"
                if "columns" in d:
                    comment += f"> {d['columns']}\n"
                if columns is not None:
                    cols = ",".join(columns)
                    comment += f"> {cols}\n"

            comment += "\n"

            ffile.write(comment)

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
