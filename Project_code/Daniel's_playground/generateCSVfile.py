# Import stuf
import csv
import pandas as pd

path_uk = "C:\\Users\\danie\\Desktop\\Skole\\DataVisualization\\project_data\\UK_car_accidents\\"

column_list = ["Accident_Index", "Vehicle_Reference", "Vehicle_Type", "Sex_of_Driver"]

uk_acc = pd.read_csv(path_uk + "Accidents0515.csv")
uk_veh = pd.read_csv(path_uk + "Vehicles0515.csv", usecols=column_list)

# Make data frame for data
df = pd.DataFrame({'Accident_Index': uk_acc["Accident_Index"],
                   'Accident_Severity': uk_acc["Accident_Severity"],
                   'Latitude': uk_acc["Latitude"],
                   'Longitude': uk_acc["Longitude"],
                   'Date': uk_acc["Date"],
                   'Time': uk_acc["Time"],
                   'Speed_limit': uk_acc["Speed_limit"]})

# Usefull data from Vehicle dataset
df2 = pd.DataFrame({'Accident_Index': uk_veh["Accident_Index"],
                   'Vehicle_Reference': uk_veh["Vehicle_Reference"],
                   'Vehicle_Type': uk_veh["Vehicle_Type"],
                   'Sex_of_Driver': uk_veh["Sex_of_Driver"]})

# Use only fatal accidents
df = df.loc[df['Accident_Severity']==1]

# Delete all NaN cells
df = df.dropna()

# reset index number
df = df.reset_index()

# Split date after year, month and day
day_list = []
month_list = []
year_list = []

df_Date = pd.DataFrame({'Date': df["Date"]})

for i in range(len(df_Date)):
    df_Date["Date"].values[i]=df_Date["Date"].values[i].split('/')
    day_list.append(int(df_Date["Date"].values[i][0]))
    month_list.append(int(df_Date["Date"].values[i][1]))
    year_list.append(int(df_Date["Date"].values[i][2]))


# Only use hour of Time
hour_list = []

df_Time = pd.DataFrame({'Time': df["Time"]})
for i in range(len(df_Time)):
    df_Time["Time"].values[i] = df_Time["Time"].values[i].split(':')
    hour_list.append(int(df_Time["Time"].values[i][0]))
#

# Add year, month, day and hour to Data frame
df.insert(5, "Year", year_list, True)
df.insert(6, "Month", month_list, True)
df.insert(7, "Day", day_list, True)
df.insert(8, "Hour", hour_list, True)
#

# Add type of vehicle columns in dataframe
df['Car_involved_in_accident'] = 0
df['Motorcycle_involved_in_accident'] = 0
df['Truck_involved_in_accident'] = 0
df['Other_vehicle_involved_in_accident'] = 0

# Check type of vehicle in all accidents
for i in range(len(df)):
    id = df["Accident_Index"][i]
    print(i)
    for x in range(df2[df2.Accident_Index == id].shape[0]):
        if df2[df2.Accident_Index == id].iloc[x]['Vehicle_Type'] == 9 or df2[df2.Accident_Index == id].iloc[x]['Vehicle_Type'] == 19:
            df.at[i, 'Car_involved_in_accident'] = 1
        elif df2[df2.Accident_Index == id].iloc[x]['Vehicle_Type'] in range(2,6):
            df.at[i, 'Motorcycle_involved_in_accident'] = 1
        elif df2[df2.Accident_Index == id].iloc[x]['Vehicle_Type'] in range(20, 22):
            df.at[i, 'Truck_involved_in_accident'] = 1
        else:
            df.at[i, 'Other_vehicle_involved_in_accident'] = 1


# Drop Date and Time columns
df = df.drop(columns=['Date', 'Time'])
#

# Make .csv file
with open('clean_UK_Data.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Accident_Index", "Latitude", "Longitude",
                     "Year", "Month", "Day", "Hour", "Speed_limit",
                     "Car_involved_in_accident", "Motorcycle_involved_in_accident",
                     "Truck_involved_in_accident", "Other_vehicle_involved_in_accident"])
    for i in range(len(df)):
        writer.writerow([df["Accident_Index"].values[i],
                         df["Latitude"].values[i],
                         df["Longitude"].values[i],
                         df["Year"].values[i],
                         df["Month"].values[i],
                         df["Day"].values[i],
                         df["Hour"].values[i],
                         df["Speed_limit"].values[i],
                         df["Car_involved_in_accident"].values[i],
                         df["Motorcycle_involved_in_accident"].values[i],
                         df["Truck_involved_in_accident"].values[i],
                         df["Other_vehicle_involved_in_accident"].values[i]])