from GET_Data import GET_RESULTS, GET_TABLE, GET_CROSS_TABLE, CREATE_CSV
import time


def GET_ALL(): 
    i = 1
    while i < 35:
        #url = "https://www.dfb.de/bundesliga/spieltagtabelle/?spieledb_path=/competitions/12/seasons/17683/matchday&spieledb_path=%2Fcompetitions%2F12%2Fseasons%2F17820%2Fmatchday%2F" + str(i)
        #url = "https://www.dfb.de/2-bundesliga/spieltagtabelle/?no_cache=1&spieledb_path=%2Fcompetitions%2F3%2Fseasons%2Fcurrent%2Fmatchday%2F" + str(i)
        #url = "https://www.dfb.de/3-liga/spieltagtabelle/?no_cache=1&spieledb_path=%2Fcompetitions%2F4%2Fseasons%2Fcurrent%2Fmatchday%2F" + str(i)
        CREATE_CSV(url)
        time.sleep(5)
        i = i + 1




#url = "https://www.dfb.de/bundesliga/spieltagtabelle/?spieledb_path=/competitions/12/seasons/17683/matchday&spieledb_path=%2Fcompetitions%2F12%2Fseasons%2F17820%2Fmatchday%2F13"
url = "https://www.dfb.de/2-bundesliga/spieltagtabelle/?no_cache=1&spieledb_path=%2Fcompetitions%2F3%2Fseasons%2Fcurrent%2Fmatchday%2F13"
#url = "https://www.dfb.de/3-liga/spieltagtabelle/?no_cache=1&spieledb_path=%2Fcompetitions%2F4%2Fseasons%2Fcurrent%2Fmatchday%2F15"



#print(GET_TABLE(url))

#print(GET_RESULTS(url))

#print(GET_CROSS_TABLE(url))
#print(GET_CROSS_TABLE(doc)[6][6])

#CREATE_CSV(url)
