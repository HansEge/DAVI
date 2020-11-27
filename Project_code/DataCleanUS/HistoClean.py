import csv
import os
import glob
import pandas as pd
import numpy as np


os.chdir("C:\\Users\\stinu\\Desktop\\DAVI\\Data\\US_car_accidents\\CleanedFilesUS\\")

extension = 'csv'
all_filenames = [i for i in glob.glob('*.{}'.format(extension))]
df_list = []

# Used to get speed limit from vehicle.csv because data has different structure for different years :(
index_for_speed = 2009

for f in all_filenames:
    df = pd.read_csv(f)
    # Get stuff from ACCIDENT.CSV

    print('Reading from', f)

    if 'YEAR' in df.columns:
        if df['YEAR'][0] < 2008:
            new_df = pd.DataFrame({'Acc_index': df['ST_CASE'],
                                   'Year': df['YEAR'],
                                   'Month': df['MONTH'],
                                   'Day': df['DAY'],
                                   'Hour': df['HOUR'],
                                   'Speed_limit': df['SP_LIMIT']})

        elif 2007 < df['YEAR'][0] < 2010:
            new_df = pd.DataFrame({'Acc_index': df['ST_CASE'],
                                   'Year': df['YEAR'],
                                   'Month': df['MONTH'],
                                   'Day': df['DAY'],
                                   'Hour': df['HOUR'],
                                   'Speed_limit': df['SP_LIMIT']})

        if df['YEAR'][0] > 2009:
            new_df = pd.DataFrame({'Acc_index': df['ST_CASE'],
                                   'Year': df['YEAR'],
                                   'Month': df['MONTH'],
                                   'Day': df['DAY'],
                                   'Hour': df['HOUR']})

        df_list.append(new_df)

    # Get stuff from VEHICLES.CSV
    if 'VEH_NO' in df.columns:

        # Due to FARS changing datastructure from 2009-14 speed limit must be obtained from VEHICLES.CSV :(
        if 'VSPD_LIM' in df.columns:

            speed_limit = pd.DataFrame({'Speed_limit': df['VSPD_LIM']})

            for i in range(len(df_list)):
                if df_list[i]['Year'][0] > index_for_speed:
                    index_for_speed = index_for_speed + 1
                    df_list[i].insert(5, 'Speed_limit', speed_limit['Speed_limit'], True)

        # Extract number of vehicles in each accident
        veh_in_acc = pd.DataFrame({'NO_VEH': df['ST_CASE']})
        veh_in_acc = pd.DataFrame({'Num_veh_acc': veh_in_acc.groupby(['NO_VEH']).size()
                                  .reset_index()[0]})

        for i in range(len(df_list)):
            # Add "Vehicles in accident" to the correct dataframe
            if len(df_list[i]) == len(veh_in_acc):
                df_list[i].insert(6, 'Num_veh_acc', veh_in_acc['Num_veh_acc'],
                                  True)

# Concat all dataframes from list and drop all NaN rows of dataset
combined_df = pd.concat(df_list, ignore_index=True)
combined_df.dropna(inplace=True)
combined_df = combined_df.reset_index()

# Make new cleaned CSV file
with open('US_cleaned_histo.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Acc_index', 'Year', 'Month', 'Day', 'Hour', 'Speed_limit', 'Num_veh_acc'])
    for i in range(len(combined_df)):
        writer.writerow([combined_df['Acc_index'][i],
                         combined_df['Year'][i],
                         combined_df['Month'][i],
                         combined_df['Day'][i],
                         combined_df['Hour'][i],
                         combined_df['Speed_limit'][i],
                         combined_df['Num_veh_acc'][i]]
                        )
