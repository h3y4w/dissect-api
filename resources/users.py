from flask_restful import Resource, request
from dissect_auth import Tokens, login_required
import dissect_db

class User:
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


    class VirtualDirectory (Resource):

        @login_required()
        def post(self):
            params = request.get_json(force=True)
            params['user_id'] = Tokens.get_user_id(request.headers['Authorization'])

            return dissect_db.to_dict(dissect_db.Node.create(params))

        @login_required()
        def delete(self, id):
            params = request._get_json(force=True)
            user_id = Tokens.get_user_id(request.headers['Authorization'])

            return dissect_db.Node.find_by_id(params['id'], user_id).delete()

        @login_required()
        def put(self):
            params = request.get_json(force=True)
            user_id = Tokens.get_user_id(request.headers['Authorization'])

            node = dissect_db.Node.find_by_id(params['id'], user_id)
            if params['edit'] == 'rename':
                node.rename(params['data'])
            elif params['edit'] == 'favorite':
                node.favorite(params['data'])


