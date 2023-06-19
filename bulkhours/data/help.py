import glob

from .datasets import datasets, datacategories


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
    ffile = open("/home/guydegnol/projects/bulkhours/data/README.md", "w")
    ffile.write('# Data<a name="data"></a>\n\n')

    for c, category in enumerate(datacategories):
        ffile.write(f'{c+1}. [{category["label"]}](#{category["tag"]})\n')

    for c, category in enumerate(datacategories):
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

    dfiles = [f.split("/")[-1] for f in glob.glob("/home/guydegnol/projects/bulkhours/data/*")]
    for f in dfiles:
        if f not in raw_files:
            print(f"{f}: data is not referenced")


def help():
    import IPython

    IPython.display.display(
        IPython.display.Markdown(
            """
#### `bulkhours.get_data("supercomputers")`
The file has been downloaded from the page https://ourworldindata.org/grapher/supercomputer-power-flops

#### `bulkhours.get_data("life_expectancy_vs_gdp_2018")`
The file has been downloaded from the page https://ourworldindata.org/grapher/life-expectancy-vs-gdp-per-capita
Source: Maddison Project Database (2020); UN WPP (2022); Zijdeman et al. (2015)

#### `bulkhours.get_data("france.retraites")`
The file has been downloaded from the page https://www.insee.fr/fr/statistiques/2415121#tableau-figure1

#### `bulkhours.get_data("france.income")`
Distribution des salaires mensuels nets en équivalent temps plein (EQTP) en 2020
The file has been downloaded from the page https://www.insee.fr/fr/statistiques/6436313#tableau-figure2

#### `bulkhours.get_data("france.salaires")`
The file has been downloaded from the page https://www.insee.fr/fr/statistiques/6436313#tableau-figure2

#### `data/world_gdp_hist.csv`
"Data Source","World Development Indicators", "Last Updated Date","2022-12-22",

#### `bulkhours.get_data("co2.main")` `bulkhours.get_data("co2.mapmain")`
Data on CO2 and Greenhouse Gas Emissions by Our World in Data
- https://github.com/owid/co2-data/blob/master/owid-co2-codebook.csv
- Data source: https://raw.githubusercontent.com/owid/co2-data/master/owid-co2-data.csv

#### `bulkhours.get_data("co2.concentrations")` or `bulkhours.get_data("co2.mapconcentrations")`
Data concentrations
- Data source: https://ourworldindata.org/atmospheric-concentrations

#### https://www.statsmodels.org/stable/index.html data
- Australian passengers: bulkhours.get_data("statsdata.air_passengers")
- bulkhours.get_data("statsdata.air")
- bulkhours.get_data("statsdata.aust")
- bulkhours.get_data("statsdata.livestock2")

#### https://www.cor-retraites.fr/
- bulkhours/data/demo-pop-pyram.xlsx
- bulkhours/data/Données septembre partie 1.xlsx
- bulkhours/data/Données_RA2022_P2.xlsx
- bulkhours/data/Données_RA2022_P4.xlsx
- bulkhours/data/Données septembre 2022 - partie 3.xlsx
- bulkhours/data/Données septembre 2022 - partie 5.xlsx
- bulkhours/data/Données complémentaires partie 2 RA 2022.xlsx

#### Other data
- bulkhours.get_data("world.macro")
- bulkhours.get_data("world.mappoverty")
- bulkhours.get_data("world.corruption")
- bulkhours.get_data("gmacro.us_gdp")
- bulkhours.get_data("gmacro.fr_gdp")
- bulkhours.get_data("wages")
- bulkhours.get_data("mincer.params") 
    """
        )
    )
