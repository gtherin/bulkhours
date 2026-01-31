
from .activity import Activity  # noqa
from .activities import Activities  # noqa
from .strava import *  # noqa
from .athlete import Athlete  # noqa
from .log_perf import *  # noqa


def get_synthetic_biking_data(m=500):
    df_bike = pd.DataFrame({
        "weekly_tss": np.random.normal(420, 130, m).clip(80, 900),
        "hrs_week": np.random.normal(7, 3, m).clip(2, 20),
        "z3_pct": np.random.normal(15, 5, m).clip(5, 35),
        "z4_pct": np.random.normal(9, 4, m).clip(2, 25),
        "z5_pct": np.random.normal(2, 1, m).clip(0.1, 8),
        "weight": np.random.normal(72, 7, m),})

    df_bike["ftp"] = (
        0.8 * df_bike["weekly_tss"]
        + 2.4 * df_bike["z4_pct"]
        + np.random.normal(0, 30, m)
    ) / 10 + 50
    return df_bike


def get_synthetic_running_data(n=600):

    np.random.seed(42)

    n = 600

    df_run = pd.DataFrame({
        "avg_hr": np.random.normal(150, 9, n),
        "weekly_km": np.random.normal(50, 14, n).clip(10, 130),
        "weight": np.random.normal(70, 7, n),
        "vo2max_est": np.random.normal(48, 4, n),
    })

    df_run["time_10k"] = (
        60
        - 0.32 * (df_run["weekly_km"] - 40)
        - 0.6 * (df_run["vo2max_est"] - 45)
        + 0.06 * (df_run["weight"] - 70)
        + np.random.normal(0, 1.5, n)
    )
    return df_run


def get_vo2max_synthetic_data(n=200, random_state=42):
    np.random.seed(random_state)

    speed_5min = np.random.normal(15, 2, n)
    hr_max = np.random.normal(185, 8, n)
    age = np.random.normal(35, 10, n)
    weight = np.random.normal(72, 10, n)   # <<< nouvelle variable

    # VO2max synthétique (relation linéaire + bruit)
    vo2max = 3.5 * speed_5min + 0.15 * hr_max - 0.2 * age - 0.1 * weight + np.random.normal(0, 3, n)

    return pd.DataFrame({
        "speed_5min": speed_5min,
        "hr_max": hr_max,
        "age": age,
        "weight": weight,
        "vo2max": vo2max
    })


def get_pca_synthetic_data(n=200, random_state=42):
    rng = np.random.default_rng(0)
    n = 300

    # ----- MATRICE DE CORRÉLATION RÉALISTE -----
    corr = np.array([
        [1.00,  0.80, -0.65,  0.20,  0.85],
        [0.80,  1.00, -0.55,  0.30,  0.75],
        [-0.65, -0.55, 1.00, -0.20, -0.45],
        [0.20,  0.30, -0.20,  1.00,  0.25],
        [0.85,  0.75, -0.45,  0.25,  1.00]
    ])
    L = np.linalg.cholesky(corr)
    Z = rng.normal(size=(n, 5))
    X = Z @ L.T

    # ----- DONNÉES RÉALISTES-----
    df = pd.DataFrame({
        "vo2max":    X[:,0] * 7 + 55,
        "power_w":   X[:,1] * 40 + 260,
        "heartrate": X[:,2] * 8 + 150,
        "cadence":   X[:,3] * 4 + 88,
        "speed_5km": X[:,4] * 1.2 + 16
    })
    return df
