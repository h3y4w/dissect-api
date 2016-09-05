from flask_restful import Resource,reqparse
import bugsnag
import bugsnaginfo

class manager(Resource):
    def get(self,id):
        pass
        # will return basic info of manager instance - when created, what type,etc

    #********************** Heartbeat *******************#
    class heartbeat(Resource):
        def post(self,id):
            r={}
            try:
                print 'PING FROM MANAGER {}'.format(id)
                #MAKE SURE HEARTBEAT SHOWS ITS RUNNING
                #ALL IF API GOES DOWN FORWHATEVER REASON, IT WILL GET ALL RUNNNG SERVICES
                #Input LAST_PING: (current time)  into DB, json or whatever
                r['Success']={'LAST_PING':'CURRENT TIME 9:44'}
                return r
            except Exception as e:
                bugsnag.notify(
                    Exception(str(e)),
                    context="POST Request manager.heartbeat"
                )
                r['Error']=str(e)
                return r


    #********************** active **********************#
    class active(Resource):
        def put(self,id):
            parser = reqparse.RequestParser()
            parser.add_argument('mode',type=int,help='TRUE || FALSE')
            args = parser.parse_args()
            print "Changing MANAGER {} active to: {}".format(id, bool(args['mode']))

        def get(self,id):
            # CHECKS DB JSON OR SOME SHIT
            print "MANAGER {} is active: {}".format(id, 'TRUE (CHANGE WHEN DB IS INTEGRATED)')

        def delete(self,id):
            try:
                # DESTROYS MANAGER AFTER FINISHING CURRENT REQUESTS
                print "DELETING MANAGER {}!".format(id)
                return {'Success':{'Request':'DELETE'}}

            except Exception as e:
                print "ERROR: {}".format(e)
                bugsnag.notify(
                    e,
                    context='DELETE REQUEST in manager.active - managerAPI.py'
                )
                return {'Error':{'Request':'DELETE'}}

bugsnag.configure(
    api_key=bugsnaginfo.key
)
