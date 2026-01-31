import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import sys

from .activity import Activity

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


class Activities:

    @staticmethod
    def get_summary_df(folder_name=None, summary_file=None):
        if folder_name is not None:
            return pd.read_csv(f"{folder_name}/activities.csv")
        else:
            return pd.read_csv(f"https://drive.google.com/uc?export=download&id={self.summary_file}")

    def __init__(self, folder_name=None, summary_file=None, activities_folder_info=None):
        self.folder_name, self.summary_file, self.activities_folder_info = folder_name, summary_file, activities_folder_info

        self.df = Activities.get_summary_df(folder_name=folder_name, summary_file=summary_file)
        self.df = format_activities(self.df)
        self.format_date()
        if self.activities_folder_info is not None:
            self.df = self.df.merge(self.read_list(drive=True), how='left', on="filename")
        elif self.folder_name is not None:
            self.df = self.df.merge(self.read_list(drive=False), how='left', on="filename")

    def read_list(self, drive=True):
        if drive:
            alist = pd.read_json(f"https://drive.google.com/uc?export=download&id={self.activities_folder_info}").T
        else:
            alist = pd.read_json(f"/home/ubuntu/bulkcats/strava/activities_folder_info.json").T
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
