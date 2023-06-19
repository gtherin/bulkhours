from io import StringIO
import pandas as pd

from . import tools


@tools.register("france.retraites")
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


@tools.register("france.income")
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


# OECD (2023), Adult education level (indicator). doi: 10.1787/36bce3fe-en (Accessed on 24 January 2023)


@tools.register("france.salaires")
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


@tools.register("france.histsalaires")
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
