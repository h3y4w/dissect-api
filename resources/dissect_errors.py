from flask import abort#, response
class UserErrors:

    @staticmethod
    def AccountDoesNotExist():
        error = {
            'Status Code': '404',
            'Error': {
                'Type': '',
                'Message': 'Account is not found'
            }
        }
        abort(404, error)
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


class NodeErrors:

    @staticmethod
    def NodeDoesNotExist():
        error = {
            'Status Code': '404',
            'Error': {
                'Type': '',
                'Message': 'Node is not found'
            }
        }
        abort(404, error)

    @staticmethod
    def InsufficientNodePermission():
        error = {
            'Status Code': '401',
            'Error': {
                'Type': '',
                'Message': 'Insufficient Permissions'
            }
        }
        abort(401, error)

class FileErrors:

    @staticmethod
    def CannotShareFile():
        error = {
            'Status Code': '400',
            'Error': {
                'Type': 'Runtime error',
                'Message': 'Cannot Share File'
            }
        }
        abort(400, error)
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

    @staticmethod
    def InsufficientFilePermission():
        error = {
            'Status Code': '401',
            'Error': {
                'Type': '',
                'Message': 'Insufficient Permissions'
            }
        }
        abort(401, error)
class Clouds:
    pass

