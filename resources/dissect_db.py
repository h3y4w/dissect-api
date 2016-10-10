from flask_sqlalchemy import SQLAlchemy
from dissect_errors import FileErrors, UserErrors, NodeErrors
from datetime import datetime

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

def remove_from_db(obj):
    db.session.delete(obj)
    db.session.commit()

def to_dict(obj):
    return {o.name: getattr(obj, o.name) for o in obj.__table__.columns}

################################################################################
 ################################ MODEL #######################################
  ############################################################################

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
        u = db.session.query(User).filter_by(email=user_info['email'], password=user_info['password']).first()
        if u is None:
            UserErrors.IncorrectLogin()
        return u

    @staticmethod
    def change_password(user_info):
        u = db.session.query(User).filter_by(email=user_info['email'], password=user_info['password']).first()
        if u is None:
            UserErrors.AccountDoesNotExist()
        u.password = User.__password_hash(user_info['new_password'])
        db.session.commit()

    @staticmethod
    def __password_hash(password):
        return password

class Node(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, primary_key=True)
    parent_id = db.Column(db.Integer)
    type = db.Column(db.String(10)) #folder or file
    file_id = db.Column(db.Integer)
    name = db.Column(db.String(100))
    icon = db.Column(db.String(250))
    favorite = db.Column(db.Boolean, default=False)
    def __init__(node_info):
        pass

    @staticmethod
    def find_by_id(id, user_id):
        node = db.session.query(Node).filter_by(id=id).first()
        if node is not None:
            if node.user_id == user_id:
                return node
            NodeErrors.InsufficientNodePermission()
        NodeErrors.NodeDoesNotExist()

    @staticmethod
    def create(node_info):
        return add_to_db(Node(node_info))

    def delete(self):
        try:
            remove_from_db(self)
        except:
            return False
        return True

    def move(self, parent_id):
        self.parent_id = parent_id
        db.session.commit()

    def rename(self, name):
        self.name = name
        db.session.commit()

    def get_children(self):
        pass

    def favorite(self, active):
        self.favorite = active
        db.session.commit()

    def change_icon(self, icon):
        self.icon = icon
        db.session.commit()

    @staticmethod
    def jstree_format(self, nodes):
        data = []
        for node in nodes:
            if node.parent_id == 0: node.parent_id = '#'
            if node.icon == None: node.icon = "default"
            temp = {
                "id": node.id,
                "parent": node.parent_id,
                "text": node.name,
                "type": node.type,
                "icon": node.icon
            }
            data.append(temp)

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
    def find_by_id(id):
        return db.session.query(FileShare).query.filter_by(id=id).first()

    @staticmethod
    def find_by_file_and_user_id(file_id, user_id):
        return db.session.query(FileShare).filter_by(file_id=file_id, user_id=user_id).first()

class File(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    parts = db.Column(db.Integer)
    size = db.Column(db.Integer)
    name = db.Column(db.String(100))
    def __init__ (self, file_info):
        self.user_id = file_info['user_id']
        self.parts = len(file_info['parts'])
        self.size = file_info['size']
        self.name = file_info['name']

    @staticmethod
    def create(file_info):

        f = add_to_db(File(file_info))
        for part in file_info['parts']:
            FilePart.create(part, f.id)
        return f


    def delete(file_id, user_id):
        pass

    def check_permission(self,user_id):
        permission = 0
        if self.user_id == user_id:
            return 7
        fs = FileShare.find_by_file_and_user_id(self.id, user_id)
        if fs is not None:
            print 'found file share'
            permission = fs.permission
        return permission

    @staticmethod
    def find_by_id(id, user_id):
        f = db.session.query(File).filter_by(id=id).first()
        if f is not None:
            if f.check_permission(user_id)>=4:
                return f
            print f.check_permission(user_id)
            FileErrors.InsufficientFilePermission()
        FileErrors.FileDoesNotExist()

    def get_parts(self):
        return db.session.query(FilePart).filter_by(file_id = self.id).all()

class FilePart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    file_id = db.Column(db.Integer)
    size = db.Column(db.Integer)
    location = db.Column(db.String(20))

    def __init__(self, filepart_info, file_id):
        self.file_id = file_id
        self.location = filepart_info['location']
        self.size = filepart_info['size']

    @staticmethod
    def create(filepart_info, file_id):
        return add_to_db(FilePart(filepart_info, file_id))



class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    start = db.Column(db.DateTime)
    file_id = db.Column(db.Integer)
    user_id = db.Column(db.Integer)
    end = db.Column(db.DateTime)
    stage = db.Column(db.Integer)
    socket = db.Column(db.String(100))
    s3 = db.Column(db.String(150)) #holds location of file in s3
    def __init__(self, task_info):
        self.start = datetime.utcnow()
        self.stage = 0
        self.file_id = task_info['file_id']
        self.user_id = task_info['user_id']
        self.socket = 'SOMETHING' #CREATES QUEUE

#FOR TESTING TO CREATE DB!!!
if __name__ == "__main__":
    print 'Creating Tables'
    db.create_all()
    print 'Saving Tables'
    db.session.commit()

