import glob
import os
import IPython


from .data_parser import DataParser
from ..core.tools import abspath

datacategories = [
    dict(label="Economics", tag="Economics"),
    dict(label="Predictive maintenance", tag="Predictive_Maintenance"),
    dict(label="Computing", tag="Computing"),
    dict(label="Physics", tag="Physics"),
    dict(label="Health", tag="Health"),
    dict(label="Climate Evolution", tag="Climate_Evolution"),
    dict(label="Machine learning data", tag="Machine_learning"),
]


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


def get_header_links(filename, licence=True, github=True, sagemaker=True, kaggle=False, vstudio=True, jupyter=False):
    afilename = f"guydegnol/bulkhours/blob/main/{filename}"
    links = f"[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/{afilename}) "

    if github:
        links += f"[![GitHub](https://badgen.net/badge/icon/Open%20in%20Github?icon=github&label)](https://github.com/{afilename}) "

    if sagemaker:
        links += f"[![Open in AWS Studio](https://studiolab.sagemaker.aws/studiolab.svg)](https://studiolab.sagemaker.aws/import/github/{afilename}) "

    if vstudio:
        links += f"[![Open in Visual Studio Code](https://img.shields.io/static/v1?logo=visualstudiocode&label=&message=Open%20in%20Visual%20Studio&labelColor=2c2c32&color=007acc&logoColor=007acc)](https://vscode.dev/github/{afilename}) "

    if kaggle:
        links += f"[![Open In Kaggle](https://kaggle.com/static/images/open-in-kaggle.svg)](https://kaggle.com/kernels/welcome?src=https://github.com/{afilename}) "

    if jupyter:
        links += f"[![Open In Jupyter](https://img.shields.io/static/v1?logo=jupyter&label=&message=Open%20in%20Jupyter&labelColor=636363&color=007acc&logoColor=F37726)](http://jupyter.localhost/notebooks/web/bulkhours/notebooks/{filename}) "

    if licence:
        links += f"[![CC-by-nc-sa license](https://badgen.net/badge/icon/CC%20by-nc-sa?label=Licence)](https://creativecommons.org/licenses/by-nc-sa/4.0) "

    return links + "\n"


def generate_header_links(filename, **kwargs):
    IPython.display.display(IPython.display.Markdown(get_header_links(filename, **kwargs)))


def build_readme(category=None, load_data=True, save_datasets=True, save_examples=True):
    examples = sorted(glob.glob(abspath("examples/*")))

    if save_examples:
        with open(f"/home/guydegnol/projects/bulkhours/examples/README.md", "w") as ff:
            ff.write("""Here is the list of the examples:\n\n""")
            for example in examples:
                if ".ipynb" in example or ".md" in example:
                    example_label = example.split("/")[-1].split(".")[0]
                    filename = "examples/" + example.split("/")[-1]
                    line = f"- [**`{example_label}`**](https://github.com/guydegnol/bulkhours/blob/main/{filename}) "
                    if ".ipynb" in example:
                        line += get_header_links(filename, licence=False, github=False)
                    ff.write(line + "\n")

        os.system(
            f"cp -r /home/guydegnol/projects/bulkhours/data/README.md /home/guydegnol/projects/bulkhours.wiki/data.md"
        )

    from ..phyu.constants import Units

    DataParser.build_clean_datasets()
    if category is not None:
        readme = ""
        for c, lcategory in enumerate(datacategories):
            if not (lcategory["label"] == category or lcategory["tag"] == category):
                continue

            readme += f'\n\n## {lcategory["tag"]} \n\n'

            if lcategory["label"] == "Physics":
                readme += Units().info(size="+1", code=True)

            for k, d in DataParser.clean_datasets.items():
                if d["category"] == lcategory["tag"]:
                    readme += DataParser(**d).get_info(load_columns=load_data)

        return readme

    if save_datasets:
        ffile = open(get_readme_filename(), "w")
        ffile.write("# Data\n\n")

        for c, category in enumerate(datacategories):
            ffile.write(f'- [{c+1}. {category["label"]}](#{category["tag"]}) \n')

        for c, category in enumerate(datacategories):
            ffile.write(f'\n\n## {category["tag"]} \n\n')

            if category["label"] == "Physics":
                ffile.write(Units().info(size="+1", code=True))

            for k, d in DataParser.clean_datasets.items():
                if d["category"] == category["tag"]:
                    ffile.write(DataParser(**d).get_info(load_columns=load_data))

        raw_files = set()
        for k, d in DataParser.clean_datasets.items():
            if "raw_data" in d and type(d["raw_data"]) == str:
                raw_files.add(d["raw_data"])

        dfiles = [f.split("/")[-1] for f in glob.glob(get_readme_filename("*"))]
        for f in dfiles:
            if f not in raw_files:
                print(f"{f}: data is not referenced")


def help(category=None, load_data=True, show_categories=False, save_datasets=True):
    if show_categories:
        import pandas as pd

        IPython.display.display(pd.DataFrame(datacategories))

    elif category is not None:
        readme = build_readme(category=category, load_data=False, save_examples=False, save_datasets=save_datasets)
        IPython.display.display(IPython.display.Markdown(readme))
    else:
        build_readme(category=category, load_data=load_data, save_datasets=save_datasets)

        readme = open(get_readme_filename()).readlines()
        IPython.display.display(IPython.display.Markdown("\n".join(readme)))
