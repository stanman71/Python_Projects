# Error: ImportError: Missing required dependencies ['dateutil']
# >>> Try pd.test()
# >>> pip install python-dateutil pytz --force-reinstall --upgrade


import pandas as pd
import numpy as np


def GET_ALL_GOALS(file):

    df = pd.read_csv(file, delimiter=",")

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



def GET_STATS_FROM_CLUB(Club, file):  
    
    df = pd.read_csv(file, delimiter=",")
    
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



def GET_ATT_DEF_VALUE(Club, file):

    # https://www.onlinemathe.de/forum/Fussballergebnisse-Berechnen-Formel

    # Verhältnis von den (durchschnittlichen) Heimtoren/Heimtreffern des Vereins zu den 
    # (durchschnittlichen) Heimtoren aller Vereine

    df = pd.read_csv(file, delimiter=",")

    return_list = []

    ATT_Heim = (GET_STATS_FROM_CLUB(Club, file)[3])/(GET_ALL_GOALS(file)[4])
    ATT_Heim = round(ATT_Heim, 2)
    DEF_Heim = (GET_STATS_FROM_CLUB(Club, file)[5])/(GET_ALL_GOALS(file)[6])
    DEF_Heim = round(DEF_Heim, 2)

    ATT_Aus  = (GET_STATS_FROM_CLUB(Club, file)[8])/(GET_ALL_GOALS(file)[6])
    ATT_Aus  = round(ATT_Aus, 2)
    DEF_Aus  = (GET_STATS_FROM_CLUB(Club, file)[10])/(GET_ALL_GOALS(file)[4])
    DEF_Aus  = round(DEF_Aus, 2)

    return_list.append(ATT_Heim)
    return_list.append(DEF_Heim)
    return_list.append(ATT_Aus)
    return_list.append(DEF_Aus)

    return(return_list)



def GET_ESTIMATE_GOALS(Club_1, Club_2, file):

    # https://www.onlinemathe.de/forum/Fussballergebnisse-Berechnen-Formel
    # https://www.wettstern.com/sportwetten-mathematik/poisson-saisonwetten
 
    df = pd.read_csv(file, delimiter=",")

    return_list = []

    Goals_Club_1 = GET_ATT_DEF_VALUE(Club_1, file)[0] * GET_ALL_GOALS(file)[4] * GET_ATT_DEF_VALUE(Club_2, file)[3]
    Goals_Club_1 = round(Goals_Club_1, 2)
    Goals_Club_2 = GET_ATT_DEF_VALUE(Club_1, file)[1] * GET_ALL_GOALS(file)[6] * GET_ATT_DEF_VALUE(Club_2, file)[2]
    Goals_Club_2 = round(Goals_Club_2, 2)

    return_list.append(Goals_Club_1)
    return_list.append(Goals_Club_2)   

    return(return_list)



def GET_POINTS(Club, file):

    df = pd.read_csv(file, delimiter=",")

    return_list = []    
 
    df = df[(df.Team_1 == Club) | (df.Team_2 == Club)]

    df = df.copy()

    conditions = [
        (df['Team_1'] == Club) & ((df['Tore_Team_1']) >  (df['Tore_Team_2'])),
        (df['Team_1'] == Club) & ((df['Tore_Team_1']) == (df['Tore_Team_2'])),
        (df['Team_1'] == Club) & ((df['Tore_Team_1']) <  (df['Tore_Team_2'])),
        (df['Team_2'] == Club) & ((df['Tore_Team_1']) >  (df['Tore_Team_2'])),
        (df['Team_2'] == Club) & ((df['Tore_Team_1']) == (df['Tore_Team_2'])),
        (df['Team_2'] == Club) & ((df['Tore_Team_1']) <  (df['Tore_Team_2']))]

    choices = [3, 1, 0, 0, 1, 3]
    df['Points'] = np.select(conditions, choices)
    
    Sum        = df['Points'].sum()
    Complete   = df['Points'].values.tolist()
    AVG_Points = df['Points'].mean()
    AVG_Points = round(AVG_Points, 2)

    Last_5 = Complete[-5:]
    Last_5 = sum(Last_5) / float(len(Last_5))
    Last_5 = round(Last_5, 2)

    Trend = Last_5 - AVG_Points
    Trend = round(Trend, 2)

    return_list.append(Sum)
    return_list.append(AVG_Points)
    return_list.append(Trend)        
    return_list.append(Complete)

    return(return_list)



def GET_SEASON(Club, file):

    df = pd.read_csv(file, delimiter=",")

    return_list = []
  
    df = df[(df.Team_1 == Club) | (df.Team_2 == Club)]

    Complete_1 = df['Team_1'].values.tolist()
    Complete_2 = df['Team_2'].values.tolist()

    for i in range (0, len(Complete_1)):
        return_list.append(i+1)
        return_list.append(Complete_1[i])
        return_list.append(Complete_2[i])
    
    return(return_list)



def CALC_SEASON(Club, file):

    return_list = []

    season = GET_SEASON(Club, file)

    for i in range (0, len(season), 3):
        result = GET_ESTIMATE_GOALS(season[i + 1], season[i + 2], file)

        return_list.append(season[i])

        if season[i + 1] == Club:
            return_list.append("H")
            return_list.append(season[i + 2])   # Gegner
            return_list.append(result[0])       # Tore Club
            return_list.append(result[1])       # Hits Club
        else:
            return_list.append("A")
            return_list.append(season[i + 1])   # Gegner
            return_list.append(result[1])       # Tore Club
            return_list.append(result[0])       # Hits Club

    return(return_list)
