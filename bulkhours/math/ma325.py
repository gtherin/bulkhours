from io import StringIO
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

def get_project_data():
    data = StringIO(
        """Français	Maths	H-G	Anglais	LV2	SPC	SVT	SES	EPS
Elève 1	14	17,93	17,67	17,52	18,25	16,7	19,35	16,5	14,58
Elève 2	15,2	16,63	17,31	19,2	15,28	16,36	15,87	15	16,38
Elève 3	10	12,79	16,67	18,27	15,14	13,56	11,75	18	16,88
Elève 4	15,11	15,72	15,25	18	17,46	15,57	15,81	15,5	17,5
Elève 5	11,09	13,67	12,69	18,45	17,84	14,24	16,79	14	17,25
Elève 6	13,36	15,11	13,38	17,06	18,03	16,74	14,47	15	18,67
Elève 7	14,5	16,56	14,5	17,15	15,22	16,17	15,62	16,5	15,42
Elève 8	6,78	7	10,3	11,72	12,87	7,05	8,85	9	16
Elève 9	10,57	16,04	15,83	18,07	14,36	18,05	15,09	15,5	18,75
Elève 10	13,57	14,67	13,19	18,21	13,33	13,94	13,68	12	17
Elève 11	10,3	13,25	12	19,72	9,52	15,05	15,48	15,5	18,58
Elève 12	13,7	18,67	16	15,45	17,04	17,2	18,49	15,5	14,88
Elève 13	14,29	16,11	14,5	18,45	16,84	16	14,67	14	18,25
Elève 14	8	8,72	12,13	8,14	11,95	9,23	8,04	10	16
Elève 15	10,71	11,22	11,5	12,28	15,67	11,56	7,59	15	14,5
Elève 16	8,88	9,83	12,25	14,9	13,75	11,38	9,25	8,5	14,67
Elève 17	14	12,28	15,44	17,79	16,87	16,62	13,57	18	16,13
Elève 18	15,11	11,9	17,17	18,32	19,1	17,71	13,9	15,5	15,5
Elève 19	10,78	10,29	12,63	16,16	12,02	12,74	11,59	14	15,58
Elève 20	10,56	14,69	11,56	18,21	13,12	16,59	11,07	14	19,13
Elève 21	9,38	10,67	12,69	16,84	13,19	11,64	11,31	14,5	14
Elève 22	8,78	10,04	9,25	16,8	17,24	10,58	7,11	9,5	16,25
Elève 23	13	16,56	14,5	17,6	16,25	15,75	14,3	13,5	16,75
Elève 24	6,63	3,29	6,75	7,27	3,29	8,21	5,62	7	16,17
Elève 25	11,57	16,22	9,31	17,85	16,96	14,15	11,78	10,5	17
Elève 26	13	13,67	12,93	15,93	15,39	13,47	12,54	13	17,88
Elève 27	10	9,96	10,31	16,34	12,88	11,97	11,41	12,5	16,5
Elève 28	13	10,78	15,44	17,02	16,58	12,21	12,15	17	7,75
Elève 29	11,25	14,06	13,63	16,24	17,84	15,83	10,19	13	15,5
Elève 30	11,25	11,08	10,38	17	15,45	12,7	15,7	15	16
Elève 31	12,89	13,21	14,94	17,87	17,12	13,32	9,95	13	14,25
Elève 32	9,11	14,06	6,5	18,22	9,91	13,89	13,34	13	16,13
Elève 33	12,11	12,22	10,25	18,1	13,94	13,5	9,84	13,5	14,5
Elève 34	12,56	19,6	17,5	17,75	16,47	17,67	16,14	14	15,17
Elève 35	8,88	15,5	11,25	10,35	15,15	11,42	11,4	11	12,75
Elève 36	12,44	13,82	13,5	16,29	15,82	12,57	14,72	16	16,2
Elève 37	10,88	12,33	12	12,11	15,9	7,07	13,33	11,5	15
Elève 38	10,49	15,73	9,7	11,39	10,44	5,37	10,69	11,5	17,8
Elève 39	13,46	14,82	13	10,71	14,59	10,23	18,06	12	9
Elève 40	6,79	10,18	12,4	10,86	8	9,1	9,67	8	15,05
Elève 41	11,78	16,73	11,9	17,57	12,73	14,4	15	15,5	17,4
Elève 42	13,37	14,09	14	17	14,71	13,75	15,38	15	15,6
Elève 43	17,04	16	14,8	16,14	18,64	15,47	16,54	17,5	16
Elève 44	10,3	15,36	13,3	10,86	16,77	11,87	10,83	16	12,65
Elève 45	15,29	17,36	14,5	9	15,44	15,8	17,65	14	15
Elève 46	11,23	10	13,3	14	13,81	7	12,92	12,5	12,8
Elève 47	12,63	14,5	14,9	9,71	12,06	7,13	15,59	12,5	15,55
Elève 48	10,39	13,73	12,4	10,36	11,06	13,4	15,14	15,5	12,7
Elève 49	12,05	15,18	12,7	16,43	10,73	7,1	13,75	14	16,5
Elève 50	11,1	13,73	13,4	14,86	14,05	7,97	12,92	15,5	16,5
Elève 51	10,03	11	11	12	7,9	10,27	10,94	9,5	14,5
Elève 52	13,81	16,55	15,1	15,78	17,65	11,17	18,89	16,5	14
Elève 53	8,85	10,64	9,5	10,91	8,02	4,47	9,31	7	12,6
Elève 54	16,96	15,91	15,7	18,14	15,78	13,57	11,25	15	18,75
Elève 55	13,53	16,73	14	18	16,69	12,63	18,89	16,5	15,15
Elève 56	12,85	13,64	15,5	13,22	11,36	14,03	13,06	14	16,8
Elève 57	9,64	13,64	15,5	11,11	8,27	14,03	13,06	14	16,1
Elève 58	13,04	11,55	13	16,86	13,51	6,2	16,81	15	16,95
Elève 59	12,66	10,91	13,5	18,44	13,67	12	16,94	13,5	17,8
Elève 60	9,12	10	12,2	14,56	14,95	9,33	9,72	14	13,4
Elève 61	14,14	18,45	14,5	18,27	17,78	16,4	15	18,5	18,65
Elève 62	9,75	9,88	12	11,22	15,82	8	12,22	8,5	17,5
Elève 63	16,44	18,36	16,6	19,44	20	17,2	18,33	18	18,75
Elève 64	10,3	12,91	10,3	14,09	14,65	5,23	11,81	13	18,8
Elève 65	10,59	13,18	9,8	12,29	10,45	6,53	6,88	10	13,45
Elève 66	13,75	18,91	13,7	19,56	20	14,7	17,78	16,5	16,05""".replace(",", "."))

    return pd.read_csv(data, sep="	", index_col=0)


def get_wisc_results():
    data = StringIO(
        """WISC|CUB|PUZ|CAL|MEM|COM|VOC
I1| 5     |5    |  4   |0    |1   |1
I2| 4     |3    |  3   |2    |2   |1
I3| 2     |1    |  2   |3    |2   |2
I4|5      |3    |  5  |3    |4   |3
I5|4      |4    |  3   |2    |3   |2
I6|2      |0    |  1  |3    |1   |1
I7|3      |3    |  4   |2    |4   |4
I8|1      |2    |   1  |4    |3   |3
I9|0      |1    |   0  |3    |1   |0
I10|2      | 0   |  1   |3    |1   |0
I11|1      | 2   |  1   |1    |0   |1
I12|4      | 2   |  4   |2    |1   |2
I13|3      | 2   |  3   |3    |2   |3
I14|1      | 0   |  0   |3    |2   |2
I15|2      | 1   |  1   |2    |3   |2""")

    return pd.read_csv(data, sep="|", index_col=0)


def get_wisc_saturations():
    return StringIO(
        """ Score1 Score2 Contribution1 Contribution2 Cos2_1 Cos2_Fact12
I1 -2,5616 3,0568 13,43 33,91 0,4078 0,5807
I2 -0,9661 0,9370 1,91 3,19 0,3907 0,3676
I3 0,6765 -0,6624 0,94 1,59 0,4446 0,4263
I4 -2,7969 -1,4636 16,01 7,77 0,7160 0,1961
I5 -1,8423 0,1211 6,95 0,05 0,8142 0,0035
I6 1,8891 0,1350 7,30 0,07 0,8426 0,0043
I7 -2,3396 -1,5487 11,20 8,70 0,6028 0,2641
I8 0,7275 -2,2054 1,08 17,65 0,0816 0,7499
I9 2,8400 0,5423 16,50 1,07 0,8745 0,0319
I10 2,1733 0,6117 9,66 1,36 0,7433 0,0589
I11 1,2940 2,0373 3,43 15,06 0,2256 0,5592
I12 -0,9947 0,8181 2,02 2,43 0,3120 0,2110
I13 -0,6099 -0,8730 0,76 2,77 0,1949 0,3994
I14 2,0150 -0,9470 8,31 3,25 0,7548 0,1667
I15 0,4957 -0,5591 0,50 1,13 0,1151 0,1464""".replace(",", "."))


def get_grades():
    grades = StringIO(
        """ Maths Sciences French Latin Music
Jean 6 6 5 5,5 8
Aline 8 8 8 8 9
Annie 6 7 11 9,5 11
Monique 14,5 14,5 15,5 15 8
Didier 14 14 12 12 10
André 11 10 5,5 7 13
Pierre 5,5 7 14 11,5 10
Brigitte 13 12,5 8,5 9,5 12
Evelyne 9 9,5 12,5 12 18""".replace(",", "."))
    return pd.read_csv(grades, sep=" ", index_col=0)


def get_london_bombing():
    return pd.DataFrame({"Number_of_bombs": range(6), "Nk": [229, 211, 93, 35, 7, 1]})


def plot_london_bombing_dynamics(lambdas=None, frames=None, interval=100):
    from matplotlib.animation import FuncAnimation
    import scipy as sp

    # Set up the figure and axis
    fig, ax = plt.subplots()
    if lambdas is None:
        lambdas = np.arange(0, 10, 1)
    line, = ax.plot(lambdas, sp.stats.poisson.pmf(lambdas, mu=0))

    # Initial legend
    legend = ax.legend([f'lambda = {0}'])

    def update(num):
        line.set_ydata(sp.stats.poisson.pmf(lambdas, mu=num))
        legend.get_texts()[0].set_text(f'λ = #bombs/districts = {num:.2f}')
        return line,

    if frames is None:
        frames = np.linspace(0, 5, 50)
    return fig, lambdas, frames, interval, update