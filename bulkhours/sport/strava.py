import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import sys

from .activity import Activity
from .activities import Activities
from .athlete import Athlete
from ..data import safe_loader as loader


class Performance:

    def __init__(self, athlete, activities):
        self.athlete = athlete
        self.activities = activities

    def preprocess(self):
        gdf = self.activities.df
        gdf['zones'] = ''
        zone_in_bpm = self.athlete.get_zones_in_bpm()
        print(self.athlete.zones, zone_in_bpm)
        gdf['TRIMP'] = self.athlete.trimp_from_df(gdf)
        return

        strimps = {
            16731673287: 140,
            16779135626: 77,
            16802972475: 91,
            16854653997: 92,
            16915566584: 215,
            16935972434: 118,
            17012903551: 177, # 2025-01-11
            17049890266: 145, # 2025-01-14
            17061165277: 161, # 2025-01-15
            }
        gdf['STRIMP'] = gdf['activity_id'].map(strimps)

        for index in gdf.index:

            print(index, gdf.loc[index]['date'], gdf.loc[index]['activity_id'], gdf.loc[index]['type'], gdf.loc[index]['filename'])
            activity = Activity(None, gdf.loc[index], local=True)
            if activity.df.empty:
                continue

            df = activity.df#[['heart_rate']]
            df = df.set_index("seconds")

            tzones = {}
            rzones = []
            for i in range(5):
                ev = df[(df['heart_rate'] >= zone_in_bpm[i]) & (df['heart_rate'] < zone_in_bpm[i+1])]
                rzones.append(f"{ev['delta_seconds'].sum():.0f}")

            gdf.loc[index, 'zones'] = ';'.join(rzones)
            print(rzones)

        print(gdf.columns)
        print(gdf[['load', 'activity_id', 'elapsed_s', 'type', 'avg_hr', 'date','zones', 'TRIMP', 'STRIMP']].tail(10))
        print(f"/home/ubuntu/bulkcats/strava/summary.csv")
        loader.secure_save(gdf, f"/home/ubuntu/bulkhours/data/stravism.csv.enc", os.environ['BULK_SPORT_KEY'])
        gdf.to_csv(filename:=f"/home/ubuntu/bulkcats/strava/summary.csv")
        self.activities.df = df


def preprocess(argv=sys.argv):
    file_id = os.environ['BULK_SPORT_ACTIVITIES_FOLDER']
    activities = Activities(folder_name='/home/ubuntu/bulkcats/strava')

    athlete = Athlete(age=46, weight=79, hr_max=174, vo2_max=52,
                      hr_rest=48, v_max=27, css=0.86, ftp=210)

    p = Performance(athlete, activities)
    p.preprocess()

    return
    if list_files:
        import bulkback
        bulkback.admin.gdrive.GFolders.force_list_folder(
            file_id, 
            #folder_cache=f"/home/ubuntu/bulkcats/strava/folder.{file_id}.json"
            folder_cache=f"/home/ubuntu/bulkcats/strava/activities_folder_info.json"
            )
