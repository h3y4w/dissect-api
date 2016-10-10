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
app.config['SQLALCHEMY_DATABASE_URI']='mysql://deno@localhost/dissect'
api = Api(app)
db = SQLAlchemy(app)
from resources.managers import Managers
from resources.workers import Workers
from resources.users import User
from resources.files import File, FileShare
from resources.tasks import Task
from resources.dissect_db import setup_db

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
    api.add_resource(Task, '/task')
    api.add_resource(Task.Tasks, '/task/<int:id>')
    ########################################
    #################USERS##################
    ########################################
    api.add_resource(User.Login,'/user/login')
    api.add_resource(User.Register,'/user/register')
    api.add_resource(User.VirtualDirectory, '/user/vd')

    ########################################
    ##################FILES#################
    ########################################
    api.add_resource(File,'/file')
    api.add_resource(File.Files, '/file/<int:id>')

    api.add_resource(FileShare, '/file/share')
    api.add_resource(FileShare.FileShares, '/file/share/<int:id>')
    ###########################################################
    ##################### Workers ############################
    ###########################################################
    api.add_resource(Workers, '/workers')
    api.add_resource(Workers.Spawn,'/workers/spawn', endpoint='spawnWorker')
    api.add_resource(Workers.DownloadRun, '/workers/download/run', endpoint='runWorker')

    api.add_resource(Workers.Active, '/workers/<string:workerid>/active', endpoint='activeWorker')
    app.run(debug=True,host='0.0.0',port=8080)

