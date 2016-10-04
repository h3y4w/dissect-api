from flask_restful import Resource
from flask import make_response,request
import boto3
import bugsnag
import json
import os

class Workers(Resource):
    class Spawn (Resource):
        snapshotId='ami-d732f0b7'
        def post(self):
            #try:
            if True:
                FILE=request.get_json()
                string_json=json.dumps(FILE)
                with open('worker_files/run_worker.sh', 'r') as f:
                    UserData=f.read() % (FILE['manager_ip'],string_json)
                instance = ec2.create_instances(ImageId=self.snapshotId,
                                                MinCount=1,
                                                MaxCount=1,
                                                SecurityGroupIds=[
                                                    'sg-b2ba5fcb',
                                                ],
                                                UserData=UserData,
                                                InstanceType='t2.micro',
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

                return {'Success': {'Instance':{'dns':instance.public_dns_name,
                                                'id':instance.id
                                                }
                                    }
                        }
            #except Exception as e:
            else:
                return {'Error': str(e)}
    class DownloadRun(Resource):
            run_file='worker_files/run_worker.sh'
            def get(self):
                try:
                    with open(self.run_file, 'r') as f:
                        data=f.read()
                    return make_response(data,200)

                except Exception as e:
                    return {'Error':str(e)}


    class Active (Resource):

        def instanceError(self, e):
            return {"Success": {'error':str(e)}}

        def get(self, workerid):
            try:
                worker=ec2.Instance(workerid)
                return {'Success': worker.state}
            except Exception as e:
                return self.instanceError(e)


        def delete(self, workerid):
            try:
                worker=ec2.Instance(workerid)
                return {"Success": worker.terminate()['TerminatingInstances'][0]['CurrentState']['Code'] in (32,48)} #32 means terminating, 48 means already terminated
            except Exception as e:
                self.instanceError(e)


        def put(self, workerid):
            try:
                worker=ec2.Instance(workerid)
            except Exception as e:
                return self.instanceError(e)

            else:
                return {"Success": "ADD SOME SHIT EHER"}

    class Status (Resource):
        pass

if __name__ is not "__main__":
    bugsnag.configure(
        api_key=os.environ['bugsnag_key']
    )
    ec2 = boto3.resource('ec2', region_name='us-west-2', aws_access_key_id=os.environ['aws_id'],
                                  aws_secret_access_key=os.environ['aws_key'])

