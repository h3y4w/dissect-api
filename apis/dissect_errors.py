from flask import abort#, response
class UserErrors:

    @staticmethod
    def IncorrectLogin():
        error = {
            'Status Code': '401',
            'Error': {
                'Type': 'Authentication',
                'Message': 'Incorrect Login'
            }
        }
        abort(401, error)
    @staticmethod
    def ExpiredToken():
        error = {

            'Status Code': '401',
            'Error': {
                'Type': 'Authentication',
                'Message': 'Expired Token'
                }
            }
        abort(401, error)

    @staticmethod
    def IncorrectRole():
        error = {
            'Status Code': '401',
            'Error': {
                'Type': 'Permissions',
                'Message': 'Do not have correct role'
            }
        }
        abort(401, error)

class Files:
    @staticmethod
    def FileDoesNotExist():
        error = {
            'Status Code': '404',
            'Error': {
                'Type': '',
                'Message': 'File is not found'
            }
        }
        abort(404, error)

class Clouds:
    pass

