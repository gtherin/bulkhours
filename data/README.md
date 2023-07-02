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

<details>
  <summary>Show columns info</summary>
> https://github.com/owid/poverty-data/blob/main/datasets/pip_codebook.csv

| Column   |      Info |
|-----------|:-----------|
| country |  |
| year |  |
| reporting_level |  |
| welfare_type |  |
| ppp_version |  |
| survey_year |  |
| survey_comparability |  |
| headcount_ratio_international_povline |  |
| headcount_ratio_lower_mid_income_povline |  |
| headcount_ratio_upper_mid_income_povline |  |
| headcount_ratio_100 |  |
| headcount_ratio_1000 |  |
| headcount_ratio_2000 |  |
| headcount_ratio_3000 |  |
| headcount_ratio_4000 |  |
| headcount_ratio_40_median |  |
| headcount_ratio_50_median |  |
| headcount_ratio_60_median |  |
| headcount_international_povline |  |
| headcount_lower_mid_income_povline |  |
| headcount_upper_mid_income_povline |  |
| headcount_100 |  |
| headcount_1000 |  |
| headcount_2000 |  |
| headcount_3000 |  |
| headcount_4000 |  |
| headcount_40_median |  |
| headcount_50_median |  |
| headcount_60_median |  |
| avg_shortfall_international_povline |  |
| avg_shortfall_lower_mid_income_povline |  |
| avg_shortfall_upper_mid_income_povline |  |
| avg_shortfall_100 |  |
| avg_shortfall_1000 |  |
| avg_shortfall_2000 |  |
| avg_shortfall_3000 |  |
| avg_shortfall_4000 |  |
| avg_shortfall_40_median |  |
| avg_shortfall_50_median |  |
| avg_shortfall_60_median |  |
| total_shortfall_international_povline |  |
| total_shortfall_lower_mid_income_povline |  |
| total_shortfall_upper_mid_income_povline |  |
| total_shortfall_100 |  |
| total_shortfall_1000 |  |
| total_shortfall_2000 |  |
| total_shortfall_3000 |  |
| total_shortfall_4000 |  |
| total_shortfall_40_median |  |
| total_shortfall_50_median |  |
| total_shortfall_60_median |  |
| income_gap_ratio_international_povline |  |
| income_gap_ratio_lower_mid_income_povline |  |
| income_gap_ratio_upper_mid_income_povline |  |
| income_gap_ratio_100 |  |
| income_gap_ratio_1000 |  |
| income_gap_ratio_2000 |  |
| income_gap_ratio_3000 |  |
| income_gap_ratio_4000 |  |
| income_gap_ratio_40_median |  |
| income_gap_ratio_50_median |  |
| income_gap_ratio_60_median |  |
| poverty_gap_index_international_povline |  |
| poverty_gap_index_lower_mid_income_povline |  |
| poverty_gap_index_upper_mid_income_povline |  |
| poverty_gap_index_100 |  |
| poverty_gap_index_1000 |  |
| poverty_gap_index_2000 |  |
| poverty_gap_index_3000 |  |
| poverty_gap_index_4000 |  |
| mean |  |
| median |  |
| decile1_avg |  |
| decile2_avg |  |
| decile3_avg |  |
| decile4_avg |  |
| decile5_avg |  |
| decile6_avg |  |
| decile7_avg |  |
| decile8_avg |  |
| decile9_avg |  |
| decile10_avg |  |
| decile1_share |  |
| decile2_share |  |
| decile3_share |  |
| decile4_share |  |
| decile5_share |  |
| decile6_share |  |
| decile7_share |  |
| decile8_share |  |
| decile9_share |  |
| decile10_share |  |
| decile1_thr |  |
| decile2_thr |  |
| decile3_thr |  |
| decile4_thr |  |
| decile6_thr |  |
| decile7_thr |  |
| decile8_thr |  |
| decile9_thr |  |
| gini |  |
| mld |  |
| polarization |  |
| palma_ratio |  |
| s80_s20_ratio |  |
| p90_p10_ratio |  |
| p90_p50_ratio |  |
| p50_p10_ratio |  |
| index |  |
| iso |  |
| m49 |  |
| region1 |  |
| region2 |  |
| continent |  |

</details>
         
#### World Bank Poverty and Inequality data (with gpx extra info)
#### `bulkhours.get_data("world.mappoverty")`
- Raw data: [pip_dataset.csv](https://nyc3.digitaloceanspaces.com/owid-public/data/poverty/pip_dataset.csv)  ([raw](https://nyc3.digitaloceanspaces.com/owid-public/data/poverty/pip_dataset.csv))
- Enrich data: [world.py](https://github.com/guydegnol/bulkhours/blob/main/bulkhours/data/world.py)  ([raw](https://raw.githubusercontent.com/guydegnol/bulkhours/main/bulkhours/data/world.py))
- Direct source: https://ourworldindata.org/poverty
- Reference site: https://pip.worldbank.org/

<details>
  <summary>Show columns info</summary>
> https://github.com/owid/poverty-data/blob/main/datasets/pip_codebook.csv

| Column   |      Info |
|-----------|:-----------|
| pop_est |  |
| continent |  |
| name |  |
| iso_a3 |  |
| gdp_md_est |  |
| geometry |  |
| year |  |
| reporting_level |  |
| welfare_type |  |
| ppp_version |  |
| survey_year |  |
| survey_comparability |  |
| headcount_ratio_international_povline |  |
| headcount_ratio_lower_mid_income_povline |  |
| headcount_ratio_upper_mid_income_povline |  |
| headcount_ratio_100 |  |
| headcount_ratio_1000 |  |
| headcount_ratio_2000 |  |
| headcount_ratio_3000 |  |
| headcount_ratio_4000 |  |
| headcount_ratio_40_median |  |
| headcount_ratio_50_median |  |
| headcount_ratio_60_median |  |
| headcount_international_povline |  |
| headcount_lower_mid_income_povline |  |
| headcount_upper_mid_income_povline |  |
| headcount_100 |  |
| headcount_1000 |  |
| headcount_2000 |  |
| headcount_3000 |  |
| headcount_4000 |  |
| headcount_40_median |  |
| headcount_50_median |  |
| headcount_60_median |  |
| avg_shortfall_international_povline |  |
| avg_shortfall_lower_mid_income_povline |  |
| avg_shortfall_upper_mid_income_povline |  |
| avg_shortfall_100 |  |
| avg_shortfall_1000 |  |
| avg_shortfall_2000 |  |
| avg_shortfall_3000 |  |
| avg_shortfall_4000 |  |
| avg_shortfall_40_median |  |
| avg_shortfall_50_median |  |
| avg_shortfall_60_median |  |
| total_shortfall_international_povline |  |
| total_shortfall_lower_mid_income_povline |  |
| total_shortfall_upper_mid_income_povline |  |
| total_shortfall_100 |  |
| total_shortfall_1000 |  |
| total_shortfall_2000 |  |
| total_shortfall_3000 |  |
| total_shortfall_4000 |  |
| total_shortfall_40_median |  |
| total_shortfall_50_median |  |
| total_shortfall_60_median |  |
| income_gap_ratio_international_povline |  |
| income_gap_ratio_lower_mid_income_povline |  |
| income_gap_ratio_upper_mid_income_povline |  |
| income_gap_ratio_100 |  |
| income_gap_ratio_1000 |  |
| income_gap_ratio_2000 |  |
| income_gap_ratio_3000 |  |
| income_gap_ratio_4000 |  |
| income_gap_ratio_40_median |  |
| income_gap_ratio_50_median |  |
| income_gap_ratio_60_median |  |
| poverty_gap_index_international_povline |  |
| poverty_gap_index_lower_mid_income_povline |  |
| poverty_gap_index_upper_mid_income_povline |  |
| poverty_gap_index_100 |  |
| poverty_gap_index_1000 |  |
| poverty_gap_index_2000 |  |
| poverty_gap_index_3000 |  |
| poverty_gap_index_4000 |  |
| mean |  |
| median |  |
| decile1_avg |  |
| decile2_avg |  |
| decile3_avg |  |
| decile4_avg |  |
| decile5_avg |  |
| decile6_avg |  |
| decile7_avg |  |
| decile8_avg |  |
| decile9_avg |  |
| decile10_avg |  |
| decile1_share |  |
| decile2_share |  |
| decile3_share |  |
| decile4_share |  |
| decile5_share |  |
| decile6_share |  |
| decile7_share |  |
| decile8_share |  |
| decile9_share |  |
| decile10_share |  |
| decile1_thr |  |
| decile2_thr |  |
| decile3_thr |  |
| decile4_thr |  |
| decile6_thr |  |
| decile7_thr |  |
| decile8_thr |  |
| decile9_thr |  |
| gini |  |
| mld |  |
| polarization |  |
| palma_ratio |  |
| s80_s20_ratio |  |
| p90_p10_ratio |  |
| p90_p50_ratio |  |
| p50_p10_ratio |  |
| index |  |
| iso |  |
| m49 |  |
| region1 |  |
| region2 |  |

</details>
         
#### World Bank Gdp data
#### `bulkhours.get_data("world.gdp")`
- Raw data: [pip_dataset.csv](https://nyc3.digitaloceanspaces.com/owid-public/data/poverty/pip_dataset.csv)  ([raw](https://nyc3.digitaloceanspaces.com/owid-public/data/poverty/pip_dataset.csv))
- Enrich data: [world.py](https://github.com/guydegnol/bulkhours/blob/main/bulkhours/data/world.py)  ([raw](https://raw.githubusercontent.com/guydegnol/bulkhours/main/bulkhours/data/world.py))
- Direct source: https://ourworldindata.org/poverty
- Reference site: https://pip.worldbank.org/

<details>
  <summary>Show columns info</summary>
> https://github.com/owid/poverty-data/blob/main/datasets/pip_codebook.csv

| Column   |      Info |
|-----------|:-----------|
| country |  |
| year |  |
| gdp |  |
| index |  |
| iso |  |
| m49 |  |
| region1 |  |
| region2 |  |
| continent |  |

</details>
         
#### World Bank Gdp data (with gpx extra info)
#### `bulkhours.get_data("world.mapgdp")`
- Raw data: [pip_dataset.csv](https://nyc3.digitaloceanspaces.com/owid-public/data/poverty/pip_dataset.csv)  ([raw](https://nyc3.digitaloceanspaces.com/owid-public/data/poverty/pip_dataset.csv))
- Enrich data: [world.py](https://github.com/guydegnol/bulkhours/blob/main/bulkhours/data/world.py)  ([raw](https://raw.githubusercontent.com/guydegnol/bulkhours/main/bulkhours/data/world.py))
- Direct source: https://ourworldindata.org/poverty
- Reference site: https://pip.worldbank.org/

<details>
  <summary>Show columns info</summary>
> https://github.com/owid/poverty-data/blob/main/datasets/pip_codebook.csv

| Column   |      Info |
|-----------|:-----------|
| pop_est |  |
| continent |  |
| name |  |
| iso_a3 |  |
| gdp_md_est |  |
| geometry |  |
| year |  |
| gdp |  |
| index |  |
| iso |  |
| m49 |  |
| region1 |  |
| region2 |  |

</details>
         
#### Global economic data
#### `bulkhours.get_data("world.macro")`
- Raw data: [corruption.csv](https://github.com/guydegnol/bulkhours/blob/main/data/corruption.csv), [cost_of_living.csv](https://github.com/guydegnol/bulkhours/blob/main/data/cost_of_living.csv), [richest_countries.csv](https://github.com/guydegnol/bulkhours/blob/main/data/richest_countries.csv), [unemployment.csv](https://github.com/guydegnol/bulkhours/blob/main/data/unemployment.csv), [tourism.csv](https://github.com/guydegnol/bulkhours/blob/main/data/tourism.csv), [continent.tsv](https://github.com/guydegnol/bulkhours/blob/main/data/continent.tsv)
- Enrich data: [world.py](https://github.com/guydegnol/bulkhours/blob/main/bulkhours/data/world.py)  ([raw](https://raw.githubusercontent.com/guydegnol/bulkhours/main/bulkhours/data/world.py))

<details>
  <summary>Show columns info</summary>

| Column   |      Info |
|-----------|:-----------|
| country |  |
| annual_income |  |
| corruption_index |  |
| cost_index |  |
| monthly_income |  |
| purchasing_power_index |  |
| gdp_per_capita |  |
| unemployment_rate |  |
| tourists_in_millions |  |
| receipts_in_billions |  |
| receipts_per_tourist |  |
| percentage_of_gdp |  |
| index_x |  |
| iso_x |  |
| m49_x |  |
| region1_x |  |
| region2_x |  |
| continent_x |  |
| index_y |  |
| iso_y |  |
| m49_y |  |
| region1_y |  |
| region2_y |  |
| continent_y |  |

</details>
         
#### Global economic data (with gpx extra info)
#### `bulkhours.get_data("world.mapmacro")`
- Raw data: [corruption.csv](https://github.com/guydegnol/bulkhours/blob/main/data/corruption.csv), [cost_of_living.csv](https://github.com/guydegnol/bulkhours/blob/main/data/cost_of_living.csv), [richest_countries.csv](https://github.com/guydegnol/bulkhours/blob/main/data/richest_countries.csv), [unemployment.csv](https://github.com/guydegnol/bulkhours/blob/main/data/unemployment.csv), [tourism.csv](https://github.com/guydegnol/bulkhours/blob/main/data/tourism.csv), [continent.tsv](https://github.com/guydegnol/bulkhours/blob/main/data/continent.tsv)
- Enrich data: [world.py](https://github.com/guydegnol/bulkhours/blob/main/bulkhours/data/world.py)  ([raw](https://raw.githubusercontent.com/guydegnol/bulkhours/main/bulkhours/data/world.py))

<details>
  <summary>Show columns info</summary>

| Column   |      Info |
|-----------|:-----------|
| pop_est |  |
| continent |  |
| name |  |
| iso_a3 |  |
| gdp_md_est |  |
| geometry |  |
| annual_income |  |
| corruption_index |  |
| cost_index |  |
| monthly_income |  |
| purchasing_power_index |  |
| gdp_per_capita |  |
| unemployment_rate |  |
| tourists_in_millions |  |
| receipts_in_billions |  |
| receipts_per_tourist |  |
| percentage_of_gdp |  |
| index_x |  |
| iso_x |  |
| m49_x |  |
| region1_x |  |
| region2_x |  |
| continent_x |  |
| index_y |  |
| iso_y |  |
| m49_y |  |
| region1_y |  |
| region2_y |  |
| continent_y |  |

</details>
         
#### Life expectancy versus GDP/capita per country
#### `bulkhours.get_data("world.life_expectancy_vs_gdp_2018")`
- Raw data: [life-expectancy-vs-gdp-per-capita.csv](https://github.com/guydegnol/bulkhours/blob/main/data/life-expectancy-vs-gdp-per-capita.csv)
- Enrich data: [world.py](https://github.com/guydegnol/bulkhours/blob/main/bulkhours/data/world.py)  ([raw](https://raw.githubusercontent.com/guydegnol/bulkhours/main/bulkhours/data/world.py))
- Direct source: https://ourworldindata.org/grapher/life-expectancy-vs-gdp-per-capita
- Reference site: Maddison Project Database (2020); UN WPP (2022); Zijdeman et al. (2015)

<details>
  <summary>Show columns info</summary>

| Column   |      Info |
|-----------|:-----------|
| Country |  |
| Code |  |
| Year |  |
| Life expectancy (years) |  |
| GDP per capita ($) |  |
| annotations |  |
| Population |  |
| Continent |  |

</details>
         
#### Descriptive statistics of hourly wages in selected EU countries in 2010 (in PPS)
#### `bulkhours.get_data("mincer.stats")`
- Direct source: https://www.nbp.pl/publikacje/materialy_i_studia/226_en.pdf (table 2)

<details>
  <summary>Show columns info</summary>

| Column   |      Info |
|-----------|:-----------|
| Mean |  |
| Minimum |  |
| Maximum |  |
| Variance |  |
| Coefficient |  |
| of |  |
| variation |  |

</details>
         
#### Mincer equation parameters per country
#### `bulkhours.get_data("mincer.params")`
- Enrich data: [mincer.py](https://github.com/guydegnol/bulkhours/blob/main/bulkhours/data/mincer.py)  ([raw](https://raw.githubusercontent.com/guydegnol/bulkhours/main/bulkhours/data/mincer.py))
- Direct source: https://www.nbp.pl/publikacje/materialy_i_studia/226_en.pdf (table 3)

<details>
  <summary>Show columns info</summary>

| Column   |      Info |
|-----------|:-----------|
| alpha_0i |  |
| alpha_1i |  |
| alpha_2i |  |
| alpha_3i |  |
| alpha_0i_e |  |
| alpha_1i_e |  |
| alpha_2i_e |  |
| alpha_3i_e |  |

</details>
         
#### Age de la population au 1er janvier (fin novembre 2022)
#### `bulkhours.get_data("pyramide")`
- Raw data: [pyramide.tsv](https://github.com/guydegnol/bulkhours/blob/main/data/pyramide.tsv)
- Direct source: https://www.insee.fr/fr/statistiques/2381472#tableau-figure1

<details>
  <summary>Show columns info</summary>

| Column   |      Info |
|-----------|:-----------|
| Année de naissance |  |
| Age révolu |  |
| Nombre de femmes |  |
| Nombre d'hommes |  |
| Ensemble |  |

</details>
         
#### Cotisants, retraités et rapport démographique tous régimes en 2020
#### `bulkhours.get_data("france.retraites")`
- Enrich data: [france.py](https://github.com/guydegnol/bulkhours/blob/main/bulkhours/data/france.py)  ([raw](https://raw.githubusercontent.com/guydegnol/bulkhours/main/bulkhours/data/france.py))
- Direct source: https://www.insee.fr/fr/statistiques/2415121#tableau-figure1

<details>
  <summary>Show columns info</summary>

| Column   |      Info |
|-----------|:-----------|
| active |  |
| retired |  |
| rapport |  |

</details>
         
#### Distribution des salaires mensuels nets en équivalent temps plein (EQTP) en 2020
#### `bulkhours.get_data("france.income")`
- Enrich data: [france.py](https://github.com/guydegnol/bulkhours/blob/main/bulkhours/data/france.py)  ([raw](https://raw.githubusercontent.com/guydegnol/bulkhours/main/bulkhours/data/france.py))
- Direct source: https://www.insee.fr/fr/statistiques/6436313#tableau-figure2

<details>
  <summary>Show columns info</summary>

| Column   |      Info |
|-----------|:-----------|
| index |  |
| income |  |
| population |  |
| xmin |  |
| xmax |  |
| is_valid |  |

</details>
         
#### Revenu salarial et salaire en EQTP annuels moyens selon le sexe en 2019
#### `bulkhours.get_data("france.salaires")`
- Enrich data: [france.py](https://github.com/guydegnol/bulkhours/blob/main/bulkhours/data/france.py)  ([raw](https://raw.githubusercontent.com/guydegnol/bulkhours/main/bulkhours/data/france.py))
- Direct source: https://www.insee.fr/fr/statistiques/6047743?sommaire=6047805

<details>
  <summary>Show columns info</summary>

| Column   |      Info |
|-----------|:-----------|
| Revenu annuel Femmes moyen   |  Revenu annuel Femmes moyen |         
| Revenu annuel Hommes moyen  |  Revenu annuel Hommes moyen | 
| Revenu annuel Femmes moyen Écart relatif (en %)   |   Revenu annuel Femmes moyen Écart relatif (en %)	| 
| Salaire annuel Femmes moyen EQTP  |  Salaire annuel Femmes moyen EQTP | 
| Salaire annuel Hommes moyen EQTP   |  Salaire annuel Hommes moyen EQTP |
| Salaire annuel Femmes moyen EQTP Écart relatif (en % EQTP)   |  Salaire annuel Femmes moyen EQTP Écart relatif (en % EQTP) |

</details>
         
#### Inégalités salariales entre femmes et hommes de 1995 à 2019
#### `bulkhours.get_data("france.histsalaires")`
- Enrich data: [france.py](https://github.com/guydegnol/bulkhours/blob/main/bulkhours/data/france.py)  ([raw](https://raw.githubusercontent.com/guydegnol/bulkhours/main/bulkhours/data/france.py))
- Direct source: https://www.insee.fr/fr/statistiques/6047743?sommaire=6047805

<details>
  <summary>Show columns info</summary>

| Column   |      Info |
|-----------|:-----------|
| delta_rev_legacy   |  écart relatif du revenu salarial moyen homme/femme |         
| delta_rev  |  écart relatif (en %) du revenu salarial moyen.1| 
| delta_rev_eqtp_legacy   |  écart relatif du salaire moyen en EQTP	| 
| delta_rev_eqtp  |  écart relatif du salaire moyen en EQTP| 
| delta_vol_eqtp   |  écart relatif du volume de travail en EQTP moyen |

</details>
         
#### Evolution du PIB et de ses composantes par rapport au trimestre precedent en volume en %
#### `bulkhours.get_data("gmacro.fr_qgdp")`
- Enrich data: [gmacro.py](https://github.com/guydegnol/bulkhours/blob/main/bulkhours/data/gmacro.py)  ([raw](https://raw.githubusercontent.com/guydegnol/bulkhours/main/bulkhours/data/gmacro.py))
- Direct source: https://www.insee.fr/fr/statistiques/2830547#tableau-figure1

<details>
  <summary>Show columns info</summary>

| Column   |      Info |
|-----------|:-----------|
| gdp |  |
| Importations |  |
| consommation_menages |  |
| consommation_APU1 |  |
| capital_fixe |  |
| capital_fixe_non_financieres |  |
| menages |  |
| APU1 |  |
| Exportations |  |
| demaNaNe_interieure |  |
| Variations de stocks |  |
| Commerce exterieur |  |
| date |  |

</details>
         
#### Évolution du produit intérieur brut et de ses composantes
#### `bulkhours.get_data("gmacro.fr_unemployement")`
- Enrich data: [gmacro.py](https://github.com/guydegnol/bulkhours/blob/main/bulkhours/data/gmacro.py)  ([raw](https://raw.githubusercontent.com/guydegnol/bulkhours/main/bulkhours/data/gmacro.py))
- Direct source: https://www.insee.fr/fr/statistiques/2830547#tableau-figure1

<details>
  <summary>Show columns info</summary>

| Column   |      Info |
|-----------|:-----------|
| Femmes |  |
| Femmes_15-24 |  |
| Femmes_25-49 |  |
| Femmes_plus_50 |  |
| Hommes |  |
| Hommes_15-24 |  |
| Hommes_25-49 |  |
| Hommes_plus_50 |  |
| Ensemble |  |
| Ensemble_15-24 |  |
| Ensemble_25-49 |  |
| Ensemble_plus_50 |  |
| Longue_duree |  |
| date |  |

</details>
         
#### United States Macroeconomic data (1959q1 - 2009q3)
#### `bulkhours.get_data("gmacro.us_gdp")`
- Enrich data: [gmacro.py](https://github.com/guydegnol/bulkhours/blob/main/bulkhours/data/gmacro.py)  ([raw](https://raw.githubusercontent.com/guydegnol/bulkhours/main/bulkhours/data/gmacro.py))
- Direct source: https://www.statsmodels.org/0.6.1/datasets/generated/macrodata.html

<details>
  <summary>Show columns info</summary>

| Column   |      Info |
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


</details>
         
#### France Macroeconomic data
#### `bulkhours.get_data("gmacro.fr_gdp")`
- Enrich data: [gmacro.py](https://github.com/guydegnol/bulkhours/blob/main/bulkhours/data/gmacro.py)  ([raw](https://raw.githubusercontent.com/guydegnol/bulkhours/main/bulkhours/data/gmacro.py))

<details>
  <summary>Show columns info</summary>

| Column   |      Info |
|-----------|:-----------|
| yquarter |  |
| diff(gdp) |  |
| diff(unemployement) |  |

</details>
         
#### Scipy list of available distributions
#### `bulkhours.get_data("scipy_distributions_list")`
- Enrich data: [statsdata.py](https://github.com/guydegnol/bulkhours/blob/main/bulkhours/data/statsdata.py)  ([raw](https://raw.githubusercontent.com/guydegnol/bulkhours/main/bulkhours/data/statsdata.py))
#### Oil production in Saudi Arabia from 1996 to 2007
#### `bulkhours.get_data("statsdata.oil")`
- Enrich data: [statsdata.py](https://github.com/guydegnol/bulkhours/blob/main/bulkhours/data/statsdata.py)  ([raw](https://raw.githubusercontent.com/guydegnol/bulkhours/main/bulkhours/data/statsdata.py))
- Direct source: https://www.statsmodels.org/stable/index.html

<details>
  <summary>Show columns info</summary>

| Column   |      Info |
|-----------|:-----------|
| oil |  |

</details>
         
#### Air pollution data
#### `bulkhours.get_data("statsdata.air")`
- Enrich data: [statsdata.py](https://github.com/guydegnol/bulkhours/blob/main/bulkhours/data/statsdata.py)  ([raw](https://raw.githubusercontent.com/guydegnol/bulkhours/main/bulkhours/data/statsdata.py))
- Direct source: https://www.statsmodels.org/stable/index.html

<details>
  <summary>Show columns info</summary>

| Column   |      Info |
|-----------|:-----------|
| air |  |

</details>
         
#### Forecasting livestock, sheep in Asia: comparing forecasting performance of non-seasonal methods.
#### `bulkhours.get_data("statsdata.livestock2")`
- Enrich data: [statsdata.py](https://github.com/guydegnol/bulkhours/blob/main/bulkhours/data/statsdata.py)  ([raw](https://raw.githubusercontent.com/guydegnol/bulkhours/main/bulkhours/data/statsdata.py))
- Direct source: https://www.statsmodels.org/stable/index.html

<details>
  <summary>Show columns info</summary>

| Column   |      Info |
|-----------|:-----------|
| livestock2 |  |

</details>
         
#### Forecasting livestock, sheep in Asia: comparing forecasting performance of non-seasonal methods. (3)
#### `bulkhours.get_data("statsdata.livestock3")`
- Enrich data: [statsdata.py](https://github.com/guydegnol/bulkhours/blob/main/bulkhours/data/statsdata.py)  ([raw](https://raw.githubusercontent.com/guydegnol/bulkhours/main/bulkhours/data/statsdata.py))
- Direct source: https://www.statsmodels.org/stable/index.html

<details>
  <summary>Show columns info</summary>

| Column   |      Info |
|-----------|:-----------|
| livestock3 |  |

</details>
         
#### International visitor night in Australia (millions) < 2005
#### `bulkhours.get_data("statsdata.aust")`
- Enrich data: [statsdata.py](https://github.com/guydegnol/bulkhours/blob/main/bulkhours/data/statsdata.py)  ([raw](https://raw.githubusercontent.com/guydegnol/bulkhours/main/bulkhours/data/statsdata.py))

<details>
  <summary>Show columns info</summary>

| Column   |      Info |
|-----------|:-----------|
| aust |  |

</details>
         
#### International visitor night in Australia (millions) > 2005
#### `bulkhours.get_data("statsdata.air_passengers")`
- Raw data: [AirPassengers.csv](https://github.com/guydegnol/bulkhours/blob/main/data/AirPassengers.csv)
- Enrich data: [statsdata.py](https://github.com/guydegnol/bulkhours/blob/main/bulkhours/data/statsdata.py)  ([raw](https://raw.githubusercontent.com/guydegnol/bulkhours/main/bulkhours/data/statsdata.py))

<details>
  <summary>Show columns info</summary>

| Column   |      Info |
|-----------|:-----------|
| #Passengers |  |
| is_test |  |

</details>
         
#### All-Transactions House Price Index for Houston
#### `bulkhours.get_data("statsdata.hhousing")`
- Enrich data: [statsdata.py](https://github.com/guydegnol/bulkhours/blob/main/bulkhours/data/statsdata.py)  ([raw](https://raw.githubusercontent.com/guydegnol/bulkhours/main/bulkhours/data/statsdata.py))
- Direct source: https://fred.stlouisfed.org/series/ATNHPIUS26420Q

<details>
  <summary>Show columns info</summary>

| Column   |      Info |
|-----------|:-----------|
| HOUSTNSA |  |

</details>
         
#### Market prices of SP500 stocks
#### `bulkhours.get_data("prices-split-adjusted")`
- Raw data: [prices-split-adjusted.csv](https://github.com/kyi3081/stock-analysis/master/prices-split-adjusted.csv)  ([raw](https://raw.githubusercontent.com/kyi3081/stock-analysis/master/prices-split-adjusted.csv))
- Direct source: https://github.com/kyi3081/stock-analysis

<details>
  <summary>Show columns info</summary>

| Column   |      Info |
|-----------|:-----------|
| date |  |
| symbol |  |
| open |  |
| close |  |
| low |  |
| high |  |
| volume |  |

</details>
         
#### Market fundamentals of SP500 stocks
#### `bulkhours.get_data("fundamentals")`
- Raw data: [fundamentals.csv](https://github.com/kyi3081/stock-analysis/master/fundamentals.csv)  ([raw](https://raw.githubusercontent.com/kyi3081/stock-analysis/master/fundamentals.csv))
- Direct source: https://github.com/kyi3081/stock-analysis

<details>
  <summary>Show columns info</summary>

| Column   |      Info |
|-----------|:-----------|
| Unnamed: 0 |  |
| Ticker Symbol |  |
| Period Ending |  |
| Accounts Payable |  |
| Accounts Receivable |  |
| Add'l income/expense items |  |
| After Tax ROE |  |
| Capital Expenditures |  |
| Capital Surplus |  |
| Cash Ratio |  |
| Cash and Cash Equivalents |  |
| Changes in Inventories |  |
| Common Stocks |  |
| Cost of Revenue |  |
| Current Ratio |  |
| Deferred Asset Charges |  |
| Deferred Liability Charges |  |
| Depreciation |  |
| Earnings Before Interest and Tax |  |
| Earnings Before Tax |  |
| Effect of Exchange Rate |  |
| Equity Earnings/Loss Unconsolidated Subsidiary |  |
| Fixed Assets |  |
| Goodwill |  |
| Gross Margin |  |
| Gross Profit |  |
| Income Tax |  |
| Intangible Assets |  |
| Interest Expense |  |
| Inventory |  |
| Investments |  |
| Liabilities |  |
| Long-Term Debt |  |
| Long-Term Investments |  |
| Minority Interest |  |
| Misc. Stocks |  |
| Net Borrowings |  |
| Net Cash Flow |  |
| Net Cash Flow-Operating |  |
| Net Cash Flows-Financing |  |
| Net Cash Flows-Investing |  |
| Net Income |  |
| Net Income Adjustments |  |
| Net Income Applicable to Common Shareholders |  |
| Net Income-Cont. Operations |  |
| Net Receivables |  |
| Non-Recurring Items |  |
| Operating Income |  |
| Operating Margin |  |
| Other Assets |  |
| Other Current Assets |  |
| Other Current Liabilities |  |
| Other Equity |  |
| Other Financing Activities |  |
| Other Investing Activities |  |
| Other Liabilities |  |
| Other Operating Activities |  |
| Other Operating Items |  |
| Pre-Tax Margin |  |
| Pre-Tax ROE |  |
| Profit Margin |  |
| Quick Ratio |  |
| Research and Development |  |
| Retained Earnings |  |
| Sale and Purchase of Stock |  |
| Sales, General and Admin. |  |
| Short-Term Debt / Current Portion of Long-Term Debt |  |
| Short-Term Investments |  |
| Total Assets |  |
| Total Current Assets |  |
| Total Current Liabilities |  |
| Total Equity |  |
| Total Liabilities |  |
| Total Liabilities & Equity |  |
| Total Revenue |  |
| Treasury Stock |  |
| For Year |  |
| Earnings Per Share |  |
| Estimated Shares Outstanding |  |

</details>
         
#### Stocks information for SP500
#### `bulkhours.get_data("securities")`
- Raw data: [securities.csv](https://github.com/kyi3081/stock-analysis/master/securities.csv)  ([raw](https://raw.githubusercontent.com/kyi3081/stock-analysis/master/securities.csv))
- Direct source: https://github.com/kyi3081/stock-analysis

<details>
  <summary>Show columns info</summary>

| Column   |      Info |
|-----------|:-----------|
| Ticker symbol |  |
| Security |  |
| SEC filings |  |
| GICS Sector |  |
| GICS Sub Industry |  |
| Address of Headquarters |  |
| Date first added |  |
| CIK |  |

</details>
         
#### Statement of Apple stock (Quarterly)
#### `bulkhours.get_data("trading.apple")`
- Raw data: [APPLE_DownloadFPrepStatementQuarter.tsv](https://github.com/guydegnol/bulkhours/blob/main/data/APPLE_DownloadFPrepStatementQuarter.tsv)
- Enrich data: [trading.py](https://github.com/guydegnol/bulkhours/blob/main/bulkhours/data/trading.py)  ([raw](https://raw.githubusercontent.com/guydegnol/bulkhours/main/bulkhours/data/trading.py))

<details>
  <summary>Show columns info</summary>

| Column   |      Info |
|-----------|:-----------|
| date |  |
| symbol |  |
| reportedCurrency |  |
| cik |  |
| fillingDate |  |
| acceptedDate |  |
| calendarYear |  |
| period |  |
| revenue |  |
| costOfRevenue |  |
| grossProfit |  |
| grossProfitRatio |  |
| researchAndDevelopmentExpenses |  |
| generalAndAdministrativeExpenses |  |
| sellingAndMarketingExpenses |  |
| sellingGeneralAndAdministrativeExpenses |  |
| otherExpenses |  |
| operatingExpenses |  |
| costAndExpenses |  |
| interestIncome |  |
| interestExpense |  |
| depreciationAndAmortization |  |
| ebitda |  |
| ebitdaratio |  |
| operatingIncome |  |
| operatingIncomeRatio |  |
| totalOtherIncomeExpensesNet |  |
| incomeBeforeTax |  |
| incomeBeforeTaxRatio |  |
| incomeTaxExpense |  |
| netIncome |  |
| netIncomeRatio |  |
| eps |  |
| epsdiluted |  |
| weightedAverageShsOut |  |
| weightedAverageShsOutDil |  |
| link |  |
| finalLink |  |

</details>
         
#### Standardized country information (iso m49)
#### `bulkhours.get_data("continent")`
- Raw data: [continent.tsv](https://github.com/guydegnol/bulkhours/blob/main/data/continent.tsv)

<details>
  <summary>Show columns info</summary>

| Column   |      Info |
|-----------|:-----------|
| index |  |
| country |  |
| iso |  |
| m49 |  |
| region1 |  |
| region2 |  |
| continent |  |

</details>
         
#### Corruption index per country
#### `bulkhours.get_data("corruption")`
- Raw data: [corruption.csv](https://github.com/guydegnol/bulkhours/blob/main/data/corruption.csv)

<details>
  <summary>Show columns info</summary>

| Column   |      Info |
|-----------|:-----------|
| country |  |
| annual_income |  |
| corruption_index |  |

</details>
         
#### Cost of living
#### `bulkhours.get_data("cost_of_living")`
- Raw data: [cost_of_living.csv](https://github.com/guydegnol/bulkhours/blob/main/data/cost_of_living.csv)

<details>
  <summary>Show columns info</summary>

| Column   |      Info |
|-----------|:-----------|
| country   |   |         
| cost_index  |   | 
| monthly_income   |  	| 
| purchasing_power_index  |  |


</details>
         
#### GDP per capita per country
#### `bulkhours.get_data("richest_countries")`
- Raw data: [richest_countries.csv](https://github.com/guydegnol/bulkhours/blob/main/data/richest_countries.csv)

<details>
  <summary>Show columns info</summary>

| Column   |      Info |
|-----------|:-----------|
| country   |   |         
| gdp_per_capita  |   | 


</details>
         
#### Tourism information per country
#### `bulkhours.get_data("tourism")`
- Raw data: [tourism.csv](https://github.com/guydegnol/bulkhours/blob/main/data/tourism.csv)

<details>
  <summary>Show columns info</summary>

| Column   |      Info |
|-----------|:-----------|
| country |  |
| tourists_in_millions |  |
| receipts_in_billions |  |
| receipts_per_tourist |  |
| percentage_of_gdp |  |

</details>
         
#### Unemployemnt rates per country
#### `bulkhours.get_data("unemployment")`
- Raw data: [unemployment.csv](https://github.com/guydegnol/bulkhours/blob/main/data/unemployment.csv)

<details>
  <summary>Show columns info</summary>

| Column   |      Info |
|-----------|:-----------|
| country |  |
| unemployment_rate |  |

</details>
         
#### Simple synthetic data for exercice
#### `bulkhours.get_data("wages")`
- Raw data: [wages.tsv](https://github.com/guydegnol/bulkhours/blob/main/data/wages.tsv)

<details>
  <summary>Show columns info</summary>

| Column   |      Info |
|-----------|:-----------|
| wage |  |
| experience |  |
| studies |  |

</details>
         
#### COR data
#### `bulkhours.get_data("COR_1")`
- Raw data: [Données septembre partie 1.xlsx](https://github.com/guydegnol/bulkhours/blob/main/data/Données septembre partie 1.xlsx)

<details>
  <summary>Show columns info</summary>

| Column   |      Info |
|-----------|:-----------|
| Unnamed: 0 |  |

</details>
         
#### COR data
#### `bulkhours.get_data("COR_2")`
- Raw data: [Données_RA2022_P2.xlsx](https://github.com/guydegnol/bulkhours/blob/main/data/Données_RA2022_P2.xlsx)

<details>
  <summary>Show columns info</summary>

| Column   |      Info |
|-----------|:-----------|
| Sommaire |  |

</details>
         
#### COR data
#### `bulkhours.get_data("COR_2bis")`
- Raw data: [Données complémentaires partie 2 RA 2022.xlsx](https://github.com/guydegnol/bulkhours/blob/main/data/Données complémentaires partie 2 RA 2022.xlsx)

<details>
  <summary>Show columns info</summary>

| Column   |      Info |
|-----------|:-----------|
| Figure 2.1 – PIB observé et projeté |  |
| Unnamed: 1 |  |
| Unnamed: 2 |  |
| Unnamed: 3 |  |
| Unnamed: 4 |  |
| Unnamed: 5 |  |
| Unnamed: 6 |  |
| Unnamed: 7 |  |
| Unnamed: 8 |  |
| Unnamed: 9 |  |
| Unnamed: 10 |  |
| Unnamed: 11 |  |
| Unnamed: 12 |  |
| Unnamed: 13 |  |
| Unnamed: 14 |  |
| Unnamed: 15 |  |
| Unnamed: 16 |  |
| Unnamed: 17 |  |
| Unnamed: 18 |  |
| Unnamed: 19 |  |
| Unnamed: 20 |  |
| Unnamed: 21 |  |
| Unnamed: 22 |  |
| Unnamed: 23 |  |
| Unnamed: 24 |  |
| Unnamed: 25 |  |
| Unnamed: 26 |  |
| Unnamed: 27 |  |
| Unnamed: 28 |  |
| Unnamed: 29 |  |
| Unnamed: 30 |  |
| Unnamed: 31 |  |
| Unnamed: 32 |  |
| Unnamed: 33 |  |
| Unnamed: 34 |  |
| Unnamed: 35 |  |
| Unnamed: 36 |  |
| Unnamed: 37 |  |
| Unnamed: 38 |  |
| Unnamed: 39 |  |
| Unnamed: 40 |  |
| Unnamed: 41 |  |
| Unnamed: 42 |  |
| Unnamed: 43 |  |
| Unnamed: 44 |  |
| Unnamed: 45 |  |
| Unnamed: 46 |  |
| Unnamed: 47 |  |
| Unnamed: 48 |  |
| Unnamed: 49 |  |
| Unnamed: 50 |  |
| Unnamed: 51 |  |
| Unnamed: 52 |  |
| Unnamed: 53 |  |
| Unnamed: 54 |  |
| Unnamed: 55 |  |
| Unnamed: 56 |  |
| Unnamed: 57 |  |
| Unnamed: 58 |  |
| Unnamed: 59 |  |
| Unnamed: 60 |  |
| Unnamed: 61 |  |
| Unnamed: 62 |  |
| Unnamed: 63 |  |
| Unnamed: 64 |  |
| Unnamed: 65 |  |
| Unnamed: 66 |  |
| Unnamed: 67 |  |
| Unnamed: 68 |  |
| Unnamed: 69 |  |
| Unnamed: 70 |  |
| Unnamed: 71 |  |
| Unnamed: 72 |  |
| Unnamed: 73 |  |

</details>
         
#### COR data
#### `bulkhours.get_data("COR_3")`
- Raw data: [Données septembre 2022 - partie 3.xlsx](https://github.com/guydegnol/bulkhours/blob/main/data/Données septembre 2022 - partie 3.xlsx)

<details>
  <summary>Show columns info</summary>

| Column   |      Info |
|-----------|:-----------|
| Partie 3. Les résultats : les évolutions du système de retraite au regard de l'objectif d'un niveau de vie satisfaisant pour les retraités |  |

</details>
         
#### COR data
#### `bulkhours.get_data("COR_4")`
- Raw data: [Données_RA2022_P4.xlsx](https://github.com/guydegnol/bulkhours/blob/main/data/Données_RA2022_P4.xlsx)

<details>
  <summary>Show columns info</summary>

| Column   |      Info |
|-----------|:-----------|
| Partie 4. Les résultats : les évolutions du système de retraite au regard de l'objectif d'équité entre les assurés |  |

</details>
         
#### COR data
#### `bulkhours.get_data("COR_5")`
- Raw data: [Données septembre 2022 - partie 5.xlsx](https://github.com/guydegnol/bulkhours/blob/main/data/Données septembre 2022 - partie 5.xlsx)

<details>
  <summary>Show columns info</summary>

| Column   |      Info |
|-----------|:-----------|
| Partie 5. Les âges et les conditions de départ à la retraite |  |

</details>
         


## Predictive_Maintenance 

#### Synthetic data for machine failure data (1)
#### `bulkhours.get_data("maintenance1")`
- Raw data: [fe_equipment_failure_data_1.csv](https://github.com/shadgriffin/feature_engineering_equipment_failure/main/fe_equipment_failure_data_1.csv)  ([raw](https://raw.githubusercontent.com/shadgriffin/feature_engineering_equipment_failure/main/fe_equipment_failure_data_1.csv))

<details>
  <summary>Show columns info</summary>

| Column   |      Info |
|-----------|:-----------|
| ID |  |
| DATE |  |
| MANUFACTURER |  |
| S15 |  |
| EQUIPMENT_FAILURE |  |

</details>
         
#### Synthetic data for machine failure data (2)
#### `bulkhours.get_data("maintenance2")`
- Raw data: [fe_equipment_failure_data_2.csv](https://github.com/shadgriffin/feature_engineering_equipment_failure/main/fe_equipment_failure_data_2.csv)  ([raw](https://raw.githubusercontent.com/shadgriffin/feature_engineering_equipment_failure/main/fe_equipment_failure_data_2.csv))

<details>
  <summary>Show columns info</summary>

| Column   |      Info |
|-----------|:-----------|
| ID |  |
| DATE |  |
| MANUFACTURER |  |
| S15 |  |
| EQUIPMENT_FAILURE |  |

</details>
         
#### Synthetic data for machine failure data (3)
#### `bulkhours.get_data("maintenance3")`
- Raw data: [equipment_failure_data_1.csv](https://github.com/shadgriffin/machine_failure/master/equipment_failure_data_1.csv)  ([raw](https://raw.githubusercontent.com/shadgriffin/machine_failure/master/equipment_failure_data_1.csv))

<details>
  <summary>Show columns info</summary>

| Column   |      Info |
|-----------|:-----------|
| ID |  |
| DATE |  |
| REGION_CLUSTER |  |
| MAINTENANCE_VENDOR |  |
| MANUFACTURER |  |
| WELL_GROUP |  |
| S15 |  |
| S17 |  |
| S13 |  |
| S5 |  |
| S16 |  |
| S19 |  |
| S18 |  |
| EQUIPMENT_FAILURE |  |
| S8 |  |
| AGE_OF_EQUIPMENT |  |

</details>
         
#### Synthetic data for machine failure data (4)
#### `bulkhours.get_data("maintenance4")`
- Raw data: [equipment_failure_data_2.csv](https://github.com/shadgriffin/machine_failure/master/equipment_failure_data_2.csv)  ([raw](https://raw.githubusercontent.com/shadgriffin/machine_failure/master/equipment_failure_data_2.csv))

<details>
  <summary>Show columns info</summary>

| Column   |      Info |
|-----------|:-----------|
| ID |  |
| DATE |  |
| REGION_CLUSTER |  |
| MAINTENANCE_VENDOR |  |
| MANUFACTURER |  |
| WELL_GROUP |  |
| S15 |  |
| S17 |  |
| S13 |  |
| S5 |  |
| S16 |  |
| S19 |  |
| S18 |  |
| EQUIPMENT_FAILURE |  |
| S8 |  |
| AGE_OF_EQUIPMENT |  |

</details>
         


## Computing 

#### Computational capacity of the fastest supercomputers
#### `bulkhours.get_data("supercomputers")`
- Raw data: [Supercomputer%20power%20(FLOPS)%20%E2%80%93%20TOP500%20Database.csv](https://github.com/owid/owid-datasets/dd7a4ecbb249f98028e25c304ef7d68de8979ea9/datasets/Supercomputer%20power%20(FLOPS)%20%E2%80%93%20TOP500%20Database/Supercomputer%20power%20(FLOPS)%20%E2%80%93%20TOP500%20Database.csv)  ([raw](https://raw.githubusercontent.com/owid/owid-datasets/dd7a4ecbb249f98028e25c304ef7d68de8979ea9/datasets/Supercomputer%20power%20(FLOPS)%20%E2%80%93%20TOP500%20Database/Supercomputer%20power%20(FLOPS)%20%E2%80%93%20TOP500%20Database.csv))
- Direct source: https://ourworldindata.org/grapher/supercomputer-power-flops

<details>
  <summary>Show columns info</summary>
> The number of floating-point operations per second (GigaFLOPS) by the fastest supercomputer in any given year

| Column   |      Info |
|-----------|:-----------|
| Entity |  |
| Year |  |
| Floating-Point Operations per Second |  |

</details>
         
#### transistor_count
#### `bulkhours.get_data("hpc.transistor_count")`
- Reference site: https://en.wikipedia.org/wiki/Transistor_count

<details>
  <summary>Show columns info</summary>

| Column   |      Info |
|-----------|:-----------|
| processor |  |
| count |  |
| date |  |
| designer |  |
| manufacturer |  |
| engraving_scale |  |
| area |  |
| density |  |
| ref |  |

</details>
         
#### Semiconductor device fabrication: MOSFET scaling
#### `bulkhours.get_data("hpc.engraving_scale")`
- Reference site: https://en.wikipedia.org/wiki/Transistor_count

<details>
  <summary>Show columns info</summary>

| Column   |      Info |
|-----------|:-----------|
| year |  |
| scale |  |

</details>
         
#### FLOPS sub-units
#### `bulkhours.get_data("hpc.FLOPS_units")`
- Reference site: https://en.wikipedia.org/wiki/FLOPS

<details>
  <summary>Show columns info</summary>

| Column   |      Info |
|-----------|:-----------|
| Name |  |
| Unit |  |
| Value |  |

</details>
         
#### FLOPS for gpus
#### `bulkhours.get_data("hpc.FLOPS_gpus")`
- Reference site: https://en.wikipedia.org/wiki/FLOPS

<details>
  <summary>Show columns info</summary>

| Column   |      Info |
|-----------|:-----------|
| date |  |
| un_costs |  |
| costs |  |
| platform |  |
| comments |  |

</details>
         
#### FLOPS for cpus
#### `bulkhours.get_data("hpc.FLOPS_cpus")`
- Reference site: https://en.wikipedia.org/wiki/FLOPS

<details>
  <summary>Show columns info</summary>

| Column   |      Info |
|-----------|:-----------|
| processor |  |
| count |  |
| date |  |
| designer |  |
| engraving_scale |  |
| area |  |
| density |  |
| engraving_scale2 |  |
| engraving_scale3 |  |

</details>
         


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

<details>
  <summary>Show columns info</summary>
> https://en.wikipedia.org/wiki/Wolf_number

| Column   |      Info |
|-----------|:-----------|
| ssn |  |
| smoothed_ssn |  |
| observed_swpc_ssn |  |
| smoothed_swpc_ssn |  |
| f10.7 |  |
| smoothed_f10.7 |  |

</details>
         


## Health 

#### Coronavirus Pandemic (COVID-19) data
#### `bulkhours.get_data("vaccinations")`
- Raw data: [vaccinations.csv](https://github.com/owid/covid-19-data/master/public/data/vaccinations/vaccinations.csv)  ([raw](https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/vaccinations/vaccinations.csv))
- Direct source: https://ourworldindata.org/coronavirus
- Reference site: https://covid19.who.int/data

<details>
  <summary>Show columns info</summary>
> https://github.com/owid/covid-19-data/tree/master/public/data/

| Column   |      Info |
|-----------|:-----------|
| location |  |
| iso_code |  |
| date |  |
| total_vaccinations |  |
| people_vaccinated |  |
| people_fully_vaccinated |  |
| total_boosters |  |
| daily_vaccinations_raw |  |
| daily_vaccinations |  |
| total_vaccinations_per_hundred |  |
| people_vaccinated_per_hundred |  |
| people_fully_vaccinated_per_hundred |  |
| total_boosters_per_hundred |  |
| daily_vaccinations_per_million |  |
| daily_people_vaccinated |  |
| daily_people_vaccinated_per_hundred |  |

</details>
         
#### Prostate cancer data
#### `bulkhours.get_data("prostate")`
- Raw data: [prostate.tsv](https://github.com/guydegnol/bulkhours/blob/main/data/prostate.tsv)
- Direct source: https://hastie.su.domains/ElemStatLearn/data.html

<details>
  <summary>Show columns info</summary>

| Column   |      Info |
|-----------|:-----------|
| lcavol   |  |         
| lweight  | | 
| lbph   | 	| 
| svi  |  | 
| lcp   |   |
| gleason   |  |
| pgg45   |   |
| [outcome]   |   |


</details>
         
#### Coronavirus Pandemic (COVID-19) data
#### `bulkhours.get_data("covid")`
- Raw data: [owid-covid-data.csv](https://covid.ourworldindata.org/data/owid-covid-data.csv)  ([raw](https://covid.ourworldindata.org/data/owid-covid-data.csv))
- Direct source: https://ourworldindata.org/coronavirus
- Reference site: https://covid19.who.int/data

<details>
  <summary>Show columns info</summary>
> https://github.com/owid/covid-19-data/tree/master/public/data/

| Column   |      Info |
|-----------|:-----------|
| iso_code |  |
| continent |  |
| location |  |
| date |  |
| total_cases |  |
| new_cases |  |
| new_cases_smoothed |  |
| total_deaths |  |
| new_deaths |  |
| new_deaths_smoothed |  |
| total_cases_per_million |  |
| new_cases_per_million |  |
| new_cases_smoothed_per_million |  |
| total_deaths_per_million |  |
| new_deaths_per_million |  |
| new_deaths_smoothed_per_million |  |
| reproduction_rate |  |
| icu_patients |  |
| icu_patients_per_million |  |
| hosp_patients |  |
| hosp_patients_per_million |  |
| weekly_icu_admissions |  |
| weekly_icu_admissions_per_million |  |
| weekly_hosp_admissions |  |
| weekly_hosp_admissions_per_million |  |
| total_tests |  |
| new_tests |  |
| total_tests_per_thousand |  |
| new_tests_per_thousand |  |
| new_tests_smoothed |  |
| new_tests_smoothed_per_thousand |  |
| positive_rate |  |
| tests_per_case |  |
| tests_units |  |
| total_vaccinations |  |
| people_vaccinated |  |
| people_fully_vaccinated |  |
| total_boosters |  |
| new_vaccinations |  |
| new_vaccinations_smoothed |  |
| total_vaccinations_per_hundred |  |
| people_vaccinated_per_hundred |  |
| people_fully_vaccinated_per_hundred |  |
| total_boosters_per_hundred |  |
| new_vaccinations_smoothed_per_million |  |
| new_people_vaccinated_smoothed |  |
| new_people_vaccinated_smoothed_per_hundred |  |
| stringency_index |  |
| population_density |  |
| median_age |  |
| aged_65_older |  |
| aged_70_older |  |
| gdp_per_capita |  |
| extreme_poverty |  |
| cardiovasc_death_rate |  |
| diabetes_prevalence |  |
| female_smokers |  |
| male_smokers |  |
| handwashing_facilities |  |
| hospital_beds_per_thousand |  |
| life_expectancy |  |
| human_development_index |  |
| population |  |
| excess_mortality_cumulative_absolute |  |
| excess_mortality_cumulative |  |
| excess_mortality |  |
| excess_mortality_cumulative_per_million |  |

</details>
         


## Climate_Evolution 

#### Greenhouse effect gaz concentrations
#### `bulkhours.get_data("co2.concentrations")`
- Raw data: [climate-change.csv](https://github.com/guydegnol/bulkhours/blob/main/data/climate-change.csv)
- Enrich data: [world.py](https://github.com/guydegnol/bulkhours/blob/main/bulkhours/data/world.py)  ([raw](https://raw.githubusercontent.com/guydegnol/bulkhours/main/bulkhours/data/world.py))
- Direct source: https://ourworldindata.org/atmospheric-concentrations

<details>
  <summary>Show columns info</summary>

| Column   |      Info |
|-----------|:-----------|
| country |  |
| year |  |
| CO2 concentrations |  |
| CH4 concentrations |  |
| N2O concentrations |  |
| February |  |
| September |  |
| Mass U.S. glaciers |  |
| CSIRO |  |
| IAP |  |
| MRIJMA |  |
| NOAA |  |
| Snow cover |  |
| Sea surface temp |  |
| Sea surface temp (lower-bound) |  |
| Sea surface temp (upper-bound) |  |
| IAP.1 |  |
| NOAA.1 |  |
| MRIJMA.1 |  |
| February.1 |  |
| September.1 |  |

</details>
         
#### Greenhouse effect gaz concentrations
#### `bulkhours.get_data("co2.mapconcentrations")`
- Raw data: [climate-change.csv](https://github.com/guydegnol/bulkhours/blob/main/data/climate-change.csv)
- Enrich data: [world.py](https://github.com/guydegnol/bulkhours/blob/main/bulkhours/data/world.py)  ([raw](https://raw.githubusercontent.com/guydegnol/bulkhours/main/bulkhours/data/world.py))
- Direct source: https://ourworldindata.org/atmospheric-concentrations

<details>
  <summary>Show columns info</summary>

| Column   |      Info |
|-----------|:-----------|
| pop_est |  |
| continent |  |
| name |  |
| iso_a3 |  |
| gdp_md_est |  |
| geometry |  |
| year |  |
| CO2 concentrations |  |
| CH4 concentrations |  |
| N2O concentrations |  |
| February |  |
| September |  |
| Mass U.S. glaciers |  |
| CSIRO |  |
| IAP |  |
| MRIJMA |  |
| NOAA |  |
| Snow cover |  |
| Sea surface temp |  |
| Sea surface temp (lower-bound) |  |
| Sea surface temp (upper-bound) |  |
| IAP.1 |  |
| NOAA.1 |  |
| MRIJMA.1 |  |
| February.1 |  |
| September.1 |  |

</details>
         
#### Data on CO2 and Greenhouse Gas Emissions by Our World in Data
#### `bulkhours.get_data("co2.main")`
- Raw data: [owid-co2-data.csv](https://github.com/owid/co2-data/master/owid-co2-data.csv)  ([raw](https://raw.githubusercontent.com/owid/co2-data/master/owid-co2-data.csv))
- Enrich data: [world.py](https://github.com/guydegnol/bulkhours/blob/main/bulkhours/data/world.py)  ([raw](https://raw.githubusercontent.com/guydegnol/bulkhours/main/bulkhours/data/world.py))

<details>
  <summary>Show columns info</summary>
> https://github.com/owid/co2-data/blob/master/owid-co2-codebook.csv

| Column   |      Info |
|-----------|:-----------|
| country |  |
| year |  |
| iso_code |  |
| population |  |
| gdp |  |
| cement_co2 |  |
| cement_co2_per_capita |  |
| co2 |  |
| co2_growth_abs |  |
| co2_growth_prct |  |
| co2_including_luc |  |
| co2_including_luc_growth_abs |  |
| co2_including_luc_growth_prct |  |
| co2_including_luc_per_capita |  |
| co2_including_luc_per_gdp |  |
| co2_including_luc_per_unit_energy |  |
| co2_per_capita |  |
| co2_per_gdp |  |
| co2_per_unit_energy |  |
| coal_co2 |  |
| coal_co2_per_capita |  |
| consumption_co2 |  |
| consumption_co2_per_capita |  |
| consumption_co2_per_gdp |  |
| cumulative_cement_co2 |  |
| cumulative_co2 |  |
| cumulative_co2_including_luc |  |
| cumulative_coal_co2 |  |
| cumulative_flaring_co2 |  |
| cumulative_gas_co2 |  |
| cumulative_luc_co2 |  |
| cumulative_oil_co2 |  |
| cumulative_other_co2 |  |
| energy_per_capita |  |
| energy_per_gdp |  |
| flaring_co2 |  |
| flaring_co2_per_capita |  |
| gas_co2 |  |
| gas_co2_per_capita |  |
| ghg_excluding_lucf_per_capita |  |
| ghg_per_capita |  |
| land_use_change_co2 |  |
| land_use_change_co2_per_capita |  |
| methane |  |
| methane_per_capita |  |
| nitrous_oxide |  |
| nitrous_oxide_per_capita |  |
| oil_co2 |  |
| oil_co2_per_capita |  |
| other_co2_per_capita |  |
| other_industry_co2 |  |
| primary_energy_consumption |  |
| share_global_cement_co2 |  |
| share_global_co2 |  |
| share_global_co2_including_luc |  |
| share_global_coal_co2 |  |
| share_global_cumulative_cement_co2 |  |
| share_global_cumulative_co2 |  |
| share_global_cumulative_co2_including_luc |  |
| share_global_cumulative_coal_co2 |  |
| share_global_cumulative_flaring_co2 |  |
| share_global_cumulative_gas_co2 |  |
| share_global_cumulative_luc_co2 |  |
| share_global_cumulative_oil_co2 |  |
| share_global_cumulative_other_co2 |  |
| share_global_flaring_co2 |  |
| share_global_gas_co2 |  |
| share_global_luc_co2 |  |
| share_global_oil_co2 |  |
| share_global_other_co2 |  |
| share_of_temperature_change_from_ghg |  |
| temperature_change_from_ch4 |  |
| temperature_change_from_co2 |  |
| temperature_change_from_ghg |  |
| temperature_change_from_n2o |  |
| total_ghg |  |
| total_ghg_excluding_lucf |  |
| trade_co2 |  |
| trade_co2_share |  |

</details>
         
#### Data on CO2 and Greenhouse Gas Emissions by Our World in Data (with extra gpx data)
#### `bulkhours.get_data("co2.mapmain")`
- Raw data: [owid-co2-data.csv](https://github.com/owid/co2-data/master/owid-co2-data.csv)  ([raw](https://raw.githubusercontent.com/owid/co2-data/master/owid-co2-data.csv))
- Enrich data: [world.py](https://github.com/guydegnol/bulkhours/blob/main/bulkhours/data/world.py)  ([raw](https://raw.githubusercontent.com/guydegnol/bulkhours/main/bulkhours/data/world.py))

<details>
  <summary>Show columns info</summary>
> https://github.com/owid/co2-data/blob/master/owid-co2-codebook.csv

| Column   |      Info |
|-----------|:-----------|
| country |  |
| year |  |
| iso_code |  |
| population |  |
| gdp |  |
| cement_co2 |  |
| cement_co2_per_capita |  |
| co2 |  |
| co2_growth_abs |  |
| co2_growth_prct |  |
| co2_including_luc |  |
| co2_including_luc_growth_abs |  |
| co2_including_luc_growth_prct |  |
| co2_including_luc_per_capita |  |
| co2_including_luc_per_gdp |  |
| co2_including_luc_per_unit_energy |  |
| co2_per_capita |  |
| co2_per_gdp |  |
| co2_per_unit_energy |  |
| coal_co2 |  |
| coal_co2_per_capita |  |
| consumption_co2 |  |
| consumption_co2_per_capita |  |
| consumption_co2_per_gdp |  |
| cumulative_cement_co2 |  |
| cumulative_co2 |  |
| cumulative_co2_including_luc |  |
| cumulative_coal_co2 |  |
| cumulative_flaring_co2 |  |
| cumulative_gas_co2 |  |
| cumulative_luc_co2 |  |
| cumulative_oil_co2 |  |
| cumulative_other_co2 |  |
| energy_per_capita |  |
| energy_per_gdp |  |
| flaring_co2 |  |
| flaring_co2_per_capita |  |
| gas_co2 |  |
| gas_co2_per_capita |  |
| ghg_excluding_lucf_per_capita |  |
| ghg_per_capita |  |
| land_use_change_co2 |  |
| land_use_change_co2_per_capita |  |
| methane |  |
| methane_per_capita |  |
| nitrous_oxide |  |
| nitrous_oxide_per_capita |  |
| oil_co2 |  |
| oil_co2_per_capita |  |
| other_co2_per_capita |  |
| other_industry_co2 |  |
| primary_energy_consumption |  |
| share_global_cement_co2 |  |
| share_global_co2 |  |
| share_global_co2_including_luc |  |
| share_global_coal_co2 |  |
| share_global_cumulative_cement_co2 |  |
| share_global_cumulative_co2 |  |
| share_global_cumulative_co2_including_luc |  |
| share_global_cumulative_coal_co2 |  |
| share_global_cumulative_flaring_co2 |  |
| share_global_cumulative_gas_co2 |  |
| share_global_cumulative_luc_co2 |  |
| share_global_cumulative_oil_co2 |  |
| share_global_cumulative_other_co2 |  |
| share_global_flaring_co2 |  |
| share_global_gas_co2 |  |
| share_global_luc_co2 |  |
| share_global_oil_co2 |  |
| share_global_other_co2 |  |
| share_of_temperature_change_from_ghg |  |
| temperature_change_from_ch4 |  |
| temperature_change_from_co2 |  |
| temperature_change_from_ghg |  |
| temperature_change_from_n2o |  |
| total_ghg |  |
| total_ghg_excluding_lucf |  |
| trade_co2 |  |
| trade_co2_share |  |

</details>
         
#### CO2 transportation info
#### `bulkhours.get_data("co2.travel_mode")`
- Raw data: [carbon-footprint-travel-mode.csv](https://github.com/guydegnol/bulkhours/blob/main/data/carbon-footprint-travel-mode.csv)
- Direct source: https://ourworldindata.org/grapher/carbon-footprint-travel-mode

<details>
  <summary>Show columns info</summary>

| Column   |      Info |
|-----------|:-----------|
| Entity |  |
| Code |  |
| Year |  |
| GHG emissions (gCO2e/km) |  |

</details>
         


## Machine_learning 

#### Cat or not training data
#### `bulkhours.get_data("train_catvnoncat")`
- Raw data: [train_catvnoncat.h5](https://github.com/guydegnol/bulkhours/blob/main/data/train_catvnoncat.h5)
#### Cat or not test data
#### `bulkhours.get_data("test_catvnoncat")`
- Raw data: [test_catvnoncat.h5](https://github.com/guydegnol/bulkhours/blob/main/data/test_catvnoncat.h5)
