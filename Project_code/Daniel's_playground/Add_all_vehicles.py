import csv
import os
import glob
import pandas as pd
import numpy as np

path_uk = "C:\\Users\\danie\\Desktop\\Skole\\DataVisualization\\Git\\DAVI\\Project_code\\Cleaned_data\\"

uk_acc = pd.read_csv(path_uk + "UK_cleaned.csv")

uk_acc['All_veh'] = 1


# Create final dataframe
df_final = pd.DataFrame({'Acc_index': uk_acc["Acc_index"],
                         'Lat': uk_acc["Lat"],
                         'Lon': uk_acc["Lon"],
                         'Num_veh_acc': uk_acc["Num_veh_acc"],
                         'Car_acc': uk_acc["Car_acc"],
                         'Mc_acc': uk_acc["Mc_acc"],
                         'Truck_acc': uk_acc["Truck_acc"],
                         'Other_acc': uk_acc["Other_acc"],
                         'Year': uk_acc["Year"],
                         'Quarter': uk_acc["Quarter"],
                         'T_day': uk_acc["T_day"],
                         'Speed_limit': uk_acc["Speed_limit"],
                         'All_veh': uk_acc["All_veh"]})


# Make final CSV file with correct names
with open('UK_cleaned1.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Acc_index', 'Lat', 'Lon', 'Num_veh_acc',
                     'Car_acc', 'Mc_acc', 'Truck_acc',
                     'Other_acc', 'Year', 'Quarter', 'T_day', 'Speed_limit', 'All_veh'])
    for i in range(len(df_final)):
        writer.writerow([df_final["Acc_index"].values[i],
                         df_final["Lat"].values[i],
                         df_final["Lon"].values[i],
                         df_final["Num_veh_acc"].values[i],
                         df_final["Car_acc"].values[i],
                         df_final["Mc_acc"].values[i],
                         df_final["Truck_acc"].values[i],
                         df_final["Other_acc"].values[i],
                         df_final["Year"].values[i],
                         df_final["Quarter"].values[i],
                         df_final["T_day"].values[i],
                         df_final["Speed_limit"].values[i],
                         df_final["All_veh"].values[i]])


print("here")

