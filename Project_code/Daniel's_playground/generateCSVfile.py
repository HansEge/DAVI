import csv
import pandas as pd

path_uk = "C:\\Users\\danie\\Desktop\\Skole\\DataVisualization\\project_data\\UK_car_accidents\\"

uk_acc = pd.read_csv(path_uk + "Accidents0515.csv")

print(uk_acc["Accident_Index"][0])

with open('testData.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Accident_Index", "Longitude", "Latitude"])
    for i in range(len(uk_acc)):
        writer.writerow([uk_acc["Accident_Index"][i], uk_acc["Longitude"][i], uk_acc["Latitude"][i]])


