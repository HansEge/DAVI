import numpy as np
import pandas as pd
import plotly
import plotly.offline as offline
import plotly.graph_objs as go
import plotly.express as px

px.set_mapbox_access_token("pk.eyJ1IjoiaGFuc2VnZSIsImEiOiJja2dtMmU1cDEycmZjMnlzMXoyeGtlN3E2In0.I2uGd7CT-xoOOdDEAFoyew")

path = "C:\\Users\\stinu\\OneDrive\\Desktop\\Computerteknologi\\DAVI\\Datasets\\UK_car_accidents\\"

uk_veh = pd.read_csv (path + "Accidents0515.csv", nrows=500000)

fig = px.scatter_mapbox(uk_veh,
                        lat=uk_veh["Latitude"],
                        lon=uk_veh["Longitude"],
                        color = uk_veh["Day_of_Week"],
                        )

fig.show()