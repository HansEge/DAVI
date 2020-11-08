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
    if 'YEAR' in df.columns:
        if df['YEAR'][0] < 2008:
            new_df = pd.DataFrame({'ST_CASE': df['ST_CASE'],
                                   'Latitude': df['latitude'],
                                   'Longitude': df['longitud'],
                                   'Year': df['YEAR'],
                                   'Month': df['MONTH'],
                                   'Day': df['DAY'],
                                   'Hour': df['HOUR'],
                                   'Speed Limit': df['SP_LIMIT']})

        elif 2007 < df['YEAR'][0] < 2010:
            new_df = pd.DataFrame({'ST_CASE': df['ST_CASE'],
                                   'Latitude': df['LATITUDE'],
                                   'Longitude': df['LONGITUD'],
                                   'Year': df['YEAR'],
                                   'Month': df['MONTH'],
                                   'Day': df['DAY'],
                                   'Hour': df['HOUR'],
                                   'Speed Limit': df['SP_LIMIT']})

        if df['YEAR'][0] > 2009:
            new_df = pd.DataFrame({'ST_CASE': df['ST_CASE'],
                                   'Latitude': df['LATITUDE'],
                                   'Longitude': df['LONGITUD'],
                                   'Year': df['YEAR'],
                                   'Month': df['MONTH'],
                                   'Day': df['DAY'],
                                   'Hour': df['HOUR'],})
        df_list.append(new_df)

    # Get stuff from VEHICLES.CSV
    if 'VEH_NO' in df.columns:

        # Due to FARS changing datastructure in from 2009-14 :(
        if 'VSPD_LIM' in df.columns:
            speed_df = pd.DataFrame({'Speed Limit': df['VSPD_LIM']})
            for i in range(len(df_list)):
                if df_list[i]['Year'][0] > index_for_speed:
                    index_for_speed = index_for_speed + 1
                    df_list[i].insert(7, 'Speed Limit', speed_df['Speed Limit'], True)

        # Extract number of vehicles in each accident
        veh_in_acc = pd.DataFrame({'NO_VEH': df['ST_CASE']})
        veh_in_acc = pd.DataFrame({'Number of vehicles in accident': veh_in_acc.groupby(['NO_VEH']).size()
                                  .reset_index()[0]})

        # PURE EVIL CANCER!
        car_involved = pd.DataFrame({'BODY_TYP': df['BODY_TYP'],
                                     'ST_CASE': df['ST_CASE']})
        tmp = car_involved.query('BODY_TYP > 11')['BODY_TYP']
        car_involved = pd.DataFrame({'Car_involved': tmp.reindex(range(len(car_involved)), fill_value=1)})
        car_involved = car_involved.query('Car_involved < 2').reindex(range(len(car_involved)), fill_value=0)
        car_involved.insert(1, 'ST_CASE', df['ST_CASE'])

        for i in range(len(car_involved)):
            if car_involved['ST_CASE'][i] == car_involved['ST_CASE'][i+1]:
                if car_involved['Car_involved'][i] != car_involved['Car_involved'][i+1]:
                    car_involved.drop(car_involved.index[i], inplace=True)

        m1 = car_involved['ST_CASE'].duplicated(keep=False)
        m2 = car_involved['Car_involved'] == 0

        car_involved = car_involved[~(m1 & m2)]

        car_involved = car_involved.drop_duplicates(subset=('ST_CASE')).reset_index(drop=True)
        car_involved.drop(columns='ST_CASE', inplace=True)

        # Add stuff to dataframe list
        for i in range(len(df_list)):
            # Add "Vehicles in accident" to the correct dataframe
            if len(df_list[i]) == len(veh_in_acc):
                df_list[i].insert(3, 'Number of vehicles in accident', veh_in_acc['Number of vehicles in accident'],
                                  True)
            if len(df_list[i]) == len(car_involved):
                df_list[i].insert(4, 'Car_involved', car_involved['Car_involved'], True)


# Concat all dataframes from list and drop all NaN rows of dataset
combined_df = pd.concat(df_list, ignore_index=True)
combined_df.dropna(inplace=True)
combined_df = combined_df.reset_index()

# Make new cleaned CSV file
with open('US_cleaned.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['ST_CASE', 'Latitude', 'Longitude', 'Number of vehicles in accident', 'Car_involved', 'Year', 'Month', 'Day', 'Hour', 'Speed Limit'])
    for i in range(len(combined_df)):
        writer.writerow([combined_df['ST_CASE'][i],
                         combined_df['Latitude'][i],
                         combined_df['Longitude'][i],
                         combined_df['Number of vehicles in accident'][i],
                         combined_df['Car_involved'][i],
                         combined_df['Year'][i],
                         combined_df['Month'][i],
                         combined_df['Day'][i],
                         combined_df['Hour'][i],
                         combined_df['Speed Limit'][i]])
