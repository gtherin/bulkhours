import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def format_activities(df) -> pd.DataFrame:
    """Clean and compact Strava French export column names."""

    from pathlib import Path
    import gzip
    from fitparse import FitFile
    import re
    import dateparser

    mapping = {
        "ID de l'activité": "activity_id",
        "Date de l'activité": "date",
        "Nom de l'activité": "name",
        "Nom du fichier": "filename",
        "Type d'activité": "type",
        "Temps écoulé": "elapsed_s",
        "Temps écoulé.1": "elapsed_s1",
        "Durée de déplacement": "moving_s",
        "Distance": "distance_km",
        "Distance.1": "distance_m",
        "Vitesse max.": "vmax",
        "Vitesse moyenne": "vmean",
        "Dénivelé positif": "elev_gain",
        "Dénivelé négatif": "elev_loss",
        "Altitude min.": "alt_min",
        "Altitude max.": "alt_max",
        "Pente max.": "grade_max",
        "Pente moyenne": "grade_mean",
        "Cadence max.": "cad_max",
        "Cadence moyenne": "cad_mean",
        "Puissance moyenne": "pwr_mean",
        "Puissance moyenne pondérée": "pwr_weighted",
        "Calories": "calories",
        "Charge d’entraînement": "load",
        "Intensité": "intensity",
        "Récupération": "recovery",
        "Support": "media_path",
        "Poids du vélo": "bike_weight",
        "À partir du téléchargement": "from_upload",
        "Distance sur chemin": "trail_distance",
        "CO2 économisé": "co2_saved",
        'Fréquence cardiaque max.': 'max_hr',
        'Fréquence cardiaque max..1': 'max_hr1',
        'Fréquence cardiaque moyenne': 'avg_hr',
        'Vitesse moyenne ajustée selon la pente': 'vmean_adjslope',
    }

    columns = set(['id', 'Effort relatif', 'Température moyenne', 'Effort relatif.1', 'Puissance moyenne pondérée',
       'Distance ajustée selon la pente', 'Intensité des précipitations', 'Couverture nuageuse', 'Signalé', 'Vitesse moyenne (temps écoulé)',
       'Longueur de piscine'] + list(mapping.keys()))
    df = df[list(columns)]
    df = df.rename(columns=mapping)

    # Clean the rest (remove accents, punctuation, spaces)
    def clean_col(c):
        c = c.lower().replace("’", "'").replace("'", "").replace("î", "i").replace("é", "e").replace("è", "e").replace("à", "a").replace("ç", "c")
        c = re.sub(r"[^a-z0-9_]+", "_", c)
        c = re.sub(r"_+", "_", c).strip("_")
        return c

    df.columns = [clean_col(col) for col in df.columns]
    arename = {k: clean_col(k) for k in list(df['type'].unique())}
    df['type'] = df['type'].map(arename)

    num_cols = ["distance_km", "vmean", "vmean_adjslope", "avg_hr",  "max_hr", "calories", "moving_s"]
    for col in num_cols:
        if col in df.columns:
            df[col] = (df[col].astype(str).str.replace(",", ".").astype(float, errors="ignore"))

    return df


def read_fit_file(folder_name, activity):

    import requests
    import gzip
    import io
    from fitparse import FitFile

    url = f"https://drive.google.com/uc?export=download&id={activity.id}"

    # Download file bytes
    response = requests.get(url)
    data = response.content

    # If file is gzipped, decompress it
    fit_bytes = gzip.decompress(data)

    # Load FIT
    fitfile = FitFile(io.BytesIO(fit_bytes))

    # Get all data messages that are of type 'record'
    records = []
    for record in fitfile.get_messages('record'):
        # Get all data fields from the record
        record_data = {}
        for data_field in record.fields:
            record_data[data_field.name] = data_field.value
        records.append(record_data)

    # Create a pandas DataFrame
    return pd.DataFrame(records)


class Activity:
    def __init__(self, folder_name, info, atype=None, *args, **kwargs):
        self.atype = atype
        self.info = info
        if '.fit' in self.info.filename:
            df = read_fit_file(folder_name, self.info)
            self.df = df[[c for c in df.columns if not c.startswith('unknown_')]]
        else:
            error


class Activities:

    def __init__(self, folder_name=None, gid=None, aid=None):
        self.folder_name, self.gid, self.aid = folder_name, gid, aid

        if folder_name is not None:
            self.df = pd.read_csv(f"{folder_name}/activities.csv")
        else:
            self.df = pd.read_csv(f"https://drive.google.com/uc?export=download&id={aid}")

        self.df = format_activities(self.df)
        self.format_date()
        # Add app ids
        self.df = self.df.merge(self.read_list(), how='left', on="filename")


    def read_list(self):
        alist = pd.read_json(f"https://drive.google.com/uc?export=download&id={self.gid}").T
        alist['filename'] = 'activities/' + alist.index
        return alist

    def format_date(self):
        months = {"janv.": "Jan", "févr.": "Feb", "mars": "Mar", "avr.": "Apr", "mai": "May", "juin": "Jun", 
        "juil.": "Jul", "août": "Aug", "sept.": "Sep", "oct.": "Oct", "nov.": "Nov", "déc.": "Dec"}

        s = self.df["date"]
        for fr, en in months.items():
            s = s.str.replace(fr, en, regex=False)
        self.df["date"] = pd.to_datetime(s, format="%d %b %Y, %H:%M:%S")

    def get_activity(self, index, atype=None):
        # ['course_a_pied', 'natation', 'velo', 'randonnee', 'velo_virtuel', 'kayak', 'entra_nement', 'stand_up_paddle']
        if atype is not None:
            activity = self.df[self.df['type'] == atype].iloc[index].dropna()
        else:
            activity = self.df.iloc[index].dropna()
        return Activity(self.folder_name, activity, atype)


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
