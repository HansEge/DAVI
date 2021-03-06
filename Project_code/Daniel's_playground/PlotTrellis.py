import plotly.express as px
import pandas as pd

import dash
import dash_core_components as dcc
import dash_html_components as html

from dash.dependencies import Input, Output
path_uk = "C:\\Users\\danie\\Desktop\\Skole\\DataVisualization\\Git\\DAVI\\Project_code\\Daniel's_playground\\"
uk_acc = pd.read_csv(path_uk + "clean_UK_Data.csv")

import plotly.express as px
import pandas as pd

import plotly.graph_objects as go
from plotly.subplots import make_subplots

import dash
import dash_core_components as dcc
import dash_html_components as html

from dash.dependencies import Input, Output

px.set_mapbox_access_token("pk.eyJ1IjoiaGFuc2VnZSIsImEiOiJja2dtMmU1cDEycmZjMnlzMXoyeGtlN3E2In0.I2uGd7CT-xoOOdDEAFoyew")
mapbox_access_token = "pk.eyJ1IjoiaGFuc2VnZSIsImEiOiJja2dtMmU1cDEycmZjMnlzMXoyeGtlN3E2In0.I2uGd7CT-xoOOdDEAFoyew"

path_uk = "C:\\Users\\danie\\Desktop\\Skole\\DataVisualization\\Git\\DAVI\\Project_code\\Daniel's_playground\\"
uk_acc = pd.read_csv(path_uk + "UK_Cleaned_Data.csv")
path_us = "C:\\Users\\stinu\\Desktop\\DAVI\\Data\\US_car_accidents\\CleanedFilesUS\\"

us_acc = pd.read_csv(path_us + "US_cleaned.CSV")

# Convert dec
uk_acc['Car_involved_in_accident'] = uk_acc['Car_involved_in_accident'].astype(str)
uk_acc['Motorcycle_involved_in_accident'] = uk_acc['Motorcycle_involved_in_accident'].astype(str)
uk_acc['Truck_involved_in_accident'] = uk_acc['Truck_involved_in_accident'].astype(str)
uk_acc['Other_vehicle_involved_in_accident'] = uk_acc['Other_vehicle_involved_in_accident'].astype(str)

us_acc['Car_involved_in_accident'] = us_acc['Car_involved_in_accident'].astype(int)
us_acc['Motorcycle_involved_in_accident'] = us_acc['Motorcycle_involved_in_accident'].astype(int)
us_acc['Truck_involved_in_accident'] = us_acc['Truck_involved_in_accident'].astype(int)
us_acc['Other_involved_in_accident'] = us_acc['Other_involved_in_accident'].astype(int)

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

variables = ['Vehicle type', 'Speed Limit', 'Number of cars involed', 'Year']

app.layout = html.Div([
    html.Div([
        html.H3('Map of US'),
        dcc.Graph(id='US_graph', style={'display': 'internal-block'}, figure={}),
        dcc.Dropdown(
            id='US_plot',
            style={'height': '30px', 'width': '900px'},
            options=[{'label': i, 'value': i} for i in variables],
            value=variables,
            multi=True
        ),
    ])
])

def switcher(arg):
    switch = {
        'Vehicle type': ['Car_involved_in_accident', 'Motorcycle_involved_in_accident',
                         'Truck_involved_in_accident', 'Other_involved_in_accident'],
        'Speed Limit': 'Speed Limit',
        'Number of cars involed': 'Number of cars involed',
        'Year': 'Year'
    }
    return switch[arg]


@app.callback(
    Output('US_graph', 'figure'),
    [Input('US_plot', 'value')])
def update_figure(selected_param):

    params = [switcher(i) for i in selected_param]

    fig = make_subplots(
        rows=2, cols=2,
        specs=[[{"type": "mapbox"}, {"type": "mapbox"}],
               [{"type": "mapbox"}, {"type": "mapbox"}]]
    )

    fig.add_trace(
        go.Scattermapbox(
            lat=us_acc.loc[(us_acc[params[0][0]] == 1)]['Latitude'],
            lon=us_acc.loc[(us_acc[params[0][0]] == 1)]['Longitude'],
            mode='markers',
            text=us_acc.loc[(us_acc[params[0][0]] == 1)],
            marker=go.scattermapbox.Marker(
                size=4,
                color=us_acc.loc[(us_acc[params[0][0]] == 1)][selected_param[3]]
            )),
        row=1, col=1
    )
    fig.add_trace(
        go.Scattermapbox(
            lat=us_acc.loc[us_acc['Motorcycle_involved_in_accident'] == 1]['Latitude'],
            lon=us_acc.loc[us_acc['Motorcycle_involved_in_accident'] == 1]['Longitude'],
            mode='markers',
            marker=go.scattermapbox.Marker(
                size=4,
                color=us_acc.loc[us_acc['Motorcycle_involved_in_accident'] == 1]['Speed Limit']
            )),
        row=1,
        col=2
    )
    fig.update_layout(
        autosize=False,
        hovermode='closest',
        title_text="Stacked Subplots"
    )
    fig.update_mapboxes(
        bearing=0,
        accesstoken=mapbox_access_token,
        center=dict(
            lat=38,
            lon=-97
        ),
        pitch=0,
        zoom=3
    )

    fig.update_yaxes()
    fig.update_xaxes()
    fig.update_layout(transition_duration=500)

    return fig

app.run_server(debug=True, use_reloader=False)
