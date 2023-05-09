def data_help():
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
