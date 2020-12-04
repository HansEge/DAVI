import plotly.express as px
import pandas as pd
import numpy as np

import plotly.graph_objects as go
from plotly.subplots import make_subplots

import dash
import dash_core_components as dcc
import dash_html_components as html

from dash.dependencies import Input, Output

px.set_mapbox_access_token("pk.eyJ1IjoiaGFuc2VnZSIsImEiOiJja2dtMmU1cDEycmZjMnlzMXoyeGtlN3E2In0.I2uGd7CT-xoOOdDEAFoyew")
mapbox_access_token = "pk.eyJ1IjoiaGFuc2VnZSIsImEiOiJja2dtMmU1cDEycmZjMnlzMXoyeGtlN3E2In0.I2uGd7CT-xoOOdDEAFoyew"

# Daniels path
path_uk = "C:\\Users\\danie\\Desktop\\Skole\\DataVisualization\\Git\\DAVI\\Project_code\\Cleaned_data\\"
# path_us = "C:\\Users\\danie\\Desktop\\Skole\\DataVisualization\\project_data\\Cleaned_data\\"

# Stinus path
#path_uk = "C:\\Users\\stinu\\Desktop\\DAVI\Data\\UK_car_accidents\\"
#path_us = "C:\\Users\\stinu\\Desktop\\DAVI\\Data\\US_car_accidents\\CleanedFilesUS\\"

#uk_acc = pd.read_csv(path_uk + "clean_UK_Data.csv")
uk_acc = pd.read_csv(path_uk + "UK_cleaned.csv")
#us_acc = pd.read_csv(path_us + "US_cleaned.CSV")

# Convert dec
'''
uk_acc['Car_involved_in_accident'] = uk_acc['Car_involved_in_accident'].astype(str)
uk_acc['Motorcycle_involved_in_accident'] = uk_acc['Motorcycle_involved_in_accident'].astype(str)
uk_acc['Truck_involved_in_accident'] = uk_acc['Truck_involved_in_accident'].astype(str)
uk_acc['Other_vehicle_involved_in_accident'] = uk_acc['Other_vehicle_involved_in_accident'].astype(str)

us_acc['Car_involved_in_accident'] = us_acc['Car_involved_in_accident'].astype(int)
us_acc['Motorcycle_involved_in_accident'] = us_acc['Motorcycle_involved_in_accident'].astype(int)
us_acc['Truck_involved_in_accident'] = us_acc['Truck_involved_in_accident'].astype(int)
us_acc['Other_involved_in_accident'] = us_acc['Other_involved_in_accident'].astype(int)
'''


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

variables = ['Quarter', 'Time of day', 'Speed Limit']
color_var = ['Car involved in accident', 'Motorcycle involved in accident', 'Truck involved in accident',
             'Other vehicle involved in accident']

str_quarter_titles = ['First quarter', 'Second Quarter', 'Third quarter', 'Fourth quarter']
str_T_day_titles = ['10pm - 5am', '6am - 1pm', '2pm - 9pm']
str_speed_limit_titles = ['0mph - 35mph', '36mph - 59mph', '60mph - 100mph']


app.layout = html.Div(children=[
    html.Div([
        html.H3('Map of UK'),
        dcc.Graph(id='UK_graph', style={'display': 'internal-block'}, figure={})
    ]),
    html.P('''Pick the parameter that determines the columns in the trellis-plot'''),
    html.Div(
        [
            dcc.Dropdown(
                id='UK_plot_x',
                options=[{'label': i, 'value': i} for i in variables],
                placeholder='Pick one',
                value=variables[1],
                style=dict(width='40%',
                           verticalAlign="middle")
            )
        ],
        style=dict(display='flex')
    ),
    html.P('''Pick the parameter that determines the rows of the trellis-plot'''),
    html.Div(
        [
            dcc.Dropdown(
                id='UK_plot_y',
                options=[{'label': i, 'value': i} for i in variables],
                placeholder='Pick one',
                value=variables[2],
                style=dict(width='40%',
                           display='inline-block',
                           verticalAlign="middle")
            )
        ],
        style=dict(display='flex')
    ),
    html.P('''Pick the vehicle type to focus on (the accidents with that involve the type of vehicle will be colored red'''),
    html.Div(
        [
            dcc.Dropdown(
                id='UK_color',
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
])


def switcher(arg):
    switch = {
        'Quarter': ['Quarter', str_quarter_titles],
        'Speed Limit': ['Speed_limit', str_speed_limit_titles],
        'Time of day': ['T_day', str_T_day_titles],
        'Car involved in accident': 'Car_acc',
        'Motorcycle involved in accident': 'Mc_acc',
        'Truck involved in accident': 'Truck_acc',
        'Other vehicle involved in accident': 'Other_acc'
    }
    return switch[arg]


@app.callback(
    Output('UK_graph', 'figure'),
    [Input('UK_plot_x', 'value'),
     Input('UK_plot_y', 'value'),
     Input('UK_color', 'value'),
     Input('year-range-slider', 'value')])
def update_figure(uk_plot_x, uk_plot_y, uk_color, years_slider):
    x_params = switcher(uk_plot_x)
    y_params = switcher(uk_plot_y)
    years = years_slider
    uk_color = switcher(uk_color)

    if len(x_params[0]) != 1 or len(y_params[0]) != 1:
        # Todo: code condition to handle vehicle type
        pass

    # dynamically estimate number of columns
    n_columns = len(set(uk_acc[x_params[0]]))

    # dynamically estimate number of rows
    n_rows = len(set(uk_acc[y_params[0]]))
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
        shared_xaxes=False,
        shared_yaxes=True,
        horizontal_spacing=0.01,
        vertical_spacing=0.01,
        column_titles=x_params[1],
        row_titles=y_params[1]
    )


    for i in range(n_rows):
        for k in range(n_columns):

            if (i == 0) and (k == 0):

                fig.add_trace(

                    # https://plotly.com/python-api-reference/generated/plotly.graph_objects.Scattermapbox.html
                    go.Scattermapbox(

                        lat=uk_acc.loc[((uk_acc[y_params[0]] == i) &
                                        (uk_acc[x_params[0]] == k) &
                                        (uk_acc[uk_color] == 0) &
                                        ((uk_acc['Year'] >= min(years)) &
                                        (uk_acc['Year'] <= max(years)))
                                        )]['Lat'],
                        lon=uk_acc.loc[((uk_acc[y_params[0]] == i) &
                                        (uk_acc[x_params[0]] == k) &
                                        (uk_acc[uk_color] == 0) &
                                        ((uk_acc['Year'] >= min(years)) &
                                        (uk_acc['Year'] <= max(years)))
                                        )]['Lon'],
                        legendgroup="Group1",
                        name="Gray",
                        mode='markers',
                        text=uk_acc["Num_veh_acc"],
                        hovertemplate="Latitude: %{lat}<br>" +
                                      "Longitude: %{lon}<br>" +
                                      "Number of vehicles in accident: %{text}<br>" +
                                      "Color: %{'rgb(120,120,120)'}",
                        hoverlabel=go.scattermapbox.Hoverlabel(
                            bgcolor='gold'
                        ),
                        marker=go.scattermapbox.Marker(
                            size=uk_acc["Num_veh_acc"]+2,
                            color='rgb(120,120,120)'
                        )),
                    row=i+1, col=k+1
                )

                fig.add_trace(

                    # https://plotly.com/python-api-reference/generated/plotly.graph_objects.Scattermapbox.html
                    go.Scattermapbox(

                        lat=uk_acc.loc[((uk_acc[y_params[0]] == i) &
                                        (uk_acc[x_params[0]] == k) &
                                        (uk_acc[uk_color] == 1) &
                                        ((uk_acc['Year'] >= min(years)) &
                                         (uk_acc['Year'] <= max(years)))
                                        )]['Lat'],
                        lon=uk_acc.loc[((uk_acc[y_params[0]] == i) &
                                        (uk_acc[x_params[0]] == k) &
                                        (uk_acc[uk_color] == 1) &
                                        ((uk_acc['Year'] >= min(years)) &
                                         (uk_acc['Year'] <= max(years)))
                                        )]['Lon'],
                        mode='markers',
                        name="Red",
                        showlegend=True,
                        legendgroup="Group2",
                        hoverlabel=go.scattermapbox.Hoverlabel(
                            bgcolor='rgb(0,0,0)'
                        ),
                        text=uk_acc["Num_veh_acc"],
                        hovertemplate="Latitude: %{lat}<br>" +
                                      "Longitude: %{lon}<br>" +
                                      "Number of vehicles in accident: %{text}",
                        # text=us_acc.loc[(us_acc[x_params] == 1)],
                        marker=go.scattermapbox.Marker(
                            size=uk_acc["Num_veh_acc"] + 2,
                            color='rgb(255,0,0)'
                        )),
                    row=i + 1, col=k + 1
                )
            else:
                fig.add_trace(

                    # https://plotly.com/python-api-reference/generated/plotly.graph_objects.Scattermapbox.html
                    go.Scattermapbox(

                        lat=uk_acc.loc[((uk_acc[y_params[0]] == i) &
                                        (uk_acc[x_params[0]] == k) &
                                        (uk_acc[uk_color] == 0) &
                                        ((uk_acc['Year'] >= min(years)) &
                                         (uk_acc['Year'] <= max(years)))
                                        )]['Lat'],
                        lon=uk_acc.loc[((uk_acc[y_params[0]] == i) &
                                        (uk_acc[x_params[0]] == k) &
                                        (uk_acc[uk_color] == 0) &
                                        ((uk_acc['Year'] >= min(years)) &
                                         (uk_acc['Year'] <= max(years)))
                                        )]['Lon'],
                        legendgroup="Group1",
                        showlegend=False,
                        name="Gray",
                        mode='markers',
                        text=uk_acc["Num_veh_acc"],
                        hovertemplate="Latitude: %{lat}<br>" +
                                      "Longitude: %{lon}<br>" +
                                      "Number of vehicles in accident: %{text}<br>" +
                                      "Color: %{marker.color}",
                        hoverlabel=go.scattermapbox.Hoverlabel(
                            bgcolor='gold'
                        ),
                        # text=us_acc.loc[(us_acc[x_params] == 1)],
                        marker=go.scattermapbox.Marker(
                            size=uk_acc["Num_veh_acc"] + 2,
                            color='rgb(120,120,120)'
                        )),
                    row=i + 1, col=k + 1
                )

                fig.add_trace(

                    # https://plotly.com/python-api-reference/generated/plotly.graph_objects.Scattermapbox.html
                    go.Scattermapbox(

                        lat=uk_acc.loc[((uk_acc[y_params[0]] == i) &
                                        (uk_acc[x_params[0]] == k) &
                                        (uk_acc[uk_color] == 1) &
                                        ((uk_acc['Year'] >= min(years)) &
                                         (uk_acc['Year'] <= max(years)))
                                        )]['Lat'],
                        lon=uk_acc.loc[((uk_acc[y_params[0]] == i) &
                                        (uk_acc[x_params[0]] == k) &
                                        (uk_acc[uk_color] == 1) &
                                        ((uk_acc['Year'] >= min(years)) &
                                         (uk_acc['Year'] <= max(years)))
                                        )]['Lon'],
                        mode='markers',
                        name="Red",
                        showlegend=False,
                        legendgroup="Group2",
                        hoverlabel=go.scattermapbox.Hoverlabel(
                            bgcolor='rgb(0,0,0)'
                        ),
                        text=uk_acc["Num_veh_acc"],
                        hovertemplate="Latitude: %{lat}<br>" +
                                      "Longitude: %{lon}<br>" +
                                      "Number of vehicles in accident: %{text}",
                        # text=us_acc.loc[(us_acc[x_params] == 1)],
                        marker=go.scattermapbox.Marker(
                            size=uk_acc["Num_veh_acc"] + 2,
                            color='rgb(255,0,0)'
                        )),
                    row=i + 1, col=k + 1
                )







    # Set size of plots in pixels
    fig.layout.height=1500
    fig.layout.width=1900

    fig.update_layout(
        autosize=False,
        hovermode='closest',
        title_text="Stacked Subplots",
        hoverlabel=go.scattermapbox.Hoverlabel(
            bgcolor='rgb(0,0,0)'
        )
    )
    fig.update_mapboxes(
        bearing=0,
        accesstoken=mapbox_access_token,
        center=dict(
            lat=54.832621,
            lon=-4.577778
        ),
        pitch=0,
        zoom=4
    )

    fig.update_yaxes()
    fig.update_xaxes()
    fig.update_layout(transition_duration=500)


    return fig

app.run_server(debug=True, use_reloader=False)



'''customdata=pd.concat([uk_acc.loc[((uk_acc[y_params[0]] == i) &
                                    (uk_acc[x_params[0]] == k) &
                                    ((uk_acc['Year'] >= min(years)) &
                                    (uk_acc['Year'] <= max(years)))
                                    )]['Num_veh_acc'],
                                    uk_acc.loc[((uk_acc[y_params[0]] == i) &
                                    (uk_acc[x_params[0]] == k) &
                                    ((uk_acc['Year'] >= min(years)) &
                                    (uk_acc['Year'] <= max(years)))
                                    )]['Car_acc']], axis=1),
                    '''










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
                    style=dict(width='70%', display='inline-block', verticalAlign="middle")
                    ),

                html.P('Pick the parameter that determines the columns in the trellis-plot', className="card-text"),
                dcc.Dropdown(
                    id='US_plot_x',
                    options=[{'label': i, 'value': i} for i in variables],
                    placeholder='Pick one',
                    value=variables[0],
                    style=dict(width='70%', display='inline-block', verticalAlign="middle")),

                html.P('Pick the parameter that determines the rows in the trellis-plot', className="card-text"),
                dcc.Dropdown(
                    id='US_plot_y',
                    options=[{'label': i, 'value': i} for i in variables],
                    placeholder='Pick one',
                    value=variables[1],
                    style=dict(width='70%',
                               display='inline-block',
                               verticalAlign="middle")),

                html.P('Pick the parameter that determines the rows in the trellis-plot', className="card-text"),
                dcc.Dropdown(
                    id='US_color',
                    options=[{'label': i, 'value': i} for i in color_var],
                    placeholder='Pick one',
                    value=color_var[0],
                    style=dict(width='70%',
                               display='inline-block',
                               verticalAlign="middle")),


                html.Div(
                    [
                        html.Button('Toggle size',
                                    id='toggle_btn',
                                    n_clicks=0),
                    ]),

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
        dcc.Graph(id='US_graph', style={'display': 'internal-block'}, figure={})
    ]
)


app.layout = html.Div([
    dbc.Row([dbc.Col(user_options_card, width=3),
             dbc.Col(graph_card, width=9)])])