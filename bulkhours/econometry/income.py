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
Moins de 1 200	583943
De 1 200 à 1 300	613321
De 1 300 à 1 400	835135
De 1 400 à 1 500	969172
De 1 500 à 1 600	1_052_630
De 1 600 à 1 700	1_008_034
De 1 700 à 1 800	939 538
De 1 800 à 1 900	863 042
De 1 900 à 2 000	782 314
De 2 000 à 2 100	706 339
De 2 100 à 2 200	630 132
De 2 200 à 2 300	563 387
De 2 300 à 2 400	504 240
De 2 400 à 2 500	452 167
De 2 500 à 2 600	407 908
De 2 600 à 2 700	365 648
De 2 700 à 2 800	329 810
De 2 800 à 2 900	294 230
De 2 900 à 3 000	265 925
De 3 000 à 3 100	241 899
De 3 100 à 3 200	218 832
De 3 200 à 3 300	198 266
De 3 300 à 3 400	180 386
De 3 400 à 3 500	164 164
De 3 500 à 3 600	150 218
De 3 600 à 3 700	136 878
De 3 700 à 3 800	124 602
De 3 800 à 3 900	114 322
De 3 900 à 4 000	106 638
De 4 000 à 4 100	97 332
De 4 100 à 4 200	89 173
De 4 200 à 4 300	82 839
De 4 300 à 4 400	76 130
De 4 400 à 4 500	69 887
De 4 500 à 4 600	64 863
De 4 600 à 4 700	60 466
De 4 700 à 4 800	55 998
De 4 800 à 4 900	52 101
De 4 900 à 5 000	48 438
De 5 000 à 5 100	44 831
De 5 100 à 5 200	41 854
De 5 200 à 5 300	38 848
De 5 300 à 5 400	36 480
De 5 400 à 5 500	34 092
De 5 500 à 5 600	31 841
De 5 600 à 5 700	29 948
De 5 700 à 5 800	27 840
De 5 800 à 5 900	26 335
De 5 900 à 6 000	25 270
De 6 000 à 6 100	23 380
De 6 100 à 6 200	21 912
De 6 200 à 6 300	20 313
De 6 300 à 6 400	19 320
De 6 400 à 6 500	18 286
De 6 500 à 6 600	17 333
De 6 600 à 6 700	16 394
De 6 700 à 6 800	15 519
De 6 800 à 6 900	14 700
De 6 900 à 7 000	13 549
De 7 000 à 7 100	13 210
De 7 100 à 7 200	12 278
De 7 200 à 7 300	11 829
De 7 300 à 7 400	11 186
De 7 400 à 7 500	10 567
De 7 500 à 7 600	10 063
De 7 600 à 7 700	9 698
De 7 700 à 7 800	9 178
De 7 800 à 7 900	8 974
De 7 900 à 8 000	8 689
De 8 000 à 8 100	8 170
De 8 100 à 8 200	7 697
De 8 200 à 8 300	7 431
De 8 300 à 8 400	7 057
De 8 400 à 8 500	6 674
De 8 500 à 8 600	6 410
De 8 600 à 8 700	6 138
De 8 700 à  8800	5 772
De 8 800 à 8 900	5 585
De 8 900 à 9 000	5 408
Plus de 9 000	183 314
"""
    )

    df = pd.read_csv(data, sep="\t").reset_index()

    df["eqt"] = df["eqt"].str.replace(" ", "").astype(float)
    df["xvalue"] = (
        df["Income"]
        .str.replace("De ", "")
        .str.replace("Moins de", "1100 à")
        .str.replace("Plus de 9 000", "9000 à 9100")
    )
    df["xvalue"] = df["xvalue"].str.replace(" ", "").str.split("à")
    df["xvalue"] = df["xvalue"].apply(lambda x: (int(x[0]) + int(x[1])) / 2)
    df["is_valid"] = df.index.isin([0, len(df) - 1])

    return df.set_index("xvalue")
