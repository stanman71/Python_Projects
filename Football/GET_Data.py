import requests
from bs4 import BeautifulSoup
import sys, csv ,operator


########################
# GET_BASICINFO
########################

def GET_BASICINFO(url, doc):
 
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

    info[2] = info[2].split(" ")[1]

    if int(info[2]) < 10:
        info[2] = "0" + info[2]

    return(info)




########################
# GET_RESULTS
########################

def GET_RESULTS(url):

    r = requests.get(url)
    doc = BeautifulSoup(r.text, "html.parser")

    data_results = GET_BASICINFO(url, doc)

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

def GET_TABLE(url):

    r = requests.get(url)
    doc = BeautifulSoup(r.text, "html.parser")

    table = GET_BASICINFO(url, doc)

    content = doc.find("div", {"id": "tabular"})

    rows = content.find_all('tr')

    for row in rows:
        cols = row.find_all('td')
        cols = [ele.text.strip() for ele in cols]

        table.append([ele for ele in cols if ele])

    return(table)




########################
# GET_Cross_Table
########################

def GET_CROSS_TABLE(url):

    r = requests.get(url)
    doc = BeautifulSoup(r.text, "html.parser")

    cross_table = GET_BASICINFO(url, doc)

    content = doc.select_one(".cross-tab")

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

def CREATE_CSV(url):

    data = GET_RESULTS(url)

    season = data[1].replace("/", "_")

    file = "./Python_Projects/Football/CSV/" + data[0] + "_" + season + ".csv"

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

    if exist_entry == False and not "- : -" in data[4]:
        with open(file, mode='a', encoding="utf-8", newline='') as result_file:
            result_writer = csv.writer(result_file, delimiter=',')

            counter = len(data)

            for i in range (3, counter, 3):
                goals = data[i+1].split(" : ")
                result_writer.writerow([data[2], data[i], data[i+2], goals[0], goals[1]])
                # data[2]   > Spieltag
                # data[i]   > Team_1
                # data[i+2] > Team_2 
                # goals[0]  > Tore_Team_1
                # goals[1]  > Tore_Team_2

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
                    for row in sortedlist:
                        fileWriter.writerow(row)                    

                else:
                    for i, row in enumerate(sortedlist):
                        if i < counter-1:
                            fileWriter.writerow(row)
