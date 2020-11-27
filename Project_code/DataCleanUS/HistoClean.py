import csv
import os
import glob
import pandas as pd
import numpy as np


os.chdir("C:\\Users\\stinu\\Desktop\\DAVI\\Data\\US_car_accidents\\Histo\\")

extension = 'csv'
all_filenames = [i for i in glob.glob('*.{}'.format(extension))]

for f in all_filenames:
    combined_df = pd.read_csv(f)

    print('Reading from', f)

    combined_df.insert(12, "All_veh", 1)

with open('US_cleaned.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Acc_index', 'Lat', 'Lon', 'Num_veh_acc', 'Car_acc',
                     'Mc_acc', 'Truck_acc', 'Other_acc',
                     'Year', 'Quarter', 'T_day', 'Speed_limit', 'All_veh'])
    for i in range(len(combined_df)):
        writer.writerow([combined_df['Acc_index'][i],
                         combined_df['Lat'][i],
                         combined_df['Lon'][i],
                         combined_df['Num_veh_acc'][i],
                         combined_df['Car_acc'][i],
                         combined_df['Mc_acc'][i],
                         combined_df['Truck_acc'][i],
                         combined_df['Other_acc'][i],
                         combined_df['Year'][i],
                         combined_df['Quarter'][i],
                         combined_df['T_day'][i],
                         combined_df['Speed_limit'][i],
                         combined_df['All_veh'][i]]
                        )