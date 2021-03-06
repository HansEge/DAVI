import pandas as pd

path_uk = "C:\\Users\\danie\\Desktop\\Skole\\DataVisualization\\project_data\\UK_car_accidents\\"
column_list = ["Accident_Index", "Vehicle_Reference", "Vehicle_Type", "Sex_of_Driver"]

uk_acc = pd.read_csv(path_uk + "Accidents0515.csv")
uk_veh = pd.read_csv(path_uk + "Vehicles0515.csv", usecols=column_list)

df = pd.DataFrame({'Accident_Index': uk_acc["Accident_Index"],
                   'Accident_Severity': uk_acc["Accident_Severity"],
                   'Latitude': uk_acc["Latitude"],
                   'Longitude': uk_acc["Longitude"],
                   'Date': uk_acc["Date"],
                   'Time': uk_acc["Time"],
                   'Speed_limit': uk_acc["Speed_limit"]})

# Use only fatal accidents
df = df.loc[df['Accident_Severity']==1]

# Delete all NaN cells
df = df.dropna()

# reset index number
df = df.reset_index()

# Dataframe for one index
df_acc_id = df.Accident_Index


df2 = pd.DataFrame({'Accident_Index': uk_veh["Accident_Index"],
                   'Vehicle_Reference': uk_veh["Vehicle_Reference"],
                   'Vehicle_Type': uk_veh["Vehicle_Type"],
                   'Sex_of_Driver': uk_veh["Sex_of_Driver"]})

# Data frame for
df2 = df2.loc[df2["Accident_Index"].isin(df["Accident_Index"])]
df2 = df2.reset_index()

df['Car_involved_in_accident'] = 0
df['Motorcycle_involved_in_accident'] = 0
df['Truck_involved_in_accident'] = 0
df['Other_vehicle_involved_in_accident'] = 0

df_car = pd.DataFrame({'Car_involved_in_accident': df.Car_involved_in_accident})
df_mcycle = pd.DataFrame({'Motorcycle_involved_in_accident': df.Motorcycle_involved_in_accident})
df_truck = pd.DataFrame({'Truck_involved_in_accident': df.Truck_involved_in_accident})
df_other = pd.DataFrame({'Other_vehicle_involved_in_accident': df.Other_vehicle_involved_in_accident})

for i in range(len(df)):
    id = df["Accident_Index"][i]
    print(i)
    for x in range(df2[df2.Accident_Index == id].shape[0]):
        if df2[df2.Accident_Index == id].iloc[x]['Vehicle_Type'] == 9 or df2[df2.Accident_Index == id].iloc[x]['Vehicle_Type'] == 19:
            df_car.at[i, 'Car_involved_in_accident'] = 1
        elif df2[df2.Accident_Index == id].iloc[x]['Vehicle_Type'] in range(2,6):
            df_mcycle.at[i, 'Motorcycle_involved_in_accident'] = 1
        elif df2[df2.Accident_Index == id].iloc[x]['Vehicle_Type'] in range(20, 22):
            df_truck.at[i, 'Truck_involved_in_accident'] = 1
        else:
            df_other.at[i, 'Other_vehicle_involved_in_accident'] = 1