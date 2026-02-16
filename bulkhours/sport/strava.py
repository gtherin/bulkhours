import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import sys

from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload, MediaFileUpload
from google.oauth2 import service_account

from .activity import Activity
from .activities import Activities
from .athlete import Athlete
from .. import core
from .. import data

try:
    # Setup google drive
    credentials = service_account.Credentials.from_service_account_file('/home/ubuntu/.safebg.pyc', scopes=['https://www.googleapis.com/auth/drive'])
    service = build("drive", "v3", credentials=credentials)
except:
    service = None


class Performance:

    def __init__(self, athlete):
        self.athlete = athlete
        self.filename = "/home/ubuntu/bulkhours/data/stravism.csv.enc"

    def bpm_zones(self, df):
        # 113, 141, 155, 169
        zone_in_bpm = self.athlete.get_zones('bpm')
        df["zones_bpm"] = pd.cut(df["heart_rate"], bins=zone_in_bpm, labels=range(5), include_lowest=True)
        time_in_zone = df.groupby("zones_bpm", observed=True)["dt"].sum()
        self.update_value('zones_bpm', ";".join(time_in_zone.reindex(range(5), fill_value=0).astype(int).astype(str)))

    def update_value(self, field, value):
        self.gdf.loc[self.index, field] = value

    def update_file_id(self, ainfo, folder_id):
        # Set media mime type
        filename = f'/home/ubuntu/bulkcats/strava/{ainfo.filename}'

        media = MediaFileUpload(filename, mimetype='application/zip')
        file_metadata = {'name': filename.split('/')[-1], 'parents': [folder_id]}
        file = service.files().create(body=file_metadata, media_body=media).execute()
        #if "anyone" == str(cloud):
        service.permissions().create(fileId=file['id'], body={'type': 'anyone', 'role': 'writer'}).execute()
        core.tools.dmd(f"""* 📁 {filename.split('/')[-1]} ☁️ {file['id']}\n""")
        self.update_value('id', file['id'])
        self.update_value('modifiedTime', pd.Timestamp.now(tz="UTC"))

    def preprocess(self):
        # Load formatted new data
        gdf = Activities.get_formatted_activities('/home/ubuntu/bulkcats/strava/activities.csv')

        # Get previous reference file
        pdf = data.get_data("sport.stravism", credit=False, password=os.environ['BULK_SPORT_KEY'])

        # Merge google info
        gdf = gdf.merge(pdf[['id', 'modifiedTime', 'filename']], how='left', on="filename")

        # Add new summary columns for activities
        zcols = ['zones_bpm', 'zones_strava', 'zones_minetti', 'zones_bpm']
        for z in zcols:
            gdf[z] = ''

        # Add TRIMP load
        gdf['TRIMP'] = self.athlete.trimp_from_df(gdf)
        # Add Strava ref sTRIMP
        strimps = {16731673287: 140, 16779135626: 77, 16802972475: 91, 16854653997: 92, 16915566584: 215, 16935972434: 118, 17012903551: 177, # 2025-01-11
            17049890266: 145, # 2025-01-14
            17061165277: 161, # 2025-01-15
            }
        gdf['STRIMP'] = gdf['activity_id'].map(strimps)
        # ['course_a_pied', 'natation', 'velo', 'randonnee', 'velo_virtuel', 'kayak', 'entra_nement', 'stand_up_paddle']

        self.gdf = gdf

        for index in gdf.index:
            self.index = index

            # Get activity info
            ainfo = gdf.loc[index]
            print(index, len(gdf), ainfo.type)

            if str(ainfo.id) == 'nan':
                self.update_file_id(ainfo, os.environ['BULK_SPORT_ACTIVITIES_FOLDER'])

            # Load activity
            activity = Activity(None, ainfo, local=True)
            if activity.df.empty:
                continue

            # Get basic data
            df = activity.df#[['heart_rate']]
            df = df.set_index("seconds")
            df["dt"] = df.index.diff().fillna(0)

            zone_in_vma = self.athlete.get_zones(ainfo.type)

            self.bpm_zones(df)

            if ainfo.type == "natation":
                pass
            elif ainfo.type == "velo_virtuel":
                df = df[['dt', 'speed', 'heart_rate', 'enhanced_altitude', 'altitude', 'enhanced_speed', 'power', 'cadence', 'minutes', 'delta_seconds']]

                df['power'] = df.rolling(30, min_periods=10)["power"].mean()
                df["zones"] = pd.cut(df["power"], bins=zone_in_vma, labels=range(5), include_lowest=True)
                time_in_zone = df.groupby("zones", observed=True)["dt"].sum()
                self.update_value('zones', ";".join(time_in_zone.reindex(range(5), fill_value=0).astype(int).astype(str)))
            else:
                if 'enhanced_altitude' not in df.columns:
                    df["enhanced_altitude"] = 0

                df['delta_distance'] = df['distance'].diff()
                df['delta_altitude'] = df['enhanced_altitude'].diff()

                res = df.rolling(50, min_periods=10)[["delta_distance", "delta_seconds", 'delta_altitude']].sum()
                res["speed"] = 3.6 * res["delta_distance"] / res["delta_seconds"]
                res["slope"] = res["delta_altitude"] / res["delta_distance"]
                res[['distance']] = df[['distance']]

                # Minetti correction
                def correct_speed_to_slope(speed, slope):
                    C = 155.4*slope**5 - 30.4*slope**4 - 43.3*slope**3 + 46.3*slope**2 + 19.5*slope + 3.6
                    return speed * C / 3.6

                # Strava correction
                def correct_speed_to_slope2(speed, slope):
                    g = 100 * slope
                    F = 1 + 0.033*g + 0.0006*(g**2)
                    return speed * F

                res["dt"] = res.index.diff().fillna(0)
                res["speed_flat_minetti"] = correct_speed_to_slope(res["speed"], res["slope"])
                res["zones_minetti"] = pd.cut(res["speed_flat_minetti"], bins=zone_in_vma, labels=range(5), include_lowest=True)
                time_in_zone = res.groupby("zones_minetti", observed=True)["dt"].sum()
                self.update_value('zones_minetti', ";".join(time_in_zone.reindex(range(5), fill_value=0).astype(int).astype(str)))
 
                res["speed_flat_strava"] = correct_speed_to_slope2(res["speed"], res["slope"])
                res["zones_strava"] = pd.cut(res["speed_flat_strava"], bins=zone_in_vma, labels=range(5), include_lowest=True)
                time_in_zone = res.groupby("zones_strava", observed=True)["dt"].sum()
                self.update_value('zones_strava', ";".join(time_in_zone.reindex(range(5), fill_value=0).astype(int).astype(str)))

        print(self.gdf.columns)
        #print(gdf[['load', 'activity_id', 'elapsed_s', 'type', 'avg_hr', 'date', 'TRIMP', 'STRIMP'] + zcols].tail(10))
        print(f"/home/ubuntu/bulkhours/data/stravism.csv.enc")
        data.secure_save(gdf, f"/home/ubuntu/bulkhours/data/stravism.csv.enc", os.environ['BULK_SPORT_KEY'])

def preprocess(argv=sys.argv):
    athlete = Athlete(age=46, weight=79, hr_max=174, vo2_max=52,
                      hr_rest=48, v_max=27, css=0.95, ftp=236)

    p = Performance(athlete)
    p.preprocess()
