import pandas as pd

path_uk = "C:\\Users\\danie\\Desktop\\Skole\\DataVisualization\\project_data\\UK_car_accidents\\"

uk_acc = pd.read_csv(path_uk + "Accidents0515.csv")

df = pd.DataFrame({'Date': uk_acc["Date"]})


data=df.iloc[0,0].split('/')

print(int(data[0]))