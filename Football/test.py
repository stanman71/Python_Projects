# Error: ImportError: Missing required dependencies ['dateutil']
# >>> Try pd.test()
# >>> pip install python-dateutil pytz --force-reinstall --upgrade


import pandas as pd


df = pd.read_csv("./Python_Projects/Football/2.Bundesliga_2018_2019.csv", delimiter=",")

print(df[["Spieltag", "Team_1", "Tore_Team_1"]])

