from flask import Flask, request, make_response
from flask_restful import Resource, Api, reqparse
from distutils.version import StrictVersion
run_file='/home/ubuntu/dissect-api/run.sh'
rsa_file='/home/ubuntu/dissect-api/id_rsa'

class checkVersion (Resource):
    def get(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('version',type=str,help='help')
            args = parser.parse_args()

            with open(run_file) as runFile:
                currentVersion=runFile.readlines()[1]

            return StrictVersion(currentVersion) < StrictVersion(args['version'])

        except Exception as e:
            return {'ERROR':str(e)}

class downloadCurrentVersion(Resource):

    def get(self):
        try:

            with open(run_file, 'r') as runfile:
                data=runfile.read()
            return make_response(data, 200)

        except:
            pass

class downloadRSA(Resource):

    def get(self):
        try:
            with open(rsa_file, 'r') as rsafile:
                data=rsafile.read()
            return make_response(data,200)
        except:
            pass

class currentFileManip (Resource):
    def get(self):
        try:
            pass
            #returns running instances
        except Exception as e:
            return {'ERROR':str(e)}

    def post (self):
        pass
        #add to file

    def put (self):
        pass
        # change

    def delete (self):
        pass
        #deletes currently running scripts


if __name__== "__main__":
    app = Flask(__name__)
    api = Api(app)
    api.add_resource(downloadRSA,'/downloadRSA')
    api.add_resource(downloadCurrentVersion,'/downloadCurrentVersion')
    app.run(debug=True,host="0.0.0.0",port=80)
