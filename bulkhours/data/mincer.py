from io import StringIO
import pandas as pd

from .data_parser import DataParser


@DataParser.register_dataset(
    label="mincer.stats",
    summary="Descriptive statistics of hourly wages in selected EU countries in 2010 (in PPS)",
    category="Economics",
    ref_source="https://www.nbp.pl/publikacje/materialy_i_studia/226_en.pdf (table 2)",
)
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


@DataParser.register_dataset(
    label="mincer.params",
    summary="Mincer equation parameters per country",
    category="Economics",
    ref_source="https://www.nbp.pl/publikacje/materialy_i_studia/226_en.pdf (table 3)",
    source="""- Mincer equation formula: ln(hourly_wage) = alpha_0i + alpha_1i * edu + alpha_2i * age + alpha_3i * age**2
The results of estimation of parameters in Mincer equations in a set of countries. We
put the point estimates, standard errors (in italics) and p-values for zero restriction test of a
particular parameter (in square brackets)""",
    enrich_data="https://github.com/guydegnol/bulkhours/blob/main/bulkhours/data/mincer.py",
)
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
