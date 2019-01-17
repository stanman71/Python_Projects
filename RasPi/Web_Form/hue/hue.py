from flask import request
from flask_sqlalchemy  import SQLAlchemy

from hue.RBGtoXY import RGBtoXY
from hue.phue import Bridge
from app import app


""" ######## """
""" database """
""" ######## """

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://python:python@localhost/raspi'
db = SQLAlchemy(app)

class Hue(db.Model):

    __tablename__ = 'hue'
    id          = db.Column(db.Integer, primary_key=True)
    ip          = db.Column(db.String(50), unique=True)
    color_red   = db.Column(db.Integer)
    color_green = db.Column(db.Integer)
    color_blue  = db.Column(db.Integer)
    color_y     = db.Column(db.Float)
    color_x     = db.Column(db.Float)
    brightness  = db.Column(db.Integer)

# Create all database tables
db.create_all()

# Create default hue settings
if Hue.query.filter_by().first() is None:
    hue = Hue(
        id = '1',
        ip = 'default',
    )
    db.session.add(hue)
    db.session.commit()


""" ######### """
""" Functions """
""" ######### """

def GET_RGB(ID = 1):

    id = ID
    entry = Hue.query.get(id)

    # RGB control
    if entry.color_red is not None:
        red   = entry.color_red
        green = entry.color_green
        blue  = entry.color_blue    
    else:
        red   = ''
        green = ''
        blue  = ''

    if request.method == 'POST':
 
        try:
            red   = request.form['slider_red']
            green = request.form['slider_green']
            blue  = request.form['slider_blue'] 

            xy = RGBtoXY(float(red), float(green), float(blue))

            entry.color_x     = xy[0]
            entry.color_y     = xy[1]
            entry.color_red   = red
            entry.color_green = green
            entry.color_blue  = blue     
            db.session.commit()    

        except:
            pass

    return (red, green, blue)


def GET_Brightness(ID = 1):

    id = ID
    entry = Hue.query.get(id)

    if entry.brightness is not None:
        brightness = entry.brightness    
    else:
        brightness = 0

    if request.method == 'POST':

        try:
            brightness = request.form['slider_brightness']
            entry.brightness = brightness     
            db.session.commit()    
   
        except:
            pass     

    return (brightness)


def GET_IP(ID = 1):
    entry = Hue.query.get(ID)
    return (entry.ip)  


def SET_IP(IP, ID = 1):    
    entry = Hue.query.get(ID) 
    entry.ip = IP
    db.session.commit()