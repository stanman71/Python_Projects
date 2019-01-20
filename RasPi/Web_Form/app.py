from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap
from flask_restful import Api
from flask_wtf import FlaskForm 
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Email, Length
from flask_sqlalchemy  import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from functools import wraps
from flask_colorpicker import colorpicker

from REST_API import TodoListResource, TodoResource


app = Flask(__name__)
app.config['SECRET_KEY'] = 'Thisissupposedtobesecret!'
colorpicker(app)


""" ######## """
""" REST_API """
""" ######## """

api = Api(app)
api.add_resource(TodoListResource, '/api/resource', endpoint='users')
api.add_resource(TodoResource, '/api/resource/<string:id>', endpoint='user')


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


""" ##### """
""" Sites """
""" ##### """

@app.route('/', methods=['GET', 'POST'])
def index():

    return render_template('index.html')


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


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegisterForm()

    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method='sha256')
        new_user = User(username=form.username.data, email=form.email.data, password=hashed_password, role="user")
        db.session.add(new_user)
        db.session.commit()
        return render_template('index.html', form=form, check=True)
        
    return render_template('signup.html', form=form)


@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
@superuser_required
def dashboard():
    return render_template('dashboard.html', name=current_user.username)


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


# HUE scenes
@app.route('/dashboard/hue/scenes', methods=['GET', 'POST'])
@login_required
@superuser_required
def dashboard_hue_scenes():

    from hue.hue import SET_SCENE_NAME, DEL_SCENE, GET_SCENE_01, GET_SCENE_02, GET_SCENE_03, GET_SCENE_04, GET_SCENE_05

    if request.method == "GET":  
            
        # Change scene name
        name_01 = request.args.get("name_01") 
        if name_01 is not None:
            SET_SCENE_NAME(1, name_01)
        name_02 = request.args.get("name_02")
        if name_02 is not None:
            SET_SCENE_NAME(2, name_02)
        name_03 = request.args.get("name_03")
        if name_03 is not None:
            SET_SCENE_NAME(3, name_03)
        name_04 = request.args.get("name_04")
        if name_04 is not None:                   
            SET_SCENE_NAME(4, name_04)
        name_05 = request.args.get("name_05")
        if name_05 is not None:
            SET_SCENE_NAME(5, name_05)

        # RGB
        rgb_11 = request.args.get("1 1") 
        rgb_12 = request.args.get("1 2")

        print(rgb_11)
        print(rgb_12)


    if request.method == "POST": 

        # Delete scene
        if 'delete_1' in request.form:
            DEL_SCENE("1")
        if 'delete_2' in request.form:
            DEL_SCENE("2")
        if 'delete_3' in request.form:
            DEL_SCENE("3")
        if 'delete_4' in request.form:
            DEL_SCENE("4")
        if 'delete_5' in request.form:
            DEL_SCENE("5")


    try:
        entries_scene_01 = GET_SCENE_01()[0]
    except:
        entries_scene_01 = None
    try:    
        scene_01_name    = GET_SCENE_01()[1]
    except:
        scene_01_name    = None
    try:
        entries_scene_02 = GET_SCENE_02()[0]
    except:
        entries_scene_02 = None
    try:
        scene_02_name    = GET_SCENE_02()[1]
    except: 
        scene_02_name    = None
    try: 
        entries_scene_03 = GET_SCENE_03()[0]
    except:  
        entries_scene_03 = None
    try: 
        scene_03_name    = GET_SCENE_03()[1]
    except: 
        scene_03_name    = None
    try:
        entries_scene_04 = GET_SCENE_04()[0]
    except:  
        entries_scene_04 = None
    try:
        scene_04_name    = GET_SCENE_04()[1]
    except:  
        scene_04_name    = None
    try:
        entries_scene_05 = GET_SCENE_05()[0]
    except:  
        entries_scene_05 = None
    try:
        scene_05_name    = GET_SCENE_05()[1]
    except:  
        scene_05_name    = None
 

    return render_template('dashboard_hue_scenes.html', 
                            entries_scene_01=entries_scene_01,
                            entries_scene_02=entries_scene_02,
                            entries_scene_03=entries_scene_03,
                            entries_scene_04=entries_scene_04,
                            entries_scene_05=entries_scene_05,
                            scene_01_name=scene_01_name,
                            scene_02_name=scene_02_name,
                            scene_03_name=scene_03_name,
                            scene_04_name=scene_04_name,
                            scene_05_name=scene_05_name,
                            rgb_11="rgb(234, 41, 41)",
                            rgb_12="rgb(234, 0, 41)",
                            siteID="hue",
                            hueSITE="scenes")


# HUE settings
@app.route('/dashboard/hue/settings', methods=['GET', 'POST'])
@login_required
@superuser_required
def dashboard_hue_settings():

    from hue.hue import GET_IP, SET_IP

    ID = 1
    ip = GET_IP()
                         
    if request.method == "GET":  
            
        # Change ip
        if request.args.get("ip") is not None:
            ip = request.args.get("ip")   
            SET_IP(ip)
                 
    return render_template('dashboard_hue_settings.html', 
                            ip=ip,
                            siteID="hue",
                            hueSITE="settings")



@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
