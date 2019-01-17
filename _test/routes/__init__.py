from flask import Flask
from routes.index import main
from routes.users import users

app = Flask(__name__)

app.register_blueprint(main, url_prefix='/')
app.register_blueprint(users, url_prefix='/admin')