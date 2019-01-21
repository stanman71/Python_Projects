from flask import request
from flask_sqlalchemy  import SQLAlchemy

from hue.RBGtoXY import RGBtoXY
from hue.phue import Bridge
from app import app

import re

""" ################ """
""" database settings"""
""" ################ """

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


class Bulks(db.Model):

    __tablename__ = 'bulks'
    id   = db.Column(db.Integer, primary_key=True, autoincrement = True)
    name = db.Column(db.String(50), unique = True)


class Scene_01(db.Model):

    __tablename__ = 'scene_01'
    id          = db.Column(db.Integer, primary_key=True, autoincrement = True)
    scene_id    = db.Column(db.Integer, db.ForeignKey('scenes.id'), server_default=("1"))
    scene_name  = db.relationship('Scenes')
    bulk_id     = db.Column(db.Integer, db.ForeignKey('bulks.id'), unique = True)
    bulk_name   = db.relationship('Bulks')
    color_red   = db.Column(db.Integer, server_default=("0"))
    color_green = db.Column(db.Integer, server_default=("0"))
    color_blue  = db.Column(db.Integer, server_default=("0"))
    color_x     = db.Column(db.Float)
    color_y     = db.Column(db.Float)
    brightness  = db.Column(db.Integer)
    

class Scene_02(db.Model):

    __tablename__ = 'scene_02'
    id          = db.Column(db.Integer, primary_key=True, autoincrement = True)
    scene_id    = db.Column(db.Integer, db.ForeignKey('scenes.id'), server_default=("2"))
    scene_name  = db.relationship('Scenes')
    bulk_id     = db.Column(db.Integer, db.ForeignKey('bulks.id'), unique = True)
    bulk_name   = db.relationship('Bulks')    
    color_red   = db.Column(db.Integer, server_default=("0"))
    color_green = db.Column(db.Integer, server_default=("0"))
    color_blue  = db.Column(db.Integer, server_default=("0"))
    color_x     = db.Column(db.Float)
    color_y     = db.Column(db.Float)
    brightness  = db.Column(db.Integer)
    

class Scene_03(db.Model):

    __tablename__ = 'scene_03'
    id          = db.Column(db.Integer, primary_key=True, autoincrement = True)
    scene_id    = db.Column(db.Integer, db.ForeignKey('scenes.id'), server_default=("3"))
    scene_name  = db.relationship('Scenes')
    bulk_id     = db.Column(db.Integer, db.ForeignKey('bulks.id'), unique = True)
    bulk_name   = db.relationship('Bulks')
    color_red   = db.Column(db.Integer, server_default=("0"))
    color_green = db.Column(db.Integer, server_default=("0"))
    color_blue  = db.Column(db.Integer, server_default=("0"))
    color_x     = db.Column(db.Float)
    color_y     = db.Column(db.Float)
    brightness  = db.Column(db.Integer)


class Scene_04(db.Model):

    __tablename__ = 'scene_04'
    id          = db.Column(db.Integer, primary_key=True, autoincrement = True)
    scene_id    = db.Column(db.Integer, db.ForeignKey('scenes.id'), server_default=("4"))
    scene_name  = db.relationship('Scenes')
    bulk_id     = db.Column(db.Integer, db.ForeignKey('bulks.id'), unique = True)
    bulk_name   = db.relationship('Bulks')
    color_red   = db.Column(db.Integer, server_default=("0"))
    color_green = db.Column(db.Integer, server_default=("0"))
    color_blue  = db.Column(db.Integer, server_default=("0"))
    color_x     = db.Column(db.Float)
    color_y     = db.Column(db.Float)
    brightness  = db.Column(db.Integer)


class Scene_05(db.Model):

    __tablename__ = 'scene_05'
    id          = db.Column(db.Integer, primary_key=True, autoincrement = True)
    scene_id    = db.Column(db.Integer, db.ForeignKey('scenes.id'), server_default=("5"))
    scene_name  = db.relationship('Scenes')
    bulk_id     = db.Column(db.Integer, db.ForeignKey('bulks.id'), unique = True)
    bulk_name   = db.relationship('Bulks') 
    color_red   = db.Column(db.Integer, server_default=("0"))
    color_green = db.Column(db.Integer, server_default=("0"))
    color_blue  = db.Column(db.Integer, server_default=("0"))
    color_x     = db.Column(db.Float)
    color_y     = db.Column(db.Float)
    brightness  = db.Column(db.Integer)



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


def GET_IP(ID = 1):
    entry = Bridge.query.get(ID)
    return (entry.ip)  


def SET_IP(IP, ID = 1):    
    entry = Bridge.query.get(ID) 
    entry.ip = IP
    db.session.commit()


def SET_SCENE_NAME(Scene, name):
    entry = Scenes.query.get(Scene)
    entry.name = name
    db.session.commit()


def GET_DROPDOWN_LIST():
    entries = Bulks.query.all()
    
    entry_list = []
    for entry in entries:
        entry_list.append(entry.name)

    return entry_list


""" ######### """
""" GET_SCENE """
""" ######### """

def GET_SCENE(Scene):

    if Scene == 1:
        entries = Scene_01.query.all()
        name = entries[0].scene_name.name
    if Scene == 2:
        entries = Scene_02.query.all()
        name = entries[0].scene_name.name
    if Scene == 3:
        entries = Scene_03.query.all()
        name = entries[0].scene_name.name
    if Scene == 4:
        entries = Scene_04.query.all()
        name = entries[0].scene_name.name
    if Scene == 5:
        entries = Scene_05.query.all()
        name = entries[0].scene_name.name
   
    return (entries, name)


""" ############### """
""" SET_SCENE_COLOR """
""" ############### """

def SET_SCENE_COLOR(Scene, rgb_scene):

    if Scene == 1:
        for i in range(len(rgb_scene)):
            if rgb_scene[i] is not None:
                entry = Scene_01.query.filter_by(bulk_id=i+1).first()
                rgb_color = re.findall(r'\d+', rgb_scene[i])
    if Scene == 2:
        for i in range(len(rgb_scene)):
            if rgb_scene[i] is not None:
                entry = Scene_02.query.filter_by(bulk_id=i+1).first()
                rgb_color = re.findall(r'\d+', rgb_scene[i])
    if Scene == 3:
        for i in range(len(rgb_scene)):
            if rgb_scene[i] is not None:
                entry = Scene_03.query.filter_by(bulk_id=i+1).first()
                rgb_color = re.findall(r'\d+', rgb_scene[i])
    if Scene == 4:
        for i in range(len(rgb_scene)):
            if rgb_scene[i] is not None:
                entry = Scene_04.query.filter_by(bulk_id=i+1).first()
                rgb_color = re.findall(r'\d+', rgb_scene[i])
    if Scene == 5:
        for i in range(len(rgb_scene)):
            if rgb_scene[i] is not None:
                entry = Scene_05.query.filter_by(bulk_id=i+1).first()
                rgb_color = re.findall(r'\d+', rgb_scene[i])
    
    try:
        entry.color_red   = rgb_color[0]
        entry.color_green = rgb_color[1]           
        entry.color_blue  = rgb_color[2]
        db.session.commit()
    except:
        pass
    


""" ######## """
""" ADD_BULK """
""" ######## """

def ADD_BULK(Scene, Name):

    entry = Bulks.query.filter_by(name=Name).first()

    # Scene 01
    if Scene == 1:
        check_entry = Scene_01.query.filter_by(bulk_id=entry.id).first()

        if check_entry is None:

            scene = Scene_01(
                bulk_id = entry.id,
            )
            db.session.add(scene)
            db.session.commit()

    # Scene 02
    if Scene == 2:
        check_entry = Scene_02.query.filter_by(bulk_id=entry.id).first()

        if check_entry is None:

            scene = Scene_02(
                bulk_id = entry.id,
            )
            db.session.add(scene)
            db.session.commit()

    # Scene 03
    if Scene == 3:
        check_entry = Scene_03.query.filter_by(bulk_id=entry.id).first()

        if check_entry is None:

            scene = Scene_03(
                bulk_id = entry.id,
            )
            db.session.add(scene)
            db.session.commit()

    # Scene 04
    if Scene == 4:
        check_entry = Scene_04.query.filter_by(bulk_id=entry.id).first()

        if check_entry is None:

            scene = Scene_04(
                bulk_id = entry.id,
            )
            db.session.add(scene)
            db.session.commit()

    # Scene 05
    if Scene == 5:
        check_entry = Scene_05.query.filter_by(bulk_id=entry.id).first()

        if check_entry is None:

            scene = Scene_05(
                bulk_id = entry.id,
            )
            db.session.add(scene)
            db.session.commit()            


""" ######## """
""" DEL_BULK """
""" ######## """

def DEL_BULK(Scene, ID):
    if Scene == 1:
        Scene_01.query.filter_by(bulk_id=ID).delete()
        db.session.commit()
    if Scene == 2:
        Scene_02.query.filter_by(bulk_id=ID).delete()
        db.session.commit()
    if Scene == 3:
        Scene_03.query.filter_by(bulk_id=ID).delete()
        db.session.commit()
    if Scene == 4:
        Scene_04.query.filter_by(bulk_id=ID).delete()
        db.session.commit()
    if Scene == 5:
        Scene_05.query.filter_by(bulk_id=ID).delete()
        db.session.commit()


""" ######### """
""" DEL_SCENE """
""" ######### """

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

