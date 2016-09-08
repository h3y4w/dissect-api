##############################################
#WILL ONLY BE ACCESSED WITH AWS EC2 INSTANCES#
##############################################

####TO DO####
#> create a whole different part of the api for workers
import os

import bugsnag
import json
from flask import Flask
from flask_restful import Resource, Api, reqparse, inputs
from managerAPI import manager
from ManagersAPI import Managers
from WorkersAPI_ import Workers


if __name__== "__main__":
    app = Flask(__name__)
    api = Api(app)
    bugsnag.configure(
        api_key =os.environ['bugsnag_key']
    )


    ##############################################################
    ###################### Managers ###############################
    ###############################################################
    api.add_resource(Managers,'/managers')
    api.add_resource(Managers.Spawn,'/managers/spawn')
    api.add_resource(Managers.Active,'/managers/active')
    api.add_resource(Managers.DownloadRun,'/managers/download/run')
    ##################################################################
    ###################### manager ###################################
    ##################################################################
    api.add_resource(manager,'/managers/<int:id>/', endpoint='id')
    api.add_resource(manager.heartbeat,'/managers/<int:id>/heartbeat', endpoint='heartbeat')
    api.add_resource(manager.active,'/managers/<int:id>/active', endpoint='single_active')



    ###########################################################
    ##################### Workers ############################
    ###########################################################
    api.add_resource(Workers, '/workers')
    api.add_resource(Workers.Spawn,'/workers/spawn', endpoint='spawnWorker')
    api.add_resource(Workers.Active, '/workers/<string:workerid>/active', endpoint='activeWorker')
    api.add_resource(Workers.DownloadRun, '/workers/download/run', endpoint='runWorker')

    #############################################################
    ########################## worker ###########################
    #############################################################
    #JSAJDJSA KDJ ADK

    app.run(debug=True,host='localhost',port=int(os.environ['port']))
    #pp.run(debug=True,host="0.0.0.0",port=80)
