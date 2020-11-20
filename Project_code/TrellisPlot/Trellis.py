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

# Daniels path
# path_uk = "C:\\Users\\danie\\Desktop\\Skole\\DataVisualization\\project_data\\Cleaned_data\\"
# path_us = "C:\\Users\\danie\\Desktop\\Skole\\DataVisualization\\project_data\\Cleaned_data\\"

# Stinus path
path_uk = "C:\\Users\\stinu\\Desktop\\DAVI\\GIT\\DAVI\\Project_code\\Cleaned_data\\"
path_us = "C:\\Users\\stinu\\Desktop\\DAVI\\GIT\\DAVI\\Project_code\\Cleaned_data\\"


#uk_acc = pd.read_csv(path_uk + "clean_UK_Data.csv")
uk_acc = pd.read_csv(path_uk + "UK_cleaned.csv")
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

variables = ['Vehicle type', 'Speed Limit', 'Number of vehicles in accident', 'Year', 'Motorcycle_involved_in_accident']

app.layout = html.Div([
    html.Div([
        html.H3('Map of US'),
        dcc.Graph(id='US_graph', style={'display': 'internal-block'}, figure={})
    ]),
    html.Div([
        dcc.Dropdown(
            id='US_plot_x',
            style={'height': '30px', 'width': '900px'},
            options=[{'label': i, 'value': i} for i in variables],
            placeholder='Pick one',
            value=variables[4]

        ),
        dcc.Dropdown(
            id='US_plot_y',
            style={'height': '30px', 'width': '900px'},
            options=[{'label': i, 'value': i} for i in variables],
            placeholder='Pick one',
            value=variables[3]
        ),
    ],
    style={'width': '48%', 'display': 'inline-block'})
])


def switcher(arg):
    switch = {
        'Vehicle type': ['Car_involved_in_accident', 'Motorcycle_involved_in_accident',
                         'Truck_involved_in_accident', 'Other_involved_in_accident'],
        'Speed Limit': 'Speed Limit',
        'Number of vehicles in accident': 'Number of vehicles in accident',
        'Year': 'Year',
        'Motorcycle_involved_in_accident': 'Motorcycle_involved_in_accident'
    }
    return switch[arg]


@app.callback(
    Output('US_graph', 'figure'),
    [Input('US_plot_x', 'value'),
     Input('US_plot_y', 'value')])
def update_figure(us_plot_x, us_plot_y):

    x_params = switcher(us_plot_x)
    y_params = switcher(us_plot_y)

    if len(x_params) != 1 or len(y_params) != 1:
        # Todo: code condition to handle vehicle type and other stuff
        pass

    # dynamically estimate number of columns
    n_columns = len(set(us_acc[x_params]))

    # dynamically estimate number of rows
    n_rows = len(set(us_acc[y_params]))
    # number_of_values = Counter(us_acc[params[0]]).values()

    # make specs_matrix in right dimensions
    specs_matrix = []
    for x in range(n_rows):
        innerlist = []
        for y in range(n_columns):
            innerlist.append({"type": "mapbox"})
        specs_matrix.append(innerlist)

    fig = make_subplots(
        rows=n_rows, cols=n_columns,
        specs=specs_matrix
    )

    for i in range(n_rows):
        for k in range(n_columns):

            fig.add_trace(
                go.Scattermapbox(
                    lat=us_acc.loc[((us_acc[y_params] == 2005+i) & (us_acc[x_params] == k))]['Latitude'],
                    lon=us_acc.loc[((us_acc[y_params] == 2005+i) & (us_acc[x_params] == k))]['Longitude'],
                    mode='markers',
                    # text=us_acc.loc[(us_acc[x_params] == 1)],
                    marker=go.scattermapbox.Marker(
                        size=4,
                    )),
                row=i+1, col=k+1
            )


    # Set size of plots in pixels
    fig.layout.height=1200
    fig.layout.width=1200

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
