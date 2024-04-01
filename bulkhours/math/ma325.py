from io import StringIO
import pandas as pd

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
    return pd.DataFrame([229, 211, 93, 35, 7, 1], columns=["Nk"]).T


def plot_london_bombing_dynamics(lambdas=None, frames=None, interval=100):
    from matplotlib.animation import FuncAnimation

    # Set up the figure and axis
    fig, ax = plt.subplots()
    if lambdas is None:
        lambdas = np.arange(0, 10, 1)
    line, = ax.plot(lambdas, sp.stats.poisson.pmf(lambdas, mu=0))

    # Initial legend
    legend = ax.legend([f'lambda = {0}'])

    def update(num):
        line.set_ydata(sp.stats.poisson.pmf(lambdas, mu=num))
        legend.get_texts()[0].set_text(f'#bombs/districts = lambda = {num:.2f}')
        return line,

    if frames is None:
        frames = np.linspace(0, 5, 50)
    return fig, lambdas, frames, interval, update