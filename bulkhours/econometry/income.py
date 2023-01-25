from io import StringIO
import numpy as np
import pandas as pd


def get_fr_income(credit=True):
    """
        Source https://www.insee.fr/fr/statistiques/6436313#tableau-figure2

        Distribution des salaires mensuels nets en équivalent temps plein (EQTP) en 2020

    Note : certains salaires en EQTP sont inférieurs au Smic ; ceci est en effet permis par certains statuts. Cependant, l'existence de rémunérations inférieures au Smic peut aussi provenir d’incohérences entre salaires et durées travaillées dans les déclarations administratives, qui ne peuvent être toutes redressées.
    Lecture : en 2020, en EQTP, 50 % des salariés gagnent plus de 2 005 euros.
    Champ : France hors Mayotte, salariés du privé et des entreprises publiques, y compris bénéficiaires de contrats aidés et de contrats de professionnalisation ; hors apprentis, stagiaires, salariés agricoles et salariés des particuliers employeurs.

    """
    if credit:
        print("Data source INSEE: salaires mensuels nets en équivalent temps plein (EQTP) en 2020")
    data = StringIO(
        """Income	eqt
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

    df["eqt"] = df["eqt"].str.replace(" ", "").astype(float)
    df["xvalue"] = (
        df["Income"]
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


#OECD (2023), Adult education level (indicator). doi: 10.1787/36bce3fe-en (Accessed on 24 January 2023)