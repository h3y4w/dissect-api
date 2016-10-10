from flask_restful import Resource, request
#uploadQueue = boto3.resource('sqs', region_name='us-west-2',
#                             aws_access_key_id=os.environ['aws_key'],
#                             aws_secret_access_key=os.environ['aws_secret']
#)
class Task(Resource):
    def get(self):
        pass

    def post(self):
        pass

    class Tasks(Resource):
        def get(self, id):
            pass

        def delete(self, id):
            pass
