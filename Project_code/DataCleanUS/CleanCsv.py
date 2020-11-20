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

            # Extract month and group into quarters
            months = pd.DataFrame({'Months': df['MONTH'], 'Acc_index': df['ST_CASE']})
            q1 = months.query('Months < 4')['Months']
            q2 = months.query('Months > 3 and Months < 7')['Months']
            q3 = months.query('Months > 6 and Months < 10')['Months']
            q4 = months.query('Months > 9 and Months < 13')['Months']

            q1.replace([1, 2, 3], 0, inplace=True)
            q2.replace([4, 5, 6], 1, inplace=True)
            q3.replace([7, 8, 9], 2, inplace=True)
            q4.replace([10, 11, 12], 3, inplace=True)

            frames = [q1, q2, q3, q4]
            quarters = pd.DataFrame({'Quarters': pd.concat(frames)})
            quarters = quarters.reindex(range(len(quarters)))

            # Extract hour and group into time of day(0-2)
            t_day = pd.DataFrame({'T_day': df['HOUR'], 'Acc_index': df['ST_CASE']})
            t_0 = t_day.query('T_day > 21 or T_day >= 0 and T_day < 6')['T_day']
            t_1 = t_day.query('T_day > 5 and T_day < 14')['T_day']
            t_2 = t_day.query('T_day > 13 and T_day < 22')['T_day']

            t_0.replace(t_0.unique(), 0, inplace=True)
            t_1.replace(t_1.unique(), 1, inplace=True)
            t_2.replace(t_2.unique(), 2, inplace=True)

            frames = [t_0, t_1, t_2]
            t_day = pd.DataFrame({'T_day': pd.concat(frames)})
            t_day = t_day.reindex(range(len(t_day)))

            # Extract speed limit and group into low, medium and high
            speed_limit = pd.DataFrame({'Speed_limit': df['SP_LIMIT']})
            s_0 = speed_limit.query('Speed_limit < 36')['Speed_limit']
            s_1 = speed_limit.query('Speed_limit > 35 and Speed_limit < 60')['Speed_limit']
            s_2 = speed_limit.query('Speed_limit > 59 and Speed_limit < 99')['Speed_limit']

            s_0.replace(s_0.unique(), 0, inplace=True)
            s_1.replace(s_1.unique(), 1, inplace=True)
            s_2.replace(s_2.unique(), 2, inplace=True)

            frames = [s_0, s_1, s_2]
            speed_limit = pd.DataFrame({'Speed_limit': pd.concat(frames)})
            speed_limit = speed_limit.reindex(range(len(speed_limit)))

            new_df = pd.DataFrame({'ST_CASE': df['ST_CASE'],
                                   'Latitude': df['latitude'],
                                   'Longitude': df['longitud'],
                                   'Year': df['YEAR'],
                                   'Quarter': quarters['Quarters'],
                                   'T_day': t_day['T_day'],
                                   'Speed_limit': speed_limit['Speed_limit'],
                                   'Day': df['DAY']})

        elif 2007 < df['YEAR'][0] < 2010:

            # Extract month and group into quarters
            months = pd.DataFrame({'Months': df['MONTH'], 'Acc_index': df['ST_CASE']})
            q1 = months.query('Months < 4')['Months']
            q2 = months.query('Months > 3 and Months < 7')['Months']
            q3 = months.query('Months > 6 and Months < 10')['Months']
            q4 = months.query('Months > 9 and Months < 13')['Months']

            q1.replace([1, 2, 3], 0, inplace=True)
            q2.replace([4, 5, 6], 1, inplace=True)
            q3.replace([7, 8, 9], 2, inplace=True)
            q4.replace([10, 11, 12], 3, inplace=True)

            frames = [q1, q2, q3, q4]
            quarters = pd.DataFrame({'Quarters': pd.concat(frames)})
            quarters = quarters.reindex(range(len(quarters)))

            # Extract hour and group into time of day(0-2)
            t_day = pd.DataFrame({'T_day': df['HOUR'], 'Acc_index': df['ST_CASE']})
            t_0 = t_day.query('T_day > 21 or T_day >= 0 and T_day < 6')['T_day']
            t_1 = t_day.query('T_day > 5 and T_day < 14')['T_day']
            t_2 = t_day.query('T_day > 13 and T_day < 22')['T_day']

            t_0.replace(t_0.unique(), 0, inplace=True)
            t_1.replace(t_1.unique(), 1, inplace=True)
            t_2.replace(t_2.unique(), 2, inplace=True)

            frames = [t_0, t_1, t_2]
            t_day = pd.DataFrame({'T_day': pd.concat(frames)})
            t_day = t_day.reindex(range(len(t_day)))

            # Extract speed limit and group into low, medium and high
            speed_limit = pd.DataFrame({'Speed_limit': df['SP_LIMIT']})
            s_0 = speed_limit.query('Speed_limit < 36')['Speed_limit']
            s_1 = speed_limit.query('Speed_limit > 35 and Speed_limit < 60')['Speed_limit']
            s_2 = speed_limit.query('Speed_limit > 59 and Speed_limit < 99')['Speed_limit']

            s_0.replace(s_0.unique(), 0, inplace=True)
            s_1.replace(s_1.unique(), 1, inplace=True)
            s_2.replace(s_2.unique(), 2, inplace=True)

            frames = [s_0, s_1, s_2]
            speed_limit = pd.DataFrame({'Speed_limit': pd.concat(frames)})
            speed_limit = speed_limit.reindex(range(len(speed_limit)))

            new_df = pd.DataFrame({'ST_CASE': df['ST_CASE'],
                                   'Latitude': df['LATITUDE'],
                                   'Longitude': df['LONGITUD'],
                                   'Year': df['YEAR'],
                                   'Quarter': quarters['Quarters'],
                                   'T_day': t_day['T_day'],
                                   'Speed_limit': speed_limit['Speed_limit'],
                                   'Day': df['DAY']})

        if df['YEAR'][0] > 2009:

            # Extract month and group into quarters
            months = pd.DataFrame({'Months': df['MONTH'], 'Acc_index': df['ST_CASE']})
            q1 = months.query('Months < 4')['Months']
            q2 = months.query('Months > 3 and Months < 7')['Months']
            q3 = months.query('Months > 6 and Months < 10')['Months']
            q4 = months.query('Months > 9 and Months < 13')['Months']

            q1.replace([1, 2, 3], 0, inplace=True)
            q2.replace([4, 5, 6], 1, inplace=True)
            q3.replace([7, 8, 9], 2, inplace=True)
            q4.replace([10, 11, 12], 3, inplace=True)

            frames = [q1, q2, q3, q4]
            quarters = pd.DataFrame({'Quarters': pd.concat(frames)})
            quarters = quarters.reindex(range(len(quarters)))

            # Extract hour and group into time of day(0-2)
            t_day = pd.DataFrame({'T_day': df['HOUR'], 'Acc_index': df['ST_CASE']})
            t_0 = t_day.query('T_day > 21 or T_day >= 0 and T_day < 6')['T_day']
            t_1 = t_day.query('T_day > 5 and T_day < 14')['T_day']
            t_2 = t_day.query('T_day > 13 and T_day < 22')['T_day']

            t_0.replace(t_0.unique(), 0, inplace=True)
            t_1.replace(t_1.unique(), 1, inplace=True)
            t_2.replace(t_2.unique(), 2, inplace=True)

            frames = [t_0, t_1, t_2]
            t_day = pd.DataFrame({'T_day': pd.concat(frames)})
            t_day = t_day.reindex(range(len(t_day)))




            new_df = pd.DataFrame({'ST_CASE': df['ST_CASE'],
                                   'Latitude': df['LATITUDE'],
                                   'Longitude': df['LONGITUD'],
                                   'Year': df['YEAR'],
                                   'Quarter': quarters['Quarters'],
                                   'T_day': t_day['T_day'],
                                   'Day': df['DAY']})
        df_list.append(new_df)

    # Get stuff from VEHICLES.CSV
    if 'VEH_NO' in df.columns:
        # Due to FARS changing datastructure from 2009-14 speed limit must be obtained from VEHICLES.CSV :(
        if 'VSPD_LIM' in df.columns:
            speed_limit = pd.DataFrame({'Speed_limit': df['VSPD_LIM']})

            s_0 = speed_limit.query('Speed_limit < 36')['Speed_limit']
            s_1 = speed_limit.query('Speed_limit > 35 and Speed_limit < 60')['Speed_limit']
            s_2 = speed_limit.query('Speed_limit > 59 and Speed_limit < 99')['Speed_limit']

            s_0.replace(s_0.unique(), 0, inplace=True)
            s_1.replace(s_1.unique(), 1, inplace=True)
            s_2.replace(s_2.unique(), 2, inplace=True)

            frames = [s_0, s_1, s_2]
            speed_limit = pd.DataFrame({'Speed_limit': pd.concat(frames)})
            speed_limit = speed_limit.reindex(range(len(speed_limit)))


            for i in range(len(df_list)):
                if df_list[i]['Year'][0] > index_for_speed:
                    index_for_speed = index_for_speed + 1
                    df_list[i].insert(7, 'Speed_limit', speed_limit['Speed_limit'], True)

        # Extract number of vehicles in each accident
        veh_in_acc = pd.DataFrame({'NO_VEH': df['ST_CASE']})
        veh_in_acc = pd.DataFrame({'Number of vehicles in accident': veh_in_acc.groupby(['NO_VEH']).size()
                                  .reset_index()[0]})

        # PURE EVIL CANCER!

        # Only look at cars(1-11 + 17) and pickups(30-39) here
        car_involved = pd.DataFrame({'BODY_TYP': df['BODY_TYP'], 'ST_CASE': df['ST_CASE']})
        tmp = \
        car_involved.query('(0 < BODY_TYP and 12 > BODY_TYP) or 17 == BODY_TYP or (29 < BODY_TYP and 40 > BODY_TYP)')[
            'BODY_TYP']
        car_involved = pd.DataFrame({'Car_involved': tmp.reindex(range(len(car_involved)), fill_value=0)})
        car_involved = car_involved.query('Car_involved == 0').reindex(range(len(car_involved)), fill_value=1)
        car_involved.insert(1, 'ST_CASE', df['ST_CASE'])

        # Only look at motorcycles(80-89) here
        motorcycle_involved = pd.DataFrame({'BODY_TYP': df['BODY_TYP'], 'ST_CASE': df['ST_CASE']})
        tmp = motorcycle_involved.query('79 < BODY_TYP and 90 > BODY_TYP')['BODY_TYP']
        motorcycle_involved = pd.DataFrame(
            {'Motorcycle_involved': tmp.reindex(range(len(motorcycle_involved)), fill_value=0)})
        motorcycle_involved = motorcycle_involved.query('Motorcycle_involved == 0').reindex(
            range(len(motorcycle_involved)), fill_value=1)
        motorcycle_involved.insert(1, 'ST_CASE', df['ST_CASE'])

        # Only look at trucks(60-79) here
        trucks_involved = pd.DataFrame({'BODY_TYP': df['BODY_TYP'], 'ST_CASE': df['ST_CASE']})
        tmp = trucks_involved.query('59 < BODY_TYP and  80 > BODY_TYP')['BODY_TYP']
        trucks_involved = pd.DataFrame({'Trucks_involved': tmp.reindex(range(len(trucks_involved)), fill_value=0)})
        trucks_involved = trucks_involved.query('Trucks_involved == 0').reindex(range(len(trucks_involved)),
                                                                                fill_value=1)
        trucks_involved.insert(1, 'ST_CASE', df['ST_CASE'])

        # Only look at other vehicles here
        other_involved = pd.DataFrame({'BODY_TYP': df['BODY_TYP'], 'ST_CASE': df['ST_CASE']})
        tmp = other_involved.query('(11 < BODY_TYP and 17 > BODY_TYP) or (17 < BODY_TYP and 30 > BODY_TYP) or '
                                   '(39 < BODY_TYP and 60 > BODY_TYP) or (89 < BODY_TYP and 100 > BODY_TYP)')[
            'BODY_TYP']
        other_involved = pd.DataFrame({'Other_involved': tmp.reindex(range(len(other_involved)), fill_value=0)})
        other_involved = other_involved.query('Other_involved == 0').reindex(range(len(other_involved)), fill_value=1)
        other_involved.insert(1, 'ST_CASE', df['ST_CASE'])

        # Create final dataframes and add to dataframe list
        car_involved_final = pd.DataFrame(np.zeros((len(car_involved.drop_duplicates(subset=('ST_CASE')).reset_index(
            drop=True)), 1)), columns=['Car_involved_in_accident'])
        motorcycle_involved_final = pd.DataFrame(np.zeros((len(motorcycle_involved.drop_duplicates(
            subset=('ST_CASE')).reset_index(drop=True)), 1)), columns=['Motorcycle_involved_in_accident'])
        trucks_involved_final = pd.DataFrame(np.zeros((len(trucks_involved.drop_duplicates(
            subset=('ST_CASE')).reset_index(drop=True)), 1)), columns=['Truck_involved_in_accident'])
        other_involved_final = pd.DataFrame(np.zeros((len(other_involved.drop_duplicates(
            subset=('ST_CASE')).reset_index(drop=True)), 1)), columns=['Other_vehicle_involved_in_accident'])

        # Get all ST_CASE ids
        ids = car_involved.drop_duplicates(subset=('ST_CASE')).reset_index(drop=True)['ST_CASE']

        # TODO: Vectorize this operation
        for i in range(len(ids)):
            id = ids[i]
            for k in range(car_involved[car_involved.ST_CASE == id].shape[0]):
                if car_involved[car_involved.ST_CASE == id].iloc[k]['Car_involved'] != 0:
                    car_involved_final.at[i, 'Car_involved_in_accident'] = 1
                if motorcycle_involved[motorcycle_involved.ST_CASE == id].iloc[k]['Motorcycle_involved'] != 0:
                    motorcycle_involved_final.at[i, 'Motorcycle_involved_in_accident'] = 1
                if trucks_involved[trucks_involved.ST_CASE == id].iloc[k]['Trucks_involved'] != 0:
                    trucks_involved_final.at[i, 'Truck_involved_in_accident'] = 1
                if other_involved[other_involved.ST_CASE == id].iloc[k]['Other_involved'] != 0:
                    other_involved_final.at[i, 'Other_involved_in_accident'] = 1

        print("Done with", f)

        # Add stuff to dataframe list
        for i in range(len(df_list)):
            # Add "Vehicles in accident" to the correct dataframe
            if len(df_list[i]) == len(veh_in_acc):
                df_list[i].insert(3, 'Number of vehicles in accident', veh_in_acc['Number of vehicles in accident'],
                                  True)
            if len(df_list[i]) == len(car_involved_final):
                df_list[i].insert(4, 'Car_involved_in_accident', car_involved_final['Car_involved_in_accident'], True)
                df_list[i].insert(5, 'Motorcycle_involved_in_accident',
                                  motorcycle_involved_final['Motorcycle_involved_in_accident'], True)
                df_list[i].insert(6, 'Truck_involved_in_accident', trucks_involved_final['Truck_involved_in_accident'],
                                  True)
                df_list[i].insert(7, 'Other_involved_in_accident', other_involved_final['Other_involved_in_accident'],
                                  True)

# Concat all dataframes from list and drop all NaN rows of dataset
combined_df = pd.concat(df_list, ignore_index=True)
combined_df.dropna(inplace=True)
combined_df = combined_df.reset_index()

# Make new cleaned CSV file
with open('US_cleaned.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Acc_index', 'Lat', 'Lon', 'Num_veh_acc', 'Car_acc',
                     'Mc_acc', 'Truck_acc', 'Other_acc',
                     'Year', 'Quarter', 'T_day', 'Speed_limit'])
    for i in range(len(combined_df)):
        writer.writerow([combined_df['ST_CASE'][i],
                         combined_df['Latitude'][i],
                         combined_df['Longitude'][i],
                         combined_df['Number of vehicles in accident'][i],
                         combined_df['Car_involved_in_accident'][i],
                         combined_df['Motorcycle_involved_in_accident'][i],
                         combined_df['Truck_involved_in_accident'][i],
                         combined_df['Other_involved_in_accident'][i],
                         combined_df['Year'][i],
                         combined_df['Quarter'][i],
                         combined_df['T_day'][i],
                         combined_df['Speed_limit'][i]]
                        )
