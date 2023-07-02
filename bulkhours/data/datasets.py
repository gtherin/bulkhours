datacategories = [
    dict(label="Economics", tag="Economics"),
    dict(label="Predictive maintenance", tag="Predictive_Maintenance"),
    dict(label="Computing", tag="Computing"),
    dict(label="Physics", tag="Physics"),
    dict(label="Health", tag="Health"),
    dict(label="Climate Evolution", tag="Climate_Evolution"),
    dict(label="Machine learning data", tag="Machine_learning"),
]

datasets = [
    dict(
        label="world.poverty",
        summary="World Bank Poverty and Inequality data",
        category="Economics",
        raw_data="https://nyc3.digitaloceanspaces.com/owid-public/data/poverty/pip_dataset.csv",
        ref_source="https://ourworldindata.org/poverty",
        ref_site="""https://pip.worldbank.org/""",
        enrich_data="https://github.com/guydegnol/bulkhours/blob/main/bulkhours/data/world.py",
        columns_info="https://github.com/owid/poverty-data/blob/main/datasets/pip_codebook.csv",
    ),
    dict(
        label="world.mappoverty",
        summary="World Bank Poverty and Inequality data (with gpx extra info)",
        reference="world.poverty",
    ),
    dict(
        label="world.gdp",
        summary="World Bank Gdp data",
        category="Economics",
        raw_data="https://nyc3.digitaloceanspaces.com/owid-public/data/poverty/pip_dataset.csv",
        ref_source="https://ourworldindata.org/poverty",
        ref_site="""https://pip.worldbank.org/""",
        # drop=["Country Code", "Indicator Name", "Indicator Code", "Unnamed: 66"]
        enrich_data="https://github.com/guydegnol/bulkhours/blob/main/bulkhours/data/world.py",
        columns_info="https://github.com/owid/poverty-data/blob/main/datasets/pip_codebook.csv",
    ),
    dict(label="world.mapgdp", summary="World Bank Gdp data (with gpx extra info)", reference="world.gdp"),
    dict(
        label="world.macro",
        summary="Global economic data",
        category="Economics",
        raw_data=[
            "corruption.csv",
            "cost_of_living.csv",
            "richest_countries.csv",
            "unemployment.csv",
            "tourism.csv",
            "continent.tsv",
        ],
        on="country",
        enrich_data="https://github.com/guydegnol/bulkhours/blob/main/bulkhours/data/world.py",
    ),
    dict(label="world.mapmacro", summary="Global economic data (with gpx extra info)", reference="world.macro"),
    dict(
        label="world.life_expectancy_vs_gdp_2018",
        summary="Life expectancy versus GDP/capita per country",
        category="Economics",
        raw_data="life-expectancy-vs-gdp-per-capita.csv",
        info="GDP per capita is measured in 2011 international dollars, which corrects for inflation and cross-country price differences",
        ref_source="https://ourworldindata.org/grapher/life-expectancy-vs-gdp-per-capita",
        ref_site="""Maddison Project Database (2020); UN WPP (2022); Zijdeman et al. (2015)""",
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
        # drop=["annotations", "Continent"],
        enrich_data="https://github.com/guydegnol/bulkhours/blob/main/bulkhours/data/world.py",
        query="Year == 2018 and Population > 1e7",
    ),
    dict(
        label="mincer.stats",
        summary="Descriptive statistics of hourly wages in selected EU countries in 2010 (in PPS)",
        category="Economics",
        ref_source="https://www.nbp.pl/publikacje/materialy_i_studia/226_en.pdf (table 2)",
    ),
    dict(
        label="mincer.params",
        summary="Mincer equation parameters per country",
        category="Economics",
        ref_source="https://www.nbp.pl/publikacje/materialy_i_studia/226_en.pdf (table 3)",
        source="""- Mincer equation formula: ln(hourly_wage) = alpha_0i + alpha_1i * edu + alpha_2i * age + alpha_3i * age**2
The results of estimation of parameters in Mincer equations in a set of countries. We
put the point estimates, standard errors (in italics) and p-values for zero restriction test of a
particular parameter (in square brackets)""",
        enrich_data="https://github.com/guydegnol/bulkhours/blob/main/bulkhours/data/mincer.py",
    ),
    dict(
        label="pyramide",
        summary="Age de la population au 1er janvier (fin novembre 2022)",
        category="Economics",
        raw_data="pyramide.tsv",
        source="""la France compte 805 914 personnes de 65 ans dont 425 143 femmes et 380 771 hommes""",
        ref_source="https://www.insee.fr/fr/statistiques/2381472#tableau-figure1",
    ),
    dict(
        label="france.retraites",
        summary="Cotisants, retraités et rapport démographique tous régimes en 2020",
        category="Economics",
        source="""- Note: certains salaires en EQTP sont inférieurs au Smic ; ceci est en effet permis par certains statuts. Cependant, l'existence de rémunérations inférieures au Smic peut aussi provenir d’incohérences entre salaires et durées travaillées dans les déclarations administratives, qui ne peuvent être toutes redressées.
- Lecture: en 2020, en EQTP, 50 % des salariés gagnent plus de 2 005 euros.
- Champ: France hors Mayotte, salariés du privé et des entreprises publiques, y compris bénéficiaires de contrats aidés et de contrats de professionnalisation ; hors apprentis, stagiaires, salariés agricoles et salariés des particuliers employeurs.""",
        enrich_data="https://github.com/guydegnol/bulkhours/blob/main/bulkhours/data/france.py",
        ref_source="https://www.insee.fr/fr/statistiques/2415121#tableau-figure1",
    ),
    dict(
        label="france.income",
        summary="Distribution des salaires mensuels nets en équivalent temps plein (EQTP) en 2020",
        category="Economics",
        source="""- Note : certains salaires en EQTP sont inférieurs au Smic ; ceci est en effet permis par certains statuts.
Cependant, l'existence de rémunérations inférieures au Smic peut aussi provenir d'incohérences entre salaires et durées travaillées dans
les déclarations administratives, qui ne peuvent être toutes redressées.
- Lecture : en 2020, en EQTP, 50 % des salariés gagnent plus de 2 005 euros.
- Champ : France hors Mayotte, salariés du privé et des entreprises publiques, y compris bénéficiaires de contrats aidés et
de contrats de professionnalisation ; hors apprentis, stagiaires, salariés agricoles et salariés des particuliers employeurs.""",
        enrich_data="https://github.com/guydegnol/bulkhours/blob/main/bulkhours/data/france.py",
        ref_source="https://www.insee.fr/fr/statistiques/6436313#tableau-figure2",
    ),
    dict(
        label="france.salaires",
        summary="Revenu salarial et salaire en EQTP annuels moyens selon le sexe en 2019",
        category="Economics",
        columns_description="""| Column   |      Info |
|-----------|:-----------|
| Revenu annuel Femmes moyen   |  Revenu annuel Femmes moyen |         
| Revenu annuel Hommes moyen  |  Revenu annuel Hommes moyen | 
| Revenu annuel Femmes moyen Écart relatif (en %)   |   Revenu annuel Femmes moyen Écart relatif (en %)	| 
| Salaire annuel Femmes moyen EQTP  |  Salaire annuel Femmes moyen EQTP | 
| Salaire annuel Hommes moyen EQTP   |  Salaire annuel Hommes moyen EQTP |
| Salaire annuel Femmes moyen EQTP Écart relatif (en % EQTP)   |  Salaire annuel Femmes moyen EQTP Écart relatif (en % EQTP) |""",
        source="""En 2019, le revenu salarial annuel moyen dans le secteur privé et la fonction publique s'élève à 18_970 euros
pour les femmes, soit un niveau inférieur de 22 % à celui des hommes (figure 1).
Le revenu salarial médian des femmes est inférieur de 16 % à celui des hommes (figure 2).
Cet écart s'amplifie à la fois dans les bas revenus (écart de 25 % pour le premier décile du revenu salarial) et
dans les hauts revenus (écart de 21 % pour le neuvième décile).""",
        enrich_data="https://github.com/guydegnol/bulkhours/blob/main/bulkhours/data/france.py",
        ref_source="https://www.insee.fr/fr/statistiques/6047743?sommaire=6047805",
    ),
    dict(
        label="france.histsalaires",
        summary="Inégalités salariales entre femmes et hommes de 1995 à 2019",
        category="Economics",
        columns_description="""| Column   |      Info |
|-----------|:-----------|
| delta_rev_legacy   |  écart relatif du revenu salarial moyen homme/femme |         
| delta_rev  |  écart relatif (en %) du revenu salarial moyen.1| 
| delta_rev_eqtp_legacy   |  écart relatif du salaire moyen en EQTP	| 
| delta_rev_eqtp  |  écart relatif du salaire moyen en EQTP| 
| delta_vol_eqtp   |  écart relatif du volume de travail en EQTP moyen |""",
        enrich_data="https://github.com/guydegnol/bulkhours/blob/main/bulkhours/data/france.py",
        ref_source="https://www.insee.fr/fr/statistiques/6047743?sommaire=6047805",
        rename=["delta_rev_legacy", "delta_rev", "delta_rev_eqtp_legacy", "delta_rev_eqtp", "delta_vol_eqtp"],
    ),
    dict(
        label="gmacro.fr_qgdp",
        summary="Evolution du PIB et de ses composantes par rapport au trimestre precedent en volume en %",
        category="Economics",
        source="""- Note : données revisitées ; les volumes sont mesures aux prix de l'année précédente changés et corrigés des variations saisonnieres et des effets des jours ouvrables.
- Lecture: au 4e trimestre 2022. le produit interieur brut (PIB) en volume augmente de 0.1 % par rapport au trimestre precedent.""",
        enrich_data="https://github.com/guydegnol/bulkhours/blob/main/bulkhours/data/gmacro.py",
        ref_source="https://www.insee.fr/fr/statistiques/2830547#tableau-figure1",
    ),
    dict(
        label="gmacro.fr_unemployement",
        summary="Évolution du produit intérieur brut et de ses composantes",
        category="Economics",
        enrich_data="https://github.com/guydegnol/bulkhours/blob/main/bulkhours/data/gmacro.py",
        ref_source="https://www.insee.fr/fr/statistiques/2830547#tableau-figure1",
    ),
    dict(
        label="gmacro.us_gdp",
        summary="United States Macroeconomic data (1959q1 - 2009q3)",
        category="Economics",
        enrich_data="https://github.com/guydegnol/bulkhours/blob/main/bulkhours/data/gmacro.py",
        ref_source="https://www.statsmodels.org/0.6.1/datasets/generated/macrodata.html",
        columns_description="""| Column   |      Info |
|-----------|:-----------|
| year      |  1959q1 - 2009q3 |
| quarter   |    1-4 |
| realgdp   | Real gross domestic product (Bil. of chained 2005\$, seasonally adjusted annual rate) |         
| realcons  |  Real personal consumption expenditures (Bil. of chained 2005\$, seasonally adjusted annual rate)| 
| realinv   |  Real gross private domestic investment (Bil. of chained 2005\$, seasonally adjusted annual rate)| 
| realgovt  |  Real federal consumption expenditures & gross investment(Bil. of chained 2005 US$, seasonally adjusted annual rate)| 
| realdpi   |  Real private disposable income (Bil. of chained 2005 US$, seasonally adjusted annual rate)| 
| cpi       |  End of the quarter consumer price index for all urban consumers: all items (1982-84 = 100, seasonally adjusted).| 
| m1        |  End of the quarter M1 nominal money stock (Seasonally adjusted)| 
| tbilrate  |  Quarterly monthly average of the monthly 3-month treasury bill: secondary market rate| 
| unemp     |  Seasonally adjusted unemployment rate (%)| 
| pop       |  End of the quarter total population: all ages incl. armed forces over seas| 
| infl      |  Inflation rate (ln(cpi_{t}/cpi_{t-1}) * 400)| 
| realint   |  Real interest rate (tbilrate - infl)| 
""",
    ),
    dict(
        label="gmacro.fr_gdp",
        summary="France Macroeconomic data",
        category="Economics",
        enrich_data="https://github.com/guydegnol/bulkhours/blob/main/bulkhours/data/gmacro.py",
    ),
    dict(
        label="scipy_distributions_list",
        summary="Scipy list of available distributions",
        category="Economics",
        enrich_data="https://github.com/guydegnol/bulkhours/blob/main/bulkhours/data/statsdata.py",
    ),
    dict(
        label="statsdata.oil",
        summary="Oil production in Saudi Arabia from 1996 to 2007",
        category="Economics",
        ref_source="""https://www.statsmodels.org/stable/index.html""",
        enrich_data="https://github.com/guydegnol/bulkhours/blob/main/bulkhours/data/statsdata.py",
    ),
    dict(
        label="statsdata.air",
        summary="Air pollution data",
        category="Economics",
        ref_source="""https://www.statsmodels.org/stable/index.html""",
        enrich_data="https://github.com/guydegnol/bulkhours/blob/main/bulkhours/data/statsdata.py",
    ),
    dict(
        label="statsdata.livestock2",
        summary="Forecasting livestock, sheep in Asia: comparing forecasting performance of non-seasonal methods.",
        category="Economics",
        ref_source="""https://www.statsmodels.org/stable/index.html""",
        enrich_data="https://github.com/guydegnol/bulkhours/blob/main/bulkhours/data/statsdata.py",
    ),
    dict(
        label="statsdata.livestock3",
        summary="Forecasting livestock, sheep in Asia: comparing forecasting performance of non-seasonal methods. (3)",
        category="Economics",
        ref_source="""https://www.statsmodels.org/stable/index.html""",
        enrich_data="https://github.com/guydegnol/bulkhours/blob/main/bulkhours/data/statsdata.py",
    ),
    dict(
        label="statsdata.aust",
        summary="International visitor night in Australia (millions) < 2005",
        category="Economics",
        enrich_data="https://github.com/guydegnol/bulkhours/blob/main/bulkhours/data/statsdata.py",
    ),
    dict(
        label="statsdata.air_passengers",
        summary="International visitor night in Australia (millions) > 2005",
        category="Economics",
        raw_data="AirPassengers.csv",
        enrich_data="https://github.com/guydegnol/bulkhours/blob/main/bulkhours/data/statsdata.py",
    ),
    dict(
        label="statsdata.hhousing",
        summary="All-Transactions House Price Index for Houston",
        category="Economics",
        ref_source="""https://fred.stlouisfed.org/series/ATNHPIUS26420Q""",
        enrich_data="https://github.com/guydegnol/bulkhours/blob/main/bulkhours/data/statsdata.py",
    ),
    dict(
        label="prices-split-adjusted",
        summary="Market prices of SP500 stocks",
        category="Economics",
        ref_source="""https://github.com/kyi3081/stock-analysis""",
        raw_data="https://raw.githubusercontent.com/kyi3081/stock-analysis/master/prices-split-adjusted.csv",
    ),
    dict(
        label="fundamentals",
        summary="Market fundamentals of SP500 stocks",
        category="Economics",
        ref_source="""https://github.com/kyi3081/stock-analysis""",
        raw_data="https://raw.githubusercontent.com/kyi3081/stock-analysis/master/fundamentals.csv",
    ),
    dict(
        label="securities",
        summary="Stocks information for SP500",
        category="Economics",
        ref_source="""https://github.com/kyi3081/stock-analysis""",
        raw_data="https://raw.githubusercontent.com/kyi3081/stock-analysis/master/securities.csv",
    ),
    dict(
        label="trading.apple",
        summary="Statement of Apple stock (Quarterly)",
        category="Economics",
        raw_data="APPLE_DownloadFPrepStatementQuarter.tsv",
        enrich_data="https://github.com/guydegnol/bulkhours/blob/main/bulkhours/data/trading.py",
    ),
    dict(
        label="continent",
        summary="Standardized country information (iso m49)",
        category="Economics",
        raw_data="continent.tsv",
    ),
    dict(
        label="corruption",
        summary="Corruption index per country",
        category="Economics",
        raw_data="corruption.csv",
    ),
    dict(
        label="cost_of_living",
        summary="Cost of living",
        category="Economics",
        raw_data="cost_of_living.csv",
        columns_description="""| Column   |      Info |
|-----------|:-----------|
| country   |   |         
| cost_index  |   | 
| monthly_income   |  	| 
| purchasing_power_index  |  |
""",
    ),
    dict(
        label="richest_countries",
        summary="GDP per capita per country",
        category="Economics",
        raw_data="richest_countries.csv",
        columns_description="""| Column   |      Info |
|-----------|:-----------|
| country   |   |         
| gdp_per_capita  |   | 
""",
    ),
    dict(
        label="tourism",
        summary="Tourism information per country",
        category="Economics",
        raw_data="tourism.csv",
    ),
    dict(
        label="unemployment",
        summary="Unemployemnt rates per country",
        category="Economics",
        raw_data="unemployment.csv",
    ),
    dict(
        label="wages",
        summary="Simple synthetic data for exercice",
        category="Economics",
        raw_data="wages.tsv",
    ),
    dict(
        label="COR_1",
        summary="COR data",
        category="Economics",
        raw_data="Données septembre partie 1.xlsx",
    ),
    dict(label="COR_2", reference="COR_1", raw_data="Données_RA2022_P2.xlsx"),
    dict(label="COR_2bis", reference="COR_1", raw_data="Données complémentaires partie 2 RA 2022.xlsx"),
    dict(label="COR_3", reference="COR_1", raw_data="Données septembre 2022 - partie 3.xlsx"),
    dict(label="COR_4", reference="COR_1", raw_data="Données_RA2022_P4.xlsx"),
    dict(label="COR_5", reference="COR_1", raw_data="Données septembre 2022 - partie 5.xlsx"),
    dict(
        label="supercomputers",
        summary="Computational capacity of the fastest supercomputers",
        category="Computing",
        raw_data="https://raw.githubusercontent.com/owid/owid-datasets/dd7a4ecbb249f98028e25c304ef7d68de8979ea9/datasets/Supercomputer%20power%20(FLOPS)%20%E2%80%93%20TOP500%20Database/Supercomputer%20power%20(FLOPS)%20%E2%80%93%20TOP500%20Database.csv",
        ref_source="""https://ourworldindata.org/grapher/supercomputer-power-flops""",
        columns_info="The number of floating-point operations per second (GigaFLOPS) by the fastest supercomputer in any given year",
    ),
    dict(
        label="co2.concentrations",
        summary="Greenhouse effect gaz concentrations",
        category="Climate_Evolution",
        raw_data="climate-change.csv",
        ref_source="""https://ourworldindata.org/atmospheric-concentrations""",
        kwargs=dict(zone="World"),
        enrich_data="https://github.com/guydegnol/bulkhours/blob/main/bulkhours/data/world.py",
    ),
    dict(label="co2.mapconcentrations", reference="co2.concentrations"),
    dict(
        label="co2.main",
        summary="Data on CO2 and Greenhouse Gas Emissions by Our World in Data",
        category="Climate_Evolution",
        raw_data="https://raw.githubusercontent.com/owid/co2-data/master/owid-co2-data.csv",
        enrich_data="https://github.com/guydegnol/bulkhours/blob/main/bulkhours/data/world.py",
        columns_info="https://github.com/owid/co2-data/blob/master/owid-co2-codebook.csv",
    ),
    dict(
        label="co2.mapmain",
        summary="Data on CO2 and Greenhouse Gas Emissions by Our World in Data (with extra gpx data)",
        reference="co2.main",
    ),
    dict(
        label="vaccinations",
        summary="Coronavirus Pandemic (COVID-19) data",
        category="Health",
        raw_data="https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/vaccinations/vaccinations.csv",
        ref_site="""https://covid19.who.int/data""",
        ref_source="""https://ourworldindata.org/coronavirus""",
        columns_info="https://github.com/owid/covid-19-data/tree/master/public/data/",
    ),
    dict(
        label="prostate",
        summary="Prostate cancer data",
        category="Health",
        raw_data="prostate.tsv",
        source="""lpsa train/test indicator (column 10) This last column indicates which 67 observations were used as the "training set" and which 30 as the test set, as described on page 48 in the book.
There was an error in these data in the first edition of this book. Subject 32 had a value of 6.1 for lweight, which translates to a 449 gm prostate! The correct value is 44.9 gm. We are grateful to Prof. Stephen W. Link for alerting us to this error.
The features must first be scaled to have mean zero and  variance 96 (=n) before the analyses in Tables 3.1 and beyond.  That is, if x is the  96 by 8 matrix of features, we compute xp <- scale(x,TRUE,TRUE)""",
        ref_source="https://hastie.su.domains/ElemStatLearn/data.html",
        columns_description="""| Column   |      Info |
|-----------|:-----------|
| lcavol   |  |         
| lweight  | | 
| lbph   | 	| 
| svi  |  | 
| lcp   |   |
| gleason   |  |
| pgg45   |   |
| [outcome]   |   |
""",
    ),
    dict(
        label="covid",
        summary="Coronavirus Pandemic (COVID-19) data",
        category="Health",
        raw_data="https://covid.ourworldindata.org/data/owid-covid-data.csv",
        ref_site="""https://covid19.who.int/data""",
        ref_source="https://ourworldindata.org/coronavirus",
        columns_info="https://github.com/owid/covid-19-data/tree/master/public/data/",
    ),
    dict(
        label="statsdata.sunspots",
        summary="Quarterly sunspots activity (ssn)",
        category="Physics",
        ref_site="""https://services.swpc.noaa.gov/json/solar-cycle/observed-solar-cycle-indices.json""",
        raw_data="https://services.swpc.noaa.gov/json/solar-cycle/observed-solar-cycle-indices.json",
        enrich_data="https://github.com/guydegnol/bulkhours/blob/main/bulkhours/data/statsdata.py",
        ref_source="https://www.swpc.noaa.gov/products/solar-cycle-progression",
        columns_info="https://en.wikipedia.org/wiki/Wolf_number",
    ),
    dict(
        label="co2.travel_mode",
        summary="CO2 transportation info",
        category="Climate_Evolution",
        ref_source="""https://ourworldindata.org/grapher/carbon-footprint-travel-mode""",
        raw_data="carbon-footprint-travel-mode.csv",
    ),
    dict(
        label="train_catvnoncat",
        summary="Cat or not training data",
        category="Machine_learning",
        raw_data="train_catvnoncat.h5",
    ),
    dict(
        label="test_catvnoncat",
        summary="Cat or not test data",
        category="Machine_learning",
        raw_data="test_catvnoncat.h5",
    ),
    dict(
        label="maintenance1",
        summary="Synthetic data for machine failure data (1)",
        category="Predictive_Maintenance",
        raw_data="https://raw.githubusercontent.com/shadgriffin/feature_engineering_equipment_failure/main/fe_equipment_failure_data_1.csv",
    ),
    dict(
        label="maintenance2",
        summary="Synthetic data for machine failure data (2)",
        category="Predictive_Maintenance",
        raw_data="https://raw.githubusercontent.com/shadgriffin/feature_engineering_equipment_failure/main/fe_equipment_failure_data_2.csv",
    ),
    dict(
        label="maintenance3",
        summary="Synthetic data for machine failure data (3)",
        category="Predictive_Maintenance",
        raw_data="https://raw.githubusercontent.com/shadgriffin/machine_failure/master/equipment_failure_data_1.csv",
    ),
    dict(
        label="maintenance4",
        summary="Synthetic data for machine failure data (4)",
        category="Predictive_Maintenance",
        raw_data="https://raw.githubusercontent.com/shadgriffin/machine_failure/master/equipment_failure_data_2.csv",
    ),
    dict(
        label="hpc.transistor_count",
        summary="transistor_count",
        category="Computing",
        ref_site="https://en.wikipedia.org/wiki/Transistor_count",
    ),
    dict(
        label="hpc.engraving_scale",
        summary="Semiconductor device fabrication: MOSFET scaling",
        category="Computing",
        ref_site="https://en.wikipedia.org/wiki/Transistor_count",
    ),
    dict(
        label="hpc.FLOPS_units",
        summary="FLOPS sub-units",
        category="Computing",
        ref_site="https://en.wikipedia.org/wiki/FLOPS",
    ),
    dict(
        label="hpc.FLOPS_gpus",
        summary="FLOPS for gpus",
        category="Computing",
        ref_site="https://en.wikipedia.org/wiki/FLOPS",
    ),
    dict(
        label="hpc.FLOPS_cpus",
        summary="FLOPS for cpus",
        category="Computing",
        ref_site="https://en.wikipedia.org/wiki/FLOPS",
    ),
]

for f in (
    ["chose1.jpg", "chose2.jpg", "radian2.png", "README.md", "brown.gif", "gradient_descent.png", "TCL.png"]
    + ["lognormal.png", "in_trading.csv", "galton.jpg", "ffcontrol.csv", "galtonr.png"]
    + ["exercices", "freefight.csv", "cache"]
):
    datasets.append(dict(label=f, raw_data=f, category="Internal"))

ddatasets = {v["label"]: v for v in datasets}


for d in range(len(datasets)):
    if "reference" in datasets[d] and (lr := datasets[d]["reference"]) in ddatasets:
        datasets[d] = {**ddatasets[lr], **datasets[d]}
        ddatasets[datasets[d]["label"]] = datasets[d]
