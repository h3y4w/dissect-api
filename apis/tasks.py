from flask_restful import Resource, abort, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import boto3
import os
import json
import inspect
db=SQLAlchemy()
def task_setup(db_):
    global db
    db=db_
session = db.session()
#uploadQueue = boto3.resource('sqs', region_name='us-west-2',
#                             aws_access_key_id=os.environ['aws_key'],
#                             aws_secret_access_key=os.environ['aws_secret']
#)
class Tasks(Resource):
    def get(self):
        all_tasks=Task.query.all()
        TASKS=[]
        for t in all_tasks:
            TASKS.append(t.id)
        return TASKS

    def post(self):
        params = request.get_json(force=True)
        t=Task()
        session.add(t)
        session.commit()
        return t.id

    class task(Resource):
        def get(self, id):
            t=Task.query.filter_by(id=id).first()
            return json.dumps(t.getDict())

        def delete(self, id):
            t=Task.query.filter_by(id=id).first()
            session.delete(t)
            session.commit()
            return {
                'Method':inspect.stack()[0][3],
                'Object':self.__class__.__name__,
                'id': id
            }
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    start = db.Column(db.DateTime)
    end = db.Column(db.DateTime)
    stage = db.Column(db.Integer)
    def __init__(self):
        self.start = datetime.utcnow()
        self.stage = 0

    def getDict(self):
        return {
            'id': self.id,
            'start': str(self.start),
            'end': str(self.end),
            'stage': self.stage
        }
