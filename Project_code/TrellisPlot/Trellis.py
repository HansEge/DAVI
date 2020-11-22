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

# uk_acc = pd.read_csv(path_uk + "clean_UK_Data.csv")
uk_acc = pd.read_csv(path_uk + "UK_cleaned.csv")
us_acc = pd.read_csv(path_us + "US_cleaned.CSV")

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

variables = ['Vehicle type', 'Speed Limit', 'Number of vehicles in accident', 'Quarter', 'Time of day', 'Motorcycle_involved_in_accident']

str_quarter_titles = ['First quarter', 'Second Quarter', 'Third quarter', 'Fourth quarter']
str_T_day_titles = ['10pm - 5am', '6am - 1pm', '2pm - 9pm']
str_speed_limit_titles = ['0mph - 35mph', '36mph - 59mph', '60mph - 100mph']



app.layout = html.Div(
    [
        html.Div(
            [
                html.H3('Map of US'),
                dcc.Graph(id='US_graph', style={'display': 'internal-block'}, figure={})
            ]
        ),

        html.Div(
            [
                dcc.Dropdown(
                    id='US_plot_x',
                    options=[{'label': i, 'value': i} for i in variables],
                    placeholder='Pick one',
                    value=variables[1],
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
                    value=variables[4],
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
        'Vehicle type': ['Car_involved_in_accident', 'Motorcycle_involved_in_accident',
                         'Truck_involved_in_accident', 'Other_involved_in_accident'],
        'Number of vehicles in accident': 'Num_veh_acc',
        'Year': 'Year',
        'Motorcycle_involved_in_accident': 'Mc_acc',
        'Quarter': ['Quarter', str_quarter_titles],
        'Speed Limit': ['Speed_limit', str_speed_limit_titles],
        'Time of day': ['T_day', str_T_day_titles]

    }
    return switch[arg]


@app.callback(
    Output('US_graph', 'figure'),
    [Input('US_plot_x', 'value'),
     Input('US_plot_y', 'value'),
     Input('year-range-slider', 'value')])
def update_figure(us_plot_x, us_plot_y, years_slider):
    x_params = switcher(us_plot_x)
    y_params = switcher(us_plot_y)
    years = years_slider

    if len(x_params[0]) != 1 or len(y_params[0]) != 1:
        # Todo: code condition to handle vehicle type and other stuff
        pass

    # dynamically estimate number of columns
    n_columns = len(set(us_acc[x_params[0]]))

    # dynamically estimate number of rows
    n_rows = len(set(us_acc[y_params[0]]))
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
            fig.add_trace(
                go.Scattermapbox(
                    lat=us_acc.loc[((us_acc[y_params[0] ]== i) &
                                    (us_acc[x_params[0]] == k) &
                                    ((us_acc['Year'] >= min(years)) &
                                     (us_acc['Year'] <= max(years)))
                                    )]['Lat'],
                    lon=us_acc.loc[((us_acc[y_params[0]] == i) &
                                    (us_acc[x_params[0]] == k) &
                                    ((us_acc['Year'] >= min(years)) &
                                     (us_acc['Year'] <= max(years)))
                                    )]['Lon'],
                    mode='markers',
                    text=us_acc['Num_veh_acc'],
                    marker=go.scattermapbox.Marker(
                        size=us_acc['Num_veh_acc']+1,
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
            lat=38,
            lon=-97
        ),
        pitch=0,
        zoom=2
    )

    fig.update_yaxes()
    fig.update_xaxes()
    fig.update_layout(transition_duration=500)

    return fig


app.run_server(debug=True)
