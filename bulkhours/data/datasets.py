datacategories = [
    dict(label="Economics", tag="Economics"),
    dict(label="Predictive maintenance", tag="Maintenance"),
    dict(label="Computing", tag="Computing"),
    dict(label="Physics", tag="Physics"),
    dict(label="Health", tag="Health"),
    dict(label="Climate Evolution", tag="Climate"),
    dict(label="Other Machine learning training data", tag="IA"),
]

datasets = [
    dict(
        label="world.poverty",
        category="Economics",
        raw_data="https://nyc3.digitaloceanspaces.com/owid-public/data/poverty/pip_dataset.csv",
        source="""World Bank Poverty and Inequality Platform
- Direct source: https://ourworldindata.org/poverty
- Data source: https://pip.worldbank.org/
- Info columns: https://github.com/owid/poverty-data/blob/main/datasets/pip_codebook.csv
        """,
    ),
    dict(
        label="world.mappoverty",
        category="Economics",
        raw_data="https://nyc3.digitaloceanspaces.com/owid-public/data/poverty/pip_dataset.csv",
        source="""World Bank Poverty and Inequality Platform
- Direct source: https://ourworldindata.org/poverty
- Data source: https://pip.worldbank.org/
- Info columns: https://github.com/owid/poverty-data/blob/main/datasets/pip_codebook.csv
        """,
    ),
    dict(
        label="world.gdp",
        category="Economics",
        raw_data="https://nyc3.digitaloceanspaces.com/owid-public/data/poverty/pip_dataset.csv",
        source="""World Bank Poverty and Inequality Platform
- Direct source: https://ourworldindata.org/poverty
- Data source: https://pip.worldbank.org/
- Info columns: https://github.com/owid/poverty-data/blob/main/datasets/pip_codebook.csv
        """,
        # drop=["Country Code", "Indicator Name", "Indicator Code", "Unnamed: 66"]
    ),
    dict(label="world.mapgdp", reference="world.gdp"),
    dict(
        label="world.macro",
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
        source="nope",
        enrich_data="https://github.com/guydegnol/bulkhours/blob/main/bulkhours/data/world.py",
    ),
    dict(label="world.mapmacro", reference="world.macro"),
    dict(
        label="world.corruption",
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
        source="nope",
        enrich_data="https://github.com/guydegnol/bulkhours/blob/main/bulkhours/data/world.py",
    ),
    dict(
        label="world.life_expectancy_vs_gdp_2018",
        category="Economics",
        raw_data="life-expectancy-vs-gdp-per-capita.csv",
        info="GDP per capita is measured in 2011 international dollars, which corrects for inflation and cross-country price differences",
        source="""Life expectancy versus GDP/capita per country
- Direct source: https://ourworldindata.org/grapher/life-expectancy-vs-gdp-per-capita
- Data source: Maddison Project Database (2020); UN WPP (2022); Zijdeman et al. (2015)
- Info columns: GDP per capita is measured in 2011 international dollars, which corrects for inflation and cross-country price differences
        """,
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
        category="Economics",
        source="""Descriptive statistics of hourly wages in selected EU countries in 2010 (in PPS) 
Table 2: https://www.nbp.pl/publikacje/materialy_i_studia/226_en.pdf
    """,
    ),
    dict(
        label="mincer.params",
        category="Economics",
        source="""ln(hourly_wage) = alpha_0i + alpha_1i * edu + alpha_2i * age + alpha_3i * age**2
Table 3. https://www.nbp.pl/publikacje/materialy_i_studia/226_en.pdf
The results of estimation of parameters in Mincer equations in a set of countries. We
put the point estimates, standard errors (in italics) and p-values for zero restriction test of a
particular parameter (in square brackets)        
        """,
    ),
    dict(
        label="pyramide",
        category="Economics",
        raw_data="pyramide.tsv",
        source="""Age de la population au 1er janvier ; données provisoires arrêtées à fin novembre 2022 (https://www.insee.fr/fr/)
Lecture : au 1er janvier 2023, la France compte 805 914 personnes de 65 ans dont 425 143 femmes et 380 771 hommes. Champ : France.
    Source : https://www.insee.fr/fr/statistiques/2381472#tableau-figure1
    """,
    ),
    dict(
        label="france.retraites",
        category="Economics",
        source="""Salaires mensuels nets en équivalent temps plein (EQTP) en 2020 (https://www.insee.fr/fr/)
        Source https://www.insee.fr/fr/statistiques/2415121#tableau-figure1

        Distribution des salaires mensuels nets en équivalent temps plein (EQTP) en 2020

    Note : certains salaires en EQTP sont inférieurs au Smic ; ceci est en effet permis par certains statuts. Cependant, l'existence de rémunérations inférieures au Smic peut aussi provenir d’incohérences entre salaires et durées travaillées dans les déclarations administratives, qui ne peuvent être toutes redressées.
    Lecture : en 2020, en EQTP, 50 % des salariés gagnent plus de 2 005 euros.
    Champ : France hors Mayotte, salariés du privé et des entreprises publiques, y compris bénéficiaires de contrats aidés et de contrats de professionnalisation ; hors apprentis, stagiaires, salariés agricoles et salariés des particuliers employeurs.
    """,
    ),
    dict(
        label="france.income",
        category="Economics",
        source="""Distribution des salaires mensuels nets en équivalent temps plein (EQTP) en 2020 (https://www.insee.fr/fr/)
        Source https://www.insee.fr/fr/statistiques/6436313#tableau-figure2
      - Note : certains salaires en EQTP sont inférieurs au Smic ; ceci est en effet permis par certains statuts.
    Cependant, l'existence de rémunérations inférieures au Smic peut aussi provenir d’incohérences entre salaires et durées travaillées dans
    les déclarations administratives, qui ne peuvent être toutes redressées.
      - Lecture : en 2020, en EQTP, 50 % des salariés gagnent plus de 2 005 euros.
    Champ : France hors Mayotte, salariés du privé et des entreprises publiques, y compris bénéficiaires de contrats aidés et
    de contrats de professionnalisation ; hors apprentis, stagiaires, salariés agricoles et salariés des particuliers employeurs.
    """,
    ),
    dict(
        label="france.salaires",
        category="Economics",
        source="""Revenu salarial et salaire en EQTP annuels moyens selon le sexe en 2019 (https://www.insee.fr/fr/)
          Source https://www.insee.fr/fr/statistiques/6047743?sommaire=6047805
    En 2019, le revenu salarial annuel moyen dans le secteur privé et la fonction publique s’élève à 18_970 euros
    pour les femmes, soit un niveau inférieur de 22 % à celui des hommes (figure 1).
    Le revenu salarial médian des femmes est inférieur de 16 % à celui des hommes (figure 2).
    Cet écart s’amplifie à la fois dans les bas revenus (écart de 25 % pour le premier décile du revenu salarial) et
    dans les hauts revenus (écart de 21 % pour le neuvième décile).
    colonne 1: Revenu annuel Femmes moyen
    colonne 2: Revenu annuel Hommes moyen
    colonne 3: Revenu annuel Femmes moyen Écart relatif (en %)
    colonne 4: Salaire annuel Femmes moyen EQTP
    colonne 4: Salaire annuel Hommes moyen EQTP
    colonne 4: Salaire annuel Femmes moyen EQTP Écart relatif (en % EQTP)""",
    ),
    dict(
        label="france.histsalaires",
        category="Economics",
        source="""Inégalités salariales entre femmes et hommes de 1995 à 2019 (https://www.insee.fr/fr/)
Source https://www.insee.fr/fr/statistiques/6047743?sommaire=6047805

    colonne 1: Revenu annuel Femmes moyen
    colonne 2: Revenu annuel Hommes moyen
    colonne 3: Revenu annuel Femmes moyen Écart relatif (en %)
    colonne 4: Salaire annuel Femmes moyen EQTP
    colonne 4: Salaire annuel Hommes moyen EQTP
    colonne 4: Salaire annuel Femmes moyen EQTP Écart relatif (en % EQTP)""",
    ),
    dict(
        label="gmacro.fr_qgdp",
        category="Economics",
        source="""https://www.insee.fr/fr/statistiques/2830547#tableau-figure1
        Evolution du PIB et de ses composantes par rapport au trimestre precedent en volume en %
    nd : donnee non disponible.
    Note : donnees revistees ; les volumes sont mesures aux prix de l'annee precedente changés et corriges des variations saisonnieres et des effets des jours ouvrables.
    Lecture: au 4e trimestre 2022. le produit interieur brut (PIB) en volume augmente de 0.1 % par rapport au trimestre precedent.
    Source : Insee, comptes nationaux trimestriels - base 2014.
    Contributions Demande,Variations de stocks,Commerce exterieur""",
    ),
    dict(
        label="gmacro.fr_unemployement",
        category="Economics",
        source="""https://www.insee.fr/fr/statistiques/2830547#tableau-figure1""",
    ),
    dict(
        label="gmacro.us_gdp",
        category="Economics",
        source="""https://www.statsmodels.org/0.6.1/datasets/generated/macrodata.html""",
    ),
    dict(
        label="gmacro.fr_gdp",
        category="Economics",
        source="""https://www.insee.fr/""",
    ),
    dict(
        label="statsdata.scipy_distributions_list",
        category="Economics",
        source="""Scipy list of models""",
    ),
    dict(
        label="statsdata.oil",
        category="Economics",
        source="""Oil production in Saudi Arabia from 1996 to 2007
        https://www.statsmodels.org/stable/index.html
        """,
    ),
    dict(
        label="statsdata.air",
        category="Economics",
        source="""https://www.statsmodels.org/stable/index.html""",
    ),
    dict(
        label="statsdata.livestock2",
        category="Economics",
        source="""Forecasting livestock, sheep in Asia: comparing forecasting performance of non-seasonal methods.
        https://www.statsmodels.org/stable/index.html""",
    ),
    dict(
        label="statsdata.livestock3",
        category="Economics",
        source="""https://www.statsmodels.org/stable/index.html""",
    ),
    dict(
        label="statsdata.aust",
        category="Economics",
        source="""https://www.statsmodels.org/stable/index.html""",
    ),
    dict(
        label="statsdata.air_passengers",
        category="Economics",
        source="""https://www.statsmodels.org/stable/index.html""",
        raw_data="AirPassengers.csv",
    ),
    dict(
        label="statsdata.hhousing",
        category="Economics",
        source="""All-Transactions House Price Index for Houston
- Data source: https://fred.stlouisfed.org/series/ATNHPIUS26420Q
        """,
    ),
    dict(
        label="prices-split-adjusted",
        category="Economics",
        source="""Kaggle
https://github.com/kyi3081/stock-analysis
        """,
        raw_data="https://raw.githubusercontent.com/kyi3081/stock-analysis/master/prices-split-adjusted.csv",
    ),
    dict(
        label="fundamentals",
        category="Economics",
        source="""Kaggle
https://github.com/kyi3081/stock-analysis
        """,
        raw_data="https://raw.githubusercontent.com/kyi3081/stock-analysis/master/fundamentals.csv",
    ),
    dict(
        label="securities",
        category="Economics",
        source="""Kaggle
https://github.com/kyi3081/stock-analysis
        """,
        raw_data="https://raw.githubusercontent.com/kyi3081/stock-analysis/master/securities.csv",
    ),
    dict(
        label="trading.apple",
        category="Economics",
        source="""FPREP
        """,
        raw_data="APPLE_DownloadFPrepStatementQuarter.tsv",
    ),
    dict(
        label="continent",
        category="Economics",
        source="""iso m49 country information
Standardized country information
        """,
        raw_data="continent.tsv",
    ),
    dict(
        label="corruption",
        category="Economics",
        source="""Corruption index per country
        """,
        raw_data="corruption.csv",
    ),
    dict(
        label="cost_of_living",
        category="Economics",
        source="""country,cost_index,monthly_income,purchasing_power_index
        """,
        raw_data="cost_of_living.csv",
    ),
    dict(
        label="richest_countries",
        category="Economics",
        source="""country,gdp_per_capita
        """,
        raw_data="richest_countries.csv",
    ),
    dict(
        label="tourism",
        category="Economics",
        source="""country,tourists_in_millions,receipts_in_billions,receipts_per_tourist,percentage_of_gdp
        """,
        raw_data="tourism.csv",
    ),
    dict(
        label="unemployment",
        category="Economics",
        source="""country,unemployment_rate
        """,
        raw_data="unemployment.csv",
    ),
    dict(
        label="wages",
        category="Economics",
        source="""Simple synthetic data for exercice
        """,
        raw_data="wages.tsv",
    ),
    dict(
        label="COR_1",
        category="Economics",
        source="""COR
    """,
        raw_data="Données septembre partie 1.xlsx",
    ),
    dict(label="COR_2", reference="COR_1", raw_data="Données_RA2022_P2.xlsx"),
    dict(label="COR_2bis", reference="COR_1", raw_data="Données complémentaires partie 2 RA 2022.xlsx"),
    dict(label="COR_3", reference="COR_1", raw_data="Données septembre 2022 - partie 3.xlsx"),
    dict(label="COR_4", reference="COR_1", raw_data="Données_RA2022_P4.xlsx"),
    dict(label="COR_5", reference="COR_1", raw_data="Données septembre 2022 - partie 5.xlsx"),
    dict(
        label="supercomputers",
        category="Computing",
        raw_data="https://raw.githubusercontent.com/owid/owid-datasets/dd7a4ecbb249f98028e25c304ef7d68de8979ea9/datasets/Supercomputer%20power%20(FLOPS)%20%E2%80%93%20TOP500%20Database/Supercomputer%20power%20(FLOPS)%20%E2%80%93%20TOP500%20Database.csv",
        source="""Computational capacity of the fastest supercomputers
- Direct source: https://ourworldindata.org/grapher/supercomputer-power-flops
- Info columns: The number of floating-point operations per second (GigaFLOPS) by the fastest supercomputer in any given year
        """,
    ),
    dict(
        label="co2.concentrations",
        category="Climate",
        raw_data="climate-change.csv",
        source="""Data concentrations
- Data source: https://ourworldindata.org/atmospheric-concentrations
""",
        kwargs=dict(zone="World"),
    ),
    dict(label="co2.mapconcentrations", reference="co2.concentrations"),
    dict(
        label="co2.main",
        category="Climate",
        raw_data="https://raw.githubusercontent.com/owid/co2-data/master/owid-co2-data.csv",
        source="""Data on CO2 and Greenhouse Gas Emissions by Our World in Data
- Data source: https://raw.githubusercontent.com/owid/co2-data/master/owid-co2-data.csv
- Info columns: https://github.com/owid/co2-data/blob/master/owid-co2-codebook.csv
        """,
    ),
    dict(label="co2.mapmain", reference="co2.main"),
    dict(
        label="vaccinations",
        category="Health",
        raw_data="https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/vaccinations/vaccinations.csv",
        source="""Coronavirus Pandemic (COVID-19) data
- Direct source: https://ourworldindata.org/coronavirus
- Data source: https://covid19.who.int/data
- Info columns: https://github.com/owid/covid-19-data/tree/master/public/data/
""",
    ),
    dict(
        label="prostate",
        category="Health",
        raw_data="prostate.tsv",
        source="""https://hastie.su.domains/ElemStatLearn/data.html
        
columns: lcavol, lweight, age, lbph, svi, lcp, gleason, pgg45, [outcome]

lpsa train/test indicator (column 10) This last column indicates which 67 observations were used as the "training set" and which 30 as the test set, as described on page 48 in the book.
There was an error in these data in the first edition of this book. Subject 32 had a value of 6.1 for lweight, which translates to a 449 gm prostate! The correct value is 44.9 gm. We are grateful to Prof. Stephen W. Link for alerting us to this error.
The features must first be scaled to have mean zero and  variance 96 (=n) before the analyses in Tables 3.1 and beyond.  That is, if x is the  96 by 8 matrix of features, we compute xp <- scale(x,TRUE,TRUE)
""",
    ),
    dict(
        label="covid",
        category="Health",
        raw_data="https://covid.ourworldindata.org/data/owid-covid-data.csv",
        source="""Coronavirus Pandemic (COVID-19) data
- Direct source: https://ourworldindata.org/coronavirus
- Data source: https://covid19.who.int/data
- Info columns: https://github.com/owid/covid-19-data/tree/master/public/data/
""",
    ),
    dict(
        label="statsdata.sunspots",
        category="Physics",
        source="""Quarterly sunspots data (ssn)
- Direct source: https://www.swpc.noaa.gov/products/solar-cycle-progression
- Data source: https://services.swpc.noaa.gov/json/solar-cycle/observed-solar-cycle-indices.json
- Info columns: https://en.wikipedia.org/wiki/Wolf_number
        """,
        raw_data="https://services.swpc.noaa.gov/json/solar-cycle/observed-solar-cycle-indices.json",
    ),
    dict(
        label="co2.travel_mode",
        category="Climate",
        source="""Transportation info
https://ourworldindata.org/grapher/carbon-footprint-travel-mode
        """,
        raw_data="carbon-footprint-travel-mode.csv",
    ),
    dict(
        label="catvnoncat",
        category="IA",
        source="""Cat or not""",
        raw_data="train_catvnoncat.h5",
    ),
    dict(
        label="train_catvnoncat",
        category="IA",
        source="""Cat or not""",
        raw_data="train_catvnoncat.h5",
    ),
    dict(
        label="test_catvnoncat",
        category="IA",
        source="""Cat or not""",
        raw_data="test_catvnoncat.h5",
    ),
    dict(
        label="maintenance1",
        category="Maintenance",
        raw_data="https://raw.githubusercontent.com/shadgriffin/feature_engineering_equipment_failure/main/fe_equipment_failure_data_1.csv",
        source="""Bing bing""",
    ),
    dict(
        label="maintenance2",
        category="Maintenance",
        raw_data="https://raw.githubusercontent.com/shadgriffin/feature_engineering_equipment_failure/main/fe_equipment_failure_data_2.csv",
        source="""Bing bing""",
    ),
]


for f in (
    ["chose1.jpg", "chose2.jpg", "radian2.png", "README.md", "brown.gif", "gradient_descent.png", "TCL.png"]
    + ["lognormal.png", "in_trading.csv", "galton.jpg", "ffcontrol.csv", "galtonr.png"]
    + ["exercices", "freefight.csv"]
):
    datasets.append(dict(label=f, raw_data=f, category="Internal"))

ddatasets = {v["label"]: v for v in datasets}


for d in range(len(datasets)):
    if "reference" in datasets[d] and (lr := datasets[d]["reference"]) in ddatasets:
        datasets[d] = {**ddatasets[lr], **datasets[d]}
        ddatasets[datasets[d]["label"]] = datasets[d]
