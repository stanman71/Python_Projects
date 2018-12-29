from GET_Data import GET_RESULTS, GET_TABLE, GET_CROSS_TABLE, CREATE_CSV, GET_ALL
from GET_Calc import GET_ALL_GOALS, GET_ESTIMATE_GOALS_POISSON , GET_POINTS, GET_SEASON, GET_STATS_FROM_CLUB, CALC_SEASON_POISSON, GET_ALL_CLUBS

from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap 

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

import io
import base64


def build_graph(x_coordinates, y_coordinates):
    img = io.BytesIO()
    plt.plot(x_coordinates, y_coordinates)
    plt.savefig(img, format='png')
    img.seek(0)
    graph_url = base64.b64encode(img.getvalue()).decode()
    plt.close()
    
    return 'data:image/png;base64,{}'.format(graph_url)


url  = "https://www.dfb.de/bundesliga/spieltagtabelle/?spieledb_path=/competitions/12/seasons/17683/matchday&spieledb_path=%2Fcompetitions%2F12%2Fseasons%2F17820%2Fmatchday%2F13"
file = "./Python_Projects/Football/CSV/1_Bundesliga_2018_2019.csv"


app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 1
Bootstrap(app)


@app.route('/', methods=['GET'])
def graphs():

    name = request.args.get("name")
    age  = request.args.get("age")

    dropdown_list = GET_ALL_CLUBS(file)

    return render_template('index.html',
                            site1="Start", 
                            site2="sitegfgf2",
                            name=name,
                            age=age,
                            dropdown_list=dropdown_list
                            )




@app.route('/login', methods=['GET', 'POST'])
def login():

    name = request.args.get("name")
    age  = request.args.get("age")

    if request.method == "POST":
        club_name = request.form.get("club", None)
        if club_name!=None:
            
            y1 = GET_POINTS(club_name, file)[3]  
            x1 = list(range(1, (len(y1)+1) ))
            
            graph1_url = build_graph(x1,y1)    
   
    dropdown_list = GET_ALL_CLUBS(file)

    return render_template('index.html',
                            graph1=graph1_url,
                            site1="Start", 
                            site2="sitegfgf2",
                            name=name,
                            age=age,
                            club_name=club_name,
                            dropdown_list=dropdown_list
                            )




# update images
@app.after_request
def add_header(response):
    # response.cache_control.no_store = True
    if 'Cache-Control' not in response.headers:
        response.headers['Cache-Control'] = 'no-store'
    return response


if __name__ == '__main__':
    app.debug = True
    app.run()


