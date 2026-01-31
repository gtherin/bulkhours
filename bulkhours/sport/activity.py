import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import sys


def read_from_drive(folder_name, activity):
    import requests
    # Download file bytes
    response = requests.get(f"https://drive.google.com/uc?export=download&id={activity.id}")
    data = response.content
    return data


def read_fit_file(data):
    import gzip
    import io
    from fitparse import FitFile

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
    def __init__(self, folder_name, info, atype=None, local=True, *args, **kwargs):
        self.atype = atype
        self.info = info

        if local:
            with open(f'/home/ubuntu/bulkcats/strava/{self.info.filename}', "rb") as f:
                data = f.read()
        else:
            data = read_from_drive(folder_name, activity)

        if '.fit' in self.info.filename:
            df = read_fit_file(data)
            #df = read_fit_file(folder_name, self.info)
            df = df[[c for c in df.columns if not c.startswith('unknown_')]].set_index('timestamp')
            df["minutes"] = (df.index - df.index[0]).total_seconds() / 60.
            df["heart_rate"] = df["heart_rate"].replace(0, np.nan)
            self.df = df
        else:
            error
