import pandas as pd
import plotly.express as px

import dash
import dash_core_components as dcc
import dash_html_components as html

from dash.dependencies import Input, Output


px.set_mapbox_access_token("pk.eyJ1IjoiaGFuc2VnZSIsImEiOiJja2dtMmU1cDEycmZjMnlzMXoyeGtlN3E2In0.I2uGd7CT-xoOOdDEAFoyew")

# Stinus path
# path_uk = "C:\\Users\\stinu\\OneDrive\\Desktop\\Computerteknologi\\DAVI\\Datasets\\UK_car_accidents\\"
# path_us = "C:\\Users\\stinu\\OneDrive\\Desktop\\Computerteknologi\\DAVI\\Datasets\\US_new\\2015\\"

# Daniel path
path_us = "C:\\Users\\danie\\Desktop\\Skole\\DataVisualization\\project_data\\US_car_accidents\\2015\\"
path_uk = "C:\\Users\\danie\\Desktop\\Skole\\DataVisualization\\project_data\\UK_car_accidents\\"


uk_acc = pd.read_csv(path_uk + "Accidents0515.csv", nrows=100000)
us_acc = pd.read_csv(path_us + "accident.csv")


# Dash stuff
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    dcc.Graph(id='dropdown_parameters'),
    dcc.Dropdown(
        id='dropdown',
        options=[
            {'label': "Day of the week", 'value': 'Day_of_Week'},
            {'label': "Accident Severity", 'value': 'Accident_Severity'},
            {'label': "Local Authority(District)", 'value': 'Local_Authority_(District)'}
        ],
        value='Day_of_Week'
    )
])

@app.callback(
    Output('dropdown_parameters', 'figure'),
    [Input('dropdown', 'value')])
def update_figure(selected_param):

    filtered_df = uk_acc[selected_param]

    fig_uk = px.scatter_mapbox(uk_acc,
                            lat=uk_acc["Latitude"],
                            lon=uk_acc["Longitude"],
                            color=filtered_df)

    '''
    fig_us = px.scatter_mapbox(us_acc,
                            lat=us_acc['LATITUDE'],
                            lon=us_acc['LONGITUD'],
                            color=us_acc['DAY_WEEK'])

    fig_us.update_yaxes()
    fig_us.update_xaxes()
    fig_us.update_layout(transition_duration=500)
    '''

    fig_uk.update_yaxes()
    fig_uk.update_xaxes()
    fig_uk.update_layout(transition_duration=500)

    return fig_uk

app.run_server(debug=True)