from flask_sqlalchemy import SQLAlchemy
from dissect_errors import FileErrors, UserErrors


#FOR TESTING TO CREATE DB!!!
if __name__ == "__main__":
    from flask import Flask
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI']='mysql://localhost/dissect'
    db=SQLAlchemy(app)

else:
    db = SQLAlchemy()

def setup_db(_db):
    global db
    db=_db

def add_to_db(obj):
    db.session.add(obj)
    db.session.flush()
    db.session.commit()
    return obj

def to_dict(obj):
    return {o.name: getattr(obj, o.name) for o in obj.__table__.columns}

class User(db.Model):
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
        self.password = User.__password_hash(user_info['password'])
        self.role='regular'

    @staticmethod
    def create(user_info):
        return add_to_db(User(user_info))

    @staticmethod
    def auth(user_info):
        u = User.query.filter_by(email=user_info['email'], password=user_info['password']).first()
        if u is None:
            UserErrors.IncorrectLogin()
        return u

    @staticmethod
    def change_password(user_info):
        u = User.query.filter_by(email=user_info['email'], password=user_info['password']).first()
        if u is None:
            UserErrors.AccountDoesNotExist()
        u.password = User.__password_hash(user_info['new_password'])
        db.session.commit()

    @staticmethod
    def __password_hash(password):
        return password

class FileShare(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    file_id = db.Column(db.Integer)
    user_id = db.Column(db.Integer)
    permission = db.Column(db.Integer) #7=owner, 6=shared user - write and read, 4=shared user - read

    def __init__(self,share_info):
        self.file_id = share_info['file_id']
        self.user_id = share_info['user_id']
        self.permission = share_info['permission']

    @staticmethod
    def create(share_info):
        return add_to_db(FileShare(share_info))

    @staticmethod
    def find_by_file_and_user_id(file_id, user_id):
        return FileShare.query.filter_by(file_id=file_id, user_id=user_id).first()

class File(db.Model):
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

    @staticmethod
    def create(file_info):
        return add_to_db(File(file_info))

    @staticmethod
    def delete(file_id, user_id):
        f = find_by
        pass

    def check_permission(self,user_id):
        permission = 0
        print 'self.user_id {}'.format(self.user_id)
        print 'user_id {}'.format(user_id)
        if self.user_id == user_id:
            return 7
        fs = FileShare.find_by_file_and_user_id(self.id, user_id)
        if fs is not None:
            permission = fs.permission
        return permission

    @staticmethod
    def find_by_id(id, user_id):
        f = File.query.filter_by(id=id).first() #Error is happening here
        if f is not None:
            if f.check_permission(user_id)>=4:
                return f
            print f.check_permission(user_id)
            FileErrors.InsufficientFilePermission()
        FileErrors.FileDoesNotExist()

class FilePart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    file_id = db.Column(db.Integer)
    size = db.Column(db.Integer)
    location = db.Column(db.String(20))


#FOR TESTING TO CREATE DB!!!
if __name__ == "__main__":
    print 'Creating Tables'
    db.create_all()
    print 'Saving Tables'
    db.session.commit()

