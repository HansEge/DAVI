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
# path_uk = "C:\\Users\\danie\\Desktop\\Skole\\DataVisualization\\Git\\DAVI\\Project_code\\Cleaned_data\\"
# path_us = "C:\\Users\\danie\\Desktop\\Skole\\DataVisualization\\Git\\DAVI\\Project_code\\Cleaned_data\\"

# Stinus path
path_uk = "C:\\Users\\stinu\\Desktop\\DAVI\\GIT\\DAVI\\Project_code\\Cleaned_data\\"
path_us = "C:\\Users\\stinu\\Desktop\\DAVI\\GIT\\DAVI\\Project_code\\Cleaned_data\\"

# Stinus laptop
# path_uk = 'C:\\Users\\stinu\\OneDrive\\Desktop\\Computerteknologi\\DAVI\\DAVI\\Project_code\\Cleaned_data\\'
# path_us = 'C:\\Users\\stinu\\OneDrive\\Desktop\\Computerteknologi\\DAVI\\DAVI\\Project_code\\Cleaned_data\\'


# uk_acc = pd.read_csv(path_uk + "clean_UK_Data.csv")
uk_acc = pd.read_csv(path_uk + "UK_cleaned.csv")
us_acc = pd.read_csv(path_us + "US_cleaned.CSV")

'''
us_acc = us_acc.astype({'Num_veh_acc': 'int32',
                     'Car_acc': 'int32',
                     'Mc_acc': 'int32',
                     'Truck_acc': 'int32',
                     'Year': 'int32',
                     'Quarter': 'int32',
                     'T_day': 'int32',
                     'Speed_limit': 'int32'})
'''
uk_histo = pd.read_csv(path_uk + "UK_cleaned_histo.csv")
us_histo = pd.read_csv(path_uk + "US_cleaned_histo.csv")

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.SANDSTONE])

variables = ['Speed Limit', 'Quarter', 'Time of day']
variables_histo = ['Speed Limit', 'Quarter', 'Time of day', 'Year']

color_var = ['Car involved in accident', 'Motorcycle involved in accident', 'Truck involved in accident',
             'All vehicle types']

# center coords and zoom level
uk_center_coords = [54.832621, -4.577778, 3.5]
us_center_coords = [38, -97, 2]

# Used to load different datasets
datasets = [uk_acc, us_acc]
datasets_str = ['UK', 'US']

current_dataset = 'UK'
current_coords = {
    'lat': uk_center_coords[0],
    'lon': uk_center_coords[1],
    'zoom': uk_center_coords[2]
}

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
                    style=dict(width='70%', display='inline-block', verticalAlign="middle", marginBottom='2em')
                ),

                html.P('Pick the parameter that determines the columns in the trellis-plot', className="card-text"),
                dcc.Dropdown(
                    id='US_plot_x',
                    options=[{'label': i, 'value': i} for i in variables],
                    placeholder='Pick one',
                    value=variables[0],
                    style=dict(width='70%', display='inline-block', verticalAlign="middle", marginBottom='2em')),

                html.P('Pick the parameter that determines the rows in the trellis-plot', className="card-text"),
                dcc.Dropdown(
                    id='US_plot_y',
                    options=[{'label': i, 'value': i} for i in variables],
                    placeholder='Pick one',
                    value=variables[1],
                    style=dict(width='70%',
                               display='inline-block',
                               verticalAlign="middle",
                               marginBottom='2em')),

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
                        marginBottom='2em')
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
histo_option_card = dbc.Card(
    [
        html.P('Pick a parameter for the x-axis', className="card-text"),
        dcc.Dropdown(
            id='histo_x',
            options=[{'label': i, 'value': i} for i in variables_histo],
            placeholder='Pick one',
            value=variables_histo[3],
            style=dict(width='70%',
                       display='inline-block',
                       verticalAlign="middle",
                       marginBottom='2em'))
    ]
)

graph_card = dbc.Card(
    [
        dcc.Graph(id='US_graph', style={'display': 'internal-block'}, figure={})
    ]
)

histo_card = dbc.Card(
    [
        dcc.Graph(id='histogram', style={'display': 'internal-block'}, figure={})
    ]
)

app.layout = html.Div([
    dbc.Row([dbc.Col(user_options_card, width=3),
             dbc.Col(graph_card, width=9)]
            ),
    dbc.Row([dbc.Col(histo_option_card, width=3),
             dbc.Col(histo_card, width=9)])
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
        'UK': [datasets[0], uk_center_coords, uk_histo],
        'US': [datasets[1], us_center_coords, us_histo]
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
def update_figure(us_plot_x, us_plot_y, years, us_color, dataset, toggle, relayout_data):
    x_params = switcher(us_plot_x)
    y_params = switcher(us_plot_y)
    veh_type_str = us_color
    us_color = switcher(us_color)
    data = switcher(dataset)[0]
    start_coords = switcher(dataset)[1]

    # Used for size of dots
    scale = 0.5

    global current_coords
    global current_dataset

    if relayout_data != None:
        if not 'autosize' in relayout_data and not 'dragmode' in relayout_data:
            values_view = relayout_data.values()
            value_iterator = iter(values_view)
            current_coords, zoom_level = next(value_iterator), next(value_iterator)
            current_coords['zoom'] = zoom_level

    # Reset coords and zoom when loading new dataset
    if dataset != current_dataset:
        current_coords = {
            'lat': start_coords[0],
            'lon': start_coords[1],
            'zoom': start_coords[2]
        }
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
        row_titles=y_params[1]
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
                            size=size_param + current_coords['zoom']*scale,
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
                            size=size_param + current_coords['zoom']*scale,
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
                            size=size_param + current_coords['zoom']*scale,
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
                            size=size_param + current_coords['zoom']*scale,
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
            lat=current_coords['lat'],
            lon=current_coords['lon']
        ),
        pitch=0,
        zoom=current_coords['zoom']
    )

    fig.update_yaxes()
    fig.update_xaxes()
    fig.update_layout()

    return fig


def histo_switcher(arg):
    switch = {
        'Speed Limit': 'Speed_limit',
        'Time of day': 'Hour',
        'Quarter': 'Month',
        'Year': 'Year'
    }
    return switch[arg]



@app.callback(
    Output('histogram', 'figure'),
    [Input('US_graph', 'selectedData'),
     Input('dataset', 'value'),
     Input('histo_x', 'value')])
def update_hist(box_select_vals, dataset, param):
    fig = px.histogram()

    if box_select_vals != None:

        filter = histo_switcher(param)
        data = switcher(dataset)[2]
        global current_selected_points

        values_view = box_select_vals.values()
        value_iterator = iter(values_view)
        selected_points = next(value_iterator)

        lat = []
        lon = []

        for i in range(len(selected_points)):
            lat.append(selected_points[i]['lat'])
            lon.append(selected_points[i]['lon'])

        coords = pd.DataFrame({'Lat': lat,
                               'Lon': lon})

        data_list = []

        for k in range(len(coords)):
            data_list.append(data.loc[((data['Lat'] == coords['Lat'][k]) &
                                       (data['Lon'] == coords['Lon'][k]))])

        new_data = pd.concat(data_list, ignore_index=True)

        fig = px.histogram(new_data, x=filter, nbins=len(data[filter].unique()))
        fig.update_layout(bargap=0.2)
        fig.update_xaxes(type='category')

        if filter == 'Hour' and len(new_data) > 0:
            # bins = 0.5*(bins[:-1] + bins[1:])
            fig = px.bar(x=range(new_data['Hour'].unique().shape[0]), y=new_data['Hour'].value_counts().sort_index(),
                         labels={'x':'Time of day [24hr]', 'y':'count'})

        return fig

    return fig


app.run_server(debug=True)
