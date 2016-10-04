from flask_restful import Resource, abort, request
from flask import make_response
from dissect_auth import Tokens, login_required
import dissect_db
class Users:
    class Register(Resource):
        def post(self):
            params=request.get_json(force=True)
            u = dissect_db.User.create(params)
            {
                'first_name': 'John',
                'last_name': 'Doe',
                'email': 'johndoe@mail.com',
                'password': 'password'
            }
            return {'token': Tokens.generate(u)}

    class Login(Resource):
        def post(self):
            params=request.get_json(force=True)#)
            print params
            u = dissect_db.User.auth(params)
            return {'token': Tokens.generate(u)}

    class hey(Resource):
        @login_required()
        def get(self):
            user_id = Tokens.get_user_id(request.headers['Authorization'])
            return user_id
