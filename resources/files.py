from flask_sqlalchemy import SQLAlchemy
from flask_restful import Resource, request
from dissect_auth import login_required, Tokens
import dissect_db
db=SQLAlchemy()
def file_setup(db_):
    global db
    db=db_


class Files(Resource):

    @login_required()
    def post(self):
        params=request.get_json(force=True)
        params['user_id'] = Tokens.get_user_id(request.headers['Authorization'])

        f = dissect_db.File.create(params)
        return f.id
        #upload a new file

    class File (Resource):
        def delete(self):
            #delete a file
            pass

        def put(self):
            #edit an existing file
            pass

        @login_required()
        def get(self, id):
            user_id = Tokens.get_user_id(request.headers['Authorization'])
            return dissect_db.to_dict(dissect_db.File.find_by_id(id,user_id)) #converts the File object (db.model) to a dict


class FileParts (Resource):
    @login_required()
    def post(self):
        pass

    class FilePart (Resource):
        def get(self):
            pass

