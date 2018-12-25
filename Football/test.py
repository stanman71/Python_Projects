import requests
from bs4 import BeautifulSoup

import csv

url = "https://www.dfb.de/bundesliga/spieltagtabelle/?spieledb_path=/competitions/12/seasons/17683/matchday&spieledb_path=/competitions/12/seasons/17820/matchday/17"

r = requests.get(url)

doc = BeautifulSoup(r.text, "html.parser")

content = doc.select_one(".cross-tab")


print(content)

