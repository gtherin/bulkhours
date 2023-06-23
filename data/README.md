# Data

- [1. Economics](#Economics) 
- [2. Predictive maintenance](#Predictive_Maintenance) 
- [3. Computing](#Computing) 
- [4. Physics](#Physics) 
- [5. Health](#Health) 
- [6. Climate Evolution](#Climate_Evolution) 
- [7. Machine learning data](#Machine_learning) 


## Economics 

#### World Bank Poverty and Inequality data
#### `bulkhours.get_data("world.poverty")`
- Raw data: [pip_dataset.csv](https://nyc3.digitaloceanspaces.com/owid-public/data/poverty/pip_dataset.csv)  ([raw](https://nyc3.digitaloceanspaces.com/owid-public/data/poverty/pip_dataset.csv))
- Enrich data: [world.py](https://github.com/guydegnol/bulkhours/blob/main/bulkhours/data/world.py)  ([raw](https://raw.githubusercontent.com/guydegnol/bulkhours/main/bulkhours/data/world.py))
- Direct source: https://ourworldindata.org/poverty
- Reference site: https://pip.worldbank.org/
- Columns:
> https://github.com/owid/poverty-data/blob/main/datasets/pip_codebook.csv

#### World Bank Poverty and Inequality data (with gpx extra info)
#### `bulkhours.get_data("world.mappoverty")`
- Raw data: [pip_dataset.csv](https://nyc3.digitaloceanspaces.com/owid-public/data/poverty/pip_dataset.csv)  ([raw](https://nyc3.digitaloceanspaces.com/owid-public/data/poverty/pip_dataset.csv))
- Enrich data: [world.py](https://github.com/guydegnol/bulkhours/blob/main/bulkhours/data/world.py)  ([raw](https://raw.githubusercontent.com/guydegnol/bulkhours/main/bulkhours/data/world.py))
- Direct source: https://ourworldindata.org/poverty
- Reference site: https://pip.worldbank.org/
- Columns:
> https://github.com/owid/poverty-data/blob/main/datasets/pip_codebook.csv

#### World Bank Gdp data
#### `bulkhours.get_data("world.gdp")`
- Raw data: [pip_dataset.csv](https://nyc3.digitaloceanspaces.com/owid-public/data/poverty/pip_dataset.csv)  ([raw](https://nyc3.digitaloceanspaces.com/owid-public/data/poverty/pip_dataset.csv))
- Enrich data: [world.py](https://github.com/guydegnol/bulkhours/blob/main/bulkhours/data/world.py)  ([raw](https://raw.githubusercontent.com/guydegnol/bulkhours/main/bulkhours/data/world.py))
- Direct source: https://ourworldindata.org/poverty
- Reference site: https://pip.worldbank.org/
- Columns:
> https://github.com/owid/poverty-data/blob/main/datasets/pip_codebook.csv

#### World Bank Gdp data (with gpx extra info)
#### `bulkhours.get_data("world.mapgdp")`
- Raw data: [pip_dataset.csv](https://nyc3.digitaloceanspaces.com/owid-public/data/poverty/pip_dataset.csv)  ([raw](https://nyc3.digitaloceanspaces.com/owid-public/data/poverty/pip_dataset.csv))
- Enrich data: [world.py](https://github.com/guydegnol/bulkhours/blob/main/bulkhours/data/world.py)  ([raw](https://raw.githubusercontent.com/guydegnol/bulkhours/main/bulkhours/data/world.py))
- Direct source: https://ourworldindata.org/poverty
- Reference site: https://pip.worldbank.org/
- Columns:
> https://github.com/owid/poverty-data/blob/main/datasets/pip_codebook.csv

#### Global economic data
#### `bulkhours.get_data("world.macro")`
- Raw data: [corruption.csv](https://github.com/guydegnol/bulkhours/blob/main/data/corruption.csv), [cost_of_living.csv](https://github.com/guydegnol/bulkhours/blob/main/data/cost_of_living.csv), [richest_countries.csv](https://github.com/guydegnol/bulkhours/blob/main/data/richest_countries.csv), [unemployment.csv](https://github.com/guydegnol/bulkhours/blob/main/data/unemployment.csv), [tourism.csv](https://github.com/guydegnol/bulkhours/blob/main/data/tourism.csv), [continent.tsv](https://github.com/guydegnol/bulkhours/blob/main/data/continent.tsv)
- Enrich data: [world.py](https://github.com/guydegnol/bulkhours/blob/main/bulkhours/data/world.py)  ([raw](https://raw.githubusercontent.com/guydegnol/bulkhours/main/bulkhours/data/world.py))

#### Global economic data (with gpx extra info)
#### `bulkhours.get_data("world.mapmacro")`
- Raw data: [corruption.csv](https://github.com/guydegnol/bulkhours/blob/main/data/corruption.csv), [cost_of_living.csv](https://github.com/guydegnol/bulkhours/blob/main/data/cost_of_living.csv), [richest_countries.csv](https://github.com/guydegnol/bulkhours/blob/main/data/richest_countries.csv), [unemployment.csv](https://github.com/guydegnol/bulkhours/blob/main/data/unemployment.csv), [tourism.csv](https://github.com/guydegnol/bulkhours/blob/main/data/tourism.csv), [continent.tsv](https://github.com/guydegnol/bulkhours/blob/main/data/continent.tsv)
- Enrich data: [world.py](https://github.com/guydegnol/bulkhours/blob/main/bulkhours/data/world.py)  ([raw](https://raw.githubusercontent.com/guydegnol/bulkhours/main/bulkhours/data/world.py))

#### Life expectancy versus GDP/capita per country
#### `bulkhours.get_data("world.life_expectancy_vs_gdp_2018")`
- Raw data: [life-expectancy-vs-gdp-per-capita.csv](https://github.com/guydegnol/bulkhours/blob/main/data/life-expectancy-vs-gdp-per-capita.csv)
- Enrich data: [world.py](https://github.com/guydegnol/bulkhours/blob/main/bulkhours/data/world.py)  ([raw](https://raw.githubusercontent.com/guydegnol/bulkhours/main/bulkhours/data/world.py))
- Direct source: https://ourworldindata.org/grapher/life-expectancy-vs-gdp-per-capita
- Reference site: Maddison Project Database (2020); UN WPP (2022); Zijdeman et al. (2015)

#### Descriptive statistics of hourly wages in selected EU countries in 2010 (in PPS)
#### `bulkhours.get_data("mincer.stats")`
- Direct source: https://www.nbp.pl/publikacje/materialy_i_studia/226_en.pdf (table 2)

#### Mincer equation parameters per country
#### `bulkhours.get_data("mincer.params")`
- Enrich data: [mincer.py](https://github.com/guydegnol/bulkhours/blob/main/bulkhours/data/mincer.py)  ([raw](https://raw.githubusercontent.com/guydegnol/bulkhours/main/bulkhours/data/mincer.py))
- Direct source: https://www.nbp.pl/publikacje/materialy_i_studia/226_en.pdf (table 3)

#### Age de la population au 1er janvier (fin novembre 2022)
#### `bulkhours.get_data("pyramide")`
- Raw data: [pyramide.tsv](https://github.com/guydegnol/bulkhours/blob/main/data/pyramide.tsv)
- Direct source: https://www.insee.fr/fr/statistiques/2381472#tableau-figure1

#### Cotisants, retraités et rapport démographique tous régimes en 2020
#### `bulkhours.get_data("france.retraites")`
- Enrich data: [france.py](https://github.com/guydegnol/bulkhours/blob/main/bulkhours/data/france.py)  ([raw](https://raw.githubusercontent.com/guydegnol/bulkhours/main/bulkhours/data/france.py))
- Direct source: https://www.insee.fr/fr/statistiques/2415121#tableau-figure1

#### Distribution des salaires mensuels nets en équivalent temps plein (EQTP) en 2020
#### `bulkhours.get_data("france.income")`
- Enrich data: [france.py](https://github.com/guydegnol/bulkhours/blob/main/bulkhours/data/france.py)  ([raw](https://raw.githubusercontent.com/guydegnol/bulkhours/main/bulkhours/data/france.py))
- Direct source: https://www.insee.fr/fr/statistiques/6436313#tableau-figure2

#### Revenu salarial et salaire en EQTP annuels moyens selon le sexe en 2019
#### `bulkhours.get_data("france.salaires")`
- Enrich data: [france.py](https://github.com/guydegnol/bulkhours/blob/main/bulkhours/data/france.py)  ([raw](https://raw.githubusercontent.com/guydegnol/bulkhours/main/bulkhours/data/france.py))
- Direct source: https://www.insee.fr/fr/statistiques/6047743?sommaire=6047805
- Columns:
> Revenu annuel Femmes moyen, Revenu annuel Hommes moyen, Revenu annuel Femmes moyen Écart relatif (en %), Salaire annuel Femmes moyen EQTP, Salaire annuel Hommes moyen EQTP, Salaire annuel Femmes moyen EQTP Écart relatif (en % EQTP)

#### Inégalités salariales entre femmes et hommes de 1995 à 2019
#### `bulkhours.get_data("france.histsalaires")`
- Enrich data: [france.py](https://github.com/guydegnol/bulkhours/blob/main/bulkhours/data/france.py)  ([raw](https://raw.githubusercontent.com/guydegnol/bulkhours/main/bulkhours/data/france.py))
- Direct source: https://www.insee.fr/fr/statistiques/6047743?sommaire=6047805
- Columns:
> colonne 1: Revenu annuel Femmes moyen
colonne 2: Revenu annuel Hommes moyen
colonne 3: Revenu annuel Femmes moyen Écart relatif (en %)
colonne 4: Salaire annuel Femmes moyen EQTP
colonne 4: Salaire annuel Hommes moyen EQTP
colonne 4: Salaire annuel Femmes moyen EQTP Écart relatif (en % EQTP)
    

#### Evolution du PIB et de ses composantes par rapport au trimestre precedent en volume en %
#### `bulkhours.get_data("gmacro.fr_qgdp")`
- Enrich data: [gmacro.py](https://github.com/guydegnol/bulkhours/blob/main/bulkhours/data/gmacro.py)  ([raw](https://raw.githubusercontent.com/guydegnol/bulkhours/main/bulkhours/data/gmacro.py))
- Direct source: https://www.insee.fr/fr/statistiques/2830547#tableau-figure1

#### Évolution du produit intérieur brut et de ses composantes
#### `bulkhours.get_data("gmacro.fr_unemployement")`
- Enrich data: [gmacro.py](https://github.com/guydegnol/bulkhours/blob/main/bulkhours/data/gmacro.py)  ([raw](https://raw.githubusercontent.com/guydegnol/bulkhours/main/bulkhours/data/gmacro.py))
- Direct source: https://www.insee.fr/fr/statistiques/2830547#tableau-figure1

#### United States Macroeconomic data
#### `bulkhours.get_data("gmacro.us_gdp")`
- Enrich data: [gmacro.py](https://github.com/guydegnol/bulkhours/blob/main/bulkhours/data/gmacro.py)  ([raw](https://raw.githubusercontent.com/guydegnol/bulkhours/main/bulkhours/data/gmacro.py))
- Direct source: https://www.statsmodels.org/0.6.1/datasets/generated/macrodata.html
- Columns:
> year      - 1959q1 - 2009q3
quarter   - 1-4
realgdp   - Real gross domestic product (Bil. of chained 2005 US$,
            seasonally adjusted annual rate)
realcons  - Real personal consumption expenditures (Bil. of chained
            2005 US$, seasonally adjusted annual rate)
realinv   - Real gross private domestic investment (Bil. of chained
            2005 US$, seasonally adjusted annual rate)
realgovt  - Real federal consumption expenditures & gross investment
            (Bil. of chained 2005 US$, seasonally adjusted annual rate)
realdpi   - Real private disposable income (Bil. of chained 2005
            US$, seasonally adjusted annual rate)
cpi       - End of the quarter consumer price index for all urban
            consumers: all items (1982-84 = 100, seasonally adjusted).
m1        - End of the quarter M1 nominal money stock (Seasonally
            adjusted)
tbilrate  - Quarterly monthly average of the monthly 3-month
            treasury bill: secondary market rate
unemp     - Seasonally adjusted unemployment rate (%)
pop       - End of the quarter total population: all ages incl. armed
            forces over seas
infl      - Inflation rate (ln(cpi_{t}/cpi_{t-1}) * 400)
realint   - Real interest rate (tbilrate - infl)
        

#### France Macroeconomic data
#### `bulkhours.get_data("gmacro.fr_gdp")`
- Enrich data: [gmacro.py](https://github.com/guydegnol/bulkhours/blob/main/bulkhours/data/gmacro.py)  ([raw](https://raw.githubusercontent.com/guydegnol/bulkhours/main/bulkhours/data/gmacro.py))

#### Scipy list of available distributions
#### `bulkhours.get_data("statsdata.scipy_distributions_list")`
- Enrich data: [statsdata.py](https://github.com/guydegnol/bulkhours/blob/main/bulkhours/data/statsdata.py)  ([raw](https://raw.githubusercontent.com/guydegnol/bulkhours/main/bulkhours/data/statsdata.py))

#### Oil production in Saudi Arabia from 1996 to 2007
#### `bulkhours.get_data("statsdata.oil")`
- Enrich data: [statsdata.py](https://github.com/guydegnol/bulkhours/blob/main/bulkhours/data/statsdata.py)  ([raw](https://raw.githubusercontent.com/guydegnol/bulkhours/main/bulkhours/data/statsdata.py))
- Direct source: https://www.statsmodels.org/stable/index.html

#### Air pollution data
#### `bulkhours.get_data("statsdata.air")`
- Enrich data: [statsdata.py](https://github.com/guydegnol/bulkhours/blob/main/bulkhours/data/statsdata.py)  ([raw](https://raw.githubusercontent.com/guydegnol/bulkhours/main/bulkhours/data/statsdata.py))
- Direct source: https://www.statsmodels.org/stable/index.html

#### Forecasting livestock, sheep in Asia: comparing forecasting performance of non-seasonal methods.
#### `bulkhours.get_data("statsdata.livestock2")`
- Enrich data: [statsdata.py](https://github.com/guydegnol/bulkhours/blob/main/bulkhours/data/statsdata.py)  ([raw](https://raw.githubusercontent.com/guydegnol/bulkhours/main/bulkhours/data/statsdata.py))
- Direct source: https://www.statsmodels.org/stable/index.html

#### Forecasting livestock, sheep in Asia: comparing forecasting performance of non-seasonal methods. (3)
#### `bulkhours.get_data("statsdata.livestock3")`
- Enrich data: [statsdata.py](https://github.com/guydegnol/bulkhours/blob/main/bulkhours/data/statsdata.py)  ([raw](https://raw.githubusercontent.com/guydegnol/bulkhours/main/bulkhours/data/statsdata.py))
- Direct source: https://www.statsmodels.org/stable/index.html

#### International visitor night in Australia (millions) < 2005
#### `bulkhours.get_data("statsdata.aust")`
- Enrich data: [statsdata.py](https://github.com/guydegnol/bulkhours/blob/main/bulkhours/data/statsdata.py)  ([raw](https://raw.githubusercontent.com/guydegnol/bulkhours/main/bulkhours/data/statsdata.py))

#### International visitor night in Australia (millions) > 2005
#### `bulkhours.get_data("statsdata.air_passengers")`
- Raw data: [AirPassengers.csv](https://github.com/guydegnol/bulkhours/blob/main/data/AirPassengers.csv)
- Enrich data: [statsdata.py](https://github.com/guydegnol/bulkhours/blob/main/bulkhours/data/statsdata.py)  ([raw](https://raw.githubusercontent.com/guydegnol/bulkhours/main/bulkhours/data/statsdata.py))

#### All-Transactions House Price Index for Houston
#### `bulkhours.get_data("statsdata.hhousing")`
- Enrich data: [statsdata.py](https://github.com/guydegnol/bulkhours/blob/main/bulkhours/data/statsdata.py)  ([raw](https://raw.githubusercontent.com/guydegnol/bulkhours/main/bulkhours/data/statsdata.py))
- Direct source: https://fred.stlouisfed.org/series/ATNHPIUS26420Q

#### Market prices of SP500 stocks
#### `bulkhours.get_data("prices-split-adjusted")`
- Raw data: [prices-split-adjusted.csv](https://github.com/kyi3081/stock-analysis/master/prices-split-adjusted.csv)  ([raw](https://raw.githubusercontent.com/kyi3081/stock-analysis/master/prices-split-adjusted.csv))
- Direct source: https://github.com/kyi3081/stock-analysis

#### Market fundamentals of SP500 stocks
#### `bulkhours.get_data("fundamentals")`
- Raw data: [fundamentals.csv](https://github.com/kyi3081/stock-analysis/master/fundamentals.csv)  ([raw](https://raw.githubusercontent.com/kyi3081/stock-analysis/master/fundamentals.csv))
- Direct source: https://github.com/kyi3081/stock-analysis

#### Stocks information for SP500
#### `bulkhours.get_data("securities")`
- Raw data: [securities.csv](https://github.com/kyi3081/stock-analysis/master/securities.csv)  ([raw](https://raw.githubusercontent.com/kyi3081/stock-analysis/master/securities.csv))
- Direct source: https://github.com/kyi3081/stock-analysis

#### Statement of Apple stock (Quarterly)
#### `bulkhours.get_data("trading.apple")`
- Raw data: [APPLE_DownloadFPrepStatementQuarter.tsv](https://github.com/guydegnol/bulkhours/blob/main/data/APPLE_DownloadFPrepStatementQuarter.tsv)
- Enrich data: [trading.py](https://github.com/guydegnol/bulkhours/blob/main/bulkhours/data/trading.py)  ([raw](https://raw.githubusercontent.com/guydegnol/bulkhours/main/bulkhours/data/trading.py))

#### Standardized country information (iso m49)
#### `bulkhours.get_data("continent")`
- Raw data: [continent.tsv](https://github.com/guydegnol/bulkhours/blob/main/data/continent.tsv)

#### Corruption index per country
#### `bulkhours.get_data("corruption")`
- Raw data: [corruption.csv](https://github.com/guydegnol/bulkhours/blob/main/data/corruption.csv)

#### Cost of living
#### `bulkhours.get_data("cost_of_living")`
- Raw data: [cost_of_living.csv](https://github.com/guydegnol/bulkhours/blob/main/data/cost_of_living.csv)
- Columns:
> country,cost_index,monthly_income,purchasing_power_index

#### GDP per capita per country
#### `bulkhours.get_data("richest_countries")`
- Raw data: [richest_countries.csv](https://github.com/guydegnol/bulkhours/blob/main/data/richest_countries.csv)
- Columns:
> country,gdp_per_capita

#### Tourism information per country
#### `bulkhours.get_data("tourism")`
- Raw data: [tourism.csv](https://github.com/guydegnol/bulkhours/blob/main/data/tourism.csv)
- Columns:
> country,gdp_per_capita

#### Unemployemnt rates per country
#### `bulkhours.get_data("unemployment")`
- Raw data: [unemployment.csv](https://github.com/guydegnol/bulkhours/blob/main/data/unemployment.csv)
- Columns:
> country,gdp_per_capita

#### Simple synthetic data for exercice
#### `bulkhours.get_data("wages")`
- Raw data: [wages.tsv](https://github.com/guydegnol/bulkhours/blob/main/data/wages.tsv)

#### COR data
#### `bulkhours.get_data("COR_1")`
- Raw data: [Données septembre partie 1.xlsx](https://github.com/guydegnol/bulkhours/blob/main/data/Données septembre partie 1.xlsx)

#### COR data
#### `bulkhours.get_data("COR_2")`
- Raw data: [Données_RA2022_P2.xlsx](https://github.com/guydegnol/bulkhours/blob/main/data/Données_RA2022_P2.xlsx)

#### COR data
#### `bulkhours.get_data("COR_2bis")`
- Raw data: [Données complémentaires partie 2 RA 2022.xlsx](https://github.com/guydegnol/bulkhours/blob/main/data/Données complémentaires partie 2 RA 2022.xlsx)

#### COR data
#### `bulkhours.get_data("COR_3")`
- Raw data: [Données septembre 2022 - partie 3.xlsx](https://github.com/guydegnol/bulkhours/blob/main/data/Données septembre 2022 - partie 3.xlsx)

#### COR data
#### `bulkhours.get_data("COR_4")`
- Raw data: [Données_RA2022_P4.xlsx](https://github.com/guydegnol/bulkhours/blob/main/data/Données_RA2022_P4.xlsx)

#### COR data
#### `bulkhours.get_data("COR_5")`
- Raw data: [Données septembre 2022 - partie 5.xlsx](https://github.com/guydegnol/bulkhours/blob/main/data/Données septembre 2022 - partie 5.xlsx)



## Predictive_Maintenance 

#### Synthetic data for machine failure data (1)
#### `bulkhours.get_data("maintenance1")`
- Raw data: [fe_equipment_failure_data_1.csv](https://github.com/shadgriffin/feature_engineering_equipment_failure/main/fe_equipment_failure_data_1.csv)  ([raw](https://raw.githubusercontent.com/shadgriffin/feature_engineering_equipment_failure/main/fe_equipment_failure_data_1.csv))

#### Synthetic data for machine failure data (2)
#### `bulkhours.get_data("maintenance2")`
- Raw data: [fe_equipment_failure_data_2.csv](https://github.com/shadgriffin/feature_engineering_equipment_failure/main/fe_equipment_failure_data_2.csv)  ([raw](https://raw.githubusercontent.com/shadgriffin/feature_engineering_equipment_failure/main/fe_equipment_failure_data_2.csv))

#### Synthetic data for machine failure data (3)
#### `bulkhours.get_data("maintenance3")`
- Raw data: [equipment_failure_data_1.csv](https://github.com/shadgriffin/machine_failure/master/equipment_failure_data_1.csv)  ([raw](https://raw.githubusercontent.com/shadgriffin/machine_failure/master/equipment_failure_data_1.csv))

#### Synthetic data for machine failure data (4)
#### `bulkhours.get_data("maintenance4")`
- Raw data: [equipment_failure_data_2.csv](https://github.com/shadgriffin/machine_failure/master/equipment_failure_data_2.csv)  ([raw](https://raw.githubusercontent.com/shadgriffin/machine_failure/master/equipment_failure_data_2.csv))



## Computing 

#### Computational capacity of the fastest supercomputers
#### `bulkhours.get_data("supercomputers")`
- Raw data: [Supercomputer%20power%20(FLOPS)%20%E2%80%93%20TOP500%20Database.csv](https://github.com/owid/owid-datasets/dd7a4ecbb249f98028e25c304ef7d68de8979ea9/datasets/Supercomputer%20power%20(FLOPS)%20%E2%80%93%20TOP500%20Database/Supercomputer%20power%20(FLOPS)%20%E2%80%93%20TOP500%20Database.csv)  ([raw](https://raw.githubusercontent.com/owid/owid-datasets/dd7a4ecbb249f98028e25c304ef7d68de8979ea9/datasets/Supercomputer%20power%20(FLOPS)%20%E2%80%93%20TOP500%20Database/Supercomputer%20power%20(FLOPS)%20%E2%80%93%20TOP500%20Database.csv))
- Direct source: https://ourworldindata.org/grapher/supercomputer-power-flops
- Columns:
> The number of floating-point operations per second (GigaFLOPS) by the fastest supercomputer in any given year



## Physics 


* <font size='+1'>Celsius en Kelvin: $273.15°K=0°C$</font><br/>
```python
from bulkhours import constants as bkc
bkc.c2k := 273.15  # K.C-1
bkc.kelvin := 273.15  # K.C-1
```

* <font size='+1'>Celerité de la lumière: $c = 3 \cdot 10^{5}m\cdot s^{-1}$</font><br/>
```python
from bulkhours import constants as bkc
bkc.c := 3e+05  # m.s-1
bkc.vitesse_lumiere := 3e+05  # m.s-1
```

* <font size='+1'>Distance parcourue par la lumière en 1an: $al = 9.461 \cdot 10^{15}m$</font><br/>
```python
from bulkhours import constants as bkc
bkc.al := 9.461e+15  # m
bkc.annee_lumiere := 9.461e+15  # m
```

* <font size='+1'>Une Unité astrononique faisant un angle d'une seconde d'arc (ancienne déf.): $1pc \equiv \frac{180\cdot60\cdot60}{\pi} = 3.086 \cdot 10^{16}m = 3.26al$</font><br/>
```python
from bulkhours import constants as bkc
bkc.parsec := 3.086e+16  # m.pc-1
```

* <font size='+1'>Une Unité astrononique faisant un angle d'une seconde d'arc (ancienne déf.): $1kpc \equiv \frac{1000\cdot180\cdot60\cdot60}{\pi}$</font><br/>
```python
from bulkhours import constants as bkc
bkc.kparsec := 3.086e+19  # m.kpc-1
```

* <font size='+1'>Constante de la gravitation: $G = 6.67 \cdot 10^{-11}N\cdot m^2\cdot kg^{-2}$   [6.6743e-11N.m2.kg-2]</font><br/>
```python
from bulkhours import constants as bkc
bkc.G := 6.67e-11  # N.m2.kg-2
```

* <font size='+1'>Acceleration standard de la gravitation: $g = 9.8m\cdot s^{-2}$   [9.80665m.s-2]</font><br/>
```python
from bulkhours import constants as bkc
bkc.g := 9.8  # m.s-2
```

* <font size='+1'>Constante de Planck: $h = 6.626 \cdot 10^{-34}J\cdot s$   [6.62607015e-34J.s]</font><br/>
```python
from bulkhours import constants as bkc
bkc.h := 6.626e-34  # J.s
```

* <font size='+1'>Constante de Planck réduite: $\bar{h} = \frac{h}{2\pi}$</font><br/>
```python
from bulkhours import constants as bkc
bkc.hbar := 1.055e-34  # J.s
```

* <font size='+1'>Nombre d'Avogadro: $N_\mathcal{A} = 6.02 \cdot 10^{23}mol-1$ (Carbone: $12g\Leftrightarrow 1mol$)</font><br/>
```python
from bulkhours import constants as bkc
bkc.N_A := 6.02e+23  # mol-1
bkc.A := 6.02e+23  # mol-1
```

* <font size='+1'>Constante de Stefan-Boltzmann: $\sigma = 5.67 \cdot 10^{-8} W\cdot m^{-2}\cdot K^{-4}$</font><br/>
```python
from bulkhours import constants as bkc
bkc.sigma := 5.67e-08  # W.m-2.K-4
bkc.stefan := 5.67e-08  # W.m-2.K-4
```

* <font size='+1'>Constante de Wien: $\lambda_{\text{max}} \cdot T = 0.003m\cdot K$   [0.002897771955m.K]</font><br/>
```python
from bulkhours import constants as bkc
bkc.Wien := 0.003  # m.K
bkc.wien := 0.003  # m.K
bkc.lambda_max := 0.003  # m.K
```

* <font size='+1'>Constante de Rydberg: $R_H({\text{Hydrogene}}) = 1.1 \cdot 10^{7}m-1$</font><br/>
```python
from bulkhours import constants as bkc
bkc.Rydberg := 1.1e+07  # m-1
bkc.rydberg := 1.1e+07  # m-1
bkc.R_H := 1.1e+07  # m-1
```

* <font size='+1'>Energie cinetique e sous 1Volt: $\mathrm{eV} = 1.6 \cdot 10^{-19}J\cdot eV^{-1}$   [1.602176634e-19J.eV-1]</font><br/>
```python
from bulkhours import constants as bkc
bkc.eV := 1.6e-19  # J.eV-1
bkc.ev := 1.6e-19  # J.eV-1
```

* <font size='+1'>Masse electron: $m_e = 9.109 \cdot 10^{-31}kg$   [9.1093837015e-31kg]</font><br/>
```python
from bulkhours import constants as bkc
bkc.m_e := 9.109e-31  # kg
```

* <font size='+1'>Rayon de Bohr: $a = 5.3 \cdot 10^{-11} m$</font><br/>
```python
from bulkhours import constants as bkc
bkc.r_bohr := 5.300e-11  # m
bkc.a := 5.300e-11  # m
```

* <font size='+1'>Masse proton: $m_p = 1.673 \cdot 10^{-27}kg$   [1.67262192369e-27kg]</font><br/>
```python
from bulkhours import constants as bkc
bkc.m_p := 1.673e-27  # kg
```

* <font size='+1'>Masse proton: $m_p = 1.007276uma$ ($1uma \equiv \frac{M(^{12}C)}{12}$)   [1.007276466621uma]</font><br/>
```python
from bulkhours import constants as bkc
bkc.m_puma := 1.007276  # uma
```

* <font size='+1'>Masse neutron: $m_n = 1.008663uma$ ($1uma \equiv \frac{M(^{12}C)}{12}$)   [1.00866491595uma]</font><br/>
```python
from bulkhours import constants as bkc
bkc.m_numa := 1.008663  # uma
```

* <font size='+1'>Unité de Masse Atomique: $m_{nuc} = 1.660 \cdot 10^{-27}kg\cdot uma^{-1}$ ($1uma \equiv \frac{M(^{12}C)}{12}$)   [1.6605390666e-27kg.uma-1]</font><br/>
```python
from bulkhours import constants as bkc
bkc.uma := 1.660e-27  # kg.uma-1
```

* <font size='+1'>Unité de Masse Atomique (MeV): $m_{nuc} = 931.500MeV\cdot uma^{-1}$ ($1uma \equiv \frac{M(^{12}C)}{12}$)</font><br/>
```python
from bulkhours import constants as bkc
bkc.uma_mev := 931.500  # MeV.uma-1
```

* <font size='+1'>Masse: $M_{\mathrm{mercure}} = 3.301 \cdot 10^{23}kg$</font><br/>
```python
from bulkhours import constants as bkc
bkc.M_mercure := 3.301e+23  # kg
```

* <font size='+1'>Distance au soleil: $d_{\odot \mathrm{mercure}} = 0.38ua$</font><br/>
```python
from bulkhours import constants as bkc
bkc.d_mercure := 0.38  # ua
```

* <font size='+1'>Rayon: $R_{\mathrm{mercure}} = 2439km$</font><br/>
```python
from bulkhours import constants as bkc
bkc.R_mercure := 2439  # km
```

* <font size='+1'>Albedo: $A_{\mathrm{mercure}} = 0.09$</font><br/>
```python
from bulkhours import constants as bkc
bkc.A_mercure := 0.09  # Sans unité (entre 0 et 1)
```

* <font size='+1'>Effet de serre: $S_{\mathrm{mercure}} = 0$</font><br/>
```python
from bulkhours import constants as bkc
bkc.S_mercure := 0  # Sans unité (entre 0 et 1)
```

* <font size='+1'>Temperature moyenne: $T_{\mathrm{mercure}} = 167.0°C$</font><br/>
```python
from bulkhours import constants as bkc
bkc.T_mercure := 167.0  # °C
```

* <font size='+1'>Masse: $M_{\mathrm{venus}} = 4.867 \cdot 10^{24}kg$</font><br/>
```python
from bulkhours import constants as bkc
bkc.M_venus := 4.867e+24  # kg
```

* <font size='+1'>Distance au soleil: $d_{\odot \mathrm{venus}} = 0.72ua$</font><br/>
```python
from bulkhours import constants as bkc
bkc.d_venus := 0.72  # ua
```

* <font size='+1'>Rayon: $R_{\mathrm{venus}} = 3390km$</font><br/>
```python
from bulkhours import constants as bkc
bkc.R_venus := 3390  # km
```

* <font size='+1'>Albedo: $A_{\mathrm{venus}} = 0.77$</font><br/>
```python
from bulkhours import constants as bkc
bkc.A_venus := 0.77  # Sans unité (entre 0 et 1)
```

* <font size='+1'>Effet de serre: $S_{\mathrm{venus}} = 0.991$</font><br/>
```python
from bulkhours import constants as bkc
bkc.S_venus := 0.991  # Sans unité (entre 0 et 1)
```

* <font size='+1'>Temperature moyenne: $T_{\mathrm{venus}} = 464.0°C$</font><br/>
```python
from bulkhours import constants as bkc
bkc.T_venus := 464.0  # °C
```

* <font size='+1'>Masse: $M_{\mathrm{terre}} = 5.972 \cdot 10^{24}kg$</font><br/>
```python
from bulkhours import constants as bkc
bkc.M_terre := 5.972e+24  # kg
```

* <font size='+1'>Distance au soleil: $d_{\odot \mathrm{terre}} = 1.00ua$</font><br/>
```python
from bulkhours import constants as bkc
bkc.d_terre := 1.00  # ua
```

* <font size='+1'>Rayon: $R_{\mathrm{terre}} = 6371km$</font><br/>
```python
from bulkhours import constants as bkc
bkc.R_terre := 6371  # km
```

* <font size='+1'>Albedo: $A_{\mathrm{terre}} = 0.30$</font><br/>
```python
from bulkhours import constants as bkc
bkc.A_terre := 0.30  # Sans unité (entre 0 et 1)
```

* <font size='+1'>Effet de serre: $S_{\mathrm{terre}} = 0.394$</font><br/>
```python
from bulkhours import constants as bkc
bkc.S_terre := 0.394  # Sans unité (entre 0 et 1)
```

* <font size='+1'>Temperature moyenne: $T_{\mathrm{terre}} = 15.0°C$</font><br/>
```python
from bulkhours import constants as bkc
bkc.T_terre := 15.0  # °C
```

* <font size='+1'>Distance au soleil: $d_{\odot \mathrm{terre}} = 1ua = 1.500 \cdot 10^{11}m$   [149597870700.0m]</font><br/>
```python
from bulkhours import constants as bkc
bkc.d_terre_solm := 1.500e+11  # m
bkc.d_terresoleil := 1.500e+11  # m
```

* <font size='+1'>Masse: $M_{\mathrm{mars}} = 6.417 \cdot 10^{23}kg$</font><br/>
```python
from bulkhours import constants as bkc
bkc.M_mars := 6.417e+23  # kg
```

* <font size='+1'>Distance au soleil: $d_{\odot \mathrm{mars}} = 1.52ua$</font><br/>
```python
from bulkhours import constants as bkc
bkc.d_mars := 1.52  # ua
```

* <font size='+1'>Rayon: $R_{\mathrm{mars}} = 3390km$</font><br/>
```python
from bulkhours import constants as bkc
bkc.R_mars := 3390  # km
```

* <font size='+1'>Albedo: $A_{\mathrm{mars}} = 0.25$</font><br/>
```python
from bulkhours import constants as bkc
bkc.A_mars := 0.25  # Sans unité (entre 0 et 1)
```

* <font size='+1'>Effet de serre: $S_{\mathrm{mars}} = 0.010$</font><br/>
```python
from bulkhours import constants as bkc
bkc.S_mars := 0.010  # Sans unité (entre 0 et 1)
```

* <font size='+1'>Temperature moyenne: $T_{\mathrm{mars}} = -62.8°C$</font><br/>
```python
from bulkhours import constants as bkc
bkc.T_mars := -62.8  # °C
```

* <font size='+1'>Masse: $M_{\odot} = 1.988 \cdot 10^{30}kg$</font><br/>
```python
from bulkhours import constants as bkc
bkc.M_soleil := 1.988e+30  # kg
```

* <font size='+1'>Rayon: $R_{\odot} = 7 \cdot 10^{5}km$</font><br/>
```python
from bulkhours import constants as bkc
bkc.R_soleil := 7e+05  # km
```

* <font size='+1'>Luminosité: $L_{\odot} = 3.83 \cdot 10^{26}W$</font><br/>
```python
from bulkhours import constants as bkc
bkc.L_soleil := 3.83e+26  # W
bkc.L_sol := 3.83e+26  # W
bkc.L_sun := 3.83e+26  # W
```

* <font size='+1'>Temperature moyenne: $T_{\odot} = 5800.0°C$</font><br/>
```python
from bulkhours import constants as bkc
bkc.T_soleil := 5800.0  # °C
```

* <font size='+1'>Masse: $M_{\mathrm{lune}} = 7.350 \cdot 10^{22}kg$</font><br/>
```python
from bulkhours import constants as bkc
bkc.M_lune := 7.350e+22  # kg
```

* <font size='+1'>Distance au soleil: $d_{\odot \mathrm{lune}} = 1.00ua$</font><br/>
```python
from bulkhours import constants as bkc
bkc.d_lune := 1.00  # ua
```

* <font size='+1'>Rayon: $R_{\mathrm{lune}} = 6371km$</font><br/>
```python
from bulkhours import constants as bkc
bkc.R_lune := 6371  # km
```

* <font size='+1'>Albedo: $A_{\mathrm{lune}} = 0.11$</font><br/>
```python
from bulkhours import constants as bkc
bkc.A_lune := 0.11  # Sans unité (entre 0 et 1)
```

* <font size='+1'>Distance à la lune: $d_{\mathrm{terre} \mathrm{lune}} = 3.844 \cdot 10^{8}m$</font><br/>
```python
from bulkhours import constants as bkc
bkc.d_terre_lune := 3.844e+08  # m
```

* <font size='+1'>Perimètre d'un cercle de rayon 1/2🙂: $pi = 3.141593$</font><br/>
```python
from bulkhours import constants as bkc
bkc.pi := 3.141593  # 
```

#### Quarterly sunspots activity (ssn)
#### `bulkhours.get_data("statsdata.sunspots")`
- Raw data: [observed-solar-cycle-indices.json](https://services.swpc.noaa.gov/json/solar-cycle/observed-solar-cycle-indices.json)  ([raw](https://services.swpc.noaa.gov/json/solar-cycle/observed-solar-cycle-indices.json))
- Enrich data: [statsdata.py](https://github.com/guydegnol/bulkhours/blob/main/bulkhours/data/statsdata.py)  ([raw](https://raw.githubusercontent.com/guydegnol/bulkhours/main/bulkhours/data/statsdata.py))
- Direct source: https://www.swpc.noaa.gov/products/solar-cycle-progression
- Reference site: https://services.swpc.noaa.gov/json/solar-cycle/observed-solar-cycle-indices.json
- Columns:
> https://en.wikipedia.org/wiki/Wolf_number



## Health 

#### Coronavirus Pandemic (COVID-19) data
#### `bulkhours.get_data("vaccinations")`
- Raw data: [vaccinations.csv](https://github.com/owid/covid-19-data/master/public/data/vaccinations/vaccinations.csv)  ([raw](https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/vaccinations/vaccinations.csv))
- Direct source: https://ourworldindata.org/coronavirus
- Reference site: https://covid19.who.int/data
- Columns:
> https://github.com/owid/covid-19-data/tree/master/public/data/

#### Prostate cancer data
#### `bulkhours.get_data("prostate")`
- Raw data: [prostate.tsv](https://github.com/guydegnol/bulkhours/blob/main/data/prostate.tsv)
- Direct source: https://hastie.su.domains/ElemStatLearn/data.html
- Columns:
> lcavol, lweight, age, lbph, svi, lcp, gleason, pgg45, [outcome]

#### Coronavirus Pandemic (COVID-19) data
#### `bulkhours.get_data("covid")`
- Raw data: [owid-covid-data.csv](https://covid.ourworldindata.org/data/owid-covid-data.csv)  ([raw](https://covid.ourworldindata.org/data/owid-covid-data.csv))
- Direct source: https://ourworldindata.org/coronavirus
- Reference site: https://covid19.who.int/data
- Columns:
> https://github.com/owid/covid-19-data/tree/master/public/data/



## Climate_Evolution 

#### Greenhouse effect gaz concentrations
#### `bulkhours.get_data("co2.concentrations")`
- Raw data: [climate-change.csv](https://github.com/guydegnol/bulkhours/blob/main/data/climate-change.csv)
- Enrich data: [world.py](https://github.com/guydegnol/bulkhours/blob/main/bulkhours/data/world.py)  ([raw](https://raw.githubusercontent.com/guydegnol/bulkhours/main/bulkhours/data/world.py))
- Direct source: https://ourworldindata.org/atmospheric-concentrations

#### Greenhouse effect gaz concentrations
#### `bulkhours.get_data("co2.mapconcentrations")`
- Raw data: [climate-change.csv](https://github.com/guydegnol/bulkhours/blob/main/data/climate-change.csv)
- Enrich data: [world.py](https://github.com/guydegnol/bulkhours/blob/main/bulkhours/data/world.py)  ([raw](https://raw.githubusercontent.com/guydegnol/bulkhours/main/bulkhours/data/world.py))
- Direct source: https://ourworldindata.org/atmospheric-concentrations

#### Data on CO2 and Greenhouse Gas Emissions by Our World in Data
#### `bulkhours.get_data("co2.main")`
- Raw data: [owid-co2-data.csv](https://github.com/owid/co2-data/master/owid-co2-data.csv)  ([raw](https://raw.githubusercontent.com/owid/co2-data/master/owid-co2-data.csv))
- Enrich data: [world.py](https://github.com/guydegnol/bulkhours/blob/main/bulkhours/data/world.py)  ([raw](https://raw.githubusercontent.com/guydegnol/bulkhours/main/bulkhours/data/world.py))
- Columns:
> https://github.com/owid/co2-data/blob/master/owid-co2-codebook.csv

#### Data on CO2 and Greenhouse Gas Emissions by Our World in Data (with extra gpx data)
#### `bulkhours.get_data("co2.mapmain")`
- Raw data: [owid-co2-data.csv](https://github.com/owid/co2-data/master/owid-co2-data.csv)  ([raw](https://raw.githubusercontent.com/owid/co2-data/master/owid-co2-data.csv))
- Enrich data: [world.py](https://github.com/guydegnol/bulkhours/blob/main/bulkhours/data/world.py)  ([raw](https://raw.githubusercontent.com/guydegnol/bulkhours/main/bulkhours/data/world.py))
- Columns:
> https://github.com/owid/co2-data/blob/master/owid-co2-codebook.csv

#### CO2 transportation info
#### `bulkhours.get_data("co2.travel_mode")`
- Raw data: [carbon-footprint-travel-mode.csv](https://github.com/guydegnol/bulkhours/blob/main/data/carbon-footprint-travel-mode.csv)
- Direct source: https://ourworldindata.org/grapher/carbon-footprint-travel-mode



## Machine_learning 

#### Cat or not training data
#### `bulkhours.get_data("train_catvnoncat")`
- Raw data: [train_catvnoncat.h5](https://github.com/guydegnol/bulkhours/blob/main/data/train_catvnoncat.h5)

#### Cat or not test data
#### `bulkhours.get_data("test_catvnoncat")`
- Raw data: [test_catvnoncat.h5](https://github.com/guydegnol/bulkhours/blob/main/data/test_catvnoncat.h5)

