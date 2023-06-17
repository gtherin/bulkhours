# Data<a name="data"></a>

1. [Economics](#Economics)
2. [Predictive maintenance](#maintenance)
3. [Computing](#Computing)
4. [Physics](#Physics)
5. [Health](#Health)
6. [Climate Evolution](#Climate)
7. [Other Machine learning training data](#IA)


### Economics<a name="Economics"></a>

world_data = bulkhours.get_data("world.mappoverty", credit=True, timeopt="last")

AirPassengers.csv
APPLE_DownloadFPrepStatementQuarter.tsv
chomage_france.csv


#### `bulkhours.get_data("poverty")`
World Bank Poverty and Inequality Platform
- Data File: https://nyc3.digitaloceanspaces.com/owid-public/data/poverty/pip_dataset.csv
- Direct source: https://ourworldindata.org/poverty
- Data source: https://pip.worldbank.org/
- Info columns: https://github.com/owid/poverty-data/blob/main/datasets/pip_codebook.csv

#### `bulkhours.get_data("supercomputers")`

    "scipy_distributions_list": dict(drop=get_scipy_distributions_list),
    "macro": dict(
        raw_data=[
            "corruption.csv",
            "cost_of_living.csv",
            "richest_countries.csv",
            "unemployment.csv",
            "tourism.csv",
            "continent.tsv",
        ],
        on="country",
    ),
    "life_expectancy_vs_gdp_2018": dict(
        raw_data=["life-expectancy-vs-gdp-per-capita.csv"],
        info="GDP per capita is measured in 2011 international dollars, which corrects for inflation and cross-country price differences",
        source="""Life expectancy versus GDP/capita per country
- Direct source: https://ourworldindata.org/grapher/life-expectancy-vs-gdp-per-capita
- Data source: Maddison Project Database (2020); UN WPP (2022); Zijdeman et al. (2015)
- Info columns: GDP per capita is measured in 2011 international dollars, which corrects for inflation and cross-country price differences
        """,
        filter=clean_life_expectancy_vs_gdp_2018,
        rename=[
            "Country",
            "Code",
            "Year",
            "Life expectancy (years)",
            "GDP per capita ($)",
            "annotations",
            "Population",
            "Continent",
        ],
        drop=["annotations", "Continent"],
    ),
}



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
- bulkhours.get_data("world.corruption")
- bulkhours.get_data("gmacro.us_gdp")
- bulkhours.get_data("gmacro.fr_gdp")
- bulkhours.get_data("wages")
- bulkhours.get_data("mincer.params") 

continent.tsv
corruption.csv
cost_of_living.csv
'Données complémentaires partie 2 RA 2022.xlsx'
Données_RA2022_P2.xlsx
Données_RA2022_P4.xlsx
'Données septembre 2022 - partie 3.xlsx'
'Données septembre 2022 - partie 5.xlsx'
'Données septembre partie 1.xlsx'

ffcontrol.csv
freefight.csv
in_trading.csv

france_pyramide.csv
fundamentals.csv
life-expectancy-vs-gdp-per-capita.csv

prices-split-adjusted.csv
richest_countries.csv
securities.csv
tourism.csv
unemployment.csv
wages.tsv
world_gdp_hist.csv


### Predictive maintenance<a name="maintenance"></a>


#### `bulkhours.get_data("maintenance1")`<a name="maintenance1"></a>
https://raw.githubusercontent.com/shadgriffin/machine_failure/master/equipment_failure_data_1.csv
https://raw.githubusercontent.com/shadgriffin/machine_failure/master/equipment_failure_data_2.csv
https://github.com/shadgriffin/feature_engineering_equipment_failure/blob/main/Feature%20Engineering%20for%20Equipment%20Failure%20Problems.ipynb
https://github.com/shadgriffin/machine_failure/blob/master/Machine%20Learning%20for%20%20Equipment%20Maintenance%20-%20Pub.ipynb
https://medium.com/swlh/machine-learning-for-equipment-failure-prediction-and-predictive-maintenance-pm-e72b1ce42da1


Metadata explaining all of the fields in the data set.
| Field | Description |
| -------- | ------- |
|ID | field that represents a specific machine.|
|DATE | The date of the observation.|
|REGION_CLUSTER | a field that represents the region in which the machine resides.|
|MAINTENANCE_VENDOR | a field that represents the company that provides maintenance and service to the machine.|
|MANUFACTURER | the company that manufactured the equipment in question.|
|WELL_GROUP | a field representing the type of machine.|
|EQUIPMENT_AGE | Age of the machine, in days.|
|S15, S17, S13, S16, S19, S18, S8 | Sensors Values.|
|EQUIPMENT_FAILURE | A ‘1’ means that the equipment failed. A ‘0’ means the equipment did not fail.|

Our first goal in this exercise is to build a model that predicts equipment failure. In other words, we will use the other variables in the data frame to predict EQUIPMENT_FAILURE.


#### `bulkhours.get_data("oil_leakage")`
https://www.kaggle.com/c/equipfails/data
https://github.com/williamhuybui/Oil-Gas-Leakage-Analysis-and-Equipment-Failure-Detection/tree/master
https://towardsdatascience.com/rolling-in-the-deep-589f3460960f
https://github.com/sanjeev21095/TAMU-Datathon/blob/master/Team_friyay_Final_submission.ipynb
https://www.kaggle.com/competitions/equipfails/code
https://github.com/shadgriffin/feature_engineering_equipment_failure/blob/main/Feature%20Engineering%20for%20Equipment%20Failure%20Problems.ipynb
https://medium.com/swlh/machine-learning-for-equipment-failure-prediction-and-predictive-maintenance-pm-e72b1ce42da1


https://raw.githubusercontent.com/williamhuybui/Oil-Gas-Leakage-Analysis-and-Equipment-Failure-Detection/master/equipfails/equip_failures_test_set.csv
https://raw.githubusercontent.com/williamhuybui/Oil-Gas-Leakage-Analysis-and-Equipment-Failure-Detection/master/equipfails/equip_failures_training_set.csv


### Computing<a name="Computing"></a>

#### `bulkhours.get_data("supercomputers")`
Computational capacity of the fastest supercomputers
- Data File: https://raw.githubusercontent.com/owid/owid-datasets/dd7a4ecbb249f98028e25c304ef7d68de8979ea9/datasets/Supercomputer%20power%20(FLOPS)%20%E2%80%93%20TOP500%20Database/Supercomputer%20power%20(FLOPS)%20%E2%80%93%20TOP500%20Database.csv
- Direct source: https://ourworldindata.org/grapher/supercomputer-power-flops
- Info columns: The number of floating-point operations per second (GigaFLOPS) by the fastest supercomputer in any given year


### Physics<a name="Physics"></a>

sun_data = bulkhours.get_data("statsdata.sunspots", credit=True)["ssn"]

from bulkhours import constants as bkc

planetes = bkc.DataFrame(index=["mercure", "venus", "terre", "mars"], columns=["Albedo", "d_ua", "T_C"])
bkc.print(r"Equilibre thermique: $(1-A)\frac{ L_\odot R^2}{4 d^2} \equiv (1-S) 4 \pi R^2 \sigma T^4$", size="+1")
planetes["T_C/no atmo."] = (((1-planetes.Albedo) * bkc.L_soleil / (16 * np.pi * (planetes.d_ua * bkc.d_terresoleil)**2 * bkc.sigma))**0.25-bkc.c2k).round()
planetes["Effet de serre"] = (1-( (1 - planetes.Albedo) * bkc.L_soleil / (planetes.T_C + bkc.c2k)**4 / (16 * bkc.pi * (planetes.d_ua * bkc.d_terresoleil)**2 * bkc.sigma))).round(3)

bkc.print(r"Forcage radiatif: $F = S\cdot \sigma \cdot T^4$", size="+1")
planetes["Forcage radiatif (W/m2)"] = (planetes["Effet de serre"] * bkc.sigma * (planetes.T_C + bkc.c2k)**4).round(3)
display(planetes)

# Affichage des propriétés de la terre (pour cc(CO2)=280ppm)
# bkc.help("Terre", code=False, size=1)



### Health<a name="Health"></a>

#### `bulkhours.get_data("vaccinations")`<a name="vaccinations"></a>
Coronavirus Pandemic (COVID-19) data
- Data File: https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/vaccinations/vaccinations.csv
- Direct source: https://ourworldindata.org/coronavirus
- Data source: https://covid19.who.int/data
- Info columns: https://github.com/owid/covid-19-data/tree/master/public/data/

covid = bulkhours.get_data("covid", credit=True, query="iso_code in ('FRA')", index="date")['new_cases']

prostate.tsv



### Climate Evolution<a name="Climate"></a>

#### `bulkhours.get_data("co2.main")` `bulkhours.get_data("co2.mapmain")`
Data on CO2 and Greenhouse Gas Emissions by Our World in Data
- https://github.com/owid/co2-data/blob/master/owid-co2-codebook.csv
- Data source: https://raw.githubusercontent.com/owid/co2-data/master/owid-co2-data.csv

#### `bulkhours.get_data("co2.concentrations")` or `bulkhours.get_data("co2.mapconcentrations")`
Data concentrations
- Data source: https://ourworldindata.org/atmospheric-concentrations


img = bulkhours.get_data("chose1.jpg")
carbon-footprint-travel-mode.csv


### Other Machine learning training data<a name="IA"></a>


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

climate-change.csv


# Get and format image
img = bulkhours.get_data("chose1.jpg")
img = bulkhours.get_data("chose2.jpg")

test_catvnoncat.h5
train_catvnoncat.h5


galton.jpg
galtonr.png
gradient_descent.png
lognormal.png
radian2.png
README.md
TCL.png

### Data concentrations
    - Data File: bulkhours://climate-change.csv
    - Data source: https://ourworldindata.org/atmospheric-concentrations