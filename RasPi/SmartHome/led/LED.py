from flask import request
from flask_sqlalchemy import SQLAlchemy

from led.phue import Bridge
from app import app

import re

'''
RasPi:

import sys
sys.path.insert(0, "/home/pi/Python/SmartHome/led")
from phue import Bridge
'''


""" ################# """
""" database settings """
""" ################# """


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



""" ############### """
""" database create """
""" ############### """


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


# Create default scenes
if Scenes.query.filter_by().first() is None:   
    for i in range(1,11):
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
    entries = LED.query.all()
    
    entry_list = []
    for entry in entries:
        entry_list.append(entry.name)
    return entry_list


""" ############ """
""" IP Functions """
""" ############ """


def GET_IP(ID = 1):
    entry = Bridge.query.get(ID)
    return (entry.ip)  


def SET_IP(IP, ID = 1):    
    entry = Bridge.query.get(ID) 
    entry.ip = IP
    db.session.commit()


""" ############# """
""" LED Functions """
""" ############# """


def GET_LED():
    entries = LED.query.all()
    return (entries)


def SET_LED_NAME(ID, name):

    if (LED.query.filter_by(name=name).first()):
        return ("Name schon vergeben")

    entry = LED.query.filter_by(id=ID).first()
    entry.name = name
    db.session.commit()
    return ("")


def ADD_LED(Scene, Name):

    entry = LED.query.filter_by(name=Name).first()

    # Scene 01
    if Scene == 1:
        check_entry = Scene_01.query.filter_by(LED_id=entry.id).first()

        if check_entry is None:
            scene = Scene_01(
                LED_id = entry.id,
            )
            db.session.add(scene)
            db.session.commit()

    # Scene 02
    if Scene == 2:
        check_entry = Scene_02.query.filter_by(LED_id=entry.id).first()

        if check_entry is None:
            scene = Scene_02(
                LED_id = entry.id,
            )
            db.session.add(scene)
            db.session.commit()

    # Scene 03
    if Scene == 3:
        check_entry = Scene_03.query.filter_by(LED_id=entry.id).first()

        if check_entry is None:
            scene = Scene_03(
                LED_id = entry.id,
            )
            db.session.add(scene)
            db.session.commit()

    # Scene 04
    if Scene == 4:
        check_entry = Scene_04.query.filter_by(LED_id=entry.id).first()

        if check_entry is None:
            scene = Scene_04(
                LED_id = entry.id,
            )
            db.session.add(scene)
            db.session.commit()

    # Scene 05
    if Scene == 5:
        check_entry = Scene_05.query.filter_by(LED_id=entry.id).first()

        if check_entry is None:
            scene = Scene_05(
                LED_id = entry.id,
            )
            db.session.add(scene)
            db.session.commit()            


def DEL_LED(Scene, ID):
    if Scene == 1:
        Scene_01.query.filter_by(LED_id=ID).delete()
        db.session.commit()
    if Scene == 2:
        Scene_02.query.filter_by(LED_id=ID).delete()
        db.session.commit()
    if Scene == 3:
        Scene_03.query.filter_by(LED_id=ID).delete()
        db.session.commit()
    if Scene == 4:
        Scene_04.query.filter_by(LED_id=ID).delete()
        db.session.commit()
    if Scene == 5:
        Scene_05.query.filter_by(LED_id=ID).delete()
        db.session.commit()


""" ############### """
""" SCENE Functions """
""" ############### """


def GET_SCENE(Scene):

    if Scene == 1:
        if Scene_01.query.all():
            entries = Scene_01.query.all()
            name = entries[0].scene_name.name
        else:
            entries = None
            name    = None
    if Scene == 2:
        if Scene_02.query.all():
            entries = Scene_02.query.all()
            name = entries[0].scene_name.name
        else:
            entries = None
            name    = None            
    if Scene == 3:
        if Scene_03.query.all():
            entries = Scene_03.query.all()
            name = entries[0].scene_name.name
        else:
            entries = None
            name    = None           
    if Scene == 4:
        if Scene_04.query.all():
            entries = Scene_04.query.all()
            name = entries[0].scene_name.name
        else:
            entries = None
            name    = None                 
    if Scene == 5:
        if Scene_05.query.all():
            entries = Scene_05.query.all()
            name = entries[0].scene_name.name
        else:
            entries = None
            name    = None    

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
    if Scene == 2:
        for i in range(len(rgb_scene)):
            if rgb_scene[i] is not None:
                entry = Scene_02.query.filter_by(LED_id=i+1).first()
                rgb_color = re.findall(r'\d+', rgb_scene[i])
    if Scene == 3:
        for i in range(len(rgb_scene)):
            if rgb_scene[i] is not None:
                entry = Scene_03.query.filter_by(LED_id=i+1).first()
                rgb_color = re.findall(r'\d+', rgb_scene[i])
    if Scene == 4:
        for i in range(len(rgb_scene)):
            if rgb_scene[i] is not None:
                entry = Scene_04.query.filter_by(LED_id=i+1).first()
                rgb_color = re.findall(r'\d+', rgb_scene[i])
    if Scene == 5:
        for i in range(len(rgb_scene)):
            if rgb_scene[i] is not None:
                entry = Scene_05.query.filter_by(LED_id=i+1).first()
                rgb_color = re.findall(r'\d+', rgb_scene[i])
    
    try:
        entry.color_red   = rgb_color[0]
        entry.color_green = rgb_color[1]           
        entry.color_blue  = rgb_color[2]
        db.session.commit()
    except:
        pass
    

def DEL_SCENE(Scene):
    if Scene == 1:
        Scene_01.query.delete()
        entry = Scenes.query.get(1)
        entry.name = ""
        db.session.commit()
    if Scene == 2:
        Scene_02.query.delete()
        entry = Scenes.query.get(2)
        entry.name = ""
        db.session.commit()
    if Scene == 3:
        Scene_03.query.delete()
        entry = Scenes.query.get(3)
        entry.name = ""
        db.session.commit()
    if Scene == 4:
        Scene_04.query.delete()
        entry = Scenes.query.get(4)
        entry.name = ""
        db.session.commit()
    if Scene == 5:
        Scene_05.query.delete()
        entry = Scenes.query.get(5)
        entry.name = ""
        db.session.commit()