import glob
import os

from .datasets import datasets, datacategories


def get_readme_filename(filename="README.md"):
    return os.path.abspath(os.path.dirname(__file__) + f"../../../data/{filename}")


def get_rdata(d, dname):
    if dname not in d:
        return ""
    if "http" in d[dname]:
        label = d[dname].split("/")[-1]
        address = d[dname].replace("raw.githubusercontent.com", "github.com")
        return f"[{label}]({address})"
    if type(d[dname]) in [list]:
        return ", ".join([f"[{f}](https://github.com/guydegnol/bulkhours/blob/main/data/{f})" for f in d[dname]])
    return f"[{d[dname]}](https://github.com/guydegnol/bulkhours/blob/main/data/{d[dname]})"


def build_readme():
    ffile = open(get_readme_filename(), "w")
    ffile.write("# Data\n\n")

    from ..phyu.constants import Units

    for c, category in enumerate(datacategories):
        ffile.write(f'- [{c+1}. {category["label"]}](#{category["tag"]}) \n')

    for c, category in enumerate(datacategories):
        # ffile.write(f'\n\n### [{c+1}. {category["label"]}](#{category["tag"]})\n\n')
        # ffile.write(f'\n\n### {c+1}. {category["label"]} <a name="{category["tag"]}"></a> \n\n')
        # ffile.write(f'\n\n### {category["tag"]} <a name="{category["tag"]}"></a> \n\n')
        ffile.write(f'\n\n### {category["tag"]} \n\n')

        if category["label"] == "Physics":
            ffile.write(Units().info(size="+1", code=True))

        for d in datasets:
            if d["category"] != category["tag"]:
                continue

            comment = ""
            if "summary" in d:
                comment += f"### {d['summary']}\n"
            comment += f'#### `bulkhours.get_data("{d["label"]}")`\n'
            if "raw_data" in d:
                comment += f"- Raw data {get_rdata(d, 'raw_data')}\n"
            if "enrich_data" in d:
                comment += f"- Enrich data: {get_rdata(d, 'enrich_data')}\n"
            if "source" in d:
                comment += d["source"] + "\n"
            if "ref_source" in d:
                comment += f"- Direct source: {d['ref_source']}\n"
            if "columns" in d:
                comment += f"> Columns: {d['columns']}\n"

            comment += "\n"

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
