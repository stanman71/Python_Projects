# Error: ImportError: Missing required dependencies ['dateutil']
# >>> Try pd.test()
# >>> pip install python-dateutil pytz --force-reinstall --upgrade


import pandas as pd



def GET_ALL_GOALS(df):

    return_list = []

    Sum = int(df.shape[0] / 9)

    df_1         = df["Tore_Team_1"]
    Heim         = df_1.sum()
    Heim_AVG     = df_1.mean()
    Heim_AVG     = round(Heim_AVG, 2)

    df_2         = df["Tore_Team_2"]
    Aus          = df_2.sum()
    Aus_AVG      = df_2.mean()
    Aus_AVG      = round(Aus_AVG, 2)

    Complete     = Heim + Aus
    Complete_AVG = Heim_AVG + Aus_AVG

    return_list.append(Sum)
    return_list.append(Complete)
    return_list.append(Complete_AVG) 
    return_list.append(Heim)
    return_list.append(Heim_AVG)
    return_list.append(Aus)
    return_list.append(Aus_AVG)

    return(return_list)



def GET_STATS_FROM_CLUB(Club, df):  
    
    return_list = []    
 
    df_heim_0 = df.loc[df['Team_1'] == Club]
    Sum_Heim = df_heim_0.shape[0]

    df_aus_0 = df.loc[df['Team_2'] == Club]  
    Sum_Aus = df_aus_0.shape[0]

    Sum = Sum_Heim + Sum_Aus

    df_heim_1      = df_heim_0["Tore_Team_1"]
    Heim_Goals     = df_heim_1.sum()
    Heim_Goals_AVG = df_heim_1.mean()
    Heim_Goals_AVG = round(Heim_Goals_AVG, 2)
  
    df_heim_2      = df_heim_0["Tore_Team_2"]
    Heim_Hits      = df_heim_2.sum()
    Heim_Hits_AVG  = df_heim_2.mean()
    Heim_Hits_AVG  = round(Heim_Hits_AVG, 2)

    df_aus_1       = df_aus_0["Tore_Team_2"]
    Aus_Goals      = df_aus_1.sum()
    Aus_Goals_AVG  = df_aus_1.mean()
    Aus_Goals_AVG  = round(Aus_Goals_AVG, 2)

    df_aus_2       = df_aus_0["Tore_Team_1"]
    Aus_Hits       = df_aus_2.sum()
    Aus_Hits_AVG   = df_aus_2.mean()
    Aus_Hits_AVG   = round(Aus_Hits_AVG, 2)

    return_list.append(Sum)
    return_list.append(Sum_Heim)
    return_list.append(Heim_Goals) 
    return_list.append(Heim_Goals_AVG)
    return_list.append(Heim_Hits)
    return_list.append(Heim_Hits_AVG)
    return_list.append(Sum_Aus)
    return_list.append(Aus_Goals) 
    return_list.append(Aus_Goals_AVG)
    return_list.append(Aus_Hits)
    return_list.append(Aus_Hits_AVG)

    return(return_list)   



def GET_ATT_DEF_VALUE(Club, df):

    # https://www.onlinemathe.de/forum/Fussballergebnisse-Berechnen-Formel

    # Verhältnis von den (durchschnittlichen) Heimtoren/Heimtreffern des Vereins zu den 
    # (durchschnittlichen) Heimtoren aller Vereine

    return_list = []

    ATT_Heim = (GET_STATS_FROM_CLUB(Club, df)[3])/(GET_ALL_GOALS(df)[4])
    ATT_Heim = round(ATT_Heim, 2)
    DEF_Heim = (GET_STATS_FROM_CLUB(Club, df)[5])/(GET_ALL_GOALS(df)[4])
    DEF_Heim = round(DEF_Heim, 2)

    ATT_Aus  = (GET_STATS_FROM_CLUB(Club, df)[8])/(GET_ALL_GOALS(df)[6])
    ATT_Aus  = round(ATT_Aus, 2)
    DEF_Aus  = (GET_STATS_FROM_CLUB(Club, df)[10])/(GET_ALL_GOALS(df)[6])
    DEF_Aus  = round(DEF_Aus, 2)

    return_list.append(ATT_Heim)
    return_list.append(DEF_Heim)
    return_list.append(ATT_Aus)
    return_list.append(DEF_Aus)

    return(return_list)



def GET_APP_GOALS(Club_1, Club_2, df):

    # https://www.onlinemathe.de/forum/Fussballergebnisse-Berechnen-Formel
 
    return_list = []

    Goals_Club_1 = GET_ATT_DEF_VALUE(Club_1, df)[0] * GET_ALL_GOALS(df)[2] * GET_ATT_DEF_VALUE(Club_2, df)[3]
    Goals_Club_1 = round(Goals_Club_1, 2)
    Goals_Club_2 = GET_ATT_DEF_VALUE(Club_1, df)[1] * GET_ALL_GOALS(df)[2] * GET_ATT_DEF_VALUE(Club_2, df)[2]
    Goals_Club_2 = round(Goals_Club_2, 2)

    return_list.append(Goals_Club_1)
    return_list.append(Goals_Club_2)   

    return(return_list)





file = "./Python_Projects/Football/CSV/1_Bundesliga_2018_2019.csv"
df   = pd.read_csv(file, delimiter=",")



#print(GET_ALL_GOALS(df))

#print(GET_STATS_FROM_CLUB("FC Augsburg", df))

print(GET_ATT_DEF_VALUE("Bayern München", df))

print(GET_APP_GOALS("Borussia Dortmund", "Bayern München", df))