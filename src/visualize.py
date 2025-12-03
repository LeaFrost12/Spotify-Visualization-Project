import pandas as pd
import plotly.express as px
from src.clean import load_all_data

def heatmap():
    df = load_all_data()

    # properly order the weekdays
    weekdays = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    df['weekday'] = pd.Categorical(df['weekday'], categories=weekdays, ordered=True)

    # group by weekday and hour
    time_totals = (df.groupby(['weekday', 'hour'])['ms_played'].sum().reset_index())

    # pivot to get weekday columns
    heatmap_df = time_totals.pivot(index='hour', columns='weekday', values='ms_played')

    fig = px.imshow(heatmap_df)
    
    return fig