from flask import Flask, jsonify, abort, make_response
from flask_restful import reqparse, abort, Resource, fields, marshal_with
from flask_httpauth import HTTPBasicAuth

from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


""" ######## """
""" database """
""" ######## """

# database login 
Session = sessionmaker(autocommit = False,
                       autoflush  = False,
                       bind       = create_engine('mysql+pymysql://python:python@localhost/python'))
session = scoped_session(Session)

# table structure
user_fields = {'id'      : fields.Integer,
               'username': fields.String,
               'email'   : fields.String,
               'password': fields.String, 
               'uri'     : fields.Url('user', absolute=True),
               }

parser = reqparse.RequestParser()
parser.add_argument('username', type=str)
parser.add_argument('email',    type=str)
parser.add_argument('password', type=str)

class Todo(Base):

    """ Database informations """

    __tablename__ = 'user'

    id       = Column(Integer, primary_key=True)
    username = Column(String(15), unique=True)
    email    = Column(String(50), unique=True)
    password = Column(String(80))


""" ################ """
""" authentification """
""" ################ """

auth = HTTPBasicAuth()

# definate user
USER_DATA = {"admin": "SuperSecretPwd"}

@auth.verify_password
def verify(username, password):
    if not (username and password):
        return False
    return USER_DATA.get(username) == password

@auth.error_handler
def unauthorized():
    return make_response(jsonify({'message': 'Unauthorized access'}), 403)


""" ######### """
""" functions """
""" ######### """

# specific entry
class TodoResource(Resource):
    decorators = [auth.login_required]

    @marshal_with(user_fields)
    def get(self, id):
        todo = session.query(Todo).filter(Todo.id == id).first()
        if not todo:
            abort(404, message="User {} doesn't exist".format(id))
        return todo

    def delete(self, id):
        todo = session.query(Todo).filter(Todo.id == id).first()
        if not todo:
            return "ID {} doesn't exist".format(id)
        session.delete(todo)
        session.commit()
        return "ID {} deleted".format(id)

    @marshal_with(user_fields)
    def put(self, id):
        parsed_args = parser.parse_args()
        todo = session.query(Todo).filter(Todo.id == id).first()
        
        if (parsed_args['username']) is not None:
            todo.username = parsed_args['username']
        if (parsed_args['email']) is not None:    
            todo.email = parsed_args['email']
        if (parsed_args['password']) is not None:  
            todo.password = parsed_args['password']

        session.add(todo)
        session.commit()
        return todo, 201


class TodoListResource(Resource):
    decorators = [auth.login_required] 

    @marshal_with(user_fields)
    def get(self):
        todo = session.query(Todo).all()
        return todo

    @marshal_with(user_fields)
    def post(self):
        parsed_args = parser.parse_args()
        todo = Todo(username = parsed_args['username'],
                    email    = parsed_args['email'],
                    password = parsed_args['password'])
        session.add(todo)
        session.commit()
        return todo, 201


if __name__ == "__main__":
    
    from sqlalchemy import create_engine
    from settings import DB_URI
    
    engine = create_engine(DB_URI)
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)