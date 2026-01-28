import pandas as pd
import numpy as np
import sklearn.linear_model


class LogModel(sklearn.linear_model.LinearRegression):
    def __init__(self, intercept=1.0, slope=-0.05, fit_intercept=True, name=''):
        super().__init__(fit_intercept=fit_intercept)

        # store parameters (for cloning / introspection)
        self.intercept = intercept
        self.slope = slope

        self.intercept_ = intercept
        self.coef_ = np.array([slope])
        self.n_features_in_ = 1
        self.name = name

    def fit(self, X, y):
        X_log = np.log(np.asarray(X))
        return super().fit(X_log, y)

    def predict(self, X):
        X_log = np.log(np.asarray(X))
        return super().predict(X_log)

    def __repr__(self):
        return f'{self.name}={self.intercept_:.2f} {self.coef_[0]:.2f} x log(D)'


import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from scipy.optimize import fsolve


def ftp_to_speed_scalar(ftp, mass=80, CdA=0.25, Cr=0.004, rho=1.225,):
    def equation(v):
        return 0.5 * rho * CdA * v**3 + Cr * mass * 9.81 * v - ftp
    v0 = 10  # initial guess (m/s)
    v = fsolve(equation, v0)[0]
    return v * 3.6  # km/h
ftp_to_speed = np.vectorize(ftp_to_speed_scalar)



class Discipline:

    def plot(self, athlete, D=None):
        import plotly.graph_objects as go
        from plotly.subplots import make_subplots

        if D is None:
            D = np.array([0.4, 0.8, 1.5, 3, 5, 10, 20, 21.1, 42.195])

        df = pd.DataFrame({"Distance (km)": D})
        df = self.predict_speed(athlete, df)
        df['Estimated time (h)'] = df['Distance (km)'] / df['Speed (km/h)']
        df['TriEstimated time (h)'] = df['Distance (km)'] / df['TriSpeed (km/h)']

        display(df.T)

        # Create figure with secondary axis
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        fig.add_trace(go.Scatter(x=df["Distance (km)"], y=df["Speed (km/h)"], mode="lines+markers", name="Speed (km/h)"), secondary_y=False)
        fig.add_trace(go.Scatter(x=df["Distance (km)"], y=df["TriSpeed (km/h)"], mode="lines+markers", name="Tri-Speed (km/h)"), secondary_y=False)
        fig.add_trace(go.Scatter(x=df["Distance (km)"], y=df["Estimated time (h)"], mode="lines+markers", name="Estimated time (h)"), secondary_y=True)
        fig.add_trace(go.Scatter(x=df["Distance (km)"], y=df["TriEstimated time (h)"], mode="lines+markers", name="Tri-Estimated time (h)"), secondary_y=True)
        return fig

    def predict_speed(self, athlete, df):
        df['Speed (km/h)'] = self.raw.predict(df[['Distance (km)']]) * self.perf_max(athlete)
        df['TriSpeed (km/h)'] = self.min3.predict(df[['Distance (km)']]) * self.perf_max(athlete)
        return df


class Swim(Discipline):
    def __init__(self):
        self.emp = pd.DataFrame({
            "Distance (km)": [0.75, 1.5, 1.9, 3.8],
            "Intensity (min)": [0.95, 0.92, 0.88, 0.85],
            "Intensity (max)": [1.00, 0.97, 0.92, 0.90],
            })

        self.min3 = LogModel(name='swim3_min').fit(self.emp[["Distance (km)"]], self.emp["Intensity (min)"])
        self.max3 = LogModel(name='swim3_max').fit(self.emp[["Distance (km)"]], self.emp["Intensity (max)"])
        self.raw = LogModel(name='swim0', intercept=1.05, slope=-0.05)
    def perf_max(self, athlete):
        return athlete.css
swim = Swim()


class Bike(Discipline):
    def __init__(self):
        self.emp = pd.DataFrame({
            "Distance (km)": [20, 40, 90, 180],
            "Intensity (min)": [0.95, 0.90, 0.80, 0.70],
            "Intensity (max)": [1.05, 0.95, 0.85, 0.78],
        })

        self.min3 = LogModel(name='bike3_min').fit(self.emp[["Distance (km)"]], self.emp["Intensity (min)"])
        self.max3 = LogModel(name='bike3_max').fit(self.emp[["Distance (km)"]], self.emp["Intensity (max)"])
        self.raw = LogModel(name='bike0', intercept=1.00, slope=-0.05)

    def predict_speed(self, athlete, df):
        df['Speed (km/h)'] = ftp_to_speed(mbike0.predict(df[['Distance (km)']]) * ftp)
        df['TriSpeed (km/h)'] = ftp_to_speed(mbike3.predict(df[['Distance (km)']]) * ftp)
        return df

    def perf_max(self, athlete):
        return athlete.ftp
bike = Bike()

class Run(Discipline):
    def __init__(self):
        self.emp = pd.DataFrame({
            "Distance (km)": [5.0, 10.0, 21.1, 42.195],
            "Intensity (min)": [0.90, 0.85, 0.75, 0.65],
            "Intensity (max)": [0.95, 0.90, 0.82, 0.75],
        })

        self.min3 = LogModel(name='run3_min').fit(self.emp[["Distance (km)"]], self.emp["Intensity (min)"])
        self.max3 = LogModel(name='run3_max').fit(self.emp[["Distance (km)"]], self.emp["Intensity (max)"])
        self.raw = LogModel(name='run0', intercept=1.06, slope=-0.06)
    def perf_max(self, athlete):
        return athlete.vma
run = Run()
