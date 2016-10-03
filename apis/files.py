from flask_sqlalchemy import SQLAlchemy
from flask_restful import Resource, request
from dissect_auth import login_required, Tokens
from dissect_errors import FileErrors
db=SQLAlchemy()
def file_setup(db_):
    global db
    db=db_

class FileTable(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    parts = db.Column(db.Integer)
    size = db.Column(db.Integer)
    name = db.Column(db.String(100))

    def __init__ (self, file_info):
        self.user_id = file_info['user_id']
        self.parts = file_info['parts']
        self.size = file_info['size']
        self.name = file_info['name']

class FilePartTable(db.Model):
            id = db.Column(db.Integer, primary_key=True)
            file_id = db.Column(db.Integer)
            size = db.Column(db.Integer)
            location = db.Column(db.String(20))

class Files(Resource):

    @login_required()
    def post(self):
        params=request.get_json(force=True)
        params['user_id'] = Tokens.get_user_id(request.headers['Authorization'])
        f = Files.FileTable(params)
        db.session.add(f)
        print db.session.commit()
        return f.id
        #upload a new file
        pass

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
            f = FileTable.query.filter_by(id=id).first()
            if f is None:
                FileErrors.FileDoesNotExist()

            if f.user_id == user_id:
                return {
                    'size': f.size,
                    'parts': f.parts,
                    'name': f.name
                }


class FileParts (Resource):
    @login_required()
    def post(self):
        pass

    class FilePart (Resource):
        def get(self):
            pass

