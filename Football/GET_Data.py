import requests
from bs4 import BeautifulSoup

import csv

url = "https://www.dfb.de/bundesliga/spieltagtabelle/?spieledb_path=/competitions/12/seasons/17683/matchday&spieledb_path=/competitions/12/seasons/17820/matchday/17"

r = requests.get(url)

doc = BeautifulSoup(r.text, "html.parser")



########################
# LIGA
########################

if "bundesliga" in url:
    liga = "1_Bundesliga"

    if "2-bundesliga" in url:
        liga = "2_Bundesliga"

#print (liga)



########################
# DAY
########################

gameday = []

for option in doc.find_all('option', selected=True):
    gameday.append(option.text)

#print(gameday)



########################
# RESULTS
########################

content = doc.select_one(".table-match-comparison")

data_list = []

for data in content.findAll('a', href=True):
    data = data.text.splitlines()

    if data != [' Vergleich'] and data != [' Schema']:       
        data_list.extend(data)

#print(data_list)



########################
# Create CSV
########################


with open('./Python_Projects/Football/results.csv', mode='w', encoding="utf-8") as result_file:
    result_writer = csv.writer(result_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

    result_writer.writerow([liga])
    result_writer.writerow([gameday[0]])
    result_writer.writerow([gameday[1]])

    counter = len(data_list)

    for i in range (0, counter, 3):
        result_writer.writerow([data_list[i], data_list[i+1], data_list[i+2]])

    print("CSV created")



