from flask import request
from flask_sqlalchemy  import SQLAlchemy

from hue.RBGtoXY import RGBtoXY
from hue.phue import Bridge
from app import app


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


def SET_SCENE_NAME(ID, name):
    entry = Scenes.query.get(ID)
    entry.name = name
    db.session.commit()


def DEL_SCENE(ID):
    if ID == "1":
        Scene_01.query.delete()
        entry = Scenes.query.get(1)
        entry.name = ""
        db.session.commit()
    if ID == "2":
        Scene_02.query.delete()
        entry = Scenes.query.get(2)
        entry.name = ""
        db.session.commit()
    if ID == "3":
        Scene_03.query.delete()
        entry = Scenes.query.get(3)
        entry.name = ""
        db.session.commit()
    if ID == "4":
        Scene_04.query.delete()
        entry = Scenes.query.get(4)
        entry.name = ""
        db.session.commit()
    if ID == "5":
        Scene_05.query.delete()
        entry = Scenes.query.get(5)
        entry.name = ""
        db.session.commit()


def GET_SCENE_01():

    entries = Scene_01.query.all()
    name = entries[0].scene_name.name
    return (entries, name)

def GET_SCENE_02():

    entries = Scene_02.query.all()
    name = entries[0].scene_name.name
    return (entries, name)

def GET_SCENE_03():

    entries = Scene_03.query.all()
    name = entries[0].scene_name.name
    return (entries, name)

def GET_SCENE_04():

    entries = Scene_04.query.all()
    name = entries[0].scene_name.name
    return (entries, name)

def GET_SCENE_05():

    entries = Scene_05.query.all()
    name = entries[0].scene_name.name
    return (entries, name)