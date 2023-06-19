import glob
import os

from .datasets import datasets, datacategories


def get_readme_filename(filename="README.md"):
    return os.path.abspath(os.path.dirname(__file__) + f"../../../data/{filename}")


def get_rdata(d, dname, dlabel):
    if dname not in d:
        return ""
    if "http" in d[dname]:
        label = d[dname].split("/")[-1]
        address = d[dname].replace("raw.githubusercontent.com", "github.com")
        return f"- {dlabel}: [{label}]({address})\n"
    if type(d[dname]) in [list]:
        return ""
    return f"- {dlabel}: [{d[dname]}](https://github.com/guydegnol/bulkhours/blob/main/data/{d[dname]})\n"


def build_readme():
    ffile = open(get_readme_filename(), "w")
    ffile.write("#Data\n\n")

    for c, category in enumerate(datacategories):
        ffile.write(f'{c+1}. [{category["label"]}](#{category["tag"]})\n')
        ffile.write(f'{c+1} [{category["label"]}](#getting-started-with-markdown)\n')

    for c, category in enumerate(datacategories):
        ffile.write(
            f'\n\n### [{c+1}. {category["label"]}](https://github.com/guydegnol/bulkhours/blob/main/data/README.md#{category["tag"]})\n\n'
        )
        ffile.write(f'\n\n### {c+1}. {category["label"]}\n\n')
        ffile.write(f'\n\n### {c+1}. {category["label"]}<a name="{category["tag"]}"></a>\n\n')

        for d in datasets:
            if d["category"] != category["label"]:
                continue
            rdata = get_rdata(d, "raw_data", "Raw data")
            edata = get_rdata(d, "enrich_data", "Rich data")
            comment = f"""#### `bulkhours.get_data("{d["label"]}")`
{rdata}{edata}{d["source"]}\n"""
            # print(d["label"])  # , comment)
            # bulkhours.get_data(d["label"])
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
