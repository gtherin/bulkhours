import pandas as pd
import bulkhours


def test_languages():
    df = bulkhours.hpc.get_languages_perf()
    print(df)
