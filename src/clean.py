# module for processing json files

import os
import json
import pandas as pd

dir = "./data/raw"

df_all = pd.DataFrame()


# iterate through files
for file in os.listdir(dir):
    filename = os.fsdecode(file)
    if filename.endswith(".json"): 
        # get path
        file_path = os.path.join(dir, filename)
        #print(filename)
        
        #### clean & convert to csv
        # load json
        with open(file_path, 'r', encoding="utf-8") as f:
            data = json.load(f)
        # convert data to df
        df = pd.DataFrame(data)

        # drop irrelevant variables
        df = df[['ts', 'ms_played', 'master_metadata_track_name', 'master_metadata_album_artist_name',
        'master_metadata_album_album_name','spotify_track_uri']]
        # clean
        #print("Before cleaning:")
        #print(df.isna().sum())
        df_clean = df.dropna(subset=['master_metadata_track_name'])
        #print("After cleaning:")
        #print(df_clean.isna().sum())




        # create time variables
        df["ts"] = pd.to_datetime(df["ts"], utc=True)
        df["ts_local"] = df["ts"].dt.tz_convert("US/Eastern")
        df["year"] = df["ts_local"].dt.year
        df["month"] = df["ts_local"].dt.month
        df["day"] = df["ts_local"].dt.day
        df["weekday"] = df["ts_local"].dt.day_name()
        df["hour"] = df["ts_local"].dt.hour
        df["date"] = df["ts_local"].dt.date

        # rename columns to something nice
        df = df.rename(columns={
            "master_metadata_track_name": "track_name",
            "master_metadata_album_artist_name": "artist_name",
            "master_metadata_album_album_name": "album_name"
        })

        # drop white noise
        df = df[df['artist_name'] != "White Noise Therapy"]

        # add to total df
        df_all = pd.concat([df_all, df])

        continue
    else:
        continue

# save to csv
df_all.to_csv('./data/clean/spotify_clean.csv')

# callable function
def load_all_data():
    return df_all


