#PASS PUBLIC IP THROUGH CLASS
#ALSO PASS BUGSNAG CONFIG AS WELL AS BOTO3
from flask_restful import Resource, reqparse
from flask import make_response
import boto3
import boto3conf
import bugsnag
import bugsnaginfo

import os
class Workers(Resource):

    class Spawn (Resource):
        def post(self):
            parser = reqparse.RequestParser()
            parser.add_argument('type',type=str,help='TYPE OF MANAGER - UPLOAD || DOWNLOAD')
            with open('worker_files/run_worker.sh','r') as f:
                UserData=f.read() % os.environ['api_ip'] #Avoided .format() because of bug
            try:
                ec2 = boto3.resource('ec2', region_name='us-west-2', aws_access_key_id=boto3conf.info[0],
                                    aws_secret_access_key=boto3conf.info[1])
                if ec2 is not None:
                    print "Successfully connected to AWS!"
                    return {'Success':{'instance':{'ip':os.environ['api_ip'],'launched':'launch times'
                                                }
                                        }
                            }
                #Before I uncomment the lines, make sure to configure VOLUMESIZE and pass the type of manager to UserData
                #instance = ec2.create_instances(ImageId=self.snapshotId,
                #                                        MinCount=1,
                #                                        MaxCount=1,
                #                                        SecurityGroupIds=[
                #                                            'sg-b2ba5fcb',
                #                                        ],
                #                                        UserData=UserData,
                #                                        InstanceType='t2.micro',
                #                                        KeyName='heyaws',
                #                                        BlockDeviceMappings=[
                #                                            {
                #                                                'DeviceName': '/dev/sdb',
                #                                                'Ebs': {
                #                                                    'VolumeSize': self.FILE['sizeGB'],
                #                                                    'DeleteOnTermination': True,
                #                                                    'VolumeType': 'gp2', #'Iops': 123, NOT SUPPORTED FOR gp2
                #                                                    'Encrypted': False
                #                                                },
                #                                            },
                #                                        ]
                #                                        )[0]
                #CREATES A MANAGER TYPE

                else:
                    e='Could not connect to AWS Server - WorkersAPI.py'
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

    class Active (Resource):
        def get(self):
            #gets whether or not its Active
            pass

        def delete(self):
            #deletes a worker
            pass

        def put(self):
            #change activeness
            pass

    class DownloadRun(Resource):
            run_file='worker_files/run_worker.sh'
            def get(self):
                try:
                    with open(self.run_file, 'r') as f:
                        data=f.read()
                    return make_response(data,200)

                except Exception as e:
                    return {'Error':str(e)}

bugsnag.configure(
    api_key=os.environ['bugsnag_key']
)
