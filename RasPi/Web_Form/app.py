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

from RBGtoXY import RGBtoXY
from phue import Bridge
from REST_API import TodoListResource, TodoResource


app = Flask(__name__)
app.config['SECRET_KEY'] = 'Thisissupposedtobesecret!'

# REST_API
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


class Hue(db.Model):

    __tablename__ = 'hue'
    id          = db.Column(db.Integer, primary_key=True)
    ip          = db.Column(db.String(50), unique=True)
    color_red   = db.Column(db.Integer)
    color_green = db.Column(db.Integer)
    color_blue  = db.Column(db.Integer)
    color_y     = db.Column(db.Float)
    color_x     = db.Column(db.Float)
    brightness  = db.Column(db.Integer)

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

# Create default hue settings
if Hue.query.filter_by().first() is None:
    hue = Hue(
        id = '1',
        ip = 'default',
    )
    db.session.add(hue)
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

@app.route('/')
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
    return render_template('dashboard.html',
                            name=current_user.username,
                            user_list=user_list 
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


# philips hue
@app.route('/dashboard/hue/', methods=['GET', 'POST'])
@login_required
@superuser_required
def dashboard_hue():

    id = 1
    entry = Hue.query.get(id)


    # RGB control
    if entry.color_red is not None:
        red   = entry.color_red
        green = entry.color_green
        blue  = entry.color_blue    
    else:
        red   = ''
        green = ''
        blue  = ''

    if request.method == 'POST':
 
        try:
            red   = request.form['slider_red']
            green = request.form['slider_green']
            blue  = request.form['slider_blue'] 

            xy = RGBtoXY(float(red), float(green), float(blue))

            entry.color_x     = xy[0]
            entry.color_y     = xy[1]
            entry.color_red   = red
            entry.color_green = green
            entry.color_blue  = blue     
            db.session.commit()    

        except:
            pass


    # brightness
    if entry.brightness is not None:
        brightness = entry.brightness    
    else:
        brightness = 0

    if request.method == 'POST':
 
        try:
            brightness = request.form['slider_brightness']
            entry.brightness = brightness     
            db.session.commit()    
   
        except:
            pass     


    # HUE settings
    ip = entry.ip 

    if request.args.get("ip") is not None:
        ip = request.args.get("ip")
        entry.ip = ip
        db.session.commit()

    #b = Bridge(ip)

    return render_template('dashboard.html', 
                            red=red,
                            green=green, 
                            blue=blue, 
                            brightness=brightness,
                            ip=ip)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
