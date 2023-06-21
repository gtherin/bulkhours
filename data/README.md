# Data

- [1. Economics](#Economics) 
- [2. Predictive maintenance](#Maintenance) 
- [3. Computing](#Computing) 
- [4. Physics](#Physics) 
- [5. Health](#Health) 
- [6. Climate Evolution](#Climate) 
- [7. Other Machine learning training data](#IA) 


### Economics 

#### `bulkhours.get_data("world.poverty")`
- Raw data: [pip_dataset.csv](https://nyc3.digitaloceanspaces.com/owid-public/data/poverty/pip_dataset.csv)
World Bank Poverty and Inequality Platform
- Direct source: https://ourworldindata.org/poverty
- Data source: https://pip.worldbank.org/
- Info columns: https://github.com/owid/poverty-data/blob/main/datasets/pip_codebook.csv
        
#### `bulkhours.get_data("world.mappoverty")`
- Raw data: [pip_dataset.csv](https://nyc3.digitaloceanspaces.com/owid-public/data/poverty/pip_dataset.csv)
World Bank Poverty and Inequality Platform
- Direct source: https://ourworldindata.org/poverty
- Data source: https://pip.worldbank.org/
- Info columns: https://github.com/owid/poverty-data/blob/main/datasets/pip_codebook.csv
        
#### `bulkhours.get_data("world.gdp")`
- Raw data: [pip_dataset.csv](https://nyc3.digitaloceanspaces.com/owid-public/data/poverty/pip_dataset.csv)
World Bank Poverty and Inequality Platform
- Direct source: https://ourworldindata.org/poverty
- Data source: https://pip.worldbank.org/
- Info columns: https://github.com/owid/poverty-data/blob/main/datasets/pip_codebook.csv
        
#### `bulkhours.get_data("world.mapgdp")`
- Raw data: [pip_dataset.csv](https://nyc3.digitaloceanspaces.com/owid-public/data/poverty/pip_dataset.csv)
World Bank Poverty and Inequality Platform
- Direct source: https://ourworldindata.org/poverty
- Data source: https://pip.worldbank.org/
- Info columns: https://github.com/owid/poverty-data/blob/main/datasets/pip_codebook.csv
        
#### `bulkhours.get_data("world.macro")`
- Rich data: [world.py](https://github.com/guydegnol/bulkhours/blob/main/bulkhours/data/world.py)
nope
#### `bulkhours.get_data("world.mapmacro")`
- Rich data: [world.py](https://github.com/guydegnol/bulkhours/blob/main/bulkhours/data/world.py)
nope
#### `bulkhours.get_data("world.corruption")`
- Rich data: [world.py](https://github.com/guydegnol/bulkhours/blob/main/bulkhours/data/world.py)
nope
#### `bulkhours.get_data("world.life_expectancy_vs_gdp_2018")`
- Raw data: [life-expectancy-vs-gdp-per-capita.csv](https://github.com/guydegnol/bulkhours/blob/main/data/life-expectancy-vs-gdp-per-capita.csv)
- Rich data: [world.py](https://github.com/guydegnol/bulkhours/blob/main/bulkhours/data/world.py)
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
        
#### `bulkhours.get_data("pyramide")`
- Raw data: [pyramide.tsv](https://github.com/guydegnol/bulkhours/blob/main/data/pyramide.tsv)
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
#### `bulkhours.get_data("statsdata.scipy_distributions_list")`
Scipy list of models
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
- Raw data: [AirPassengers.csv](https://github.com/guydegnol/bulkhours/blob/main/data/AirPassengers.csv)
https://www.statsmodels.org/stable/index.html
#### `bulkhours.get_data("statsdata.hhousing")`
All-Transactions House Price Index for Houston
- Data source: https://fred.stlouisfed.org/series/ATNHPIUS26420Q
        
#### `bulkhours.get_data("prices-split-adjusted")`
- Raw data: [prices-split-adjusted.csv](https://github.com/kyi3081/stock-analysis/master/prices-split-adjusted.csv)
Kaggle
https://github.com/kyi3081/stock-analysis
        
#### `bulkhours.get_data("fundamentals")`
- Raw data: [fundamentals.csv](https://github.com/kyi3081/stock-analysis/master/fundamentals.csv)
Kaggle
https://github.com/kyi3081/stock-analysis
        
#### `bulkhours.get_data("securities")`
- Raw data: [securities.csv](https://github.com/kyi3081/stock-analysis/master/securities.csv)
Kaggle
https://github.com/kyi3081/stock-analysis
        
#### `bulkhours.get_data("trading.apple")`
- Raw data: [APPLE_DownloadFPrepStatementQuarter.tsv](https://github.com/guydegnol/bulkhours/blob/main/data/APPLE_DownloadFPrepStatementQuarter.tsv)
FPREP
        
#### `bulkhours.get_data("continent")`
- Raw data: [continent.tsv](https://github.com/guydegnol/bulkhours/blob/main/data/continent.tsv)
iso m49 country information
Standardized country information
        
#### `bulkhours.get_data("corruption")`
- Raw data: [corruption.csv](https://github.com/guydegnol/bulkhours/blob/main/data/corruption.csv)
Corruption index per country
        
#### `bulkhours.get_data("cost_of_living")`
- Raw data: [cost_of_living.csv](https://github.com/guydegnol/bulkhours/blob/main/data/cost_of_living.csv)
country,cost_index,monthly_income,purchasing_power_index
        
#### `bulkhours.get_data("richest_countries")`
- Raw data: [richest_countries.csv](https://github.com/guydegnol/bulkhours/blob/main/data/richest_countries.csv)
country,gdp_per_capita
        
#### `bulkhours.get_data("tourism")`
- Raw data: [tourism.csv](https://github.com/guydegnol/bulkhours/blob/main/data/tourism.csv)
country,tourists_in_millions,receipts_in_billions,receipts_per_tourist,percentage_of_gdp
        
#### `bulkhours.get_data("unemployment")`
- Raw data: [unemployment.csv](https://github.com/guydegnol/bulkhours/blob/main/data/unemployment.csv)
country,unemployment_rate
        
#### `bulkhours.get_data("wages")`
- Raw data: [wages.tsv](https://github.com/guydegnol/bulkhours/blob/main/data/wages.tsv)
Simple synthetic data for exercice
        
#### `bulkhours.get_data("COR_1")`
- Raw data: [Données septembre partie 1.xlsx](https://github.com/guydegnol/bulkhours/blob/main/data/Données septembre partie 1.xlsx)
COR
    
#### `bulkhours.get_data("COR_2")`
- Raw data: [Données_RA2022_P2.xlsx](https://github.com/guydegnol/bulkhours/blob/main/data/Données_RA2022_P2.xlsx)
COR
    
#### `bulkhours.get_data("COR_2bis")`
- Raw data: [Données complémentaires partie 2 RA 2022.xlsx](https://github.com/guydegnol/bulkhours/blob/main/data/Données complémentaires partie 2 RA 2022.xlsx)
COR
    
#### `bulkhours.get_data("COR_3")`
- Raw data: [Données septembre 2022 - partie 3.xlsx](https://github.com/guydegnol/bulkhours/blob/main/data/Données septembre 2022 - partie 3.xlsx)
COR
    
#### `bulkhours.get_data("COR_4")`
- Raw data: [Données_RA2022_P4.xlsx](https://github.com/guydegnol/bulkhours/blob/main/data/Données_RA2022_P4.xlsx)
COR
    
#### `bulkhours.get_data("COR_5")`
- Raw data: [Données septembre 2022 - partie 5.xlsx](https://github.com/guydegnol/bulkhours/blob/main/data/Données septembre 2022 - partie 5.xlsx)
COR
    


### Maintenance 

#### `bulkhours.get_data("maintenance1")`
- Raw data: [fe_equipment_failure_data_1.csv](https://github.com/shadgriffin/feature_engineering_equipment_failure/main/fe_equipment_failure_data_1.csv)
Bing bing
#### `bulkhours.get_data("maintenance2")`
- Raw data: [fe_equipment_failure_data_2.csv](https://github.com/shadgriffin/feature_engineering_equipment_failure/main/fe_equipment_failure_data_2.csv)
Bing bing


### Computing 

#### `bulkhours.get_data("supercomputers")`
- Raw data: [Supercomputer%20power%20(FLOPS)%20%E2%80%93%20TOP500%20Database.csv](https://github.com/owid/owid-datasets/dd7a4ecbb249f98028e25c304ef7d68de8979ea9/datasets/Supercomputer%20power%20(FLOPS)%20%E2%80%93%20TOP500%20Database/Supercomputer%20power%20(FLOPS)%20%E2%80%93%20TOP500%20Database.csv)
Computational capacity of the fastest supercomputers
- Direct source: https://ourworldindata.org/grapher/supercomputer-power-flops
- Info columns: The number of floating-point operations per second (GigaFLOPS) by the fastest supercomputer in any given year
        


### Physics 


* <font size='+1'>Celsius en Kelvin: $273.15°K=0°C$</font><br/>```python
bkc.c2k=273.15  # K.C-1
bkc.kelvin=273.15  # K.C-1
```

* <font size='+1'>Celerité de la lumière: $c = 3 \cdot 10^{5}m\cdot s^{-1}$</font><br/>```python
bkc.c=3e+05  # m.s-1
bkc.vitesse_lumiere=3e+05  # m.s-1
```

* <font size='+1'>Distance parcourue par la lumière en 1an: $al = 9.461 \cdot 10^{15}m$</font><br/>```python
bkc.al=9.461e+15  # m
bkc.annee_lumiere=9.461e+15  # m
```

* <font size='+1'>Une Unité astrononique faisant un angle d'une seconde d'arc (déprécié): $1pc \equiv \frac{180\cdot60\cdot60}{\pi} = 3.086 \cdot 10^{16}m = 3.26al$</font><br/>```python
bkc.parsec=3.086e+16  # m.pc-1
```

* <font size='+1'>Une Unité astrononique faisant un angle d'une seconde d'arc (déprécié): $1kpc \equiv \frac{1000\cdot180\cdot60\cdot60}{\pi}$</font><br/>```python
bkc.kparsec=3.086e+19  # m.kpc-1
```

* <font size='+1'>Constante de la gravitation: $G = 6.67 \cdot 10^{-11}N\cdot m^2\cdot kg^{-2}$   [6.6743e-11N.m2.kg-2]</font><br/>```python
bkc.G=6.67e-11  # N.m2.kg-2
```

* <font size='+1'>Acceleration standard de la gravitation: $g = 9.8m\cdot s^{-2}$   [9.80665m.s-2]</font><br/>```python
bkc.g=9.8  # m.s-2
```

* <font size='+1'>Constante de Planck: $h = 6.626 \cdot 10^{-34}J\cdot s$   [6.62607015e-34J.s]</font><br/>```python
bkc.h=6.626e-34  # J.s
```

* <font size='+1'>: $\bar{h} = \frac{h}{2\pi}$</font><br/>```python
bkc.hbar=1.055e-34  # J.s
```

* <font size='+1'>Nombre d'Avogadro: $N_\mathcal{A} = 6.02 \cdot 10^{23}mol-1$ (Carbone: $12g\Leftrightarrow 1mol$)</font><br/>```python
bkc.N_A=6.02e+23  # mol-1
bkc.A=6.02e+23  # mol-1
```

* <font size='+1'>Constante de Stefan-Boltzmann: $\sigma = 5.67 \cdot 10^{-8} W\cdot m^{-2}\cdot K^{-4}$</font><br/>```python
bkc.sigma=5.67e-08  # W.m-2.K-4
bkc.stefan=5.67e-08  # W.m-2.K-4
```

* <font size='+1'>Constante de Wien: $\lambda_{\text{max}} \cdot T = 0.003m\cdot K$   [0.002897771955m.K]</font><br/>```python
bkc.Wien=0.003  # m.K
bkc.wien=0.003  # m.K
bkc.lambda_max=0.003  # m.K
```

* <font size='+1'>Constante de Rydberg: $R_H({\text{Hydrogene}}) = 1.1 \cdot 10^{7}m-1$</font><br/>```python
bkc.Rydberg=1.1e+07  # m-1
bkc.rydberg=1.1e+07  # m-1
bkc.R_H=1.1e+07  # m-1
```

* <font size='+1'>Energie cinetique e sous 1Volt: $\mathrm{eV} = 1.6 \cdot 10^{-19}J\cdot eV^{-1}$   [1.602176634e-19J.eV-1]</font><br/>```python
bkc.eV=1.6e-19  # J.eV-1
bkc.ev=1.6e-19  # J.eV-1
```

* <font size='+1'>Masse electron: $m_e = 9.109 \cdot 10^{-31}kg$   [9.1093837015e-31kg]</font><br/>```python
bkc.m_e=9.109e-31  # kg
```

* <font size='+1'>Rayon de Bohr: $a = 5.3 \cdot 10^{-11} m$</font><br/>```python
bkc.r_bohr=5.300e-11  # m
bkc.a=5.300e-11  # m
```

* <font size='+1'>Masse proton: $m_p = 1.673 \cdot 10^{-27}kg$   [1.67262192369e-27kg]</font><br/>```python
bkc.m_p=1.673e-27  # kg
```

* <font size='+1'>Masse proton: $m_p = 1.007276uma$ ($1uma \equiv \frac{M(^{12}C)}{12}$)   [1.007276466621uma]</font><br/>```python
bkc.m_puma=1.007276  # uma
```

* <font size='+1'>Masse neutron: $m_n = 1.008663uma$ ($1uma \equiv \frac{M(^{12}C)}{12}$)   [1.00866491595uma]</font><br/>```python
bkc.m_numa=1.008663  # uma
```

* <font size='+1'>Unité de Masse Atomique: $m_{nuc} = 1.660 \cdot 10^{-27}kg\cdot uma^{-1}$ ($1uma \equiv \frac{M(^{12}C)}{12}$)   [1.6605390666e-27kg.uma-1]</font><br/>```python
bkc.uma=1.660e-27  # kg.uma-1
```

* <font size='+1'>Unité de Masse Atomique (MeV): $m_{nuc} = 931.500MeV\cdot uma^{-1}$ ($1uma \equiv \frac{M(^{12}C)}{12}$)</font><br/>```python
bkc.uma_mev=931.500  # MeV.uma-1
```

* <font size='+1'>Masse: $M_{\mathrm{mercure}} = 3.301 \cdot 10^{23}kg$</font><br/>```python
bkc.M_mercure=3.301e+23  # kg
```

* <font size='+1'>Distance au soleil: $d_{\odot \mathrm{mercure}} = 0.38ua$</font><br/>```python
bkc.d_mercure=0.38  # ua
```

* <font size='+1'>Rayon: $R_{\mathrm{mercure}} = 2439km$</font><br/>```python
bkc.R_mercure=2439  # km
```

* <font size='+1'>Albedo: $A_{\mathrm{mercure}} = 0.09$</font><br/>```python
bkc.A_mercure=0.09  # Sans unité (entre 0 et 1)
```

* <font size='+1'>Effet de serre: $S_{\mathrm{mercure}} = 0$</font><br/>```python
bkc.S_mercure=0  # Sans unité (entre 0 et 1)
```

* <font size='+1'>Temperature moyenne: $T_{\mathrm{mercure}} = 167.0°C$</font><br/>```python
bkc.T_mercure=167.0  # °C
```

* <font size='+1'>Masse: $M_{\mathrm{venus}} = 4.867 \cdot 10^{24}kg$</font><br/>```python
bkc.M_venus=4.867e+24  # kg
```

* <font size='+1'>Distance au soleil: $d_{\odot \mathrm{venus}} = 0.72ua$</font><br/>```python
bkc.d_venus=0.72  # ua
```

* <font size='+1'>Rayon: $R_{\mathrm{venus}} = 3390km$</font><br/>```python
bkc.R_venus=3390  # km
```

* <font size='+1'>Albedo: $A_{\mathrm{venus}} = 0.77$</font><br/>```python
bkc.A_venus=0.77  # Sans unité (entre 0 et 1)
```

* <font size='+1'>Effet de serre: $S_{\mathrm{venus}} = 0.991$</font><br/>```python
bkc.S_venus=0.991  # Sans unité (entre 0 et 1)
```

* <font size='+1'>Temperature moyenne: $T_{\mathrm{venus}} = 464.0°C$</font><br/>```python
bkc.T_venus=464.0  # °C
```

* <font size='+1'>Masse: $M_{\mathrm{terre}} = 5.972 \cdot 10^{24}kg$</font><br/>```python
bkc.M_terre=5.972e+24  # kg
```

* <font size='+1'>Distance au soleil: $d_{\odot \mathrm{terre}} = 1.00ua$</font><br/>```python
bkc.d_terre=1.00  # ua
```

* <font size='+1'>Rayon: $R_{\mathrm{terre}} = 6371km$</font><br/>```python
bkc.R_terre=6371  # km
```

* <font size='+1'>Albedo: $A_{\mathrm{terre}} = 0.30$</font><br/>```python
bkc.A_terre=0.30  # Sans unité (entre 0 et 1)
```

* <font size='+1'>Effet de serre: $S_{\mathrm{terre}} = 0.394$</font><br/>```python
bkc.S_terre=0.394  # Sans unité (entre 0 et 1)
```

* <font size='+1'>Temperature moyenne: $T_{\mathrm{terre}} = 15.0°C$</font><br/>```python
bkc.T_terre=15.0  # °C
```

* <font size='+1'>Distance au soleil: $d_{\odot \mathrm{terre}} = 1ua = 1.500 \cdot 10^{11}m$   [149597870700.0m]</font><br/>```python
bkc.d_terre_solm=1.500e+11  # m
bkc.d_terresoleil=1.500e+11  # m
```

* <font size='+1'>Masse: $M_{\mathrm{mars}} = 6.417 \cdot 10^{23}kg$</font><br/>```python
bkc.M_mars=6.417e+23  # kg
```

* <font size='+1'>Distance au soleil: $d_{\odot \mathrm{mars}} = 1.52ua$</font><br/>```python
bkc.d_mars=1.52  # ua
```

* <font size='+1'>Rayon: $R_{\mathrm{mars}} = 3390km$</font><br/>```python
bkc.R_mars=3390  # km
```

* <font size='+1'>Albedo: $A_{\mathrm{mars}} = 0.25$</font><br/>```python
bkc.A_mars=0.25  # Sans unité (entre 0 et 1)
```

* <font size='+1'>Effet de serre: $S_{\mathrm{mars}} = 0.010$</font><br/>```python
bkc.S_mars=0.010  # Sans unité (entre 0 et 1)
```

* <font size='+1'>Temperature moyenne: $T_{\mathrm{mars}} = -62.8°C$</font><br/>```python
bkc.T_mars=-62.8  # °C
```

* <font size='+1'>Masse: $M_{\odot} = 1.988 \cdot 10^{30}kg$</font><br/>```python
bkc.M_soleil=1.988e+30  # kg
```

* <font size='+1'>Rayon: $R_{\odot} = 7 \cdot 10^{5}km$</font><br/>```python
bkc.R_soleil=7e+05  # km
```

* <font size='+1'>Luminosité: $L_{\odot} = 3.83 \cdot 10^{26}W$</font><br/>```python
bkc.L_soleil=3.83e+26  # W
bkc.L_sol=3.83e+26  # W
bkc.L_sun=3.83e+26  # W
```

* <font size='+1'>Temperature moyenne: $T_{\odot} = 5800.0°C$</font><br/>```python
bkc.T_soleil=5800.0  # °C
```

* <font size='+1'>Masse: $M_{\mathrm{lune}} = 7.350 \cdot 10^{22}kg$</font><br/>```python
bkc.M_lune=7.350e+22  # kg
```

* <font size='+1'>Distance au soleil: $d_{\odot \mathrm{lune}} = 1.00ua$</font><br/>```python
bkc.d_lune=1.00  # ua
```

* <font size='+1'>Rayon: $R_{\mathrm{lune}} = 6371km$</font><br/>```python
bkc.R_lune=6371  # km
```

* <font size='+1'>Albedo: $A_{\mathrm{lune}} = 0.11$</font><br/>```python
bkc.A_lune=0.11  # Sans unité (entre 0 et 1)
```

* <font size='+1'>Distance à la lune: $d_{\mathrm{terre} \mathrm{lune}} = 3.844 \cdot 10^{8}$</font><br/>```python
bkc.d_terre_lune=3.844e+08  # 
```

* <font size='+1'>: $pi = 3.141593$</font><br/>```python
bkc.pi=3.141593  # 
```

#### `bulkhours.get_data("statsdata.sunspots")`
- Raw data: [observed-solar-cycle-indices.json](https://services.swpc.noaa.gov/json/solar-cycle/observed-solar-cycle-indices.json)
Quarterly sunspots data (ssn)
- Direct source: https://www.swpc.noaa.gov/products/solar-cycle-progression
- Data source: https://services.swpc.noaa.gov/json/solar-cycle/observed-solar-cycle-indices.json
- Info columns: https://en.wikipedia.org/wiki/Wolf_number
        


### Health 

#### `bulkhours.get_data("vaccinations")`
- Raw data: [vaccinations.csv](https://github.com/owid/covid-19-data/master/public/data/vaccinations/vaccinations.csv)
Coronavirus Pandemic (COVID-19) data
- Direct source: https://ourworldindata.org/coronavirus
- Data source: https://covid19.who.int/data
- Info columns: https://github.com/owid/covid-19-data/tree/master/public/data/

#### `bulkhours.get_data("prostate")`
- Raw data: [prostate.tsv](https://github.com/guydegnol/bulkhours/blob/main/data/prostate.tsv)
https://hastie.su.domains/ElemStatLearn/data.html
        
columns: lcavol, lweight, age, lbph, svi, lcp, gleason, pgg45, [outcome]

lpsa train/test indicator (column 10) This last column indicates which 67 observations were used as the "training set" and which 30 as the test set, as described on page 48 in the book.
There was an error in these data in the first edition of this book. Subject 32 had a value of 6.1 for lweight, which translates to a 449 gm prostate! The correct value is 44.9 gm. We are grateful to Prof. Stephen W. Link for alerting us to this error.
The features must first be scaled to have mean zero and  variance 96 (=n) before the analyses in Tables 3.1 and beyond.  That is, if x is the  96 by 8 matrix of features, we compute xp <- scale(x,TRUE,TRUE)

#### `bulkhours.get_data("covid")`
- Raw data: [owid-covid-data.csv](https://covid.ourworldindata.org/data/owid-covid-data.csv)
Coronavirus Pandemic (COVID-19) data
- Direct source: https://ourworldindata.org/coronavirus
- Data source: https://covid19.who.int/data
- Info columns: https://github.com/owid/covid-19-data/tree/master/public/data/



### Climate 

#### `bulkhours.get_data("co2.concentrations")`
- Raw data: [climate-change.csv](https://github.com/guydegnol/bulkhours/blob/main/data/climate-change.csv)
Data concentrations
- Data source: https://ourworldindata.org/atmospheric-concentrations

#### `bulkhours.get_data("co2.mapconcentrations")`
- Raw data: [climate-change.csv](https://github.com/guydegnol/bulkhours/blob/main/data/climate-change.csv)
Data concentrations
- Data source: https://ourworldindata.org/atmospheric-concentrations

#### `bulkhours.get_data("co2.main")`
- Raw data: [owid-co2-data.csv](https://github.com/owid/co2-data/master/owid-co2-data.csv)
Data on CO2 and Greenhouse Gas Emissions by Our World in Data
- Data source: https://raw.githubusercontent.com/owid/co2-data/master/owid-co2-data.csv
- Info columns: https://github.com/owid/co2-data/blob/master/owid-co2-codebook.csv
        
#### `bulkhours.get_data("co2.mapmain")`
- Raw data: [owid-co2-data.csv](https://github.com/owid/co2-data/master/owid-co2-data.csv)
Data on CO2 and Greenhouse Gas Emissions by Our World in Data
- Data source: https://raw.githubusercontent.com/owid/co2-data/master/owid-co2-data.csv
- Info columns: https://github.com/owid/co2-data/blob/master/owid-co2-codebook.csv
        
#### `bulkhours.get_data("co2.travel_mode")`
- Raw data: [carbon-footprint-travel-mode.csv](https://github.com/guydegnol/bulkhours/blob/main/data/carbon-footprint-travel-mode.csv)
Transportation info
https://ourworldindata.org/grapher/carbon-footprint-travel-mode
        


### IA 

#### `bulkhours.get_data("catvnoncat")`
- Raw data: [train_catvnoncat.h5](https://github.com/guydegnol/bulkhours/blob/main/data/train_catvnoncat.h5)
Cat or not
#### `bulkhours.get_data("train_catvnoncat")`
- Raw data: [train_catvnoncat.h5](https://github.com/guydegnol/bulkhours/blob/main/data/train_catvnoncat.h5)
Cat or not
#### `bulkhours.get_data("test_catvnoncat")`
- Raw data: [test_catvnoncat.h5](https://github.com/guydegnol/bulkhours/blob/main/data/test_catvnoncat.h5)
Cat or not
