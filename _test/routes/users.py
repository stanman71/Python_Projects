from flask import Blueprint

users = Blueprint('users', __name__)

@users.route('/')
def index():
    return "Admin"