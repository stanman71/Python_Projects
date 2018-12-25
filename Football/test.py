import sys, csv ,operator
import codecs





file = "./Python_Projects/Football/1.Bundesliga_2018_2019.csv"




    # Sort CSV


with open(file, newline='', encoding='utf-8') as f:
    data = csv.reader(f)

    sortedlist = sorted(data, key=operator.itemgetter(0))   

    with open(file, "w", encoding="utf-8", newline='') as f:
        fileWriter = csv.writer(f, delimiter=',')
        for row in sortedlist:
            fileWriter.writerow(row)

  
