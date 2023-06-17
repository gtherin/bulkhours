# Data<a name="data"></a>

1. [Economics](#Economics)
2. [Predictive maintenance](#Maintenance)
3. [Computing](#Computing)
4. [Physics](#Physics)
5. [Health](#Health)
6. [Climate Evolution](#Climate)
7. [Other Machine learning training data](#IA)


### 1. Economics<a name="Economics"></a>

#### `bulkhours.get_data("world.poverty")`
World Bank Poverty and Inequality Platform
- Direct source: [securities.csv](securities.csv)
- Direct source: [a workaround link](repo/blob/main/README.md)
- Direct source: [a workaround link](bulkhours/blob/main/README.md)

- Direct source: https://ourworldindata.org/poverty
- Data source: https://pip.worldbank.org/
- Info columns: https://github.com/owid/poverty-data/blob/main/datasets/pip_codebook.csv
        
#### `bulkhours.get_data("world.mappoverty")`
Same as previous, with extra gps information
#### `bulkhours.get_data("world.gdp")`
World Bank Poverty and Inequality Platform
- Direct source: https://ourworldindata.org/poverty
- Data source: https://pip.worldbank.org/
- Info columns: https://github.com/owid/poverty-data/blob/main/datasets/pip_codebook.csv
        
#### `bulkhours.get_data("world.mapgdp")`
Same as previous, with extra gps information
#### `bulkhours.get_data("world.macro")`
Nope
#### `bulkhours.get_data("world.mapmacro")`
Same as previous, with extra gps information
#### `bulkhours.get_data("world.corruption")`
Nope
#### `bulkhours.get_data("scipy_distributions_list")`
Scipy list of models
#### `bulkhours.get_data("macro")`
nope
#### `bulkhours.get_data("life_expectancy_vs_gdp_2018")`
Life expectancy versus GDP/capita per country
- Direct source: https://ourworldindata.org/grapher/life-expectancy-vs-gdp-per-capita
- Data source: Maddison Project Database (2020); UN WPP (2022); Zijdeman et al. (2015)
- Info columns: GDP per capita is measured in 2011 international dollars, which corrects for inflation and cross-country price differences
        
#### `bulkhours.get_data("mincer.stats")`
Descriptive statistics of hourly wages in selected EU countries in 2010 (in PPS) 
Table 2: https://www.nbp.pl/publikacje/materialy_i_studia/226_en.pdf
    
#### `bulkhours.get_data("mincer.params")`
ln(hourly_wage) = alpha_0i + alpha_1i * edu + alpha_2i * age + alpha_3i * age**2
Table 3. https://www.nbp.pl/publikacje/materialy_i_studia/226_en.pdf
The results of estimation of parameters in Mincer equations in a set of countries. We
put the point estimates, standard errors (in italics) and p-values for zero restriction test of a
particular parameter (in square brackets)        
        
#### `bulkhours.get_data("france.pyramide")`
Age de la population au 1er janvier ; données provisoires arrêtées à fin novembre 2022 (https://www.insee.fr/fr/)
Lecture : au 1er janvier 2023, la France compte 805 914 personnes de 65 ans dont 425 143 femmes et 380 771 hommes. Champ : France.
    Source : https://www.insee.fr/fr/statistiques/2381472#tableau-figure1
    
#### `bulkhours.get_data("france.retraites")`
Salaires mensuels nets en équivalent temps plein (EQTP) en 2020 (https://www.insee.fr/fr/)
        Source https://www.insee.fr/fr/statistiques/2415121#tableau-figure1

        Distribution des salaires mensuels nets en équivalent temps plein (EQTP) en 2020

    Note : certains salaires en EQTP sont inférieurs au Smic ; ceci est en effet permis par certains statuts. Cependant, l'existence de rémunérations inférieures au Smic peut aussi provenir d’incohérences entre salaires et durées travaillées dans les déclarations administratives, qui ne peuvent être toutes redressées.
    Lecture : en 2020, en EQTP, 50 % des salariés gagnent plus de 2 005 euros.
    Champ : France hors Mayotte, salariés du privé et des entreprises publiques, y compris bénéficiaires de contrats aidés et de contrats de professionnalisation ; hors apprentis, stagiaires, salariés agricoles et salariés des particuliers employeurs.
    
#### `bulkhours.get_data("france.income")`
Distribution des salaires mensuels nets en équivalent temps plein (EQTP) en 2020 (https://www.insee.fr/fr/)
        Source https://www.insee.fr/fr/statistiques/6436313#tableau-figure2
      - Note : certains salaires en EQTP sont inférieurs au Smic ; ceci est en effet permis par certains statuts.
    Cependant, l'existence de rémunérations inférieures au Smic peut aussi provenir d’incohérences entre salaires et durées travaillées dans
    les déclarations administratives, qui ne peuvent être toutes redressées.
      - Lecture : en 2020, en EQTP, 50 % des salariés gagnent plus de 2 005 euros.
    Champ : France hors Mayotte, salariés du privé et des entreprises publiques, y compris bénéficiaires de contrats aidés et
    de contrats de professionnalisation ; hors apprentis, stagiaires, salariés agricoles et salariés des particuliers employeurs.
    
#### `bulkhours.get_data("france.salaires")`
Revenu salarial et salaire en EQTP annuels moyens selon le sexe en 2019 (https://www.insee.fr/fr/)
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
    colonne 4: Salaire annuel Femmes moyen EQTP Écart relatif (en % EQTP)
#### `bulkhours.get_data("france.histsalaires")`
Inégalités salariales entre femmes et hommes de 1995 à 2019 (https://www.insee.fr/fr/)
Source https://www.insee.fr/fr/statistiques/6047743?sommaire=6047805

    colonne 1: Revenu annuel Femmes moyen
    colonne 2: Revenu annuel Hommes moyen
    colonne 3: Revenu annuel Femmes moyen Écart relatif (en %)
    colonne 4: Salaire annuel Femmes moyen EQTP
    colonne 4: Salaire annuel Hommes moyen EQTP
    colonne 4: Salaire annuel Femmes moyen EQTP Écart relatif (en % EQTP)
#### `bulkhours.get_data("gmacro.fr_qgdp")`
https://www.insee.fr/fr/statistiques/2830547#tableau-figure1
        Evolution du PIB et de ses composantes par rapport au trimestre precedent en volume en %
    nd : donnee non disponible.
    Note : donnees revistees ; les volumes sont mesures aux prix de l'annee precedente changés et corriges des variations saisonnieres et des effets des jours ouvrables.
    Lecture: au 4e trimestre 2022. le produit interieur brut (PIB) en volume augmente de 0.1 % par rapport au trimestre precedent.
    Source : Insee, comptes nationaux trimestriels - base 2014.
    Contributions Demande,Variations de stocks,Commerce exterieur
#### `bulkhours.get_data("gmacro.fr_unemployement")`
https://www.insee.fr/fr/statistiques/2830547#tableau-figure1
#### `bulkhours.get_data("gmacro.us_gdp")`
https://www.statsmodels.org/0.6.1/datasets/generated/macrodata.html
#### `bulkhours.get_data("gmacro.fr_gdp")`
https://www.insee.fr/
#### `bulkhours.get_data("statsdata.oil")`
Oil production in Saudi Arabia from 1996 to 2007
        https://www.statsmodels.org/stable/index.html
        
#### `bulkhours.get_data("statsdata.air")`
https://www.statsmodels.org/stable/index.html
#### `bulkhours.get_data("statsdata.livestock2")`
Forecasting livestock, sheep in Asia: comparing forecasting performance of non-seasonal methods.
        https://www.statsmodels.org/stable/index.html
#### `bulkhours.get_data("statsdata.livestock3")`
https://www.statsmodels.org/stable/index.html
#### `bulkhours.get_data("statsdata.aust")`
https://www.statsmodels.org/stable/index.html
#### `bulkhours.get_data("statsdata.air_passengers")`
https://www.statsmodels.org/stable/index.html
#### `bulkhours.get_data("statsdata.hhousing")`
All-Transactions House Price Index for Houston
- Data source: https://fred.stlouisfed.org/series/ATNHPIUS26420Q
        
#### `bulkhours.get_data("trading.apple")`
FPREP
        
