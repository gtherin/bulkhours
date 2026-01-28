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

eswim3 = pd.DataFrame({
    "Distance (km)": [0.75, 1.5, 1.9, 3.8],
    "Intensity (min)": [0.95, 0.92, 0.88, 0.85],
    "Intensity (max)": [1.00, 0.97, 0.92, 0.90],
    })

mswim3 = LogModel(name='mswim3').fit(eswim3[["Distance (km)"]], eswim3["Intensity (min)"])
mswim0 = LogModel(name='mswim0', intercept=1.05, slope=-0.05)

ebike3 = pd.DataFrame({
    "Distance (km)": [20, 40, 90, 180],
    "Intensity (min)": [0.95, 0.90, 0.80, 0.70],
    "Intensity (max)": [1.05, 0.95, 0.85, 0.78],
    })
mbike3 = LogModel(name='mbike3').fit(ebike3[["Distance (km)"]], ebike3["Intensity (min)"])
mbike0 = LogModel(name='mbike0', intercept=1.00, slope=-0.05)
mbike3.predict(ebike3[['Distance (km)']])

erun3 = pd.DataFrame({
    "Distance (km)": [5.0, 10.0, 21.1, 42.195],
    "Intensity (min)": [0.90, 0.85, 0.75, 0.65],
    "Intensity (max)": [0.95, 0.90, 0.82, 0.75],
    })
mrun3 = LogModel(name='mrun3').fit(erun3[["Distance (km)"]], erun3["Intensity (min)"])
mrun3.predict(erun3[['Distance (km)']])
mrun0 = LogModel(name='mrun0', intercept=1.06, slope=-0.06)

