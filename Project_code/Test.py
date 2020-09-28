import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import seaborn as sns

# Daniels path
path_dalle_us = "C:\\Users\\danie\\Desktop\\Skole\\DataVisualization\\project_data\\US_car_accidents\\"
path_dalle_uk = "C:\\Users\\danie\\Desktop\\Skole\\DataVisualization\\project_data\\UK_car_accidents\\"


us_veh = pd.read_csv (path_dalle_us + "VEH_AUX.csv")
us_per = pd.read_csv (path_dalle_us + "PER_AUX.csv")
us_acc = pd.read_csv (path_dalle_us + "ACC_AUX.csv")

# New dataframe only including year and hit and run attribute
df2 = pd.DataFrame({"Year" : us_acc["YEAR"], "Hit and run": us_acc["A_HR"]})

# placeholders for y values in plot
count_hit_and_run = []
count_no_hit_and_run = []

# foor-loop to count hit and run and not hit and run for each year
for year in range(1982, 2018):
    count_hit_and_run.append(len(df2.loc[(df2['Year'] == year) & (df2['Hit and run'] == 1)]))
    count_no_hit_and_run.append(len(df2.loc[(df2['Year'] == year) & (df2['Hit and run'] == 2)]))

# x values in plot
years = us_acc["YEAR"].unique()

# Plot bar diagram
fig = go.Figure()
fig.add_trace(go.Bar(
    x=years,
    y=count_hit_and_run,
    name='Hit and run',
    marker_color='indianred'
))
fig.add_trace(go.Bar(
    x=years,
    y=count_no_hit_and_run,
    name='No hit and run',
    marker_color='lightsalmon'
))

fig.update_layout(barmode='group', xaxis_tickangle=-45)
fig.show()
