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

    columns = set(['Effort relatif', 'Température moyenne', 'Effort relatif.1', 'Puissance moyenne pondérée',
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

    from pathlib import Path
    import gzip
    from fitparse import FitFile
    import re
    import dateparser

    path = Path(f"{folder_name}/{activity.filename}")

    # Open the gzip file and read its content into memory
    with gzip.open(path, 'rb') as f:
        fit_content = f.read()

    # Parse the FIT data from the content in memory
    fitfile = FitFile(fit_content)

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
        #super().__init__(*args, **kwargs)
        self.atype = atype
        self.info = info
        if '.fit' in self.info.filename:
            df = read_fit_file(folder_name, self.info)
            self.df = df[[c for c in df.columns if not c.startswith('unknown_')]]
        else:
            error


class Activities:#(pd.DataFrame):

    def __init__(self, folder_name=None, gid=None, aid=None, athlete_name=None):
        #super().__init__(*args, **kwargs)
        self.athlete_name = athlete_name
        self.folder_name = folder_name

        if folder_name is not None:
            self.df = pd.read_csv(f"{folder_name}/activities.csv")
        else:
            self.df = pd.read_csv(f"https://drive.google.com/uc?export=download&id={aid}")
            alist = pd.read_json(f"https://drive.google.com/uc?export=download&id={gid}")
            self.df = self.df.merge(alist.T, how='left', left_on="Nom du fichier", right_index=True)

        self.df = format_activities(self.df)

    def get_activity(self, index, atype=None):
        # ['course_a_pied', 'natation', 'velo', 'randonnee', 'velo_virtuel', 'kayak', 'entra_nement', 'stand_up_paddle']
        if atype is not None:
            activity = self.df[self.df['type'] == atype].iloc[index].dropna()
        else:
            activity = self.df.iloc[index].dropna()
        return Activity(self.folder_name, activity, atype)
