import pandas as pd
import plotly.express as px

import dash
import dash_core_components as dcc
import dash_html_components as html

from dash.dependencies import Input, Output


px.set_mapbox_access_token("pk.eyJ1IjoiaGFuc2VnZSIsImEiOiJja2dtMmU1cDEycmZjMnlzMXoyeGtlN3E2In0.I2uGd7CT-xoOOdDEAFoyew")

# Bærbar
'''
path_uk = "C:\\Users\\stinu\\OneDrive\\Desktop\\Computerteknologi\\DAVI\\Datasets\\UK_car_accidents\\"
path_us = "C:\\Users\\stinu\\OneDrive\\Desktop\\Computerteknologi\\DAVI\\Datasets\\US_new\\2015\\"
'''

# Stationær
path_uk = "C:\\Users\\stinu\\Desktop\\DAVI\Data\\UK_car_accidents\\"
path_us = "C:\\Users\\stinu\\Desktop\\DAVI\\Data\\US_car_accidents\\CleanedFilesUS\\"


# Daniel path
'''
path_us = "C:\\Users\\danie\\Desktop\\Skole\\DataVisualization\\project_data\\US_car_accidents\\2015\\"
path_uk = "C:\\Users\\danie\\Desktop\\Skole\\DataVisualization\\project_data\\UK_car_accidents\\"
'''
# path_uk = "C:\\Users\\danie\\Desktop\\Skole\\DataVisualization\\Git\\DAVI\\Project_code\\Daniel's_playground\\"


uk_acc = pd.read_csv(path_uk + "clean_UK_Data.csv")
us_acc = pd.read_csv(path_us + "US_cleaned.CSV")

# Dash stuff
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# Convert dec
uk_acc['Car_involved_in_accident'] = uk_acc['Car_involved_in_accident'].astype(str)
uk_acc['Motorcycle_involved_in_accident'] = uk_acc['Motorcycle_involved_in_accident'].astype(str)
uk_acc['Truck_involved_in_accident'] = uk_acc['Truck_involved_in_accident'].astype(str)
uk_acc['Other_vehicle_involved_in_accident'] = uk_acc['Other_vehicle_involved_in_accident'].astype(str)

us_acc['Car_involved_in_accident'] = us_acc['Car_involved_in_accident'].astype(str)
us_acc['Motorcycle_involved_in_accident'] = us_acc['Motorcycle_involved_in_accident'].astype(str)
us_acc['Truck_involved_in_accident'] = us_acc['Truck_involved_in_accident'].astype(str)
us_acc['Other_involved_in_accident'] = us_acc['Other_involved_in_accident'].astype(str)


app.layout = html.Div([
    html.Div([

        html.H3('Map of United Kingdom'),
        dcc.Graph(id='UK_graph', style={'display': 'internal-block'}),
        dcc.Dropdown(
            id='UK_plot',
            style={'height': '30px', 'width': '900px'},
            options=[
                {'label': "Speed Limit", 'value': 'Speed_limit'},
                {'label': "Car involved in accident", 'value': 'Car_involved_in_accident'},
                {'label': "Motorcycle involved in accident", 'value': 'Motorcycle_involved_in_accident'},
                {'label': "Truck involved in accident", 'value': 'Truck_involved_in_accident'},
                {'label': "Other type of vehicle involved in accident", 'value': 'Other_vehicle_involved_in_accident'}
            ],
            value='Car_involved_in_accident')
        ]),


    html.Div([
        html.Div([
            html.H3('Map of United States of America'),
            dcc.Graph(id='US_graph', style={'display': 'internal-block'}),
            dcc.Dropdown(
                id='US_plot',
                style={'height': '30px', 'width': '900px'},
                options=[
                    {'label': "Speed Limit", 'value': 'Speed Limit'},
                    {'label': "Car involved in accident", 'value': 'Car_involved_in_accident'},
                    {'label': "Motorcycle involved in accident", 'value': 'Motorcycle_involved_in_accident'},
                    {'label': "Truck involved in accident", 'value': 'Truck_involved_in_accident'},
                    {'label': "Other type of vehicle involved in accident", 'value': 'Other_vehicle_involved_in_accident'}
                ],
                value='Car_involved_in_accident')
            ]),
        ]),
    ])


@app.callback(
    Output('UK_graph', 'figure'),
    [Input('UK_plot', 'value')])
def update_figure(selected_param):

    filtered_df = uk_acc[selected_param]

    fig_uk = px.scatter_mapbox(uk_acc,
                               lat=uk_acc["Latitude"],
                               lon=uk_acc["Longitude"],
                               color=filtered_df,
                               color_continuous_scale= px.colors.sequential.Viridis,
                               color_discrete_sequence= px.colors.qualitative.G10,
                               width=1000,
                               height=900,
                               zoom= 5,
                               center= dict(lat=54.832621, lon=-4.577778)
                               )

    fig_uk.update_yaxes()
    fig_uk.update_xaxes()
    fig_uk.update_layout(transition_duration=500)

    return fig_uk

@app.callback(
    Output('US_graph', 'figure'),
    [Input('US_plot', 'value')])
def update_figure(selected_param):

    filtered_df = us_acc[selected_param]

    fig_us = px.scatter_mapbox(us_acc,
                               lat=us_acc["Latitude"],
                               lon=us_acc["Longitude"],
                               color=filtered_df,
                               color_continuous_scale= px.colors.sequential.Viridis,
                               color_discrete_sequence= px.colors.qualitative.G10,
                               width=1000,
                               height=900,
                               zoom= 3,
                               center= dict(lat=34.17189722, lon=-87.42448889)
                               )

    fig_us.update_yaxes()
    fig_us.update_xaxes()
    fig_us.update_layout(transition_duration=500)

    return fig_us


app.run_server(debug=True)