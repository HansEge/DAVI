import csv
import os
import glob
import pandas as pd

os.chdir("C:\\Users\\stinu\\Desktop\\DAVI\\Data\\US_car_accidents\\CleanedFilesUS\\")

extension = 'csv'
all_filenames = [i for i in glob.glob('*.{}'.format(extension))]
df_list = []

index_for_speed = 2009

for f in all_filenames:
    df = pd.read_csv(f)
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

    if 'VSPD_LIM' in df.columns:
        speed_df = pd.DataFrame({'Speed Limit': df['VSPD_LIM']})

        for i in range(len(df_list)):
            if df_list[i]['Year'][0] > index_for_speed:
                index_for_speed = index_for_speed + 1
                df_list[i].insert(7, 'Speed Limit', speed_df['Speed Limit'], True)
                break

# Concat all dataframes from list and drop all NaN rows of dataset
combined_df = pd.concat(df_list, ignore_index=True)
combined_df.dropna(inplace=True)
combined_df = combined_df.reset_index()

with open('US_cleaned.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['ST_CASE', 'Latitude', 'Longitude', 'Year', 'Month', 'Day', 'Hour', 'Speed Limit'])
    for i in range(len(combined_df)):
        writer.writerow([combined_df['ST_CASE'][i],
                         combined_df['Latitude'][i],
                         combined_df['Longitude'][i],
                         combined_df['Year'][i],
                         combined_df['Month'][i],
                         combined_df['Day'][i],
                         combined_df['Hour'][i],
                         combined_df['Speed Limit'][i]])
