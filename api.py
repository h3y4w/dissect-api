##############################################
#WILL ONLY BE ACCESSED WITH AWS EC2 INSTANCES#
##############################################

####TO DO####
#> create a whole different part of the api for workers
import os
from flask_restful import Api
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import bugsnag
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='mysql://localhost/dissect'
api = Api(app)
db = SQLAlchemy(app)
from resources.managers import Managers
from resources.workers import Workers
from resources.users import Users
from resources.files import Files
from resources.dissect_db import setup_db
#from apis.tasks import Tasks
setup_db(db)


if __name__ == "__main__":
    try:
        bugsnag.configure(
            api_key =os.environ['bugsnag_key']
        )
    except:
        'WORKING OFFLINE - BUGSNAG NOT CONNECTED\n\n\n\n'

    ##############################################################
    ###################### Managers ###############################
    ###############################################################
    api.add_resource(Managers,'/managers')
    api.add_resource(Managers.Spawn,'/managers/spawn')
    api.add_resource(Managers.Active,'/managers/active')
    api.add_resource(Managers.DownloadRun,'/managers/download/run')

    api.add_resource(Managers,'/managers/<int:id>/', endpoint='id')
    api.add_resource(Managers.Heartbeat,'/managers/<int:id>/heartbeat', endpoint='heartbeat')
    api.add_resource(Managers.Active,'/managers/<int:id>/active', endpoint='single_active')

    #######################################
    ##################TASKS################
    #######################################
    #api.add_resource(Tasks, '/tasks')
    #api.add_resource(Tasks.task, '/tasks/<int:id>')
    ########################################
    #################USERS##################
    ########################################
    api.add_resource(Users.Login,'/users/login')
    api.add_resource(Users.hey,'/hey')
    api.add_resource(Users.Register,'/users/register')

    ########################################
    ##################FILES#################
    ########################################
    api.add_resource(Files,'/files')
    api.add_resource(Files.File, '/files/<int:id>')
    ###########################################################
    ##################### Workers ############################
    ###########################################################
    api.add_resource(Workers, '/workers')
    api.add_resource(Workers.Spawn,'/workers/spawn', endpoint='spawnWorker')
    api.add_resource(Workers.DownloadRun, '/workers/download/run', endpoint='runWorker')

    api.add_resource(Workers.Active, '/workers/<string:workerid>/active', endpoint='activeWorker')
    app.run(debug=True,host='localhost',port=int(os.environ['port']))

