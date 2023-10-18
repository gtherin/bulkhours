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
- Raw data: [pip_dataset.csv](https://nyc3.digitaloceanspaces.com/owid-public/data/poverty/pip_dataset.csv)  ([raw](https://nyc3.digitaloceanspaces.com/owid-public/data/poverty/pip_dataset.csv)🔄)
- Enrich data: [world.py](https://github.com/gtherin/bulkhours/main/bulkhours/data/world.py)  ([raw](https://raw.githubusercontent.com/gtherin/bulkhours/main/bulkhours/data/world.py))
- Direct source: https://ourworldindata.org/poverty
- Reference site: https://pip.worldbank.org/

<details>
<summary>Show columns info</summary>
> <a href="https://github.com/owid/poverty-data/blob/main/datasets/pip_codebook.csv">https://github.com/owid/poverty-data/blob/main/datasets/pip_codebook.csv</a>

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


<details>
<summary>Show code</summary>
<code>
def get_poverty(self, timeopt=None):
    timeopt = self.data_info["timeopt"] if "timeopt" in self.data_info else None
    df = self.read_raw_data(self.raw_data)
    return geo_format(df, timeopt)
</code>
</details>

#### World Bank Poverty and Inequality data (with gpx extra info)
#### `bulkhours.get_data("world.mappoverty")`
- Raw data: [pip_dataset.csv](https://nyc3.digitaloceanspaces.com/owid-public/data/poverty/pip_dataset.csv)  ([raw](https://nyc3.digitaloceanspaces.com/owid-public/data/poverty/pip_dataset.csv)🔄)
- Enrich data: [world.py](https://github.com/gtherin/bulkhours/main/bulkhours/data/world.py)  ([raw](https://raw.githubusercontent.com/gtherin/bulkhours/main/bulkhours/data/world.py))
- Direct source: https://ourworldindata.org/poverty
- Reference site: https://pip.worldbank.org/

<details>
<summary>Show columns info</summary>
> <a href="https://github.com/owid/poverty-data/blob/main/datasets/pip_codebook.csv">https://github.com/owid/poverty-data/blob/main/datasets/pip_codebook.csv</a>

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


<details>
<summary>Show code</summary>
<code>
def get_mappoverty(self, **kwargs):
    return get_mapgeneric(get_poverty(self, **kwargs))
</code>
</details>

#### World Bank Gdp data
#### `bulkhours.get_data("world.gdp")`
- Raw data: [pip_dataset.csv](https://nyc3.digitaloceanspaces.com/owid-public/data/poverty/pip_dataset.csv)  ([raw](https://nyc3.digitaloceanspaces.com/owid-public/data/poverty/pip_dataset.csv)🔄)
- Enrich data: [world.py](https://github.com/gtherin/bulkhours/main/bulkhours/data/world.py)  ([raw](https://raw.githubusercontent.com/gtherin/bulkhours/main/bulkhours/data/world.py))
- Direct source: https://ourworldindata.org/poverty
- Reference site: https://pip.worldbank.org/

<details>
<summary>Show columns info</summary>
> <a href="https://github.com/owid/poverty-data/blob/main/datasets/pip_codebook.csv">https://github.com/owid/poverty-data/blob/main/datasets/pip_codebook.csv</a>

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


<details>
<summary>Show code</summary>
<code>
def get_gdp(self, timeopt=None, **data_info):
    timeopt = self.data_info["timeopt"] if "timeopt" in self.data_info else None
    df = self.read_raw_data(self.raw_data)
    df = df.set_index("country").stack().to_frame().reset_index()
    df.columns = ["country", "year", "gdp"]

    return geo_format(df, timeopt)
</code>
</details>

#### World Bank Gdp data (with gpx extra info)
#### `bulkhours.get_data("world.mapgdp")`
- Raw data: [pip_dataset.csv](https://nyc3.digitaloceanspaces.com/owid-public/data/poverty/pip_dataset.csv)  ([raw](https://nyc3.digitaloceanspaces.com/owid-public/data/poverty/pip_dataset.csv)🔄)
- Enrich data: [world.py](https://github.com/gtherin/bulkhours/main/bulkhours/data/world.py)  ([raw](https://raw.githubusercontent.com/gtherin/bulkhours/main/bulkhours/data/world.py))
- Direct source: https://ourworldindata.org/poverty
- Reference site: https://pip.worldbank.org/

<details>
<summary>Show columns info</summary>
> <a href="https://github.com/owid/poverty-data/blob/main/datasets/pip_codebook.csv">https://github.com/owid/poverty-data/blob/main/datasets/pip_codebook.csv</a>

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


<details>
<summary>Show code</summary>
<code>
def get_mapgdp(self, **kwargs):
    return get_mapgeneric(get_gdp(self, **kwargs))
</code>
</details>

#### Global economic data
#### `bulkhours.get_data("world.macro")`
- Raw data: [corruption.csv](https://github.com/gtherin/bulkhours/blob/main/data/corruption.csv), [cost_of_living.csv](https://github.com/gtherin/bulkhours/blob/main/data/cost_of_living.csv), [richest_countries.csv](https://github.com/gtherin/bulkhours/blob/main/data/richest_countries.csv), [unemployment.csv](https://github.com/gtherin/bulkhours/blob/main/data/unemployment.csv), [tourism.csv](https://github.com/gtherin/bulkhours/blob/main/data/tourism.csv), [continent.tsv](https://github.com/gtherin/bulkhours/blob/main/data/continent.tsv)
- Enrich data: [world.py](https://github.com/gtherin/bulkhours/main/bulkhours/data/world.py)  ([raw](https://raw.githubusercontent.com/gtherin/bulkhours/main/bulkhours/data/world.py))

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


<details>
<summary>Show code</summary>
<code>
def get_macro(self, **data_info):
    df = self.read_raw_data(self.raw_data)
    return geo_format(df, None)
</code>
</details>

#### Global economic data (with gpx extra info)
#### `bulkhours.get_data("world.mapmacro")`
- Raw data: [corruption.csv](https://github.com/gtherin/bulkhours/blob/main/data/corruption.csv), [cost_of_living.csv](https://github.com/gtherin/bulkhours/blob/main/data/cost_of_living.csv), [richest_countries.csv](https://github.com/gtherin/bulkhours/blob/main/data/richest_countries.csv), [unemployment.csv](https://github.com/gtherin/bulkhours/blob/main/data/unemployment.csv), [tourism.csv](https://github.com/gtherin/bulkhours/blob/main/data/tourism.csv), [continent.tsv](https://github.com/gtherin/bulkhours/blob/main/data/continent.tsv)
- Enrich data: [world.py](https://github.com/gtherin/bulkhours/main/bulkhours/data/world.py)  ([raw](https://raw.githubusercontent.com/gtherin/bulkhours/main/bulkhours/data/world.py))

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


<details>
<summary>Show code</summary>
<code>
def get_mapmacro(self, **kwargs):
    return get_mapgeneric(get_macro(self, **kwargs))
</code>
</details>

#### Corruption index per country
#### `bulkhours.get_data("world.corruption")`
- Raw data: [corruption.csv](https://github.com/gtherin/bulkhours/main/data/corruption.csv)  ([raw](https://raw.githubusercontent.com/gtherin/bulkhours/main/data/corruption.csv))

<details>
<summary>Show code</summary>
<code>
def get_corruption(self, show_truth=False, **data_info):
    show_truth = self.data_info["show_truth"] if "show_truth" in self.data_info else False
    df = self.read_raw_data(self.raw_data)

    if not show_truth:
        df["corruption_index"] = df["corruption_index"].where(
            ~df.index.isin(["Spain", "Japan", "Sweden", "Romania"]), other=np.nan
        )
    df = df[["annual_income", "corruption_index", "gdp_per_capita", "unemployment_rate"]]
    df = df.dropna(subset=["annual_income", "gdp_per_capita", "unemployment_rate"])

    return geo_format(df, None)
</code>
</details>

#### Life expectancy versus GDP/capita per country
#### `bulkhours.get_data("world.life_expectancy_vs_gdp_2018")`
- Raw data: [life-expectancy-vs-gdp-per-capita.csv](https://huggingface.co/datasets/guydegnol/bulkhours/blob/main/life-expectancy-vs-gdp-per-capita.csv)  ([raw](https://huggingface.co/datasets/guydegnol/bulkhours/raw/main/life-expectancy-vs-gdp-per-capita.csv)🤗)
- Enrich data: [world.py](https://github.com/gtherin/bulkhours/main/bulkhours/data/world.py)  ([raw](https://raw.githubusercontent.com/gtherin/bulkhours/main/bulkhours/data/world.py))
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


<details>
<summary>Show code</summary>
<code>
def get_life_expectancy_vs_gdp_2018(self, **data_info):
    return self.read_raw_data(self.raw_data)  # .dropna()
</code>
</details>

#### Evolution du PIB et de ses composantes par rapport au trimestre precedent en volume en %
#### `bulkhours.get_data("gmacro.fr_qgdp")`
- Enrich data: [gmacro.py](https://github.com/gtherin/bulkhours/main/bulkhours/data/gmacro.py)  ([raw](https://raw.githubusercontent.com/gtherin/bulkhours/main/bulkhours/data/gmacro.py))
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


<details>
<summary>Show code</summary>
<code>
def get_fr_qgdp(self):
    data = StringIO(
        """quarter;gdp;Importations;consommation_menages;consommation_APU1;capital_fixe;capital_fixe_non_financieres;menages;APU1;Exportations;demande_interieure;Variations de stocks;Commerce exterieur
2022-T4;0,1;-1,9;-0,9;0,2;0,8;1,2;-0,2;0,3;-0,3;-0,2;-0,2;0,5
2022-T3;0,2;3,9;0,5;0,2;2,3;3,8;-0,7;1,0;0,8;0,9;0,3;-1,0
2022-T2;0,5;1,5;0,5;0,0;0,3;0,5;-0,1;-0,2;1,0;0,3;0,3;-0,2
2022-T1;-0,2;1,3;-1,0;0,2;0,4;0,2;0,0;1,1;1,7;-0,4;0,1;0,1
2021-T4;0,6;5,0;0,6;0,6;-0,3;-0,2;-0,7;-0,5;2,9;0,4;0,8;-0,6
2021-T3;3,3;0,6;5,4;3,1;0,5;0,9;1,2;-1,6;2,1;3,7;-0,8;0,4
2021-T2;1,1;1,9;1,2;0,6;2,1;1,8;4,0;0,5;2,6;1,2;-0,3;0,1
2021-T1;0,1;1,4;0,5;-0,6;0,7;0,6;0,4;-1,5;-0,4;0,3;0,3;-0,6
2020-T4;-0,9;0,8;-5,5;-0,1;2,5;2,0;6,1;0,4;3,7;-2,4;0,7;0,8
2020-T3;18,4;17,7;18,2;17,6;24,2;24,8;28,8;17,4;22,4;19,7;-1,9;0,6
2020-T2;-13,5;-19,2;-11,6;-11,8;-14,3;-13,5;-16,3;-12,5;-25,3;-12,3;0,4;-1,6
2020-T1;-5,6;-5,5;-5,2;-3,3;-9,6;-8,8;-14,2;-5,1;-6,8;-5,8;0,6;-0,3
2019-T4;-0,3;-1,0;0,2;0,1;0,3;0,4;0,4;0,3;-1,1;0,2;-0,5;0,0
2019-T3;0,0;-0,4;0,2;0,4;0,8;0,6;0,9;1,2;-1,1;0,4;-0,1;-0,2
2019-T2;0,7;0,0;0,6;0,3;1,7;1,2;1,9;2,6;0,3;0,8;-0,2;0,1
2019-T1;0,7;2,2;0,8;0,1;1,0;0,4;0,4;3,0;0,3;0,7;0,6;-0,6
2018-T4;0,6;1,3;0,2;0,5;0,8;0,3;0,0;3,0;2,2;0,4;-0,1;0,3
2018-T3;0,4;-1,1;0,4;-0,1;0,7;0,6;0,4;1,2;0,2;0,4;-0,4;0,4
2018-T2;0,4;1,0;-0,1;0,3;1,3;1,7;0,7;1,5;0,9;0,3;0,2;-0,1
2018-T1;0,1;0,6;0,4;0,0;0,1;0,1;0,1;0,4;-0,2;0,2;0,1;-0,2
2017-T4;0,6;1,3;0,0;0,1;0,8;1,4;0,4;0,0;2,5;0,2;0,0;0,4
2017-T3;0,9;1,9;0,7;0,5;1,3;1,9;0,6;0,4;1,5;0,8;0,2;-0,1
2017-T2;0,8;-0,1;0,3;0,5;1,1;1,2;1,6;0,1;2,7;0,6;-0,6;0,9
2017-T1;0,8;2,2;0,4;0,1;2,4;3,1;2,1;-0,4;-0,3;0,8;0,8;-0,8
2016-T4;0,6;0,8;0,9;0,4;0,9;0,5;1,5;0,5;1,4;0,8;-0,4;0,2
2016-T3;0,3;2,0;0,0;0,5;0,4;0,0;1,1;-0,5;0,5;0,2;0,6;-0,5
2016-T2;-0,3;-1,7;0,0;0,2;-0,2;-0,9;0,7;0,1;0,2;0,0;-0,9;0,6
2016-T1;0,6;0,6;1,3;0,4;1,1;1,8;0,4;-0,7;-0,2;1,0;-0,1;-0,2
2015-T4;0,2;1,9;-0,1;0,4;1,1;1,1;0,8;1,1;0,9;0,3;0,3;-0,3
2015-T3;0,2;1,8;0,2;0,2;1,2;1,0;0,7;2,8;0,0;0,4;0,4;-0,6
2015-T2;0,1;0,1;0,3;0,2;-0,8;0,4;-0,3;-5,5;1,6;0,0;-0,4;0,5
2015-T1;0,5;2,1;0,5;0,2;1,0;1,6;0,0;0,2;0,9;0,6;0,4;-0,4
2014-T4;0,0;1,1;0,3;0,3;-0,7;-0,6;-0,8;-1,8;1,7;0,1;-0,3;0,2
2014-T3;0,6;1,8;0,3;0,4;0,5;1,5;-1,3;-1,4;1,6;0,4;0,3;-0,1
2014-T2;0,1;1,1;0,6;0,3;-0,3;0,3;-2,1;-1,5;0,0;0,3;0,1;-0,3
2014-T1;0,0;1,0;-0,5;0,3;-0,5;-0,5;-0,8;-1,8;0,7;-0,3;0,4;-0,1
2013-T4;0,6;1,2;0,6;0,3;0,8;1,3;0,4;-1,0;1,2;0,6;0,1;0,0
2013-T3;-0,1;1,0;0,0;0,3;0,1;0,6;-0,1;-1,1;-0,3;0,1;0,2;-0,4
2013-T2;0,7;2,2;0,4;0,5;0,2;0,7;0,0;0,0;2,3;0,4;0,3;0,0
2013-T1;0,1;-0,2;0,0;0,4;-0,6;-0,5;0,3;-0,1;0,0;0,0;0,1;0,1
2012-T4;-0,1;0,0;0,2;0,3;-0,4;-0,2;-0,2;-0,1;0,1;0,1;-0,3;0,0
2012-T3;0,2;0,4;0,1;0,3;0,3;0,6;-0,3;0,7;0,0;0,2;0,2;-0,1
2012-T2;-0,2;0,3;-0,2;0,5;-0,8;-0,9;-2,0;0,6;0,8;-0,2;-0,1;0,1
2012-T1;0,0;0,9;0,2;0,5;-0,5;-1,3;-0,3;0,4;0,5;0,1;0,0;-0,1
2011-T4;0,2;-0,8;-0,4;0,3;1,2;1,5;0,3;0,9;1,8;0,1;-0,7;0,7
2011-T3;0,5;0,1;0,2;0,6;0,6;0,8;-0,5;0,2;0,6;0,4;0,0;0,1
2011-T2;-0,1;-1,2;-1,2;0,1;0,2;0,3;-0,3;-0,6;1,0;-0,6;-0,2;0,6
2011-T1;1,1;3,9;0,5;0,3;0,2;1,0;-0,1;-2,8;2,4;0,4;1,2;-0,5
2010-T4;0,7;0,9;0,8;0,1;0,5;1,2;0,5;-1,7;1,5;0,6;0,0;0,1
2010-T3;0,6;2,8;0,6;0,4;1,3;1,6;1,7;-0,1;1,0;0,7;0,4;-0,5
2010-T2;0,5;4,2;0,3;0,2;0,8;1,4;1,3;-1,0;3,3;0,4;0,3;-0,2
2010-T1;0,3;0,7;0,2;0,1;1,0;1,9;0,9;-0,7;3,7;0,4;-0,8;0,8
2009-T4;0,7;3,7;0,7;0,5;0,5;1,0;-0,1;0,7;0,1;0,7;1,0;-1,0
2009-T3;0,2;1,0;0,0;0,5;-0,6;-0,5;-1,2;0,3;1,8;0,0;0,0;0,2
2009-T2;0,0;-1,9;0,7;0,7;-2,5;-3,5;-2,5;0,9;0,0;0,0;-0,5;0,5
2009-T1;-1,7;-7,1;-0,1;0,7;-4,1;-6,0;-5,3;2,9;-7,5;-0,8;-0,9;0,0
2008-T4;-1,5;-2,7;-0,4;0,8;-3,2;-4,2;-4,5;1,6;-4,7;-0,8;-0,2;-0,5
2008-T3;-0,2;-0,4;0,1;0,5;-0,8;-0,2;-2,9;-0,1;-0,9;0,0;0,0;-0,2
2008-T2;-0,5;-0,8;0,0;0,1;-1,1;-0,9;-1,5;-1,9;-1,5;-0,3;-0,1;-0,2
2008-T1;0,5;1,1;-0,4;0,1;1,6;2,7;-0,3;0,3;2,3;0,2;0,0;0,3
2007-T4;0,2;0,6;0,3;0,2;0,5;1,2;-0,2;-1,3;0,4;0,3;-0,1;-0,1
2007-T3;0,5;0,7;0,9;0,4;1,2;2,4;-0,2;-0,3;0,2;0,9;-0,2;-0,2
2007-T2;0,7;2,8;1,0;0,5;1,2;2,0;0,7;-0,1;1,6;0,9;0,1;-0,4
2007-T1;0,7;1,0;0,6;0,6;1,8;2,7;0,9;1,8;0,3;0,9;0,0;-0,2
2006-T4;0,7;2,6;0,5;0,5;1,5;2,3;0,7;1,0;1,9;0,8;0,1;-0,2
2006-T3;0,1;-0,6;0,2;0,1;0,7;0,9;0,7;-0,1;-1,5;0,3;0,0;-0,2
2006-T2;1,0;1,6;0,6;0,4;1,9;2,5;1,6;0,2;1,5;0,8;0,2;0,0
2006-T1;0,8;0,5;0,8;0,6;0,6;0,3;1,4;-0,9;2,2;0,7;-0,4;0,5
2005-T4;0,7;3,3;0,6;0,1;0,6;0,7;1,3;-1,3;2,3;0,5;0,5;-0,3
2005-T3;0,6;2,5;0,5;0,3;1,0;1,0;1,2;0,7;2,2;0,6;0,0;-0,1
2005-T2;0,3;0,9;0,2;0,4;0,5;0,2;1,7;0,5;1,4;0,3;-0,2;0,1
2005-T1;0,2;0,4;0,6;0,3;0,6;0,8;1,0;0,2;-0,7;0,5;0,0;-0,3
2004-T4;0,8;2,5;1,5;0,3;1,4;1,8;0,8;1,9;2,0;1,1;-0,3;-0,1
2004-T3;0,3;1,8;0,0;0,3;0,3;0,3;0,6;0,3;0,4;0,1;0,5;-0,4
2004-T2;0,6;2,0;0,4;0,5;0,5;0,2;1,1;0,5;1,7;0,5;0,2;0,0
2004-T1;1,0;0,7;0,6;0,6;1,1;1,0;1,3;0,8;0,4;0,7;0,4;-0,1
2003-T4;0,7;1,7;0,3;0,8;0,2;-0,4;0,9;0,7;2,6;0,4;0,0;0,3
2003-T3;0,7;0,9;0,6;0,4;1,7;2,1;1,0;0,9;1,1;0,7;-0,1;0,1
2003-T2;-0,2;-0,7;0,1;0,6;0,0;-0,9;0,5;1,4;-0,8;0,2;-0,3;-0,1
2003-T1;0,1;0,1;0,4;0,0;0,1;-0,5;0,4;1,1;-2,2;0,2;0,5;-0,6
2002-T4;0,2;0,0;0,6;0,7;1,1;0,9;0,7;1,5;0,1;0,7;-0,5;0,0
2002-T3;0,2;0,8;0,6;0,6;0,4;0,3;0,8;0,3;0,4;0,5;-0,2;-0,1
2002-T2;0,4;0,7;0,5;0,9;-0,6;-1,7;0,8;0,7;2,5;0,3;-0,4;0,5
2002-T1;0,6;2,5;0,4;0,2;-0,6;-1,1;0,8;-0,6;1,5;0,2;0,6;-0,2
2001-T4;-0,1;-0,6;0,4;0,3;-0,2;-0,8;0,8;0,6;-1,3;0,3;-0,1;-0,2
2001-T3;0,3;-1,6;0,2;0,3;0,1;0,5;0,4;-0,7;0,1;0,3;-0,5;0,5
2001-T2;0,1;-0,7;0,7;0,2;-0,3;-0,1;-0,1;-0,9;-2,3;0,4;0,2;-0,5
2001-T1;0,5;-1,4;1,0;0,2;0,6;1,2;0,3;-0,3;0,2;0,7;-0,7;0,4
2000-T4;0,8;3,2;0,3;0,2;0,6;1,0;0,0;0,2;4,0;0,3;0,2;0,3
2000-T3;0,7;3,8;0,6;0,3;1,9;3,2;0,1;0,8;2,1;0,8;0,3;-0,4
2000-T2;1,0;4,4;0,7;0,4;1,4;1,3;0,4;2,8;3,5;0,8;0,4;-0,2
2000-T1;1,0;4,3;0,7;0,6;1,7;1,2;1,5;3,2;4,0;0,9;0,2;0,0
1999-T4;1,4;4,4;1,0;0,6;1,9;1,5;1,2;3,3;2,4;1,1;0,8;-0,4
1999-T3;1,1;2,5;2,5;0,6;1,9;2,0;1,4;1,9;3,8;1,9;-1,1;0,4
1999-T2;0,3;1,8;0,4;0,3;1,7;2,1;1,3;1,0;2,1;0,7;-0,5;0,1
1999-T1;1,1;0,9;0,1;0,6;2,3;2,5;2,9;0,8;-0,3;0,7;0,7;-0,3
1998-T4;0,7;0,7;0,6;0,5;1,4;1,3;1,8;0,8;-0,3;0,7;0,2;-0,2
1998-T3;0,7;1,5;1,4;0,0;1,9;1,9;1,8;1,4;1,5;1,1;-0,4;0,0
1998-T2;0,8;2,0;1,0;-0,3;2,0;2,6;1,4;0,8;1,6;0,9;0,0;-0,1
1998-T1;0,9;4,0;0,9;-0,5;1,6;2,2;0,7;0,5;1,7;0,7;0,7;-0,5
1997-T4;1,0;2,8;1,2;-0,2;1,5;2,1;1,0;-0,1;3,0;0,9;-0,1;0,1
1997-T3;1,0;4,3;1,0;0,1;0,6;0,8;1,2;-1,4;3,1;0,6;0,5;-0,2
1997-T2;1,0;2,7;0,2;0,1;1,5;2,4;1,4;-1,3;4,5;0,4;0,1;0,5
1997-T1;0,3;1,8;-0,1;0,1;-1,0;-1,3;0,5;-2,4;3,4;-0,2;0,2;0,4
1996-T4;0,3;1,4;-1,1;0,6;-0,2;0,0;0,7;-1,8;3,1;-0,5;0,3;0,4
1996-T3;0,5;-0,2;1,4;0,4;0,5;0,6;1,1;-0,7;2,0;1,0;-0,9;0,5
1996-T2;0,1;0,4;-0,4;0,7;-0,3;-1,3;0,4;1,0;-0,2;-0,1;0,4;-0,1
1996-T1;0,7;0,9;1,7;0,8;0,8;1,0;0,3;0,2;1,8;1,2;-0,8;0,2
1995-T4;0,0;-0,4;-0,1;0,5;0,1;-0,1;-0,7;1,1;0,7;0,1;-0,4;0,2
1995-T3;0,2;0,6;-0,6;0,4;0,1;0,5;-0,4;-1,0;-0,9;-0,2;0,7;-0,3
1995-T2;0,6;3,3;1,6;0,1;-0,5;-0,7;-0,7;-0,1;2,6;0,8;-0,1;-0,1
1995-T1;0,3;0,0;0,1;-0,3;0,8;1,3;0,5;-1,6;1,5;0,1;-0,2;0,3
1994-T4;0,9;3,8;0,5;0,0;0,4;0,4;1,3;-1,0;4,6;0,4;0,3;0,2
1994-T3;0,9;3,2;0,4;0,0;0,8;1,7;1,5;-1,8;3,1;0,4;0,4;0,0
1994-T2;1,0;3,2;0,8;0,0;1,1;1,5;1,6;0,0;3,6;0,7;0,2;0,1
1994-T1;0,7;2,3;0,0;-0,2;1,6;1,4;1,9;2,7;0,0;0,3;0,8;-0,5
1993-T4;0,2;2,6;0,4;0,2;-0,3;-0,2;0,6;-0,2;3,4;0,2;-0,2;0,2
1993-T3;0,2;0,8;0,1;0,2;-1,3;-1,2;-0,7;-1,1;1,7;-0,2;0,2;0,2
1993-T2;0,0;-3,4;0,7;1,1;-1,8;-1,6;-1,5;-2,1;-2,8;0,2;-0,4;0,1
1993-T1;-0,7;0,2;-1,4;1,1;-1,7;-2,7;-1,3;-0,7;1,8;-0,9;-0,1;0,3
1992-T4;-0,2;-1,8;0,6;1,0;-1,4;-2,2;-1,7;-0,4;-1,3;0,2;-0,5;0,1
1992-T3;-0,1;-1,7;0,5;1,2;-1,1;-1,7;-0,7;-0,1;-0,8;0,3;-0,5;0,2
1992-T2;0,1;-0,8;0,2;0,7;-1,2;-0,9;-2,0;-0,7;0,7;0,0;-0,3;0,3
1992-T1;0,8;3,8;0,1;0,6;0,6;1,0;0,8;1,2;2,2;0,4;0,8;-0,4
1991-T4;0,7;-0,6;0,3;0,9;-0,7;-0,8;-3,4;0,9;2,2;0,2;-0,2;0,6
1991-T3;0,2;0,0;-0,1;0,5;-0,1;-0,5;-1,0;1,2;2,6;0,1;-0,4;0,6
1991-T2;0,4;0,0;0,1;1,3;0,4;0,6;-1,5;1,7;2,8;0,5;-0,6;0,6
1991-T1;0,1;2,9;-0,1;0,9;-0,9;-0,6;-2,7;0,1;0,7;-0,1;0,7;-0,5
1990-T4;0,0;-0,2;0,6;0,6;-0,1;0,0;-0,6;0,0;1,8;0,4;-0,9;0,4
1990-T3;0,5;-0,3;0,0;1,2;0,6;1,4;-2,0;1,0;0,6;0,4;-0,1;0,2
1990-T2;0,5;1,6;0,4;0,3;0,4;0,6;-1,2;1,5;-1,2;0,4;0,7;-0,6
1990-T1;0,4;0,1;1,1;1,2;1,4;1,9;-0,7;2,5;1,3;1,2;-1,0;0,2
1989-T4;1,3;4,2;0,4;0,8;2,0;2,7;0,2;2,1;3,3;0,9;0,7;-0,2
1989-T3;1,1;0,1;1,1;0,6;1,2;1,5;0,5;1,3;-0,4;1,0;0,1;-0,1
1989-T2;1,2;2,6;0,4;0,1;1,6;1,4;3,8;-0,4;2,6;0,6;0,6;0,0
1989-T1;1,2;1,9;1,0;0,6;2,4;3,5;0,7;1,7;4,3;1,2;-0,5;0,5
1988-T4;0,9;1,6;0,8;-0,2;1,6;1,1;3,6;1,0;1,4;0,8;0,1;-0,1
1988-T3;1,3;4,3;1,3;0,6;2,0;2,4;2,2;1,0;3,3;1,3;0,2;-0,2
1988-T2;0,8;0,5;0,5;0,6;1,8;2,0;0,7;2,8;1,5;0,8;-0,2;0,2
1988-T1;1,2;1,8;0,0;1,1;2,5;2,3;2,2;2,9;1,2;0,8;0,6;-0,1
1987-T4;1,4;2,3;1,8;1,3;1,9;2,5;-0,1;2,8;1,9;1,7;-0,2;-0,1
1987-T3;0,7;1,9;0,1;0,8;2,1;2,2;1,4;2,9;2,9;0,7;-0,2;0,2
1987-T2;1,5;2,4;1,3;0,7;2,3;3,0;0,0;3,4;2,6;1,4;0,0;0,0
1987-T1;0,1;4,1;1,0;0,4;0,3;0,4;2,2;-2,3;-0,9;0,7;0,5;-1,0
1986-T4;0,1;-2,5;0,2;0,8;0,8;0,9;0,7;0,9;-1,2;0,5;-0,7;0,4
1986-T3;0,5;3,2;0,5;0,7;0,9;1,3;-0,2;1,2;2,1;0,7;0,1;-0,3
1986-T2;1,1;1,7;1,6;0,7;1,5;1,4;-0,1;3,7;-1,9;1,4;0,6;-0,8
1986-T1;0,4;1,7;0,9;0,5;0,6;1,9;0,2;-2,5;-0,9;0,7;0,2;-0,6
1985-T4;0,4;1,8;1,1;0,8;0,6;0,5;0,7;0,5;1,2;0,9;-0,4;-0,1
1985-T3;0,5;1,9;0,6;0,4;1,4;1,4;1,3;1,5;-1,8;0,7;0,7;-0,9
1985-T2;0,9;0,6;0,5;0,8;1,7;2,7;-1,9;4,0;2,3;0,8;-0,3;0,4
1985-T1;0,3;1,6;1,4;0,8;-0,1;0,0;-0,9;0,6;-0,4;0,9;-0,1;-0,5
1984-T4;-0,1;1,9;-0,7;0,6;0,8;1,7;-1,5;1,5;-0,1;-0,1;0,5;-0,5
1984-T3;0,7;-1,3;0,2;1,2;-0,2;0,6;-3,1;1,5;1,3;0,3;-0,3;0,6
1984-T2;0,4;2,4;0,4;0,7;-0,5;-1,0;0,3;-1,1;3,8;0,2;-0,1;0,3
1984-T1;0,4;1,3;0,4;0,0;0,4;0,8;-1,2;1,0;-0,3;0,3;0,5;-0,4
1983-T4;0,6;0,6;0,5;0,6;-0,5;-0,2;-1,4;-0,4;1,8;0,3;0,0;0,3
1983-T3;0,1;2,6;-0,4;0,7;-0,4;-0,3;-0,5;-1,0;4,0;-0,2;0,0;0,3
1983-T2;0,0;-3,2;-0,2;0,0;-1,1;-1,1;-0,7;-1,9;2,3;-0,4;-0,9;1,2
1983-T1;0,4;-1,3;-0,2;0,5;-0,5;-1,2;0,5;0,0;-1,1;-0,1;0,5;0,1
1982-T4;0,6;-0,2;1,2;0,7;-1,0;0,0;-2,8;-1,2;3,6;0,6;-0,8;0,8
1982-T3;0,0;-1,2;0,0;1,7;-1,5;-2,0;-0,7;-1,5;-0,3;0,0;-0,3;0,2
1982-T2;0,7;2,0;1,0;0,7;0,4;1,4;-2,3;1,8;-2,6;0,8;0,9;-1,0
1982-T1;0,8;0,1;0,8;1,5;-0,6;0,4;-2,8;-0,1;-0,7;0,6;0,4;-0,2
1981-T4;0,6;1,3;1,4;0,7;0,6;1,1;-1,2;2,2;-2,5;1,0;0,4;-0,8
1981-T3;0,7;3,0;0,1;0,9;-0,1;-0,3;-0,5;0,9;3,2;0,2;0,4;0,0
1981-T2;0,7;-0,5;1,5;0,8;0,2;-0,2;0,1;1,1;3,0;1,0;-1,1;0,8
1981-T1;0,3;-1,8;-0,1;0,7;-0,5;-0,8;-1,4;1,2;1,1;0,0;-0,3;0,7
1980-T4;-0,2;-1,7;0,7;0,5;-0,7;-1,1;-0,5;-0,4;1,1;0,3;-1,1;0,6
1980-T3;0,2;0,5;0,7;0,8;-0,1;0,8;-1,6;0,0;-1,0;0,5;-0,1;-0,3
1980-T2;-0,7;-0,5;-1,2;0,8;-0,2;0,7;-1,4;-0,4;-0,9;-0,5;-0,1;-0,1
1980-T1;1,0;3,6;0,8;nd;0,8;1,2;1,3;-0,8;1,5;0,8;0,6;-0,4
1979-T4;0,3;0,2;0,5;nd;1,7;2,5;1,2;0,3;0,5;0,8;-0,6;0,1
1979-T3;1,3;3,9;0,2;nd;2,4;3,7;0,8;1,4;3,8;0,9;0,4;0,0
1979-T2;0,4;0,8;0,7;nd;0,8;1,2;-0,4;1,8;0,6;0,7;-0,2;0,0
1979-T1;1,1;3,3;1,0;nd;-0,7;-1,3;0,5;-1,9;1,9;0,5;0,8;-0,2
1978-T4;1,1;2,7;1,4;nd;1,3;1,3;1,0;1,7;1,6;1,3;0,0;-0,2
1978-T3;0,6;0,4;0,3;nd;0,3;-0,5;1,9;-0,2;1,3;0,5;-0,1;0,2
1978-T2;1,1;1,6;1,6;nd;1,4;1,7;1,1;1,2;1,5;1,5;-0,4;0,0
1978-T1;1,4;2,3;1,2;nd;1,5;1,1;3,9;-1,0;1,3;1,4;0,1;-0,2
1977-T4;0,8;0,3;0,4;nd;-0,4;-1,1;0,9;-0,7;1,7;0,4;0,1;0,3
1977-T3;0,8;-0,4;1,3;nd;0,3;0,1;0,6;0,1;2,3;1,0;-0,7;0,5
1977-T2;0,4;-0,2;0,2;nd;-0,5;0,8;0,5;-6,1;1,8;0,2;-0,2;0,4
1977-T1;1,1;-1,2;0,0;nd;0,9;2,4;-1,9;0,6;0,8;0,3;0,4;0,4
1976-T4;0,7;0,3;1,0;nd;-0,6;-1,1;1,3;-2,6;3,5;0,4;-0,4;0,6
1976-T3;1,2;3,9;1,4;nd;-1,7;-1,3;-2,3;-2,2;1,0;0,5;1,3;-0,6
1976-T2;1,4;4,7;0,9;nd;0,4;-0,7;3,2;-0,8;3,5;0,7;0,9;-0,3
1976-T1;1,0;7,4;1,4;nd;2,3;4,4;0,0;1,2;3,2;1,5;0,2;-0,7
1975-T4;2,1;5,0;1,9;nd;2,0;3,9;-0,6;1,8;1,7;1,9;0,9;-0,7
1975-T3;0,0;1,4;1,6;nd;-1,5;-2,7;-1,6;2,1;-0,1;0,7;-0,5;-0,3
1975-T2;0,0;0,2;0,8;nd;-0,6;-0,5;-2,6;2,6;-0,7;0,6;-0,5;-0,2
1975-T1;-0,8;-6,3;0,2;nd;-2,1;-2,9;-3,0;1,9;-4,1;-0,2;-1,2;0,7
1974-T4;-1,8;-6,1;-0,4;nd;-2,6;-4,5;-1,8;1,1;-0,6;-0,6;-2,2;0,9
1974-T3;1,1;-0,5;0,1;nd;-0,9;-2,1;-0,5;1,8;2,7;0,0;0,5;0,6
1974-T2;0,7;0,7;0,6;nd;0,8;1,4;0,1;-0,1;0,8;0,8;-0,2;0,0
1974-T1;1,6;2,9;0,2;nd;0,4;-0,9;2,5;0,6;4,2;0,4;0,9;0,3
1973-T4;1,2;2,0;2,4;nd;1,2;0,8;2,4;0,2;4,3;1,7;-1,0;0,4
1973-T3;1,5;4,1;0,5;nd;2,3;2,8;2,3;0,3;2,5;1,0;0,8;-0,3
1973-T2;1,4;1,5;0,7;nd;1,8;1,7;2,9;-0,3;2,6;1,1;0,2;0,2
1973-T1;1,8;5,3;2,4;nd;1,4;1,0;1,9;1,1;2,9;1,9;0,2;-0,4
1972-T4;1,6;5,7;0,8;nd;2,0;1,7;2,1;1,7;5,1;1,2;0,4;-0,1
1972-T3;1,4;1,4;2,3;nd;1,5;1,3;2,1;0,6;0,0;1,8;-0,2;-0,2
1972-T2;0,7;1,2;0,2;nd;1,3;1,0;2,1;0,4;3,9;0,7;-0,4;0,5
1972-T1;1,1;8,2;1,6;nd;1,7;0,8;5,0;-0,8;3,9;1,4;0,3;-0,6
1971-T4;1,0;-0,4;1,1;nd;0,9;1,7;0,2;-0,6;0,1;1,0;-0,2;0,1
1971-T3;1,3;5,4;1,5;nd;1,4;3,1;-1,4;1,0;4,3;1,4;0,1;-0,1
1971-T2;1,1;2,6;1,6;nd;1,8;3,0;-0,7;2,3;1,3;1,5;-0,2;-0,2
1971-T1;1,6;-1,3;0,8;nd;3,0;2,1;8,5;-2,1;2,3;1,5;-0,6;0,6
1970-T4;1,3;1,2;2,5;nd;0,2;2,0;-3,3;1,3;2,6;1,7;-0,6;0,2
1970-T3;1,1;4,1;0,6;nd;1,4;0,7;3,1;0,8;1,9;1,0;0,4;-0,3
1970-T2;1,8;3,7;1,2;nd;2,3;1,7;3,6;1,8;4,0;1,5;0,2;0,1
1970-T1;1,5;1,8;2,0;nd;-0,1;1,1;-3,6;1,4;4,6;1,3;-0,2;0,4
1969-T4;1,5;-1,1;-0,8;nd;1,6;-1,2;8,0;-0,2;4,9;0,2;0,4;0,9
1969-T3;1,4;-1,1;1,0;nd;1,4;0,3;3,3;1,7;3,1;1,2;-0,4;0,6
1969-T2;2,1;6,3;2,8;nd;3,7;5,3;1,6;2,1;3,3;2,8;-0,2;-0,5
1969-T1;0,9;4,4;-0,4;nd;-0,4;-0,1;-0,5;0,0;3,6;-0,1;1,1;-0,1
1968-T4;1,1;5,4;2,6;nd;1,7;3,2;-0,5;0,8;-2,6;2,1;0,2;-1,2
1968-T3;8,0;20,1;5,0;nd;9,1;14,3;4,1;2,2;26,5;5,7;1,6;0,8
1968-T2;-5,3;-8,4;-0,5;nd;-5,6;-8,0;0,0;-6,2;-14,1;-1,6;-2,8;-0,9
1968-T1;2,7;5,2;0,1;nd;2,7;2,7;4,4;0,1;6,1;0,9;1,7;0,1
1967-T4;1,0;1,8;0,7;nd;1,7;2,8;0,7;0,0;3,9;1,0;-0,2;0,3
1967-T3;1,1;2,1;1,2;nd;1,3;0,7;3,0;0,5;0,9;1,2;0,1;-0,2
1967-T2;1,2;-1,9;0,8;nd;1,6;1,4;3,2;0,4;2,6;1,0;-0,5;0,6
1967-T1;1,7;4,3;1,5;nd;3,0;2,4;3,2;4,2;3,2;1,9;-0,1;-0,1
1966-T4;0,6;3,4;1,7;nd;0,9;0,9;-0,6;2,8;-1,2;1,4;-0,1;-0,6
1966-T3;1,2;4,2;0,5;nd;1,8;3,0;-0,4;1,7;2,5;0,9;0,4;-0,2
1966-T2;1,6;2,3;1,9;nd;2,1;1,9;3,2;1,3;1,6;1,8;-0,1;-0,1
1966-T1;0,9;3,1;0,9;nd;1,5;2,9;0,9;-1,0;0,4;1,1;0,1;-0,3
1965-T4;1,5;2,2;0,3;nd;3,3;1,8;9,0;0,1;3,0;1,1;0,3;0,1
1965-T3;1,5;1,5;1,7;nd;0,3;0,0;0,3;1,1;2,9;1,2;0,1;0,2
1965-T2;1,8;2,7;2,5;nd;2,3;2,0;2,5;2,6;2,4;2,1;-0,3;0,0
1965-T1;0,5;-1,5;-0,3;nd;0,3;-0,7;0,9;1,8;2,9;0,1;-0,2;0,6
1964-T4;1,4;0,5;1,2;nd;1,4;-0,9;4,6;3,6;4,4;1,2;-0,3;0,5
1964-T3;0,8;-0,3;0,8;nd;2,7;2,0;4,2;2,4;0,7;1,3;-0,7;0,1
1964-T2;1,3;2,1;0,2;nd;1,2;0,8;1,9;1,8;-0,5;0,6;1,0;-0,3
1964-T1;2,2;5,9;2,0;nd;3,3;2,0;5,4;4,5;4,4;2,2;0,2;-0,2
1963-T4;-0,2;4,7;1,3;nd;0,0;2,1;-6,1;1,5;-0,4;0,9;-0,5;-0,7
1963-T3;3,4;2,4;2,0;nd;5,3;3,5;11,4;3,2;3,8;2,7;0,5;0,2
1963-T2;4,5;10,9;2,9;nd;6,0;4,2;3,8;14,2;4,8;3,4;1,7;-0,7
1963-T1;-1,0;0,1;1,7;nd;-0,1;0,5;3,8;-6,3;1,5;1,0;-2,2;0,2
1962-T4;1,1;1,4;0,9;nd;-0,2;-1,1;-0,1;2,3;1,9;0,7;0,4;0,1
1962-T3;1,9;4,1;1,7;nd;2,2;3,1;-0,1;2,5;-0,4;1,7;0,8;-0,5
1962-T2;1,5;-4,1;1,6;nd;1,0;0,7;0,0;2,9;-0,3;1,4;-0,3;0,5
1962-T1;2,2;4,2;3,2;nd;2,0;2,4;0,2;3,3;1,0;2,6;0,0;-0,4
1961-T4;1,8;3,0;1,2;nd;1,5;1,2;1,0;3,4;-0,7;1,4;0,9;-0,5
1961-T3;0,9;0,4;0,9;nd;2,7;2,9;1,8;3,3;0,4;1,4;-0,5;0,0
1961-T2;0,6;4,4;0,9;nd;0,6;-1,1;2,8;3,2;2,4;0,9;-0,1;-0,2
1961-T1;1,4;0,2;2,5;nd;5,3;6,9;3,6;2,8;1,4;2,8;-1,6;0,2
1960-T4;1,1;0,5;1,6;nd;2,3;2,0;3,1;2,3;0,1;1,6;-0,5;0,0
1960-T3;1,7;6,0;1,0;nd;2,7;3,1;2,4;1,7;3,3;1,3;0,6;-0,2
1960-T2;2,5;-1,0;1,4;nd;2,7;3,8;1,5;1,1;0,8;1,5;0,8;0,2
1960-T1;2,0;3,5;2,0;nd;-0,5;-1,5;0,6;0,8;6,8;1,0;0,4;0,6
1959-T4;2,5;7,6;0,8;nd;2,8;4,4;0,3;1,3;5,3;1,2;1,5;-0,2
1959-T3;1,1;0,7;0,7;nd;0,9;0,9;0,0;2,2;4,3;0,7;-0,1;0,5
1959-T2;1,2;4,4;-0,3;nd;2,6;3,8;-0,2;3,2;7,9;0,5;0,2;0,5
1959-T1;0,2;-3,0;0,9;nd;0,3;-0,6;-0,3;4,0;-1,6;0,7;-0,6;0,1
1958-T4;0,3;-2,0;1,7;nd;1,6;1,7;0,0;3,4;4,9;1,4;-1,9;0,9
1958-T3;-0,2;-2,0;-0,5;nd;0,3;-0,6;0,4;2,2;1,7;-0,2;-0,5;0,5
1958-T2;0,4;0,7;0,1;nd;-1,0;-2,6;1,0;0,9;-1,7;-0,2;0,9;-0,3
1958-T1;1,3;0,4;-1,1;nd;3,6;5,8;1,7;-0,6;1,0;0,1;1,1;0,1
1957-T4;0,3;-4,0;0,4;nd;1,1;0,8;2,2;0,0;-0,5;0,4;-0,6;0,5
1957-T3;1,7;-1,4;1,0;nd;1,9;1,8;2,7;1,0;-0,1;1,0;0,4;0,2
1957-T2;0,7;0,9;1,4;nd;-0,9;-3,6;2,9;2,0;1,5;0,7;-0,1;0,1
1957-T1;1,9;4,0;0,7;nd;4,6;6,0;2,6;3,6;5,7;1,5;0,2;0,2
1956-T4;1,5;2,4;1,4;nd;3,4;4,2;1,8;3,3;-0,3;1,7;0,1;-0,4
1956-T3;1,2;4,5;1,8;nd;1,0;0,5;0,6;3,2;1,8;1,5;0,1;-0,4
1956-T2;1,7;9,8;1,6;nd;5,7;9,9;-0,4;3,0;5,1;2,5;-0,2;-0,6
1956-T1;0,8;1,5;2,0;nd;-1,6;-3,3;-0,8;2,5;-6,1;1,2;0,5;-1,0
1955-T4;1,1;4,2;1,6;nd;1,8;2,6;-0,2;2,6;-0,6;1,6;0,1;-0,6
1955-T3;1,5;3,0;1,3;nd;2,5;3,3;1,0;2,5;1,6;1,5;0,1;-0,1
1955-T2;1,4;3,6;2,3;nd;3,8;5,1;2,6;2,3;-0,4;2,3;-0,4;-0,5
1955-T1;1,3;-0,2;1,7;nd;1,0;-1,1;4,1;2,4;0,5;1,3;0,0;0,1
1954-T4;0,7;0,7;0,2;nd;2,0;0,4;5,1;2,6;1,0;0,6;0,1;0,1
1954-T3;1,6;0,5;0,9;nd;4,1;3,8;5,7;3,2;4,1;1,4;-0,3;0,5
1954-T2;1,7;1,4;0,9;nd;4,8;4,9;5,7;3,6;2,6;1,5;0,1;0,2
1954-T1;1,4;3,0;1,2;nd;-0,9;-4,6;5,2;3,6;2,0;0,4;1,1;-0,1
1953-T4;1,6;-1,0;1,1;nd;2,6;1,9;4,1;3,2;5,1;1,2;-0,4;0,8
1953-T3;0,4;0,8;0,5;nd;1,9;1,3;2,8;2,5;-2,9;0,7;0,2;-0,5
1953-T2;1,6;-0,6;1,7;nd;2,1;2,4;1,5;1,6;0,2;1,5;0,0;0,1
1953-T1;1,2;2,6;1,6;nd;3,0;4,5;0,6;1,2;-1,5;1,7;0,2;-0,6
1952-T4;-0,2;-2,2;1,1;nd;-1,5;-3,5;0,7;2,1;-0,3;0,6;-1,1;0,3
1952-T3;1,0;1,0;1,0;nd;0,5;-0,6;1,2;3,6;1,0;0,9;0,1;0,0
1952-T2;-0,5;-4,1;0,6;nd;-2,5;-6,2;2,1;5,4;-0,1;0,1;-1,3;0,6
1952-T1;1,5;-0,7;1,5;nd;0,7;-1,6;3,4;6,9;-1,1;1,4;0,2;-0,1
1951-T4;1,0;3,7;1,0;nd;2,0;0,5;4,9;5,3;-4,4;1,3;1,0;-1,3
1951-T3;1,4;6,2;1,4;nd;1,4;-0,3;6,5;3,0;1,6;1,4;0,7;-0,6
1951-T2;0,8;5,9;0,6;nd;0,1;-1,9;7,7;0,1;-0,6;0,6;1,1;-0,9
1951-T1;0,3;3,2;1,8;nd;5,8;6,9;8,7;-2,3;0,1;2,3;-1,6;-0,4
1950-T4;2,4;6,4;1,3;nd;0,7;-0,4;7,5;-1,7;13,0;1,2;0,0;1,2
1950-T3;2,5;3,5;4,2;nd;2,5;2,5;5,6;-0,6;4,8;3,2;-1,0;0,3
1950-T2;2,5;-2,0;2,2;nd;1,7;1,5;3,3;1,0;3,6;1,9;-0,2;0,8
1950-T1;2,8;9,7;1,6;nd;0,3;-0,6;1,1;3,3;8,1;nd;nd;nd
1949-T4;1,3;-5,6;-0,4;nd;1,1;0,8;0,8;1,9;2,5;nd;nd;nd
1949-T3;1,5;-4,6;2,3;nd;1,3;1,1;1,0;1,9;0,8;nd;nd;nd
1949-T2;0,9;0,0;0,9;nd;1,5;1,3;1,7;1,8;3,1;nd;nd;nd""".replace(
            "nd", "NaN"
        )
        .replace("-T", "-Q")
        .replace(",", ".")
    )
    df = pd.read_csv(data, sep=";")
    df = df.set_index("quarter").astype(float)
    df["date"] = pd.PeriodIndex(df.index, freq="Q").to_timestamp()

    # return get_unemployement()
    return df.sort_values("date")
</code>
</details>

#### Évolution du produit intérieur brut et de ses composantes
#### `bulkhours.get_data("gmacro.fr_unemployement")`
- Enrich data: [gmacro.py](https://github.com/gtherin/bulkhours/main/bulkhours/data/gmacro.py)  ([raw](https://raw.githubusercontent.com/gtherin/bulkhours/main/bulkhours/data/gmacro.py))
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


<details>
<summary>Show code</summary>
<code>
def get_fr_unemployement(self):
    data = StringIO(
        """quarter,1975-T1,1975-T2,1975-T3,1975-T4,1976-T1,1976-T2,1976-T3,1976-T4,1977-T1,1977-T2,1977-T3,1977-T4,1978-T1,1978-T2,1978-T3,1978-T4,1979-T1,1979-T2,1979-T3,1979-T4,1980-T1,1980-T2,1980-T3,1980-T4,1981-T1,1981-T2,1981-T3,1981-T4,1982-T1,1982-T2,1982-T3,1982-T4,1983-T1,1983-T2,1983-T3,1983-T4,1984-T1,1984-T2,1984-T3,1984-T4,1985-T1,1985-T2,1985-T3,1985-T4,1986-T1,1986-T2,1986-T3,1986-T4,1987-T1,1987-T2,1987-T3,1987-T4,1988-T1,1988-T2,1988-T3,1988-T4,1989-T1,1989-T2,1989-T3,1989-T4,1990-T1,1990-T2,1990-T3,1990-T4,1991-T1,1991-T2,1991-T3,1991-T4,1992-T1,1992-T2,1992-T3,1992-T4,1993-T1,1993-T2,1993-T3,1993-T4,1994-T1,1994-T2,1994-T3,1994-T4,1995-T1,1995-T2,1995-T3,1995-T4,1996-T1,1996-T2,1996-T3,1996-T4,1997-T1,1997-T2,1997-T3,1997-T4,1998-T1,1998-T2,1998-T3,1998-T4,1999-T1,1999-T2,1999-T3,1999-T4,2000-T1,2000-T2,2000-T3,2000-T4,2001-T1,2001-T2,2001-T3,2001-T4,2002-T1,2002-T2,2002-T3,2002-T4,2003-T1,2003-T2,2003-T3,2003-T4,2004-T1,2004-T2,2004-T3,2004-T4,2005-T1,2005-T2,2005-T3,2005-T4,2006-T1,2006-T2,2006-T3,2006-T4,2007-T1,2007-T2,2007-T3,2007-T4,2008-T1,2008-T2,2008-T3,2008-T4,2009-T1,2009-T2,2009-T3,2009-T4,2010-T1,2010-T2,2010-T3,2010-T4,2011-T1,2011-T2,2011-T3,2011-T4,2012-T1,2012-T2,2012-T3,2012-T4,2013-T1,2013-T2,2013-T3,2013-T4,2014-T1,2014-T2,2014-T3,2014-T4,2015-T1,2015-T2,2015-T3,2015-T4,2016-T1,2016-T2,2016-T3,2016-T4,2017-T1,2017-T2,2017-T3,2017-T4,2018-T1,2018-T2,2018-T3,2018-T4,2019-T1,2019-T2,2019-T3,2019-T4,2020-T1,2020-T2,2020-T3,2020-T4,2021-T1,2021-T2,2021-T3,2021-T4,2022-T1,2022-T2,2022-T3
Femmes,"4,6","4,9","5,2","5,5","5,8","5,9","5,8","5,8","6,1","6,5","6,6","6,5","6,3","6,3","6,6","7,0","7,1","7,2","7,4","7,7","8,0","8,1","8,2","8,4","8,8","9,1","9,3","9,4","9,4","9,5","9,6","9,7","9,6","9,5","9,7","10,0","10,5","10,8","10,9","11,1","11,2","11,1","11,1","10,9","10,8","10,9","11,1","11,2","11,4","11,5","11,3","11,3","11,2","11,0","11,1","11,0","10,8","10,6","10,4","10,3","10,3","10,2","10,1","10,0","10,0","10,1","10,3","10,6","10,8","10,9","11,0","11,1","11,2","11,3","11,6","11,8","12,0","12,1","12,1","11,9","11,8","11,5","11,3","11,4","11,7","11,9","11,9","11,8","11,8","11,8","11,8","11,8","11,6","11,5","11,4","11,4","11,4","11,3","11,1","10,7","10,3","9,9","9,6","9,4","9,2","9,1","8,9","8,8","8,7","8,6","8,7","8,7","9,3","9,4","9,1","9,5","10,0","9,5","9,6","9,5","9,2","9,5","9,9","10,0","10,0","9,6","9,8","8,6","9,0","8,6","8,2","7,8","7,5","7,7","7,8","8,2","8,8","9,3","9,4","9,4","9,4","9,4","9,4","9,8","9,7","9,4","9,5","9,4","9,4","9,8","9,7","10,1","10,2","10,3","10,1","10,1","9,8","9,9","10,1","10,1","9,9","10,0","9,9","9,8","9,7","9,8","10,0","9,9","9,7","9,5","9,4","8,9","9,3","9,1","8,9","8,8","8,7","8,4","8,3","8,1","8,0","6,8","9,0","8,0","7,8","7,9","8,1","7,3","7,3","7,3","7,1"
Femmes_15-24,"9,8","10,4","11,1","11,8","12,8","13,1","12,7","12,6","13,5","14,6","15,0","14,7","14,4","14,5","15,7","16,6","16,9","17,3","17,8","18,7","19,7","20,2","20,4","20,9","21,8","22,6","23,2","23,5","23,5","23,8","24,1","24,1","23,8","23,9","24,5","25,6","27,2","28,2","28,5","28,7","28,4","27,5","27,2","26,6","26,1","26,1","26,2","26,0","25,8","25,5","25,0","24,7","24,5","24,1","23,9","23,1","22,5","22,1","21,5","21,6","21,6","21,4","21,2","21,5","21,8","22,4","23,0","23,2","23,8","23,9","24,4","25,0","25,6","26,3","27,0","27,5","28,2","28,9","29,1","29,0","28,7","27,7","26,8","27,1","27,5","28,1","28,7","29,0","29,1","28,8","28,3","27,7","26,6","26,2","26,2","26,3","26,7","26,4","25,4","23,9","22,4","21,3","20,5","20,1","20,0","19,8","19,6","19,9","20,0","19,7","19,4","20,1","22,8","23,3","21,4","23,3","24,4","24,6","24,9","24,8","24,1","24,6","27,2","26,9","27,6","27,4","28,9","25,0","26,4","24,0","22,0","22,7","21,4","21,9","22,1","23,8","25,9","26,6","26,9","26,4","25,9","28,7","28,4","28,1","29,2","27,2","26,5","26,4","26,2","26,5","28,0","30,7","30,0","30,3","29,2","28,5","27,7","26,5","27,1","27,2","27,1","28,2","27,5","26,8","27,3","28,4","29,3","26,9","25,2","26,6","24,2","23,8","25,4","23,0","22,6","22,9","21,5","20,9","21,0","23,0","22,8","24,1","26,0","21,5","21,3","19,6","19,7","15,0","15,8","17,5","16,5"
Femmes_25-49,"3,3","3,5","3,7","3,9","4,0","4,0","4,0","4,0","4,1","4,3","4,4","4,4","4,3","4,2","4,4","4,5","4,5","4,6","4,7","4,8","4,9","5,0","5,0","5,2","5,5","5,8","5,9","6,0","6,0","6,1","6,2","6,2","6,2","6,1","6,2","6,4","6,7","6,9","7,0","7,2","7,4","7,6","7,7","7,7","7,7","7,9","8,2","8,4","8,7","8,9","8,8","8,9","8,9","8,8","9,1","9,1","9,1","8,9","8,8","8,7","8,6","8,6","8,5","8,5","8,4","8,4","8,7","9,0","9,2","9,4","9,5","9,5","9,6","9,8","10,0","10,3","10,6","10,7","10,7","10,5","10,3","10,2","10,1","10,2","10,5","10,6","10,6","10,5","10,5","10,6","10,7","10,7","10,6","10,5","10,5","10,5","10,5","10,4","10,2","9,9","9,6","9,3","9,1","8,8","8,7","8,5","8,4","8,2","8,0","8,0","8,1","8,1","8,6","8,6","8,4","8,6","8,9","8,6","8,7","8,6","8,4","8,7","8,7","9,0","8,9","8,2","8,5","7,6","7,7","7,6","7,6","6,9","6,6","6,8","6,9","7,3","7,7","8,1","8,3","8,3","8,3","8,0","8,1","8,6","8,4","8,3","8,6","8,4","8,7","8,9","8,8","8,8","9,0","9,2","8,9","9,0","8,6","9,1","9,2","9,3","9,1","9,0","9,0","8,9","8,9","8,7","8,7","9,1","8,9","8,6","9,0","8,1","8,7","8,5","8,2","7,9","7,8","7,6","7,5","7,1","7,1","5,9","8,0","7,1","7,3","7,2","7,4","6,9","6,7","6,6","6,4"
Femmes_plus_50,"2,1","2,2","2,4","2,5","2,6","2,7","2,8","3,0","3,2","3,3","3,3","3,1","2,9","2,9","3,1","3,3","3,5","3,7","3,9","4,2","4,5","4,6","4,6","4,6","4,7","4,7","4,8","4,8","4,8","4,9","5,1","5,1","5,1","5,1","5,1","5,2","5,4","5,5","5,5","5,6","5,7","5,7","5,9","5,8","5,6","5,6","5,6","5,8","6,2","6,4","6,6","6,7","6,6","6,5","6,4","6,4","6,4","6,3","6,2","6,1","6,1","6,0","6,1","6,1","6,3","6,4","6,6","6,8","6,9","6,9","6,8","6,6","6,3","6,2","6,2","6,3","6,2","6,0","6,0","6,0","6,1","6,1","6,0","6,0","6,4","6,5","6,7","6,8","6,9","6,9","6,9","6,9","7,0","7,0","7,0","7,0","6,9","6,9","6,8","6,6","6,4","6,2","6,0","5,7","5,5","5,5","5,5","5,2","5,2","5,4","5,4","5,2","4,8","5,5","5,5","5,9","6,6","5,3","5,3","5,6","5,4","5,0","5,6","5,4","5,3","5,8","5,4","4,8","5,3","4,9","4,5","4,3","4,0","4,4","4,5","4,4","4,8","5,5","5,1","5,9","5,8","5,5","5,6","5,8","5,8","5,5","5,7","5,9","5,4","6,3","5,8","6,1","6,4","6,5","6,6","6,6","6,9","6,6","6,9","6,5","6,2","6,6","6,4","6,5","6,3","6,2","6,8","6,4","6,8","6,3","6,1","6,0","6,0","6,3","6,1","6,5","6,7","6,2","6,1","5,6","5,4","4,0","6,3","5,7","4,8","5,8","5,7","5,5","5,6","5,1","5,3"
Hommes,"2,3","2,6","2,8","2,9","2,9","2,8","2,7","2,7","2,9","3,1","3,3","3,3","3,2","3,3","3,5","3,7","3,8","3,8","3,8","3,8","3,7","3,7","3,7","4,0","4,4","4,7","4,9","5,1","5,2","5,3","5,5","5,6","5,6","5,7","5,8","6,1","6,5","6,9","7,2","7,5","7,6","7,6","7,7","7,7","7,7","7,7","7,7","7,6","7,6","7,6","7,5","7,4","7,4","7,2","7,1","6,8","6,6","6,4","6,3","6,3","6,3","6,3","6,3","6,3","6,3","6,4","6,6","6,8","7,1","7,3","7,6","7,9","8,2","8,6","9,0","9,4","9,6","9,6","9,4","9,1","8,8","8,6","8,5","8,7","9,0","9,3","9,4","9,6","9,7","9,7","9,6","9,5","9,2","9,1","9,0","9,1","9,2","9,1","8,8","8,4","8,0","7,6","7,2","6,9","6,6","6,5","6,7","6,9","7,1","7,2","7,2","7,3","7,6","7,7","7,8","8,1","8,1","8,1","8,2","8,3","8,2","8,2","8,2","8,2","8,4","8,4","8,1","8,1","8,0","7,7","7,7","7,1","6,9","6,9","7,1","7,3","8,4","9,1","9,0","9,6","9,4","9,2","9,1","8,7","8,7","8,8","9,0","9,3","9,6","9,6","9,8","10,2","10,5","10,6","10,4","10,2","10,5","10,4","10,5","10,8","10,7","11,0","10,8","10,7","10,7","10,3","9,8","10,2","9,6","9,6","9,6","9,1","9,2","9,1","9,1","8,7","8,8","8,5","8,5","8,3","7,8","7,4","9,0","8,2","8,5","8,0","7,9","7,5","7,4","7,6","7,6"
Hommes_15-24,"4,8","5,4","5,8","6,0","6,0","5,8","5,6","5,9","6,6","7,2","7,5","7,2","6,8","6,9","7,5","7,9","8,0","8,0","8,0","8,0","8,2","8,2","8,3","9,0","9,8","10,5","11,1","11,5","11,7","12,0","12,5","12,8","12,9","13,1","13,7","14,6","15,8","17,0","17,8","18,2","18,5","18,0","17,7","17,3","16,9","16,9","16,3","15,8","15,5","15,3","15,1","15,2","15,1","14,6","14,0","13,2","12,5","12,2","12,2","12,5","12,9","13,0","13,0","13,1","12,9","13,2","13,3","13,4","13,7","14,1","15,1","16,0","16,8","17,8","18,6","19,1","19,7","20,1","19,3","18,3","17,4","16,6","16,1","17,0","17,6","18,6","19,1","19,6","19,9","19,8","19,4","18,9","18,4","18,3","18,9","19,5","20,2","19,9","18,9","17,5","16,2","15,4","14,8","14,4","14,2","14,2","14,8","15,3","15,6","15,9","16,6","16,9","16,0","17,7","18,4","19,3","19,2","18,9","19,6","19,4","19,5","18,9","19,9","19,6","21,1","20,7","19,1","21,0","19,1","18,8","18,2","17,7","16,7","17,8","19,1","20,2","22,6","24,1","24,2","24,4","23,5","21,7","23,1","20,4","21,1","21,6","21,0","22,0","22,6","23,7","24,4","25,6","25,1","24,1","23,6","22,5","23,3","24,6","24,4","25,3","25,6","24,3","24,8","25,3","25,3","24,0","23,8","23,7","22,7","23,1","22,2","21,2","21,0","21,3","22,1","19,0","20,7","20,1","19,0","20,4","18,8","20,9","20,3","19,1","20,7","19,4","18,8","17,0","17,3","18,5","19,8"
Hommes_25-49,"1,7","1,9","2,1","2,1","2,1","2,0","1,9","1,9","2,0","2,1","2,3","2,3","2,3","2,4","2,5","2,6","2,8","2,8","2,8","2,7","2,6","2,6","2,6","2,9","3,1","3,4","3,6","3,8","3,8","3,9","4,0","4,0","4,0","4,0","4,2","4,4","4,7","5,0","5,2","5,4","5,6","5,6","5,8","5,9","5,9","6,0","6,1","6,1","6,2","6,2","6,1","6,1","6,1","6,0","6,0","5,8","5,6","5,5","5,5","5,4","5,4","5,4","5,4","5,4","5,5","5,6","5,8","6,0","6,2","6,4","6,7","7,0","7,4","7,8","8,2","8,5","8,7","8,7","8,6","8,4","8,2","8,0","8,0","8,1","8,3","8,5","8,6","8,8","8,9","9,0","9,0","8,8","8,5","8,3","8,2","8,2","8,2","8,2","7,9","7,6","7,3","6,9","6,6","6,3","6,0","6,0","6,1","6,3","6,5","6,6","6,4","6,4","7,0","7,0","6,9","7,3","7,3","7,2","7,3","7,7","7,5","7,6","7,4","7,3","7,4","7,5","7,3","6,9","7,2","7,0","7,0","6,4","6,2","5,9","6,1","6,2","7,3","8,0","7,8","8,5","8,4","8,4","8,1","8,0","7,9","8,0","8,3","8,7","8,9","8,9","9,0","9,2","9,6","9,9","9,8","9,7","10,0","9,7","9,9","10,0","9,9","10,2","9,9","9,8","9,9","9,5","8,6","9,2","8,7","8,7","8,6","8,2","8,3","8,2","8,1","8,1","7,8","7,6","7,7","7,4","7,0","6,7","8,7","7,6","7,6","6,9","6,9","6,7","6,5","6,7","6,5"
Hommes_plus_50,"1,8","2,0","2,1","2,2","2,2","2,2","2,2","2,2","2,3","2,5","2,5","2,6","2,7","2,7","2,8","2,9","2,9","3,0","3,0","3,0","3,0","3,0","3,1","3,2","3,4","3,5","3,6","3,7","3,8","3,8","3,9","3,9","3,9","4,0","4,0","4,0","4,1","4,3","4,4","4,5","4,6","4,8","5,1","5,3","5,3","5,4","5,3","5,3","5,4","5,4","5,4","5,4","5,4","5,2","5,1","5,0","5,0","4,8","4,6","4,5","4,4","4,3","4,3","4,4","4,4","4,5","4,8","5,0","5,3","5,5","5,5","5,4","5,3","5,4","5,6","5,8","5,9","5,8","5,8","5,7","5,8","5,8","5,8","5,8","6,1","6,3","6,3","6,3","6,4","6,4","6,4","6,5","6,5","6,6","6,7","6,7","6,7","6,6","6,4","6,1","5,8","5,5","5,1","4,7","4,4","4,3","4,4","4,5","4,6","4,8","4,9","4,9","4,9","4,7","5,2","5,1","5,0","5,5","4,9","4,7","4,6","4,6","4,9","5,4","5,3","5,2","5,0","5,2","5,2","4,6","4,7","4,2","4,3","4,9","4,4","4,3","4,8","5,1","5,5","5,8","5,7","5,5","5,5","5,4","5,2","5,5","5,8","5,8","6,1","5,9","6,1","6,8","6,9","7,0","7,0","6,6","6,9","6,9","6,6","7,5","7,0","7,9","7,6","7,4","7,2","7,2","7,4","7,4","6,9","6,8","7,1","6,8","6,8","6,5","6,3","6,1","6,6","6,3","6,4","6,0","5,5","4,7","5,9","5,7","6,0","6,1","6,0","5,9","5,5","5,2","5,0"
Ensemble,"3,2","3,5","3,8","3,9","4,0","4,0","3,9","4,0","4,2","4,5","4,7","4,6","4,5","4,5","4,8","5,0","5,1","5,2","5,3","5,4","5,5","5,5","5,6","5,8","6,2","6,5","6,8","6,9","7,0","7,1","7,2","7,3","7,3","7,3","7,5","7,8","8,2","8,6","8,8","9,0","9,1","9,1","9,1","9,1","9,0","9,1","9,1","9,2","9,3","9,3","9,2","9,1","9,0","8,9","8,9","8,7","8,4","8,3","8,1","8,1","8,1","8,0","8,0","8,0","7,9","8,1","8,3","8,5","8,7","8,9","9,1","9,3","9,6","9,9","10,2","10,5","10,7","10,7","10,6","10,4","10,2","9,9","9,8","9,9","10,2","10,5","10,5","10,6","10,7","10,7","10,6","10,5","10,3","10,2","10,1","10,2","10,2","10,2","9,9","9,5","9,1","8,7","8,4","8,0","7,8","7,7","7,7","7,8","7,8","7,9","7,9","7,9","8,4","8,5","8,4","8,8","9,0","8,8","8,9","8,9","8,6","8,8","9,0","9,1","9,2","9,0","8,9","8,4","8,5","8,1","8,0","7,5","7,2","7,3","7,4","7,7","8,6","9,2","9,2","9,5","9,4","9,3","9,2","9,2","9,2","9,1","9,2","9,3","9,5","9,7","9,7","10,2","10,3","10,5","10,3","10,1","10,1","10,2","10,3","10,5","10,3","10,5","10,3","10,2","10,2","10,0","9,9","10,0","9,6","9,5","9,5","9,0","9,3","9,1","9,0","8,7","8,7","8,4","8,4","8,2","7,9","7,1","9,0","8,1","8,2","7,9","8,0","7,4","7,3","7,4","7,3"
Ensemble_15-24,"7,0","7,6","8,2","8,6","9,1","9,1","8,9","8,9","9,7","10,6","11,0","10,6","10,2","10,4","11,2","11,9","12,1","12,3","12,5","12,9","13,5","13,6","13,8","14,4","15,3","16,1","16,7","17,0","17,0","17,4","17,8","17,9","17,8","18,0","18,5","19,6","21,0","22,1","22,6","23,0","23,0","22,3","22,0","21,5","21,1","21,1","20,9","20,5","20,2","20,0","19,7","19,6","19,4","19,0","18,5","17,7","17,0","16,7","16,4","16,7","16,9","16,8","16,7","16,9","17,0","17,4","17,7","17,8","18,3","18,5","19,3","20,1","20,8","21,7","22,5","23,0","23,6","24,0","23,7","23,2","22,6","21,7","21,0","21,6","22,1","22,9","23,4","23,8","24,0","23,8","23,4","22,9","22,1","21,9","22,1","22,5","23,0","22,8","21,7","20,4","19,0","18,0","17,4","16,9","16,8","16,7","17,0","17,3","17,5","17,6","17,8","18,3","19,1","20,3","19,8","21,1","21,6","21,5","22,0","21,8","21,5","21,5","23,2","22,9","24,1","23,7","23,5","22,8","22,5","21,2","19,9","19,9","18,8","19,7","20,4","21,8","24,1","25,2","25,5","25,3","24,6","24,9","25,5","23,8","24,8","24,2","23,5","24,0","24,2","25,0","26,0","27,9","27,3","26,9","26,1","25,3","25,3","25,5","25,6","26,2","26,3","26,1","26,1","26,0","26,2","26,0","26,4","25,2","23,9","24,7","23,0","22,4","23,0","22,1","22,3","20,7","21,1","20,5","19,9","21,6","20,6","22,4","22,9","20,2","21,0","19,5","19,2","16,1","16,6","18,0","18,3"
Ensemble_25-49,"2,3","2,5","2,7","2,8","2,8","2,8","2,7","2,7","2,8","3,0","3,1","3,2","3,1","3,1","3,2","3,4","3,5","3,5","3,6","3,6","3,6","3,5","3,6","3,8","4,1","4,4","4,6","4,7","4,8","4,8","4,9","4,9","4,9","4,9","5,0","5,3","5,6","5,8","6,0","6,2","6,4","6,5","6,6","6,7","6,7","6,8","7,0","7,1","7,3","7,4","7,3","7,3","7,3","7,2","7,3","7,3","7,1","7,0","6,9","6,9","6,9","6,8","6,8","6,8","6,8","6,9","7,1","7,3","7,6","7,8","7,9","8,1","8,4","8,7","9,0","9,4","9,6","9,6","9,6","9,4","9,2","9,0","8,9","9,1","9,3","9,5","9,5","9,6","9,7","9,7","9,8","9,7","9,5","9,3","9,2","9,2","9,3","9,2","9,0","8,7","8,4","8,0","7,8","7,5","7,3","7,2","7,2","7,2","7,2","7,2","7,2","7,2","7,8","7,8","7,6","7,9","8,1","7,9","8,0","8,1","7,9","8,1","8,0","8,1","8,1","7,8","7,9","7,3","7,4","7,3","7,3","6,6","6,4","6,4","6,5","6,7","7,5","8,0","8,0","8,4","8,3","8,2","8,1","8,3","8,2","8,1","8,4","8,6","8,8","8,9","8,9","9,0","9,3","9,5","9,4","9,4","9,3","9,4","9,6","9,7","9,5","9,6","9,5","9,3","9,4","9,1","8,7","9,2","8,8","8,6","8,8","8,1","8,5","8,4","8,2","8,0","7,8","7,6","7,6","7,3","7,1","6,3","8,3","7,4","7,4","7,0","7,1","6,8","6,6","6,6","6,5"
Ensemble_plus_50,"1,9","2,1","2,2","2,3","2,4","2,4","2,4","2,5","2,7","2,8","2,8","2,8","2,8","2,8","2,9","3,0","3,2","3,3","3,4","3,5","3,6","3,6","3,7","3,8","3,9","4,0","4,1","4,1","4,2","4,3","4,4","4,4","4,4","4,4","4,4","4,5","4,6","4,8","4,9","5,0","5,0","5,2","5,4","5,5","5,4","5,5","5,4","5,5","5,7","5,8","5,9","5,9","5,9","5,8","5,7","5,6","5,6","5,4","5,3","5,2","5,1","5,1","5,1","5,1","5,2","5,4","5,6","5,8","6,0","6,1","6,0","5,9","5,7","5,7","5,8","6,0","6,0","5,9","5,9","5,9","5,9","5,9","5,9","5,9","6,2","6,4","6,5","6,5","6,6","6,6","6,7","6,7","6,7","6,8","6,8","6,8","6,8","6,8","6,6","6,3","6,1","5,8","5,5","5,2","4,9","4,9","4,9","4,8","4,9","5,1","5,1","5,0","4,8","5,1","5,3","5,5","5,7","5,4","5,1","5,2","5,0","4,8","5,2","5,4","5,3","5,5","5,2","5,0","5,3","4,7","4,6","4,2","4,1","4,7","4,5","4,3","4,8","5,3","5,3","5,8","5,7","5,5","5,5","5,6","5,5","5,5","5,8","5,8","5,8","6,1","6,0","6,5","6,7","6,8","6,8","6,6","6,9","6,7","6,8","7,0","6,6","7,2","7,0","6,9","6,7","6,7","7,1","6,9","6,8","6,5","6,6","6,4","6,4","6,4","6,2","6,3","6,6","6,2","6,3","5,8","5,5","4,4","6,1","5,7","5,4","5,9","5,8","5,7","5,5","5,2","5,1"
Longue_duree,nd,nd,nd,nd,nd,nd,nd,nd,nd,nd,nd,nd,nd,nd,nd,nd,nd,nd,nd,nd,nd,nd,nd,nd,nd,nd,nd,nd,nd,nd,nd,nd,nd,nd,nd,nd,nd,nd,nd,nd,nd,nd,nd,nd,nd,nd,nd,nd,nd,nd,nd,nd,nd,nd,nd,nd,nd,nd,nd,nd,nd,nd,nd,nd,nd,nd,nd,nd,nd,nd,nd,nd,nd,nd,nd,nd,nd,nd,nd,nd,nd,nd,nd,nd,nd,nd,nd,nd,nd,nd,nd,nd,nd,nd,nd,nd,nd,nd,nd,nd,nd,nd,nd,nd,nd,nd,nd,nd,nd,nd,nd,nd,"2,2","2,2","2,2","2,4","2,3","2,3","2,3","2,5","2,4","2,5","2,5","2,3","2,4","2,5","2,5","2,4","2,4","2,1","2,1","1,9","1,9","1,9","1,8","1,7","1,7","2,0","2,1","2,3","2,5","2,4","2,4","2,4","2,4","2,5","2,6","2,6","2,6","2,6","2,6","2,7","2,8","2,8","2,8","3,0","3,0","3,1","3,1","3,1","3,1","3,1","3,1","3,1","3,2","3,2","3,1","3,1","3,0","3,0","3,0","2,7","2,6","2,6","2,5","2,5","2,4","2,3","2,2","2,2","2,0","1,4","2,2","2,1","2,5","2,3","2,4","2,2","2,2","2,1","2,0"
""".replace(
            "nd", "NaN"
        ).replace(
            "-T", "-Q"
        )
    )

    df = pd.read_csv(data, sep=",", quotechar='"').set_index("quarter").T
    for c in df.columns:
        df[c] = df[c].astype(str).str.replace(",", ".").astype(float)
    df["date"] = pd.PeriodIndex(df.index, freq="Q").to_timestamp()
    return df.sort_values("date")
</code>
</details>

#### United States Macroeconomic data (1959q1 - 2009q3)
#### `bulkhours.get_data("gmacro.us_gdp")`
- Enrich data: [gmacro.py](https://github.com/gtherin/bulkhours/main/bulkhours/data/gmacro.py)  ([raw](https://raw.githubusercontent.com/gtherin/bulkhours/main/bulkhours/data/gmacro.py))
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


<details>
<summary>Show code</summary>
<code>
def get_us_gdp(self, simplify=True):
    import statsmodels.api as sm  # Statistical models

    us_okun = sm.datasets.macrodata.load_pandas().data
    if not simplify:
        return us_okun

    us_okun["diff(gdp)"] = 100 * us_okun["realgdp"].diff() / us_okun["realgdp"]
    us_okun["diff(unemployement)"] = us_okun["unemp"].diff()
    us_okun["yquarter"] = us_okun["year"].astype(str).str[:4] + "-Q" + us_okun["quarter"].astype(str).str[0]
    us_okun = us_okun[["yquarter", "diff(gdp)", "diff(unemployement)"]]
    us_okun = us_okun.dropna()
    us_okun["quarter"] = pd.PeriodIndex(us_okun["yquarter"], freq="Q").to_timestamp()

    return us_okun.set_index("quarter")
</code>
</details>

#### France Macroeconomic data
#### `bulkhours.get_data("gmacro.fr_gdp")`
- Enrich data: [gmacro.py](https://github.com/gtherin/bulkhours/main/bulkhours/data/gmacro.py)  ([raw](https://raw.githubusercontent.com/gtherin/bulkhours/main/bulkhours/data/gmacro.py))

<details>
<summary>Show columns info</summary>

| Column   |      Info |
|-----------|:-----------|
| yquarter |  |
| diff(gdp) |  |
| diff(unemployement) |  |

</details>


<details>
<summary>Show code</summary>
<code>
def get_fr_gdp(self, simplify=True):
    gdp = get_fr_qgdp(self).reset_index()
    une = get_fr_unemployement(self).reset_index()
    fr_okun = gdp.merge(une, how="inner", left_on="quarter", right_on="index")

    if not simplify:
        return fr_okun

    if simplify:
        fr_okun = fr_okun.rename(columns={"gdp": "diff(gdp)", "quarter": "yquarter"})
        fr_okun["diff(unemployement)"] = fr_okun["Ensemble"].diff()
        fr_okun = fr_okun[["yquarter", "diff(gdp)", "diff(unemployement)"]]
        fr_okun = fr_okun.dropna()
        fr_okun["quarter"] = pd.PeriodIndex(fr_okun["yquarter"], freq="Q").to_timestamp()

    return fr_okun.set_index("quarter")
</code>
</details>

#### World happiness report data (2015-2020)
#### `bulkhours.get_data("world.happiness")`
- Raw data: [DataForFigure2.1WHR2023.xls](https://happiness-report.s3.amazonaws.com/2023/DataForFigure2.1WHR2023.xls)  ([raw](https://happiness-report.s3.amazonaws.com/2023/DataForFigure2.1WHR2023.xls)🔄)
- Direct source: https://worldhappiness.report/data/

<details>
<summary>Show code</summary>
<code>
def get_happiness(self, **data_info):
    df = self.read_raw_data(self.raw_data)

    return df.sort_values("Ladder score", ascending=False)[
        [
            "Country name",
            "Ladder score",
            "Logged GDP per capita",
            "Social support",
            "Healthy life expectancy",
            "Freedom to make life choices",
            "Generosity",
            "Perceptions of corruption",
        ]
    ].rename(columns={"Country name": "country"})
</code>
</details>

#### World Bank Poverty and Inequality data (with gpx extra info)
#### `bulkhours.get_data("world.maphappiness")`
- Raw data: [DataForFigure2.1WHR2023.xls](https://happiness-report.s3.amazonaws.com/2023/DataForFigure2.1WHR2023.xls)  ([raw](https://happiness-report.s3.amazonaws.com/2023/DataForFigure2.1WHR2023.xls)🔄)
- Direct source: https://worldhappiness.report/data/

<details>
<summary>Show code</summary>
<code>
def get_mappoverty(self, **kwargs):
    return get_mapgeneric(get_happiness(self, **kwargs))
</code>
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

#### Standardized country information (iso m49)
#### `bulkhours.get_data("continent")`
- Raw data: [continent.tsv](https://github.com/gtherin/bulkhours/main/data/continent.tsv)  ([raw](https://raw.githubusercontent.com/gtherin/bulkhours/main/data/continent.tsv))

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
- Raw data: [corruption.csv](https://github.com/gtherin/bulkhours/main/data/corruption.csv)  ([raw](https://raw.githubusercontent.com/gtherin/bulkhours/main/data/corruption.csv))

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
- Raw data: [cost_of_living.csv](https://github.com/gtherin/bulkhours/main/data/cost_of_living.csv)  ([raw](https://raw.githubusercontent.com/gtherin/bulkhours/main/data/cost_of_living.csv))

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
- Raw data: [richest_countries.csv](https://github.com/gtherin/bulkhours/main/data/richest_countries.csv)  ([raw](https://raw.githubusercontent.com/gtherin/bulkhours/main/data/richest_countries.csv))

<details>
<summary>Show columns info</summary>

| Column   |      Info |
|-----------|:-----------|
| country   |   |         
| gdp_per_capita  |   | 


</details>

#### Tourism information per country
#### `bulkhours.get_data("tourism")`
- Raw data: [tourism.csv](https://github.com/gtherin/bulkhours/main/data/tourism.csv)  ([raw](https://raw.githubusercontent.com/gtherin/bulkhours/main/data/tourism.csv))

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
- Raw data: [unemployment.csv](https://github.com/gtherin/bulkhours/main/data/unemployment.csv)  ([raw](https://raw.githubusercontent.com/gtherin/bulkhours/main/data/unemployment.csv))

<details>
<summary>Show columns info</summary>

| Column   |      Info |
|-----------|:-----------|
| country |  |
| unemployment_rate |  |

</details>

#### Simple synthetic data for exercice
#### `bulkhours.get_data("wages")`
- Raw data: [wages.tsv](https://github.com/gtherin/bulkhours/main/data/wages.tsv)  ([raw](https://raw.githubusercontent.com/gtherin/bulkhours/main/data/wages.tsv))

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
- Raw data: [Données septembre partie 1.xlsx](https://huggingface.co/datasets/guydegnol/bulkhours/blob/main/Données septembre partie 1.xlsx)  ([raw](https://huggingface.co/datasets/guydegnol/bulkhours/raw/main/Données septembre partie 1.xlsx)🤗)
#### COR data
#### `bulkhours.get_data("COR_2")`
- Raw data: [Données_RA2022_P2.xlsx](https://huggingface.co/datasets/guydegnol/bulkhours/blob/main/Données_RA2022_P2.xlsx)  ([raw](https://huggingface.co/datasets/guydegnol/bulkhours/raw/main/Données_RA2022_P2.xlsx)🤗)
#### COR data
#### `bulkhours.get_data("COR_2bis")`
- Raw data: [Données complémentaires partie 2 RA 2022.xlsx](https://huggingface.co/datasets/guydegnol/bulkhours/blob/main/Données complémentaires partie 2 RA 2022.xlsx)  ([raw](https://huggingface.co/datasets/guydegnol/bulkhours/raw/main/Données complémentaires partie 2 RA 2022.xlsx)🤗)
#### COR data
#### `bulkhours.get_data("COR_3")`
- Raw data: [Données septembre 2022 - partie 3.xlsx](https://huggingface.co/datasets/guydegnol/bulkhours/blob/main/Données septembre 2022 - partie 3.xlsx)  ([raw](https://huggingface.co/datasets/guydegnol/bulkhours/raw/main/Données septembre 2022 - partie 3.xlsx)🤗)
#### COR data
#### `bulkhours.get_data("COR_4")`
- Raw data: [Données_RA2022_P4.xlsx](https://huggingface.co/datasets/guydegnol/bulkhours/blob/main/Données_RA2022_P4.xlsx)  ([raw](https://huggingface.co/datasets/guydegnol/bulkhours/raw/main/Données_RA2022_P4.xlsx)🤗)
#### COR data
#### `bulkhours.get_data("COR_5")`
- Raw data: [Données septembre 2022 - partie 5.xlsx](https://huggingface.co/datasets/guydegnol/bulkhours/blob/main/Données septembre 2022 - partie 5.xlsx)  ([raw](https://huggingface.co/datasets/guydegnol/bulkhours/raw/main/Données septembre 2022 - partie 5.xlsx)🤗)
#### Statement of Apple stock (Quarterly)
#### `bulkhours.get_data("trading.apple")`
- Raw data: [APPLE_DownloadFPrepStatementQuarter.tsv](https://huggingface.co/datasets/guydegnol/bulkhours/blob/main/APPLE_DownloadFPrepStatementQuarter.tsv)  ([raw](https://huggingface.co/datasets/guydegnol/bulkhours/raw/main/APPLE_DownloadFPrepStatementQuarter.tsv)🤗)
- Enrich data: [trading.py](https://github.com/gtherin/bulkhours/main/bulkhours/data/trading.py)  ([raw](https://raw.githubusercontent.com/gtherin/bulkhours/main/bulkhours/data/trading.py))

<details>
<summary>Show columns info</summary>

| Column   |      Info |
|-----------|:-----------|
| revenue |  |
| grossProfit |  |
| ebitda |  |
| netIncome |  |
| eps |  |

</details>


<details>
<summary>Show code</summary>
<code>
def get_apple(self):
    apple = self.read_raw_data(self.raw_data).iloc[-4 * 5 :]

    apple.index = pd.to_datetime(apple.index)
    apple = apple[["date", "revenue", "grossProfit", "ebitda", "netIncome", "eps"]].set_index("date")
    apple["revenue"] = apple["revenue"].astype(float)
    apple.index = pd.date_range("2017-12-30", periods=20, freq="Q")

    return apple
</code>
</details>

#### Cotisants, retraités et rapport démographique tous régimes en 2020
#### `bulkhours.get_data("france.retraites")`
- Enrich data: [france.py](https://github.com/gtherin/bulkhours/main/bulkhours/data/france.py)  ([raw](https://raw.githubusercontent.com/gtherin/bulkhours/main/bulkhours/data/france.py))
- Direct source: https://www.insee.fr/fr/statistiques/2415121#tableau-figure1

<details>
<summary>Show columns info</summary>

| Column   |      Info |
|-----------|:-----------|
| active |  |
| retired |  |
| rapport |  |

</details>


<details>
<summary>Show code</summary>
<code>
def get_retraites(self):
    return (
        pd.read_csv(
            StringIO(
                """
year	active	retired	rapport
2020	28,2	16,9	1,67
2019	28,5	16,7	1,71
2018	28,2	16,5	1,71
2017	27,9	16,3	1,72
2016	27,6	16,1	1,71
2015	27,4	16,0	1,71
2014	27,3	15,8	1,73
2013	27,2	15,6	1,74
2012	27,1	15,3	1,77
2011	27,0	15,3	1,77
2010	26,8	15,1	1,78
2009	26,8	14,7	1,82
""".replace(
                    ",", "."
                )
            ),
            sep="\t",
        )
        .set_index("year")
        .astype(float)
        .sort_index()
    )
</code>
</details>

#### Distribution des salaires mensuels nets en équivalent temps plein (EQTP) en 2020
#### `bulkhours.get_data("france.income")`
- Enrich data: [france.py](https://github.com/gtherin/bulkhours/main/bulkhours/data/france.py)  ([raw](https://raw.githubusercontent.com/gtherin/bulkhours/main/bulkhours/data/france.py))
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


<details>
<summary>Show code</summary>
<code>
def get_income(self):
    data = StringIO(
        """income	population
Moins de 1_200	583943
De 1_200 à 1_300	613_321
De 1_300 à 1_400	835_135
De 1_400 à 1_500	969_172
De 1_500 à 1_600	1_052_630
De 1_600 à 1_700	1_008_034
De 1_700 à 1_800	939_538
De 1_800 à 1_900	863_042
De 1_900 à 2_000	782_314
De 2_000 à 2_100	706_339
De 2_100 à 2_200	630_132
De 2_200 à 2_300	563_387
De 2_300 à 2_400	504_240
De 2_400 à 2_500	452_167
De 2_500 à 2_600	407_908
De 2_600 à 2_700	365_648
De 2_700 à 2_800	329_810
De 2_800 à 2_900	294_230
De 2_900 à 3_000	265_925
De 3_000 à 3_100	241_899
De 3_100 à 3_200	218_832
De 3_200 à 3_300	198_266
De 3_300 à 3_400	180_386
De 3_400 à 3_500	164_164
De 3_500 à 3_600	150_218
De 3_600 à 3_700	136_878
De 3_700 à 3_800	124_602
De 3_800 à 3_900	114_322
De 3_900 à 4_000	106_638
De 4_000 à 4_100	97_332
De 4_100 à 4_200	89_173
De 4_200 à 4_300	82_839
De 4_300 à 4_400	76_130
De 4_400 à 4_500	69_887
De 4_500 à 4_600	64_863
De 4_600 à 4_700	60_466
De 4_700 à 4_800	55_998
De 4_800 à 4_900	52_101
De 4_900 à 5_000	48_438
De 5_000 à 5_100	44_831
De 5_100 à 5_200	41_854
De 5_200 à 5_300	38_848
De 5_300 à 5_400	36_480
De 5_400 à 5_500	34_092
De 5_500 à 5_600	31_841
De 5_600 à 5_700	29_948
De 5_700 à 5_800	27_840
De 5_800 à 5_900	26_335
De 5_900 à 6_000	25_270
De 6_000 à 6_100	23_380
De 6_100 à 6_200	21_912
De 6_200 à 6_300	20_313
De 6_300 à 6_400	19_320
De 6_400 à 6_500	18_286
De 6_500 à 6_600	17_333
De 6_600 à 6_700	16_394
De 6_700 à 6_800	15_519
De 6_800 à 6_900	14_700
De 6_900 à 7_000	13_549
De 7_000 à 7_100	13_210
De 7_100 à 7_200	12_278
De 7_200 à 7_300	11_829
De 7_300 à 7_400	11_186
De 7_400 à 7_500	10_567
De 7_500 à 7_600	10_063
De 7_600 à 7_700	9_698
De 7_700 à 7_800	9_178
De 7_800 à 7_900	8_974
De 7_900 à 8_000	8_689
De 8_000 à 8_100	8_170
De 8_100 à 8_200	7_697
De 8_200 à 8_300	7_431
De 8_300 à 8_400	7_057
De 8_400 à 8_500	6_674
De 8_500 à 8_600	6_410
De 8_600 à 8_700	6_138
De 8_700 à 8_800	5_772
De 8_800 à 8_900	5_585
De 8_900 à 9_000	5_408
Plus de 9_000	183_314
"""
    )

    df = pd.read_csv(data, sep="\t").reset_index()

    df["population"] = df["population"].str.replace(" ", "").astype(float)
    df["xvalue"] = (
        df["income"]
        .str.replace("De ", "")
        .str.replace("Moins de", "1_100 à")
        .str.replace("Plus de 9_000", "9_000 à 9_100")
    )
    df["xvalue"] = df["xvalue"].str.replace(" ", "").str.split("à")
    df["xmin"] = df["xvalue"].apply(lambda x: float(x[0]))
    df["xmax"] = df["xvalue"].apply(lambda x: float(x[1]))
    df["xvalue"] = 0.5 * (df["xmin"] + df["xmax"])
    df["is_valid"] = ~df.index.isin([0, len(df) - 1])

    return df.set_index("xvalue")
</code>
</details>

#### Revenu salarial et salaire en EQTP annuels moyens selon le sexe en 2019
#### `bulkhours.get_data("france.salaires")`
- Enrich data: [france.py](https://github.com/gtherin/bulkhours/main/bulkhours/data/france.py)  ([raw](https://raw.githubusercontent.com/gtherin/bulkhours/main/bulkhours/data/france.py))
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


<details>
<summary>Show code</summary>
<code>
def get_salaires(self):
    data = StringIO(
        """
categorie	revenu_femme	revenu_homme	revenu_diff	salaire_ajusté_femme	salaire_ajusté_homme	salaire_ajusté_diff
Age: Moins de 25 ans	7 360	9 110	19,2	17 930	19 210	6,7
Age: 25-39 ans	18 220	22 610	19,4	24 460	27 660	11,6
Age: 40-49 ans	22 830	29 710	23,1	28 190	34 270	17,7
Age: 50-54 ans	23 070	31 340	26,4	28 280	35 740	20,9
Age: 55 ans ou plus	21 410	29 430	27,2	29 520	38 740	23,8
Diplôme: Pas de diplôme	12 450	17 400	28,5	19 590	23 260	15,8
Diplôme: inférieur au baccalauréat	15 180	20 510	26,0	21 460	25 650	16,3
Diplôme: Baccalauréat à bac+2	20 480	26 560	22,9	25 570	31 000	17,5
Diplôme: Bac+3 ou plus	30 790	44 410	30,7	36 190	50 140	27,8
SocioPro: Cadres	36 040	45 370	20,6	42 820	52 950	19,1
SocioPro: Professions intermédiaires	21 770	26 040	16,4	27 230	30 690	11,3
SocioPro: Employés	13 900	15 310	9,2	20 860	22 850	8,7
SocioPro: Ouvriers	11 960	17 200	30,5	19 580	22 930	14,6
Secteur: privé et entreprises publiques	18 010	24 260	25,7	26 330	31 580	16,6
Secteur: Fonction publique	21 330	25 290	15,7	26 640	31 090	14,3
Secteur: Ensemble	18 970	24 420	22,3	26 430	31 510	16,1
"""
    )
    df = pd.read_csv(data, sep="\t").set_index("categorie")
    for c in df.columns:
        df[c] = df[c].str.replace(" ", "").str.replace(",", ".").astype(float)

    return df
</code>
</details>

#### Inégalités salariales entre femmes et hommes de 1995 à 2019
#### `bulkhours.get_data("france.histsalaires")`
- Enrich data: [france.py](https://github.com/gtherin/bulkhours/main/bulkhours/data/france.py)  ([raw](https://raw.githubusercontent.com/gtherin/bulkhours/main/bulkhours/data/france.py))
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


<details>
<summary>Show code</summary>
<code>
def get_histsalaires(self):
    data = StringIO(
        """
Année	écart relatif du revenu salarial moyen	écart relatif du revenu salarial moyen	écart relatif du salaire moyen en EQTP	écart relatif du salaire moyen en EQTP	écart relatif du volume de travail en EQTP moyen
1995	27,4		18,5		10,9
1996	27,8		18,8		11,1
1997	27,6		18,5		11,2
1998	27,8		18,3		11,4
1999	27,9		17,9		11,9
2000	28,2		18,6		11,6
2001	28,2		18,8		11,3
2002	27,8		18,5		11,3
2003	27,6		18,5		11,1
2004	27,3		18,4		10,9
2005	27,1		18,3		10,8
2006	26,9		18,2		10,6
2007	26,8		18,5		10,2
2008	27,1		18,7		10,3
2009	26,1		18,3		9,6
2010	25,5		18,2		9,0
2011	25,6		18,2		9,2
2012	25,3	25,5	18,2	18,5	8,8
2013		24,8		18,2	8,2
2014		24,1		17,9	7,8
2015		23,7		17,8	7,2
2016		23,3		17,0	7,7
2017		22,9		16,7	7,7
2018		22,8		16,6	7,6
2019		22,3		16,1	7,6
"""
    )
    df = pd.read_csv(data, sep="\t").set_index("Année")
    for c in df.columns:
        df[c] = df[c].str.replace(" ", "").str.replace(",", ".").astype(float)

    return df
</code>
</details>

#### Age de la population au 1er janvier (fin novembre 2022)
#### `bulkhours.get_data("pyramide")`
- Raw data: [pyramide.tsv](https://github.com/gtherin/bulkhours/main/data/pyramide.tsv)  ([raw](https://raw.githubusercontent.com/gtherin/bulkhours/main/data/pyramide.tsv))
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


<details>
<summary>Show code</summary>
<code>
def get_stats(self):
    return pd.read_csv(
        StringIO(
            """Country Mean Minimum Maximum Variance Coefficient of variation
Austria 16.196 7.330 46.400 64.591 0.4962
Belgium 18.741 10.010 42.140 58.243 0.4072
Bulgaria 5.349 2.340 13.050 7.771 0.5212
Czech Republic 8.060 3.700 20.060 14.024 0.4646
Denmark 19.528 11.750 35.650 29.825 0.2797
Estonia 7.552 3.160 17.840 11.965 0.4580
Finland 16.068 8.990 35.360 38.538 0.3863
France 15.106 8.080 40.320 43.449 0.4364
Germany 17.764 7.520 40.000 67.286 0.4618
Hungary 8.055 3.760 19.730 15.993 0.4965
Ireland 19.313 10.180 40.300 58.440 0.3958
Italy 16.040 7.690 42.550 80.968 0.5610
Latvia 6.238 3.160 13.160 5.978 0.3920
Netherlands 16.471 7.230 32.420 34.222 0.3552
Poland 8.821 4.080 22.620 20.516 0.5135
Portugal 11.422 4.150 31.150 54.673 0.6474
Romania 5.903 2.450 15.250 12.481 0.5985
Slovakia 7.703 3.790 18.970 13.479 0.4766
Slovenia 12.708 5.760 33.910 48.510 0.5481
Spain 14.489 7.390 35.940 44.362 0.4597
Sweden 14.651 9.550 28.050 18.079 0.2902
United Kingdom 16.368 7.590 36.390 53.933 0.4487
"""
        ),
        sep=" ",
    ).set_index("Country")
</code>
</details>

#### Mincer equation parameters per country
#### `bulkhours.get_data("mincer.params")`
- Enrich data: [mincer.py](https://github.com/gtherin/bulkhours/main/bulkhours/data/mincer.py)  ([raw](https://raw.githubusercontent.com/gtherin/bulkhours/main/bulkhours/data/mincer.py))
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


<details>
<summary>Show code</summary>
<code>
def get_params(self):
    return pd.read_csv(
        StringIO(
            """Country alpha_0i alpha_1i alpha_2i alpha_3i alpha_0i_e alpha_1i_e alpha_2i_e alpha_3i_e
Austria 0.804517 0.331677 0.426552 -0.03883 0.218682 0.021472 0.113136 0.01396
Belgium 1.297771 0.285186 0.335843 -0.02938 0.142724 0.014014 0.073839 0.009111
Bulgaria 0.322091 0.416255 0.113577 -0.01772 0.228792 0.022465 0.118367 0.014605
Czech_Republic 0.520228 0.346856 0.289626 -0.03328 0.229066 0.022491 0.118508 0.014622
Denmark 1.545782 0.174215 0.437635 -0.04545 0.140934 0.013838 0.072913 0.008997
Estonia 0.737041 0.352713 0.205628 -0.03139 0.238293 0.023397 0.123282 0.015211
Finland 1.352042 0.258832 0.319167 -0.03292 0.177835 0.017461 0.092004 0.011352
France 1.259472 0.292803 0.224716 -0.01589 0.159000 0.015612 0.08226 0.01015
Germany 0.694024 0.339402 0.54815 -0.05546 0.180304 0.017704 0.093281 0.01151
Hungary 0.770683 0.375923 0.068702 -0.0028 0.204335 0.020063 0.105714 0.013044
Ireland 0.992552 0.26368 0.571297 -0.05996 0.171045 0.016794 0.088491 0.010919
Italy 0.652806 0.340295 0.448101 -0.03797 0.227626 0.02235 0.117763 0.014531
Latvia 0.856984 0.320107 0.07136 -0.01262 0.182072 0.017877 0.094196 0.011623
Netherlands 0.851423 0.248588 0.571987 -0.05838 0.136289 0.013382 0.07051 0.0087
Poland 0.395191 0.383528 0.325102 -0.0356 0.227625 0.02235 0.117763 0.01453
Portugal -0.04775 0.46068 0.463982 -0.04216 0.262584 0.025783 0.135849 0.016762
Romania 0.128356 0.453002 0.158483 -0.01838 0.269076 0.02642 0.139208 0.017177
Slovakia 0.628832 0.341852 0.223241 -0.02638 0.238073 0.023376 0.123168 0.015197
Slovenia 0.764813 0.385382 0.233162 -0.01591 0.190327 0.018688 0.098467 0.01215
Spain 1.181748 0.317969 0.161371 -0.0043 0.187973 0.018457 0.097249 0.011999
Sweden 1.471135 0.19044 0.324012 -0.03441 0.14431 0.014169 0.07466 0.009212
United_Kingdom 0.750457 0.34039 0.540786 -0.06146 0.186361 0.018298 0.096415 0.011896"""
        ),
        sep=" ",
    ).set_index("Country")
</code>
</details>

#### Scipy list of available distributions
#### `bulkhours.get_data("scipy_distributions_list")`
- Enrich data: [statsdata.py](https://github.com/gtherin/bulkhours/main/bulkhours/data/statsdata.py)  ([raw](https://raw.githubusercontent.com/gtherin/bulkhours/main/bulkhours/data/statsdata.py))

<details>
<summary>Show code</summary>
<code>
def get_scipy_distributions_list(self):
    import scipy as sp

    return [d for d in dir(sp.stats._continuous_distns) if not d in ["levy_stable", "studentized_range"]]
</code>
</details>

#### Oil production in Saudi Arabia from 1996 to 2007
#### `bulkhours.get_data("statsdata.oil")`
- Enrich data: [statsdata.py](https://github.com/gtherin/bulkhours/main/bulkhours/data/statsdata.py)  ([raw](https://raw.githubusercontent.com/gtherin/bulkhours/main/bulkhours/data/statsdata.py))
- Direct source: https://www.statsmodels.org/stable/index.html

<details>
<summary>Show columns info</summary>

| Column   |      Info |
|-----------|:-----------|
| oil |  |

</details>


<details>
<summary>Show code</summary>
<code>
def get_oil(self):
    return pd.Series(
        [
            446.6565,
            454.4733,
            455.663,
            423.6322,
            456.2713,
            440.5881,
            425.3325,
            485.1494,
            506.0482,
            526.792,
            514.2689,
            494.211,
        ],
        pd.date_range(start="1996", end="2008", freq="A"),
    ).to_frame("oil")
</code>
</details>

#### Air pollution data
#### `bulkhours.get_data("statsdata.air")`
- Enrich data: [statsdata.py](https://github.com/gtherin/bulkhours/main/bulkhours/data/statsdata.py)  ([raw](https://raw.githubusercontent.com/gtherin/bulkhours/main/bulkhours/data/statsdata.py))
- Direct source: https://www.statsmodels.org/stable/index.html

<details>
<summary>Show columns info</summary>

| Column   |      Info |
|-----------|:-----------|
| air |  |

</details>


<details>
<summary>Show code</summary>
<code>
def get_air(self):
    air = pd.Series(
        [
            17.5534,
            21.86,
            23.8866,
            26.9293,
            26.8885,
            28.8314,
            30.0751,
            30.9535,
            30.1857,
            31.5797,
            32.5776,
            33.4774,
            39.0216,
            41.3864,
            41.5966,
        ],
        pd.date_range(start="1990", end="2005", freq="A"),
    )
    return air.to_frame("air")
</code>
</details>

#### Forecasting livestock, sheep in Asia: comparing forecasting performance of non-seasonal methods.
#### `bulkhours.get_data("statsdata.livestock2")`
- Enrich data: [statsdata.py](https://github.com/gtherin/bulkhours/main/bulkhours/data/statsdata.py)  ([raw](https://raw.githubusercontent.com/gtherin/bulkhours/main/bulkhours/data/statsdata.py))
- Direct source: https://www.statsmodels.org/stable/index.html

<details>
<summary>Show columns info</summary>

| Column   |      Info |
|-----------|:-----------|
| livestock2 |  |

</details>


<details>
<summary>Show code</summary>
<code>
def get_livestock2(self):
    index = pd.date_range(start="1970", end="2001", freq="A")
    return pd.Series(
        [
            263.9177,
            268.3072,
            260.6626,
            266.6394,
            277.5158,
            283.834,
            290.309,
            292.4742,
            300.8307,
            309.2867,
            318.3311,
            329.3724,
            338.884,
            339.2441,
            328.6006,
            314.2554,
            314.4597,
            321.4138,
            329.7893,
            346.3852,
            352.2979,
            348.3705,
            417.5629,
            417.1236,
            417.7495,
            412.2339,
            411.9468,
            394.6971,
            401.4993,
            408.2705,
            414.2428,
        ],
        index,
    ).to_frame("livestock2")
</code>
</details>

#### Forecasting livestock, sheep in Asia: comparing forecasting performance of non-seasonal methods. (3)
#### `bulkhours.get_data("statsdata.livestock3")`
- Enrich data: [statsdata.py](https://github.com/gtherin/bulkhours/main/bulkhours/data/statsdata.py)  ([raw](https://raw.githubusercontent.com/gtherin/bulkhours/main/bulkhours/data/statsdata.py))
- Direct source: https://www.statsmodels.org/stable/index.html

<details>
<summary>Show columns info</summary>

| Column   |      Info |
|-----------|:-----------|
| livestock3 |  |

</details>


<details>
<summary>Show code</summary>
<code>
def get_livestock3(self):
    data = [407.9979, 403.4608, 413.8249, 428.105, 445.3387, 452.9942, 455.7402]
    return pd.Series(data, pd.date_range(start="2001", end="2008", freq="A")).to_frame("livestock3")
</code>
</details>

#### International visitor night in Australia (millions) < 2005
#### `bulkhours.get_data("statsdata.aust")`
- Enrich data: [statsdata.py](https://github.com/gtherin/bulkhours/main/bulkhours/data/statsdata.py)  ([raw](https://raw.githubusercontent.com/gtherin/bulkhours/main/bulkhours/data/statsdata.py))

<details>
<summary>Show columns info</summary>

| Column   |      Info |
|-----------|:-----------|
| aust |  |

</details>


<details>
<summary>Show code</summary>
<code>
def get_aust(self):
    data = [
        41.7275,
        24.0418,
        32.3281,
        37.3287,
        46.2132,
        29.3463,
        36.4829,
        42.9777,
        48.9015,
        31.1802,
        37.7179,
        40.4202,
        51.2069,
        31.8872,
        40.9783,
        43.7725,
        55.5586,
        33.8509,
        42.0764,
        45.6423,
        59.7668,
        35.1919,
        44.3197,
        47.9137,
    ]
    return pd.Series(data, pd.date_range(start="2005", end="2010-Q4", freq="QS-OCT")).to_frame("aust")
</code>
</details>

#### International visitor night in Australia (millions) > 2005
#### `bulkhours.get_data("air_passengers")`
- Raw data: [AirPassengers.csv](https://huggingface.co/datasets/guydegnol/bulkhours/blob/main/AirPassengers.csv)  ([raw](https://huggingface.co/datasets/guydegnol/bulkhours/raw/main/AirPassengers.csv)🤗)
- Enrich data: [statsdata.py](https://github.com/gtherin/bulkhours/main/bulkhours/data/statsdata.py)  ([raw](https://raw.githubusercontent.com/gtherin/bulkhours/main/bulkhours/data/statsdata.py))

<details>
<summary>Show columns info</summary>

| Column   |      Info |
|-----------|:-----------|
| #Passengers |  |
| is_test |  |

</details>


<details>
<summary>Show code</summary>
<code>
def get_air_passengers(self):
    df = self.read_raw_data(self.raw_data).set_index("Month")

    df.index = pd.to_datetime(df.index)
    df.index.freq = "MS"
    df["is_test"] = df.index >= df.index[120]

    return df
</code>
</details>

#### All-Transactions House Price Index for Houston
#### `bulkhours.get_data("statsdata.hhousing")`
- Enrich data: [statsdata.py](https://github.com/gtherin/bulkhours/main/bulkhours/data/statsdata.py)  ([raw](https://raw.githubusercontent.com/gtherin/bulkhours/main/bulkhours/data/statsdata.py))
- Direct source: https://fred.stlouisfed.org/series/ATNHPIUS26420Q

<details>
<summary>Show code</summary>
<code>
def get_hhousing(self):
    from pandas_datareader import data as pdr  # To get data

    data = pdr.get_data_fred("HOUSTNSA", "1959-01-01")  # , "2019-06-01")
    housing = data.HOUSTNSA.pct_change().dropna()
    # Scale by 100 to get percentages
    housing = 100 * housing.asfreq("MS")
    return housing.to_frame()
</code>
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


<details>
<summary>Show code</summary>
<code>
def get_dfistor_count(self):
    columns = ["processor", "count", "date", "designer", "manufacturer", "engraving_scale", "area", "density", "ref"]
    df = flops.get_table_from_wiki(wpage="Transistor_count", in_table="Voodoo Graphics", columns=columns)
    return df.iloc[:-1]
</code>
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


<details>
<summary>Show code</summary>
<code>
def get_engraving_scale(self):
    return flops.get_engraving_scale(verbose=True)
</code>
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


<details>
<summary>Show code</summary>
<code>
def get_FLOPS(self):
    return flops.get_table_from_wiki("FLOPS", "Computer performance")
</code>
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


<details>
<summary>Show code</summary>
<code>
def get_gpus(self):
    return flops.get_table_from_wiki("FLOPS", "NVIDIA", columns=["date", "un_costs", "costs", "platform", "comments"])
</code>
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


<details>
<summary>Show code</summary>
<code>
def get_cpus(self):
    columns = ["processor", "count", "date", "designer", "engraving_scale", "area", "density"]
    df = flops.get_table_from_wiki(
        wpage="Transistor_count", in_table="20-bit, 6-chip, 28 chips total", columns=columns
    )
    df = df.iloc[:-1]
    df["date"] = df["date"].str.replace("March ", "").str.replace("November ", "")
    df["date"] = df["date"].str.replace("March ", "").str.replace("November ", "")
    df["date"] = df["date"].str.split("[").str[0].astype(int)

    df["count"] = df["count"].str.replace(",", "")
    df["count"] = df["count"].str.split("[").str[0]
    df["count"] = df["count"].str.split("+").str[0]
    df["count"] = df["count"].str.split(" ").str[0]
    df["count"] = pd.to_numeric(df["count"], errors="coerce")

    df["engraving_scale"] = df["engraving_scale"].str.split("[").str[0]
    df["engraving_scale"] = df["engraving_scale"].str.replace(",", "")
    df["engraving_scale"] = df["engraving_scale"].str.split("(").str[0]
    df["engraving_scale"] = df["engraving_scale"].str.replace("\xa0nm", "")
    df["engraving_scale"] = df["engraving_scale"].str.replace("nm", "")
    df["engraving_scale"] = pd.to_numeric(df["engraving_scale"], errors="coerce")

    l = [3, 4, 6, 8, 15, 23, 50, 80, 150, 300, 500, 800, 1000, 3000, 5000, 10000]
    df["engraving_scale2"] = pd.cut(df["engraving_scale"], bins=l, include_lowest=True)
    df["engraving_scale3"] = df["engraving_scale2"].map(
        dict(zip(df["engraving_scale2"].unique(), range(len(df["engraving_scale2"].unique()))))
    )
    df["engraving_scale3"] = df["engraving_scale3"].fillna(1).astype(float)

    return df
</code>
</details>

#### Costs of FLOPS
#### `bulkhours.get_data("hpc.FLOPS_costs")`
- Reference site: https://en.wikipedia.org/wiki/FLOPS

<details>
<summary>Show columns info</summary>

| Column   |      Info |
|-----------|:-----------|
| ('Date', 'Date') |  |
| ('Approximate USD per GFLOPS', 'Unadjusted') |  |
| ('Approximate USD per GFLOPS', '2022[69]') |  |
| ('Platform providing the lowest cost per GFLOPS', 'Platform providing the lowest cost per GFLOPS') |  |
| ('Comments', 'Comments') |  |

</details>


<details>
<summary>Show code</summary>
<code>
def get_costs(self):
    return flops.get_table_from_wiki("FLOPS", "Approximate USD per GFLOPS")#, columns=["date", "un_costs", "costs", "platform", "comments"])
</code>
</details>

#### Energy Efficiency (GFlops/watts)
#### `bulkhours.get_data("hpc.green500")`
- Raw data: [green500_top_202306.xlsx](https://huggingface.co/datasets/guydegnol/bulkhours/blob/main/green500_top_202306.xlsx)  ([raw](https://huggingface.co/datasets/guydegnol/bulkhours/raw/main/green500_top_202306.xlsx)🤗)
- Reference site: https://www.top500.org/lists/green500/2023/06/

<details>
<summary>Show columns info</summary>

| Column   |      Info |
|-----------|:-----------|
| Rank |  |
| TOP500 Rank |  |
| Name |  |
| Computer |  |
| Site |  |
| Manufacturer |  |
| Country |  |
| Year |  |
| Segment |  |
| Total Cores |  |
| Accelerator/Co-Processor Cores |  |
| Rmax [TFlop/s] |  |
| Rpeak [TFlop/s] |  |
| Power (kW) |  |
| Power Source |  |
| Energy Efficiency [GFlops/Watts] |  |
| Power Source.1 |  |
| Power Quality Level |  |
| Optimized Run (HPL) |  |
| Optimized Run (Peak Power) |  |
| Memory |  |
| Architecture |  |
| Processor |  |
| Processor Technology |  |
| Processor Speed (MHz) |  |
| Operating System |  |
| OS Family |  |
| Accelerator/Co-Processor |  |
| Cores per Socket |  |
| Processor Generation |  |
| System Model |  |
| System Family |  |
| Interconnect Family |  |
| Interconnect |  |
| Continent |  |
| Site ID |  |
| System ID |  |

</details>

#### Energy Efficiency (GFlops/watts)
#### `bulkhours.get_data("hpc.top500")`
- Raw data: [TOP500_202306.xlsx](https://huggingface.co/datasets/guydegnol/bulkhours/blob/main/TOP500_202306.xlsx)  ([raw](https://huggingface.co/datasets/guydegnol/bulkhours/raw/main/TOP500_202306.xlsx)🤗)
- Reference site: https://www.top500.org/lists/top500/2023/06/

<details>
<summary>Show columns info</summary>

| Column   |      Info |
|-----------|:-----------|
| Rank |  |
| Previous Rank |  |
| First Appearance |  |
| First Rank |  |
| Name |  |
| Computer |  |
| Site |  |
| Manufacturer |  |
| Country |  |
| Year |  |
| Segment |  |
| Total Cores |  |
| Accelerator/Co-Processor Cores |  |
| Rmax [TFlop/s] |  |
| Rpeak [TFlop/s] |  |
| Nmax |  |
| Nhalf |  |
| HPCG [TFlop/s] |  |
| Power (kW) |  |
| Power Source |  |
| Energy Efficiency [GFlops/Watts] |  |
| Memory |  |
| Architecture |  |
| Processor |  |
| Processor Technology |  |
| Processor Speed (MHz) |  |
| Operating System |  |
| OS Family |  |
| Accelerator/Co-Processor |  |
| Cores per Socket |  |
| Processor Generation |  |
| System Model |  |
| System Family |  |
| Interconnect Family |  |
| Interconnect |  |
| Continent |  |
| Site ID |  |
| System ID |  |

</details>

#### Computational capacity of the fastest supercomputers
#### `bulkhours.get_data("supercomputers")`
- Raw data: [Supercomputer%20power%20(FLOPS)%20%E2%80%93%20TOP500%20Database.csv](https://github.com/owid/owid-datasets/dd7a4ecbb249f98028e25c304ef7d68de8979ea9/datasets/Supercomputer%20power%20(FLOPS)%20%E2%80%93%20TOP500%20Database/Supercomputer%20power%20(FLOPS)%20%E2%80%93%20TOP500%20Database.csv)  ([raw](https://raw.githubusercontent.com/owid/owid-datasets/dd7a4ecbb249f98028e25c304ef7d68de8979ea9/datasets/Supercomputer%20power%20(FLOPS)%20%E2%80%93%20TOP500%20Database/Supercomputer%20power%20(FLOPS)%20%E2%80%93%20TOP500%20Database.csv))
- Direct source: https://ourworldindata.org/grapher/supercomputer-power-flops

<details>
<summary>Show columns info</summary>
> <a href="The number of floating-point operations per second (GigaFLOPS) by the fastest supercomputer in any given year">The number of floating-point operations per second (GigaFLOPS) by the fastest supercomputer in any given year</a>

| Column   |      Info |
|-----------|:-----------|
| Entity   | The number of GigaFLOP/S by the fastest supercomputer in any given year |         


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
#### `bulkhours.get_data("sunspots")`
- Raw data: [observed-solar-cycle-indices.json](https://services.swpc.noaa.gov/json/solar-cycle/observed-solar-cycle-indices.json)  ([raw](https://services.swpc.noaa.gov/json/solar-cycle/observed-solar-cycle-indices.json)🔄)
- Enrich data: [statsdata.py](https://github.com/gtherin/bulkhours/main/bulkhours/data/statsdata.py)  ([raw](https://raw.githubusercontent.com/gtherin/bulkhours/main/bulkhours/data/statsdata.py))
- Direct source: https://www.swpc.noaa.gov/products/solar-cycle-progression
- Reference site: https://services.swpc.noaa.gov/json/solar-cycle/observed-solar-cycle-indices.json

<details>
<summary>Show columns info</summary>

| Column   |      Info |
|-----------|:-----------|
| ssn | SunSpot Number (aka Wolf Number or Zürich number): number of sunspots and groups of sunspots present on the surface of the Sun (source: S.I.D.C. Brussels International Sunspot Number) |
| smoothed_ssn | smoothed ssn (source: S.I.D.C. Brussels International Sunspot Number) |
| observed_swpc_ssn | mean monthly SWPC/SWO ssn (source: SWPC Space Weather Operations) |
| smoothed_swpc_ssn | smoothed ssn (source: SWPC Space Weather Operations) |
| f10.7 | mean monthly  flux values (sfu) (source: Penticton, B.C. 10.7cm radio) |
| smoothed_f10.7 | smoothed radio flux values (source: Penticton, B.C. 10.7cm radio) |

</details>


<details>
<summary>Show code</summary>
<code>
def get_sunspots(self):
    dta = pd.read_json(self.raw_data)
    sunspots = dta.set_index("time-tag")
    sunspots.index = pd.to_datetime(sunspots.index)
    sunspots.index.freq = sunspots.index.inferred_freq

    sunspots = sunspots.resample("MS").mean()
    sunspots = sunspots.resample("Q").mean().iloc[-400:]

    return sunspots
</code>
</details>



## Health 

#### Coronavirus Pandemic (COVID-19) data
#### `bulkhours.get_data("vaccinations")`
- Raw data: [vaccinations.csv](https://github.com/owid/covid-19-data/master/public/data/vaccinations/vaccinations.csv)  ([raw](https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/vaccinations/vaccinations.csv))
- Direct source: https://ourworldindata.org/coronavirus
- Reference site: https://covid19.who.int/data

<details>
<summary>Show columns info</summary>
> <a href="https://github.com/owid/covid-19-data/tree/master/public/data/">https://github.com/owid/covid-19-data/tree/master/public/data/</a>

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
- Raw data: [prostate.tsv](https://github.com/gtherin/bulkhours/main/data/prostate.tsv)  ([raw](https://raw.githubusercontent.com/gtherin/bulkhours/main/data/prostate.tsv))
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
- Raw data: [owid-covid-data.csv](https://covid.ourworldindata.org/data/owid-covid-data.csv)  ([raw](https://covid.ourworldindata.org/data/owid-covid-data.csv)🔄)
- Direct source: https://ourworldindata.org/coronavirus
- Reference site: https://covid19.who.int/data

<details>
<summary>Show columns info</summary>
> <a href="https://github.com/owid/covid-19-data/tree/master/public/data/">https://github.com/owid/covid-19-data/tree/master/public/data/</a>

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

#### Data on CO2 and Greenhouse Gas Emissions by Our World in Data
#### `bulkhours.get_data("co2.main")`
- Raw data: [owid-co2-data.csv](https://github.com/owid/co2-data/master/owid-co2-data.csv)  ([raw](https://raw.githubusercontent.com/owid/co2-data/master/owid-co2-data.csv))
- Enrich data: [world.py](https://github.com/gtherin/bulkhours/main/bulkhours/data/world.py)  ([raw](https://raw.githubusercontent.com/gtherin/bulkhours/main/bulkhours/data/world.py))

<details>
<summary>Show columns info</summary>
> <a href="https://github.com/owid/co2-data/blob/master/owid-co2-codebook.csv">https://github.com/owid/co2-data/blob/master/owid-co2-codebook.csv</a>

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
- Enrich data: [world.py](https://github.com/gtherin/bulkhours/main/bulkhours/data/world.py)  ([raw](https://raw.githubusercontent.com/gtherin/bulkhours/main/bulkhours/data/world.py))

<details>
<summary>Show columns info</summary>
> <a href="https://github.com/owid/co2-data/blob/master/owid-co2-codebook.csv">https://github.com/owid/co2-data/blob/master/owid-co2-codebook.csv</a>

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
- Raw data: [carbon-footprint-travel-mode.csv](https://huggingface.co/datasets/guydegnol/bulkhours/blob/main/carbon-footprint-travel-mode.csv)  ([raw](https://huggingface.co/datasets/guydegnol/bulkhours/raw/main/carbon-footprint-travel-mode.csv)🤗)
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

#### Greenhouse effect gaz concentrations
#### `bulkhours.get_data("co2.concentrations")`
- Raw data: [climate-change.csv](https://github.com/gtherin/bulkhours/main/data/climate-change.csv)  ([raw](https://raw.githubusercontent.com/gtherin/bulkhours/main/data/climate-change.csv))
- Enrich data: [world.py](https://github.com/gtherin/bulkhours/main/bulkhours/data/world.py)  ([raw](https://raw.githubusercontent.com/gtherin/bulkhours/main/bulkhours/data/world.py))
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


<details>
<summary>Show code</summary>
<code>
def get_concentrations(self, zone="World", **data_info):
    df = self.read_raw_data(self.raw_data)

    df = df.rename(columns={"Entity": "country", "Year": "year"})

    if zone is not None:
        df = df.query(f"country == '{zone}'")
    return df
</code>
</details>

#### Greenhouse effect gaz concentrations
#### `bulkhours.get_data("co2.mapconcentrations")`
- Raw data: [climate-change.csv](https://github.com/gtherin/bulkhours/main/data/climate-change.csv)  ([raw](https://raw.githubusercontent.com/gtherin/bulkhours/main/data/climate-change.csv))
- Enrich data: [world.py](https://github.com/gtherin/bulkhours/main/bulkhours/data/world.py)  ([raw](https://raw.githubusercontent.com/gtherin/bulkhours/main/bulkhours/data/world.py))
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


<details>
<summary>Show code</summary>
<code>
def get_mapconcentrations(self, **kwargs):
    return get_mapgeneric(get_concentrations(self, **kwargs))
</code>
</details>

#### Les incidences économique de l'action pour le climat
#### `bulkhours.get_data("climate.pisaniferry")`
- Raw data: [2023-incidences-economiques-transition-climat-rapport-de-synthese_0.pdf](https://www.strategie.gouv.fr/sites/strategie.gouv.fr/files/atoms/files/2023-incidences-economiques-transition-climat-rapport-de-synthese_0.pdf)  ([raw](https://www.strategie.gouv.fr/sites/strategie.gouv.fr/files/atoms/files/2023-incidences-economiques-transition-climat-rapport-de-synthese_0.pdf)🔄)
#### La contribution des émissions importées à l'empreinte carbone de la France
#### `bulkhours.get_data("climate.francecarbone")`
- Raw data: [Rapport-OFCE-HCC-2020.pdf](https://www.ofce.sciences-po.fr/pdf-articles/actu/Rapport-OFCE-HCC-2020.pdf)  ([raw](https://www.ofce.sciences-po.fr/pdf-articles/actu/Rapport-OFCE-HCC-2020.pdf)🔄)


## Machine_learning 

#### Cat or not training data: keys=[train_set_x, train_set_y]
#### `bulkhours.get_data("train_catvnoncat")`
- Raw data: [train_catvnoncat.h5](https://huggingface.co/datasets/guydegnol/bulkhours/blob/main/train_catvnoncat.h5)  ([raw](https://huggingface.co/datasets/guydegnol/bulkhours/resolve/main/train_catvnoncat.h5)🤗)
#### Cat or not test data: keys=[test_set_x, test_set_y, list_classes]
#### `bulkhours.get_data("test_catvnoncat")`
- Raw data: [test_catvnoncat.h5](https://huggingface.co/datasets/guydegnol/bulkhours/blob/main/test_catvnoncat.h5)  ([raw](https://huggingface.co/datasets/guydegnol/bulkhours/resolve/main/test_catvnoncat.h5)🤗)
