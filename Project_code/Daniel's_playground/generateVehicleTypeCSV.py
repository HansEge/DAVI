import csv
import pandas as pd
import numpy as np

path_uk = "C:\\Users\\danie\\Desktop\\Skole\\DataVisualization\\project_data\\UK_car_accidents\\"

column_list = ["Accident_Index", "Vehicle_Reference", "Vehicle_Type", "Sex_of_Driver"]

uk_acc = pd.read_csv(path_uk + "Accidents0515.csv")
uk_veh = pd.read_csv(path_uk + "Vehicles0515.csv", usecols=column_list)

# Make data frame for data
df_acc = pd.DataFrame({'Accident_Index': uk_acc["Accident_Index"],
                   'Accident_Severity': uk_acc["Accident_Severity"],
                   'Latitude': uk_acc["Latitude"],
                   'Longitude': uk_acc["Longitude"],
                   'Date': uk_acc["Date"],
                   'Time': uk_acc["Time"],
                   'Speed_limit': uk_acc["Speed_limit"]})

# Usefull data from Vehicle dataset
df_veh = pd.DataFrame({'Accident_Index': uk_veh["Accident_Index"],
                   'Vehicle_Type': uk_veh["Vehicle_Type"]})

# Use only fatal accidents
df_acc = df_acc.loc[df_acc['Accident_Severity']==1]

# Delete all NaN cells
df_acc = df_acc.dropna()

# reset index number
df_acc = df_acc.reset_index()



df_veh = df_veh.loc[df_veh["Accident_Index"].isin(df_acc["Accident_Index"])]
df_veh = df_veh.reset_index()
df_veh = df_veh.drop(columns=['index'])

# Only look at cars(9 + 19) here
car_involved = pd.DataFrame({'Vehicle_Type': df_veh['Vehicle_Type'], 'Accident_Index': df_veh['Accident_Index']})
tmp = car_involved.query('Vehicle_Type == 9 or Vehicle_Type == 19')['Vehicle_Type']
car_involved = pd.DataFrame({'Car_involved': tmp.reindex(range(len(car_involved)), fill_value=0)})
car_involved = car_involved.query('Car_involved == 0').reindex(range(len(car_involved)), fill_value=1)
car_involved.insert(1, 'Accident_Index', df_veh['Accident_Index'])

# Only look at motorcycles(2-5 + 97) here
motorcycle_involved = pd.DataFrame({'Vehicle_Type': df_veh['Vehicle_Type'], 'Accident_Index': df_veh['Accident_Index']})
tmp = motorcycle_involved.query('1 < Vehicle_Type and 6 > Vehicle_Type or Vehicle_Type == 97')['Vehicle_Type']
motorcycle_involved = pd.DataFrame({'Motorcycle_involved': tmp.reindex(range(len(motorcycle_involved)), fill_value=0)})
motorcycle_involved = motorcycle_involved.query('Motorcycle_involved == 0').reindex(range(len(motorcycle_involved)), fill_value=1)
motorcycle_involved.insert(1, 'Accident_Index', df_veh['Accident_Index'])

# Only look at trucks(20-21) here
trucks_involved = pd.DataFrame({'Vehicle_Type': df_veh['Vehicle_Type'], 'Accident_Index': df_veh['Accident_Index']})
tmp = trucks_involved.query('19 < Vehicle_Type and  22 > Vehicle_Type')['Vehicle_Type']
trucks_involved = pd.DataFrame({'Trucks_involved': tmp.reindex(range(len(trucks_involved)), fill_value=0)})
trucks_involved = trucks_involved.query('Trucks_involved == 0').reindex(range(len(trucks_involved)), fill_value=1)
trucks_involved.insert(1, 'Accident_Index', df_veh['Accident_Index'])

# Only look at other vehicles here
other_involved = pd.DataFrame({'Vehicle_Type': df_veh['Vehicle_Type'], 'Accident_Index': df_veh['Accident_Index']})
tmp = other_involved.query('Vehicle_Type == 1 or (9 < Vehicle_Type and 19 > Vehicle_Type) or '
                           '(21 < Vehicle_Type and 96 > Vehicle_Type) or Vehicle_Type == 98')['Vehicle_Type']
other_involved = pd.DataFrame({'Other_involved': tmp.reindex(range(len(other_involved)), fill_value=0)})
other_involved = other_involved.query('Other_involved == 0').reindex(range(len(other_involved)), fill_value=1)
other_involved.insert(1, 'Accident_Index', df_veh['Accident_Index'])

# Create final dataframes to add to dataframe list
car_involved_final = pd.DataFrame(np.zeros((len(car_involved.drop_duplicates(subset=('Accident_Index')).reset_index(
    drop=True)),1)), columns=['Car_involved_in_accident'])
motorcycle_involved_final = pd.DataFrame(np.zeros((len(motorcycle_involved.drop_duplicates(
    subset=('Accident_Index')).reset_index(drop=True)),1)), columns=['Motorcycle_involved_in_accident'])
trucks_involved_final = pd.DataFrame(np.zeros((len(trucks_involved.drop_duplicates(
    subset=('Accident_Index')).reset_index(drop=True)),1)), columns=['Truck_involved_in_accident'])
other_involved_final = pd.DataFrame(np.zeros((len(other_involved.drop_duplicates(
    subset=('Accident_Index')).reset_index(drop=True)),1)), columns=['Other_vehicle_involved_in_accident'])

ids = car_involved.drop_duplicates(subset=('Accident_Index')).reset_index(drop=True)['Accident_Index']

for i in range(len(ids)):
    id = ids[i]
    if i % 100 == 0:
        print(i)
    for k in range(car_involved[car_involved.Accident_Index == id].shape[0]):
        if car_involved[car_involved.Accident_Index == id].iloc[k]['Car_involved'] != 0:
            car_involved_final.at[i, 'Car_involved_in_accident'] = 1
        if motorcycle_involved[motorcycle_involved.Accident_Index == id].iloc[k]['Motorcycle_involved'] != 0:
            motorcycle_involved_final.at[i, 'Motorcycle_involved_in_accident'] = 1
        if trucks_involved[trucks_involved.Accident_Index == id].iloc[k]['Trucks_involved'] != 0:
            trucks_involved_final.at[i, 'Truck_involved_in_accident'] = 1
        if other_involved[other_involved.Accident_Index == id].iloc[k]['Other_involved'] != 0:
            other_involved_final.at[i, 'Other_vehicle_involved_in_accident'] = 1

# Make final data frame
df_final = pd.DataFrame({'Accident_Index': df_acc["Accident_Index"],
                         'Car_involved_in_accident': car_involved_final['Car_involved_in_accident'],
                         'Motorcycle_involved_in_accident': motorcycle_involved_final['Motorcycle_involved_in_accident'],
                         'Truck_involved_in_accident': trucks_involved_final['Truck_involved_in_accident'],
                         'Other_vehicle_involved_in_accident': other_involved_final['Other_vehicle_involved_in_accident']})

df_final['Car_involved_in_accident'] = df_final['Car_involved_in_accident'].astype(int)
df_final['Motorcycle_involved_in_accident'] = df_final['Motorcycle_involved_in_accident'].astype(int)
df_final['Truck_involved_in_accident'] = df_final['Truck_involved_in_accident'].astype(int)
df_final['Other_vehicle_involved_in_accident'] = df_final['Other_vehicle_involved_in_accident'].astype(int)


with open('Clean_Vehicle_Type_Data.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Accident_Index",
                     "Car_involved_in_accident", "Motorcycle_involved_in_accident",
                     "Truck_involved_in_accident", "Other_vehicle_involved_in_accident"])
    for i in range(len(df_final)):
        writer.writerow([df_final["Accident_Index"].values[i],
                         df_final["Car_involved_in_accident"].values[i],
                         df_final["Motorcycle_involved_in_accident"].values[i],
                         df_final["Truck_involved_in_accident"].values[i],
                         df_final["Other_vehicle_involved_in_accident"].values[i]])

print("now you are here")
