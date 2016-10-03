from flask_restful import Resource, abort, request
from flask import make_response
from flask_sqlalchemy import SQLAlchemy
from dissect_auth import Tokens, login_required
from dissect_errors import UserErrors
db=SQLAlchemy()
def user_setup(db_):
    global db
    db=db_
class UserTable(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(120))
    role = db.Column(db.String(10))
    def __init__(self, user_info):
        self.first_name = user_info['first_name']
        self.last_name = user_info['last_name']
        self.email = user_info['email']
        self.password = user_info['password'] #hash password here or b4
        self.role='regular'
    @staticmethod
    def auth(user):
        return UserTable.query.filter_by(email=user['email'], password=user['password']).first()


class Users:
    class Register(Resource):
        def post(self):
            params=request.get_json(force=True)
            user = UserTable(params)
            db.session.add(user)
            print db.session.commit()
            {
                'first_name': 'John',
                'last_name': 'Doe',
                'email': 'johndoe@mail.com',
                'password': 'password'
            }
            return {'token': Tokens.generate(user)}

    class Login(Resource):
        def post(self):
            params=request.get_json(force=True)#)
            print params
            user = UserTable.auth(params)
            if user is not None:
                return {'token': Tokens.generate(user)}
            else:
                UserErrors.IncorrectLogin()

    class hey(Resource):
        @login_required()
        def get(self):
            user_id = Tokens.get_user_id(request.headers['Authorization'])
            return user_id
