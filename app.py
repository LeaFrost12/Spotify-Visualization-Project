# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.


from dash import Dash, html, dcc,Input, Output
import plotly.express as px
import pandas as pd
from src.aggregate import load_agg_data, load_artist_data, load_track_data
from src.clean import load_all_data
from src.visualize import heatmap

# Initialize app
app = Dash(__name__)
server = app.server

###############
### data
df = load_all_data()
daily_df = load_agg_data(df)
artist_options = sorted(df['artist_name'].dropna().unique().tolist())


# Create app layout
app.layout = html.Div(children=[
    html.H1(children='CSCE 567 Final Project - Lea Frost'),

    html.Div('The data for this project was downloaded from my Spotify account.'),

    html.Div(['The raw original data in json format is accessible by this link: ',
    html.A("Kaggle Link", href="https://www.kaggle.com/datasets/leafrost/my-spotify-extended-streaming-history",
           target="_blank")]),
    
    html.Br(), html.Br(),

    ### listening graph
    html.B(children=
        "Listening time",
        style={
        'fontSize': '24px'}),
    html.Br(),html.Br(),
    html.Div(children=
        "Filter by year"),

    dcc.Dropdown(
        id='year-dropdown1',
        #year options
        options=[{'label': 'All Years', 'value': 'all'}] + 
                    [{'label': str(y), 'value': y} for y in sorted(daily_df['year'].unique())],
        # default value is all
        value='all',
        clearable=False
    ),
    dcc.Graph(
        id='listening-graph'
    ),

    ### artist bar chart
    html.B(children=
        "Top artists",
        style={
        'fontSize': '24px'}),
    html.Br(),html.Br(),
    html.Div(children=
        "Filter by year"),
    dcc.Dropdown(
        id='year-dropdown2',
        #year options
        options=[{'label': 'All Years', 'value': 'all'}] + 
                    [{'label': str(y), 'value': y} for y in sorted(daily_df['year'].unique())],
        # default value is all
        value='all',
        clearable=False
    ),
    dcc.Graph(
        id='top-artist-graph'
    ),

    ### track bar chart
    html.B(children=
        "Top tracks",
        style={
        'fontSize': '24px'}),
    html.Br(),html.Br(),
    html.Div(children=
        "Filter by year"),
    dcc.Dropdown(
        id='year-dropdown3',
        #year options
        options=[{'label': 'All Years', 'value': 'all'}] + 
                    [{'label': str(y), 'value': y} for y in sorted(daily_df['year'].unique())],
        # default value is all
        value='all',
        clearable=False
    ),
    dcc.Graph(
        id='track-graph'
    ),

    #############
    ### artist over time
    html.B(children=
        "Artists over time",
        style={
        'fontSize': '24px'}),
    html.Br(),html.Br(),
    html.Div(children=
        "Choose an artist"),
    dcc.Dropdown(
        id='artist-dropdown',
        #year options
        options= [{'label': a, 'value': a} for a in artist_options],
        # default value is all
        value='Clairo',
        clearable=True,
        placeholder="Type in artist name..."
    ),
    dcc.Graph(
        id='artist-graph'
    ),

    ##########
    # time heat map
    html.B(children=
        "Listening over the week",
        style={
        'fontSize': '24px'}),
    dcc.Graph(id="heatmap",
              figure = heatmap()),
    
])

# Callback 1: Listening line chart
@app.callback(
    Output('listening-graph', 'figure'),
    Input('year-dropdown1', 'value')
)
def update_figure1(year):
    # filter the df by year
    if year == 'all':
        filtered = daily_df
        title = "Daily Listening (All Years)"
    else:
        filtered = daily_df[daily_df['year'] == year]
        title = f"Daily Listening ({year})"

    ### Create figures
    fig = px.line(filtered, x='ts_local', y='min_played', 
                  title=title, template='plotly_white',
                  )
    

    fig.update_traces(opacity=0.2)
    fig.add_scatter(x=filtered['ts_local'], y=filtered['30d_avg'], mode='lines', name='30-day avg')
    fig.update_traces(
            hovertemplate=
                "%{x}<br>" + 
                "Minutes: %{y:.0f}"
        )
    fig.update_traces(line_color='#1db954')
    fig.update_xaxes(title='Date')
    fig.update_yaxes(title='Minutes listened')


    fig.update_xaxes(title='Date')
    fig.update_yaxes(title='Minutes listened')
    return fig

# Callback 2: Artist chart
@app.callback(
    Output('top-artist-graph', 'figure'),
    Input('year-dropdown2', 'value')
)
def update_figure2(year):
    # filter the df by year
    if year == 'all':
        # load regular data
        _, top10 = load_artist_data(df)
        title = "Top 10 Artists (All Years)"

    else: # if year specified, load only that year
        _, top10 = load_artist_data(df, year)
        title = f"Top 10 Artists ({year})"

    ### Create figs
    top10_fig = px.bar(top10, y='artist_name', x='min_played', title=title,
                color='artist_name', orientation='h')
    top10_fig.update_yaxes(title='')
    top10_fig.update_xaxes(title='Minutes listened')
    top10_fig.update_layout(showlegend=False)

    top10_fig.update_traces(
            hovertemplate=
                "%{y}<br>" + 
                "Minutes: %{x:.0f}"
        )

    return top10_fig

# Callback 3: Track chart
@app.callback(
    Output('track-graph', 'figure'),
    Input('year-dropdown3', 'value')
)
def update_figure3(year):
    # filter the df by year
    if year == 'all':
        # load regular data
        track_totals, top10_tracks = load_track_data(df)
        title = "Top 10 Tracks (All Years)"

    else: # if year specified, load only that year
        track_totals, top10_tracks = load_track_data(df, year)
        title = f"Top 10 Tracks ({year})"

    ### Create figs
    top10_fig = px.bar(top10_tracks, y='track_name', x='min_played', title=title,
                color='track_name', template='plotly_white', orientation='h' )
    top10_fig.update_yaxes(title='')
    top10_fig.update_xaxes(title='Minutes listened')
    top10_fig.update_layout(showlegend=False)

    top10_fig.update_traces(
            hovertemplate=
                "%{y}<br>" + 
                "Minutes: %{x:.0f}"
        )

    return top10_fig

# Callback 4: Artist over time
@app.callback(
    Output('artist-graph', 'figure'),
    Input('artist-dropdown', 'value')
)
def update_artist_plot(artist):
     if not artist: # no artist selected
        fig = px.line(title="Enter an artist to see listening over time")
        return fig
     # get artist's data
     artist_df = df[df['artist_name'].str.lower() == artist.lower()]

    # if no data
     if artist_df.empty:
        fig = px.line(title=f"No listening found for '{artist}'")
        return fig
     
     artist_daily = artist_df.groupby(artist_df['ts_local'].dt.date)['ms_played'].sum()
     daily_min = artist_daily / (1000 * 60)
     daily_df = daily_min.reset_index(name='min_played')
     # aggregate 30 days
     daily_df['30d_avg'] = daily_df['min_played'].rolling(30, min_periods=1).mean()

     fig = px.line(daily_df, x='ts_local', y='30d_avg', title=f"Listening for {artist}")
     fig.update_xaxes(title='Date')
     fig.update_yaxes(title='Minutes listened (30 day average)')
     fig.update_traces(line_color='#1db954')

     fig.update_traces(
            hovertemplate=
                "%{x}<br>" + 
                "Minutes: %{y:.0f}"
        )

     return fig



# run
if __name__ == '__main__':
    app.run(debug=True)
