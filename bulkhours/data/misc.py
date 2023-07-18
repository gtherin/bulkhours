from .data_parser import DataParser


DataParser.register_dataset(
    label="prices-split-adjusted",
    summary="Market prices of SP500 stocks",
    category="Economics",
    ref_source="""https://github.com/kyi3081/stock-analysis""",
    raw_data="https://raw.githubusercontent.com/kyi3081/stock-analysis/master/prices-split-adjusted.csv",
    func=None,
)

DataParser.register_dataset(
    label="fundamentals",
    summary="Market fundamentals of SP500 stocks",
    category="Economics",
    ref_source="""https://github.com/kyi3081/stock-analysis""",
    raw_data="https://raw.githubusercontent.com/kyi3081/stock-analysis/master/fundamentals.csv",
    func=None,
)

DataParser.register_dataset(
    label="securities",
    summary="Stocks information for SP500",
    category="Economics",
    ref_source="""https://github.com/kyi3081/stock-analysis""",
    raw_data="https://raw.githubusercontent.com/kyi3081/stock-analysis/master/securities.csv",
)


DataParser.register_dataset(
    label="continent",
    summary="Standardized country information (iso m49)",
    category="Economics",
    raw_data="continent.tsv",
)

DataParser.register_dataset(
    label="corruption", summary="Corruption index per country", category="Economics", raw_data="corruption.csv"
)

DataParser.register_dataset(
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
    func=None,
)

DataParser.register_dataset(
    label="richest_countries",
    summary="GDP per capita per country",
    category="Economics",
    raw_data="richest_countries.csv",
    columns_description="""| Column   |      Info |
|-----------|:-----------|
| country   |   |         
| gdp_per_capita  |   | 
""",
)


DataParser.register_dataset(
    label="tourism", summary="Tourism information per country", category="Economics", raw_data="tourism.csv"
)

DataParser.register_dataset(
    label="unemployment", summary="Unemployemnt rates per country", category="Economics", raw_data="unemployment.csv"
)
DataParser.register_dataset(
    label="wages", summary="Simple synthetic data for exercice", category="Economics", raw_data="wages.tsv"
)
DataParser.register_dataset(
    label="COR_1",
    summary="COR data",
    category="Economics",
    raw_data="https://huggingface.co/datasets/guydegnol/bulkhours/raw/main/Données septembre partie 1.xlsx",
)


DataParser.register_dataset(
    label="COR_2",
    reference="COR_1",
    raw_data="https://huggingface.co/datasets/guydegnol/bulkhours/raw/main/Données_RA2022_P2.xlsx",
)
DataParser.register_dataset(
    label="COR_2bis",
    reference="COR_1",
    raw_data="https://huggingface.co/datasets/guydegnol/bulkhours/raw/main/Données complémentaires partie 2 RA 2022.xlsx",
)
DataParser.register_dataset(
    label="COR_3",
    reference="COR_1",
    raw_data="https://huggingface.co/datasets/guydegnol/bulkhours/raw/main/Données septembre 2022 - partie 3.xlsx",
)
DataParser.register_dataset(
    label="COR_4",
    reference="COR_1",
    raw_data="https://huggingface.co/datasets/guydegnol/bulkhours/raw/main/Données_RA2022_P4.xlsx",
)
DataParser.register_dataset(
    label="COR_5",
    reference="COR_1",
    raw_data="https://huggingface.co/datasets/guydegnol/bulkhours/raw/main/Données septembre 2022 - partie 5.xlsx",
)
DataParser.register_dataset(
    label="supercomputers",
    summary="Computational capacity of the fastest supercomputers",
    category="Computing",
    raw_data="https://raw.githubusercontent.com/owid/owid-datasets/dd7a4ecbb249f98028e25c304ef7d68de8979ea9/datasets/Supercomputer%20power%20(FLOPS)%20%E2%80%93%20TOP500%20Database/Supercomputer%20power%20(FLOPS)%20%E2%80%93%20TOP500%20Database.csv",
    ref_source="""https://ourworldindata.org/grapher/supercomputer-power-flops""",
    columns_info="The number of floating-point operations per second (GigaFLOPS) by the fastest supercomputer in any given year",
    columns_description="""| Column   |      Info |
|-----------|:-----------|
| Entity   | The number of GigaFLOP/S by the fastest supercomputer in any given year |         
""",
)

DataParser.register_dataset(
    label="vaccinations",
    summary="Coronavirus Pandemic (COVID-19) data",
    category="Health",
    raw_data="https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/vaccinations/vaccinations.csv",
    ref_site="""https://covid19.who.int/data""",
    ref_source="""https://ourworldindata.org/coronavirus""",
    columns_info="https://github.com/owid/covid-19-data/tree/master/public/data/",
)
DataParser.register_dataset(
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
)
DataParser.register_dataset(
    label="covid",
    summary="Coronavirus Pandemic (COVID-19) data",
    category="Health",
    raw_data="https://covid.ourworldindata.org/data/owid-covid-data.csv",
    ref_site="""https://covid19.who.int/data""",
    ref_source="https://ourworldindata.org/coronavirus",
    columns_info="https://github.com/owid/covid-19-data/tree/master/public/data/",
)
DataParser.register_dataset(
    label="train_catvnoncat",
    summary="Cat or not training data: keys=[train_set_x, train_set_y]",
    category="Machine_learning",
    raw_data="https://huggingface.co/datasets/guydegnol/bulkhours/resolve/main/train_catvnoncat.h5",
)
DataParser.register_dataset(
    label="test_catvnoncat",
    summary="Cat or not test data: keys=[test_set_x, test_set_y, list_classes]",
    category="Machine_learning",
    raw_data="https://huggingface.co/datasets/guydegnol/bulkhours/resolve/main/test_catvnoncat.h5",
)


DataParser.register_dataset(
    label="maintenance1",
    summary="Synthetic data for machine failure data (1)",
    category="Predictive_Maintenance",
    raw_data="https://raw.githubusercontent.com/shadgriffin/feature_engineering_equipment_failure/main/fe_equipment_failure_data_1.csv",
)
DataParser.register_dataset(
    label="maintenance2",
    summary="Synthetic data for machine failure data (2)",
    category="Predictive_Maintenance",
    raw_data="https://raw.githubusercontent.com/shadgriffin/feature_engineering_equipment_failure/main/fe_equipment_failure_data_2.csv",
)
DataParser.register_dataset(
    label="maintenance3",
    summary="Synthetic data for machine failure data (3)",
    category="Predictive_Maintenance",
    raw_data="https://raw.githubusercontent.com/shadgriffin/machine_failure/master/equipment_failure_data_1.csv",
)
DataParser.register_dataset(
    label="maintenance4",
    summary="Synthetic data for machine failure data (4)",
    category="Predictive_Maintenance",
    raw_data="https://raw.githubusercontent.com/shadgriffin/machine_failure/master/equipment_failure_data_2.csv",
)

for f in (
    ["chose1.jpg", "chose2.jpg", "radian2.png", "README.md", "gradient_descent.png", "TCL.png"]
    + ["lognormal.png", "in_trading.csv", "ffcontrol.csv", "galton.jpg", "galtonr.png"]
    + ["exercices", "freefight.csv", "cache"]
):
    DataParser.register_dataset(label=f, raw_data=f, category="Internal")
