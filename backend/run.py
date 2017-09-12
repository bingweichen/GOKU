# -*- coding: UTF-8 -*-
"""
flask main function

Author: Bingwei Chen
Date: 2017.07.20
"""
from datetime import timedelta
import json

from flask import Flask
from flask import jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_jwt_extended import get_jwt_claims
from flask_jwt_extended import jwt_required

from datetime import datetime
from flask import request
from flask import g

from server.database.model import Logs
from server.database.db import database

from server.route import user_route, \
    e_bike_model_route, appointment_route, coupon_route, \
    virtual_card_route, battery_rent_route, store_route, school_route, \
    refund_table_route, report_table_route

from server.manager_route import basic_setting, appointment_setting, \
    battery_setting, support, users_setting

from server.wx import wx_route

app = Flask(__name__, static_url_path='')

CORS(app, supports_credentials=True)

app.register_blueprint(user_route.user_app)
app.register_blueprint(e_bike_model_route.e_bike_model_app)
app.register_blueprint(appointment_route.appointment_app)
app.register_blueprint(virtual_card_route.virtual_card_app)
app.register_blueprint(coupon_route.coupon)
app.register_blueprint(battery_rent_route.battery_rent)
app.register_blueprint(store_route.store_app)
app.register_blueprint(school_route.school_app)
app.register_blueprint(refund_table_route.refund_table)
app.register_blueprint(report_table_route.report_table_app)

app.register_blueprint(basic_setting.basic_setting)
app.register_blueprint(appointment_setting.appointment_setting)
app.register_blueprint(battery_setting.battery_setting)
app.register_blueprint(support.support_app)
app.register_blueprint(users_setting.user_setting)

app.register_blueprint(wx_route.wx_app)

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


# Bearer JWToken

def after_this_request(f):
    if not hasattr(g, 'after_request_callbacks'):
        g.after_request_callbacks = []
    g.after_request_callbacks.append(f)
    return f


def get_request_log():
    # parse args and forms
    values = ''
    if len(request.values) > 0:
        for key in request.values:
            values += key + ': ' + request.values[key] + ', '
    route = '/' + request.base_url.replace(request.host_url, '')
    request_log = {
        'route': route,
        'method': request.method,
    }
    if len(request.get_data()) != 0:
        body = json.loads(request.get_data())
        if "password" in body:
            body.pop("password")
        print("body", body)
        request_log['body'] = body

    if len(values) > 0:
        request_log['values'] = values
    return request_log


def get_response_log(response):
    return {
        'status': response.status,
        # 'response': response.response
    }


@app.before_request
def before_request():
    database.connect()
    start = datetime.utcnow()

    @after_this_request
    def after(response):
        end = datetime.utcnow()
        dur = end - start
        request_log = get_request_log()
        category = request_log['route'].split('/')[1]
        if category != "virtual_card":
            return response

        response_log = get_response_log(response)

        status = response_log['status']
        extra_info = {
            # 'request': request_log,
            # 'response': response_log,
            'duration': str(dur)
        }

        Logs.create(
            start=start,
            end=end,
            request=request_log,
            response=response_log,
            category=category,
            status=status,
            extra_info=extra_info
        )
        return response


@app.after_request
def call_after_request_callbacks(response):
    database.close()
    for callback in getattr(g, 'after_request_callbacks', ()):
        callback(response)
    return response


def main():
    pass


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True, threaded=True)
