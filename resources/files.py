from flask_sqlalchemy import SQLAlchemy
from flask_restful import Resource, request
from dissect_auth import login_required, Tokens
import dissect_db
from dissect_errors import FileErrors
db=SQLAlchemy()
def file_setup(db_):
    global db
    db=db_


class Files(Resource):

    @login_required()
    def post(self):

        """
        Example:
            params = {
                "size": 10000,
                "name": "rns.mov",
                "parts": [
                    {
                        "location": "googledrive",
                        "size": 3248
                    }
                    {
                        "location": "dropbox",
                        "size": 3432
                    }
                    {
                        "location": "mediafire",
                        "size":3423
                    }
                ]
            }
        """
        params=request.get_json(force=True)
        params['user_id'] = Tokens.get_user_id(request.headers['Authorization'])

        return dissect_db.File.create(params).id
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
            FILE = {}

            f = dissect_db.File.find_by_id(id,user_id)
            FILE['file'] = dissect_db.to_dict(f)
            FILE['parts'] = [dissect_db.to_dict(part) for part in f.get_parts()]

            return FILE



class FileShares(Resource):

    @login_required()
    def post(self):

        """
        Example:
            Params = {
                "shared_user": {
                    "user_id": 6,
                    "file_id": 3,
                    "permission": 4
                }
            }
        """
        params = request.get_json(force=True)
        params['user_id'] = Tokens.get_user_id(request.headers['Authorization'])
        if params['user_id'] != params['shared_user']['user_id']:
            f = dissect_db.File.find_by_id(params['shared_user']['file_id'], params['user_id'])
            if f is not None:
                if f.check_permission(params['user_id']) == 7:
                    return dissect_db.to_dict(dissect_db.FileShare.create(params['shared_user']))
                FileErrors.InsufficientFilePermission()
        FileErrors.CannotShareFile()

    class FileShare(Resource):
        @login_required()
        def get(self, id):
            return dissect_db.to_dict(dissect_db.FileShare.find_by_id(id))

class FileParts (Resource):
    @login_required()
    def post(self):
        pass

    class FilePart (Resource):
        def get(self):
            pass

