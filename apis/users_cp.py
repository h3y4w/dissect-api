from __future__ import absolute_import
import jwt
from flask_restful import Resource, abort, request
from flask import make_response
from datetime import datetime, timedelta
from functools import wraps
from flask_sqlalchemy import SQLAlchemy
db=SQLAlchemy()
def user_setup(db_):
    global db
    db=db_
def login_and_role(*roles):
    def wrapper(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            print request.headers['Authorization']
            payload=Tokens.valid(request.headers['Authorization'])
            if payload['uro'] not in roles or roles is not None:
                abort(401)
            return f(*args, **kwargs)
        return wrapped
    return wrapper

class Tokens (object):

    @staticmethod
    def valid(t):
        try:
            return jwt.decode(t, 'secret')
        except jwt.ExpiredSignatureError:
            r=make_response('Token Expired',401)
            print 'Token Expired'
            return abort(r)
        except:
            return {'uro':None}

    @staticmethod
    def generate(user):
        payload = {
            'uid': user.id,
            'uro': user.role,
            'iat': datetime.utcnow(),
            'exp': datetime.utcnow() + timedelta(hours=1)
        }
        return jwt.encode(payload,'secret')

class Users:
    class DB(db.Model):
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
            return Users.DB.query.filter_by(email=user['email'], password=user['password']).first()

    class Register(Resource):
        def post(self):
            params=request.get_json(force=True)
            user = Users.DB(params)
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
            user = Users.DB.auth(params)
            if user is not None:
                return {'token': Tokens.generate(user)}
            else:
                abort(401)



    class Files:

        class File(db.Model):
            id = db.Column(db.Integer, primary_key=True)
            user_id = db.Column(db.Integer)
            parts = db.Column(db.Integer)
            size = db.Column(db.Integer)
            name = db.Column(db.String(100))









    class hey(Resource):
        @login_and_role()
        def get(self):
            return 'itworked'
