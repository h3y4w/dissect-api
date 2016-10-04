from datetime import datetime, timedelta
from functools import wraps
import jwt
from flask_restful import request
from flask import Response, abort
from dissect_errors import UserErrors
def login_required(roles=[]):
    def wrapper(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            try:
                payload=Tokens.valid(request.headers['Authorization'])
            except KeyError:
                abort(409)
            if payload['uro'] not in roles and roles != [] :
                UserErrors.IncorrectRole()
            return f(*args, **kwargs)
        return wrapped
    return wrapper

class Tokens (object):

    @staticmethod
    def valid(t):
        try:
            return jwt.decode(t, 'secret')
        except jwt.ExpiredSignatureError:
            return UserErrors.ExpiredToken()
        except:
            return {'uro':None}

    @staticmethod
    def generate(user):
        payload = {
            'uid': user.id,
            'uro': user.role,
            'iat': datetime.utcnow(),
            'exp': datetime.utcnow() + timedelta(days=1)
        }
        return jwt.encode(payload,'secret')

    @staticmethod
    def get_user_id(token):
        return Tokens.valid(token)['uid']


