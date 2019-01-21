from flask import Flask, render_template, redirect, url_for, request, send_from_directory
from flask_bootstrap import Bootstrap
from flask_restful import Api
from flask_wtf import FlaskForm 
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Email, Length
from flask_sqlalchemy  import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from functools import wraps
from hue.colorpicker_local import colorpicker

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


# HUE scene 01
@app.route('/dashboard/hue/scene_01', methods=['GET', 'POST'])
@login_required
@superuser_required
def dashboard_hue_scene_01():

    from hue.hue import GET_DROPDOWN_LIST, ADD_BULK, SET_SCENE_NAME, SET_SCENE_COLOR, DEL_SCENE, GET_SCENE

    scene = 1

    if request.method == "GET":  
            
        # Change scene name
        name = request.args.get("name") 
        if name is not None:
            SET_SCENE_NAME(scene, name)
    
        # Set RGB color
        rgb_scene = []

        for i in range(1,10):
            rgb_scene.append(request.args.get("1 " + str(i)))

        SET_SCENE_COLOR(scene, rgb_scene)

        # Add bulb
        add_bulb = request.args.get("bulb_scene") 
        if add_bulb is not None:
            ADD_BULK(scene, add_bulb)
 

    if request.method == "POST": 

        # Delete scene
        if 'delete' in request.form:
            DEL_SCENE(scene)

    try:
        entries_scene = GET_SCENE(scene)[0]
    except:
        entries_scene = None
    try:    
        scene_name    = GET_SCENE(scene)[1]
    except:
        scene_name    = None
 
    dropdown_list = GET_DROPDOWN_LIST()

    return render_template('dashboard_hue_scene_01.html', 
                            entries_scene=entries_scene,
                            scene_name=scene_name,
                            dropdown_list=dropdown_list
                            )


# Delete bulk scene 01
@app.route('/dashboard/hue/scene_01/delete/<int:id>')
@login_required
@superuser_required
def delete_bulk_scene_01(id):
    
    from hue.hue import DEL_BULK 
    DEL_BULK(1, id)

    return redirect(url_for('dashboard_hue_scene_01'))


# HUE scene 02
@app.route('/dashboard/hue/scene_02', methods=['GET', 'POST'])
@login_required
@superuser_required
def dashboard_hue_scene_02():

    from hue.hue import GET_DROPDOWN_LIST, ADD_BULK, SET_SCENE_NAME, SET_SCENE_COLOR, DEL_SCENE, GET_SCENE

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

        # Add bulb
        add_bulb = request.args.get("bulb_scene") 
        if add_bulb is not None:
            ADD_BULK(scene, add_bulb)
 

    if request.method == "POST": 

        # Delete scene
        if 'delete' in request.form:
            DEL_SCENE(scene)
   
    try:
        entries_scene = GET_SCENE(scene)[0]
    except:
        entries_scene = None
    try:    
        scene_name    = GET_SCENE(scene)[1]
    except:
        scene_name    = None
 
    dropdown_list = GET_DROPDOWN_LIST()

    return render_template('dashboard_hue_scene_02.html', 
                            entries_scene=entries_scene,
                            scene_name=scene_name,
                            dropdown_list=dropdown_list
                            )


# Delete bulk scene 02
@app.route('/dashboard/hue/scene_02/delete/<int:id>')
@login_required
@superuser_required
def delete_bulk_scene_02(id):
    
    from hue.hue import DEL_BULK 
    DEL_BULK(2, id)

    return redirect(url_for('dashboard_hue_scene_02'))


# HUE scene 03
@app.route('/dashboard/hue/scene_03', methods=['GET', 'POST'])
@login_required
@superuser_required
def dashboard_hue_scene_03():

    from hue.hue import GET_DROPDOWN_LIST, ADD_BULK, SET_SCENE_NAME, SET_SCENE_COLOR, DEL_SCENE, GET_SCENE

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

        # Add bulb
        add_bulb = request.args.get("bulb_scene") 
        if add_bulb is not None:
            ADD_BULK(scene, add_bulb)
 

    if request.method == "POST": 

        # Delete scene
        if 'delete' in request.form:
            DEL_SCENE(scene)
   
    try:
        entries_scene = GET_SCENE(scene)[0]
    except:
        entries_scene = None
    try:    
        scene_name    = GET_SCENE(scene)[1]
    except:
        scene_name    = None
 
    dropdown_list = GET_DROPDOWN_LIST()

    return render_template('dashboard_hue_scene_03.html', 
                            entries_scene=entries_scene,
                            scene_name=scene_name,
                            dropdown_list=dropdown_list
                            )


# Delete bulk scene 03
@app.route('/dashboard/hue/scene_03/delete/<int:id>')
@login_required
@superuser_required
def delete_bulk_scene_03(id):
    
    from hue.hue import DEL_BULK 
    DEL_BULK(3, id)

    return redirect(url_for('dashboard_hue_scene_03'))


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


# Host files for colorpicker_local
@app.route('/get_media/<path:filename>', methods=['GET'])
def get_media(filename):
    return send_from_directory('C:/Users/stanman/Desktop/Unterlagen/GIT/Python_Projects/RasPi/Web_Form/static/colorpicker/', filename)



if __name__ == '__main__':
    app.run(debug=True)
