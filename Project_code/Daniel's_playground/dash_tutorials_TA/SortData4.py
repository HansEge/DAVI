import csv
import os
import glob
import pandas as pd
import numpy as np


path_uk = "C:\\Users\\danie\\Desktop\\Skole\\DataVisualization\\project_data\\Cleaned_data\\"

uk_acc = pd.read_csv(path_uk + "UK_cleaned.csv")

Quater_list = []
T_day_list = []
Speed_limit_list = []

'''
Sort month into quater
Jan - Feb - Marts = Q1 = 0
April - Maj -Juni = Q2 = 1
Juli - Aug - Sep = Q3 = 2
Okt - Nov - Dec = Q4 = 3
'''
for i in range(len(uk_acc["Month"])):
    if (uk_acc["Month"][i] > 0) and (uk_acc["Month"][i] < 4):
        Quater_list.append(int(0))
    elif (uk_acc["Month"][i] > 3) and (uk_acc["Month"][i] < 7):
        Quater_list.append(int(1))
    elif (uk_acc["Month"][i] > 6) and (uk_acc["Month"][i] < 10):
        Quater_list.append(int(2))
    elif (uk_acc["Month"][i] > 9) and (uk_acc["Month"][i] < 13):
        Quater_list.append(int(3))

'''
Sort Hour of day into interval
22-05 = 0
06-13 = 1
14-21 = 2 
'''
for i in range(len(uk_acc["Hour"])):
    if (uk_acc["Hour"][i] > 21) or ((uk_acc["Hour"][i] >= 0) and ((uk_acc["Hour"][i] < 6))):
        T_day_list.append(int(0))
    elif (uk_acc["Hour"][i] > 5) and (uk_acc["Hour"][i] < 14):
        T_day_list.append(int(1))
    elif (uk_acc["Hour"][i] > 13) and (uk_acc["Hour"][i] < 22):
        T_day_list.append(int(2))


'''
Sort speed limit into interval
35 or under = 0
36 - 59 = 1
59+ = 2 
'''
for i in range(len(uk_acc["Speed Limit"])):
    if (uk_acc["Speed Limit"][i] < 36):
        Speed_limit_list.append(int(0))
    elif (uk_acc["Speed Limit"][i] > 35) and (uk_acc["Speed Limit"][i] < 60):
        Speed_limit_list.append(int(1))
    elif (uk_acc["Speed Limit"][i] > 59):
        Speed_limit_list.append(int(2))


# Create final dataframe
df_final = pd.DataFrame({'Acc_index': uk_acc["Accident_Index"],
                         'Lat': uk_acc["Latitude"],
                         'Lon': uk_acc["Longitude"],
                         'Num_veh_acc': uk_acc["Number_Of_Vehicles_In_Accident"],
                         'Car_acc': uk_acc["Car_involved_in_accident"],
                         'Mc_acc': uk_acc["Motorcycle_involved_in_accident"],
                         'Truck_acc': uk_acc["Truck_involved_in_accident"],
                         'Other_acc': uk_acc["Other_vehicle_involved_in_accident"],
                         'Year': uk_acc["Year"],
                         'Quarter': Quater_list,
                         'T_day': T_day_list,
                         'Speed_limit': Speed_limit_list,
                         'Day': uk_acc["Day"]})



# Make final CSV file with correct names
with open('UK_cleaned.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Acc_index', 'Lat', 'Lon', 'Num_veh_acc',
                     'Car_acc', 'Mc_acc', 'Truck_acc',
                     'Other_acc', 'Year', 'Quarter', 'T_day', 'Speed_limit', 'Day'])
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
                         df_final["Day"].values[i]])


print("Quater done")


