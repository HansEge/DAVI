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

path_uk = "C:\\Users\\stinu\\Desktop\\DAVI\Data\\UK_car_accidents\\"
path_us = "C:\\Users\\stinu\\Desktop\\DAVI\\Data\\US_car_accidents\\CleanedFilesUS\\"

uk_acc = pd.read_csv(path_uk + "clean_UK_Data.csv")
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

fig = make_subplots(
    rows=1, cols=2,
    specs=[[{"type": "mapbox"}, {"type": "mapbox"}]]
)

fig.add_trace(
    go.Scattermapbox(
        lat=us_acc.loc[((us_acc['Car_involved_in_accident']==1) & (us_acc['Year']==2005))]['Latitude'],
        lon=us_acc.loc[((us_acc['Car_involved_in_accident']==1) & (us_acc['Year']==2005))]['Longitude'],
        mode='markers',
        text=us_acc.loc[((us_acc['Car_involved_in_accident']==1) & (us_acc['Year']==2005))]['Number of vehicles in accident'],
        marker=go.scattermapbox.Marker(
            size=4,
            color=us_acc.loc[((us_acc['Car_involved_in_accident']==1) & (us_acc['Year']==2005))]['Number of vehicles in accident']
        )),
    row=1, col=1
)
fig.add_trace(
    go.Scattermapbox(
        lat=us_acc.loc[us_acc['Motorcycle_involved_in_accident']==1]['Latitude'],
        lon=us_acc.loc[us_acc['Motorcycle_involved_in_accident']==1]['Longitude'],
        mode='markers',
        marker=go.scattermapbox.Marker(
            size=4,
            color=us_acc.loc[us_acc['Motorcycle_involved_in_accident']==1]['Speed Limit']
        )),
    row=1,
    col=2
)


fig.update_layout(
    autosize=True,
    hovermode='closest'
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

fig.show()
