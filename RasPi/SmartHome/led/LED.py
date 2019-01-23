from flask import request
from flask_sqlalchemy import SQLAlchemy
import re
import sys


""" ################ """
""" general settings """
""" ################ """

# Windows WORK
#sys.path.insert(0, "C:/Users/mstan/GIT/Python_Projects/RasPi/SmartHome/led")
#PATH = 'C:/Users/mstan/GIT/Python_Projects/RasPi/SmartHome/static/CDNJS/'

# Windows HOME
sys.path.insert(0, "C:/Users/stanman/Desktop/Unterlagen/GIT/Python_Projects/RasPi/SmartHome/led")
PATH = 'C:/Users/stanman/Desktop/Unterlagen/GIT/Python_Projects/RasPi/SmartHome/static/CDNJS/'

# RasPi:
#sys.path.insert(0, "/home/pi/Python/SmartHome/led")


""" ################# """
""" database settings """
""" ################# """

from app import app
from phue import Bridge

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://python:python@localhost/raspi'
db = SQLAlchemy(app)

class Bridge(db.Model):
    __tablename__ = 'bridge'
    id = db.Column(db.Integer, primary_key=True, autoincrement = True)
    ip = db.Column(db.String(50), unique = True)

class Scenes(db.Model):
    __tablename__ = 'scenes'
    id   = db.Column(db.Integer, primary_key=True, autoincrement = True)
    name = db.Column(db.String(50))

class LED(db.Model):
    __tablename__ = 'LED'
    id      = db.Column(db.Integer, primary_key=True, autoincrement = True)
    name    = db.Column(db.String(50), unique = True)
    version = db.Column(db.String(50))

class BRIGHTNESS_GLOBAL(db.Model):
    __tablename__ = 'brightness_global'
    id                = db.Column(db.Integer, primary_key=True, autoincrement = True)
    brightness_global = db.Column(db.Integer)

class Scene_01(db.Model):
    __tablename__ = 'scene_01'
    id          = db.Column(db.Integer, primary_key=True, autoincrement = True)
    scene_id    = db.Column(db.Integer, db.ForeignKey('scenes.id'), server_default=("1"))
    scene_name  = db.relationship('Scenes')
    LED_id      = db.Column(db.Integer, db.ForeignKey('LED.id'), unique = True)
    LED_name    = db.relationship('LED')
    color_red   = db.Column(db.Integer, server_default=("0"))
    color_green = db.Column(db.Integer, server_default=("0"))
    color_blue  = db.Column(db.Integer, server_default=("0"))
    brightness  = db.Column(db.Integer, server_default=("100"))

class Scene_02(db.Model):
    __tablename__ = 'scene_02'
    id          = db.Column(db.Integer, primary_key=True, autoincrement = True)
    scene_id    = db.Column(db.Integer, db.ForeignKey('scenes.id'), server_default=("2"))
    scene_name  = db.relationship('Scenes')
    LED_id      = db.Column(db.Integer, db.ForeignKey('LED.id'), unique = True)
    LED_name    = db.relationship('LED')    
    color_red   = db.Column(db.Integer, server_default=("0"))
    color_green = db.Column(db.Integer, server_default=("0"))
    color_blue  = db.Column(db.Integer, server_default=("0"))
    brightness  = db.Column(db.Integer, server_default=("100"))

class Scene_03(db.Model):
    __tablename__ = 'scene_03'
    id          = db.Column(db.Integer, primary_key=True, autoincrement = True)
    scene_id    = db.Column(db.Integer, db.ForeignKey('scenes.id'), server_default=("3"))
    scene_name  = db.relationship('Scenes')
    LED_id      = db.Column(db.Integer, db.ForeignKey('LED.id'), unique = True)
    LED_name    = db.relationship('LED')
    color_red   = db.Column(db.Integer, server_default=("0"))
    color_green = db.Column(db.Integer, server_default=("0"))
    color_blue  = db.Column(db.Integer, server_default=("0"))
    brightness  = db.Column(db.Integer, server_default=("100"))

class Scene_04(db.Model):
    __tablename__ = 'scene_04'
    id          = db.Column(db.Integer, primary_key=True, autoincrement = True)
    scene_id    = db.Column(db.Integer, db.ForeignKey('scenes.id'), server_default=("4"))
    scene_name  = db.relationship('Scenes')
    LED_id      = db.Column(db.Integer, db.ForeignKey('LED.id'), unique = True)
    LED_name    = db.relationship('LED')
    color_red   = db.Column(db.Integer, server_default=("0"))
    color_green = db.Column(db.Integer, server_default=("0"))
    color_blue  = db.Column(db.Integer, server_default=("0"))
    brightness  = db.Column(db.Integer, server_default=("100"))

class Scene_05(db.Model):
    __tablename__ = 'scene_05'
    id          = db.Column(db.Integer, primary_key=True, autoincrement = True)
    scene_id    = db.Column(db.Integer, db.ForeignKey('scenes.id'), server_default=("5"))
    scene_name  = db.relationship('Scenes')
    LED_id      = db.Column(db.Integer, db.ForeignKey('LED.id'), unique = True)
    LED_name    = db.relationship('LED') 
    color_red   = db.Column(db.Integer, server_default=("0"))
    color_green = db.Column(db.Integer, server_default=("0"))
    color_blue  = db.Column(db.Integer, server_default=("0"))
    brightness  = db.Column(db.Integer, server_default=("100"))


""" ############################## """
""" database create default values """
""" ############################## """

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

# Create default brightness_global settings
if BRIGHTNESS_GLOBAL.query.filter_by().first() is None:
    brightness_global = BRIGHTNESS_GLOBAL(
        id                = '1',
        brightness_global = '100',
    )
    db.session.add(brightness_global)
    db.session.commit()

# Create default scenes
if Scenes.query.filter_by().first() is None:   
    for i in range(1,10):
        scene = Scenes(
            id = i,
            name = "Szene " + str(i),
        )
        db.session.add(scene)
        db.session.commit()


""" ######### """
""" Functions """
""" ######### """

def GET_DROPDOWN_LIST():
    entry_list = []
    entries = LED.query.all()
    for entry in entries:
        entry_list.append(entry.name)
    return entry_list

def GET_BRIGHTNESS_GLOBAL():
    entry = BRIGHTNESS_GLOBAL.query.filter_by().first()
    return (entry.brightness_global)

def SET_BRIGHTNESS_GLOBAL(brightness_global):
    entry = BRIGHTNESS_GLOBAL.query.filter_by().first()
    entry.brightness_global = brightness_global
    db.session.commit()


""" ############ """
""" IP Functions """
""" ############ """

def GET_IP():
    entry = Bridge.query.filter_by().first()
    return (entry.ip)  

def SET_IP(IP):    
    entry = Bridge.query.filter_by().first()
    entry.ip = IP
    db.session.commit()


""" ############# """
""" LED Functions """
""" ############# """

def GET_LED():
    entries = LED.query.all()
    return (entries)

def SET_LED_NAME(ID, name):
    if name is "":
        return ("Kein Name angegeben")
    if (LED.query.filter_by(name=name).first()):
        return ("Name schon vergeben")
    entry = LED.query.filter_by(id=ID).first()
    entry.name = name
    db.session.commit()
    return ("")

def ADD_LED(Scene, Name):
    entry = LED.query.filter_by(name=Name).first() 
    if Scene == 1:
        check_entry = Scene_01.query.filter_by(LED_id=entry.id).first()
        if check_entry is None:
            scene = Scene_01(
                LED_id = entry.id,
            )
    if Scene == 2:
        check_entry = Scene_02.query.filter_by(LED_id=entry.id).first()
        if check_entry is None:
            scene = Scene_02(
                LED_id = entry.id,
            )
    if Scene == 3:
        check_entry = Scene_03.query.filter_by(LED_id=entry.id).first()
        if check_entry is None:
            scene = Scene_03(
                LED_id = entry.id,
            )
    if Scene == 4:
        check_entry = Scene_04.query.filter_by(LED_id=entry.id).first()
        if check_entry is None:
            scene = Scene_04(
                LED_id = entry.id,
            )
    if Scene == 5:
        check_entry = Scene_05.query.filter_by(LED_id=entry.id).first()
        if check_entry is None:
            scene = Scene_05(
                LED_id = entry.id,
            )       
    try:        
        db.session.add(scene)
        db.session.commit()        
    except:
        pass    

def DEL_LED(Scene, ID):
    if Scene == 1:
        Scene_01.query.filter_by(LED_id=ID).delete()
    if Scene == 2:
        Scene_02.query.filter_by(LED_id=ID).delete()
    if Scene == 3:
        Scene_03.query.filter_by(LED_id=ID).delete()
    if Scene == 4:
        Scene_04.query.filter_by(LED_id=ID).delete()
    if Scene == 5:
        Scene_05.query.filter_by(LED_id=ID).delete()
    db.session.commit()


""" ############### """
""" SCENE Functions """
""" ############### """

def GET_SCENE(Scene):
    entries = None
    name    = None
    if Scene == 1:
        if Scene_01.query.all():
            entries = Scene_01.query.all()
            name = entries[0].scene_name.name
    if Scene == 2:
        if Scene_02.query.all():
            entries = Scene_02.query.all()
            name = entries[0].scene_name.name
    if Scene == 3:
        if Scene_03.query.all():
            entries = Scene_03.query.all()
            name = entries[0].scene_name.name
    if Scene == 4:
        if Scene_04.query.all():
            entries = Scene_04.query.all()  
            name = entries[0].scene_name.name
    if Scene == 5:
        if Scene_05.query.all():
            entries = Scene_05.query.all()
            name = entries[0].scene_name.name
    return (entries, name)

def SET_SCENE_NAME(Scene, name):
    entry = Scenes.query.filter_by(id=Scene).first()
    entry.name = name
    db.session.commit()

def SET_SCENE_COLOR(Scene, rgb_scene):
    if Scene == 1:
        for i in range(len(rgb_scene)):
            if rgb_scene[i] is not None:
                entry = Scene_01.query.filter_by(LED_id=i+1).first()
                rgb_color = re.findall(r'\d+', rgb_scene[i])
                break
    if Scene == 2:
        for i in range(len(rgb_scene)):
            if rgb_scene[i] is not None:
                entry = Scene_02.query.filter_by(LED_id=i+1).first()
                rgb_color = re.findall(r'\d+', rgb_scene[i])
                break
    if Scene == 3:
        for i in range(len(rgb_scene)):
            if rgb_scene[i] is not None:
                entry = Scene_03.query.filter_by(LED_id=i+1).first()
                rgb_color = re.findall(r'\d+', rgb_scene[i])
                break
    if Scene == 4:
        for i in range(len(rgb_scene)):
            if rgb_scene[i] is not None:
                entry = Scene_04.query.filter_by(LED_id=i+1).first()
                rgb_color = re.findall(r'\d+', rgb_scene[i])
                break
    if Scene == 5:
        for i in range(len(rgb_scene)):
            if rgb_scene[i] is not None:
                entry = Scene_05.query.filter_by(LED_id=i+1).first()
                rgb_color = re.findall(r'\d+', rgb_scene[i])
                break 
    try:
        entry.color_red   = rgb_color[0]
        entry.color_green = rgb_color[1]           
        entry.color_blue  = rgb_color[2]
        db.session.commit()
    except:
        pass
    
def SET_SCENE_BRIGHTNESS(Scene, brightness):
    if Scene == 1:
        for i in range(len(brightness)):
            if brightness[i] is not None:
                entry = Scene_01.query.filter_by(LED_id=i+1).first()
                brightness = brightness[i]
                break
    if Scene == 2:
        for i in range(len(brightness)):
            if brightness[i] is not None:
                entry = Scene_02.query.filter_by(LED_id=i+1).first()
                brightness = brightness[i]
                break
    if Scene == 3:
        for i in range(len(brightness)):
            if brightness[i] is not None:
                entry = Scene_03.query.filter_by(LED_id=i+1).first()
                brightness = brightness[i]
                break            
    if Scene == 4:
        for i in range(len(brightness)):
            if brightness[i] is not None:
                entry = Scene_04.query.filter_by(LED_id=i+1).first()
                brightness = brightness[i]
                break
    if Scene == 5:
        for i in range(len(brightness)):
            if brightness[i] is not None:
                entry = Scene_05.query.filter_by(LED_id=i+1).first()
                brightness = brightness[i]
                break
    try:
        entry.brightness = brightness
        db.session.commit()
    except:
        pass

def DEL_SCENE(Scene):
    if Scene == 1:
        Scene_01.query.delete()
    if Scene == 2:
        Scene_02.query.delete()
    if Scene == 3:
        Scene_03.query.delete()
    if Scene == 4:
        Scene_04.query.delete()
    if Scene == 5:
        Scene_05.query.delete()
    entry = Scenes.query.get(Scene)
    entry.name = ""
    db.session.commit()