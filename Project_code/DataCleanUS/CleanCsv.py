import csv
import os
import glob
import pandas as pd

os.chdir("C:\\Users\\stinu\\Desktop\\DAVI\\Data\\US_car_accidents\\CleanedFilesUS\\")

extension = 'csv'
all_filenames = [i for i in glob.glob('*.{}'.format(extension))]
df_list = []

for f in all_filenames:
    df = pd.read_csv(f)
    if 'latitude' in df.columns:
        new_df = pd.DataFrame({'ST_CASE': df['ST_CASE'],
                               'Latitude': df['latitude'],
                               'Longitude': df['longitud'],
                               'Year': df['YEAR'],
                               'Month': df['MONTH'],
                               'Day': df['DAY'],
                               'Hour': df['HOUR']})
    else:
        new_df = pd.DataFrame({'ST_CASE': df['ST_CASE'],
                               'Latitude': df['LATITUDE'],
                               'Longitude': df['LONGITUD'],
                               'Year': df['YEAR'],
                               'Month': df['MONTH'],
                               'Day': df['DAY'],
                               'Hour': df['HOUR']})

    df_list.append(new_df)
combined_df = pd.concat(df_list, ignore_index=True)

with open('US_cleaned.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['ST_CASE', 'Latitude', 'Longitude', 'Year', 'Month', 'Day', 'Hour'])
    for i in range(len(combined_df)):
        writer.writerow([combined_df['ST_CASE'][i],
                         combined_df['Latitude'][i],
                         combined_df['Longitude'][i],
                         combined_df['Year'][i],
                         combined_df['Month'][i],
                         combined_df['Day'][i],
                         combined_df['Hour'][i]])
