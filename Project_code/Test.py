# DAVI fun

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

path_stinus_us = "C:\\Users\\stinu\\OneDrive\\Desktop\\Computerteknologi\\DAVI\\Datasets\\US_car_accidents\\"
path_stinus_uk = "C:\\Users\\stinu\\OneDrive\\Desktop\\Computerteknologi\\DAVI\\Datasets\\UK_car_accidents\\"


us_veh = pd.read_csv (path_stinus_us + "VEH_AUX.csv")
us_per = pd.read_csv (path_stinus_us + "PER_AUX.csv")
us_acc = pd.read_csv (path_stinus_us + "ACC_AUX.csv")


fig = px.scatter(x=us_per["YEAR"], y=us_per["A_PTYPE"])
fig.show()

fig = go.Figure()
fig.add_trace(go.Bar(
    x=us_per["YEAR"],
    y=[20, 14, 25, 16, 18, 22, 19, 15, 12, 16, 14, 17],
    name='Driver',
    marker_color='indianred'
))
fig.add_trace(go.Bar(
    x=us_per["YEAR"],
    y=[19, 14, 22, 14, 16, 19, 15, 14, 10, 12, 12, 16],
    name='Secondary Product',
    marker_color='lightsalmon'
))

# Here we modify the tickangle of the xaxis, resulting in rotated labels.
fig.update_layout(barmode='group', xaxis_tickangle=-45)
fig.show()