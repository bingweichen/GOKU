# -*- coding: UTF-8 -*-
"""
flask main function

Author: Bingwei Chen
Date: 2017.07.20
"""
from flask import Flask
from flask import jsonify
from flask_cors import CORS
from datetime import timedelta

from flask_jwt_extended import JWTManager
from flask_jwt_extended import jwt_required
from flask_jwt_extended import get_jwt_claims

from playhouse.shortcuts import model_to_dict

from server.database.db import database
from server.route import user_route, resource_route,\
    e_bike_model_route, appointment_route

app = Flask(__name__, static_url_path='')

CORS(app, supports_credentials=True)

app.register_blueprint(user_route.user_app)
app.register_blueprint(resource_route.resource_app)
app.register_blueprint(e_bike_model_route.e_bike_model_app)
app.register_blueprint(appointment_route.appointment_app)

app.secret_key = 'super-super-secret'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(days=30)
# Setup the Flask-JWT-Extended extension
jwt = JWTManager(app)
# This method will get whatever object is passed into the
# create_access_token method.


@jwt.user_claims_loader
def add_claims_to_access_token(user):
    # add more claims in the future
    user_json = user
    return {'user': user_json}


# This method will also get whatever object is passed into the
# create_access_token method, and let us define what the identity
# should be for this object
@jwt.user_identity_loader
def user_identity_lookup(user):
    return user["username"]


# This is an example for jwt_required
# Protect a view with jwt_required, which requires a valid access token
# in the request to access.
@app.route('/refresh_token', methods=['GET'])
@jwt_required
def refresh_token():
    # Access the identity of the current user with get_jwt_identity
    # current_user = get_jwt_identity()
    claims = get_jwt_claims()
    return jsonify({'user': claims['user']}), 200


@app.before_request
def before_request():
    database.connect()


@app.after_request
def after_request(response):
    database.close()
    return response


def main():
    pass


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True, threaded=True)
