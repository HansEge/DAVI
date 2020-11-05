import csv
import pandas as pd

path_uk = "C:\\Users\\danie\\Desktop\\Skole\\DataVisualization\\project_data\\UK_car_accidents\\"

uk_acc = pd.read_csv(path_uk + "Accidents0515.csv")

# Make data frame for data
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

# Split date after day month year
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


# Add year, month, day and hour to Data frame
df.insert(5, "Year", year_list, True)
df.insert(6, "Month", month_list, True)
df.insert(7, "Day", day_list, True)
df.insert(8, "Hour", hour_list, True)

# Drop Date and Time columns
df = df.drop(columns=['Date', 'Time'])

# Make .csv file
with open('clean_UK_Data.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Accident_Index", "Latitude", "Longitude",
                     "Year", "Month", "Day", "Hour", "Speed_limit"])
    for i in range(len(df)):
        writer.writerow([df["Accident_Index"].values[i],
                         df["Latitude"].values[i],
                         df["Longitude"].values[i],
                         df["Year"].values[i],
                         df["Month"].values[i],
                         df["Day"].values[i],
                         df["Hour"].values[i],
                         df["Speed_limit"].values[i]])




