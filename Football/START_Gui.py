from GET_Calc import GET_ALL_GOALS, GET_POINTS, GET_SEASON, CALC_SEASON_POISSON, GET_ALL_CLUBS
from BUILD_Graph import build_graph

from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap 


file = "./Python_Projects/Football/CSV/1_Bundesliga_2018_2019.csv"


app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 1
Bootstrap(app)


# landing Page
@app.route('/', methods=['GET'])
def index():

    dropdown_list = GET_ALL_CLUBS(file)

    # input formular with checkbox
    if request.args.get('checkbox') == "on":  

        name = request.args.get("name")
        age  = request.args.get("age")

        return render_template('index.html',
                                site1="Start", 
                                name=name, 
                                age=age,
                                check=True,
                                dropdown_list=dropdown_list
                                )

    return render_template('index.html',
                        site1="Start",                                       
                        dropdown_list=dropdown_list                   
                        )


# club information
@app.route('/club', methods=['GET', 'POST']) 
def club():

    club_name = request.args.get("club")    
    dropdown_list = GET_ALL_CLUBS(file)

    # input dropdown (add value to the url)
    if request.method == "GET":     

        if club_name != None:       
 
            return render_template('club.html',
                                    site1="Start", 
                                    club_name=club_name,
                                    dropdown_list=dropdown_list,
                                    )
   
    # input buttons
    if request.method == "POST": 

        # Spielplan
        if 'Button_1' in request.form:

            season = GET_SEASON(club_name, file) 

            return render_template('club.html',
                                    site1="Start", 
                                    club_name=club_name,
                                    dropdown_list=dropdown_list,
                                    season=season
                                    )

        # Punkte
        if 'Button_2' in request.form:

            y1 = GET_POINTS(club_name, file)[3]  
            x1 = list(range(1, (len(y1)+1) ))        
            graph1_url = build_graph(x1,y1)  

            return render_template('club.html',
                                    site1="Start",                            
                                    club_name=club_name,
                                    dropdown_list=dropdown_list,
                                    graph1=graph1_url
                                    )

        # Poisson
        if 'Button_3' in request.form:

            poisson = CALC_SEASON_POISSON(club_name, file) 

            return render_template('club.html',
                                    site1="Start",                              
                                    club_name=club_name,
                                    dropdown_list=dropdown_list,
                                    poisson=poisson
                                    )


# update diagram
@app.after_request
def add_header(response):
    # response.cache_control.no_store = True
    if 'Cache-Control' not in response.headers:
        response.headers['Cache-Control'] = 'no-store'
    return response


if __name__ == '__main__':
    app.debug = True
    app.run()


