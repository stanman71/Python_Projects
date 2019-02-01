from flask import Flask, render_template, redirect, url_for, request, send_from_directory
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm 
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Email, Length
from flask_sqlalchemy  import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from functools import wraps
import sys
import datetime


""" ################# """
""" genernal settings """
""" ################# """

sys.path.insert(0, "C:/Users/stanman/Desktop/Unterlagen/GIT/Python_Projects/RasPi/SmartHome/led")
sys.path.insert(0, "C:/Users/mstan/GIT/Python_Projects/RasPi/SmartHome/led")
sys.path.insert(0, "/home/pi/Python/SmartHome/led")

# Windows Home
PATH_CSS = 'C:/Users/stanman/Desktop/Unterlagen/GIT/Python_Projects/RasPi/SmartHome/static/CDNJS/'

# Windows Work
#PATH_CSS = 'C:/Users/mstan/GIT/Python_Projects/RasPi/SmartHome/static/CDNJS/'

# RasPi:
#PATH_CSS = '/home/pi/Python/static/CDNJS/'


from colorpicker_local import colorpicker
from LED_database import *
from LED_control import *


""" ######### """
""" schedular """
""" ######### """

from flask_apscheduler import APScheduler

scheduler = APScheduler()

@scheduler.task('cron', id='scheduler_job', minute='*')
def scheduler_job():
    now = datetime.datetime.now()
    print(now.strftime('%a'))
    print(now.strftime('%H'))
    print(now.strftime('%M'))


""" ##### """
""" flask """
""" ##### """

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Thisissupposedtobesecret!'
Bootstrap(app)
colorpicker(app)


""" ######## """
""" database """
""" ######## """

# connect to database
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://python:python@localhost/raspi'
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# define table structure
class User(UserMixin, db.Model):
    __tablename__ = 'user'
    id       = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True)
    email    = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(100))
    role     = db.Column(db.String(20), server_default=("user"))

class Schedular(UserMixin, db.Model):
    __tablename__ = 'schedular'
    id     = db.Column(db.Integer, primary_key=True)
    name   = db.Column(db.String(50), unique=True)
    day    = db.Column(db.String(50))
    hour   = db.Column(db.String(50))
    minute = db.Column(db.String(50))
    task   = db.Column(db.String(100))
    repeat = db.Column(db.String(50))

# create all database tables
db.create_all()

# create default user
if User.query.filter_by(username='default').first() is None:
    user = User(
        username='default',
        email='member@example.com',
        password=generate_password_hash('qwer1234', method='sha256'),
        role='superuser'
    )
    db.session.add(user)
    db.session.commit()


""" ############### """
""" Role Management """
""" ############### """

# create role "superuser"
def superuser_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if current_user.role == "superuser":
            return f(*args, **kwargs)
        else:
            form = LoginForm()
            return render_template('login.html', form=form, role_check=False)
    return wrap

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


""" ##### """
""" LogIn """
""" ##### """

class LoginForm(FlaskForm):
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])
    remember = BooleanField('remember me')

class RegisterForm(FlaskForm):
    email    = StringField('email', validators=[InputRequired(), Email(message='Invalid email'), Length(max=50)])
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])


""" ############ """
""" Landing Page """
""" ############ """

# landing page
@app.route('/', methods=['GET', 'POST'])
def index():

    connect_bridge = False
    scene = 0
    brightness_global = 100
    value_1 = ""
    value_2 = ""
    value_3 = ""
    value_4 = ""
    value_5 = ""
    value_6 = ""
    value_7 = ""
    value_8 = ""
    value_9 = ""    
    program_massage = False
    
    led_update = ""
    led_update = UPDATE_LED()

    if request.method == "GET":     
        # change scene   
        try:     
            scene = int(request.args.get("radio_scene"))
            brightness_global = request.args.get("brightness_global")
            LED_SET_SCENE(scene,brightness_global)

            if scene == 1:
                value_1 = "checked = 'on'"
            if scene == 2:
                value_2 = "checked = 'on'"
            if scene == 3:
                value_3 = "checked = 'on'"
            if scene == 4:
                value_4 = "checked = 'on'"
            if scene == 5:
                value_5 = "checked = 'on'"        
            if scene == 6:
                value_6 = "checked = 'on'"
            if scene == 7:
                value_7 = "checked = 'on'"
            if scene == 8:
                value_8 = "checked = 'on'"
            if scene == 9:
                value_9 = "checked = 'on'"   
        except:
            pass

        # select a program   
        try:     
            program = int(request.args.get("radio_program"))
            program_massage = START_PROGRAM(program)
            
        except:
            pass

    # get scene names
    scene_name_01 = GET_SCENE(1)[1]
    if scene_name_01 == None:
        scene_name_01 = ""
    scene_name_02 = GET_SCENE(2)[1]
    if scene_name_02 == None:
        scene_name_02 = ""    
    scene_name_03 = GET_SCENE(3)[1]
    if scene_name_03 == None:
        scene_name_03 = ""
    scene_name_04 = GET_SCENE(4)[1]
    if scene_name_04 == None:
        scene_name_04 = ""
    scene_name_05 = GET_SCENE(5)[1]
    if scene_name_05 == None:
        scene_name_05 = ""
    scene_name_06 = GET_SCENE(6)[1]
    if scene_name_06 == None:
        scene_name_06 = ""    
    scene_name_07 = GET_SCENE(7)[1]
    if scene_name_07 == None:
        scene_name_07 = ""
    scene_name_08 = GET_SCENE(8)[1]
    if scene_name_08 == None:
        scene_name_08 = ""
    scene_name_09 = GET_SCENE(9)[1]
    if scene_name_09 == None:
        scene_name_09 = ""

    program_list = GET_ALL_PROGRAMS()

    return render_template('index.html', 
                            led_update=led_update,
                            scene_name_01=scene_name_01,
                            scene_name_02=scene_name_02,
                            scene_name_03=scene_name_03,
                            scene_name_04=scene_name_04,
                            scene_name_05=scene_name_05,
                            scene_name_06=scene_name_06,
                            scene_name_07=scene_name_07,
                            scene_name_08=scene_name_08,
                            scene_name_09=scene_name_09,
                            value_1=value_1,
                            value_2=value_2,
                            value_3=value_3,
                            value_4=value_4,
                            value_5=value_5,
                            value_6=value_6,
                            value_7=value_7,
                            value_8=value_8,
                            value_9=value_9,                            
                            brightness_global=brightness_global,
                            program_list=program_list,
                            program_massage=program_massage
                            )


""" ########## """
""" Sites User """
""" ########## """

# login
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if check_password_hash(user.password, form.password.data):
                login_user(user, remember=form.remember.data)
                return redirect(url_for('dashboard'))

        return render_template('login.html', form=form, login_check=False)

    return render_template('login.html', form=form)


# signup
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegisterForm()

    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method='sha256')
        new_user = User(username=form.username.data, email=form.email.data, password=hashed_password, role="user")
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('index'))
        
    return render_template('signup.html', form=form)


# Dashboard
@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
@superuser_required
def dashboard():
    return render_template('dashboard.html', name=current_user.username)


""" ######### """
""" Sites LED """
""" ######### """

# LED scene 01
@app.route('/dashboard/LED/scene_01', methods=['GET', 'POST'])
@login_required
@superuser_required
def dashboard_LED_scene_01():
    scene = 1

    if request.method == "GET":  
            
        # Change scene name
        name = request.args.get("name") 
        if name is not None:
            SET_SCENE_NAME(scene, name)
    
        # Set RGB color
        rgb_scene  = []
        for i in range(1,10):
            rgb_scene.append(request.args.get(str(scene) + " " + str(i)))
        SET_SCENE_COLOR(scene, rgb_scene)

        # Set brightness
        brightness = []
        for i in range(1,10):
            brightness.append(request.args.get(str(i)))
        SET_SCENE_BRIGHTNESS(scene, brightness)  

        # Add LED
        add_LED = request.args.get("LED_scene") 
        if add_LED is not None:
            ADD_LED(scene, add_LED)
 
    if request.method == "POST": 
        # Delete scene
        if 'delete' in request.form:
            DEL_SCENE(scene)

    led_update = ""
    led_update = LED_SET_SCENE(scene)

    entries_scene = GET_SCENE(scene)[0]
    scene_name    = GET_SCENE(scene)[1]
    dropdown_list = GET_DROPDOWN_LIST_LED()

    return render_template('dashboard_LED_scenes.html', 
                            led_update=led_update,
                            entries_scene=entries_scene,
                            scene_name=scene_name,
                            dropdown_list=dropdown_list,
                            number=scene,
                            active01="active"
                            )


# LED scene 02
@app.route('/dashboard/LED/scene_02', methods=['GET', 'POST'])
@login_required
@superuser_required
def dashboard_LED_scene_02():
    scene = 2

    if request.method == "GET":  
            
        # Change scene name
        name = request.args.get("name") 
        if name is not None:
            SET_SCENE_NAME(scene, name)
    
        # Set RGB color
        rgb_scene = []
        for i in range(1,10):
            rgb_scene.append(request.args.get(str(scene) + " " + str(i)))  
        SET_SCENE_COLOR(scene, rgb_scene)

        # Set brightness
        brightness = []
        for i in range(1,10):
            brightness.append(request.args.get(str(i)))
        SET_SCENE_BRIGHTNESS(scene, brightness)  

        # Add LED
        add_LED = request.args.get("LED_scene") 
        if add_LED is not None:
            ADD_LED(scene, add_LED)
 
    if request.method == "POST": 
        # Delete scene
        if 'delete' in request.form:
            DEL_SCENE(scene)

    led_update = ""
    led_update = LED_SET_SCENE(scene)

    entries_scene = GET_SCENE(scene)[0]
    scene_name    = GET_SCENE(scene)[1]
    dropdown_list = GET_DROPDOWN_LIST_LED()

    return render_template('dashboard_LED_scenes.html',
                            led_update=led_update,
                            entries_scene=entries_scene,
                            scene_name=scene_name,
                            dropdown_list=dropdown_list,
                            number=scene,
                            active02="active"
                            )


# LED scene 03
@app.route('/dashboard/LED/scene_03', methods=['GET', 'POST'])
@login_required
@superuser_required
def dashboard_LED_scene_03():
    scene = 3

    if request.method == "GET":  
            
        # Change scene name
        name = request.args.get("name") 
        if name is not None:
            SET_SCENE_NAME(scene, name)
    
        # Set RGB color
        rgb_scene = []
        for i in range(1,10):
            rgb_scene.append(request.args.get(str(scene) + " " + str(i))) 
        SET_SCENE_COLOR(scene, rgb_scene)

        # Set brightness
        brightness = []
        for i in range(1,10):
            brightness.append(request.args.get(str(i)))
        SET_SCENE_BRIGHTNESS(scene, brightness)  

        # Add LED
        add_LED = request.args.get("LED_scene") 
        if add_LED is not None:
            ADD_LED(scene, add_LED)
 
    if request.method == "POST": 
        # Delete scene
        if 'delete' in request.form:
            DEL_SCENE(scene)

    led_update = ""
    led_update = LED_SET_SCENE(scene)

    entries_scene = GET_SCENE(scene)[0]
    scene_name    = GET_SCENE(scene)[1]
    dropdown_list = GET_DROPDOWN_LIST_LED()

    return render_template('dashboard_LED_scenes.html', 
                            led_update=led_update,
                            entries_scene=entries_scene,
                            scene_name=scene_name,
                            dropdown_list=dropdown_list,
                            number=scene,
                            active03="active"
                            )


# LED scene 04
@app.route('/dashboard/LED/scene_04', methods=['GET', 'POST'])
@login_required
@superuser_required
def dashboard_LED_scene_04():
    scene = 4

    if request.method == "GET":  
            
        # Change scene name
        name = request.args.get("name") 
        if name is not None:
            SET_SCENE_NAME(scene, name)
    
        # Set RGB color
        rgb_scene = []
        for i in range(1,10):
            rgb_scene.append(request.args.get(str(scene) + " " + str(i)))      
        SET_SCENE_COLOR(scene, rgb_scene)

        # Set brightness
        brightness = []
        for i in range(1,10):
            brightness.append(request.args.get(str(i)))
        SET_SCENE_BRIGHTNESS(scene, brightness)  

        # Add LED
        add_LED = request.args.get("LED_scene") 
        if add_LED is not None:
            ADD_LED(scene, add_LED)
 
    if request.method == "POST": 
        # Delete scene
        if 'delete' in request.form:
            DEL_SCENE(scene)

    led_update = ""
    led_update = LED_SET_SCENE(scene)

    entries_scene = GET_SCENE(scene)[0]
    scene_name    = GET_SCENE(scene)[1]
    dropdown_list = GET_DROPDOWN_LIST_LED()

    return render_template('dashboard_LED_scenes.html', 
                            led_update=led_update,
                            entries_scene=entries_scene,
                            scene_name=scene_name,
                            dropdown_list=dropdown_list,
                            number=scene,
                            active04="active"
                            )



# LED scene 05
@app.route('/dashboard/LED/scene_05', methods=['GET', 'POST'])
@login_required
@superuser_required
def dashboard_LED_scene_05():
    scene = 5

    if request.method == "GET":  
            
        # Change scene name
        name = request.args.get("name") 
        if name is not None:
            SET_SCENE_NAME(scene, name)
    
        # Set RGB color
        rgb_scene = []
        for i in range(1,10):
            rgb_scene.append(request.args.get(str(scene) + " " + str(i)))     
        SET_SCENE_COLOR(scene, rgb_scene)

        # Set brightness
        brightness = []
        for i in range(1,10):
            brightness.append(request.args.get(str(i)))
        SET_SCENE_BRIGHTNESS(scene, brightness)  

        # Add LED
        add_LED = request.args.get("LED_scene") 
        if add_LED is not None:
            ADD_LED(scene, add_LED)
 

    if request.method == "POST": 
        # Delete scene
        if 'delete' in request.form:
            DEL_SCENE(scene)

    led_update = ""
    led_update = LED_SET_SCENE(scene)

    entries_scene = GET_SCENE(scene)[0]
    scene_name    = GET_SCENE(scene)[1]
    dropdown_list = GET_DROPDOWN_LIST_LED()

    return render_template('dashboard_LED_scenes.html',
                            led_update=led_update,
                            entries_scene=entries_scene,
                            scene_name=scene_name,
                            dropdown_list=dropdown_list,
                            number=scene,
                            active05="active"
                            )


# LED scene 06
@app.route('/dashboard/LED/scene_06', methods=['GET', 'POST'])
@login_required
@superuser_required
def dashboard_LED_scene_06():
    scene = 6

    if request.method == "GET":  
            
        # Change scene name
        name = request.args.get("name") 
        if name is not None:
            SET_SCENE_NAME(scene, name)
    
        # Set RGB color
        rgb_scene = []
        for i in range(1,10):
            rgb_scene.append(request.args.get(str(scene) + " " + str(i)))  
        SET_SCENE_COLOR(scene, rgb_scene)

        # Set brightness
        brightness = []
        for i in range(1,10):
            brightness.append(request.args.get(str(i)))
        SET_SCENE_BRIGHTNESS(scene, brightness)  

        # Add LED
        add_LED = request.args.get("LED_scene") 
        if add_LED is not None:
            ADD_LED(scene, add_LED)
 
    if request.method == "POST": 
        # Delete scene
        if 'delete' in request.form:
            DEL_SCENE(scene)

    led_update = ""
    led_update = LED_SET_SCENE(scene)

    entries_scene = GET_SCENE(scene)[0]
    scene_name    = GET_SCENE(scene)[1]
    dropdown_list = GET_DROPDOWN_LIST_LED()

    return render_template('dashboard_LED_scenes.html',
                            led_update=led_update,
                            entries_scene=entries_scene,
                            scene_name=scene_name,
                            dropdown_list=dropdown_list,
                            number=scene,
                            active06="active"
                            )


# LED scene 07
@app.route('/dashboard/LED/scene_07', methods=['GET', 'POST'])
@login_required
@superuser_required
def dashboard_LED_scene_07():
    scene = 7

    if request.method == "GET":  
            
        # Change scene name
        name = request.args.get("name") 
        if name is not None:
            SET_SCENE_NAME(scene, name)
    
        # Set RGB color
        rgb_scene = []
        for i in range(1,10):
            rgb_scene.append(request.args.get(str(scene) + " " + str(i))) 
        SET_SCENE_COLOR(scene, rgb_scene)

        # Set brightness
        brightness = []
        for i in range(1,10):
            brightness.append(request.args.get(str(i)))
        SET_SCENE_BRIGHTNESS(scene, brightness)  

        # Add LED
        add_LED = request.args.get("LED_scene") 
        if add_LED is not None:
            ADD_LED(scene, add_LED)
 
    if request.method == "POST": 
        # Delete scene
        if 'delete' in request.form:
            DEL_SCENE(scene)

    led_update = ""
    led_update = LED_SET_SCENE(scene)

    entries_scene = GET_SCENE(scene)[0]
    scene_name    = GET_SCENE(scene)[1]
    dropdown_list = GET_DROPDOWN_LIST_LED()

    return render_template('dashboard_LED_scenes.html', 
                            led_update=led_update,
                            entries_scene=entries_scene,
                            scene_name=scene_name,
                            dropdown_list=dropdown_list,
                            number=scene,
                            active07="active"
                            )


# LED scene 08
@app.route('/dashboard/LED/scene_08', methods=['GET', 'POST'])
@login_required
@superuser_required
def dashboard_LED_scene_08():
    scene = 8

    if request.method == "GET":  
            
        # Change scene name
        name = request.args.get("name") 
        if name is not None:
            SET_SCENE_NAME(scene, name)
    
        # Set RGB color
        rgb_scene = []
        for i in range(1,10):
            rgb_scene.append(request.args.get(str(scene) + " " + str(i)))      
        SET_SCENE_COLOR(scene, rgb_scene)

        # Set brightness
        brightness = []
        for i in range(1,10):
            brightness.append(request.args.get(str(i)))
        SET_SCENE_BRIGHTNESS(scene, brightness)  

        # Add LED
        add_LED = request.args.get("LED_scene") 
        if add_LED is not None:
            ADD_LED(scene, add_LED)
 
    if request.method == "POST": 
        # Delete scene
        if 'delete' in request.form:
            DEL_SCENE(scene)

    led_update = ""
    led_update = LED_SET_SCENE(scene)

    entries_scene = GET_SCENE(scene)[0]
    scene_name    = GET_SCENE(scene)[1]
    dropdown_list = GET_DROPDOWN_LIST_LED()

    return render_template('dashboard_LED_scenes.html', 
                            led_update=led_update,
                            entries_scene=entries_scene,
                            scene_name=scene_name,
                            dropdown_list=dropdown_list,
                            number=scene,
                            active08="active"
                            )


# LED scene 09
@app.route('/dashboard/LED/scene_09', methods=['GET', 'POST'])
@login_required
@superuser_required
def dashboard_LED_scene_09():
    scene = 9

    if request.method == "GET":  
            
        # Change scene name
        name = request.args.get("name") 
        if name is not None:
            SET_SCENE_NAME(scene, name)
    
        # Set RGB color
        rgb_scene = []
        for i in range(1,10):
            rgb_scene.append(request.args.get(str(scene) + " " + str(i)))     
        SET_SCENE_COLOR(scene, rgb_scene)

        # Set brightness
        brightness = []
        for i in range(1,10):
            brightness.append(request.args.get(str(i)))
        SET_SCENE_BRIGHTNESS(scene, brightness)  

        # Add LED
        add_LED = request.args.get("LED_scene") 
        if add_LED is not None:
            ADD_LED(scene, add_LED)
 

    if request.method == "POST": 
        # Delete scene
        if 'delete' in request.form:
            DEL_SCENE(scene)

    led_update = ""
    led_update = LED_SET_SCENE(scene)

    entries_scene = GET_SCENE(scene)[0]
    scene_name    = GET_SCENE(scene)[1]
    dropdown_list = GET_DROPDOWN_LIST_LED()

    return render_template('dashboard_LED_scenes.html',
                            led_update=led_update,
                            entries_scene=entries_scene,
                            scene_name=scene_name,
                            dropdown_list=dropdown_list,
                            number=scene,
                            active09="active"
                            )


# Delete LED 
@app.route('/dashboard/LED/scene/delete/<int:scene>/<int:id>')
@login_required
@superuser_required
def delete_LED(scene, id): 
    DEL_LED(scene, id)
    if scene == 1:
        return redirect(url_for('dashboard_LED_scene_01'))
    if scene == 2:
        return redirect(url_for('dashboard_LED_scene_02'))
    if scene == 3:
        return redirect(url_for('dashboard_LED_scene_03'))
    if scene == 4:
        return redirect(url_for('dashboard_LED_scene_04'))
    if scene == 5:
        return redirect(url_for('dashboard_LED_scene_05'))
    if scene == 6:
        return redirect(url_for('dashboard_LED_scene_06'))
    if scene == 7:
        return redirect(url_for('dashboard_LED_scene_07'))
    if scene == 8:
        return redirect(url_for('dashboard_LED_scene_08'))
    if scene == 9:
        return redirect(url_for('dashboard_LED_scene_09'))


# LED programs
@app.route('/dashboard/LED/programs', methods=['GET', 'POST'])
@login_required
@superuser_required
def dashboard_LED_programs():

    program = ""
    rgb = "rgb(0, 0, 0)"
    led_update = ""

    if request.method == "GET": 
        # create a new program
        new_program = request.args.get("new_program") 
        if new_program is not None and new_program is not "":
            NEW_PROGRAM(new_program)

        # get the selected program
        get_Program = request.args.get("get_program") 
        if get_Program is not None:
            program = GET_PROGRAM_NAME(get_Program)

        # update programs, i = program ID
        for i in range(1,25):
            update_Program = request.args.get("update_" + str(i))
            if update_Program is not None:
                UPDATE_PROGRAM(i, update_Program)

        # start program
        for i in range(1,25):
            start_Program = request.args.get("start_" + str(i))
            if start_Program is not None:
                led_update = START_PROGRAM(i)

        # get rgb values
        for i in range(1,25):
            get_rgb = request.args.get("get_rgb_" + str(i)) 
            if get_rgb is not None:
                rgb = get_rgb               
                program = GET_PROGRAM_ID(i)  

        # rename program
        for i in range(1,25):
            program_name = request.args.get("program_name_" + str(i)) 
            if program_name is not None:
                SET_PROGRAM_NAME(i, program_name)              
                program = GET_PROGRAM_ID(i)  
            
        # delete the selected program
        delete_Program = request.args.get("delete_program") 
        if delete_Program is not None:
            DELETE_PROGRAM(delete_Program)              

    dropdown_list = GET_DROPDOWN_LIST_PROGRAMS()

    return render_template('dashboard_LED_programs.html',
                            led_update=led_update,
                            dropdown_list=dropdown_list,
                            program=program,
                            rgb=rgb
                            )


# LED settings
@app.route('/dashboard/LED/settings')
@login_required
@superuser_required
def dashboard_LED_settings():

    led_update = "" 

    if request.method == "GET": 
        # change bridge ip
        bridge_ip = request.args.get("bridge_ip") 
        if bridge_ip is not None:
            SET_BRIDGE_IP(bridge_ip)
            led_update = UPDATE_LED()

    ip = GET_BRIDGE_IP()            
    LED_list = GET_ALL_LEDS()

    return render_template('dashboard_LED_settings.html',
                            led_update=led_update,
                            ip=ip,
                            LED_list=LED_list
                            )


""" ############## """
""" Site Schedular """
""" ############## """

# Dashboard tasks
@app.route('/dashboard/schedular/', methods=['GET'])
@login_required
@superuser_required
def dashboard_schedular():

    error_massage = ""
    set_name = ""
    set_task = ""

    if request.method == "GET": 
        # change bridge ip
        if request.args.get("set_name") is not None:
            if request.args.get("set_name") == "":
                error_massage = "Kein Name angegeben"
                set_task = request.args.get("set_task")
            elif request.args.get("set_task") == "":
                error_massage = "Keine Aufgabe angegeben"  
                set_name = request.args.get("set_name")             
            else:         
                name   = request.args.get("set_name")
                day    = request.args.get("set_day") 
                hour   = request.args.get("set_hour") 
                minute = request.args.get("set_minute")
                task   = request.args.get("set_task")
                if request.args.get("checkbox"):
                    repeat = True
                else:
                    repeat = False

                check_entry = Schedular.query.filter_by(name=name).first()
                if check_entry is None:
                    # find a unused id
                    for i in range(1,25):
                        if Schedular.query.filter_by(id=i).first():
                            pass
                        else:
                            # add the new program
                            task = Schedular(
                                    id     = i,
                                    name   = name,
                                    day    = day,
                                    hour   = hour,
                                    minute = minute,
                                    task   = task,
                                    repeat = repeat,
                                )
                            db.session.add(task)
                            db.session.commit()
                            break
 
    schedular_list = Schedular.query.all()

    dropdown_list_days    = ["*", "Mon", "Thu", "Wed", "Thu", "Fri", "Sat", "Sun"]
    dropdown_list_hours   = ["*", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12",
                             "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23"]
    dropdown_list_minutes = ["*", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12",
                             "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23", "24", 
                             "25", "26", "27", "28", "29", "30", "31", "32", "33", "34", "35", "36", 
                             "37", "38", "39", "40", "41", "42", "43", "44", "45", "46", "47", "48",
                             "49", "50", "51", "52", "53", "54", "55", "56", "57", "58", "59"]

    return render_template('dashboard_schedular.html',
                            dropdown_list_days=dropdown_list_days,
                            dropdown_list_hours=dropdown_list_hours,
                            dropdown_list_minutes=dropdown_list_minutes,
                            schedular_list=schedular_list,
                            error_massage=error_massage,
                            set_name=set_name,
                            set_task=set_task
                            )


# Delete tasks
@app.route('/dashboard/schedular/delete/<int:id>')
@login_required
@superuser_required
def delete_schedular(id):
    Schedular.query.filter_by(id=id).delete()
    db.session.commit()
    return redirect(url_for('dashboard_schedular'))


""" ########## """
""" Sites User """
""" ########## """

# Dashboard user
@app.route('/dashboard/user/', methods=['GET', 'POST'])
@login_required
@superuser_required
def dashboard_user():
    user_list = User.query.all()
    return render_template('dashboard_user.html',
                            name=current_user.username,
                            user_list=user_list,
                            )


# Change user role
@app.route('/dashboard/user/role/<int:id>')
@login_required
@superuser_required
def promote_user(id):
    entry = User.query.get(id)
    entry.role = "superuser"
    db.session.commit()
    user_list = User.query.all()
    return redirect(url_for('dashboard_user'))


# Delete user
@app.route('/dashboard/user/delete/<int:id>')
@login_required
@superuser_required
def delete_user(id):
    User.query.filter_by(id=id).delete()
    db.session.commit()
    user_list = User.query.all()
    return redirect(url_for('dashboard_user'))


""" ########### """
""" Sites Other """
""" ########### """

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


# Host files for colorpicker_local
@app.route('/get_media/<path:filename>', methods=['GET'])
def get_media(filename):
    return send_from_directory(PATH_CSS, filename)


if __name__ == '__main__':
    scheduler.start()
    app.run(debug=True)

