import requests
from bs4 import BeautifulSoup
import csv


#url = "https://www.dfb.de/bundesliga/spieltagtabelle/?spieledb_path=/competitions/12/seasons/17683/matchday&spieledb_path=%2Fcompetitions%2F12%2Fseasons%2F17820%2Fmatchday%2F17"
url = "https://www.dfb.de/2-bundesliga/spieltagtabelle/?no_cache=1&spieledb_path=%2Fcompetitions%2F3%2Fseasons%2Fcurrent%2Fmatchday%2F18"
#url = "https://www.dfb.de/3-liga/spieltagtabelle/?no_cache=1&spieledb_path=%2Fcompetitions%2F4%2Fseasons%2Fcurrent%2Fmatchday%2F20"

r = requests.get(url)

doc = BeautifulSoup(r.text, "html.parser")



########################
# GET_BASICINFO
########################

def GET_BasicInfo(input):

    info = []

    # LIGA

    if "bundesliga" in url:
        liga = "1_Bundesliga"

        if "2-bundesliga" in url:
            liga = "2_Bundesliga"

    if "3-liga" in url:
        liga = "3_Bundesliga"

    info.append(liga)


    # DAY

    for option in doc.find_all('option', selected=True):
        info.append(option.text)    

    return(info)




########################
# GET_RESULTS
########################

def GET_Results(input):

    data_results = GET_BasicInfo(doc)

    # RESULTS   

    content = doc.select_one(".table-match-comparison")

    for data in content.findAll('a', href=True):
        data = data.text.splitlines()

        if data != [' Vergleich'] and data != [' Schema']:       
            data_results.extend(data)

    return(data_results)



########################
# GET_Table
########################

def GET_Table(input):

    table = GET_BasicInfo(doc)

    content = input.find("div", {"id": "tabular"})

    rows = content.find_all('tr')

    for row in rows:
        cols = row.find_all('td')
        cols = [ele.text.strip() for ele in cols]

        table.append([ele for ele in cols if ele])

    return(table)




########################
# GET_Cross_Table
########################

def GET_Cross_Table(input):

    cross_table = GET_BasicInfo(doc)
  
    content = input.select_one(".cross-tab")

    # GET Clubs

    club_list = []

    for club in content.findAll('img'):
        club = club.get('title')

        if club not in club_list:  
            club_list.append(club)


    # GET Cross_Table

    rows = content.find_all('tr')

    for i, row in enumerate(rows):
        cols = row.find_all('td')
        cols = [ele.text.strip() for ele in cols]

        cross_table.append([ele for ele in cols if ele])
    
        if i < len(rows)-1:
            cross_table.append(club_list[i])
        
    return(cross_table)



########################
# Create CSV
########################

def CREATE_CSV(data):

    with open('./Python_Projects/Football/results.csv', mode='w', encoding="utf-8") as result_file:
        result_writer = csv.writer(result_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

        result_writer.writerow([data[0]])
        result_writer.writerow([data[1]])
        result_writer.writerow([data[2]])

        counter = len(data)

        for i in range (3, counter, 3):
            print(i)
            result_writer.writerow([data[i], data[i+1], data[i+2]])

        print("CSV created")




#print(GET_Results(doc))

#print(GET_Table(doc))

#CREATE_CSV(GET_Results(doc))

#print(GET_Cross_Table(doc))

#print(GET_Cross_Table(doc)[6][6])

