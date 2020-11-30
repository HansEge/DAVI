import plotly.express as px
import pandas as pd

import plotly.graph_objects as go
from plotly.subplots import make_subplots

import numpy as np

import json

import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_daq as daq

from dash.dependencies import Input, Output, State

px.set_mapbox_access_token("pk.eyJ1IjoiaGFuc2VnZSIsImEiOiJja2dtMmU1cDEycmZjMnlzMXoyeGtlN3E2In0.I2uGd7CT-xoOOdDEAFoyew")
mapbox_access_token = "pk.eyJ1IjoiaGFuc2VnZSIsImEiOiJja2dtMmU1cDEycmZjMnlzMXoyeGtlN3E2In0.I2uGd7CT-xoOOdDEAFoyew"

# Daniels path
path_uk = "C:\\Users\\danie\\Desktop\\Skole\\DataVisualization\\Git\\DAVI\\Project_code\\Cleaned_data\\"
path_us = "C:\\Users\\danie\\Desktop\\Skole\\DataVisualization\\Git\\DAVI\\Project_code\\Cleaned_data\\"

# Stinus path
#path_uk = "C:\\Users\\stinu\\Desktop\\DAVI\\GIT\\DAVI\\Project_code\\Cleaned_data\\"
#path_us = "C:\\Users\\stinu\\Desktop\\DAVI\\GIT\\DAVI\\Project_code\\Cleaned_data\\"

# uk_acc = pd.read_csv(path_uk + "clean_UK_Data.csv")
uk_acc = pd.read_csv(path_uk + "UK_cleaned.csv")
us_acc = pd.read_csv(path_us + "US_cleaned.CSV")
uk_histo = pd.read_csv(path_uk + "UK_cleaned_histo.csv")
us_histo = pd.read_csv(path_uk + "US_cleaned_histo.csv")


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.SANDSTONE])

variables = ['Speed Limit', 'Quarter', 'Time of day']

color_var = ['Car involved in accident', 'Motorcycle involved in accident', 'Truck involved in accident',
             'All vehicle types']

# center coords and zoom level
uk_center_coords = [54.832621, -4.577778, 3.5]
us_center_coords = [38, -97, 2]

# Used to load different datasets
datasets = [uk_acc, us_acc]
datasets_str = ['UK', 'US']

current_dataset = ''

str_quarter_titles = ['First quarter', 'Second Quarter', 'Third quarter', 'Fourth quarter']
str_T_day_titles = ['10pm - 5am', '6am - 1pm', '2pm - 9pm']
str_speed_limit_titles = ['0mph - 35mph', '36mph - 59mph', '60mph - 100mph']

user_options_card = dbc.Card(
    [
        dbc.CardBody(
            [
                html.P('Pick which dataset to load', className="card-text"),
                dcc.Dropdown(
                    id='dataset',
                    options=[{'label': i, 'value': i} for i in datasets_str],
                    placeholder='Pick one',
                    value=datasets_str[0],
                    style=dict(width='70%', display='inline-block', verticalAlign="middle", marginBottom= '2em')
                ),

                html.P('Pick the parameter that determines the columns in the trellis-plot', className="card-text"),
                dcc.Dropdown(
                    id='US_plot_x',
                    options=[{'label': i, 'value': i} for i in variables],
                    placeholder='Pick one',
                    value=variables[0],
                    style=dict(width='70%', display='inline-block', verticalAlign="middle", marginBottom= '2em')),

                html.P('Pick the parameter that determines the rows in the trellis-plot', className="card-text"),
                dcc.Dropdown(
                    id='US_plot_y',
                    options=[{'label': i, 'value': i} for i in variables],
                    placeholder='Pick one',
                    value=variables[1],
                    style=dict(width='70%',
                               display='inline-block',
                               verticalAlign="middle",
                               marginBottom= '2em')),

                html.P('Pick a vehicle type', className="card-text"),
                dcc.Dropdown(
                    id='US_color',
                    options=[{'label': i, 'value': i} for i in color_var],
                    placeholder='Pick one',
                    value=color_var[0],
                    style=dict(
                        width='70%',
                        display='inline-block',
                        verticalAlign="middle",
                        marginBottom= '2em')
                ),

                html.P('Toggle size for number of vehicles in accidents', className="card-text"),
                html.Div(
                    [
                        daq.BooleanSwitch(
                            id='toggle-switch',
                            on=True,
                            color="#a1d99b",
                            style=dict(
                                display='inline-block',
                                verticalAlign='left',
                                marginBottom='5em'
                            )
                        )
                    ]),


                html.P('Select year range', className="card-text"),
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
                    ])
            ]
        )
    ]
)

graph_card = dbc.Card(
    [
        dcc.Graph(id='US_graph', style={'display': 'internal-block'}, figure={}),
        # dcc.Graph(id='histogram', style={'display': 'internal-block'}, figure={})
    ]
)

test_card = dbc.Card(
    [
        # html.Pre(id='lasso', style={'overflowY': 'scroll', 'height': '100vh'})
        dcc.Graph(id='histogram', style={'display': 'internal-block'}, figure={})
    ]
)

app.layout = html.Div([
    dbc.Row([dbc.Col(user_options_card, width=3),
             dbc.Col(graph_card, width=9)]
            ),
    dbc.Row([dbc.Col(test_card, width=12)])
    ]
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
        'All vehicle types': 'All_veh',
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
     Input('dataset', 'value'),
     Input('toggle-switch', 'on'),
     Input('US_graph', 'relayoutData')])
def update_figure(us_plot_x, us_plot_y, years_slider, us_color, dataset, toggle, relayout_data):
    x_params = switcher(us_plot_x)
    y_params = switcher(us_plot_y)
    years = years_slider
    veh_type_str = us_color
    us_color = switcher(us_color)
    data = switcher(dataset)[0]
    start_coords = switcher(dataset)[1]

    # used when program starts
    zoom_level = start_coords[2]
    center_coords = {
        'lat': start_coords[0],
        'lon': start_coords[1]
    }

    if relayout_data != None:
        if not 'autosize' in relayout_data and not 'dragmode' in relayout_data:
            center_coords.clear()
            values_view = relayout_data.values()
            value_iterator = iter(values_view)
            center_coords, zoom_level = next(value_iterator), next(value_iterator)

            # Reset coords and zoom when loading new dataset
            global current_dataset
            if dataset != current_dataset and not 'autosize' in relayout_data:
                center_coords = {
                    'lat': start_coords[0],
                    'lon': start_coords[1]
                }
                zoom_level = start_coords[2]
                current_dataset = dataset

    # Toggle switch stuff
    if toggle:
        size_param = data['Num_veh_acc']
    else:
        size_param = 1

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

            if (i == 0) and (k == 0):
                fig.add_trace(
                    go.Scattermapbox(
                        lat=data.loc[((data[y_params[0]] == i) &
                                      (data[x_params[0]] == k) &
                                      (data[us_color] == 0) &
                                      ((data['Year'] >= min(years)) &
                                       (data['Year'] <= max(years)))
                                      )]['Lat'],
                        lon=data.loc[((data[y_params[0]] == i) &
                                      (data[x_params[0]] == k) &
                                      (data[us_color] == 0) &
                                      ((data['Year'] >= min(years)) &
                                       (data['Year'] <= max(years)))
                                      )]['Lon'],
                        legendgroup="Group1",
                        name="All other vehicle types",
                        mode='markers',
                        hoverlabel=go.scattermapbox.Hoverlabel(
                            bgcolor='rgb(200,200,200)',
                            bordercolor='rgb(0,0,0)',
                            font=dict(family='Overpass')
                        ),
                        hovertemplate="Latitude: %{lat}<br>" +
                                      "Longitude: %{lon}<br>" +
                                      "Number of vehicles in accident: %{text}",
                        text=data['Num_veh_acc'],
                        marker=go.scattermapbox.Marker(
                            size=size_param + 2,
                            color='rgb(120,120,120)'
                        )),
                    row=i + 1, col=k + 1
                )
                fig.add_trace(
                    go.Scattermapbox(
                        lat=data.loc[((data[y_params[0]] == i) &
                                      (data[x_params[0]] == k) &
                                      (data[us_color] == 1) &
                                      ((data['Year'] >= min(years)) &
                                       (data['Year'] <= max(years)))
                                      )]['Lat'],
                        lon=data.loc[((data[y_params[0]] == i) &
                                      (data[x_params[0]] == k) &
                                      (data[us_color] == 1) &
                                      ((data['Year'] >= min(years)) &
                                       (data['Year'] <= max(years)))
                                      )]['Lon'],
                        legendgroup="Group2",
                        name=veh_type_str,
                        mode='markers',
                        hoverlabel=go.scattermapbox.Hoverlabel(
                            bgcolor='rgb(200,200,200)',
                            bordercolor='rgb(0,0,0)',
                            font=dict(family='Overpass')
                        ),
                        hovertemplate="Latitude: %{lat}<br>" +
                                      "Longitude: %{lon}<br>" +
                                      "Number of vehicles in accident: %{text}",
                        text=data['Num_veh_acc'],
                        marker=go.scattermapbox.Marker(
                            size=size_param + 2,
                            color='rgb(255,0,0)'

                        )),
                    row=i + 1, col=k + 1
                )
            else:
                fig.add_trace(
                    go.Scattermapbox(
                        lat=data.loc[((data[y_params[0]] == i) &
                                      (data[x_params[0]] == k) &
                                      (data[us_color] == 0) &
                                      ((data['Year'] >= min(years)) &
                                       (data['Year'] <= max(years)))
                                      )]['Lat'],
                        lon=data.loc[((data[y_params[0]] == i) &
                                      (data[x_params[0]] == k) &
                                      (data[us_color] == 0) &
                                      ((data['Year'] >= min(years)) &
                                       (data['Year'] <= max(years)))
                                      )]['Lon'],
                        legendgroup="Group1",
                        showlegend=False,
                        name="All other vehicle types",
                        mode='markers',
                        hoverlabel=go.scattermapbox.Hoverlabel(
                            bgcolor='rgb(200,200,200)',
                            bordercolor='rgb(0,0,0)',
                            font=dict(family='Overpass')
                        ),
                        hovertemplate="Latitude: %{lat}<br>" +
                                      "Longitude: %{lon}<br>" +
                                      "Number of vehicles in accident: %{text}",
                        text=data['Num_veh_acc'],
                        marker=go.scattermapbox.Marker(
                            size=size_param + 2,
                            color='rgb(120,120,120)'
                        )),
                    row=i + 1, col=k + 1
                )
                fig.add_trace(
                    go.Scattermapbox(
                        lat=data.loc[((data[y_params[0]] == i) &
                                      (data[x_params[0]] == k) &
                                      (data[us_color] == 1) &
                                      ((data['Year'] >= min(years)) &
                                       (data['Year'] <= max(years)))
                                      )]['Lat'],
                        lon=data.loc[((data[y_params[0]] == i) &
                                      (data[x_params[0]] == k) &
                                      (data[us_color] == 1) &
                                      ((data['Year'] >= min(years)) &
                                       (data['Year'] <= max(years)))
                                      )]['Lon'],
                        legendgroup="Group2",
                        showlegend=False,
                        name=veh_type_str,
                        mode='markers',
                        hoverlabel=go.scattermapbox.Hoverlabel(
                            bgcolor='rgb(200,200,200)',
                            bordercolor='rgb(0,0,0)',
                            font=dict(family='Overpass')
                        ),
                        hovertemplate="Latitude: %{lat}<br>" +
                                      "Longitude: %{lon}<br>" +
                                      "Number of vehicles in accident: %{text}",
                        text=data['Num_veh_acc'],
                        marker=go.scattermapbox.Marker(
                            size=size_param + 2,
                            color='rgb(255,0,0)'

                        )),
                    row=i + 1, col=k + 1
                )

    # Set size of plots in pixels
    fig.layout.height = 1200
    fig.layout.width = 1200

    fig.update_layout(
        autosize=False,
        hovermode='closest',
        title_text="Trellis plot"
    )
    fig.update_mapboxes(
        bearing=0,
        accesstoken=mapbox_access_token,
        center=dict(
            lat=center_coords['lat'],
            lon=center_coords['lon']
        ),
        pitch=0,
        zoom=zoom_level
    )

    fig.update_yaxes()
    fig.update_xaxes()
    fig.update_layout(transition_duration=500)

    return fig


@app.callback(
    Output('histogram', 'figure'),
    [Input('US_graph', 'selectedData')])
def update_hist(box_select_vals):

    fig = px.histogram()

    if box_select_vals != None:

        values_view = box_select_vals.values()
        value_iterator = iter(values_view)
        selected_points = next(value_iterator)

        lat = []
        lon = []

        for i in range(len(selected_points)):
            lat.append(selected_points[i]['lat'])
            lon.append(selected_points[i]['lon'])

        coords = pd.DataFrame({'lat': lat,
                               'lon': lon})

        fig = px.histogram(uk_histo, x=uk_histo.loc[
            ((uk_histo['lat'] == coords['lat']) &
             (uk_histo['lon'] == coords['lon']))])

        return fig

    return fig





app.run_server(debug=True)
