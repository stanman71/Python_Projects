import requests
from bs4 import BeautifulSoup

import csv

url = "https://www.dfb.de/2-bundesliga/spieltagtabelle/?no_cache=1"

r = requests.get(url)

doc = BeautifulSoup(r.text, "html.parser")





def GET_Table(input):

    table = []

    content = input.find("div", {"id": "tabular"})

    rows = content.find_all('tr')

    for row in rows:
        cols = row.find_all('td')
        cols = [ele.text.strip() for ele in cols]

        table.append([ele for ele in cols if ele])

    return(table)

print(GET_Table(doc))