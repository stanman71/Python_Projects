import requests
from bs4 import BeautifulSoup
import sys, csv ,operator
import pandas as pd


#url = "https://www.dfb.de/bundesliga/spieltagtabelle/?spieledb_path=/competitions/12/seasons/17683/matchday&spieledb_path=%2Fcompetitions%2F12%2Fseasons%2F17820%2Fmatchday%2F13"
url = "https://www.dfb.de/2-bundesliga/spieltagtabelle/?no_cache=1&spieledb_path=%2Fcompetitions%2F3%2Fseasons%2Fcurrent%2Fmatchday%2F6"
#url = "https://www.dfb.de/3-liga/spieltagtabelle/?no_cache=1&spieledb_path=%2Fcompetitions%2F4%2Fseasons%2Fcurrent%2Fmatchday%2F15"

r = requests.get(url)

doc = BeautifulSoup(r.text, "html.parser")


########################
# GET_BASICINFO
########################

def GET_BasicInfo(input):

    info = []

    # LIGA

    if "bundesliga" in url:
        liga = "1.Bundesliga"

        if "2-bundesliga" in url:
            liga = "2.Bundesliga"

    if "3-liga" in url:
        liga = "3.Bundesliga"

    info.append(liga)


    # DAY

    for option in doc.find_all('option', selected=True):
        info.append(option.text)    

    info[2] = info[2].split(" ")[1]

    if int(info[2]) < 10:
        info[2] = "0" + info[2]

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

    season = data[1].replace("/", "_")

    file = "./Python_Projects/Football/" + data[0] + "_" + season + ".csv"

    # Check CSV

    exist_entry = False

    try:
        with open(file, newline='', encoding='utf-8') as f:
            spamreader = csv.reader(f)      

            for row in spamreader:
                if data[2] in row:
                    exist_entry = True

            if exist_entry == True:
                print("Already exist")

    except:
        pass
 

    # ADD Infos

    if exist_entry == False:
        with open(file, mode='a', encoding="utf-8", newline='') as result_file:
            result_writer = csv.writer(result_file, delimiter=',')

            counter = len(data)

            for i in range (3, counter, 3):
                goals = data[i+1].split(" : ")
                result_writer.writerow([data[2], data[i], data[i+2], goals[0], goals[1]])

            print("CSV created")

 
        # Sort CSV

        with open(file, newline='', encoding='utf-8') as f:
            data = csv.reader(f)

            sortedlist = sorted(data, key=operator.itemgetter(0))   

            with open(file, "w", encoding="utf-8", newline='') as f:
                fileWriter = csv.writer(f, delimiter=',')
                fileWriter.writerow(["Spieltag", "Team_1", "Team_2", "Tore_Team_1", "Tore_Team_2"])

                counter = len(sortedlist)

                # Case: Empty list
                if counter < 10:
                    for i, row in enumerate(sortedlist):
                        fileWriter.writerow(row)                    

                else:
                    for i, row in enumerate(sortedlist):
                        if i < counter-1:
                            fileWriter.writerow(row)
                

               
         

#print(GET_BasicInfo(doc))

#print(GET_Results(doc))

#print(GET_Table(doc))

#print(GET_Cross_Table(doc))
#print(GET_Cross_Table(doc)[6][6])

CREATE_CSV(GET_Results(doc))

