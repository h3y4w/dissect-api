from flask_restful import Resource, reqparse
from flask import make_response,request
import boto3
import bugsnag
import json

import os
class Workers(Resource):
    class Spawn (Resource):
        snapshotId='ami-d732f0b7'
        def post(self):
            FILE=request.get_json()
            string_json=json.dumps(FILE)
            print string_json
            with open('worker_files/run_worker.sh', 'r') as f:
                UserData=f.read() % ('"API IP"',string_json)
            instance = ec2.create_instances(ImageId=self.snapshotId,
                                            MinCount=1,
                                            MaxCount=1,
                                            SecurityGroupIds=[
                                                'sg-b2ba5fcb',
                                            ],
                                            UserData=UserData,
                                            InstanceTyp='t2.micro',
                                            KeyName='heyaws',
                                            BlockDeviceMappings=[
                                                {
                                                    'DeviceName': '/dev/sdb',
                                                    'Ebs': {
                                                        'VolumeSize': FILE['sizeGB'],
                                                        'DeleteOnTermination': True,
                                                        'VolumeType': 'gp2', #'Iops': 123, NOT SUPPORTED FOR gp2
                                                        'Encrypted': False
                                                    },
                                                },
                                            ]
                                            )[0]

            instance.wait_until_running()
            instance.load()
            dns=instance.public_dns_name

            return {'Success':{'dns':dns}}



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

if __name__ is not "__main__":
    bugsnag.configure(
        api_key=os.environ['bugsnag_key']
    )
    ec2 = boto3.resource('ec2', region_name='us-west-2', aws_access_key_id=os.environ['aws_id'],
                                  aws_secret_access_key=os.environ['aws_key'])

