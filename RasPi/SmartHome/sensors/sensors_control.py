from flask import request
from flask_sqlalchemy import SQLAlchemy
import datetime

from app import app

""" ################# """
""" database settings """
""" ################# """

# connect to database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///smarthome.sqlite3'
db = SQLAlchemy(app)


# define table structure

class Sensor(db.Model):
    __tablename__ = 'sensor'
    id   = db.Column(db.Integer, primary_key=True, autoincrement = True)
    name = db.Column(db.String(50), unique=True)

class Sensor_GPIO_A00(db.Model):
    __tablename__ = 'sensor_gpio_a00'
    id        = db.Column(db.Integer, primary_key=True, autoincrement = True)
    value     = db.Column(db.Integer)    
    time      = db.Column(db.Date, onupdate=datetime.datetime.now)

class Sensor_GPIO_A01(db.Model):
    __tablename__ = 'sensor_gpio_a01'
    id        = db.Column(db.Integer, primary_key=True, autoincrement = True)
    value     = db.Column(db.Integer)    
    time      = db.Column(db.Date, onupdate=datetime.datetime.now)

class Sensor_GPIO_A02(db.Model):
    __tablename__ = 'sensor_gpio_a02'
    id        = db.Column(db.Integer, primary_key=True, autoincrement = True)
    value     = db.Column(db.Integer)    
    time      = db.Column(db.Date, onupdate=datetime.datetime.now)

class Sensor_GPIO_A03(db.Model):
    __tablename__ = 'sensor_gpio_a03'
    id        = db.Column(db.Integer, primary_key=True, autoincrement = True)
    value     = db.Column(db.Integer)    
    time      = db.Column(db.Date, onupdate=datetime.datetime.now)

class Sensor_GPIO_A04(db.Model):
    __tablename__ = 'sensor_gpio_a04'
    id        = db.Column(db.Integer, primary_key=True, autoincrement = True)
    value     = db.Column(db.Integer)    
    time      = db.Column(db.Date, onupdate=datetime.datetime.now)

class Sensor_GPIO_A05(db.Model):
    __tablename__ = 'sensor_gpio_a05'
    id        = db.Column(db.Integer, primary_key=True, autoincrement = True)
    value     = db.Column(db.Integer)    
    time      = db.Column(db.Date, onupdate=datetime.datetime.now)

class Sensor_GPIO_A06(db.Model):
    __tablename__ = 'sensor_gpio_a06'
    id        = db.Column(db.Integer, primary_key=True, autoincrement = True)
    value     = db.Column(db.Integer)    
    time      = db.Column(db.Date, onupdate=datetime.datetime.now)    

class Sensor_GPIO_A07(db.Model):
    __tablename__ = 'sensor_gpio_a07'
    id        = db.Column(db.Integer, primary_key=True, autoincrement = True)
    value     = db.Column(db.Integer)    
    time      = db.Column(db.Date, onupdate=datetime.datetime.now)

class Sensor_MQTT_00(db.Model):
    __tablename__ = 'sensor_mqtt_00'
    id        = db.Column(db.Integer, primary_key=True, autoincrement = True)
    value     = db.Column(db.Integer)    
    time      = db.Column(db.Date, onupdate=datetime.datetime.now)

class Sensor_MQTT_01(db.Model):
    __tablename__ = 'sensor_mqtt_01'
    id        = db.Column(db.Integer, primary_key=True, autoincrement = True)
    value     = db.Column(db.Integer)    
    time      = db.Column(db.Date, onupdate=datetime.datetime.now)

class Sensor_MQTT_02(db.Model):
    __tablename__ = 'sensor_mqtt_02'
    id        = db.Column(db.Integer, primary_key=True, autoincrement = True)
    value     = db.Column(db.Integer)    
    time      = db.Column(db.Date, onupdate=datetime.datetime.now)    


# create all database tables
db.create_all()


""" ################ """
""" Sensor Functions """
""" ################ """

def GET_SENSOR_VALUES(id):

    sensor_name = Sensor.query.filter_by(id=id).first()
    sensor_name = sensor_name.name

    if sensor_name == "GPIO_A00":
        sensor_values = Sensor_GPIO_A00.query.all()
    if sensor_name == "GPIO_A01":
        sensor_values = Sensor_GPIO_A01.query.all()
    if sensor_name == "GPIO_A02":
        sensor_values = Sensor_GPIO_A02.query.all()
    if sensor_name == "GPIO_A03":
        sensor_values = Sensor_GPIO_A03.query.all()
    if sensor_name == "GPIO_A04":
        sensor_values = Sensor_GPIO_A04.query.all()
    if sensor_name == "GPIO_A05":
        sensor_values = Sensor_GPIO_A05.query.all()
    if sensor_name == "GPIO_A06":
        sensor_values = Sensor_GPIO_A06.query.all()
    if sensor_name == "GPIO_A07":
        sensor_values = Sensor_GPIO_A07.query.all()        
    if sensor_name == "MQTT_00":
        sensor_values = Sensor_MQTT_00.query.all()
    if sensor_name == "MQTT_01":
        sensor_values = Sensor_MQTT_01.query.all()
    if sensor_name == "MQTT_02":
        sensor_values = Sensor_MQTT_02.query.all()
    
    if sensor_values == []:
        return None
    else:
        return sensor_values


def DELETE_SENSOR_VALUES(id):

    sensor_name = Sensor.query.filter_by(id=id).first()
    sensor_name = sensor_name.name

    if sensor_name == "GPIO_A00":
        Sensor_GPIO_A00.query.delete()
    if sensor_name == "GPIO_A01":
        Sensor_GPIO_A01.query.delete()
    if sensor_name == "GPIO_A02":
        Sensor_GPIO_A02.query.delete()
    if sensor_name == "GPIO_A03":
        Sensor_GPIO_A03.query.delete()
    if sensor_name == "GPIO_A04":
        Sensor_GPIO_A04.query.delete()
    if sensor_name == "GPIO_A05":
        Sensor_GPIO_A05.query.delete()
    if sensor_name == "GPIO_A06":
        Sensor_GPIO_A06.query.delete()
    if sensor_name == "GPIO_A07":
        Sensor_GPIO_A07.query.delete()
    if sensor_name == "MQTT_00":
        Sensor_MQTT_00.query.delete()
    if sensor_name == "MQTT_01":
        Sensor_MQTT_01.query.delete()
    if sensor_name == "MQTT_02":
        Sensor_MQTT_02.query.delete()

    db.session.commit() 
    return "Werte geloescht"

def READ_SENSOR(name):
    pass

def WATERING_PLANTS():
    pass