import csv
import pandas as pd
import numpy as np

path_uk = "C:\\Users\\danie\\Desktop\\Skole\\DataVisualization\\project_data\\UK_car_accidents\\"

uk_acc = pd.read_csv(path_uk + "Accidents0515.csv")

# Make data frame for data
df_acc = pd.DataFrame({'Accident_Index': uk_acc["Accident_Index"],
                   'Accident_Severity': uk_acc["Accident_Severity"],
                   'Latitude': uk_acc["Latitude"],
                   'Longitude': uk_acc["Longitude"],
                   'Date': uk_acc["Date"],
                   'Time': uk_acc["Time"],
                   'Speed_limit': uk_acc["Speed_limit"]})

# Use only fatal accidents
df_acc = df_acc.loc[df_acc['Accident_Severity']==1]

# Delete all NaN cells
df_acc = df_acc.dropna()

# reset index number
df_acc = df_acc.reset_index()

# Split date after year, month and day
day_list = []
month_list = []
year_list = []

df_Date = pd.DataFrame({'Date': df_acc["Date"]})

for i in range(len(df_Date)):
    df_Date["Date"].values[i]=df_Date["Date"].values[i].split('/')
    day_list.append(int(df_Date["Date"].values[i][0]))
    month_list.append(int(df_Date["Date"].values[i][1]))
    year_list.append(int(df_Date["Date"].values[i][2]))


# Only use hour of Time
hour_list = []

df_Time = pd.DataFrame({'Time': df_acc["Time"]})
for i in range(len(df_Time)):
    df_Time["Time"].values[i] = df_Time["Time"].values[i].split(':')
    hour_list.append(int(df_Time["Time"].values[i][0]))
#

df_final = pd.DataFrame({'Accident_Index': df_acc["Accident_Index"],
                         'Year': year_list,
                         'Month': month_list,
                         'Day': day_list,
                         'Hour': hour_list})

df_final['Year'] = df_final['Year'].astype(int)
df_final['Month'] = df_final['Month'].astype(int)
df_final['Day'] = df_final['Day'].astype(int)
df_final['Hour'] = df_final['Hour'].astype(int)

with open('Clean_Time_Data.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Accident_Index",
                     "Year", "Month",
                     "Day", "Hour"])
    for i in range(len(df_final)):
        writer.writerow([df_final["Accident_Index"].values[i],
                         df_final["Year"].values[i],
                         df_final["Month"].values[i],
                         df_final["Day"].values[i],
                         df_final["Hour"].values[i]])

print("now you are here")