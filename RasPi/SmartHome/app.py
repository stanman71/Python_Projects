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


""" ################# """
""" genernal settings """
""" ################# """

# Windows Home
sys.path.insert(0, "C:/Users/stanman/Desktop/Unterlagen/GIT/Python_Projects/RasPi/SmartHome/led")
PATH = 'C:/Users/stanman/Desktop/Unterlagen/GIT/Python_Projects/RasPi/SmartHome/static/CDNJS/'

# Windows Work
#sys.path.insert(0, "C:/Users/mstan/GIT/Python_Projects/RasPi/SmartHome/led")
#PATH = 'C:/Users/mstan/GIT/Python_Projects/RasPi/SmartHome/static/CDNJS/'

# RasPi:
#sys.path.insert(0, "/home/pi/Python/SmartHome/led")
#PATH = '/home/pi/Python/static/CDNJS/'


""" ##### """
""" flask """
""" ##### """

from colorpicker_local import colorpicker
from LED import *
from LED_control import *

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Thisissupposedtobesecret!'
colorpicker(app)


""" ######## """
""" database """
""" ######## """

# Database login 
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://python:python@localhost/raspi'
bootstrap = Bootstrap(app)
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Database table entries
class User(UserMixin, db.Model):
    __tablename__ = 'user'
    id       = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True)
    email    = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(100))
    role     = db.Column(db.String(20))

# Create all database tables
db.create_all()

# Create default user
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

# Role Management
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


""" ########## """
""" Sites User """
""" ########## """

# landing page
@app.route('/', methods=['GET', 'POST'])
def index():

    if request.method == "POST":         
        # Change scene
        for i in range(1,10):
            if str(i) in request.form:               
                print(i)

    if request.method == "GET":              
        # Change brightness
        brightness_global = request.args.get("brightness_global") 
        if brightness_global is not None:
            SET_BRIGHTNESS_GLOBAL(brightness_global) 

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

    brightness_global = GET_BRIGHTNESS_GLOBAL()
    LED_SET_BRIGHTNESS_GLOBAL(brightness_global)
    
    return render_template('index.html', 
                            scene_name_01=scene_name_01,
                            scene_name_02=scene_name_02,
                            scene_name_03=scene_name_03,
                            scene_name_04=scene_name_04,
                            scene_name_05=scene_name_05,
                            brightness_global=brightness_global
                            )


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


# Dashboard user
@app.route('/dashboard/user/', methods=['GET', 'POST'])
@login_required
@superuser_required
def dashboard_user():
    user_list = User.query.all()
    return render_template('dashboard_user.html',
                            name=current_user.username,
                            user_list=user_list,
                            siteID="user" 
                            )


# Change user role
@app.route('/dashboard/user/role/<int:id>')
@login_required
@superuser_required
def promote(id):
    entry = User.query.get(id)
    entry.role = "superuser"
    db.session.commit()
    user_list = User.query.all()
    return redirect(url_for('dashboard_user'))


# Delete user
@app.route('/dashboard/user/delete/<int:id>')
@login_required
@superuser_required
def delete(id):
    User.query.filter_by(id=id).delete()
    db.session.commit()
    user_list = User.query.all()
    return redirect(url_for('dashboard_user'))


""" ############ """
""" Sites Scenes """
""" ############ """

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
            rgb_scene.append(request.args.get("1 " + str(i)))
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
        if 'start' in request.form:
            print("start")


    entries_scene = GET_SCENE(scene)[0]
    scene_name    = GET_SCENE(scene)[1]
    dropdown_list = GET_DROPDOWN_LIST()

    return render_template('dashboard_LED_scene_01.html', 
                            entries_scene=entries_scene,
                            scene_name=scene_name,
                            dropdown_list=dropdown_list
                            )


# Delete LED scene 01
@app.route('/dashboard/LED/scene_01/delete/<int:id>')
@login_required
@superuser_required
def delete_LED_scene_01(id): 
    DEL_LED(1, id)
    return redirect(url_for('dashboard_LED_scene_01'))


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
            rgb_scene.append(request.args.get("2 " + str(i)))  
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
        if 'start' in request.form:
            print("start") 

    entries_scene = GET_SCENE(scene)[0]
    scene_name    = GET_SCENE(scene)[1]
    dropdown_list = GET_DROPDOWN_LIST()

    return render_template('dashboard_LED_scene_02.html', 
                            entries_scene=entries_scene,
                            scene_name=scene_name,
                            dropdown_list=dropdown_list
                            )


# Delete LED scene 02
@app.route('/dashboard/LED/scene_02/delete/<int:id>')
@login_required
@superuser_required
def delete_LED_scene_02(id):
    DEL_LED(2, id)
    return redirect(url_for('dashboard_LED_scene_02'))


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
            rgb_scene.append(request.args.get("3 " + str(i))) 
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
        if 'start' in request.form:
            print("start") 

    entries_scene = GET_SCENE(scene)[0]
    scene_name    = GET_SCENE(scene)[1]
    dropdown_list = GET_DROPDOWN_LIST()

    return render_template('dashboard_LED_scene_03.html', 
                            entries_scene=entries_scene,
                            scene_name=scene_name,
                            dropdown_list=dropdown_list
                            )


# Delete LED scene 03
@app.route('/dashboard/LED/scene_03/delete/<int:id>')
@login_required
@superuser_required
def delete_LED_scene_03(id):
    DEL_LED(3, id)
    return redirect(url_for('dashboard_LED_scene_03'))


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
            rgb_scene.append(request.args.get("4 " + str(i)))      
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
        if 'start' in request.form:
            print("start")

    entries_scene = GET_SCENE(scene)[0]
    scene_name    = GET_SCENE(scene)[1]
    dropdown_list = GET_DROPDOWN_LIST()

    return render_template('dashboard_LED_scene_04.html', 
                            entries_scene=entries_scene,
                            scene_name=scene_name,
                            dropdown_list=dropdown_list
                            )


# Delete LED scene 04
@app.route('/dashboard/LED/scene_04/delete/<int:id>')
@login_required
@superuser_required
def delete_LED_scene_04(id):
    DEL_LED(4, id)
    return redirect(url_for('dashboard_LED_scene_04'))


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
            rgb_scene.append(request.args.get("5 " + str(i)))     
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
        if 'start' in request.form:
            print("start")   

    entries_scene = GET_SCENE(scene)[0]
    scene_name    = GET_SCENE(scene)[1]
    dropdown_list = GET_DROPDOWN_LIST()

    return render_template('dashboard_LED_scene_05.html', 
                            entries_scene=entries_scene,
                            scene_name=scene_name,
                            dropdown_list=dropdown_list
                            )


# Delete LED scene 05
@app.route('/dashboard/LED/scene_05/delete/<int:id>')
@login_required
@superuser_required
def delete_LED_scene_05(id): 
    DEL_LED(5, id)
    return redirect(url_for('dashboard_LED_scene_05'))


# LED programs
@app.route('/dashboard/LED/programs')
@login_required
@superuser_required
def dashboard_LED_programs():
    return render_template('dashboard_LED_programs.html', 
                            )


# LED settings
@app.route('/dashboard/LED/settings', methods=['GET', 'POST'])
@login_required
@superuser_required
def dashboard_LED_settings():
    ip = GET_BRIDGE_IP()
    entries_LED = GET_LED()        
        
    if request.method == "GET":  
            
        # Change ip
        if request.args.get("ip") is not None:
            ip = request.args.get("ip")   
            SET_BRIDGE_IP(ip)
        
        # Change LED name
        name_error = "" 
        for i in range(1,10):
            name = request.args.get(str(i)) 
            if name is not None:
                name_error = SET_LED_NAME(i, name)

    return render_template('dashboard_LED_settings.html', 
                            ip=ip,
                            entries_LED=entries_LED,
                            name_error=name_error
                            )


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
    return send_from_directory(PATH, filename)


if __name__ == '__main__':
    app.run(debug=True)
