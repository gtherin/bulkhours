import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def get_activities() -> pd.DataFrame:
    """Clean and compact Strava French export column names."""

    df = pd.read_csv("/content/drive/MyDrive/bulkcats/sport/strava/activities.csv")

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
