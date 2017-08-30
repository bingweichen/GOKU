"""

"""
from functools import wraps
from flask import make_response
from flask import request
import jwt
from flask_jwt_extended import get_jwt_identity

from server.service import user_service


def authenticate():
    """Sends a 401 response that enables basic auth"""
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


def check_admin_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        username = get_jwt_identity()
        user = user_service.get(username=username)
        if not user.admin:
            return authenticate()
        func = f(*args, **kwargs)
        return func
    return decorated


def check_admin(username):
    user = user_service.get(username=username)
    return user.admin
