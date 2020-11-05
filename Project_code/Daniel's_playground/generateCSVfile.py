import csv
import pandas as pd

path_uk = "C:\\Users\\danie\\Desktop\\Skole\\DataVisualization\\project_data\\UK_car_accidents\\"

uk_acc = pd.read_csv(path_uk + "Accidents0515.csv")

df = pd.DataFrame({'Accident_Index': uk_acc["Accident_Index"],
                   'Accident_Severity': uk_acc["Accident_Severity"],
                   'Longitude': uk_acc["Longitude"],
                   'Latitude': uk_acc["Latitude"],
                   'Date': uk_acc["Date"],
                   'Time': uk_acc["Time"],
                   'Speed_limit': uk_acc["Speed_limit"]})

df2 = df.loc[df['Accident_Severity']==1]

with open('testData.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Accident_Index", "Longitude", "Latitude", "Date", "Time", "Speed_limit"])
    for i in range(len(df2)):
        writer.writerow([df2["Accident_Index"].values[i],
                         df2["Longitude"].values[i],
                         df2["Latitude"].values[i],
                         df2["Date"].values[i],
                         df2["Time"].values[i],
                         df2["Speed_limit"].values[i]])



'''
with open('testData.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Accident_Index", "Longitude", "Latitude"])
    for i in range(len(uk_acc)):
        writer.writerow([uk_acc["Accident_Index"][i], uk_acc["Longitude"][i], uk_acc["Latitude"][i]])

'''


