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
    username = db.Column(db.String(15), unique=True)
    email    = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(80))
    role     = db.Column(db.String(80))



def admin_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if current_user.role == "admin":
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
        new_user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return render_template('index.html', form=form, check=True)
        
    return render_template('signup.html', form=form)


@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
@admin_required
def dashboard():
    return render_template('dashboard.html', name=current_user.username)


@app.route('/dashboard/user/', methods=['GET', 'POST'])
@login_required
def dashboard_user():
    user_list = User.query.all()
    return render_template('dashboard.html',
                            name=current_user.username,
                            user_list=user_list 
                            )


@app.route('/dashboard/user/role/<int:id>')
@login_required
def promote(id):
    entry = User.query.get(id)
    entry.role = "admin"
    db.session.commit()
    user_list = User.query.all()
    return redirect(url_for('dashboard_user'))


@app.route('/dashboard/user/delete/<int:id>')
@login_required
def delete(id):
    User.query.filter_by(id=id).delete()
    db.session.commit()
    user_list = User.query.all()
    return redirect(url_for('dashboard_user'))


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)

    
