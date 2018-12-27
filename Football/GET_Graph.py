from flask import Flask, render_template
from flask_bootstrap import Bootstrap 

from GET_Calc import GET_POINTS
import matplotlib.pyplot as plt
import io
import base64



app = Flask(__name__)
Bootstrap(app)


import pandas as pd
 
file = "./Python_Projects/Football/CSV/1_Bundesliga_2018_2019.csv"
df   = pd.read_csv(file, delimiter=",")



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

    x1 = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17] 
    y1 = GET_POINTS("Borussia Dortmund", df)[3]

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
                            site2="sitegfgf2")


if __name__ == '__main__':
    app.debug = True
    app.run()