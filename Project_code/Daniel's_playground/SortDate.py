import pandas as pd

path_uk = "C:\\Users\\danie\\Desktop\\Skole\\DataVisualization\\project_data\\UK_car_accidents\\"

uk_acc = pd.read_csv(path_uk + "Accidents0515.csv")
'''
day_list = []
month_list = []
year_list = []

df = pd.DataFrame({'Date': uk_acc["Date"]})

for i in range(len(df)):
    df["Date"].values[i]=df["Date"].values[i].split('/')
    day_list.append(int(df["Date"].values[i][0]))
    month_list.append(int(df["Date"].values[i][1]))
    year_list.append(int(df["Date"].values[i][2]))


df2 = pd.DataFrame({'Day': day_list,
                    'Month': month_list,
                    'Year': year_list})
print(df2)
'''
Hour_list = []


df = pd.DataFrame({'Time': uk_acc["Time"]})
df = df.dropna()
for i in range(len(df)):
    df["Time"].values[i] = df["Time"].values[i].split(':')
    Hour_list.append(int(df["Time"].values[i][0]))

df2 = pd.DataFrame({'Hour': Hour_list})
print(df2)
    #df["Time"].values[i]=df["Date"].values[i].split('/')