from GET_Data import GET_RESULTS, GET_TABLE, GET_CROSS_TABLE, CREATE_CSV, GET_ALL
from GET_Calc import GET_ALL_GOALS, GET_ATT_DEF_VALUE, GET_ESTIMATE_GOALS, GET_POINTS, GET_SEASON, GET_STATS_FROM_CLUB, CALC_SEASON





#url = "https://www.dfb.de/bundesliga/spieltagtabelle/?spieledb_path=/competitions/12/seasons/17683/matchday&spieledb_path=%2Fcompetitions%2F12%2Fseasons%2F17820%2Fmatchday%2F13"
#url = "https://www.dfb.de/2-bundesliga/spieltagtabelle/?no_cache=1&spieledb_path=%2Fcompetitions%2F3%2Fseasons%2Fcurrent%2Fmatchday%2F3"
#url = "https://www.dfb.de/3-liga/spieltagtabelle/?no_cache=1&spieledb_path=%2Fcompetitions%2F4%2Fseasons%2Fcurrent%2Fmatchday%2F3"


#GET_ALL(url)

#print(GET_TABLE(url))

#print(GET_RESULTS(url))

#print(GET_CROSS_TABLE(url))
#print(GET_CROSS_TABLE(doc)[6][6])

#CREATE_CSV(url)





file = "./Python_Projects/Football/CSV/1_Bundesliga_2018_2019.csv"


print(GET_ALL_GOALS(file))

#print(GET_STATS_FROM_CLUB("Borussia Dortmund", file))

#print(GET_ATT_DEF_VALUE("1. FC Nürnberg", file))
#print(GET_ATT_DEF_VALUE("VfB Stuttgart", file))

#print(GET_ESTIMATE_GOALS("Borussia Dortmund", "1. FC Nürnberg", file))

#print(GET_POINTS("Borussia Dortmund", file))

#print(GET_SEASON("Borussia Dortmund", file))

#print(CALC_SEASON("Borussia Dortmund", file))




"""

from scipy.stats import poisson

# http://muthu.co/poisson-distribution-with-python/

mu = 6.39

arr = []

rv = poisson(0.56)  # Average
for num in range(0,5):
    arr.append(rv.pmf(num))

print(arr)

prob = rv.pmf(28)

"""