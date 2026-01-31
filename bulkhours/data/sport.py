from io import StringIO
import pandas as pd

from .data_parser import DataParser


@DataParser.register_dataset(
    label="sport.stravism2",
    summary="Activities",
    category="Sport",
    enrich_data="https://github.com/gtherin/bulkhours/blob/main/bulkhours/data/sport.py",
)
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


@DataParser.register_dataset(
    label="sport.income2",
    summary="Distribution des salaires mensuels nets en équivalent temps plein (EQTP) en 2020",
    category="Economics",
    source="""- Note : certains salaires en EQTP sont inférieurs au Smic ; ceci est en effet permis par certains statuts.
de contrats de professionnalisation ; hors apprentis, stagiaires, salariés agricoles et salariés des particuliers employeurs.""",
    enrich_data="https://github.com/gtherin/bulkhours/blob/main/bulkhours/data/france.py",
    ref_source="https://www.insee.fr/fr/statistiques/6436313#tableau-figure2",
)
def get_income(self):
    data = StringIO(
        """income	population
Moins de 1_200	583943
De 1_200 à 1_300	613_321
De 1_300 à 1_400	835_135
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


DataParser.register_dataset(
    label="pyramide2",
    summary="Age de la population au 1er janvier (fin novembre 2022)",
    category="Sport",
    raw_data="pyramide.tsv",
    source="""la France compte 805 914 personnes de 65 ans dont 425 143 femmes et 380 771 hommes""",
    ref_source="https://www.insee.fr/fr/statistiques/2381472#tableau-figure1",
)

DataParser.register_dataset(
    label="sport.stravism",
    summary="Activities",
    category="Sport",
    raw_data="stravism.csv.enc",
)
