import plotly.graph_objects as go

import pandas as pd


# path = "C:\\Users\\stinu\\Desktop\\DAVI\\Data\\US_car_accidents\\"
path = "C:\\Users\\stinu\\OneDrive\\Desktop\\Computerteknologi\\DAVI\\Datasets\\UK_car_accidents\\"

uk_veh = pd.read_csv (path + "Accidents0515.csv", nrows=1000)


fig = go.Figure(data=go.Scattergeo(
        lon = uk_veh['Longitude'],
        lat = uk_veh['Latitude'],
        text = "Av av av",
        mode = 'markers',
        ))

fig.update_layout(
        title = 'Most trafficked US airports<br>(Hover for airport names)',
        geo_scope='europe',
    )
fig.show()