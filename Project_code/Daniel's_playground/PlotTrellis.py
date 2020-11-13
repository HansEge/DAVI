import plotly.express as px
import pandas as pd

import dash
import dash_core_components as dcc
import dash_html_components as html

from dash.dependencies import Input, Output
path_uk = "C:\\Users\\danie\\Desktop\\Skole\\DataVisualization\\Git\\DAVI\\Project_code\\Daniel's_playground\\"
uk_acc = pd.read_csv(path_uk + "clean_UK_Data.csv")


# Convert dec
uk_acc['Car_involved_in_accident'] = uk_acc['Car_involved_in_accident'].astype(str)
uk_acc['Motorcycle_involved_in_accident'] = uk_acc['Motorcycle_involved_in_accident'].astype(str)
uk_acc['Truck_involved_in_accident'] = uk_acc['Truck_involved_in_accident'].astype(str)
uk_acc['Other_vehicle_involved_in_accident'] = uk_acc['Other_vehicle_involved_in_accident'].astype(str)

fig = px.scatter_mapbox(uk_acc, x=uk_acc.Latitude, y=uk_acc.Longitude, color=uk_acc.Speed_limit,facet_col=uk_acc.Year, facet_col_wrap=4)
fig.show()