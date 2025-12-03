# aggregate the data by date
import pandas as pd
from src.clean import load_all_data

df = load_all_data()

#########
# convert to datetime
df['ts_local'] = pd.to_datetime(df['ts_local'], errors='coerce')
#group by date
daily = df.groupby(df['ts_local'].dt.date)['ms_played'].sum()
# calculate the mins
daily_min = daily / (1000 * 60)
# convert to df
daily_df = daily_min.reset_index(name='min_played')

########
# cut out before certain date
# ensure datetime
daily_df['ts_local'] = pd.to_datetime(daily_df['ts_local'])
# filter out rows before cutoff
cutoff = "2021-05-01"
daily_df = daily_df[daily_df['ts_local'] >= cutoff]

########
# aggregate 7 days
daily_df['7d_avg'] = daily_df['min_played'].rolling(7, min_periods=1).mean()
# aggregate 30 days
daily_df['30d_avg'] = daily_df['min_played'].rolling(30, min_periods=1).mean()

daily_df['year'] = daily_df['ts_local'].dt.year


# callable function to get agg data
def load_agg_data():
    return daily_df



###################3
# agg by artist


# group
artist_totals = df.groupby('artist_name')['ms_played'].sum().reset_index()
# calculate minutes
artist_totals['min_played'] = artist_totals['ms_played'] /(1000*60)
# sort
artist_totals = artist_totals.sort_values('min_played', ascending=False)
top10_artist = artist_totals.sort_values('min_played', ascending=False).head(10)


def load_artist_data(df, year=None):
    if year is not None: # return all years
        df['ts_local'] = pd.to_datetime(df['ts_local'])
        df['year'] = df['ts_local'].dt.year
        df = df[df['year'] == year]
    
    artist_totals = df.groupby('artist_name')['ms_played'].sum().reset_index()
    # calculate minutes
    artist_totals['min_played'] = artist_totals['ms_played'] /(1000*60)
    # sort
    artist_totals = artist_totals.sort_values('min_played', ascending=False)
    top10 = artist_totals.sort_values('min_played', ascending=False).head(10)

    return artist_totals, top10


###############
# agg by track
# group
track_totals = df.groupby('track_name')['ms_played'].sum().reset_index()
# calculate minutes
track_totals['min_played'] = track_totals['ms_played'] /(1000*60)
# sort
track_totals = track_totals.sort_values('min_played', ascending=False)
top10_track = track_totals.sort_values('min_played', ascending=False).head(10)


def load_track_data(df, year=None):
    if year is not None: # return all years
        df['ts_local'] = pd.to_datetime(df['ts_local'])
        df['year'] = df['ts_local'].dt.year
        df = df[df['year'] == year]
    
    track_totals = df.groupby('track_name')['ms_played'].sum().reset_index()
    # calculate minutes
    track_totals['min_played'] = track_totals['ms_played'] /(1000*60)
    # sort
    track_totals = track_totals.sort_values('min_played', ascending=False)
    top10_track = track_totals.sort_values('min_played', ascending=False).head(10)

    return track_totals, top10_track


#################
# aggregate by time of week
time_totals = df.groupby(['weekday', 'hour'])['ms_played'].sum().reset_index()

