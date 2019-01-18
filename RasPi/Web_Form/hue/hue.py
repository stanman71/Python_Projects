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

class Bridge(db.Model):

    __tablename__ = 'bridge'
    id = db.Column(db.Integer, primary_key=True)
    ip = db.Column(db.String(50))


class Bulks(db.Model):

    __tablename__ = 'bulks'
    id          = db.Column(db.Integer, primary_key=True)
    scene       = db.Column(db.Integer)
    color_red   = db.Column(db.Integer)
    color_green = db.Column(db.Integer)
    color_blue  = db.Column(db.Integer)
    color_x     = db.Column(db.Float)
    color_y     = db.Column(db.Float)
    brightness  = db.Column(db.Integer)
    

# Create all database tables
db.create_all()



# Create default bridge settings
if Bridge.query.filter_by().first() is None:
    bridge = Bridge(
        id = '1',
        ip = 'default',
    )
    db.session.add(bridge)
    db.session.commit()


""" ######### """
""" Functions """
""" ######### """


def GET_IP(ID = 1):
    entry = Bridge.query.get(ID)
    return (entry.ip)  


def SET_IP(IP, ID = 1):    
    entry = Bridge.query.get(ID) 
    entry.ip = IP
    db.session.commit()