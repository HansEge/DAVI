import csv
import os
import glob
import pandas as pd
import numpy as np

os.chdir("C:\\Users\\stinu\\Desktop\\DAVI\\Data\\US_car_accidents\\CleanedFilesUS\\")

extension = 'csv'

# Used to get speed limit from vehicle.csv because data has different structure for different years :(
index_for_speed = 2009

df = pd.read_csv('US_cleaned.csv')

df['All_veh'] = 1

with open('US_cleaned_new.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Lat', 'Lon', 'Num_veh_acc', 'Car_acc',
                     'Mc_acc', 'Truck_acc', 'Year', 'Quarter', 'T_day', 'Speed_limit', 'All_veh'])
    for i in range(len(df)):
        writer.writerow([df['Lat'][i],
                         df['Lon'][i],
                         df['Num_veh_acc'][i],
                         df['Car_acc'][i],
                         df['Mc_acc'][i],
                         df['Truck_acc'][i],
                         df['Year'][i],
                         df['Quarter'][i],
                         df['T_day'][i],
                         df['Speed_limit'][i],
                         df['All_veh'][i]]
                        )