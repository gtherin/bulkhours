import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import sys
import requests
import time
import datetime
import json
from urllib.parse import urlencode

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



def load_env_file(env_file=None):
    env_path = env_file or os.getenv("BULKHOURS_ENV_FILE", "/home/ubuntu/.env")
    if not os.path.exists(env_path):
        return

    with open(env_path, "r") as handle:
        for raw_line in handle:
            line = raw_line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, value = line.split("=", 1)
            key = key.strip()
            value = value.strip().strip('"').strip("'")
            if key and key not in os.environ:
                os.environ[key] = value


load_env_file()

CLIENT_ID = os.getenv("STRAVA_CLIENT_ID", "")
CLIENT_SECRET = os.getenv("STRAVA_CLIENT_SECRET", "")
REFRESH_TOKEN = os.getenv("STRAVA_REFRESH_TOKEN", "")


def _validate_strava_config():
    missing = []
    if not CLIENT_ID:
        missing.append("STRAVA_CLIENT_ID")
    if not CLIENT_SECRET:
        missing.append("STRAVA_CLIENT_SECRET")
    if not REFRESH_TOKEN:
        missing.append("STRAVA_REFRESH_TOKEN")

    if missing:
        raise ValueError(f"Missing Strava credentials: {', '.join(missing)}")


def refresh_access_token():
    _validate_strava_config()

    TOKEN_URL = "https://www.strava.com/oauth/token"
    response = requests.post(
        TOKEN_URL,
        data={"client_id": CLIENT_ID, "client_secret": CLIENT_SECRET,
            "grant_type": "refresh_token",
            "refresh_token": REFRESH_TOKEN,
        },
        timeout=30,
    )

    if response.status_code >= 400:
        details = response.text
        try:
            payload = response.json()
            if isinstance(payload, dict):
                msg = payload.get("message")
                errors = payload.get("errors")
                details = f"message={msg}; errors={errors}"
        except ValueError:
            pass
        raise RuntimeError(
            f"Strava token refresh failed ({response.status_code}). {details}. "
            "Check STRAVA_CLIENT_ID/STRAVA_CLIENT_SECRET/STRAVA_REFRESH_TOKEN and regenerate refresh_token if needed."
        )

    tokens = response.json()
    access_token = tokens.get("access_token")
    if not access_token:
        raise RuntimeError("Strava token response does not contain 'access_token'.")
    return access_token


def get_last_week_timestamp():
    now = datetime.datetime.utcnow()
    last_week = now - datetime.timedelta(days=7)
    return int(last_week.timestamp())


def _strava_error_details(response):
    details = response.text
    try:
        payload = response.json()
        if isinstance(payload, dict):
            message = payload.get("message")
            errors = payload.get("errors")
            details = f"message={message}; errors={errors}"
    except ValueError:
        pass
    return details


def build_strava_authorization_url():
    params = {
        "client_id": CLIENT_ID,
        "redirect_uri": os.getenv("STRAVA_REDIRECT_URI", "https://localhost/exchange_token"),
        "response_type": "code",
        "approval_prompt": "force",
        "scope": os.getenv("STRAVA_SCOPE", "activity:read_all"),
    }
    return f"https://www.strava.com/oauth/authorize?{urlencode(params)}"


def download_last_week_activities(access_token):
    after_timestamp = get_last_week_timestamp()
    page = 1
    per_page = 100
    all_activities = []

    headers = {"Authorization": f"Bearer {access_token}"}

    while True:
        params = {"after": after_timestamp, "page": page, "per_page": per_page,}

        ACTIVITIES_URL = "https://www.strava.com/api/v3/athlete/activities"
        response = requests.get(
            ACTIVITIES_URL, headers=headers, params=params, timeout=30
        )

        if response.status_code == 401:
            details = _strava_error_details(response)
            raise PermissionError(
                f"Strava activities request unauthorized (401). {details}. "
                "This usually means the token is invalid/expired or the app does not have activity read scope."
            )
        if response.status_code >= 400:
            details = _strava_error_details(response)
            raise RuntimeError(f"Strava activities request failed ({response.status_code}). {details}")

        activities = response.json()

        if not activities:
            break

        all_activities.extend(activities)
        page += 1

    return all_activities


def _download_activity_details(access_token, activity_id):
    headers = {"Authorization": f"Bearer {access_token}"}

    ACTIVITY_URL = "https://www.strava.com/api/v3/activities"
    detail_response = requests.get(
        f"{ACTIVITY_URL}/{activity_id}",
        headers=headers,
        params={"include_all_efforts": "true"},
        timeout=30,
    )
    if detail_response.status_code >= 400:
        details = _strava_error_details(detail_response)
        raise RuntimeError(f"Failed to fetch activity {activity_id} details ({detail_response.status_code}). {details}")

    ACTIVITY_STREAMS_URL = "https://www.strava.com/api/v3/activities/{activity_id}/streams"
    streams_response = requests.get(
        ACTIVITY_STREAMS_URL.format(activity_id=activity_id),
        headers=headers,
        params={
            "keys": "time,latlng,distance,altitude,velocity_smooth,heartrate,cadence,watts,temp,moving,grade_smooth",
            "key_by_type": "true",
        },
        timeout=30,
    )
    if streams_response.status_code >= 400:
        details = _strava_error_details(streams_response)
        raise RuntimeError(f"Failed to fetch activity {activity_id} streams ({streams_response.status_code}). {details}")

    return detail_response.json(), streams_response.json()


def download_activity_details(access_token, activities, output_dir="last_week_activity_details"):
    os.makedirs(output_dir, exist_ok=True)
    exported = 0

    for activity in activities:
        activity_id = activity.get("id")
        if not activity_id:
            continue

        try:
            detail, streams = _download_activity_details(access_token, activity_id)
        except Exception as exc:
            print(f"⚠️ Skip activity {activity_id}: {exc}")
            continue

        payload = {"summary": activity, "detail": detail, "streams": streams,}

        activity_file = os.path.join(output_dir, f"activity_{activity_id}.json")
        with open(activity_file, "w") as handle:
            json.dump(payload, handle, indent=2)
        exported += 1

    print(f"💾 Saved {exported} detailed activity files in {output_dir}")
    return exported


# Get strava data
def copy_strava_files(dry_run=False):
    print("🔄 Refreshing access token...")
    try:
        access_token = refresh_access_token()
    except Exception as exc:
        print(f"❌ {exc}")
        return []

    print("📥 Downloading last week activities...")
    try:
        activities = download_last_week_activities(access_token)
    except PermissionError as exc:
        print(f"⚠️ {exc}")
        print("🔁 Retrying once with a newly refreshed token...")
        access_token = refresh_access_token()
        try:
            activities = download_last_week_activities(access_token)
        except PermissionError as exc_retry:
            print(f"❌ {exc_retry}")
            print("🔐 Re-authorize the Strava app with activity read scope, then replace STRAVA_REFRESH_TOKEN.")
            print(f"🌐 Authorization URL: {build_strava_authorization_url()}")
            print("ℹ️ After approval, exchange the returned code for a new refresh token.")
            return []

    print(f"✅ Retrieved {len(activities)} activities")

    # Save to file
    with open("last_week_activities.json", "w") as f:
        json.dump(activities, f, indent=2)

    print("💾 Saved to last_week_activities.json")

    print("📦 Downloading detailed activities and streams...")
    download_activity_details(access_token, activities)

    return activities

def preprocess(argv=sys.argv):
    if 0:
        copy_strava_files(dry_run=False)
    athlete = Athlete(age=46, weight=79, hr_max=174, vo2_max=52,
                      hr_rest=48, v_max=27, css=0.95, ftp=236)

    p = Performance(athlete)
    p.preprocess()
