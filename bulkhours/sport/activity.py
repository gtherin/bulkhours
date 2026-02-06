import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import sys
import requests


class Activity:
    def __init__(self, folder_name, info, atype=None, local=True, *args, **kwargs):
        self.atype = atype
        self.info = info

        try:
            if '.fit' in self.info.filename:
                if local:
                    with open(f'/home/ubuntu/bulkcats/strava/{self.info.filename}', 'rb') as f:
                        data = f.read()
                else:
                    response = requests.get(f"https://drive.google.com/uc?export=download&id={self.info.id}")
                    data = response.content
                df = Activity.read_fit_file(data)
            elif '.gpx' in self.info.filename:
                df = Activity.read_gpx_file(f'/home/ubuntu/bulkcats/strava/{self.info.filename}')
            elif '.tcx' in self.info.filename:
                df = Activity.read_tcx_file(f'/home/ubuntu/bulkcats/strava/{self.info.filename}')
            else:
                print(f'Fuck {self.info.filename}')
                raise Exception(f'Fuck {self.info.filename}')
            df.index = pd.to_datetime(df.index)
            df["seconds"] = (df.index - df.index[0]).total_seconds()
            df["minutes"] = df["seconds"] / 60.
            df["delta_seconds"] = df["seconds"].diff()
            if 'heart_rate' in df.columns:
                df["heart_rate"] = df["heart_rate"].replace(0, np.nan)
            else:
                df["heart_rate"] = np.nan
            self.df = df
        except:
            self.df = pd.DataFrame()

    @staticmethod
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
        df = pd.DataFrame(records)
        return df[[c for c in df.columns if not c.startswith('unknown_')]].set_index('timestamp')

    @staticmethod
    def read_gpx_file(path):
        import gpxpy
        rows = []
        with open(path, "r") as f:
            gpx = gpxpy.parse(f)

        for track in gpx.tracks:
            for seg in track.segments:
                for p in seg.points:
                    row = {"time": p.time, "lat": p.latitude, "lon": p.longitude, "elevation": p.elevation}
                    # ---- EXTENSIONS (HR, cadence, power, temp...) ----
                    for ext in p.extensions:
                        for child in ext:
                            tag = child.tag.split("}")[-1]  # remove namespace
                            try:
                                row[tag] = float(child.text)
                            except (TypeError, ValueError):
                                row[tag] = child.text

                    rows.append(row)
        return pd.DataFrame(rows).set_index("time")

    @staticmethod
    def read_tcx_file(path):

        import gzip
        import pandas as pd
        import xmltodict

        with gzip.open(path, "rb") as f:
            tcx = xmltodict.parse(f)

        # Navigate to trackpoints (handles 1 or multiple laps)
        activity = tcx["TrainingCenterDatabase"]["Activities"]["Activity"]
        laps = activity["Lap"]

        if not isinstance(laps, list):
            laps = [laps]

        trackpoints = []
        for lap in laps:
            track = lap.get("Track")
            if not track:
                continue
            tps = track["Trackpoint"]
            if isinstance(tps, dict):
                tps = [tps]
            trackpoints.extend(tps)

        df = pd.json_normalize(trackpoints).set_index('Time')
        df = df.rename(columns={
            'DistanceMeters': 'distance',
            'AltitudeMeters': 'altitude',
            })
        print(df)
        return df
