import plotly.express as px
import pandas as pd

import plotly.graph_objects as go
from plotly.subplots import make_subplots

import dash
import dash_core_components as dcc
import dash_html_components as html

from dash.dependencies import Input, Output, State

px.set_mapbox_access_token("pk.eyJ1IjoiaGFuc2VnZSIsImEiOiJja2dtMmU1cDEycmZjMnlzMXoyeGtlN3E2In0.I2uGd7CT-xoOOdDEAFoyew")
mapbox_access_token = "pk.eyJ1IjoiaGFuc2VnZSIsImEiOiJja2dtMmU1cDEycmZjMnlzMXoyeGtlN3E2In0.I2uGd7CT-xoOOdDEAFoyew"

# Daniels path
# path_uk = "C:\\Users\\danie\\Desktop\\Skole\\DataVisualization\\project_data\\Cleaned_data\\"
# path_us = "C:\\Users\\danie\\Desktop\\Skole\\DataVisualization\\project_data\\Cleaned_data\\"

# Stinus path
path_uk = "C:\\Users\\stinu\\Desktop\\DAVI\\GIT\\DAVI\\Project_code\\Cleaned_data\\"
path_us = "C:\\Users\\stinu\\Desktop\\DAVI\\GIT\\DAVI\\Project_code\\Cleaned_data\\"

# uk_acc = pd.read_csv(path_uk + "clean_UK_Data.csv")
uk_acc = pd.read_csv(path_uk + "UK_cleaned.csv")
us_acc = pd.read_csv(path_us + "US_cleaned.CSV")

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

variables = ['Speed Limit', 'Quarter', 'Time of day']

color_var = ['Car involved in accident', 'Motorcycle involved in accident', 'Truck involved in accident',
             'Other vehicle involved in accident']

# center coords and zoom level
uk_center_coords = [54.832621, -4.577778, 3.5]
us_center_coords = [38, -97, 2]

datasets = [uk_acc, us_acc]
datasets_str = ['UK', 'US']

str_quarter_titles = ['First quarter', 'Second Quarter', 'Third quarter', 'Fourth quarter']
str_T_day_titles = ['10pm - 5am', '6am - 1pm', '2pm - 9pm']
str_speed_limit_titles = ['0mph - 35mph', '36mph - 59mph', '60mph - 100mph']

app.layout = html.Div(
    [
        html.Div(
            [
                html.H6('Pick which dataset to load'),
                dcc.Dropdown(
                    id='dataset',
                    options=[{'label': i, 'value': i} for i in datasets_str],
                    placeholder='Pick one',
                    value=datasets_str[0],
                    style=dict(width='40%', verticalAlign="middle")
                )
            ]
        ),
        html.Div(
            [
                dcc.Graph(id='US_graph', style={'display': 'internal-block'}, figure={})
            ]
        ),

        html.Div(
            [
                dcc.Dropdown(
                    id='US_plot_x',
                    options=[{'label': i, 'value': i} for i in variables],
                    placeholder='Pick one',
                    value=variables[0],
                    style=dict(width='40%',
                               verticalAlign="middle")
                )
            ],
            style=dict(display='flex')
        ),

        html.Div(
            [
                dcc.Dropdown(
                    id='US_plot_y',
                    options=[{'label': i, 'value': i} for i in variables],
                    placeholder='Pick one',
                    value=variables[1],
                    style=dict(width='40%',
                               display='inline-block',
                               verticalAlign="middle")
                )
            ],
            style=dict(display='flex')
        ),
        html.Div(
            [
                dcc.Dropdown(
                    id='US_color',
                    options=[{'label': i, 'value': i} for i in color_var],
                    placeholder='Pick one',
                    value=color_var[0],
                    style=dict(width='40%',
                               display='inline-block',
                               verticalAlign="middle")
                )
            ],
            style=dict(display='flex')
        ),
        html.Div(
            [
                dcc.RangeSlider(
                    id='year-range-slider',
                    min=2005,
                    max=2014,
                    step=1,
                    value=[2005, 2006],
                    tooltip=(dict(placement='bottom')),
                    marks={2005: '2005',
                           2014: '2014'}

                ),
                html.Div(id='output-container-range-slider')
            ]
        )
    ],
)


def switcher(arg):
    switch = {
        'Quarter': ['Quarter', str_quarter_titles],
        'Speed Limit': ['Speed_limit', str_speed_limit_titles],
        'Time of day': ['T_day', str_T_day_titles],
        'Number of vehicles in accident': 'Num_veh_acc',
        'Year': 'Year',
        'Motorcycle_involved_in_accident': 'Mc_acc',
        'Car involved in accident': 'Car_acc',
        'Motorcycle involved in accident': 'Mc_acc',
        'Truck involved in accident': 'Truck_acc',
        'Other vehicle involved in accident': 'Other_acc',
        'UK': [datasets[0], uk_center_coords],
        'US': [datasets[1], us_center_coords]
    }
    return switch[arg]


@app.callback(
    Output('US_graph', 'figure'),
    [Input('US_plot_x', 'value'),
     Input('US_plot_y', 'value'),
     Input('year-range-slider', 'value'),
     Input('US_color', 'value'),
     Input('dataset', 'value')])
def update_figure(us_plot_x, us_plot_y, years_slider, us_color, dataset):
    x_params = switcher(us_plot_x)
    y_params = switcher(us_plot_y)
    years = years_slider
    us_color = switcher(us_color)
    data = switcher(dataset)[0]
    center_coords = switcher(dataset)[1]

    # dynamically estimate number of columns
    n_columns = len(set(data[x_params[0]]))

    # dynamically estimate number of rows
    n_rows = len(set(data[y_params[0]]))
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
        specs=specs_matrix,
        horizontal_spacing=0.01,
        vertical_spacing=0.01,
        column_titles=x_params[1],
        row_titles=y_params[1],
        shared_xaxes='rows'
    )

    for i in range(n_rows):
        for k in range(n_columns):
            fig.add_trace(
                go.Scattermapbox(
                    lat=data.loc[((data[y_params[0]] == i) &
                                  (data[x_params[0]] == k) &
                                  ((data['Year'] >= min(years)) &
                                   (data['Year'] <= max(years)))
                                  )]['Lat'],
                    lon=data.loc[((data[y_params[0]] == i) &
                                  (data[x_params[0]] == k) &
                                  ((data['Year'] >= min(years)) &
                                   (data['Year'] <= max(years)))
                                  )]['Lon'],
                    mode='markers',
                    text=data['Num_veh_acc'],
                    marker=go.scattermapbox.Marker(
                        size=data["Num_veh_acc"] + 2,
                        colorscale=[[0, 'rgb(228,26,28)'], [1, 'rgb(55,126,184)']],
                        color=data[us_color]
                    )),
                row=i + 1, col=k + 1
            )
    # Set size of plots in pixels
    fig.layout.height = 1200
    fig.layout.width = 1200

    fig.update_layout(
        autosize=False,
        hovermode='closest',
        title_text="Stacked Subplots"
    )
    fig.update_mapboxes(
        bearing=0,
        accesstoken=mapbox_access_token,
        center=dict(
            lat=center_coords[0],
            lon=center_coords[1]
        ),
        pitch=0,
        zoom=center_coords[2]
    )

    fig.update_yaxes()
    fig.update_xaxes()
    fig.update_layout(transition_duration=500)

    return fig


app.run_server(debug=True)
