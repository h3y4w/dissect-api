##############################################
#WILL ONLY BE ACCESSED WITH AWS EC2 INSTANCES#
##############################################

####TO DO####
#>Seperate endpoint groups to different file

import bugsnag
import bugsnaginfo
import json
from flask import Flask, make_response
from flask_restful import Resource, Api, reqparse, inputs

from managerAPI import manager
from ManagersAPI import Managers

class downloadCurrentVersion(Resource):

    def get(self):
        try:

            with open(run_file, 'r') as runfile:
                data=runfile.read()
            return make_response(data, 200)

        except:
            pass


if __name__== "__main__":
    bugsnag.configure(
        api_key = bugsnaginfo.key
    )
    app = Flask(__name__)
    api = Api(app)
    api.add_resource(downloadCurrentVersion,'/downloadCurrentVersion')

    ##############################################################
    ###################### Managers ###############################
    ###############################################################
    api.add_resource(Managers,'/managers')
    api.add_resource(Managers.Spawn,'/managers/spawn')
    api.add_resource(Managers.Active,'/managers/active')
    ##################################################################
    ###################### manager ###################################
    ##################################################################
    api.add_resource(manager,'/managers/<int:id>/', endpoint='id')
    api.add_resource(manager.heartbeat,'/managers/<int:id>/heartbeat', endpoint='heartbeat')
    api.add_resource(manager.active,'/managers/<int:id>/active', endpoint='single_active')


    app.run(debug=True,host='localhost',port=5000)
    #app.run(debug=True,host="0.0.0.0",port=80)
