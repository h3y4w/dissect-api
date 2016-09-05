from flask_restful import Resource, reqparse, inputs
from flask import make_response
import json
import bugsnag
import boto3
import boto3conf
import os

class Managers(Resource):
    def get(self,id):
        try:
                ## LOOK INTO XML JSON OR DB STORAGE METHODS!!!
            with open('managerInfo','r') as f:

                mDict = json.loads(f.read())
            return mDict['active']

        except Exception as e:
            bugsnag.notify(
                Exception(str(e)),
                context="GET Request for Managers, backend API",
            )
    def post(self,id):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('active',type=inputs.boolean,help='is active')
            args = parser.parse_args()

            with open('managerInfo', 'r') as f:
                data = json.loads(f.read())

            data['active']=args['active']
            with open('manager', 'w') as f:
                f.write(json.dumps(data))
            return {'Success': 'OK'}

        except Exception as e:
            bugsnag.notify(
                Exception(str(e)),
                context="POST Request for Managers, backend API"
            )
            return False


    class Active(Resource):
        def put(self):
            parser = reqparse.RequestParser()
            parser.add_argument('mode',type=int,help='TRUE || FALSE')
            args = parser.parse_args()
            print "Changing ALL MANAGERS active to: {}".format(bool(args['mode']))

        def get(self):
            # CHECKS DB JSON OR SOME SHIT
            print "ALL MANAGERS are active: {}".format('TRUE (CHANGE WHEN DB IS INTEGRATED)')

        def delete(self):
            try:
                # DESTROYS ALL MANAGERS AFTER FINISHING CURRENT REQUESTS
                print "DELETING ALL MANAGERS !"
                return {'Success':{'Request':'DELETE'}}

            except Exception as e:
                print "ERROR: {}".format(e)
                bugsnag.notify(
                    e,
                    context='DELETE REQUEST in Managers.Active - ManagersAPI.py'
                )
                return {'Error':{'Request':'DELETE'}}






    #***************** Spawn ******************#
    class Spawn(Resource):
        def post(self):
            parser = reqparse.RequestParser()
            parser.add_argument('type',type=str,help='TYPE OF MANAGER - UPLOAD || DOWNLOAD')
            args = parser.parse_args()
            with open('manager_files/run_manager.sh','r') as f:
                UserData=f.read() % (os.environ['api_ip'],args['type']) #Avoided .format() because of bug

            try:
                ec2 = boto3.resource('ec2', region_name='us-west-2', aws_access_key_id=boto3conf.info[0],
                                    aws_secret_access_key=boto3conf.info[1])
                if ec2 is not None:
                    print "Successfully connected to AWS!"

                    instance = ec2.create_instances(ImageId=self.snapshotId,
                                                        MinCount=1,
                                                        MaxCount=1,
                                                        SecurityGroupIds=[
                                                            'sg-b2ba5fcb',
                                                        ],
                                                        UserData=UserData,
                                                        InstanceType='t2.micro',
                                                        KeyName='heyaws'
                                                        )[0]

                    return {'Success':{'instance':{'ip':os.environ['api_ip'],'launched':'launch times'}}}

                else:
                    e='Could not connect to AWS Server - ManagersAPI.py'
                    bugsnag.notify(
                        Exception(e),
                        context='add context here'
                    )
                    return {'Error':e}

            except Exception as e:
                bugsnag.notify(
                    e,
                    context='POST Request in Managers.Spawn - ManagersAPI.py'
                )
                return {'Error':str(e)}

    class DownloadRun(Resource):
        run_file='manager_files/run_manager.sh'
        def get(self):
            try:
                with open(self.run_file, 'r') as f:
                    data=f.read()
                return make_response(data, 200)

            except Exception as e:
                return {'Error': str(e)}

bugsnag.configure(
    api_key=os.environ['bugsnag_key']
)
