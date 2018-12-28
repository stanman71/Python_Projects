from GET_Data import GET_RESULTS, GET_TABLE, GET_CROSS_TABLE, CREATE_CSV, GET_ALL
from GET_Calc import GET_ALL_GOALS, GET_ATT_DEF_VALUE, GET_ESTIMATE_GOALS_POISSON , GET_POINTS, GET_SEASON, GET_STATS_FROM_CLUB, CALC_SEASON_POISSON

from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap 

import matplotlib.pyplot as plt
import io
import base64


url  = "https://www.dfb.de/bundesliga/spieltagtabelle/?spieledb_path=/competitions/12/seasons/17683/matchday&spieledb_path=%2Fcompetitions%2F12%2Fseasons%2F17820%2Fmatchday%2F13"
file = "./Python_Projects/Football/CSV/1_Bundesliga_2018_2019.csv"


app = Flask(__name__)
Bootstrap(app)



def build_graph(x_coordinates, y_coordinates):
    img = io.BytesIO()
    plt.plot(x_coordinates, y_coordinates)
    plt.savefig(img, format='png')
    img.seek(0)
    graph_url = base64.b64encode(img.getvalue()).decode()
    plt.close()
    
    return 'data:image/png;base64,{}'.format(graph_url)



@app.route('/') # Change URL
def graphs():

    name = request.args.get("name")
    age  = request.args.get("age")


    y1 = GET_POINTS("Borussia Dortmund", file)[3]  
    x1 = list(range(1, (len(y1)+1) ))
      
    x2 = [0, 1, 2, 3, 4]
    y2 = [50, 30, 20, 10, 50]
    x3 = [0, 1, 2, 3, 4]
    y3 = [0, 30, 10, 5, 30]

    graph1_url = build_graph(x1,y1)
    graph2_url = build_graph(x2,y2)
    graph3_url = build_graph(x3,y3)
 
    return render_template('index.html',
                            graph1=graph1_url,
                            graph2=graph2_url,
                            graph3=graph3_url,
                            site1="sitegfgf1", 
                            site2="sitegfgf2",
                            name=name,
                            age=age
                            )


if __name__ == '__main__':
    app.debug = True
    app.run()