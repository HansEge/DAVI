import csv
import pandas as pd
import numpy as np

path_uk = "C:\\Users\\danie\\Desktop\\Skole\\DataVisualization\\project_data\\UK_car_accidents\\"
path_csv = "C:\\Users\\danie\\Desktop\\Skole\\DataVisualization\\Git\\DAVI\\Project_code\\Daniel's_playground\\"

uk_acc = pd.read_csv(path_uk + "Accidents0515.csv")
time_CSV = pd.read_csv(path_csv + "Clean_Time_Data.csv")
vehicle_Type_CSV = pd.read_csv(path_csv + "Clean_Vehicle_Type_Data.csv")

# Make data frame for data
df_acc = pd.DataFrame({'Accident_Index': uk_acc["Accident_Index"],
                       'Accident_Severity': uk_acc["Accident_Severity"],
                       'Latitude': uk_acc["Latitude"],
                       'Longitude': uk_acc["Longitude"],
                       'Number_Of_Vehicles_In_Accident': uk_acc["Number_of_Vehicles"],
                       'Date': uk_acc["Date"],
                       'Time': uk_acc["Time"],
                       'Speed_Limit': uk_acc["Speed_limit"]})

# Use only fatal accidents
df_acc = df_acc.loc[df_acc['Accident_Severity']==1]

# Delete all NaN cells
df_acc = df_acc.dropna()

# reset index number
df_acc = df_acc.reset_index()

df_final = pd.DataFrame({'Accident_Index': df_acc["Accident_Index"],
                         'Latitude': df_acc["Latitude"],
                         'Longitude': df_acc["Longitude"],
                         'Number_Of_Vehicles_In_Accident': df_acc["Number_Of_Vehicles_In_Accident"],
                         'Car_involved_in_accident': vehicle_Type_CSV["Car_involved_in_accident"],
                         'Motorcycle_involved_in_accident': vehicle_Type_CSV["Motorcycle_involved_in_accident"],
                         'Truck_involved_in_accident': vehicle_Type_CSV["Truck_involved_in_accident"],
                         'Other_vehicle_involved_in_accident': vehicle_Type_CSV["Other_vehicle_involved_in_accident"],
                         'Year': time_CSV["Year"],
                         'Month': time_CSV["Month"],
                         'Day': time_CSV["Day"],
                         'Hour': time_CSV["Hour"],
                         "Speed_Limit": df_acc["Speed_Limit"]})

with open('UK_Cleaned_Data.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Accident_Index', 'Latitude', 'Longitude', 'Number_Of_Vehicles_In_Accident',
                     'Car_involved_in_accident', 'Motorcycle_involved_in_accident', 'Truck_involved_in_accident',
                     'Other_vehicle_involved_in_accident', 'Year', 'Month', 'Day', 'Hour', 'Speed Limit'])
    for i in range(len(df_final)):
        writer.writerow([df_final["Accident_Index"].values[i],
                         df_final["Latitude"].values[i],
                         df_final["Longitude"].values[i],
                         df_final["Number_Of_Vehicles_In_Accident"].values[i],
                         df_final["Car_involved_in_accident"].values[i],
                         df_final["Motorcycle_involved_in_accident"].values[i],
                         df_final["Truck_involved_in_accident"].values[i],
                         df_final["Other_vehicle_involved_in_accident"].values[i],
                         df_final["Year"].values[i],
                         df_final["Month"].values[i],
                         df_final["Day"].values[i],
                         df_final["Hour"].values[i],
                         df_final["Speed_Limit"].values[i]])
print("now you are here")



