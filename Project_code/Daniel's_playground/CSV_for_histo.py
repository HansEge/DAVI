import csv
import os
import glob
import pandas as pd
import numpy as np

path_time_data = "C:\\Users\\danie\\Desktop\\Skole\\DataVisualization\\Git\\DAVI\\Project_code\\Daniel's_playground\\"
path_uk = "C:\\Users\\danie\\Desktop\\Skole\\DataVisualization\\project_data\\UK_car_accidents\\"

uk_time_data = pd.read_csv(path_time_data + "Clean_time_data.csv")
uk_acc = pd.read_csv(path_uk + "Accidents0515.csv")

df = pd.DataFrame({'Accident_Index': uk_acc["Accident_Index"],
                   'Speed_limit': uk_acc["Speed_limit"],
                   'Num_veh_acc': uk_acc["Number_of_Vehicles"]})

df = df.loc[df["Accident_Index"].isin(uk_time_data["Accident_Index"])]
df = df.reset_index()

df_final = pd.DataFrame({'Acc_index': uk_time_data["Accident_Index"],
                         'Year': uk_time_data["Year"],
                         'Month': uk_time_data["Month"],
                         'Day': uk_time_data["Day"],
                         'Hour': uk_time_data["Hour"],
                         'Speed_limit': df["Speed_limit"],
                         'Num_veh_acc': df["Num_veh_acc"]})

# Make final CSV file with correct names
with open('UK_cleaned_histo.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Acc_index', 'Year', 'Month', 'Day',
                     'Hour', 'Speed_limit', 'Num_veh_acc'])
    for i in range(len(df_final)):
        writer.writerow([df_final["Acc_index"].values[i],
                         df_final["Year"].values[i],
                         df_final["Month"].values[i],
                         df_final["Day"].values[i],
                         df_final["Hour"].values[i],
                         df_final["Speed_limit"].values[i],
                         df_final["Num_veh_acc"].values[i]])

print("Hej")

