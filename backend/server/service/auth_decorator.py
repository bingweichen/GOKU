"""

"""
from functools import wraps
from flask import make_response
from flask import request
import jwt


def authenticate():
    """Sends a 401 response that enables basic auth"""
    # TODO can't use 'jsonify', need to research for the reason
    return make_response('Could not verify your access level for that URL.\n'
                         'You have to login with proper credentials', 401)


def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        result = token_verify()
        if not result:
            return authenticate()
        return f(*args, **kwargs)

    return decorated


def token_verify():
    token = request.headers.get('Authorization')
    if not token:
        return False
    data = jwt.decode(token, 'super-super-secret', algorithms=['HS256'])
    return data

